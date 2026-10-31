# Algebra 2 cheat sheets — Units 4, 5, 7, 8, 9, 10, 11

Units 1, 2, 3 and 6 already had cheat sheets. This adds the seven that were missing. They are built with the site's shared cheat-sheet builder (`scripts/cheat-sheets/`, the same style as every Algebra 1 and Geometry sheet).

| Unit | Title | PDF |
|---|---|---|
| 4 | Polynomial Functions Cheat Sheet | artifacts/polynomial-functions-cheat-sheet/worksheet.pdf |
| 5 | Radicals & Rational Exponents Cheat Sheet | artifacts/radicals-rational-exponents-cheat-sheet/worksheet.pdf |
| 7 | Rational Functions Cheat Sheet | artifacts/rational-functions-cheat-sheet/worksheet.pdf |
| 8 | Sequences & Series Cheat Sheet | artifacts/sequences-series-cheat-sheet/worksheet.pdf |
| 9 | Conic Sections Cheat Sheet | artifacts/conic-sections-cheat-sheet/worksheet.pdf |
| 10 | Trigonometric Functions Cheat Sheet | artifacts/trigonometric-functions-cheat-sheet/worksheet.pdf |
| 11 | Probability & Statistics Cheat Sheet | artifacts/probability-statistics-cheat-sheet/worksheet.pdf |

## What's in the ZIP (repo-relative paths, upload over the repo root)
- `scripts/cheat-sheets/content/<unit>.cjs` — source for each sheet (6 + 6 sections, worked examples with `check` entries).
- `artifacts/<unit>-cheat-sheet/worksheet.pdf` — 2-page Letter PDF.
- `thumbs/<unit>-cheat-sheet.jpg` — 720 × 450 thumbnail.
- `data.js` — the 7 new library entries (Printable; topics Cheat sheet / Reference / unit / Unit N; added 2026-10-31), each appended to its Algebra 2 unit's `artifacts` list.
- `resource-details.js` — `{pages: 2, referenceSheet: true}` for each new PDF, matching the existing cheat sheets.
- `patches/data.js.patch`, `patches/resource-details.js.patch` — the same two edits as unified diffs, in case `data.js` or `resource-details.js` changed on the live repo since this copy was taken. Apply the patches instead of overwriting the files if so.

## Checks run
- `node scripts/cheat-sheets/build.cjs …` — 90 worked-example checks pass for the new sheets; no section or page overflows.
- `CHECK_ONLY=1 node scripts/cheat-sheets/build.cjs all` — all 34 cheat sheets: 248 checks, 0 overflows.
- `python3 scripts/check_library.py` — no new problems (the 2 reported "assessment readiness check" duplicate-title items were already there).
- `node scripts/test-resource-eligibility.cjs` — PASS.
- Every page was rendered and inspected visually.
