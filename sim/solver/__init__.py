"""Quasi-static volume-conductor solver: own Gmsh mesh plus FEniCSx (A-010, A-011).

Units: SI inside the solver (m, S/m, A, V). Convert from the configuration's mm and mA with
sim.solver.units before calling it. Verified against exact solutions in tests/test_solver.py
(checklist step 3.1).

Conductivities are never defaulted here: the caller passes them, with their labels and
sources, per layer.
"""

from .fem import (
    FAR_BOUNDARIES,
    MAX_AREA_ERROR,
    UnderResolvedLayerWarning,
    VolumeConductor,
    layer_spreading_check,
)
from .geometry import (
    BOX_EDGE_LIMIT,
    CONTACT_TAG0,
    FAR_TAG,
    SURFACE_TAG,
    HalfSpaceMesh,
    HalfSpaceModel,
    MeshSizing,
    RefineBox,
    SurfaceContact,
    box_resolution,
    build_mesh,
)

__all__ = [
    "BOX_EDGE_LIMIT",
    "CONTACT_TAG0",
    "FAR_BOUNDARIES",
    "FAR_TAG",
    "MAX_AREA_ERROR",
    "SURFACE_TAG",
    "HalfSpaceMesh",
    "HalfSpaceModel",
    "MeshSizing",
    "RefineBox",
    "SurfaceContact",
    "UnderResolvedLayerWarning",
    "VolumeConductor",
    "box_resolution",
    "build_mesh",
    "layer_spreading_check",
]
