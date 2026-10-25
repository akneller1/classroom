# Menu Assessment Generator

A browser-only builder for restaurant-style choice assessments ("Assessment Menus"). It has no server, no
accounts and no paid services, so it runs on GitHub Pages. Open `worksheet-generator/menu-assessment.html`.

**Supported units (Algebra 1 roadmap):**
- Units 1–2 · Foundations & Solving Linear Equations (`algebra1-expressions-equations`)
- Unit 3 · Linear Inequalities (`algebra1-inequalities`)
- Unit 4 · Relations and Functions (`algebra1-relations-functions`)
- Unit 5 · Linear Functions and Graphing (`algebra1-linear-equations-slope`)
- Unit 6 · Systems of Equations and Inequalities (`algebra1-systems-of-equations`)
- Unit 7 · Exponents and Scientific Notation (`algebra1-exponents-scientific-notation`)
- Unit 9 · Polynomials (`algebra1-polynomials`)
- Unit 8 · Exponential Functions (`algebra1-exponential-functions`)
- Unit 10 · Factoring and Zero Product Property (`algebra1-factoring-zero-product`)
- Unit 12 · Statistics and Data Modeling (`algebra1-statistics-data-modeling`)

Other units appear in the unit list as "not yet supported" until they have generators that pass the same
verification tests (see *Adding a unit*). Open a unit directly with `menu-assessment.html#unit=<id>`. Each
unit keeps its own autosave. The existing static Assessment Menu PDFs are unchanged and still listed on every unit page.

## Teacher workflow
1. **Course and unit.** Also set the menu title and subtitle.
2. **Class level.** Choose CP2 (foundational), CP1 (standard) or Honors (advanced). You can also force
   whole-number answers or allow fraction answers.
3. **Menu and rules.** Set the sections (rename, add or remove them), points per problem, how many problems
   are offered, how many students must complete, each section's difficulty (± fine-tuning), which skills
   each section may use, and the skill-coverage rule. The maximum score and any impossible or inconsistent
   rule are shown live. Presets: standard 100-point menu, short quiz, unit test.
4. **Skills.** Uncheck skills to exclude them. "Sample" shows the same skill at all 7 difficulty levels.
5. **Build.** Choose Versions A, B or A–C.
6. **Review and edit.**

   **Applies to this version only:**
   - **New problem**: regenerate this problem with the same skill and difficulty.
   - **Pin**: keep this problem when other problems are regenerated.
   - **Edit**: change the problem by hand. The answer is re-verified; the old answer is never trusted.
   - **Approve**: accept a hand-entered answer that cannot be checked automatically.

   **Applies to every version, so the versions stay parallel:**
   - **Easier / Harder**
   - **Change skill**
   - **Move** to another section
   - **↑ / ↓** reorder
   - **Delete** (with Undo)
   - **Add a problem** (any skill and difficulty)
   - **Write your own** problem
   - **Make required** ("everyone must do")

   The **Problem bank** makes, for example, ten problems of one skill and difficulty, each with its answer
   and worked solution, so you can choose the ones you want. Undo (Ctrl/⌘-Z) covers every change.
7. **Preview** the student menu and the teacher key. Layout options:
   - problems with workspace, or menu + separate work pages
   - compact, standard or spacious
   - blank, graph-paper or coordinate-plane workspace
   - an optional reference page
   - an optional teacher-guide page
8. **Print or save as PDF** (US Letter). You can also:
   - save named copies in this browser
   - download or open a `.json` file
   - duplicate an assessment

   Your work is autosaved in the browser.

## Difficulty model
Each problem has one difficulty number **c = 1…7**. It changes the mathematics (structure, signs, number
size, fractions, number of steps, number of parts), not only the label:

| Level  | Appetizers | Entrées | Chef's Specials | Answers by default |
|--------|-----------:|--------:|----------------:|--------------------|
| CP2    | 1 | 2 | 3 | whole numbers |
| CP1    | 3 | 4 | 5 | whole numbers |
| Honors | 5 | 6 | 7 | fractions allowed |

Section tiers and the ± buttons move a whole section; Easier/Harder moves one problem. Skills also say
which tiers they suit (`best`), so Appetizers lean on one- or two-step skills and Chef's Specials on
multi-step and multi-part ones.

