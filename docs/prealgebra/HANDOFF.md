# Pre-Algebra (Grade 8) question banks — integration handoff

Course `prealgebra`, 7 units, 58 skills, **3,480 questions** (60 per skill: 20 Remedial `cp2`, 20 Standard `cp1`, 20 Advanced `honors`). All items are original, Claude-authored, and **awaiting human subject-matter review**. No existing file was modified.

## 1. Files added (repository-relative)

| Path | Contents |
|---|---|
| `question-banks/prealgebra/<unit-id>.json` (7) | Banks in the existing schemaVersion 1 format |
| `question-banks/prealgebra/meta/<unit-id>.tags.json` (7) | Per-question tags, using only the existing Algebra 2 tag vocabulary (`graph`, `error-analysis`, `misconception`, `modeling`, `reasoning`, `challenge`, `connections`, `multiple-representations`, `multistep`) |
| `question-banks/assets/prealgebra/<unit-id>/<question-id>.png` (608) | One generated diagram per diagram question (`diagram.type: "image"`, non-empty `alt`) |
| `question-banks/manifest.prealgebra-additions.json` | Manifest entries to merge **after** approval (not merged) |
| `tools/prealgebra-authoring/` | Deterministic authoring scripts, independent verifier, reports, and `out/*.checks.json` verification specs |
| `docs/prealgebra/` | This handoff, `COVERAGE.csv`, `ACTIVITY_COMPATIBILITY.csv`, `COMPATIBILITY_SUMMARY.md`, `VERIFICATION_REPORT.md`, `CHECKPOINT.md` |

Unit IDs (confirmed against `data.js` / `MK_COURSE_CATALOG.getSkillRecords`): `real-numbers-exponents` (11 skills, 660 q), `equations-expressions` (8, 480), `linear-functional-relationships` (11, 660), `systems-linear-equations` (6, 360), `patterns-bivariate-data` (6, 360), `congruence-similarity` (9, 540), `geometry-applications` (7, 420). Skill IDs were read through the site's own `getSkillRecords`; no skills were added, renamed or reordered.

## 2. Required changes before students see the content (left to ChatGPT)

1. **Manifest.** `question-bank-loader.js` loads non-Algebra 2 banks only with `approved: true`. After human review, merge the 7 entries from `question-banks/manifest.prealgebra-additions.json` into `question-banks/manifest.json`. They are written with `"approved": false`; flip to `true` only after review (per `docs/CLAUDE_QUESTION_BANK_HANDOFF.md`).
2. **No catalog/skill registrations are needed**; all skillIds already exist.
3. **Algebra 2–specific hooks that must be generalized** for the bank-native printable/menu path (they test `/^algebra2-/` or `courseId:'algebra2'`):
   - `worksheet-generator/menu/printables.js` lines ~109–110, 220, 330, 525 (authored-format selection for maze/Who/Tarsia, used-set handling, partner minimum, honors maze/tarsia rule). Prealgebra set ids are `prealgebra-<unit-id>`; test `NS.skillSets[id].authoredBank` instead.
   - `worksheet-generator/menu/printables-ui.js` ~542 (hint text).
   - `worksheet-generator/algebra2-bank-native.js` already registers any course whose bank is `available()`, but its skill blurb says "Algebra 2 bank" and `MK_COURSE_BANKS_READY` naming is Algebra 2–centric.
   - `bank-printable.js`, `algebra2-practice.js`, `algebra2-quest.js` (Detective/Escape), `practice/practice.js` hard-code `courseId:'algebra2'`; parameterize by course (`games/course-source.js` is already course-neutral).
4. Grade 8 labels: show `cp2/cp1/honors` as **Remedial/Standard/Advanced** (the loader/adapters keep the internal codes; `docs/CLAUDE_QUESTION_BANK_HANDOFF.md` confirms the mapping).

## 3. Content conventions

