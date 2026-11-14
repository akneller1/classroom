# 2026-11-14: Course and title renames (Classroom repo)

Display names only. Course and unit **ids are unchanged**, so URLs, student links, saved work and bank paths keep working.

| Before | After | Why |
|---|---|---|
| Pre-Algebra (7th) | **Pre-Algebra** | The course is a full pre-algebra sequence: every Grade 7 standard plus most of Grade 8. It is the accelerated Grade 7 route into Algebra 1 in Grade 8. The new blurb says so. |
| Pre-Algebra (8th) | **8th Grade Math** | The course follows the Grade 8 standards one-to-one. The new name matches "6th Grade Math". |
| Precalculus Unit 7 "Vectors" | **Vectors, Complex Numbers & Polar Coordinates** | The unit also teaches complex-number operations, the complex plane and polar coordinates. |
| Basics & Reasoning Cheat Sheet | Foundations of Geometry Cheat Sheet | Matches the unit name. |
| Triangles & Congruence Cheat Sheet | Triangle Congruence Cheat Sheet | Matches the unit name. |
| Factoring and Zero Product Cheat Sheet | Factoring and Zero Product Property Cheat Sheet | Matches the unit name. |
| Quadratic Functions Cheat Sheet (Algebra 1) | Quadratic Functions and Equations Cheat Sheet | Matches the unit name. |
| Quadratics & Complex Numbers Cheat Sheet | Quadratic Functions & Complex Numbers Cheat Sheet | Matches the unit name. |
| Exponential & Log Functions Cheat Sheet | Exponential & Logarithmic Functions Cheat Sheet | Matches the unit name. |
| AP Review Cheat Sheet | AP Calculus Review Cheat Sheet | Matches the unit name. |

## Where the names changed
- Every text file outside `_site/`: `data.js`, `app.js` (home tile text), `assets/site-header.js`, `unit-specific-arcade.js`, `worksheet-generator/*`, `courses/*.html`, project pages, interactive tools, cheat-sheet content and the authoring tools.
- 21 cheat-sheet PDFs were rebuilt with `node scripts/cheat-sheets/build.cjs …`: 20 Pre-Algebra/8th Grade sheets plus `precalculus-vectors`. The build reported 208 example checks and 0 overflow problems.

## Not changed
- Project PDF, Word and PowerPoint files still print the old course name in their header. Rebuild them with `tools/course-projects-20261105` when convenient.
- No standard Grade 7 course exists yet. Pre-Algebra covers the Grade 7 standards for accelerated students; Grade 7 standards it was missing are being added as new skills.
