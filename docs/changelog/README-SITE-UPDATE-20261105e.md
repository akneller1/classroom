# Site update e — November 5, 2026 (one Algebra 2 question)

Install this after `site-update-20261105d.zip`. It contains one file: `question-banks/algebra2/linear-functions-systems.json`.

## What changed

Question `a2-ls-s02-cp1-016` (Algebra 2, Linear Functions & Systems, slope skill, CP1) asked students to find the error in a slope calculation. The student's flipped ratio actually gave the correct slope, −1, and the answer said "right by coincidence."

The question now uses the points (2, 5) and (6, 3):

- The student's flipped ratio, (6 − 2) ÷ (3 − 5), gives −2.
- The correct slope, (3 − 5) ÷ (6 − 2), is −1/2.

The answer choices and worked steps were updated to match. No other question changed.

## The error-analysis check behind it

| Bank | Questions checked | Result |
| --- | --- | --- |
| Pre-Algebra 8 | 137 error-analysis questions, each worked by hand | All correct: every "student answer" is really wrong |
| Algebra 2, added Nov 5 | 522 error-analysis questions, independent verifier | 0 errors |
| Algebra 2, older | 80 items tagged error-analysis, each worked by hand | 79 correct; this one rewritten |

## Tests

These pass with the change:

- `test-published-question-banks`
- `test-algebra2-native`
- `test-algebra2-bank-approval`
- `check-algebra2-coverage`
- `test-algebra2-printable-sections`
- `test-question-bank-loader`
