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

---

# Second and third passes (same day): remaining gaps

**Algebra 1**
- Unit 4: `graph-from-story`.
- Unit 5: `absolute-value-functions` (features, an equation from a description, an equation from a drawn graph) and `compare-functions`.
- Unit 6: `sys-linear-quadratic`, `sys-three-variable` (Honors) and `viable-solutions`.
- Unit 7: `rational-exponents-variables`.
- Unit 8: `exp-overtakes-linear`.
- Unit 11: `quadratic-forms`.

**Geometry**
- Unit 1: `protractor-reading` (new `geo-protractor` figure), `conditional-statements`, `undefined-terms-postulates` and `constructions-concepts` (authored question templates with random point names; the verifier holds its own answer key).
- Unit 2: `two-transversals` (new `geo-two-trans` figure) and `parallel-lines-proof` (two-column proof with missing reasons on the numbered transversal figure, checked row by row).
- Unit 4: `triangle-orthocenter-coordinates` and `triangle-relationship-proof` (reuses the congruence proof engine through `NS.congruenceProofFor`).
- Unit 5: `similarity-proof` (AA proofs on the `geo-tri-par` figure).
- Unit 6: `law-of-sines-ambiguous`.
- Unit 7: `quadrilateral-classify-grid` and `quadrilateral-proof`.
- Unit 8: `rigid-motion-mapping`. The verifier applies the student's described sequence to the vertices.
- Unit 9: `circle-equation-three-points-tangent` and `circle-arc-sector-decimal`.
- Unit 10: `measure-composite-plane` (new `geo-comp` figure; the dimensions are also stated in the sentence).

**Shared**
- `engine.js` drops any suggested distractor that the verifier would accept.
- Proof tables now render under any proof figure (`F.proofTable`).
- `standards.js` adds A-REI.C.7 and G-CO.D.13.
- Planner notes are updated for U4-L6, U6-L10, U8-L8 and U11-L4.
- A variable-name collision introduced in pass 2 (`STORIES`) broke the existing graph-behavior stories. It is fixed.

**Still limited by design**
- Hand-drawn graphs and sketches are checked by the teacher.
- Compass work is described in words.
- Paragraph proofs are not generated.

---

# Fourth pass (same day): proofs and choose-all quadrilaterals

- Geometry Unit 5: `similarity-proof-sss-sas`. Students complete SSS~ and SAS~ proofs on a drawn pair of triangles. Ratios appear as "p : q", and every ratio is re-derived from the given lengths.
- Written two-column proofs: at Honors, `parallel-lines-proof`, `similarity-proof` and `similarity-proof-sss-sas` sometimes give a blank table that students fill in. Typed answers use the form "1. statement — reason; 2. …". The verifier checks every row. It also requires the rows to be numbered 1, 2, 3 … in order and requires at least 3 rows.
- Choose all that apply, for `quadrilateral-classify-grid`: "Select every name that applies to quadrilateral X." The verifier classifies the shape from its grid coordinates, using an exclusive definition of trapezoid that is stated in the prompt. It never offers Kite as a wrong answer for a rhombus or a square.
- Cache versions are bumped to `coverage-20261111c`.

---

# Fifth pass (same day): paragraph proofs

- From difficulty 4 up, about a third of these proofs are printed as paragraph proofs instead of tables: `parallel-lines-proof`, `similarity-proof`, `similarity-proof-sss-sas`, `triangle-relationship-proof` and `quadrilateral-proof`.
- Each paragraph is built from the same rows as the two-column proof. The rows become sentences, for example "We are given that … Then ∠2 ≅ ∠7 by (a) ____. Therefore, …". Every blank is checked by the same row-by-row verifier, and the answer key fills in the blanks.
- A paragraph proof never asks for "Given" as a reason. The rendering lives in the shared `F.proofTable` (`proof.paragraph`, optional `proof.lead`).
- `coverage-gap-tests.cjs` checks that each skill produces paragraph proofs, that the student copy shows no answers, that the key fills every blank, and that a wrong blank is rejected.
- Still limited: students do not write paragraph proofs from scratch. Written-from-scratch proofs stay two-column at Honors.
- Cache versions are bumped to `coverage-20261111d`.
