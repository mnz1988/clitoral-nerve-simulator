# clitoral-nerve-simulator

A plan, and later the code, for simulating the dorsal nerve of the clitoris with free tools and open data.

- **Mode A, electrical stimulation:** finite-element field in tissue driving cable-model axons in NEURON. Biophysical and testable.
- **Mode B, touch:** contact mechanics and receptor filter models driving the same axons. Phenomenological; no human recordings exist to fit it.

## Where to start

1. [docs/blueprint.md](docs/blueprint.md): the plan.
2. `checklist/index.html`: open it in a browser. It lists every step with what to do, what to download or find, how to verify it, who should review it, and which AI model and tools fit it.
3. [docs/amendments.md](docs/amendments.md): how the plan changes when a new problem turns up.
4. [CLAUDE.md](CLAUDE.md): working rules for AI agents in this repository.

## Status

Planning only. No simulation code yet. The first milestone is an idealized-nerve recruitment model built with [NRV](https://nrv.readthedocs.io/).

## Data

Scan volumes, segmentations and third-party meshes are not stored in this repository. See section 13 of the blueprint.
