# Blueprint: a biophysical simulator of the dorsal nerve of the clitoris

Free tools and open data only. Version 2 (corrected), 2026-11-13.

This replaces an earlier draft. The backbone of that draft was sound: geometry from a scan, a finite-element field in tissue, and NEURON axons driven by that field. The corrections are listed in [section 12](#12-what-changed-from-the-first-draft).

## How to read this document

Every number and model here carries one of three labels. Keep them in the code and in the UI too.

| Label | Meaning |
|---|---|
| **[measured]** | Reported in a paper for human clitoral tissue. |
| **[literature]** | Standard value from peripheral-nerve modeling, measured in other nerves or species. |
| **[assumption]** | Chosen by us. Must be varied in a sensitivity analysis. |

Citations marked *(verify)* were written from memory and must be checked against the primary source before any value is used.

## 0. What is being built

Two modes that share geometry and axons but differ greatly in how well they are grounded.

**Mode A, electrical stimulation (biophysical).**

```
electrode current
  -> potential field in tissue (FEM, quasi-static)
  -> extracellular potential at every node of Ranvier
  -> action potentials in DNC axons (cable models in NEURON)
  -> OUTPUT: recruitment curves, activation sites, conduction delays
```

Every stage is a standard, published method. This mode can be verified and partly validated.

**Mode B, touch (phenomenological).**

```
indentation on glans or hood
  -> skin deformation (contact mechanics)
  -> receptor response (filter model, parameters assumed)
  -> spike trains in the same axon population
  -> OUTPUT: firing-rate maps
```

No human clitoral afferent recordings exist to fit this against, so Mode B is an illustration built on assumptions. It must be labelled that way.

**Out of scope as model outputs:** "perceived intensity" and an "erection loop". Nothing available can validate them. An optional engorgement state is described in section 8 as a manual parameter, not a prediction.

## 1. Tooling

| Purpose | Tool | Notes |
|---|---|---|
| Stimulation pipeline | **NRV** (`nrv-py`) | Wraps Gmsh, FEniCSx and NEURON for peripheral-nerve stimulation. Use it instead of writing the coupling by hand. |
| Axon simulation | NEURON 8.x + Python | Called by NRV; usable directly for custom fibers. |
| FEM | FEniCSx (dolfinx) | Needed directly only for scan-derived geometry. |
| Meshing | Gmsh; pygalmesh (CGAL), iso2mesh or fTetWild | Gmsh for idealized geometry. A label-map mesher for scan-derived geometry. |
| Viewing large scans | Fiji, Neuroglancer | Use virtual stacks; the volumes do not fit in RAM. |
| Segmentation | 3D Slicer, ilastik, ITK-SNAP | |
| Centerlines | VMTK (SlicerVMTK extension) | |
| Visualization | ParaView, PyVista | |
| Touch model | TouchSim (Python) as a starting point | Fitted to the primate hand, not to genital skin. |
| UI | Streamlit + PyVista + Plotly | |

Not needed: Brian2 (no extracellular-stimulation mechanism, so mirroring the axons there adds nothing) and LFPy (it simulates recordings, not stimulation; add it only if simulated nerve recordings become a goal).

**Platform:** NRV and FEniCSx do not support Windows natively. Use WSL2 with conda. Follow the install command on the NRV package page, which pins the dolfinx version.

**Not free, for reference only:** ASCENT (Duke) is the best-documented pipeline of this kind but requires COMSOL.

## 2. Data sources

| Source | Use | Status on 2026-11-13 |
|---|---|---|
| Tunçkol et al., *Sci Rep* 2024, doi:10.1038/s41598-024-72898-8 | Fiber and bundle counts | Checked against the full text. |
| "Neuroanatomy of the clitoris", bioRxiv 2026, doi:10.64898/2026.03.18.712572 | Trunk trajectories (HiP-CT, two donors) | Preprint, not peer-reviewed. Full text not read; five trunks and 0.7 mm widest trunk come from press coverage. |
| Human Organ Atlas, human-organ-atlas.esrf.eu | Raw HiP-CT volumes | **Not confirmed** that the female genitalia scans are publicly downloadable. Check the portal first. |
| NIH 3D, entry 3DPX-017321 | Pelvis context (bones, perineal muscles) | Exists, CC-BY. |
| NIH 3D, entry 3DPX-020984 | Pelvis context | **Not found.** Do not rely on it. |
| Geneva 3D pelvic kit (PMID 32675048) | In-vivo shape reference | Not checked. Confirm the license before redistributing anything derived from it. |
| SPARC portal, sparc.science | Animal pudendal data | Not checked. Mostly animal data; do not assume human afferent recordings exist there. |

### Fiber population

| Quantity | Value | Label |
|---|---|---|
| Bundles, crus | 12 ± 3 | [measured] Tunçkol |
| Bundles, hemi-body | 32 ± 13 | [measured] Tunçkol |
| Axons, crus (per side) | 2917 ± 446, 76% myelinated | [measured] Tunçkol |
| Axons, hemi-body (per side) | 3137 ± 753, 71% myelinated | [measured] Tunçkol |
| Myelinated fibers per dorsal nerve | about 5,140 | [measured] Peters et al. *(verify)*; conflicts with Tunçkol |
| Axon diameter distribution | **not reported by Tunçkol** | [assumption] |

Consequences:

- Treat the count as a range of roughly 3,000 to 5,000 per side and run both ends.
- The diameter distribution is the largest unknown in Mode A, because threshold and conduction velocity both scale with diameter. Declare a distribution, state that it is assumed, and vary it. Check whether Peters et al. or other histology reports diameters before choosing.
- All donors were elderly (75 to 98 years in Tunçkol; postmenopausal in the preprint). Fiber counts decline with age, so the numbers may understate younger anatomy.
- Do not scale penile nerve data down. Branching differs, and the hood, mons and posterior labial contributions are separate.

## 3. Phase 1: idealized-nerve recruitment model

Do this first. It needs no scan data and exercises the whole of Mode A.

1. Install NRV in WSL2. Run its tutorials to confirm the install.
2. Build one nerve: a cylinder 0.7 mm across **[measured, preprint]** containing fascicles. Bundle count from the table above; fascicle diameters are an **[assumption]** until measured from scans.
3. Fill the fascicles with axons: count from the range above, 71 to 76% myelinated, diameters from the declared distribution.
4. Place the electrode. For a surface electrode, add skin and subcutaneous layers and see section 5.3.
5. Run threshold searches by bisection for each axon across pulse widths.
6. Produce recruitment curves (percent of fibers active against current) and strength-duration curves.
7. Run the verification tests in section 10.1 before trusting any output.

## 4. Phase 2: scan-derived geometry

Start only once the HOA data is confirmed downloadable.

1. **Download** the lowest-resolution whole-organ volume first. Full-resolution volumes are tens to hundreds of gigabytes.
2. **View** in Fiji as a virtual stack. Crop to the clitoral body, glans and pubic symphysis. Keep 16-bit data until after windowing.
3. **Segment** in 3D Slicer: corpus cavernosum, glans, nerve trunks, vessels. Nerve contrast against connective tissue is low. Expect mostly manual painting with "Fill between slices", or an ilastik pixel classifier trained on annotated slices. Vesselness filters were designed for hollow, high-contrast vessels and may or may not help; test before relying on them.
4. **Centerlines** with VMTK, exported with radius.
5. **Shrinkage:** fixed, ex-vivo tissue is smaller than in vivo. Scale against an in-vivo reference (MRI-based model) and record the factor as an **[assumption]**.
6. **Check** against the preprint: number of trunks, trunk diameters, branch pattern.

What the scan cannot give: single axons, fascicle-level perineurium thickness at whole-organ resolution, and where each axon ends in the skin.

## 5. Phase 3: volume conductor

### 5.1 Mesh

Mesh directly from the segmentation label map with pygalmesh (CGAL), iso2mesh or fTetWild. Building conforming multi-tissue volumes in Gmsh from overlapping surface STLs is fragile and not recommended.

Element size about 0.1 mm near nerves and electrode, coarsening to 1 mm or more far away. Confirm with a convergence test (section 10.1).

### 5.2 Conductivities

Low-frequency values in S/m. All *(verify)* against the cited source.

| Tissue | Value | Label and source |
|---|---|---|
| Endoneurium, longitudinal | 0.571 | [literature] Ranck & BeMent 1965 |
| Endoneurium, transverse | 0.083 | [literature] Ranck & BeMent 1965 |
| Perineurium | about 0.0009 | [literature] Weerasuriya 1984, as used in ASCENT |
| Epineurium | about 0.16 | [literature] |
| Muscle, longitudinal / transverse | 0.35 / 0.086 | [literature] Gielen 1984 |
| Fat | 0.03 to 0.04 | [literature] Gabriel 1996 |
| Cortical bone | about 0.02 | [literature] Gabriel 1996 |
| Blood | 0.6 to 0.7 | [literature] |
| Erectile tissue, flaccid / engorged | 0.3 / 0.6 | **[assumption]**; no measurement found |
| Skin | see 5.3 | |

Rules:

- **Perineurium is mandatory.** It is the most resistive layer and largely sets thresholds. It is too thin to mesh at full scale, so model it as a thin-layer (contact impedance) interface, with thickness about 3% of fascicle diameter [literature, Grinberg 2008 *(verify)*]. Check whether the installed NRV version supports the thin-layer approximation; otherwise mesh a thickened layer with proportionally scaled conductivity.
- **Myelin is not in the FEM.** It belongs to the axon model.
- **Anisotropy:** orient the endoneurium tensor along the local centerline tangent.

### 5.3 Equations and boundary conditions

Quasi-static: `div(sigma * grad(V)) = 0`.

- **Electrode:** impose current, not voltage. Apply a normal current density `I / A` on the contact surface.
- **Return:** `V = 0` on the return electrode, or on a distant cut boundary if the return is far away.
- **Skin to air:** zero normal current.
- **Scaling:** solve once for 1 mA and scale linearly with amplitude. Solve again only if geometry or conductivities change.

**Surface electrodes:** the stratum corneum dominates the impedance and is strongly frequency-dependent (around 2e-4 S/m at low frequency, far higher for hydrated skin or with gel). A purely resistive skin layer can misestimate thresholds for short pulses. Treat skin conductivity and the electrode-skin interface as the main **[assumption]** and vary them.

### 5.4 Coupling to axons

Interpolate `V` at every node of Ranvier, apply it through NEURON's `extracellular` mechanism, scale by the stimulus waveform, and search for threshold. Plot the second spatial difference of `V` along each fiber (the activating function, Rattay 1986) to see where spikes should start.

## 6. Axon models

| Fiber type | Model | Notes |
|---|---|---|
| Myelinated, generic | MRG (McIntyre, Richardson, Grill 2002), ModelDB 3810 | A motor-axon model. Geometry is tabulated for 5.7 to 16 µm; later work and ASCENT extend or interpolate to smaller diameters *(verify)*. Use the tabulated geometry, not "internode = 100 × diameter". |
| Myelinated, sensory | Gaines et al. 2018 sensory variant of MRG | Preferable for afferents. |
| Unmyelinated | Sundt et al. 2015 or Tigerholm et al. 2014 | Required for the 24 to 29% unmyelinated fibers. MRG cannot represent them. |

NRV ships implementations of these families; check its documentation for the exact list.

Settings: time step 0.005 ms or smaller. Models are parameterized near body temperature; do not change `celsius` without checking how each mechanism scales.

Expected behavior: conduction velocity around 4.5 to 6 m/s per µm of fiber diameter for myelinated fibers and around 0.5 to 2 m/s for unmyelinated fibers [literature]. The fiber classes present follow from the diameter distribution, which is assumed.

## 7. Phase 4: touch pathway (Mode B)

All parameters in this section are **[assumption]**.

1. **Contact mechanics.** Convert indenter position, shape and depth into stress or strain at receptor depth. Start with an elastic half-space, as TouchSim does. A finite-element hyperelastic model in FEniCSx is a later refinement.
2. **Receptor response.** Use a filter model, not a static curve: a weighted sum of indentation, its rate and its acceleration, followed by rectification and saturation. Rapidly adapting units weight the rate terms; slowly adapting units weight the static term. A static function of pressure cannot tell the two apart.
3. **Receptor types.** The dominant specialized endings in genital skin are Krause (genital) corpuscles and free nerve endings. Mouse data show Krause corpuscles are low-threshold, rapidly adapting and tuned to vibration around 40 to 80 Hz (Qi et al., *Nature* 2024 *(verify)*). Starting from Meissner-like parameters is defensible only as a placeholder.
4. **Spike generation.** Inject the receptor current at the distal node of the assigned axon. This is a generator-current approximation.
5. **Receptive fields.** Scans show trunks, not endings. Assign each axon a skin location by rule: follow its trunk to the nearest distal branch end and scatter terminals over the adjacent skin. Any laterality or regional selectivity in the output is a consequence of this rule, not a finding.

Calibration targets do not exist for human clitoral afferents. Published psychophysical thresholds (vibration and monofilament studies) can bound the population response, loosely.

## 8. Optional: engorgement state

Expose engorgement as a manual slider that changes erectile-tissue conductivity and geometry within the assumed range in 5.2. Do not close a feedback loop from afferent firing to engorgement and call it biophysical; that would be two invented equations. If a reflex loop is added for teaching purposes, label it phenomenological in the UI.

## 9. Interface

Streamlit with PyVista and Plotly.

- Controls: mode, electrode position and current, pulse width and frequency; for Mode B indenter location, depth and vibration frequency; engorgement.
- Center: 3D geometry with fibers colored by threshold (Mode A) or firing rate (Mode B).
- Right: recruitment curve, strength-duration curve, rasters, conduction delay.
- Always visible: the label of each quantity on screen (measured, literature, assumption) and a banner on Mode B.

Precompute FEM solutions and thresholds offline. The UI should only scale and look up.

## 10. Validation

### 10.1 Verification (is the code right?)

- Point source in a homogeneous medium: FEM must match `V = I / (4 * pi * sigma * r)`.
- Mesh convergence: thresholds change by less than a few percent on refinement.
- Axon model: reproduce published MRG conduction velocities and strength-duration behavior.
- Linearity: doubling current doubles `V` everywhere.

### 10.2 Validation (is the model right?)

- **Geometry:** trunk count, trunk diameters and branch pattern against the preprint. Dice overlap between two independent segmenters, not against the model's own input.
- **Mode A:** compare predicted thresholds with human perception thresholds from dorsal genital nerve stimulation studies (surface electrodes, reported in mA), and conduction delays with pudendal evoked-potential and bulbocavernosus reflex latencies. These targets still need to be collected from the clinical literature.
- **Mode B:** no direct validation is available. Report it as unvalidated.

### 10.3 Not validation

- Matching axon count or myelinated fraction to the values that were put in.
- Ipsilateral-only recruitment, when the receptive-field rule assumes it.

### 10.4 Uncertainty

Report every output as a range from a sensitivity analysis over fiber count, diameter distribution, perineurium and skin conductivity, and shrinkage factor.

## 11. Milestones

| Milestone | Content | Done when |
|---|---|---|
| M1 | WSL2 + NRV; idealized nerve; recruitment curves | Verification tests in 10.1 pass |
| M2 | Sensitivity analysis on the idealized model | Output ranges reported |
| M3 | Confirm data access; segment trunks; centerlines | Geometry checks in 10.2 pass |
| M4 | Scan-derived mesh and FEM; realistic recruitment | Convergence shown; compared with clinical thresholds |
| M5 | Touch pathway | Runs; labelled unvalidated |
| M6 | Streamlit interface | Shows labels and ranges |

M1 is about two weeks of work. The whole plan is months, and it is not a publishable result until M4 with its validation.

## 12. What changed from the first draft

| First draft | Correction |
|---|---|
| Sci Rep figures give diameter distributions | The paper reports no diameters. Distribution is an assumption. |
| Hand-built Gmsh + FEniCSx + NEURON coupling | Use NRV, which already does this. |
| Start by segmenting HiP-CT | Start with an idealized nerve; scan data access is unconfirmed. |
| Static receptor curve with invented P50 values | Filter model; all parameters labelled as assumptions. |
| Skin deformation shown but not implemented | Contact-mechanics stage added. |
| No receptive-field map | Explicit rule, labelled as an assumption. |
| Myelin in the FEM; no perineurium; no transverse nerve conductivity | Perineurium added; myelin removed; anisotropic endoneurium. |
| 1 V Dirichlet electrode | Current boundary condition, scaled linearly. |
| MRG for all fibers; internode = 100 × diameter | Tabulated MRG geometry; sensory variant; separate unmyelinated model. |
| Brian2 mirror and LFPy | Removed. |
| Surface STL to Gmsh volume mesh | Mesh from the label map. |
| Autonomic feedback loop as "biophysical" | Manual engorgement parameter; any loop labelled phenomenological. |
| Validation by matching input counts | Separated verification, validation and non-validation. |
| "Publishable in two weeks" | M1 in two weeks; publishable after M4. |

## 13. Data handling and licensing

- HOA data is CC-BY-4.0: cite the dataset DOIs in the app and in any publication.
- Do not commit scan volumes, segmentations or third-party meshes to this repository. Keep them under `data/`, which is ignored.
- The scans come from human donors. Follow the terms of each dataset.

## 14. Repository layout

```
docs/            this blueprint and later notes
data/            scans and third-party models (not committed)
segmentation/    label maps (not committed)
meshes/          generated meshes (not committed)
axons/           population definitions (CSV: x, y, z, diameter, type)
sim/             FEM, axon, touch and coupling code
app/             Streamlit interface
tests/           verification tests from section 10.1
```

## References

Checked on 2026-11-13:

- Tunçkol E. et al. Innervation pattern and fiber counts of the human dorsal nerve of clitoris. *Sci Rep* 2024. doi:10.1038/s41598-024-72898-8
- Neuroanatomy of the clitoris. bioRxiv 2026. doi:10.64898/2026.03.18.712572 (existence and headline findings only)
- NRV documentation: https://nrv.readthedocs.io/
- NIH 3D entry 3DPX-017321: https://3d.nih.gov/entries/3DPX-017321

From memory *(verify)*:

- McIntyre C.C., Richardson A.G., Grill W.M. Modeling the excitability of mammalian nerve fibers. *J Neurophysiol* 2002.
- Gaines J.L. et al. A model of motor and sensory axon activation in the median nerve. *J Comput Neurosci* 2018.
- Sundt D. et al. Spike propagation through the dorsal root ganglia in an unmyelinated sensory neuron. *J Neurophysiol* 2015.
- Tigerholm J. et al. Modeling activity-dependent changes of axonal spike conduction in primary afferent C-nociceptors. *J Neurophysiol* 2014.
- Couppey T. et al. NRV: an open framework for in silico evaluation of peripheral nerve electrical stimulation strategies. *PLOS Comput Biol* 2024.
- Musselman E.D. et al. ASCENT. *PLOS Comput Biol* 2021.
- Saal H.P. et al. Simulating tactile signals from the whole hand with millisecond precision. *PNAS* 2017.
- Qi L. et al. Krause corpuscles are genital vibrotactile sensors for sexual behaviours. *Nature* 2024.
- Walsh C.L. et al. Imaging intact human organs with local resolution of cellular structures using hierarchical phase-contrast tomography. *Nat Methods* 2021.
- Peters B. et al. Histomorphometric evaluation of the dorsal nerve of the clitoris. *J Sex Med* 2023.
- Ranck J.B., BeMent S.L. *Exp Neurol* 1965. Weerasuriya A. et al. 1984. Gielen F.L.H. et al. 1984. Gabriel S. et al. 1996. Grinberg Y. et al. 2008. Rattay F. 1986.
