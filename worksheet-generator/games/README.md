# Generated games

Five classroom games that run on fresh, independently checked problems from the Menu Assessment skill
banks (`worksheet-generator/menu/skills/`). They look and play like the hand-built games on the site.

| Game | Folder name | How it plays |
|------|-------------|--------------|
| Flashcards | `<unit>-flashcards` | every skill at the level's three difficulties; flip for answer + worked solution; rate cards; practice missed; new deck |
| Showdown | `<unit>-showdown` | one column per skill category, 100–500 points; CP2/CP1/Honors/Mixed boards; choices and answers on demand; up to four teams |
| Connect Four | `<unit>-connect-four` | two teams; a correct multiple-choice answer earns a disc; a miss shows the solution and passes the turn; optional timer |
| Tic-Tac-Toe | `<unit>-tic-tac-toe` | two teams; claim a square with a correct answer; a miss lets the other team steal; optional timer |
| Picture Reveal | `<unit>-picture-reveal` | 10 problems, mostly typed; each correct answer uncovers a piece of an original picture |

## How correctness is guaranteed
- Every problem comes from `MKMENU.generateProblem`, so it already passed the independent verifier.
- `bank.js` makes one game item per answer part. Wrong choices are made by changing one number, one
  inequality sign or one key word of the key (or by using another part's answer, e.g. the range given as
  the domain). A wrong choice is used **only if the verifier reads it and rejects it**, and it must look like
  something a student could write (sorted sets, intervals from smaller to larger, values on the drawn graph).
- Typed answers (`3, -1`, `{-2, 0, 3}`, `-2 <= x < 5`, `y = 1/2x + 3`, `h = (A - 2b)/3`) are turned into
  math and handed to the same verifier, so any correct form is accepted. Answers that need words
  ("Yes, because…") are multiple choice only.

## Units with games
- Relations and Functions (`relations-functions-*`), Foundations of Algebra (`foundations-algebra-*`, expression skills), Exponential Functions (`exponential-functions-*`), Factoring (`factoring-zero-product-*`), Statistics (`statistics-data-modeling-*`), Linear Functions (`linear-functions-*`; the older hand-made `linear-equations-slope-*` games stay), Systems (`systems-*`; the hand-made `systems-of-equations-*` games stay), Exponents (`exponents-*`; the hand-made `exponents-exponential-functions-*` games stay).

## Adding a unit
1. The unit needs a menu skill set (`worksheet-generator/menu/skills/<set>.js`).
2. `python3 mkgames.py <repo> <unit-folder> <skill-set-id> "<Unit Label>" [skill,ids]` writes the five
   pages (the optional list limits a page to some skills, as Foundations does with the expression skills).
3. Thumbnails: screenshots at 1200×750 saved as `thumbs/<unit>-<game>.jpg` (720×450).
4. Add the `data.js` entries and bump `?v=` in `index.html` and `activity.html`.

## Tests
- `node games/tests/games-tests.cjs` (Node): every key verifies, every wrong choice is rejected, every
  typeable key is accepted in several student forms, wrong typed answers are rejected.
- `node games/tests/games-browser.cjs` (Playwright, server at `BASE`): plays all five games for each unit
  (wins, steals, misses, scoring, all ten picture pieces).
