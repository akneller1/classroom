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
- Cache-busting `?v=` strings for verify.js and the three figure-bearing skill files bumped to `geo-sim-2`.

- Area, Surface Area & Volume: new `geo-plane` (rectangle, triangle, parallelogram, trapezoid with dashed heights and right-angle marks) and `geo-solid` (prism, cylinder, pyramid, cone, sphere) figures in `menu/geometry-measure-figures.js`, drawn from the true numbers; unknowns can be labelled `x`. 14 skills, all with figures (5 new: cone volume, sphere volume, sphere surface, prism height, cylinder height). Verifier rejects a figure that prints a number the question never states.

- Transformations: new `geo-grid` coordinate-plane figure (`menu/geometry-grid-figures.js`); the checker recomputes every drawn image vertex from its preimage. The 7 point skills now show P on a grid; 4 new triangle skills (translate-read-from-grid, reflect across a mirror line, rotate, dilate). The verifier recomputes the asked coordinate from the figure and the printed transformation (tamper-tested).

- Right Triangles & Trigonometry: new `geo-rt` figure (`menu/geometry-triangle-figures.js`), drawn to scale from the two legs; numeric side/angle labels are checked against the drawn triangle; used by Pythagorean, SOH-CAH-TOA, special-triangle, elevation/depression, inverse-trig and radical items (1,092 of 1,176 sampled items carry one).
- Similarity: new `geo-sim` (pair of similar triangles from sides, angles or SAS) and `geo-tri-par` (DE ∥ BC, refused unless AD/DB = AE/EC) in `menu/geometry-similar-figures.js`. The verifier requires every number the figure prints to appear in the question.
- Test: geometry-figures-tests now covers 3,678 generated figures across 12 figure kinds.

## Known issues found (not fixed)
- `triangles-congruence` "third angle" prompt prints its own equation ("Use x+74+64=180 to find x").
- `polygon-interior-sum` and `polygon-diagonal-count` use unrealistic sizes (up to 95 sides, 4,370 diagonals).
- Existing figures in `geometry-diagrams.js` (triangle pair, similar pair, right triangle, proof, landmark) are fixed schematics, not drawn from the question's numbers.
- Browser/print visual review done only via standalone galleries of the new figures, not inside the live pages.

## Next steps, in order
1. Push this work (needs GitHub linked) and confirm Actions are green; bump `?v=` strings.
2. (done) Circles figures.
3. (Area/SA/Volume figures done.) Still to do: composition of transformations, symmetry, nets, composite solids, cross-sections.
4. (Trig and Similarity done.) Still schematic: Triangle Relationships landmarks (midsegment, centroid, bisector, altitude) and Congruence pairs/proofs; Similarity word problems (shadows, scale, perimeter) have no figure.
5. Geometry Daily Lesson Planner scope and lesson-skills map.
6. Generate the four Geometry games per unit with `mkgames.py` (needs figure scripts in the template), retire hand-built duplicates only after parity.
7. Cheat sheets for Units 6–10; self-assessments review; live browser and print QA.

## Triangle Relationships and Congruence figures (latest)
- Unit 4 uses `geo-tri` (exact constructions: angles, exterior angle, isosceles ticks, midsegment, centroid, perpendicular bisector, altitude).
- Unit 3 uses `geo-cong` (geometry-congruence-figures.js). Tick groups, arcs and right marks are checked against the drawn coordinates; the SSS/SAS/ASA/AAS/HL/SSA/AAA criterion is derived from the marks alone (`F.cong.derive`). Proof diagrams (`shared`, `cross`) are marked "Not drawn to scale" and verified by `F.cong.proofKind`.
- CI fix: `geometry-generator-regression.cjs` asserted the retired schematic kinds (`geo-similar-pair`, `geo-right-triangle`, `geo-triangle-landmark`, `geo-triangle-pair`, `geo-proof`). It now requires the new data-driven kinds, runs each figure's own geometric check, checks print-safe colours, and keeps every tamper test. Nothing was weakened.

## Similarity word-problem figures
- `geo-shadow` (geometry-similar-figures.js): pole/tree shadows with parallel sun rays, drawn to scale; checker requires h/s = H/S. The verifier recomputes the tree height from the printed numbers (`geo-sim-shadow-*` branch), so changing any printed height or shadow is rejected.
- Scale-factor and perimeter skills now show similar triangles (`geo-sim`, marked "Not drawn to scale"); the perimeter prompt says "triangles" to match the picture.

