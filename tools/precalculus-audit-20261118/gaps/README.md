# Precalculus audit, batch P4 (2026-11-18)

Offline authoring tools for Precalculus audit item #4 (standards with no items). Nothing here runs on the site.

New skills (16 items per level: 7 short answer, 6 multiple choice, 2 find-the-mistake, 1 four-part open response):

| Unit | Skill | Standards |
| --- | --- | --- |
| functions (skill 19) | Rational Expressions and Partial Fractions | A-APR.D.7, A-APR.D.6 |
| functions (skill 20) | Verifying Inverses and Restricting Domains | F-BF.B.4b, F-BF.B.4c, F-BF.B.4d |
| vectors (skill 12) | Complex Conjugates, Moduli, and Quotients | N-CN.A.3 |
| vectors (skill 13) | Products, Powers, and Roots in Polar Form | N-CN.B.5 |
| vectors (skill 14) | Limaçons and Cardioids | APPC.3.14, APPC.3.13 |
| sequences-series-limits (skill 06) | The Binomial Theorem | A-APR.C.5 |
| sequences-series-limits (skill 07) | Continuity and One-Sided Limits | F-IF.C.7b, F-IF.C.7d |

## Files

- `families.py` – the question families (uses `core.py` and `fmt.py` from `tools/audit-gap-skills-20261116`).
- `build.py` – registers the skills at the end of `course-catalog.js` and appends items and tags. Skips what already exists.
- `verify.py` – recomputes every answer, option and student answer from `out/checks.json` with its own formulas,
  reads the keyed text back with `../mathx.py`, and checks that the parameters are printed in the prompt.
  Must print `TOTAL ERRORS 0`. CI runs it in the Precalculus bank job.

## Running

    python3 tools/precalculus-audit-20261118/gaps/build.py
    python3 tools/precalculus-audit-20261118/gaps/verify.py
    python3 tools/precalculus-audit-20261118/build_notes.py
    node scripts/build_standards_map.cjs
    node scripts/test-precalculus-gap-skills.cjs

The site owner accepted these items as reviewed on 2026-11-18; their `sourceNotes` say "Teacher reviewed 2026-11-18".

## Context problems (#5) and question variety (#6)

- `contexts.py` – real-world context families. `build.py` adds 9 per level to one skill in every unit
  (ids ending `-w###`, tagged `modeling` and `context-problem`), plus 6 per level for the Law of Sines
  (triangle trigonometry skill 02) and infinite geometric series (sequences skill 03).
- `variety.py` + `replace.py` – in 21 skills one question template made up 40% or more of the items. `replace.py`
  swaps the excess (short answer and multiple choice only) for items from new families that fit the skill,
  keeping each item's id, level, format and standards, until no template is above 35%. Re-running is safe.

    python3 tools/precalculus-audit-20261118/gaps/build.py      # new skills, then context problems
    python3 tools/precalculus-audit-20261118/gaps/replace.py    # question variety
    python3 tools/precalculus-audit-20261118/gaps/verify.py     # TOTAL ERRORS 0
