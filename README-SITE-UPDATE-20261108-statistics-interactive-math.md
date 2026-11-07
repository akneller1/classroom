# Site update 2026-11-08: Interactive Math for Statistics

**Baseline:** commit `3d8d7b8ee5e6596a2bb03e19bf8597d77f72aa44`, from `SOURCE_COMMIT.txt` in `Statistics_Repository_Files_Claude.zip`.

**This ZIP is cumulative.** It replaces the earlier Statistics ZIP and adds a seventh tool, the Random Assignment Lab. If the earlier ZIP was already merged, upload this one over it. The only shared-file difference is the Statistics block at the end of `data.js`, which now has 8 entries instead of 7; replace that block as a whole. The ZIP contains only new and changed files at their repository paths (64 files, one upload). Nothing has been committed, pushed or deployed.

The ChatGPT library link (`statistics-bank-expansion.zip`) needs a login, so I couldn't open it. The interactive tools don't use the question bank, so nothing here depends on it.

## Contents
- **7 new Statistics tools,** each with a 2-page Explore & Reflect worksheet, a 2-page teacher key with teacher notes, and a thumbnail.
- **The Algebra 2 Probability Simulation Lab** is also listed in Anticipating Patterns, for the topic "Probability: Long-Run Relative Frequency and the Law of Large Numbers".
- **Statistics stays a `planned` course** (the CI test requires this). Its unit pages now also show an Interactive Math section when a unit has tools.
- **A new shared helper, `artifacts/interactive-math/lab-stats.js`,** adds seeded random numbers, normal and t distributions and summary statistics. Only the Statistics tools load it.
- **Two small fixes to my previous update:**
  - `drawRadian()` had been duplicated inside the Unit Circle tool's tab callback. The behavior was unchanged, but the code was not clean.
  - The dilation regression test hard-coded the old starting center. It now reads the center from the page, so it passes with ChatGPT's newer starting state, O(−1, 0).

## Install
1. Unzip at the repository root and upload with GitHub "Add files via upload", keeping the folder structure. There are 64 files.
2. **Nothing needs to be deleted.**
3. If `app.js`, `data.js`, `guide.html`, `index.html` or `activity.html` changed on `main` after `3d8d7b8`, merge the changes below by hand instead of replacing the file.
4. `artifacts/geometry-dilation-similarity-lab/index.html` is **not** in this ZIP. If `main` has not already rebuilt it from ChatGPT's fixed source, run `python3 tools/interactive-math-20261105/build.py`. That rebuild changes only that page and the Unit Circle page, which is included here.

## Merge notes (shared files)

| File | Exact change |
| --- | --- |
| `app.js` | (1) New helpers just above `function unitView(c, u)`. `plannedInteractive(c, u)` returns the unit's Interactive Math items, using the `interactive` group of `RESOURCE_GROUPS`. `plannedToolUnits(c)` counts the units that have such items. (2) Inside the `if (c.planned) { … }` branch of `unitView`, `var tools = plannedInteractive(c, u);` is added. When tools exist, a `<section class="algebra-unit-section" aria-labelledby="algebra-interactive">` with the cards (built by `cardHtml`) is inserted after the topic list. The band meta then reads "Course outline · Interactive Math available · More activities coming soon", and the empty-state heading reads "More activities coming soon". (3) The planned course band meta and the home-card count add "Interactive Math in N units" / "· Interactive Math" when `plannedToolUnits(c)` is non-zero. Planned courses without tools (Discrete Math) render exactly as before. |
| `data.js` | **Append only:** one block at the end, starting `/* Interactive Math Statistics 2026-11-08 …`, with 8 `{course, unit, a}` entries. It uses the same skip-if-present pattern as the earlier Interactive Math blocks. |
| `index.html` | Cache strings: `data.js?v=interactive-math-statistics-20261108` and `app.js?v=interactive-math-statistics-20261108`. |
| `activity.html` | Cache string: `data.js?v=interactive-math-statistics-20261108`. |
| `guide.html` | Interactive Math section: a Statistics row in the coverage table; a paragraph on adding `&seed=` to a student link so a class shares the same random results; "Statistics" added to three existing sentences. |
| `tools/interactive-math-20261105/src/algebra2-unit-circle-sine-wave.js` | Removed the duplicate `drawRadian()` that a string replacement had inserted into the tab callback. The callback is again `function (id) { st.mode = id; build(); draw(); }`. The rebuilt `artifacts/algebra2-unit-circle-sine-wave/index.html` is included. |
| `tools/interactive-math-20261107/tests/revised-tools.cjs` | The dilation section moves the center relative to wherever it starts (`centerO`/`moveO` helpers) instead of assuming (−3, −2). |
| New: `.github/workflows/interactive-math-statistics.yml`, `scripts/test-interactive-math-statistics.cjs` | A CI workflow that checks placements and resources, that the course stays planned, that student links route directly, and that `app.js` has the planned-page section. It also runs the math-library test and recomputes the worksheet answers. The existing CI files are unchanged. |