## Architecture (`worksheet-generator/menu/`)
| File | Job |
|------|-----|
| `mathcheck.js` | **Independent checker.** Its own tokenizer and parser (TeX subset + plain typing), BigInt rationals, multivariate polynomials and rational functions. Solves linear equations (clearing denominators, excluded values), tests equivalence and "fully simplified" form, checks literal equations by substitution. Shares no code with the generators. |
| `verify.js` | Re-derives every answer from the **student-facing text**. The math in a part's `check` must appear verbatim in the printed question. Word problems are re-solved from the numbers and words in the prompt. Also checks every worked-solution step. |
| `engine.js` | Skill-set registry, levels, menu rules (maximum score, max-flow coverage feasibility, warnings), generation loop (generate → verify → de-duplicate → retry; a failure becomes a flagged slot, never a substitute), versions sharing one slot structure, all teacher operations, problem bank, rebuild, save/load (re-verifies on load). |
| `skills/algebra1-expressions-equations.js` | The 11 E&E skills, answer-first, difficulty 1–7, worked steps with rubric weights, reference page, documented gaps. |
| `figures.js` | Number lines drawn from data specs, and `readNumberLine()`, which reads the **drawn SVG** back (circles, segments, arrows) so the verifier checks the picture itself. |
| `skills/kit.js` | Shared TeX/step/number-line helpers for skill files (generator side only). |
| `render.js` | Student menu (cover, directions, order form, score table, sections, work pages, reference page) and teacher key (guide, every offered dish, answer, worked solution, partial-credit rubric). Letter pages are measured so nothing is split across pages. Text outside math is HTML-escaped. |
| `app.js`, `menu.css` | The 8-step teacher interface and the paper styles. |

Reused from the worksheet generator, unchanged: `core/rng.js` (seeded randomness), `core/frac.js` (exact
fractions for the generators), `core/tex.js` (TeX builders), `core/framework.js` (`gen.need`/reject), `core/graph.js`
(coordinate planes), `core/render.js` (KaTeX rendering), `core/app.css` (look and feel, print rules), `vendor/` (KaTeX, fonts).

## Skills in the pilot
| Tag | Skill | Level 1 → 7 (examples) |
|-----|-------|-------------------------|
| SIMPLIFY | Combine like terms | `x`-terms only → two variables, negatives → squared terms and fraction coefficients |
| SIMPLIFY | Evaluate expressions | `5x+1` at `x=4` → two variables, squares → fraction bars, fraction inputs |
| DISTRIB | Distribute and simplify | `5(3x+2)` → two groups, subtraction of a group → fraction factors, nested brackets |
| SOLVE | One- and two-step equations | `x+9=13` → `−15−7x=13` → fraction or decimal coefficients |
| SOLVE | Multi-step equations | `6(x−3)=−6` → distribute and combine → fraction factor plus a second group, nested |
| SOLVE | Variables on both sides | `9x+5=5x+25` → distribution on both sides → extra terms, fractions |
| SOLVE | Fractions and decimals | `x/7=5` → `(x−12)/4=−3`, decimals → LCD, fractions on both sides |
| SOLVE | One / none / infinitely many | simplified sides → distribution on both sides |
| SOLVE | Proportions | `x/36=3/9` → variable in a denominator → binomials on both sides |
| LITERAL | Literal equations and formulas | solve for `y` in one move → `ax+by=c`, formulas → multi-step formulas, then use them (2 parts) |
| MODEL | Word problems | fee + rate → consecutive integers, perimeter → comparing plans, multi-part |

### Linear Inequalities skills (tags SOLVE · COMPOUND · REASON · APPLY)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| SOLVE | One- and two-step | `x+9>13` → negative coefficients that reverse the sign → fraction/decimal coefficients |
| SOLVE | Multi-step | `a(x+b)<c` → both sides, `d−e(x+f)` → LCDs, several groups |
| SOLVE | All real numbers / no solution | simplified sides → distribution on both sides |
| COMPOUND | “And” | `a<x+b≤c` → negative coefficient, two separate inequalities → fraction middles |
| COMPOUND | “Or” | simple → coefficients, a negative → fractions, overlapping rays (all real numbers) |
| COMPOUND | Absolute value | `|x|<a` → `|x−h|`, `|ax+b|` → isolate first, special cases |
| REASON | Graphs | draw/read a ray → read and draw intervals and “or” graphs → write absolute value inequalities for a graph (2 parts) |
| REASON | Which values are solutions? | always tests the boundary value (open vs. closed) |
| REASON | Find and fix the mistake | forgot to reverse → one-sided LCD → distribution sign errors in longer work |
| APPLY | Word problems | budget → fees, saving goals, comparing plans → compound budgets, averages, listing whole-number answers |

