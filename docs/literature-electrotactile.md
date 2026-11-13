# Electro-tactile modeling methods and human thresholds

Checklist step 1.11. Searched and read on 2026-11-13.

**How to read this file.** Values were extracted from the papers' web pages by an automated reader, not copied by hand from the PDFs. Treat every number as "to be spot-checked against the paper" until step 1.11 is ticked Verified. Sources that could not be read are listed in section 6.

## 1. Answers to the two claims that were written from memory

### Claim 1: surface electrodes mainly excite nerve fibers in the skin, not the nerve trunk

**Confirmed, with a condition.**

- The 2024 review by Kajimoto's group describes the working model as: surface current activates afferent fibers or their endings in the skin, and electrical stimulation acts on the axons rather than on the receptors themselves.
- The Aalborg models (Tigerholm 2019; Poulsen 2020, 2021) place small fibers ending in the epidermis and large fibers ending in the dermis, and reproduce human perception thresholds with fibers at those depths.
- Zhu 2017 places tactile fibers ending in the dermis; in their model excitation starts at the node nearest the dermis-fat boundary.

Condition: where excitation starts depends on electrode size and current. Small contacts act on the superficial endings. Large contacts and higher currents reach deeper along the fiber, and with suitable placement a nerve trunk (the review cites electrodes on the back of the hand reaching the median and ulnar nerves). So the trunk case stays in the plan as secondary.

### Claim 2: polarity changes which fiber orientations respond

**Supported as a model-based proposal with psychophysical backing; not shown by nerve recordings.**

- Kajimoto et al. (ICAT 1999) derive it from the activating function. Legible parts of the paper state: for one polarity "activating function of horizontal axon is positive while that of vertical axon is negative"; for the other it "is reversed and only vertical axon is stimulated"; and the section on the rapidly adapting (Meissner) mode is titled "RA mode by anodic current". The body text of the PDF could not be decoded, so electrode sizes and currents from this paper are not recorded here.
- Yem and Kajimoto (reported in the 2024 review): anodic stimulation produced only vibratory sensations; cathodic produced vibratory and pressure sensations. The review rests this on one comparative study.
- Araiza Illan 2019 reproduce it in simulation: anodic current activated only the fiber with a segment perpendicular to the skin; cathodic activated both fibers, at roughly three times the current.

What this means for the simulator: fiber orientation must be an explicit property of every terminal fiber, and polarity must be an input. The link from "which orientation fires" to "which receptor type" to "what is felt" is a hypothesis, to be tested by the hardware project.

## 2. Published models

| | Tigerholm 2019; Poulsen 2020, 2021 (Aalborg) | Zhu 2017 | Araiza Illan 2019 |
|---|---|---|---|
| Body site | Forearm skin (flat block) | Forearm (cylinder) | Finger (cylinder with rounded tip) |
| Skin layers | Stratum corneum, epidermis, dermis, hypodermis | Stratum corneum, epidermis, dermis, fat, muscle, bone, marrow, gel | One skin layer, fat, bone |
| Anisotropy | Yes, in epidermis and dermis | Yes, in epidermis, dermis, muscle | No |
| Field solution | Steady state. Time-dependent solutions were computed for comparison; permittivity had little effect | Steady state; argued from a charge relaxation time of about 1 µs | Steady state; capacitive effects neglected |
| Electrodes | Pin (0.2 mm cathodes with ring anode), patch (15 x 20 mm), concentric, array, intra-epidermal | Disc 5 to 12 mm, 9 mm for validation, with 1 mm gel; return 18 mm disc 120 mm away | Eight bars 1 x 8.5 mm, 1 mm apart; fields combined by superposition |
| Drive | Current | Current, biphasic, cathodic first | Current, within ±5 mA per contact, sum about zero |
| Fiber models | Aδ 3.5 µm with unmyelinated ending in the epidermis and branches; Aβ 9 µm ending at a node in mid-dermis. Detailed ion channels | Aβ double-cable model after McIntyre 2002, 2 to 8 µm, roughly perpendicular to skin, ending in dermis | Three myelinated 4 µm fibers, Hodgkin-Huxley type, parallel and bent paths at 1.5 to 2 mm depth |
| Fiber ending | Aδ: explicit unmyelinated ending. Aβ: ends at a node, no receptor | Straight cable, no ending geometry | Not modeled |
| Validation against people | Strength-duration time constant, threshold electrotonus, slowly rising pulses, compared with published perception data. Parameters were tuned to fit | Six subjects. Trends with electrode size and pulse width match; absolute thresholds for a 3 µm fiber were far above measured | Qualitative match to the polarity effect only |
| Software | COMSOL + NEURON | COMSOL + NEURON | Elmer + Gmsh + MATLAB, all files published on figshare |
| Free tools only | No | No | Yes (MATLAB aside) |

### Which to follow

No single paper does everything. The recommendation, for the expert reviewer to confirm:

