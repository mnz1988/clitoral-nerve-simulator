"""Quasi-static volume-conductor solve with FEniCSx (dolfinx 0.9).

Units: SI throughout. Lengths m, conductivity S/m, current A, potential V,
current density A/m2.

Equation: div(sigma grad V) = 0 in the tissue, sigma piecewise constant per layer.

Boundary conditions (n is the outward normal of the tissue; on the skin n = +z):
- Contact j (current-controlled): sigma dV/dn = +I_j / A_j on the contact, i.e. the normal
  current density -sigma dV/dn is I_j / A_j flowing inward, so the total current I_j enters
  the tissue spread uniformly over the contact (uniform current density, not an equipotential
  electrode). A_j is the meshed area of contact j itself, so exactly I_j is injected.
  Positive I_j is current into the tissue (anode). A contact with I_j = 0 is insulating.
- Rest of the skin surface: insulating (sigma dV/dn = 0).
- Far boundary (hemisphere of radius R centred on the origin), two choices:
  "robin" (default): dV/dn = -V / R. This is exact for the monopole field c / r of a source
  at the origin, so it acts as a first-order absorbing far boundary and pins V -> 0 at
  infinity; it also fixes the potential gauge, so the problem is well posed even when the
  contact currents sum to zero. It is approximate for sources away from the origin and for
  the dipole part of the field; its computed effect is in tests/test_solver.py.
  "dirichlet": V = 0 on the far boundary, which shifts V by about -I / (2 pi sigma R).

Discretisation: Lagrange elements (degree 2 by default) on the Gmsh tetrahedral mesh. Linear
solver: CG with hypre BoomerAMG, relative residual tolerance 1e-12 by default ("cg-amg"), or
MUMPS LU ("direct").

Guards (both thresholds are assumptions set in step 3.1, see tests/test_solver.py):
- Meshed contact area: if the meshed area of any contact differs from its geometric area by
  more than `max_area_error` (default 2 %), the constructor raises ValueError. The injected
  current stays exact, but the current density on that contact would be off by that much.
- Conductive layers: a layer of thickness h and conductivity s1 over a layer s2 < s1 spreads
  the current sideways over about L = h s1 / s2. When L reaches past the refined region
  (the near-contact zone, or a RefineBox that spans the layer depth with size <= h), the
  constructor issues UnderResolvedLayerWarning. Computed in step 3.1: a 10 um layer 1000x more
  conductive than the one below (L = 10 mm) is 2 to 7 % off (3.9 to 4.4 % in the fix pass)
  and a 0.2 mm layer 100x more conductive (L = 20 mm) 2.2 to 2.3 % off, both above the 2 %
  target. A RefineBox out to L (2 to 21 mm wide, size h) was not honoured by Gmsh, so
  build_mesh refuses it. These cases are outside the verified range (known limit, kept in
  tests/test_solver.py). The warning is conservative: a 20 um layer 100x more conductive
  under a 0.1 mm disc (L = 2 mm) stayed within 0.5 % unrefined, yet it warns.
"""

from __future__ import annotations

import warnings
from collections.abc import Sequence

import numpy as np
import ufl
from dolfinx import fem, geometry
from dolfinx.fem import petsc as fem_petsc
from petsc4py import PETSc

from .geometry import CONTACT_TAG0, FAR_TAG, HalfSpaceMesh

FAR_BOUNDARIES = ("robin", "dirichlet")
LINEAR_SOLVERS = ("cg-amg", "direct")
MAX_AREA_ERROR = 0.02  # assumption: equal to the step 3.1 potential target


class UnderResolvedLayerWarning(UserWarning):
    """A conductive layer spreads current beyond the refined part of the mesh."""


def layer_spreading_check(model, sizing, sigma) -> list[str]:
    """Problems with conductive layers whose spreading length leaves the refined region.

    For layer i (thickness h, conductivity s_i) over layer i + 1, L = h s_i / s_(i+1). The
    refined region reaches E + near_distance from the origin, E being the largest contact
    extent, or further where a RefineBox spans the whole layer depth with size <= h (its
    smallest half-width about the origin counts). A message is returned when E + L is beyond
    that reach. The criterion is an assumption set in step 3.1.
    """
    reach_contacts = max(c.extent for c in model.contacts)
    tol = 1e-9 * model.radius
    problems = []
    z_top = 0.0
    for i, h in enumerate(model.layer_thicknesses):
        z_bot = z_top - h
        spread = h * sigma[i] / sigma[i + 1]
        reach = reach_contacts + sizing.near_distance
        for b in sizing.boxes:
            if b.zmax >= z_top - tol and b.zmin <= z_bot + tol and b.size <= h * (1 + 1e-9):
                reach = max(reach, min(-b.xmin, b.xmax, -b.ymin, b.ymax))
        if reach_contacts + spread > reach * (1 + 1e-9):
            problems.append(
                f"layer {i}: spreading length h s{i}/s{i + 1} = {spread * 1e3:.3g} mm reaches "
                f"{(reach_contacts + spread) * 1e3:.3g} mm from the origin, but the mesh is "
                f"refined only to {reach * 1e3:.3g} mm (add a RefineBox over the layer, "
                f"size <= h, out to that distance)"
            )
        z_top = z_bot
    return problems


