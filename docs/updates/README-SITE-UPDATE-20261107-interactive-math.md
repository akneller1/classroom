# Site update 2026-11-07: Interactive Math for 6th Grade, Pre-Algebra, Precalculus and Calculus

**Baseline:** commit `9a1312775149e62edfa67646aaadb0b4d9702269` (from the comment of the uploaded `classroom-main.zip`). The ZIP contains only new and changed files, at their repository paths. Nothing has been committed, pushed or deployed.

## Contents
- 14 new Interactive Math tools: 4 for 6th Grade, 3 for Pre-Algebra (7th), 2 for Pre-Algebra (8th), 1 for Precalculus and 4 for Calculus. Each comes with a 2-page Explore & Reflect worksheet, a 2-page teacher key and a thumbnail.
- A review of the 32 existing tools. 9 were improved (4 had math or logic errors), 23 kept unchanged, none removed.
- Existing tools listed in more courses where the objective and scaffolding fit (9 cards).
- A fix for **Copy student link** on every Interactive Math card. It opened the games' skill picker, which never produced a link for a tool.

## Install
1. The update has 112 files, so it comes in two parts to stay under GitHub's 100-file web-upload limit:
   - **Part 1** (`classroom-update-interactive-math-20261107-part1-site.zip`) holds everything the website uses: tools, PDFs, thumbnails, shared files and this README.
   - **Part 2** (`...-part2-sources.zip`) holds only the build sources and tests under `tools/`; the site works without it.
   
   Unzip each one, then drag its folders onto GitHub with "Add files via upload", keeping the folder structure. Upload Part 1 first.
2. **Nothing needs to be deleted.** No tool was removed and no file is obsolete (the deletion manifest is empty).
3. If `data.js`, `guide.html`, `index.html`, `activity.html` or `student-game-share.js` changed on `main` after the baseline, merge them by hand. The merge notes below show exactly what changed.

## Merge notes for the changed shared files
Each change is self-contained, so apply it to the current version of the file. Don't replace a newer file with the one in the ZIP.

| File | Exact change |
| --- | --- |
| `data.js` | **Append only.** It adds one block at the very end, starting with the comment `/* Interactive Math 2026-11-07: ...`. The block is an IIFE with an `ITEMS` array of 23 `{course, unit, a}` entries, using the same pattern as the two Interactive Math blocks above it. Nothing above it changed. To merge, copy that block onto the end of the current `data.js`. Each entry is skipped automatically if its unit is missing or already lists that path. |
| `student-game-share.js` | A new helper `isInteractiveMath(path)`, plus one line at the top of `supports(path)`: `if (isInteractiveMath(path)) return false;`. Interactive Math tools (catalog `bankFormat: "interactive-math"`) now get the plain `?student=1` link from cards and from the activity viewer. Games keep the skill picker. |
| `guide.html` | In the **Interactive Math** section: the coverage sentence becomes a course-by-course table (wrapped in `<div class="table">`). It adds a bullet about teacher notes and the "What should I notice?" panel, plus a paragraph about the new five-part worksheet sequence. Nothing else changed. |
| `index.html`, `activity.html` | Cache strings only: `data.js?v=interactive-math-20261107` and `student-game-share.js?v=interactive-math-20261107`. |
| `artifacts/interactive-math/lab-plus.js` | **New** shared file, loaded only by the 14 new tools. `lab.js` and `lab.css` are unchanged. |

## The new tools

