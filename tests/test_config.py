"""Tests for the electrode and stimulus configuration schema (checklist step 2.4)."""

from __future__ import annotations

import copy
import shutil
from pathlib import Path

import pytest
import yaml

from sim.config import (
    ConfigError,
    available_regions,
    default_layout_data,
    load_layout,
    load_model_limits,
    load_region,
    parse_layout,
)
from sim.config.limits import DEFAULT_REGIONS_DIR, LABELS

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = sorted((ROOT / "examples" / "layouts").glob("T*.yaml"))


def pair(region: str = "forearm", **over) -> dict:
    """Two 2 mm discs 3 mm apart with balanced currents; edit with keyword overrides."""
    data = {
        "region": region,
        "contacts": [
            {
                "id": "a",
                "shape": "disc",
                "diameter": "2 mm",
                "position": {"x": "-2.5 mm", "y": "0 mm"},
                "role": "active",
                "current_share": 1,
            },
            {
                "id": "b",
                "shape": "disc",
                "diameter": "2 mm",
                "position": {"x": "2.5 mm", "y": "0 mm"},
                "role": "active",
                "current_share": -1,
            },
        ],
        "stimulus": {},
    }
    data.update(over)
    return copy.deepcopy(data)


def rejects(data: dict, *fragments: str, **kwargs) -> str:
    with pytest.raises(ConfigError) as info:
        parse_layout(data, **kwargs)
    message = str(info.value)
    for fragment in fragments:
        assert fragment in message, message
    return message


# ------------------------------------------------------------ examples


def test_six_examples_present():
    assert [p.name[:2] for p in EXAMPLES] == ["T1", "T2", "T3", "T4", "T5", "T6"]


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_example_loads(path):
    layout = load_layout(path)
    assert layout.contacts
    assert layout.drive == "current"


def test_t5_equals_default_interface_state():
    t5 = load_layout(ROOT / "examples" / "layouts" / "T5_glans_pair.yaml")
    default = parse_layout(default_layout_data("glans"))
    assert t5.contacts == default.contacts
    assert t5.stimulus == default.stimulus
    assert (t5.material, t5.skin_condition) == (default.material, default.skin_condition)
    assert default.driver_voltage_limit_V == 150


def test_t5_has_the_small_contact_flag_and_nothing_else():
    layout = load_layout(ROOT / "examples" / "layouts" / "T5_glans_pair.yaml")
    assert {f.name for f in layout.flags} == {"small_contact"}


# ------------------------------------------------------------ data labels


def test_every_limit_and_region_value_has_label_and_source():
    limits = load_model_limits()
    for limit in limits.limits.values():
        assert limit.label in LABELS and limit.source
        assert limit.default_label in LABELS and limit.default_source
    for flag in limits.flags.values():
        assert flag.label in LABELS and flag.source
    for name in available_regions():
        region = load_region(name)
        for label, source in region.provenance.values():
            assert label in LABELS and source


def test_four_regions_with_expected_sizes():
    assert available_regions() == ["fingertip", "forearm", "glans", "hood"]
    glans = load_region("glans")
    assert (glans.length_mm, glans.width_mm, glans.largest_contact_mm) == (6.4, 5.1, 5)
    assert load_region("forearm").default_skin_condition == "gelled"
    assert load_region("hood").default_skin_condition == "dry"


# ------------------------------------------------------------ units


@pytest.mark.parametrize(
    "path, value",
    [
        (("contacts", 0, "diameter"), 2),
        (("contacts", 0, "position", "x"), -2.5),
        (("stimulus", "pulse_width"), 200),
        (("stimulus", "current"), 0.5),
        (("stimulus", "rate"), 50),
        (("stimulus", "interphase_gap"), 0),
        (("stimulus", "train_length"), 1),
        (("driver_voltage_limit",), 150),
        (("contacts", 0, "diameter"), "2"),
    ],
)
def test_missing_unit_is_rejected(path, value):
    data = pair()
    if path == ("driver_voltage_limit",):
        data["driver_voltage_limit"] = value
    else:
        target = data
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    rejects(data, "no unit")


