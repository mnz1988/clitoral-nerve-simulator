# Electro-tactile modeling methods and human thresholds

Checklist step 1.11. First written 2026-11-13 from web pages; rewritten the same day from the PDFs in `downloaded-manually/`.

**How the values were checked.** Each value below was extracted from the PDF with its page number. Six pages were then read a second time directly and matched: Zhu p.3, Araiza-Illan p.5, Malešević p.7, Kajimoto pp.6-7, Cavalcanti p.4, Poulsen p.19. All ten citations were confirmed against OpenAlex or arXiv. Items that remain uncertain are listed in section 7. Page numbers are PDF pages.

## 1. Answers to the two claims that were written from memory

### Claim 1: surface electrodes mainly excite nerve fibers in the skin, not the nerve trunk

**Confirmed, with a condition.**

- Kajimoto 1999 (p.7): the felt location was "always 1-3 mm shifted to fingertip direction", which the authors take as evidence that the current "doesn't stimulate mechanoreceptor itself, but stimulates axon".
- The Aalborg models place small fibers ending in the epidermis and large fibers ending in the middle of the dermis (Tigerholm 2019 p.3; Poulsen 2020 pp.10-12), and report that fibers "were activated at the nerve fiber ending" (Poulsen p.19).
- Zhu 2017 (p.4) places tactile fibers rising from muscle and ending in the dermis.

Condition: small contacts act on the superficial endings; large contacts and higher currents reach deeper. The nerve trunk stays in the plan as a secondary case.

### Claim 2: polarity changes which fiber orientations respond

**Supported as a model-based proposal with qualitative human observations. Not shown by nerve recordings.**

- Kajimoto 1999 (p.5): cathodic current "can't stimulate vertically oriented nerve axon such as RA"; with anodic current "only vertically oriented nerve axon is stimulated while horizontally oriented axon is suppressed". The paper assumes the Meissner (RA) axon is perpendicular to the skin and "temporary" assumes Merkel and Pacinian axons are horizontal (p.2). Its experiment is qualitative and gives no subject count.
- Kourtesis 2022 (p.3) repeats it: anodic gives "perpendicular depolarization", cathodic "horizontal".
- Araiza-Illan 2019 (pp.10-12, 23) reproduce it in simulation: anodic current activated the fiber with a perpendicular segment and inhibited the parallel one; cathodic activated both at "currents three times greater" (0.21 against 0.07 mA in their model).

For the simulator: orientation is an explicit property of every terminal fiber, and polarity is an input. The step from "which orientation fires" to "which receptor type" to "what is felt" is a hypothesis for the hardware project.

## 2. Published models

| | Tigerholm 2019 and Poulsen 2020 (Aalborg) | Zhu 2017 | Araiza-Illan 2019 |
|---|---|---|---|
| Body site | Forearm skin, flat block | Forearm, 150 mm cylinder | Finger, cylinder with spherical tip |
| Layers | Stratum corneum, epidermis, dermis, hypodermis; Poulsen adds a 10 µm interface layer and 1 mm hydrogel | Stratum corneum, epidermis, dermis, fat, muscle, cortical bone, marrow, gel | Skin (one layer, "set to be dry"), fat, bone |
| Anisotropy | Epidermis and dermis | Epidermis, dermis, muscle | None |
| Field solution | Steady state. "little effect from the tissue permittivity" (Tigerholm p.3); time-dependent runs showed "a limited effect" (Poulsen pp.9-10). Frequency-domain runs used for impedance only | Steady state; relaxation time about 1 µs, and capacitance "can be neglected" under current-regulated stimulation, citing Kuhn 2009 (p.3) | Steady state; capacitive effects "minor influence", neglected (p.3) |
| Electrodes | Intra-epidermal needle, 15-pin, planar concentric, planar array (12 square cathodes), Ag/AgCl patch on hydrogel. Patch cathode 1.5 x 2 cm (Tigerholm p.3) | Disc 5 to 12 mm, 9 mm typical; return 18 mm disc 120 mm away. Experiment: gold disc with thin gel layer | Eight bars 1 x 8.5 mm, 1 mm apart; fingernail area grounded |
| Drive | 1 mA and -1 mA spread evenly over cathodes and anode | Biphasic, charge-balanced, cathodic first; 10 µs to 1 ms | Within ±5 mA per contact; random patterns sum to about zero |
| Fiber models | Aδ 3.5 µm: myelinated deep, unmyelinated ending in the epidermis with two side branches. Aβ 9 µm: ends at a node in mid-dermis (about 700 to 790 µm deep). Both run horizontally in the hypodermis, then rise at 45° | Aβ double-cable after McIntyre 2002, 2 to 8 µm, 7 mm long, perpendicular to skin, about 2 per mm² | 4 µm myelinated, Hodgkin-Huxley type at 20 °C; parallel at 1.5 and 2 mm, and one bent fiber rising to 1 mm |
| Validation against people | Tigerholm: normalized measures only. Poulsen: measured and modeled rheobase and chronaxie for five electrodes (section 4) | Six subjects; trend with electrode size matches a 7 µm fiber; a 3 µm fiber's threshold is "far more than the experimental values" (p.10) | None of its own; compared with Yem and Kajimoto 2017 |
| Software | COMSOL 5.3 + NEURON (Poulsen p.5) | COMSOL 4.2a + NEURON 7.3; over 10 million elements; 64 GB RAM | Elmer + Gmsh + MATLAB; 28 files on figshare |
| Code published | Not stated | Not stated | Yes: figshare.com/articles/case2_sif/6241070 (article is CC BY; no separate license on the files) |