## The tools

| Unit (id) | Tool | Central relationship students discover |
| --- | --- | --- |
| Exploring Data (`exploring-data`) | Residuals & Influence Lab | A patterned residual plot means a line is the wrong model even when r ≈ 0.985. Outliers (large residual), high-leverage points (extreme x) and influential points (change the line when removed) are different things, and changing units rescales the slope but not r or r². |
| Sampling and Experimentation (`sampling-experimentation`) | Sampling Methods Lab | Bias is where estimates center; variability is how they spread. Convenience sampling stays biased at any n. Stratifying on grade cuts variability (SD 0.145 vs. 0.19), and single-grade homeroom clusters raise it (0.39). |
| Anticipating Patterns (`anticipating-patterns`) | Sampling Distribution Lab | The sampling distribution of x̄ or p̂ is centered at the parameter, its SD is σ/√n or √(p(1 − p)/n), and it becomes approximately normal (CLT, Large Counts). It is distinct from the population and from one sample, which are shown as three linked plots. |
| Anticipating Patterns | Conditional Probability: Screening Tests | P(C \| +) ≠ P(+ \| C). Rare conditions make false positives dominate (50% for a 99%/99% test at 1% prevalence), specificity matters most, and independence means P(+ \| C) = P(+ \| not C). |
| Anticipating Patterns | *Probability Simulation Lab (reused from Algebra 2)* | The Law of Large Numbers with coins and dice. The objective and scaffolding fit the course's first topic. |
| Sampling and Experimentation | Random Assignment Lab | Self-selection confounds the treatment with GPA (a fake +8.6-point effect when the app does nothing). Random assignment is unbiased and balances GPA on average, but 14% of single assignments are off by ≥ 0.3 GPA (exact, over all 184,756 assignments). Randomized matched pairs cut the SD from 3.04 to 1.40. A randomization test's p-value is the share of label shuffles at least as large as the observed difference. |
| Statistical Inference (`statistical-inference`) | Confidence Interval Lab | The confidence level is the long-run capture rate of the method. Higher confidence means wider intervals, and 4 × n halves the margin of error. Capture rates fall short when Large Counts fails or when z* is used with s (≈ 88% at n = 5). |
| Statistical Inference | Significance Test & Power Explorer | The p-value is a tail area under the null model, and two-sided tests double it. The same p̂ becomes significant with larger n. Type I error = α, Type II = β and power = 1 − β, shown as areas; lowering α raises β. |

Every tool has:
- an opening state where no challenge is already done;
- linked representations and live readouts;
- 5–6 "Try this" challenges (predict, construct, counterexample, transfer);
- Reset, live feedback, and a closed "What should I notice?" panel;
- arrow-key alternatives for every draggable point;
- −/+ buttons on every slider;
- information carried by labels and shapes, not color alone (dashed ✗ misses, a square-framed extra point, striped false positives).

All simulated values are labeled as estimates. Normal approximations are stated on screen.

## Priority review (why these tools)

