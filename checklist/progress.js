// Saved checklist progress. Replace this file with the one the Export button
// in index.html downloads, then commit it.
window.PROGRESS = {
  "updated": "2026-11-13T20:54:49.083Z",
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
      "notes": "2026-11-14, three passes (Sonnet 5.5; step recommends Fable 5.2 / high). Details in docs/literature-glans-hood.md and amendment A-009. Checked in PDFs: Longhurst 2024 (glans 6.40 x 5.14 mm, prepuce length 23.19 mm), Garcia-Mesa 2020 (corpuscle types; no depths; density unit unreliable). Abstracts only: Jackson 2019 (glans 8 x 4 mm cadaver; nerve density numbers need full text), Shih 2013 (1-14 corpuscles per 100x field, field area unknown). Sources disagree on Pacinian corpuscles in the glans. NOT found: layer thickness, nerve depth, usable density, conductivity of glans/hood skin. Conductivity proxy: two attempts (PubMed; IT-IS page without table) failed, stopped per rule 1; options in section 8 of the findings file (download IT-IS spreadsheet, accept Gabriel 1996 wet-skin/mucosa values as labelled assumption, or sweep a range). Step stays doing. Process: read PDFs directly with Desktop Commander read_file; PubMed search needs 2-3 terms.",
      "t": 1794603289083
    }
  },
  "amendments": []
};