class VolumeConductor:
    """Assembled system for one mesh, one set of layer conductivities and one far boundary.

    The matrix and one right-hand side per contact (for 1 A) are assembled once; `solve`
    combines them for any set of contact currents.
    """

    def __init__(
        self,
        hs: HalfSpaceMesh,
        sigma: Sequence[float],
        degree: int = 2,
        far_boundary: str = "robin",
        rtol: float = 1e-12,
        linear_solver: str = "cg-amg",
        amg_options: dict[str, object] | None = None,
        max_area_error: float | None = MAX_AREA_ERROR,
    ) -> None:
        if far_boundary not in FAR_BOUNDARIES:
            raise ValueError(f"far_boundary must be one of {FAR_BOUNDARIES}")
        if linear_solver not in LINEAR_SOLVERS:
            raise ValueError(f"linear_solver must be one of {LINEAR_SOLVERS}")
        if len(sigma) != hs.model.n_layers:
            raise ValueError(f"need {hs.model.n_layers} conductivities, got {len(sigma)}")
        if any(not s > 0 for s in sigma):
            raise ValueError("conductivities must be positive (S/m)")
        for problem in layer_spreading_check(hs.model, hs.sizing, sigma):
            warnings.warn(problem, UnderResolvedLayerWarning, stacklevel=2)
        self.hs = hs
        self.far_boundary = far_boundary
        mesh = hs.mesh
        self.mesh = mesh
        self.space = fem.functionspace(mesh, ("Lagrange", degree))

        # Piecewise-constant conductivity from the layer cell tags.
        self.sigma = fem.Function(fem.functionspace(mesh, ("DG", 0)))
        self.sigma.x.array[:] = np.nan
        for i, s in enumerate(sigma):
            self.sigma.x.array[hs.cell_tags.find(i + 1)] = s
        n_owned = mesh.topology.index_map(mesh.topology.dim).size_local
        if np.isnan(self.sigma.x.array[:n_owned]).any():
            raise RuntimeError("some cells have no layer tag")
        self.sigma.x.scatter_forward()

        u, w = ufl.TrialFunction(self.space), ufl.TestFunction(self.space)
        self._ds = ufl.Measure("ds", domain=mesh, subdomain_data=hs.facet_tags)
        R = hs.model.radius
        a = self.sigma * ufl.inner(ufl.grad(u), ufl.grad(w)) * ufl.dx
        self._bcs = []
        if far_boundary == "robin":
            a = a + self.sigma * u * w / R * self._ds(FAR_TAG)
        else:
            mesh.topology.create_connectivity(mesh.topology.dim - 1, mesh.topology.dim)
            dofs = fem.locate_dofs_topological(
                self.space, mesh.topology.dim - 1, hs.facet_tags.find(FAR_TAG)
            )
            self._bcs = [fem.dirichletbc(PETSc.ScalarType(0.0), dofs, self.space)]
        self._a = fem.form(a)
        self._A = fem_petsc.assemble_matrix(self._a, bcs=self._bcs)
        self._A.assemble()

        # Unit-current right-hand sides: uniform flux 1 A / (meshed area of this contact).
        self.contact_areas = []
        self._unit_rhs = []
        for j, contact in enumerate(hs.model.contacts):
            tag = CONTACT_TAG0 + j
            area = self._integrate(1.0 * self._ds(tag))
            if not area > 0:
                raise RuntimeError(f"contact {j} has no facets in the mesh")
            area_error = area / contact.area - 1
            if max_area_error is not None and abs(area_error) > max_area_error:
                raise ValueError(
                    f"contact {j}: meshed area differs from the geometric area by "
                    f"{100 * area_error:.2f} % (limit {100 * max_area_error:g} %); "
                    "use a smaller near-contact element size"
                )
            self.contact_areas.append(area)
            b = fem_petsc.assemble_vector(fem.form((1.0 / area) * w * self._ds(tag)))
            b.ghostUpdate(addv=PETSc.InsertMode.ADD, mode=PETSc.ScatterMode.REVERSE)
            fem_petsc.set_bc(b, self._bcs)
            self._unit_rhs.append(b)

        self._ksp = PETSc.KSP().create(mesh.comm)
        self._ksp.setOperators(self._A)
        prefix = f"vc{id(self)}_"
        self._ksp.setOptionsPrefix(prefix)
        opts = PETSc.Options()
        for key, value in (amg_options or {}).items():
            opts[prefix + key] = value
        if linear_solver == "cg-amg":
            self._ksp.setType("cg")
            self._ksp.getPC().setType("hypre")
            self._ksp.getPC().setHYPREType("boomeramg")
            self._ksp.setTolerances(rtol=rtol, atol=0.0, max_it=2000)
            self._ksp.setFromOptions()
            self._ksp.getPC().setFromOptions()
        else:
            self._ksp.setType("preonly")
            self._ksp.getPC().setType("lu")
            self._ksp.getPC().setFactorSolverType("mumps")
        self.last_iterations = 0
        self._tree = None

    def _integrate(self, form) -> float:
        local = fem.assemble_scalar(fem.form(form))
        return self.mesh.comm.allreduce(local)

    def solve(self, currents: Sequence[float]) -> fem.Function:
        """Potential (V) for contact currents `currents` (A, positive into the tissue)."""
        n = len(self._unit_rhs)
        if len(currents) != n:
            raise ValueError(f"need {n} contact currents, got {len(currents)}")
        b = self._unit_rhs[0].duplicate()
        b.set(0.0)
        for current, unit in zip(currents, self._unit_rhs, strict=True):
            b.axpy(float(current), unit)
        V = fem.Function(self.space)
        self._ksp.solve(b, V.x.petsc_vec)
        reason = self._ksp.getConvergedReason()
        if reason <= 0:
            raise RuntimeError(f"linear solver did not converge (PETSc reason {reason})")
        self.last_iterations = self._ksp.getIterationNumber()
        V.x.scatter_forward()
        b.destroy()
        return V

    def injected_current(self, currents: Sequence[float]) -> list[float]:
        """Current (A) the assembled right-hand side puts through each contact.

        The Lagrange basis sums to 1, so the sum of the entries of a contact's right-hand side
        is the discrete integral of its flux over the contact, as it enters the solve.
        """
        if len(currents) != len(self._unit_rhs):
            raise ValueError(f"need {len(self._unit_rhs)} contact currents, got {len(currents)}")
        return [float(i) * b.sum() for i, b in zip(currents, self._unit_rhs, strict=True)]

    def contact_current(self, V: fem.Function, j: int) -> float:
        """Current (A) into the tissue through contact j, recovered from the solution V.

        Consistent boundary flux: with chi = 1 at the dofs of contact j and 0 elsewhere,
        a(V, chi) equals the Neumann flux through contact j (chi vanishes on the far boundary
        and the rest of the surface is insulating). It does not use the stored contact areas.
        """
        fdim = self.mesh.topology.dim - 1
        self.mesh.topology.create_connectivity(fdim, self.mesh.topology.dim)
        dofs = fem.locate_dofs_topological(
            self.space, fdim, self.hs.facet_tags.find(CONTACT_TAG0 + j)
        )
        chi = fem.Function(self.space)
        chi.x.array[dofs] = 1.0
        chi.x.scatter_forward()
        form = self.sigma * ufl.inner(ufl.grad(V), ufl.grad(chi)) * ufl.dx
        if self.far_boundary == "robin":
            form = form + self.sigma * V * chi / self.hs.model.radius * self._ds(FAR_TAG)
        return self._integrate(form)

    def far_current(self, V: fem.Function) -> float:
        """Current (A) leaving through the far boundary, from the discrete weak form.

        Robin: integral of sigma V / R over the far boundary. Dirichlet: the consistent
        boundary flux -integral(sigma grad V . grad chi), chi = 1 at the far-boundary nodes.
        """
        if self.far_boundary == "robin":
            return self._integrate(self.sigma * V / self.hs.model.radius * self._ds(FAR_TAG))
        chi = fem.Function(self.space)
        chi.x.array[self._bcs[0].dof_indices()[0]] = 1.0
        chi.x.scatter_forward()
        return -self._integrate(self.sigma * ufl.inner(ufl.grad(V), ufl.grad(chi)) * ufl.dx)

    def evaluate(self, V: fem.Function, points: np.ndarray) -> np.ndarray:
        """V at `points` (N x 3, m). Serial use; raises if a point is outside the mesh."""
        pts = np.ascontiguousarray(np.atleast_2d(points), dtype=np.float64)
        if self._tree is None:
            self._tree = geometry.bb_tree(self.mesh, self.mesh.topology.dim)
        candidates = geometry.compute_collisions_points(self._tree, pts)
        colliding = geometry.compute_colliding_cells(self.mesh, candidates, pts)
        cells = np.empty(len(pts), dtype=np.int32)
        for i in range(len(pts)):
            links = colliding.links(i)
            if len(links) == 0:
                raise ValueError(f"point {pts[i]} is not inside the mesh")
            cells[i] = links[0]
        return V.eval(pts, cells)[:, 0]
