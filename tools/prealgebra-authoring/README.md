# Grade 8 Pre-Algebra authoring tools (offline)

- `lib.py` formatting, problem record, seeded RNG, diagram drawing helpers
- `u1_*.py` … `u7_*.py` problem families per skill (Remedial/Standard/Advanced), select-all, open-response and error-analysis extras
- `build.py` materialises banks, tags, PNG diagrams and `out/<unit>.checks.json`
- `verify.py` + `mathtext.py` + `checks_custom.py` independent verification (does not import the families)
- `report.py` coverage and activity-compatibility CSVs
- `vm_catalog.py` reads exact skill IDs through the site's `MK_COURSE_CATALOG.getSkillRecords`

Environment: `PA8_REPO` (repository root, for data.js/course-catalog.js/math-display.js) and `PA8_OUT` (output root).
These scripts are an authoring aid only; the site uses the materialised JSON.