def test_wrong_kind_of_unit_is_rejected():
    data = pair()
    data["stimulus"]["current"] = "5 V"
    rejects(data, "stimulus.current", "not a current unit")


def test_units_are_converted():
    data = pair()
    data["stimulus"].update(pulse_width="0.2 ms", rate="0.05 kHz", current="500 uA")
    layout = parse_layout(data)
    assert layout.stimulus.pulse_width_s == pytest.approx(200e-6)
    assert layout.stimulus.rate_Hz == pytest.approx(50)
    assert layout.stimulus.current_mA == pytest.approx(0.5)


# ------------------------------------------------------------ input limits


@pytest.mark.parametrize(
    "key, value, fragment",
    [
        ("pulse_width", "5 us", "below the minimum 10 us"),
        ("pulse_width", "20 ms", "above the maximum 10 ms"),
        ("interphase_gap", "2 ms", "above the maximum 1 ms"),
        ("current", "11 mA", "above the maximum 10 mA"),
        ("rate", "2 kHz", "above the maximum 1000 Hz"),
        ("rate", "0.5 Hz", "below the minimum 1 Hz"),
        ("train_length", "10 s", "above the maximum 5 s"),
        ("train_length", "0.01 s", "below the minimum 50 ms"),
    ],
)
def test_stimulus_value_outside_limit_is_rejected_with_reason(key, value, fragment):
    data = pair()
    data["stimulus"][key] = value
    rejects(data, f"stimulus.{key}", fragment, "model limit")


def test_driver_voltage_limit_range():
    for bad, fragment in (("4 V", "below the minimum 5 V"), ("301 V", "above the maximum 300 V")):
        rejects(pair(driver_voltage_limit=bad), "driver_voltage_limit", fragment)
    assert parse_layout(pair(driver_voltage_limit="60 V")).driver_voltage_limit_V == 60


def test_pulse_must_fit_in_one_period():
    data = pair()
    data["stimulus"].update(pulse_width="5 ms", rate="100 Hz")  # biphasic 10 ms = period
    parse_layout(data)
    data["stimulus"]["pulse_width"] = "6 ms"
    rejects(data, "does not fit inside one period")
    data["stimulus"].update(pulse_shape="monophasic")
    parse_layout(data)


def test_interphase_gap_counts_in_the_period_check():
    data = pair()
    data["stimulus"].update(pulse_width="4.6 ms", rate="100 Hz")  # 9.2 ms of 10 ms
    parse_layout(data)
    data["stimulus"]["interphase_gap"] = "1 ms"  # 10.2 ms of 10 ms
    rejects(data, "does not fit inside one period")
    data["stimulus"]["pulse_width"] = "4.5 ms"  # exactly 10 ms of 10 ms
    parse_layout(data)


def test_pulse_width_sweep_limit_and_period():
    data = pair()
    data["stimulus"].update(pulse_width="1 ms", rate="10 Hz")
    data["stimulus"]["pulse_width_sweep"] = {"min": "1 ms", "max": "20 ms"}
    rejects(data, "pulse_width_sweep.max", "above the maximum 10 ms", "model limit")
    data["stimulus"]["pulse_width_sweep"] = {"min": "5 us", "max": "1 ms"}
    rejects(data, "pulse_width_sweep.min", "below the minimum 10 us")
    data["stimulus"]["pulse_width_sweep"] = {"min": "2 ms", "max": "1 ms"}
    rejects(data, "min is above max")
    # biphasic 100 Hz, sweep up to 10 ms: a 20 ms pulse in a 10 ms period
    data["stimulus"].update(pulse_width="1 ms", rate="100 Hz")
    data["stimulus"]["pulse_width_sweep"] = {"min": "1 ms", "max": "10 ms"}
    rejects(data, "pulse_width_sweep.max", "does not fit inside one period", "20 ms", "10 ms")
    # the interphase gap counts for the sweep too: 2 x 4.6 ms + 1 ms = 10.2 ms
    data["stimulus"].update(interphase_gap="1 ms")
    data["stimulus"]["pulse_width_sweep"] = {"min": "1 ms", "max": "4.6 ms"}
    rejects(data, "pulse_width_sweep.max", "does not fit inside one period")
    data["stimulus"]["pulse_width_sweep"] = {"min": "1 ms", "max": "4.5 ms"}  # exactly 10 ms
    parse_layout(data)
    # monophasic has one phase: a 10 ms sweep maximum fits in the 20 ms period at 50 Hz
    data["stimulus"].update(pulse_shape="monophasic", interphase_gap="0 us", rate="50 Hz")
    data["stimulus"]["pulse_width_sweep"] = {"min": "1 ms", "max": "10 ms"}
    parse_layout(data)


