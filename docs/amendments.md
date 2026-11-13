# Amendments log

The blueprint and the checklist are expected to change. This file records every change and why it was made.

## When to write an amendment

- A step turns up a subject or problem the blueprint does not cover.
- A source contradicts a value or claim in the blueprint.
- A data source, tool or method turns out to be unavailable or unsuitable.
- A step is blocked after two failed attempts and the decision is to change the approach or drop it.
- A reviewer asks for a change.
- A decision changes the scope (for example the checkpoint in step 3.7).

## How an amendment is processed

1. Draft it: in the form at the bottom of `checklist/index.html`, or directly here.
2. Decide: you accept, change or reject it. Rejected amendments stay in this log with the reason.
3. Fold it in, all in one commit:
   - edit the affected sections of `docs/blueprint.md` and raise its version line;
   - add, change or retire steps in `checklist/steps.js` (retired steps are removed; their id is never reused);
   - record the entry below with status `accepted`.
4. Mark the draft "folded into the plan" in the checklist page.

## Template

```
## A-000: short title
- Date:
- Raised by: (you / agent / reviewer name or role)
- Found in step:
- What was found:
- Why the current plan does not handle it:
- Decision: accepted / rejected / deferred, and why
- Blueprint sections changed:
- Checklist steps added, changed or retired:
- Effect on results already produced: (none / which results must be rerun)
```

## Log

## A-001: first corrected blueprint
- Date: 2026-11-13
- Raised by: agent, on review of the first draft
- Found in step: before the checklist existed
- What was found: several wrong or invented elements in the first draft (static receptor curve, myelin in the field model, missing perineurium, voltage boundary condition, unsupported diameter claim, circular validation).
- Why the current plan does not handle it: the first draft presented assumptions as facts.
- Decision: accepted. See section 12 of the blueprint for the full list.
- Blueprint sections changed: all (version 2).
- Checklist steps added, changed or retired: checklist created.
- Effect on results already produced: none; no results existed.

## A-002: scope decided, surface electro-tactile stimulation
- Date: 2026-11-13
- Raised by: owner's answers to the open scope questions
- Found in step: 0.2, 0.3, 0.4
- What was found:
  1. The simulator is a test bench for a hardware project that stimulates different parts of the clitoris through skin electrodes to produce sensations such as touch and tapping.
  2. Electrodes and stimulus must be fully adjustable: size, shape, number, waveform, current range.
  3. Accuracy target: as accurate as open data allows.
  4. Safety limits will be defined and tested in the hardware project and entered into later versions of the simulator.
  5. No deadline. Machine checked: 64 GB RAM, 4 cores, 379 GB free on F, only 16 GB free on C.
- Why the current plan does not handle it:
  - The first model in blueprint section 3 was a nerve trunk with fascicles. Surface electrodes mainly excite fine branches and endings in the skin, so the trunk is the wrong first target.
  - The blueprint assumed one fixed electrode. Adjustable multi-contact layouts need a parameter schema and one stored field solution per contact.
  - The touch pathway (old Mode B) was an optional illustration. With "produce touch and tapping" as the goal, its useful role is to supply reference firing patterns of natural touch for comparison.
  - NRV was recommended as the whole pipeline. It is built around nerve trunks; whether it covers layered skin and surface electrode arrays is unconfirmed.
  - Nothing prepared the simulator to receive bench data later.
- Decision: accepted.
- Blueprint sections changed: version line, 0, 1, 3, 5.3, 7, 11. New documents: `docs/scope.md`, `docs/reviewers.md`.
- Checklist steps added, changed or retired:
  - Changed: 0.2, 0.3, 0.4, 1.9, 2.1, 3.1, 3.3, 3.4, 3.5, 3.7, 5.2; phase P5 retitled.
  - Added: 1.10 (skin and nerve-ending data), 1.11 (electro-tactile modeling and threshold literature), 2.4 (electrode and stimulus configuration schema), 3.8 (selectivity analysis), 3.9 (method validation on the fingertip), 8.1 (bench-data format for version 2), 8.2 (enter safety limits, later); new phase P8.
  - Retired: none.
- Effect on results already produced: none; no results existed.

## A-003: all electrode and stimulus values are interface inputs; material and skin options; testing order
- Date: 2026-11-13
- Raised by: owner's answers to the remaining scope questions
- Found in step: 0.3
- What was found:
  1. Contact size, spacing, current, pulse width and rate are inputs the user sets in the interface before running; no fixed ranges or layouts.
  2. Regions for version 1: glans and hood. More regions in later versions.
  3. Electrode material is selectable: stainless steel, copper (PCB), silver, gold, titanium. Skin condition is selectable: dry, moist, gelled.
  4. Version 1 represents one approximate anatomy; accepted.
  5. Order of testing: no tests on people in versions 1 or 2; bench safety tests first; then tests on fingers only, to recheck safety and update the safety data.
