"""Electrode layout and stimulus configuration: parsing, validation and flags.

A layout file is YAML. Every quantity is written with its unit ("1.5 mm", "200 us", "0.5 mA").
Positions are contact centres on the region's modeled surface, with the origin at the surface
centre, x along the region's length and y along its width.

Validation never changes a user's value: a value that is not allowed is rejected with the reason.
Flags are warnings only. The driver-voltage flag needs the field solver and is not computed here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

from .errors import ConfigError
from .limits import (
    SHAPES,
    SKIN_CONDITIONS,
    Region,
    _load_yaml,
    load_model_limits,
    load_region,
)
from .units import fmt, parse_quantity

MATERIALS = ("stainless_steel", "copper", "silver", "gold", "titanium")
PULSE_SHAPES = ("monophasic", "biphasic_symmetric", "biphasic_asymmetric")
PHASES = ("cathodic", "anodic")
ROLES = ("active", "return", "unconnected")
RETURN_PATHS = ("local", "distant")
_TOL = 1e-9

_TOP_KEYS = {
    "name",
    "region",
    "material",
    "skin_condition",
    "drive",
    "driver_voltage_limit",
    "return_path",
    "contacts",
    "stimulus",
}
_STIM_KEYS = {
    "pulse_shape",
    "leading_phase",
    "pulse_width",
    "pulse_width_sweep",
    "interphase_gap",
    "current",
    "rate",
    "train_length",
    "zero_average",
}
_CONTACT_KEYS = {
    "id",
    "shape",
    "diameter",
    "length",
    "width",
    "outer_diameter",
    "inner_diameter",
    "position",
    "role",
    "current_share",
}
_SHAPE_DIMS = {
    "disc": ("diameter",),
    "rectangle": ("length", "width"),
    "ring": ("outer_diameter", "inner_diameter"),
}


@dataclass(frozen=True)
class Contact:
    id: str
    shape: str
    dims_mm: dict[str, float]
    x_mm: float
    y_mm: float
    role: str
    current_share: float  # signed fraction; for a distant return it is computed

    @property
    def half_extents_mm(self) -> tuple[float, float]:
        d = self.dims_mm
        if self.shape == "disc":
            return d["diameter"] / 2, d["diameter"] / 2
        if self.shape == "ring":
            return d["outer_diameter"] / 2, d["outer_diameter"] / 2
        return d["length"] / 2, d["width"] / 2

    @property
    def largest_dim_mm(self) -> float:
        hx, hy = self.half_extents_mm
        return 2 * max(hx, hy)

    @property
    def area_mm2(self) -> float:
        d = self.dims_mm
        if self.shape == "disc":
            return math.pi * d["diameter"] ** 2 / 4
        if self.shape == "ring":
            return math.pi * (d["outer_diameter"] ** 2 - d["inner_diameter"] ** 2) / 4
        return d["length"] * d["width"]


@dataclass(frozen=True)
class Stimulus:
    pulse_shape: str
    leading_phase: str
    pulse_width_s: float
    pulse_width_sweep_s: tuple[float, float] | None
    interphase_gap_s: float
    current_mA: float
    rate_Hz: float
    train_length_s: float
    zero_average: bool


@dataclass(frozen=True)
class Flag:
    name: str
    message: str
    contact: str | None = None


@dataclass(frozen=True)
class Layout:
    name: str
    region: Region
    material: str
    skin_condition: str
    drive: str
    driver_voltage_limit_V: float
    return_path: str
    contacts: tuple[Contact, ...]
    stimulus: Stimulus
    flags: tuple[Flag, ...] = field(default_factory=tuple)

    def contact_current_mA(self, contact: Contact) -> float:
        """Signed current of one contact: amplitude times its share."""
        return self.stimulus.current_mA * contact.current_share


# ---------------------------------------------------------------- helpers


def _mapping(value: object, where: str) -> dict:
    if not isinstance(value, dict):
        raise ConfigError(f"{where}: expected a mapping, got {value!r}")
    return value


def _choice(value: object, options: tuple[str, ...], where: str) -> str:
    if value not in options:
        raise ConfigError(f"{where}: {value!r} is not allowed; choose one of {', '.join(options)}")
    return value  # type: ignore[return-value]


def _quantity(data: dict, key: str, dimension: str, where: str, limit_name: str | None):
    """Read `key` as a quantity with unit, apply the model limit, or return the default."""
    limits = load_model_limits()
    field_name = f"{where}.{key}" if where else key
    if key not in data:
        if limit_name is None:
            raise ConfigError(f"{where}: missing required field {key!r}")
        default = limits[limit_name].default
        assert default is not None
        return default
    value = parse_quantity(data[key], dimension, field_name)
    if limit_name is not None:
        limits[limit_name].check(value, field_name)
    return value


def _edge_distance(a: Contact, b: Contact) -> float:
    """Shortest distance between the outlines of two contacts; negative when they overlap.

    A ring is treated as its outer disc.
    """
    ha, hb = a.half_extents_mm, b.half_extents_mm
    circ_a, circ_b = a.shape != "rectangle", b.shape != "rectangle"
    dx, dy = b.x_mm - a.x_mm, b.y_mm - a.y_mm
    if circ_a and circ_b:
        return math.hypot(dx, dy) - ha[0] - hb[0]
    if not circ_a and not circ_b:
        gx, gy = abs(dx) - ha[0] - hb[0], abs(dy) - ha[1] - hb[1]
        if gx < 0 and gy < 0:
            return max(gx, gy)
        return math.hypot(max(gx, 0.0), max(gy, 0.0))
    circle, rect = (a, b) if circ_a else (b, a)
    rc = circle.half_extents_mm[0]
    hx, hy = rect.half_extents_mm
    px = min(max(circle.x_mm, rect.x_mm - hx), rect.x_mm + hx)
    py = min(max(circle.y_mm, rect.y_mm - hy), rect.y_mm + hy)
    d = math.hypot(circle.x_mm - px, circle.y_mm - py)
    return d - rc if d > 0 else -rc


# ---------------------------------------------------------------- contacts


def _parse_contact(raw: object, index: int, region: Region) -> Contact:
    where = f"contacts[{index}]"
    data = _mapping(raw, where)
    unknown = set(data) - _CONTACT_KEYS
    if unknown:
        raise ConfigError(f"{where}: unknown field(s) {sorted(unknown)}")
    cid = str(data.get("id", f"c{index + 1}"))
    where = f"contact {cid!r}"
    shape = _choice(data.get("shape"), SHAPES, f"{where}.shape")
    if shape not in region.shapes:
        raise ConfigError(
            f"{where}: shape {shape!r} is not offered on the {region.name} region "
            f"(offered: {', '.join(region.shapes)})"
        )
    wanted = _SHAPE_DIMS[shape]
    stray = [
        k
        for k in ("diameter", "length", "width", "outer_diameter", "inner_diameter")
        if k in data and k not in wanted
    ]
    if stray:
        raise ConfigError(f"{where}: field(s) {stray} do not apply to a {shape}")
    lo, hi = region.contact_size_range()
    model_min = load_model_limits()["contact_size"].minimum or 0.0
    dims: dict[str, float] = {}
    for key in wanted:
        if key not in data:
            raise ConfigError(f"{where}: a {shape} needs {key!r}")
        size = parse_quantity(data[key], "length", f"{where}.{key}")
        dims[key] = size
        if key == "inner_diameter":
            continue
        if size < lo - _TOL:
            who = "model" if lo <= model_min + _TOL else f"{region.name} region"
            raise ConfigError(
                f"{where}.{key}: {fmt(size, 'length')} is below the smallest allowed contact "
                f"{fmt(lo, 'length')} ({who} limit)"
            )
        if size > hi + _TOL:
            raise ConfigError(
                f"{where}.{key}: {fmt(size, 'length')} is above the largest single contact "
                f"{fmt(hi, 'length')} allowed on the {region.name} region "
                f"[{region.provenance['largest_contact'][0]}: "
                f"{region.provenance['largest_contact'][1]}]"
            )
    if shape == "ring":
        wall = (dims["outer_diameter"] - dims["inner_diameter"]) / 2
        if dims["inner_diameter"] <= 0 or wall < lo - _TOL:
            raise ConfigError(
                f"{where}: ring inner_diameter must be positive and leave a wall of at least "
                f"{fmt(lo, 'length')}; got outer {fmt(dims['outer_diameter'], 'length')}, "
                f"inner {fmt(dims['inner_diameter'], 'length')}"
            )
    position = _mapping(data.get("position"), f"{where}.position")
    if set(position) != {"x", "y"}:
        raise ConfigError(f"{where}.position: needs exactly x and y, each with a unit")
    x = parse_quantity(position["x"], "length", f"{where}.position.x")
    y = parse_quantity(position["y"], "length", f"{where}.position.y")
    role = _choice(data.get("role", "active"), ROLES, f"{where}.role")
    share = data.get("current_share")
    if role == "return" and share is not None:
        raise ConfigError(
            f"{where}: is the return, so its current_share is computed (minus the sum of the "
            f"active shares) and cannot be set; leave current_share out"
        )
    if share is None:
        share = 0.0 if role == "unconnected" else None
    elif isinstance(share, bool) or not isinstance(share, (int, float)):
        raise ConfigError(f"{where}.current_share: expected a plain number, got {share!r}")
    if isinstance(share, (int, float)):
        load_model_limits()["current_share"].check(float(share), f"{where}.current_share")
    if role == "unconnected" and share not in (None, 0, 0.0):
        raise ConfigError(f"{where}: an unconnected contact must have current_share 0")
    if role == "active" and share is None:
        raise ConfigError(f"{where}: an active contact needs current_share (-1 to +1)")
    return Contact(cid, shape, dims, x, y, role, 0.0 if share is None else float(share))


def _check_layout_geometry(contacts: list[Contact], region: Region) -> None:
    half_l, half_w = region.length_mm / 2, region.width_mm / 2
    for c in contacts:
        hx, hy = c.half_extents_mm
        if (
            c.x_mm - hx < -half_l - _TOL
            or c.x_mm + hx > half_l + _TOL
            or c.y_mm - hy < -half_w - _TOL
            or c.y_mm + hy > half_w + _TOL
        ):
            raise ConfigError(
                f"contact {c.id!r} does not fit on the {region.name} region: its outline spans "
                f"x {c.x_mm - hx:g} to {c.x_mm + hx:g} mm and y {c.y_mm - hy:g} to "
                f"{c.y_mm + hy:g} mm, but the modeled surface is {region.length_mm:g} x "
                f"{region.width_mm:g} mm (x within +-{half_l:g}, y within +-{half_w:g})"
            )
    gap_lo, _ = region.gap_range()
    for i, a in enumerate(contacts):
        for b in contacts[i + 1 :]:
            d = _edge_distance(a, b)
            if d < 0:
                raise ConfigError(f"contacts {a.id!r} and {b.id!r} overlap")
            if d < gap_lo - _TOL:
                raise ConfigError(
                    f"gap between contacts {a.id!r} and {b.id!r} is {d:g} mm, below the "
                    f"smallest allowed gap {gap_lo:g} mm"
                )


def _check_currents(contacts: list[Contact], return_path: str, amplitude: float) -> list[Contact]:
    """Check roles and current balance. Returns contacts with the return share filled in."""
    returns = [c for c in contacts if c.role == "return"]
    active = [c for c in contacts if c.role == "active"]
    limits = load_model_limits()
    if return_path == "local":
        if returns:
            raise ConfigError(
                "return_path is local but contact "
                f"{returns[0].id!r} has role 'return'; use return_path: distant or role active"
            )
        total = sum(c.current_share for c in active)
        if abs(total) > _TOL:
            raise ConfigError(
                f"currents do not balance: no return contact is defined, so the contact "
                f"current shares must sum to zero, but they sum to {total:g}"
            )
        return contacts
    if len(returns) != 1:
        raise ConfigError(
            f"return_path is distant, which needs exactly one contact with role 'return'; "
            f"found {len(returns)}"
        )
    ret = returns[0]
    balance = -sum(c.current_share for c in active)
    limits["current"].check(abs(balance) * amplitude, f"return contact {ret.id!r} current")
    return [
        Contact(c.id, c.shape, c.dims_mm, c.x_mm, c.y_mm, c.role, balance) if c is ret else c
        for c in contacts
    ]


# ---------------------------------------------------------------- stimulus


def _parse_stimulus(raw: object) -> Stimulus:
    data = _mapping(raw if raw is not None else {}, "stimulus")
    unknown = set(data) - _STIM_KEYS
    if unknown:
        raise ConfigError(f"stimulus: unknown field(s) {sorted(unknown)}")
    limits = load_model_limits()
    shape = _choice(
        data.get("pulse_shape", "biphasic_symmetric"), PULSE_SHAPES, "stimulus.pulse_shape"
    )
    phase = _choice(data.get("leading_phase", "cathodic"), PHASES, "stimulus.leading_phase")
    width = _quantity(data, "pulse_width", "time", "stimulus", "pulse_width")
    gap = _quantity(data, "interphase_gap", "time", "stimulus", "interphase_gap")
    current = _quantity(data, "current", "current", "stimulus", "current")
    rate = _quantity(data, "rate", "frequency", "stimulus", "pulse_rate")
    train = _quantity(data, "train_length", "time", "stimulus", "train_length")
    zero_avg = data.get("zero_average", True)
    if not isinstance(zero_avg, bool):
        raise ConfigError(f"stimulus.zero_average: expected true or false, got {zero_avg!r}")
    sweep = None
    if "pulse_width_sweep" in data:
        s = _mapping(data["pulse_width_sweep"], "stimulus.pulse_width_sweep")
        if set(s) != {"min", "max"}:
            raise ConfigError("stimulus.pulse_width_sweep: needs exactly min and max")
        lo = parse_quantity(s["min"], "time", "stimulus.pulse_width_sweep.min")
        hi = parse_quantity(s["max"], "time", "stimulus.pulse_width_sweep.max")
        limits["pulse_width"].check(lo, "stimulus.pulse_width_sweep.min")
        limits["pulse_width"].check(hi, "stimulus.pulse_width_sweep.max")
        if lo > hi:
            raise ConfigError("stimulus.pulse_width_sweep: min is above max")
        sweep = (lo, hi)
    # One pulse must fit inside one period. Phase count: monophasic 1, biphasic 2. For the
    # asymmetric shape the second phase is not defined in scope.md, so only a lower bound
    # (the same width for both phases) is checked.
    phases = 1 if shape == "monophasic" else 2
    duration = phases * width + (gap if phases == 2 else 0.0)
    if duration > 1.0 / rate + 1e-12:
        raise ConfigError(
            f"stimulus: one pulse ({fmt(duration, 'time')}) does not fit inside one period "
            f"({fmt(1.0 / rate, 'time')} at {rate:g} Hz); lower the rate or the pulse width"
        )
    if sweep is not None:
        longest = phases * sweep[1] + (gap if phases == 2 else 0.0)
        if longest > 1.0 / rate + 1e-12:
            raise ConfigError(
                f"stimulus.pulse_width_sweep.max: at {fmt(sweep[1], 'time')} one pulse "
                f"({fmt(longest, 'time')}) does not fit inside one period "
                f"({fmt(1.0 / rate, 'time')} at {rate:g} Hz); lower the rate or the sweep maximum"
            )
    return Stimulus(shape, phase, width, sweep, gap, current, rate, train, zero_avg)


# ---------------------------------------------------------------- flags


def _compute_flags(layout_contacts: list[Contact], stim: Stimulus, region: Region) -> list[Flag]:
    flags_cfg = load_model_limits().flags
    small = flags_cfg["small_contact_area"].value
    density = flags_cfg["current_density"].value
    flat = flags_cfg["flat_skin_fraction"].value
    flags: list[Flag] = []
    if stim.zero_average and stim.pulse_shape == "monophasic":
        flags.append(
            Flag(
                "net_charge_per_pulse",
                "zero_average is on but a monophasic pulse carries net charge and cannot "
                "average to zero",
            )
        )
    for c in layout_contacts:
        if c.role == "return" and abs(c.current_share) > 1 + _TOL:
            flags.append(
                Flag(
                    "return_share_exceeds_unit",
                    f"return contact {c.id!r} computed current share is {c.current_share:g}; "
                    f"scope.md defines the share per contact as -1 to +1",
                    c.id,
                )
            )
        area = c.area_mm2
        if area < small:
            flags.append(
                Flag(
                    "small_contact",
                    f"contact {c.id!r} area {area:.3g} mm2 is below {small:g} mm2",
                    c.id,
                )
            )
        if c.role != "unconnected":
            amps = abs(stim.current_mA * c.current_share)
            if amps / area > density:
                flags.append(
                    Flag(
                        "current_density",
                        f"contact {c.id!r} current density {amps / area:.3g} mA/mm2 is above "
                        f"{density:g} mA/mm2 (outside the checked range)",
                        c.id,
                    )
                )
        if c.largest_dim_mm > flat * region.shorter_side_mm:
            flags.append(
                Flag(
                    "flat_skin_approximation_poor",
                    f"contact {c.id!r} is {c.largest_dim_mm:g} mm wide, more than half the "
                    f"{region.name} region's shorter side ({region.shorter_side_mm:g} mm)",
                    c.id,
                )
            )
    return flags


# ---------------------------------------------------------------- public API


def parse_layout(
    data: dict,
    *,
    region: str | None = None,
    regions_dir: Path | str | None = None,
    source: str = "layout",
) -> Layout:
    """Validate a layout mapping and return a Layout. `region` overrides the file's region."""
    data = _mapping(data, source)
    unknown = set(data) - _TOP_KEYS
    if unknown:
        raise ConfigError(f"{source}: unknown field(s) {sorted(unknown)}")
    region_name = region or data.get("region")
    if not isinstance(region_name, str):
        raise ConfigError(f"{source}: missing required field 'region'")
    reg = load_region(region_name, regions_dir)
    limits = load_model_limits()
    material = _choice(data.get("material", "stainless_steel"), MATERIALS, "material")
    skin = _choice(
        data.get("skin_condition", reg.default_skin_condition), SKIN_CONDITIONS, "skin_condition"
    )
    drive = data.get("drive", "current")
    if drive != "current":
        raise ConfigError(f"drive: {drive!r} is not supported; the drive is current-controlled")
    vlim = _quantity(data, "driver_voltage_limit", "voltage", "", "driver_voltage_limit")
    return_path = _choice(data.get("return_path", "local"), RETURN_PATHS, "return_path")
    raw_contacts = data.get("contacts")
    if not isinstance(raw_contacts, list) or not raw_contacts:
        raise ConfigError(f"{source}: 'contacts' must be a non-empty list")
    limits["contact_count"].check(len(raw_contacts), "number of contacts")
    contacts = [_parse_contact(raw, i, reg) for i, raw in enumerate(raw_contacts)]
    ids = [c.id for c in contacts]
    if len(set(ids)) != len(ids):
        raise ConfigError(f"{source}: contact ids must be unique, got {ids}")
    _check_layout_geometry(contacts, reg)
    stim = _parse_stimulus(data.get("stimulus"))
    contacts = _check_currents(contacts, return_path, stim.current_mA)
    flags = _compute_flags(contacts, stim, reg)
    return Layout(
        name=str(data.get("name", source)),
        region=reg,
        material=material,
        skin_condition=skin,
        drive=drive,
        driver_voltage_limit_V=vlim,
        return_path=return_path,
        contacts=tuple(contacts),
        stimulus=stim,
        flags=tuple(flags),
    )


