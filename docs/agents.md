# Agents: who does what, with which model and effort

Written 2026-11-14 (amendment A-012). The definitions are in `.claude/agents/<name>.md`. Each file sets the model and the effort in its header. The rules for using them are rules 8 to 12 in `CLAUDE.md`.

## The main session

The main session is the orchestrator. It plans, talks to the owner, writes the briefs, checks the results, writes the important files, and makes every commit, push and download request. It also ticks nothing in the expert-review boxes. Only the owner does that.

## The five agents

| Agent | Task | Model | Effort | Tools | Must not |
|---|---|---|---|---|---|
| `literature-scout` | Find and read papers. Return values with page references. | Sonnet 5.5 (`sonnet`) | medium | all | Write repository files. Download or install. |
| `judge` | Decide between models or sources. Reconcile papers that disagree. Draft amendments and expert questions. | Fable 5.2 (`fable`) | high | Read, Grep, Glob, WebFetch, WebSearch | Edit files. Run commands. |
| `builder` | Write code, tests and configuration. Run installs only after the owner approves. | Sonnet 5.5 (`sonnet`) | medium | all | Download or install without approval. Commit. Edit `docs/` or `checklist/`. |
| `numerics-verifier` | Check numbers, solver results and fibre models. Give a second read of any claim. | Opus 5.5 (`opus`) | high | all | Edit repository files. Download or install. |
| `bookkeeper` | Apply exact edits to checklist and docs. Run the checklist test. | Haiku 5.5 (`haiku`) | low | Read, Edit, Write, Grep, Glob, PowerShell | Decide content. Commit. Tick `reviewed`. |

A step in `checklist/steps.js` can set its own model and effort. The step value wins over the agent default. Example: step 3.1 and step 3.2 say Opus 5.5, high, so the builder runs at that level for these steps.

## Two limits found

1. **New agent files load only when a session starts.** The running session did not find the named agents (attempt 1). The main session now starts the general-purpose agent and sets the model and effort on each call. The brief contains the text of the agent file (attempt 2). After a restart, the named agents should be available.
2. **Effort cannot be seen from inside an agent.** The agent can report its model. It cannot report its effort. We trust the value that was set. If an agent seems to work at the wrong level, set the `effort` field in `.claude/agents/<name>.md` by hand and restart the session.

## How the agents were used so far

| Step | Work | Agent and settings |
|---|---|---|
| 2.4 | Configuration schema and layouts | `builder` (Sonnet 5.5, medium); check by `numerics-verifier` (Opus 5.5, high); fix by `builder` |
| 3.1 | FEniCSx solver and tests | `builder` (Opus 5.5, high, set by the step); check by `numerics-verifier` (Opus 5.5, high); fix by `builder` (Opus 5.5, high) |
| 3.2 | Published targets for fibre models | `literature-scout` (Sonnet 5.5, medium) |
| 3.2 | Measure the NRV fibre models | `builder` (Opus 5.5, high) |

The agent that checks work is never the agent that wrote it.

## How to change a setting

Open `.claude/agents/<name>.md`. Change the `model` or `effort` line in the header. Restart the session. Record the change and the reason in `docs/amendments.md`.