- Fields used: `id, skillId, level, format, prompt, answer, solutionSteps, options, parts, diagram, standards, sourceNotes` — all allowed by `schemas/question-bank.schema.json`. IDs: `pa8-<unit-abbr>-s<NN>-<level>-<NNN>` (globally unique; checked across all banks including Algebra 2).
- Per skill and level: ≥10 short-answer, ≥8 multiple-choice (4 options, one correct, correct positions balanced: A/B/C/D/E overall 400/391/363/367/1; 5-option items are the fixed set-classification lists), plus 2 extras (select-all with ≥2 correct and ≥1 incorrect, open-response with ≥4 parts, or an error-analysis item). Every skill has ≥5 problem families (`COVERAGE.csv`).
- **Answers are strings** (the native games require string short answers; `GB.answerOk` compares strings exactly). Select-all `answer` is the list of correct option texts; open-response `answer` joins the part answers `(a) …; (b) …`.
- **Math text** follows the site display layer (`worksheet-generator/core/math-display.js`): fractions are written `a/b` (or `(a/b)x`) and rendered as stacked fractions; the verifier ran every student-facing string containing `/` through the site's own `MK_MATH_DISPLAY.fractions` and rejected any slash that survived or produced a malformed fraction (e.g. `√a/b`, exponents captured in a numerator). Division of expressions uses `÷` with parentheses. Exponents use Unicode superscripts; roots `√`, `∛`; `π`; repeating decimals `0.4545… (45 repeats)`; non-repeating `1.1010010001… (pattern never repeats)`; scientific notation `3.2 × 10⁵`.
- Rounding/exactness is stated in every prompt that needs it ("in terms of π", "use 3.14 for π and round to the nearest tenth", "exact value", "nearest tenth"). Radius vs diameter and unit squares/cubes are explicit.
- Error analysis is carried in the existing structure: the prompt shows a student's incorrect work (or claim) and asks for the first wrong step or the correct result; `solutionSteps` explain the error. 137 items carry the `error-analysis` tag. The verifier confirms step-based errors really change the solution set at the stated step.

## 4. Existing consumers and compatibility (see `COMPATIBILITY_SUMMARY.md`, per-question flags in `ACTIVITY_COMPATIBILITY.csv`)

| Consumer | Uses | Grade 8 questions eligible |
|---|---|---:|
| Lesson plans, worksheets, assessments, Readiness Checks (bank-native generators) | all formats | 3,480 (auto-grading only for MC: 1,522) |
| Showdown | all formats | 3,480 |
| Flashcards (bank-native deck) | SA + MC | 3,269 |
| Connect 4, Tic-Tac-Toe, Picture Reveal, Detective, Escape Room | MC; `approved-game-items.js` also excludes diagram items | 1,184 text-only MC (MC with diagrams: 338 more for decks that render images) |
| Maze (MC, prompt ≤92, answer ≤14, no figure) | | 551 |
| Color-by-number | SA/MC, prompt ≤170, answer ≤30 | 2,910 |
| Partner Check (pairs of different prompts with the same answer, same level) | | 1,036 items in 246 answer-sharing groups (no duplicated prompts) |
| Whodunnit (MC, ≤150/≤30) | | 1,250 |
| Stations (≤260/≤60) | | 3,186 |
| Tarsia (MC, "Evaluate/Simplify/Solve …" ≤22 chars, answer ≤12) | | 56 (units 1–2 only) — **limited**; most Grade 8 prompts are longer |
| Error Analysis printable | needs generator steps with a marked mistake (`s.m`) | **0** — not representable by authored banks (same limitation as Algebra 2) |
| Vocabulary activities | — | not supplied; the bank schema has no vocabulary/definition fields |

Limitations: `approved-flashcards.html` renders prompts with `textContent` and its `.af-prompt` class is not in the math-display selector list, so `a/b` and superscripts show as plain text there (the bank-native flashcard deck uses the formatter). Mazes for `patterns-bivariate-data` are nearly impossible because its prompts carry data sets.