Every "solve" problem prints a blank number line for the student; the key shows the graph. The verifier
solves the printed inequality itself. It handles chains (`−3<2x+1≤7`), “and”/“or”, `|…|` and fraction bars,
using the critical-point method on exact rationals. It also re-reads the key's drawn number line, checks that the
blank student line shows every endpoint, checks which line in a "find the mistake" problem is the first wrong one,
and re-solves word problems from the printed numbers.

### Relations and Functions skills (tags RELATIONS · NOTATION · REPRESENT · RATE · SEQUENCE)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| RELATIONS | Domain and range | ordered pairs → table → mapping diagram, graphed points (a repeated input) → graphs as inequalities with open dots and arrows |
| RELATIONS | Is it a function? | pairs, tables, mapping diagrams, points → vertical line test on lines and curves → a split graph where one dot decides → equations such as `x=y²` |
| NOTATION | Function notation | `f(4)` → negative inputs, quadratics, solve `f(x)=k` → `2f(1)−g(3)` → simplify `f(2a+3)` and solve |
| NOTATION | Read tables and graphs | `f(a)` and `f(x)=k` from a table → one-piece graph → two solutions on V-shaped and three-piece graphs → `f(f(a))` |
| REPRESENT | Write a rule | `x=0,1,2…` → negative rates, “is it linear?” → a graph with a fraction slope → uneven x-steps → fraction rates without `x=0`, then predict |
| REPRESENT | Complete a table | linear outputs → quadratics → missing inputs that must be solved, fraction rules |
| RATE | Rate of change | two points → linear table → word problems with units → average rate of a quadratic, comparing two intervals |
| RATE | Increasing / decreasing | where is it increasing → all three behaviours → stories (distance from home) |
| SEQUENCE | Arithmetic sequences | next two terms → the nth term → explicit formula → which term is k → formula from two terms → recursive + explicit + “is k a term?” |

Tables, mapping diagrams and coordinate graphs are drawn from a spec and the verifier reads them back from the drawn SVG/HTML
before checking anything: domain and range from the drawn pieces (open dots, arrows), the vertical line test at every
drawn x and between them, values and solutions of `f(x)=k` read off the drawing, a line fitted through every table row,
missing table entries, rates from the printed points or interval, and arithmetic-sequence formulas checked term by term.
Explanations are checked too: a "not a function" answer must name an input that really has two outputs, and a word-problem
rate explanation must use the same rate.

### Exponential Functions skills (tags EVAL · GROWTH · MODEL · SOLVE · SEQUENCE · APPLY)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| EVAL | Evaluate | `f(3)` for `3·2ˣ` → x = 0 and negative inputs, fraction bases → shifts `a·b^(x−h)+k`, decimal bases, `f(3) − g(0)` |
| GROWTH | Growth or decay, initial value, factor, rate | integer bases → fraction bases, `1.05`, `0.85` → models in context, fraction bases above 1, value after 2 years |
| GROWTH | Key features | intercept and increasing/decreasing from a graph → asymptote, domain, range → shifts and reflections, all five features |
| MODEL | Linear, exponential or neither | integer tables → decreasing and decay → x-steps of 2, fraction ratios, “neither” |
| MODEL | Write `y = a·bˣ` | tables from x = 0 → tables from x = 1, decay tables, x = 2 → two points (+ predict a value), fraction factors |
| SOLVE | Common base | `2ˣ = 32` → `3·2ˣ = 48`, `3ˣ⁻¹ = 27`, same base both sides → rewrite bases, `(1/4)^(x+3) = 64`, fraction answers |
| SEQUENCE | Geometric sequences | next terms → negative and fraction ratios, nth term, explicit formula → which term, formula from two terms, recursive + explicit |
| APPLY | Growth and decay | doubling, halving → percent growth/decay value, write `P(t) = a(1 ± r)ᵗ` → rounding, doubling periods `2^(t/3)`, when a value first passes a target |

