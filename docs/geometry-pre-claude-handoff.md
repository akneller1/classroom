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

## Four priority units: source-level content audit (2026-10-28)
- Quadrilaterals/Polygons: five registered skills. The quadrilateral-angle generator had a fallback producing angle totals other than 360°. Replaced it with valid interior-angle sampling so all four angles are strictly between 0° and 180° and sum to 360°.
- Circles: seven skills. The central-angle-to-arc item used the tautology `2*x=2*x`, which could not independently verify the displayed central angle. Changed the question to label the unknown arc `x` and check `x=<given angle>`.
- Transformations: seven skills; all are single-coordinate numerical answers rather than complete ordered-pair or figure transformations. Needs diagram-rich, multistep items and composition.
- Area/Surface Area/Volume: nine skills; missing cones, spheres, composite solids, nets, cross-sections and scale-factor reasoning.
- All four files are text-first and do not attach per-question `fig` payloads. Visual coverage is a priority for Claude, particularly Quadrilaterals and Transformations.
- No claim of end-to-end Honors calibration or live visual verification. Run GitHub Actions after these correctness corrections before adding new skill families.

## Quadrilateral skills expansion (2026-10-28)
- Added three independently verified skills: rectangle diagonal congruence/bisection, rhombus diagonal bisection, and trapezoid midsegment theorem. Eight registered skills total in the unit (previously five).
- All three use numerical givens in student prompts, with verifier-side reconstruction of the corresponding equation; the equation is not exposed in the question prompt. No existing Geometry skill IDs were changed.
- These remain text-first; Claude handoff should prioritize diagrams, special-quadrilateral classification, and multistep Honors reasoning. CI status must be confirmed after this change.

## Text-only Quadrilateral and Polygon skills (2026-10-28)
- Added consecutive-angle relationships in parallelograms (supplementary angle reasoning) and diagonal counting in convex polygons (double-counting reasoning), increasing the unit to ten skills.
- The generators have 131 and at least 70 unique numerical prompts, respectively, exceeding the 25-card capacity requirement. Both use independent checks of the student-visible givens. No figures or drawings were created; all visual/diagram work is reserved for Claude.
- Next text-first opportunities: classification using verbal property descriptions and formal reasoning; all visual proof/diagram work remains in Claude's scope. CI needs confirmation on this commit.

## Text-only special-quadrilateral classification (2026-10-28)
- Added `classify-square-rhombus`: given a rectangle or parallelogram with two algebraic adjacent-side expressions, students solve the equality condition that makes it a square or rhombus and justify why that property is sufficient. For higher tiers both sides have variable expressions, increasing algebraic reasoning.
- The verifier independently reconstructs the equation from the two student-visible side expressions; no diagram or drawing is included. All visual classification examples remain assigned to Claude. The Quadrilaterals/Polygons menu bank now has 11 registered skills. CI requires confirmation on this commit.

## Algebraic Honors reasoning without diagrams (2026-10-28)
- Added `parallelogram-algebraic-consecutive-angles`, requiring students to solve an equation from two algebraic adjacent-angle expressions, justify why they are supplementary, and distinguish the adjacent-angle rule from the opposite-angle congruence rule.
- For higher complexity tiers both angle expressions have coefficients 2–3; all generated actual angles are positive and sum to 180°. The verifier independently reconstructs the equation from the two visible expressions. Quadrilaterals/Polygons now has 12 registered skills.
- No figures, drawings, or diagram-based proof items added. Claude remains responsible for those. Confirm CI after this commit.

## Text-only converse reasoning: parallelogram diagonals (2026-10-28)
- Added `parallelogram-diagonal-bisection-converse`: students use both diagonals bisecting each other as a **sufficient** condition for a parallelogram, solve an algebraic half-diagonal equation, and justify the converse theorem.
- The generator supplies BE and ED as matching positive lengths and constructs AE=EC with a positive integer x. The verifier independently checks **both** the displayed BE/ED equality and the algebraic AE/EC equation, preventing mutated printed givens from silently passing.
- Unit now has 13 registered skills. No diagrams/drawings were created; Claude owns visual diagrams, figures and visual proof activities. CI pending after this commit.

## Circles: text-only product-theorem expansion (2026-10-28)
- Added `circle-intersecting-chords` and `circle-two-secants`, raising Circles from seven to nine skills. Chords use PA·PB = PC·PD. Secants use external×whole products, distinguishing whole and external lengths. Generated answers are positive integers and whole secant lengths exceed external segments.
- The verifier reconstructs both equations from student-visible givens, and checks the second secant's whole/external inequality. No diagrams or drawings were made; Claude owns all circle figures and visual proofs. CI pending.

## Circles: tangent–secant theorem, text-only (2026-10-28)
- Added `circle-tangent-secant`, raising the Circles menu bank to 10 registered skills. A tangent of length t and a secant with external segment e and whole secant x satisfy e·x=t². Questions explicitly distinguish the whole secant from the internal segment.
- Constructed with e>0 and t=e·m for integer m≥2, giving x=e·m²>e. The verification equation remains linear in x, compatible with the existing independent linear solver. The verifier re-derives the equation from the visible tangent/external measurements.
- No diagrams or drawings created; Claude owns visual figures and proofs. CI pending for this commit.

## Circles: exact arc length and sector area (2026-10-28)
- Added `circle-arc-length-exact` and `circle-sector-area-exact` (12 registered Circles skills). Students determine the coefficient x of pi in exact arc length or sector area, with no decimal approximation.
- Central angles are proper minor-arc angles (30°, 36°, 40°, 45°, 60°, 72°, 90°, 120°, or 180°); radius is chosen to give positive integer coefficients. The verifier independently reconstructs each formula from the student-visible radius and central angle.
- No diagrams or drawings; Claude retains all figures and visual proofs. CI pending.

## Circles: coordinate equation parameter from center and point (2026-10-28)
- Added `circle-radius-squared-from-point` (13 registered Circles skills). Given a center (h,k) and a point on the circle, students compute the radius squared x in the standard circle equation (X-h)^2+(Y-k)^2=x. Includes negative coordinates, squared differences, and a justification based on distance.
- The verifier independently derives the absolute coordinate differences from the displayed center and point, then checks the equation for x. All results are positive integers; no graph or drawing was created. Claude retains all visual coordinate-plane tasks.
- Also note: the arc-length bank includes semicircle arcs of 180°, so the arc verifier should permit central angle 180° (currently it rejects this boundary). CI pending.

## Circles: chord length from perpendicular center distance (2026-10-28)
- Added `circle-chord-length-from-distance`, now 14 registered Circles skills. Given radius and perpendicular distance from the center to a chord, students use the Pythagorean theorem to calculate the half-chord and double it. Generated values come from integer Pythagorean triples, scaled to provide broad exact-answer variety.
- Independent verifier reads the printed radius and distance, requires radius > distance > 0, checks that sqrt(r²−d²) is a positive integer, and verifies the displayed answer equation x=2·half-chord. No diagrams/drawings were made; Claude owns visual representations and proofs. CI pending.

## Circles: expanded equations (2026-10-28)
- Added `circle-center-expanded-equation`, identifying the X-coordinate of the center by completing the square in the expanded circle equation X²−2hX+Y²−2kY+C=0. Students must explain why the linear coefficient determines h.
- Constructed using positive integer h,k and radius, with C=h²+k²−r². Independent verifier parses all displayed coefficients and the constant, ensures a positive perfect-square radius², and verifies 2x=2h. This adds a distinct algebraic reasoning format without drawings or diagrams.
- Circles now has 15 registered skills. CI pending for this commit; Claude retains all figures and visual circle-equation representations.
