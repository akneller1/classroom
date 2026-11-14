# 2026-11-14 — Interactive Math for every unit (Classroom repo)

Before this update, 26 units had no Interactive Math tool. Every 6th–12th grade unit now has at least one, and so does the new Precalculus Unit 9. The Grade 5 units are covered by the FinancialAlgebra update of the same date.

## 7 new tools (`tools/interactive-math-20261114`)
Each tool has five self-checking "Try this" challenges (none is checked when the page opens), a closed "What should I notice?" panel, Present/Fit/zoom, a 2-page Explore & Reflect worksheet, a 2-page teacher key with teacher notes, and a 720 × 450 thumbnail.

| Unit | Tool |
|---|---|
| 6th Grade · Rational Numbers | Rational Numbers: Opposites, Absolute Value & the Plane |
| Algebra 2 · Radicals & Rational Exponents | Rational Exponent Explorer |
| Precalculus · Trigonometry of General Triangles | Law of Sines: The Ambiguous Case |
| Precalculus · Matrices | Matrix Transformation Explorer |
| Calculus · Applications of Derivatives | Optimization: Open-Top Box |
| Calculus · Applications of Integrals | Area Between Curves & Solids of Revolution |
| Calculus · Differential Equations | Slope Field Explorer |

How to rebuild (from the repository root):

```
cd tools/interactive-math-20261114 && python3 manifest_src.py && cd ../..
python3 tools/interactive-math-20261114/build.py
node tools/interactive-math-20261114/fit_spacing.cjs
python3 tools/interactive-math-20261114/build_worksheets.py
node tools/interactive-math-20261114/print_pdfs.cjs
node tools/interactive-math-20261114/make_thumbs.cjs
```

Checks:
- `tests/walkthrough.py` plays every challenge with real controls (sliders, buttons, tabs, arrow keys on draggable points). Result: 7/7 tools reach 5 of 5, with no page errors.
- `tests/worksheet_answers.py` recomputes every numeric answer in the keys. All pass.

Fix in `build_worksheets.py`: exponents (`^{…}`) are now converted before fractions, so `8^{1/3}` prints as a raised exponent.

## Existing tools now also listed in units that had none (`data.js`, "Interactive Math sharing" block)
A shared tool keeps its own course name, worksheet and key.

**Pre-Algebra**
- Algebraic Expressions and Integers: Algebra Tiles Lab
- One-Step Equations and Inequalities: Equation Balance Scale and Inequality Number Line
- Decimals and Equations: Dot Plot Balance
- Factors, Fractions and Exponents: Exponent Rules Unpacker and Square Roots on the Number Line
- Operations with Fractions: Fraction Division
- Solving Equations and Inequalities: Equation Balance Scale
- Spatial Thinking: Parallel Lines & Transversal and Transformation Studio
- Area and Volume: Parallelogram & Triangle Area Lab and Solids Volume Lab
- Nonlinear Functions and Polynomials: Area Model Multiplier and Linear vs. Exponential Race

**6th Grade**
- Expressions and Equations: Algebra Tiles Lab
- Inequalities: Inequality Number Line

**8th Grade**
- Equations and Expressions: Equation Balance Scale and Exponent Rules Unpacker
- Patterns and Bivariate Data: Line of Best Fit Lab

**Precalculus**
- Sequences, Series, and Limits: Sequence Builder and Limit Explorer

**Calculus**
- AP Calculus Review: Limit Explorer, Secant to Tangent, Riemann Sum Lab and Accumulation Function Explorer

**Discrete Math**
- Speaking Mathematically: Venn Diagram Explorer and Truth Table Lab

The `data.js?v=` cache string is now `interactive-20261114` on every page.
