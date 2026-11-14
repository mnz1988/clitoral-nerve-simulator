"""Verification of the volume-conductor solver against exact solutions (checklist step 3.1).

Units: SI (m, S/m, A, V). Run with `python -m pytest tests/test_solver.py -s` to see the error
tables. Every geometry, conductivity and current below is a round test value chosen for the
check (label: assumption). None of them is a tissue value.

Achieved errors are printed; the targets are those of step 3.1 (themselves assumptions).
"""

from __future__ import annotations

import warnings

import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("gmsh")

from sim.solver import (  # noqa: E402
    MAX_AREA_ERROR,
    HalfSpaceModel,
    MeshSizing,
    RefineBox,
    SurfaceContact,
    UnderResolvedLayerWarning,
    VolumeConductor,
    box_resolution,
    build_mesh,
    layer_spreading_check,
    units,
)
from sim.solver import analytic as an  # noqa: E402

A = 1e-3  # disc radius, m (assumption: round test value)
SIGMA = 1.0  # S/m (assumption: round test value, not a tissue value)
CURRENT = 1e-3  # A (assumption: round test value)
R = 0.1  # truncation radius, m (assumption: 100 contact radii)
# Mesh: size A/8 within A of the contact, growing 0.2 m per m of distance, at most R/8
# (assumption: chosen by trial in step 3.1; gives < 0.2 % potential error, see test 1).
SIZING = MeshSizing(near=A / 8, far=R / 8, near_distance=A, growth=0.2)
PAIR_OFFSET = 3e-3  # centre of each contact of the pair at x = -/+ 3 mm (assumption)

TARGET_POTENTIAL = 0.02  # step 3.1 target, assumption
TARGET_SUPERPOSITION = 0.01  # step 3.1 target, assumption
TARGET_THRESHOLD_CHANGE = 0.03  # step 3.1 target, assumption
SOLVER_LEVEL = 1e-9  # linear-algebra round-off level for CG rtol 1e-12 (assumption, margin)


def axis_points(depth, x=0.0) -> np.ndarray:
    depth = np.asarray(depth, dtype=float)
    return np.c_[np.full_like(depth, x), np.zeros_like(depth), -depth]


def rel(fe, ex) -> np.ndarray:
    return (np.asarray(fe) - np.asarray(ex)) / np.abs(ex)


def table(title, labels, values) -> None:
    print(f"\n{title}")
    for lab, val in zip(labels, values, strict=True):
        print(f"  {lab:>28}: " + " ".join(f"{v:9.4f}" for v in np.atleast_1d(val)))


# ------------------------------------------------------------------ the references themselves


def test_reference_disc_quadrature_matches_closed_form():
    d = A * np.array([0.1, 0.5, 1, 5])
    quad = an.disc_potential(axis_points(d), CURRENT, A, an.halfspace_kernel(SIGMA))
    assert np.max(np.abs(rel(quad, an.halfspace_disc_axis(CURRENT, A, SIGMA, d)))) < 1e-6
    # the reduced rule used for long image series agrees on the surface points of test 5
    surface = np.c_[np.array([2, 4, 10]) * A, np.zeros(3), np.zeros(3)]
    kern = an.halfspace_kernel(SIGMA)
    full = an.disc_potential(surface, CURRENT, A, kern)
    reduced = an.disc_potential(surface, CURRENT, A, kern, n_radial=16, n_angle=32)
    assert np.max(np.abs(rel(reduced, full))) < 1e-4