| Unit | Candidate | Concept revealed | Decision |
| --- | --- | --- | --- |
| Anticipating Patterns | Sampling distribution / CLT simulator | Shape, center and spread of x̄ and p̂ | **Built (highest).** Only a simulation shows a sampling distribution forming, and it is the foundation for all inference. |
| Statistical Inference | Confidence-interval coverage simulator | Meaning of confidence, margin of error, conditions | **Built (highest).** It directly targets the most common interpretation error. |
| Statistical Inference | p-value, errors and power | Tail areas, α/β trade-off, power | **Built (high).** Power is abstract without overlapping curves. |
| Sampling and Experimentation | Sampling methods simulator | Bias vs. variability; stratified vs. cluster | **Built (high).** The "a bigger sample fixes bias" misconception is visible at once. |
| Anticipating Patterns | Two-way table / tree for screening tests | P(A\|B) vs. P(B\|A), base rates, independence | **Built (high).** A high-stakes misconception with a strong visual (who tests positive). |
| Exploring Data | Regression with residual plot and influence | Residual patterns, r², outlier vs. leverage vs. influence | **Built (high).** It is distinct from the Algebra 1 Line of Best Fit Lab, which has no residual plot, r² or influence analysis. |
| Anticipating Patterns | Law of Large Numbers | Long-run relative frequency | **Reused** the Algebra 2 Probability Simulation Lab; no new build was needed. |
| Sampling and Experimentation | Random assignment / experiment simulator | Confounding, blocking, randomization distribution | **Built (high), as the Random Assignment Lab.** The experiments half of the unit had no tool, and the randomization test also gives the Inference unit a simulation-based p-value. |
| Exploring Data | Distribution and boxplot explorer (SD, IQR, 1.5·IQR, transformations) | Resistance, spread, linear transformations | **Not built.** It partly overlaps the 6th-grade Dot Plot Balance; it would rank lower than the regression tool. |
| Anticipating Patterns | Binomial / geometric distribution explorer | np, √(np(1 − p)), shape | **Not built.** It is more calculator-like; the Sampling Distribution Lab's p̂ mode covers the shape-and-spread idea. |
| Exploring Data | Algebra 1 Line of Best Fit Lab (reuse) | Least squares | **Not reused.** Its challenges and worksheet are Algebra 1-level; the new regression tool covers the Statistics objectives. |

## Review of existing tools relevant to Statistics