## Transformations: two-step compositions
- New skill `compose-triangle-figure` (reflect over an axis, or rotate 90°, then translate). The figure shows the original, a dashed middle triangle, and the final triangle; the grid checker recomputes both images.
- The verifier (`geo-transform-fig-compose-*`) rebuilds the answer from the printed vertices and both printed steps and requires the drawn triangles to agree; tamper tests are in the regression file.

## Transformations: symmetry of regular polygons
- New skills `symmetry-lines-regular` and `symmetry-rotation-regular` use a plain `geo-regular` figure (`plain:true`: no exterior-angle mark, no side count in the alt text). The number of sides is never printed; students count it from the figure.
- The verifier reads n from the figure and checks the key (x = n for lines; n·x = 360 for rotation). A figure with a different n invalidates the key (regression test).

## Unit 10: nets, stacked solids, and answer-key hardening
- `geo-net` (cross net of a rectangular prism, drawn to scale) and `geo-stack` (two stacked prisms, oblique view); skills `measure-net-surface` and `measure-composite-volume`. The numbers appear only on the drawing, and the verifier derives the key from the figure.
- Hardening: all 16 Unit 10 skills now have an independent `geo-measure-*` verifier branch that recomputes the answer from the printed numbers or the drawing (previously cylinder, triangle and several others accepted a changed printed number). A tamper test covers every skill and tier.
- Symmetry skills got six prompt phrasings each so that 25 distinct questions exist at every tier (math-tests N=25 requires this).

## Geometry Daily Lesson Planner
- `lesson-planner.html` now has a Course selector (Algebra 1 / Geometry). `planner/course.js` picks the course from `#course=geometry` or a `#unit=geometry-…` link; Algebra 1 behaviour is unchanged.
- New data: `scope-geometry.js` (180-day draft scope, 10 units), `lesson-skills-geometry.js` (lesson→skill sets), `notes-data-geometry.js` and `notes-geometry.js` (vocabulary and key ideas). All are generated by `scripts/build_geometry_planner.py`; the JSON is `planner/geometry_scope_sequence.json`.
- Engine changes (shared): step math written with ⟨…⟩ is no longer double-wrapped; PowerPoint titles/file names use the course name (`Geometry-Day037-…`); inverse-trig prompt has nine lead-ins so the planner always finds distinct problems.
- Fixed: all five pages (worksheet, practice test, printables, assessment, planner) now load all ten Geometry skill files (several only loaded the first three, so later units were missing); cache tags bumped for verify.js and changed figure/skill files.
- Fixed: planner sidebar and section rows overflowed on phones (grid `minmax(0,1fr)`, wrapping rows).
- Tests (0 failures): planner-tests (143,152 checks, 26,982 problems, 180 days × 3 levels × 3 seeds), pptx-tests (180 decks), planner-browser (915 checks, all 180 days, phone width). The browser test now takes `COURSE=geometry`, and its stale selectors (`#plNoted`, `#plPptx`) were updated.
- Known, not mine: Algebra planner-tests (103) and Algebra browser "unverified problems" on 9 days exist on the base commit too.

## Geometry games, cheat sheets and listings
- Generated Showdown, Connect Four, Tic-Tac-Toe and Picture Reveal for all ten units (`games/mkgeometrygames.py`); hand-built pages are kept as `legacy.html`. Node bank test (119,990 checks) and the browser test (all four games × ten units, plus flashcards) pass.
- Cheat sheets: added Unit 4 Triangle Relationships and Unit 7 Quadrilaterals & Polygons, fixed the Congruence sheet's unit number (3), and built the PDFs for all ten (the PDFs for eight of them were missing from the repo: the thumbnails and content existed but the folders were empty).
- `data.js`: every Geometry unit now lists the readiness check, lesson planner, worksheet and assessment generators, cheat sheet, flashcards and the four games (`scripts/sync_geometry_listings.py`). Quadrilaterals & Polygons and Triangle Relationships previously listed only flashcards (plus tools for Unit 4).
- Thumbnails regenerated for all generated Geometry games.

