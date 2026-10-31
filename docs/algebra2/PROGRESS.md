# Algebra 2 content — progress manifest (resume here)

Session 1 (2026-10-31). Repo snapshot: classroom-main ZIP uploaded by user.
Session 2 (2026-10-31): Units 4–11 authored; Units 1–3 topped up. All 89 skills ≥ 30 items. Repo snapshot: classroom-main (2).zip.

## Findings (do not re-inspect)
- Bank format: `question-banks/algebra2/<unitId>.json`, schema `schemas/question-bank.schema.json` (no extra question keys allowed).
- Levels: `cp2`, `cp1`, `honors`. Formats: short-answer, multiple-choice (exactly 1 correct), select-all (≥2 correct), open-response (≥4 parts).
- Skill IDs: `<unitId>-skill-NN` in catalog order (`course-catalog.js` → `algebra2`). 11 units, 89 skills.
- Diagrams playable in shared tools only as raster images under `question-banks/assets/...` (type "image", alt required).
- Existing Algebra 2 bank items before this work: none. Algebra 1/Geometry use JS generators in `worksheet-generator/menu/skills/` (not the bank format).
- Approval: never set `approved: true` in `question-banks/manifest.json`; human review first (docs/CLAUDE_QUESTION_BANK_HANDOFF.md).

## Session 2 (2026-10-31)
- sympy unavailable (package registries blocked). `lib.py` now imports sympy optionally; new `mathlite.py` supplies exact Fraction polynomials (`P`), `factor_str`, `rad`, `lb`, numeric text checker `peval`/`eqcheck`, and `sel_auto` (select-all whose correct options are decided by a computed predicate).
- `Bank.resume(...)` loads an existing bank and continues ID numbering (for the units 1–3 top-up without regenerating them).
- `package.py batch-name unit ...` writes one batch ZIP (banks, assets, per-unit docs, coverage matrix, PROGRESS, tools).
- Bank RNG now seeded with crc32(unitId) (Python's hash() is randomized per run) and a fresh run clears that unit's asset folder, so reruns are reproducible.
- Units 1–3 JSON copied unchanged from their session-1 ZIPs (their scripts still need sympy to rerun).

## Status
| # | Unit | Items | Status |
|---|---|---|---|
| 1 | functions-transformations | 262 | draft complete (top-up, batch 5) |
| 2 | linear-functions-systems | 221 | draft complete (top-up, batch 5) |
| 3 | quadratic-functions-complex-numbers | 247 | draft complete (top-up, batch 5) |
| 4 | polynomial-functions | 272 | draft complete (batch 1) |
| 5 | radicals-rational-exponents | 248 | draft complete (batch 1; rebuilt batch 5) |
| 6 | exponential-logarithmic-functions | 251 | draft complete (batch 1) |
| 7 | rational-functions | 241 | draft complete (batch 2) |
| 8 | sequences-series | 241 | draft complete (batch 2) |
| 9 | conic-sections | 216 | draft complete (batch 3) |
| 10 | trigonometric-functions | 277 | draft complete (batch 3) |
| 11 | probability-statistics | 241 | draft complete (batch 4) |
Per-skill counts: COVERAGE_MATRIX.md.

Totals: 2,717 items (short-answer 1,335 · multiple-choice 732 · select-all 334 · open-response 316; cp2 535 · cp1 1,620 · honors 562).
None are approved; manifest.json untouched. `node scripts/check-question-bank.cjs` passes for all 11 banks.

## Session 2 notes
- Top-up scripts `u01_topup.py`, `u02_topup.py`, `u03_topup.py` call `Bank.resume()` on the pristine session-1 banks in `base/` (copy them from the session-1 ZIPs), so reruns are idempotent and session-1 IDs are untouched; new IDs continue each skill/level sequence.
- `s1_fixes.py` applies cosmetic notation fixes to 10 session-1 items (same IDs, same meaning): `y = (x - (4))/1/2` → `y = (x - 4)/(1/2)`, `y + (1) = 2(x - (3))` → `y + 1 = 2(x - 3)`, `-3/2x` → `-(3/2)x`. Affected: a2-ft-s04-cp2-001…005 (solution steps), a2-ls-s01-cp2-010/011/012, a2-ls-s01-honors-004/005.
- Verification: every computed answer comes from exact Fractions/`P` polynomials or numeric checks (`sel_auto` decides select-all keys by predicate; `eqcheck` compares expressions at sample points); hand-written answers have `assert`s. Several draft errors were caught this way (3×3 hyperbola coefficients in conic conversion, a bracket mismatch, a/b factor-theorem system, single-answer select-alls).
- Units 4–6 in batch 1 were generated before the RNG fix, so their MC option order differs from the current rebuild; content is identical. Use the complete `algebra2-all-units` ZIP as the source of truth.
- Reviewer flags: rounding conventions (money to cents, logs to 3–4 decimals) are stated in prompts; some modeling answers accept equivalent forms (e.g. sigma notation, sinusoid phase) — the answer text notes "(other forms possible)" where relevant.

## How to resume
1. Python 3 + matplotlib + numpy (sympy optional; only the session-1 unit scripts need it). Put `lib.py` and the `uNN_*.py` scripts in one folder; set `lib.OUT`.
2. New content: follow `u04_polynomials.py`…`u11_probstat.py` (mathlite helpers, `sel_auto`, `graph()`); top-ups: follow `u0N_topup.py`.
3. `python3 uNN_*.py` then `node scripts/check-question-bank.cjs out/question-banks/algebra2/<unit>.json`.
4. `python3 package.py <batch-name> <unit> …` builds one ZIP (banks, assets, docs, tools); no args → one ZIP per unit.
5. Next: human math review; then integration decides difficulty-label mapping (cp2/cp1/honors kept as-is).

## Lessons from session 1
- Verify every hand-written answer with an assert; three draft errors were caught this way (3×3 systems, LP minimum, perpendicular k).
- `lib.clean()` normalizes "+ -", "- -n", "1x"; `roots_txt()` prints conjugate roots as "a ± b".
- Dedupe key = prompt + diagram src, so the same prompt may reuse different graphs.