The checker now reads variable and fractional exponents exactly (`4^{3/2} = 8`; an irrational power is refused). It
recovers `a`, `b` and `k` of a printed rule by evaluating it, checks a drawn exponential curve against the rule,
solves exponential equations through logarithms (proving the solution is unique) and then confirms the answer exactly,
detects arithmetic vs. geometric sequences, and re-solves word problems from the printed numbers (growth words,
percent, doubling period, rounding instruction).

### Factoring and Zero Product Property skills (tags GCF · TRI · SPECIAL · SOLVE · APPLY)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| GCF | GCF and grouping | `6x + 9` → `4x² + 10x`, a common binomial, three terms → grouping, GCF then grouping, `x(x + h)(x² − n²)` |
| TRI | `x² + bx + c` | positive → negative b and c → prime trinomials and a negative leading term, a GCF first, `x³` trinomials, `x⁴ − 13x² + 36` |
| TRI | `ax² + bx + c` | `2x² + 7x + 3` → mixed signs, `a` composite → a GCF first, `4x⁴ − 17x² + 4` |
| SPECIAL | Special products | `x² − 64` → perfect squares, `4x² − 1` → a GCF first, `2a⁴ − 32`, sums of squares are prime |
| SOLVE | Zero product property | `(x − 2)(x − 5) = 0` → `x² + 5x + 4 = 0`, terms on both sides, `(x − 1)(x + 4) = 24` → `5x² − 32x + 12 = 0`, cubics |
| APPLY | Problems | consecutive (even/odd) integers → rectangles (`L = w + k`, `2w ± k`) → a uniform border, dropped and thrown objects |

A factorization is accepted only if it multiplies back to the printed polynomial, every number factor is an integer,
and every other factor has no common factor and is irreducible over the integers (degree 1; degree 2 with a
non-square discriminant; degree 3 with no rational root). “Prime” is accepted only for primitive irreducible
polynomials. Equations are solved by finding every rational root (rational root theorem, exact arithmetic);
problems whose roots are not all rational are refused. Word problems are re-solved from the printed numbers and
wording (“consecutive even integers”, “3 feet less than twice its width”, “uniform width”) and keep only the
answer that makes sense.

### Polynomials skills (tags CLASSIFY · ADDSUB · MULT · SPECIAL · APPLY)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| CLASSIFY | Classify polynomials | degree → name by terms → name by degree and terms → standard form and leading coefficient → degree with two variables → degree of a product → simplify, then the degree |
| ADDSUB | Add and subtract | add → subtract → missing terms → terms out of order → three polynomials → two variables → multiples of polynomials |
| MULT | Multiply | monomial × binomial → two binomials → monomial × trinomial → leading coefficients ≠ 1 → binomial × trinomial → two variables → three binomials |
| SPECIAL | Special products | (a+b)² → (a−b)² → (a+b)(a−b) → (ka±b)² → two-variable squares → two-variable sum × difference → difference of squares of binomials, a cube |
| APPLY | Divide; geometry | perimeter → area → divide by a monomial → shaded region → square with a hole → box volume → divide with two variables |

Answers must be equivalent to the printed expression (or to the expression built from the printed side lengths, matched
in the order they are printed) and in standard form: one simplified term per degree, highest degree first.

### Exponents and Scientific Notation skills (tags PRODUCT · QUOTIENT · EVAL · SCI · SCIOPS)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| PRODUCT | Product and power rules | multiply powers → power of a power → with coefficients → power of a product → two-variable products → combined powers and products → with negative coefficients |
| QUOTIENT | Quotient, zero and negative exponents | divide powers → with coefficients → zero and negative exponents → quotient leaving a fraction → two variables → products with negative exponents → a negative power of a monomial |
| EVAL | Evaluate powers | products of powers → zero and negative exponents → quotients → negative bases and sums → fraction bases → unit rational exponents → rational exponents m/n, negative |
| SCI | Scientific notation | large numbers → back to standard form → small numbers → negative exponents to standard form → fix a first factor over 10 → fix a first factor under 1 → which is largest |
| SCIOPS | Operations | multiply → divide → multiply and rewrite → divide with negative exponents → add or subtract → "how many times" → "how many times", rounded |

A simplified answer must be equivalent to the printed expression and fully simplified: one term (or one fraction of two
terms), each variable once, exponents 2 or more (positive only), reduced numbers and no variable on both levels.
Scientific notation answers must have a first factor with 1 ≤ a < 10; values are recomputed exactly from the printed numbers.