### Which to follow

For the expert reviewer to confirm:

1. **Skin layers, fiber placement and electrode interface: the Aalborg model.** It has fibers ending at stated depths, separate small and large fibers, an interface layer and hydrogel, and absolute comparison with human thresholds for five electrode types.
2. **Multi-contact handling with free tools: Araiza-Illan 2019.** Elmer and Gmsh, fields combined across eight contacts, files published.
3. **Tactile fiber model: Zhu 2017's diameter-scaled Aβ model,** compared against the Aalborg Aβ model.

### What these papers teach

- **How far off absolute thresholds are.** In Poulsen 2020 the modeled rheobase was 0.2 to 4.6 times the measured one across five electrodes, and within a factor of two for three of them (section 4). Tigerholm 2019 (p.13) says the skin's uneven composition and the electrode-skin interface have "a strong influence on the absolute value of the perception threshold", and compares normalized values only. Expect version 1 to be within a small factor at best, and better at comparing settings.
- **Steady-state field solutions are standard** for current-controlled stimulation: stated or tested in all three model families.
- **Fiber diameter dominates.** Zhu's best match moved from a 3 µm to a 7 µm fiber.
- **Sweat ducts and uneven skin are left out by everyone** and named as a limit (Poulsen p.29: they "can have a large influence on the current spread").
- **The skin values are not independent.** Zhu and the Aalborg group take epidermis and dermis conductivities from the same sources (Tavernier 1993; Yamamoto 1976; Gabriel 1996). Agreement between them is not confirmation.

## 3. Skin layer values used by these models

Forearm skin. None is for genital or mucosal skin.

| Layer | Aalborg (Tigerholm p.3; Poulsen p.8) | Zhu 2017 (Table 1, p.3): min, typical, max |
|---|---|---|
| Stratum corneum | 20 µm; frequency-dependent in Poulsen; fixed value in Tigerholm (exponent unreadable in the PDF; the web version read 2e-4 S/m) | 29 µm; 1e-5, 2e-5, 1e-4 S/m |
| Epidermis | 82 µm; horizontal 0.95, vertical 0.15 S/m | 60 µm; axial 0.95, radial 0.15 S/m |
| Dermis | 1300 µm; horizontal 2.57, vertical 1.62 S/m | 1411 µm; axial 2, 2.57, 3.8; radial 1, 1.62, 2.8 S/m |
| Hypodermis or fat | 5000 µm; 0.023 S/m (Poulsen) | 2.5 mm; 0.0017, 0.01, 0.1 S/m |
| Interface layer | 10 µm (Poulsen, from Chi 2010) | not modeled |
| Gel | 1 mm hydrogel, 0.0149 S/m (Poulsen) | 1 mm; 0.0001, 0.02, 1.0 S/m |
| Muscle | not modeled | 13.5 mm; axial 0.33, radial 0.11 S/m |

Fingerpad receptor depths and axon diameters (Kajimoto 1999, Table 1, p.2): Meissner 0.7 mm, 3 to 5 µm; Merkel 0.9 mm, 7 to 12 µm; Pacinian 2 mm or deeper, 5 to 13 µm.

To settle in steps 1.6 and 1.10:

- Neither paper defines its direction labels. "Horizontal" and "axial" are presumably parallel to the skin surface, "vertical" and "radial" through it. Confirm in Tavernier 1993.
- Stratum corneum conductivity differs about tenfold between the two models.
- The dermis values (1.6 to 2.6 S/m) are higher than blood. Read Tavernier 1993 before using them; Zhu marks the dermis range as "adjusted for the sensitivity analysis".

