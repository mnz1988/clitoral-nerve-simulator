"""Electrode and stimulus configuration: schema, region presets, validation, flags.

See docs/scope.md section 5. Presets live in sim/config/regions/*.yaml; model limits and
defaults in sim/config/model_limits.yaml.
"""

from .errors import ConfigError
from .layout import (
    Contact,
    Flag,
    Layout,
    Stimulus,
    default_layout_data,
    load_layout,
    parse_layout,
)
from .limits import Region, available_regions, load_model_limits, load_region

__all__ = [
    "ConfigError",
    "Contact",
    "Flag",
    "Layout",
    "Region",
    "Stimulus",
    "available_regions",
    "default_layout_data",
    "load_layout",
    "load_model_limits",
    "load_region",
    "parse_layout",
]
