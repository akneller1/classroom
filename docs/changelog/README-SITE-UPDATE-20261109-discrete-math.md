# Site update 2026-11-09: Discrete Math course build-out

**Baseline:** `origin/main` at `f85d24e5`. **Nothing has been committed, pushed or deployed.** The ZIP holds only new and changed files at their repository paths. Unchanged files are not included.

Course ID `discrete`, display name **Discrete Math**. Unit IDs and order are unchanged: 1 `speaking-mathematically` … 10 `linear-programming`.

## What is included

| Deliverable | Files | Notes |
| --- | --- | --- |
| Question banks | `question-banks/discrete/<unit>.json` (10), `question-banks/assets/discrete/**` (34 PNG diagrams) | 2,805 questions, every `course-catalog.js` skill ≥ 30 (≥ 8 per level), all five formats, 18 error-analysis items per unit. Schema-valid (no extra properties). |
| Partner checks | `artifacts/discrete-<unit>-partner-check-{1,2}/worksheet.pdf` (20), `artifacts/discrete-partner-checks/teacher-key.pdf`, `thumbs/discrete-<unit>-partner-check-{1,2}.jpg` | Each PDF has 6 pages: CP2 A/B, CP1 A/B, Honors A/B, 6 matched pairs per level. The shared key is 30 pages, encrypted with code 205 as for the other courses (owner password `mrk-owner-discrete`). |
| Error analysis | inside the banks (`… (family: <name>_error)`) | 18 per unit (6 per level), with incorrect work, locate/explain and correct prompts, and teacher explanations. The site's Error Analysis Generator uses them. |
| Cheat sheets | `artifacts/discrete-<unit>-cheat-sheet/worksheet.pdf` (10), `thumbs/discrete-<unit>-cheat-sheet.jpg`, sources `scripts/cheat-sheets/content/discrete-<unit>.cjs`, `scripts/cheat-sheets/dmfigs.cjs` | Front and back, built with the existing `scripts/cheat-sheets/build.cjs`, every example checked. |
| Interactive Math | `artifacts/discrete-{truth-table-lab, euclid-explorer, recursion-explorer, venn-explorer, relation-explorer, counting-explorer, graph-lab, voting-explorer}/{index.html, worksheet.pdf, teacher-key.pdf}`, `thumbs/discrete-*.jpg` (8) | 8 new tools, plus the existing Feasible Region Optimizer listed under Linear Programming. Sources and tests are in `tools/interactive-math-discrete/`. |
| Vocabulary, planner | edits to existing files (see below) | 135 terms across all 10 units. |
| Reports | `docs/discrete/COVERAGE.md`, `docs/discrete/COVERAGE.csv`, `docs/discrete/VALIDATION_REPORT.md` | |
| Build tools and tests | `tools/discrete-math/**` (bank, partner, integration, report, patches), `tools/interactive-math-discrete/**`, `scripts/test-discrete-bank.cjs`, `.github/workflows/discrete-math.yml` | Everything can be rebuilt from source. |

## Install

1. Unzip at the repository root and upload with "Add files via upload", keeping the folder structure. The ZIP is split into numbered parts of at most 100 files each; upload each part the same way, in any order.
2. **Nothing needs to be deleted.**
3. If any of the existing files below changed on `main` after `f85d24e5`, apply the matching patch in `tools/discrete-math/patches/` (`git apply tools/discrete-math/patches/<file>.patch`) instead of replacing the file. Each patch is small and self-contained.
4. Optional rebuilds (outputs are already included):
   - banks: `python3 tools/discrete-math/bank/build_all.py`
   - partner checks: `python3 tools/discrete-math/partner/build.py`
   - cheat sheets: `node scripts/cheat-sheets/build.cjs discrete-<unit>`
   - tools: `python3 tools/interactive-math-discrete/build.py`, then `build_worksheets.py`, `print_pdfs.cjs` and `make_thumbs.cjs`
   - site wiring: `node tools/discrete-math/integration.cjs` (idempotent)

## Existing files that change (exactly these 16)