def test_reference_two_layer_series_is_consistent():
    s1, s2, h = 1.0, 0.1, 0.2e-3  # assumption: test values
    r = np.array([0.1e-3, 1e-3, 5e-3])
    # equal conductivities reduce to the homogeneous half-space
    same = an.two_layer_point_kernel(1.0, 1.0, h, r, 0.5 * h)
    assert np.allclose(same, 1 / (2 * np.pi * np.hypot(r, 0.5 * h)), rtol=1e-12)
    # potential and normal current are continuous across the interface
    eps = 1e-6 * h

    def kern(depth):
        return an.two_layer_point_kernel(s1, s2, h, r, np.full_like(r, depth))

    # top-layer formula at d = h against lower-layer formula one float step below the interface
    v_top, v_bot = kern(h), kern(np.nextafter(h, 1.0))
    assert np.allclose(v_top, v_bot, rtol=1e-12)
    dv_top = v_top - kern(h - eps)
    dv_bot = kern(h + eps) - v_bot
    assert np.allclose(s1 * dv_top, s2 * dv_bot, rtol=1e-4)
    # far from the source the lower layer dominates: V -> I / (2 pi s2 r)
    far = an.two_layer_point_kernel(s1, s2, h, np.array([0.5]), np.array([0.0]))
    assert abs(far[0] * 2 * np.pi * s2 * 0.5 - 1) < 1e-3
    # disc on-axis closed form equals quadrature of the point kernel
    d = np.array([0.0, 0.5 * h, h, 3 * h])
    a = 0.5e-3
    quad = an.disc_potential(axis_points(d + 1e-12), 1.0, a, an.two_layer_kernel(s1, s2, h))
    assert np.allclose(quad, an.two_layer_disc_axis(1.0, a, s1, s2, h, d), rtol=1e-5)


def test_reference_disc_quadrature_off_centre():
    """The quadrature honours both coordinates of the disc centre (x and y)."""
    centre = (0.7 * A, -1.3 * A)
    d = A * np.array([0.5, 1, 3])
    pts = np.c_[np.full_like(d, centre[0]), np.full_like(d, centre[1]), -d]
    quad = an.disc_potential(pts, CURRENT, A, an.halfspace_kernel(SIGMA), centre=centre)
    assert np.max(np.abs(rel(quad, an.halfspace_disc_axis(CURRENT, A, SIGMA, d)))) < 1e-6


# (s1, s2) pairs: contrasts 1/10 to 1000 both ways (assumption: test values)
HANKEL_CONTRASTS = [(1.0, 0.1), (0.1, 1.0), (1.0, 1e-3), (1e-3, 1.0), (1.0, 0.01)]


def test_reference_two_layer_images_against_hankel():
    """Image series against the independent Hankel-transform solution (analytic.py)."""
    h, a = 0.2e-3, 0.75e-3  # m (assumption: test values)
    worst_point = worst_disc = 0.0
    for s1, s2 in HANKEL_CONTRASTS:
        for r in (0.0, 0.1e-3, 1e-3, 5e-3):
            for d in (0.0, 0.5 * h, h, 1.5 * h, 5 * h):
                if r == 0 and d == 0:
                    continue
                img = an.two_layer_point_kernel(s1, s2, h, np.array([r]), np.array([d]))[0]
                ref = an.two_layer_point_hankel(s1, s2, h, r, d)
                worst_point = max(worst_point, abs(img / ref - 1))
        for d in (0.0, 0.5 * h, h, 3 * h, 10 * h):
            img = an.two_layer_disc_axis(1.0, a, s1, s2, h, [d])[0]
            ref = an.two_layer_point_hankel(s1, s2, h, 0.0, d, disc_radius=a)
            worst_disc = max(worst_disc, abs(img / ref - 1))
    print(f"\nimages vs Hankel: point kernel {worst_point:.1e}, disc axis {worst_disc:.1e}")
    assert worst_point < 1e-8
    assert worst_disc < 1e-8


# ------------------------------------------------------------------ units adapter


