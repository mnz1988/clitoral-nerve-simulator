"""Smoke tests: the installed software matches what environment.yml pins.

Checklist step 2.3. These tests run no simulation; they only import the packages and compare
versions, so they take seconds.
"""

import re
from pathlib import Path

import pytest

ENV_FILE = Path(__file__).resolve().parents[1] / "environment.yml"


def pinned(name: str) -> str:
    """Return the version pinned for `name` in environment.yml (conda `=` or pip `==`)."""
    text = ENV_FILE.read_text(encoding="utf-8")
    match = re.search(rf"^\s*-\s*{re.escape(name)}==?([\w.]+)\s*$", text, re.MULTILINE)
    assert match, f"{name} is not pinned in environment.yml"
    return match.group(1)


def test_environment_file_exists():
    assert ENV_FILE.is_file()


def test_nrv_version_matches_pin():
    import nrv

    assert nrv.__version__ == pinned("nrv-py")


def test_dolfinx_version_matches_pin():
    import dolfinx

    assert dolfinx.__version__ == pinned("fenics-dolfinx")


def test_gmsh_importable():
    gmsh = pytest.importorskip("gmsh")
    assert gmsh.__version__ == pinned("python-gmsh")


def test_neuron_version_matches_pin():
    import neuron

    assert neuron.__version__ == pinned("neuron")
