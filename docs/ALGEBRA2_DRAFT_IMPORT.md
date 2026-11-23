# Algebra 2 draft-bank import and review

These are **unreviewed authoring drafts**, not approved student-facing resources. Do not add them to `question-banks/manifest.json` or set `approved: true` until an independent qualified reviewer checks the mathematics.

## Prepare incoming ZIP packages

1. Verify archive entries before extraction; reject absolute paths, `../`, duplicate destinations, and symlinks.
2. Extract question-bank JSON into `question-banks/algebra2/`, companion tags under `question-banks/algebra2/meta/`, and images under `question-banks/assets/algebra2/`, preserving their relative paths.
3. Run `node scripts/audit-algebra2-drafts.cjs`. This wraps the existing structure validator, checks the presence of referenced images, detects repeated IDs across files, and summarizes coverage. Inspect warnings.
4. Inspect representative images visually, then independently review **every** question, distractor, worked solution, graph, ambiguity, and difficulty level. Structural checks alone are not math review.
5. Document approval for each unit. Only then update `question-banks/manifest.json` explicitly and test every supported consumer.

## Compatibility boundaries

Algebra 2 currently has **11 units** and **89 skills** in the course catalog. The current supplied draft batch covers the first three units with 486 questions; the other eight units are not authored yet. Internal levels are `cp2`, `cp1`, and `honors`. Do not relabel `cp1` in JSON merely to change a display label. Existing game adapters exclude diagram-dependent questions, and the existing text game flow supports only short-answer and multiple-choice. Select-all and multipart open response require a compatible consumer.

Keep the original Algebra 1 and Geometry question-generation systems untouched. Connecting this new bank schema to additional generators is a separate, tested integration task; copying the JSON files alone will not activate them.