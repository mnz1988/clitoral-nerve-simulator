"""Model limits and region presets, both read from YAML files.

Adding a region needs only a new YAML file in sim/config/regions/ (or in a directory passed as
`regions_dir`); no code changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from .errors import ConfigError
from .units import fmt, parse_quantity

LABELS = ("measured", "literature", "assumption")
PACKAGE_DIR = Path(__file__).parent
DEFAULT_REGIONS_DIR = PACKAGE_DIR / "regions"
MODEL_LIMITS_FILE = PACKAGE_DIR / "model_limits.yaml"


def _load_yaml(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as error:
        raise ConfigError(f"{path.name}: not valid YAML: {error}") from error
    if not isinstance(data, dict):
        raise ConfigError(f"{path.name}: expected a mapping at the top level")
    return data


def _check_label(label: object, source: object, where: str) -> None:
    if label not in LABELS:
        raise ConfigError(f"{where}: label must be one of {', '.join(LABELS)}, got {label!r}")
    if not isinstance(source, str) or not source.strip():
        raise ConfigError(f"{where}: a source string is required")


def _num(raw: object, dimension: str, where: str) -> float | None:
    if raw is None:
        return None
    if dimension in ("count", "fraction", "current_density"):
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise ConfigError(f"{where}: expected a plain number, got {raw!r}")
        return float(raw)
    return parse_quantity(raw, dimension, where)


@dataclass(frozen=True)
class Limit:
    """Default and allowed range of one input, with its label and source."""

    name: str
    dimension: str
    default: float | None
    minimum: float | None
    maximum: float | None
    label: str
    source: str
    default_label: str
    default_source: str

    def show(self, value: float) -> str:
        return fmt(value, self.dimension) if self.dimension != "count" else f"{value:g}"

    def check(self, value: float, field: str) -> None:
        """Raise ConfigError with the reason if `value` is outside the model limit."""
        if self.minimum is not None and value < self.minimum - 1e-12:
            raise ConfigError(
                f"{field}: {self.show(value)} is below the minimum {self.show(self.minimum)} "
                f"(model limit [{self.label}]: {self.source})"
            )
        if self.maximum is not None and value > self.maximum + 1e-12:
            raise ConfigError(
                f"{field}: {self.show(value)} is above the maximum {self.show(self.maximum)} "
                f"(model limit [{self.label}]: {self.source})"
            )


@dataclass(frozen=True)
class FlagThreshold:
    name: str
    value: float
    label: str
    source: str


@dataclass(frozen=True)
class ModelLimits:
    limits: dict[str, Limit]
    flags: dict[str, FlagThreshold]

    def __getitem__(self, name: str) -> Limit:
        return self.limits[name]


@lru_cache(maxsize=1)
def load_model_limits() -> ModelLimits:
    data = _load_yaml(MODEL_LIMITS_FILE)
    flags_raw = data.pop("flags", {})
    limits: dict[str, Limit] = {}
    for name, entry in data.items():
        where = f"model_limits.yaml: {name}"
        dimension = entry["dimension"]
        _check_label(entry.get("label"), entry.get("source"), where)
        default_label = entry.get("default_label", entry["label"])
        default_source = entry.get("default_source", entry["source"])
        _check_label(default_label, default_source, where + " (default)")
        limits[name] = Limit(
            name=name,
            dimension=dimension,
            default=_num(entry.get("default"), dimension, where + ".default"),
            minimum=_num(entry.get("min"), dimension, where + ".min"),
            maximum=_num(entry.get("max"), dimension, where + ".max"),
            label=entry["label"],
            source=entry["source"],
            default_label=default_label,
            default_source=default_source,
        )
    flags: dict[str, FlagThreshold] = {}
    for name, entry in flags_raw.items():
        where = f"model_limits.yaml: flags.{name}"
        _check_label(entry.get("label"), entry.get("source"), where)
        flags[name] = FlagThreshold(
            name, _num(entry["value"], entry["dimension"], where), entry["label"], entry["source"]
        )
    return ModelLimits(limits, flags)


@dataclass(frozen=True)
class Region:
    """A body region preset: modeled surface and its own electrode limits."""

    name: str
    length_mm: float
    width_mm: float
    largest_contact_mm: float
    shapes: tuple[str, ...]
    default_skin_condition: str
    contact_size_min_mm: float | None
    gap_min_mm: float | None
    provenance: dict[str, tuple[str, str]]  # field -> (label, source)

    @property
    def shorter_side_mm(self) -> float:
        return min(self.length_mm, self.width_mm)

    def contact_size_range(self) -> tuple[float, float]:
        """Effective (min, max) contact dimension: the tighter of model and region limits."""
        model = load_model_limits()["contact_size"]
        lo = max(model.minimum or 0.0, self.contact_size_min_mm or 0.0)
        hi = self.largest_contact_mm
        if model.maximum is not None:
            hi = min(hi, model.maximum)
        return lo, hi

    def gap_range(self) -> tuple[float, float]:
        """Effective (min, max) gap between contacts."""
        model = load_model_limits()["contact_gap"]
        lo = max(model.minimum or 0.0, self.gap_min_mm or 0.0)
        hi = max(self.length_mm, self.width_mm)
        if model.maximum is not None:
            hi = min(hi, model.maximum)
        return lo, hi


_REGION_KEYS = {
    "name",
    "default_skin_condition",
    "length",
    "width",
    "largest_contact",
    "shapes",
    "contact_size_min",
    "gap_min",
}
SKIN_CONDITIONS = ("dry", "moist", "gelled")
SHAPES = ("disc", "rectangle", "ring")


def _region_field(data: dict, key: str, where: str, dimension: str = "length"):
    if key not in data:
        raise ConfigError(f"{where}: missing required field {key!r}")
    entry = data[key]
    if not isinstance(entry, dict) or "value" not in entry:
        raise ConfigError(f"{where}: {key} must have value, label and source")
    _check_label(entry.get("label"), entry.get("source"), f"{where}: {key}")
    return entry["value"], (entry["label"], entry["source"])


def parse_region(data: dict, expected_name: str, where: str) -> Region:
    unknown = set(data) - _REGION_KEYS
    if unknown:
        raise ConfigError(f"{where}: unknown field(s) {sorted(unknown)}")
    if data.get("name") != expected_name:
        raise ConfigError(f"{where}: name {data.get('name')!r} must equal the file name")
    prov: dict[str, tuple[str, str]] = {}
    values: dict[str, float] = {}
    for key in ("length", "width", "largest_contact"):
        raw, prov[key] = _region_field(data, key, where)
        values[key] = parse_quantity(raw, "length", f"{where}: {key}")
        if values[key] <= 0:
            raise ConfigError(f"{where}: {key} must be positive")
    skin, prov["default_skin_condition"] = _region_field(data, "default_skin_condition", where)
    if skin not in SKIN_CONDITIONS:
        raise ConfigError(f"{where}: default_skin_condition must be one of {SKIN_CONDITIONS}")
    shapes = data.get("shapes")
    if not isinstance(shapes, list) or not shapes or not set(shapes) <= set(SHAPES):
        raise ConfigError(f"{where}: shapes must be a non-empty list from {SHAPES}")
    optional: dict[str, float | None] = {"contact_size_min": None, "gap_min": None}
    for key in optional:
        if key in data:
            raw, prov[key] = _region_field(data, key, where)
            optional[key] = parse_quantity(raw, "length", f"{where}: {key}")
    return Region(
        name=expected_name,
        length_mm=values["length"],
        width_mm=values["width"],
        largest_contact_mm=values["largest_contact"],
        shapes=tuple(shapes),
        default_skin_condition=skin,
        contact_size_min_mm=optional["contact_size_min"],
        gap_min_mm=optional["gap_min"],
        provenance=prov,
    )


def available_regions(regions_dir: Path | str | None = None) -> list[str]:
    directory = Path(regions_dir) if regions_dir is not None else DEFAULT_REGIONS_DIR
    return sorted(path.stem for path in directory.glob("*.yaml"))


def load_region(name: str, regions_dir: Path | str | None = None) -> Region:
    directory = Path(regions_dir) if regions_dir is not None else DEFAULT_REGIONS_DIR
    path = directory / f"{name}.yaml"
    if not path.is_file():
        raise ConfigError(
            f"region {name!r} has no preset file; available regions: "
            f"{', '.join(available_regions(directory)) or 'none'}"
        )
    return parse_region(_load_yaml(path), name, path.name)
