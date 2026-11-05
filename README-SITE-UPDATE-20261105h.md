# Site update h: Interactive Math

This update adds 22 hands-on Interactive Math tools: 12 for Algebra 1 and 10 for Algebra 2. Each tool comes with a printable Explore & Reflect worksheet and a teacher key. Every unit page that has a tool shows it in a new **Interactive Math** section after Games and Study Guides.

This update is built on the live site, which includes your Math Millionaire upload. Unzip it at the repository root.

## Changed files

| File | Change |
| --- | --- |
| `app.js` | Adds the Interactive Math category: the unit-page section, the Interactive Math shortcut (shown only where a course or unit has tools), a Browse Activities filter option, the card's "Explore" button, and the worksheet and teacher key links on each card. |
| `data.js` | One block added at the end that lists the tools. Nothing above it changed. |
| `activity.js`, `student-share-cards.js` | Interactive tools get a **Copy student link** button, so students can use them on their own devices. |
| `guide.html` | New Teacher Guide section, "Interactive Math", plus a link in the table of contents. Interactive Math tools are also added to the list of activities with a student link. |
| `index.html`, `activity.html` | Cache versions bumped. |

## New files

- `artifacts/interactive-math/lab.css`, `lab.js`: the shared look and behavior for every tool.
- `artifacts/<tool>/index.html`, `worksheet.pdf` and `teacher-key.pdf` for each tool. Every worksheet and key is 2 pages.
- `thumbs/<tool>.jpg`: one card thumbnail per tool (720 × 450).
- `tools/interactive-math-20261105/`: the sources. These files are only for rebuilding; the site doesn't load them.
  - `src/*.js` and `manifest.json`: the tools.
  - `worksheets.py`: the worksheet content.
  - `build.py`, `build_worksheets.py`, `print_pdfs.cjs`: the build scripts.

## The tools

| Course | Unit | Tool |
| --- | --- | --- |
| Algebra 1 | Foundations of Algebra | Algebra Tiles Lab |
| | Solving Linear Equations | Equation Balance Scale |
| | Linear Inequalities | Inequality Number Line |
| | Relations and Functions | Function Detector |
| | Linear Functions and Graphing | Slope-Intercept Explorer |
| | Systems of Equations and Inequalities | Systems Explorer |
| | Exponents and Scientific Notation | Exponent Rules Unpacker |
| | Exponential Functions | Linear vs. Exponential Race |
| | Polynomials | Area Model Multiplier |
| | Factoring and Zero Product Property | Factor Rectangle Builder |
| | Quadratic Functions and Equations | Parabola Explorer |
| | Statistics and Data Modeling | Line of Best Fit Lab |
| Algebra 2 | Functions & Transformations | Transformation Lab |
| | Linear Functions & Systems | Feasible Region Optimizer |
| | Quadratic Functions & Complex Numbers | Discriminant & Roots Explorer |
| | Polynomial Functions | Zeros & Multiplicity Builder |
| | Exponential & Logarithmic Functions | Exponential & Log Mirror |
| | Rational Functions | Asymptote & Hole Explorer |
| | Sequences & Series | Sequence Builder |
| | Conic Sections | Conic Explorer |
| | Trigonometric Functions | Unit Circle to Sine Wave (also listed in Precalculus → Trigonometric Functions and Calculus → Precalculus Review) |
| | Probability & Statistics | Probability Simulation Lab |

Radicals & Rational Exponents has no separate tool. The Transformation Lab covers √x.

## What every tool has

- **Interactive parts:** sliders with − / + buttons, draggable points (mouse, touch or arrow keys) and a live equation readout.
- **A "Try this" list:** 4–6 challenges that check themselves as students explore.
- **Display:**
  - Fractions are always stacked.
  - The tools follow light and dark mode.
  - They fit phones.
- **The Explore & Reflect worksheet has five parts:**
  1. Predict
  2. Explore (tables to fill in)
  3. Write the rule (sentence frames)
  4. Check (no tool)
  5. Reflect
- **The teacher key** has every answer in red. In tables where results depend on what a student did (for example their own line of fit or coin flips), the key says "answers vary".

## Tested

- Every tool opens with no script errors, and nothing overflows sideways at phone width in either theme.
- Every "Try this" challenge was completed by an automated walkthrough, including dragging points.
- Unit pages show the section in Algebra 1, Algebra 2, Precalculus and Calculus, and not in Geometry.
- Browse Activities lists all 24 cards (22 tools, with the unit circle tool in three courses).
- Cards open in the activity viewer, and student links open just the tool.
- `python3 scripts/check_library.py` reports 0 problems, and `worksheet-generator/games/tests/student-share-tests.cjs` passes.