1. **Skin layers and fiber placement: follow the Aalborg model.** It is the only one with fibers ending at stated depths, separate small and large fibers, and quantitative comparison with human perception data.
2. **Multi-contact handling: follow Araiza Illan 2019.** It already uses free tools (Elmer, Gmsh) and combines per-contact fields by superposition, which is the design in `scope.md` section 5.
3. **Tactile fiber model: start from Zhu 2017's diameter-scaled Aβ model** and compare with the Aalborg Aβ model.

### Lessons these papers give

- **Absolute thresholds are hard to predict.** Zhu 2017 matched trends but missed absolute values; the Aalborg group tuned parameters to fit. Expect version 1 to be reliable for comparisons between settings, and unreliable for absolute current values until it is calibrated with bench data.
- **Steady-state field solutions are accepted practice** for current-controlled stimulation; two groups checked or argued it. This settles the open question in blueprint section 5.3 for the tissue field. Skin and interface capacitance still matter for the voltage the driver must supply.
- **Fiber diameter dominates.** In Zhu 2017 the best match to measured thresholds moved from a 3 µm to a 7 µm fiber. This is the same unknown as checklist step 1.5.
- **Fat and deep-layer properties matter** more than expected (Zhu 2017 sensitivity analysis).
- **Sweat ducts, hair follicles and uneven skin are left out** by all three, and all three name this as a limit on absolute accuracy.

## 3. Skin layer values reported by these models

Forearm skin. None is for genital or mucosal skin.

| Layer | Tigerholm 2019 | Zhu 2017 |
|---|---|---|
| Stratum corneum | 20 µm; 2e-4 S/m; relative permittivity 2e3 | 29 µm; 2e-5 S/m typical (1e-5 to 1e-4) |
| Epidermis | 82 µm; 0.95 and 0.15 S/m in the two directions | about 60 µm; about 0.95 and 0.15 S/m |
| Dermis | 1300 µm; 2.57 and 1.62 S/m | 1.2 to 1.7 mm; 2.57 (2 to 3.8) and 1.62 (1 to 2.8) S/m |
| Fat or hypodermis | 5000 µm; 0.02 S/m | 2.5 mm; 0.01 S/m (0.0017 to 0.1) |
| Gel | not used | 1 mm; 0.02 S/m |

Points to settle in steps 1.6 and 1.10:

- The two papers differ tenfold on stratum corneum conductivity.
- The dermis values (1.6 to 2.6 S/m) are higher than blood and well above the 0.17 S/m skin value in the first draft of the blueprint. Trace them to their primary source before use.
- Which direction each anisotropic value belongs to was not clear from the extracted tables.

## 4. Human thresholds found

| Source | Site | Electrode | Stimulus | Result | Complete enough to reproduce? |
|---|---|---|---|---|---|
| Zhu 2017 | Forearm | 9 mm disc, platinum, gel; return 18 mm disc 120 mm away | Biphasic, cathodic first, 200 µs, 50 Hz; also 50 to 400 µs | Thresholds about 0.5 to 1.5 mA, six subjects aged 22 to 30; per-subject and per-size values are in figures | Mostly. Values must be read from figures |
| Tigerholm 2019, using earlier perception data | Forearm | Pin and patch, dimensions given | Rectangular pulses up to 16 ms; prepulses; slowly rising pulses | Strength-duration time constants 1060 ± 690 µs (pin) and 580 ± 160 µs (patch) | Yes for relative measures |
| Cavalcanti 2007 | Clitoris, each side | Not retrieved | Square pulses 0.2 ms, 4.7 Hz | Sensory threshold 3.64 ± 1.01 mA left, 3.84 ± 1.53 mA right; 38 women enrolled | No: electrode type, size and position missing |
| Warren, fingertip receptive fields | Fingertip | Not retrieved | 2 mA fixed; pulse width raised to threshold, mean 1.03 ± 0.70 ms; 25 and 75 Hz | Threshold expressed as pulse width | No |
| Multi-pad study, Applied Sciences 2021 | Fingertip and proximal phalanx | Multi-pad, details not retrieved | Not retrieved | Sensation, localization, smearing and discomfort thresholds in 11 subjects | Unknown: paper could not be loaded |
| Preprint 2021 | Finger | 1.5 mm copper contacts; return 30 mm copper disc on the palm | Voltage-driven, 40 to 120 V; current limited to 0.2 mA | Thresholds given as voltages | No: voltage-driven |

**Consequence:** no fingertip dataset with every parameter has been obtained yet. The most complete dataset is the forearm one in Zhu 2017. Step 3.9 is changed accordingly (amendment A-005).

**For checklist step 1.7:** Cavalcanti 2007 is the first clitoral electrical threshold found, and its value (about 3.7 mA at 0.2 ms) is several times the forearm thresholds above. That may reflect the electrode used; get the full methods before reading anything into it.

