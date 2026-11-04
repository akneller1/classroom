# Grade 6 (`math6`) question banks: integration handoff for ChatGPT

**Contents:** 7 units, 53 skills, **2,544 original questions**. Every skill has 48 questions: 16 Remedial (`cp2`), 16 Standard (`cp1`) and 16 Advanced (`honors`).

There are 349 diagram questions, each with its own generated PNG. These include:
- number lines with fractional ticks;
- coordinate planes;
- composite polygons and nets;
- rectangular prisms;
- dot plots, histograms and box plots.

The independent verifier reported **0 errors**. The items still **need human subject-matter review** before students see them. No file that already exists in the repository is replaced.

This package uses the same schema, tools, patch and process as Package A (Grade 7). You can install it with or without Package A.

## 1. Files in this package (paths are repository-relative)

| Path | Contents |
|---|---|
| `question-banks/math6/<unit-id>.json` (7) and `meta/<unit-id>.tags.json` (7) | Banks (schemaVersion 1) and per-question tags |
| `question-banks/assets/math6/<unit-id>/<question-id>.png` | Diagrams (`diagram.type: "image"` with a non-empty `alt`) |
| `question-banks/manifest.math6-additions.json` | 7 manifest entries with `"approved": false`. Merge them after review. |
| `worksheet-generator/vocabulary-data-middle-grades.js` | Vocabulary for flashcards and the vocabulary activities: 64 Grade 6 entries (`math6-<unit-id>`) and 139 Grade 7 entries. This file is identical to Package A's. |
| `scripts/test-grade-bank-integration.cjs` | End-to-end test. Run it with `MG_COURSE=math6 MG_PREFIX=m6-`. |
| `patches/grade6-7-integration.patch` | The same patch as Package A, covering both grades. Apply it once. |
| `tools/middle-grades-authoring/` | All generation and verification scripts for both grades (`g6_u01.py` … `g6_u07.py` plus the shared tools), and `out/math6/*.checks.json` |
| `docs/math6/` | This handoff, `COVERAGE.md` / `.csv`, `ACTIVITY_COMPATIBILITY.md`, `VERIFICATION_REPORT.md`, `VALIDATION_LOG.txt` and `SKILL_MANIFEST.json` |

Unit IDs, skill IDs and skill names were read through `MK_COURSE_CATALOG.getSkillRecords('math6', unitId)`. Nothing was added, renamed or reordered.

## 2. Integration steps

1. **Copy the files** in. If Package A is already installed, the shared files (tools, patch, test and vocabulary) are identical and can be overwritten.
2. **Apply `patches/grade6-7-integration.patch`** if it is not already applied. See Package A's `docs/prealgebra7/HANDOFF.md` §2 for what each hunk does. Every hunk already handles `math6`: printables, lesson-planner scope, unit listings in `data.js`, the unit view in `app.js`, vocabulary script tags and level labels.
3. **After human review,** merge `question-banks/manifest.math6-additions.json` into `question-banks/manifest.json` with `"approved": true`.
4. **Run the checks:**
   ```
   for f in question-banks/math6/*.json; do node scripts/check-question-bank.cjs $f; done
   node scripts/test-published-question-banks.cjs
   MG_COURSE=math6 MG_PREFIX=m6- node scripts/test-grade-bank-integration.cjs
   MG_OUT=$PWD python3 tools/middle-grades-authoring/gverify.py math6
   ```

## 3. Results already obtained in a test copy of the repository

These runs used a test copy with the patch applied and the Grade 7 and Grade 6 entries marked approved. Full output is in `VALIDATION_LOG.txt`.

- **Structural checker:** PASS for all 7 banks.
- **`test-published-question-banks`:** PASS (38 banks, 14,213 globally unique IDs, every image present).
- **Adapter, loader, eligibility, game-item and Grade 8 integration tests:** PASS.
- **`test-grade-bank-integration` (Grade 6):**
  - 159/159 skill-level selections generate a bank problem;
  - 159 lesson plans build;
  - 21 Connect 4 decks (7 units × 3 levels) have 20 distinct items, each multiple-choice with one correct choice;
  - **147/147 printable builds succeed:** Color by Number, Partner Check, Whodunnit, Stations, Error Analysis, Tarsia and Maze for every unit and level;
  - 7 flashcard players work in all three modes;
  - every unit has a vocabulary bank of 8 or more terms.
- **Cross-course duplicates:** none across Grade 6, Grade 7 and the published Grade 8 banks (11,496 questions).

## 4. Content and difficulty notes

- **Conventions are the same as Grade 7:**
  - per skill and level, 7 short-answer, 6 multiple-choice, 2 error-analysis, and 1 select-all or open-response;
  - answers are strings;
  - fractions are written `a/b` and shown stacked by `math-display.js`;
  - area and volume answers use `cm²` and `in³`.
- **Grade 6 scope is kept:**
  - Inequalities use positive coefficients only. The sign is never reversed, following 6.EE.8. A distractor that reverses the sign is labelled as that misconception.
  - Rational-number work uses halves, quarters, tenths and thirds.
  - Prism volume uses fractional edges (6.G.2), including counting cubes with edge 1/2, 1/3 or 1/4.
  - Statistics uses MAD, IQR and shape, with no standard deviation.
- **Levels:**
  - Remedial uses whole numbers and familiar denominators.
  - Standard adds unlike denominators, mixed numbers and context.
  - Advanced adds multi-step work, reasoning items (counting integers between two rationals, finding a fourth vertex, missing dimensions) and composite figures.
- **Reused Grade 7 families.** About 41% of the questions (1,035 of 2,544) come from verified Grade 7 families reused at Grade 6–appropriate levels through `glib.reuse`, for skills such as order of operations, one-step equations and inequality graphs. The reuse is mapped so each Grade 6 level uses an equal or easier Grade 7 level. Every item is newly generated and differs from the Grade 7 items; cross-course duplicate prompts are rejected.

## 5. Limitations

- **Escape Room cipher.** When a skill/level has no bank answer that is an integer from 1 to 25, Escape Room uses its existing unit-aligned cipher generator, which already covers all 7 units. Per-skill counts are in `ACTIVITY_COMPATIBILITY.md`.
- **Authored-key checks.** 42 conceptual items are checked against an authored key rather than recomputed: statistical-question wording, dependent and independent variables, and interpreting `<` in context.
- **Diagrams** were reviewed by sampling each diagram family, not one by one.
- **Statistical questions skill.** “Statistical Questions” is mostly multiple-choice classification. Its short-answer items answer a statistical question with data (the median), and its extras come from data-summary families.
