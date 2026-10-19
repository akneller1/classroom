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
  "tagline": "Interactive math games and practice for Algebra and Geometry. Pick a course, choose a unit, and open an activity on any device.",
  "footer": "Activities open in a new tab and run in any modern browser. Saved activities are kept in this browser only.",
  "newDays": 30,
  "courses": [
    {
      "id": "algebra",
      "name": "Algebra",
      "color": "blue",
      "art": "curve",
      "blurb": "Equations, inequalities, functions, and polynomials.",
      "units": [
        {
          "id": "expressions-equations",
          "name": "Expressions & Equations",
          "artifacts": [
            {
              "title": "Expressions & Equations Cheat Sheet",
              "path": "artifacts/expressions-equations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/expressions-equations-cheat-sheet.svg",
              "description": "Colorful two-page printable study guide: Expressions, equations, order of operations, combining like terms, multi-step solving, proportions and formulas.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Reference", "Expressions & Equations"],
              "added": "2026-10-19"
            },
            {
              "title": "Equations Four",
              "path": "artifacts/expressions-equations-connect-four/index.html",
              "thumb": "thumbs/expressions-equations-connect-four.jpg",
              "description": "Connect Four for two teams. Simplify, evaluate, or solve to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Multi-step equations",
                "Literal equations"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Expressions & Equations Flashcards",
              "path": "artifacts/expressions-equations-flashcards/index.html",
              "thumb": "thumbs/expressions-equations-flashcards.jpg",
              "description": "25 flashcards with worked solutions for vocabulary, evaluating, simplifying, solving equations, proportions and applications. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Evaluating expressions",
                "Simplifying",
                "Solving equations",
                "Proportions"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Expressions & Equations Picture Reveal",
              "path": "artifacts/expressions-equations-picture-reveal/index.html",
              "thumb": "thumbs/expressions-equations-picture-reveal.jpg",
              "description": "Evaluate, simplify and solve 10 problems to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Evaluating expressions",
                "Simplifying",
                "Solving equations",
                "Proportions"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Equations Showdown",
              "path": "artifacts/expressions-equations-jeopardy/index.html",
              "thumb": "thumbs/expressions-equations-jeopardy.jpg",
              "description": "A game board for Expressions and Equations. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Combining like terms",
                "Distributive property",
                "Multi-step equations",
                "Literal equations"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Solving Equations Maze",
              "path": "artifacts/expressions-equations-maze/worksheet.pdf",
              "thumb": "thumbs/expressions-equations-maze.jpg",
              "description": "Printable 4-page worksheet: solve multi-step equations to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Multi-step equations",
                "Distributive property",
                "Variables on both sides"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Expressions & Equations Error Analysis",
              "path": "artifacts/expressions-equations-error-analysis/worksheet.pdf",
              "thumb": "thumbs/expressions-equations-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Distributive property",
                "Combining like terms",
                "Multi-step equations",
                "Literal equations"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "inequalities",
          "name": "Inequalities",
          "artifacts": [
            {
              "title": "Inequalities Cheat Sheet",
              "path": "Mr_Ks_Algebra_Inequalities_Cheat_Sheet.pdf",
              "thumb": "thumbs/inequalities-cheat-sheet.svg",
              "description": "Colorful, two-page printable reference sheet covering inequality vocabulary and symbols, number-line graphs, solving and checking inequalities, compound inequalities, and common mistakes.",
              "type": "Printable",
              "topics": [
                "Inequality symbols and vocabulary",
                "Number-line graphs",
                "Solving inequalities",
                "Compound inequalities"
              ],
              "added": "2026-10-19"
            },
            {
              "title": "Compound Inequalities Picture Reveal",
              "path": "artifacts/compound-inequalities-picture-reveal/index.html",
              "thumb": "thumbs/compound-inequalities-picture-reveal.jpg",
              "description": "Solve 10 compound inequalities to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Compound inequalities",
                "AND and OR",
                "Solving inequalities"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Compound Inequalities Maze",
              "path": "artifacts/compound-inequalities-maze/worksheet.pdf",
              "thumb": "thumbs/compound-inequalities-maze.svg",
              "description": "Printable 4-page worksheet: solve compound inequalities to navigate a maze, then graph solutions on number lines. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Compound inequalities",
                "Number line graphs",
                "Maze worksheet"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Inequalities Flashcards",
              "path": "artifacts/inequalities-flashcards/index.html",
              "thumb": "thumbs/inequalities-flashcards.jpg",
              "description": "25 flashcards with worked solutions and number-line graphs: translating, testing solutions, one- and multi-step inequalities, flipping the sign, compound inequalities, special cases and word problems. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Translating and testing solutions",
                "Solving and flipping the sign",
                "Graphing on a number line",
                "Compound inequalities"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Inequality Four",
              "path": "artifacts/inequality-four/index.html",
              "thumb": "thumbs/inequality-four.jpg",
              "description": "Connect Four for two teams. Solve, graph, or translate a compound inequality to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Compound inequalities",
                "Number line graphs"
              ],
              "added": "2026-10-16"
            },
            {
              "title": "Inequality Showdown",
              "path": "artifacts/inequality-showdown/index.html",
              "thumb": "thumbs/inequality-showdown.jpg",
              "description": "A game board for Algebra 1 review. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Compound inequalities",
                "Absolute value inequalities"
              ],
              "added": "2026-10-16"
            },
            {
              "title": "Inequalities Error Analysis",
              "path": "artifacts/inequalities-error-analysis/worksheet.pdf",
              "thumb": "thumbs/inequalities-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Dividing by a negative",
                "Compound inequalities",
                "AND and OR",
                "Number-line graphs"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "linear-equations-slope",
          "name": "Linear Equations & Slope",
          "artifacts": [
            {
              "title": "Linear Equations & Slope Cheat Sheet",
              "path": "artifacts/linear-equations-slope-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/linear-equations-slope-cheat-sheet.svg",
              "description": "Colorful two-page printable study guide: Slope, rate of change, linear equation forms, intercepts, graphing, and parallel and perpendicular lines.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Reference", "Linear Equations & Slope"],
              "added": "2026-10-19"
            },
            {
              "title": "Slope Four",
              "path": "artifacts/linear-equations-slope-connect-four/index.html",
              "thumb": "thumbs/linear-equations-slope-connect-four.jpg",
              "description": "Connect Four for two teams. Find slopes, intercepts, and equations of lines, and read graphs, to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Slope from points, tables, and graphs",
                "Slope-intercept, point-slope, and standard form",
                "Parallel and perpendicular lines",
                "Linear models"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Linear Equations & Slope Flashcards",
              "path": "artifacts/linear-equations-slope-flashcards/index.html",
              "thumb": "thumbs/linear-equations-slope-flashcards.jpg",
              "description": "25 flashcards with worked solutions for slope, slope-intercept, point-slope and standard form, writing equations of lines, parallel and perpendicular lines, intercepts and rate of change. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Slope from points, graphs and tables",
                "Slope-intercept, point-slope and standard form",
                "Parallel and perpendicular lines",
                "Rate of change"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Linear Equations & Slope Picture Reveal",
              "path": "artifacts/linear-equations-slope-picture-reveal/index.html",
              "thumb": "thumbs/linear-equations-slope-picture-reveal.jpg",
              "description": "Find slopes, intercepts and equations of lines to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Slope from points and graphs",
                "Slope-intercept and point-slope form",
                "Parallel and perpendicular lines",
                "Rate of change"
              ],
              "added": "2026-10-18"
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
              "title": "Slope Showdown",
              "path": "artifacts/linear-equations-slope-jeopardy/index.html",
              "thumb": "thumbs/linear-equations-slope-jeopardy.jpg",
              "description": "A game board for Linear Equations and Slope. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Slope from points, tables, and graphs",
                "Slope-intercept, point-slope, and standard form",
                "Parallel and perpendicular lines",
                "Linear models"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Slope & Linear Equations Maze",
              "path": "artifacts/linear-equations-slope-maze/worksheet.pdf",
              "thumb": "thumbs/linear-equations-slope-maze.jpg",
              "description": "Printable 4-page worksheet: find slopes and write equations in slope-intercept form to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Slope from two points",
                "Slope from an equation",
                "Writing y = mx + b"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Linear Equations & Slope Error Analysis",
              "path": "artifacts/linear-equations-slope-error-analysis/worksheet.pdf",
              "thumb": "thumbs/linear-equations-slope-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Slope",
                "Slope-intercept form",
                "Parallel and perpendicular lines",
                "Intercepts"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "graphing-inequalities",
          "name": "Graphing Inequalities on the Coordinate Plane",
          "artifacts": [
            {
              "title": "Graphing Inequalities Cheat Sheet",
              "path": "artifacts/graphing-inequalities-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/graphing-inequalities-cheat-sheet.svg",
              "description": "Colorful two-page printable study guide: Graphing linear inequalities on the coordinate plane, boundary lines, shading, and systems.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Reference", "Graphing Inequalities"],
              "added": "2026-10-19"
            },
            {
              "title": "Inequality Graphs Four",
              "path": "artifacts/graphing-inequalities-connect-four/index.html",
              "thumb": "thumbs/graphing-inequalities-connect-four.jpg",
              "description": "Connect Four for two teams. Test points, choose solid or dashed lines, decide the shading, and match graphs to inequalities to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Solid and dashed boundary lines",
                "Rewriting in slope-intercept form",
                "Test points and shading",
                "Systems of inequalities"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Graphing Inequalities Flashcards",
              "path": "artifacts/graphing-inequalities-flashcards/index.html",
              "thumb": "thumbs/graphing-inequalities-flashcards.jpg",
              "description": "25 flashcards with worked solutions and shaded graphs for inequalities in two variables: solid or dashed boundary lines, test points, shading, writing an inequality from a graph, systems, and real-world constraints. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Solid and dashed boundary lines",
                "Test points and shading",
                "Writing inequalities from graphs",
                "Systems of inequalities"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Graphing Inequalities Picture Reveal",
              "path": "artifacts/graphing-inequalities-picture-reveal/index.html",
              "thumb": "thumbs/graphing-inequalities-picture-reveal.jpg",
              "description": "Test points, read boundary lines and shading, and work with systems of inequalities to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Test points",
                "Solid or dashed boundary lines",
                "Writing inequalities from graphs",
                "Systems of inequalities"
              ],
              "added": "2026-10-18"
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
              "title": "Inequality Graphs Showdown",
              "path": "artifacts/graphing-inequalities-jeopardy/index.html",
              "thumb": "thumbs/graphing-inequalities-jeopardy.jpg",
              "description": "A game board for graphing linear inequalities. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Solid and dashed boundary lines",
                "Rewriting in slope-intercept form",
                "Test points and shading",
                "Systems of inequalities"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Graphing Inequalities Error Analysis",
              "path": "artifacts/graphing-inequalities-error-analysis/worksheet.pdf",
              "thumb": "thumbs/graphing-inequalities-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 incorrect graphs and solutions. Students find the error, explain it, and graph the correct answer.",
              "type": "Printable",
              "topics": [
                "Solid vs. dashed boundary",
                "Shading and test points",
                "Graphing linear inequalities"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "systems-of-equations",
          "name": "Systems of Equations",
          "artifacts": [
            {
              "title": "Systems of Equations Cheat Sheet",
              "path": "artifacts/systems-of-equations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/systems-of-equations-cheat-sheet.svg",
              "description": "Colorful two-page printable study guide: Solving systems by graphing, substitution and elimination, with corrected graphs and applications.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Reference", "Systems of Equations"],
              "added": "2026-10-19"
            },
            {
              "title": "Systems Four",
              "path": "artifacts/systems-of-equations-connect-four/index.html",
              "thumb": "thumbs/systems-of-equations-connect-four.jpg",
              "description": "Connect Four for two teams. Check a solution, solve by substitution or elimination, read a graph, or model a story. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Checking and graphing solutions",
                "Substitution",
                "Elimination",
                "Special cases and word problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Systems of Equations Flashcards",
              "path": "artifacts/systems-of-equations-flashcards/index.html",
              "thumb": "thumbs/systems-of-equations-flashcards.jpg",
              "description": "25 flashcards with worked solutions for checking solutions, reading graphs and tables, substitution, elimination, special cases, choosing a method and word problems. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Checking and graphing",
                "Substitution",
                "Elimination",
                "No or infinite solutions",
                "Word problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Systems of Equations Picture Reveal",
              "path": "artifacts/systems-of-equations-picture-reveal/index.html",
              "thumb": "thumbs/systems-of-equations-picture-reveal.jpg",
              "description": "Solve systems by graphing, substitution and elimination, then tackle word problems to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Solving by graphing",
                "Substitution",
                "Elimination",
                "Word problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Systems Showdown",
              "path": "artifacts/systems-of-equations-jeopardy/index.html",
              "thumb": "thumbs/systems-of-equations-jeopardy.jpg",
              "description": "A game board for Systems of Equations. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Checking and graphing solutions",
                "Substitution",
                "Elimination",
                "Special cases and word problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Systems of Equations Maze",
              "path": "artifacts/systems-of-equations-maze/worksheet.pdf",
              "thumb": "thumbs/systems-of-equations-maze.jpg",
              "description": "Printable 4-page worksheet: solve systems of linear equations by substitution or elimination to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Solving by substitution",
                "Solving by elimination",
                "No solution and infinitely many solutions"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Systems of Equations Error Analysis",
              "path": "artifacts/systems-of-equations-error-analysis/worksheet.pdf",
              "thumb": "thumbs/systems-of-equations-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Substitution",
                "Elimination",
                "No solution and infinite solutions",
                "Writing systems"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "exponents-exponential-functions",
          "name": "Exponents & Exponential Functions",
          "artifacts": [
            {
              "title": "Exponents & Exponential Functions Cheat Sheet",
              "path": "artifacts/exponents-exponential-functions-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/exponents-exponential-functions-cheat-sheet.svg",
              "description": "Colorful two-page printable guide to exponent rules, scientific notation, exponential growth and decay, and worked examples.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Reference", "Exponents & Exponential Functions"],
              "added": "2026-10-19"
            },
            {
              "title": "Exponents Four",
              "path": "artifacts/exponents-exponential-functions-connect-four/index.html",
              "thumb": "thumbs/exponents-exponential-functions-connect-four.jpg",
              "description": "Connect Four for two teams. Use exponent rules, scientific notation, and exponential growth and decay to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Zero and negative exponents",
                "Scientific notation",
                "Exponential growth and decay"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Exponents & Exponential Functions Flashcards",
              "path": "artifacts/exponents-exponential-functions-flashcards/index.html",
              "thumb": "thumbs/exponents-exponential-functions-flashcards.jpg",
              "description": "25 flashcards with worked solutions for exponent rules, zero and negative exponents, scientific notation, exponential functions, growth and decay, and compound-growth word problems. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Exponent rules",
                "Zero and negative exponents",
                "Scientific notation",
                "Exponential growth and decay"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Exponents & Exponential Functions Picture Reveal",
              "path": "artifacts/exponents-exponential-functions-picture-reveal/index.html",
              "thumb": "thumbs/exponents-exponential-functions-picture-reveal.jpg",
              "description": "Use exponent rules, scientific notation, exponential equations and growth and decay to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Scientific notation",
                "Exponential equations",
                "Growth and decay"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Exponents Showdown",
              "path": "artifacts/exponents-exponential-functions-jeopardy/index.html",
              "thumb": "thumbs/exponents-exponential-functions-jeopardy.jpg",
              "description": "A game board for Exponents and Exponential Functions. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Exponent rules",
                "Zero and negative exponents",
                "Scientific notation",
                "Exponential growth and decay"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Exponent Rules Maze",
              "path": "artifacts/exponents-exponential-functions-maze/worksheet.pdf",
              "thumb": "thumbs/exponents-exponential-functions-maze.jpg",
              "description": "Printable 4-page worksheet: simplify and evaluate expressions with the exponent rules to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Product, quotient and power rules",
                "Zero and negative exponents",
                "Evaluating powers"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Exponents & Exponential Functions Error Analysis",
              "path": "artifacts/exponents-exponential-functions-error-analysis/worksheet.pdf",
              "thumb": "thumbs/exponents-exponential-functions-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Exponent rules",
                "Negative and zero exponents",
                "Exponential growth and decay"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "polynomials-factoring",
          "name": "Polynomials & Factoring",
          "artifacts": [
            {
              "title": "Polynomials & Factoring Cheat Sheet",
              "path": "artifacts/polynomials-factoring-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/polynomials-factoring-cheat-sheet.svg",
              "description": "Colorful two-page printable guide to polynomial operations, multiplication, special products, factoring methods, and solving by factoring.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Reference", "Polynomials & Factoring"],
              "added": "2026-10-19"
            },
            {
              "title": "Factoring Four",
              "path": "artifacts/polynomials-factoring-connect-four/index.html",
              "thumb": "thumbs/polynomials-factoring-connect-four.jpg",
              "description": "Connect Four for two teams. Multiply, factor, or solve to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Adding, subtracting and multiplying polynomials",
                "GCF and trinomial factoring",
                "Difference of squares",
                "Zero-product property"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Polynomials & Factoring Flashcards",
              "path": "artifacts/polynomials-factoring-flashcards/index.html",
              "thumb": "thumbs/polynomials-factoring-flashcards.jpg",
              "description": "25 flashcards with worked solutions for classifying, adding, subtracting and multiplying polynomials, then factoring with GCF, trinomials, difference of squares and factoring completely. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Adding, subtracting and multiplying polynomials",
                "GCF and trinomial factoring",
                "Difference of squares",
                "Factoring completely"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Polynomials & Factoring Picture Reveal",
              "path": "artifacts/polynomials-factoring-picture-reveal/index.html",
              "thumb": "thumbs/polynomials-factoring-picture-reveal.jpg",
              "description": "Add, multiply and factor polynomials, then use factoring to solve area problems and uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Factoring trinomials",
                "Factoring completely"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Polynomials Showdown",
              "path": "artifacts/polynomials-factoring-jeopardy/index.html",
              "thumb": "thumbs/polynomials-factoring-jeopardy.jpg",
              "description": "A game board for Polynomials and Factoring. Add, subtract, and multiply polynomials, factor every way you know, and use the zero-product property.",
              "type": "Game",
              "topics": [
                "Adding, subtracting and multiplying polynomials",
                "GCF and trinomial factoring",
                "Difference of squares",
                "Zero-product property"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Factoring Maze",
              "path": "artifacts/polynomials-factoring-maze/worksheet.pdf",
              "thumb": "thumbs/polynomials-factoring-maze.jpg",
              "description": "Printable 4-page worksheet: factor trinomials, differences of squares, and GCF problems completely to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Factoring x^2 + bx + c and ax^2 + bx + c",
                "Difference of squares",
                "Factoring out the GCF first"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Polynomials & Factoring Error Analysis",
              "path": "artifacts/polynomials-factoring-error-analysis/worksheet.pdf",
              "thumb": "thumbs/polynomials-factoring-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Adding and subtracting polynomials",
                "Multiplying polynomials",
                "Factoring",
                "Zero product property"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "quadratics",
          "name": "Quadratics",
          "artifacts": [
            {
              "title": "Quadratics Cheat Sheet",
              "path": "artifacts/quadratics-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/quadratics-cheat-sheet.svg",
              "description": "Colorful two-page printable study guide: Parabolas, vertex and intercepts, factoring, quadratic formula, and discriminant.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Reference", "Quadratics"],
              "added": "2026-10-19"
            },
            {
              "title": "Quadratics Four",
              "path": "artifacts/quadratics-connect-four/index.html",
              "thumb": "thumbs/quadratics-connect-four.jpg",
              "description": "Connect Four for two teams. Solve quadratics, find vertices and axes of symmetry, and use the discriminant. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Solving quadratic equations",
                "Vertex and axis of symmetry",
                "The discriminant",
                "Projectile motion"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Quadratics Flashcards",
              "path": "artifacts/quadratics-flashcards/index.html",
              "thumb": "thumbs/quadratics-flashcards.jpg",
              "description": "25 flashcards with worked solutions for parabolas (vertex, axis, intercepts, vertex form), solving by factoring, square roots, completing the square and the quadratic formula, the discriminant, and projectile and area problems. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Vertex and axis of symmetry",
                "Solving quadratics",
                "The discriminant",
                "Projectile and area problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Quadratics Picture Reveal",
              "path": "artifacts/quadratics-picture-reveal/index.html",
              "thumb": "thumbs/quadratics-picture-reveal.jpg",
              "description": "Find vertices, solve quadratic equations by factoring, square roots and the quadratic formula, and model a launched object to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Vertex and axis of symmetry",
                "Solving by factoring and square roots",
                "Quadratic formula and discriminant",
                "Projectile problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Quadratics Showdown",
              "path": "artifacts/quadratics-jeopardy/index.html",
              "thumb": "thumbs/quadratics-jeopardy.jpg",
              "description": "A game board for Quadratics. Solve by factoring, square roots, completing the square, and the quadratic formula, then work with parabolas, the discriminant, and projectile problems.",
              "type": "Game",
              "topics": [
                "Solving quadratic equations",
                "Vertex and axis of symmetry",
                "The discriminant",
                "Projectile motion"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Solving Quadratics Maze",
              "path": "artifacts/quadratics-maze/worksheet.pdf",
              "thumb": "thumbs/quadratics-maze.jpg",
              "description": "Printable 4-page worksheet: solve quadratic equations by factoring, square roots, and the quadratic formula to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Solving by factoring",
                "Solving with square roots",
                "The quadratic formula"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Quadratics Error Analysis",
              "path": "artifacts/quadratics-error-analysis/worksheet.pdf",
              "thumb": "thumbs/quadratics-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Quadratic formula",
                "Completing the square",
                "Vertex and graph",
                "Projectile problems"
              ],
              "added": "2026-10-18"
            }
          ]
        }
      ]
    },
    {
      "id": "geometry",
      "name": "Geometry",
      "color": "orange",
      "art": "triangle",
      "blurb": "Reasoning, shapes, measurement, and transformations.",
      "units": [
        {
          "id": "basics-reasoning",
          "name": "Basics & Reasoning",
          "artifacts": [
            {
              "title": "Geometry Basics Cheat Sheet",
              "path": "artifacts/geometry-basics-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-basics-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Points, lines, rays, segments, angles, midpoints, coordinate distance, and angle relationships.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Reasoning Four",
              "path": "artifacts/basics-reasoning-connect-four/index.html",
              "thumb": "thumbs/basics-reasoning-connect-four.jpg",
              "description": "Connect Four for two teams. Use segment addition, midpoints, angle relationships, and conditional statements to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Segment addition and midpoints",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Properties used in proofs"
              ],
              "added": "2026-10-18"
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
              "thumb": "thumbs/basics-reasoning-picture-reveal.jpg",
              "description": "Use segment and angle addition, midpoints, angle pairs and logical reasoning to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Segment addition and midpoints",
                "Angle addition and angle pairs",
                "Conditional statements",
                "Properties used in proofs"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Reasoning Showdown",
              "path": "artifacts/basics-reasoning-jeopardy/index.html",
              "thumb": "thumbs/basics-reasoning-jeopardy.jpg",
              "description": "A game board for Geometry basics and reasoning. Segments and angles with algebra, conditional statements, and the properties that justify steps in a proof.",
              "type": "Game",
              "topics": [
                "Segment addition and midpoints",
                "Angle addition and bisectors",
                "Converse, inverse, contrapositive",
                "Properties used in proofs"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Segments & Angles Maze",
              "path": "artifacts/basics-reasoning-maze/worksheet.pdf",
              "thumb": "thumbs/basics-reasoning-maze.jpg",
              "description": "Printable 4-page worksheet: use segment addition, midpoints, angle addition, complementary and supplementary angles, and angle bisectors to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Segment addition and midpoints",
                "Angle addition and angle bisectors",
                "Complementary and supplementary angles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Basics & Reasoning Error Analysis",
              "path": "artifacts/basics-reasoning-error-analysis/worksheet.pdf",
              "thumb": "thumbs/basics-reasoning-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Segment addition and midpoints",
                "Complementary and supplementary angles",
                "Conditional statements",
                "Logical reasoning"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "angles-parallel-lines",
          "name": "Angles & Parallel Lines",
          "artifacts": [
            {
              "title": "Angles & Parallel Lines Cheat Sheet",
              "path": "artifacts/geometry-angles-parallel-lines-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-angles-parallel-lines-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Transversals, corresponding and alternate angles, linear pairs, and parallel-line relationships.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Angles Four",
              "path": "artifacts/angles-parallel-lines-connect-four/index.html",
              "thumb": "thumbs/angles-parallel-lines-connect-four.jpg",
              "description": "Connect Four for two teams. Use angle pairs, parallel lines, and polygon angle sums to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Triangle and exterior angles",
                "Interior and exterior angles of polygons"
              ],
              "added": "2026-10-18"
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
              "thumb": "thumbs/angles-parallel-lines-picture-reveal.jpg",
              "description": "Find angle measures and solve for x with vertical angles, linear pairs and parallel lines cut by a transversal to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Angles made by a transversal",
                "Solving for x with parallel lines",
                "Proving lines parallel"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Angles Showdown",
              "path": "artifacts/angles-parallel-lines-jeopardy/index.html",
              "thumb": "thumbs/angles-parallel-lines-jeopardy.jpg",
              "description": "A game board for angle relationships. Angle pairs, parallel lines cut by a transversal, and angle sums in triangles and polygons.",
              "type": "Game",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Triangle and exterior angles",
                "Interior and exterior angles of polygons"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Angles & Parallel Lines Maze",
              "path": "artifacts/angles-parallel-lines-maze/worksheet.pdf",
              "thumb": "thumbs/angles-parallel-lines-maze.jpg",
              "description": "Printable 4-page worksheet: use vertical angles, linear pairs, and parallel-line angle pairs to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Vertical angles & linear pairs",
                "Parallel lines cut by a transversal",
                "Solving for x and angle measures"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Angles & Parallel Lines Error Analysis",
              "path": "artifacts/angles-parallel-lines-error-analysis/worksheet.pdf",
              "thumb": "thumbs/angles-parallel-lines-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Vertical angles and linear pairs",
                "Parallel lines and transversals",
                "Angle bisectors",
                "Angles around a point"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "triangles-congruence",
          "name": "Triangles & Congruence",
          "artifacts": [
            {
              "title": "Triangles & Congruence Cheat Sheet",
              "path": "artifacts/geometry-triangles-congruence-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-triangles-congruence-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Triangle angle facts, triangle classifications, and triangle congruence criteria.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Congruence Four",
              "path": "artifacts/triangles-congruence-connect-four/index.html",
              "thumb": "thumbs/triangles-congruence-connect-four.jpg",
              "description": "Connect Four for two teams. Triangle inequality, missing angles, congruence criteria and corresponding parts. A wrong answer lets the other team steal. Three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Triangle inequality and angle sums",
                "SSS, SAS, ASA, AAS, HL",
                "Corresponding parts and CPCTC",
                "Solving for x with congruent parts"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Triangles & Congruence Flashcards",
              "path": "artifacts/triangles-congruence-flashcards/index.html",
              "thumb": "thumbs/triangles-congruence-flashcards.jpg",
              "description": "25 flashcards with worked solutions on triangle angles, isosceles triangles, the triangle inequality, SSS, SAS, ASA, AAS, HL, CPCTC and proof planning. Mark cards you need to practice and review them again.",
              "type": "Practice",
              "topics": [
                "Triangle angle sum and exterior angles",
                "Isosceles triangles and the triangle inequality",
                "SSS, SAS, ASA, AAS, HL",
                "CPCTC and proof planning"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Triangles & Congruence Picture Reveal",
              "path": "artifacts/triangles-congruence-picture-reveal/index.html",
              "thumb": "thumbs/triangles-congruence-picture-reveal.jpg",
              "description": "Use the triangle angle sum, exterior angles, isosceles triangles, corresponding parts and the congruence shortcuts to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Triangle angle sum and exterior angles",
                "Isosceles triangles",
                "Corresponding parts (CPCTC)",
                "SAS, ASA and HL"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Triangles Showdown",
              "path": "artifacts/triangles-congruence-jeopardy/index.html",
              "thumb": "thumbs/triangles-congruence-jeopardy.jpg",
              "description": "A game board for Triangles and Congruence. Triangle facts, proving triangles congruent with SSS, SAS, ASA, AAS and HL, and using corresponding parts.",
              "type": "Game",
              "topics": [
                "Triangle inequality and angle sums",
                "SSS, SAS, ASA, AAS, HL",
                "Corresponding parts and CPCTC",
                "Solving for x with congruent parts"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Triangle Angles Maze",
              "path": "artifacts/triangles-congruence-maze/worksheet.pdf",
              "thumb": "thumbs/triangles-congruence-maze.jpg",
              "description": "Printable 4-page worksheet: use the triangle angle sum, the exterior angle theorem, and isosceles and equilateral triangle facts to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Triangle angle sum",
                "Exterior angle theorem",
                "Isosceles & equilateral triangles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Triangles & Congruence Error Analysis",
              "path": "artifacts/triangles-congruence-error-analysis/worksheet.pdf",
              "thumb": "thumbs/triangles-congruence-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Angle sum and exterior angles",
                "Triangle inequality",
                "Congruence shortcuts",
                "CPCTC proofs"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "similarity",
          "name": "Similarity",
          "artifacts": [
            {
              "title": "Similarity Cheat Sheet",
              "path": "artifacts/geometry-similarity-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-similarity-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Similar figures, proportional side lengths, scale factor, dilations, and similar triangles.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Similarity Four",
              "path": "artifacts/similarity-connect-four/index.html",
              "thumb": "thumbs/similarity-connect-four.jpg",
              "description": "Connect Four for two teams. Proportions, scale factor, area and perimeter ratios, similar triangles, side-splitter, shadows and scale drawings. A wrong answer lets the other team steal. Three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Ratios and proportions",
                "Scale factor and area ratio",
                "AA, SSS∼ and SAS∼",
                "Side-splitter and indirect measurement"
              ],
              "added": "2026-10-18"
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
              "thumb": "thumbs/similarity-picture-reveal.jpg",
              "description": "Use proportions, scale factor, AA, SAS and SSS similarity, the Triangle Proportionality Theorem and shadows to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Proportions and scale factor",
                "AA, SAS and SSS similarity",
                "Triangle Proportionality Theorem",
                "Area ratios and indirect measurement"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Similarity Showdown",
              "path": "artifacts/similarity-jeopardy/index.html",
              "thumb": "thumbs/similarity-jeopardy.jpg",
              "description": "A game board for Similarity. Ratios and proportions, similar figures with area and volume ratios, and similar triangles with AA, SSS, SAS, the side-splitter theorem and shadow problems.",
              "type": "Game",
              "topics": [
                "Ratios and proportions",
                "Scale factor and area ratio",
                "AA, SSS∼ and SAS∼",
                "Side-splitter and indirect measurement"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Similarity & Proportions Maze",
              "path": "artifacts/similarity-maze/worksheet.pdf",
              "thumb": "thumbs/similarity-maze.jpg",
              "description": "Printable 4-page worksheet: solve proportions, find scale factors and missing sides of similar figures, and use the side-splitter theorem and shadows to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Solving proportions",
                "Scale factor & similar triangles",
                "Side-splitter & shadow problems"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Similarity Error Analysis",
              "path": "artifacts/similarity-error-analysis/worksheet.pdf",
              "thumb": "thumbs/similarity-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Proportions",
                "Scale factors",
                "AA similarity",
                "Area and volume ratios"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "right-triangles-trigonometry",
          "name": "Right Triangles & Trigonometry",
          "artifacts": [
            {
              "title": "Right Triangles & Trigonometry Cheat Sheet",
              "path": "artifacts/geometry-right-triangles-trigonometry-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-right-triangles-trigonometry-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Pythagorean theorem, special right triangles, SOH-CAH-TOA, and inverse trigonometry.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Trig Four",
              "path": "artifacts/right-triangles-trigonometry-connect-four/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-connect-four.jpg",
              "description": "Connect Four for two teams. Use the Pythagorean Theorem, special right triangles and trig ratios to earn a disc. A wrong answer lets the other team steal. Three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Angles of elevation and depression"
              ],
              "added": "2026-10-18"
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
              "thumb": "thumbs/right-triangles-trigonometry-picture-reveal.jpg",
              "description": "Use the Pythagorean Theorem, special right triangles, SOH-CAH-TOA and angles of depression to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Angles of elevation and depression"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Right Triangles Showdown",
              "path": "artifacts/right-triangles-trigonometry-jeopardy/index.html",
              "thumb": "thumbs/right-triangles-trigonometry-jeopardy.jpg",
              "description": "A game board for Right Triangles and Trigonometry. Pythagorean Theorem, special right triangles, sine, cosine and tangent, and real-world applications. Reveal each worked solution to check it.",
              "type": "Game",
              "topics": [
                "Pythagorean Theorem and its converse",
                "Special right triangles",
                "Sine, cosine and tangent",
                "Angles of elevation and depression"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Right Triangles Maze",
              "path": "artifacts/right-triangles-trigonometry-maze/worksheet.pdf",
              "thumb": "thumbs/right-triangles-trigonometry-maze.jpg",
              "description": "Printable 4-page worksheet: use the Pythagorean theorem, special right triangles, and trig ratios to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Pythagorean theorem",
                "45°-45°-90° and 30°-60°-90° triangles",
                "Trig ratios (SOH CAH TOA)"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Right Triangles & Trigonometry Error Analysis",
              "path": "artifacts/right-triangles-trigonometry-error-analysis/worksheet.pdf",
              "thumb": "thumbs/right-triangles-trigonometry-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Pythagorean theorem",
                "Sine, cosine and tangent",
                "Special right triangles",
                "Angles of depression"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "circles",
          "name": "Circles",
          "artifacts": [
            {
              "title": "Circles Cheat Sheet",
              "path": "artifacts/geometry-circles-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-circles-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Circle parts, circumference, area, arcs, sectors, inscribed angles, chords and tangents.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Circles Four",
              "path": "artifacts/circles-connect-four/index.html",
              "thumb": "thumbs/circles-connect-four.jpg",
              "description": "Connect Four for two teams. Find lengths, areas, angle measures and circle equations to earn a disc. A wrong answer lets the other team steal. Three levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles"
              ],
              "added": "2026-10-18"
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
              "thumb": "thumbs/circles-picture-reveal.jpg",
              "description": "Find arc lengths, sector areas, inscribed angles, tangent and chord lengths, and equations of circles to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Arc length and sector area",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Circles Showdown",
              "path": "artifacts/circles-jeopardy/index.html",
              "thumb": "thumbs/circles-jeopardy.jpg",
              "description": "A game board for Circles. Circumference, area, arcs and sectors; central and inscribed angles, tangents and chords; and equations of circles. Reveal each worked solution to check it.",
              "type": "Game",
              "topics": [
                "Circumference, area, arcs and sectors",
                "Central and inscribed angles",
                "Tangents and chords",
                "Equations of circles"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Circles Maze",
              "path": "artifacts/circles-maze/worksheet.pdf",
              "thumb": "thumbs/circles-maze.jpg",
              "description": "Printable 4-page worksheet: find circumference, area, arc length, sector area, angle measures, and the center and radius of a circle to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Arc length and sector area",
                "Central and inscribed angles",
                "Equation of a circle"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Circles Error Analysis",
              "path": "artifacts/circles-error-analysis/worksheet.pdf",
              "thumb": "thumbs/circles-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Arc length and sectors",
                "Inscribed angles",
                "Tangents",
                "Intersecting chords"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "area-surface-area-volume",
          "name": "Area, Surface Area & Volume",
          "artifacts": [
            {
              "title": "Area, Surface Area & Volume Cheat Sheet",
              "path": "artifacts/geometry-area-surface-area-volume-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-area-surface-area-volume-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Area of plane figures, nets, surface area, and volume of solids.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Volume Four",
              "path": "artifacts/area-surface-area-volume-connect-four/index.html",
              "thumb": "thumbs/area-surface-area-volume-connect-four.jpg",
              "description": "Connect Four for two teams. Find areas, volumes, surface areas, and missing dimensions to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume of prisms, cylinders, cones, pyramids and spheres",
                "Surface area",
                "Scaling dimensions"
              ],
              "added": "2026-10-18"
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
              "thumb": "thumbs/area-surface-area-volume-picture-reveal.jpg",
              "description": "Find areas of polygons and composite figures, then surface area and volume of cylinders, cones, pyramids and spheres to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume and surface area of solids",
                "Scale factor effects"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Measurement Showdown",
              "path": "artifacts/area-surface-area-volume-jeopardy/index.html",
              "thumb": "thumbs/area-surface-area-volume-jeopardy.jpg",
              "description": "A game board for Area, Surface Area and Volume. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Area of polygons and composite figures",
                "Volume of prisms, cylinders, cones, pyramids and spheres",
                "Surface area",
                "Scaling dimensions"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Area & Volume Maze",
              "path": "artifacts/area-surface-area-volume-maze/worksheet.pdf",
              "thumb": "thumbs/area-surface-area-volume-maze.jpg",
              "description": "Printable 4-page worksheet: find areas of polygons and the volume and surface area of prisms, cylinders, cones, pyramids, and spheres to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Area of polygons",
                "Volume of solids",
                "Surface area of solids"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Area, Surface Area & Volume Error Analysis",
              "path": "artifacts/area-surface-area-volume-error-analysis/worksheet.pdf",
              "thumb": "thumbs/area-surface-area-volume-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Area of polygons",
                "Surface area",
                "Volumes of prisms, cylinders, cones and spheres",
                "Unit conversion"
              ],
              "added": "2026-10-18"
            }
          ]
        },
        {
          "id": "coordinate-geometry-transformations",
          "name": "Coordinate Geometry & Transformations",
          "artifacts": [
            {
              "title": "Coordinate Geometry & Transformations Cheat Sheet",
              "path": "artifacts/geometry-coordinate-transformations-cheat-sheet/worksheet.pdf",
              "thumb": "thumbs/geometry-coordinate-transformations-cheat-sheet.svg",
              "description": "Colorful two-page printable geometry reference guide: Coordinate formulas, translations, reflections, rotations, dilations and transformation sequences.",
              "type": "Printable",
              "topics": ["Cheat sheet", "Geometry", "Reference"],
              "added": "2026-10-19"
            },
            {
              "title": "Transformations Four",
              "path": "artifacts/coordinate-geometry-transformations-connect-four/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-connect-four.jpg",
              "description": "Connect Four for two teams. Use distance, midpoint, slope and transformations on the coordinate plane to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Reflections, rotations, translations and dilations",
                "Classifying figures from coordinates",
                "Parallel and perpendicular lines"
              ],
              "added": "2026-10-18"
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
              "thumb": "thumbs/coordinate-geometry-transformations-picture-reveal.jpg",
              "description": "Use distance, midpoint and slope, classify figures on the plane, and find images under translations, reflections, rotations, dilations and compositions to uncover a hidden picture. Instant feedback, worked solutions, and saved progress.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Parallel and perpendicular lines",
                "Classifying figures",
                "Transformations and compositions"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Coordinate Showdown",
              "path": "artifacts/coordinate-geometry-transformations-jeopardy/index.html",
              "thumb": "thumbs/coordinate-geometry-transformations-jeopardy.jpg",
              "description": "A game board for Coordinate Geometry and Transformations. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              "type": "Game",
              "topics": [
                "Distance, midpoint and slope",
                "Reflections, rotations, translations and dilations",
                "Classifying figures from coordinates",
                "Parallel and perpendicular lines"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Coordinate Geometry Maze",
              "path": "artifacts/coordinate-geometry-transformations-maze/worksheet.pdf",
              "thumb": "thumbs/coordinate-geometry-transformations-maze.jpg",
              "description": "Printable 4-page worksheet: find midpoints, distances, parallel and perpendicular slopes, and images of points under transformations to find the right door through a maze, and record each answer with work. Includes teacher answer keys.",
              "type": "Printable",
              "topics": [
                "Midpoint and distance",
                "Parallel and perpendicular slopes",
                "Transformations of points"
              ],
              "added": "2026-10-18"
            },
            {
              "title": "Coordinate Geometry & Transformations Error Analysis",
              "path": "artifacts/coordinate-geometry-transformations-error-analysis/worksheet.pdf",
              "thumb": "thumbs/coordinate-geometry-transformations-error-analysis.jpg",
              "description": "Printable 5-page worksheet: 10 worked solutions that each hide one mistake. Students find the error, explain it, and show the correct work.",
              "type": "Printable",
              "topics": [
                "Distance and midpoint",
                "Reflections and rotations",
                "Translations and dilations",
                "Equation of a circle"
              ],
              "added": "2026-10-18"
            }
          ]
        }
      ]
    }
  ]
};
