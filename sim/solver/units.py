"""Adapter from the configuration's units to the solver's SI units.

sim.config stores lengths in mm and currents in mA (sim/config/units.py); conductivities are
in S/m in both places. The solver works in m, A, S/m and V. The factors are exact (SI prefix
definitions), not data.

The sign of a contact's current (which phase, which contact is the return) is not mapped
here: the solver takes positive as current into the tissue, and the caller decides.
"""

from __future__ import annotations

import numpy as np

from .geometry import SurfaceContact

M_PER_MM = 1e-3  # exact, SI prefix
A_PER_MA = 1e-3  # exact, SI prefix


def length_m(value_mm):
    """mm -> m."""
    return np.asarray(value_mm, dtype=float) * M_PER_MM


def current_a(value_mA):
    """mA -> A."""
    return np.asarray(value_mA, dtype=float) * A_PER_MA


def conductivity_s_per_m(value_S_per_m):
    """S/m -> S/m (same unit on both sides; kept so every quantity passes through here)."""
    return np.asarray(value_S_per_m, dtype=float)


def contact_to_si(contact) -> SurfaceContact:
    """A sim.config Contact (dims and position in mm) as a solver SurfaceContact (m)."""
    d = contact.dims_mm
    centre = (float(length_m(contact.x_mm)), float(length_m(contact.y_mm)))
    if contact.shape == "disc":
        return SurfaceContact("disc", centre, radius=float(length_m(d["diameter"] / 2)))
    if contact.shape == "ring":
        return SurfaceContact(
            "ring",
            centre,
            radius=float(length_m(d["outer_diameter"] / 2)),
            inner_radius=float(length_m(d["inner_diameter"] / 2)),
        )
    if contact.shape == "rectangle":
        return SurfaceContact(
            "rectangle",
            centre,
            length=float(length_m(d["length"])),
            width=float(length_m(d["width"])),
        )
    raise ValueError(f"unknown contact shape {contact.shape!r}")
