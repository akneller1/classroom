# Integration note

Installed on the newer main branch, preserving its Statistics expansion: 1,931 Statistics questions, 114 authored partner pairs, 140 error-analysis items, all current printable links, the Statistics-specific pairing path, and refreshed previews. The 18 new Honors items were appended without replacing existing questions or corrections. The older counts and Statistics exclusions in the original package report below describe the package author’s earlier source, not the merged installation.

# Site update 2026-11-07 · Activity-audit fixes

Built on `origin/main` at `4e80792` ("Refresh activity preview images from passing browser tests"). That
includes the Statistics restore/homepage work in `56a1346`. The only files both updates touch are `index.html`,
`activity.html` (a cache string) and `data.js` (one block). Those were merged on top of the newer versions.

## 1. Change summary

### Vocabulary Builder (standalone and inside Activity Builder)
- `worksheet-generator/vocabulary.html` now loads the shared catalog (`course-catalog.js` and
  `menu/course-catalog-bridge.js`), the same discovery the other generators use. The builder lists every course
  and unit in that catalog that has a vocabulary bank, so there is no second hand-kept list. It now offers
  Grade 6 (7 units), Grade 7 (13), Grade 8 (7), Algebra 1 (12), Geometry (10), Algebra 2 (all 11, replacing the
  old 9-unit list), Precalculus (8), Calculus (9) and Statistics (4).
- Geometry Transformations: `vocabulary-data.js` now has one shared alias table and two helpers,
  `MKVOCAB_BANK_ID`/`MKVOCAB_BANK`. They map `geometry-transformations` to the existing
  `geometry-coordinate-geometry-transformations` bank, so the bank is not duplicated. The flashcards
  (`games/vocabulary-flashcards.js`) use the same table. A link with the legacy id opens the right unit.
- A unit link (`?unit=…`, or the Activity Builder iframe) selects its own course and unit. Without a unit, the
  builder still opens on Algebra 1.

### Partner Check generator (`worksheet-generator/menu/printables.js`)
The short sheets had two causes:
- **Content:** in most short selections, almost no two approved questions shared an answer.
- **Algorithm:** three problems in the pairing code:
  1. It allowed at most 4 rows per skill, so units whose matches sat in a few skills stopped early.
  2. For bank questions it matched answers by exact string, so `x = 2` and `2` never paired. At the same time,
     two rows such as `15` and `n = 15` could both appear on one sheet.
  3. It kept only the first valid pair of an answer group, even when a same-skill pair existed.

What changed:
- **Algorithm:** the skill rounds now continue until the sheet is full, and the sheet still spreads across
  skills. Bank answers are compared in one canonical form, used both to pair and to keep rows distinct. A
  same-skill pair is preferred.
- **Explanation:** a sheet with fewer than 8 rows now says why on the page. It never repeats, rewords or
  borrows questions from another level.
- **Level-aware capability:** whether a bank skill can feed a printable was sampled only at CP1. It is now
  checked at the selected level, by `PR.capable(unit, skill, kind, level)`. The UI greying uses the same check.
- **Content:** 142 new short-answer *companion* questions were added to the banks, in
  `tools/partner-check-companions-20261107/`.
  - Each one is a different problem with exactly the same answer string as an existing question at the same
    level, usually in the same skill.
  - Each answer is recomputed independently in that script.
  - Each question's `sourceNotes` names its partner and says "Awaiting human review", like the existing items.
  - Existing questions, IDs, answers, diagrams and manifest approval flags are unchanged.
  - The static Algebra 2 partner-check PDFs (22 listings) are untouched.
  - The new questions by bank:

    | Bank | New |
    |---|---|
    | Algebra 2 · Quadratic Functions & Complex Numbers | 20 |
    | Algebra 2 · Rational Functions | 14 |
    | Algebra 2 · Sequences & Series | 12 |
    | Algebra 2 · Polynomial Functions | 8 |
    | Algebra 2 · Functions & Transformations | 7 |
    | Algebra 2 · Exponential & Logarithmic Functions | 7 |
    | Algebra 2 · Conic Sections | 7 |
    | Algebra 2 · Linear Functions & Systems | 6 |
    | Calculus · Precalculus Review | 22 |
    | Calculus · Antiderivatives and Definite Integrals | 5 |
    | Calculus · Fundamental Theorem of Calculus | 5 |
    | Grade 6 · Inequalities | 21 |
    | Grade 7 · Decimals and Equations | 8 |

