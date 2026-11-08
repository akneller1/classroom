# Discrete Math validation report

Baseline: `origin/main` at `f85d24e5`. All commands were run from the repository root in a Linux sandbox with Node 22, Python 3.12 and Playwright Chromium. Nothing was committed, pushed or deployed.

## Checks that were run

| Area | Command | Result |
| --- | --- | --- |
| Bank schema, coverage, structure, answers | `node scripts/test-discrete-bank.cjs` | PASS: 2,805 questions in 10 banks. Every skill has ≥ 30 questions and ≥ 8 per level. Every unit has 18 error-analysis items (6 per level). 519 answers were recomputed independently in JavaScript (truth columns, set operations, list counts, gcd/lcm, Fibonacci, dice sums, Hamilton apportionment, Banzhaf, LP optima, and every quick-check template). |
| Bank build (Python, jsonschema + lint) | `python3 tools/discrete-math/bank/build_all.py` | PASS: validates every item against the bank schema (no extra properties) and checks MC (exactly one correct), select-all (≥ 2 correct) and open response (≥ 4 parts). |
| Shared consumers | `MG_COURSE=discrete MG_PREFIX=dm- node scripts/test-hs-bank-integration.cjs` | PASS: 10 flashcard players, 10 vocabulary banks, 231 lesson plans, 231 skill/level selections, 30 exact-level game decks, 210 printable builds (maze, color, partner, who, stations, Tarsia, error analysis); 0 printable failures. |
| Tarsia, all courses | `node scripts/test-tarsia-all-courses.cjs` | PASS: 273 builds, 0 failures. Discrete Tarsias use exact-level questions at every level. (Before the fix in this update, CP2 Tarsias for Speaking Mathematically fell back to CP1. I added computed quick-check items so each unit and level has about 25–45 distinct short answers.) |
| Published banks | `node scripts/test-published-question-banks.cjs` | PASS: 69 banks, 27,206 unique questions, all local diagrams present. |
| Adapter / loader | `node scripts/test-question-bank-adapter.cjs`, `node scripts/test-question-bank-loader.cjs` | PASS |
| Partner checks | `python3 tools/discrete-math/partner/build.py` | PASS: 360 matched A/B pairs (10 units × 3 levels × 2 sets × 6). All 720 printed problems were re-solved from their printed text by a separate solver and matched in pairs. 20 PDFs (6 pages each), 1 encrypted teacher key (30 pages). |
| Cheat sheets | `CHECK_ONLY=1 node scripts/cheat-sheets/build.cjs discrete-…` (all 10) | PASS: 127 example checks, 0 overflow problems. All 10 PDFs were rendered and inspected visually, front and back. |
| Interactive tools: challenges | `node tools/interactive-math-discrete/tests/walkthrough.cjs` | PASS 8/8: every "Try this" challenge is completed by driving the real controls. No challenge is done at the start, and there are no page errors. |
| Interactive tools: correctness and access | `node tools/interactive-math-discrete/tests/correctness.cjs` | PASS 121 checks. Outputs are compared with values computed independently or taken from the cheat sheets: equivalences and argument validity, gcd/lcm/Bézout and negative remainders, Fibonacci and closed forms, set expressions, relation properties and classes, all four counting models with full lists, Euler/Hamilton/χ/Kruskal, voting winners, Banzhaf and Shapley–Shubik, Hamilton/Jefferson/Webster/Adams. Also checked: keyboard Enter on relation vertices, arrow keys on graph vertices, no sideways scrolling at 390 px, and an accessible name on every control. |
| Real pointer input | ad-hoc Playwright script (mouse clicks on relation matrix cells, graph vertices, empty canvas, mouse drag) | PASS: adding edges, adding vertices, dragging and toggling pairs all work with a real mouse. |
| Worksheet keys | `python3 tools/interactive-math-discrete/tests/worksheet-answers.py` | PASS 93/93: every numeric and set answer in the 8 teacher keys is recomputed. |
| Worksheet PDFs | `node tools/interactive-math-discrete/fit_spacing.cjs`, `print_pdfs.cjs` | Every worksheet and key prints on exactly 2 pages. Several were inspected visually. |
| Site integration | `node tools/interactive-math-discrete/tests/site-integration.cjs` | PASS 112 checks. Each of the 9 tool cards appears in its unit's Interactive Math section with Explore, worksheet, key and Copy student link. The student link and activity viewer both load the tool. Generators are present. The course page is published. The cheat sheet and Millionaire appear on unit pages, and all 20 partner checks appear in Browse Activities → Printable Worksheets. |
| Statistics Interactive Math site test (updated) | `node tools/interactive-math-statistics/tests/site-integration.cjs` | Its Discrete Math assertion now expects a published course. |
| Menu bridge | `node worksheet-generator/menu/course-catalog-bridge.test.cjs` | PASS (now 9 groups, 69 units). |
| Interactive Math catalog | `node scripts/test-interactive-math-update.cjs` | PASS |
| Library | `python3 scripts/check_library.py` | 0 problems |
| Public site | `node scripts/build-site.mjs` then `node scripts/test-public-site.cjs` | All 10 Discrete unit pages link all four generators. See the pre-existing failure below. |
| Browser suites (with `python3 -m http.server 8765`) | `test-browse-activities-browser`, `test-course-parity-browser`, `test-approved-browser`, `test-unit-specific-arcade-browser`, `test-algebra2-integration-browser`, `test-algebra2-printable-browser`, `test-slope-golf-browser` | PASS (589 parity scenarios, 51 arcade routes, 157 Algebra 2 routes). These tests rewrite `thumbs/previews/**`; I restored those images afterward, so none are included. |
| All other node CI scripts (55 commands from `.github/workflows`) | run on both the baseline and this tree | Identical results apart from the Tarsia fix above. |

## Pre-existing failures (also fail on the untouched baseline `f85d24e5`)

- `scripts/test-statistics-bank.cjs` stops at its first line: it asserts Statistics is *not* planned, but Statistics is planned on `main`. I changed only the later line that required Discrete Math to stay planned. It now checks that the 10-unit outline is preserved.
- `scripts/test-public-site.cjs` fails on `statistics/anticipating-patterns` (a planned course has no generator links). With Statistics exempted, the test passes, including all 10 Discrete Math units. I removed the old Discrete Math "planned course" exemption.
- `test-escape-unit-ciphers.cjs` and the browser tests that need a server on port 8765 fail without one. The browser tests listed above pass when the server is running.

## Not run

- The GitHub Actions workflows themselves (no push). The new `.github/workflows/discrete-math.yml` runs the Discrete-specific checks above.
- `scripts/publish-resource-previews.cjs` / preview-image refresh: CI regenerates `thumbs/previews/**` ("Refresh activity preview images"). No preview images are included.
- A human mathematics review of all 2,805 items. The computed checks cover every quick check and every family with a recomputation engine; the remaining items were checked by their generators' own assertions (each family computes its answer and distractors from the same parameters).

## Honest limits

- The tools check truth tables, set identities by regions, relation properties and the like **by exhaustive computation**. None of them claims to check a written proof. The Recursion Explorer says explicitly that matching 15 terms is evidence, not proof.
- The Hamiltonian-cycle search is exhaustive and limited to 10 vertices. Above that, the tool says so instead of guessing.
