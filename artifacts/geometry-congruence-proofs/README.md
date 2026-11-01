# Triangle Congruence Proofs (Geometry · Triangle Congruence)

Interactive two-column proofs. A set has 12 proofs in five stages:

| Proofs | Stage | Student task |
|---|---|---|
| 1–3 | 1 | Drag statements into place (reasons given) |
| 4–5 | 2 | Drag reasons into place (statements given) |
| 6–8 | 3 | Drag statements and reasons (proof 8 adds a CPCTC row) |
| 9–10 | 4 | Write the proof, no word bank |
| 11–12 | 5 | Write a CPCTC proof, no word bank |

- `proofs.js` builds every diagram from an exact construction (reflection kite, half-turn bowtie, parallelogram with diagonal, isosceles with median/altitude/bisector, overlapping shared-angle triangles, translated triangles on a line), so the givens are true and the triangles really are congruent. Postulates: SSS, SAS, ASA, AAS, HL; CPCTC in proofs 8, 11, 12.
- The checker reads what students write (≅ or =, ∠ or "angle", △ or "triangle", any vertex order that matches, rows 1–3 in any order, reasons such as "def of midpoint", "Side-Angle-Side"), works out what each statement means in the drawn figure, and marks each row.
- `#seed=N` fixes a set; **New set** makes another. Progress is kept in the browser. Teacher view includes the printable key. Shared student links use `?student=1#seed=N` and hide teacher resources and model answers.
- `node tests/verify-proofs.cjs 2000` re-checks 24,000 proofs independently (givens, diagram quality, model proofs, postulate, CPCTC, every bank distractor, and mutations such as a wrong vertex order or SSA).
