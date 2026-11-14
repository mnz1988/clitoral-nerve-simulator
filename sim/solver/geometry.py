"""Gmsh model of a layered, truncated half-space with flat contacts on its surface.

Units: SI throughout (metre). The tissue occupies z <= 0; the skin surface is the plane z = 0
and depth is -z. Layers are flat slabs stacked from the surface down; the last layer is the
remaining half-space. The half-space is truncated by a hemisphere of radius R centred on the
origin (the far boundary). Contacts are flat surfaces cut into the plane z = 0, so each one is
a separately tagged part of the boundary.

The mesh is built in memory and handed to dolfinx; no mesh file is written (rule 7).

This module builds our own mesh (A-010); it does not use NRV's mesher.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from mpi4py import MPI

# Facet tags. Layer i (0 = top) has cell tag i + 1.
FAR_TAG = 1
SURFACE_TAG = 2  # insulating part of the skin surface
CONTACT_TAG0 = 100  # contact j has facet tag CONTACT_TAG0 + j

SHAPES = ("disc", "ring", "rectangle")


@dataclass(frozen=True)
class SurfaceContact:
    """A flat contact on the plane z = 0. Lengths in metres.

    disc: `radius`; ring: `radius` (outer) and `inner_radius`; rectangle: `length` along x and
    `width` along y. `centre` is (x, y).
    """

    shape: str
    centre: tuple[float, float] = (0.0, 0.0)
    radius: float = 0.0
    inner_radius: float = 0.0
    length: float = 0.0
    width: float = 0.0

    def __post_init__(self) -> None:
        if self.shape not in SHAPES:
            raise ValueError(f"contact shape {self.shape!r} is not one of {SHAPES}")
        if self.shape in ("disc", "ring") and not self.radius > 0:
            raise ValueError(f"a {self.shape} contact needs radius > 0")
        if self.shape == "ring" and not 0 < self.inner_radius < self.radius:
            raise ValueError("a ring contact needs 0 < inner_radius < radius")
        if self.shape == "rectangle" and not (self.length > 0 and self.width > 0):
            raise ValueError("a rectangle contact needs length > 0 and width > 0")

    @property
    def area(self) -> float:
        """Geometric area (m2). The solver uses the meshed area instead."""
        if self.shape == "disc":
            return math.pi * self.radius**2
        if self.shape == "ring":
            return math.pi * (self.radius**2 - self.inner_radius**2)
        return self.length * self.width

    @property
    def feature_size(self) -> float:
        """Smallest length that sets the field scale near the contact (m).

        disc: radius; ring: the smaller of the inner radius and the ring width; rectangle: half
        the shorter side. The near-contact element size is scaled by it (see MeshSizing).
        """
        if self.shape == "disc":
            return self.radius
        if self.shape == "ring":
            return min(self.inner_radius, self.radius - self.inner_radius)
        return min(self.length, self.width) / 2

    @property
    def extent(self) -> float:
        """Largest distance from the origin to a point of the contact (m)."""
        cx, cy = self.centre
        if self.shape == "rectangle":
            half = math.hypot(self.length / 2, self.width / 2)
        else:
            half = self.radius
        return math.hypot(cx, cy) + half


@dataclass(frozen=True)
class RefineBox:
    """Axis-aligned box (m) inside which the element size is at most `size` (m)."""

    xmin: float
    xmax: float
    ymin: float
    ymax: float
    zmin: float
    zmax: float
    size: float


@dataclass(frozen=True)
class MeshSizing:
    """Element size control (all in metres except `growth`, which is dimensionless).

    Per contact: `near` and `near_distance` apply to the contact with the largest
    `feature_size`; contact j gets both multiplied by feature_size_j / largest feature_size,
    so every contact has the same number of elements across it (with near = a/8 for the
    largest disc, a disc of radius a_j gets a_j/8). Within that distance of the contact the size
    is the contact's near size, then it grows linearly with the distance at `growth` metres of
    size per metre of distance, up to `far`. Boxes can force smaller sizes, for example inside
    a thin layer or along an evaluation line.
    """

    near: float
    far: float
    near_distance: float
    growth: float
    boxes: tuple[RefineBox, ...] = ()

    def scaled(self, factor: float) -> MeshSizing:
        """Every size multiplied by `factor` (factor 0.5 halves h everywhere)."""
        return replace(
            self,
            near=self.near * factor,
            far=self.far * factor,
            growth=self.growth * factor,
            boxes=tuple(replace(b, size=b.size * factor) for b in self.boxes),
        )

    def _contact_scales(self, contacts) -> list[float]:
        sizes = [c.feature_size for c in contacts]
        return [s / max(sizes) for s in sizes]

    def near_sizes(self, contacts) -> list[float]:
        """Near-contact element size (m) of each contact."""
        return [self.near * f for f in self._contact_scales(contacts)]

    def near_distances(self, contacts) -> list[float]:
        """Distance (m) from each contact within which its near size applies."""
        return [self.near_distance * f for f in self._contact_scales(contacts)]


@dataclass(frozen=True)
class HalfSpaceModel:
    """Geometry: contacts, layer thicknesses (top to bottom, m) and truncation radius R (m).

    `layer_thicknesses` lists every layer except the last, which fills the rest of the
    hemisphere. An empty tuple means a homogeneous half-space.
    """

    contacts: tuple[SurfaceContact, ...]
    layer_thicknesses: tuple[float, ...] = ()
    radius: float = 0.1

    def __post_init__(self) -> None:
        if not self.contacts:
            raise ValueError("at least one contact is needed")
        if any(t <= 0 for t in self.layer_thicknesses):
            raise ValueError("layer thicknesses must be positive")
        if sum(self.layer_thicknesses) >= self.radius / 2:
            raise ValueError("layers must end well inside the truncation radius")
        for c in self.contacts:
            # The far-boundary condition assumes sources near the centre (see fem.py).
            if c.extent > self.radius / 4:
                raise ValueError("contacts must lie within R/4 of the origin")

    @property
    def n_layers(self) -> int:
        return len(self.layer_thicknesses) + 1


@dataclass
class HalfSpaceMesh:
    """dolfinx mesh with cell tags (layer i -> i + 1) and facet tags (see module constants)."""

    model: HalfSpaceModel
    sizing: MeshSizing
    mesh: object
    cell_tags: object
    facet_tags: object

    @property
    def n_cells(self) -> int:
        imap = self.mesh.topology.index_map(self.mesh.topology.dim)
        return imap.size_global


def _contact_surface(occ, c: SurfaceContact) -> int:
    cx, cy = c.centre
    if c.shape == "disc":
        return occ.addDisk(cx, cy, 0.0, c.radius, c.radius)
    if c.shape == "rectangle":
        return occ.addRectangle(cx - c.length / 2, cy - c.width / 2, 0.0, c.length, c.width)
    outer = occ.addDisk(cx, cy, 0.0, c.radius, c.radius)
    inner = occ.addDisk(cx, cy, 0.0, c.inner_radius, c.inner_radius)
    out, _ = occ.cut([(2, outer)], [(2, inner)])
    return out[0][1]


def _build_gmsh_model(gmsh, model: HalfSpaceModel, sizing: MeshSizing) -> None:
    occ = gmsh.model.occ
    R = model.radius
    tops = [0.0]
    for t in model.layer_thicknesses:
        tops.append(tops[-1] - t)
    bottoms = tops[1:] + [-R]

    layer_vols = []
    for ztop, zbot in zip(tops, bottoms, strict=True):
        sphere = occ.addSphere(0.0, 0.0, 0.0, R)
        box = occ.addBox(-R, -R, zbot, 2 * R, 2 * R, ztop - zbot)
        out, _ = occ.intersect([(3, sphere)], [(3, box)])
        layer_vols.append(out)
    tools = [(2, _contact_surface(occ, c)) for c in model.contacts]

    objects = [v for vols in layer_vols for v in vols]
    _, out_map = occ.fragment(objects, tools)
    occ.synchronize()

    n_obj = len(objects)
    k = 0
    all_vols = []
    for i, vols in enumerate(layer_vols):
        tags = []
        for _ in vols:
            tags += [e[1] for e in out_map[k] if e[0] == 3]
            k += 1
        gmsh.model.addPhysicalGroup(3, tags, tag=i + 1)
        all_vols += tags

    contact_surfs = []
    surfs_per_contact = []
    for j in range(len(model.contacts)):
        surfs = [e[1] for e in out_map[n_obj + j] if e[0] == 2]
        if not surfs:
            raise RuntimeError(f"contact {j} was lost when cutting it into the surface")
        gmsh.model.addPhysicalGroup(2, surfs, tag=CONTACT_TAG0 + j)
        contact_surfs += surfs
        surfs_per_contact.append(surfs)

    boundary = gmsh.model.getBoundary([(3, v) for v in all_vols], combined=True, oriented=False)
    # Outer surfaces are either the plane z = 0 or patches of the sphere. (Bounding boxes are
    # padded by the OCC tolerance, so the surface type is used instead.)
    far, top = [], []
    for dim, tag in boundary:
        if tag in contact_surfs:
            continue
        if gmsh.model.getType(dim, tag) == "Plane":
            z_com = occ.getCenterOfMass(dim, tag)[2]
            if abs(z_com) > 1e-9 * R:
                raise RuntimeError(f"planar outer surface {tag} is not on z = 0")
            top.append(tag)
        else:
            far.append(tag)
    gmsh.model.addPhysicalGroup(2, far, tag=FAR_TAG)
    gmsh.model.addPhysicalGroup(2, top, tag=SURFACE_TAG)

    # Size field: graded distance to each contact (sizes scaled per contact, see MeshSizing),
    # plus optional boxes.
    fld = gmsh.model.mesh.field
    fields = []
    for near, near_distance, surfs in zip(
        sizing.near_sizes(model.contacts),
        sizing.near_distances(model.contacts),
        surfs_per_contact,
        strict=True,
    ):
        curves = gmsh.model.getBoundary([(2, s) for s in surfs], combined=False)
        dist = fld.add("Distance")
        fld.setNumbers(dist, "CurvesList", sorted({abs(c[1]) for c in curves}))
        fld.setNumbers(dist, "SurfacesList", surfs)
        fld.setNumber(dist, "Sampling", 100)
        thr = fld.add("Threshold")
        fld.setNumber(thr, "InField", dist)
        fld.setNumber(thr, "SizeMin", near)
        fld.setNumber(thr, "SizeMax", sizing.far)
        fld.setNumber(thr, "DistMin", near_distance)
        fld.setNumber(thr, "DistMax", near_distance + (sizing.far - near) / sizing.growth)
        fields.append(thr)
    for b in sizing.boxes:
        bf = fld.add("Box")
        for name, val in (
            ("VIn", b.size),
            ("VOut", sizing.far),
            ("XMin", b.xmin),
            ("XMax", b.xmax),
            ("YMin", b.ymin),
            ("YMax", b.ymax),
            ("ZMin", b.zmin),
            ("ZMax", b.zmax),
        ):
            fld.setNumber(bf, name, val)
        fields.append(bf)
    fmin = fld.add("Min")
    fld.setNumbers(fmin, "FieldsList", fields)
    fld.setAsBackgroundMesh(fmin)

    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
    gmsh.option.setNumber("Mesh.MeshSizeMax", sizing.far)
    gmsh.option.setNumber("Mesh.Algorithm3D", 1)  # Delaunay: deterministic
    gmsh.model.mesh.generate(3)


# A RefineBox counts as honoured when the 95th percentile of the longest edge of the cells
# whose centroid lies in the box is at most this multiple of the box size. Assumption set in
# step 3.1: honoured boxes gave 1.9 to 2.0, the same regions without the box 3.3 to 3.5, and
# a large thin box that Gmsh failed to refine (2.1 mm wide, 20 um deep) gave 85.
BOX_EDGE_LIMIT = 2.5


def box_resolution(hs: HalfSpaceMesh) -> list[float]:
    """For each RefineBox: 95th percentile of (longest cell edge / box size) inside the box.

    Cells count when their centroid is inside the box. Returns inf for a box that contains
    no cell centroid.
    """
    mesh = hs.mesh
    x = mesh.geometry.x
    n_owned = mesh.topology.index_map(mesh.topology.dim).size_local
    p = x[mesh.geometry.dofmap[:n_owned, :4]]  # vertices of the owned tetrahedra
    centroid = p.mean(axis=1)
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    longest = np.max([np.linalg.norm(p[:, i] - p[:, j], axis=1) for i, j in pairs], axis=0)
    out = []
    for b in hs.sizing.boxes:
        inside = (
            (centroid[:, 0] >= b.xmin)
            & (centroid[:, 0] <= b.xmax)
            & (centroid[:, 1] >= b.ymin)
            & (centroid[:, 1] <= b.ymax)
            & (centroid[:, 2] >= b.zmin)
            & (centroid[:, 2] <= b.zmax)
        )
        ratios = np.concatenate(mesh.comm.allgather(longest[inside] / b.size))
        out.append(float(np.percentile(ratios, 95)) if ratios.size else math.inf)
    return out


def build_mesh(
    model: HalfSpaceModel,
    sizing: MeshSizing,
    comm: MPI.Comm = MPI.COMM_WORLD,
    check_boxes: bool = True,
) -> HalfSpaceMesh:
    """Build the Gmsh model on rank 0, mesh it and convert it to a dolfinx mesh.

    With `check_boxes`, raises RuntimeError when a RefineBox was not honoured (see
    BOX_EDGE_LIMIT): Gmsh can fail to refine a large thin box without reporting an error.
    """
    import gmsh
    from dolfinx.io import gmshio

    gmsh.initialize(interruptible=False)
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("halfspace")
        if comm.rank == 0:
            _build_gmsh_model(gmsh, model, sizing)
        mesh, cell_tags, facet_tags = gmshio.model_to_mesh(gmsh.model, comm, 0, gdim=3)
    finally:
        gmsh.finalize()
    hs = HalfSpaceMesh(model, sizing, mesh, cell_tags, facet_tags)
    if check_boxes:
        for i, ratio in enumerate(box_resolution(hs)):
            if ratio > BOX_EDGE_LIMIT:
                raise RuntimeError(
                    f"RefineBox {i} was not honoured: 95th percentile of longest edge / size "
                    f"is {ratio:.3g} (limit {BOX_EDGE_LIMIT}); the mesh is not refined there"
                )
    return hs