### Systems of Equations and Inequalities skills (tags GRAPH · SUBST · ELIM · APPLY · INEQ)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| GRAPH | Solutions and graphs | solve from a graph → is a point a solution? → graph with a fraction slope → how many solutions (graph) → is a point a solution (standard form) → how many solutions (equations) → the value of k for none / infinitely many |
| SUBST | Substitution | y = kx → y = mx + b → x isolated → isolate x → isolate y → fraction slope → fraction coefficient and fraction solution |
| ELIM | Elimination | opposite coefficients → equal coefficients → multiply one equation → multiply both → rearrange first → no solution / infinitely many / one → decimal coefficients |
| APPLY | Systems in context | sum and difference → ticket sales → write the system → when two plans cost the same → prices with cents → mixtures → boat and current |
| INEQ | Inequalities in two variables | is a point a solution? → inequality from a graph → a point in the solution of a system → is a point a solution of a system? → system from a graph → with a fraction slope → a system from a situation and a check |

Systems are solved again (exactly) from the printed equations, the two drawn lines, or the numbers in the story (each
equation of a story is described by references to the printed numbers). Half-planes are drawn from a spec (boundary,
dashed or solid, shaded side) and read back from the drawing: the boundary from the line, the side from the shaded
polygon. An inequality answer must describe the same half-plane (same line, same side, same strictness); "name a point in
the region" accepts any correct point.

### Linear Functions and Graphing skills (tags SLOPE · FORMS · WRITE · PARPERP · APPLY)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| SLOPE | Find slope | two points → fraction slopes → zero and undefined slopes → from a table → from a graph → a missing coordinate → are three points on one line? |
| FORMS | Slope-intercept, point-slope, standard form | slope and y-intercept → y = b + mx → point-slope to slope-intercept → standard to slope-intercept with the y-intercept → slope-intercept to standard → intercepts of Ax + By = C → point-slope to both forms |
| WRITE | Write the equation of a line | slope and y-intercept → horizontal or vertical line → slope and a point → two points → from a graph → point-slope form → standard form from two points |
| PARPERP | Parallel and perpendicular lines | parallel slope → perpendicular slope → parallel, perpendicular or neither → parallel line through a point → perpendicular line → given line in standard form → answer in standard form |
| APPLY | Linear models | a value from words → write the model → when does it reach a value → interpret slope and intercept → model from two data points → predict → rate, start and model together |

Every line is rebuilt from what is printed (two points, a slope read after the word "slope", a point, a given equation, the drawn
graph or table) and compared with the answer as a set of points; the requested form is then checked (slope-intercept,
point-slope using the given point, or standard form with integers, A ≥ 0 and no common factor). Models read the start value
and rate from the printed numbers and decide up or down from the words (drains, burns, adds, charges, …).

### Statistics and Data Modeling skills (tags CENTER · SPREAD · DISPLAY · TWOWAY · SCATTER)
| Tag | Skill | Level 1 → 7 |
|-----|-------|-------------|
| CENTER | Mean, median, mode, MAD | mean → median (even count) → MAD, a missing value → a dot plot (mean, median, mode) → a value added → compare two groups by MAD |
| SPREAD | Range, quartiles, IQR, outliers | range → IQR → five-number summary → outliers (1.5 × IQR) → mean or median? → effect of removing an outlier → fences |
| DISPLAY | Box plots | median → Q1 and Q3 → median, IQR, range → percent between values → compare two box plots (median, IQR, consistency) |
| TWOWAY | Two-way tables | joint and marginal relative frequency → complete a table → conditional relative frequency (by row, by column, rounded) → association |
| SCATTER | Scatter plots | correlation → line through two points → predict → residual → interpret slope and intercept → over/underestimate → line, prediction, residual and slope together |

New displays: dot plots, box plots, scatter plots (with real scales and an optional line) and two-way tables, each drawn
from a spec and read back from the drawing. Quartiles use the medians of the lower and upper halves, leaving out the
median when the count is odd (as on the TI-84). Rounding is accepted only when the problem prints the instruction.
Correlation is judged from the drawn points (r ≥ 0.6 positive, r ≤ −0.6 negative, |r| ≤ 0.3 none; anything in between is refused).
An association answer must quote both conditional percents; tables whose percents differ by 5–15 points are refused as too close to call.

