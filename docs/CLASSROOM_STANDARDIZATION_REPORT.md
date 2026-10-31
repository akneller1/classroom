# Classroom activity standardization and Algebra 2 integration

Date: 2026-10-31. Scope: existing resources in `akneller1/classroom`.

## Coverage

The approved manifest includes all 11 Algebra 2 units: 2,717 supplied questions, 87 skills and 76 distinct referenced images. Question-bank payloads and supplied mathematical images were not rewritten during standardization. Package validation checks structure, routing, source preservation and image references; it does not replace human mathematical review.

| Course | Units | Standard activity routes |
|---|---:|---:|
| Algebra 1 | 12 | 84 |
| Algebra 2 | 11 | 77 |
| Geometry | 10 | 70 |
| Pre-Algebra, grade 8 | 7 | 49 |
| Pre-Algebra, grade 7 | 13 | 91 |
| Grade 6 math | 7 | 49 |
| Total | 60 | 420 |

Seven formats use consistent catalog titles, descriptions and course routing: Flashcards, Connect 4, Tic-Tac-Toe, Picture Reveal, Showdown, Detective and Escape Room. Existing standalone resources and original catalog records are retained; duplicate visible game cards are consolidated, and saved legacy links map to their canonical cards. Middle-school courses retain their existing hidden navigation status and expose honest empty-bank states through direct activity routes.

## Behavior and presentation

- Division expressions render as stacked fractions with grouped numerators, denominators and exponents. Existing mathematical source strings remain intact.
- Connect 4 offers the opposing team a steal after a missed answer, hides the answer until the steal resolves, supports passing, and awards the disc to the answering team. Existing wins, column placement and turn controls remain.
- Detective uses the established case board, ten evidence clues, suspects, locations, methods, hints, worked solutions and final accusation.
- Escape Room uses five rooms, interactive locks, the cipher decoder, classification panels, ordered source solution steps, key cards and the final password. Incorrect submissions cost 30 seconds; hints cost 90 seconds.
- Showdown keeps the selected bank difficulty for every point value. It can present complete short-answer, select-all and multi-part source problems, with full answer details, rather than filtering the board to single-answer multiple-choice items.
- Catalog previews are screenshots of the actual corresponding course, unit and activity interface. Publishing requires all 420 previews and passing browser checks.
- Existing worksheet, practice-test, printable, menu-assessment and lesson-planner integrations continue to use the common approved-bank adapter. Existing original activities without a compatible bank-backed format are retained.

## Content limits

Every Algebra 2 skill has at least 11 standard-level source questions. All 87 standard-level Showdown categories have five distinct source questions: 435 populated cells. The supplied bank has 47 skill/level combinations with fewer than five total questions and 75 without multiple-choice questions. These are content-capacity limits, not permission to invent choices, split dependent investigations, change difficulty silently or author missing questions. Sparse optional levels show only available questions. Tarsia and Error Analysis retain existing resources where no compatible authored content is supplied.

## Validation evidence

- [Release integration workflow](https://github.com/akneller1/classroom/actions/runs/41207336117): passed. Includes 157 Algebra 2 routes, 372 cross-class activity scenarios, all 435 standard Showdown cells, 81 existing sharing catalogues, published-bank checks, resource eligibility, and generator editing/version/print regression.
- All 420 actual previews published in commit `fa107160561ba7aeee648d2c75ac6491c5491539` after those checks passed.
- Existing mathematics audit passed on the release source; the earlier complete per-unit audit passed all 23 jobs across Algebra 1 and Geometry.
- Geometry flashcard regression was aligned with the existing single-card eligibility policy: diagram criterion cards check their displayed criterion, and excluded dependent investigations must remain complete verified Showdown problems. [Geometry QA in GitHub Actions](https://github.com/akneller1/classroom/actions/runs/41207647154) passed: 1,089 independently checked cards and 441 whole-problem skill/tier cases, across ten units and three difficulties. No mathematical generator or diagram source was changed to satisfy this test.
- Live browser verification confirmed all 35 Conic Sections Showdown cells are playable and an ellipse question displays stacked fractions.

For source-by-source counts, see [Algebra 2 integration validation](algebra2/INTEGRATION_VALIDATION.md) and [coverage matrix](algebra2/COVERAGE_MATRIX.md).

Preservation check: the complete `question-banks` and `artifacts` Git tree hashes match the pre-standardization integration commit `e37ee685dd54eb066b700ecacbc1beb4aeda1acd` exactly (`17dafa7648e5a27c8b16c9efcc6f51547a78e021` and `e9f613e29bcdf2ec53a454a43b9d0622e7136e6b`).

Final repeat regression after the Geometry test correction: [integration run 41207647205](https://github.com/akneller1/classroom/actions/runs/41207647205) passed, including all 157 + 372 browser checks, generator regressions and the 420-preview publication. Pages deployment for source commit `ba8133bbfe9bc7794c8c6376cda5dd542be9e598` passed.
