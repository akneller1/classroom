# Geometry pre-Claude handoff — 2026-10-27

## Scope and verification
Source inspection covered all ten registered Geometry skill files in `worksheet-generator/menu/skills/`, plus the loader, curriculum test, capacity audit, and math regression harness. This is a source audit, **not** a browser/print visual audit. Do not equate 25 unique algebraically verified cards with adequate Geometry pedagogy.

Latest baseline before this audit: Menu assessment generator #367, Geometry flashcard QA #116, Algebra 1 smoke #220, and worksheet audit #628 passed (per GitHub Actions screenshots). **New commits after that baseline must pass CI again.**

## Objective corrections made
- `geometry-triangles-congruence.js`: triangle perimeter generation now satisfies strict triangle inequality; structured proof angle values are limited to valid interior-angle measures.
- `geometry-similarity.js`: SSS sides now satisfy strict triangle inequality; connected Honors parallel-segment problems now produce geometrically realizable triangles.
- `geometry-circles.js`: radius, diameter, and arc prompts no longer ambiguously reuse x for both a given and an unknown.
- `menu/tests/geometry-plausibility-tests.cjs`: new 1,600-case plausibility regression (100 seeds × four tiers × four families); invoked in Menu Assessment Generator CI.

## Prioritized content gaps (derived from actual skill-set gaps metadata)
| Priority | Unit | Existing registered skills | Recommended Claude work |
|---|---|---:|---|
| P0 | Quadrilaterals and Polygons | 5 | Rectangle/rhombus/square/trapezoid/kite properties, diagonals, classification, diagram questions and proofs |
| P0 | Circles | 7 | Chords, secants, intersecting chords, arc length, sectors, equations, annotated diagrams |
| P0 | Transformations | 7 | Full ordered-pair answers, graphing figures, composition, symmetry and rigid-motion proofs |
| P0 | Area, Surface Area and Volume | 9 | Cones, spheres, composite solids, nets, cross-sections, conversions and scale effects |
| P1 | Angles and Parallel Lines | 8 | Clearly labeled transversal diagrams and angle relationships inferred from the figure |
| P1 | Triangle Congruence | 11 | Full diagram-supported two-column/flow proofs and correspondence checking |
| P1 | Triangle Relationships | 11 | Triangle inequality variants, labeled diagrams and non-routine connected Honors investigations |
| P1 | Foundations of Geometry | 7 | Construction/measurement diagrams and geometric notation |
| P2 | Similarity | 10 | Coordinate dilations and formal proofs |
| P2 | Right Triangles and Trigonometry | 14 | Noninteger trigonometric applications and calculator-based multistep questions |

## Pre-Claude checklist
1. **Question quality** — source review of ten skill files completed; objective corrections made; full rendered-card review still needed.
2. **Algebra 1 / Geometry feature parity** — not yet verified end-to-end. Compare actual controls and persistence for flashcards, self-assessments, worksheet generator, menu assessments, lesson plans, vocabulary, PDF preview and student links. Do not assume parity from shared naming.
3. **Coverage** — 89 registered Geometry skills across ten units; gaps above require curriculum-level review.
4. **Difficulty calibration** — inspect actual question outputs at tiers 1–7; ensure CP2/CP1/Honors increases conceptual demand rather than just magnitude.
5. **UX/print** — needs browser and PDF inspection on desktop/mobile: answer-key lock code 205, print contrast, diagram labels, graph interaction, regeneration and copy-student-link.
6. **CI** — keep math regression, capacity audit, flashcard QA and plausibility checks. Do not relax verification to hide errors.

## Instructions for Claude
- Preserve existing skill IDs, unit IDs, tested infrastructure, and student-facing controls.
- Add skills and verified diagrams incrementally; avoid changing unrelated Algebra 1 files.
- For every new question family: prove the geometry is possible, answer matches figure, labels do not leak answers, and CP2/CP1/Honors variants are appropriate.
- Open Response must have at least four meaningful parts when that format is used.
- Keep all teacher answer keys behind code 205.
- Run existing tests and new geometry-plausibility checks; provide screenshots/PDF previews for diagram-heavy changes.
- Separate a question-bank's finite pedagogical variety from its mathematical correctness; do not force arbitrary 25-card uniqueness where mathematically inappropriate.
- Do not begin broad redesign until new CI run is green.