def test_contact_count_limits():
    data = pair()
    data["contacts"] = [
        {
            "id": f"c{i}",
            "shape": "disc",
            "diameter": "1 mm",
            "position": {"x": f"{(i - 8.5) * 3} mm", "y": "0 mm"},
            "role": "unconnected",
        }
        for i in range(17)
    ]
    rejects(data, "number of contacts", "above the maximum 16")
    data["contacts"] = []
    rejects(data, "non-empty list")


def test_small_contact_below_model_minimum_is_rejected():
    data = pair()
    data["contacts"][0]["diameter"] = "0.1 mm"
    rejects(data, "contact 'a'", "below the smallest allowed contact 0.2 mm", "model limit")


def test_negative_current_is_rejected():
    data = pair()
    data["stimulus"]["current"] = "-1 mA"
    rejects(data, "stimulus.current", "below the minimum 0 mA", "model limit")
    data["stimulus"]["current"] = "0 mA"
    parse_layout(data)


def test_unknown_contact_field_is_rejected():
    data = pair()
    data["contacts"][0]["colour"] = "red"
    rejects(data, "contacts[0]", "unknown field", "colour")
    data = pair()
    data["stimulus"]["wobble"] = 1
    rejects(data, "stimulus", "unknown field", "wobble")


def test_current_share_range():
    data = pair()
    data["contacts"][0]["current_share"] = 1.5
    rejects(data, "current_share", "above the maximum 1")


def test_choice_fields_are_validated():
    rejects(pair(material="lead"), "material", "stainless_steel")
    rejects(pair(skin_condition="wet"), "skin_condition", "dry, moist, gelled")
    rejects(pair(drive="voltage"), "current-controlled")
    rejects(pair(region="knee"), "region 'knee' has no preset file", "glans")
    data = pair()
    data["stimulus"]["pulse_shape"] = "triangle"
    rejects(data, "pulse_shape")
    data["stimulus"] = {"leading_phase": "left"}
    rejects(data, "leading_phase")
    rejects(pair(typo=1), "unknown field")


def test_all_five_materials_accepted():
    for material in ("stainless_steel", "copper", "silver", "gold", "titanium"):
        assert parse_layout(pair(material=material)).material == material


# ------------------------------------------------------------ region limits and fit


def test_effective_contact_range_is_the_tighter_limit():
    assert load_region("glans").contact_size_range() == (0.2, 5)
    assert load_region("forearm").contact_size_range() == (0.2, 60)
    assert load_region("hood").gap_range()[0] == 0.2


def test_contact_larger_than_region_maximum_is_rejected():
    data = pair("glans")
    data["contacts"][0]["diameter"] = "6 mm"
    rejects(data, "above the largest single contact 5 mm", "glans")
    data = pair("forearm")
    data["contacts"][0]["diameter"] = "6 mm"
    data["contacts"][0]["position"]["x"] = "-10 mm"
    parse_layout(data)


def test_same_layout_accepted_on_forearm_and_rejected_on_glans():
    t1 = ROOT / "examples" / "layouts" / "T1_forearm_patch.yaml"
    assert load_layout(t1).region.name == "forearm"
    message = rejects(yaml.safe_load(t1.read_text(encoding="utf-8")), "glans", region="glans")
    assert "above the largest single contact 5 mm" in message
    with pytest.raises(ConfigError, match="glans"):
        load_layout(t1, region="glans")


