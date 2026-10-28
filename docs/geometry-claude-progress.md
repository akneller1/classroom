# Geometry completion — progress (Claude session, 2026-10-28)

Resume from this file. Everything below was verified in this session unless marked **unverified**.

## Baseline (before changes, from a fresh clone of `main`)
All Geometry CI scripts pass locally: diagrams, curriculum, model, config-parity, reasoning-prompts (480), plausibility (1600), select-all, mcas-context, math audit (N=25). Capacity audit: 3 of 212 skill/tier settings below 25 (inverse-trig, tiers 1 and 5). `scripts/check_library.py` reports 2 problems (identical titles "assessment readiness check" for Algebra and Geometry practice-test links); they pre-date this work.
GitHub Actions status was **not observable** from this session (GitHub not linked); nothing here has run in CI.

## Parity matrix (Algebra 1 reference vs Geometry)
| Capability | Geometry status |
|---|---|
| Assessment / Worksheet generators | Shared engine and config; 10 units, ~110 skills. Parity of settings proven by `geometry-config-parity-tests`. |
| Practice test, printables, vocabulary | Pages exist; use shared code. Visual/print review **not done**. |
| Daily Lesson Planner | **Missing.** `planner/scope-*.js` and `lesson-skills.js` hold Algebra 1 only. Geometry cards link `lesson-planner.html#unit=geometry-…`, which has no Geometry scope. Needs a Geometry scope & sequence and lesson→skill map (`planner/tests/planner-tests.cjs` enforces completeness). |
| Games (Showdown, Connect 4, Tic-Tac-Toe, Picture Reveal) | **Not parity.** Algebra 1 uses generated games from `games/mkgames.py` with the shared bank. Geometry games are older hand-built pages (e.g. `artifacts/angles-parallel-lines-jeopardy`). Only Geometry **flashcards** are generated. Escape rooms / mysteries are hand-built for both. |
| Flashcards | Generated, shared infrastructure; figure script now loaded (see below). |
| Cheat sheets | PDFs exist for Units 1–5 only (`Geometry_0x_*.pdf` in repo root); `scripts/cheat-sheets/` has a build system with `geo.cjs`. Units 6–10 missing. |
| Self-assessments | Not inspected. |
| Diagrams | Was 32% of generated items (816/2544), five units at zero. See below. |

## Done this session (uncommitted to GitHub; local commit only)
- New `worksheet-generator/menu/geometry-figures.js`: data-driven SVG figures sharing one source of truth with the answer key. Kinds: `geo-transversal`, `geo-adjacent`, `geo-cross`, `geo-quad` (parallelogram, rectangle, rhombus, square, trapezoid with midsegment, kite, general quadrilateral from four angles), `geo-regular`, `geo-circle` (central/inscribed/intercepted arcs, tangent, diameter, semicircle, chords, secants, tangent-secant, arc length, sector area, chord distance). Print-safe (black/white), obstacle-aware label placement, "not to scale" note only when a figure is clamped or schematic.
- Every figure is validated: tick marks, angle arcs, right-angle marks and parallel marks must be true of the drawn shape; angle sums must hold. Invalid figures render nothing and make `verifyProblem` fail the item.
- `verify.js`: figure consistency check; transversal equation is rebuilt from the figure's marked positions (equal vs supplementary), and must agree with any printed givens.
- Angles & Parallel Lines: all 8 skills now carry figures (was 0). Honors (tiers 5–7) transversal items give the angles only in the figure and do not name the relationship.
- Quadrilaterals & Polygons: 11 of 13 skills carry figures (was 0). `polygon-interior-sum` and `polygon-diagonal-count` stay text-only (up to 95 sides). Angle-sum items now keep angles in 40–150° so the figure is drawable.
- Script tag added after `geometry-diagrams.js` in 5 worksheet-generator pages and 10 flashcard pages; test loader updated.
- New `menu/tests/geometry-figures-tests.cjs` (894 generated figures checked against their answers; negative cases) added to `menu-generator-tests.yml`.
- Local results after changes: all scripts above pass; math audit PASS (528,310 checks).

- Circles: 22 generator variants now carry figures (3 equation-of-circle variants stay text-only). 624 circle figures checked, including that numeric angle/arc labels equal the drawn angles.
- Cache-busting `?v=` strings for verify.js and the three figure-bearing skill files bumped to `geo-figures-2`.

## Known issues found (not fixed)
- `triangles-congruence` "third angle" prompt prints its own equation ("Use x+74+64=180 to find x").
- `polygon-interior-sum` and `polygon-diagonal-count` use unrealistic sizes (up to 95 sides, 4,370 diagonals).
- Existing figures in `geometry-diagrams.js` (triangle pair, similar pair, right triangle, proof, landmark) are fixed schematics, not drawn from the question's numbers.
- Browser/print visual review done only via standalone galleries of the new figures, not inside the live pages.

## Next steps, in order
1. Push this work (needs GitHub linked) and confirm Actions are green; bump `?v=` strings.
2. (done) Circles figures.
3. Transformations and Area/Surface Area/Volume figures (coordinate plane with image/preimage; prisms, cylinders, cones, spheres, nets).
4. Replace schematic triangle/similarity/trig figures with data-driven ones; finish Triangle Relationships/Congruence correspondence marks.
5. Geometry Daily Lesson Planner scope and lesson-skills map.
6. Generate the four Geometry games per unit with `mkgames.py` (needs figure scripts in the template), retire hand-built duplicates only after parity.
7. Cheat sheets for Units 6–10; self-assessments review; live browser and print QA.