def test_units_adapter_converts_config_units_to_si():
    from sim.config import Contact

    disc = units.contact_to_si(Contact("c1", "disc", {"diameter": 1.5}, 2.0, -1.0, "active", 1.0))
    assert disc.radius == pytest.approx(0.75e-3, rel=1e-15)
    assert disc.centre == pytest.approx((2e-3, -1e-3), rel=1e-15)
    ring = units.contact_to_si(
        Contact("c2", "ring", {"outer_diameter": 4.0, "inner_diameter": 2.0}, 0, 0, "return", -1)
    )
    assert (ring.radius, ring.inner_radius) == pytest.approx((2e-3, 1e-3), rel=1e-15)
    rect = units.contact_to_si(
        Contact("c3", "rectangle", {"length": 3.0, "width": 0.5}, 0, 0, "active", 1.0)
    )
    assert (rect.length, rect.width) == pytest.approx((3e-3, 0.5e-3), rel=1e-15)
    # Quantities that expose a mixed-unit mistake (mm and mA passed unconverted together give
    # the same V = I / (sigma L) but not these). Expected values worked out by hand.
    # Current density of 1 mA on a 1.5 mm disc: 1e-3 A / (pi (0.75e-3 m)^2) = 565.884 A/m2.
    density = units.current_a(1.0) / disc.area
    assert density == pytest.approx(565.884242, rel=1e-6)
    # Second x-difference of V over a point source, 1 mA, 0.5 S/m, 2 mm below it:
    # d2V/dx2 = -I / (2 pi sigma z^3) = -1e-3 / (pi * 8e-9) = -39788.7 V/m2.
    sigma = units.conductivity_s_per_m(0.5)
    step, z = units.length_m(0.01), units.length_m(2.0)
    x = np.array([-step, 0.0, step])
    v = an.halfspace_point(units.current_a(1.0), sigma, np.hypot(x, z))
    second = (v[0] - 2 * v[1] + v[2]) / step**2
    assert second == pytest.approx(-39788.7, rel=1e-4)


# ------------------------------------------------------------------ guards


def test_contact_area_guard():
    """A near-contact size too coarse for the contact makes the meshed area wrong: refuse it."""
    model = HalfSpaceModel((SurfaceContact("disc", radius=A),), radius=R)
    hs = build_mesh(model, MeshSizing(near=A / 1.5, far=R / 4, near_distance=A, growth=0.3))
    with pytest.raises(ValueError, match="meshed area"):
        VolumeConductor(hs, [SIGMA])
    unchecked = VolumeConductor(hs, [SIGMA], max_area_error=None)
    area_error = unchecked.contact_areas[0] / model.contacts[0].area - 1
    print(f"\ncoarse disc (near = a/1.5): meshed area error {100 * area_error:.2f} %")
    assert abs(area_error) > MAX_AREA_ERROR


def test_layer_spreading_guard():
    a = 0.1e-3  # m (assumption: test values below)
    h = 0.01e-3
    model = HalfSpaceModel((SurfaceContact("disc", radius=a),), layer_thicknesses=(h,), radius=R)
    w = a + 5 * h
    sizing = MeshSizing(a / 8, R / 8, a, 0.2, boxes=(RefineBox(-w, w, -w, w, -h, 0.0, h / 2),))
    # 1000x more conductive than below: L = 10 mm, far beyond the 0.15 mm box
    assert len(layer_spreading_check(model, sizing, [100.0, 0.1])) == 1
    # resistive layer: no lateral spreading
    assert layer_spreading_check(model, sizing, [1e-4, 0.1]) == []
    # a box out to a + L with size h covers it
    big = a + 10e-3
    wide = MeshSizing(a / 8, R / 8, a, 0.2, boxes=(RefineBox(-big, big, -big, big, -h, 0, h),))
    assert layer_spreading_check(model, wide, [100.0, 0.1]) == []
    # a box that is too coarse (size > h) or does not span the layer depth does not count
    coarse = MeshSizing(
        a / 8, R / 8, a, 0.2, boxes=(RefineBox(-big, big, -big, big, -h, 0, 2 * h),)
    )
    assert len(layer_spreading_check(model, coarse, [100.0, 0.1])) == 1
    shallow = MeshSizing(
        a / 8, R / 8, a, 0.2, boxes=(RefineBox(-big, big, -big, big, -h / 2, 0, h),)
    )
    assert len(layer_spreading_check(model, shallow, [100.0, 0.1])) == 1
    # and the solver issues it as a warning (cheap coarse mesh, 0.2 mm layer, L = 200 mm)
    coarse_model = HalfSpaceModel(
        (SurfaceContact("disc", radius=A),), layer_thicknesses=(0.2e-3,), radius=R
    )
    hs = build_mesh(coarse_model, MeshSizing(near=A / 4, far=R / 4, near_distance=A, growth=0.3))
    with pytest.warns(UnderResolvedLayerWarning, match="spreading length"):
        VolumeConductor(hs, [100.0, 0.1])
    with warnings.catch_warnings():
        warnings.simplefilter("error", UnderResolvedLayerWarning)
        VolumeConductor(hs, [0.1, 1.0])


