# Grade 7 (`prealgebra7`) question banks: integration handoff for ChatGPT

**Contents:** 13 units, 114 skills, **5,472 original questions**. Every skill has 48 questions: 16 Remedial (`cp2`), 16 Standard (`cp1`) and 16 Advanced (`honors`).

There are 265 diagram questions, each with its own generated PNG.

All items were written by Claude and checked by an independent verifier, which reported **0 errors**. They still **need human subject-matter review** before students see them. No file that already exists in the repository is replaced by this package.

## 1. Files in this package (paths are repository-relative)

| Path | Contents |
|---|---|
| `question-banks/prealgebra7/<unit-id>.json` (13) | Banks in the existing schemaVersion 1 format, the same as Grade 8 |
| `question-banks/prealgebra7/meta/<unit-id>.tags.json` (13) | Per-question tags, using only the existing tag vocabulary |
| `question-banks/assets/prealgebra7/<unit-id>/<question-id>.png` | Diagrams (`diagram.type: "image"` with a non-empty `alt`) |
| `question-banks/manifest.prealgebra7-additions.json` | 13 manifest entries with `"approved": false`. Merge these into the manifest only after review. |
| `worksheet-generator/vocabulary-data-middle-grades.js` | New file. Adds 139 vocabulary entries for the 13 units (`prealgebra7-<unit-id>`) to `MKVOCAB_BANKS`. Package B ships the same file with the Grade 6 entries added; when both packages are installed, use Package B's copy. |
| `scripts/test-grade-bank-integration.cjs` | New end-to-end test, modeled on `test-prealgebra-integration.cjs`. Set `MG_COURSE=prealgebra7 MG_PREFIX=pa7-` to run it for Grade 7. |
| `patches/grade6-7-integration.patch` | Small edits to existing site code so its generators treat Grades 6 and 7 the same way as Grade 8 (see §2). |
| `tools/middle-grades-authoring/` | Generation scripts, the independent verifier, reports, and `out/prealgebra7/*.checks.json` verification specs |
| `docs/prealgebra7/` | This handoff, `COVERAGE.md` / `.csv`, `ACTIVITY_COMPATIBILITY.md`, `VERIFICATION_REPORT.md`, `VALIDATION_LOG.txt` and `SKILL_MANIFEST.json` |

Unit IDs, skill IDs and skill names were read through the site's own `MK_COURSE_CATALOG.getSkillRecords('prealgebra7', unitId)`. No skills were added, renamed or reordered.

## 2. Integration steps

1. **Copy the files** into the repository at the paths above.
2. **Apply the patch** with `patch -p1 < patches/grade6-7-integration.patch`. It was checked with `--dry-run` against the current `main`. Each change extends an existing Grade 8 code path to `prealgebra7` and `math6`; there is no new runtime:
   - `worksheet-generator/algebra2-bank-native.js`: adds `prealgebra7` and `math6` to the courses whose authored banks may build Tarsia and Error Analysis printables. This list is currently hard-coded to `prealgebra`.
   - `worksheet-generator/planner/scope-algebra2.js`, `planner/course.js`, `planner/planner-ui.js`: register lesson-planner scopes `MKPLAN_SCOPE_PREALGEBRA7` and `MKPLAN_SCOPE_MATH6`, using the same code that builds the Grade 8 scope. They also select the right scope from `#course=` or `#unit=`, and use the Remedial/Standard/Advanced labels.
   - `data.js`: adds a block, after the Grade 8 block, that lists the same per-unit resources for Grades 7 and 6. Those resources are the seven games, the Vocabulary activities, the Error Analysis and Tarsia generators, and the Assessment Readiness Check. The block uses existing generic thumbnails. `python3 scripts/check_library.py` reports 0 problems with it.
   - `app.js`: one condition, so Grade 7 and Grade 6 unit pages use `algebraUnitView`, the same view as Grade 8. This makes the generators visible. If you prefer to keep the current unit pages, skip this hunk.
   - `vocabulary.html`, `course-game.html`, `approved-flashcards.html`, `middle-school-game.html`: load `vocabulary-data-middle-grades.js` right after `vocabulary-data.js`.
   - `vocabulary-builder.js`: show Remedial/Standard/Advanced labels for the `prealgebra7-` and `math6-` units.
3. **After human review**, merge the entries from `question-banks/manifest.prealgebra7-additions.json` into `question-banks/manifest.json` and set `"approved": true`. `question-bank-loader.js` serves non–Algebra 2 banks only when they are approved; see `docs/CLAUDE_QUESTION_BANK_HANDOFF.md`.
4. **Run the checks:**
   ```
   for f in question-banks/prealgebra7/*.json; do node scripts/check-question-bank.cjs $f; done
   node scripts/test-published-question-banks.cjs
   MG_COURSE=prealgebra7 MG_PREFIX=pa7- node scripts/test-grade-bank-integration.cjs
   python3 tools/middle-grades-authoring/gverify.py prealgebra7      # with MG_OUT=$PWD
   ```

