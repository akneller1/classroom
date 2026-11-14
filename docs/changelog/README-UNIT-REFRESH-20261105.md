# Unit refresh — November 5, 2026

Drop-in update for every course (Algebra 1, Geometry, Algebra 2, 6th Grade, Pre-Algebra 7th, Pre-Algebra 8th, Precalculus, Calculus). Unzip it at the repository root. Folder paths match the site, so the files land in place. No questions or existing resources were removed.

## 1. Escape Room: a unique theme and cipher for every unit

- **Themes file.** `worksheet-generator/games/escape-themes.json` gives each of the 77 bank units its own setting, which includes:
  - the room story, title, scene emojis and colors
  - a 5-letter key-card password
  - a Caesar-cipher sentence whose answer word is unique to that unit
- **How it loads.** `games/course-activity.js` loads the theme for the unit the student opened, for every level (CP2, CP1, Honors).
  - The room headings follow the theme (for example "The Folding Room Lock").
  - The key-card stamps spell that unit's password in order.
- **Duplicates removed.** "PLANETS" and "COMET" no longer appear anywhere.
  - The older Algebra, Geometry and Algebra 2 room stories were kept wherever they were already unique.
  - Units that shared a word were given new ones.
- **Button colors (`games/escape.css`).**
  - Multiple-choice and panel buttons are now navy.
  - A selected choice gets a gold outline.
  - The submit buttons are now a separate bright green with a 🔒 icon: *Unlock*, *Open the door*, *Lock in this answer* and *Test the code*.
- **Verification.** All 77 units × 3 levels (231 rooms) were opened in a browser.
  - Each room showed its own title, password and cipher answer.
  - The stamps spelled the password every time.
  - No page errors occurred.

## 2. Cheat sheets for 6th Grade, Pre-Algebra (7th), Precalculus and Calculus

37 new two-page printable cheat sheets, one per unit:

| Course | Units |
| --- | --- |
| 6th Grade | 7 |
| Pre-Algebra (7th) | 13 |
| Precalculus | 8 |
| Calculus | 9 |

- **Format.** They use the same builder and layout as the existing Algebra and Pre-Algebra 8 sheets.
  - Front: vocabulary, formulas and worked examples.
  - Back: more examples, common mistakes and a self-check.
- **Answer checks.** Every worked-example answer is checked by the build script: 311 checks, all passing, with no layout overflow.
- **Files:**
  - content: `scripts/cheat-sheets/content/<course>-<unit>.cjs`
  - PDF: `artifacts/<course>-<unit>-cheat-sheet/worksheet.pdf`
  - thumbnail: `thumbs/<course>-<unit>-cheat-sheet.jpg`
  - listings: a block at the end of `data.js`
  - page counts: `resource-details.js`
- **Rebuilding.** To rebuild after editing content, run `node scripts/cheat-sheets/build.cjs <name> …`.
  - The Python generators in `tools/unit-refresh-20261105/` (`cs_*.py`) recreate the content files.

## 3. "Printable Activities" removed from unit pages

`app.js` no longer adds the Printable Activities section to 6th Grade, Pre-Algebra 7, Precalculus and Calculus unit pages.

Those generators (Maze, Color by Number, Partner Check, Station Work, Whodunnit, Error Analysis, Tarsia, Vocabulary/Crosswords) are all still in the Activity Generator. Their data entries were left in place, so nothing else breaks.

## 4. One activity order everywhere

Unit pages, the Activities browser and grouped views now use the same order:

- **Games:** Showdown (the Jeopardy-style game), Connect 4, Tic-Tac-Toe, Detective, Escape Room, Picture Reveal, then unit-specific activities and games.
- **Study Guides:** Assessment Readiness Check, Flashcards, Cheat Sheet.

This was checked on all 77 unit pages. Geometry Unit 3 still has its existing "Practice Activities: Triangle Congruence Proofs" section after Study Guides.

## 5. Projects for 6th Grade, Pre-Algebra (7th), Precalculus and Calculus

There is now one project for every unit of the four new courses, 37 projects in all:

| Course | Projects |
| --- | --- |
| 6th Grade | 7 |
| Pre-Algebra (7th) | 13 |
| Precalculus | 8 |
| Calculus | 9 |

The projects follow the Algebra 1 project format exactly.

- **Each project includes:**
  - CP2 (guided, with starters), CP1 (standard) and Honors (extension) versions, each as PDF, Word (.docx) and PowerPoint (.pptx)
  - a teacher guide with pacing, standards, misconceptions, extension ideas and an answer key for every question at every level
  - a project page and a thumbnail
- **Layout of each student handout** (6 pages):
  - Page 1: the scenario and illustration, learning goals and a timeline.
  - Pages 2–4: the three daily parts with answer boxes.
  - Page 5: the final product and reflection.
  - Page 6: the scoring rubric.
- **Fractions.** In the Word and PDF files, division is written as stacked fractions.
- **Where they appear.** The projects are in the Activity Generator only: Printable → Projects for each unit, registered in `worksheet-generator/menu/printables-projects.js`. No unit-page cards were added.
- **Files:**
  - `artifacts/<course>-project-<slug>/`
  - `thumbs/<course>-project-<slug>.jpg`
- **Rebuilding.** The generator is in `tools/course-projects-20261105/`. Run `python3 buildall.py` from that folder to rebuild every file after editing the content files `p_g6.py`, `p_g7.py`, `p_pc.py` and `p_ca.py`. It needs python-docx, python-pptx, Playwright, and LibreOffice with its Math module.
- **Checks.**
  - Every computed answer was checked with a script.
  - All 148 PDFs were scanned for blank or near-empty pages, and none were found.
  - Each of the 37 units was opened in the Activity Generator: every project card and download link loaded, with no page errors.

## Cache-busting

The `?v=` strings were bumped (`unit-refresh-20261105`) for these files, so browsers fetch the new versions:

- `index.html`: `data.js`, `app.js` and `resource-details.js`
- `activity.html`: `data.js` and `resource-details.js`
- `course-activity.html`: `course-activity.js`
- `printables.html`: `menu/printables-projects.js`

## Tests

The repository tests were run before and after the change:

- Escape cipher, lock, highlight and order tests: pass.
- Published question banks, grade, HS and Pre-Algebra bank integration: pass.
- Vocabulary flashcards, resource eligibility, browse-activities browser, arcade links, Algebra 2 native and integration, unit-specific arcade, approved games and question-bank loader: pass.
- `test-public-site` (run after `node scripts/build-site.mjs`): passes. Two assertions in it were updated to match intended changes:
  - the project count, from 37 to 74
  - the `app.js?v=` version string

## Not changed

The older standalone `artifacts/*-escape-room/` pages are not linked from any unit page and were left as they were.
