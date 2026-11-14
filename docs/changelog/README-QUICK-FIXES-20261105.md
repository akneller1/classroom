# Projects + quick fixes — November 5, 2026

Built on the live site (commit 59e3bf9). Unzip at the repository root; the folder paths match the site. No questions or existing resources were removed by the zip itself.

## 1. Projects for 6th Grade, Pre-Algebra (7th), Precalculus and Calculus

37 new projects, one for every unit (6th Grade 7, Pre-Algebra 7th 13, Precalculus 8, Calculus 9), in the Algebra 1 project format:

- CP2, CP1 and Honors versions, each as PDF, Word and PowerPoint, plus a teacher guide with answer keys.
- They appear only in the Activity Generator (Printable → Projects), registered in `worksheet-generator/menu/printables-projects.js`. No unit-page cards were added.
- Files: `artifacts/<course>-project-<slug>/`, `thumbs/<course>-project-<slug>.jpg`. The generator that rebuilds them is in `tools/course-projects-20261105/`.

## 2. Algebra 2 activities no longer fail at CP2 / Honors

`worksheet-generator/menu/printables.js`: when an Algebra 2 unit doesn't have enough CP2 or Honors questions for a Maze, Whodunnit or Partner Check, the generator now builds it from the Standard (CP1) questions. It shows a note saying so instead of an error.

Checked in a browser across all 11 Algebra 2 units: there are 0 errors (there were 24). 35 activity/level combinations now show the CP1 note. Tarsia and Error Analysis are still switched off for Algebra 2, as before.

## 3. Leftover generator cards removed from Browse Activities

`app.js`: the old per-unit "Maze / Color by Number / Partner Check / …" generator entries in 6th Grade, Pre-Algebra 7, Precalculus and Calculus are no longer:

- listed in Browse Activities
- counted in course totals
- shown as thumbnails on course-page unit cards
- offered in the unit filter

For example, 6th Grade now shows 63 activities instead of 119. Unit pages still link to the Activity Generator as before.

## 4. Lesson Planner course menu

`worksheet-generator/planner/planner-ui.js`: the Course menu now lists all eight courses:

1. 6th Grade Math
2. Pre-Algebra (7th)
3. Pre-Algebra (8th)
4. Algebra 1
5. Geometry
6. Algebra 2
7. Precalculus
8. Calculus

The course you're on is selected. Previously, 6th Grade, Pre-Algebra 7, Precalculus and Calculus all showed "Pre-Algebra" selected. Switching to any course from the menu now loads it.

## 5. Duplicate files — needs one extra step

A zip can't delete files, so the cleanup is in `cleanup/`. `cleanup/DELETE-LIST.txt` lists 250 items, about 40 MB and 664 files in total:

- **6 root `Geometry_0*.pdf` files.** Old cheat sheets, replaced by the `artifacts/geometry-*-cheat-sheet` pages.
- **Root `math6/` and `prealgebra7/` folders.** Identical copies of `question-banks/math6` and `question-banks/prealgebra7`.
- **13 root unit-named image folders.** Identical copies of folders in `question-banks/assets/`: `inequalities/`, `rational-numbers/`, `area-volume/` and 10 others.
- **225 root `m6-*.png` images.** Identical copies in `question-banks/assets/math6/`.
- **Root `manifest.math6-additions.json` and `manifest.prealgebra7-additions.json`.** Already merged into `question-banks/manifest.json`.
- **`INTEGRATION_AUDIT.json` and `practice-test-register.js`.** Not loaded by any page.

Pick one way to delete them:

- **From a local copy:** run `bash cleanup/delete-duplicates.sh` from the repository root, then commit and push.
- **From the GitHub website:**
  1. Move `cleanup/cleanup-duplicates.yml` into `.github/workflows/`.
  2. Open Actions → "Delete duplicate root files" → Run workflow.
  3. Afterwards, delete that workflow file and the `cleanup/` folder.

The older standalone game folders (48) and their thumbnails were kept. Old tests and possibly student bookmarks still point to them.

## Cache-busting

| File | Version bump |
| --- | --- |
| `index.html` | `app.js?v=quick-fixes-20261105` |
| `printables.html` | `menu/printables.js?v=quick-fixes-20261105` and `menu/printables-projects.js?v=new-course-projects-20261105` |
| `lesson-planner.html` | `planner/planner-ui.js?v=quick-fixes-20261105` |

`scripts/test-public-site.cjs` was updated to match: the project count changed from 37 to 74, and the `app.js` version string was updated.

## Tests

All tests were run with the duplicate files already deleted.

- `node scripts/build-site.mjs` followed by `node scripts/test-public-site.cjs` passes.
- All 50 other `scripts/test-*.cjs` and catalog checks pass, including browse-activities, course parity, Algebra 2 integration and printable browser tests.
- Planner and planner browser tests, games tests, match tests, cheat-sheet checks and the geometry suites pass.
- Unchanged from before this update, these still fail, as listed in the site audit:
  - `menu/tests/browser-test.cjs`: wording check
  - `menu/tests/printables-browser.cjs`: it forces Algebra 2 Error Analysis, which has no worked-step questions yet
  - `games/tests/games-browser.cjs`: legacy game folders
  - `geometry-curriculum-tests.cjs`: passes only when run from the repository root
