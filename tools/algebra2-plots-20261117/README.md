# Algebra 2 Graphing Practice and Stations (2026-11-17)

Algebra 2 audit items #10 and #14. Nothing here runs on the site.

`build.cjs` adds 24 plot items (8 per level) to each Algebra 2 unit that had no Graphing Practice:

| Unit | Items |
| --- | --- |
| linear-functions-systems | solve systems by graphing (skill 04, `system` tool); graph linear inequalities, some in standard form (skill 06, `region`) |
| conic-sections | circles: center and four points (skill 01, `points`); parabolas (x − h)² = 4p(y − k) or from vertex and focus (skill 02, `parabola`) |
| sequences-series | first four terms of arithmetic (skill 01) and geometric (skill 02) sequences as points (n, aₙ) |
| probability-statistics | histograms of simulated results (skill 09) and of measurement data (skill 07) |

Each target is checked against the site's grader (`worksheet-generator/core/plot.js`): the correct response passes and
every wrong response gets its feedback code. Answer keys are drawn by the site's own renderer (`MK_PLOT.blank`) with
the correct response and saved as PNG in `question-banks/assets/plot-keys/`. `scripts/test-algebra2-plot-items.cjs`
recomputes every target from the printed prompt alone. The four units are added to the Graphing Practice units map in `data.js`.

`add_stations.py` lists the bank-driven Stations Generator (`printables.html#unit=algebra2-<unit>&kind=stations`) for
the seven units that had no station set, with a thumbnail.

    PLAYWRIGHT=<path to playwright> CHROME=<path to chrome> node tools/algebra2-plots-20261117/build.cjs
    python3 tools/algebra2-plots-20261117/add_stations.py
    node scripts/build_standards_map.cjs
    node scripts/test-algebra2-plot-items.cjs

Both scripts skip what already exists. The site owner accepted these items as reviewed on 2026-11-18; their `sourceNotes` say "Teacher reviewed 2026-11-18". Report any problem found later through the usual question fixes.