def test_refine_box_guard():
    """A box Gmsh does not honour is refused (computed in step 3.1: this one gave 60 % error).

    0.1 mm disc, 20 um layer, box 2.1 mm wide with size 20 um: the 3D Delaunay could not insert
    most nodes and the layer stayed coarse, without an error from Gmsh.
    """
    a, h = 0.1e-3, 20e-6  # m (assumption: test values)
    w = a + 100 * h
    model = HalfSpaceModel((SurfaceContact("disc", radius=a),), layer_thicknesses=(h,), radius=R)
    sizing = MeshSizing(a / 8, R / 8, a, 0.2, boxes=(RefineBox(-w, w, -w, w, -h, 0.0, h),))
    with pytest.raises(RuntimeError, match="not honoured"):
        build_mesh(model, sizing)


# ------------------------------------------------------------------ fixtures (one mesh each)


@pytest.fixture(scope="module")
def homog():
    hs = build_mesh(HalfSpaceModel((SurfaceContact("disc", radius=A),), radius=R), SIZING)
    vc = VolumeConductor(hs, [SIGMA])
    return hs, vc, vc.solve([CURRENT])


@pytest.fixture(scope="module")
def pair():
    contacts = (
        SurfaceContact("disc", centre=(-PAIR_OFFSET, 0.0), radius=A),
        SurfaceContact("disc", centre=(PAIR_OFFSET, 0.0), radius=A),
    )
    hs = build_mesh(HalfSpaceModel(contacts, radius=R), SIZING)
    return hs, VolumeConductor(hs, [SIGMA])


# Unequal pair: 1 mm disc and 0.25 mm disc, both off the x axis (assumption: test values).
BIG = SurfaceContact("disc", centre=(-PAIR_OFFSET, 1e-3), radius=A)
SMALL = SurfaceContact("disc", centre=(PAIR_OFFSET, -1e-3), radius=A / 4)


@pytest.fixture(scope="module")
def unequal():
    hs = build_mesh(HalfSpaceModel((BIG, SMALL), radius=R), SIZING)
    vc = VolumeConductor(hs, [SIGMA])
    currents = [CURRENT, -CURRENT]
    return hs, vc, currents, vc.solve(currents)


# ------------------------------------------------------------------ 1. homogeneous half-space


def test_1_homogeneous_disc_against_analytic(homog):
    hs, vc, V = homog
    d = A * np.array([0, 0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 50])
    e_axis = rel(vc.evaluate(V, axis_points(d)), an.halfspace_disc_axis(CURRENT, A, SIGMA, d))
    r = A * np.array([1.5, 2, 5, 10, 20, 50])
    diag = np.c_[r / np.sqrt(2), np.zeros_like(r), -r / np.sqrt(2)]
    fe = vc.evaluate(V, diag)
    e_diag = rel(fe, an.disc_potential(diag, CURRENT, A, an.halfspace_kernel(SIGMA)))
    e_point = rel(fe, an.halfspace_point(CURRENT, SIGMA, r))
    print(f"\nhomogeneous half-space: {hs.n_cells} cells, CG iterations {vc.last_iterations}")
    table("on axis", ["depth / a", "error % vs disc formula"], [d / A, 100 * e_axis])
    table(
        "45 degree ray",
        ["distance / a", "error % vs disc quadrature", "error % vs I/(2 pi sigma r)"],
        [r / A, 100 * e_diag, 100 * e_point],
    )
    assert np.max(np.abs(e_axis)) < TARGET_POTENTIAL
    assert np.max(np.abs(e_diag)) < TARGET_POTENTIAL
    # far field: the disc acts as a point source from about 5 radii on
    assert np.max(np.abs(e_point[r >= 5 * A])) < TARGET_POTENTIAL
    # all injected current leaves through the far boundary (discrete conservation)
    assert abs(vc.far_current(V) / CURRENT - 1) < SOLVER_LEVEL


