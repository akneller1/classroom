# 2026-11-14 — Pre-Algebra: Comparing Two Populations (7.SP.B.3–4)

This fills the one Grade 7 standard cluster the accelerated course was missing.

- **New skill.** Pre-Algebra Unit 12 (Data Analysis and Probability) has a new skill 09, "Comparing Two Populations" (`data-analysis-probability-skill-09`), added at the end of the unit's list in `course-catalog.js`.
- **48 new items**, 16 each at CP2, CP1 and Honors:
  - 7 short answer, 6 multiple choice, 2 error analysis and 1 four-part open response per level.
  - Families: difference of means; MAD of a data set; difference of means as a multiple of the MAD (Honors works it out from the raw data); difference of medians; and "which statement is best supported" for random samples (overlap judged by whether the difference is ≥ 2 MADs).
  - Standards: 7.SP.B.3 and 7.SP.B.4. The items are tagged in the meta tags file.
- **Checking.** `tools/hs-gap-skills-20261114/verify.py` recomputes every answer, distractor and student answer from the data printed in the prompt: 48 items, 0 errors.
  - To rebuild: `python3 build.py <root> pa7` (from `pa7_families.py`).
  - `build.py` now also reads catalogs indented with 4 or 6 spaces, and keeps statement-answer families out of short-answer, error-analysis and open-response items.
- **Cheat sheet.** Unit 12's back page now has a "Comparing Two Populations" example in place of "Check Yourself". The PDF was rebuilt, and its 9 example checks pass.
- **Vocabulary.** Added "mean absolute deviation (MAD)" to the Unit 12 vocabulary cards.
- **Standards.**
  - Added a description for 7.SP.B.4 in `worksheet-generator/menu/standards.js`.
  - Regenerated `standards-map.js` (883 skills; every standard has a description).
  - Updated `docs/prealgebra7/SKILL_MANIFEST.json`.
- **Cache strings.** `course-catalog.js`, `standards-map.js`, `menu/standards.js` and `vocabulary-data-middle-grades.js` now use `?v=pa7-compare-20261114`.

Tests that pass: audit-course-catalog, audit-question-banks, test-grade-bank-integration (345 prealgebra7 selections), test-prealgebra-integration, test-published-question-banks, test-question-bank-adapter, test-standards, test-vocabulary-flashcards, and check-question-bank.
