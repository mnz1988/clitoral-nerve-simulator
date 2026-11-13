# clitoral-nerve-simulator

A plan, and later the code, for simulating the dorsal nerve of the clitoris with free tools and open data.

- **Mode A, electrical stimulation:** finite-element field in tissue driving cable-model axons in NEURON. Biophysical and testable.
- **Mode B, touch:** contact mechanics and receptor filter models driving the same axons. Phenomenological; no human recordings exist to fit it.

Start with [docs/blueprint.md](docs/blueprint.md).

## Status

Planning only. No simulation code yet. The first milestone is an idealized-nerve recruitment model built with [NRV](https://nrv.readthedocs.io/).

## Data

Scan volumes, segmentations and third-party meshes are not stored in this repository. See section 13 of the blueprint.
