# Working rules for this repository

Read these before doing any step. They are the owner's standing instructions.

## Where things are

- `docs/blueprint.md`: the plan. Every number carries a label: measured, literature or assumption.
- `checklist/steps.js`: step definitions (what to do, how to verify, who reviews, model, tools).
- `checklist/progress.js`: saved progress. `checklist/index.html` is the interactive view.
- `docs/amendments.md`: every change to the plan, with its reason.

## Rules

1. **Two failed attempts, then stop.** If a task fails, try at most once more, and change something on the second try (approach, model or effort level). After two failures, stop. Record both attempts in the step's notes, set the step to blocked, and tell the owner what was tried, why it failed, and the options: fix it by hand, change the approach, or drop the step. Do not make a third attempt without the owner's decision.

2. **Say what is missing.** If a request or the plan leaves out something that would make the process or the result more accurate or realistic, tell the owner, every time, before or alongside the work. Do not silently fill the gap with a guess.

3. **No assumption presented as fact.** Keep the three labels in code, documents and interface. Cite the source of every measured or literature value. Mark anything not checked against its primary source as unverified.

4. **A step is complete only when verified.** Run the step's verification checks and record the evidence in its notes before marking it verified. Only the owner ticks an expert-review box, after a named person has answered the step's question. An AI opinion is not an expert review.

5. **Changes go through amendments.** New subjects, problems, contradictions and scope changes are written into `docs/amendments.md` and folded into the blueprint and `checklist/steps.js` in the same commit. Never reuse a retired step id.

6. **Keep the checklist current.** When a step's state changes, update `checklist/progress.js` (same shape the Export button writes; set `t` to the current time in milliseconds so the page prefers it over older browser state). After any change to `steps.js`, `progress.js` or `index.html`, run `node checklist/test_checklist.js checklist` and commit only if it passes.

7. **No data in the repository.** Scans, segmentations, third-party meshes and papers stay under ignored folders.

## Spending fewer tokens

- Use the model and effort level written on the step. Go one level up only after a failed attempt; go down when a step proves easy, and record that in `steps.js`.
- Use the skills and plugins named on the step instead of doing the work by hand.
- For wide searches use a search subagent and keep only the conclusion.
- Never load scan volumes, meshes or whole PDFs into context; read the pages or values needed.
- Do not re-read files that have not changed. Do not re-derive facts already recorded in the notes.
- Precompute and cache simulation results; do not rerun to re-read a number.

## Improving the process

At the end of each step, add one line to its notes: what would make this step cheaper or more accurate next time. When the evidence shows a different model, effort level, tool or check works better, update that step in `checklist/steps.js` in the same commit.

## Environment facts

- Windows 11, PowerShell. NRV and FEniCSx need WSL2.
- `scoop` and `rtk` are installed. `gh` and `poppler` were not installed on 2026-11-13.
- Reading papers (seen 2026-11-13): PubMed Central and Frontiers pages load with the web fetch tool. MDPI, bioRxiv, DOAJ, SciELO and university repository PDFs refused or failed. Do not retry those; ask the owner to download the PDF into `data/papers/`, or use a browser the owner is signed in to.
