# Package A: Grade 7 (`prealgebra7`) question banks, ready to integrate

Unzip this at the repository root. Every path matches the repository layout, and no existing file is replaced.

- **Start here:** `docs/prealgebra7/HANDOFF.md` has the integration steps for ChatGPT, the test results, the conventions and the limitations.
- **Coverage:** `docs/prealgebra7/COVERAGE.md` has unit and skill tables. There are 13 units, 114 skills and 5,472 questions, with 16 per skill per level.
- **Verification:** `docs/prealgebra7/VERIFICATION_REPORT.md` and `VALIDATION_LOG.txt`. The independent verifier reported 0 errors, and all repository tests pass.
- **Activities:** `docs/prealgebra7/ACTIVITY_COMPATIBILITY.md`.
- **Banks:** `question-banks/prealgebra7/`. Diagrams are in `question-banks/assets/prealgebra7/`.
- **Manifest entries:** `question-banks/manifest.prealgebra7-additions.json`. They are set to `approved: false`; merge them after human review.
- **Vocabulary for flashcards:** `worksheet-generator/vocabulary-data-middle-grades.js`.
- **Integration patch:** `patches/grade6-7-integration.patch`, shared with Grade 6.
- **New end-to-end test:** `scripts/test-grade-bank-integration.cjs`.
- **Generation and verification scripts:** `tools/middle-grades-authoring/`.
