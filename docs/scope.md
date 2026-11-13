# Scope

Decided by the owner on 2026-11-13. Recorded as amendments A-002, A-003, A-004 and A-007. Change it only through a new amendment.

## 1. Purpose

Simulate the electrical response of clitoral nerve fibers to surface electro-tactile stimulation. The simulator is the base test bench for a separate hardware project that applies pulse waveforms through skin electrodes to different parts of the clitoris, with the aim of producing different sensations such as touch and tapping.

## 2. The question the simulator answers

> For a given electrode layout and pulse waveform on a given part of the clitoris, which nerve fibers fire, where, at what current, and in what firing pattern?

## 3. What it can and cannot tell you

| It can estimate | It cannot tell you |
|---|---|
| Which fibers are recruited, by location, depth, diameter and type | What the stimulation feels like |
| The current needed to recruit a given share of fibers | Whether a sensation is pleasant, neutral or painful |
| How focused or spread the activation is for each electrode layout | Perception thresholds of a real person, before calibration |
| How waveform, pulse width, polarity and frequency shift recruitment | Whether a setting is safe |
| The firing pattern each fiber produces for a pulse train | Central effects: adaptation, attention, arousal |

The gap between "which fibers fire" and "what is felt" is closed only by measurements on people in the hardware project. The simulator narrows the search; it does not replace those measurements.

Published models of this kind reproduce trends between settings better than absolute thresholds (checklist step 1.11). Until version 1 is calibrated with bench data, trust its comparisons between settings more than its absolute current values.

## 4. What this changes in the model

**Surface electrodes mainly excite the fine nerve branches and endings in the skin under the electrode, not the main nerve trunk.** [literature; confirmed in checklist step 1.11, sources in `literature-electrotactile.md`] The first model is therefore a layered skin model with terminal fibers, not a nerve trunk with fascicles. The trunk model stays as a secondary case: it is the standard published test of the field-to-axon coupling, and it matters for large electrodes and high currents.

This shifts where the uncertainty is. The quantities that matter most are now:

- skin layer thicknesses and conductivities on the glans, hood and nearby skin;
- depth, density, orientation and diameter of the terminal fibers;
- the electrode-to-skin interface (dry, gel or moist).

None of these has been found in open data for the clitoris yet (checklist steps 1.10 and 1.11).

## 5. Electrodes and stimulus: inputs in the interface

The owner's requirement: size, shape, number, waveform and current range are all inputs in the interface. The user sets them, then runs the simulation. Nothing is fixed in advance.

### Regions

Version 1: **glans** and **hood**. More regions are added in later versions. A **fingertip** preset is also needed, for validation (checklist step 3.9) and because the hardware project tests on fingers first.

### Electrode material (selectable)

Stainless steel, copper (PCB), silver, gold, titanium.

### Skin condition (selectable)

Dry, moist, gelled.

### What these two choices change, and what they do not

| Choice | Changes | Does not change (to a first approximation) |
|---|---|---|
| Skin condition | Surface-layer conductivity and contact impedance, so how current spreads and concentrates at contact edges, so which fibers fire | |
| Electrode material | The voltage the driver must supply; how evenly current leaves the contact; electrochemical behavior at the surface | Which fibers fire |
| Electrode material or dry skin, when the needed voltage exceeds what the driver can supply | The current actually delivered falls below the set value, so fewer fibers fire than requested | |

The hardware is **current-controlled** (decided by the owner, A-004). The driver sets the current and supplies whatever voltage that takes, up to its limit (its compliance voltage). The simulator therefore reports the voltage each contact needs and flags any setting the driver could not deliver.

The user sets the current and the driver's voltage limit in the interface. The voltage actually applied is a result of the simulation, not a separate setting: for a given electrode and skin, current and voltage cannot both be chosen freely.

All metals listed conduct millions of times better than tissue, so in the tissue field they behave almost identically. The differences are at the metal-to-skin interface. [literature, verify in checklist step 1.12]

The interface must say this next to the material selector, so a user does not read meaning into a result that did not change.

Note for the hardware project, not a result of this simulator: the listed metals differ in corrosion and ion release under stimulation, and copper and silver are the ones usually questioned for skin and mucosal contact. [literature, verify] That is a hardware safety topic.

### Defaults, input limits and test layouts

Because every value is a user input, the simulator still needs three things, proposed by the agent from the electro-tactile literature and accepted by the owner (checklist step 0.3):

