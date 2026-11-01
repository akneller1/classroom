# Geometry proof skills (Triangle Congruence, 2026-11-01)

Six skills in `worksheet-generator/menu/skills/geometry-triangles-congruence.js` (tag PROOFS). They appear in the
Worksheet Generator, Assessment Generator, Lesson Planner, practice pages and games for Geometry Unit 3.

| Skill id | Student task | Blanks by difficulty |
|---|---|---|
| `congruence-proof-missing-reason` | supply one missing reason | 1 (works as multiple choice and in the games) |
| `congruence-proof-reasons` | fill in the missing reasons | 2 (c1–2), 3 (c3–4), every reason (c5–7) |
| `congruence-proof-statements` | fill in the missing statements | 2, 3, up to 4 |
| `congruence-proof-mixed` | missing statements and reasons (never both in one row) | 2, 3, 4, every row |
| `congruence-proof-write` | write the whole two-column proof | empty numbered table |
| `congruence-proof-cpctc` | prove a pair of parts congruent (triangles first, then CPCTC) | mixed blanks (c1–5), whole proof (c6–7) |

From c5 up, about half of the one-reason, reasons, statements and mixed proofs end with a CPCTC step. The older
`congruence-structured-proof` (shared side / vertical angles, reasons only, solve for x) is unchanged.

**Diagrams.** The same six exact constructions as the Triangle Congruence Proofs activity: kite (reflection), bowtie
(half-turn), parallelogram with a diagonal, isosceles triangle with its median, overlapping triangles sharing an
angle, and translated triangles on a line. Criteria: SSS, SAS, ASA, AAS, HL. Each Given is marked with tick marks,
arcs, parallel arrows or a right-angle box. Easier difficulties use the simpler figures.

**Format.** The prompt has the form `Given: …; …. Prove: …. <instruction>`. `fig` is a `geo-cong` figure with
`fig.proof = { rows: [{ s, r, sb?, rb? }], write? }`. `sb`/`rb` hold a blank's letter, and each blank is one part.
`figHtml` draws the two-column table under the diagram, so every page that shows the figure also shows the table.
`NS.proofKeyFig(p)` fills in the blanks for answer keys, and the planner slides print the table rows as text.

**Checking.** `verify.js` handles `geo-proof-blank` and `geo-proof-write` (`NS.proofCheck`). It reads only the
printed Given/Prove text, the coordinates and the completed table, and checks that:

- every Given and the Prove statement are true in the drawing;
- every support row is true and its reason applies (Given, Reflexive, Vertical angles, Alternate interior or
  Corresponding angles from a given parallel, midpoint, angle bisector, perpendicular, Segment Addition);
- the rows give the named criterion for the named correspondence (SSA and AAA are rejected);
- the CPCTC row is the Prove statement and a pair of corresponding parts.

Typing is flexible: ≅ or "is congruent to", "angle" or ∠, "triangle" or △, any equivalent vertex order, support
rows in any order, and common reason wordings.

**Multiple choice.** Distractors come from `games/bank.js`, and each one is rejected by the checker before it is used:

- **Reason blanks:** the other standard reasons.
- **Whole-proof questions:** the correct proof with one flaw (wrong criterion, wrong vertex order, unsupported
  Given, or CPCTC used wrongly). These questions are reworded to "Which two-column proof is correct?".

**Planner.** U3-L6 uses the five proof skills plus the old one. U3-L7 adds `congruence-proof-cpctc`. To change
these mappings, edit `scripts/build_geometry_planner.py` and rerun it.

**Test.** `node worksheet-generator/menu/tests/geometry-proof-table-tests.cjs [n]`. It re-checks every generated
proof with its own reader, rejects mutated proofs and accepts loosely typed ones.
