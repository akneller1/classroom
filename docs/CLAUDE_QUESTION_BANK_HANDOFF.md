# Claude question-bank authoring and approval handoff

This guide is for content **authored by Claude**, reviewed by a qualified human, and then loaded into Mr. K's Classroom's shared approved-bank infrastructure. Do not mark authored questions approved automatically. Do not replace the legacy Algebra 1 or Geometry banks.

## Source of truth
- The course and unit identifiers live in `data.js`.
- Exact skill IDs are returned by `MK_COURSE_CATALOG.getSkillRecords(courseId, unitId)` in `course-catalog.js`. Never invent them.
- `schemas/question-bank.schema.json` defines the JSON layout.
- `question-bank-adapter.js` enforces runtime structural validation; `scripts/check-question-bank.cjs` performs a command-line check.
- `question-banks/manifest.json` contains only **explicitly and independently approved** entries.

## Difficulty terms
- Grade 6 (`math6`), Grade 7 (`prealgebra7`), Grade 8 (`prealgebra`): **Remedial**, **Standard**, **Advanced**.
- Internal storage codes for these are `cp2`, `cp1`, `honors`, respectively. Preserve these codes exactly in JSON.
- High-school courses continue using CP2, CP1, Honors.

## Exact payload format
Save one JSON file per unit in `question-banks/<courseId>/<unitId>.json`. This is an illustrative *structure* only; replace all placeholders, do not submit example math as reviewed content.

```json
{
  "schemaVersion": 1,
  "courseId": "math6",
  "unitId": "REPLACE_WITH_EXISTING_UNIT_ID",
  "questions": [
    {
      "id": "unique-stable-id",
      "skillId": "COPY_FROM_CATALOG",
      "level": "cp1",
      "format": "multiple-choice",
      "prompt": "Write an original mathematically valid question.",
      "answer": "Correct answer",
      "solutionSteps": ["Explain each valid mathematical step."],
      "options": [
        {"text": "Correct answer", "correct": true},
        {"text": "Plausible misconception A", "correct": false},
        {"text": "Plausible misconception B", "correct": false}
      ],
      "sourceNotes": "Original item; independently verify math and distractors."
    }
  ]
}
```

## Authoring and review checklist
1. Choose an existing course/unit, copy *exact* skill IDs, and generate original problems for the appropriate level (Remedial/Standard/Advanced for middle school).
2. Verify every correct answer, every distractor, all solution steps, notation, defined variables, and unique answer assumptions. Check for duplicates and ambiguities.
3. Multiple-choice: **exactly one** correct `options[].correct`. Select-all: **at least two** correct. Open-response: **at least four** `parts`. Include meaningful worked steps on all items.
4. For a diagram, provide a separately reviewed accessible image at `question-banks/assets/<filename>.png` (or jpg/jpeg/webp), `diagram.type: "image"`, and `diagram.spec.src` / nonempty `diagram.spec.alt`. Other diagram types are not yet playable in shared games, and shared game adapters currently exclude **all** diagram-dependent questions.
5. Run `node scripts/check-question-bank.cjs question-banks/<courseId>/<unitId>.json`. Run the repository's adapter/loader/game tests as well. Passing these tests **does not prove the mathematics**.
6. Obtain human subject-matter approval **before** setting `approved: true` in the manifest. Until then, leave the file out of the manifest or mark it `approved: false`. Never use a tool or script to assert editorial approval merely because tests passed.

## Manifest format (only after explicit approval)
```json
{
  "version": 1,
  "banks": [
    {
      "courseId": "math6",
      "unitId": "EXISTING_UNIT_ID",
      "path": "question-banks/math6/EXISTING_UNIT_ID.json",
      "approved": true
    }
  ]
}
```

## Current product boundaries
- Approved flashcards: short-answer/multiple-choice with text and safe local raster images.
- Approved game prototypes (Connect 4, Tic-Tac-Toe, Picture Reveal): **text-only** short-answer/multiple-choice; geometry or diagram-specific questions are excluded until renderers are complete.
- Short-answer games remain teacher-judged. Multiple-choice items are automatically scored when a choice was selected.
- Do not claim that legacy question banks have been converted, or that any unreviewed questions are available.
