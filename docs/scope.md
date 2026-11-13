# Scope

Decided by the owner on 2026-11-13. Recorded as amendments A-002, A-003 and A-004. Change it only through a new amendment.

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

## 4. What this changes in the model

**Surface electrodes mainly excite the fine nerve branches and endings in the skin under the electrode, not the main nerve trunk.** [literature, verify] The first model is therefore a layered skin model with terminal fibers, not a nerve trunk with fascicles. The trunk model stays as a secondary case: it is the standard published test of the field-to-axon coupling, and it matters for large electrodes and high currents.

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

All metals listed conduct millions of times better than tissue, so in the tissue field they behave almost identically. The differences are at the metal-to-skin interface. [literature, verify in checklist step 1.12]

The interface must say this next to the material selector, so a user does not read meaning into a result that did not change.

Note for the hardware project, not a result of this simulator: the listed metals differ in corrosion and ion release under stimulation, and copper and silver are the ones usually questioned for skin and mucosal contact. [literature, verify] That is a hardware safety topic.

### Defaults, input limits and test layouts

Because every value is a user input, the simulator still needs three things, proposed by the agent from the electro-tactile literature and accepted by the owner (checklist step 0.3):

1. **A default** for each input, so the interface opens in a sensible state. Labelled assumption.
2. **Input limits**: the range inside which the model is valid (for example contact size against mesh resolution, pulse width against the field model's assumptions). These are model limits, not safety limits.
3. **A few fixed test layouts** used only by the automated tests, so results can be compared between code versions.

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
| Driver voltage limit | the highest voltage the driver can supply; an input |

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

- The highest voltage the hardware's driver can supply, if known. Until then it is an input with an assumed default.
- Confirmation that the version order in section 7 matches the owner's intent.

## 6. Accuracy target

"As accurate as open data allows." In practice this means:

1. Every parameter is traced to a source and labelled measured, literature or assumption.
2. Every output is reported as a range from a sensitivity analysis, never a single number.
3. The method is first validated where human data exist (fingertip electro-tactile thresholds), then transferred to clitoral anatomy (checklist step 3.9).
4. Scan-derived geometry is used wherever the scans can be obtained.
5. Where no open data exists, the gap is stated; it is not filled silently.

## 7. Versions and safety

The owner's order of work (A-003). The version numbers are the agent's reading of it; correct them if wrong.

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