## 4. Human thresholds

| Source | Site | Electrode | Stimulus | Result | Enough to reproduce? |
|---|---|---|---|---|---|
| Poulsen 2020 | Forearm, cathode 5 cm from the elbow | Five types (section 2); dimensions are in the paper's figure 1 | Rectangular pulses 0.1, 0.5, 1 and 10 ms; perception threshold by a method of limits | Rheobase, measured then modeled, median mA: intra-epidermal 0.168 / 0.130; planar concentric 0.222 / 0.0425; pin 0.107 / 0.092; planar array 0.151 / 0.689; patch 0.381 / 0.210. Chronaxies between about 460 and 870 µs | Yes, once dimensions are read from figure 1 |
| Zhu 2017 | Volar forearm, 2 cm from the wrist crease | Gold disc 5 to 12 mm with thin gel; return about 12 cm away | Biphasic cathodic-first, 50 to 400 µs; staircase to 50% detection | "between 0.5 and 1.5 mA"; six subjects aged 22 to 30; per-subject and per-size values only in figures 9 and 10D | Mostly; values must be read from figures |
| Malešević 2021 | Index finger, distal and proximal phalanx | Six printed pads of 11 mm² each, 1.6 mm apart (4.6 mm centre to centre); H-shaped reference of 150 mm²; held by a silicone sleeve | Current-controlled, biphasic symmetric, 400 µs, 30 Hz; adjusted in 0.1 mA steps | Median / IQR in mA: sensation 1.0 / 0.4; localization 1.5 / 1.1; smearing 2.1 / 1.8; discomfort 2.9 / 2.6. Eleven subjects. No difference between pads or phalanges | Mostly. Pad shape is in a figure; conductor and gel or dry not stated |
| Kajimoto 1999 | Fingertip | Eight line electrodes 0.5 x 10 mm, 1 mm apart; metal ring as ground | Biphasic, main pulse 200 µs, 200 Hz; at most 2 mA per electrode; ±150 V supply | At 0.2 mA a faint tremble; 0.4 mA pressure shaped like the electrode; 0.6 mA vibration added. Qualitative; subject count not given | No |
| Cavalcanti 2007 | Beside the clitoris at 3 and 9 o'clock; anode between labia minora and majora | "conventional bipolar stimulator"; type, size and material not stated | Square pulses 0.2 ms, 4.7 Hz | Sensory threshold 3.64 ± 1.01 mA left (n = 34), 3.84 ± 1.53 mA right (n = 33); no relation to age (20 to 74), body mass index or height. Two to three times threshold "was well tolerated" | No: electrode not described |

**Consequence (amendment A-006, replacing part of A-005):** validation data exist for both the forearm and the fingertip. Poulsen 2020 is the strongest, because it gives measured and modeled absolute values for five electrode types.

**For step 1.7:** the clitoral threshold (about 3.7 mA at 0.2 ms) cannot be compared with the others, because the electrode is not described and the cathode sat beside the clitoris, not on it.

## 5. Parameter values seen in this literature

For step 0.3 (defaults and input limits). These are what researchers used, not recommendations and not safety limits.

| Parameter | Values seen |
|---|---|
| Contact size | 0.5 x 10 mm lines (Kajimoto); 1 x 8.5 mm bars (Araiza-Illan); 11 mm² pads (Malešević); 5 to 12 mm discs (Zhu); 1.5 x 2 cm patch (Tigerholm). Kourtesis (p.2): "10mm^2 or larger electrodes appear to be more appropriate", because small electrodes give high current density and discomfort |
| Contact spacing | 1 mm (Kajimoto, Araiza-Illan); 1.6 mm gap, 4.6 mm centre to centre (Malešević) |
| Current | Stimulator ranges: up to 2 mA per electrode (Kajimoto); 0 to 9 mA (Malešević). Model bound ±5 mA per contact, because larger currents "would result in pain and discomfort" (Araiza-Illan p.5). Thresholds: 0.1 to 0.4 mA rheobase (Poulsen); 0.5 to 1.5 mA (Zhu); 1.0 mA sensation and 2.9 mA discomfort on the finger (Malešević) |
| Usable range above threshold | Localization at 123 to 176% of sensation threshold; discomfort at 185 to 526% (Malešević p.7) |
| Pulse width | 200 µs (Kajimoto, Zhu typical); 400 µs (Malešević); 50 to 400 µs (Zhu); 0.1 to 10 ms (Poulsen) |
| Pulse rate | 30 Hz (Malešević); 50 Hz (Zhu); 200 Hz (Kajimoto); adjustable to 1 kHz (Kajimoto) |
| Waveform | Biphasic and charge-balanced in every hardware study. Kourtesis (p.3): square pulses "strongly preferred"; biphasic "prevents half-cell reaction ... and skin irritation" |
| Driver voltage | ±150 V supply (Kajimoto, figure 11) |
| Contact materials | Stainless steel pins and needle; Ag/AgCl on hydrogel; gold disc with gel; printed conductive ink; plain metal lines. Kourtesis (p.2): "noble metals or conductive polymers appear to alleviate or avoid undesired electrochemical reactions" |
| Design rules used | Contact currents sum to zero "so that current was confined locally"; time average of each pulse zero so charge does not accumulate (Kajimoto p.6) |