## Follow-up verification note
The four-family plausibility test was wired to the workflow and its generator API was checked against `menu/engine.js`. CI status could not be confirmed from the available GitHub connector (commit status endpoint returned no statuses and workflow-run lookup only exposes PR-triggered runs). Treat the new test as **unverified until a green GitHub Actions run is observed**. A direct repository clone was also unavailable in this environment due to DNS restrictions.

## Configuration parity follow-up (2026-10-27)
- Added `menu/tests/geometry-config-parity-tests.cjs` to compare all ten Geometry units against an Algebra 1 unit in the same shared assessment engine, for menu/test/worksheet configurations and CP2/CP1/Honors tier mapping (30 configuration comparisons, 90 level mappings).
- Wired parity checks into `.github/workflows/menu-generator-tests.yml`. **CI pass not yet confirmed**.
- Fixed an overescaped regular expression in the Honors triangle plausibility test; earlier version would have failed matching legitimate numeric givens.
- Updated `menu-assessment.html` cache-busting query parameters for corrected Congruence, Similarity and Circles skill scripts so deployed browsers fetch the latest source.
- This proves shared configuration code paths, **not** UI feature parity in separate flashcard, self-assessment, lesson-planner, or vocabulary applications; those remain pending.

## Student reasoning and difficulty calibration follow-up (2026-10-27)
- Inspected actual Triangle Congruence and Similarity student-facing prompt builders and found equation scaffolding that undermined reasoning, including four-part Honors proportionality investigations.
- Removed supplied worked equations from these prompts; left independently checked answers and full teacher solution steps intact. Students now establish equations, proportions, and segment relationships themselves.
- Added `menu/tests/geometry-reasoning-prompts-tests.cjs` (360 generated instances: four tiers × 30 seeds × three question families) and wired it into Menu Assessment Generator CI.
- Updated cache versions in `worksheet-generator/menu-assessment.html` so browsers receive revised question wording.
- **Outstanding:** confirm green CI, inspect other eight Geometry banks for over-scaffolding, review actual rendered diagrams and PDFs, and compare separate Geometry/Algebra 1 interfaces. These source changes do not establish complete CP2/CP1/Honors instructional calibration.

## Remaining eight question-bank reasoning pass (2026-10-27)
- Reviewed prompt builders in Foundations, Angles/Parallel Lines, Triangle Relationships, Quadrilaterals, Right Triangles/Trigonometry, Transformations, Circles, and Area/Surface Area/Volume.
- Removed explicit worked-equation scaffolding in student prompts where it substituted for setting up the geometric relationship; preserved teacher key equations and verifier metadata.
- Fixed a substantive Foundations angle-bisector defect: the question previously supplied no numeric angle givens in the student prompt. It now states the two adjacent angle measures explicitly.
- Added a regression assertion for the angle-bisector givens to the reasoning-prompt test (now 480 generated instances: four tiers × 30 seeds × four families).
- Refreshed browser cache query strings for all eight updated Geometry scripts in the Menu Assessment Generator.
- **Verification gate remains:** no confirmed green GitHub Actions result for the newest commits; do not claim the suite passed. A separate diagram and print preview inspection is still required.

## Green CI baseline and flashcard cache parity (2026-10-28)
- GitHub Actions commit `f4e70f3` passed all five workflows: Menu Assessment Generator, Geometry Flashcard QA, Algebra 1 smoke tests, Worksheet Math Bank Audit, and Pages deployment.
- Inspected all ten Geometry flashcard entrypoint HTML files. Each uses the same shared `games/games.js` and `games/bank.js` infrastructure as Algebra 1 flashcards, with shared level controls. This establishes shared code, not visual/browser parity of every generated skill.
- All ten Geometry flashcard pages previously referenced older cache keys for `menu/verify.js` and their respective `menu/skills/geometry-*.js`. Updated those script cache keys together to the green-tested `f4e70f3` version so browsers fetch the verified code.
- Remaining: inspect live desktop/mobile flashcard settings, all ten diagram renderings, PDF/print quality, and self-assessment/lesson-planner/vocabulary feature parity. CI for this cache-only change requires confirmation.