| Course | Unit (id) | Tool | Central relationship students discover |
| --- | --- | --- | --- |
| 6th Grade Math | ratios-rates-percent-proportions | Double Number Line Ratio Explorer | Equivalent ratios come from multiplying both amounts by the same number. The unit rate stays constant, and equivalent pairs lie on a line through (0, 0). Adding the same amount to both parts breaks the ratio. |
| 6th Grade Math | fractions-decimals-operations | Fraction Division: How Many Groups? | a ÷ d counts groups of size d. A leftover is a fraction of a group, not of the whole. Cutting both into equal pieces gives a ÷ (n/m) = a × (m/n). |
| 6th Grade Math | geometry | Parallelogram & Triangle Area Lab | Shearing keeps the base and height, so the area stays the same. Cut-and-slide turns a parallelogram into a rectangle, and a triangle is half a parallelogram. The slanted side is irrelevant. |
| 6th Grade Math | data-displays | Dot Plot Balance: Mean, Median & Spread | The mean is the balance point (distances below = distances above). The median depends only on order, and outliers pull the mean. MAD is the typical distance from the mean. |
| Pre-Algebra (7th) | linear-functions-graphing | Proportional Relationship Explorer | Proportional means y/x is constant, the graph passes through (0, 0) and the equation is y = kx. A straight line with a starting fee is not proportional. |
| Pre-Algebra (7th) | ratios-proportions-percentages | Percent Change Bar Model | A percent change multiplies by (100% ± p%) of the starting amount. In a chain the base changes, so changes multiply rather than add (+20% then −20% ≠ 0%). |
| Pre-Algebra (7th) | data-analysis-probability | Spinner Probability Lab | Theoretical probability is parts ÷ total parts. Small samples vary widely and large samples settle near the theoretical probability. Expected count = P × n, and spins have no memory. |
| Pre-Algebra (8th), also 7th right-triangles-algebra | geometry-applications | Pythagorean Squares Explorer | Squares on the sides of lattice triangles: a² + b² = c² exactly for right triangles. The converse classifies triangles as acute or obtuse, and a tilted square's area can be found without measuring its side. |
| Pre-Algebra (8th) | real-numbers-exponents | Square Roots on the Number Line | √A is a side length. Squaring neighbors traps it one place value at a time. Non-perfect squares are irrational, so decimals are approximations, and zooming is not a proof. |
| Precalculus | vectors | Vector Explorer | Vectors add component-wise (tip to tail). \|u + v\| ≤ \|u\| + \|v\|, with equality only when u and v point the same way. k·u scales length by \|k\| and reverses direction when k < 0. u − v runs from the tip of v to the tip of u. |
| Calculus | limits-continuity | Limit Explorer | The limit describes values near a, not at a. Both one-sided limits must agree, and f(a) can differ or be undefined. Tables and zooming are evidence, not proof (oscillation case). |
| Calculus | derivatives | Secant to Tangent | Secant slopes approach the tangent slope as h → 0 from both sides. A corner (\|x\|) has no derivative, and the traced tangent slopes form the graph of f′. |
| Calculus | antiderivatives-definite-integrals | Riemann Sum Lab | Sums approach the exact integral as n grows. Area below the axis counts negative (signed vs. total area), and increasing vs. decreasing f decides whether a sum over- or underestimates. |
| Calculus | fundamental-theorem-calculus | Accumulation Function Explorer | A(x) = ∫ₐˣ f increases where f > 0, and A′(x) = f(x). Extrema of A occur where f changes sign, and changing a shifts A by a constant. |

Every new tool includes:
- an opening state where no challenge is already done;
- linked representations (model, table, graph, equation or verbal);
- live readouts;
- 5–6 "Try this" challenges that progress from establishing the idea to confronting a misconception or transferring it (predict, construct, counterexample, explain);
- a Reset button;
- live feedback;
- a closed **"What should I notice?"** panel;
- draggable objects that also work with the arrow keys;
- −/+ step buttons on every slider, and number boxes where values are typed.

## Why these tools (priority review)

