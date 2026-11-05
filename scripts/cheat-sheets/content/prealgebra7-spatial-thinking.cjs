/* Pre-Algebra (7th) Unit 9 cheat sheet (Spatial Thinking). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-spatial-thinking",
 "course": "Pre-Algebra (7th)",
 "unitNo": 9,
 "unitName": "Spatial Thinking",
 "focus": "points, lines, planes, angle pairs, parallel lines and polygons",
 "morefocus": "congruence, circles, constructions, translations, symmetry and rotations",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "point, line, plane",
     "Location; straight path with no ends; flat surface.",
     "A, line AB, plane P"
    ],
    [
     "segment",
     "Part of a line with two endpoints.",
     "segment CD"
    ],
    [
     "ray",
     "One endpoint, extends one way.",
     "ray EF"
    ],
    [
     "congruent",
     "Same size and shape.",
     "△ABC ≅ △DEF"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Angle Pairs",
   "kind": "table",
   "plain": true,
   "head": [
    "Pair",
    "Relationship"
   ],
   "rows": [
    [
     "Complementary",
     "sum to 90°"
    ],
    [
     "Supplementary",
     "sum to 180°"
    ],
    [
     "Vertical",
     "equal"
    ],
    [
     "Adjacent",
     "share a side and vertex"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Finding Missing Angles",
   "kind": "example",
   "text": "Use the angle pair relationship to write an equation.",
   "example": "Two supplementary angles: one is 3 times the other.",
   "steps": [
    [
     "Equation:",
     "x + 3x = 180"
    ]
   ],
   "answer": "45° and 135°",
   "check": {
    "num": "180/4",
    "is": 45
   },
   "color": "green"
  },
  {
   "title": "Parallel Lines and a Transversal",
   "kind": "table",
   "plain": true,
   "head": [
    "Angle pair",
    "Relationship"
   ],
   "rows": [
    [
     "Corresponding",
     "equal"
    ],
    [
     "Alternate interior",
     "equal"
    ],
    [
     "Same-side interior",
     "sum to 180°"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Polygon Angle Sum",
   "kind": "example",
   "text": "Sum = (n − 2) · 180°.",
   "example": "Each angle of a regular hexagon",
   "steps": [
    [
     "Sum:",
     "(6 − 2)180 = 720°"
    ],
    [
     "Divide by 6:",
     "120°"
    ]
   ],
   "answer": "120°",
   "check": {
    "num": "(6-2)*180/6",
    "is": 120
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Complementary → corner (90°); supplementary → straight (180°).",
    "Mark congruent sides and angles with matching ticks.",
    "A regular polygon has equal sides AND angles."
   ],
   "bad": [
    [
     "Vertical angles add to 180°",
     "they are equal"
    ],
    [
     "Hexagon sum = 6 · 180°",
     "(6 − 2) · 180°"
    ],
    [
     "Calling a ray a line",
     "a ray has one endpoint"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Circles",
   "kind": "table",
   "plain": true,
   "head": [
    "Measure",
    "Formula"
   ],
   "rows": [
    [
     "Diameter",
     "d = 2r"
    ],
    [
     "Circumference",
     "⟨C = \\pi d = 2\\pi r⟩"
    ],
    [
     "Central angles",
     "sum to 360°"
    ]
   ],
   "after": "A circle with r = 5 cm has C ≈ 31.4 cm.",
   "check": {
    "num": "2*Math.PI*5",
    "is": 31.41592653589793
   },
   "color": "purple"
  },
  {
   "title": "Constructions (compass and straightedge)",
   "kind": "words",
   "rows": [
    [
     "Copy a segment",
     "measure with the compass, mark the same length"
    ],
    [
     "Bisect a segment",
     "equal arcs from both ends, connect the crossings"
    ],
    [
     "Bisect an angle",
     "arc across both sides, equal arcs, draw the ray"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Translations",
   "kind": "example",
   "text": "Slide every point the same distance: (x, y) → (x + a, y + b).",
   "example": "Translate (−2, 5) by 4 right, 3 down.",
   "steps": [
    [
     "Rule:",
     "(x + 4, y − 3)"
    ]
   ],
   "answer": "(2, 2)",
   "check": [
    {
     "num": "-2+4",
     "is": 2
    },
    {
     "num": "5-3",
     "is": 2
    }
   ],
   "color": "green"
  },
  {
   "title": "Rotations about the Origin",
   "kind": "example",
   "text": "Use the rules for 90°, 180° and 270° counterclockwise.",
   "example": "Rotate (3, 1) 90° counterclockwise.",
   "steps": [
    [
     "Rule:",
     "(x, y) → (−y, x)"
    ]
   ],
   "answer": "(−1, 3)",
   "check": {
    "num": "-1",
    "is": -1
   },
   "color": "orange"
  },
  {
   "title": "Symmetry",
   "kind": "table",
   "plain": true,
   "head": [
    "Figure",
    "Symmetry"
   ],
   "rows": [
    [
     "Square",
     "4 lines; rotational 90°"
    ],
    [
     "Equilateral triangle",
     "3 lines; rotational 120°"
    ],
    [
     "Rectangle",
     "2 lines; rotational 180°"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I label the angle pair correctly?",
    "Did I move every vertex by the same rule?",
    "Did I rotate counterclockwise unless told otherwise?",
    "Does my answer make sense in the picture?"
   ],
   "color": "teal"
  }
 ]
};