def test_grid_that_fits_forearm_but_not_glans_by_layout():
    """Each contact is small enough for the glans, but the whole layout does not fit."""
    data = pair("forearm")
    data["contacts"] = [
        {
            "id": f"c{i}",
            "shape": "disc",
            "diameter": "1.5 mm",
            "position": {"x": f"{(i - 2) * 2.5} mm", "y": "0 mm"},
            "role": "active",
            "current_share": 1 if i % 2 == 0 else -1,
        }
        for i in range(6)
    ]
    assert parse_layout(data).region.name == "forearm"
    message = rejects(data, "does not fit on the glans region", region="glans")
    assert "6.4 x 5.1 mm" in message


def test_contact_off_the_surface_is_rejected():
    data = pair("glans")
    data["contacts"][0]["position"]["x"] = "-1.2 mm"
    data["contacts"][1]["position"]["x"] = "3 mm"
    rejects(data, "contact 'b' does not fit on the glans region")


def test_contact_off_the_surface_in_y_is_rejected():
    """Glans is 6.4 x 5.1 mm: y must stay within +-2.55 mm; the x range is fine here."""
    data = pair("glans")
    data["contacts"][0]["position"]["x"] = "-1.5 mm"
    data["contacts"][1]["position"]["x"] = "1.5 mm"
    data["contacts"][0]["position"]["y"] = "1.6 mm"  # top edge 2.6 mm, above 2.55 mm
    rejects(data, "contact 'a' does not fit on the glans region", "y ")
    data["contacts"][0]["position"]["y"] = "-1.6 mm"  # bottom edge -2.6 mm
    rejects(data, "contact 'a' does not fit on the glans region")
    data["contacts"][0]["position"]["y"] = "1.5 mm"  # top edge 2.5 mm fits
    parse_layout(data)


def test_shape_not_offered_on_region_is_rejected(tmp_path):
    preset = yaml.safe_load((DEFAULT_REGIONS_DIR / "forearm.yaml").read_text(encoding="utf-8"))
    preset["shapes"] = ["disc"]
    (tmp_path / "forearm.yaml").write_text(yaml.safe_dump(preset), encoding="utf-8")
    data = pair("forearm")
    data["contacts"][0].update(shape="ring", outer_diameter="4 mm", inner_diameter="2 mm")
    del data["contacts"][0]["diameter"]
    rejects(data, "not offered on the forearm region", regions_dir=tmp_path)
    parse_layout(data)  # the real preset offers rings


def test_rectangle_and_ring_contacts():
    data = pair("forearm")
    data["contacts"][0] = {
        "id": "a",
        "shape": "rectangle",
        "length": "4 mm",
        "width": "2 mm",
        "position": {"x": "-5 mm", "y": "0 mm"},
        "current_share": 1,
    }
    data["contacts"][1] = {
        "id": "b",
        "shape": "ring",
        "outer_diameter": "6 mm",
        "inner_diameter": "3 mm",
        "position": {"x": "5 mm", "y": "0 mm"},
        "current_share": -1,
    }
    layout = parse_layout(data)
    assert layout.contacts[0].area_mm2 == pytest.approx(8)
    assert layout.contacts[1].area_mm2 == pytest.approx(3.14159265 * 27 / 4)
    data["contacts"][1]["inner_diameter"] = "5.8 mm"
    rejects(data, "ring", "wall")
    data["contacts"][1].update(inner_diameter="3 mm", diameter="2 mm")
    rejects(data, "do not apply to a ring")


# ------------------------------------------------------------ overlap, gap, balance


def test_overlapping_contacts_are_rejected():
    data = pair()
    data["contacts"][1]["position"]["x"] = "-1.5 mm"  # centres 1 mm apart, radii 1 mm each
    rejects(data, "overlap", "'a'", "'b'")


