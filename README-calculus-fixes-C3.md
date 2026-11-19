# Calculus audit fixes, batch C3 of 3

Fixes #5, #6, #15, #16 and #17. Upload after C1 and C2. Unzip at the repository root and commit; no files are deleted.

## What changes

| # | Fix | Where |
|---|-----|-------|
| 5 | Every skill and level now has an AP-style free-response problem (210 problems, 28 problem types matched to the skills): a context, table, graph or formula; four parts that build on each other; at least one "justify" or "explain" part; and scoring notes with points for each part. Graph-based problems have new images. | `tools/calculus-audit-20261118/frq.py`; images `question-banks/assets/calculus/*/cal-*-015.png` |
| 6 | Teaching notes for all 70 Calculus skills (objective, key idea, vocabulary, common mistake, explanation cards), loaded by the lesson planner. | `worksheet-generator/planner/notes-teach-calculus.js` (built by `build_notes.py` from `notes/`), `lesson-planner.html`, `notes-teach.js` |
| 15 | Graphing Practice for Calculus in 5 units: tangent lines, values of f′, relative extrema, points of inflection, accumulation functions, antiderivatives through a point, particular solutions of a DE, position from velocity. Exact checking, worked solutions and answer-key graphs. | `worksheet-generator/plot-calculus.js` (new), `plot-practice.js`, `plot-practice.html`, `data.js` |
| 16 | Two new labs: **Related Rates: Sliding Ladder** (Applications of Derivatives) and **Particle Motion: Position, Velocity and Distance** (Applications of Integrals, also listed in Applications of Derivatives), each with an Explore & Reflect worksheet, teacher key and card. | `artifacts/calculus-related-rates-lab/`, `artifacts/calculus-particle-motion-lab/`, `thumbs/`, `data.js`; sources in `tools/calculus-audit-20261118/labs/` |
| 17 | Two AP Calculus AB practice exams in AP Review: 30 no-calculator + 15 calculator multiple choice, 2 calculator + 4 no-calculator free response, timing notes, and a teacher key with worked solutions, scoring notes and a composite-score guide (marked as a practice estimate, not an official conversion). | `artifacts/calculus-ap-practice-exam-a/` and `-b/`, `thumbs/`, `data.js`; built by `exams.py` and `print_exams.cjs` |

New CI steps: free-response, graphing and exam checks in the Calculus bank workflow; lab checks in the Interactive Math
workflow; a browser test of the labs and Calculus Graphing Practice in the deploy workflow.

## Tests run before packaging

All passed:

- `node scripts/test-calculus-audit.cjs`: 210 free-response problems of 28 types, each with four parts, a justification and scoring notes
- `node scripts/test-calculus-plot.cjs`: 2,160 generated graphing items graded by the real grader (correct accepted, moved or swapped rejected)
- `node scripts/test-calculus-labs.cjs`, `python3 tools/calculus-audit-20261118/labs/tests/worksheet-answers.py`
- `node scripts/test-calculus-labs-browser.cjs .` (both labs: exact readouts, all 10 challenges reachable; Graphing Practice at phone width)
- `node scripts/test-calculus-exams.cjs` (keys match, four distinct options, no question in both exams)
- `node scripts/test-calculus-notes.cjs`: 70 skills
- `python3 tools/calculus-audit-20261118/verify_keys.py`, `node scripts/test-calculus-grading.cjs`, `node scripts/test-published-question-banks.cjs`,
  `node scripts/test-standards.cjs`, `node scripts/test-interactive-math-update.cjs`, bank integration (0 printable failures), `tests/reaudit-fixes.test.cjs`
- Rebuilding every bank from `main` with `run_all.sh` reproduces this batch byte for byte.
- Local replay of every workflow's `run:` steps compared with `main`: no new failures.