def test_1b_truncation_boundary_effect(homog):
    """Robin (chosen) against Dirichlet V = 0 on the same mesh.

    Dirichlet shifts V by about -I / (2 pi sigma R).
    """
    hs, robin, V_r = homog
    dirichlet = VolumeConductor(hs, [SIGMA], far_boundary="dirichlet")
    V_d = dirichlet.solve([CURRENT])
    d = A * np.array([1, 5, 10, 20, 50])
    ex = an.halfspace_disc_axis(CURRENT, A, SIGMA, d)
    e_r = rel(robin.evaluate(V_r, axis_points(d)), ex)
    v_d = dirichlet.evaluate(V_d, axis_points(d))
    e_d = rel(v_d, ex)
    shift = CURRENT / (2 * np.pi * SIGMA * R)
    e_d_corrected = rel(v_d + shift, ex)
    table(
        "truncation at R = 100 a",
        ["depth / a", "Robin error %", "Dirichlet error %", "Dirichlet + I/(2 pi s R) err %"],
        [d / A, 100 * e_r, 100 * e_d, 100 * e_d_corrected],
    )
    assert np.max(np.abs(e_r)) < 0.005
    assert np.max(np.abs(e_d_corrected)) < 0.005
    assert abs(dirichlet.far_current(V_d) / CURRENT - 1) < 1e-6


# ------------------------------------------------------------------ 2. linearity


def test_2_linearity(homog):
    _, vc, V1 = homog
    V2 = vc.solve([2 * CURRENT])
    err = np.max(np.abs(V2.x.array - 2 * V1.x.array)) / np.max(np.abs(V2.x.array))
    print(f"\nlinearity: max |V(2I) - 2 V(I)| / max |V(2I)| = {err:.2e} (tolerance {SOLVER_LEVEL})")
    assert err < SOLVER_LEVEL


# ------------------------------------------------------------------ 3. superposition


def test_3_superposition(pair):
    _, vc = pair
    i_a, i_b = CURRENT, -0.5 * CURRENT  # assumption: unequal test currents
    V_a = vc.solve([i_a, 0.0])
    V_b = vc.solve([0.0, i_b])
    V_ab = vc.solve([i_a, i_b])
    err = np.max(np.abs(V_ab.x.array - V_a.x.array - V_b.x.array)) / np.max(np.abs(V_ab.x.array))
    print(f"\nsuperposition: max |V_ab - V_a - V_b| / max |V_ab| = {err:.2e} (target 1e-2)")
    assert err < TARGET_SUPERPOSITION
    # It is exact up to round-off on one mesh; larger means a nonlinearity or normalisation bug.
    assert err < SOLVER_LEVEL


# ------------------------------------------------------------------ 6. charge balance and gauge


def test_6_balanced_pair_is_well_posed(pair):
    """+I and -I: fluxes sum to zero; Robin far boundary fixes the gauge (V -> 0 far away)."""
    _, vc = pair
    currents = [CURRENT, -CURRENT]
    V = vc.solve(currents)
    injected = vc.injected_current(currents)
    far = vc.far_current(V)
    print(
        f"\nbalanced pair: injected {injected[0]:.6e} A and {injected[1]:.6e} A, "
        f"sum {sum(injected):.2e} A, through far boundary {far:.2e} A, "
        f"CG iterations {vc.last_iterations}"
    )
    assert abs(injected[0] / CURRENT - 1) < 1e-12 and abs(injected[1] / CURRENT + 1) < 1e-12
    assert abs(sum(injected)) < 1e-12 * CURRENT
    assert abs(far) < SOLVER_LEVEL * CURRENT
    # gauge: compare with the exact pair potential (sum of the two disc solutions, V = 0 at
    # infinity); a gauge offset would show as a constant error, largest where V is small.
    depth = np.array([0.5, 1, 2, 5]) * A
    xs = np.array([-2 * PAIR_OFFSET, -PAIR_OFFSET, 0.0, PAIR_OFFSET / 3])
    pts = np.array([[x, 0.0, -z] for x in xs for z in depth])
    kern = an.halfspace_kernel(SIGMA)
    ex = an.disc_potential(pts, CURRENT, A, kern, centre=(-PAIR_OFFSET, 0.0))
    ex -= an.disc_potential(pts, CURRENT, A, kern, centre=(PAIR_OFFSET, 0.0))
    fe = vc.evaluate(V, pts)
    scale = np.max(np.abs(ex))
    err = np.max(np.abs(fe - ex)) / scale
    mid = np.abs(pts[:, 0]) < 1e-12  # symmetry plane, where the exact V is 0
    print(
        f"  max |V - exact| / max |exact| = {100 * err:.3f} %, on the symmetry plane "
        f"max |V| / max |exact| = {100 * np.max(np.abs(fe[mid])) / scale:.3f} %"
    )
    assert err < TARGET_POTENTIAL
    assert np.max(np.abs(fe[mid])) / scale < 0.005


