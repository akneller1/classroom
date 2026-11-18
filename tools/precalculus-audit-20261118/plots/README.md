# Precalculus Graphing Practice (2026-11-18)

Precalculus audit item #8. Nothing here runs on the site.

`build.cjs` (adapted from `tools/algebra2-plots-20261117/build.cjs`) adds 24 plot items, 8 per level, to each of four
units that had no Graphing Practice:

| Unit | Items |
| --- | --- |
| equations-inequalities | solve systems by graphing (skill 08, `system`); graph linear inequalities (skill 07, `region`) |
| conics | circles: center and four points (skill 01, `points`); parabolas from the equation or vertex and focus (skill 02, `parabola`) |
| sequences-series-limits | first four terms of arithmetic and geometric sequences as points (n, aₙ) (skill 01) |
| vectors | polar points converted and plotted (skill 09); z, z̄, −z and iz in the complex plane (skill 12) |

Each target is checked against the site's grader (`worksheet-generator/core/plot.js`); answer keys are drawn by the
site's renderer and saved in `question-banks/assets/plot-keys/`. `scripts/test-precalculus-plot-items.cjs` recomputes
every target from the printed prompt alone. The units are added to the Graphing Practice units map in `data.js`.

    PLAYWRIGHT=<path to playwright> CHROME=<path to chrome> node tools/precalculus-audit-20261118/plots/build.cjs
    node scripts/test-precalculus-plot-items.cjs