## Geometry printables (print QA)
- The Printables page loads all Geometry skills; Maze and Tarsia need short problems with no diagram, which no Geometry skill has, so they are now shown as "not available for this unit" instead of an error (`supported()` in printables-ui.js, same capability test as the skill greying). Congruence (proof-based) offers Stations only.
- Diagrams in the small boxes (Color by Number, Error Analysis, Partner Check, Whodunnit) were rendered at full size and cut off the bottom of the box (the "Color:" line was clipped). CSS now sizes them (0.75 in tall, caption 6.5 pt); Color by Number skips Geometry items with prompts over 140 characters. All Geometry units × printables × levels × student/key pages now fit (printables-browser.cjs).
- `printables-browser.cjs` skips the Vocabulary Builder (its own builder) and switched-off combinations. Its later "unit page links the maze generator" assertion for Algebra was already failing before this work.
- `data.js` lists the available printables for each Geometry unit.

## Assessment Generator preview bug (all courses)
- `menu/app.js` line 569 called `$('input[name=mmLSpacing]').forEach(...)` (single-element helper), which threw "forEach is not a function" when the Preview step opened, so the Preview never showed pages for any course. Changed to `$$`. The menu browser test now runs through the PDF layout checks; it still stops at an Algebra-only "edited problem" assertion that was already failing.
- N=300 `math-tests.cjs` passed: 6,588,340 checks, 122,453 wrong keys caught.
- The eight hand-built Geometry escape rooms were re-solved stage by stage (all keys correct, 10 minutes and 30 s penalty defaults present); all 74 Geometry game pages load with no script errors.

## Open Response for every Geometry unit and clearer circle figures

User report: some circle skills showed "No verified problem" in Open Response sections, and chord/tangent labels were hard to read.

- Open Response needs four connected, verified parts. Only 6 Geometry skills made four parts, so Circles, Angles, Quadrilaterals, Transformations and Area/Volume had none and defaulted to red cards. Each of those units now has a four-part investigation skill (tag INVEST): `circle-open-response-investigation`, `angles-open-response-investigation`, `polygon-open-response-investigation`, `transformations-open-response-investigation`, `solids-open-response-investigation`, and Right Triangles gained `right-trig-investigation` (second four-part skill, so selections rotate). Audit: all 10 units × test/worksheet × 3 seeds with every section set to Open Response → 840 items, 0 failures.
- Verifier: `geometryDerived` re-derives these. The solids investigation recomputes every equation from the printed dimensions; the others require each equation number to be printed for students, a standard constant, or an earlier part's answer. Tamper test passes.
- The red-card message now says to pick a "Four-part" skill.
- Test change (not weakened): the Geometry choose-all test skips four-part skills, which are not choose-all items.
- Circle figures: circle radius 56→66, viewBox cropped to the drawing (labels render about 1.4× larger on phones), chord labels sit in separate wedges (one per half-chord), the tangent ray is longer so the x° label fits between ray and tangent.
- Pre-existing, unchanged: `right-inverse-trig-decimal` tier 1 has 24/25 distinct questions in the capacity audit.

## Diagrams for four-part and coordinate problems (user request: "diagrams and pictures when appropriate")

- New figure kinds in `menu/geometry-diagrams.js`: `geo-numline` (points placed in proportion, only given values printed), `geo-tri-chain` (midsegment DE, median AM, centroid G), `geo-cong-pair` (congruent triangles ABC/DEF with only the given labels). `geo-angle` gained `mid`, `equal`, and a drawn outer arc for the whole angle (the old figure printed the total as a floating number with no arc).
- Figures added: angle bisector, coordinate midpoint/distance/investigation (number line), congruent sides/angles/third angle/perimeter (triangle pair), and every four-part investigation that has a single picture (honors triangle chain, parallel lines, regular polygon, right triangle, prism, chords, coordinate grid).
- Adjacent-angle figure (complement/supplement/linear pair): labels now sit outside the arcs, so "68°" no longer sits on the right-angle mark.
- Chord and tangent labels, circle size and cropping: see the previous section.
- Verifier: the right-triangle investigation is re-derived from the printed hypotenuse and sin/cos ratios (a tampered ratio is rejected). Midpoint skill no longer produces B = A.
- Not drawn: the first (mixed-triangle) four-part triangle investigation, whose parts use different triangles.

## Accuracy audit of earlier (ChatGPT) work: triangles and similarity
- Triangle angle labels must sit inside the triangle with room to spare; narrow triangles fall back to an outside label.
- Similarity parallel-line figures are now schematic ("Not drawn to scale"); side lengths are kept within a 1.6 ratio so drawings stay readable.
- Outside angle labels get a short leader line to their vertex.
- Still to audit visually: right triangles, congruence criteria, angles/parallel lines, basics, transformations, area/volume.

