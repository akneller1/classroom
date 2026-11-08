# Claude handoff: Discrete Math Honors Partner Checks

Open CLAUDE_PROMPT.md first.

This is an isolated reference bundle from https://github.com/akneller1/classroom at commit 0953f0b9972ebb13ea6234f8f723ac2bd291af1e (2026-11-08). It is NOT an install package and must NOT replace the website.

Target: Discrete Math Unit 4 — Sequences, Mathematical Induction, and Recursion.
Bank: question-banks/discrete/sequences-induction-recursion.json
Current bank: 273 questions; CP2 92, CP1 91, Honors 90.

Start with these files:
1. question-banks/discrete/sequences-induction-recursion.json
2. tools/discrete-math/bank/u04_sequences.py
3. tools/discrete-math/bank/build_all.py and core.py
4. worksheet-generator/menu/printables.js
5. scripts/test-partner-check-pairs.cjs

The bundle includes the complete worksheet-generator runtime, all current unit-bank JSON files, the Discrete Math diagram assets, schema, authoring helpers, and relevant tests. Other courses' diagram assets, fixed PDFs, homepage files, site branding, and deployment workflows are intentionally omitted to keep it compact.

This supports the focused bank/generator checks below. It is not a complete website preview; some links and non-Discrete diagrams point at omitted site assets. For a full site/browser audit use a fresh checkout of the repository at the recorded commit.

Requirements:
- Node.js 22 or compatible for the Node checks.
- Python 3 with jsonschema, plus any imports used by the included bank authoring helpers, for rebuilding.
- Rebuild only this unit:
  python3 tools/discrete-math/bank/build_all.py u04_sequences

Verification:
  node scripts/test-discrete-bank.cjs
  node scripts/test-partner-check-pairs.cjs 5

For the integration check set MG_COURSE=discrete and MG_PREFIX=dm-, then run:
  node scripts/test-hs-bank-integration.cjs

The Discrete bank test contains an expected total of 2,805 across all units. If you add questions, update that expected total and coverage reports to the independently counted new total. Keep all validation, answer checks, coverage minimums, and level checks intact.

Return a NEW minimal update ZIP containing only the changed files, a short installation note, and the verification results. Do not return this whole reference bundle as a site update. Do not edit or overwrite the homepage, layout, styles, spacing, colors, navigation, Seating Chart, or unrelated courses. Claude cannot push or deploy to GitHub for this task; return files for installation in ChatGPT.

REFERENCE_MANIFEST.json records the source commit and included file hashes.
