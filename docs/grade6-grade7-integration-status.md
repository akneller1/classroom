# Grade 7 and Grade 6 integration status — 2026-11-04

## Published content
- Grade 7 (`prealgebra7`): 13 units, 114 skills, 5,472 authored questions, 265 diagrams.
- Grade 6 (`math6`): 7 units, 53 skills, 2,544 authored questions, 349 diagrams.
- Every skill has 16 questions at each of `cp2`, `cp1`, and `honors`; 48 per skill.
- 20 unit banks and their tags were moved/copied from the uploaded top-level folders to `question-banks/<course>/`.
- All 614 image files were copied to their canonical `question-banks/assets/<course>/<unit>/` paths.
- All 20 banks were added to `question-banks/manifest.json` and explicitly activated (`approved: true`) at the user's request to populate the website. This is a deployment decision, not a claim of human editorial signoff.

## Resource integration
- Shared native question bank loader / bank-to-skill adapters (same path as approved Grade 8).
- Course and unit resource-generator banners for both grades, with correct unit context.
- Lesson Plan, Worksheet, Assessment, and Printable Generator shortcuts.
- Games: Showdown, Connect 4, Tic-Tac-Toe, Escape Room, Detective, Picture Reveal.
- Study guides: Flashcards (vocabulary and questions), Assessment Readiness Check.
- Printables: Vocabulary, Error Analysis, Tarsia, Maze, Color by Number, Partner Check, Station Work, Whodunnit.
- Appropriate course, unit, difficulty and vocabulary labels; no Coming Soon labels for these grades.
- 16 activity cards registered per unit (320 in total), in addition to generator shortcuts.
- Existing Algebra 1, Geometry, Algebra 2 and Grade 8 question banks remain intact.

## Validation evidence and limits
- Each of the 20 published JSON files passed the existing `MK_QUESTION_BANKS.validate` schema and skill-ID checks after copying.
- All 20 expected bank paths and 614 image asset paths exist in the repository.
- Claude's delivered verification reports state 0 math-verifier errors. A subset of conceptual answers was checked against authored keys rather than independent computation; image families were spot-reviewed rather than every image individually.
- Claude's integration handoff reports successful builds in its test copy of the repo for all skill/level selections, 60 complete Connect 4 decks, 420 printable builds, 20 flashcard players and lesson-plan generation.
- CI has been added at `.github/workflows/grade6-grade7-bank-integration.yml` to run the repository's published-bank and full grade integration tests on affected pushes. Results of an actual GitHub Actions run are **not yet independently confirmed here**.
- The deployed browser pages have **not** been visually checked end-to-end. Please spot-check several student links and generated printouts before assigning to a full class.
- Specialized games, standalone projects and custom cheat sheets that require original authored assets are not synthesized merely by importing generic question banks.

See `docs/prealgebra7/` and `docs/math6/` for authoring handoff, coverage and validation reports.