### Statistics Honors formats
- 8 new Honors multiple-choice questions for Exploring Data and 10 for Sampling and Experimentation, in
  `tools/statistics-honors-formats-20261107/`. Each has a recomputed key and three distinct, rejected distractors.
- With the level-aware capability check, the Exploring Data printable Whodunnit and the Sampling and
  Experimentation Maze now build at Honors from Honors questions only:
  - Whodunnit: 10 clue cards.
  - Maze: 3 × 4 rooms. The Standard maze is still 2 × 2.
- The Standard-substitution note no longer appears for these, because no substitution happens. The layout
  limits are unchanged.

### Grade 8 activity catalog (`data.js`)
- The existing Grade 6/7 block of bank-driven printable links now includes Grade 8 (`prealgebra`). It adds 35
  entries: Maze, Color by Number, Partner Check, Station Work and Whodunnit Generator for each of the 7 units.
- The new entries reuse the same titles, thumbnails, `bankFormat`, levels and topics as Grades 6/7, with
  `added: 2026-11-07`.
- They use the existing generators and unit links. The Whodunnit is the printable `kind=who` and stays separate
  from the online Detective game.

### Tests and cache strings
- New: `scripts/test-partner-check-pairs.cjs`.
- Updated exact-count guards:
  - `scripts/test-statistics-bank.cjs`: 1221 → 1239.
  - `scripts/check-algebra2-coverage.cjs`: 4586 → 4667.
- Cache strings changed to `?v=audit-fixes-20261107`:
  - `data.js` in `index.html`, `activity.html` and `printables.html`.
  - `printables.js` and `printables-ui.js` in `printables.html`.
  - `vocabulary-data.js` and `vocabulary-builder.js` in `vocabulary.html`.

### Not changed (intentional exclusions kept)
None of these were added or changed:
- Statistics partner checks or error analysis.
- Discrete Math.
- Sampling and Experimentation color-by-number or printable Whodunnit.
- Matching Card Sort outside its function families.
- Interactive tools.
- Restoring removed games.
- Homepage or navigation.
- New standalone cards.

## 2. Installation
1. Unzip the package. Do not upload the ZIP itself.
2. On GitHub, use **Add file → Upload files** at the repository root. Drag in the unzipped folders and files
   (`question-banks`, `scripts`, `tools`, `worksheet-generator`, `data.js`, `index.html`, `activity.html`,
   and this README), keeping their folder paths. There are 33 files, under the 100-file upload limit.
3. Commit to `main`. GitHub Pages republishes automatically.
4. Optional local check, run from the repository root with a static server on port 8765:
   `node scripts/test-partner-check-pairs.cjs`.

## 3. Deletion manifest
None. No file needs to be deleted.

## 4. Validation report

### Tests run on this tree (rebased on 4e80792)
| Check | Result |
|---|---|
| `scripts/check_library.py` | 0 problems |
| `scripts/audit-course-catalog.cjs` | PASS (1548 resource entries) |
| `test-published-question-banks` | PASS, 59 banks, 24,561 unique questions |
| `test-statistics-bank` | PASS, 1,239 questions |
| `check-algebra2-coverage` | PASS, 4,667 questions |
| `test-algebra2-native`, `-bank-approval`, `-printable-sections`, `-printable-browser`, `-integration-browser` | PASS (157 browser routes) |
| `test-prealgebra-integration`, `test-grade-bank-integration` (Grades 6, 7), `test-hs-bank-integration` (Precalculus, Calculus, Statistics) | PASS |
| `test-tarsia-all-courses` | PASS, no failures |
| `test-vocabulary-flashcards` | PASS, 40 units |
| `test-coverage-report`, `test-resource-eligibility`, `test-browse-activities-browser`, `test-course-parity-browser` (589 scenarios), `test-interactive-math-update`, `test-interactive-math-statistics`, `test-arcade-links-thumbnails` | PASS |
| `printables-match-tests` | PASS, 1152 builds |
| Cheat sheets (`build.cjs all`, check only) | PASS, 0 overflow |
| `build-site.mjs` + `test-public-site` (85 projects with PDF/Word/PowerPoint, 1240 references) | PASS |
| **New** `test-partner-check-pairs` (3 seeds; 5 seeds for the audit selections) | PASS (723 sheets, 5,521 rows) |

The new partner test checks the following:
- Every row has two different problems.
- Each problem's key equals its bank answer at the sheet's level, or is verified by the generator's verifier.
- The two answers are equal, and no two rows share an answer.
- There is no level substitution.
- The 15 audit selections give 8 rows for every seed.
- All 142 companion questions match their partners.
- The two Statistics Honors formats use only Honors questions across 5 seeds.

