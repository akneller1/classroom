Fix the Discrete Math Honors sequences Partner Check shortage using the attached current-source reference bundle.

Repository: https://github.com/akneller1/classroom
Live site: https://akneller1.github.io/classroom/
Snapshot commit: 0953f0b9972ebb13ea6234f8f723ac2bd291af1e

Scope
- Course: Discrete Math
- Unit 4: Sequences, Mathematical Induction, and Recursion
- Unit id: sequences-induction-recursion
- Generator set id: discrete-sequences-induction-recursion
- Current unit bank: 273 questions (92 CP2, 91 CP1, 90 Honors).
- Preserve the current website layout completely.

Problem
The Partner Check generator needs two different questions with the same verified answer for each row, and different rows must not share answers. The current Honors pool does not reliably supply enough matching pairs. A confirmed failure is:
  discrete-sequences-induction-recursion/honors/seed 1:
  partner check substituted another level
from scripts/test-partner-check-pairs.cjs using cfg.seed = 'pair-1'.

The generic printable builder can fall back to CP1 after unsuccessful attempts. Disabling that fallback alone makes this Honors activity unavailable; that is NOT a complete fix.

Required work
1. Read the existing bank schema, generator, source helpers, and tests before editing.
2. Add deliberately matched, mathematically distinct Honors companion questions for this unit. Aim for at least 12 distinct shared-answer groups so eight valid rows can be sampled reliably across seeds. Spread them across suitable sequences/recursion/induction skills.
3. Keep the questions genuinely Honors level. Use substantive reasoning such as recurrences, explicit formulas, sums/products, induction, Fibonacci patterns, or equivalent unit content as appropriate. Do not relabel easy CP1 problems as Honors.
4. Each pair needs different prompts and independently correct worked solutions with matching answer strings accepted by the existing engine. Avoid duplicate or near-identical questions. Preserve unique IDs, skill IDs, level, difficulty, answer format, and schema conventions.
5. Update tools/discrete-math/bank/u04_sequences.py (and a helper only if necessary), then regenerate question-banks/discrete/sequences-induction-recursion.json. The bank must be reproducible from source. Preserve existing questions and other levels unless a genuine error is identified.
6. Prefer fixing the question pool. Do not redesign the generator or change unrelated activities. Do not pass tests by hiding the activity, returning empty worksheets, lowering the level, weakening assertions, or suppressing coverage checks.
7. Independently verify the answers, each pairing, uniqueness across rows, and difficulty. Show that the default whole-unit Honors Partner Check produces eight valid same-level rows for at least 20 deterministic seeds, including pair-1 through pair-20.
8. Run the included Discrete Math bank checks, Partner Check checks (at least five seeds per selection), and Discrete Math integration checks. Preserve CP2/CP1 behavior and all other activities fed by the bank. Check both the student pages and teacher keys when browser testing is available. Report any testing limitation accurately.
9. Update legitimate expected question totals and coverage reports after additions. Do not remove minimum coverage or independent answer checks. If another failure predates your changes, distinguish it and include evidence.

Deliverables
- A minimal ZIP with changed files at their original repository-relative paths.
- A short installation note, counts before/after, number of new Honors pairs, and exact tests/results.
- No homepage/layout/style/navigation files. Preserve the current rainbow cards, very pale Teacher Guide, nine-card grid, reduced gaps, Seating Chart tool, and standards on teacher materials.
- Do not upload or push anything to GitHub. Claude should return the files; ChatGPT will install them.
- Do not include unrelated reference files in the update ZIP.

Start with the target bank and u04_sequences.py; use the other files only as needed. This bundle omits the large fixed-activity PDFs and most unrelated diagrams. It is a testing/reference subset, not a replacement for the full site.
