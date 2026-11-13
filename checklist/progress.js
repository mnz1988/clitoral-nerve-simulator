// Saved checklist progress. Replace this file with the one the Export button
// in index.html downloads, then commit it.
window.PROGRESS = {
  "updated": "2026-11-13T21:50:28.144Z",
  "steps": {
    "0.1": {
      "status": "done",
      "verified": false,
      "reviewed": false,
      "fails": 0,
      "t": 1794572210874,
      "notes": "2026-11-13: owner created the GitHub repository and pushed. `git status -sb` shows main tracking origin/main (first check passed). Second check, the GitHub page listing the files, was not run by the agent: tick Verified after looking at the page."
    },
    "0.2": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "t": 1794572210874,
      "notes": "2026-11-13: owner decided the scope. Recorded in docs/scope.md and amendment A-002. Later steps were re-mapped to the question in the same amendment."
    },
    "0.3": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "t": 1794585769204,
      "notes": "2026-11-13: defaults, allowed ranges, three warning flags and six test layouts are in docs/scope.md section 5, each with a source or the word assumption; a default for the driver's voltage limit is recorded (150 V). The owner accepted them as written (amendment A-007). All three verification checks pass. Still open: review by the electro-tactile engineer (role B in docs/reviewers.md); the owner ticks that box. Process note: once step 1.11 was verified this took one pass; Opus 5.5 at medium is enough."
    },
    "0.4": {
      "status": "doing",
      "verified": false,
      "reviewed": false,
      "fails": 0,
      "t": 1794572210874,
      "notes": "2026-11-13: six role descriptions written in docs/reviewers.md. Owner will search for and contact candidates."
    },
    "0.5": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "t": 1794572210874,
      "notes": "2026-11-13: F 379 GB free of 466. C 16 GB free. RAM 64 GB. CPU Intel Core i3-13100F, 4 cores, 8 threads. GPU NVIDIA RTX 3080 Ti. `wsl --status` reports default version 2; no Linux distribution installed. Consequence: install WSL distribution on F (step 2.1). Next time: one PowerShell call is enough; Haiku 5.5 at low is sufficient."
    },
    "1.11": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "t": 1794585178568,
      "notes": "2026-11-13: rewritten from the PDFs in downloaded-manually/ (amendment A-006). Verification: every value carries a PDF page number; six pages were re-read directly and matched; all ten citations confirmed against OpenAlex or arXiv. Three models summarized; both claims confirmed with sources and conditions; validation datasets found for forearm (Poulsen 2020, Zhu 2017) and fingertip (Malesevic 2021). Seven small items remain uncertain or unread and are listed in section 7 of docs/literature-electrotactile.md. Expert review still needed. Process note: three Sonnet 5.5 agents did the extraction for about 416,000 tokens; for short papers, reading the relevant pages directly is cheaper. Fable 5.2 at high was right for judging which model to follow; the lookups themselves suit Sonnet 5.5."
    },
    "0.6": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-13: redefined by amendment A-006. PDFs are read with the Desktop Commander plugin's read_file; poppler was not installed and is not needed. Evidence: six pages read directly and matched against extracted values (Zhu p.3, Araiza-Illan p.5, Malesevic p.7, Kajimoto pp.6-7, Cavalcanti p.4, Poulsen p.19). Limits: figures are not readable; minus signs and superscripts can be lost in tables.",
      "t": 1794585178568
    },
    "1.10": {
      "status": "doing",
      "verified": false,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-14, fifth pass (Sonnet 5.5; step recommends Fable 5.2 / high). See docs/literature-glans-hood.md sections 1-9 and A-009. Sizes and corpuscle types checked in PDFs; Jackson 2019 and Shih 2013 abstracts only (owner could not get full texts: AJOG zip was an unrelated issue bundle, Shih paywalled). Conductivity: IT-IS V5.0 read; Vagina value is a copy of intestine/stomach/oesophagus, Mucous Membrane a copy of muscle/tongue, Penis a copy of blood vessel wall. Only Skin (0.148 S/m, range 0.057-0.25) is usable; glans/inner-hood conductivity has no proxy and is a swept assumption (0.06-0.5 S/m). STILL MISSING: layer thickness, nerve-ending depth, usable density. Step stays doing. Decision pending: try one search for an open copy of Jackson 2019, or skip.",
      "t": 1794604164514
    },
    "1.9": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-14 (Sonnet 5.5, as recommended). Read the source of NRV 1.4.0 (commit 7dc11954), not run. Findings in docs/nrv-capabilities.md and amendment A-010. Result: hybrid plan; custom 3D mesh with layered domains, thin layers, Dirichlet/Neumann surfaces and external per-contact footprints that NRV scales and sums; no skin geometry, flat surface electrodes, terminal-ending fibres or Zhu/Aalborg models; fibres straight along x. The check \"links to documentation pages for the installed version\" could not be met (rendered docs returned only a nav index twice; nothing installed); the owner accepted source-file links of v1.4.0 instead on 2026-11-14, so verified. Untested items are in section 4 of the findings file (needs install, step 2.x). Process: a shallow git clone and grep of the source answered more in 6 calls than 6 documentation fetches; start with the clone next time (docs/ checkout fails on Windows long paths; nrv/ is complete).",
      "t": 1794605865065
    },
    "2.1": {
      "status": "doing",
      "verified": false,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-14 (Sonnet 5.5 / low). Ran: wsl --install Ubuntu-22.04 --location F:\\WSL\\Ubuntu-22.04 --no-launch (owner approved the download). Result: wsl -l -v shows Ubuntu-22.04, VERSION 2; disk file F:\\WSL\\Ubuntu-22.04\\ext4.vhdx (1.3 GB) is on drive F; guest is Ubuntu 22.04.5 LTS. The command printed ERROR_ALREADY_EXISTS yet the distribution was installed and runs (probably a second pass over an install that had already completed). No Linux user exists yet: owner must open Ubuntu once and choose a username and password (agent does not enter passwords). Still to do: Miniforge install and conda --version check, so the step is not done. Process: --location and --no-launch work on WSL 3.0.5 from a non-admin shell; nesting quotes with awk in a wsl bash -c call from PowerShell breaks; use getent or a script file.",
      "t": 1794606628144
    }
  },
  "amendments": []
};
