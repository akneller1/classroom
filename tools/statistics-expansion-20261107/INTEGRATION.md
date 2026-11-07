# Statistics integration, 2026-11-07

The four banks are installed under question-banks/statistics and registered in the manifest. Statistics now uses the shared native generators, games, flashcards, readiness check, and lesson planner. Existing courses and interactive tools are preserved.

Local checks: strict Draft 2020-12 schema validation of all 1,017 questions; all 282 new numerical checks passed; 114 topic/level coverage cells; all published bank shapes, IDs and figure paths; 36 default worksheet/test/menu builds; 114 skill/level selections; 12 unique-choice game decks; 51 compatible printable builds; 114 lesson-plan builds; flashcards in mixed, skill and vocabulary modes. The actual browser generated a Statistics worksheet with its histogram, and a CP2 Sampling and Experimentation escape room accepted a cluster-sampling answer and correctly locked a numerical cipher answer before enabling shifts.

Printable availability follows successful builds rather than raw bank size. Statistics Partner Check and Error Analysis are disabled. Sampling and Experimentation additionally disables Color by Number, Whodunnit printables, and Tarsia; its Maze, Stations and vocabulary remain available. Other units retain Maze, Color by Number, Whodunnit, Stations and Tarsia. Whole-unit game pools have sufficient questions at every level. Narrow single-skill selections can still underfill long games. Written explanations use the existing teacher/self-review flow.

The independent new-answer verifier is run from the repository root:

    python tools/statistics-expansion-20261107/scripts/verification/verify_expansion.py .

Its checks.json sidecar is resolved relative to the verifier, outside the published site. Original authoring sources and reports are retained here. The original change summary is an author report, not a claim that all conceptual questions have received external teacher review.
