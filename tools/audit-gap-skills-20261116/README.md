# Audit gap skills (2026-11-16)

Offline authoring tools for the ten skills added after the November 2026 site audit found
standards with no questions. Nothing here runs on the site.

| Course | Unit | New skill | Standard |
| --- | --- | --- | --- |
| 8th Grade Math | linear-functional-relationships | Proportional relationships, unit rate, and slope | 8.EE.B.5 |
| Pre-Algebra (Grade 7) | ratios-proportions-percentages | Rewriting Expressions in Context | 7.EE.A.2 |
| Algebra 2 | polynomial-functions | Binomial Theorem and Pascal's Triangle | A-APR.C.5 |
| Precalculus | functions | Solving Exponential and Logarithmic Equations | F-LE.A.4, F-BF.B.5 |
| Calculus | fundamental-theorem-calculus | Integration Using Long Division and Completing the Square | AP FUN-6.D |
| Statistics | statistical-inference | Chi-Square Goodness-of-Fit Tests | APSTATS.IV.B.6 |
| Statistics | statistical-inference | Chi-Square Tests for Homogeneity and Independence | APSTATS.IV.B.6 |
| Statistics | statistical-inference | Significance Tests for the Slope of a Regression Line | APSTATS.IV.B.7 |
| Geometry | right-triangles-trigonometry | Law of Sines and Law of Cosines | G-SRT.D.10, G-SRT.D.11 |
| Geometry | foundations-geometry | Conditional Statements, Converses, and Biconditionals | G-CO.C.9 |

Each skill has 48 items: 16 per level (7 short answer, 6 multiple choice, 2 error analysis,
1 four-part open response).

## Files

- `core.py` – the item contract shared by the families.
- `ms_families.py`, `hs_families.py`, `stat_families.py`, `geo_families.py` – the question families.
- `statements.json` – the conditional statements (with truth of the converse and a counterexample).
- `build.py` – registers the skills at the end of `course-catalog.js` and appends the items to the banks.
- `verify.py` – recomputes every answer from the printed problem and rejects every distractor and
  "student answer". It never imports the families. It must print `TOTAL ERRORS 0`.
- `fmt.py` – display-text helpers and evaluator (copied from `tools/hs-gap-skills-20261114/hsfmt.py`).
- `out/checks.json` – the data `verify.py` works from.

## Running

    python3 tools/audit-gap-skills-20261116/build.py .
    python3 tools/audit-gap-skills-20261116/verify.py .
    node scripts/build_standards_map.cjs
    node --test tests/audit-gap-skills.test.cjs

`build.py` skips skills that already have questions, so re-running it changes nothing. Needs
Python 3 with NumPy and SciPy, and Node.

## Review status

The site owner accepted these items as reviewed on 2026-11-16; their `sourceNotes` say
"Teacher reviewed 2026-11-16". Report any problem found later through the usual question fixes.