**Gaps (not generated, use "Write your own"):** Statistics: standard deviation, histograms and computing least-squares regression.  Factoring: two variables (x² − 9y²) and sums/differences of cubes.  Exponential Functions: compound interest with several periods per year and continuous growth.  Relations and Functions: describing a curved graph in words.  Linear Inequalities: absolute-value *equations*. Foundations & Solving Linear Equations: error-analysis ("find the mistake") problems; percent
and absolute-value equations. A skill that cannot produce a verified problem at a requested difficulty is
flagged in red with a reason; it is never silently replaced.

## Tests
```
node worksheet-generator/menu/tests/math-tests.cjs     # default N=200; N=1000 for the large batch
node worksheet-generator/menu/tests/model-tests.cjs    # menu rules, versions, pin/regenerate, edit, bank, save/load
node worksheet-generator/menu/tests/browser-test.cjs   # Playwright + Chromium: teacher controls, PDFs, site links
sh worksheet-generator/menu/tests/run-all.sh
```

**`math-tests.cjs`** runs every skill × difficulty 1–7 × whole-number/fraction policy and checks that:
- every problem is re-verified independently
- formatting is clean (no `+-`, `1x`, `0x`, `\frac{n}{1}`, `\frac{a}{a}`)
- no answer appears in the question
- no duplicate is repeated within a menu
- difficulty 1–5 has whole-number answers

It also:
- tries thousands of wrong keys (off-by-one, sign flips, swapped classification, unsimplified answers, a changed printed number) and requires the verifier to catch every one
- requires an independent complexity score (computed from the printed math) to rise with the difficulty number
- checks structural promises (level 1 is one-step, `a(x+b)=c`, positive numbers, an LCD at level 5, …)

Last run with N=1000: 948,499 checks on 154,000 generated problems, 0 failures, 4,897/4,897 wrong keys caught.

**`browser-test.cjs`** does the following:
- builds CP2 and Honors menus and uses every control
- prints 12 PDFs (3 layouts × 2 versions × student/key) and checks that they are US Letter, that nothing overflows a page, that no answer or solution text appears in a student PDF, and that each key has one answer per offered dish
- checks that autosave, file save/open and tamper detection work, that there is no horizontal scrolling at tablet width, and that every control has an accessible name
- checks that the site still works: the unit page links the generator, the activity listings work, the existing generator and the PDF viewer load, and every file `data.js` references exists

Browser support: tested in Chromium (Chrome/Edge). Firefox and Safari print engines were not tested.

## Answer keys and the code-205 prompt
Keys are printed by the teacher and stay on the teacher's computer. The generator never publishes a key.
If you post a key on the site, link it through the activity viewer (`resource-details.js` → `answerKey`),
which shows the existing code-205 prompt. That prompt is a browser-side convenience, not security:
anyone who has the file's address can open a publicly hosted file.

## Adding a unit (Geometry, Algebra 2, other Algebra 1 units)
1. Create `menu/skills/<course>-<unit>.js`. Call `MKMENU.registerSkillSet({id, course, unit, unitName, title, tags,
   reference, gaps, skills:[…]})`, where `id` matches an entry in `engine.js → CATALOG`.
2. Each skill has `{id, tag, name, blurb, best:[tiers], generate(ctx)}`, where `ctx = {rng, c, intOnly, level}`.
   It returns `{variant, prompt, parts:[{label, prompt, answer, check}], steps:[{t, m, w}], space:[compact, standard, spacious]}`.
   Build answer-first and reject bad draws with `MKWS.gen.need(cond)`.
3. Every part needs a `check` that `verify.js` understands: `solve`, `classify`, `simplify`, `evaluate`,
   `literal`, `literal-eval`, `model-eq`, `scenario`. Add a new type to `verify.js` (and, if needed, a
   math capability to `mathcheck.js`) **before** adding a skill that needs it. Geometry will need figure
   checks: re-read the drawn SVG numbers the way `tests/math-audit.cjs` does for graphs.
4. Add the file's `<script>` tag to `menu-assessment.html`, add it to `tests/load.cjs`, and add the unit's
   entry to `data.js`.
5. Run the tests at N=1000 and fix the generator until there are 0 failures and difficulty rises with c.