def test_6b_unequal_contacts(unequal):
    """1 mm (+I) and 0.25 mm (-I) discs: each contact gets its own area, current and mesh size."""
    hs, vc, currents, V = unequal
    area_err = [vc.contact_areas[j] / c.area - 1 for j, c in enumerate((BIG, SMALL))]
    injected = vc.injected_current(currents)
    # current recovered from the solution (consistent flux), not from the stored areas
    recovered = [vc.contact_current(V, j) for j in range(2)]
    far = vc.far_current(V)
    kern = an.halfspace_kernel(SIGMA)
    # axis of each contact: closed form for that disc plus quadrature for the other one
    d_small = SMALL.radius * np.array([0, 0.5, 1, 2, 5])
    d_big = A * np.array([0, 0.5, 1, 2])
    p_small = np.c_[np.full((5, 2), SMALL.centre), -d_small]
    p_big = np.c_[np.full((4, 2), BIG.centre), -d_big]
    ex_small = an.halfspace_disc_axis(-CURRENT, SMALL.radius, SIGMA, d_small)
    ex_small += an.disc_potential(p_small, CURRENT, A, kern, centre=BIG.centre)
    ex_big = an.halfspace_disc_axis(CURRENT, A, SIGMA, d_big)
    ex_big += an.disc_potential(p_big, -CURRENT, SMALL.radius, kern, centre=SMALL.centre)
    e_small = rel(vc.evaluate(V, p_small), ex_small)
    e_big = rel(vc.evaluate(V, p_big), ex_big)
    # points off both axes, with y != 0, against the summed quadrature
    p_off = np.array([[0.0, 2e-3, -1e-3], [1e-3, -2e-3, -0.5e-3], [-3e-3, 3e-3, -0.5e-3]])
    ex_off = an.disc_potential(p_off, CURRENT, A, kern, centre=BIG.centre)
    ex_off += an.disc_potential(p_off, -CURRENT, SMALL.radius, kern, centre=SMALL.centre)
    e_off = rel(vc.evaluate(V, p_off), ex_off)
    print(
        f"\nunequal pair, {hs.n_cells} cells: area error % {np.round(100 * np.array(area_err), 3)},"
        f" injected {injected}, recovered from V {recovered}, far {far:.1e} A"
    )
    table(
        "unequal pair, error %",
        ["small axis depth / a2", "error %", "big axis depth / a", "error %", "off-axis error %"],
        [d_small / SMALL.radius, 100 * e_small, d_big / A, 100 * e_big, 100 * e_off],
    )
    # per-contact near size (a_j / 8): both areas well inside the guard
    assert max(abs(e) for e in area_err) < 0.005
    assert injected == pytest.approx(currents, rel=1e-12)
    assert recovered == pytest.approx(currents, rel=1e-8)
    assert abs(far) < 1e-8 * CURRENT
    assert np.max(np.abs(e_small)) < TARGET_POTENTIAL
    assert np.max(np.abs(e_big)) < TARGET_POTENTIAL
    assert np.max(np.abs(e_off)) < TARGET_POTENTIAL


# ------------------------------------------------------------------ 5. two-layer half-space

SIGMA_LOWER = 0.1  # S/m (assumption: round test value)
# (contact radius m, top-layer thickness m, top/lower conductivity ratios). Assumption: test
# values. 0.75 mm radius is the 1.5 mm default contact and 0.1 mm the 0.2 mm pin that
# docs/scope.md names as the smallest modelled contact; 10 um at 1/1000 is a resistive
# surface sheet of stratum-corneum-like thinness (no tissue value implied).
TWO_LAYER_CASES = [
    (0.75e-3, 0.2e-3, (10.0, 0.1)),
    (0.1e-3, 0.02e-3, (10.0, 0.1)),
    (0.1e-3, 0.01e-3, (0.001,)),
]


