// Checklist definitions. Edit this file to add, change or retire steps.
// Progress is NOT stored here; it lives in progress.js and in the browser.
// Text in `backticks` is shown as code. Model and effort are starting
// recommendations (estimates, not measurements): lower them when a step
// proves easy, raise them only after a failed attempt.
window.CHECKLIST = {
  version: "2026-11-13, amendment A-005",
  phases: [
    { id: "P0", title: "Setup and decisions" },
    { id: "P1", title: "Sources: find, download, check" },
    { id: "P2", title: "Software environment" },
    { id: "P3", title: "Idealized nerve model (milestones M1, M2)" },
    { id: "P4", title: "Scan-derived geometry (milestones M3, M4)" },
    { id: "P5", title: "Natural-touch reference patterns (milestone M5)" },
    { id: "P6", title: "Interface (milestone M6)" },
    { id: "P7", title: "Review before sharing" },
    { id: "P8", title: "Version 2: data from the hardware project (later)" }
  ],
  steps: [
    // ---------------------------------------------------------------- P0
    {
      id: "0.1", phase: "P0", kind: "do", who: "you",
      title: "Put the repository on GitHub",
      what: [
        "Create an empty repository at github.com/new (no README, no .gitignore, no license).",
        "Add it as the remote and push `main`."
      ],
      verify: [
        "`git -C F:/clitoral-nerve-simulator status -sb` prints `## main...origin/main`.",
        "The GitHub page lists README.md, CLAUDE.md, docs and checklist."
      ],
      review: null,
      model: "Haiku 5.5", effort: "low", why: "Two git commands.",
      tools: ["git"], needs: [], blueprint: ""
    },
    {
      id: "0.2", phase: "P0", kind: "decide", who: "you",
      title: "Decide the scope and the one question the model must answer",
      what: [
        "Decided on 2026-11-13: a test bench for surface electro-tactile stimulation with adjustable electrodes and waveforms, as accurate as open data allows. See `docs/scope.md`.",
        "Reopen only through an amendment."
      ],
      verify: [
        "The decision is written in `docs/scope.md`.",
        "Every later step you keep can be traced to that question; steps that cannot are dropped through an amendment."
      ],
      review: null,
      model: "Opus 5.5", effort: "medium", why: "Only to talk the trade-offs through; the decision is yours.",
      tools: [], needs: [], blueprint: "0"
    },
    {
      id: "0.3", phase: "P0", kind: "decide", who: "you+ai",
      title: "Agree defaults, input limits and test layouts for the interface",
      what: [
        "Decided on 2026-11-13: every electrode and stimulus value is an input in the interface; regions are glans and hood; material and skin condition are selectable. See `docs/scope.md` section 5.",
        "The agent proposes, from the electro-tactile literature (step 1.11): a default for each input, the limits inside which the model is valid, and a few fixed layouts for automated tests. Each is labelled an assumption.",
        "You accept or change them.",
        "Drive type decided on 2026-11-13: current-controlled.",
        "The driver's voltage limit is set by the user in the interface (decided 2026-11-13); it needs a default like every other input."
      ],
      verify: [
        "Defaults, input limits and test layouts are in `docs/scope.md` section 5, each with a source or the word assumption.",
        "A default for the driver's voltage limit is recorded.",
        "You have accepted them (say so in this step's notes)."
      ],
      review: {
        who: "Electro-tactile stimulation engineer (role B in `docs/reviewers.md`)",
        ask: "Are these defaults and limits realistic for thin or moist skin, and do they cover what the hardware will actually use?"
      },
      model: "Opus 5.5", effort: "medium", why: "Needs care with units and with what the model can validly represent.",
      tools: [], needs: ["0.2", "1.11"], blueprint: "5.3, 9"
    },
    {
      id: "0.4", phase: "P0", kind: "find", who: "you",
      title: "Find your expert reviewers",
      what: [
        "Six roles are described in `docs/reviewers.md`: the expertise required, how to recognise a fit, where to look, search terms, and the questions to ask.",
        "Search for two or three candidates per role, in the priority order given there, and contact them.",
        "The safety role (F) can wait for the hardware project."
      ],
      get: ["One named person per role, or a written decision to go without that review."],
      verify: [
        "Each step with an expert-review box has a person assigned (role and initials in `docs/scope.md`; keep contact details out of the repository)."
      ],
      review: null,
      model: "Sonnet 5.5", effort: "low", why: "Only to draft outreach messages; you send them.",
      tools: [], needs: [], blueprint: "10.2"
    },
    {
      id: "0.5", phase: "P0", kind: "do", who: "ai",
      title: "Check the machine",
      what: [
        "Free space on drive F, installed RAM, CPU cores, whether WSL2 is installed.",
        "Rough needs (estimates): 20 GB for Phase 3; several hundred GB and 32 GB RAM or more for scan work in Phase 4."
      ],
      verify: ["The numbers are pasted into this step's notes.", "`wsl --status` runs without error."],
      review: null,
      model: "Haiku 5.5", effort: "low", why: "Reading system facts.",
      tools: ["PowerShell"], needs: [], blueprint: "1"
    },
    {
      id: "0.6", phase: "P0", kind: "do", who: "ai",
      title: "Install PDF tooling so papers can be read",
      what: [
        "Install poppler (`scoop install poppler`). On 2026-11-13 the agent could not read the preprint PDF because `pdftoppm` was missing."
      ],
      verify: ["`pdftoppm -v` prints a version.", "The agent reads page 1 of the preprint and quotes its title."],
      review: null,
      model: "Haiku 5.5", effort: "low", why: "One install command.",
      tools: ["scoop", "pdf skill"], needs: [], blueprint: ""
    },
    {
      id: "0.7", phase: "P0", kind: "do", who: "you",
      title: "Fix GitHub access for the agent (optional)",
      what: [
        "The GitHub connector failed on 2026-11-13 with an authorization-header error, and the `gh` command is not installed.",
        "Either reconnect the GitHub plugin, or install `gh` and run `gh auth login`."
      ],
      verify: ["The agent can list the repository's files on GitHub."],
      review: null,
      model: "Haiku 5.5", effort: "low", why: "Configuration only.",
      tools: ["GitHub plugin"], needs: ["0.1"], blueprint: ""
    },

    // ---------------------------------------------------------------- P1
    {
      id: "1.1", phase: "P1", kind: "download", who: "you+ai",
      title: "Tunçkol 2024 paper and its supplement",
      what: ["Download the PDF and any supplementary files into `data/papers/` (not committed)."],
      get: ["Tunçkol et al., Sci Rep 2024, doi:10.1038/s41598-024-72898-8"],
      verify: [
        "Each value in blueprint section 2 (bundles, axon counts, myelinated fraction) matches a table or sentence in the paper; page numbers recorded in the notes.",
        "Confirm by reading that no axon diameters are reported."
      ],
      review: null,
      model: "Sonnet 5.5", effort: "medium", why: "Careful reading of one paper.",
      tools: ["pdf skill", "Bio Research plugin (PubMed)", "reference-checking plugin"], needs: ["0.6"], blueprint: "2"
    },
    {
      id: "1.2", phase: "P1", kind: "find", who: "you",
      title: "Ask the Tunçkol authors for raw data",
      what: [
        "The paper says data are available on reasonable request. Ask for axon diameters or the histology images.",
        "The agent can draft the message; you send it."
      ],
      get: ["Axon diameter measurements for the dorsal nerve of the clitoris."],
      verify: ["A reply is on file, or three weeks have passed and the outcome is recorded in the notes."],
      review: null,
      model: "Sonnet 5.5", effort: "low", why: "Drafting a short message.",
      tools: [], needs: ["1.1"], blueprint: "2"
    },
    {
      id: "1.3", phase: "P1", kind: "find", who: "you+ai",
      title: "Read the 2026 HiP-CT preprint in full",
      what: [
        "Extract: voxel sizes, donor identifiers, data-availability statement, dataset DOIs, trunk count and diameters, how nerves were segmented.",
        "Copy the PDF into `data/papers/`."
      ],
      get: ["Neuroanatomy of the clitoris, bioRxiv 2026, doi:10.64898/2026.03.18.712572"],
      verify: [
        "Every extracted value carries a page number.",
        "You spot-check five values against the PDF yourself.",
        "Blueprint section 2 is updated; the words 'from press coverage' are gone."
      ],
      review: null,
      model: "Opus 5.5", effort: "high", why: "Everything in Phase 4 depends on these facts being right.",
      tools: ["pdf skill", "Bio Research plugin (bioRxiv; the site blocked plain fetching)"], needs: ["0.6"], blueprint: "2, 4"
    },
    {
      id: "1.4", phase: "P1", kind: "find", who: "you+ai",
      title: "Confirm the scan data can actually be downloaded",
      what: [
        "Find the female genitalia datasets on human-organ-atlas.esrf.eu.",
        "Record: dataset DOI, resolution levels, size in GB, license, download method.",
        "If it is not public: open an amendment. Options are to ask the authors, or to stay with the idealized model."
      ],
      get: ["Dataset DOI and a working download route."],
      verify: [
        "The DOI resolves.",
        "The file list is visible when signed in.",
        "One small file downloads and opens."
      ],
      review: null,
      model: "Sonnet 5.5", effort: "medium", why: "Web navigation and record keeping.",
      tools: ["built-in browser"], needs: ["1.3"], blueprint: "2, 4"
    },
    {
      id: "1.5", phase: "P1", kind: "find", who: "you+ai",
      title: "Find an axon diameter distribution",
      what: [
        "Search: Peters et al. 2023, other histology of the dorsal nerve of the clitoris and the pudendal nerve.",
        "If nothing human and female exists, choose a distribution, say why, and label it an assumption.",
        "Write the choice into `axons/README.md`."
      ],
      get: ["A diameter distribution with source, sample size, method and figure or table reference."],
      verify: [
        "Each candidate source is listed with what it measured and how.",
        "The chosen distribution states its label (measured or assumption) and the range to use in sensitivity analysis."
      ],
      review: {
        who: "Neuroanatomist",
        ask: "Is this diameter distribution plausible for the dorsal nerve of the clitoris, and is the sensitivity range wide enough?"
      },
      model: "Fable 5.2", effort: "high", why: "Judgment under thin evidence; this is the largest unknown in Mode A.",
      tools: ["Bio Research plugin (PubMed)", "research-superpowers (literature-review)", "reference-checking plugin", "WebSearch"],
      needs: ["1.1"], blueprint: "2"
    },
    {
      id: "1.6", phase: "P1", kind: "do", who: "ai",
      title: "Check every citation and conductivity marked (verify)",
      what: [
        "For each row in blueprint section 5.2, each model in section 6 and each reference written from memory: find the primary source and confirm the value.",
        "Log each mismatch as an amendment."
      ],
      verify: [
        "Every row has a DOI and a page or table number.",
        "No '(verify)' tag remains in the blueprint, or each remaining one has a reason in the amendments log."
      ],
      review: null,
      model: "Opus 5.5", effort: "high", why: "Wrong constants silently corrupt every result. Sonnet 5.5 at medium can do the lookups if Opus checks the mismatches.",
      tools: ["reference-checking plugin", "Bio Research plugin (PubMed)", "pdf skill"], needs: [], blueprint: "5.2, 6"
    },
    {
      id: "1.7", phase: "P1", kind: "find", who: "you+ai",
      title: "Collect validation targets from the clinical literature",
      what: [
        "Dorsal genital nerve stimulation: perception and tolerance thresholds, with electrode size, position and pulse width.",
        "Pudendal evoked-potential latency and bulbocavernosus (clitoral-anal) reflex latency.",
        "Write them into `docs/validation-targets.md`."
      ],
      get: ["A table of human measurements the model can be compared with."],
      verify: ["Each target lists source, sample size, electrode, stimulus and value with spread."],
      review: {
        who: "Clinical neurophysiologist or urologist",
        ask: "Are these measurements comparable to the modeled setup, and which are trustworthy enough to validate against?"
      },
      model: "Fable 5.2", effort: "high", why: "Deciding what counts as a fair comparison.",
      tools: ["Bio Research plugin (PubMed)", "research-superpowers (literature-review)", "reference-checking plugin"],
      needs: ["0.3"], blueprint: "10.2"
    },
    {
      id: "1.8", phase: "P1", kind: "download", who: "you+ai",
      title: "Pelvis context models",
      what: [
        "Download NIH 3D entry 3DPX-017321.",
        "Find the Geneva 3D pelvic kit and read its license before using it."
      ],
      get: ["NIH 3DPX-017321 (CC-BY)", "Geneva kit, PMID 32675048 (license unknown)"],
      verify: ["Each model opens in Blender or ParaView.", "License and source are recorded in `data/README.md`."],
      review: null,
      model: "Sonnet 5.5", effort: "low", why: "Download and record.",
      tools: ["built-in browser"], needs: [], blueprint: "2"
    },
    {
      id: "1.9", phase: "P1", kind: "find", who: "ai",
      title: "Check what NRV can and cannot do",
      what: [
        "Confirm against the documentation of the version you will install: which fiber models ship with it, thin-layer perineurium, importing custom geometry.",
        "The key question after amendment A-002: can it model layered skin, arrays of surface contacts and fibers that end in the tissue? If not, the skin model is built with Gmsh and FEniCSx directly and NRV supplies only the fiber models.",
        "Anything missing becomes an amendment before coding starts."
      ],
      verify: ["Each capability is linked to a documentation page for the installed version."],
      review: null,
      model: "Sonnet 5.5", effort: "medium", why: "Reading documentation.",
      tools: ["WebFetch"], needs: [], blueprint: "1, 5.2, 6"
    },
    {
      id: "1.10", phase: "P1", kind: "find", who: "you+ai",
      title: "Find skin and nerve-ending data for the glans and hood",
      what: [
        "Thickness of the surface layer and the layers beneath it, per region.",
        "Depth, density, type and orientation of nerve endings and fine branches (genital corpuscles, free endings).",
        "Conductivity of thin and moist skin. If nothing exists for genital skin, take the nearest measured tissue and label it an assumption."
      ],
      get: ["Histology papers on the glans clitoris and prepuce that give measurements, not only descriptions."],
      verify: [
        "Each value has source, sample size, method and figure or table reference.",
        "Values with no source are listed as assumptions, each with a range, in `docs/scope.md` section 4."
      ],
      review: {
        who: "Clitoral and pelvic neuroanatomist",
        ask: "Are these depths, densities and layer thicknesses right, and what is missing?"
      },
      model: "Fable 5.2", effort: "high", why: "The skin model stands on these numbers and the literature is thin.",
      tools: ["Bio Research plugin (PubMed)", "research-superpowers (literature-review)", "reference-checking plugin", "pdf skill"],
      needs: [], blueprint: "3.1"
    },
    {
      id: "1.11", phase: "P1", kind: "find", who: "you+ai",
      title: "Electro-tactile modeling methods and human thresholds",
      what: [
        "Published models of surface electro-tactile stimulation: how skin, electrode interface and fiber endings were modeled.",
        "Human electro-tactile thresholds with full stimulus details: on the fingertip, and any on genital skin.",
        "Check two claims written from memory: surface electrodes mainly excite fibers in the skin; polarity changes which fiber orientations respond."
      ],
      get: ["A published method to follow.", "A threshold dataset complete enough to reproduce."],
      verify: [
        "Each method paper is summarized with its skin model, fiber model and how it was validated.",
        "At least one threshold dataset has every parameter needed to reproduce it; if none does, that is recorded as an amendment.",
        "Both claims are confirmed with a source, or corrected in the blueprint."
      ],
      review: {
        who: "Electro-tactile stimulation engineer",
        ask: "Which published model is the right starting point, and which threshold data are reliable?"
      },
      model: "Fable 5.2", effort: "high", why: "Choosing the method the whole skin model will follow.",
      tools: ["Bio Research plugin (PubMed)", "research-superpowers (literature-review)", "reference-checking plugin", "WebSearch"],
      needs: [], blueprint: "0, 3.1, 5.3"
    },
    {
      id: "1.12", phase: "P1", kind: "find", who: "you+ai",
      title: "Electrode interface values for each material and skin condition",
      what: [
        "For stainless steel, copper (PCB), silver, gold and titanium: how the metal-to-skin interface behaves under stimulation pulses, on moist skin and with gel.",
        "For dry, moist and gelled skin on glans-like, hood-like and fingertip skin: surface-layer conductivity and contact impedance.",
        "Write a short table of what each option changes in the model and what it does not."
      ],
      get: ["Measured interface values that state electrode area, the medium, and the frequency or pulse conditions."],
      verify: [
        "Each of the five materials and three skin conditions has values with sources, or is labelled an assumption with a range.",
        "The table in `docs/scope.md` section 5 is confirmed or corrected, and the '(verify)' tags there are resolved."
      ],
      review: {
        who: "Electro-tactile stimulation engineer",
        ask: "Are these interface values and their expected effects realistic, and is a resistive skin model enough for our pulse widths?"
      },
      model: "Fable 5.2", effort: "high", why: "Scattered, condition-dependent literature; easy to misapply a value.",
      tools: ["Bio Research plugin (PubMed)", "research-superpowers (literature-review)", "reference-checking plugin", "WebSearch"],
      needs: [], blueprint: "5.2, 5.3"
    },

    // ---------------------------------------------------------------- P2
    {
      id: "2.4", phase: "P2", kind: "do", who: "ai",
      title: "Electrode and stimulus configuration schema",
      what: [
        "Implement the parameter set from `docs/scope.md` section 5 as validated configuration files, including region (glans, hood, fingertip), material (five options), skin condition (three options) and the driver's voltage limit. Drive is current-controlled.",
        "Enforce the input limits from step 0.3.",
        "Add the test layouts from step 0.3 as examples."
      ],
      verify: [
        "Each example file loads.",
        "A value outside an input limit is rejected with the reason.",
        "Files with missing units, overlapping contacts, or currents that do not balance when no return contact is defined are rejected with a clear message.",
        "`pytest` covers each rejection."
      ],
      review: null,
      model: "Sonnet 5.5", effort: "medium", why: "Ordinary validation code.",
      tools: ["quick-gate-python plugin (not installed yet)"], needs: ["2.3", "0.3"], blueprint: "5.3"
    },
    {
      id: "2.1", phase: "P2", kind: "do", who: "you+ai",
      title: "Install WSL2, Ubuntu and conda",
      what: [
        "Install Ubuntu under WSL2 (needs administrator rights, so you may have to run it). WSL2 itself is present; no distribution is installed.",
        "Drive C has only 16 GB free: put the distribution on drive F (check the current `wsl --install` options for choosing a location, or export it and re-import it onto F).",
        "Install Miniforge inside Ubuntu."
      ],
      verify: ["`wsl -l -v` shows Ubuntu with VERSION 2.", "The distribution's disk file is on drive F.", "`conda --version` works inside Ubuntu."],
      review: null,
      model: "Sonnet 5.5", effort: "low", why: "Standard installation.",
      tools: ["PowerShell"], needs: ["0.5"], blueprint: "1"
    },
    {
      id: "2.2", phase: "P2", kind: "do", who: "ai",
      title: "Install NRV and run its first tutorial",
      what: ["Follow the install command on the NRV package page (it pins the dolfinx version).", "Run the first documented tutorial."],
      verify: [
        "`python -c \"import nrv; print(nrv.__version__)\"` prints a version.",
        "The tutorial produces a propagating action potential.",
        "Versions are written to `environment.yml`."
      ],
      review: null,
      model: "Sonnet 5.5", effort: "medium", why: "Dependency problems are likely; medium effort to diagnose them.",
      tools: [], needs: ["2.1", "1.9"], blueprint: "1, 3"
    },
    {
      id: "2.3", phase: "P2", kind: "do", who: "ai",
      title: "Scaffold the code repository",
      what: ["Add `environment.yml`, `sim/`, `axons/`, `tests/`, pytest and ruff configuration."],
      verify: ["`pytest` runs.", "A fresh clone plus `conda env create -f environment.yml` reproduces the environment."],
      review: null,
      model: "Sonnet 5.5", effort: "medium", why: "Routine scaffolding.",
      tools: ["quick-gate-python plugin (not installed yet)"], needs: ["2.2"], blueprint: "14"
    },

    // ---------------------------------------------------------------- P3
    {
      id: "3.1", phase: "P3", kind: "do", who: "ai",
      title: "Solver verification tests",
      what: [
        "Point source in a homogeneous medium against the analytic solution.",
        "Linearity: doubling current doubles the potential.",
        "Superposition: a two-contact solve equals the sum of the two single-contact solutions.",
        "Mesh convergence of thresholds."
      ],
      verify: [
        "`pytest tests/` passes.",
        "Superposition error is under 1%.",
        "Point-source error is under 2% away from the source (target is an assumption; record the achieved value).",
        "Thresholds change by under 3% on one refinement."
      ],
      review: null,
      model: "Opus 5.5", effort: "high", why: "Numerical correctness; mistakes here hide in every later result.",
      tools: ["code-review skill", "quick-gate-python plugin (not installed yet)"], needs: ["2.3"], blueprint: "10.1"
    },
    {
      id: "3.2", phase: "P3", kind: "do", who: "ai",
      title: "Check the axon models against their papers",
      what: ["Reproduce conduction velocity against diameter and a strength-duration curve for each fiber model used."],
      verify: ["Values fall within 10% of the published figures; differences are explained in the notes."],
      review: {
        who: "Computational neuroscientist",
        ask: "Are these the right fiber models for sensory and unmyelinated axons in this nerve, and is the small-diameter handling acceptable?"
      },
      model: "Opus 5.5", effort: "high", why: "Comparing simulation output with published curves.",
      tools: ["dataviz skill"], needs: ["2.2", "1.6"], blueprint: "6"
    },
    {
      id: "3.3", phase: "P3", kind: "do", who: "ai",
      title: "Build the fiber population files",
      what: [
        "For the skin model: `axons/terminals.csv` with position, depth, orientation, diameter, type and a label column (measured, literature, assumption).",
        "For the trunk model: `axons/population.csv` with position, diameter, type and label.",
        "Produce low and high variants of count and density."
      ],
      verify: ["Counts and myelinated fraction match the chosen inputs exactly.", "A diameter histogram is saved and matches the chosen distribution."],
      review: {
        who: "Neuroanatomist",
        ask: "Do the terminal fibers (depth, density, orientation, diameters) and the trunk population (count range, myelinated fraction, fascicle layout) look like this tissue?"
      },
      model: "Sonnet 5.5", effort: "medium", why: "Straightforward data generation.",
      tools: ["Data plugin (validate-data)", "dataviz skill"], needs: ["1.5", "1.10"], blueprint: "2, 3"
    },
    {
      id: "3.4", phase: "P3", kind: "do", who: "ai",
      title: "Build the idealized skin-surface model and electrode layouts",
      what: [
        "Layered tissue block with terminal fibers, as presets for glans, hood and fingertip, each in dry, moist and gelled condition.",
        "Electrode layouts loaded from configuration files, with an interface layer per contact set by the selected material.",
        "One stored unit-current field per contact.",
        "The voltage each contact needs, compared with the driver's limit.",
        "Afterwards, the secondary nerve-trunk case (nerve with fascicles and perineurium under the skin model)."
      ],
      verify: [
        "Changing the currents on the contacts does not trigger a new field solve.",
        "A setting that needs more voltage than the driver's limit is flagged, not silently simulated.",
        "The conductivity table printed by the code equals blueprint section 5.2.",
        "Current through a closed surface around the electrode equals the injected current within 1%.",
        "A mesh picture is saved."
      ],
      review: {
        who: "Electro-tactile stimulation engineer and computational neuroscientist",
        ask: "Is the skin and electrode-interface model adequate for these pulse widths, and is the treatment of fiber endings and of the perineurium sound?"
      },
      model: "Opus 5.5", effort: "high", why: "Geometry, materials and boundary conditions must all be right together.",
      tools: ["code-review skill"], needs: ["3.1", "0.3", "1.6", "1.10", "1.12", "2.4"], blueprint: "3.1, 3.2, 5"
    },
    {
      id: "3.5", phase: "P3", kind: "do", who: "ai",
      title: "Recruitment and strength-duration curves",
      what: [
        "Threshold search for every fiber across the reference layouts and waveforms; plot recruitment against current.",
        "Maps of which fibers fire, by position, depth, orientation and type."
      ],
      verify: [
        "Recruitment rises monotonically with current.",
        "Larger myelinated fibers have lower thresholds; thresholds rise with distance from the electrode.",
        "Strength-duration curves have the expected falling shape.",
        "A rerun with the same seed gives identical numbers."
      ],
      review: {
        who: "Computational neuroscientist",
        ask: "Do thresholds, recruitment order and chronaxie look physiologically reasonable?"
      },
      model: "Opus 5.5", effort: "high", why: "Long simulation code plus sanity reasoning.",
      tools: ["dataviz skill"], needs: ["3.2", "3.3", "3.4"], blueprint: "3"
    },
    {
      id: "3.6", phase: "P3", kind: "do", who: "ai",
      title: "Sensitivity analysis",
      what: ["Vary fiber count, diameter distribution, perineurium and skin conductivity, electrode position.", "Write `docs/results-m2.md`."],
      verify: ["Every headline output is reported as a range.", "Parameters are ranked by influence."],
      review: {
        who: "Computational neuroscientist",
        ask: "Are the parameter ranges fair, and are the conclusions supported by the spread?"
      },
      model: "Fable 5.2", effort: "high", why: "Interpreting what the spread means. Running the sweeps themselves needs only Opus 5.5 at medium.",
      tools: ["Data plugin (statistical-analysis)", "dataviz skill"], needs: ["3.5"], blueprint: "10.4"
    },
    {
      id: "3.7", phase: "P3", kind: "decide", who: "you",
      title: "Checkpoint: what should scan-derived geometry add?",
      what: [
        "The accuracy target is 'as accurate as open data allows', so Phase 4 goes ahead if the scan data can be obtained (step 1.4).",
        "Use the sensitivity results to decide what the scans must supply for a skin-surface model: region shape and curvature, branch paths to each region, trunk depth.",
        "Record the decision as an amendment."
      ],
      verify: ["The decision and its reason are in `docs/amendments.md`."],
      review: null,
      model: "Fable 5.2", effort: "medium", why: "A short, honest second opinion on the decision.",
      tools: [], needs: ["3.6", "3.9"], blueprint: "11"
    },
    {
      id: "3.8", phase: "P3", kind: "do", who: "ai",
      title: "Selectivity analysis across electrode layouts and waveforms",
      what: [
        "For each reference layout and waveform: how focused the activation is, how deep it reaches, the mix of fiber types and orientations recruited, and how these change with polarity, pulse width and contact size.",
        "Write `docs/results-selectivity.md`."
      ],
      verify: [
        "Each result is a range from the sensitivity analysis.",
        "Every statement about sensation is worded as a hypothesis for the hardware project to test."
      ],
      review: {
        who: "Electro-tactile stimulation engineer and somatosensory neuroscientist",
        ask: "Do these selectivity results agree with what electro-tactile experiments show, and which differences could plausibly be felt?"
      },
      model: "Fable 5.2", effort: "high", why: "Interpretation where overclaiming is easy.",
      tools: ["dataviz skill", "Data plugin (statistical-analysis)"], needs: ["3.6"], blueprint: "0, 3.1"
    },
    {
      id: "3.9", phase: "P3", kind: "do", who: "ai",
      title: "Validate the method on published human data",
      what: [
        "Rebuild the forearm experiment of Zhu 2017 with the same code: 9 mm disc with gel, biphasic cathodic-first pulses, forearm skin values from the literature. It is the most complete dataset found in step 1.11.",
        "Compare predicted thresholds with the measured ones, for absolute values and for trends with electrode size and pulse width.",
        "Repeat on the fingertip when a complete fingertip dataset is obtained (see `docs/literature-electrotactile.md` section 6)."
      ],
      verify: [
        "Predicted and measured thresholds sit in one table, with ranges.",
        "The difference is reported as it is. Parameters are not tuned to close it unless the tuning is declared."
      ],
      review: {
        who: "Computational neuroscientist",
        ask: "Is this a fair test of the method, and is the agreement good enough to transfer the method to other skin?"
      },
      model: "Opus 5.5", effort: "high", why: "A full model rebuild plus an honest comparison.",
      tools: ["dataviz skill", "code-review skill"], needs: ["3.5", "1.11"], blueprint: "3.1, 10.2"
    },

    // ---------------------------------------------------------------- P4
    {
      id: "4.1", phase: "P4", kind: "download", who: "you",
      title: "Download the lowest-resolution scan volume",
      what: ["Download through the route found in step 1.4 into `data/hoa/` (not committed)."],
      get: ["Whole-organ HiP-CT volume at the coarsest resolution, with its metadata."],
      verify: ["File sizes or checksums match the portal.", "It opens in Fiji as a virtual stack.", "Voxel size in the metadata matches the dataset page."],
      review: null,
      model: "Haiku 5.5", effort: "low", why: "Guidance only; the download is manual.",
      tools: [], needs: ["1.4", "3.7"], blueprint: "4"
    },
    {
      id: "4.2", phase: "P4", kind: "do", who: "you",
      title: "Segment nerve trunks and tissues",
      what: ["Manual work in 3D Slicer (or a trained ilastik classifier). The agent can guide and write helper scripts but cannot do the tracing."],
      verify: [
        "Trunk count and widest trunk diameter agree with the preprint.",
        "A second person segments a sub-volume; overlap (Dice) is 0.8 or higher (target is an assumption)."
      ],
      review: {
        who: "Neuroanatomist",
        ask: "Are these structures nerves, and is the branching traced correctly?"
      },
      model: "Sonnet 5.5", effort: "medium", why: "Guidance and small scripts.",
      tools: [], needs: ["4.1"], blueprint: "4"
    },
    {
      id: "4.3", phase: "P4", kind: "do", who: "ai",
      title: "Centerlines and shrinkage correction",
      what: ["Extract centerlines with radius.", "Choose a shrinkage factor from an in-vivo reference and record its source."],
      verify: ["Every centerline point lies inside its segment.", "The factor and its source are recorded as an assumption."],
      review: null,
      model: "Sonnet 5.5", effort: "medium", why: "Scripted geometry processing.",
      tools: [], needs: ["4.2", "1.8"], blueprint: "4"
    },
    {
      id: "4.4", phase: "P4", kind: "do", who: "ai",
      title: "Mesh from the label map",
      what: ["Generate the tetrahedral mesh directly from the segmentation."],
      verify: ["No inverted elements; quality statistics saved.", "Tissue volumes are within 5% of the segmentation.", "Visual check in ParaView."],
      review: null,
      model: "Opus 5.5", effort: "high", why: "Meshing failures are subtle and costly to debug.",
      tools: ["code-review skill"], needs: ["4.3"], blueprint: "5.1"
    },
    {
      id: "4.5", phase: "P4", kind: "do", who: "ai",
      title: "Realistic field model and recruitment",
      what: ["Rerun Phase 3 on the scan-derived mesh.", "Compare with the targets from step 1.7."],
      verify: ["The step 3.1 tests pass on the new mesh.", "Convergence is shown.", "Differences from clinical targets are stated and explained, not tuned away."],
      review: {
        who: "Computational neuroscientist and clinician",
        ask: "Is the comparison with clinical data fair, and what does the remaining gap mean?"
      },
      model: "Opus 5.5", effort: "high", why: "Code. Use Fable 5.2 at high for interpreting the comparison.",
      tools: ["dataviz skill", "Data plugin (statistical-analysis)"], needs: ["4.4", "1.7"], blueprint: "5, 10.2"
    },

    // ---------------------------------------------------------------- P5
    {
      id: "5.1", phase: "P5", kind: "do", who: "ai",
      title: "Contact mechanics",
      what: ["Elastic half-space model from indenter to stress at receptor depth."],
      verify: ["A sphere on a half-space matches the Hertz solution within 5%."],
      review: null,
      model: "Opus 5.5", effort: "high", why: "Numerical mechanics.",
      tools: ["code-review skill"], needs: ["0.2"], blueprint: "7"
    },
    {
      id: "5.2", phase: "P5", kind: "do", who: "ai",
      title: "Receptor filter model and reference firing patterns",
      what: [
        "Rapidly and slowly adapting filter models.",
        "A written rule that assigns each axon a skin location.",
        "Reference firing patterns for touch, tapping and vibration, to compare with the patterns electrical stimulation produces."
      ],
      verify: [
        "Rapidly adapting units fire on ramps and vibration and fall silent during a static hold; slowly adapting units keep firing.",
        "Every parameter is labelled an assumption in code and interface."
      ],
      review: {
        who: "Somatosensory neuroscientist",
        ask: "Are the receptor types, tuning and the receptive-field rule defensible as placeholders for genital skin?"
      },
      model: "Fable 5.2", effort: "high", why: "Design with no ground truth. The coding itself needs only Opus 5.5 at high.",
      tools: ["Bio Research plugin (PubMed)"], needs: ["5.1", "3.3"], blueprint: "7"
    },

    // ---------------------------------------------------------------- P6
    {
      id: "6.1", phase: "P6", kind: "do", who: "ai",
      title: "Streamlit interface",
      what: [
        "Inputs for every electrode and stimulus value, region, electrode material and skin condition, each bounded by its input limit.",
        "A Run button that starts a job, shows progress and an estimated time, and caches results by configuration.",
        "3D view and curves; labels and ranges always visible; the notes on anatomy, safety and what material does not change."
      ],
      verify: [
        "The app starts and shows no console errors.",
        "Changing only currents or waveform reuses the stored field; changing contacts, region or skin condition starts a new field solve.",
        "A value outside an input limit is refused and the reason is shown.",
        "A repeated run returns from the cache.",
        "Each displayed quantity shows its label.",
        "Someone who did not build it sets up a layout and produces a recruitment curve without help."
      ],
      review: null,
      model: "Opus 5.5", effort: "medium", why: "Job handling and caching on top of ordinary interface work.",
      tools: ["run skill", "dataviz skill", "built-in browser preview"], needs: ["3.6", "2.4"], blueprint: "9"
    },

    // ---------------------------------------------------------------- P7
    {
      id: "7.1", phase: "P7", kind: "review", who: "you+ai",
      title: "Full review before sharing or publishing",
      what: ["Code review, citation check, license check, and a referee-style read of the write-up."],
      verify: [
        "Every step above is complete, or closed by an amendment.",
        "`git ls-files` lists no scan data, segmentations or third-party meshes.",
        "Every dataset used is cited with its DOI."
      ],
      review: {
        who: "All reviewers",
        ask: "Each reviewer signs off the sections they reviewed, or lists what still blocks them."
      },
      model: "Fable 5.2", effort: "high", why: "Last chance to catch overclaims.",
      tools: ["code-review skill", "reference-checking plugin (referee review)", "research-superpowers (requesting-peer-review)"],
      needs: [], blueprint: "10, 13"
    },

    // ---------------------------------------------------------------- P8
    {
      id: "8.1", phase: "P8", kind: "do", who: "you+ai",
      title: "Define the format for bench and human data",
      what: [
        "Decide which measurements the hardware project will record so they can calibrate the simulator. From bench tests without people: electrode impedance per material and skin condition, delivered current and voltage. From the later finger tests: perception threshold per layout and waveform, reported sensation quality and location, comfort limit.",
        "Write the file format and an empty example into `calibration/`.",
        "Do this before the hardware project starts collecting data, so nothing has to be measured twice."
      ],
      verify: [
        "Every measurement names its electrode layout and waveform using the same configuration files as the simulator.",
        "Whoever leads the hardware project confirms the format is practical."
      ],
      review: {
        who: "Electro-tactile stimulation engineer",
        ask: "Is this the right set of measurements, and is anything essential missing?"
      },
      model: "Opus 5.5", effort: "medium", why: "Design of a small data format with long-term consequences.",
      tools: [], needs: ["2.4"], blueprint: "scope 7"
    },
    {
      id: "8.2", phase: "P8", kind: "do", who: "you",
      title: "Enter safety limits from the hardware project (later)",
      what: [
        "Order decided by the owner: bench safety tests first, with no people; then tests on fingers only, to recheck safety; the safety data is updated after each.",
        "When the hardware project has defined and tested its safety limits, enter them as constraints so the simulator flags settings outside them.",
        "Limits measured on fingers are entered for the fingertip preset only; they are not copied to the glans or hood.",
        "Until then the simulator reports charge per phase and charge density for information only."
      ],
      verify: [
        "Each limit cites the hardware project's test record.",
        "A setting outside a limit is flagged in the interface."
      ],
      review: {
        who: "Stimulation-safety engineer",
        ask: "Are the limits entered correctly and applied to the right quantities?"
      },
      model: "Sonnet 5.5", effort: "medium", why: "Small, careful change to existing code.",
      tools: ["code-review skill"], needs: ["8.1", "6.1"], blueprint: "scope 7"
    }
  ]
};
