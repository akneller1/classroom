# Site update 2026-11-11 · Coverage gaps closed (Algebra 1 and Geometry)

Every new skill follows the existing architecture: it is generated answer-first in its unit's skill file, and
`menu/verify.js` re-derives the answer independently from what is printed. A problem that fails verification is never
shown. Each skill is listed under its class → unit, can be found in topic search, and is available to the
Assessment Generator, printables, games and the lesson planner through the shared registry.

## Skills added or repaired

**Algebra 1**
- Unit 1 · Foundations: `properties`. Students identify a property, tell two look-alike properties apart, rewrite an expression with a named property, find the error in a claim, justify all four steps of a simplification, and test subtraction or division for a property. The verifier reads the property from the structure of the equation and accepts only equations that show exactly one property. `real-number-operations` (planner U1-L4). `interpret-expression` (U1-L7).
- Unit 5 · Linear Functions: `direct-variation`.
- Unit 11 · Quadratics: `table-model-type`: linear, quadratic or exponential from differences and ratios (U11-L12).
- Planner U4-L7: the "no generator yet" note was stale because `discrete-continuous` already exists. The lesson is now mapped to it.

**Geometry**
- Unit 2: `angle-pairs-figure` (numbered diagram) and `parallel-lines-converse` (planner U2-L6).
- Unit 3: `congruence-rigid-motions`. Unit 8: `transformation-sequence-congruence`, which includes glide reflections. Both use the shared `K.rigidSequence`.
- Unit 4: `triangle-concurrency-name` and `triangle-circumcenter-incenter`.
- Unit 5: `similarity-area-volume-ratio` and `similarity-area-investigation` (four parts).
- Unit 6: `law-of-sines` and `law-of-cosines`, drawn with the new `geo-oblique` triangle figure.
- Unit 7: `kite-isosceles-trapezoid`, drawn with the existing `geo-quad` figures.
- Unit 10: `measure-pyramid-surface`, `measure-cone-surface`, `measure-composite-round`, `measure-unit-conversion` and `measure-similar-solids`.
- Unit 8: three existing skills were hidden from the skill list because their tags were not registered: `compose-triangle-figure`, `symmetry-lines-regular` and `symmetry-rotation-regular`. Their tags are now registered.

## Response formats
- Multiple choice: distractors come from `check.alts` or from property names in `games/bank.js`. Every distractor is rejected by the verifier.
- Choose all that apply:
  - Properties: "Select every equation that shows the …".
  - Angle pairs: "Select every pair of angles that are …".
  - Every option is re-derived by the verifier. Other new skills report choose-all as unsupported.
- Open Response:
  - `properties` and `direct-variation` set `openResponse:{minC:4}`, so an Algebra Open Response section keeps them from difficulty 4 up. Below that, the existing four-part context bank is used, as before.
  - Geometry uses the dedicated "Four-part" skill.

## Shared fixes
- `engine.js`: an item adopted from a derived question keeps its source key "used", so the same source problem cannot be generated again.
- The choose-all direction text now reads "select every correct choice" outside the Inequalities unit.
- When a unit has no remaining gaps, the gap panel shows an accurate coverage note instead of an empty "Not generated yet" list.
- Cache versions are bumped to `coverage-20261111` for changed scripts.

## Tests
New: `tests/coverage-gap-tests.cjs` and `tests/coverage-gap-browser.cjs`, both added to `run-all.sh`. Updated: `select-all-mcas-tests.cjs` and `geometry-diagrams-tests.cjs`.
