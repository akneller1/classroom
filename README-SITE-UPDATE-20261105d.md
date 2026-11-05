# Site update d — November 5, 2026 (changed files only)

Install this after `site-update-20261105c.zip`. This zip holds only the files that changed or are new since then. Unzip it at the repository root; folder paths match the site.

## 1. A unit-specific game for every unit

There are 39 new Math Arcade games, so every unit of 6th Grade, Pre-Algebra 7 and 8, Precalculus and Calculus now has one. That's 44 bank games, counting the 5 from update c.

- **How they work.** Each game uses one of the six arcade engines (rocket, lava bridge, laser lock, portal gates, cannon, mirror maze) with questions from that unit's own question bank. It uses only multiple-choice questions with exactly one correct choice, so every answer is checked against the bank's key.
- **Levels.** Games run 6 levels, ramping from the lowest level to the highest. Middle-grade games use Remedial / Standard / Advanced.
- **Question images.** Graphs and diagrams now appear in the arcade; before, the arcade dropped them. This also fixes the 5 games from update c.
- **Where they're defined.** All 44 are in `unit-specific-arcade.js` (`MK_UNIT_GAMES`), which the unit pages and the arcade page both read. Each has its own thumbnail (`thumbs/arcade-<game>.svg`).

- **6th Grade Math** (7): Ratio Rocket Relay (Ratios, Rates, Percent and Proportions); Decimal Gate Dash (Operations with Fractions and Decimals); Number Line Lava Crossing (Rational Numbers); Equation Launch Pad (Expressions and Equations); Inequality Stepping Stones (Inequalities); Polygon Explorer (Geometry); Statistic Sharpshooter (Data Displays)
- **Pre-Algebra (7th)** (13): Integer Launch Control (Algebraic Expressions and Integers); One-Step Lava Hop (Solving One-Step Equations and Inequalities); Decimal Docking Mission (Decimals and Equations); Prime Factor Portals (Factors, Fractions, and Exponents); Fraction Fusion Lab (Operations with Fractions); Lava Bridge Builder (Solving Equations and Inequalities); Proportion Cannon (Ratios, Proportions, and Percentages); Slope Laser Lab (Linear Functions and Graphing); Symmetry Mirror Maze (Spatial Thinking); Cargo Capacity Launch (Area and Volume); Pythagoras Cannon (Right Triangles in Algebra); Probability Portals (Data Analysis and Probability); Growth Curve Lasers (Nonlinear Functions and Polynomials)
- **Pre-Algebra (8th)** (7): Exponent Escape Velocity (Real Numbers and Exponents); Equation Lava Path (Equations and Expressions); Function Rule Gates (Linear and Functional Relationships); Laser Lock: Systems (Systems of Linear Equations); Best-Fit Beam Lab (Patterns and Bivariate Data); Transformation Mirror Maze (Congruence and Similarity); Pythagorean Cannon (Geometry)
- **Precalculus** (8): Interval Lava Bridge (Equations and Inequalities); Function Gates (Functions); Conic Orbit Gates (Conics); Radian Cannon (Trigonometric Functions); Triangulation Lasers (Trigonometry of General Triangles); Matrix Mission Control (Matrices); Vector Navigator (Vectors); Odds Gates (Probability)
- **Calculus** (9): Function Review Gates (Precalculus Review); Limit Lava Bridge (Limits and Continuity); Tangent Line Cannon (Derivatives); Optimization Rocket (Applications of Derivatives); Riemann Laser Grid (Antiderivatives and Definite Integrals); Accumulation Gates (The Fundamental Theorem of Calculus); Displacement Explorer (Applications of Integrals); Growth and Decay Bridge (Differential Equations); AP Exam Launch (AP Calculus Review)

## 2. The four thin units are deeper

These units went from 16 to 24 questions per skill per level:

| Unit | Questions |
| --- | --- |
| 6th Grade Inequalities | 240 → 360 |
| Precalculus Conics | 288 → 432 |
| Calculus Precalculus Review | 240 → 358 |
| Calculus Fundamental Theorem | 240 → 360 |