Browser checks (Playwright, run against a local server):
- **Vocabulary: all 44 audit selections, embedded and standalone.** Each was opened through the real Activity
  Builder link (`printables.html#unit=…&kind=vocabulary`, iframe) and through standalone
  `vocabulary.html?unit=…`. All 44 passed:
  - The correct course and unit are selected in both.
  - Matching, fill-in-the-blank, examples and the crossword are generated, with one teacher-key section per
    student section.
  - Crossword cells stay white on screen and in print emulation.
- **Vocabulary: drawing tasks.** Draw-and-label tasks appear where the bank has diagram prompts (Geometry
  Transformations). The other 43 banks have no diagram prompts, so the builder says so instead of inventing
  them.
- **Vocabulary: legacy id.** The legacy `geometry-coordinate-geometry-transformations` link opens Geometry →
  Transformations.
- **Grade 8: all 35 listings.** Each listing's destination opened with the correct unit and printable selected
  and built pages at Remedial, Standard and Advanced. All thumbnails load, and the static site lists all 35.
  - Unit pages and Browse Activities intentionally do not show per-unit printable generator cards. This is the
    same for Grades 6/7 (`listed()` in `app.js`).
- **Statistics Honors through the UI.** Exploring Data Whodunnit (12 pages) and Sampling Maze (4 pages) built
  without an error or a fallback note.

### Pre-existing failures (identical on the unmodified base)
- `printables-tests.cjs`: "algebra1-statistics-data-modeling tarsia cp2: listed as unsupported". Algebra 1 is
  generated content and is not affected by this update.
- `printables-browser.cjs`: its expected list of known gaps is stale; it lists the intentionally excluded
  Statistics error-analysis and partner checks. The failure list is line-for-line the same as on the base
  commit.

### Remaining limitations
- **Remaining short partner sheets.** No sheet falls back any more. These whole-unit selections still have 4–7
  rows, and each shows its explanation note:
  - Algebra 1 · Factoring: Remedial (CP2), 4–7 rows depending on the seed.
  - Algebra 1 · Polynomials: Honors, 7.
  - Algebra 2 · Radicals: CP2 7, CP1 6, Honors 5.
  - Algebra 2 · Quadratic Functions & Complex Numbers: CP2, 6.
  - Algebra 2 · Polynomial Functions: Honors, 6.
  - Algebra 2 · Exponential & Logarithmic Functions: CP2 7, Honors 6.
  - Algebra 2 · Sequences & Series: CP2, 5.
  - Algebra 2 · Conic Sections: CP2, 6.
  - Algebra 2 · Probability & Statistics: Honors, 5.
  - Calculus · Derivatives: 5, 5 and 4.
  - Calculus · Fundamental Theorem of Calculus: CP2 5, Honors 7.
  - Calculus · Applications of Integrals: 7, 7 and 6.
  - Calculus · AP Review: CP1, 7.
  - Precalculus · Conics: CP2 7, CP1 5.
  - Precalculus · General Triangle Trigonometry: CP1 5, Honors 5.
  - Precalculus · Vectors: 5, 4 and 4.
  - Precalculus · Probability: CP1, 7.
  - Grade 8 · Systems: Advanced, 7.
  - Grade 7 · Area and Volume: 5, 5 and 7.
  - Grade 7 · Decimals and Equations: Remedial 7, Advanced 6.
  - Grade 7 · Linear Functions: Remedial, 7.
  - Grade 6 · Fractions and Decimals: Standard, 6.
  - Grade 6 · Rational Numbers: Advanced, 7.
  - Grade 6 · Geometry: Remedial 6, Advanced 5.
  - Grade 6 · Data Displays: Advanced, 7.

  Closing these needs more companion questions. The script in `tools/partner-check-companions-20261107/`
  takes them in the same format.
- **Review status.** The 160 new questions (142 companions and 18 Statistics Honors) are machine-checked, not
  teacher-reviewed. Like the existing authored items, they say "Awaiting human review".
- **Checks I could not perform.**
  - I did not test on the deployed GitHub Pages site or in browsers other than Chromium.
  - No printed paper output was examined; print was checked by CSS emulation only.
  - I did not have the audit document itself, so the audit's full pair-count table was not available. Instead,
    every partner-capable unit and level was scanned with the same generator.