## 5. Parameter values seen in this literature

For step 0.3 (defaults and input limits). These are what researchers used, not recommendations and not safety limits.

| Parameter | Values seen |
|---|---|
| Contact size | 0.2 mm pins; 1 mm bars; 1.5 mm discs; 5 to 12 mm discs; 15 x 20 mm patch |
| Contact spacing | 1 mm gaps; 2 mm pitch; "3 mm or less" for arrays |
| Current | Thresholds 0.5 to 1.5 mA (forearm, 9 mm); 2 mA fixed (fingertip); model bound ±5 mA per contact; clitoral threshold about 3.7 mA |
| Pulse width | 50 to 400 µs in psychophysics; 200 µs common; 10 µs to 1 ms simulated; up to about 1 ms on the fingertip |
| Pulse rate | 5 Hz to 2 kHz tested; 50 Hz common; lowest threshold reported near 160 Hz |
| Voltage needed | 40 to 120 V for small dry copper contacts on a finger. This supports having the driver's voltage limit as an input |
| Other effects | Warmer skin lowered thresholds by 13 to 17%. Sweat and movement change thresholds from moment to moment |

Reported links between settings and sensation, from the 2024 review, all on ordinary skin: about 5 Hz felt as light prickling; about 250 Hz as uncomfortable tingling; different rates were described as itching, tickling, vibrating or prickling; concentric contacts felt more natural and were easier to locate.

## 6. What could not be read (two attempts each, then stopped)

Download these by hand into `data/papers/` so they can be read after step 0.6 installs the PDF tool.

| Paper | Why it matters | What happened |
|---|---|---|
| Multi-pad fingertip thresholds, Applied Sciences 2021, doi:10.3390/app112110231 | Likely the fingertip dataset needed for validation | Journal page and university mirror both refused automated access |
| Kuhn, Keller, Lawrence, Morari 2009, doi:10.1007/s11517-008-0422-z | Their conclusion on whether capacitive effects change nerve activation, and their interface model | Repository returned an empty page; search did not reach the conclusion |
| Kajimoto et al., ICAT 1999, icat.vrsj.org/papers/99107.pdf | Fingertip receptor depths, electrode sizes, currents | PDF downloaded, but only captions could be decoded |
| Cavalcanti et al. 2007, Int Braz J Urol 33(6):815-821 | Electrode details for the clitoral threshold | Two sites refused or failed |
| Yem and Kajimoto 2017, IEEE Transactions on Haptics | Polarity effect with full stimulus parameters | Not found by search; behind a paywall |

## 7. Gaps

- No published model of electrical stimulation of genital or mucosal skin was found.
- No measured electrical properties of glans or hood skin were found (step 1.10).
- No comparison of electrode materials was found; the 2024 review names this as missing from the field (step 1.12).
- Genital-specific searches were limited to one query; step 1.7 covers this properly.

## Sources

- Tigerholm J, Poulsen AH, Andersen OK, Mørch CD. From perception threshold to ion channels: a computational study. Biophys J 2019;117(2):281-295. doi:10.1016/j.bpj.2019.04.041. https://pmc.ncbi.nlm.nih.gov/articles/PMC6700668
- Poulsen AH, Tigerholm J, Meijs S, Andersen OK, Mørch CD. Comparison of existing electrode designs for preferential activation of cutaneous nociceptors. J Neural Eng 2020. doi:10.1088/1741-2552/ab85b1 (search summary only)
- Zhu K, Li L, Wei X, Sui X. A 3D computational model of transcutaneous electrical nerve stimulation for estimating Aβ tactile nerve fiber excitability. Front Neurosci 2017;11:250. https://www.frontiersin.org/articles/10.3389/fnins.2017.00250/full (authors as listed on the page; verify)
- Araiza Illan G, Stüber H, Friedl KE, Summers IR, Peer A. A simulation environment for studying transcutaneous electrotactile stimulation. PLoS ONE 2019;14(2):e0212479. https://pmc.ncbi.nlm.nih.gov/articles/PMC6386484/ (authors verify)
- Electrotactile displays: taxonomy, cross-modality, psychophysics and challenges. Front Virtual Real 2024. doi:10.3389/frvir.2024.1406923
- Kajimoto H, Kawakami N, Maeda T, Tachi S. Tactile feeling display using functional electrical stimulation. ICAT 1999. https://icat.vrsj.org/papers/99107.pdf (title and authors from memory; verify)
- Cavalcanti GA et al. Pudendal somatosensory evoked potentials in normal women. Int Braz J Urol 2007;33(6):815-821. https://scielo.br/j/ibju/a/tkYqh8skZB66h3dNfnD4rvN/?lang=en
- Kuhn A, Keller T, Lawrence M, Morari M. A model for transcutaneous current stimulation: simulations and experiments. Med Biol Eng Comput 2009;47(3). doi:10.1007/s11517-008-0422-z (not read)
