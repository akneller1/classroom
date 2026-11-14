# 2026-11-14 — Pictures for text-described items and bank fixes (Classroom repo)

Part of the content follow-up to the 2026-11-14 site audit. Matching changes for Grades 2–5 are in the FinancialAlgebra repo (same date).

## Changed
- `question-banks/math6/ratios-rates-percent-proportions.json`: 15 hundred-grid items ("88 of the 100 squares on a grid are shaded…", family `s6_grid`) now show a 10 × 10 grid with exactly that many squares shaded. Pictures are in `question-banks/assets/math6/ratios-rates-percent-proportions/m6-rrp-s06-*.png`. Prompts, answers and checks are unchanged; each picture is drawn only from the number in its own prompt.
- `question-banks/calculus/applications-integrals.json`, `question-banks/calculus/ap-review.json`: 19 strings that printed `(-1 + e)` (computer-algebra ordering) now read `(e - 1)`, for example `4/(e - 1)`. The values are unchanged.

## How it was made
`/home/claude/work/visuals/add_visuals.py` (copy in the delivery ZIP under `tools/content-fixes-20261114/`).

## Checks
Rebuilt the production site with `scripts/build-site.mjs` and the integration steps from `deploy-site.yml`. These pass: test-grade2-release, test-grade1-release, test-elementary-generators, test-shared-course-catalogs, audit-grade5-release (0 defects), test-public-site and test-question-bank-loader.
