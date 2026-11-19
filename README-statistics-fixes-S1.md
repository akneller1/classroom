# Statistics audit fixes, batch S1 of 3

Fixes #1, #3, #6, #10, #11, #12, #13, #14, #18 and #19. Upload after the three Calculus zips (C1, C2, C3), because
some files are shared. Unzip at the repository root and commit; no files are deleted.

## What changes

| # | Fix | Where |
|---|-----|-------|
| 1 | Worked solutions: 645 numeric items whose solution was a single line now show the formula, the substitution and the result (no one-step numeric solutions remain). | `tools/statistics-audit-20261118/steps.py`; the four Statistics banks |
| 3 | Every item is tagged with a learning objective from the AP Statistics framework effective fall 2026 (127 objectives in use, codes like `APSTATS.3.7.A`). Topics the new course dropped (geometric distribution, combining random variables, linear transformations, chi-square goodness of fit, slope inference) are tagged `APSTATS.BEYOND.*` and their skills are renamed "Beyond AP: …". Course descriptions now say AP Statistics. | `ap2026.py`, `retag.py`, `std_js.py`; `worksheet-generator/menu/standards.js`, `standards-map.js`; `course-catalog.js`, `data.js`, `app.js`, `scripts/build-site.mjs` |
| 6 | 24 new items on sampling distributions of a difference (p̂₁ − p̂₂ and x̄₁ − x̄₂): center, spread, shape conditions and probabilities, 8 per level. | `new_items.py` |
| 10 | A key checker that reads each prompt and recomputes the answer with scipy (z-scores, Normal and binomial probabilities, critical values, intervals, test statistics, chi-square, regression, random variables). 189 keys checked, 0 mismatches. Runs in CI. | `verify_keys.py`, `.github/workflows/statistics-bank.yml` |
| 11 | 24 "choose the procedure" items (8 per level) mixing all inference procedures, filed under the procedure's skill. | `new_items.py` |
| 12 | Six items keyed from technology now say "Use technology (normalcdf)" and show the Table A value alongside. | `fix_text.py` |
| 13 | Notation: lowercase symbols at the start of prompts (σ, x̄, p̂, t*, …), "p-value" throughout, superscripts instead of ^, "Round to four decimal places" instead of "(4 dp)". | `fix_text.py` |
| 14 | 10 duplicate prompts within a skill reworded in new contexts (same answers, so Partner Check pairs still match). | `dedupe.py` |
| 18 | Course scope stated as AP Statistics (2026 framework) with Beyond AP topics marked. | as #3 |
| 19 | Confidence-interval simulation items explain the number of captures with the range chance usually gives, instead of a fixed sentence. | `fix_text.py` |

`tools/statistics-audit-20261118/run_all.sh` rebuilds the whole batch from the previous banks. New test:
`scripts/test-statistics-audit.cjs`; `scripts/test-statistics-bank.cjs` counts the 48 new items from `added.json`;
`tests/audit-gap-skills.test.cjs` follows the new skill names and codes.

## Tests run before packaging

All passed:

- `node scripts/test-statistics-bank.cjs` (2,551 items), `node scripts/test-statistics-audit.cjs`
- `python3 tools/statistics-audit-20261118/verify_keys.py`: 189 keys, 0 mismatches
- `python3 tools/statistics-expansion-20261107/verify_expansion.py`, honors-format and Partner Check checks, `test-partner-check-pairs.cjs`
- `test-published-question-banks.cjs`, `test-standards.cjs`, bank integration for Statistics (123 selections, 84 printables), `node --test tests/*.test.cjs` (82/82)
- `run_all.sh` reproduces this batch byte for byte and is idempotent.
- Local replay of every workflow's `run:` steps: no new failures compared with `main`.
