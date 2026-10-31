# Course framework and Claude content handoff

## Current architecture
- `data.js`: canonical course and unit records, titles, artwork colors, and resource links.
- `course-catalog.js`: single shared lesson/subskill list for **all six courses**. Read with `MK_COURSE_CATALOG.getSkills(courseId,unitId)` or `listCourses(window.LIBRARY)`.
- `app.js`: existing course cards, navigation, and unit pages; uses the shared catalog.
- `worksheet-generator/menu/skills/`: existing mathematical problem factories, maintained separately.
- `worksheet-generator/games/`: existing shared game engines. Do not replicate engines by grade.

## Adding a course or a unit
1. Add a stable lowercase course ID and unique unit IDs in `data.js`.
2. Add corresponding lesson arrays in `course-catalog.js` (same course/unit IDs).
3. Leave `artifacts: []` for units without working resources. **Do not link empty units to Algebra 1 question generators.**
4. Run `node scripts/audit-course-catalog.cjs` and review any findings before publishing.

## Contract for Claude's future question content
Each lesson needs an unambiguous course ID, unit ID and skill ID; three calibrated difficulties (CP2/CP1/Honors); verified question text; independently checked answer; student-friendly worked steps; and optional diagram spec or asset. Multiple-choice questions must have exactly one correct option and independently false distractors. Select-all questions must support multiple correct choices. Open response must have at least four parts. Diagram-dependent questions must keep each figure attached to the corresponding question. Never silently substitute questions from another grade/unit.

## Integration strategy
Keep question factories and diagrams in the skill-bank layer; shared generators and games should consume validated questions, not implement grade-specific math. Start by adapting *one* small 6th Grade unit to the existing question interface, test all three levels, and only then roll out across other units. Preserve existing Algebra 1/Geometry content and avoid mass migration without regression tests.

## Automated audit
The catalog audit validates course/unit uniqueness, lesson coverage, and resource file paths. It **does not** claim math correctness, question quality, diagram validity or browser behavior. Existing math-focused tests remain necessary; do not weaken them to turn builds green.

## Stable subskill IDs and content intake
`MK_COURSE_CATALOG.getSkillRecords(courseId,unitId)` returns objects `{id,name,index}` for Claude to reference. Example: the first skill in 6th Grade Math's `ratios-rates-percent-proportions` unit is `ratios-rates-percent-proportions-skill-01`. IDs are positional, so **do not reorder existing lessons after creating question banks** without an explicit ID migration. Future work can replace these transitional IDs with authored permanent IDs.

Claude can deliver one JSON file per unit conforming to `schemas/question-bank.schema.json`, then run `node scripts/check-question-bank.cjs path/to/unit-questions.json`. This currently checks format, identifiers, options, solution presence and open-response length; mathematical verification and diagram QA remain separate. Do not publish unverified questions merely because this structural validator passes.

## Universal question bank adapter (infrastructure milestone)
`question-bank-adapter.js` exports `window.MK_QUESTION_BANKS` with:
- `validate(bank)` → `{ok, errors}`, structural checks only
- `register(bank, {verified:true})` → registers a unit bank; verification flag must come **only after independent mathematical and diagram review**
- `available(courseId, unitId)` → true only for explicitly verified banks
- `select({courseId, unitId, skillIds, level, formats, limit})` → filtered defensive copies; no bank or unverified bank yields []
- `coverage(courseId, unitId)` → per-skill counts for CP2, CP1, Honors and approval status

The adapter is independent of existing game and generator question factories. It is **not yet wired into student-facing question generation**. Do not assume a structurally valid JSON bank is mathematically verified or mark it verified automatically. The integration layer should translate only approved question formats into each existing generator, with format-specific constraints and full regression tests. A new question should be written once, independently reviewed, and reused across appropriate activities, never duplicated as inconsistent versions.

Run `node scripts/test-question-bank-adapter.cjs` for the adapter's validation, gating, filtering, and mutation-isolation checks.

## Algebra 2 coverage (all eleven units)
Algebra 2 is now included in the same unit-page lesson selection and `Copy content brief` workflow as grades 6–8; this applies even to units with only placeholder resource entries. Existing Algebra 2 games/generators remain linked where present. The shared generator discovery bridge supplements the legacy Algebra 2 generator selector with any units missing there, including Conic Sections and Probability & Statistics. Unsupported units remain disabled until their actual validated question factories exist.

Content completion must be assessed by verified skill/format/difficulty coverage, not by presence of one or two resource links in `data.js`. Algebra 2 questions and diagrams are still reserved for Claude.

## Teacher question coverage dashboard
Open `coverage.html` from the website, or `coverage.html?course=algebra2` to filter to a course. The dashboard reports **only approved questions loaded into `MK_QUESTION_BANKS`**. It shows all six courses, 60 curriculum units and 503 subskills, counts CP2/CP1/Honors per skill, expands to unit detail and exports CSV for content production planning.

**Important**: Zero does not mean that legacy Algebra 1/Geometry/Algebra 2 generators are empty. The existing verified or unverified legacy factories are **not imported into this new adapter**, so the dashboard intentionally avoids claiming their content is approved. Once Claude's content is reviewed and integrated via `MK_QUESTION_BANKS.register(bank,{verified:true})`, the registered questions will be included in the dashboard. Never mark a bank verified simply to make the dashboard green.

Run `node scripts/test-coverage-report.cjs` to test the reporting model.

## Approved question-bank loading (live integration foundation)
The website and teacher coverage dashboard now load `question-banks/manifest.json` using `question-bank-loader.js`. An empty manifest is intentional until independent mathematical and diagram review is completed. Approved entries have this shape:
```json
{"version":1,"banks":[{"courseId":"algebra2","unitId":"conic-sections","path":"question-banks/algebra2/conic-sections.json","approved":true}]}
```
The JSON file itself must match `schemas/question-bank.schema.json` and the shared catalog IDs. Only entries explicitly marked `approved:true` are fetched, checked and registered with the verified adapter; unapproved entries are never fetched by the loader. Editorial reviewers must not flip the flag until answers, mathematical rigor, diagrams and difficulty have been independently verified. Changes to the file after approval require re-review.

Run `node scripts/test-question-bank-loader.cjs` to validate manifest safeguards. This loads banks into the shared adapter for eligibility/coverage reporting. **It does not yet replace existing game or generator engines**, and the manifest is empty until approved new questions are supplied.

## Shared approved-bank flashcards
`worksheet-generator/approved-flashcards.html?course=algebra2&unit=conic-sections` is the new standalone approved-bank flashcard player. It reads approved manifests and offers CP2/CP1/Honors, skill filtering, flip, worked solutions, shuffle and self-ratings. The new course readiness interface links to it only if an approved, compatible bank is available.

This intentionally does not replace `worksheet-generator/games/games.js` or its existing verified generation/diagram logic. Future question banks may provide diagrams, but the new text-only player does **not yet support figure rendering**: do not approve diagram-dependent questions for this player until diagram rendering and regression tests are added. No current approved question files are published.

Run `node scripts/test-approved-flashcards.cjs` for the current structural regression test. A passing structural test does not replace browser interaction tests or mathematical review.