def two_layer_mesh(a: float, h: float, max_ratio: float):
    """Size a/8 within a of the contact, and h/2 inside the top layer out to a + max(5h, L).

    L = h * max_ratio is the spreading length of the most conductive top layer to be solved
    on this mesh (see layer_spreading_check in fem.py). These rules are assumptions set by
    trial in step 3.1. Computed in step 3.1: a 10 um layer stays within 0.3 % even unrefined
    (a/8 only) at contrasts 1/1000 to 100; a 10 um layer 1000x MORE conductive than the one
    below fails unrefined (2 to 7 %, growing with lateral distance) and passes (0.4 %) after
    halving every size. That case (L = 10 mm) is outside the verified range; the solver
    warns about it (UnderResolvedLayerWarning).
    """
    w = a + max(5 * h, h * max_ratio)
    sizing = MeshSizing(
        near=a / 8,
        far=R / 8,
        near_distance=a,
        growth=0.2,
        boxes=(RefineBox(-w, w, -w, w, -h, 0.0, h / 2),),
    )
    model = HalfSpaceModel((SurfaceContact("disc", radius=a),), layer_thicknesses=(h,), radius=R)
    return build_mesh(model, sizing)


@pytest.mark.slow
@pytest.mark.parametrize(("a", "h", "ratios"), TWO_LAYER_CASES)
def test_5_two_layer_against_images(a, h, ratios):
    hs = two_layer_mesh(a, h, max(ratios))
    depth = np.array([0, 0.5 * h, h, 2 * h, 0.5 * a, a, 2 * a, 5 * a, 20 * a])
    surface = np.c_[np.array([2, 4, 10]) * a, np.zeros(3), np.zeros(3)]
    for ratio in ratios:
        s1 = SIGMA_LOWER * ratio
        # MUMPS: CG + AMG needs about 200 iterations on thin conductive layers (computed in
        # step 3.1). The refinement rule above must satisfy the spreading guard.
        with warnings.catch_warnings():
            warnings.simplefilter("error", UnderResolvedLayerWarning)
            vc = VolumeConductor(hs, [s1, SIGMA_LOWER], linear_solver="direct")
        V = vc.solve([CURRENT])
        e_axis = rel(
            vc.evaluate(V, axis_points(depth)),
            an.two_layer_disc_axis(CURRENT, a, s1, SIGMA_LOWER, h, depth),
        )
        # fewer quadrature points when the image series is long (|k| close to 1)
        quad = {} if 0.01 <= ratio <= 100 else {"n_radial": 16, "n_angle": 32}
        kern = an.two_layer_kernel(s1, SIGMA_LOWER, h)
        e_surf = rel(vc.evaluate(V, surface), an.disc_potential(surface, CURRENT, a, kern, **quad))
        table(
            f"two layers a = {a * 1e3:g} mm, h = {h * 1e3:g} mm, s1/s2 = {ratio:g}, "
            f"{hs.n_cells} cells, box edge p95 / size {box_resolution(hs)[0]:.2f}",
            ["axis depth / h", "axis error %", "surface r / a", "surface error %"],
            [depth / h, 100 * e_axis, surface[:, 0] / a, 100 * e_surf],
        )
        assert np.max(np.abs(e_axis)) < TARGET_POTENTIAL
        assert np.max(np.abs(e_surf)) < TARGET_POTENTIAL