1. **A default** for each input, so the interface opens in a sensible state. Labelled assumption.
2. **Input limits**: the range inside which the model is valid (for example contact size against mesh resolution, pulse width against the field model's assumptions). These are model limits, not safety limits.
3. **A few fixed test layouts** used only by the automated tests, so results can be compared between code versions.

#### Defaults, ranges, flags and test layouts

Proposed by the agent and accepted by the owner on 2026-11-13 (amendment A-007). Not yet reviewed by an expert.

Sources are in `literature-electrotactile.md`. "Assumption" means no source was found and the value is the agent's choice. None of these ranges is a safety limit.

**Regions.** Glans and hood for use; fingertip and forearm for validation only, because that is where human data exist.

**Electrode inputs**

| Input | Default | Allowed range | Basis |
|---|---|---|---|
| Region | Glans | glans, hood, fingertip, forearm | Owner's decision; last two added for validation |
| Skin condition | glans moist; hood dry; fingertip dry; forearm gelled | dry, moist, gelled | Fingertip and forearm follow the validation papers. Glans and hood: assumption |
| Material | Stainless steel | the owner's five | Used for the pin and needle electrodes in Poulsen 2020. Does not change which fibers fire |
| Number of contacts | 2 | 1 to 16 | Papers used 6 to 8. Upper bound is computing time: assumption |
| Contact shape | Disc | disc, rectangle, ring | Owner's decision |
| Contact size | 1.5 mm diameter | 0.2 mm to 12 mm, and it must fit inside the region | Smallest modeled contact is a 0.2 mm pin (Tigerholm 2019 p.2); largest validated disc is 12 mm (Zhu 2017). Default: assumption |
| Gap between contacts | 1.0 mm | 0.2 mm up to the region size | 1 mm in Kajimoto 1999 and Araiza-Illan 2019; 1.6 mm in Malešević 2021. Lower bound: assumption (mesh resolution) |
| Return path | Local: contact currents sum to zero | local, or one distant return electrode | Kajimoto 1999 p.6 |
| Share of current per contact | +1 and -1 | -1 to +1 | Definition |

**Stimulus inputs**

| Input | Default | Allowed range | Basis |
|---|---|---|---|
| Pulse shape | Biphasic, symmetric, charge-balanced | monophasic; biphasic symmetric; biphasic asymmetric | Every hardware study read used biphasic balanced pulses |
| Leading phase | Cathodic | cathodic, anodic | Cathodic first in Zhu 2017 and Malešević 2021; both in Kajimoto 1999 |
| Pulse width per phase | 200 µs | 10 µs to 10 ms | Default: Kajimoto p.6, Zhu. Lower bound: the steady-state field assumption needs pulses far longer than about 1 µs (Zhu p.3), and 10 µs is the shortest simulated. Upper bound: longest validated (Poulsen 2020) |
| Gap between phases | 0 | 0 to 1 ms | Assumption |
| Current per contact | 0.5 mA | 0 to 10 mA | Default lies between the forearm rheobases (0.1 to 0.4 mA, Poulsen) and the fingertip sensation threshold (1.0 mA, Malešević). Upper bound covers the stimulator ranges in the papers (2 mA Kajimoto, 9 mA Malešević): assumption |
| Pulse rate | 50 Hz | 1 to 1000 Hz, and one pulse must fit inside one period | 50 Hz in Zhu; adjustable to 1 kHz in Kajimoto |
| Train length | 1 s | 0.05 to 5 s | Assumption (computing time) |
| Each pulse averages to zero | On | on, off | Kajimoto p.6 |
| Driver voltage limit | 150 V | 5 to 300 V | ±150 V supply in Kajimoto 1999 figure 11. Range: assumption |

**Flags.** These warn; they do not refuse a run.

| Flag | Rule | Basis |
|---|---|---|
| Driver cannot deliver | The voltage a contact needs exceeds the driver's limit | Amendment A-004 |
| Outside the checked range | Current density on any contact above 1 mA per mm² | The highest in the studies read is about 0.8 mA per mm² (9 mA on 11 mm², the stimulator maximum in Malešević 2021). Threshold: assumption |
| Small contact | Contact area below 10 mm² | Hand and arm studies report discomfort from the high current density of small contacts (Kourtesis 2022 p.2) |

**Test layouts.** Fixed cases for automated tests. The first four have published results to compare with.

| Name | Layout and stimulus | Compared with |
|---|---|---|
| T1 forearm patch | Cathode 15 x 20 mm, anode 2 cm away, gelled; rectangular pulses 0.1 to 10 ms | Poulsen 2020: measured rheobase 0.381 mA |
| T2 forearm disc | One 9 mm gold disc, gelled, return 12 cm away; biphasic cathodic-first, 200 µs, 50 Hz | Zhu 2017: thresholds 0.5 to 1.5 mA; trend with disc size |
| T3 fingertip pads | Six 11 mm² pads, 1.6 mm gaps, 150 mm² reference; biphasic 400 µs, 30 Hz | Malešević 2021: sensation threshold median 1.0 mA. Pad shape to be read from the paper's figure |
| T4 fingertip lines | Eight lines 0.5 x 10 mm at 1 mm pitch, currents sum to zero, 200 µs; centre contact anodic, then cathodic | Kajimoto 1999 and Araiza-Illan 2019: polarity selects fiber orientation |
| T5 glans pair | The default interface state: two 1.5 mm discs, 1 mm gap, moist, 200 µs, 50 Hz, 0.5 mA | Nothing. Regression test only |
| T6 hood grid | Four 2 mm discs in a 2 x 2 grid, 2 mm gaps, dry, same stimulus | Nothing. Regression test only |

**A design tension to know about.** The glans is small: a few millimetres across (from memory; to be confirmed in checklist step 1.10). Several contacts on it must therefore be small, and small contacts mean high current density, which hand and arm studies link to discomfort. The simulator will show this as the "small contact" and current-density flags. How to resolve it belongs to the hardware project.

### What "run" costs

| What the user changed | What is recomputed | Rough cost on this machine |
|---|---|---|
| Current per contact, polarity | Nothing in the field; fibers only | Short |
| Waveform, pulse width, rate, pattern | Fibers only | Short to moderate |
| Contact shape, size, position or number | Mesh and one field solve per changed contact, then fibers | Minutes or more |
| Region or skin condition | Everything | Longest |

Times are estimates until measured (checklist step 3.5). Results are cached by configuration, so a repeated run is instant.

### Electrode layout (one configuration file per layout)

| Parameter | Options |
|---|---|
| Number of contacts | 1 to N |
| Shape of each contact | disc, rectangle, ring; later: arbitrary outline |
| Size of each contact | free, with units |
| Position of each contact | on the skin surface of the chosen region |
| Role of each contact | active, return, or unconnected |
| Share of current per contact | signed fraction, for steering between contacts |
| Region | glans, hood; fingertip for validation |
| Material | stainless steel, copper (PCB), silver, gold, titanium |
| Skin condition | dry, moist, gelled |
| Drive | current-controlled (decided) |
| Driver voltage limit | the highest voltage the driver can supply; set by the user |

### Stimulus

| Parameter | Options |
|---|---|
| Pulse shape | monophasic, biphasic symmetric, biphasic asymmetric |
| Leading polarity | anodic or cathodic |
| Pulse width, interphase gap | free |
| Amplitude | current-controlled, free within a stated range |
| Pulse rate | free |
| Pattern | continuous, bursts, amplitude or rate modulation |

### How this stays cheap to compute

The field problem is linear. Solve it once per contact for unit current and store the result. Any pattern of currents across the contacts is then a weighted sum of the stored solutions, with no new field solve. Changing the waveform only reruns the fiber simulations. A new field solve is needed only when a contact's shape or position, or the tissue model, changes.

### Still to be given by the owner

Nothing outstanding.

## 6. Accuracy target

"As accurate as open data allows." In practice this means:

1. Every parameter is traced to a source and labelled measured, literature or assumption.
2. Every output is reported as a range from a sensitivity analysis, never a single number.
3. The method is first validated where human data exist with enough detail to reproduce (forearm thresholds from Poulsen 2020 and Zhu 2017; fingertip thresholds from Malešević 2021), then transferred to clitoral anatomy (checklist step 3.9).
4. Scan-derived geometry is used wherever the scans can be obtained.
5. Where no open data exists, the gap is stated; it is not filled silently.

## 7. Versions and safety

The owner's order of work (A-003). The version numbers are the agent's reading of it; the owner accepted them for now on 2026-11-13.

| Stage | Basis | Tested on people? | Safety content |
|---|---|---|---|
| Version 1 | Open data and literature only; glans and hood | No | None. Reports charge per phase and charge density per contact as plain numbers, for information. |
| Version 2 | Version 1 plus bench measurements from the hardware (no people) | No | Safety limits from the hardware project's bench safety tests are entered as constraints. |
| After the safety tests | Tests on fingers only, to check safety again | Fingers only | Safety data updated from the finger tests; the fingertip model is calibrated against them. |
| Later versions | More regions; further data | Not planned yet | Updated each time. |

Safety limits are defined and tested in the hardware project, not here. No output of this simulator is evidence that a setting is safe.

Two cautions:

- **Finger tests are still tests on people.** They normally need informed consent and, depending on the country and institution, ethics approval. Check this before the first finger test.
- **Finger results do not transfer directly to the glans or hood.** Fingertip skin is thick and dry; glans and hood skin is thinner and moister with denser innervation, so thresholds and tolerable current density are expected to be lower there. [literature, verify] A setting shown safe on a finger is not thereby safe elsewhere.

To make the later stages possible, version 1 must: keep all parameters in versioned files, stamp every result with the parameter and code version, include the fingertip preset, and define now the format in which bench and finger data will be entered (checklist step 8.1).

## 7a. Who the model represents

Accepted by the owner: version 1 is one approximate anatomy. All open anatomical data come from elderly donors, and anatomy differs between people. The interface states this. Variation between people is a possible later addition (several anatomy parameter sets), not part of version 1.

## 8. Machine and time

Checked on 2026-11-13.

| Item | Value | Consequence |
|---|---|---|
| Drive F | 379 GB free of 466 GB | Enough for the idealized models. Tight for full-resolution scans. |
| Drive C | 16 GB free | Too little for a Linux environment. Install WSL onto drive F. |
| RAM | 64 GB | Enough for segmentation and meshing at reduced resolution. |
| CPU | Intel Core i3-13100F, 4 cores | Population simulations will be slow; run them in batches. |
| GPU | NVIDIA RTX 3080 Ti | Useful for ilastik and visualization; the field solver and NEURON run on CPU. |
| WSL | Version 2 available, no Linux distribution installed | Step 2.1. |

No deadline. Work proceeds one step at a time.

## 9. Reviewers

Role descriptions and what to ask each expert are in [reviewers.md](reviewers.md).
