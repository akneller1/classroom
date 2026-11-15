# Generator port spec — Algebra 1 skills 09 and 10 (for `menu/skills/algebra1-relations-functions.js`)

Algebra 1 resources are generated natively. Algebra 1 has no JSON bank today. Codex can do either or both of the following:
(A) register `question-banks/algebra/relations-functions.json` (this package) through the approved-bank adapter for games, flashcards and practice tests; or
(B) port these families into the native menu engine so worksheets, assessments and printables generate endless variants.
The bank items in this package are the reference answers for (B): a ported family must reproduce them for the same parameters.

| Family (sourceNotes) | Level(s) | Parameters | Answer rule |
|---|---|---|---|
| sqrt-evaluate | all | a ∈ {1,2,3} (CP2) or {−1,1,2,3}; h, k ∈ [−5,4]; s ∈ [1,5]; x₀ = h + s² | a·s + k |
| sqrt-domain / sqrt-range | all | same | domain x ≥ h; range y ≥ k (a > 0) or y ≤ k (a < 0) |
| sqrt-endpoint | CP2 | same | (h, k) |
| sqrt-transform | CP1, Honors | same | reflect (a < 0), stretch \|a\|, shift h, shift k, in that order |
| sqrt-avg-rate | all | x₁ = h + s₁², x₂ = h + s₂², s ∈ [0,4] | (a(s₂ − s₁))/(s₂² − s₁²), exact fraction |
| sqrt-graph-match / -write | CP2–CP1 match, Honors write | marked points (h, k) and (h + 4, k + 2a) | y = a√(x − h) + k |
| sqrt-table | CP1 | x = h + t², t = 0..3 | a·t + k |
| sqrt-solve | Honors | √(x − h) + k = c, c − k = s ≥ 1 | x = h + s² (always check) |
| cbrt-evaluate | all | s ∈ {−3..3}\{0}; x₀ = h + s³ | a·s + k |
| root-domain-compare | all | h | the cube root has domain ℝ; the square root has domain x ≥ h |
| piecewise-evaluate | all | two linear pieces, boundary b ∈ [−2,3], ≤/< chosen at random; x₀ = b at CP1 and Honors | choose the piece by its condition, including the boundary |
| piecewise-graph-read | all | left ray y = m₁x + c₁ for x < b, horizontal ray y = c₂ for x > b, one closed dot at x = b | value at the closed dot when x₀ = b |
| abs-vertex / abs-range | all | a ∈ {±1, ±2, 3}, h, k ∈ [−5,5] | (h, k); y ≥ k or y ≤ k |
| abs-graph-match / -write | CP2–CP1 match, Honors write | vertex (h, k) and (h + 1, k + a) marked | y = a\|x − h\| + k |
| abs-solve | all | \|x − h\| + k = c with c − k = d ≥ 1 | x = h ± d |
| abs-solutions-count | Honors | c < k with a > 0 | no solutions |
| step-context | all | base, per ∈ {(3,2),(5,1),(2,3),(4,2)}; hours ∈ {0.5, 1.25, 2, 2.5, 3.75, 4} | base + per·⌈hours − 1⌉ (minimum 0) |
| step-floor | all | v ∈ {−3.7, …, 4.8} | ⌊v⌋ |
| step-open-response | one per level | bike-share $base + $per per started 15 minutes | 4 parts (the adapter requires ≥ 4) |

Wrong-answer choices are deliberate errors: a sign error on h, a swap of h and k, a sign error on k, a flipped inequality for the range, and using the other piece at a boundary. Keep these if the families are ported.

Graph style: integer grid from −8 to 8, axes labeled every 2, arrows at the ends of rays, closed dots filled and open dots white with a colored ring. Match `core/graph.js` if ported.
