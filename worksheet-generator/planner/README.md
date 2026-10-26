# Daily Lesson Planner (`worksheet-generator/lesson-planner.html`)

Plans any of the 180 Algebra 1 days from the scope and sequence. Open `lesson-planner.html#day=<n>` or
`#unit=<skill set id>` (the unit's first day). Optional `&level=cp2|cp1|honors`, `&seed=<s>`, `&view=plan|student|key`.

**Each day has three views:**
- **Plan:** standards, objectives, sentence frame, vocabulary, the misconception to watch for, a timed agenda, generator coverage notes, links to the unit's generators, and every problem with its answer and a *New problem* button.
- **Student handout:** one printable packet with Do Now, Notes, Practice and a cut-off Exit Ticket.
- **Teacher key:** the plan page, then every answer with worked steps.

## Teacher options
- **Minutes:** the Plan view's agenda has a minutes box for each part, with a running total. Typed times are kept in this browser for every day of the same type (one timing for Lesson days, one for Quiz days…). *Reset to the planned times* clears them. The handout, the key and the slides show the edited times; the problems do not change.
- **Student notes:** *As planned* (pre-filled only where the scope's `notes_style` says "Pre-filled"), *Students write them in*, or *Pre-filled*. Pre-filled prints each vocabulary word's definition, the key idea, the misconception and Examples 1–2 worked out; *You try* stays blank. Fill-in leaves blanks; exploration lessons also get "I notice / I wonder". The definitions and key ideas (`notes-content.js`) are always on the plan, the key and the slides.
- **Editable notes:** on a Lesson day the Plan view's Notes section is an editor. You can change the key idea, change, add or remove vocabulary words and their meanings, edit the "watch out" mistake, and add your own notes. Edits are saved per lesson in this browser (`mk-planner-note-edits`). They are used on the handout, the key, the slides and the review-day reference tables. *Reset to the original notes* removes them.
- **Download PowerPoint:** a widescreen deck (`pptx-export.js`, pptxgenjs loaded on demand from `vendor/pptxgenjs/`). It has a title slide with "Today I can…", the agenda, then each part of the day. Every problem slide is followed by its answers (worked steps for examples, *We do* and Tier 1 reteach). Vocabulary cards show definitions. Quizzes and tests get a directions slide plus answer slides for going over them. Teacher notes and answers are also in the speaker notes. Problems are editable text: `textmath.js` turns the TeX into Unicode (x², (1/2)x, ≤, √(…)). Graphs, number lines and plots are pictures, and tables are PowerPoint tables.

## Files
| File | Job |
|------|-----|
| `algebra1_scope_sequence.json` | Andrey's 180-day scope and sequence (source of truth). |
| `scope-algebra1.js` | Generated from the JSON by `scripts/build_planner_scope.py`. Rerun the script after editing the JSON. |
| `lesson-skills.js` | Lesson id → verified skills (`[set, skill, cmin, cmax]`) and coverage (`full` / `partial` / `none` + a note for the teacher). |
| `planner.js` | Engine (no DOM). `MKPLAN.buildDay(day, {level, seed, practice})` → sections → groups → problems. |
| `notes-content.js` | Definitions for every key-vocabulary word (`MKPLAN.define`, with per-unit meanings such as *range* or *standard form*) and a key idea per lesson (`MKPLAN.keyIdea`). |
| `textmath.js` | `MKPLAN.mathText`: TeX between ⟨…⟩ → plain editable text, for the slides. |
| `pptx-export.js` | `MKPLAN.buildDeck(plan, PptxGenJS, {figImage})` and `MKPLAN.exportPptx(plan)` (browser download). |
| `planner-ui.js`, `planner.css` | Page, handout and key. |

## How a day is built
- Problems come from the same verified generators as the Worksheet and Assessment Generators (`MKMENU.generateProblem`). Each answer is re-derived from the printed problem, and no problem repeats within a day. A problem that cannot be verified shows as a flagged slot; nothing is quietly substituted.
- Difficulty comes from the class level (CP2 = c 1/2/3, CP1 = 3/4/5, Honors = 5/6/7), clamped to each lesson's `cmin–cmax` range. For example, U2-L1 one-step equations uses only c = 1.
- **Do Now:** draws on `do_now_source_ids`, with about one spiral problem from `spiral_review_ids`, at the level's easiest tier. If no source is listed, it falls back to the previous lesson, or for review-type days to the lessons covered.
- **What each day type gets:**
  - **Lesson:** 2–3 examples (I do / we do / you try; 2 for pre-filled notes), *We do* 2, *You do* (practice count − 2, easier → harder), exit ticket 2 plus the sentence frame.
  - **Practice:** Level 1/2/3 sets and a self-assessment.
  - **Quiz:** 12 problems.
  - **Review:** a study guide and one station per lesson.
  - **Assessment:** a 16-problem test. The Assessment Generator makes A–C versions.
  - **Flex:** corrections table, Tier 1 reteach and enrichment.
  - **Exam Review:** 4 problems per unit.
  - **Exam:** 2 problems per unit.
  - **Diagnostic:** 12 readiness problems.
  - **Launch / Project:** fixed tasks, with no generated problems.
- **Lessons the generators do not fully cover** (marked `partial` or `none`) carry a note telling the teacher what to add. The note appears in the plan and on the key. `none` lessons still practice a related skill.

## Tests
- `tests/planner-tests.cjs`: every lesson is mapped. Every mapped skill works at every c in its range for every level. Every day × level × seed builds with verified, non-repeating problems and the right sections. `SEEDS=n`.
- `tests/planner-browser.cjs`: all 180 days in all three views, with no script errors, no unverified problems and no sideways scroll; also checks the controls, `#unit=`, and phone width.
- `tests/pptx-tests.cjs`: every word has a definition and every lesson a key idea. Every problem converts to plain text with no TeX left (~55,000 strings). Minutes and notes settings work in the engine. Every day builds a deck with no TeX, a title slide, an agenda, answer slides and the key idea. Uses `pptxgenjs` from npm and skips the deck build without it.
- All three run from `menu/tests/run-all.sh`.
