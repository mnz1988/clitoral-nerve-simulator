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

## Open questions waiting for an amendment

These are known gaps. Each becomes an amendment when it is answered.

- Scope and intended use are not decided (step 0.2).
- Electrode and stimulus are not specified (step 0.3).
- No expert reviewers are named (step 0.4).
- Scan data availability is unconfirmed (step 1.4).
- Axon diameter distribution has no source (step 1.5).
- What NRV supports for perineurium, skin layers and custom geometry is unconfirmed (step 1.9).
