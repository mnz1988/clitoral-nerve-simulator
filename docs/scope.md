# Scope

Decided by the owner on 2026-11-13. Recorded as amendment A-002. Change it only through a new amendment.

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

## 5. Electrodes and stimulus: a parameter set, not one design

The owner's requirement: size, shape, number, waveform and current range must all be adjustable.

### Electrode layout (one configuration file per layout)

| Parameter | Options |
|---|---|
| Number of contacts | 1 to N |
| Shape of each contact | disc, rectangle, ring; later: arbitrary outline |
| Size of each contact | free, with units |
| Position of each contact | on the skin surface of the chosen region |
| Role of each contact | active, return, or unconnected |
| Share of current per contact | signed fraction, for steering between contacts |
| Region | glans, hood, or other external skin near the clitoris |
| Interface | dry, gel, or moist skin (changes the skin model) |

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

- Realistic ranges for contact size, spacing, current, pulse width and rate. The simulator can accept anything, but tests and validation need bounded reference cases.
- Which regions come first.
- Electrode material and whether gel or moisture is used.

## 6. Accuracy target

"As accurate as open data allows." In practice this means:

1. Every parameter is traced to a source and labelled measured, literature or assumption.
2. Every output is reported as a range from a sensitivity analysis, never a single number.
3. The method is first validated where human data exist (fingertip electro-tactile thresholds), then transferred to clitoral anatomy (checklist step 3.9).
4. Scan-derived geometry is used wherever the scans can be obtained.
5. Where no open data exists, the gap is stated; it is not filled silently.

## 7. Versions and safety

| Version | Basis | Safety content |
|---|---|---|
| 1 | Open data and literature only | None. Reports charge per phase and charge density per contact as plain numbers, for information. |
| 2 and later | Version 1 plus bench and human measurements from the hardware project | Safety limits defined and tested in the hardware project are entered as constraints. |

Safety limits are defined and tested in the hardware project, not here. Until version 2, no output of this simulator is evidence that a setting is safe.

To make version 2 possible, version 1 must: keep all parameters in versioned files, stamp every result with the parameter and code version, and define now the format in which bench data will be entered (checklist step 8.1).

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
