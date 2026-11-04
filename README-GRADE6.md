# Package B: Grade 6 (`math6`) question banks, ready to integrate

Unzip this at the repository root. Every path matches the repository layout, and no existing file is replaced.

- **Start here:** `docs/math6/HANDOFF.md` has the integration steps for ChatGPT, the test results, the conventions and the limitations.
- **Coverage:** `docs/math6/COVERAGE.md` has unit and skill tables. There are 7 units, 53 skills and 2,544 questions, with 16 per skill per level.
- **Verification:** `docs/math6/VERIFICATION_REPORT.md` and `VALIDATION_LOG.txt`. The independent verifier reported 0 errors, and all repository tests pass.
- **Activities:** `docs/math6/ACTIVITY_COMPATIBILITY.md`.
- **Banks:** `question-banks/math6/`. Diagrams are in `question-banks/assets/math6/`.
- **Manifest entries:** `question-banks/manifest.math6-additions.json`. They are set to `approved: false`; merge them after human review.
- **Vocabulary for flashcards:** `worksheet-generator/vocabulary-data-middle-grades.js` (Grades 6 and 7).
- **Integration patch:** `patches/grade6-7-integration.patch`. Apply it once; it covers both grades.
- **New end-to-end test:** `scripts/test-grade-bank-integration.cjs`.
- **Generation and verification scripts:** `tools/middle-grades-authoring/`.
