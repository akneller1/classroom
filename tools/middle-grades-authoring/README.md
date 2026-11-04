# Grade 7 / Grade 6 authoring tools (offline)

These scripts build the `prealgebra7` (Grade 7) and `math6` (Grade 6) question banks. They are an authoring aid only. The site reads the JSON files they produce.

They reuse the Grade 8 toolkit in `tools/prealgebra-authoring/` without changing it: `lib.py`, `mathtext.py`, `verify.py` and `checks_custom.py`.

| File | Purpose |
|---|---|
| `glib.py` | Problem record `Q()` with misconception reasons. It also builds the derived extras: `err_of` (error analysis), `open_of` (4-part open response, each part checked on its own) and `select_of` (select-all). It holds the diagram helpers (number lines, figures, solids, data displays) and an exact-decimal `D()`. |
| `g7_u01.py` … `g7_u13.py` | Grade 7 problem families, one module per unit, with a `SKILLS` table keyed to the catalog order. |
| `g6_u01.py` … `g6_u07.py` | Grade 6 problem families. |
| `gbuild.py` | Builds banks, tag files, PNG diagrams and `out/<course>/<unit>.checks.json`. Each skill gets 16 questions per level: 7 short-answer, 6 multiple-choice, 2 error-analysis and 1 select-all or open-response. |
| `gchecks.py` | Grade 6/7 independent checks, registered into the Grade 8 verifier. |
| `gverify.py` | Independent verifier. It re-derives every answer and option from the student-facing text. It also checks duplicates and near-duplicates, catalog IDs, missing figures, out-of-grade notation, stacked-fraction display (through the site's own `math-display.js`) and activity readiness. |
| `greport.py` | Writes the coverage tables, skill manifest and activity compatibility report. |
| `vocab.py`, `vocab_g6.py` | Write `worksheet-generator/vocabulary-data-middle-grades.js` in the `MKVOCAB_BANKS` format. |

## How to reproduce

Run these from the repository root.

```
export MG_OUT=$PWD          # or a scratch folder
python3 tools/middle-grades-authoring/gbuild.py prealgebra7      # all 13 units (deterministic; build the whole course at once)
python3 tools/middle-grades-authoring/gverify.py prealgebra7     # must print TOTAL ERRORS 0
python3 tools/middle-grades-authoring/greport.py prealgebra7
python3 tools/middle-grades-authoring/vocab.py worksheet-generator/vocabulary-data-middle-grades.js prealgebra7 math6
```

Use `math6` in place of `prealgebra7` to build Grade 6.

Always build a whole course in one run. Duplicate prevention works across units, so rebuilding a single unit can pick different (still verified) items.

Requirements: Python 3 with matplotlib and Pillow, and Node.js (used to read `MK_COURSE_CATALOG` and to run the display check).

## How independence is achieved

Each family states its check from the problem's own data. Examples:
- the equation shown, which `mathtext.solve_linear` solves;
- the expression shown, which the verifier's own parser evaluates;
- the raw data list, from which the statistic is recomputed;
- the sides of a triangle, from which a trig value is computed with `math`;
- the claim in a counterexample item, which is re-implemented as a predicate in `gchecks.py`.

The verifier never imports the families. It parses the text exactly as students see it.

Every multiple-choice and select-all option is re-judged, and its truth must match its `correct` flag. Conceptual items whose answer is a definition or a name are checked against an authored key; the verification report lists them under `check:text`.

## Precalculus and Calculus

- Units: `pc_u01.py` … `pc_u08.py` (`precalculus`) and `ca_u01.py` … `ca_u09.py` (`calculus`), built with the same `gbuild.py` pipeline.
- `hslib.py`: SymPy expression → site display text (`T`), interval/matrix/vector text helpers, curve, trig, triangle and conic diagram drawers.
- `hschecks.py`: independent checks. `P(text)` parses the *displayed* text (√, π, e, ∞, superscripts, sin⁻¹, log bases, |…|, °); the `hs` check restates each problem in SymPy (`diff`, `integrate`, `limit`, `solve`, matrices…) and compares; custom checks cover piecewise limits, related rates, optimization, Riemann sums, differential equations, ambiguous-case triangles, linear programming, and more.
- Build: `MG_OUT=<out> python3 gbuild.py precalculus pc_u03` · Verify: `MG_OUT=<out> python3 gverify.py precalculus` · Reports: `python3 greport.py precalculus` · Vocabulary: `python3 vocab.py <path>/vocabulary-data-middle-grades.js prealgebra7 math6 precalculus calculus`.
- `gbuild.py` now drops any error-analysis item whose "student answer" passes the check, and `gverify.py` reports it if one slips through.
