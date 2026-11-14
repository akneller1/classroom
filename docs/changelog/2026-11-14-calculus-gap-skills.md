# 2026-11-14: Calculus gap skills (Classroom repo)

Five new skills close the AP Calculus AB gaps found in the 2026-11-14 audit. Each skill has 48 new questions: 16 per level (CP2, CP1, Honors), made up of:
- 7 short answer
- 6 multiple choice
- 2 error analysis
- 1 four-part open response

| Unit | New skill (catalog position) | AP code | Covers |
|---|---|---|---|
| Derivatives | The Chain Rule (skill 08) | FUN-3.C | powers of linear and quadratic insides; sin, cos, e and ln of an inside; nested functions; f(g(x)) from a table; (g(x))ⁿ |
| Derivatives | Implicit Differentiation (skill 09) | FUN-3.D | ellipse and circle forms, x² + xy + y², x³ + y³, x²y + y³, e^y + xy, sin(y) + x², xy² − x²; tangent slopes at points on the curve |
| Derivatives | Derivatives of Inverse Functions (skill 10) | FUN-3.E | sin⁻¹ and tan⁻¹ with the chain rule; (f⁻¹)′(b) for one-to-one polynomials; g′ from a table of f values |
| Applications of Derivatives | L'Hôpital's Rule (skill 12) | LIM-4.A | 0/0 and ∞/∞ limits, including repeated use; deciding whether the rule applies |
| The Fundamental Theorem of Calculus | Integration by Substitution (skill 06) | FUN-6.D | indefinite integrals with polynomial, trig, exponential and log insides; definite integrals with changed limits |

## Other changes
- "Midterm Review" in Applications of Derivatives is renamed **"Mixed Review: Limits and Derivatives"**. Its id is unchanged.
- `course-catalog.js`: the new skill names are appended, so every existing skill id is unchanged. Lesson plans, worksheets, assessments, printables, games and flashcards pick the new skills up automatically.
- `worksheet-generator/menu/standards-map.js` was regenerated with `node scripts/build_standards_map.cjs`.
- Cache string `?v=hs-gap-20261114` on `course-catalog.js` and `standards-map.js` in 18 pages.

## How the questions were made and checked
- **Tools:** `tools/hs-gap-skills-20261114/`, containing `calc_families.py`, `build.py` and `verify.py`. `hsfmt.py` evaluates the displayed math text with NumPy.
- **Why a new verifier:** SymPy isn't available in this environment, so the repo's SymPy-based `gverify.py` could not run.
- **What `verify.py` does for each question:**
  - reads the function, equation or numbers printed in the question;
  - judges the keyed answer correct by numeric differentiation, implicit partial derivatives, `brentq` root-finding for inverses, Richardson-extrapolated limits or `scipy.quad`;
  - judges every wrong option and every "student answer" incorrect.
- **Result:** 240 questions, TOTAL ERRORS 0.

To rebuild from scratch: `git checkout` the three banks and their tags, then run `python3 build.py <repo> calc` and `python3 verify.py <repo>`.

## Tests run
These pass:
- `audit-question-banks` (no issues)
- `test-published-question-banks`
- `MG_COURSE=calculus test-hs-bank-integration`: 207 lesson plans, 27 game decks, 189 printables
- `test-standards`
- `audit-course-catalog`
- `worksheet-generator/tests/math-audit`
