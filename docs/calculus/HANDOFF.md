# Calculus (`calculus`) question banks: integration handoff for ChatGPT

**Contents:** 9 units, 64 skills, **3,072 original questions**. Every skill has 48 questions: 16 CP2, 16 CP1 and 16 Honors. 148 questions carry a generated PNG diagram (graphs, conics, triangles, slope/area figures).

Every answer, every multiple-choice option and every open-response part was re-checked by an independent verifier that re-parses the **displayed text** with SymPy (it does not import the generators). Result: **0 errors**. The items still need **human subject-matter review** before students see them. No existing file in the repository is replaced except through the small patch below; no Algebra 1, Geometry, Algebra 2, Grade 6, 7 or 8 content is changed.

## 1. Files in this package (repository-relative paths)

| Path | Contents |
|---|---|
| `question-banks/calculus/<unit-id>.json` (9) | Banks in the existing schemaVersion 1 format |
| `question-banks/calculus/meta/<unit-id>.tags.json` | Per-question tags (existing tag vocabulary) |
| `question-banks/assets/calculus/<unit-id>/<question-id>.png` | Diagrams (`diagram.type: "image"`, non-empty `alt`) |
| `question-banks/manifest.calculus-additions.json` | 9 manifest entries with `"approved": false` — merge after review |
| `worksheet-generator/vocabulary-data-middle-grades.js` | Regenerated vocabulary file (Grades 6–7 unchanged; adds Precalculus and Calculus, 8–11 terms per unit) |
| `scripts/test-hs-bank-integration.cjs` | End-to-end test (`MG_COURSE=calculus MG_PREFIX=cal-`) |
| `patches/precalculus-calculus-integration.patch` | One patch for **both** courses (apply it once) |
| `tools/middle-grades-authoring/` | Generators (`pc_u0N.py`, `ca_u0N.py`), `hslib.py`, `hschecks.py`, verifier and report scripts |
| `docs/calculus/` | This handoff, `COVERAGE.md`/`.csv`, `ACTIVITY_COMPATIBILITY.md`, `VERIFICATION_REPORT.md`, `VALIDATION_LOG.txt`, `SKILL_MANIFEST.json` |

Unit IDs, skill IDs (`<unit-id>-skill-NN`) and skill names were read from the site's own `MK_COURSE_CATALOG.getSkillRecords('calculus', unitId)`. No skills were added, renamed or reordered.

## 2. Integration steps

1. **Copy the files** into the repository at the paths above (if you install both courses, copy both packages; the patch, vocabulary file, test and tools are identical in each).
2. **Apply the patch once:** `git apply patches/precalculus-calculus-integration.patch` (checked with `git apply --check` against commit 460f8c5). It touches:
   - `worksheet-generator/algebra2-bank-native.js`: adds `precalculus` and `calculus` to the courses whose authored banks may build **Tarsia** and **Error Analysis** printables (the list was hard-coded to the middle-grades courses).
   - `worksheet-generator/menu/course-catalog-bridge.js`: adds both courses to the generator's unit selector, so each unit appears as soon as its approved bank loads.
   - `worksheet-generator/planner/scope-algebra2.js`, `planner/course.js`, `planner/planner-ui.js`: register lesson-planner scopes `MKPLAN_SCOPE_PRECALCULUS` / `MKPLAN_SCOPE_CALCULUS` with the same catalog-driven code used for Algebra 2 and Grades 6–8. Unlike the middle-grades path, the high-school courses **keep the CP2 / CP1 / Honors labels**. Open with `planner.html#course=precalculus` (or `calculus`).
   - `worksheet-generator/vocabulary-data-middle-grades.js`: regenerated; the Grade 6 and 7 entries are byte-identical, and Precalculus and Calculus entries are appended (the file is already loaded by every vocabulary/flashcard page, so no page edits are needed).
   - `scripts/test-hs-bank-integration.cjs`: new end-to-end test (a copy of the Grade 6/7 test).
   - `tools/middle-grades-authoring/`: the generators, `hslib.py` (SymPy → site display text), `hschecks.py` (independent SymPy checks), and small fixes to `gbuild.py`, `gverify.py`, `glib.py`, `greport.py`, `vocab.py`.
3. **After human review**, merge `question-banks/manifest.calculus-additions.json` into `question-banks/manifest.json` and set `"approved": true`. Until then the loader keeps the banks hidden.
4. **Run the checks:**
   ```
   for f in question-banks/calculus/*.json; do node scripts/check-question-bank.cjs $f; done
   node scripts/test-published-question-banks.cjs
   MG_COURSE=calculus MG_PREFIX=cal- node scripts/test-hs-bank-integration.cjs
   MG_OUT=$PWD python3 tools/middle-grades-authoring/gverify.py calculus     # needs python3 + sympy + matplotlib
   ```