- Why the current plan does not handle it:
  - Blueprint section 9 said the interface only looks up precomputed results. Free inputs mean the interface must start runs, show progress and cache results.
  - Free inputs still need defaults, model-validity limits and fixed test layouts; nobody was assigned to produce them.
  - Nothing modeled the metal-to-skin interface, so a material selector would have had no effect, or a misleading one.
  - No fingertip preset existed outside the validation step, although the hardware project will measure on fingers first.
- Decision: accepted, with these points stated to the owner:
  - Under current-controlled drive, electrode material changes the driver voltage and interface behavior, not which fibers fire. The interface must say so.
  - Skin condition does change which fibers fire.
  - Finger tests are tests on people and need consent, and possibly ethics approval.
  - Finger results do not transfer directly to the glans or hood.
- Blueprint sections changed: version line, 5.2, 5.3, 9. `docs/scope.md` sections 5, 7, 7a.
- Checklist steps added, changed or retired:
  - Changed: 0.3, 2.4, 3.4, 6.1, 8.1, 8.2.
  - Added: 1.12 (electrode interface values per material and skin condition).
  - Retired: none.
- Effect on results already produced: none; no results existed.

## A-004: the hardware is current-controlled
- Date: 2026-11-13
- Raised by: owner's answer
- Found in step: 0.3
- What was found: the hardware driver is current-controlled.
- Why the current plan does not handle it: the plan kept both drive types open, and nothing represented the driver's voltage limit.
- Decision: accepted. Consequences:
  - The field model's current boundary condition (blueprint 5.3) is the right one; no voltage-driven mode is built.
  - Electrode material does not change which fibers fire, except when the needed voltage exceeds the driver's limit.
  - New input: the driver's voltage limit. New output: the voltage each contact needs, with a flag when it exceeds the limit.
- Blueprint sections changed: version line, 5.3, 9. `docs/scope.md` section 5.
- Confirmed by the owner later the same day: the driver's voltage limit is set by the user in the interface; the version order in `docs/scope.md` section 7 is accepted for now.
- Checklist steps added, changed or retired: changed 0.3, 2.4, 3.4. None added or retired.
- Effect on results already produced: none; no results existed.

## A-005: results of the electro-tactile literature search
- Date: 2026-11-13
- Raised by: agent, from checklist step 1.11
- Found in step: 1.11
- What was found (details and sources in `docs/literature-electrotactile.md`):
  1. Surface electrodes exciting fibers in the skin: confirmed, with the condition that large contacts and high currents reach deeper.
  2. Polarity selecting fiber orientation: supported by a model-based proposal and one psychophysical comparison, not by nerve recordings.
  3. Steady-state field solutions are accepted practice for current-controlled stimulation; two groups checked or argued it.
  4. No fingertip threshold dataset with every parameter was obtained. The most complete dataset found is for the forearm (Zhu 2017).
  5. Published models match trends between settings better than absolute thresholds.
  6. A complete free-tool precedent exists for multi-contact fields by superposition (Araiza Illan 2019, Elmer and Gmsh).
  7. Published dermis conductivities (1.6 to 2.6 S/m) are far above the 0.17 S/m skin value from the first draft, and two papers differ tenfold on the stratum corneum.
- Why the current plan does not handle it:
  - Step 3.9 and blueprint section 3.1 assumed a fingertip dataset exists.
  - Blueprint section 5.3 left the resistive-or-time-dependent question open.
  - The plan did not say that absolute thresholds are expected to be unreliable before calibration.
- Decision: accepted.
  - Step 3.9 validates on the forearm first; the fingertip is added when a complete dataset is obtained.
  - The tissue field is solved in steady state. Capacitance is modeled only for the voltage the driver must supply.
  - Version 1 is described as reliable for comparing settings, not for absolute currents.
  - Skin conductivities are flagged for tracing to primary sources (steps 1.6, 1.10).
- Blueprint sections changed: version line, 0, 3.1, 5.2, 5.3, 11. `docs/scope.md` sections 3, 4, 6.
- Checklist steps added, changed or retired: changed 3.9. None added or retired.
- Effect on results already produced: none; no results existed.

## A-006: literature summary rechecked against the PDFs
- Date: 2026-11-13
- Raised by: agent, after the owner downloaded ten papers into `downloaded-manually/`
- Found in step: 1.11
- What was found:
  1. Validation data exist for the fingertip after all (Malešević 2021: eleven subjects, sensation threshold median 1.0 mA at 400 µs and 30 Hz on 11 mm² pads). This replaces finding 4 of A-005.
  2. Poulsen 2020 gives measured and modeled rheobase for five electrode types on the forearm. The model was 0.2 to 4.6 times the measured value, within a factor of two for three of the five. This puts a number on finding 5 of A-005.
  3. The skin conductivities in the Zhu and Aalborg models come from the same primary sources (Tavernier 1993, Yamamoto 1976, Gabriel 1996), so their agreement is not independent confirmation.
  4. Neither paper defines which direction its anisotropic conductivities refer to.
  5. Corrections to the first write-up: the 2024 review is by Ray, Vasudevan and Manivannan, not Kajimoto's group; Zhu's experiment used gold discs with gel; the COMSOL version attributed to Tigerholm was an extraction error.
  6. PDFs can be read page by page with the Desktop Commander plugin, so the poppler install in step 0.6 is not needed.
  7. Useful design rules from Kajimoto 1999: contact currents sum to zero to keep current local; each pulse averages to zero so charge does not build up.