- **How they were added.** A new "deepen" mode in `tools/middle-grades-authoring/gbuild.py` adds questions after the published ones. Every existing question is unchanged.
- **Checks.** The independent verifier passed every new question. It also caught two new multiple-choice items with two correct choices, which were dropped. That's why Precalculus Review has 358.

## 3. 32 older error-analysis questions replaced

The full-course check found 32 older error-analysis questions, 13 in 6th Grade and 19 in Pre-Algebra 7, where the "student's answer" was actually correct. For example: "80% of 100 seats are filled. Dev's answer: 80. Identify the mistake."

Each one was replaced by a new, verified error-analysis question for the same skill and level, using `MG_REPLACE` in `gbuild.py`. Every skill and level still has at least 2 error-analysis questions. All four bank courses now verify with 0 errors.

## 4. Lesson Planner tests for every course

- **New test.** `worksheet-generator/planner/tests/planner-courses-browser.cjs` covers Algebra 2, 6th Grade, Pre-Algebra 7 and 8, Precalculus and Calculus. That's 678 days × 3 views, about 12,300 problems.
- **What it checks:** the Course menu, every unit link, New problems and the PowerPoint download.
- **On GitHub.** It runs in the generator workflow as a new "planner" job, with the Algebra 1 and Geometry planner tests. Deploy checks are unchanged.

## 5. Old files retired

- **48 old game folders** in `artifacts/` (the earlier Jeopardy, Connect Four, Tic-Tac-Toe, Flashcards and Picture Reveal pages and similar) are now small "this game has moved" pages. Each forwards to the matching current game in the same unit, so old bookmarks still work.
- **8 old single-unit worksheet pages** (`worksheet-generator/algebra1-*.html`) and `artifacts/worksheet-generator/` forward to the Worksheet Generator for their unit.
- **Files to delete, in `cleanup-20261105d/DELETE-LIST.txt` (58 files):**
  - 54 thumbnails that no page or data file uses
  - the old generator script `worksheet-generator/core/app.js` and its two old tests
  - the image of one replaced question

  To delete them, run `bash cleanup-20261105d/delete-old-files.sh` on a local copy, or use the one-time workflow in that folder the same way as last time.

## 6. Small fixes

- **"a" and "an" in sentences** now print as ordinary words, not as italic variables (for example "cut by a transversal", "solve an equation"). Point and variable names keep their italics ("angle A", "let a represent").
- **Arcade:** the score chip matches the score on the game screen, and the gate and stage counters no longer read "7 of 6" at the end.
- **Capital X and Y in some Geometry circle problems are intentional.** In those problems x is the unknown the student solves for, so the coordinates use X and Y. Left as is.

## 7. Tests

- **Updated tests:** the arcade tests (all 51 games), Browse Activities (it reads every page of results), and the Assessment test (the retired page forwards).
- **Results:** all site tests, the menu, printables, planner, games and Geometry suites, and the math audit pass. The details are in section 8.

## 8. Test results

All of these were run on the finished update:

- **Site build and deploy check.** `node scripts/build-site.mjs` followed by `node scripts/test-public-site.cjs` passes.
- **`scripts/test-*.cjs`:** all 46 pass, including:
  - 51 arcade routes played in a browser
  - Browse Activities
  - course parity (491 scenarios)
  - the Algebra 2 integration and printable tests
  - the bank, loader and adapter tests (23,592 unique questions)
- **Generators:**
  - the Activity Generator engine (918 builds) and the printables browser test
  - Matching Card Sort (1,152 builds)
  - the Assessment/Worksheet browser test
- **Planner:**
  - Algebra 1 and Geometry plans and slides
  - the planner browser test
  - the new all-courses planner browser test (4,831 checks)
- **Other suites:**
  - the games (bank and browser), match game and cheat-sheet checks
  - all 18 Geometry suites, plus the MCAS and proof-layout tests
- **Math audit.** The audit reads the old Algebra 1 lesson banks from `worksheet-generator/units/algebra1/legacy-banks/`, since the old pages that held them now just forward. It passes: 207 skills.
- **Question-bank verifier.** `gverify.py` reports 0 errors for 6th Grade, Pre-Algebra 7, Precalculus and Calculus.
