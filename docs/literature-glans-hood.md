# Glans and hood: dimensions, skin layers and nerve endings (checklist step 1.10, first pass)

Searched 2026-11-14 in PubMed (several short queries on clitoris, glans, hood or prepuce, histology, nerve endings, dimensions, vulvar skin thickness, dorsal nerve) and in the OpenAlex search of the reference-lookup plugin. Read by me: PubMed abstracts and metadata for all papers below; full text only for the two papers marked "full text". Pages that blocked the fetch tool were retried once through Europe PMC (see section 6).

Labels: **measured** (a number from the source's own data), **literature** (a number the source quotes from elsewhere), **assumption** (no source).
Nothing here has been reviewed by an expert (step 1.10 review box stays unticked).

## 1. What was found, in one table

| Needed by the model | Found? | Value and label | Source |
|---|---|---|---|
| Glans length and width | Yes, as a pooled average over 21 studies | Length 6.40 mm, width 5.14 mm (measured, pooled; text p.6 and Table 1 overall row p.9, PDF pages; **verified from the PDF 2026-11-14**) | Longhurst 2024 |
| Spread of glans size | Yes | Ranges 1 to 21 mm (length) and 2 to 32 mm (width) across 2432 women (Table 1 overall row). The 32 mm width maximum is not matched by any single study range listed in the table (the widest listed is 11.6 mm), so it is probably an outlier or a typing error; use 2 to 12 mm as the working width range and say so. By method the mean glans length differs: MRI 9.34 mm, cadaver 7.27 mm, living-person measurement 5.38 mm, so the pooled 6.40 mm mixes methods. Length falls with age in one large series (7.5 mm at 35-44 to 5.2 mm at 75-84; Kreklau 2018, Table 1) | Longhurst 2024, Table 1 (PDF pages 7-9) |
| Hood (prepuce) size | Length only | Mean length 23.19 mm, range 5 to 40 mm (Table 1 overall row, PDF p.9; verified). Measured on living women in the vulvar-measurement studies (Agrawal 2021, Kreklau 2018, Cao 2015, Kaya 2020; Table 1), so it is the external hood length, not thickness. Width and thickness not found | Longhurst 2024 |
| Hood fold depth | One clinical inclusion value | At least 10 mm hood depth was required to enter a study (not a population measurement) | Grau 2026 (genital bar electrode study), Table 1 via Europe PMC |
| Thickness of epidermis and dermis on the glans or hood | **No** | Not found. No paper in the search measured it | none |
| Thickness of vulvar skin (proxy) | Poor | Epidermal cell layer (basal layer to stratum corneum base) 177 ± 80 µm in normal vulvar skin of 15 women after plastic surgery (measured; site on the vulva not stated in the abstract). In vulvar lichen sclerosus (disease, not normal) the full epidermis averaged 0.41 mm, against 0.13 mm in the same disease elsewhere | Fu 2021; Scurry 2001 |
| Nerve ending types in the glans | Yes, qualitative | Free nerve endings, genital end-bulbs, Meissner-like and Pacinian corpuscles; no Ruffini corpuscles. 6 glans from donors aged 52 to 83 | García-Mesa 2020 (full text) |
| Corpuscle density in the glans | Yes, with a unit problem (**confirmed in the PDF**) | 4.37 ± 0.7 "per mm2" (all sections); 5.22 ± 0.4 at ages 52 to 60; 4.16 ± 0.8 at 61 to 83; 13.9 ± 1.3 if each lobule counts as one corpuscle (p.4-5, section 3.2). Methods (p.4) count five fields of "400 µm2" per section and say "mean of sensory corpuscles by mm2". Four corpuscles per mm2 is far too few for a glans described as densely innervated, and 400 µm2 fields would give hundreds per mm2 for even one corpuscle, so the unit is unreliable. Authors say numbers are low and untested statistically. **Do not use as a density input; ask the authors or use another source** | García-Mesa 2020, PDF pages 4-5 |
| Depth of corpuscles below the surface | **No** (only qualitative zones: subepithelial, intermediate, deep; corpuscles get larger with depth; fibre network denser at the periphery than the centre; Pacinian corpuscles only in the central glans) (verified, p.4 and p.7) | none | García-Mesa 2020 |
| Corpuscle size, fibre diameter, papilla size | **No** | none | García-Mesa 2020 |
| Free (intra-epidermal) endings in the clitoris | Animal only | Fine intra-epithelial fibres are abundant in hairy skin but rare in non-hairy genital skin and in the clitoris of guinea pig and mouse. Large complex endings sit in dermal papillae | Vilimas 2011 |
| Nerve to the glans | Yes | Dorsal nerve of the clitoris: about 2917 axons in the crus and 3137 in the hemi-body, 71 to 76 % myelinated (measured, body donors; number of donors not in the abstract); about one third of the axons of the penis, about 6 times the density per area | Tunçkol 2024 |
| Dorsal nerve thickness | **Sources disagree** | 2.0 to 3.2 mm diameter (10 fresh cadavers, abstract) versus 0.2 to 0.7 mm (quoted in a 2026 review from a later source). A factor of ten. Not resolved | Kelling 2020; review PMC13682733 |
| Where the dorsal nerve ends | Yes | Traced to within 6 mm of the glans in 9 of 10 specimens; clitoral body 37.0 mm long, lying under the hood and mons | Kelling 2020 |
| Innervation of the glans and hood | Yes, qualitative | Four branching types; innervation is not left-right symmetric; **a nerve-free area lies ventral to the glans** (9 specimens, 64 to 90 years) | Wolf-Vollenbröker 2026 |
| Conductivity of genital skin | **No** | Not searched in this pass. Nearest tissue and label: step 1.6 and 1.12 | none |
| Electrode and current used on the genital region in women | One device | Genital bar electrode through the clitoral hood (2.0 mm diameter, 25 mm long, titanium), 200 µs, 20 Hz, 0 to 25 mA, set below the pain threshold. 14 women; no sensory thresholds reported. A pierced electrode, not a surface one | Grau 2026 via Europe PMC |
| Clitoral sensory threshold, earlier result | Already known | 3.64 ± 1.01 mA left, 3.84 ± 1.53 mA right, 38 women; electrode type not stated | Cavalcanti 2007 (see `literature-electrotactile.md`) |

## 2. What this changes

1. **The provisional glans size can now be replaced.** The pooled mean is 6.40 x 5.14 mm, not 4 x 6 mm (`docs/scope.md` section 5). Because the spread is wide, the glans preset should carry the mean as its default and a measured spread as the user-editable limits. See A-009.
2. **The hood has a length but no width or thickness.** 23.19 mm long (pooled mean), so the provisional 10 x 15 mm was too short. Width is an assumption until a source is found.
3. **The three numbers the skin model stands on are still missing for the glans and hood:** layer thickness, depth of nerve endings, conductivity. They stay assumptions with wide ranges, and the model's first runs must treat them as parameters to sweep, not facts.
4. **A possible modelling trap:** in the animal data the clitoris has few free intra-epithelial endings and many large corpuscles in the dermal papillae. Models of fingertip electro-tactile stimulation assume terminal fibres in the epidermis and upper dermis. Whether the glans behaves like the fingertip is not known (human glans free-ending data were not found). Do not carry the fingertip result to the glans without that check.
5. **The nerve-free area ventral to the glans** (Wolf-Vollenbröker 2026) means the geometry may need an innervation map, not a uniform density. Only one small study; to be confirmed.

## 3. What the owner may not have specified (rule 2)

- **Which clitoral hood skin state to model.** The hood is a fold. Is the electrode on its outer (dry, skin-like) face, its inner (moist, mucosa-like) face, or both? The conductivity and thickness differ. Scope table says "hood dry"; confirm.
- **Whether the glans is covered or exposed during stimulation.** The hood retracts differently between people and with arousal. This changes which tissue the electrode touches.
- **Age and arousal.** All the histology is from donors aged 52 to 90, and blood filling changes thickness and conductivity. The scope already accepts one elderly-donor anatomy; arousal state is a separate unaddressed variable, and the engorgement slider (blueprint section 8) has no data behind it.
- **Hormonal status** (menopause, contraception) changes epithelial thickness and moisture; no source found.

## 4. Gaps still open for step 1.10 (updated 2026-11-14 after reading both PDFs)

- Thickness of epidermis, dermis and stratum corneum on the glans and hood.
- Depth and density of nerve endings per area. García-Mesa 2020 was read: no depths, and the density unit is unreliable. New leads, not yet fetched: Jackson 2019, Am J Obstet Gynecol 221:519.e1 ("Anatomy, histology, and nerve density of clitoris and associated structures", cadavers, in the Longhurst table); Shih 2013, J Sex Med 10:1783 (corpuscular receptors of the glans clitoris, compared with glans penis).
- Conductivity of genital skin (thin, moist) and its nearest measured proxy.
- Hood width and thickness.
- Resolution of the dorsal nerve diameter disagreement.

## 5. Verification record (rule 4)

| Check | Result |
|---|---|
| Every value has source, sample size, method, table or figure reference | **Partly met.** Size values and corpuscle types are now checked against the two PDFs with page references. Still unchecked: Grau 2026, Vilimas 2011, Wolf-Vollenbröker 2026, Fu 2021 (abstracts only) and the dorsal nerve diameter conflict |
| Values with no source listed as assumptions with a range in `docs/scope.md` | Done in A-009 (scope.md section 4 and the region table) |
| Region table carries measured dimensions with sources | Glans: done (pooled mean). Hood: length only |

Step 1.10 therefore stays **doing**, not done.

## 6. How the papers were read (to make the next pass cheaper)

- PubMed search ANDs every word, so queries longer than three or four terms return nothing. Two or three terms work.
- PubMed full-text tool returned an empty body for PMC7812125; the PubMed Central web page answered once with the summarising fetch tool and then showed a browser-check page for the next two papers. The same two papers were readable once through `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`. Use Europe PMC first.
- The summarising fetch tool is a small model. It dropped or merged numbers (for example a unit mismatch it reported itself). Anything that goes into the model must be re-read from the PDF page. Ask the owner to download García-Mesa 2020 (J Anat 238:446, open access via PMC7812125) into `downloaded-manually/` and Longhurst 2024 (Clin Anat 37:233, DOI 10.1002/ca.24113) if the ranges are needed.

## 7. Sources

- Longhurst GJ, Beni R, Jeong SR, Pianta M, Soper AL, Leitch P, De Witte G, Fisher L. Beyond the tip of the iceberg: a meta-analysis of the anatomy of the clitoris. Clin Anat 2024;37(2):233-252 (PubMed lists 2023-09-29 online). doi:10.1002/ca.24113. PMID 37775965. Abstract read.
- García-Mesa Y, Cárcaba L, Coronado C, Cobo R, Martín-Cruces J, García-Piqueras J, Feito J, García-Suárez O, Vega JA. Glans clitoris innervation: PIEZO2 and sexual mechanosensitivity. J Anat 2020;238(2):446-454. doi:10.1111/joa.13317. PMID 32996126, PMC7812125. Abstract read; full text read through a summarising tool.
- Tunçkol E, Heim C, Brunk I, Vida I, Brecht M. Innervation pattern and fiber counts of the human dorsal nerve of clitoris. Sci Rep 2024;14:23060. doi:10.1038/s41598-024-72898-8. PMID 39367034. Abstract read (already in the repo's data sources).
- Kelling JA, Erickson CR, Pin J, Pin PG. Anatomical dissection of the dorsal nerve of the clitoris. Aesthet Surg J 2020;40(5):541-547. doi:10.1093/asj/sjz330. PMID 31768527. Abstract read; citation confirmed in OpenAlex (listed there as 2019).
- Wolf-Vollenbröker M, Piermaier L, Filler TJ, O'Dey DM. Ramification of the dorsal clitoral nerve along its course on the human clitoris. Folia Morphol 2026;85:e01726046. doi:10.5603/fm.107254. PMID 41930831. Abstract read.
- Vilimas PI, Yuan SY, Haberberger RV, Gibbins IL. Sensory innervation of the external genital tract of female guinea pigs and mice. J Sex Med 2011;8(7):1985-95. doi:10.1111/j.1743-6109.2011.02258.x. PMID 21477025. Abstract read. Animal data.
- Grau LS, Christensen P, El Issaoui M, Klarskov N, Ellebæk MB, Qvist N, Graugaard-Jensen C, Glavind-Kristensen M, Duelund-Jakobsen J. Genital bar electrode for dorsal genital nerve stimulation. Tech Coloproctol 2026. doi:10.1007/s10151-026-03386-6. PMC13630791. Read through Europe PMC with a summarising tool (unverified numbers).
- Fu Y, Bao Y, Li Z, Gao X, Chang J. Study of melanocyte density and epidermal thickness in vulvar lichen sclerosus lesions. Int J Dermatol 2021;60(8):991-995. doi:10.1111/ijd.15555. PMID 33870483. Abstract read. Control skin from plastic surgery.
- Scurry J, Whitehead J, Healey M. Histology of lichen sclerosus varies according to site and proximity to carcinoma. Am J Dermatopathol 2001;23(5):413-8. doi:10.1097/00000372-200110000-00005. PMID 11801773. Abstract read. Diseased skin.
- Migda MS et al. High-frequency ultrasonography of the vulva, vagina and cervix. J Ultrason 2019;19(79):261-268. doi:10.15557/JoU.2019.0039. PMC6988569. Layers seen in labia and mons; **no thickness values given, and the clitoris was not measured** (Europe PMC text).
- Review of clitoral anatomy for aesthetic, reconstructive and transgender surgery. Int Braz J Urol 2026. doi:10.1590/S1677-5538.IBJU.2026.9910. PMC13682733. Used only to find the Longhurst ranges and the 0.2 to 0.7 mm nerve diameter; both are second-hand.
- Cavalcanti GA et al. 2007. doi:10.1590/s1677-55382007000600010. Already in `literature-electrotactile.md`.

## 8. Third pass, 2026-11-14: density leads and conductivity proxy (abstracts only)

| Item | Result | Source |
|---|---|---|
| Glans size, cadavers | 8 mm long (5-12), 4 mm wide (3-10), median, 27 cadavers aged 48-96 (22 gross, 5 histology) | Jackson 2019 abstract |
| Erectile tissue | Absent in the glans and labia minora; present in body, crura, bulbs | Jackson 2019 abstract |
| Dorsal nerve width | 3 mm (2-4) at the crura, 1 mm (1-2) at the distal body. With Kelling 2020 (2.0-3.2 mm) this makes the 0.2-0.7 mm figure the odd one out; treat the nerve as about 1 to 3 mm wide and the 0.2-0.7 mm figure as unreliable | Jackson 2019; Kelling 2020 |
| Nerve density, glans | Measured, but the abstract gives no numbers (only: denser on the dorsal than ventral half of the body; not significantly denser at the distal labia minora). **Full text needed** | Jackson 2019 |
| Corpuscles per field, glans | 1 to 14 per 100x high-power field (5 vulvectomy specimens; glans penis 1 to 3). Corpuscles lay in the subepithelial tissue. **Field area not in the abstract, so this cannot become a density yet** | Shih 2013 abstract |
| Pacinian corpuscles in the glans | **Sources disagree.** Shih 2013: none in the glans, only along the dorsal nerve trunk. García-Mesa 2020: present in the central glans. Unresolved | Shih 2013; García-Mesa 2020 p.5 |
| Conductivity of genital or mucosal tissue | **Not found.** PubMed returned only MHz-range colorectal cancer studies, which do not apply to low-frequency pulses. The IT'IS tissue database page that holds low-frequency values (based on Gabriel 1996) did not display its table to the fetch tool, and itself warns that its skin values "should be used with caution" | IT'IS page; Gabriel 1996 |

Effect: the glans is 4 to 8 mm long and 4 to 5 mm wide in the cadaver studies (Jackson 2019; Longhurst 2024 overall), so the 6.4 x 5.1 mm default stands. Because Jackson 2019 gives 8 x 4 mm for cadavers, the preset sizes remain editable inputs.

Two attempts were made at the conductivity proxy (PubMed searches; IT'IS page). Stopped, per rule 1. Options for the owner: (a) download the IT'IS Tissue Properties Database spreadsheet (itis.swiss, Downloads) into `downloaded-manually/`; (b) accept "wet skin" and "mucous membrane" values from Gabriel 1996 as an assumption with a wide range and sweep it; (c) drop it and sweep a plausible range (state the range) in the first runs.

Sources added: Jackson LA, Hare AM, Carrick KS, Ramirez DMO, Hamner JJ, Corton MM. Anatomy, histology, and nerve density of clitoris and associated structures: clinical applications to vulvar surgery. Am J Obstet Gynecol 2019;221(5):519.e1-519.e9. doi:10.1016/j.ajog.2019.06.048. PMID 31254525. Shih C, Cold CJ, Yang CC. Cutaneous corpuscular receptors of the human glans clitoris: descriptive characteristics and comparison with the glans penis. J Sex Med 2013;10(7):1783-9. doi:10.1111/jsm.12191. PMID 23692408. Both abstracts read only.
## 9. Conductivity proxy found, 2026-11-14 (IT'IS Tissue Properties Database V5.0, file supplied by the owner)

Read from `Thermal_dielectric_acoustic_MR properties_database_V5.0(ASCII).txt`, column "LF Conductivity [S/m]" (average, SD, sample size, min, max). The file is in `downloaded-manually/Database-V5-0.zip`; not tracked by git. The database says its values come from the Gabriel dispersion relations plus literature, and its own website warns that skin values should be used with caution. Primary sources not traced (the zip holds `References_Low_Frequency_V5.0.pdf`).

| Tissue entry | Mean | SD | Sample size | Min | Max |
|---|---|---|---|---|---|
| Skin | 0.148 | 0.042 | 7 | 0.057 | 0.25 |
| Vagina | 0.164 | 0.054 | 1 | 0.164 | 0.164 |
| Mucous Membrane | 0.461 | 0.244 | 24 | 0.1 | 0.726 |
| Connective Tissue | 0.079 | 0.023 | 14 | | |
| Fat | 0.078 | 0.093 | 91 | 0.024 | 0.215 |
| Nerve | 0.348 | 0.194 | 194 | 0.064 | 0.852 |
| Penis | 0.232 | 0.014 | 1 | | |

Cautions found while reading:
- **"Mucous Membrane", "Muscle" and "Tongue" carry identical numbers** (0.461, SD 0.244, n 24). The mucous membrane entry looks copied from muscle, so it is not independent evidence for genital mucosa. Do not use 0.461 as the default.
- **"Penis" has the same values as "Blood Vessel Wall"** (0.232, SD 0.0136, n 1): also a copy. No tissue in the database is measured genital skin.
- "Vagina" is a single value.
- All entries are bulk values. The skin entry does not separate stratum corneum, epidermis and dermis; the layer split still comes from the skin papers in `literature-electrotactile.md` section 3 (stratum corneum differs tenfold).

Effect: there is still no measured conductivity for the glans or hood. The proxies above are labelled assumptions with ranges in `docs/scope.md` section 4; the first runs sweep them.
Update (owner's screenshot of the IT'IS web table, `downloaded-manually/simplesnap-11-14-2026_at_00-37-29.png`, matches the zip): the table's own note says skin conductivity "significantly impacts the dosimetric assessment at low frequencies" and its values "should be used with caution". Checking the zip showed **"Vagina" (0.1635 S/m, SD 0.0536, n 1) is identical to Large Intestine, Small Intestine, Stomach and Esophagus**, so it is a copied value, not a vagina measurement. This replaces the use of "Vagina" as a glans proxy above. The only independent-looking entry that remains is "Skin" (0.148 S/m, 7 values, 0.057 to 0.25). The glans and hood inner face therefore have **no proxy**; scope.md section 4 now says so.