- Why the current plan does not handle it: step 3.9 named only the forearm data of Zhu 2017; step 0.6 required an install that is no longer needed; the folder for hand-downloaded papers was not ignored by git.
- Decision: accepted.
  - Step 3.9 validates against Poulsen 2020 first (absolute values, five electrodes), then Zhu 2017 (trends), then the fingertip data of Malešević 2021.
  - Step 0.6 is redefined as "confirm papers can be read" and closed.
  - `downloaded-manually/` and all PDFs are ignored by git.
- Blueprint sections changed: version line, 3.1, 5.2. `docs/scope.md` section 6. `docs/literature-electrotactile.md` rewritten.
- Checklist steps added, changed or retired: changed 0.6, 3.9. None added or retired.
- Effect on results already produced: none; no results existed.

## A-007: defaults, allowed ranges, flags and test layouts accepted
- Date: 2026-11-13
- Raised by: agent's proposal for step 0.3; accepted by the owner as written
- Found in step: 0.3
- What was found: every electrode and stimulus input now has a default and an allowed range; three warning flags and six fixed test layouts are defined. All are in `docs/scope.md` section 5, each with a source or marked as an assumption.
- Why the current plan does not handle it:
  - The plan had no forearm region, but two of the four validation layouts are on the forearm.
  - The plan had one flag (driver voltage). Two more are added: current density above 1 mA per mm², and contact area below 10 mm².
  - Nothing recorded that the glans is too small for several large contacts.
- Decision: accepted by the owner on 2026-11-13. Assumptions inside it (contact size default, upper bounds on contact count and current, voltage range, skin condition defaults for glans and hood, the current-density threshold) stay labelled as assumptions and are the first things to revisit when hardware details or an expert's review arrive.
- Blueprint sections changed: version line, 5.3, 9.
- Checklist steps added, changed or retired: changed 0.3, 2.4, 3.4, 6.1. None added or retired.
- Effect on results already produced: none; no results existed.

## A-008: electrode size, shape and spacing limits depend on the region
- Date: 2026-11-13
- Raised by: owner
- Found in step: 0.3 (after acceptance of A-007)
- What was found: the owner wants the minimum and maximum for contact size, shape and distance to depend on the body region selected in the interface, including regions added later.
- Why the current plan does not handle it: A-007 gave one range for all regions, with only the phrase "must fit inside the region". Its single 12 mm maximum also excluded the 15 x 20 mm forearm patch used in test layout T1.
- Decision: accepted.
  - Each region is a preset carrying its dimensions and its own limits. Adding a region means adding a preset.
  - The interface applies model limits (same everywhere) and region limits (from the region's size) together and shows the tighter one.
  - Changing region never silently changes a user's value; an out-of-range value is marked and the run is held.
  - A fourth flag is added: "flat-skin approximation is poor", when a contact is wider than half the region's shorter side.
  - Region dimensions are provisional. Glans and hood sizes are from memory or assumed and are set properly in step 1.10.
- Blueprint sections changed: version line, 5.3, 9. `docs/scope.md` section 5.
- Checklist steps added, changed or retired: changed 1.10, 2.4, 6.1. None added or retired.
- Effect on results already produced: none; no results existed.

## Open questions waiting for an amendment

- Region dimensions for the glans and hood are provisional (step 1.10).

These are known gaps. Each becomes an amendment when it is answered.

- The accepted defaults, ranges, flags and test layouts (A-007) still await the electro-tactile engineer's review (step 0.3).
- Seven small items in `docs/literature-electrotactile.md` section 7 remain uncertain or unread (two need a look at a figure or page image; two papers were not obtained).
- Skin conductivities are not traced to their primary sources, and their direction labels are undefined (steps 1.6, 1.10). Tavernier 1993 is the paper to read.

- The default value for the driver's voltage limit is not yet proposed (step 0.3).
- Defaults, input limits and test layouts are not yet proposed (step 0.3, after step 1.11).
- Interface values for the five materials and three skin conditions have not been found (step 1.12).
- Whether a purely resistive skin model is adequate for dry skin and short pulses is undecided (steps 1.11, 3.4).
- No expert reviewers are found yet; role descriptions are in `docs/reviewers.md` (step 0.4).
- Scan data availability is unconfirmed (step 1.4).
- Axon diameter distribution has no source (step 1.5).
- Whether NRV supports layered skin, surface electrode arrays and fiber endings is unconfirmed (step 1.9).
- Skin layer and nerve-ending data for the glans and hood have not been found (step 1.10).
- The claim that surface electrodes mainly excite fibers in the skin, and the reported effect of polarity on fiber orientation, are written from memory and must be checked (step 1.11).
