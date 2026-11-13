# Expert reviewers: who to look for

Six roles. One person can cover two roles if they have both backgrounds. Record only role and initials in this repository; keep contact details elsewhere.

An AI opinion does not count as any of these reviews.

## How to use this file

1. For each role, search with the terms given and shortlist two or three people.
2. Check the "evidence they fit" line before writing to them.
3. Send the short request: what the project is, the one or two documents to read, the specific questions, and the time you are asking for.
4. Record the answer in the notes of the checklist steps listed, then tick "Expert review done".

## Priority

| Order | Role | Needed before |
|---|---|---|
| 1 | B. Electro-tactile stimulation engineer | Building the skin model (step 3.4) |
| 2 | C. Peripheral-nerve computational modeler | Trusting any recruitment result (steps 3.2, 3.5) |
| 3 | A. Clitoral and pelvic neuroanatomist | Fixing the fiber population (steps 1.5, 1.10, 3.3) |
| 4 | D. Somatosensory neuroscientist | Interpreting results as sensations (steps 3.8, 5.2) |
| 5 | E. Clinical neurophysiologist or sexual-medicine clinician | Validation against human data (steps 1.7, 4.5) |
| 6 | F. Stimulation-safety engineer | The hardware project; version 2 here |

## A. Clitoral and pelvic neuroanatomist

- **Expertise required:** human anatomy or histology of the clitoris and pudendal nerve; nerve fiber counting or nerve-ending histology of genital skin.
- **Evidence they fit:** has published dissection, histology or imaging of the dorsal nerve of the clitoris or of genital nerve endings.
- **Where to look:** the authors of the two anatomy papers this project rests on (Tunçkol et al. 2024; the 2026 HiP-CT preprint); anatomy departments; gender-affirming and vulvar reconstructive surgery groups that publish nerve anatomy.
- **Search terms:** "dorsal nerve of the clitoris" histology; "glans clitoris" corpuscles; "genital corpuscles" human; pudendal nerve morphometry.
- **Reviews steps:** 1.5, 1.10, 3.3, 4.2.
- **Questions:**
  1. Is the assumed fiber diameter distribution plausible for this nerve?
  2. At what depth do nerve endings lie in the glans and hood, how dense are they, and how are the fine branches oriented?
  3. How thick are the epithelium and the layers beneath it on each region?
  4. Do our segmented trunks and branches look right?
- **Time to ask for:** one hour to read and answer; a second hour later for the segmentation.

## B. Electro-tactile stimulation engineer

- **Expertise required:** electro-tactile or electrocutaneous displays; skin electrode design; electrode-to-skin impedance; how polarity, pulse width and electrode size change what is felt.
- **Evidence they fit:** has built and tested electro-tactile devices on people and published thresholds or sensation-quality results.
- **Where to look:** haptics research groups (IEEE World Haptics and IEEE Transactions on Haptics authors); sensory-feedback prosthetics groups; transcutaneous stimulation groups in biomedical engineering.
- **Search terms:** electrotactile display; electrocutaneous stimulation modeling; anodic cathodic electrotactile; electrode skin interface model; transcutaneous stimulation finite element.
- **Reviews steps:** 0.3, 1.11, 3.4, 3.8.
- **Questions:**
  1. Is our skin and electrode-interface model adequate for the pulse widths we plan?
  2. Are our parameter ranges (contact size, spacing, current, pulse width, rate) realistic for thin or moist skin?
  3. Which stimulus parameters are known to change sensation quality, and which of our outputs relate to them?
  4. What goes wrong in practice that a model like this misses?
  5. For stainless steel, copper, silver, gold and titanium contacts on dry, moist and gelled skin: which interface values should we use, and what really differs between them in use?
- **Time to ask for:** one hour, plus a short follow-up on first results.

## C. Peripheral-nerve computational modeler

- **Expertise required:** finite-element volume-conductor models coupled to cable models of axons in NEURON; threshold and recruitment analysis.
- **Evidence they fit:** has published a field-plus-axon model of peripheral or transcutaneous stimulation; ideally contributes to an open pipeline such as NRV or ASCENT.
- **Where to look:** developers and users of NRV and ASCENT; neural engineering departments; authors of transcutaneous or pudendal stimulation modeling papers.
- **Search terms:** peripheral nerve stimulation computational model; MRG axon finite element; transcutaneous electrical stimulation model NEURON; terminal excitation model.
- **Reviews steps:** 3.2, 3.4, 3.5, 3.6, 4.5.
- **Questions:**
  1. Are the fiber models right for small sensory and unmyelinated fibers, and for fiber endings?
  2. Is the treatment of fiber terminals and of the perineurium sound?
  3. Do thresholds, recruitment order and strength-duration behavior look reasonable?
  4. Is the sensitivity analysis fair?
- **Time to ask for:** two hours across two rounds.

## D. Somatosensory neuroscientist

- **Expertise required:** touch receptors and their afferent fibers; how firing patterns relate to felt qualities such as pressure, flutter, vibration and tapping; ideally genital sensation.
- **Evidence they fit:** has published recordings from touch afferents (microneurography or animal work) or psychophysics of touch.
- **Where to look:** somatosensory neuroscience laboratories; groups working on genital sensory receptors (Krause corpuscles); biomimetic sensory-feedback groups.
- **Search terms:** tactile afferent coding; microneurography touch; Krause corpuscle; biomimetic tactile stimulation; rapidly adapting slowly adapting afferent psychophysics.
- **Reviews steps:** 3.8, 5.2.
- **Questions:**
  1. Which fiber classes and firing patterns are associated with touch, tapping, vibration and pain?
  2. Which of these can selective electrical stimulation plausibly reach?
  3. Are our placeholder receptor assumptions for genital skin defensible?
- **Time to ask for:** one hour.

## E. Clinical neurophysiologist or sexual-medicine clinician

- **Expertise required:** pudendal and dorsal genital nerve testing: evoked potentials, reflex latencies, sensory threshold testing of genital skin, dorsal genital nerve stimulation.
- **Evidence they fit:** performs or has published these measurements in women.
- **Where to look:** pelvic floor neurophysiology units; urogynecology and neuro-urology departments; sexual medicine societies.
- **Search terms:** dorsal genital nerve stimulation threshold; pudendal somatosensory evoked potential women; clitoral sensory threshold; genital quantitative sensory testing.
- **Reviews steps:** 1.7, 4.5.
- **Questions:**
  1. Which published measurements are comparable to our modeled setup?
  2. What ranges are normal, and how much do they vary with age and hormonal status?
  3. What does a remaining gap between model and measurement most likely mean?
- **Time to ask for:** one hour.

## F. Stimulation-safety engineer (later)

- **Expertise required:** safety of electrical stimulation of skin and nerve: charge and current density limits, electrode corrosion, skin burns, medical electrical equipment standards.
- **Needed when:** the hardware project starts, and for version 2 of the simulator. Not required to build version 1.
- **One early question worth asking anyway:** what current and charge range is realistic to simulate, so version 1 is tested over the range the hardware will actually use.

## Not a reviewer, but needed later

The owner's plan is bench safety tests first, then tests on fingers only. Finger tests are still tests on people: they need informed consent and, depending on the country and institution, ethics approval. Find out early who grants it; it often takes longer than the engineering.
