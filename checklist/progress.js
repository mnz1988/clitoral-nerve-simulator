// Saved checklist progress. Replace this file with the one the Export button
// in index.html downloads, then commit it.
window.PROGRESS = {
  "updated": "2026-11-13T00:00:00.000Z",
  "steps": {
    "0.1": {
      "status": "done", "verified": false, "reviewed": false, "fails": 0, "t": 1794572210874,
      "notes": "2026-11-13: owner created the GitHub repository and pushed. `git status -sb` shows main tracking origin/main (first check passed). Second check, the GitHub page listing the files, was not run by the agent: tick Verified after looking at the page."
    },
    "0.2": {
      "status": "done", "verified": true, "reviewed": false, "fails": 0, "t": 1794572210874,
      "notes": "2026-11-13: owner decided the scope. Recorded in docs/scope.md and amendment A-002. Later steps were re-mapped to the question in the same amendment."
    },
    "0.3": {
      "status": "doing", "verified": false, "reviewed": false, "fails": 0, "t": 1794573803588,
      "notes": "2026-11-13: owner decided all values are interface inputs; regions glans and hood; materials stainless steel, copper (PCB), silver, gold, titanium; skin dry, moist, gelled (amendment A-003). Drive type: current-controlled (A-004). Still open: the driver's voltage limit, if the owner knows it; defaults, input limits and test layouts to be proposed by the agent after step 1.11."
    },
    "0.4": {
      "status": "doing", "verified": false, "reviewed": false, "fails": 0, "t": 1794572210874,
      "notes": "2026-11-13: six role descriptions written in docs/reviewers.md. Owner will search for and contact candidates."
    },
    "0.5": {
      "status": "done", "verified": true, "reviewed": false, "fails": 0, "t": 1794572210874,
      "notes": "2026-11-13: F 379 GB free of 466. C 16 GB free. RAM 64 GB. CPU Intel Core i3-13100F, 4 cores, 8 threads. GPU NVIDIA RTX 3080 Ti. `wsl --status` reports default version 2; no Linux distribution installed. Consequence: install WSL distribution on F (step 2.1). Next time: one PowerShell call is enough; Haiku 5.5 at low is sufficient."
    }
  },
  "amendments": []
};