| Course | Existing unit | Proposed tool | Concept revealed | Priority and reason |
| --- | --- | --- | --- | --- |
| Calculus | derivatives | Secant to Tangent | Derivative as limit of secant slopes; f′ graph | **Built, highest.** This is the defining limit, and only a moving picture shows it. The corner case exposes "continuous ⇒ differentiable". |
| Calculus | antiderivatives-definite-integrals | Riemann Sum Lab | Sums → integral; signed area | **Built, highest.** Signed vs. total area is a top AP misconception, and changing n and the method is meaningful. |
| Calculus | limits-continuity | Limit Explorer | Limit vs. value; one-sided limits | **Built, highest.** It directly targets "limit = f(a)" and "zooming proves it". |
| Calculus | fundamental-theorem-calculus | Accumulation Function Explorer | A′ = f | **Built, high.** It links two graphs dynamically, which is hard to show statically. |
| 6th | ratios-rates-percent-proportions | Double number line | Multiplicative structure, unit rate | **Built, highest.** It addresses additive reasoning with linked line, table and graph. |
| 6th | fractions-decimals-operations | Fraction division groups | Measurement division, remainder in groups | **Built, highest.** The remainder misconception (2½ vs 2⅔) shows up clearly in the bars. |
| 6th | data-displays | Dot plot balance | Mean as balance point; outliers; MAD | **Built, high.** Dragging values reveals how mean and median respond differently. |
| 6th | geometry | Area shear lab | Base × height invariance | **Built, high.** It addresses the "base × slanted side" misconception, and the triangle copy explains the ½. |
| 7th | ratios-proportions-percentages | Percent change bars | Successive percents multiply | **Built, highest.** The +20%/−20% misconception is visible on one dollar scale. |
| 7th | linear-functions-graphing | Proportional explorer | y = kx vs. y = kx + b | **Built, high.** It addresses "any line is proportional". |
| 7th | data-analysis-probability | Spinner lab | Theoretical vs. experimental | **Built, high.** It is distinct from the Algebra 2 lab: unequal custom spinners, expected counts and gambler's fallacy. The Algebra 2 lab's normal-curve tab doesn't fit 7th grade. |
| 8th (+7th) | geometry-applications / right-triangles-algebra | Pythagorean squares | a² + b² = c² and converse | **Built, highest.** Exact lattice squares make the area relationship concrete, and the tilted-square trick avoids circular reasoning. |
| 8th | real-numbers-exponents | Square roots zoom | Trapping roots; irrationality | **Built, high.** It connects area, root and number line, and addresses √A = A/2. |
| Precalculus | vectors | Vector explorer | Component addition; magnitudes don't add | **Built, high.** Dragging tips makes the triangle inequality and u − v geometric. |
| Precalculus | trigonometric-functions | Radians and arc length | Radian = arc / radius | **Extended the existing Unit Circle tool** (new "What is a radian?" tab) instead of duplicating it. |
| Precalculus | trigonometric-functions | Trig transformation explorer | Amplitude, period, shifts | **Not built.** The existing Unit Circle tool's "Transform the wave" tab already does this. |
| 8th | congruence-similarity; linear-functional-relationships; systems-linear-equations | Transformations, slope, systems | Same objectives as Algebra 1 / Geometry tools | **Reused** Transformation Studio, Slope-Intercept Explorer and Systems Explorer. Objective and scaffolding fit, so no new build was needed. |
| Precalculus | functions; conics; equations-inequalities; probability | Transformations, rational functions, conics, linear programming, distributions | Algebra 2 tools match these skills | **Reused** Transformation Lab, Asymptote & Hole Explorer, Conic Explorer, Feasible Region Optimizer and Probability Simulation Lab. |
| 8th | patterns-bivariate-data | Line of Best Fit Lab | Lines of fit, residuals | **Not reused.** Its challenges and worksheet center on the correlation coefficient r, which is beyond 8th-grade scaffolding. It's a good candidate for an 8th-grade version later. |
| Calculus | differential-equations | Slope field explorer | Local slopes and solution curves | **Deferred.** Valuable, but it would take the collection past the target size. It's next in line. |
| 6th | rational-numbers | Signed-number movement | Moves on a number line | **Not built.** Lower added value than the four 6th-grade tools above. |
| Precalculus | — | Polar coordinates | — | **Not built.** There is no polar unit (polar appears only as one skill in vectors). |
| 7th | ratios-proportions-percentages | Scale drawings | Scale factor | **Not built.** It's covered conceptually by the ratio and dilation tools. |

## Review of the existing tools (all 32) and the final decisions

All 32 were smoke-tested on a Chromebook-size screen (light) and a phone-size screen (dark), and none had script errors or sideways overflow. The challenge logic and math of every source file were read.