Sensation notes, all on ordinary skin: below 100 Hz in the anodic mode felt like touching a vibrating speaker cone; above 200 Hz felt "quite uncomfortable" (Kajimoto p.7). Sweat changes skin conductance and can remove the sensation or cause discomfort, so thresholds must be re-measured during use (Kourtesis p.3).

## 6. What these papers do not give

- No model of electrical stimulation of genital or mucosal skin.
- No measured electrical properties of glans or hood skin (step 1.10).
- No comparison of stainless steel, copper, silver, gold or titanium contacts (step 1.12).
- No numeric comfort or safety limits (Kourtesis gives only qualitative statements).

## 7. Still uncertain or unread

| Item | Status |
|---|---|
| Poulsen table 3 chronaxie columns | The extracted header order is ambiguous, so which column is measured and which modeled is not recorded here. Check against the page image |
| Direction labels of the anisotropic conductivities | Not defined in either paper; see section 3 |
| Tigerholm stratum corneum and hypodermis exponents | Minus signs are lost in the PDF text |
| Electrode dimensions in Poulsen 2020 and pad shape in Malešević 2021 | Only in figures, which the text reader cannot see |
| Kuhn, Keller, Lawrence, Morari 2009 | Paywalled, not read. Its conclusion on capacitance is known only through Zhu 2017 and Araiza-Illan 2019, who both cite it as showing a minor effect |
| Yem and Kajimoto 2017 | Not obtained |
| Ray, Vasudevan, Manivannan 2024 review | Read only through the web page, not re-checked in the PDF; no number in this file depends on it |

## Sources

All confirmed against OpenAlex or arXiv on 2026-11-13.

- Tigerholm J, Poulsen AH, Andersen OK, Mørch CD. From perception threshold to ion channels: a computational study. Biophys J 2019. doi:10.1016/j.bpj.2019.04.041
- Poulsen AH, Tigerholm J, Meijs S, Andersen OK, Mørch CD. Comparison of existing electrode designs for preferential activation of cutaneous nociceptors. J Neural Eng 2020. doi:10.1088/1741-2552/ab85b1
- Zhu K, Li L, Wei X, Sui X. A 3D computational model of transcutaneous electrical nerve stimulation for estimating Aβ tactile nerve fiber excitability. Front Neurosci 2017. doi:10.3389/fnins.2017.00250
- Araiza-Illan G, Stüber H, Friedl KE, Summers IR, Peer A. A simulation environment for studying transcutaneous electrotactile stimulation. PLoS ONE 2019. doi:10.1371/journal.pone.0212479
- Malešević JM, Isaković MS, Garenfeld MA, Došen SS, Štrbac MD. The impact of stimulation intensity on spatial discrimination with multi-pad finger electrode. Appl Sci 2021. doi:10.3390/app112110231
- Kajimoto H, Kawakami N, Maeda T, Tachi S. Tactile feeling display using functional electrical stimulation. ICAT 1999. (Title confirmed; author list beyond the first is from memory.)
- Kourtesis P, Argelaguet F, Vizcay S, Marchal M, Pacchierotti C. Electrotactile feedback applications for hand and arm interactions: a systematic review, meta-analysis, and future directions. IEEE Trans Haptics 2022. doi:10.1109/TOH.2022.3189866; arXiv:2105.05343
- Cavalcanti GA et al. Pudendal somatosensory evoked potentials in normal women. Int Braz J Urol 2007;33(6):815-821. doi:10.1590/s1677-55382007000600010
- Ray RK, Vasudevan MK, Manivannan M. Electrotactile displays: taxonomy, cross-modality, psychophysics and challenges. Front Virtual Real 2024. doi:10.3389/frvir.2024.1406923
- Kuhn A, Keller T, Lawrence M, Morari M. A model for transcutaneous current stimulation: simulations and experiments. Med Biol Eng Comput 2009. doi:10.1007/s11517-008-0422-z (not read)
