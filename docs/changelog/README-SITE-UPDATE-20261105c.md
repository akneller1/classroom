# Site update — November 5, 2026 (Algebra 2 questions, open audit items, new projects and games)

Built on the live site (commit 59e3bf9). Unzip at the repository root; folder paths match the site.

This zip includes everything from the earlier `site-update-quick-fixes-20261105.zip`. If you already uploaded that one, uploading this on top is safe. No existing questions were removed.

## 1. Algebra 2 has enough questions at every level

- **1,869 new Algebra 2 questions.** The bank went from 2,717 to 4,586 questions.
- **Every level is covered.** Every skill in all 11 units now has at least 16 questions at CP2, at CP1 and at Honors.
- **Error-analysis items.** 522 of the questions are error-analysis items ("a student solved this and made a mistake").
- **Checked answers.** Every answer was computed and checked by script. A planted-mistake test confirmed the checker catches errors.
- **Review status.** Like the other banks, the new questions are marked "Awaiting human review" in their source notes.
- **Rebuilding.** The authoring scripts are in `tools/middle-grades-authoring/a2_u01.py` to `a2_u11.py`. They are built by `a2build.py` and checked by `a2verify.py` / `a2checks.py`.

With the new questions:

- All 7 activity types build for every Algebra 2 unit at all 3 levels. No level has to borrow Standard (CP1) questions any more. The borrowing fallback stays in place as a safety net.
- Partner Check finds more matching-answer pairs in every course. Algebra 2 Trig went from 1 pair to 8.

## 2. Activity Generator: the same formats in every course

- **Algebra 2:** Tarsia and Error Analysis are now on for all 11 units at all 3 levels.
- **Geometry:** Maze and Tarsia are now on for all 10 units at all 3 levels.
  - Each problem prints in full, with its diagram, on numbered problem pages: two columns, about four problems per page.
  - The maze rooms and Tarsia edges show the problem number.
- **Tarsia diagrams (every course):** when any problem in a puzzle has a diagram or graph, the "Show Your Work" pages now print the problems with their diagrams. Before, the diagram was left off.
- **Matching Card Sort:** added for 4 more function units:
  - Pre-Algebra 7 Unit 8 (Linear Functions and Graphing)
  - Pre-Algebra 7 Unit 13 (Nonlinear Functions and Polynomials)
  - Precalculus Unit 2 (Functions)
  - Calculus Unit 1 (Precalculus Review)

  Pre-Algebra 8 Unit 3 already had it. The online "Play" version works for all of them, and middle-grade units show Remedial / Standard / Advanced.
- **Color by Number:** text no longer runs past the boxes. Long problems shrink to fit, and question images are size-capped.
- **Stacked fractions:** bank questions on Activity Generator pages now print "2/5" as a stacked fraction, as the worksheets, assessments and games already did.
- **"and" / "or" in problem text:** these read as ordinary words. Before, they were printed in small capitals, a style meant for answers like "x = 2 OR x = 3".

## 3. Unit-specific games for the newer courses

There are five new Math Arcade games, one per course. Each uses the unit's own question bank, and only multiple-choice questions with exactly one correct choice. Every game has 6 levels that ramp up in difficulty.

| Course | Unit | Game | Engine |
| --- | --- | --- | --- |
| 6th Grade | Expressions and Equations | Equation Launch Pad | rocket |
| Pre-Algebra (7th) | Solving Equations and Inequalities | Lava Bridge Builder | lava island |
| Pre-Algebra (8th) | Systems of Linear Equations | Laser Lock: Systems | laser intersection |
| Precalculus | Functions | Function Gates | portal |
| Calculus | Derivatives | Tangent Line Cannon | trig cannon |

- **Where they appear.** They show on their unit pages and in Browse Activities under Games. They're registered in `unit-specific-arcade.js`, and each has its own thumbnail.
- **Level names.** Middle-grade games use Remedial / Standard / Advanced.
- **Function Portal.** The existing Algebra 2 Function Portal now shows skill names instead of internal IDs.