## Accuracy audit continued: every unit's figures re-rendered and checked by eye
Checked: right triangles, congruence, angles/parallel lines, basics, transformations, area/volume, circles. Planner glossary/key ideas and skill reference sheets were read for mathematical errors (none found).
Fixes made:
- Straight-angle (supplementary / linear-pair) figures: the two angles now have separate arcs at different radii, instead of one arc that looked like it covered both.
- Parallel-lines figures: arcs at one vertex use different radii (no more merged circles) and labels sit clear of their arcs; this also fixes the four-part investigation figure.
- Bisector figure now draws the bisector in the true middle with matching double arcs; segment-addition shows a bracket for the total length.
- Coordinate-plane figures: vertex labels avoid each other, dots, axis numbers and the figure edge (coincident points such as C and C′ on the mirror line are now separated; no clipped "P(8, −1)").
- Trapezoid height label no longer crosses the slanted side; trapezoid bases are never equal; stack figure depth label sits outside its face.
- Semicircle problems use angle A between 22° and 68° so the triangle is large enough to label; circle angle labels clear their arcs.
- Outside angle labels in similar triangles get a leader line.

## Parity check against Algebra 1 (2026-10-28)
- All 161 Geometry catalog links load in a browser with no errors; no missing files or thumbnails remain.
- Added thumbnails for the 86 Geometry generator cards (Readiness, Planner, Worksheet, Assessment, printables); the Planner and Assessment ones say Geometry instead of Algebra.
- Added the missing Triangle Congruence Flashcards card (the page already existed).
- All ten Geometry cheat-sheet PDFs were read page by page; every example and formula is correct.
- Known gaps vs Algebra 1: no Maze or Tarsia; Triangle Congruence has only the Stations printable (its problems all need diagrams); Triangle Relationships and Quadrilaterals have no escape room or mystery game.

## Generator shortcuts and the last four games (2026-10-28)

- **"Coming soon" generator buttons fixed.** `generatorLinks()` in `app.js` had a hard-coded map that only enabled 2 of the 10 geometry units, and only for Worksheet and Assessment. It now reads the unit id from the unit's own generator links in `data.js`, so every unit shows working Lesson Plan, Worksheet, Activity and Assessment buttons. Checked in a browser for all 10 units and all 40 generator-page/unit combinations. Cache tag: `app.js?v=geo-generators-20261028`.
- **Four games added** (Geometry now has an escape room and a mystery in every unit):
  - `artifacts/triangle-relationships-escape-room/`: Starlight Observatory, word COMET, stamps 14/27/41/58/70.
  - `artifacts/quadrilaterals-polygons-escape-room/`: Lockdown at the Tile Factory, word TILES, stamps 11/24/39/52/67.
  - `artifacts/triangle-relationships-harbor-museum-caper/` and `artifacts/quadrilaterals-polygons-mosaic-gallery-heist/`: typed-answer detective games.
  - Both escape rooms use the shared engine with a 10 minute timer, 30 s wrong-answer penalty and the teacher key at `#key` behind code 205.
  - Built by `scripts/build_geometry_escape_rooms.py` and `scripts/build_geometry_mysteries.py` (figures from `scripts/geo_svg.py`). The mystery builder re-computes every answer and checks that exactly one suspect, place and method survive the clues.
  - All four were played through in Playwright (wrong answer rejected, cipher shift, final stamp order, key gate). Thumbnails in `thumbs/`, entries in `data.js` (cache tag `data.js?v=geo-games-20261028`).
- Still open: Triangle Congruence printables (need text-only skills), a figure for `cross-section`, print-to-PDF QA.

## Triangle Congruence printables (2026-10-28)

- Color by Number, Error Analysis, Partner Check and Whodunnit now work for Triangle Congruence. They were "Not available" because every congruence prompt was longer than the small boxes allow, even though the diagram already carries the marks.
- Fix: the engine passes `ctx.compact` (set by `printables.js` `makeItem` for every printable except Stations in Geometry units). Congruence skills return a `compactPrompt` (givens only, for example "Triangle ABC ≅ triangle DEF. AB = x + 12 and DE = 29. Find x.") and the `C()` wrapper swaps it in when `ctx.compact` is set. Worksheets, assessments, planner and games are unchanged. The verifier still sees the printed equation (third-angle prompt keeps it).
- Catalog: four Printable cards and four thumbnails added for the unit. Cache tags: `geo-compact-2` (congruence skill, printables.js, engine in printables.html), `data.js?v=geo-cong-print-20261028`.
- The Maze and Tarsia printables stay off for all Geometry units by design (problems need diagrams).

