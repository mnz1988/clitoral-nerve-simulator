# What NRV can and cannot do for this project (checklist step 1.9)

Checked 2026-11-14 against the **source code of NRV 1.4.0**, commit `7dc11954bfa69291cd5853dd99a99de12f106bef` (dated 2026-04-22), cloned shallowly and read, **not run**. Nothing is installed yet, so every "yes" below means "the code has it", not "tested". The rendered documentation pages (nrv.readthedocs.io) returned only a site index to the fetch tool, so they could not be used.

Base for links: `https://github.com/NRV-framework/NRV/blob/7dc11954bfa69291cd5853dd99a99de12f106bef/`

Labels: **found in code** (read in the file named), **inferred** (from names or docstrings, not confirmed), **not found**.

## 1. Answer to the key question of amendment A-002

NRV is built around a nerve trunk, but its field solver is general enough to be reused for layered skin if the **mesh is our own**. The parts that fit the skin model are reusable; the parts that assume a nerve do not. A reasonable split:

- Use NRV for: the NEURON fibre wrappers and fibre models, the stimulus waveforms, the superposition of contact fields, and (if it works on a custom mesh) the FEniCSx solver wrapper.
- Build ourselves: the layered skin mesh in Gmsh, the surface contacts, the fibre placement and orientation, and fibre models NRV lacks.

## 2. Capability table

| Need | NRV 1.4.0 | Evidence | Status |
|---|---|---|---|
| Install | Linux or macOS; Windows only through WSL2 (Ubuntu 22.xx). Python 3.12, `fenics-dolfinx==0.9.0` from conda, `python-gmsh`, `mpich`; NEURON via `pip install nrv-py`; COMSOL optional and discouraged | README (read through the GitHub page) | found |
| Licence | CeCILL (a French copyleft licence, compatible with GPL). Check against blueprint section 13 before distributing | README badge, `Licence.txt` | found; licence terms not read |
| Our own mesh as the FEM domain | `FEMParameters(mesh_file=...)`; the class says only 3D is implemented | `nrv/fmod/FEM/fenics_utils/_FEMParameters.py` lines 29-78 | found |
| Layered conductivities | `add_domain(mesh_domain, mat_pty / mat_file / mat_perm)` per mesh-domain ID; a single number is isotropic, a list of three is anisotropic. A layer is therefore a Gmsh volume with its own ID | `_FEMParameters.py` lines 146-187 | found (layers via domain IDs: inferred, no skin example exists) |
| Thin interface layers | `add_inboundary(mesh_domain, in_domains, thickness, mat...)`: a thin layer of given thickness and conductivity on an internal surface | `_FEMParameters.py` lines 237-265 | found. Usable for the stratum corneum or an electrode-skin interface instead of meshing it; units and accuracy untested |
| Surface contacts with a set current | Boundary conditions are Dirichlet (voltage) or Neumann (a flux term added to the weak form, so a normal current density) on 2D mesh surfaces. Any contact is a Gmsh surface we label ourselves | `_FEMParameters.py` lines 189-235; `_FEMSimulation.py` lines 396-430 | found; Neumann units must be confirmed when we run it |
| NRV's own electrode types | Point source, LIFE, cuff, multi-polar cuff. All are nerve-shaped; none is a flat skin contact | `nrv/fmod/_electrodes.py` classes at lines 273, 381, 463, 586 | found; **not usable as they are** |
| NRV's own mesh builder | `NerveMshCreator` builds nerve, fascicles, axons and these electrodes; `MshCreator` offers generic Gmsh helpers such as `add_box` | `nrv/fmod/FEM/mesh_creator/` | found; the nerve builder does not give skin |
| One field per contact, scaled by its current, then summed | `electrode.footprint` holds the potential at fibre segments for 1 mA; `compute_vext` multiplies each by the stimulus and adds. `set_footprint` accepts an externally computed array | `_electrodes.py` lines 178-205, 369-378; `_extracellular.py` lines 240-266 | found. **This is exactly our unit-current superposition design and gives a way to inject fields we solve ourselves** |
| Waveforms | Arbitrary stimulus shapes per electrode | README | found |
| Quasistatic field | Yes; no ephaptic coupling | README | found |
| Myelinated fibre models | `MRG`, `Gaines_sensory`, `Gaines_motor` | `nrv/nmod/_myelinated.py` lines 47-51 | found |
| Unmyelinated fibre models | `HH` (squid, warned unsuitable), `Rattay_Aberham`, `Sundt`, `Tigerholm`, and `Schild_94` / `Schild_97` referenced in the code | `nrv/nmod/_unmyelinated.py` lines 36-41, 139-147, 237 | found |
| Skin-specific terminal fibre models (Zhu, Aalborg A-delta and A-beta; blueprint section 6) | No | grep of both fibre files | **not found**: must be written in NEURON ourselves |
| Fibre orientation | "All axons are assumed to be along the x-axis"; a fibre has a position (y, z), a length L and a diameter | `nrv/nmod/_axons.py` line 203; `_myelinated.py` lines 40-46 | found. Fibres perpendicular to the skin surface need the mesh built with the skin normal along x, or a hand-made footprint (see 4) |
| Fibre ending, branching, bend | No terminal ending or branch model; a fibre is a straight cable of finite length | same | **not found** |
| Fibre-in-tissue coupling | Each segment's `e_extracellular` is set from the field; no feedback to the field | `_axons.py` lines 526-538 | found |
| Thin perineurium | Not needed for the skin model; `add_inboundary` covers the trunk case in blueprint section 6 (line about perineurium) | `_FEMParameters.py` | found |

## 3. What this means for the plan

1. **Decision: hybrid.** Build the skin mesh and contacts in Gmsh ourselves, solve with NRV's FEniCSx wrapper if a custom mesh runs through it, otherwise with FEniCSx directly, and feed the results to NRV's fibre and superposition code. Settle this at the first install test (step 2.x), not before.
2. **Aalborg / Zhu fibre models are our work.** NRV does not ship them. They go into NEURON as separate mechanisms.
3. **Fibre endings and orientation are a limit.** Straight cables only. A perpendicular terminal fibre is represented as a straight fibre of finite length along x, with the field supplied by our footprint. Whether that reproduces a real terminal ending is a modelling question for step 3.x and an expert (role C), not something NRV answers.
4. **Footprints are the integration hook.** Because `set_footprint` takes any array of potentials at the fibre segment positions, the field can come from any solver. This also protects the project if NRV's FEM path does not accept a custom mesh.

## 4. Not checked (needs an install, step 2.x)

- Whether a custom Gmsh mesh with our domain and boundary IDs actually runs through `FEMSimulation` end to end.
- Neumann boundary units and the effect of `add_inboundary` thickness on accuracy.
- Whether the d-lambda rule behaves for very short, thin terminal fibres.
- Mesh size limits for a block with a 0.1 mm contact edge (memory and time on this machine).
- Exact licence terms of CeCILL against blueprint section 13.
- The rendered NRV documentation, including any tutorial that does something close to a surface electrode.

## 5. How this was read (to make the next pass cheaper)

- `nrv.readthedocs.io` pages gave the fetch tool only a 300,000-character navigation index. Two attempts (index page, then the user's-guide pages); a third approach, reading the source, worked.
- `git clone --depth 1` of the repository works but its checkout fails on Windows for `docs/html/.doctrees` (file names too long). The `nrv/` source folder is complete anyway. Use a short target path or `git config core.longpaths true` if the docs folder is needed.