def test_overlap_of_disc_and_rectangle_and_two_rectangles():
    data = pair("forearm")
    data["contacts"][0] = {
        "id": "a",
        "shape": "rectangle",
        "length": "10 mm",
        "width": "10 mm",
        "position": {"x": "0 mm", "y": "0 mm"},
        "current_share": 1,
    }
    data["contacts"][1]["position"]["x"] = "5.5 mm"  # disc edge at 4.5 mm, inside the rectangle
    rejects(data, "overlap")
    data["contacts"][1] = dict(data["contacts"][0], id="b", current_share=-1)
    data["contacts"][1]["position"] = {"x": "5 mm", "y": "5 mm"}
    rejects(data, "overlap")
    data["contacts"][1]["position"] = {"x": "11 mm", "y": "11 mm"}
    parse_layout(data)


def test_gap_below_minimum_is_rejected():
    data = pair()
    data["contacts"][1]["position"]["x"] = "-0.4 mm"  # edge gap 0.1 mm... (2.1 - 2.0 mm)
    data["contacts"][0]["position"]["x"] = "-2.5 mm"
    data["contacts"][1]["position"]["x"] = "-0.4 mm"
    rejects(data, "gap between contacts 'a' and 'b'", "below the smallest allowed gap 0.2 mm")


def test_currents_that_do_not_sum_to_zero_are_rejected():
    data = pair()
    data["contacts"][1]["current_share"] = -0.5
    rejects(data, "currents do not balance", "no return contact", "0.5")


def test_single_contact_with_current_needs_a_return():
    data = pair()
    data["contacts"] = data["contacts"][:1]
    rejects(data, "currents do not balance")


def test_distant_return_balances_automatically():
    layout = load_layout(ROOT / "examples" / "layouts" / "T2_forearm_disc.yaml")
    ret = [c for c in layout.contacts if c.role == "return"][0]
    assert ret.current_share == -1
    assert layout.contact_current_mA(ret) == pytest.approx(-0.5)


def test_role_and_return_path_consistency():
    data = pair(return_path="distant")
    rejects(data, "exactly one contact with role 'return'")
    data = pair()
    data["contacts"][1].update(role="return")
    del data["contacts"][1]["current_share"]
    rejects(data, "return_path is local")
    data = pair(return_path="distant")
    data["contacts"][1].update(role="return", current_share=0.3)
    rejects(data, "is the return", "cannot be set", "leave current_share out")
    data["contacts"][1]["current_share"] = -1  # even the value the program would compute
    rejects(data, "is the return", "cannot be set")
    del data["contacts"][1]["current_share"]
    layout = parse_layout(data)
    assert layout.contacts[1].current_share == -1
    data["contacts"][0]["role"] = "unconnected"
    data["contacts"][0]["current_share"] = 0.5
    rejects(data, "unconnected contact must have current_share 0")
    data = pair()
    del data["contacts"][0]["current_share"]
    rejects(data, "active contact needs current_share")
    data["contacts"][0]["role"] = "boss"
    rejects(data, "role")


def test_return_current_over_the_limit_is_rejected():
    data = pair(return_path="distant")
    data["stimulus"]["current"] = "5 mA"
    data["contacts"] = [
        {
            "id": f"c{i}",
            "shape": "disc",
            "diameter": "2 mm",
            "position": {"x": f"{(i - 1) * 5} mm", "y": "0 mm"},
            "role": "active",
            "current_share": 1,
        }
        for i in range(3)
    ] + [
        {
            "id": "r",
            "shape": "disc",
            "diameter": "2 mm",
            "position": {"x": "30 mm", "y": "0 mm"},
            "role": "return",
        }
    ]
    rejects(data, "return contact 'r' current", "above the maximum 10 mA")


def test_duplicate_contact_ids_and_missing_fields():
    data = pair()
    data["contacts"][1]["id"] = "a"
    rejects(data, "ids must be unique")
    data = pair()
    del data["contacts"][0]["position"]
    rejects(data, "position")
    data = pair()
    del data["region"]
    rejects(data, "missing required field 'region'")


# ------------------------------------------------------------ flags


def test_small_contact_flag_threshold():
    data = pair("forearm")
    data["contacts"][0]["diameter"] = "3.6 mm"  # 10.18 mm2, not small
    data["contacts"][1]["diameter"] = "3.5 mm"  # 9.62 mm2, small
    names = {(f.name, f.contact) for f in parse_layout(data).flags}
    assert ("small_contact", "b") in names
    assert ("small_contact", "a") not in names


