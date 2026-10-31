# Integration note — algebra2/conic-sections

Files (copy into the repo at the same relative paths):
- question-banks/algebra2/conic-sections.json — bank payload, schemaVersion 1; skill IDs from MK_COURSE_CATALOG.getSkillRecords('algebra2', 'conic-sections').
- question-banks/assets/algebra2/conic-sections/*.png — raster graphs referenced by diagram.spec.src (type "image", alt text included).
- question-banks/algebra2/meta/conic-sections.tags.json — sidecar map id → enrichment tags (challenge, misconception, error-analysis, modeling, graph, multiple-representations, reasoning, connections, multistep). Kept outside the bank because the schema forbids extra question properties.
- ANSWER_KEY.md — human-readable key with worked solutions for reviewer sign-off.

Dependencies: none beyond the existing course-catalog.js, question-bank-adapter.js and question-bank-loader.js.
Check: `node scripts/check-question-bank.cjs question-banks/algebra2/conic-sections.json` (passes).
Per docs/CLAUDE_QUESTION_BANK_HANDOFF.md, do NOT add `approved: true` to question-banks/manifest.json until a human has reviewed the math. Shared games currently skip items that have a diagram (20 items here).
Text notation is plain Unicode (x², √, ≤, π, i); no TeX.
