"""Parsing of quantities that must be written with a unit, e.g. "1.5 mm".

Canonical units after parsing: length mm, area mm2, time s, current mA, frequency Hz,
voltage V. A bare number where a unit is required is rejected.
"""

from __future__ import annotations

import re

from .errors import ConfigError

_UNITS: dict[str, dict[str, float]] = {
    "length": {"mm": 1.0, "cm": 10.0, "m": 1000.0, "um": 1e-3, "µm": 1e-3, "μm": 1e-3},
    "area": {"mm2": 1.0, "mm²": 1.0, "cm2": 100.0, "cm²": 100.0},
    "time": {"s": 1.0, "ms": 1e-3, "us": 1e-6, "µs": 1e-6, "μs": 1e-6},
    "current": {"mA": 1.0, "A": 1000.0, "uA": 1e-3, "µA": 1e-3, "μA": 1e-3},
    "frequency": {"Hz": 1.0, "kHz": 1000.0},
    "voltage": {"V": 1.0, "mV": 1e-3, "kV": 1000.0},
}
CANONICAL = {
    "length": "mm",
    "area": "mm2",
    "time": "s",
    "current": "mA",
    "frequency": "Hz",
    "voltage": "V",
}
_PATTERN = re.compile(r"^\s*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)\s*(\S*)\s*$")


def parse_quantity(value: object, dimension: str, field: str) -> float:
    """Return `value` in the canonical unit of `dimension`, or raise ConfigError.

    `value` must be a string such as "200 us". Numbers without a unit are rejected.
    """
    units = _UNITS[dimension]
    allowed = ", ".join(units)
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ConfigError(f"{field}: expected a quantity with a unit ({allowed}), got {value!r}")
    if not isinstance(value, str):
        raise ConfigError(f"{field}: value {value!r} has no unit; write it with one ({allowed})")
    match = _PATTERN.match(value)
    if match is None:
        raise ConfigError(f"{field}: cannot read {value!r} as a number with a unit ({allowed})")
    number, unit = float(match.group(1)), match.group(2)
    if not unit:
        raise ConfigError(f"{field}: value {value!r} has no unit; write it with one ({allowed})")
    if unit not in units:
        raise ConfigError(f"{field}: unit {unit!r} is not a {dimension} unit ({allowed})")
    return number * units[unit]


def fmt(value: float, dimension: str) -> str:
    """Format a canonical value for messages."""
    if dimension == "time":
        if abs(value) < 1e-3 and value != 0:
            return f"{value * 1e6:g} us"
        if abs(value) < 1 and value != 0:
            return f"{value * 1e3:g} ms"
    unit = CANONICAL.get(dimension, "")
    return f"{value:g} {unit}".strip()