| Tool | Decision | Reason |
| --- | --- | --- |
| Probability Simulation Lab (Algebra 2) | **Kept and reused** in Statistics | Accurate. Its small-sample, 7s-within-0.01 and 2σ challenges (from my last update) fit the LLN topic. |
| Line of Best Fit Lab (Algebra 1) | Kept, not reused | Good for Algebra 1; it lacks residual plots, r² and influence, which Statistics needs. |
| Dot Plot Balance (6th) and Spinner Probability Lab (7th) | Kept, not reused | The scaffolding is middle-school level. |
| Unit Circle to Sine Wave | **Improved** (code only) | Removed the duplicated `drawRadian()`. Behavior is unchanged, and the 35 revised-tool checks pass. |
| Dilation & Similarity Lab | Kept (ChatGPT's fix verified) | ChatGPT correctly fixed collinear-edge overlap and degenerate triangles in my previous code. My regression test is updated for its new starting center. |
| New Statistics tools (7) | **Added** | All passed the tests below. Two weak challenges were replaced during testing: "flip r's sign with one point" was barely possible, and the conditional-probability opening state would have answered challenge 1 in advance. |
| Removed | — | None. No deletion manifest is needed. |

## Tests (all on the final files)

| Test | Result |
| --- | --- |
| `tools/interactive-math-statistics/tests/stats-core.cjs`: normal/t CDFs and quantiles against published values. A separate SciPy comparison over 70+ values found maximum errors of 1×10⁻⁸ (Φ), 7×10⁻⁸ (Φ⁻¹) and 2×10⁻¹² (t). This test caught one bug: t* for df = 1 at 0.995 fell outside the original search range. | 28/28 |
| `tests/walkthrough.cjs`: every challenge completed through the real controls, and none done at the start. Run under 6 different random seeds. | 37/37 challenges, every seed |
| `tests/correctness.cjs`: displayed p-values, power, PPV, LSRL, r, s and t* against SciPy/NumPy values; simulations against theory; edge cases; Chromebook/light and phone/dark layout. Edge cases: p̂ = 0, every point at one x, a 2.5-seat systematic step, broken conditions, n = 1, sens = 1 − spec. Simulation checks: SD of x̄ ≈ σ/√n; t-interval coverage ≈ 95%; z*-with-s coverage ≈ 87.8% = P(\|t₄\| < 1.96); stratified < SRS < cluster spread; convenience bias. Random Assignment Lab: self-selection bias ≈ +8.6, random assignment centered on the true effect, SD ≈ 3.04 vs. 1.40 for pairs, p-value = count/1000, p < 0.05 in at most 6 of 40 null experiments and in at least 9 of 10 at δ = 12. | 157/157 |
| Mouse dragging and arrow-key focus on the regression points | pass |
| `tests/worksheet-answers.py`: standard library only, so it runs in CI. It recomputes every numeric key answer, rebuilds the tools' fixed populations with a Python copy of the seeded generator, and uses exact finite-population formulas for the sampling-method SDs. For the Random Assignment Lab it uses exact SDs and enumerates all 184,756 assignments for the imbalance probability. | all pass |
| Worksheets and keys: 14 PDFs, each exactly 2 pages | pass |
| `tests/site-integration.cjs`: the 8 Statistics cards (section, Explore, worksheet, key, student link, viewer). Statistics unit and course pages show the new text; Discrete Math (planned, no tools) is unchanged. Search finds the tools. | 102/102 |
| `&seed=2024` added to a copied student link gives identical results in two separate windows | pass |
| Existing checks: `scripts/test-interactive-math-statistics.cjs` (new), `scripts/test-interactive-math-update.cjs`, `scripts/check_library.py`, `scripts/audit-course-catalog.cjs`, `student-share-tests.cjs`, `test-browse-activities-browser.cjs`, `test-classroom-presentation.cjs`, `test-coverage-report.cjs`, `test-resource-eligibility.cjs` and three bank-integration tests | all pass |
| `test-course-parity-browser.cjs` | Too long for this environment's 5-minute command limit. A copy limited to the planned courses (Statistics and Discrete Math) passes the same 127 scenarios on the baseline and on this update. The rest of the test covers game pages this update doesn't touch. |
| Previous update's suites (2026-11-07 walkthrough, edge, revised tools) on this tree | 14/14 tools; 152/152; 35/35 |

## Limitations
- **Normal approximations.** The Significance Test & Power Explorer uses the normal approximation for a one-proportion z test. It says so and flags Large Counts failures.
- **Simulations vary.** Without `?seed=`, results differ from run to run, as intended. The keys give theory or long-run values and say which answers vary.
- **Shared tool label.** The reused Probability Simulation Lab keeps its Algebra 2 eyebrow and worksheet.
- **Worksheet fonts.** The PDFs embed the same recovered Atkinson Hyperlegible and Bricolage Grotesque glyphs as the previous update. A few symbols (for example ≈, √, μ, σ) fall back to Inter.
- **Untested.** Not tested on physical touch hardware; touch emulation and pointer events were tested.

## Evaluation of each new tool
- **Sampling Distribution Lab:** strong. The three linked plots (population, one sample, sampling distribution) separate the ideas students most often merge. The simulated SDs match σ/√n, and the skewness readout makes "approximately normal" concrete.
- **Confidence Interval Lab:** strong. The capture-rate counter makes the meaning of "95% confident" unavoidable. The z*-versus-t* comparison is the clearest demonstration of why t exists that this site offers.
- **Significance Test & Power Explorer:** strong. p-values, α, β and power are all areas on one picture, and the "smallest n for power 0.80" search builds intuition for sample-size planning.
- **Sampling Methods Lab:** strong. One seating chart shows why convenience sampling fails at any size, why stratifying helps and when clusters hurt, all from 160 named seats.
- **Conditional Probability: Screening Tests:** strong. The "who tests positive" bar and the counts out of 100,000 turn Bayes' rule into arithmetic students can check.
- **Random Assignment Lab:** strong. One seating chart and one histogram show confounding (a fake effect from self-selection), why random assignment works only on average, and how matching reduces variability. The randomization test makes the p-value a count students can see.
- **Residuals & Influence Lab:** strong. The curved-data example (r = 0.985 with an obvious pattern) and the three-way outlier/leverage/influence classification address the course's most persistent regression errors.
