# Statistics question bank expansion — change summary

Built on the reference pack baseline (production commit c9f82af, 275 questions). Integration
files only: the four unit banks, 8 PNG figures, scripts, and reports. No data.js, catalog,
manifest, loader, adapter, HTML, or approval flag is included or changed; banks remain
unapproved pending human review.

## Totals
| Unit | Baseline | New | Total |
|---|---|---|---|
| exploring-data | 101 | 166 | 267 |
| sampling-experimentation | 42 | 170 | 212 |
| anticipating-patterns | 69 | 187 | 256 |
| statistical-inference | 63 | 219 | 282 |
| **All** | **275** | **742** | **1,017** |

By level: CP2 351, CP1 344, Honors 322. By format: multiple choice 732, short answer 198,
select-all 41, open response 46 (each with ≥4 parts and a 4-point scoring guide).
All 114 skill/level cells have ≥ 8 questions (28 cells have ≥ 10; 86 have 8–9).
After collapsing prompts that differ only by numbers (>85% similar), 979 distinct items remain;
one cell (anticipating-patterns-skill-06 CP2) has 7 distinct. This similarity measure is
conservative: items that share a long table stem but ask different questions are collapsed too.

IDs: all 275 baseline IDs, unit IDs and the 38 skill IDs are unchanged. New IDs follow
`stat-u<unit>-s<skill>-<level>-x<nn>`. Every new item's sourceNotes names its family and says
whether it was numerically verified or reviewed conceptually; all say "Awaiting human review."

## Corrections to baseline items (logged in scripts/verification/corrections.log)
The 9 open responses stat-u1-t1-046, stat-u1-t3-031, stat-u2-t1-019, stat-u2-t2-023,
stat-u3-t1-023, stat-u3-t2-028, stat-u4-t1-023, stat-u4-t2-023, stat-u4-t3-013 had rubric
criteria stored as part answers (4 also had "See rubric." as the answer). Each part now has its
actual answer; the rubric stays in solutionSteps. No other baseline item was edited.

## Checks actually run
- verify_expansion.py: 282/282 new computed items independently recomputed and passed (MC keys
  unique among options). During authoring it caught real errors that were fixed, including a
  food-truck expected value (E(X) is 16.5, not 16), mismatched distractors, and tolerance
  problems. 11 warnings are inputs written in words or implied (e.g., "fair die", "Twelve").
- validate-reference.py --source-math on the returned banks: strict schema, the site's
  check-question-bank.cjs for all 4 units, unique IDs/options, MC key consistency, coverage
  (0 rows below 8), and the original source verifier (regression of the original 158
  calculations only — not evidence for new items). All passed.
- Schema engine caveat: Python jsonschema is not installed in the build environment and could
  not be downloaded, so validation used Ajv 6.15 (draft-07 engine; the schema uses only
  draft-07-compatible keywords) through scripts/verification/ajv_shim. Re-run with the real
  jsonschema package before integrating.
- Near-duplicate scan: two new items that duplicated baseline questions were replaced.
- Not done: no game, worksheet, or printable was executed; figures were rendered and one was
  inspected visually, not tested in the site's player.

## Activity readiness (pool counts, reports/activity-pools.csv)
- Unit-level MC pools are 47–76 per unit and level, so Detective (10) and Millionaire (15)
  have enough MC items when a whole unit is selected at one level.
- Per single skill, only 4 of 114 cells have ≥ 10 MC (median 6, minimum 4). Detective or
  Millionaire restricted to one skill at one level will usually be underfilled.
- Escape Room candidates (short answer, integer 1–25, ≥ 4 steps): 14 total, 0–3 per unit/level.
  This is too few for full Escape Room sessions; the runtime's exact selection rules were not tested.
- Authored Error Analysis (sourceNotes "(family: …_error)"): 26 items; Exploring Data Honors and several
  CP1 cells have only 1. Rendering of these in the Error Analysis printable was not tested.

## Remaining gaps / review notes
- Coverage target of 10 per cell is met in only 28 cells; reaching 10 everywhere needs ≈ 120 more items.
- Length cue: in 284 of 472 new MC items the key is the longest option — mostly conceptual
  items. Teachers may want distractors lengthened.
- Conceptual answers and distractors were reviewed by the author only; they need a teacher's
  review. Written-response answers are model answers for teacher scoring, not auto-gradable.
- Statistical Inference skill 11 (slope intervals) is an extension topic; its CP2 items are
  scaffolded (t* or output supplied) rather than full procedures.
