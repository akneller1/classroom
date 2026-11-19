# Calculus audit fixes, batch C2 of 3

Fixes #2, #3, #4, #9 and #10. Upload after C1 (it builds on C1's files). Unzip at the repository root and commit; no files
are deleted.

## What changes

| # | Fix | Where |
|---|-----|-------|
| 2 | Practice tests now auto-grade 1,857 of 1,963 Calculus short answers (was 1,361). A new grader checks expressions by sampling, accepts any antiderivative that differs by a constant (+ C), equivalent general and implicit solutions, and answers with units. Wrong options and the find-the-mistake answers are rejected. | `worksheet-generator/practice/calculus-grading.js` (new), `grading.js`, `practice.js`, `practice-test.html`; test `scripts/test-calculus-grading.cjs` |
| 3 | Worked solutions show the work: antiderivative, F(b), F(a) and the subtraction; each piece of a total distance; rule-by-rule derivatives and limits. Every rebuilt chain is recomputed and must end at the key; no solution has a single step. | `expand_steps.py` |
| 4 | ∫ from a to b, lim (x → a), Σ (k = 1 to n) and d/dx now print with the bounds above and below the symbol, wherever bank text is shown. **Correction to the audit:** ordinary a/b fractions in bank text were already stacked by math-display.js; this batch adds the big operators and removes extra parentheses in stacked numerators and denominators. | `worksheet-generator/core/math-display.js`, `math-display.css` |
| 9 | Honors items in 13 families use trig, exponential, log and composite functions (122 items); CP2 items carry a first-step hint (156 items). | `level_up.py` |
| 10 | Missing AP topics added: local linear approximation, implicit second derivatives, calculator-active definite integrals (tagged `calculator-active`), motion read from a velocity graph (new graph images), washers about lines other than an axis, exponential models dy/dt = ky. New items never repeat a prompt at two levels. | `add_topics.py`; images in `question-banks/assets/calculus/applications-integrals/` |

`tools/calculus-audit-20261118/run_all.sh` rebuilds every bank change from `main` in order; running it again changes nothing.

## Tests run before packaging

All passed:

- `node scripts/test-calculus-audit.cjs` (C1 and C2 checks)
- `node scripts/test-calculus-grading.cjs`: 1,857 of 1,963 auto-graded; every key grades itself correct; other courses' keys unchanged
- `python3 tools/calculus-audit-20261118/verify_keys.py`: 1,508 keys recomputed, 0 mismatches
- `node scripts/test-published-question-banks.cjs`, `node scripts/test-standards.cjs`, `node scripts/test-precalculus-audit.cjs`
- `MG_COURSE=calculus MG_PREFIX=cal- node scripts/test-hs-bank-integration.cjs`: 0 printable failures
- `node --test tests/reaudit-fixes.test.cjs`
- Local replay of every workflow's `run:` steps compared with `main`: no new failures.