## 3. Results already obtained in a test copy of the repository

These runs used a test copy with the patch applied and the 13 entries marked approved. Full output is in `docs/prealgebra7/VALIDATION_LOG.txt`.

- **Structural checker:** PASS for all 13 banks.
- **`test-published-question-banks`:** PASS (31 banks, 11,669 globally unique question IDs, every image present).
- **Adapter, loader, resource-eligibility and game-item tests:** PASS.
- **`test-grade-bank-integration` (Grade 7):**
  - 342/342 skill-level selections generate a bank problem;
  - 342 lesson plans build (Do Now, examples, practice, exit ticket);
  - 39 Connect 4 decks (13 units × 3 levels) have 20 distinct items, each multiple-choice with one correct choice;
  - 273/273 printable builds succeed: Color by Number, Partner Check, Whodunnit, Stations, Error Analysis, Tarsia and Maze for every unit and level;
  - 13 flashcard players work in mixed, vocabulary-only and skill-only modes;
  - every unit has a vocabulary bank of 8 or more terms.
- **Every other non-browser test** in `scripts/` gives the same result before and after the change. Three tests already fail on the unchanged repository: `test-escape-cipher-lock`, `test-escape-unit-ciphers` and `test-public-site`.

## 4. Content conventions (same as Grade 8)

- **Fields:** `id, skillId, level, format, prompt, answer, solutionSteps, options, parts, diagram, standards, sourceNotes`.
  - IDs look like `pa7-<unit-abbr>-sNN-<level>-NNN` and are globally unique.
  - `sourceNotes` names the problem family. Families whose names end in `_error` are the error-analysis items that the Error Analysis printable selects.
- **Formats per skill and level:**
  - 7 short-answer and 6 multiple-choice. Multiple-choice has 4 options, exactly one correct; correct positions are balanced.
  - 2 error-analysis items, which show a realistic student mistake with the reason and ask for the correct answer.
  - 1 select-all (at least 2 correct and 1 incorrect) or open-response (4 parts, each checked on its own).
- **Answers** are strings.
- **Math display:**
  - Fractions are written `a/b`, which the site's `math-display.js` shows as stacked fractions. The verifier ran every student-facing `/` through that same file.
  - Division of expressions uses `÷`.
  - Exponents use Unicode superscripts.
  - Repeating decimals follow the Grade 8 style, for example `0.4545… (45 repeats)`.
  - Units are abbreviated in area and volume answers (`cm²`, `in³`) so answers fit Tarsia and Maze cells.
- **Rounding and π:** every prompt that needs it says “use 3.14 for π”, “use π” or “in terms of π”, and states the place to round to.
- **Distractors** come from documented misconceptions, and the reason for each is used in the error-analysis items. Examples: adding denominators, forgetting to reverse an inequality sign, using the slant height as the height, simple interest used in place of compound interest, and finding the median without ordering the data.

## 5. Difficulty design

The levels differ in substance, not only in the size of the numbers. In equations, for example:
- **Remedial:** one-step, with whole numbers.
- **Standard:** integer coefficients, two steps and context.
- **Advanced:** multi-step work, fractions or decimals, variables on both sides, special cases, and reasoning items such as finding a missing exponent or reversing a midpoint.

## 6. Limitations and judgment calls

- **Gaps in specific activities.** These are listed per unit and level in `ACTIVITY_COMPATIBILITY.md`:
  - About half of the skill-level pairs have no bank answer that is an integer from 1 to 25. When a teacher's skill selection has none, Escape Room uses its existing unit-aligned cipher generator (`games/cipher-questions.js` already maps all 13 units).
  - Text-only multiple-choice games (Connect 4, Tic-Tac-Toe, Picture Reveal) skip diagram questions. Every skill-level pair still has text-only multiple-choice items.
- **Authored-key checks.** 118 conceptual items are checked against an authored key, not recomputed. These are property names, solid names, sampling methods, vocabulary-style terms and correlation-in-context. They are listed under `check:text` in `VERIFICATION_REPORT.md`.
- **Diagrams** come from the same data as the answers. Claude looked at samples from every diagram family, not at all 265 images.
- **Out-of-grade catalog topics.** A few catalog skills go beyond typical Grade 7 work: trig ratios, angles of elevation, special right triangles, FOIL, and systems by substitution. They were written at an introductory level that matches the catalog's Pre-Algebra textbook sequence. Advanced items stay within those topics and never move into Algebra 2 content.
- **Variety.** Each skill uses 2–6 problem families, and most families switch among several contexts or structures. Exact duplicates and near-duplicates are rejected across all units of both grades. Near-duplicates means the same prompt with the same numbers reordered and the same answer.