@pytest.mark.slow
def test_5c_conductive_sheet_is_a_known_limit():
    """KNOWN LIMIT, kept visible: a top layer 100x more conductive than the one below.

    0.75 mm disc, 0.2 mm layer, s1/s2 = 100, spreading length L = 20 mm. Computed in step 3.1:
    2.2 % on the axis and 2.3 % at 30 a laterally with the usual refinement (above the 2 %
    target); a RefineBox out to L (20.8 mm, size h) is not honoured by Gmsh (65 % error, now
    refused by build_mesh). The solver must warn here. If this test starts failing because
    the error dropped below the target, the limit is fixed: update fem.py and this test.
    """
    a, h, ratio = 0.75e-3, 0.2e-3, 100.0  # assumption: test values
    hs = two_layer_mesh(a, h, 1.0)  # box out to a + 5h only
    s1 = SIGMA_LOWER * ratio
    with pytest.warns(UnderResolvedLayerWarning):
        vc = VolumeConductor(hs, [s1, SIGMA_LOWER], linear_solver="direct")
    V = vc.solve([CURRENT])
    depth = np.array([0, 0.5 * h, h, 2 * h, a, 5 * a])
    e_axis = rel(
        vc.evaluate(V, axis_points(depth)),
        an.two_layer_disc_axis(CURRENT, a, s1, SIGMA_LOWER, h, depth),
    )
    lat = np.array([10, 30]) * a
    pts = np.c_[lat, np.zeros(2), np.full(2, -2 * h)]
    kern = an.two_layer_kernel(s1, SIGMA_LOWER, h)
    e_lat = rel(vc.evaluate(V, pts), an.disc_potential(pts, CURRENT, a, kern))
    worst = max(np.max(np.abs(e_axis)), np.max(np.abs(e_lat)))
    print(f"\nconductive sheet s1/s2 = 100 (known limit): worst error {100 * worst:.2f} %")
    assert worst > TARGET_POTENTIAL


# ------------------------------------------------------------------ 4. mesh convergence (proxy)

PROXY_DX = 0.5e-3  # second-difference step, m (assumption: about one node spacing)
PROXY_DEPTHS = (0.25e-3, 0.5e-3, 1e-3)  # m (assumption: illustrative fibre depths)
FINE_PROXY_TOLERANCE = 0.005  # fine-mesh proxy error vs exact (assumption, about 2x computed)


def activating_proxy(potential_at, depth) -> float:
    """Largest second difference of V along x at `depth`, V for a cathodic current.

    PROXY, not a fibre threshold: the current needed to reach a fixed second difference is
    (fixed value) / (this number per ampere), so its relative change between meshes equals
    the relative change of this number. Real axon thresholds come in step 3.2.
    """
    xs = np.arange(-4 * A, 4 * A + 1e-12, PROXY_DX / 4)
    pts = np.concatenate(
        [np.c_[xs + s * PROXY_DX, np.zeros_like(xs), np.full_like(xs, -depth)] for s in (-1, 0, 1)]
    )
    v = potential_at(pts).reshape(3, -1)
    return float(np.max(v[0] - 2 * v[1] + v[2]))


@pytest.mark.slow
def test_4_mesh_convergence_of_threshold_proxy():
    model = HalfSpaceModel((SurfaceContact("disc", radius=A),), radius=R)
    coarse_sizing = SIZING.scaled(2.0)  # h = A/4 at the contact (assumption)
    cathodic = -CURRENT
    exact = [
        activating_proxy(
            lambda p: an.disc_potential(
                p, cathodic, A, an.halfspace_kernel(SIGMA), n_radial=96, n_angle=192
            ),
            z,
        )
        for z in PROXY_DEPTHS
    ]
    proxies, cells = [], []
    for sizing in (coarse_sizing, coarse_sizing.scaled(0.5)):
        hs = build_mesh(model, sizing)
        vc = VolumeConductor(hs, [SIGMA])
        V = vc.solve([cathodic])

        def fem_potential(p, vc=vc, V=V):
            return vc.evaluate(V, p)

        proxies.append([activating_proxy(fem_potential, z) for z in PROXY_DEPTHS])
        cells.append(hs.n_cells)
    p_h, p_h2 = np.array(proxies)
    threshold_change = p_h / p_h2 - 1  # proxy threshold is proportional to 1 / proxy
    table(
        f"threshold proxy, cells {cells[0]} -> {cells[1]}",
        ["depth mm", "proxy change % h -> h/2", "error % at h vs exact", "error % at h/2"],
        [
            np.array(PROXY_DEPTHS) * 1e3,
            100 * threshold_change,
            100 * rel(p_h, exact),
            100 * rel(p_h2, exact),
        ],
    )
    # the two meshes really differ: halving h in 3D gives up to 8x the cells (grading lowers it)
    assert cells[1] >= 4 * cells[0]
    assert np.max(np.abs(threshold_change)) < TARGET_THRESHOLD_CHANGE
    # and the fine mesh is close to the exact proxy (computed in step 3.1: 0.20 to 0.27 %)
    assert np.max(np.abs(rel(p_h2, exact))) < FINE_PROXY_TOLERANCE
