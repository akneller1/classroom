# Mr. K's Classroom — Worksheet Generator

A browser-only worksheet generator. First unit: **Algebra 1 — Linear Functions** (all 21 skills).
No server, no build step, no accounts, no network calls at run time. Open
`algebra1-linear-functions.html` in a browser (double-click works), or host the folder on GitHub Pages.

## What it does
Pick skills and counts → choose difficulty, number mode, workspace, grids, title, name line, versions A/B/C,
and key style → preview the paginated Letter pages → regenerate one problem (↻ on hover/tap) or the whole sheet
("New problems") → **Print / Save PDF** (worksheet, answer key, or all versions at once).
Settings are remembered in the browser (localStorage) per unit.

## Folder layout
```
algebra1-linear-functions.html   thin page for one unit (loads scripts, names its unit in <body data-unit>)
core/
  rng.js        seeded random numbers (a worksheet is reproducible from its seed)
  frac.js       exact rational arithmetic (no floating point in the maths)
  tex.js        TeX builders for equations, points, fractions
  graph.js      accurate SVG coordinate planes + value tables
  framework.js  registry, retry/validate/dedupe loop, versions, regenerate-one, pinning
  render.js     worksheet + answer-key markup and measured pagination onto Letter pages
  app.js / app.css   the teacher UI and the print stylesheet
units/algebra1/linear-functions/
  common.js, lessons-*.js, index.js   the 21 generators and the unit/category list
vendor/   KaTeX and the two web fonts, bundled so nothing is fetched from a CDN
tests/    run-tests.js (maths), framework-tests.js, browser-test.js, ui-test.js, run-all.sh
```

## How problems are made (and why they are right)
Each skill is a deterministic template in `units/.../lessons-*.js`: it picks the **answer first** (slope, intercept,
points on the line) and builds the question backward. Anything invalid calls `gen.need(...)`, which rejects the
attempt and the framework retries (up to 600 times) — so a bad draw never reaches a worksheet. Duplicates and
near-duplicates are filtered per worksheet, across versions. There is no AI and no randomness outside the seeded RNG.
Math is exact fractions; text is KaTeX; graphs are SVG built from the same numbers as the equation.

## Adding a unit later (Geometry, Algebra 2, spiral review)
1. Copy `units/algebra1/linear-functions/` to `units/<course>/<unit>/`; write lessons with `NS.registerLesson({...})`
   and list them in `index.js` with `NS.registerUnit({...})` (categories → lesson ids).
2. Copy the HTML page, change `data-unit` and the unit `<script>` tags. `core/` is not touched.
3. A spiral review is just a unit-like page that loads several unit folders and builds its plan from lessons
   in `NS.registry.lessons` (`NS.generateOne(lessonId, opts)` and `NS.makeProblem` already work on any lesson).
   `NS.orderedLessons` / `NS.buildWorksheet` take a unit id; a spiral unit lists lessons from other units.

## Putting it on the website (nothing here touches your repository)
Your site lists activities in `data.js` and opens each from `artifacts/<name>/`. Suggested:
1. Copy this whole folder into the repo as `artifacts/worksheet-generator/` (keep the sub-folders together).
2. Optionally add a thumbnail `thumbs/worksheet-generator.jpg` (about 720 × 450).
3. In the **Algebra 1 → Linear Functions** unit in `data.js`, add:
```js
{
  title: "Worksheet Generator",
  path: "artifacts/worksheet-generator/algebra1-linear-functions.html",
  thumb: "thumbs/worksheet-generator.jpg",
  description: "Build custom Linear Functions worksheets with answer keys, versions A/B/C, and print-ready layout.",
  type: "Worksheet",
  level: ["CP", "Honors"],
  topics: ["Slope", "Graphing", "Writing Equations"],
  added: "2026-11-01"
}
```
(Match `type`/`level` spellings to the other entries.) The top-left link goes to `../../index.html`, the site home.
Nothing existing is renamed or overwritten, and the generator uses its own CSS namespace, so the site is unaffected.

## Printing tips
Choose **Letter**, **Margins: None**, and leave "Headers and footers" **off** (pages carry their own numbers).
Scale 100 %. "Save as PDF" in the print dialog produces the PDF.

## Tests
```
node tests/run-tests.js            # N=1000 default: 1,000 problems per skill (21,000), each re-derived independently
node tests/framework-tests.js      # determinism, versions, duplicates, regenerate-one, pinning
node tests/seed-stress.js           # thousands of random seeds/settings: generation must never fail
PW=.../playwright-core CHROME=.../chromium node tests/browser-test.js   # 1,170 sheets/keys through real pagination
PW=... CHROME=... node tests/ui-test.js                                  # teacher controls end to end
```
The maths tests do not share code with the generators (own fraction class, TeX/table/SVG readers): they read the
displayed question or the drawn graph back and recompute the answer.

## Known limits
- Integers-only + perpendicular lines: the given slope is shown as a unit fraction (e.g. −1/3 → answer 3) so the
  answer stays a whole number; other slopes would force a fractional answer.
- Layout is tuned and tested in Chromium (print → PDF). Firefox/Safari print engines were not tested.
- Page-fit uses real layout in the browser; a custom zoom or user font override in print settings can change it.
- Word-problem contexts (9 so far) and sub-type variety can be extended in `lessons-applications.js`.

## Menu Assessment Generator
`menu-assessment.html` builds customizable restaurant-style choice assessments (CP2/CP1/Honors, Versions A–C,
teacher keys with rubrics) on top of the same `core/` files. Pilot unit: Algebra 1 · Expressions & Equations.
See `menu/README.md` for the architecture, the independent answer checker and its tests.
