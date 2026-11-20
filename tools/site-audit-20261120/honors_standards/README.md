# Whole-site audit 2, item #7 (2026-11-20): practice for honors-only standards

Offline authoring tools. Nothing here runs on the site.

Eight standards in Precalculus and Algebra 2 had no practice items. `build.py` adds 12 items per standard
(4 per level: short answer and multiple choice) to the closest existing skill:

| Course | Skill | Standard |
| --- | --- | --- |
| Precalculus | vectors skill 01 (complex solutions) | N-CN.C.8 |
| Precalculus | matrices skill 02 (matrix operations) | N-VM.C.9 |
| Precalculus | trigonometric functions skill 02 (unit circle) | F-TF.A.4 |
| Precalculus | probability skill 01 (expected value) | S-MD.A.2, S-MD.A.4 |
| Precalculus | probability skill 05 (decisions) | S-MD.B.6 |
| Algebra 2 | probability-statistics skill 06 | S-MD.B.6, S-MD.B.7 |

Geometry's two gaps (G-C.A.4, G-GPE.A.3) are generator skills in `worksheet-generator/menu/skills/geometry-circles.js`,
checked by `verify.js` (readers `tangent-ext` and `conic-foci`).

    python3 tools/site-audit-20261120/honors_standards/build.py    # safe to re-run
    python3 tools/site-audit-20261120/honors_standards/verify.py   # TOTAL ERRORS 0 (run in CI)
    node scripts/build_standards_map.cjs
