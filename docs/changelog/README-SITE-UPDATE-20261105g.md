# Site update g: Math Millionaire

This update adds a whole-class "Math Millionaire" game show to all 77 units in all 8 courses. Unzip it at the repository root.

| File | Change |
| --- | --- |
| `worksheet-generator/millionaire.html` | **New.** The game page. |
| `data.js` | One block added at the end. It lists a Millionaire card in every unit. Nothing above it changed. |
| `app.js` | Adds Math Millionaire as a game type: its place in the game order, the "Team Games" tag, a short summary and a board-style thumbnail. |
| `guide.html` | Teacher Guide: a Math Millionaire row in the "Which game when" table, and it's named with the other whole-class games under Sharing with students (no student link). |
| `index.html`, `activity.html` | The `?v=` on `data.js` and `app.js` was bumped so browsers load the new versions. |

`python3 scripts/check_library.py` reports 0 problems.

## How it works

- **Where it is:** each unit page shows a card named "<Unit> Millionaire" with the other team games. It opens as `worksheet-generator/millionaire.html?course=<course>&unit=<unit>`.
- **Where the questions come from:** they are drawn from the same verified question banks as Showdown, Connect 4 and Tic-Tac-Toe, so there's nothing new to check. Only multiple-choice items with one correct answer and three distinct wrong answers are used. Items whose answer choices are graphs are skipped.
- **Every game is new:** each game draws 15 fresh questions.
- **Difficulty:**
  - Questions 1–5 come from the CP2 / Remedial level, 6–10 from CP1 / Standard, and 11–15 from Honors / Advanced.
  - Within that, questions are ordered by how long their worked solution is, so the ladder keeps getting harder.
  - The game spreads questions across the unit's skills.
- **Skills:** you can pick which skills to include on the start screen. All skills are selected by default.
- **Hot seat:** choose 2–10 groups. The hot seat rotates each question, and "Next group" skips a group.
- **Lifelines (each once per game):**
  - **50:50** removes two wrong answers.
  - **Ask the Class** is a vote you tally with + / − buttons, shown as a bar chart.
  - **Hint** shows the skill name and the first step of the worked solution. It stops before any "=" or ":" so it never gives the answer. If no step works as a hint, it shows a general strategy instead.
- **Ladder:** $100 to $1,000,000. Questions 5 and 10 are safe havens. After a wrong answer you can end the game or keep going for practice.
- **After each answer:** the worked solution appears under "Why".
- **Controls:**
  - Keys A–D pick an answer and Enter locks it in.
  - There is a full-screen button for projecting.
  - Sound effects can be turned off on the start screen.
- **Student links:** none. It's a teacher-run, projected game, like Showdown.

## Tested

- Built 4 games in every one of the 77 units:
  - every game had 15 questions
  - no level ran short
  - every answer key matched the bank's correct answer
  - no script errors
- Played complete games with every lifeline, a miss, practice mode and the end screen.
- Checked that the card appears on unit pages in every course and that the game opens in the activity viewer.

