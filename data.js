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
  title: "Mr. K's Classroom",
  tagline: "Interactive math games and practice for Algebra and Geometry. Pick a course, choose a unit, and open an activity on any device.",
  footer: "Activities open in a new tab and run in any modern browser. Saved activities are kept in this browser only.",
  newDays: 30,
  courses: [
    {
      id: "algebra",
      name: "Algebra",
      color: "blue",
      art: "curve",
      blurb: "Equations, inequalities, functions, and polynomials.",
      units: [
        { id: "expressions-equations", name: "Expressions & Equations", artifacts: [
          {
            title: "Expressions & Equations Flashcards",
            path: "artifacts/expressions-equations-flashcards/index.html",
            thumb: "thumbs/expressions-equations-flashcards.svg",
            description: "25 interactive flashcards with worked solutions for evaluating expressions, combining like terms, distributing, equations and applications.",
            type: "Practice",
            topics: ["Evaluating expressions", "Simplifying", "Solving equations"],
            added: "2026-10-17"
          }
        ] },
        {
          id: "inequalities",
          name: "Inequalities",
          artifacts: [
            {
              title: "Inequalities Flashcards",
              path: "artifacts/inequalities-flashcards/index.html",
              thumb: "thumbs/inequalities-flashcards.svg",
              description: "Practice 25 essential inequality problems with student-style worked solutions and number-line graphs, including compound inequalities. Review missed cards and track progress.",
              type: "Practice",
              topics: ["Solving inequalities", "Number line graphs", "Compound inequalities"],
              added: "2026-10-17"
            },
            {
              title: "Inequality Four",
              path: "artifacts/inequality-four/index.html",
              thumb: "thumbs/inequality-four.jpg",
              description: "Connect Four for two teams. Solve, graph, or translate a compound inequality to earn a disc. A wrong answer lets the other team steal. Three difficulty levels and an optional timer.",
              type: "Game",
              topics: ["Compound inequalities", "Number line graphs"],
              added: "2026-10-16"
            },
            {
              title: "Inequality Showdown",
              path: "artifacts/inequality-showdown/index.html",
              thumb: "thumbs/inequality-showdown.jpg",
              description: "A game board for Algebra 1 review. Pick a category and a point value to open a problem, then reveal the worked solution to check it.",
              type: "Game",
              topics: ["Compound inequalities", "Absolute value inequalities"],
              added: "2026-10-16"
            }
          ]
        },
        {
          id: "linear-equations-slope",
          name: "Linear Equations & Slope",
          artifacts: [
            {
              title: "Slope Links Mini Golf",
              path: "artifacts/slope-links-mini-golf/index.html",
              thumb: "thumbs/slope-links-mini-golf.jpg",
              description: "Enter a slope, pick a direction and a club, and hit. The ball follows a line through its starting point, and you only see where it went after the shot. Six holes with walls, sand, and water.",
              type: "Game",
              topics: ["Slope", "Rise over run", "Coordinate plane"],
              added: "2026-10-16"
            }
          ]
        },
        {
          id: "graphing-inequalities",
          name: "Graphing Inequalities on the Coordinate Plane",
          artifacts: [
            {
              title: "Zombie Fence",
              path: "artifacts/zombie-fence/index.html",
              thumb: "thumbs/zombie-fence.jpg",
              description: "Build fences from inequalities in slope-intercept form. Keep every survivor in the safe zone and every zombie out, using solid and dashed lines and, on later nights, two inequalities at once.",
              type: "Game",
              topics: ["Graphing inequalities", "Slope-intercept form", "Systems of inequalities"],
              added: "2026-10-16"
            }
          ]
        },
        { id: "systems-of-equations", name: "Systems of Equations", artifacts: [] },
        { id: "exponents-exponential-functions", name: "Exponents & Exponential Functions", artifacts: [] },
        { id: "polynomials-factoring", name: "Polynomials & Factoring", artifacts: [] },
        { id: "quadratics", name: "Quadratics", artifacts: [] }
      ]
    },
    {
      id: "geometry",
      name: "Geometry",
      color: "orange",
      art: "triangle",
      blurb: "Reasoning, shapes, measurement, and transformations.",
      units: [
        { id: "basics-reasoning", name: "Basics & Reasoning", artifacts: [] },
        { id: "angles-parallel-lines", name: "Angles & Parallel Lines", artifacts: [] },
        { id: "triangles-congruence", name: "Triangles & Congruence", artifacts: [] },
        { id: "similarity", name: "Similarity", artifacts: [] },
        { id: "right-triangles-trigonometry", name: "Right Triangles & Trigonometry", artifacts: [] },
        { id: "circles", name: "Circles", artifacts: [] },
        { id: "area-surface-area-volume", name: "Area, Surface Area & Volume", artifacts: [] },
        { id: "coordinate-geometry-transformations", name: "Coordinate Geometry & Transformations", artifacts: [] }
      ]
    }
  ]
};
