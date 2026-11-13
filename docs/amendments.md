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

## Open questions waiting for an amendment

These are known gaps. Each becomes an amendment when it is answered.

- Realistic ranges for contact size, spacing, current, pulse width and rate are not given (step 0.3).
- Which regions come first, electrode material and skin interface are not given (step 0.3).
- No expert reviewers are found yet; role descriptions are in `docs/reviewers.md` (step 0.4).
- Scan data availability is unconfirmed (step 1.4).
- Axon diameter distribution has no source (step 1.5).
- Whether NRV supports layered skin, surface electrode arrays and fiber endings is unconfirmed (step 1.9).
- Skin layer and nerve-ending data for the glans and hood have not been found (step 1.10).
- The claim that surface electrodes mainly excite fibers in the skin, and the reported effect of polarity on fiber orientation, are written from memory and must be checked (step 1.11).