def test_current_density_flag():
    data = pair("forearm")
    data["stimulus"]["current"] = "3 mA"  # 3 mA on a 3.14 mm2 disc is about 0.95 mA/mm2
    assert "current_density" not in {f.name for f in parse_layout(data).flags}
    data["stimulus"]["current"] = "3.5 mA"
    flags = parse_layout(data).flags
    assert {f.contact for f in flags if f.name == "current_density"} == {"a", "b"}


def test_flag_boundaries_are_not_flagged():
    """Area exactly 10 mm2 and current density exactly 1.0 mA/mm2 are inside the limits."""
    data = pair("forearm")
    for contact in data["contacts"]:
        contact.update(shape="rectangle", length="4 mm", width="2.5 mm")
        del contact["diameter"]
    data["contacts"][0]["position"]["x"] = "-3 mm"
    data["contacts"][1]["position"]["x"] = "3 mm"
    data["stimulus"]["current"] = "10 mA"
    layout = parse_layout(data)
    assert layout.contacts[0].area_mm2 == 10
    assert layout.flags == ()
    data["stimulus"]["current"] = "10.1 mA"  # density 1.01 mA/mm2 but above the 10 mA limit
    rejects(data, "above the maximum 10 mA")
    data["contacts"][0]["width"] = "2.4 mm"  # 9.6 mm2, density 1.04 mA/mm2
    data["stimulus"]["current"] = "10 mA"
    names = {f.name for f in parse_layout(data).flags}
    assert {"small_contact", "current_density"} <= names


def test_monophasic_with_zero_average_gets_the_net_charge_flag():
    data = pair()
    data["stimulus"]["pulse_shape"] = "monophasic"
    layout = parse_layout(data)  # accepted, not rejected
    flag = [f for f in layout.flags if f.name == "net_charge_per_pulse"]
    assert len(flag) == 1
    assert "monophasic" in flag[0].message and "zero" in flag[0].message
    data["stimulus"]["zero_average"] = False
    assert "net_charge_per_pulse" not in {f.name for f in parse_layout(data).flags}
    data["stimulus"].update(pulse_shape="biphasic_symmetric", zero_average=True)
    assert "net_charge_per_pulse" not in {f.name for f in parse_layout(data).flags}


def test_t1_shows_the_net_charge_flag():
    layout = load_layout(ROOT / "examples" / "layouts" / "T1_forearm_patch.yaml")
    assert "net_charge_per_pulse" in {f.name for f in layout.flags}


def test_return_share_beyond_unit_is_flagged_not_changed():
    data = pair(return_path="distant")
    data["contacts"][1].update(role="return")
    del data["contacts"][1]["current_share"]
    assert "return_share_exceeds_unit" not in {f.name for f in parse_layout(data).flags}
    data["contacts"].insert(
        1,
        {
            "id": "a2",
            "shape": "disc",
            "diameter": "2 mm",
            "position": {"x": "0 mm", "y": "5 mm"},
            "role": "active",
            "current_share": 1,
        },
    )
    layout = parse_layout(data)
    ret = [c for c in layout.contacts if c.role == "return"][0]
    assert ret.current_share == -2  # the rule is unchanged
    flag = [f for f in layout.flags if f.name == "return_share_exceeds_unit"]
    assert len(flag) == 1 and flag[0].contact == "b"
    assert "-2" in flag[0].message and "-1 to +1" in flag[0].message


def test_t3_includes_the_150_mm2_reference_and_everything_fits():
    layout = load_layout(ROOT / "examples" / "layouts" / "T3_fingertip_pads.yaml")
    assert len(layout.contacts) == 7
    ref = [c for c in layout.contacts if c.role == "return"]
    assert len(ref) == 1 and ref[0].area_mm2 == pytest.approx(150)
    assert ref[0].current_share == -1
    pads = [c for c in layout.contacts if c.role != "return"]
    assert len(pads) == 6
    assert all(c.area_mm2 == pytest.approx(11, abs=0.01) for c in pads)


