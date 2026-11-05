/* Pre-Algebra (7th) Unit 8 cheat sheet (Linear Functions and Graphing). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-linear-functions-graphing",
 "course": "Pre-Algebra (7th)",
 "unitNo": 8,
 "unitName": "Linear Functions and Graphing",
 "focus": "relations, functions, two-variable equations, slope and intercepts",
 "morefocus": "writing rules, scatter plots, systems and graphing inequalities",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "relation",
     "A set of ordered pairs.",
     "{(1, 2), (3, 5)}"
    ],
    [
     "function",
     "Each input has exactly one output.",
     "y = 2x + 1"
    ],
    [
     "slope",
     "Rate of change: rise ÷ run.",
     "⟨m = \\tfrac{y_2 - y_1}{x_2 - x_1}⟩"
    ],
    [
     "y-intercept",
     "Where the line crosses the y-axis.",
     "b in y = mx + b"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Is It a Function?",
   "kind": "example",
   "text": "No input (x) may repeat with a different output.",
   "example": "{(2, 5), (3, 7), (2, 9)}",
   "steps": [
    [
     "Check x-values:",
     "2 has outputs 5 and 9"
    ]
   ],
   "answer": "Not a function",
   "check": {
    "true": "5 !== 9"
   },
   "color": "blue"
  },
  {
   "title": "Finding Slope",
   "kind": "example",
   "text": "Divide the change in y by the change in x.",
   "example": "Slope through (1, 3) and (4, 12)",
   "steps": [
    [
     "Rise ÷ run:",
     "⟨\\tfrac{12 - 3}{4 - 1} = \\tfrac{9}{3}⟩"
    ]
   ],
   "answer": "m = 3",
   "check": {
    "num": "(12-3)/(4-1)",
    "is": 3
   },
   "color": "green"
  },
  {
   "title": "Solutions of Two-Variable Equations",
   "kind": "example",
   "text": "Substitute the x-value and solve for y.",
   "example": "Is (3, 7) a solution of y = 2x + 1?",
   "steps": [
    [
     "Substitute:",
     "2(3) + 1 = 7 ✓"
    ]
   ],
   "answer": "Yes",
   "check": {
    "true": "2*3+1 === 7"
   },
   "color": "orange"
  },
  {
   "title": "Writing a Rule",
   "kind": "example",
   "text": "Find the slope from the table, then the starting value.",
   "example": "x: 0, 1, 2 → y: 4, 7, 10",
   "steps": [
    [
     "Slope:",
     "y goes up 3 each time"
    ],
    [
     "y-intercept:",
     "4"
    ]
   ],
   "answer": "y = 3x + 4",
   "check": [
    {
     "num": "3*2+4",
     "is": 10
    }
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Slope = rise over run (y over x).",
    "Positive slope rises left to right.",
    "A vertical line is not a function."
   ],
   "bad": [
    [
     "Slope = run ÷ rise",
     "rise ÷ run"
    ],
    [
     "Subtracting coordinates in different orders",
     "same order top and bottom"
    ],
    [
     "Confusing m and b",
     "b is where x = 0"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Scatter Plots",
   "kind": "table",
   "plain": true,
   "head": [
    "Pattern",
    "Correlation"
   ],
   "rows": [
    [
     "Points rise left to right",
     "positive"
    ],
    [
     "Points fall left to right",
     "negative"
    ],
    [
     "No pattern",
     "no correlation"
    ]
   ],
   "after": "A trend line lets you make predictions.",
   "color": "purple"
  },
  {
   "title": "Systems by Graphing",
   "kind": "example",
   "text": "Graph both lines; the solution is where they cross.",
   "example": "y = x + 1 and y = −x + 5",
   "steps": [
    [
     "Cross at:",
     "x + 1 = −x + 5 → x = 2"
    ]
   ],
   "answer": "(2, 3)",
   "check": [
    {
     "num": "2+1",
     "is": 3
    },
    {
     "num": "-2+5",
     "is": 3
    }
   ],
   "color": "blue"
  },
  {
   "title": "Systems by Substitution",
   "kind": "example",
   "text": "Replace one variable with its expression from the other equation.",
   "example": "y = 2x and x + y = 12",
   "steps": [
    [
     "Substitute:",
     "x + 2x = 12 → x = 4"
    ]
   ],
   "answer": "(4, 8)",
   "check": {
    "true": "4+8===12 && 8===2*4"
   },
   "color": "green"
  },
  {
   "title": "Graphing Linear Inequalities",
   "kind": "words",
   "rows": [
    [
     "y > 2x + 1",
     "dashed line, shade above"
    ],
    [
     "y ≤ −x + 3",
     "solid line, shade below"
    ],
    [
     "Test point (0, 0)",
     "shade its side if true"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Slope at a Glance",
   "kind": "table",
   "plain": true,
   "head": [
    "Line",
    "Slope"
   ],
   "rows": [
    [
     "Horizontal (y = 4)",
     "0"
    ],
    [
     "Vertical (x = −2)",
     "undefined"
    ],
    [
     "Parallel lines",
     "equal slopes"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I check my solution in BOTH equations?",
    "Is my line solid (≤, ≥) or dashed (<, >)?",
    "Did I use a test point to shade?",
    "Does my slope sign match the graph’s direction?"
   ],
   "color": "teal"
  }
 ]
};
