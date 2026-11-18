# Calculus audit fixes, batch C1 of 3

Fixes #1, #7, #8, #11, #12, #13, #14, #18, #19 and #20 from the Calculus audit (2026-11-18).

**Upload order:** C1 first, then C2, then C3. Each zip holds only the files that batch adds or changes, at their
repository paths, so unzip it at the root of the repository (or drag the folders into GitHub's "Upload files" page)
and commit. No files are deleted in this batch.

## What changes

| # | Fix | Where |
|---|-----|-------|
| 1 | All 420 find-the-mistake items now name the mistake the student actually made (135 diagnoses rewritten, garbled student answers replaced, 4 duplicate items rewritten, 2 tank items and an Euler item corrected). | question banks; `tools/calculus-audit-20261118/fix_error_items.py` |
| 7 | Calculus pacing guide and unit briefings (AP Calculus AB: new content to about day 130, AP review to the exam in early-to-mid May, then post-exam projects). | `scripts/geo-planning.mjs`, `scripts/build-site.mjs`, `scripts/test-public-site.cjs` |
| 8 | Off-skill items replaced: Σ ↔ ∫ conversions, analyzing g(x) = ∫ f from a graph, limits of Riemann sums. | `fix_off_skill.py` |
| 11 | Each AP learning objective now has its own description ("AP Calculus CHA-2.A: …"); tags corrected (CHA-5.B/C, CHA-4.D, LIM-3.A, FUN-1.C). | `worksheet-generator/menu/standards.js`, `standards-map.js`; `retag.py` |
| 12 | Open-response stems name their skill. | `stems.py` |
| 13 | Notation clean-up (coefficient 1, "+ −", "(x − 0)", cosⁿ(x), "quadrant none" and more), with pattern checks. | `fix_text.py` |
| 14 | AP Review "Justifying Solutions" and "Notation and Written Explanations" now practise what they say. | `fix_ap_review.py` |
| 18 | The course is labelled AP Calculus AB; Euler's method is marked as a BC topic. | `data.js`, `app.js`, banks |
| 19 | IVT counting items ask what the theorem *guarantees*; motion items have units. | `fix_text.py` |
| 20 | Independent sympy key checker (1,522 keys recomputed) runs in the Calculus CI job; new regression test `scripts/test-calculus-audit.cjs`. | `verify_keys.py`, workflow |

## Tests run before packaging

All passed on this batch:

- `node scripts/test-calculus-audit.cjs`
- `python3 tools/calculus-audit-20261118/verify_keys.py`: 1,522 keys recomputed, 0 mismatches
- `node scripts/test-published-question-banks.cjs`: 79 banks
- `MG_COURSE=calculus MG_PREFIX=cal- node scripts/test-hs-bank-integration.cjs`: 210 lesson plans, 189 printables, 0 failures
- `node scripts/test-standards.cjs`
- `node --test tests/reaudit-fixes.test.cjs` (no question repeats at two levels)
- A local replay of every workflow's `run:` steps, compared with the same replay of `main`: no new failures. (Steps that need the
  live elementary course sources, a browser download or GitHub itself fail the same way on `main` in this environment.)

The site at mrksclassroom.com wasn't reachable from the build environment, so please check the Calculus pacing page and a
few questions on the live site after the deploy.