## 5. Validation commands and results (actual)

```
node scripts/check-question-bank.cjs question-banks/prealgebra/<unit>.json   # all 7: PASS
python3 tools/prealgebra-authoring/verify.py                                  # TOTAL ERRORS 0 (3,480 questions)
python3 tools/prealgebra-authoring/report.py                                  # coverage + compatibility
```
With the 7 entries temporarily added to a **test copy** of the manifest as approved: `test-published-question-banks.cjs` PASS (18 banks, 6,197 unique IDs, all images present); `test-question-bank-adapter.cjs`, `test-question-bank-loader.cjs`, `test-resource-eligibility.cjs`, `test-approved-game-items.cjs` PASS. `test-approved-flashcards.cjs` fails on the **unchanged** repository too (it rejects the existing Algebra 2 `teacherUse` entries) — pre-existing.

JSON Schema (`schemas/question-bank.schema.json`, Draft 2020-12) passes for every non-diagram item. Its `diagram.spec.src` pattern contains a double-escaped dot (`\\\\.`), so **no** image path can match it — existing Algebra 2 banks fail the same way; the runtime adapter's regex is correct. Suggest fixing the schema pattern to `\\.`.

Independent mathematical verification (`verify.py`, `mathtext.py`, `checks_custom.py`; these do not import the authoring families): it parses the student-facing text and recomputes. Methods: exact-fraction expression evaluation (482), substitution into parsed equations (160 linear, 89 systems), expression equivalence at sample points (124), rounding checks (71), and 2,443 custom recomputations (transformations re-applied from parsed descriptions with rotation/reflection matrices, angle measures from transversal geometry, correlation/quadratic-fit for associations, least-squares for best-fit choices, two-way-table totals, root scanning for nonlinear equations, repeating-decimal series values, symbolic a + b√n rationality). Every MC/select-all option's truth was recomputed and compared with its `correct` flag; MC options were checked distinct after simplification; open-response parts: 240/240 checked. Prompt duplicates were checked within and across units (none). The verifier caught and forced fixes of real defects during authoring (e.g. a missing ×10² in a water-use context, a radius/diameter-style distractor equal to the answer, ambiguous `a ÷ bxⁿ` monomials, a "multiply both equations by 2" option that actually worked).

Honest limits: 51 conceptual items (always/sometimes/never, causation vs association, property statements) and some open-response explanation parts are checked against an authored key rather than recomputed. Diagram images are generated from the same data as the answers; I reviewed representative images from every diagram family visually, not all 608. Some families with small natural pools (e.g., story-graph matching, cluster description) repeat a structure with different data. Human review is still required before `approved: true`.

## 6. Ambiguous catalog labels (kept, flagged)

- *Expressions with radical exponents* — interpreted as expressions combining radicals and integer exponents (evaluating, simplifying √(k²x²ⁿ), ∛, inverse operations, √(x²) = |x|). Rational-exponent notation was not introduced.
- *Solving exponent equations* — x² = p and x³ = p with prior steps, no-real-solution cases, (x + h)² = k², and same-base equations such as 2ˣ = 32 at Advanced only.
- *Operations with rational numbers* uses 7.NS standards as Grade 8 review.
- Algebra 1/Geometry content in this repository is procedural JavaScript generators, not static banks, so no items were copied; all 3,480 items count as original coverage.

## 7. Reproduce

```
cd tools/prealgebra-authoring
PA8_REPO=<repo root> PA8_OUT=<repo root> python3 build.py      # deterministic; rebuilds banks, tags, PNGs, checks
PA8_REPO=<repo root> PA8_OUT=<repo root> python3 verify.py
PA8_REPO=<repo root> PA8_OUT=<repo root> python3 report.py
```
Requires Python 3.10+ with numpy and matplotlib, and Node (for the site's catalog and math-display code).
