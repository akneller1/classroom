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