## 4. Projects

| Course | Projects | Where they come from |
| --- | --- | --- |
| Pre-Algebra (8th) | 7 new, one per unit | this update |
| 6th Grade, Pre-Algebra 7, Precalculus, Calculus | 37 | earlier zip |

- **Pre-Algebra 8 titles:** Space Mission Planner, Road Trip Rate Lab, Phone Plan Showdown, Food Truck Face-Off, Screen Time & Sleep Study, Tile Pattern Studio and Skate Park Design.
- **Format.** Same as the other courses: CP2 / CP1 / Honors as PDF, Word and PowerPoint, plus a teacher guide with answer keys.
- **Where they appear.** In the Activity Generator only (Printable → Projects).

Every course now has projects.

## 5. Other fixes

- **Vocabulary:** every unit has at least 10 terms. The 21 units that had fewer were brought up to at least 12.
- **Lesson Planner:**
  - The Course menu lists all 8 courses.
  - A `#unit=` link now opens the right unit without a reload, and a link into another course loads that course.
- **Assessment and Worksheet Generators:**
  - **"Approve" checkbox restored.** Teacher-written problems can be approved again: "I checked this answer" on the problem card. The approval feature had lost its checkbox.
  - **Status messages.** The summary says "need approval" for teacher-written problems and "failed verification" only for answers that failed a check. When everything checks out it says "every answer verified".
- **Algebra 1 Unit 6 cheat sheets.** The second cheat sheet is retitled "Systems of Inequalities Cheat Sheet".
- **Browse Activities.** The leftover generator cards are gone, so 6th Grade shows 63 activities instead of 119.
- **Arcade.** "and" / "or" in game questions read as normal words.

## 6. Duplicate files: one extra step

A zip can't delete files. `cleanup/DELETE-LIST.txt` lists 250 items, about 40 MB and 664 files. Each one is an identical copy of a file the site uses, an upload already merged into `question-banks/manifest.json`, or a file no page loads.

- **From a local copy:** run `bash cleanup/delete-duplicates.sh`, then commit.
- **From the GitHub website:**
  1. Move `cleanup/cleanup-duplicates.yml` into `.github/workflows/`.
  2. Open Actions → "Delete duplicate root files" → Run workflow.
  3. Delete that workflow and the `cleanup/` folder afterwards.

## 7. Tests

- **New workflow, `.github/workflows/generator-browser-tests.yml`.** It runs on any change to the generators or question banks. A broken generator now fails a check on GitHub instead of reaching a classroom. It runs:
  - the Activity Generator engine test
  - the Matching Card Sort test
  - the printables browser test
  - the Assessment/Worksheet browser test
- **Four out-of-date tests fixed:**
  - `printables-tests` skips Projects.
  - `printables-browser` runs one unit at a time, so the browser no longer runs out of memory. It checks the current unit-page links.
  - `browser-test` matches the current unit-page buttons, test layout and Yes/No questions.
  - `games-browser` matches how the games behave now.
- **Flashcard test.** `test-approved-browser` accepts decks of 10 or more cards. The decks grew with the added vocabulary.
- **Arcade tests.** They cover all 12 games.
- **Coverage test.** The Algebra 2 coverage test reflects the larger bank.

Results:

- `node scripts/build-site.mjs` followed by `node scripts/test-public-site.cjs` passes, with 81 projects checked.
- All `scripts/test-*.cjs` pass, including the browser tests.
- The menu suite passes: printables, matching, Assessment/Worksheet browser, planner, games and all Geometry suites.

## Cache-busting

Every page that loads a changed script or stylesheet now asks for `?v=site-update-20261105c`. That covers `app.js`, `data.js`, `unit-specific-arcade.js`, the menu engine, printables, matching, planner, vocabulary data and math display, so browsers fetch the new versions.