def load_layout(
    path: Path | str,
    *,
    region: str | None = None,
    regions_dir: Path | str | None = None,
) -> Layout:
    """Load and validate a layout file. `region` replaces the region named in the file."""
    path = Path(path)
    return parse_layout(_load_yaml(path), region=region, regions_dir=regions_dir, source=path.name)


def default_layout_data(region: str, regions_dir: Path | str | None = None) -> dict:
    """The interface's opening state for a region: two 1.5 mm discs 1 mm apart, +1 and -1."""
    limits = load_model_limits()
    size = limits["contact_size"].default
    gap = limits["contact_gap"].default
    assert size is not None and gap is not None
    reg = load_region(region, regions_dir)
    offset = (size + gap) / 2
    return {
        "name": f"default-{reg.name}",
        "region": reg.name,
        "contacts": [
            {
                "id": "c1",
                "shape": "disc",
                "diameter": f"{size:g} mm",
                "position": {"x": f"{-offset:g} mm", "y": "0 mm"},
                "role": "active",
                "current_share": 1,
            },
            {
                "id": "c2",
                "shape": "disc",
                "diameter": f"{size:g} mm",
                "position": {"x": f"{offset:g} mm", "y": "0 mm"},
                "role": "active",
                "current_share": -1,
            },
        ],
    }
