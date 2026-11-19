# Statistics audit fixes, batch S2 of 3

Fixes #2, #7, #8, #9 and #20. Upload after S1 (and the three Calculus zips). Unzip at the repository root and commit;
no files are deleted.

## What changes

| # | Fix | Where |
|---|-----|-------|
| 2 | One AP-style free-response problem for every skill and level (123). Each has a context, four parts (a)–(d) that build on each other, at least one part that asks students to justify, explain or interpret, and scoring notes with points for each part and a total. Inference problems that carry out a procedure use the four steps (State, Plan, Do, Conclude). CP2 parts carry a short reminder of the method; Honors parts ask for one more step. The nine "Answer each part. Show your work." mixed-review items were replaced in place (same ids). | `tools/statistics-audit-20261118/s2frq.py`, `s2run.py`; the four Statistics banks |
| 7 | The practice test now grades Statistics keys made of labelled numbers and number lists ("Min = 15, Q1 = 25, …", "μ = 1.80, σ ≈ 1.208", "z ≈ 2.40, p-value ≈ 0.0082; reject H₀"). Labels are optional; a more precise value that rounds to the key is accepted; a value printed in the question may be left out. 894 of 1,183 short answers are now auto-graded. Every written answer that is still self-checked (289) has a 2–3 point self-check list, shown after the student submits. | `worksheet-generator/practice/stat-grading.js` (new), `grading.js`, `practice.js`, `practice.css`, `practice-test.html`; `s2polish.py` |
| 8 | 204 CP drills that started with a bare formula ("σ = 12 and n = 16. Find the SD of x̄.") now have a short context with the same numbers and answer (Partner Check pairs still match). 711 CP2 items have a "Hint" button with the first step. The new Honors items are multi-step, and the audit test checks that a complexity score rises from CP2 to CP1 to Honors in every unit. | `s2polish.py`, `practice.js` |
| 9 | Graphing Practice now covers Anticipating Patterns (shade a Normal area; mark a sampling distribution's center ± 2 SD) and Statistical Inference (graph a confidence interval; shade a p-value region; shade a rejection region), with exact checking, feedback, worked solutions and an answer-key graph. 16 new figures: experiment design diagrams (completely randomized, block, matched pairs) and shaded Normal curves for p-values. | `worksheet-generator/plot-statistics.js` (new), `plot-practice.js`, `plot-practice.html`, `core/plot.js` (decimal number-line labels), `data.js`; `s2diagrams.py`, `question-banks/assets/statistics/audit/` |
| 20 | Every skill-and-level set now has at least 24 items (before: 93 of 123 sets had fewer, the smallest 15). 478 new items from 64 item families, all in context, computed with scipy. The bank now has 3,143 items. | `s2fill.py`, `added-s2.json` |

`tools/statistics-audit-20261118/run_all.sh` rebuilds S1 and S2 together from the published banks, byte for byte, and
rerunning it changes nothing. The key checker (`verify_keys.py`) now also reads the new prompt shapes: 482 keys
recomputed from the printed prompts, 0 mismatches. `schemas/question-bank.schema.json` documents the new `hint` and
`selfCheck` fields.

New tests: `scripts/test-statistics-s2.cjs` (#2, #7, #8, #9, #20) and `scripts/test-statistics-plot.cjs` (1,800
generated graphing items graded by the real checker), both added to the Statistics CI job;
`scripts/test-statistics-bank.cjs` now requires 24 items per set.

## Tests run before packaging

All passed:

- `node scripts/test-statistics-s2.cjs`, `node scripts/test-statistics-plot.cjs`, `node scripts/test-statistics-bank.cjs` (3,143 items), `node scripts/test-statistics-audit.cjs`
- `python3 tools/statistics-audit-20261118/verify_keys.py`: 482 keys, 0 mismatches
- `verify_expansion.py`, honors-format and Partner Check companion checks, `test-partner-check-pairs.cjs`
- `test-published-question-banks.cjs`, `test-standards.cjs`, bank integration for Statistics (123 selections, 84 printables), `node --test tests/*.test.cjs` (82/82), practice and Calculus grading tests, Calculus graphing test
- Graphing Practice opened in a browser for both new units (desktop and phone width, no errors).
- Local replay of every workflow's `run:` steps: no new failures compared with `main`.