**Not changed on purpose (your call):** the homepage still shows Calculus as "Coming Soon" and its unit pages are the planned-course outline. Navigation, homepage components, thumbnails, styling and student-facing URLs were left alone as instructed. When you are ready to show the activities, the two places are the course list in `app.js` (the `['algebra', 'geometry', 'algebra2', 'prealgebra', 'prealgebra7', 'math6']` checks) and the per-unit resource listing in `data.js` — the same edits that were made when Grades 6 and 7 were published.

## 3. Results in a test copy of the repository

Full output is in `VALIDATION_LOG.txt`.
- Independent verifier: **0 errors** in 3,072 questions, including cross-unit duplicate and near-duplicate checks, display checks through `math-display.js`, and a check that every error-analysis "student answer" is actually wrong.
- Structural checker: PASS for every bank; `test-published-question-banks`: PASS (55 banks, 21,221 unique IDs).
- `test-hs-bank-integration`: 192/192 skill-level selections; 192 lesson plans; 27 Connect 4 decks (20 distinct single-answer items each); **189/189 printable builds** (Color by Number, Partner Check, Whodunnit, Stations, Error Analysis, Tarsia, Maze for every unit and level, 0 failures); 9 flashcard players in all three modes; every unit has 8+ vocabulary terms.
- The other repository tests give the same results before and after (Grade 6 regression test still passes). Escape Room already had unit-aligned cipher families for both courses in `games/cipher-questions.js`, so no change was needed there.

## 4. Content conventions

- **Fields:** `id, skillId, level, format, prompt, answer, solutionSteps, options, parts, diagram, standards, sourceNotes`; IDs look like `cal-<unit-abbr>-sNN-<level>-NNN`. `sourceNotes` names the problem family; families ending in `_error` are the error-analysis items.
- **Per skill and level:** 7 short-answer, 6 multiple-choice (4 options, one correct, positions balanced), 2 error-analysis items (a realistic mistake with its reason), and 1 open-response (4 independently checked parts) or select-all.
- **Display notation** (all run through `math-display.js`): fractions `a/b` render stacked; radicals `√3`, `(√3)/2`, `x√x`; powers with superscripts; `e^(2x)`; inverse trig `sin⁻¹`; intervals `(-∞, 3] ∪ (5, ∞)`; matrices `[1, 2; 3, 4]` (rows separated by semicolons); vectors `⟨3, -4⟩`; complex numbers `a + bi`; prime notation `f′(x)`, `y″`; limits `lim (x → 2⁺)`; integrals `∫ from 0 to 2 (3x² + 1) dx`; indefinite integrals end with `+ C`. Division in prose uses `÷`.
- **Rounding:** every approximate answer states the place value (nearest tenth, thousandth, cent, degree); calculator items say which mode.
- **Distractors** are documented misconceptions (sign errors, wrong quadrant, forgetting the chain rule factor, product-of-derivatives, c² = a² + b² for an ellipse, displacement vs. distance, using p instead of 4p, etc.).
- **Levels differ in substance:** CP2 uses direct one-rule items; CP1 adds context, fractions and multi-step setups; Honors adds compound rules (chain + product, u-substitution, both-bounds variable FTC, ambiguous case, 3×3 systems, nonlinear and logistic models, Euler equations).

## 5. Limitations and judgment calls

- **Human review is still required**, especially wording and the diagram set. Claude looked at samples from every diagram family, not every image.
- **Authored-key items:** 107 conceptual multiple-choice items (theorem names, interpretations, justifications, classifications) are checked against an authored key, not recomputed.
- **Mixed review units** (Calculus Unit 4 skill 11 "Midterm Review" and Unit 9 "AP Review") reuse verified families from earlier units with new random seeds; the items are new but structurally familiar.
- **Activity-friendly families.** A few short families exist mainly so Tarsia (18 different short answers) and Partner Check (two different problems with the same answer) can build at every level — e.g. focal distances and axis lengths in conics, Pythagorean-triple magnitudes in vectors, expected counts in probability, slope-field values in differential equations. They are on-topic for their skills.
- **Partner Check quirk (existing code, not changed):** when a unit has a multiple of 3 skills, each skill only contributes items from one difficulty third. The banks were tuned so the build still succeeds; the code itself was not modified.
- **Topics covered** include limits (algebraic, one-sided, at infinity), continuity, derivative rules, tangent lines, related rates, optimization, motion, MVT, Riemann and trapezoidal sums, FTC (both parts, with the chain rule), area and volume, Euler's method, separable and initial-value differential equations.
