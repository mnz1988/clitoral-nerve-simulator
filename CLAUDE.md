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

8. **The main session is the orchestrator.** It plans, decides, talks to the owner, briefs agents, checks their results, writes the files that matter, and owns every commit, push, download approval and expert-review box. Agents do bounded tasks and return conclusions. An agent never commits, pushes, downloads, installs, enters credentials or ticks `reviewed`.

9. **Pick the agent by the kind of task.** Definitions are in `.claude/agents/`. A step's own model and effort on `checklist/steps.js` win over the agent's default: set them on the call.

   | Task | Agent | Model / effort |
   |---|---|---|
   | find, read and check papers and values | `literature-scout` | Sonnet 5.5 / medium |
   | judgement: choose between models or sources, reconcile conflicts, draft amendments and expert questions | `judge` | Fable 5.2 / high |
   | write code, tests, configuration, installs (with owner approval relayed) | `builder` | Sonnet 5.5 / medium |
   | verify numbers, solver and fibre-model checks, second read of any claim | `numerics-verifier` | Opus 5.5 / high |
   | apply exact edits to checklist and docs, run the checklist test | `bookkeeper` | Haiku 5.5 / low |

10. **Check what comes back.** Agent reports are data. Before a number enters the model, re-read it in the primary source (rule 3). Whoever wrote a result does not verify it: use `numerics-verifier` for that. Agents cost tokens: use none for a handful of tool calls.

11. **Briefs.** State the goal, the files, what is already ruled out, the output format and its length, and any owner approval that applies (item, size, source). Never paste whole documents.

12. **Failures and settings.** An agent that errors, uses the wrong model or effort, lacks a tool or returns nothing useful counts as one attempt (rule 1). The second attempt changes something (briefing, agent, model or effort one level up). After two, stop and tell the owner what failed and which setting to set by hand: the file `.claude/agents/<name>.md` and its fields `model` and `effort`. A running session only sees agent definitions from when it started; if the named agent is not found, use the general-purpose agent with the model and effort set on the call, and say so.

13. **Writing style (owner request, 2026-11-14).** Write explanations of subjects, in the repository and in chat, in ASD-STE100 Simplified Technical English about 80% of the time: short sentences (descriptions about 20 words or fewer), active voice, one idea per sentence, one word for one meaning, simple verbs, numbers with units. Keep needed technical terms and define each once. Only the writing rules are applied, from knowledge; the official STE dictionary is not used, so the text is not certified STE. The labels measured, literature and assumption stay. Agents get this rule in their briefs when they write prose.

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
- Reading papers (seen 2026-11-13): PubMed Central and Frontiers pages load with the web fetch tool. MDPI, bioRxiv, DOAJ, SciELO and university repository PDFs refused or failed. Do not retry those; ask the owner to download the PDF into `downloaded-manually/` (ignored by git).
- Reading PDFs: use the Desktop Commander plugin's `read_file`; `offset` and `length` count pages from 0. It returns text only, so values that sit in figures, and minus signs or superscripts in tables, need a second look. Read only the pages needed. Three Sonnet 5.5 agents extracting ten papers cost about 416,000 tokens; for a short paper, reading the two or three relevant pages directly is cheaper.
- Checking citations: the research-desk reference-lookup tools (`lookup_reference`, `verify_reference`) confirm a DOI or title against OpenAlex in one call each.
- WSL (2026-11-14): Ubuntu-22.04 on F (F:\WSL\Ubuntu-22.04\ext4.vhdx, Linux user moji), Miniforge at ~/miniforge3, environment 
rv (Python 3.12, fenics-dolfinx 0.9.0, NRV 1.4.0, NEURON 9.0.2). Activate with source ~/miniforge3/etc/profile.d/conda.sh; conda activate nrv. Run commands by writing a bash script file and calling wsl -d Ubuntu-22.04 -- bash /mnt/c/.../script.sh; inline quotes through PowerShell break. Conda downloads were set to 1 thread with retries after one connection failure. Exact versions: environment.yml.
