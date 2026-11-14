# Site update 2026-11-08: Common Core standards on teacher copies

Teacher versions now show which standards the lesson or problems address. Student copies are unchanged.

## Where the standards show up

| Page | Teacher copy | Student copy |
|------|--------------|--------------|
| Worksheet Generator | Answer key: a "Common Core standards addressed" table (code, plain-language summary, which questions) and small code chips under each question number | nothing |
| Assessment Generator (test and menu) | Same table on the teacher key (with dish labels such as A1, E2 for menus) and chips per question | nothing |
| Printable Generators (maze, color by number, Tarsia, error analysis, partner check, whodunnit, stations) | A closing "Standards addressed" page on the answer key | nothing |
| Daily Lesson Planner | Plan view and Teacher key list every standard with its summary. Algebra 2, Pre-Algebra, Math 6, Precalculus, Calculus and Statistics lessons now have standards too (they had none) | nothing |
| Teacher PowerPoint | Standards on the title slide and each standard's summary in the speaker notes | The Student PowerPoint no longer prints the codes on its title slide |

Where the codes come from:
- **Algebra 1 and Geometry:** the standards of the planner lessons that use each skill (up to 4 per skill, most relevant first). Skills no lesson uses were mapped by hand against the CCSS-M; the multi-part Open Response scenario lists the unit's 3 main standards.
- **Bank courses (Algebra 2, Pre-Algebra 7 and 8, Math 6, Precalculus):** the standards tagged on each approved question. A question in a key shows its own tags.
- **Calculus and Statistics:** their banks use AP framework codes, so those keys say "AP Calculus / AP Statistics framework codes" with the big idea or topic area instead of a Common Core summary.
- **Discrete Math:** the bank has no standards tags, so nothing is shown.

## Files in this update (17)

New:
- `worksheet-generator/menu/standards.js`: code normalizing, a summary for every Common Core code the site uses, and the teacher-key HTML
- `worksheet-generator/menu/standards-map.js`: generated skill → standards map (817 skills)
- `scripts/build_standards_map.cjs`: rebuilds the map (`node scripts/build_standards_map.cjs`; rerun after changing a scope, lesson-skills map or question bank)
- `scripts/test-standards.cjs`: checks the map is current and every code has a summary (added to `run-all.sh`)
- `README-SITE-UPDATE-20261108-standards.md`: this guide

Changed:
- `worksheet-generator/menu/render.js`: standards table and chips on worksheet/assessment keys
- `worksheet-generator/menu/printables-ui.js`: standards page on printable answer keys
- `worksheet-generator/algebra2-bank-native.js`: exposes each bank question's own tags
- `worksheet-generator/planner/planner-ui.js`: standards with summaries in Plan view and Teacher key
- `worksheet-generator/planner/scope-algebra2.js`: standards for catalog-course lessons
- `worksheet-generator/planner/pptx-export.js`: standards only on the teacher deck, summaries in notes
- `worksheet-generator/worksheet.html`, `menu-assessment.html`, `printables.html`, `lesson-planner.html`: load the two new scripts; cache string `?v=standards-20261108` on the changed scripts
- `worksheet-generator/menu/README.md`, `worksheet-generator/menu/tests/run-all.sh`

`data.js`, `index.html` and `app.js` are not in this update, so nothing else on the site can be overwritten.

## How to upload

1. Unzip first. Do **not** upload the ZIP itself.
2. On GitHub: Add file → Upload files, and drag in the `worksheet-generator` and `scripts` folders plus this README (not loose files at the root).
3. Commit to `main`.

## Checked

- `node scripts/test-standards.cjs`: 817 skills mapped, every code has a summary.
- Browser: worksheet, standard test, menu and Algebra 2 / Math 6 / Statistics keys; maze, stations, partner check, whodunnit, color by number, Tarsia and error analysis keys; planner days in Algebra 1, Geometry, Algebra 2 and Precalculus. No standards on any student copy, no page errors.
- Planner PowerPoint tests (Algebra 1 and Geometry): 0 failures.