| File | Change |
| --- | --- |
| `data.js` | One new block inserted directly after the Precalculus/Calculus `planned=false` line (and before the cheat-sheet and Millionaire blocks, so Millionaire picks the course up). It adds, for each unit: 7 games, vocabulary, 7 printable generators (error, Tarsia, maze, color, partner, stations, whodunnit), the Assessment Readiness Check, the cheat sheet, 2 partner checks and the Interactive Math tool. It then sets `planned=false` for `discrete`. The full block is also in `patches/data.discrete-block.js`. |
| `resource-details.js` | 30 entries appended: 20 partner checks (`pages: 6`, shared key, `keyPages: 30`) and 10 cheat sheets (`pages: 2`, `referenceSheet`). |
| `app.js` | `'discrete'` added to the same five lists that Precalculus/Calculus use: the "Coming Soon" label (home card and course band), the published band meta, unit cards, generator URLs, and the `algebraUnitView` route. No redesign. |
| `question-banks/manifest.json` | 10 `discrete` entries (`approved: true`, `teacherUse: true`). |
| `worksheet-generator/vocabulary-data-middle-grades.js` | Appended `DISCRETE-MATH-VOCAB` block (keys `discrete-<unit>`). |
| `worksheet-generator/planner/scope-algebra2.js`, `planner/course.js`, `planner/planner-ui.js` | `discrete` added to the course lists, regexes and the Course dropdown (scope key `DISCRETE`, prefix `DM`). |
| `worksheet-generator/menu/course-catalog-bridge.js` (+ `.test.cjs`) | `'discrete'` added to `courseIds`; the test now expects 9 groups and 69 units. |
| `index.html`, `activity.html` | Cache strings `data.js`, `app.js`, `resource-details.js` → `?v=discrete-math-20261109`. |
| `guide.html` | A Discrete Math row in the Interactive Math coverage table, and "Discrete Math" added to three sentences. |
| `scripts/test-public-site.cjs` | Removed the exemption that required Discrete Math unit pages to have no generators. |
| `scripts/test-statistics-bank.cjs` | The assertion that Discrete stays planned now checks that its 10-unit outline is preserved. |
| `tools/interactive-math-statistics/tests/site-integration.cjs` | The Discrete Math check now expects a published course. |

## The interactive tools

| Unit | Tool | Students discover |
| --- | --- | --- |
| 2 Logic | Truth Table Lab | Equivalence means identical columns; a conditional ≡ its contrapositive, not its converse or inverse; validity means the conclusion is true in every critical row. |
| 3 Number theory | Euclidean Algorithm Explorer | gcd(a, b) = gcd(b, r), shown as square tiling; Bézout coefficients; gcd·lcm = ab; remainders stay in 0 ≤ r < d for negative n. |
| 4 Sequences | Recursion & Closed Form Explorer | Arithmetic and geometric recurrences, fixed points, second-order recurrences; a matching closed form is a conjecture until proved by induction. |
| 5 Sets | Venn Diagram & Membership Table Explorer | Expressions are determined by their regions (a membership table); U is explicit for complements; one region with an element disproves an identity. |
| 6 Relations | Relation Property Explorer | Digraph tests for each property, with a counterexample shown in red; closures; equivalence classes form a partition. |
| 7 Counting | Counting Outcomes Explorer | Order and repetition choose the model; each combination has r! orderings; multisets are not equally likely. |
| 8 Graphs | Graph Explorer: Euler, Hamilton & Trees | Degree sum = 2|E|; Euler conditions; exhaustive Hamiltonian search; trees have n − 1 edges; χ; step-by-step Kruskal. |
| 9 Elections | Voting, Power & Apportionment Explorer | Four named methods can disagree; majority and Condorcet checks; tie rule stated, no tie-breaking; Banzhaf and Shapley–Shubik; quota rule and Alabama paradox. |
| 10 Linear programming | Feasible Region Optimizer (existing) | Reused instead of duplicated. |

Each tool has instructions, live feedback, 5–8 "Try this" challenges (none done at the start), Reset, and a closed "What should I notice?" panel. It works with mouse, touch and keyboard (−/+ on sliders, arrow keys or Enter on SVG items, form alternatives for every pointer action). It has no runtime AI or external APIs, and each has a 2-page Explore & Reflect worksheet and teacher key.

## Exceptions (documented, not hidden)

- **Unit 1, Speaking Mathematically, has no interactive tool.** Its content (variables, quantifier language, set-builder notation, relations as sets) is covered by the Truth Table, Venn and Relation tools. The unit has everything else: games, generators, cheat sheet and partner checks.
- **Linear Programming reuses the Algebra 2 Feasible Region Optimizer.** Its worksheet header says "Algebra 2".
- **Partner checks are not shown on unit pages,** which matches every other course. They are listed in Browse Activities → Printable Worksheets, and the Partner Check Generator is on every unit page.
- **Diagrams:** 72 items use image diagrams (sets, relations, counting trees, graphs, LP regions). Units 1–4 and 9 present tables and schedules in text, because the site renders only image diagrams.
- **Two failing checks already fail on the untouched baseline** (Statistics is still `planned`): `test-statistics-bank.cjs` and the Statistics part of `test-public-site.cjs`. Details are in `docs/discrete/VALIDATION_REPORT.md`.
- `thumbs/previews/**` is not included. CI refreshes those images.

"Coming soon" was removed only for Discrete Math, and only because every unit is complete and tested.