## Print QA and teacher-facing notes (2026-10-28)

- **"Not generated yet in this unit" notes rewritten.** The Geometry skill sets carried developer notes such as "Starter bank only" and "all diagrams remain pending" that were stale (cones, spheres, nets, cross-sections and diagrams all exist). Each unit now lists only what is truly not generated, in the same plain style as Algebra.
- **Circle equations print with superscripts.** The bank keeps `X^2` for the verifier; `render.js` prints `X²`/`(X-h)²` for `geo-circle-*` problems.
- **Print layout.** A Geometry figure problem may run to 240 characters before it takes a full row (was 150), and printed Geometry figures are capped at 2.3 in tall (`menu.css`). Checked by printing every Geometry worksheet through the real print path to PDF. The paginator leaves blank space at the bottom of some pages for Algebra worksheets too (same shared code), so it was left alone.
- Cache tags: `render.js?v=geo-layout-2`, `menu.css?v=geo-layout-2`, Geometry skill files `geo-gaps-1`/`geo-gaps-2` (circles).
- `printables-tests.cjs` stops at an Algebra vocabulary assertion ("Unknown printable vocabulary") on commits before this work as well; it is unrelated to Geometry.

## Rigor upgrade — Congruence of Triangles (2026-10-28)
Teacher feedback: Honors problems were too basic. Added four Honors-level (`best:[2]`, tag "Multi-step congruence investigations") four-part Open Response chains in `skills/geometry-triangles-congruence.js`:
- `congruence-investigation-algebra` — x from AB≅DE, y from BC≅EF (uses x), perimeter of ABC, z from ∠C≅∠F.
- `congruence-investigation-isosceles` — x from congruent halves of the vertex angle, ∠BAC, base angle, ∠ADB = 90 (SSS, CPCTC, angle sum, linear pair).
- `congruence-investigation-coordinate` — AB and BC lengths, AC² by the distance formula, x-coordinate of F that makes DEF congruent.
- `congruence-investigation-overlap` — overlapping triangles: x (AB = CD), y (alternate interior angles), z (CPCTC), ∠A by angle sum.
Verifier (`verify.js`): `congruence` added to the investigation rule; later parts may use earlier answers, including bare-number answers (needed by the game bank).
Test: `menu/tests/geometry-congruence-rigor-tests.cjs` re-solves 2,550 generated problems from their printed text (keys, triangle inequality, SSS for the coordinate F, honest figures). It caught a real bug: algebra-chain side lengths that could not form a triangle (fixed).
Next: the same rigor upgrade for the other nine Geometry units.

### Congruence rigor, part 2
- Added `congruence-investigation-kite` (kite with shared diagonal, SSS, two-sided equation for x, angle chase) and `congruence-investigation-hl` (right triangles by HL, two-sided hypotenuse equation, leg, CPCTC angle, complementary acute angles). Both Honors-only. Figures drawn from the printed angles.
- The one-step skills (corresponding sides/angles, third angle, perimeters, SSS/SAS/ASA/AAS/HL) are now `best:[0,1]` (CP2/CP1 tiers). The top tier draws identify, structured proofs and the six investigations.
- Rigor test now re-solves 3,150 problems. It found an infinite loop in the HL generator (a leg length that could not fit under a small hypotenuse); fixed.
- Not changed: fixed activities (escape rooms, mysteries) and printables (small boxes skip multi-part items).

## Rigor upgrade — Triangle Relationships (2026-10-28)
Four new Honors-only four-part investigations in `skills/geometry-triangle-relationships.js` (variants `geo-triangles-investigation-*`, shared investigation verifier extended with `triangles`; 3 and 90 are accepted constants there):
- `triangle-investigation-midsegment` — midsegment theorem with algebra (BC = 2 DE), midpoint of AB, perimeter of ABC, perimeter of the half-size triangle ADE.
- `triangle-investigation-exterior` — exterior angle theorem in an isosceles triangle (angles drawn to the printed values), angle B, linear pair, then a second isosceles perimeter equation.
- `triangle-investigation-coordinate` — midpoint formula, median length, centroid (one third up from M) on the coordinate plane.
- `triangle-investigation-bisector` — perpendicular bisector theorem with algebra, midpoint, perimeter of triangle PAB.
The nine one-step skills are now `best:[0,1]`. Test: `menu/tests/geometry-triangle-rigor-tests.cjs` re-solves 2,100 problems from printed text at all seven difficulties. It also caught an exterior-angle generator that silently fell back to a bad value at low difficulty (constant-term range too tight; widened).

