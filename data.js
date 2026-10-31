/*
  MR. K'S CLASSROOM: LIBRARY CONTENT

  To add an activity:
    1. Put its HTML file in a new folder under artifacts/, for example artifacts/my-activity/index.html
    2. Optional: add a preview image at thumbs/my-activity.jpg (about 720 x 450 pixels).
    3. Add an entry to the right unit's "artifacts" list below.

  Activity fields
    title        Name shown on the card.
    path         Where the activity's HTML file lives.
    thumb        Preview image (optional; a colored placeholder shows without one).
    description  One or two sentences about what students do.
    type         "Game", "Practice", "Exploration", and so on. Becomes a filter.
    level        Optional, for example ["CP"] or ["CP", "Honors"]. Becomes a filter.
    topics       Optional list of skills. Searchable and shown on the card.
    added        Date as "YYYY-MM-DD". Activities show a "New" tag for 30 days.

  Course colors: "blue", "orange", "green", or "purple". Units show in the order listed.
  A unit with no activities shows as "Coming soon".
*/
window.LIBRARY = {
  "title": "Mr. K's Classroom",
  "tagline": "Interactive math games, generators and printables for Algebra 1, Geometry, and Algebra 2. Choose a unit and open an activity on any device.",
  "footer": "Activities run in any modern browser. Saved activities are kept in this browser only.",
  "newDays": 30,
  "courses": [
    {
      "id": "algebra",
      "name": "Algebra 1",
      "color": "blue",
      "art": "curve",
      "blurb": "Equations, inequalities, functions, and polynomials.",
      "units": [
        {
          "id": "foundations-algebra",
          "name": "Foundations of Algebra",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-foundations",
              "thumb": "thumbs/practice-test.svg",
              "description": "Measure Foundations of Algebra readiness with a mixed-topic test, diagnostic skill report, and fresh targeted reassessment.",
              "type": "Study Guide",
              "topics": [
                "Foundations of Algebra",
                "Test readiness",
                "Self-assessment"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-foundations",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-foundations",
              "thumb": "thumbs/worksheet-generator-foundations.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-foundations",
              "thumb": "thumbs/menu-assessment-generator-foundations.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=maze",
              "thumb": "thumbs/maze-generator-foundations.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=color",
              "thumb": "thumbs/color-generator-foundations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-foundations.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=error",
              "thumb": "thumbs/error-generator-foundations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=partner",
              "thumb": "thumbs/partner-generator-foundations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=who",
              "thumb": "thumbs/who-generator-foundations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-foundations&kind=stations",
              "thumb": "thumbs/stations-generator-foundations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Foundations of Algebra Flashcards",
              "path": "artifacts/foundations-algebra-flashcards/index.html",
              "thumb": "thumbs/foundations-algebra-flashcards.jpg",
              "description": "A fresh deck of foundations of algebra flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra Showdown",
              "path": "artifacts/foundations-algebra-showdown/index.html",
              "thumb": "thumbs/foundations-algebra-showdown.jpg",
              "description": "A game board for foundations of algebra review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra Connect Four",
              "path": "artifacts/foundations-algebra-connect-four/index.html",
              "thumb": "thumbs/foundations-algebra-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice foundations of algebra problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra Tic-Tac-Toe",
              "path": "artifacts/foundations-algebra-tic-tac-toe/index.html",
              "thumb": "thumbs/foundations-algebra-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice foundations of algebra problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Foundations of Algebra: Picture Reveal",
              "path": "artifacts/foundations-algebra-picture-reveal/index.html",
              "thumb": "thumbs/foundations-algebra-picture-reveal.jpg",
              "description": "Solve 10 foundations of algebra problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Evaluating expressions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Midnight Library Mystery",
              "path": "artifacts/foundations-algebra-midnight-library-mystery/index.html",
              "thumb": "thumbs/foundations-algebra-midnight-library-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Order of operations",
                "Evaluating expressions",
                "Combining like terms",
                "Distributive property",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Night at the Number Museum",
              "path": "artifacts/foundations-algebra-escape-room/index.html",
              "thumb": "thumbs/foundations-algebra-escape-room.jpg",
              "description": "Story-driven escape room for teams: five galleries with a cipher, hidden clues, property plaques, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Order of operations",
                "Evaluating expressions",
                "Combining like terms",
                "Distributive property",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Foundations of Algebra Cheat Sheet",
              "path": "artifacts/foundations-algebra-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/foundations-algebra-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: variables, order of operations, real numbers, properties and simplifying. Back: like terms, the distributive property, words to algebra and integers. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Foundations of Algebra",
                "Unit 1"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "expressions-equations",
          "name": "Solving Linear Equations",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/worksheet-generator-expressions-equations.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-expressions-equations",
              "thumb": "thumbs/menu-assessment-generator.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=maze",
              "thumb": "thumbs/maze-generator-expressions-equations.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=color",
              "thumb": "thumbs/color-generator-expressions-equations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-expressions-equations.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=error",
              "thumb": "thumbs/error-generator-expressions-equations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=partner",
              "thumb": "thumbs/partner-generator-expressions-equations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=who",
              "thumb": "thumbs/who-generator-expressions-equations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-expressions-equations&kind=stations",
              "thumb": "thumbs/stations-generator-expressions-equations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Golden Whisk Caper",
              "path": "artifacts/expressions-equations-golden-whisk-caper/index.html",
              "thumb": "thumbs/expressions-equations-golden-whisk-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Solving equations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "The Great Rigged Bake-Off",
              "path": "artifacts/expressions-equations-escape-room/index.html",
              "thumb": "thumbs/expressions-equations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Solving Linear Equations Cheat Sheet",
              "path": "artifacts/expressions-equations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/expressions-equations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: solving one-step, two-step and multi-step equations, and checking solutions. Back: writing equations from words, proportions, percents and literal equations. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Solving Linear Equations",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Flashcards",
              "path": "artifacts/solving-equations-flashcards/index.html",
              "thumb": "thumbs/solving-equations-flashcards.jpg",
              "description": "A fresh deck of solving equations flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Showdown",
              "path": "artifacts/solving-equations-showdown/index.html",
              "thumb": "thumbs/solving-equations-showdown.jpg",
              "description": "A game board for solving equations review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems",
                "Team game"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Connect Four",
              "path": "artifacts/solving-equations-connect-four/index.html",
              "thumb": "thumbs/solving-equations-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice solving equations problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations Tic-Tac-Toe",
              "path": "artifacts/solving-equations-tic-tac-toe/index.html",
              "thumb": "thumbs/solving-equations-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice solving equations problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Solving Equations: Picture Reveal",
              "path": "artifacts/solving-equations-picture-reveal/index.html",
              "thumb": "thumbs/solving-equations-picture-reveal.jpg",
              "description": "Solve 10 solving equations problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Multi-step equations",
                "Variables on both sides",
                "Proportions",
                "Literal equations",
                "Equations from word problems"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "inequalities",
          "name": "Linear Inequalities",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-inequalities",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-inequalities",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Linear Inequalities",
                "Unit 3"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-inequalities",
              "thumb": "thumbs/worksheet-generator-inequalities.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Inequalities"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-inequalities",
              "thumb": "thumbs/menu-assessment-generator-inequalities.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Inequalities"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=maze",
              "thumb": "thumbs/maze-generator-inequalities.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=color",
              "thumb": "thumbs/color-generator-inequalities.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-inequalities.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=error",
              "thumb": "thumbs/error-generator-inequalities.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=partner",
              "thumb": "thumbs/partner-generator-inequalities.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=who",
              "thumb": "thumbs/who-generator-inequalities.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-inequalities&kind=stations",
              "thumb": "thumbs/stations-generator-inequalities.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Inequalities"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Golden Parabola Heist",
              "path": "artifacts/inequalities-golden-parabola-heist/index.html",
              "thumb": "thumbs/inequalities-golden-parabola-heist.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Inequalities",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Code Red: Station Nimbus",
              "path": "artifacts/inequalities-escape-room/index.html",
              "thumb": "thumbs/inequalities-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Compound inequalities",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Linear Inequalities Cheat Sheet",
              "path": "artifacts/inequalities-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/inequalities-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: writing, solving and graphing inequalities. Back: compound inequalities, absolute value and inequalities in context. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Linear Inequalities",
                "Unit 3"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Flashcards",
              "path": "artifacts/linear-inequalities-flashcards/index.html",
              "thumb": "thumbs/linear-inequalities-flashcards.jpg",
              "description": "A fresh deck of linear inequalities flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Showdown",
              "path": "artifacts/linear-inequalities-showdown/index.html",
              "thumb": "thumbs/linear-inequalities-showdown.jpg",
              "description": "A game board for linear inequalities review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems",
                "Team game"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Connect Four",
              "path": "artifacts/linear-inequalities-connect-four/index.html",
              "thumb": "thumbs/linear-inequalities-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice linear inequalities problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities Tic-Tac-Toe",
              "path": "artifacts/linear-inequalities-tic-tac-toe/index.html",
              "thumb": "thumbs/linear-inequalities-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice linear inequalities problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Inequalities: Picture Reveal",
              "path": "artifacts/linear-inequalities-picture-reveal/index.html",
              "thumb": "thumbs/linear-inequalities-picture-reveal.jpg",
              "description": "Solve 10 linear inequalities problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Solving inequalities",
                "Compound inequalities",
                "Absolute value inequalities",
                "Inequalities from word problems"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "relations-functions",
          "name": "Relations and Functions",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Relations and Functions",
                "Unit 4"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/worksheet-generator-relations-functions.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-relations-functions",
              "thumb": "thumbs/menu-assessment-generator-relations-functions.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=maze",
              "thumb": "thumbs/maze-generator-relations-functions.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=color",
              "thumb": "thumbs/color-generator-relations-functions.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-relations-functions.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=error",
              "thumb": "thumbs/error-generator-relations-functions.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=partner",
              "thumb": "thumbs/partner-generator-relations-functions.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=who",
              "thumb": "thumbs/who-generator-relations-functions.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-relations-functions&kind=stations",
              "thumb": "thumbs/stations-generator-relations-functions.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Relations and Functions Flashcards",
              "path": "artifacts/relations-functions-flashcards/index.html",
              "thumb": "thumbs/relations-functions-flashcards.jpg",
              "description": "A fresh deck of relations and functions flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions Showdown",
              "path": "artifacts/relations-functions-showdown/index.html",
              "thumb": "thumbs/relations-functions-showdown.jpg",
              "description": "A game board for relations and functions review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions Connect Four",
              "path": "artifacts/relations-functions-connect-four/index.html",
              "thumb": "thumbs/relations-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice relations and functions problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions Tic-Tac-Toe",
              "path": "artifacts/relations-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/relations-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice relations and functions problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Relations and Functions: Picture Reveal",
              "path": "artifacts/relations-functions-picture-reveal/index.html",
              "thumb": "thumbs/relations-functions-picture-reveal.jpg",
              "description": "Solve 10 relations and functions problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Arcade Token Heist",
              "path": "artifacts/relations-functions-arcade-token-heist/index.html",
              "thumb": "thumbs/relations-functions-arcade-token-heist.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Function Factory",
              "path": "artifacts/relations-functions-escape-room/index.html",
              "thumb": "thumbs/relations-functions-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a function machine, a cipher with a hidden shift, a function-or-not sorting belt, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Domain and range",
                "Function notation",
                "Rate of change",
                "Arithmetic sequences",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Relations and Functions Cheat Sheet",
              "path": "artifacts/relations-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/relations-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: relations, functions, domain and range, and function notation. Back: rate of change, linear vs. nonlinear, sequences and reading graphs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Relations and Functions",
                "Unit 4"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "linear-equations-slope",
          "name": "Linear Functions and Graphing",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Linear Functions and Graphing",
                "Unit 5"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/worksheet-generator-linear-equations-slope.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Linear functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-linear-equations-slope",
              "thumb": "thumbs/menu-assessment-generator-linear-equations-slope.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Linear functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=maze",
              "thumb": "thumbs/maze-generator-linear-equations-slope.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=color",
              "thumb": "thumbs/color-generator-linear-equations-slope.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-linear-equations-slope.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=error",
              "thumb": "thumbs/error-generator-linear-equations-slope.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=partner",
              "thumb": "thumbs/partner-generator-linear-equations-slope.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=who",
              "thumb": "thumbs/who-generator-linear-equations-slope.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-linear-equations-slope&kind=stations",
              "thumb": "thumbs/stations-generator-linear-equations-slope.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Linear functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Slope Links Mini Golf",
              "path": "artifacts/slope-links-mini-golf/index.html",
              "thumb": "thumbs/slope-links-mini-golf.jpg",
              "description": "Enter a slope, pick a direction and a club, and hit. The ball follows a line through its starting point, and you only see where it went after the shot. Six holes with walls, sand, and water.",
              "type": "Game",
              "topics": [
                "Slope",
                "Rise over run",
                "Coordinate plane"
              ],
              "added": "2026-10-16"
            },
            {
              "title": "The Summit Sabotage",
              "path": "artifacts/linear-equations-slope-summit-sabotage/index.html",
              "thumb": "thumbs/linear-equations-slope-summit-sabotage.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Slope-intercept form",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Avalanche Patrol: Race to the Lodge",
              "path": "artifacts/linear-equations-slope-escape-room/index.html",
              "thumb": "thumbs/linear-equations-slope-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Slope from points, tables, and graphs",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Linear Functions and Graphing Cheat Sheet",
              "path": "artifacts/linear-equations-slope-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/linear-equations-slope-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: slope, rate of change, slope-intercept form and graphing lines. Back: writing equations of lines, intercepts, parallel and perpendicular lines. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Linear Functions and Graphing",
                "Unit 5"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Linear Functions Flashcards",
              "path": "artifacts/linear-functions-flashcards/index.html",
              "thumb": "thumbs/linear-functions-flashcards.jpg",
              "description": "A fresh deck of linear functions flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions Showdown",
              "path": "artifacts/linear-functions-showdown/index.html",
              "thumb": "thumbs/linear-functions-showdown.jpg",
              "description": "A game board for linear functions review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions Connect Four",
              "path": "artifacts/linear-functions-connect-four/index.html",
              "thumb": "thumbs/linear-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice linear functions problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions Tic-Tac-Toe",
              "path": "artifacts/linear-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/linear-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice linear functions problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Linear Functions: Picture Reveal",
              "path": "artifacts/linear-functions-picture-reveal/index.html",
              "thumb": "thumbs/linear-functions-picture-reveal.jpg",
              "description": "Solve 10 linear functions problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Slope",
                "Linear equations",
                "Parallel and perpendicular lines",
                "Linear models"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "systems-of-equations",
          "name": "Systems of Equations and Inequalities",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Systems of Equations and Inequalities",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/worksheet-generator-systems-of-equations.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Systems of equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-systems-of-equations",
              "thumb": "thumbs/menu-assessment-generator-systems-of-equations.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Systems of equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=maze",
              "thumb": "thumbs/maze-generator-systems-of-equations.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=color",
              "thumb": "thumbs/color-generator-systems-of-equations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-systems-of-equations.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=error",
              "thumb": "thumbs/error-generator-systems-of-equations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=partner",
              "thumb": "thumbs/partner-generator-systems-of-equations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=who",
              "thumb": "thumbs/who-generator-systems-of-equations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-systems-of-equations&kind=stations",
              "thumb": "thumbs/stations-generator-systems-of-equations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Systems of equations"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Space Station Swindle",
              "path": "artifacts/systems-of-equations-space-station-swindle/index.html",
              "thumb": "thumbs/systems-of-equations-space-station-swindle.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Solving systems",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Locked In: Night at the Museum",
              "path": "artifacts/systems-of-equations-escape-room/index.html",
              "thumb": "thumbs/systems-of-equations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Checking and graphing solutions",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Systems of Equations Cheat Sheet",
              "path": "artifacts/systems-of-equations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/systems-of-equations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: solving systems by graphing, substitution and elimination. Back: special systems, choosing a method and word problems. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Systems of Equations",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Zombie Fence",
              "path": "artifacts/zombie-fence/index.html",
              "thumb": "thumbs/zombie-fence.jpg",
              "description": "Build fences from inequalities in slope-intercept form. Keep every survivor in the safe zone and every zombie out, using solid and dashed lines and, on later nights, two inequalities at once.",
              "type": "Game",
              "topics": [
                "Graphing inequalities",
                "Slope-intercept form",
                "Systems of inequalities"
              ],
              "added": "2026-10-16"
            },
            {
              "title": "Aquarium After Hours",
              "path": "artifacts/graphing-inequalities-aquarium-after-hours/index.html",
              "thumb": "thumbs/graphing-inequalities-aquarium-after-hours.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Graphing linear inequalities",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Treasure Island: The Feasible Region",
              "path": "artifacts/graphing-inequalities-escape-room/index.html",
              "thumb": "thumbs/graphing-inequalities-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Solid and dashed boundary lines",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Graphing Linear Inequalities Cheat Sheet",
              "path": "artifacts/graphing-inequalities-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/graphing-inequalities-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: graphing linear inequalities in two variables. Back: systems of inequalities and feasible regions. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Graphing Linear Inequalities",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Systems of Equations Flashcards",
              "path": "artifacts/systems-flashcards/index.html",
              "thumb": "thumbs/systems-flashcards.jpg",
              "description": "A fresh deck of systems of equations flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations Showdown",
              "path": "artifacts/systems-showdown/index.html",
              "thumb": "thumbs/systems-showdown.jpg",
              "description": "A game board for systems of equations review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations Connect Four",
              "path": "artifacts/systems-connect-four/index.html",
              "thumb": "thumbs/systems-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice systems of equations problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations Tic-Tac-Toe",
              "path": "artifacts/systems-tic-tac-toe/index.html",
              "thumb": "thumbs/systems-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice systems of equations problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Systems of Equations: Picture Reveal",
              "path": "artifacts/systems-picture-reveal/index.html",
              "thumb": "thumbs/systems-picture-reveal.jpg",
              "description": "Solve 10 systems of equations problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Systems of equations",
                "Substitution",
                "Elimination",
                "Systems of inequalities"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "exponents-exponential-functions",
          "name": "Exponents and Scientific Notation",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Exponents and Scientific Notation",
                "Unit 7"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/worksheet-generator-exponents-scientific-notation.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-exponents-scientific-notation",
              "thumb": "thumbs/menu-assessment-generator-exponents-scientific-notation.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=maze",
              "thumb": "thumbs/maze-generator-exponents-scientific-notation.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=color",
              "thumb": "thumbs/color-generator-exponents-scientific-notation.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-exponents-scientific-notation.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=error",
              "thumb": "thumbs/error-generator-exponents-scientific-notation.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=partner",
              "thumb": "thumbs/partner-generator-exponents-scientific-notation.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=who",
              "thumb": "thumbs/who-generator-exponents-scientific-notation.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponents-scientific-notation&kind=stations",
              "thumb": "thumbs/stations-generator-exponents-scientific-notation.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Exponents",
                "Scientific notation"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Exponents Flashcards",
              "path": "artifacts/exponents-flashcards/index.html",
              "thumb": "thumbs/exponents-flashcards.jpg",
              "description": "A fresh deck of exponents flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents Showdown",
              "path": "artifacts/exponents-showdown/index.html",
              "thumb": "thumbs/exponents-showdown.jpg",
              "description": "A game board for exponents review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents Connect Four",
              "path": "artifacts/exponents-connect-four/index.html",
              "thumb": "thumbs/exponents-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice exponents problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents Tic-Tac-Toe",
              "path": "artifacts/exponents-tic-tac-toe/index.html",
              "thumb": "thumbs/exponents-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice exponents problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponents: Picture Reveal",
              "path": "artifacts/exponents-picture-reveal/index.html",
              "thumb": "thumbs/exponents-picture-reveal.jpg",
              "description": "Solve 10 exponents problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Negative exponents",
                "Scientific notation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Planetarium Power Outage",
              "path": "artifacts/exponents-scientific-notation-planetarium-power-outage/index.html",
              "thumb": "thumbs/exponents-scientific-notation-planetarium-power-outage.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Zero and negative exponents",
                "Scientific notation",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Rocket Lab",
              "path": "artifacts/exponents-scientific-notation-escape-room/index.html",
              "thumb": "thumbs/exponents-scientific-notation-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with fuel gauges, a cipher with a hidden shift, a true-or-false airlock, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Zero and negative exponents",
                "Scientific notation",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Exponents and Scientific Notation Cheat Sheet",
              "path": "artifacts/exponents-scientific-notation-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/exponents-scientific-notation-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: exponent rules, zero and negative exponents, and evaluating powers. Back: scientific notation and operations with it. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Exponents and Scientific Notation",
                "Unit 7"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "exponential-functions",
          "name": "Exponential Functions",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Exponential Functions",
                "Unit 8"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/worksheet-generator-exponential-functions.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Exponential functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-exponential-functions",
              "thumb": "thumbs/menu-assessment-generator-exponential-functions.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Exponential functions"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=maze",
              "thumb": "thumbs/maze-generator-exponential-functions.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=color",
              "thumb": "thumbs/color-generator-exponential-functions.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-exponential-functions.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=error",
              "thumb": "thumbs/error-generator-exponential-functions.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=partner",
              "thumb": "thumbs/partner-generator-exponential-functions.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=who",
              "thumb": "thumbs/who-generator-exponential-functions.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-exponential-functions&kind=stations",
              "thumb": "thumbs/stations-generator-exponential-functions.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Exponential functions"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Great Pumpkin Snatch",
              "path": "artifacts/exponents-exponential-functions-great-pumpkin-snatch/index.html",
              "thumb": "thumbs/exponents-exponential-functions-great-pumpkin-snatch.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Detective game",
                "Typed answers",
                "Units 7–8"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Dr. Petri’s Growth Lab",
              "path": "artifacts/exponents-exponential-functions-escape-room/index.html",
              "thumb": "thumbs/exponents-exponential-functions-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Escape room",
                "Teamwork",
                "Units 7–8"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Exponential Functions Cheat Sheet",
              "path": "artifacts/exponents-exponential-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/exponents-exponential-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: exponential functions, growth and decay. Back: writing models, compound interest, geometric sequences and solving equations. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Exponential Functions",
                "Unit 8"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Exponential Functions Flashcards",
              "path": "artifacts/exponential-functions-flashcards/index.html",
              "thumb": "thumbs/exponential-functions-flashcards.jpg",
              "description": "A fresh deck of exponential functions flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions Showdown",
              "path": "artifacts/exponential-functions-showdown/index.html",
              "thumb": "thumbs/exponential-functions-showdown.jpg",
              "description": "A game board for exponential functions review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions Connect Four",
              "path": "artifacts/exponential-functions-connect-four/index.html",
              "thumb": "thumbs/exponential-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice exponential functions problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions Tic-Tac-Toe",
              "path": "artifacts/exponential-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/exponential-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice exponential functions problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Exponential Functions: Picture Reveal",
              "path": "artifacts/exponential-functions-picture-reveal/index.html",
              "thumb": "thumbs/exponential-functions-picture-reveal.jpg",
              "description": "Solve 10 exponential functions problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Exponential growth and decay",
                "Exponential equations",
                "Geometric sequences",
                "Linear vs. exponential"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "polynomials-factoring",
          "name": "Polynomials",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-polynomials",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-polynomials",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Polynomials",
                "Unit 9"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-polynomials",
              "thumb": "thumbs/worksheet-generator-polynomials.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Polynomials"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-polynomials",
              "thumb": "thumbs/menu-assessment-generator-polynomials.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Polynomials"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=maze",
              "thumb": "thumbs/maze-generator-polynomials.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=color",
              "thumb": "thumbs/color-generator-polynomials.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-polynomials.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=error",
              "thumb": "thumbs/error-generator-polynomials.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=partner",
              "thumb": "thumbs/partner-generator-polynomials.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=who",
              "thumb": "thumbs/who-generator-polynomials.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-polynomials&kind=stations",
              "thumb": "thumbs/stations-generator-polynomials.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Polynomials"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Polynomials Flashcards",
              "path": "artifacts/polynomials-flashcards/index.html",
              "thumb": "thumbs/polynomials-flashcards.jpg",
              "description": "A fresh deck of polynomials flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials Showdown",
              "path": "artifacts/polynomials-showdown/index.html",
              "thumb": "thumbs/polynomials-showdown.jpg",
              "description": "A game board for polynomials review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials Connect Four",
              "path": "artifacts/polynomials-connect-four/index.html",
              "thumb": "thumbs/polynomials-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice polynomials problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials Tic-Tac-Toe",
              "path": "artifacts/polynomials-tic-tac-toe/index.html",
              "thumb": "thumbs/polynomials-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice polynomials problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Polynomials: Picture Reveal",
              "path": "artifacts/polynomials-picture-reveal/index.html",
              "thumb": "thumbs/polynomials-picture-reveal.jpg",
              "description": "Solve 10 polynomials problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Toy Factory Takedown",
              "path": "artifacts/polynomials-toy-factory-takedown/index.html",
              "thumb": "thumbs/polynomials-toy-factory-takedown.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Classifying polynomials",
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Toy Workshop",
              "path": "artifacts/polynomials-escape-room/index.html",
              "thumb": "thumbs/polynomials-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a block machine, a cipher with a hidden shift, monomial-binomial-trinomial sorting bins, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Classifying polynomials",
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Special products",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Polynomials Cheat Sheet",
              "path": "artifacts/polynomials-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/polynomials-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: vocabulary, classifying, adding and subtracting polynomials. Back: multiplying, special products and dividing by a monomial. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Polynomials",
                "Unit 9"
              ],
              "added": "2026-10-25"
            }
          ]
        },
        {
          "id": "factoring-zero-product",
          "name": "Factoring and Zero Product Property",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Factoring and Zero Product Property",
                "Unit 10"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/worksheet-generator-factoring-zero-product.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Factoring"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-factoring-zero-product",
              "thumb": "thumbs/menu-assessment-generator-factoring-zero-product.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Factoring"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=maze",
              "thumb": "thumbs/maze-generator-factoring-zero-product.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=color",
              "thumb": "thumbs/color-generator-factoring-zero-product.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-factoring-zero-product.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=error",
              "thumb": "thumbs/error-generator-factoring-zero-product.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=partner",
              "thumb": "thumbs/partner-generator-factoring-zero-product.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=who",
              "thumb": "thumbs/who-generator-factoring-zero-product.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-factoring-zero-product&kind=stations",
              "thumb": "thumbs/stations-generator-factoring-zero-product.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Factoring"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Castle Crown Caper",
              "path": "artifacts/polynomials-factoring-castle-crown-caper/index.html",
              "thumb": "thumbs/polynomials-factoring-castle-crown-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Factoring",
                "Detective game",
                "Typed answers",
                "Units 9–10"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "The Wizard’s Spell Library",
              "path": "artifacts/polynomials-factoring-escape-room/index.html",
              "thumb": "thumbs/polynomials-factoring-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Adding, subtracting and multiplying polynomials",
                "Escape room",
                "Teamwork",
                "Units 9–10"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Factoring and Zero Product Cheat Sheet",
              "path": "artifacts/polynomials-factoring-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/polynomials-factoring-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: factoring GCF, trinomials, special patterns and grouping. Back: factoring completely and solving quadratics with the Zero Product Property. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Factoring and Zero Product",
                "Unit 10"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Factoring Flashcards",
              "path": "artifacts/factoring-zero-product-flashcards/index.html",
              "thumb": "thumbs/factoring-zero-product-flashcards.jpg",
              "description": "A fresh deck of factoring flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring Showdown",
              "path": "artifacts/factoring-zero-product-showdown/index.html",
              "thumb": "thumbs/factoring-zero-product-showdown.jpg",
              "description": "A game board for factoring review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring Connect Four",
              "path": "artifacts/factoring-zero-product-connect-four/index.html",
              "thumb": "thumbs/factoring-zero-product-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice factoring problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring Tic-Tac-Toe",
              "path": "artifacts/factoring-zero-product-tic-tac-toe/index.html",
              "thumb": "thumbs/factoring-zero-product-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice factoring problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Factoring: Picture Reveal",
              "path": "artifacts/factoring-zero-product-picture-reveal/index.html",
              "thumb": "thumbs/factoring-zero-product-picture-reveal.jpg",
              "description": "Solve 10 factoring problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "GCF and grouping",
                "Factoring trinomials",
                "Special products",
                "Zero product property"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "quadratics",
          "name": "Quadratic Functions and Equations",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-quadratics",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-quadratics",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Quadratic Functions and Equations",
                "Unit 11"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-quadratics",
              "thumb": "thumbs/worksheet-generator-quadratics.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Quadratics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-quadratics",
              "thumb": "thumbs/menu-assessment-generator-quadratics.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Quadratics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=maze",
              "thumb": "thumbs/maze-generator-quadratics.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=color",
              "thumb": "thumbs/color-generator-quadratics.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Tarsia Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=tarsia",
              "thumb": "thumbs/tarsia-generator-quadratics.svg",
              "description": "Make a Tarsia puzzle for this unit: cut out the triangles and match each problem to its answer to rebuild a hexagon (or triangle). Border decoys, work pages, CP2/CP1/Honors, up to three versions, and a solved key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=error",
              "thumb": "thumbs/error-generator-quadratics.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=partner",
              "thumb": "thumbs/partner-generator-quadratics.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=who",
              "thumb": "thumbs/who-generator-quadratics.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-quadratics&kind=stations",
              "thumb": "thumbs/stations-generator-quadratics.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Quadratics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "The Cannonball Circus Caper",
              "path": "artifacts/quadratics-cannonball-circus-caper/index.html",
              "thumb": "thumbs/quadratics-cannonball-circus-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Solving quadratics",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Thunder Bolt: Launch Gone Wrong",
              "path": "artifacts/quadratics-escape-room/index.html",
              "thumb": "thumbs/quadratics-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Solving quadratic equations",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Quadratic Functions Cheat Sheet",
              "path": "artifacts/quadratics-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/quadratics-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: graphing quadratic functions and their key features. Back: solving quadratic equations: factoring, square roots, completing the square and the formula. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Quadratic Functions",
                "Unit 11"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Quadratics Flashcards",
              "path": "artifacts/quadratic-practice-flashcards/index.html",
              "thumb": "thumbs/quadratic-practice-flashcards.jpg",
              "description": "A fresh deck of quadratics flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics Showdown",
              "path": "artifacts/quadratic-practice-showdown/index.html",
              "thumb": "thumbs/quadratic-practice-showdown.jpg",
              "description": "A game board for quadratics review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics Connect Four",
              "path": "artifacts/quadratic-practice-connect-four/index.html",
              "thumb": "thumbs/quadratic-practice-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice quadratics problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics Tic-Tac-Toe",
              "path": "artifacts/quadratic-practice-tic-tac-toe/index.html",
              "thumb": "thumbs/quadratic-practice-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice quadratics problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Quadratics: Picture Reveal",
              "path": "artifacts/quadratic-practice-picture-reveal/index.html",
              "thumb": "thumbs/quadratic-practice-picture-reveal.jpg",
              "description": "Solve 10 quadratics problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Parabolas",
                "Quadratic formula",
                "Completing the square",
                "Projectile motion"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "statistics-data-modeling",
          "name": "Statistics and Data Modeling",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/practice-test.svg",
              "description": "Complete a realistic unit assessment, review strengths and gaps by skill, and take a targeted reassessment. Supports CP2, CP1 and Honors.",
              "type": "Study Guide",
              "topics": [
                "Self-assessment",
                "Test readiness",
                "Interactive practice"
              ],
              "added": "2026-10-26"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/lesson-planner.svg",
              "description": "Plan any day of this unit from the 180-day scope and sequence: objectives, standards, vocabulary, sentence frame and common misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Print one student handout and a teacher key; every answer is checked.",
              "type": "Planning",
              "topics": [
                "Lesson planner",
                "Do Now",
                "Exit ticket",
                "Statistics and Data Modeling",
                "Unit 12"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/worksheet-generator-statistics-data-modeling.svg",
              "description": "Build practice worksheets for this unit. Pick skills and CP2, CP1 or Honors difficulty, then choose short answer or multiple choice for each part (or mix them). Questions go from easier to harder; print up to three versions with an answer key and worked solutions. Every answer and every multiple-choice option is checked.",
              "type": "Practice",
              "topics": [
                "Worksheet generator",
                "Multiple choice",
                "Statistics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=algebra1-statistics-data-modeling",
              "thumb": "thumbs/menu-assessment-generator-statistics-data-modeling.svg",
              "description": "Build a standard unit test (multiple choice and short answer, easier to harder) or, as an option, a choice-based restaurant-menu assessment. Pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys with worked solutions. Every answer is checked independently.",
              "type": "Printable",
              "topics": [
                "Test generator",
                "Choice menu",
                "Statistics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Maze Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=maze",
              "thumb": "thumbs/maze-generator-statistics-data-modeling.svg",
              "description": "Make a printable answer maze for this unit: solve the problem in each room and leave through the door with the answer; wrong answers lead to dead ends. CP2/CP1/Honors, up to three versions, answer key with the path and worked solutions. Every door is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=color",
              "thumb": "thumbs/color-generator-statistics-data-modeling.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems and color a picture using a code of answers. Choose the picture or get a surprise; CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=error",
              "thumb": "thumbs/error-generator-statistics-data-modeling.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix. CP2/CP1/Honors, up to three versions, answer key with the correct solution. Every wrong answer is checked to be wrong.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=partner",
              "thumb": "thumbs/partner-generator-statistics-data-modeling.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=who",
              "thumb": "thumbs/who-generator-statistics-data-modeling.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Each correct answer leads to a true clue; every wrong choice is checked to be wrong and leads to a false one. Six cases, a new culprit every time, CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Whodunnit",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=algebra1-statistics-data-modeling&kind=stations",
              "thumb": "thumbs/stations-generator-statistics-data-modeling.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Stations",
                "Statistics"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Statistics Flashcards",
              "path": "artifacts/statistics-data-modeling-flashcards/index.html",
              "thumb": "thumbs/statistics-data-modeling-flashcards.jpg",
              "description": "A fresh deck of statistics flashcards at Easy, Medium or Hard level, every skill at three difficulties. Flip for the answer and a worked solution, mark cards to practice again, and press “New cards” for brand-new problems. Every answer is checked independently.",
              "type": "Practice",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics Showdown",
              "path": "artifacts/statistics-data-modeling-showdown/index.html",
              "thumb": "thumbs/statistics-data-modeling-showdown.jpg",
              "description": "A game board for statistics review: five categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams and name them. Open a problem, show choices if you want them, then reveal the worked solution and award points. A new board is generated every time.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit",
                "Team game"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics Connect Four",
              "path": "artifacts/statistics-data-modeling-connect-four/index.html",
              "thumb": "thumbs/statistics-data-modeling-connect-four.jpg",
              "description": "Connect Four for two teams. Answer a multiple-choice statistics problem to earn a disc; a wrong answer shows the worked solution and passes the turn. CP2/CP1/Honors levels and an optional timer. Every wrong choice is a checked mistake, never a second right answer.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics Tic-Tac-Toe",
              "path": "artifacts/statistics-data-modeling-tic-tac-toe/index.html",
              "thumb": "thumbs/statistics-data-modeling-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice statistics problem to claim a square; a wrong answer lets the other team steal. CP2/CP1/Honors levels and an optional timer. Fresh problems every game.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Statistics: Picture Reveal",
              "path": "artifacts/statistics-data-modeling-picture-reveal/index.html",
              "thumb": "thumbs/statistics-data-modeling-picture-reveal.jpg",
              "description": "Solve 10 statistics problems to uncover a mystery picture. Students type most answers (the checker accepts any correct form), with instant feedback and worked solutions. Choose CP2, CP1 or Honors; “New game” makes new problems and a new picture.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots",
                "Two-way tables",
                "Scatter plots and lines of fit"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "The Stadium Scoreboard Scandal",
              "path": "artifacts/statistics-data-modeling-stadium-scoreboard-scandal/index.html",
              "thumb": "thumbs/statistics-data-modeling-stadium-scoreboard-scandal.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots and outliers",
                "Two-way tables",
                "Lines of fit and residuals",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Escape the Stats Lab",
              "path": "artifacts/statistics-data-modeling-escape-room/index.html",
              "thumb": "thumbs/statistics-data-modeling-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a data wall, a cipher with a hidden shift, a correlation sorting room, a step-ordering lock and dials, a 10-minute timer, hints that cost time, and a final password. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Measures of center and spread",
                "Box plots and outliers",
                "Two-way tables",
                "Lines of fit and residuals",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Statistics and Data Modeling Cheat Sheet",
              "path": "artifacts/statistics-data-modeling-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/statistics-data-modeling-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: center, spread, box plots and outliers. Back: two-way tables, scatter plots, lines of fit and residuals. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Statistics and Data Modeling",
                "Unit 12"
              ],
              "added": "2026-10-25"
            }
          ]
        }
      ]
    },
    {
      "id": "algebra2",
      "name": "Algebra 2",
      "color": "purple",
      "art": "curve",
      "blurb": "Functions, polynomials, logarithms, and beyond.",
      "units": [
        {
          "id": "functions-transformations",
          "name": "Functions & Transformations",
          "artifacts": [
            {
              "title": "The Function Bistro: Assessment Menu",
              "path": "artifacts/functions-transformations-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups, with printed grids for graphing dishes. 100 points total. Includes a teacher guide, rubrics and answer key with computed graphs.",
              "type": "Printable",
              "topics": [
                "Function notation",
                "Transformations",
                "Composition and inverses",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Color By Number",
              "path": "artifacts/functions-transformations-color-by-number/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems on function notation, domain, transformations, piecewise functions, composition and inverses, match each answer to the color code, then color the lighthouse on the island. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Function notation",
                "Transformations",
                "Composition & inverses",
                "Color by number"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Cheat Sheet",
              "path": "artifacts/functions-transformations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: function notation, domain and range, parent functions and transformations. Back: operations, composition, piecewise functions and inverses. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Functions & Transformations",
                "Unit 1"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Functions Four",
              "path": "artifacts/functions-transformations-connect-four/index.html",
              "thumb": "thumbs/functions-transformations-connect-four.jpg",
              "description": "Connect Four for two teams. Evaluate functions, find domain and range, match equations to graphs, transform parent functions, compose and invert, and model with piecewise functions. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Function notation, domain and range",
                "Parent functions and transformations",
                "Piecewise functions and composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Error Analysis",
              "path": "artifacts/functions-transformations-error-analysis/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on function notation, domain, horizontal shifts, reflections, stretches, composition order, inverses and piecewise graphs. Five items include computed correct-versus-student graphs. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Transformations",
                "Function notation",
                "Composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Picture Reveal",
              "path": "artifacts/functions-transformations-picture-reveal/index.html",
              "thumb": "thumbs/functions-transformations-picture-reveal.jpg",
              "description": "Evaluate functions, find domains, read transformed and piecewise graphs, compose and invert functions to uncover a hidden lighthouse scene. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Transformations",
                "Domain",
                "Composition",
                "Piecewise graphs"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Mirror Maze Mayhem",
              "path": "artifacts/functions-transformations-escape-room/index.html",
              "thumb": "thumbs/functions-transformations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a cipher, graph-reading locks, a combination-safe dial puzzle, a logic order lock, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Transformations of graphs",
                "Composition and inverse functions",
                "Domain and range",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Flashcards",
              "path": "artifacts/functions-transformations-flashcards/index.html",
              "thumb": "thumbs/functions-transformations-flashcards.jpg",
              "description": "25 flashcards with worked solutions and computed graphs for function notation, domain and range, parent functions and symmetry, transformations of graphs, piecewise functions, composition, and inverse functions. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Function notation and domain",
                "Parent functions and transformations",
                "Piecewise functions and composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Showdown",
              "path": "artifacts/functions-transformations-jeopardy/index.html",
              "thumb": "thumbs/functions-transformations-jeopardy.jpg",
              "description": "A game board for Functions & Transformations. Evaluate functions and find domains, describe and write transformations from graphs, then finish with piecewise functions, composites, and inverses.",
              "type": "Game",
              "topics": [
                "Function notation and domain",
                "Transformations of graphs",
                "Piecewise functions and composition",
                "Inverse functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Maze",
              "path": "artifacts/functions-transformations-maze/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-maze.jpg",
              "description": "Printable 4-page worksheet: evaluate functions, find domain and range, apply transformations, compose and invert functions to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Function notation, domain and range",
                "Transformations of graphs",
                "Composition and inverse functions",
                "Piecewise and transformed equations"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Stations",
              "path": "artifacts/algebra2-functions-transformations-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-functions-transformations-stations.svg",
              "description": "Printable Algebra 2 station work for Functions & Transformations. Students rotate through four problem sets to practice and review unit skills, with a teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Functions & Transformations"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Tarsia Puzzle",
              "path": "artifacts/functions-transformations-tarsia/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers function notation, piecewise functions, composition, inverse functions, domain and range, and transformations of parent graphs. Includes a show-your-work page and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Composition and inverses",
                "Domain and range",
                "Transformations of graphs",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Vanishing Violin Caper",
              "path": "artifacts/functions-transformations-vanishing-violin-caper/index.html",
              "thumb": "thumbs/functions-transformations-vanishing-violin-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers, with buttons for exponents, absolute value, intervals and function composition.",
              "type": "Game",
              "topics": [
                "Functions & transformations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Functions & Transformations Tic-Tac-Toe",
              "path": "artifacts/functions-transformations-tic-tac-toe/index.html",
              "thumb": "thumbs/functions-transformations-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Functions & transformations",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Vanishing Violin Caper (Printable)",
              "path": "artifacts/functions-transformations-whodunnit/worksheet.pdf",
              "thumb": "thumbs/functions-transformations-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Functions & transformations",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Partner Check 1: Function Operations & Evaluation",
              "path": "artifacts/algebra2-functions-transformations-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-functions-transformations-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Function Operations & Evaluation"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Transformations of Functions",
              "path": "artifacts/algebra2-functions-transformations-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-functions-transformations-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Transformations of Functions"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "linear-functions-systems",
          "name": "Linear Functions & Systems",
          "artifacts": [
            {
              "title": "The Line Cook Bistro: Assessment Menu",
              "path": "artifacts/linear-functions-systems-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups, with printed coordinate grids for graphing dishes. 100 points total. Includes a teacher guide, rubrics and answer key with graphs computed from the equations.",
              "type": "Printable",
              "topics": [
                "Linear equations",
                "Systems of equations",
                "Linear programming",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Color By Number",
              "path": "artifacts/linear-functions-systems-color-by-number/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems on slope, parallel and perpendicular lines, residuals, linear modeling, systems, linear programming and three-variable systems, match each answer to the color code, then color the hot air balloons over the patchwork farms. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Linear modeling",
                "Systems of equations",
                "Linear programming",
                "Color by number"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Cheat Sheet",
              "path": "artifacts/linear-functions-systems-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: slope, forms of a line, parallel and perpendicular lines, and linear models. Back: inequalities, systems, linear programming and three variables. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Linear Functions & Systems",
                "Unit 2"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Crossroads Four",
              "path": "artifacts/linear-functions-systems-connect-four/index.html",
              "thumb": "thumbs/linear-functions-systems-connect-four.jpg",
              "description": "Connect Four for two teams. Find slopes and equations of lines, read graphs and shaded regions, solve systems, fit lines to data, and find the best corner in linear programming. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Slope and equations of lines",
                "Linear inequalities and graphs",
                "Systems of equations and inequalities",
                "Linear programming and best-fit lines"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Error Analysis",
              "path": "artifacts/linear-functions-systems-error-analysis/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on point-slope form, perpendicular slopes, linear models, systems, dashed versus solid boundaries, shading, best-fit lines, linear programming and three-variable systems. Seven items include computed student-versus-correct graphs. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Linear equations",
                "Systems",
                "Inequalities",
                "Linear programming"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Picture Reveal",
              "path": "artifacts/linear-functions-systems-picture-reveal/index.html",
              "thumb": "thumbs/linear-functions-systems-picture-reveal.jpg",
              "description": "Find rates of change, write and graph linear equations and inequalities, solve systems, read residuals, optimize with linear programming and solve three-variable systems to uncover a hidden alpine gondola scene. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Linear equations",
                "Systems",
                "Linear programming",
                "Residuals"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Blizzard at Summit Lodge",
              "path": "artifacts/linear-functions-systems-escape-room/index.html",
              "thumb": "thumbs/linear-functions-systems-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a cipher, a scatter-plot trend line, a feasible-region check, a combination-vault dial puzzle (3 by 3 system), a linear programming order lock, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Linear functions",
                "Systems of equations and inequalities",
                "Linear programming",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Flashcards",
              "path": "artifacts/linear-functions-systems-flashcards/index.html",
              "thumb": "thumbs/linear-functions-systems-flashcards.jpg",
              "description": "25 flashcards with worked solutions and computed graphs for slope and rate of change, writing linear equations, lines of best fit and residuals, linear and absolute value inequalities, systems of two and three equations, and linear programming. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Slope and writing linear equations",
                "Linear modeling and best fit",
                "Systems of equations and inequalities",
                "Linear programming"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Showdown",
              "path": "artifacts/linear-functions-systems-jeopardy/index.html",
              "thumb": "thumbs/linear-functions-systems-jeopardy.jpg",
              "description": "A game board for Linear Functions & Systems. Write equations and model with lines of best fit, solve systems and inequalities (including graphs of shaded regions), then finish with linear programming and three-variable systems.",
              "type": "Game",
              "topics": [
                "Lines and linear models",
                "Systems and inequalities",
                "Linear programming",
                "Three-variable systems"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Maze",
              "path": "artifacts/linear-functions-systems-maze/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-maze.jpg",
              "description": "Printable 4-page worksheet: write linear equations, use parallel and perpendicular slopes, solve systems of two and three equations, fit a regression line, and optimize with linear programming to find the right door through a maze, recording each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Writing and graphing linear equations",
                "Parallel and perpendicular lines",
                "Systems of equations and inequalities",
                "Linear modeling and linear programming"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Stations",
              "path": "artifacts/algebra2-linear-functions-systems-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-linear-functions-systems-stations.svg",
              "description": "Printable Algebra 2 station work for Linear Functions & Systems. Students rotate through four problem sets to practice and review unit skills, with a teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Linear Functions & Systems"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Tarsia Puzzle",
              "path": "artifacts/linear-functions-systems-tarsia/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers writing equations of lines, parallel and perpendicular lines, linear models and lines of best fit, systems of equations and inequalities, linear programming, and three-variable systems. Includes a show-your-work page (with two graphs) and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Writing linear equations",
                "Systems of equations",
                "Linear programming",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Amber Fossil Fiasco",
              "path": "artifacts/linear-functions-systems-amber-fossil-fiasco/index.html",
              "thumb": "thumbs/linear-functions-systems-amber-fossil-fiasco.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type equations of lines in any form, ordered pairs and triples, and inequalities.",
              "type": "Game",
              "topics": [
                "Linear functions & systems",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Linear Functions & Systems Tic-Tac-Toe",
              "path": "artifacts/linear-functions-systems-tic-tac-toe/index.html",
              "thumb": "thumbs/linear-functions-systems-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Linear functions & systems",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Amber Fossil Fiasco (Printable)",
              "path": "artifacts/linear-functions-systems-whodunnit/worksheet.pdf",
              "thumb": "thumbs/linear-functions-systems-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Linear functions & systems",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Partner Check 1: Linear Equations & Graphs",
              "path": "artifacts/algebra2-linear-functions-systems-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-linear-functions-systems-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Linear Equations & Graphs"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Systems of Equations & Inequalities",
              "path": "artifacts/algebra2-linear-functions-systems-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-linear-functions-systems-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Systems of Equations & Inequalities"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "quadratic-functions-complex-numbers",
          "name": "Quadratic Functions & Complex Numbers",
          "artifacts": [
            {
              "title": "The Rising Soufflé Bistro: Assessment Menu",
              "path": "artifacts/quadratic-functions-complex-numbers-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups, with printed coordinate grids for graphing dishes. 100 points total. Includes a teacher guide, rubrics and answer key with graphs computed from the equations.",
              "type": "Printable",
              "topics": [
                "Quadratic functions",
                "Complex numbers",
                "Quadratic formula",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Color By Number",
              "path": "artifacts/quadratic-functions-complex-numbers-color-by-number/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems on vertex form, factoring, completing the square, the discriminant, the quadratic formula, complex number multiplication and division, a projectile model and a quadratic inequality, match each answer to the color code, then color the windmill among the tulip fields. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Quadratic functions",
                "Complex numbers",
                "Quadratic formula & discriminant",
                "Color by number"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratics & Complex Numbers Cheat Sheet",
              "path": "artifacts/quadratic-functions-complex-numbers-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: parabola forms, completing the square, the quadratic formula and the discriminant. Back: complex numbers, quadratic inequalities, linear-quadratic systems and modeling. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Quadratics & Complex Numbers",
                "Unit 3"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Parabola Four",
              "path": "artifacts/quadratic-functions-complex-numbers-connect-four/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-connect-four.jpg",
              "description": "Connect Four for two teams. Match parabola graphs to equations, read vertices and shaded regions, solve quadratics, use the discriminant, and simplify complex numbers. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Parabolas: vertex form, graphs, transformations",
                "Solving quadratics and the discriminant",
                "Imaginary and complex numbers",
                "Quadratic models and inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Error Analysis",
              "path": "artifacts/quadratic-functions-complex-numbers-error-analysis/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on vertex form, completing the square, square roots, the quadratic formula, the discriminant, powers of i, dividing complex numbers and quadratic inequalities. Seven items include computed student-versus-correct graphs. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Quadratics",
                "Complex numbers",
                "Discriminant",
                "Quadratic inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Picture Reveal",
              "path": "artifacts/quadratic-functions-complex-numbers-picture-reveal/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-picture-reveal.jpg",
              "description": "Solve by square roots, write a parabola from its graph, optimize area, find when a projectile lands, use the discriminant, multiply and divide complex numbers and solve quadratic inequalities and systems to uncover a hidden skate park scene. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Quadratics",
                "Complex numbers",
                "Quadratic modeling",
                "Inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Lockdown at Fountain Park",
              "path": "artifacts/quadratic-functions-complex-numbers-escape-room/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with a cipher, a parabola graph to write in vertex form, a graphs-and-discriminants true/false panel, a valve-vault dial puzzle (discriminant, vertex, powers of i), a complex-solutions order lock, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Quadratic functions",
                "Discriminant and vertex form",
                "Complex numbers",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Flashcards",
              "path": "artifacts/quadratic-functions-complex-numbers-flashcards/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-flashcards.jpg",
              "description": "25 flashcards with worked solutions and computed parabola graphs for vertex form, graphing and converting between forms, solving by factoring, square roots, completing the square and the quadratic formula, imaginary and complex numbers (conjugates and division), the discriminant, quadratic modeling, and quadratic inequalities and systems. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Vertex form and graphing parabolas",
                "Solving quadratics",
                "Complex numbers",
                "Quadratic modeling and inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Showdown",
              "path": "artifacts/quadratic-functions-complex-numbers-jeopardy/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-jeopardy.jpg",
              "description": "A game board for Quadratic Functions & Complex Numbers. Write and model with parabolas, simplify, divide and solve with complex numbers, then finish with the discriminant, quadratic inequalities and line-parabola systems, many with computed graphs.",
              "type": "Game",
              "topics": [
                "Parabolas and models",
                "Complex numbers and equations",
                "Discriminant and inequalities",
                "Systems with a parabola"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Maze",
              "path": "artifacts/quadratic-functions-complex-numbers-maze/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-maze.jpg",
              "description": "Printable 4-page worksheet: find vertices, complete the square, use the quadratic formula, simplify powers of i, multiply and divide complex numbers, solve for complex roots, and model with quadratics to find the right door through a maze, recording each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Vertex form and graphing parabolas",
                "Solving quadratics: completing the square and the quadratic formula",
                "Complex numbers and complex roots",
                "Quadratic modeling and inequalities"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Stations",
              "path": "artifacts/algebra2-quadratic-functions-complex-numbers-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-quadratic-functions-complex-numbers-stations.svg",
              "description": "Printable Algebra 2 station work for Quadratic Functions & Complex Numbers. Students rotate through four problem sets covering parabolas and forms, solving quadratics and the discriminant, complex numbers, and quadratic models, inequalities and systems, with a one-page teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Quadratic Functions & Complex Numbers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Tarsia Puzzle",
              "path": "artifacts/quadratic-functions-complex-numbers-tarsia/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers vertex and standard form, solving quadratics four ways, the discriminant, complex number arithmetic and complex roots, quadratic models, and quadratic inequalities. Includes a show-your-work page (with one graph) and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Parabolas and quadratic forms",
                "Quadratic formula and discriminant",
                "Complex numbers",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Backlot Blackout",
              "path": "artifacts/quadratic-functions-complex-numbers-backlot-blackout/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-backlot-blackout.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type vertex-form equations, vertex pairs, exact roots with ±, complex numbers in a + bi form, lists of points and interval answers.",
              "type": "Game",
              "topics": [
                "Quadratic functions & complex numbers",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Quadratic Functions & Complex Numbers Tic-Tac-Toe",
              "path": "artifacts/quadratic-functions-complex-numbers-tic-tac-toe/index.html",
              "thumb": "thumbs/quadratic-functions-complex-numbers-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Quadratic functions & complex numbers",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Backlot Blackout (Printable)",
              "path": "artifacts/quadratic-functions-complex-numbers-whodunnit/worksheet.pdf",
              "thumb": "thumbs/quadratic-functions-complex-numbers-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Quadratic functions & complex numbers",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Partner Check 1: Solving Quadratic Equations",
              "path": "artifacts/algebra2-quadratic-functions-complex-numbers-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-quadratic-functions-complex-numbers-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Solving Quadratic Equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Complex Numbers & Parabolas",
              "path": "artifacts/algebra2-quadratic-functions-complex-numbers-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-quadratic-functions-complex-numbers-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Complex Numbers & Parabolas"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "polynomial-functions",
          "name": "Polynomial Functions",
          "artifacts": [
            {
              "title": "Partner Check 1: Polynomial Operations & Graphs",
              "path": "artifacts/algebra2-polynomial-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-polynomial-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Polynomial Operations & Graphs"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Zeros, Factoring & Inequalities",
              "path": "artifacts/algebra2-polynomial-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-polynomial-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Zeros, Factoring & Inequalities"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "radicals-rational-exponents",
          "name": "Radicals & Rational Exponents",
          "artifacts": [
            {
              "title": "Partner Check 1: Simplifying Radicals & Exponents",
              "path": "artifacts/algebra2-radicals-rational-exponents-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-radicals-rational-exponents-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Simplifying Radicals & Exponents"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Radical Equations & Functions",
              "path": "artifacts/algebra2-radicals-rational-exponents-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-radicals-rational-exponents-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Radical Equations & Functions"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "exponential-logarithmic-functions",
          "name": "Exponential & Logarithmic Functions",
          "artifacts": [
            {
              "title": "The Time Capsule Switcheroo",
              "path": "artifacts/exponential-logarithmic-functions-time-capsule-switcheroo/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-time-capsule-switcheroo.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers, with symbol buttons for exponents, logs and ln.",
              "type": "Game",
              "topics": [
                "Exponential & log equations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Tic-Tac-Toe",
              "path": "artifacts/exponential-logarithmic-functions-tic-tac-toe/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-tic-tac-toe.jpg",
              "description": "Tic-Tac-Toe for two teams. Answer a multiple-choice problem to claim a square. A wrong answer lets the other team steal. Optional timer.",
              "type": "Game",
              "topics": [
                "Exponential & log equations",
                "Team game",
                "Multiple choice"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Time Capsule Switcheroo (Printable)",
              "path": "artifacts/exponential-logarithmic-functions-whodunnit/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-whodunnit.jpg",
              "description": "Printable whodunnit: 10 clue cards to post around the room, each a multiple-choice problem where every answer leads to a clue. Includes a story and case board, a show-your-work page, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Exponential & log equations",
                "Whodunnit",
                "Multiple choice",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exp & Log Functions Tarsia Puzzle",
              "path": "artifacts/exponential-logarithmic-functions-tarsia/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-tarsia.jpg",
              "description": "Printable tarsia puzzle: cut out 24 triangles and match 30 problems to their answers to rebuild a hexagon. Covers exponential and log form, evaluating logs, log properties, exponential and log equations, and modeling. Includes a show-your-work page and a teacher key with the solved hexagon.",
              "type": "Printable",
              "topics": [
                "Log and exponential form",
                "Log properties",
                "Solving exp and log equations",
                "Tarsia puzzle"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "The Logarithm Bistro: Assessment Menu",
              "path": "artifacts/exponential-logarithmic-functions-assessment-menu/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-assessment-menu.jpg",
              "description": "Choice-based test: students order 4 Appetizers, 4 Entrées and 2 Chef’s Specials worth 5, 10 and 20 points, covering all four skill groups. 100 points total. Includes a teacher guide, rubrics and answer key.",
              "type": "Printable",
              "topics": [
                "Exponential functions",
                "Logarithms",
                "Assessment",
                "Choice menu"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Pressure Drop: Escape the Deep",
              "path": "artifacts/exponential-logarithmic-functions-escape-room/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Exponential decay and half-life",
                "Evaluating and solving logarithms",
                "Extraneous solutions",
                "Escape room"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Color By Number",
              "path": "artifacts/exponential-logarithmic-functions-color-by-number/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-color-by-number.jpg",
              "description": "Printable 2-page color-by-number: solve 10 problems, match each answer to the color code, then color the nautilus shell on the sea floor. Page 1 is the picture, page 2 is the work space.",
              "type": "Printable",
              "topics": [
                "Exponential equations",
                "Logarithms",
                "Color by number",
                "Self-checking"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Error Analysis",
              "path": "artifacts/exponential-logarithmic-functions-error-analysis/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-error-analysis.jpg",
              "description": "Find the mistake in 10 worked solutions on logarithm properties, change of base, exponential and log equations, extraneous solutions and compound interest. Explain the error and show the correct work.",
              "type": "Printable",
              "topics": [
                "Log properties",
                "Change of base",
                "Extraneous solutions",
                "Compound interest"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Picture Reveal",
              "path": "artifacts/exponential-logarithmic-functions-picture-reveal/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-picture-reveal.jpg",
              "description": "Convert and evaluate logs, expand and condense, solve exponential and log equations, and model growth and half-life to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Log properties",
                "Change of base",
                "Log equations",
                "Growth and half-life"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Logs Four",
              "path": "artifacts/exponential-logarithmic-functions-connect-four/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Convert between exponential and log form, evaluate and expand logs, solve exponential and log equations, and model growth, decay, and compound interest. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Exponential and log form",
                "Properties of logs and change of base",
                "Solving exponential and log equations",
                "Compound interest and half-life"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exp & Log Functions Flashcards",
              "path": "artifacts/exponential-logarithmic-functions-flashcards/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-flashcards.jpg",
              "description": "25 flashcards with worked solutions for exponential growth and decay, graphs and asymptotes, compound and continuous interest, logarithm form and domain, log properties and change of base, solving exponential and log equations (with extraneous solutions), and half-life, growth, and pH models. Mark cards you need to practice and review them again. Filter by skill and by level (Easy, Medium or Hard).",
              "type": "Practice",
              "topics": [
                "Exponential functions and graphs",
                "Compound interest and e",
                "Logarithm properties",
                "Solving exponential and log equations"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exp & Log Functions Showdown",
              "path": "artifacts/exponential-logarithmic-functions-jeopardy/index.html",
              "thumb": "thumbs/exponential-logarithmic-functions-jeopardy.jpg",
              "description": "A game board for Exponential & Logarithmic Functions. Work with exponential models and compound interest, then log form, domain, expanding and condensing, and finish with exponential and log equations and half-life problems.",
              "type": "Game",
              "topics": [
                "Exponential functions and interest",
                "Logarithm definition and properties",
                "Solving exponential and log equations",
                "Half-life and growth models"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Maze",
              "path": "artifacts/exponential-logarithmic-functions-maze/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-maze.jpg",
              "description": "Printable 4-page worksheet: evaluate logarithms, solve exponential and logarithmic equations and model growth and decay to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Evaluating and expanding logarithms",
                "Solving exponential and log equations",
                "Extraneous solutions",
                "Compound interest and decay models"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Logarithmic Functions Stations",
              "path": "artifacts/algebra2-exponential-logarithmic-functions-stations/worksheet.pdf",
              "thumb": "thumbs/algebra2-exponential-logarithmic-functions-stations.svg",
              "description": "Printable Algebra 2 station work for Exponential & Logarithmic Functions. Students rotate through four problem sets to practice and review unit skills, with a teacher answer key.",
              "type": "Printable",
              "topics": [
                "Stations",
                "Station work",
                "Exponential & Logarithmic Functions"
              ],
              "added": "2026-10-22"
            },
            {
              "title": "Exponential & Log Functions Cheat Sheet",
              "path": "artifacts/exponential-logarithmic-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/exponential-logarithmic-functions-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet. Front: exponential functions, the number e and the logarithm. Back: log properties, solving equations and modeling. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Exponential & Log Functions",
                "Unit 6"
              ],
              "added": "2026-10-25"
            },
            {
              "title": "Partner Check 1: Exponential & Log Basics",
              "path": "artifacts/algebra2-exponential-logarithmic-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-exponential-logarithmic-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Exponential & Log Basics"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Exp & Log Equations and Graphs",
              "path": "artifacts/algebra2-exponential-logarithmic-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-exponential-logarithmic-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Exp & Log Equations and Graphs"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "rational-functions",
          "name": "Rational Functions",
          "artifacts": [
            {
              "title": "Partner Check 1: Rational Expressions & Equations",
              "path": "artifacts/algebra2-rational-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-rational-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Rational Expressions & Equations"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Graphs of Rational Functions",
              "path": "artifacts/algebra2-rational-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-rational-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Graphs of Rational Functions"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "sequences-series",
          "name": "Sequences & Series",
          "artifacts": [
            {
              "title": "Partner Check 1: Arithmetic & Geometric Sequences",
              "path": "artifacts/algebra2-sequences-series-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-sequences-series-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Arithmetic & Geometric Sequences"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Series, Binomials & Applications",
              "path": "artifacts/algebra2-sequences-series-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-sequences-series-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Series, Binomials & Applications"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "conic-sections",
          "name": "Conic Sections",
          "artifacts": [
            {
              "title": "Partner Check 1: Circles & Parabolas",
              "path": "artifacts/algebra2-conic-sections-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-conic-sections-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Circles & Parabolas"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Ellipses & Hyperbolas",
              "path": "artifacts/algebra2-conic-sections-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-conic-sections-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Ellipses & Hyperbolas"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "trigonometric-functions",
          "name": "Trigonometric Functions",
          "artifacts": [
            {
              "title": "Partner Check 1: Radians, Unit Circle & Right-Triangle Trig",
              "path": "artifacts/algebra2-trigonometric-functions-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-trigonometric-functions-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Radians, Unit Circle & Right-Triangle Trig"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Graphs of Trig Functions & Trig Equations",
              "path": "artifacts/algebra2-trigonometric-functions-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-trigonometric-functions-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Graphs of Trig Functions & Trig Equations"
              ],
              "added": "2026-10-24"
            }
          ]
        },
        {
          "id": "probability-statistics",
          "name": "Probability & Statistics",
          "artifacts": [
            {
              "title": "Partner Check 1: Counting & Probability",
              "path": "artifacts/algebra2-probability-statistics-partner-check-1/worksheet.pdf",
              "thumb": "thumbs/algebra2-probability-statistics-partner-check-1.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Counting & Probability"
              ],
              "added": "2026-10-24"
            },
            {
              "title": "Partner Check 2: Statistics & Normal Distributions",
              "path": "artifacts/algebra2-probability-statistics-partner-check-2/worksheet.pdf",
              "thumb": "thumbs/algebra2-probability-statistics-partner-check-2.jpg",
              "description": "Algebra 2 partner check: Partner A and Partner B solve different problems with matching answers. Two student pages; teacher answer key behind code 205.",
              "type": "Printable",
              "topics": [
                "Partner Check",
                "Statistics & Normal Distributions"
              ],
              "added": "2026-10-24"
            }
          ]
        }
      ],
      "comingSoon": false
    },
    {
      "id": "geometry",
      "name": "Geometry",
      "color": "orange",
      "art": "triangle",
      "blurb": "Reasoning, shapes, measurement, and transformations.",
      "units": [
        {
          "id": "foundations-geometry",
          "name": "Foundations of Geometry",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Basics & Reasoning readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-27"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Basics & Reasoning: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-27"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/geometry-worksheet-generator-basics-reasoning.svg",
              "description": "Differentiated Basics & Reasoning worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-27"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-basics-reasoning",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Basics & Reasoning quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-27"
            },
            {
              "title": "Reasoning Four",
              "path": "artifacts/basics-reasoning-connect-four/index.html",
              "description": "Connect Four for two teams on Basics & Reasoning. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/basics-reasoning-connect-four.jpg"
            },
            {
              "title": "Basics & Reasoning Flashcards",
              "path": "artifacts/basics-reasoning-flashcards/index.html",
              "thumb": "thumbs/basics-reasoning-flashcards.jpg",
              "description": "25 flashcards with worked solutions for points, lines and planes, segment and angle addition, midpoints and distance, conditional statements, inductive and deductive reasoning, and the properties used in proofs. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Basics & Reasoning Picture Reveal",
              "path": "artifacts/basics-reasoning-picture-reveal/index.html",
              "description": "Ten typed problems on Basics & Reasoning. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/basics-reasoning-picture-reveal.jpg"
            },
            {
              "title": "Reasoning Showdown",
              "path": "artifacts/basics-reasoning-showdown/index.html",
              "description": "A game board for Basics & Reasoning: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/basics-reasoning-showdown.jpg"
            },
            {
              "title": "The Pirate Cove Puzzle",
              "path": "artifacts/basics-reasoning-pirate-cove-puzzle/index.html",
              "thumb": "thumbs/basics-reasoning-pirate-cove-puzzle.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Segments and angles",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Basics & Reasoning Tic-Tac-Toe",
              "path": "artifacts/basics-reasoning-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Basics & Reasoning. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Segments, midpoints and distance",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Reasoning and proof properties",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/basics-reasoning-tic-tac-toe.jpg"
            },
            {
              "title": "Temple of Logic: Jungle Escape",
              "path": "artifacts/basics-reasoning-escape-room/index.html",
              "thumb": "thumbs/basics-reasoning-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Segment addition and midpoints",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Basics & Reasoning Cheat Sheet",
              "path": "artifacts/geometry-basics-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-basics-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Basics & Reasoning. Front: points, lines, planes, segments, rays and angles. Back: segment and angle addition, midpoints, distance and angle pairs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Basics & Reasoning",
                "Unit 1"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=color",
              "thumb": "thumbs/geometry-color-generator-basics-reasoning.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=error",
              "thumb": "thumbs/geometry-error-generator-basics-reasoning.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-basics-reasoning.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=who",
              "thumb": "thumbs/geometry-who-generator-basics-reasoning.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-basics-reasoning&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-basics-reasoning.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Basics & Reasoning"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "angles-parallel-lines",
          "name": "Angles and Parallel Lines",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Angles & Parallel Lines readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-27"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Angles & Parallel Lines: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-27"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/geometry-worksheet-generator-angles-parallel-lines.svg",
              "description": "Differentiated Angles & Parallel Lines worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-27"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-angles-parallel-lines",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Angles & Parallel Lines quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-27"
            },
            {
              "title": "Angles Four",
              "path": "artifacts/angles-parallel-lines-connect-four/index.html",
              "description": "Connect Four for two teams on Angles & Parallel Lines. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/angles-parallel-lines-connect-four.jpg"
            },
            {
              "title": "Angles & Parallel Lines Flashcards",
              "path": "artifacts/angles-parallel-lines-flashcards/index.html",
              "thumb": "thumbs/angles-parallel-lines-flashcards.jpg",
              "description": "25 flashcards with worked solutions for complementary, supplementary and vertical angles, angles made by a transversal, solving for x, proving lines parallel, and triangle angle sums. Figures are drawn to scale. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Angles & Parallel Lines Picture Reveal",
              "path": "artifacts/angles-parallel-lines-picture-reveal/index.html",
              "description": "Ten typed problems on Angles & Parallel Lines. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/angles-parallel-lines-picture-reveal.jpg"
            },
            {
              "title": "Angles Showdown",
              "path": "artifacts/angles-parallel-lines-showdown/index.html",
              "description": "A game board for Angles & Parallel Lines: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/angles-parallel-lines-showdown.jpg"
            },
            {
              "title": "The Midnight Express Mystery",
              "path": "artifacts/angles-parallel-lines-midnight-express-mystery/index.html",
              "thumb": "thumbs/angles-parallel-lines-midnight-express-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Parallel lines and triangles",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Angles & Parallel Lines Tic-Tac-Toe",
              "path": "artifacts/angles-parallel-lines-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Angles & Parallel Lines. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Proving lines parallel",
                "Triangle and exterior angles",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/angles-parallel-lines-tic-tac-toe.jpg"
            },
            {
              "title": "Crossing Tracks: Rail Yard Escape",
              "path": "artifacts/angles-parallel-lines-escape-room/index.html",
              "thumb": "thumbs/angles-parallel-lines-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Angles & Parallel Lines Cheat Sheet",
              "path": "artifacts/geometry-angles-parallel-lines-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-angles-parallel-lines-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Angles & Parallel Lines. Front: angle pairs and parallel lines cut by a transversal. Back: proving lines parallel, triangle angle sums and angle chasing. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Angles & Parallel Lines",
                "Unit 2"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=color",
              "thumb": "thumbs/geometry-color-generator-angles-parallel-lines.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=error",
              "thumb": "thumbs/geometry-error-generator-angles-parallel-lines.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-angles-parallel-lines.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=who",
              "thumb": "thumbs/geometry-who-generator-angles-parallel-lines.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-angles-parallel-lines&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-angles-parallel-lines.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Angles & Parallel Lines"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "triangle-congruence",
          "name": "Triangle Congruence",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Triangles & Congruence readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Triangles & Congruence: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/geometry-worksheet-generator-triangles-congruence.svg",
              "description": "Differentiated Triangles & Congruence worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-triangles-congruence",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Triangles & Congruence quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Triangles & Congruence Flashcards",
              "path": "artifacts/triangles-congruence-flashcards/index.html",
              "description": "Generated congruence flashcards (matching parts, SSS, SAS, ASA, AAS, HL and proofs) with Easy, Medium, and Hard settings, skill selection, and practice tracking.",
              "type": "Practice",
              "added": "2026-10-28",
              "thumb": "thumbs/triangles-congruence-flashcards.jpg"
            },
            {
              "title": "Congruence Four",
              "path": "artifacts/triangles-congruence-connect-four/index.html",
              "description": "Connect Four for two teams on Triangles & Congruence. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/triangles-congruence-connect-four.jpg"
            },
            {
              "title": "Triangles & Congruence Picture Reveal",
              "path": "artifacts/triangles-congruence-picture-reveal/index.html",
              "description": "Ten typed problems on Triangles & Congruence. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/triangles-congruence-picture-reveal.jpg"
            },
            {
              "title": "Triangles Showdown",
              "path": "artifacts/triangles-congruence-showdown/index.html",
              "description": "A game board for Triangles & Congruence: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/triangles-congruence-showdown.jpg"
            },
            {
              "title": "The Pyramid Puzzle",
              "path": "artifacts/triangles-congruence-pyramid-puzzle/index.html",
              "thumb": "thumbs/triangles-congruence-pyramid-puzzle.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Congruence rules",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Triangles & Congruence Tic-Tac-Toe",
              "path": "artifacts/triangles-congruence-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Triangles & Congruence. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "classifying triangles, angle sums, isosceles triangles and side–angle relationships",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/triangles-congruence-tic-tac-toe.jpg"
            },
            {
              "title": "Lockdown at the Robot Factory",
              "path": "artifacts/triangles-congruence-escape-room/index.html",
              "thumb": "thumbs/triangles-congruence-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Triangle inequality and angle sums",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Triangles & Congruence Cheat Sheet",
              "path": "artifacts/geometry-triangles-congruence-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-triangles-congruence-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Triangles & Congruence. Front: classifying triangles, angle sums, isosceles triangles and side–angle relationships. Back: congruence shortcuts, CPCTC and two-column proofs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Triangles & Congruence",
                "Unit 3"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=color",
              "thumb": "thumbs/geometry-color-generator-triangles-congruence.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=error",
              "thumb": "thumbs/geometry-error-generator-triangles-congruence.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-triangles-congruence.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=who",
              "thumb": "thumbs/geometry-who-generator-triangles-congruence.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangles-congruence&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-triangles-congruence.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangles & Congruence"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "triangle-relationships",
          "name": "Triangle Relationships",
          "artifacts": [
            {
              "title": "Starlight Observatory: Locked Under the Stars",
              "path": "artifacts/triangle-relationships-escape-room/index.html",
              "thumb": "thumbs/triangle-relationships-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key (code 205).",
              "type": "Game",
              "topics": [
                "Triangle relationships",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "The Harbor Museum Compass Caper",
              "path": "artifacts/triangle-relationships-harbor-museum-caper/index.html",
              "thumb": "thumbs/triangle-relationships-harbor-museum-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Triangle relationships",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Triangle Relationships readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-27"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Triangle Relationships: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-27"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/geometry-worksheet-generator-triangle-relationships.svg",
              "description": "Differentiated Triangle Relationships worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-27"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-triangle-relationships",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Triangle Relationships quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-27"
            },
            {
              "title": "Triangle Relationships Flashcards",
              "path": "artifacts/triangle-relationships-flashcards/index.html",
              "description": "Generated triangle angle-sum, exterior-angle, and isosceles-angle flashcards with Easy, Medium, and Hard settings, skill selection, and practice tracking.",
              "type": "Practice",
              "added": "2026-10-18",
              "thumb": "thumbs/triangle-relationships-flashcards.jpg"
            },
            {
              "title": "Triangle Relationships Showdown",
              "path": "artifacts/triangle-relationships-showdown/index.html",
              "description": "A game board for Triangle Relationships: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-showdown.jpg"
            },
            {
              "title": "Triangle Relationships Four",
              "path": "artifacts/triangle-relationships-connect-four/index.html",
              "description": "Connect Four for two teams on Triangle Relationships. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-connect-four.jpg"
            },
            {
              "title": "Triangle Relationships Tic-Tac-Toe",
              "path": "artifacts/triangle-relationships-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Triangle Relationships. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-tic-tac-toe.jpg"
            },
            {
              "title": "Triangle Relationships Picture Reveal",
              "path": "artifacts/triangle-relationships-picture-reveal/index.html",
              "description": "Ten typed problems on Triangle Relationships. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "angle facts, inequalities and special segments in triangles"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/triangle-relationships-picture-reveal.jpg"
            },
            {
              "title": "Triangle Relationships Cheat Sheet",
              "path": "artifacts/geometry-triangle-relationships-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-triangle-relationships-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Triangle Relationships. Front: angle facts, inequalities and special segments in triangles. Back: midsegments, medians, bisectors, altitudes and points of concurrency. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Triangle Relationships",
                "Unit 4"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=color",
              "thumb": "thumbs/geometry-color-generator-triangle-relationships.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=error",
              "thumb": "thumbs/geometry-error-generator-triangle-relationships.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-triangle-relationships.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=who",
              "thumb": "thumbs/geometry-who-generator-triangle-relationships.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-triangle-relationships&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-triangle-relationships.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Triangle Relationships"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "similarity",
          "name": "Similarity",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-similarity",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Similarity readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-similarity",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Similarity: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-similarity",
              "thumb": "thumbs/geometry-worksheet-generator-similarity.svg",
              "description": "Differentiated Similarity worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-similarity",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Similarity quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Similarity Four",
              "path": "artifacts/similarity-connect-four/index.html",
              "description": "Connect Four for two teams on Similarity. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/similarity-connect-four.jpg"
            },
            {
              "title": "Similarity Flashcards",
              "path": "artifacts/similarity-flashcards/index.html",
              "thumb": "thumbs/similarity-flashcards.jpg",
              "description": "25 flashcards with worked solutions on similar figures and scale factor, AA, SAS and SSS similarity, similar triangles inside triangles, the Triangle Proportionality Theorem, perimeter and area ratios, and indirect measurement. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Similarity Picture Reveal",
              "path": "artifacts/similarity-picture-reveal/index.html",
              "description": "Ten typed problems on Similarity. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/similarity-picture-reveal.jpg"
            },
            {
              "title": "Similarity Showdown",
              "path": "artifacts/similarity-showdown/index.html",
              "description": "A game board for Similarity: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/similarity-showdown.jpg"
            },
            {
              "title": "The Toy Workshop Theft",
              "path": "artifacts/similarity-toy-workshop-theft/index.html",
              "thumb": "thumbs/similarity-toy-workshop-theft.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Similar figures",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Similarity Tic-Tac-Toe",
              "path": "artifacts/similarity-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Similarity. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Scale factor and proportions",
                "AA, SAS~ and SSS~",
                "Triangle proportionality theorem",
                "Perimeter, area and indirect measurement",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/similarity-tic-tac-toe.jpg"
            },
            {
              "title": "The Shrink-Ray Workshop",
              "path": "artifacts/similarity-escape-room/index.html",
              "thumb": "thumbs/similarity-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Ratios and proportions",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Similarity Cheat Sheet",
              "path": "artifacts/geometry-similarity-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-similarity-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Similarity. Front: scale factors, similar figures and proportions. Back: similarity criteria, dilations, area and indirect measurement. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Similarity",
                "Unit 5"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=color",
              "thumb": "thumbs/geometry-color-generator-similarity.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=error",
              "thumb": "thumbs/geometry-error-generator-similarity.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-similarity.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=who",
              "thumb": "thumbs/geometry-who-generator-similarity.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-similarity&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-similarity.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Similarity"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "right-triangles-trigonometry",
          "name": "Right Triangles and Trigonometry",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Right Triangles & Trigonometry readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Right Triangles & Trigonometry: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/geometry-worksheet-generator-right-triangles-trigonometry.svg",
              "description": "Differentiated Right Triangles & Trigonometry worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-right-triangles-trigonometry",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Right Triangles & Trigonometry quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Trig Four",
              "path": "artifacts/right-triangles-trigonometry-connect-four/index.html",
              "description": "Connect Four for two teams on Right Triangles & Trigonometry. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/right-triangles-trigonometry-connect-four.jpg"
            },
            {
              "title": "Right Triangles & Trigonometry Flashcards",
              "path": "artifacts/right-triangles-trigonometry-flashcards/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-flashcards.jpg",
              "description": "25 flashcards with worked solutions on the Pythagorean Theorem and its converse, Pythagorean triples, special right triangles, sine, cosine and tangent, finding sides and angles, and angles of elevation and depression. Decimal answers are rounded to one decimal place.",
              "type": "Practice",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Right Triangles & Trigonometry Picture Reveal",
              "path": "artifacts/right-triangles-trigonometry-picture-reveal/index.html",
              "description": "Ten typed problems on Right Triangles & Trigonometry. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/right-triangles-trigonometry-picture-reveal.jpg"
            },
            {
              "title": "Right Triangles Showdown",
              "path": "artifacts/right-triangles-trigonometry-showdown/index.html",
              "description": "A game board for Right Triangles & Trigonometry: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/right-triangles-trigonometry-showdown.jpg"
            },
            {
              "title": "The Lighthouse Lantern Mystery",
              "path": "artifacts/right-triangles-trigonometry-lighthouse-lantern-mystery/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-lighthouse-lantern-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Right triangle trig",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Right Triangles & Trig Tic-Tac-Toe",
              "path": "artifacts/right-triangles-trigonometry-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Right Triangles & Trigonometry. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Elevation and depression",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/right-triangles-trigonometry-tic-tac-toe.jpg"
            },
            {
              "title": "Rotor Rescue: Summit Mission",
              "path": "artifacts/right-triangles-trigonometry-escape-room/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Right Triangles & Trigonometry Cheat Sheet",
              "path": "artifacts/geometry-right-triangles-trigonometry-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-right-triangles-trigonometry-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Right Triangles & Trigonometry. Front: the Pythagorean Theorem, special right triangles and trig ratios. Back: finding sides and angles with SOH-CAH-TOA, elevation and depression. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Right Triangles & Trigonometry",
                "Unit 6"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=color",
              "thumb": "thumbs/geometry-color-generator-right-triangles-trigonometry.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=error",
              "thumb": "thumbs/geometry-error-generator-right-triangles-trigonometry.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-right-triangles-trigonometry.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=who",
              "thumb": "thumbs/geometry-who-generator-right-triangles-trigonometry.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-right-triangles-trigonometry&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-right-triangles-trigonometry.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Right Triangles & Trigonometry"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "quadrilaterals-polygons",
          "name": "Quadrilaterals and Polygons",
          "artifacts": [
            {
              "title": "Lockdown at the Tile Factory",
              "path": "artifacts/quadrilaterals-polygons-escape-room/index.html",
              "thumb": "thumbs/quadrilaterals-polygons-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key (code 205).",
              "type": "Game",
              "topics": [
                "Quadrilaterals and polygons",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "The Mosaic Gallery Heist",
              "path": "artifacts/quadrilaterals-polygons-mosaic-gallery-heist/index.html",
              "thumb": "thumbs/quadrilaterals-polygons-mosaic-gallery-heist.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Quadrilaterals and polygons",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Quadrilaterals & Polygons readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Quadrilaterals & Polygons: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/geometry-worksheet-generator-quadrilaterals-polygons.svg",
              "description": "Differentiated Quadrilaterals & Polygons worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-quadrilaterals-polygons",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Quadrilaterals & Polygons quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Quadrilaterals & Polygons Flashcards",
              "path": "artifacts/quadrilaterals-polygons-flashcards/index.html",
              "description": "Generated polygon-angle and parallelogram flashcards with Easy, Medium, and Hard difficulty, skill selection, and practice tracking.",
              "type": "Practice",
              "added": "2026-10-27",
              "thumb": "thumbs/quadrilaterals-polygons-flashcards.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Showdown",
              "path": "artifacts/quadrilaterals-polygons-showdown/index.html",
              "description": "A game board for Quadrilaterals & Polygons: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-showdown.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Four",
              "path": "artifacts/quadrilaterals-polygons-connect-four/index.html",
              "description": "Connect Four for two teams on Quadrilaterals & Polygons. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-connect-four.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Tic-Tac-Toe",
              "path": "artifacts/quadrilaterals-polygons-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Quadrilaterals & Polygons. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals",
                "Team game"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-tic-tac-toe.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Picture Reveal",
              "path": "artifacts/quadrilaterals-polygons-picture-reveal/index.html",
              "description": "Ten typed problems on Quadrilaterals & Polygons. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "polygon angle sums and the properties of quadrilaterals"
              ],
              "added": "2026-10-28",
              "thumb": "thumbs/quadrilaterals-polygons-picture-reveal.jpg"
            },
            {
              "title": "Quadrilaterals & Polygons Cheat Sheet",
              "path": "artifacts/geometry-quadrilaterals-polygons-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-quadrilaterals-polygons-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Quadrilaterals & Polygons. Front: polygon angle sums and the properties of quadrilaterals. Back: parallelograms, rectangles, rhombuses, trapezoids, kites and coordinate proofs. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Quadrilaterals & Polygons",
                "Unit 7"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=color",
              "thumb": "thumbs/geometry-color-generator-quadrilaterals-polygons.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=error",
              "thumb": "thumbs/geometry-error-generator-quadrilaterals-polygons.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-quadrilaterals-polygons.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=who",
              "thumb": "thumbs/geometry-who-generator-quadrilaterals-polygons.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-quadrilaterals-polygons&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-quadrilaterals-polygons.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Quadrilaterals & Polygons"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "transformations",
          "name": "Transformations",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-transformations",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Transformations readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-transformations",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Transformations: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-transformations",
              "thumb": "thumbs/geometry-worksheet-generator-transformations.svg",
              "description": "Differentiated Transformations worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-transformations",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Transformations quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Transformations Four",
              "path": "artifacts/coordinate-geometry-transformations-connect-four/index.html",
              "description": "Connect Four for two teams on Transformations. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/coordinate-geometry-transformations-connect-four.jpg"
            },
            {
              "title": "Coordinate Geometry & Transformations Flashcards",
              "path": "artifacts/coordinate-geometry-transformations-flashcards/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-flashcards.jpg",
              "description": "25 flashcards with worked solutions for distance, midpoint and slope, classifying figures on the coordinate plane, translations, reflections, rotations, dilations and compositions. Graphs are drawn to scale. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Coordinate Geometry & Transformations Picture Reveal",
              "path": "artifacts/coordinate-geometry-transformations-picture-reveal/index.html",
              "description": "Ten typed problems on Transformations. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/coordinate-geometry-transformations-picture-reveal.jpg"
            },
            {
              "title": "Coordinate Showdown",
              "path": "artifacts/coordinate-geometry-transformations-showdown/index.html",
              "description": "A game board for Transformations: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/coordinate-geometry-transformations-showdown.jpg"
            },
            {
              "title": "The Treasure Map Mystery",
              "path": "artifacts/coordinate-geometry-transformations-treasure-map-mystery/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-treasure-map-mystery.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Transformations",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Transformations Tic-Tac-Toe",
              "path": "artifacts/coordinate-geometry-transformations-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Transformations. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Classifying figures from coordinates",
                "Translations, reflections, rotations and dilations",
                "Compositions and congruence",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/coordinate-geometry-transformations-tic-tac-toe.jpg"
            },
            {
              "title": "Glitch World: Trapped in the Game",
              "path": "artifacts/coordinate-geometry-transformations-escape-room/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Transformations Cheat Sheet",
              "path": "artifacts/geometry-coordinate-transformations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-coordinate-transformations-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Transformations. Front: distance, midpoint, slope and translations. Back: reflections, rotations, dilations and sequences of transformations. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Transformations",
                "Unit 8"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=color",
              "thumb": "thumbs/geometry-color-generator-transformations.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=error",
              "thumb": "thumbs/geometry-error-generator-transformations.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-transformations.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=who",
              "thumb": "thumbs/geometry-who-generator-transformations.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-transformations&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-transformations.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Transformations"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "circles",
          "name": "Circles",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-circles",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Circles readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-circles",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Circles: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-circles",
              "thumb": "thumbs/geometry-worksheet-generator-circles.svg",
              "description": "Differentiated Circles worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-circles",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Circles quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Circles Four",
              "path": "artifacts/circles-connect-four/index.html",
              "description": "Connect Four for two teams on Circles. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/circles-connect-four.jpg"
            },
            {
              "title": "Circles Flashcards",
              "path": "artifacts/circles-flashcards/index.html",
              "thumb": "thumbs/circles-flashcards.jpg",
              "description": "25 flashcards with worked solutions for parts of a circle, circumference and area, arcs and sectors, central and inscribed angles, tangents and chords, and equations of circles. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Circles Picture Reveal",
              "path": "artifacts/circles-picture-reveal/index.html",
              "description": "Ten typed problems on Circles. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/circles-picture-reveal.jpg"
            },
            {
              "title": "Circles Showdown",
              "path": "artifacts/circles-showdown/index.html",
              "description": "A game board for Circles: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/circles-showdown.jpg"
            },
            {
              "title": "The Carnival Caper",
              "path": "artifacts/circles-carnival-caper/index.html",
              "thumb": "thumbs/circles-carnival-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Circle measures",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Circles Tic-Tac-Toe",
              "path": "artifacts/circles-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Circles. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/circles-tic-tac-toe.jpg"
            },
            {
              "title": "Carnival After Dark: Locked In the Midway",
              "path": "artifacts/circles-escape-room/index.html",
              "thumb": "thumbs/circles-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Circles Cheat Sheet",
              "path": "artifacts/geometry-circles-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-circles-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Circles. Front: parts of a circle, circumference, area, arcs and sectors. Back: inscribed angles, chords, tangents and angles inside and outside a circle. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Circles",
                "Unit 9"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=color",
              "thumb": "thumbs/geometry-color-generator-circles.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=error",
              "thumb": "thumbs/geometry-error-generator-circles.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-circles.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=who",
              "thumb": "thumbs/geometry-who-generator-circles.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-circles&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-circles.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Circles"
              ],
              "added": "2026-10-28"
            }
          ]
        },
        {
          "id": "area-surface-area-volume",
          "name": "Area, Surface Area and Volume",
          "artifacts": [
            {
              "title": "Assessment Readiness Check",
              "path": "worksheet-generator/practice-test.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/practice-test.svg",
              "description": "A Area, Surface Area & Volume readiness check at three levels (CP2, CP1, Honors). Every problem and diagram is generated and independently verified, and the teacher key stays behind the teacher code.",
              "type": "Study Guide",
              "added": "2026-10-28"
            },
            {
              "title": "Daily Lesson Planner",
              "path": "worksheet-generator/lesson-planner.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/lesson-planner-geometry.svg",
              "description": "Day-by-day lesson plans for Geometry, including Area, Surface Area & Volume: do now, notes, examples, practice, exit ticket, handouts and PowerPoint, all with verified problems.",
              "type": "Planning",
              "added": "2026-10-28"
            },
            {
              "title": "Worksheet Generator",
              "path": "worksheet-generator/worksheet.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/geometry-worksheet-generator-area-surface-area-volume.svg",
              "description": "Differentiated Area, Surface Area & Volume worksheets with accurate diagrams and a verified answer key. Choose skills, level and how many problems.",
              "type": "Practice",
              "added": "2026-10-28"
            },
            {
              "title": "Assessment Generator",
              "path": "worksheet-generator/menu-assessment.html#unit=geometry-area-surface-area-volume",
              "thumb": "thumbs/menu-assessment-generator-geometry.svg",
              "description": "Build Area, Surface Area & Volume quizzes and tests, versions A to C, with diagrams, open response and a verified teacher key.",
              "type": "Printable",
              "added": "2026-10-28"
            },
            {
              "title": "Volume Four",
              "path": "artifacts/area-surface-area-volume-connect-four/index.html",
              "description": "Connect Four for two teams on Area, Surface Area & Volume. A correct multiple-choice answer drops a disc; a miss shows the worked solution and passes the turn. Verified problems with diagrams, three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/area-surface-area-volume-connect-four.jpg"
            },
            {
              "title": "Area, Surface Area & Volume Flashcards",
              "path": "artifacts/area-surface-area-volume-flashcards/index.html",
              "thumb": "thumbs/area-surface-area-volume-flashcards.jpg",
              "description": "25 flashcards with worked solutions for area of polygons and composite figures, volume and surface area of prisms, cylinders, pyramids, cones and spheres, unit conversions, scale factors and real-world problems. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Area, Surface Area & Volume Picture Reveal",
              "path": "artifacts/area-surface-area-volume-picture-reveal/index.html",
              "description": "Ten typed problems on Area, Surface Area & Volume. Each correct answer, checked by the independent verifier, uncovers a piece of a hidden picture. Worked solutions after each answer.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/area-surface-area-volume-picture-reveal.jpg"
            },
            {
              "title": "Measurement Showdown",
              "path": "artifacts/area-surface-area-volume-showdown/index.html",
              "description": "A game board for Area, Surface Area & Volume: six skill categories, 100 to 500 points, CP2/CP1/Honors or mixed boards. Add up to eight teams, open a problem with its diagram, show choices if you want them, then reveal the worked solution. A new board every time.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems",
                "Team game"
              ],
              "added": "2026-10-18",
              "thumb": "thumbs/area-surface-area-volume-showdown.jpg"
            },
            {
              "title": "The Candy Factory Caper",
              "path": "artifacts/area-surface-area-volume-candy-factory-caper/index.html",
              "thumb": "thumbs/area-surface-area-volume-candy-factory-caper.jpg",
              "description": "Detective game: solve each problem to unlock a clue, clear suspects, places and methods off the case board, then name the culprit. Students type their answers.",
              "type": "Game",
              "topics": [
                "Area, surface area, volume",
                "Detective game",
                "Typed answers"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Area, Surface Area & Volume Tic-Tac-Toe",
              "path": "artifacts/area-surface-area-volume-tic-tac-toe/index.html",
              "description": "Tic-Tac-Toe for two teams on Area, Surface Area & Volume. Claim a square with a correct answer; a miss lets the other team steal. Verified problems with diagrams and an optional timer.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Unit conversions and scale factors",
                "Real-world volume problems",
                "Team game"
              ],
              "added": "2026-10-21",
              "thumb": "thumbs/area-surface-area-volume-tic-tac-toe.jpg"
            },
            {
              "title": "The Pharaoh’s Pyramid: Sealed Inside",
              "path": "artifacts/area-surface-area-volume-escape-room/index.html",
              "thumb": "thumbs/area-surface-area-volume-escape-room.jpg",
              "description": "Story-driven escape room for teams: five rooms with ciphers, hidden clues, figures and logic locks, a 10-minute timer, hints that cost time, and a final puzzle. Add #key to the address for the teacher answer key.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Escape room",
                "Teamwork"
              ],
              "added": "2026-10-21"
            },
            {
              "title": "Area, Surface Area & Volume Cheat Sheet",
              "path": "artifacts/geometry-area-surface-area-volume-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-area-surface-area-volume-cheat-sheet.jpg",
              "description": "Two-page printable cheat sheet for Area, Surface Area & Volume. Front: area formulas, composite figures and units. Back: surface area and volume of prisms, cylinders, pyramids, cones and spheres. Key vocabulary, worked examples with every answer checked, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Cheat sheet",
                "Reference",
                "Area, Surface Area & Volume",
                "Unit 10"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Color by Number Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=color",
              "thumb": "thumbs/geometry-color-generator-area-surface-area-volume.svg",
              "description": "Make a color-by-number page for this unit: students solve numbered problems, with the diagram beside each one, and color a picture using a code of answers. CP2/CP1/Honors, up to three versions, colored answer key with worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Error Analysis Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=error",
              "thumb": "thumbs/geometry-error-generator-area-surface-area-volume.svg",
              "description": "Make an error-analysis worksheet for this unit: each student’s worked solution has one mistake to find, explain and fix, with the diagram shown. CP2/CP1/Honors, up to three versions, answer key with the correct solution.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Partner Check Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=partner",
              "thumb": "thumbs/geometry-partner-generator-area-surface-area-volume.svg",
              "description": "Make a partner check for this unit: Partner A and Partner B solve different problems with the same answers, then compare. CP2/CP1/Honors, up to three versions, answer key with both partners’ solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Whodunnit Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=who",
              "thumb": "thumbs/geometry-who-generator-area-surface-area-volume.svg",
              "description": "Make a printable whodunnit for this unit: 10 clue cards with four answer choices, a case board and a Show Your Work page. Every wrong choice is checked to be wrong. CP2/CP1/Honors, up to three versions, and a teacher key.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            },
            {
              "title": "Stations Generator",
              "path": "worksheet-generator/printables.html#unit=geometry-area-surface-area-volume&kind=stations",
              "thumb": "thumbs/geometry-stations-generator-area-surface-area-volume.svg",
              "description": "Make station pages for this unit: choose 2–6 stations and 6–10 problems each, and the chosen skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions.",
              "type": "Printable",
              "topics": [
                "Printable generator",
                "Area, Surface Area & Volume"
              ],
              "added": "2026-10-28"
            }
          ]
        }
      ],
      "comingSoon": false
    }
    ,  {
      "id": "prealgebra",
      "name": "Pre-Algebra (8th Grade)",
      "color": "purple",
      "art": "curve",
      "blurb": "Grade 8 mathematics: real numbers, equations, functions, data, transformations, and geometry.",
      "units": [
          {
              "id": "real-numbers-exponents",
              "name": "Real Numbers and Exponents",
              "artifacts": []
          },
          {
              "id": "equations-expressions",
              "name": "Equations and Expressions",
              "artifacts": []
          },
          {
              "id": "linear-functional-relationships",
              "name": "Linear and Functional Relationships",
              "artifacts": []
          },
          {
              "id": "systems-linear-equations",
              "name": "Systems of Linear Equations",
              "artifacts": []
          },
          {
              "id": "patterns-bivariate-data",
              "name": "Patterns and Bivariate Data",
              "artifacts": []
          },
          {
              "id": "congruence-similarity",
              "name": "Congruence and Similarity",
              "artifacts": []
          },
          {
              "id": "geometry-applications",
              "name": "Geometry",
              "artifacts": []
          }
      ],
      "comingSoon": false
  }
  ]
};