def test_flat_skin_flag_on_glans_only():
    data = pair("glans")
    data["contacts"][0].update(diameter="2.6 mm", position={"x": "-1.55 mm", "y": "0 mm"})
    data["contacts"][1].update(diameter="2 mm", position={"x": "1.8 mm", "y": "0 mm"})
    flagged = {f.contact for f in parse_layout(data).flags if f.name.startswith("flat_skin")}
    assert flagged == {"a"}  # 2.6 mm is above half of 5.1 mm; 2 mm is not
    big = pair("forearm")
    big["contacts"][0]["diameter"] = "2.6 mm"
    assert not [f for f in parse_layout(big).flags if f.name.startswith("flat_skin")]


def test_flags_never_change_values_or_refuse():
    layout = load_layout(ROOT / "examples" / "layouts" / "T4_fingertip_lines.yaml")
    assert {f.name for f in layout.flags} >= {"small_contact", "flat_skin_approximation_poor"}
    assert len(layout.contacts) == 8


def test_no_driver_voltage_flag_in_this_step():
    for path in EXAMPLES:
        assert "driver_cannot_deliver" not in {f.name for f in load_layout(path).flags}


# ------------------------------------------------------------ adding a region


def test_adding_a_region_needs_only_a_preset_file(tmp_path):
    regions = tmp_path / "regions"
    regions.mkdir()
    for name in available_regions():
        shutil.copy(DEFAULT_REGIONS_DIR / f"{name}.yaml", regions / f"{name}.yaml")
    assert "thigh" not in available_regions(regions)
    rejects(pair("thigh"), "no preset file", regions_dir=regions)
    preset = {
        "name": "thigh",
        "default_skin_condition": {"value": "dry", "label": "assumption", "source": "test"},
        "length": {"value": "30 cm", "label": "assumption", "source": "test"},
        "width": {"value": "10 cm", "label": "assumption", "source": "test"},
        "largest_contact": {"value": "40 mm", "label": "assumption", "source": "test"},
        "shapes": ["disc", "rectangle"],
        "gap_min": {"value": "0.5 mm", "label": "assumption", "source": "test"},
    }
    (regions / "thigh.yaml").write_text(yaml.safe_dump(preset), encoding="utf-8")
    assert "thigh" in available_regions(regions)
    layout = parse_layout(pair("thigh"), regions_dir=regions)
    assert layout.region.name == "thigh"
    assert layout.skin_condition == "dry"
    assert layout.region.gap_range()[0] == 0.5  # region gap limit is tighter than the model's
    # The new region's own limits apply.
    data = pair("thigh")
    data["contacts"][0]["diameter"] = "45 mm"
    rejects(data, "above the largest single contact 40 mm", "thigh", regions_dir=regions)
    data = pair("thigh")
    data["contacts"][1]["position"]["x"] = "-0.2 mm"
    data["contacts"][0]["position"]["x"] = "-2.5 mm"
    data["contacts"][1]["position"]["x"] = "-0.2 mm"
    rejects(data, "below the smallest allowed gap 0.5 mm", regions_dir=regions)
    # The shipped regions are untouched.
    assert "thigh" not in available_regions()


def test_bad_preset_files_are_rejected(tmp_path):
    good = yaml.safe_load((DEFAULT_REGIONS_DIR / "glans.yaml").read_text(encoding="utf-8"))
    cases = {
        "nolabel": ({"length": {"value": "6 mm", "source": "x"}}, "label"),
        "nounit": ({"length": {"value": 6, "label": "measured", "source": "x"}}, "no unit"),
        "nosource": ({"width": {"value": "5 mm", "label": "measured", "source": ""}}, "source"),
        "extra": ({"colour": "red"}, "unknown field"),
    }
    for name, (change, fragment) in cases.items():
        preset = dict(good, name=name, **change)
        (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump(preset), encoding="utf-8")
        with pytest.raises(ConfigError, match=fragment):
            load_region(name, tmp_path)
    (tmp_path / "wrongname.yaml").write_text(yaml.safe_dump(dict(good)), encoding="utf-8")
    with pytest.raises(ConfigError, match="must equal the file name"):
        load_region("wrongname", tmp_path)