## Rigor upgrade — Similarity (2026-10-28)
Four new Honors-only four-part investigations in `skills/geometry-similarity.js` (variants `geo-similarity-investigation-*`; verifier regex extended with `similarity`):
- `similarity-investigation-ratio` — similar triangles with a given ratio (e.g. 3 to 2), algebraic sides, missing side, perimeter of the larger triangle.
- `similarity-investigation-parallel` — triangle proportionality with algebraic segments, AB, BC from similar triangles ADE/ABC, perimeter.
- `similarity-investigation-dilation` — dilation about the origin: image coordinates, image length, image area.
- `similarity-investigation-altitude` — altitude to the hypotenuse: geometric mean with algebra, hypotenuse, leg squared, area.
One-step similarity skills are now `best:[0,1]` (SAS/SSS criteria `[1]`). Figures use `geo-cong` (expression labels are not allowed by `geo-sim`/`geo-tri-par`). Test: `menu/tests/geometry-similarity-rigor-tests.cjs` re-solves 1,680 problems from printed text at all seven difficulties.
Note: in the shared verifier, later parts must use earlier answers as numbers, not variable names.

## Rigor upgrade — Right Triangles and Trigonometry (2026-10-28)
Four new Honors-only four-part investigations in `skills/geometry-right-triangles-trigonometry.js` (variants `geo-rtchain-investigation-*`):
- `right-investigation-pyth` — two right triangles sharing a hypotenuse (65, 85 or 125 families, no needle-thin triangles): hypotenuse, other leg, algebraic leg for x, area.
- `right-investigation-special` — 30-60-90 triangle with algebraic short leg and hypotenuse, long leg squared.
- `right-investigation-converse` — Pythagorean theorem with an algebraic hypotenuse, sum of squares, perimeter.
- `right-investigation-coordinate` — right triangle on the plane, hypotenuse, median to the hypotenuse.
Verifier: `verify.js` now checks one-unknown square equations (e.g. `w^2=225`) for rtchain variants by re-deriving the positive whole-number root; every number in the equation must still be printed or an earlier answer. `checkSteps` skips the linear step comparison for those variants.
Eight one-step skills (Pythagorean, distance, sine/cosine/tangent, 45-45-90, 30-60-90) are now `best:[0,1]`.
Test: `menu/tests/geometry-righttriangle-rigor-tests.cjs` re-solves 1,120 problems from printed text and checks that 336 tampered answers are rejected.

## Rigor upgrade — Quadrilaterals and Polygons (2026-10-29)
Four new Honors-only four-part investigations in `skills/geometry-quadrilaterals-polygons.js` (variants `geo-polygons-investigation-{parallelogram,rhombus,trapezoid,polygon}-<c>`):
- parallelogram: opposite sides with algebra, consecutive angles, opposite angle, perimeter (figure drawn at the true angle).
- rhombus: diagonals bisect each other, perpendicular diagonals, side by the Pythagorean theorem, perimeter.
- isosceles trapezoid: midsegment with algebra, longer base, congruent base angles, supplementary angle.
- polygon: angle sum of a convex quadrilateral with algebraic angles, regular-polygon interior angle, algebra on it, diagonal count.
Verifier: those four variants get the digits-in-math rule and constants 3, 4, 90; the rhombus chain uses the existing square-root solve rule (as in `geo-rtchain-`). One-step skills (interior sum, opposite sides/angles, exterior, rectangle/rhombus diagonals, midsegment, consecutive angles, diagonal count, quadrilateral angle sum) are now `best:[0,1]`; algebraic consecutive angles, diagonal-bisection converse and classify remain available to Honors. Test: `menu/tests/geometry-polygon-rigor-tests.cjs` (1,680 problems; it caught non-convex quadrilateral angles, fixed).
Right Triangles and Trigonometry already had Honors chains (`right-investigation-*`), so no new work there.