| Tool (course) | Decision | Reason |
| --- | --- | --- |
| Asymptote & Hole Explorer (A2; now also Precalc) | **Improved** | Math errors. (x−2)/(x−2)² was reported as both a hole and an asymptote, and could satisfy the "make a hole" challenge. A hole could also be listed as an x-intercept. A cancelled factor still in the denominator is now an asymptote, and holes are never x-intercepts. |
| Zeros & Multiplicity Builder (A2) | **Improved** | Logic error. Two zeros at the same x were treated as separate "crossing" zeros. They now combine multiplicities (bounce at even multiplicity, flatten at odd ≥ 3). |
| Dilation & Similarity Lab (Geo) | **Improved** | Math error. The readout showed (x, y) → (kx, ky) for any center; it now shows (a + k(x − a), b + k(y − b)). Two slider-only challenges were replaced: make a reduction inside the original, and make the image not overlap at all. |
| Exponential & Log Mirror (A2) | **Improved** | The "graphs just touch y = x" challenge accepted bases 1.4–1.5. No slider base touches the line (the touching base is e^(1/e) ≈ 1.4447), and 1.5 misses it entirely. Students now find the two neighboring slider bases that bracket the change. |
| Discriminant & Roots Explorer (A2) | **Improved** | Challenge 1 was already done when the page opened. It's now "two real roots with c > 0". |
| Area Model Multiplier (A1) | **Improved** | Challenge 1 was already done when the page opened (the opening state was (x + 2)(x + 3)). It now opens at (x + 1)(x + 4). |
| Probability Simulation Lab (A2; now also Precalc) | **Improved** | Two counting challenges ("flip 1,000", "roll 500") and a click-the-chip challenge were replaced. The new ones are: a 10-flip run that misses by 0.2 (small-sample variability), the share of 7s within 0.01 of 6/36, and the 2σ area for two different σ. |
| Solids Volume Lab (Geo) | **Improved** | "Set the scale factor to 2" became "find the scale factor that makes the volume 27 times as big". |
| Unit Circle to Sine Wave (A2, Precalc, Calc) | **Improved** | Added a "What is a radian?" tab: arc length s = rθ, ticks every 1 radian, and θ unchanged when r changes. Two slider-to-value challenges were replaced with the radian challenges and a two-condition wave construction. |
| Algebra Tiles Lab (A1) | Kept | It models zero pairs and distribution faithfully, and its challenges construct rather than set values. |
| Equation Balance Scale (A1) | Kept | It's a strong model of "same operation on both sides", including no-solution and identity cases. |
| Inequality Number Line (A1) | Kept | Its "why the symbol flips" tab is a distinct, accurate discovery. |
| Function Detector (A1) | Kept | It links the vertical line test to mapping diagrams, with correct domains and ranges. |
| Slope-Intercept Explorer (A1; now also 8th) | Kept | Accurate, with good linked table and slope triangle. |
| Systems Explorer (A1; now also 8th) | Kept | It handles parallel and coincident lines correctly. |
| Exponent Rules Unpacker (A1) | Kept | The factor-chip model explains each rule and the zero/negative pattern. |
| Linear vs. Exponential Race (A1) | Kept | It shows constant difference vs. constant ratio in the table. |
| Factor Rectangle Builder (A1) | Kept | It links factoring, area and zeros, and correctly detects trinomials that don't factor. |
| Parabola Explorer (A1) | Kept | Accurate in both vertex and standard form, including a = 0. |
| Line of Best Fit Lab (A1) | Kept | It covers squared error, residuals and outliers accurately (it isn't reused in 8th grade; see the priority table). |
| Transformation Lab (A2; now also Precalc) | Kept | The same rules work across six parent functions. |
| Feasible Region Optimizer (A2; now also Precalc) | Kept | Its vertex and tie logic is correct. |
| Sequence Builder (A2) | Kept | Its convergence logic is correct, including r = ±1. |
| Conic Explorer (A2; now also Precalc) | Kept | Accurate foci, directrix and asymptotes. |
| Distance & Midpoint Explorer (Geo) | Kept | It builds the distance formula from a right triangle. |
| Parallel Lines & Transversal (Geo) | Kept | Its "tilt one line" check is a strong counterexample. |
| Triangle Congruence Builder (Geo) | Kept | It correctly shows SSA as giving 0, 1 or 2 triangles and AAA as giving many. |
| Triangle Explorer (Geo) | Kept | Accurate centers and triangle inequality. |
| Trig Ratio Explorer (Geo) | Kept | It shows the ratios depend on the angle only. |
| Polygon & Quadrilateral Explorer (Geo) | Kept | Accurate angle sums and quadrilateral classification. |
| Transformation Studio (Geo; now also 8th) | Kept | Its coordinate rules and rigid/orientation properties are correct, and it fits 8th-grade standards. |
| Circle Angle Explorer (Geo) | Kept | Inscribed/central angle and arc/sector relationships are correct. |
| Removed | — | **None.** No tool was repetitive or decorative enough to remove. The weaknesses found were fixable with focused revisions. |

The existing worksheets and keys for the revised tools were rechecked against the fixes. They don't reference the changed challenges, and their answers are correct, so they were not reprinted. The other 23 tool pages rebuild byte-for-byte identical from `tools/interactive-math-20261105`.

**New tools (14): all added.** See the evaluation at the end.

## Changed and new files
- **Changed (shared):** `data.js`, `student-game-share.js`, `guide.html`, `index.html`, `activity.html`.
- **Changed (revised tool pages and their sources):**
  - `artifacts/{algebra2-asymptote-hole-explorer, algebra2-discriminant-roots-explorer, algebra2-exponential-log-mirror, algebra2-probability-simulation-lab, algebra2-unit-circle-sine-wave, algebra2-zeros-multiplicity-builder, geometry-dilation-similarity-lab, geometry-solids-volume-lab, polynomials-factoring-area-model-multiplier}/index.html`
  - the matching `tools/interactive-math-20261105/src/*.js` (rebuild with `python3 tools/interactive-math-20261105/build.py`).
- **New:**
  - `artifacts/interactive-math/lab-plus.js`
  - 14 folders `artifacts/<tool>/` (`index.html`, `worksheet.pdf`, `teacher-key.pdf`)
  - 14 thumbnails `thumbs/<tool>.jpg` (720 × 450, screenshots of the visualization)
  - `tools/interactive-math-20261107/` (the build sources and tests; the site does not load these):
    - `src/*.js` holds the tools; `manifest_src.py` produces `manifest.json`.
    - `build.py` builds the pages. `build_worksheets.py` + `worksheets_content.py` + `spacing.json` + `fonts/` build the worksheets, `fit_spacing.cjs` picks the writing space, and `print_pdfs.cjs` prints the PDFs. `make_thumbs.cjs` makes the thumbnails.
    - `tests/` holds the test suites.
- **Deleted:** none.

Rebuild (from the repository root):

```
python3 tools/interactive-math-20261107/manifest_src.py   # run inside that folder
python3 tools/interactive-math-20261107/build.py
python3 tools/interactive-math-20261107/build_worksheets.py && node tools/interactive-math-20261107/print_pdfs.cjs
node tools/interactive-math-20261107/make_thumbs.cjs
```

## Tests performed (all on the final files)

| Test | Result |
| --- | --- |
| `tests/walkthrough.cjs`: every "Try this" challenge in every new tool is completed through the normal page using real controls (sliders, chips, number boxes, buttons, arrow keys on draggable points). It also checks that no challenge is already done at the start. | 14/14 tools, 75/75 challenges |
| `tests/edge.cjs`: boundary cases (0 : 0, a clamped dividend, a divisor larger than the dividend, an obtuse-triangle height, x = 0 in y/x, all spinner parts removed, collinear corners, a perfect square, the zero vector, oscillation and asymptote limits, \|x\| at 0, a ≥ b, x < a). It also covers mouse dragging, plus layout on a 1366 × 768 light screen and a 360 × 740 dark phone (no sideways scroll, controls ≥ 28 px, no clipped readouts, dark theme applied). | 152/152 |
| Keyboard focus persistence while dragging with the arrow keys (custom-SVG and graph handles) | pass |
| `tests/revised-tools.cjs`: the fixes in the 9 revised tools (hole/asymptote cases, coincident zeros, bracketing bases, the dilation rule about a non-origin center, new challenges, the radian tab) | 35/35 |
| `tests/worksheet-answers.py`: independently recomputes every numeric answer in the 14 keys (including that each Pythagorean table row can be built on the tool's grid) | all pass |
| Page counts: all 28 worksheet and key PDFs are exactly 2 pages, with no question split across pages | pass |
| `tests/site-integration.cjs`: the 23 new catalog cards. Each must sit in its unit's Interactive Math section with Explore, worksheet, key and Copy student link, and every file must exist. The copied student link must open the tool, and the activity viewer must load it without errors. The Interactive Math shortcut must appear only where a unit has tools, and existing Algebra 1 tools must still be listed. | 278/278 |
| The viewer's student link for every Interactive Math tool (old and new, 46 tool paths) | 46/46 |
| `python3 scripts/check_library.py` | 0 problems |
| `worksheet-generator/games/tests/student-share-tests.cjs` | pass |
| `worksheet-generator/games/tests/student-share-browser.cjs` | Fails, **identically on the untouched baseline**: "Missing share setup: artifacts/relations-functions-function-machine-factory/index.html". This is unrelated to this update. |
| Teacher Guide on a 360 px phone (the new table scrolls inside its box, no page overflow) | pass |

## Limitations
- **Worksheet fonts.** The build machine had no network, so the PDFs embed the site's Atkinson Hyperlegible (regular) and Bricolage Grotesque (bold) glyphs, recovered from the existing Interactive Math PDFs.
  - Bold body text is synthesized from the regular weight.
  - A few characters those fonts lack (for example ≈, ×, √, π) fall back to Inter.
  - The PDFs look the same as the existing ones apart from that; for exact matching, reprint on a machine with the real font files.
- **Tool fonts.** The tool pages load Google Fonts like the existing tools; they were tested with the fallback fonts only.
- **Shared tools.** A tool listed in another course keeps the eyebrow and worksheet of the course it was built for. For example, the Pythagorean tool says "Pre-Algebra (8th)" in 7th grade, and the Algebra 2 tools say "Algebra 2" in Precalculus.
- **Simulations.** The Spinner and Probability labs use `Math.random()`, so their simulation results vary from run to run (the keys say so).
- **Untested.** Not tested on physical touch hardware. Touch uses the same pointer events that the tests exercise with a mouse, and phone layout was tested with touch emulation.

## Evaluation of each new tool
- **Double Number Line Ratio Explorer:** strong. The linked line, table and graph, plus the "test a pair" counterexample, make the multiplicative structure visible. Both unit rates are found by construction.
- **Fraction Division: How Many Groups?:** strong. It is the clearest visual answer to the remainder misconception, and the piece-count sentence derives the reciprocal rule instead of asserting it.
- **Parallelogram & Triangle Area Lab:** strong and simple. The cut-and-slide and copy visuals are faithful. The "base × slanted side" readout makes the misconception testable.
- **Dot Plot Balance:** strong. The balance-point fulcrum and the always-equal left/right distance totals make the mean's definition tangible. It also has the most open-ended challenges.
- **Proportional Relationship Explorer:** good. The y/x column shows "straight line ≠ proportional" clearly. It is more a contrast than a dramatic visual.
- **Percent Change Bar Model:** strong. Re-sectioning the second bar into 10% of the new amount explains why changes multiply.
- **Spinner Probability Lab:** good. It is distinct from the Algebra 2 lab (custom unequal spinners, expected counts, no memory). Results are random by design.
- **Pythagorean Squares Explorer:** strong. Exact lattice arithmetic, the converse, a "close is not equal" challenge and the tilted-square trick. Testing showed that a² + b² − c² is always even on a lattice, so the near-miss challenge uses 2.
- **Square Roots on the Number Line:** good. Squaring-based trapping across zoom levels is the right model, and it explicitly says zooming isn't proof.
- **Vector Explorer:** strong. Dragging tips makes the triangle inequality and u − v concrete, with exact magnitudes.
- **Limit Explorer:** strong. Value vs. limit is separated by a settable f(a). It includes non-existence cases and an explicit caveat about tables and zooming. The limits are hidden until revealed, to support predictions.
- **Secant to Tangent:** strong. Signed h, a corner case and the traced f′ graph make it the most complete derivative-concept tool on the site.
- **Riemann Sum Lab:** strong. Exact integrals, signed vs. total area, and method comparison at fixed n.
- **Accumulation Function Explorer:** strong. The live A(x) with a tangent whose slope equals f(x) is the FTC in one picture. The lower-limit slider shows the constant shift.

## Integration follow-up checks

The current site retained Statistics and Discrete Math, including all ten course outlines. The dilation non-overlap check now rejects collinear segments whose bounding boxes are disjoint. Degenerate source triangles do not complete the reduction challenge. Its opening center moved to (-1, 0), keeping both triangles overlapping so the non-overlap challenge is not completed on load. Sources and generated HTML agree. Added regression checks cover the geometry cases, all 46 interactive-tool share routes, new assets, and preservation of the two course outlines.
