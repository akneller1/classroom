# Algebra 2 audit, batch D (2026-11-17)

Offline authoring tools for the Algebra 2 audit items #4–#7. Nothing here runs on the site.

New skills (16 items per level: 7 short answer, 6 multiple choice, 2 find-the-mistake, 1 four-part open response):

| Unit | Skill | Standard |
| --- | --- | --- |
| functions-transformations (skill 09) | Comparing functions in different representations | F-IF.C.9 |
| functions-transformations (skill 10) | Parametric equations | F-IF.C.10 |
| linear-functions-systems (skill 08) | Solving f(x) = g(x) with graphs and tables | A-REI.D.11 |
| exponential-logarithmic-functions (skill 09) | Interpreting the structure of expressions | A-SSE.A.1a, A-SSE.A.1b |
| probability-statistics (skill 09) | Simulation and evaluating models | S-IC.A.2 |
| probability-statistics (skill 10) | Randomized experiments and comparing treatments | S-IC.B.5, S-IC.B.3 |
| probability-statistics (skill 11) | Evaluating reports based on data | S-IC.B.6 |

Context problems (9 per level per unit, ids ending `-w###`, tagged `modeling` and `context-problem`) were added to an
existing skill in linear functions, quadratics, polynomials, radicals, rational functions, conics (parabolas and
circles), sequences and trigonometry. Contextual items in the new skills carry the same tags.

`move_tags.py` moves A-REI.D.11 off the 51 algebraic substitution items (they keep A-REI.C.6).

## Files

- `families.py` – the question families (uses `core.py` and `fmt.py` from `tools/audit-gap-skills-20261116`).
- `build.py` – registers the skills at the end of `course-catalog.js` and appends items and tags. Skips what already exists.
- `verify.py` – recomputes every answer, option and student answer from `out/checks.json` with its own formulas and checks
  that the parameters are printed in the prompt. Must print `TOTAL ERRORS 0`.
- `move_tags.py` – the A-REI.D.11 tag move (idempotent).

## Running

    python3 tools/algebra2-gaps-20261117/build.py
    python3 tools/algebra2-gaps-20261117/move_tags.py
    python3 tools/algebra2-gaps-20261117/verify.py
    node scripts/build_standards_map.cjs
    node scripts/test-algebra2-gap-skills.cjs

The site owner accepted these items as reviewed on 2026-11-18; their `sourceNotes` say "Teacher reviewed 2026-11-18". Report any problem found later through the usual question fixes.
