/* Pre-Algebra (7th) Unit 11 cheat sheet (Right Triangles in Algebra). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-right-triangles-algebra",
 "course": "Pre-Algebra (7th)",
 "unitNo": 11,
 "unitName": "Right Triangles in Algebra",
 "focus": "square roots, the Pythagorean theorem, distance and midpoint",
 "morefocus": "proportions, special right triangles and trigonometric ratios",
 "front": [
  {
   "title": "Square Roots",
   "kind": "example",
   "text": "Find the perfect squares on either side to estimate.",
   "example": "Estimate ⟨\\sqrt{55}⟩.",
   "steps": [
    [
     "Between:",
     "⟨\\sqrt{49} = 7⟩ and ⟨\\sqrt{64} = 8⟩"
    ]
   ],
   "answer": "≈ 7.4",
   "check": {
    "num": "Math.round(Math.sqrt(55)*10)/10",
    "is": 7.4
   },
   "color": "purple"
  },
  {
   "title": "The Pythagorean Theorem",
   "kind": "example",
   "text": "⟨a^2 + b^2 = c^2⟩, c is the hypotenuse.",
   "example": "Legs 9 and 12. Hypotenuse?",
   "steps": [
    [
     "Square and add:",
     "81 + 144 = 225"
    ]
   ],
   "answer": "c = 15",
   "check": {
    "num": "Math.hypot(9,12)",
    "is": 15
   },
   "color": "blue"
  },
  {
   "title": "Finding a Leg",
   "kind": "example",
   "text": "⟨b^2 = c^2 - a^2⟩",
   "example": "Hypotenuse 13, leg 5",
   "steps": [
    [
     "Subtract:",
     "169 − 25 = 144"
    ]
   ],
   "answer": "b = 12",
   "check": {
    "num": "Math.sqrt(169-25)",
    "is": 12
   },
   "color": "green"
  },
  {
   "title": "Is It a Right Triangle?",
   "kind": "example",
   "text": "Check whether ⟨a^2 + b^2 = c^2⟩ with c the longest side.",
   "example": "Sides 8, 15, 17",
   "steps": [
    [
     "Check:",
     "64 + 225 = 289 ✓"
    ]
   ],
   "answer": "Yes",
   "check": {
    "true": "64+225===289"
   },
   "color": "orange"
  },
  {
   "title": "Distance and Midpoint",
   "kind": "example",
   "text": "⟨d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}⟩; midpoint averages the coordinates.",
   "example": "(1, 2) and (7, 10)",
   "steps": [
    [
     "Distance:",
     "⟨\\sqrt{36 + 64}⟩"
    ],
    [
     "Midpoint:",
     "⟨(\\tfrac{1 + 7}{2}, \\tfrac{2 + 10}{2})⟩"
    ]
   ],
   "answer": "d = 10, M = (4, 6)",
   "check": [
    {
     "num": "Math.hypot(6,8)",
     "is": 10
    },
    {
     "num": "(1+7)/2",
     "is": 4
    }
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "The hypotenuse is opposite the right angle and longest.",
    "Square first, add second, square root last.",
    "Every positive number has two square roots (±)."
   ],
   "bad": [
    [
     "a + b = c",
     "⟨a^2 + b^2 = c^2⟩"
    ],
    [
     "Adding when finding a leg",
     "subtract"
    ],
    [
     "Midpoint = difference ÷ 2",
     "sum ÷ 2"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Write a Proportion",
   "kind": "example",
   "text": "Similar right triangles have proportional sides (shadows!).",
   "example": "A 6 ft person casts a 4 ft shadow; a tree casts 18 ft.",
   "steps": [
    [
     "Proportion:",
     "⟨\\tfrac{6}{4} = \\tfrac{h}{18}⟩"
    ]
   ],
   "answer": "27 ft",
   "check": {
    "num": "6*18/4",
    "is": 27
   },
   "color": "purple"
  },
  {
   "title": "Special Right Triangles",
   "kind": "table",
   "plain": true,
   "head": [
    "Triangle",
    "Side ratio"
   ],
   "rows": [
    [
     "45°–45°–90°",
     "⟨1 : 1 : \\sqrt{2}⟩"
    ],
    [
     "30°–60°–90°",
     "⟨1 : \\sqrt{3} : 2⟩"
    ]
   ],
   "after": "Leg 5 in a 45-45-90: hypotenuse ⟨5\\sqrt{2} \\approx 7.07⟩.",
   "check": {
    "num": "5*Math.SQRT2",
    "is": 7.0710678118654755
   },
   "color": "blue"
  },
  {
   "title": "SOH-CAH-TOA",
   "kind": "table",
   "plain": true,
   "head": [
    "Ratio",
    "Definition"
   ],
   "rows": [
    [
     "sine",
     "⟨\\tfrac{\\text{opposite}}{\\text{hypotenuse}}⟩"
    ],
    [
     "cosine",
     "⟨\\tfrac{\\text{adjacent}}{\\text{hypotenuse}}⟩"
    ],
    [
     "tangent",
     "⟨\\tfrac{\\text{opposite}}{\\text{adjacent}}⟩"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Using a Trig Ratio",
   "kind": "example",
   "text": "Choose the ratio that links what you know to what you want.",
   "example": "Hypotenuse 20, angle 30°. Opposite side?",
   "steps": [
    [
     "sin 30° = x ÷ 20:",
     "x = 20 · 0.5"
    ]
   ],
   "answer": "10",
   "check": {
    "num": "20*Math.sin(Math.PI/6)",
    "is": 10
   },
   "color": "orange"
  },
  {
   "title": "Angles of Elevation and Depression",
   "kind": "example",
   "text": "Draw the triangle; the angle is measured from the horizontal.",
   "example": "A ramp rises at 10° over 30 ft horizontally. Height? (nearest tenth)",
   "steps": [
    [
     "tan 10° = h ÷ 30:",
     "h = 30 tan 10°"
    ]
   ],
   "answer": "≈ 5.3 ft",
   "check": {
    "num": "Math.round(30*Math.tan(10*Math.PI/180)*10)/10",
    "is": 5.3
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Is c the longest side?",
    "Did I pick opposite and adjacent from the given angle?",
    "Is my calculator in degree mode?",
    "Did I round only at the end?"
   ],
   "color": "teal"
  }
 ]
};
