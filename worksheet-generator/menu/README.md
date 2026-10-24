# Menu Assessment Generator

A browser-only builder for restaurant-style choice assessments ("Assessment Menus"). It has no server, no
accounts and no paid services, so it runs on GitHub Pages. Open `worksheet-generator/menu-assessment.html`.

**Pilot status:** Algebra 1 · Expressions & Equations is fully supported. Other units appear in the unit
list as "not yet supported" until they have generators that pass the same verification tests (see
*Adding a unit*). The existing static Assessment Menu PDFs are unchanged and still listed on every unit page.

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

**Gaps (not generated, use "Write your own"):** error-analysis ("find the mistake") problems; percent
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
