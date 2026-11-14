// Saved checklist progress. Replace this file with the one the Export button
// in index.html downloads, then commit it.
window.PROGRESS = {
  "updated": "2026-11-14T13:19:22.695Z",
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
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-14 (Sonnet 5.5 / low, as recommended). Evidence for the three checks: (1) wsl -l -v shows Ubuntu-22.04, VERSION 2; (2) disk file F:\\WSL\\Ubuntu-22.04\\ext4.vhdx is on drive F; (3) conda --version inside Ubuntu prints conda 26.9.4 (Miniforge3 release 26.9.4-2, installed to ~/miniforge3, default channel conda-forge). The installer (128,272,241 bytes) matched the sha256 published in the GitHub release metadata (bbaf16b3...edbbdf); the .sha256 file URL returned 404 on the first try, so the release API was used instead. conda init added lines to the Linux ~/.bashrc only. Linux user: moji. Base Python is 3.14.10; NRV needs 3.12, so step 2.2 must create a separate environment. Process: write bash scripts to a file and run with wsl bash /mnt/f/...; inline quotes break. Release API gives the hash when no .sha256 asset exists.",
      "t": 1794607389992
    },
    "2.2": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-14 (Sonnet 5.5 / medium, as recommended). Owner approved the downloads (391 MB conda, then pip). Attempt 1 of the conda install failed with HTTP 000 connection failed on one package; attempt 2 changed the settings (1 download thread, 8 retries, longer timeouts) and succeeded. Environment nrv: python 3.12.13, fenics-dolfinx 0.9.0, python-gmsh 4.15.2, mpich 4.3.2, petsc 3.24.4, nrv-py 1.4.0 (pip), neuron 9.0.2. First import compiled nothing because make and a C++ compiler were missing (nrnivmodl exit 127) and left an empty x86_64 folder that NRV took for a finished build; fix: conda install make gxx_linux-64 gcc_linux-64 (16 MB), delete the folder, re-import: libnrnmech.so built. Checks: (1) python -c import nrv prints NRV 1.4.0. (2) Tutorial 1 run headless: unmyelinated HH d=1 um L=5000 um: same 55.5 mV rise above rest at 20/50/80 pct points, peak times 3.46/7.30/11.14 ms, 0.39 m/s (tutorial text says about 0.4 m/s); myelinated MRG d=10 um, 20 nodes (21.85 mm): spikes at nodes along the whole fibre, peak times 1.10 to 1.43 ms, fitted 57.5 m/s (not compared with a published value; 3.2 will). My first measurement script sampled internode points and had a formatting bug; both were script errors, not install failures. Open oddity: peak times at interior nodes were not strictly increasing in the quick check (duplicate segments at the same x were not investigated). (3) environment.yml written at the repo root from conda env export (pip packages pinned with ==). Recreation from the file is tested in step 2.3. Process: install compilers before first import; use script files for WSL commands; check dry-run size before download.",
      "t": 1794657255242
    },
    "2.3": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-14 (Sonnet 5.5 / medium, as recommended). Added pyproject.toml (pytest, ruff), sim/__init__.py, axons/README.md (CSV format from blueprint section 14), tests/test_environment.py (5 smoke tests: NRV, dolfinx, Gmsh, NEURON versions match environment.yml pins). Installed pytest 9.2.0 and ruff 0.17.5 into nrv (9 MB, owner approved) and re-exported environment.yml. Check 1: pytest in WSL: 5 passed; ruff check passes and ruff format applied to sim/ and tests/. Check 2: fresh git clone of the committed repo into ~/rebuild_test, conda env create -n nrv_rebuild_test -f environment.yml succeeded (dry run showed 0 packages to fetch because of the local conda cache, so this does not prove a clean machine could download everything), then pytest in that env: 5 passed. Test env and clone removed afterwards. Not done: the quick-gate-python plugin named in the step is not installed and was not used; CI and pre-commit are not set up; the scaffold lives in the same repository as the docs (blueprint section 14 layout), no separate code repo. The first run after env creation compiles NRV mods again (about 20 s). Process: dry-run the rebuild to see whether anything is downloaded before asking.",
      "t": 1794658995089
    },
    "2.4": {
      "status": "done",
      "verified": true,
      "reviewed": false,
      "fails": 0,
      "notes": "2026-11-14 (orchestrated: builder = Sonnet 5.5 / medium wrote it; numerics-verifier = Opus 5.5 / high checked it independently; builder fixed the findings; orchestrator reran the checks). Files: sim/config/ (errors, units, limits, layout, model_limits.yaml, regions/glans|hood|fingertip|forearm.yaml), examples/layouts/T1..T6, tests/test_config.py. Checks: all example files load; out-of-limit values rejected with the reason; T1 accepted on the forearm and rejected on the glans; adding a region needs only a new YAML file (tested with a temporary thigh.yaml); missing units, overlap, unbalanced currents rejected; pytest 75 passed in total, ruff check and ruff format --check clean. Verifier probes (20 inputs) and 20 single-line code mutations: first run 6 mutations survived and 3 inputs were wrongly accepted; after the fix pass all 20 mutations are killed and the probes behave (orchestrator reran the scripts). Verifier also confirmed every default, range, flag threshold and region size against scope.md section 5. Four warning flags exist: small_contact, current_density, flat_skin_approximation_poor, net_charge_per_pulse, plus return_share_exceeds_unit; the driver-voltage flag needs the solver (later). Labels the code added where scope.md gave none are assumption. Open owner decisions are in docs/amendments.md (open questions): current_share sign, T1-T4 and T6 placeholders, editable region size, scope.md table rows out of place. Not covered: primary sources behind labels were not rechecked. Process: give the builder the verifier mutation list as test-name targets; interphase gap maximum is 1 ms.",
      "t": 1794662362695
    }
  },
  "amendments": []
};
