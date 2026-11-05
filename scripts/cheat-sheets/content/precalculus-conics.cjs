/* Precalculus Unit 3 cheat sheet (Conics). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-conics",
 "course": "Precalculus",
 "unitNo": 3,
 "unitName": "Conics",
 "focus": "parabolas and circles",
 "morefocus": "ellipses, hyperbolas and identifying conics",
 "front": [
  {
   "title": "Parabolas",
   "kind": "table",
   "plain": true,
   "head": [
    "Form",
    "Opens · focus"
   ],
   "rows": [
    [
     "⟨(x - h)^2 = 4p(y - k)⟩",
     "up/down · (h, k + p)"
    ],
    [
     "⟨(y - k)^2 = 4p(x - h)⟩",
     "right/left · (h + p, k)"
    ]
   ],
   "after": "Vertex (h, k). The directrix is p units on the other side of the vertex.",
   "color": "purple"
  },
  {
   "title": "Parabola Focus and Directrix",
   "kind": "example",
   "text": "Match 4p, then move p from the vertex.",
   "example": "⟨x^2 = 12y⟩",
   "steps": [
    [
     "4p = 12:",
     "p = 3"
    ]
   ],
   "answer": "focus (0, 3), directrix y = −3",
   "check": {
    "num": "12/4",
    "is": 3
   },
   "color": "blue"
  },
  {
   "title": "Circles",
   "kind": "table",
   "plain": true,
   "head": [
    "Form",
    "Gives"
   ],
   "rows": [
    [
     "⟨(x - h)^2 + (y - k)^2 = r^2⟩",
     "center (h, k), radius r"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Complete the Square",
   "kind": "example",
   "text": "Group x’s and y’s, add the square of half each coefficient to both sides.",
   "example": "⟨x^2 + y^2 - 6x + 4y - 12 = 0⟩",
   "steps": [
    [
     "Group:",
     "⟨(x^2 - 6x + 9) + (y^2 + 4y + 4) = 12 + 9 + 4⟩"
    ]
   ],
   "answer": "center (3, −2), r = 5",
   "check": {
    "num": "Math.sqrt(12+9+4)",
    "is": 5
   },
   "color": "orange"
  },
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "focus",
     "Fixed point used to define a conic.",
     "parabola: (0, p)"
    ],
    [
     "directrix",
     "Fixed line for a parabola.",
     "y = −p"
    ],
    [
     "vertex",
     "Turning point / end of the major axis.",
     "(h, k)"
    ],
    [
     "eccentricity",
     "⟨e = \\tfrac{c}{a}⟩: how stretched.",
     "circle e = 0"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Signs inside the parentheses are opposite the center.",
    "Add the same amounts to BOTH sides when completing the square.",
    "r is the square root of the right side."
   ],
   "bad": [
    [
     "(x + 3)² → center x = 3",
     "x = −3"
    ],
    [
     "Radius = 25",
     "⟨r = \\sqrt{25} = 5⟩"
    ],
    [
     "Forgetting to add to the right side",
     "balance both sides"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Ellipses",
   "kind": "table",
   "plain": true,
   "head": [
    "Form",
    "Key facts"
   ],
   "rows": [
    [
     "⟨\\tfrac{(x - h)^2}{a^2} + \\tfrac{(y - k)^2}{b^2} = 1⟩",
     "a > b: horizontal major axis"
    ],
    [
     "Foci",
     "⟨c^2 = a^2 - b^2⟩"
    ],
    [
     "Lengths",
     "major axis 2a, minor axis 2b"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Ellipse Foci",
   "kind": "example",
   "text": "Find c from a and b.",
   "example": "⟨\\tfrac{x^2}{25} + \\tfrac{y^2}{9} = 1⟩",
   "steps": [
    [
     "c² = 25 − 9 = 16:",
     "c = 4"
    ]
   ],
   "answer": "foci (±4, 0), vertices (±5, 0)",
   "check": {
    "num": "Math.sqrt(25-9)",
    "is": 4
   },
   "color": "blue"
  },
  {
   "title": "Hyperbolas",
   "kind": "table",
   "plain": true,
   "head": [
    "Form",
    "Key facts"
   ],
   "rows": [
    [
     "⟨\\tfrac{(x - h)^2}{a^2} - \\tfrac{(y - k)^2}{b^2} = 1⟩",
     "opens left/right"
    ],
    [
     "Foci",
     "⟨c^2 = a^2 + b^2⟩"
    ],
    [
     "Asymptotes",
     "⟨y - k = \\pm\\tfrac{b}{a}(x - h)⟩"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Hyperbola Facts",
   "kind": "example",
   "text": "Positive term tells the direction.",
   "example": "⟨\\tfrac{x^2}{9} - \\tfrac{y^2}{16} = 1⟩",
   "steps": [
    [
     "c² = 9 + 16 = 25:",
     "c = 5"
    ]
   ],
   "answer": "foci (±5, 0), asymptotes ⟨y = \\pm\\tfrac{4}{3}x⟩",
   "check": {
    "num": "Math.sqrt(9+16)",
    "is": 5
   },
   "color": "orange"
  },
  {
   "title": "Identify the Conic",
   "kind": "table",
   "plain": true,
   "head": [
    "⟨Ax^2 + Cy^2 + \\dots = 0⟩",
    "Conic"
   ],
   "rows": [
    [
     "A = C",
     "circle"
    ],
    [
     "A·C > 0, A ≠ C",
     "ellipse"
    ],
    [
     "A·C < 0",
     "hyperbola"
    ],
    [
     "A = 0 or C = 0",
     "parabola"
    ]
   ],
   "after": "⟨4x^2 - y^2 + 8x = 0⟩: A·C = −4 < 0 → hyperbola.",
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Ellipse: c² = a² − b². Hyperbola: c² = a² + b².",
    "Is a under the larger (ellipse) or positive (hyperbola) term?",
    "Did I complete the square on both variables?",
    "Did I sketch to check my answer?"
   ],
   "color": "teal"
  }
 ]
};
