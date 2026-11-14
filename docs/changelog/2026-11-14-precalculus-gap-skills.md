# 2026-11-14: Precalculus gap skills and new Unit 9 (Classroom repo)

This update adds ten new skills with 480 questions. Each skill has 48 questions: 16 at each level (CP2, CP1, Honors), split into 7 short answer, 6 multiple choice, 2 error analysis and 1 four-part open response.

| Unit | New skill | Covers |
|---|---|---|
| 4 Trigonometric Functions | Fundamental Trigonometric Identities (skill 12) | finding all ratios from one ratio and a quadrant; simplifying with reciprocal, quotient and Pythagorean identities |
| 4 Trigonometric Functions | Double-Angle and Half-Angle Identities (skill 13) | sin 2θ, cos 2θ, tan 2θ, sin(θ/2) and cos(θ/2) from one ratio; rewriting with double-angle and power-reducing identities |
| 4 Trigonometric Functions | Solving Trigonometric Equations with Identities (skill 14) | every solution on [0, 2π), including quadratic-type equations, sin 2x and cos 2x, and multiple-angle equations |
| 7 Vectors, Complex Numbers & Polar Coordinates | Polar Equations and Graphs (skill 10) | polar to rectangular form; rose-curve petals; maximum r |
| 7 Vectors, Complex Numbers & Polar Coordinates | Parametric Equations (skill 11) | eliminating the parameter (lines, parabolas, circles, ellipses); position at a time t |
| **9 Sequences, Series, and Limits (new unit)** | Arithmetic and Geometric Sequences | nth terms |
| 9 | Finite Arithmetic and Geometric Series | Sₙ |
| 9 | Infinite Geometric Series | convergence and sums |
| 9 | Sigma Notation | evaluating Σ |
| 9 | Introduction to Limits | factoring, conjugates, sums and differences of cubes, complex fractions, limits at infinity, one-sided limits that disagree |

## New unit wiring
- `data.js`: the unit is added after Probability. Games, generators, Practice Test, Millionaire and printables appear automatically. The unit's cheat-sheet entry is added, and the course blurb is updated.
- `course-catalog.js`: the unit and its skills are added; new skills in existing units are appended, so all existing skill ids stay the same.
- `question-banks/manifest.json`: new bank `question-banks/precalculus/sequences-series-limits.json`, marked approved and teacherUse.
- New cheat sheet: `scripts/cheat-sheets/content/precalculus-sequences-series-limits.cjs` builds `artifacts/precalculus-sequences-series-limits-cheat-sheet/worksheet.pdf` and its thumbnail; `resource-details.js` lists it as 2 pages, reference sheet. The 19 example checks pass, with 0 overflow.
- Vocabulary: 12 terms in `worksheet-generator/vocabulary-data-middle-grades.js`, with the source in `tools/middle-grades-authoring/vocab_hs.py`.
- The Vectors cheat sheet is retitled "Vectors, Complex Numbers & Polar Coordinates Cheat Sheet" to match the renamed unit.
- `standards-map.js` is regenerated: 882 skills.
- Cache string `precalc-gap-20261114` is applied to data.js, resource-details.js, course-catalog.js, standards-map.js and the vocabulary data in 23 pages.

## Checks
- `tools/hs-gap-skills-20261114/verify.py` checked all 720 new Calculus and Precalculus questions: TOTAL ERRORS 0.
  - It recomputes every answer, option and student answer from the printed problem.
  - Trig-equation answers must list exactly the roots found by a dense numeric search.
  - Polar and parametric answers are checked at many points on the curve.
  - Series are checked from the printed terms.
- These also pass:
  - `MG_COURSE=precalculus test-hs-bank-integration`: 276 lesson plans, 27 game decks, 189 printables
  - the same test for Calculus
  - `test-published-question-banks`: 70 banks
  - `audit-question-banks`
  - `audit-course-catalog`
  - `test-standards`
- Spot-checked in Chrome: the Unit 9 page, flashcards, Showdown, Millionaire, Practice Test, Worksheet and the Lesson Planner (Unit 9 is days 120–128).
