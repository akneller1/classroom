# Geometry parity audit — 2026-10-27

Reference: Algebra 1 implementation in `data.js`, `worksheet-generator/menu/engine.js`, and the shared worksheet/activity pages. This is a repository-level inventory, not a full visual or mathematical QA certification.

## Current catalog
- Algebra 1: 12 units, 232 catalog entries.
- Geometry: 10 units, 131 catalog entries.
- Geometry catalog: no missing local primary activity paths or thumbnail targets found in the current main-branch tree. This does not prove internal links, answer-key security, correct mathematics, or print layout.
- Geometry is already public; leave Algebra 2 hidden until ready.

## Most significant findings
1. **Missing whole unit:** Quadrilaterals and Polygons has **zero** catalog entries, despite being in the course navigation. This is the clearest release-quality gap.
2. **Curriculum mismatch:** The Geometry course page has 10 units, but the generator's `NS.CATALOG` lists only 8 older skill-bank units: Basics & Reasoning; Angles & Parallel Lines; Triangles & Congruence; Similarity; Right Triangles & Trigonometry; Circles; Area/Surface Area/Volume; Coordinate Geometry & Transformations.
3. **Unrepresented in generators:** The current 10-unit syllabus separates **Triangle Relationships** and **Quadrilaterals and Polygons**; neither has its own corresponding menu skill bank. The old single "Coordinate Geometry & Transformations" generator unit does not necessarily match the current **Transformations** unit's intended scope.
4. **Uneven coverage:** Triangle Congruence has 9 catalog entries and Triangle Relationships has 7, while several other Geometry units have 16–17. Quadrilaterals and Polygons has none.
5. **No Algebra 1 parity yet:** Algebra 1 unit cards consistently offer Assessment Readiness Check, Daily Lesson Planner, Worksheet Generator, Assessment Generator and multiple printable generators. Geometry cards predominantly point to older games and static PDFs, and don't yet expose that same organized tool suite.
6. **Legacy printables:** Existing Geometry maze, stations, cheat sheet, partner check, color-by-number, and assessment PDFs should be inventoried and eventually replaced by verified generator-native content where appropriate. Do not indiscriminately delete source PDFs before a validated replacement exists.
7. **Test coverage:** Existing GitHub Actions checks mostly cover shared Algebra 1 workflows. Geometry requires its own lesson/skill coverage test, question verification tests, diagram-label consistency checks, worksheet print QA and end-to-end browser checks.

## Reuse plan (ChatGPT / Claude)
- **Reuse first:** shared worksheet menu UI, question formats, level controls (CP2/CP1/Honors), export/print styling, vocabulary banks, teacher-key access flow, and regression infrastructure.
- **Do not transplant blindly:** Algebra 1 skill-bank math, numeric distractor assumptions, inequality-only select-all logic, and Algebra-oriented validators.
- **Claude's diagram-heavy contribution:** independently defined SVG-based geometry diagram components and geometry question families (angles, triangles/congruence, similarity, quadrilaterals, circles, trig) with accompanying mathematical invariants.
- **Integration + verification:** treat diagram geometry and question answers as the same source of truth; verify random generations and inspect printable pages.

## Phased work, in order
1. Align the generator curriculum registry with the 10 published Geometry units and make unsupported units explicitly unavailable; never silently map to unrelated question banks.
2. Build missing skills for Triangle Relationships, Quadrilaterals and Polygons, and the intended Transformations scope.
3. Add Geometry-specific diagram/data schema with validated lengths, angles, orientation, labels, and nondegenerate constructions.
4. Add reusable Algebra 1-style cards for generators **only after** each intended Geometry unit is supported and its tests pass.
5. Expand unit-specific question banks and games; retire outdated static PDF cards as replacements are checked.
6. Complete test, browser, accessibility, print and answer-key audits before calling Geometry complete.

## Current unit inventory (catalog entries)
| Geometry unit | Entries |
|---|---:|
| Foundations of Geometry | 16 |
| Angles and Parallel Lines | 16 |
| Triangle Congruence | 9 |
| Triangle Relationships | 7 |
| Similarity | 16 |
| Right Triangles and Trigonometry | 17 |
| Quadrilaterals and Polygons | 0 |
| Transformations | 16 |
| Circles | 17 |
| Area, Surface Area and Volume | 17 |

## Ship criteria
A Geometry unit is at Algebra 1 parity only if: skill coverage matches its actual lesson map; generators produce verified math and diagram-dependent answers; no broken local or internal links; layouts work on phone/tablet/print; the answer key is consistent and locked; and the unit has standardized navigation and resource categories.
