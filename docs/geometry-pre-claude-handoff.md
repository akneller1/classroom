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