## Rigor upgrade — Foundations of Geometry (2026-10-29)
Four new Honors-only four-part investigations in `skills/geometry-basics-reasoning.js` (variants `geo-basics-investigation-{segment,angle,coordinate,lines}-<c>`; the shared verifier regex, digits-in-math rule, constants 3/4/90 and the square-root solve rule were extended for them):
- segment addition and midpoints with algebraic lengths;
- angle addition and an angle bisector with algebraic measures (figure drawn from the printed angles);
- missing endpoint from a midpoint, then the distance formula (3-4-5 family so lengths are whole numbers; grid figure of A and M);
- linear pair, vertical angle and bisector at intersecting lines.
The six one-step skills are `best:[0,1]`; the older `coordinate-investigation` stays Honors. Test: `menu/tests/geometry-basics-rigor-tests.cjs` (1,680 problems). The capacity audit caught too few distinct "lines" problems and the diagrams test caught a figure outside the grid; both fixed.

## Question-format greying (2026-10-29)
Teacher request: when a question format (e.g. Choose all that apply) cannot be asked for a skill or section, grey it out instead of adding problems that show "No verified problem". `NS.skillFormatOk` and `NS.formatAvailable` (engine.js) sample the existing capability checks (`multiCapable`, `mcCapable`, `mcasCapable`). In the menu UI (app.js, shared with Algebra): the part's format dropdown disables a format when none of the part's selected skills can do it ("not available here"); the per-problem skill dropdown and the "Add a problem" dropdown disable skills that cannot be asked in the part's format, and "Add a problem" defaults to the first available skill. Congruence has no select-all-capable skills, so that option is greyed there.

## Angles and Parallel Lines rigor (update-14)
- Three Honors four-part chains (`angles-investigation-corresponding|alternate|relations`): algebraic expressions on a labelled transversal figure (or no figure for complementary/supplementary/vertical), each part reuses earlier answers as numbers.
- One-step angle skills now `best:[0,1]`; Honors gets the chains. Verifier rules extended for the new variants.
- Independent test: `menu/tests/geometry-angles-rigor-tests.cjs` (1260 problems re-derived from printed text).
- Cache tags: angles file `geo-rigor-1`, verify.js `geo-v-12`.

## Transformations rigor (update-15)
- Four Honors four-part chains: mirror line found from a point and its image; dilation about a center that is not the origin (scale factor, image, length, area); rotation + translation worked forwards and backwards; regular-polygon symmetry with angle sums.
- One-step transformation skills now `best:[0,1]`. Gap note updated (non-origin dilations now generated).
- Independent test: `menu/tests/geometry-transformations-rigor-tests.cjs` (1680 problems). Cache tag `geo-rigor-1`.

## Circles rigor (update-16)
- Four Honors four-part chains: inscribed angle/arc expressions with major arc and tangent-chord angle; intersecting chords reused as a tangent with tangent-secant and second secant; expanded circle equation (center, radius via square root, area); arc length and sector area from an angle written as an expression.
- One-step circle skills now `best:[0,1]`. Verifier: square-root rule extended to `geo-circles-investigation-coordinate-`, digits rule extended to the new variants (`geo-v-13`).
- Independent test: `menu/tests/geometry-circles-rigor-tests.cjs` (1680 problems). Cache tag `geo-rigor-1`.

## Area, Surface Area and Volume rigor (update-17)
- Four Honors four-part chains (`measure-investigation-prism|cylinder|sphere|trapezoid`, variants `geo-measure-investigation-*`): prism with an algebraic length, surface area and scaling by a factor; cylinder from its volume (square-root step), lateral/total surface area and a cone; sphere from surface area, great-circle circumference or area (three givens), larger sphere, hemisphere, circumscribed cylinder; trapezoid with an algebraic base, triangle, difference and a similar copy.
- One-step measure skills now `best:[0,1]`. Verifier: part (a) of each chain is re-derived from the printed givens; square-root and step rules extended (`geo-v-14`).
- Independent test: `menu/tests/geometry-measure-rigor-tests.cjs` (1680 problems). Cache tag `geo-rigor-1`.
- All ten Geometry units now have Honors rigor chains; the remaining optional items are presets, fixed activities (escape rooms, mysteries) and printables not yet using the chains.

## Preset greying (update-18)
- `NS.presetAvailable(cfg, kind, preset)` in engine.js; "Start from" buttons (tests and worksheets) are disabled when a part the preset creates could not be asked in its format for the selected skills. Cache tag `preset-grey-1`.
