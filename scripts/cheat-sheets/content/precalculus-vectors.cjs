/* Precalculus Unit 7 cheat sheet (Vectors). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-vectors",
 "course": "Precalculus",
 "unitNo": 7,
 "unitName": "Vectors",
 "focus": "vector components, magnitude, direction and operations",
 "morefocus": "dot product, angles between vectors, projections and applications",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "vector",
     "Has magnitude and direction.",
     "⟨3, 4⟩"
    ],
    [
     "magnitude",
     "Length of the vector.",
     "⟨\\|\\langle 3, 4\\rangle\\| = 5⟩"
    ],
    [
     "unit vector",
     "Magnitude 1.",
     "⟨\\langle \\tfrac{3}{5}, \\tfrac{4}{5}\\rangle⟩"
    ],
    [
     "resultant",
     "The sum of vectors.",
     "u + v"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Component Form",
   "kind": "example",
   "text": "Terminal point minus initial point.",
   "example": "From P(1, −2) to Q(6, 10)",
   "steps": [
    [
     "Subtract:",
     "⟨6 − 1, 10 − (−2)⟩"
    ]
   ],
   "answer": "⟨5, 12⟩, magnitude 13",
   "check": {
    "num": "Math.hypot(5,12)",
    "is": 13
   },
   "color": "blue"
  },
  {
   "title": "Magnitude and Direction",
   "kind": "example",
   "text": "⟨\\|v\\| = \\sqrt{a^2 + b^2}⟩, ⟨\\tan\\theta = \\tfrac{b}{a}⟩ (check the quadrant).",
   "example": "v = ⟨−3, 3⟩",
   "steps": [
    [
     "Magnitude:",
     "⟨\\sqrt{18} = 3\\sqrt{2}⟩"
    ],
    [
     "Direction:",
     "quadrant II"
    ]
   ],
   "answer": "⟨3\\sqrt{2}⟩, 135°",
   "check": [
    {
     "num": "Math.hypot(-3,3)",
     "is": 4.242640687119286
    },
    {
     "num": "Math.atan2(3,-3)*180/Math.PI",
     "is": 135
    }
   ],
   "color": "green"
  },
  {
   "title": "Vector Operations",
   "kind": "example",
   "text": "Add or scale component by component.",
   "example": "u = ⟨2, −1⟩, v = ⟨−4, 3⟩. Find 3u − v.",
   "steps": [
    [
     "3u:",
     "⟨6, −3⟩"
    ],
    [
     "Subtract v:",
     "⟨6 + 4, −3 − 3⟩"
    ]
   ],
   "answer": "⟨10, −6⟩",
   "check": [
    {
     "num": "3*2-(-4)",
     "is": 10
    },
    {
     "num": "3*(-1)-3",
     "is": -6
    }
   ],
   "color": "orange"
  },
  {
   "title": "Vector from Magnitude and Angle",
   "kind": "example",
   "text": "⟨v = \\langle \\|v\\|\\cos\\theta, \\|v\\|\\sin\\theta \\rangle⟩",
   "example": "|v| = 10 at 30°",
   "steps": [
    [
     "Components:",
     "⟨10 cos 30°, 10 sin 30°⟩"
    ]
   ],
   "answer": "⟨\\langle 5\\sqrt{3}, 5 \\rangle⟩",
   "check": {
    "num": "10*Math.sin(Math.PI/6)",
    "is": 5
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Component form = terminal − initial.",
    "Use atan2 thinking: check the quadrant.",
    "Magnitude is never negative."
   ],
   "bad": [
    [
     "Initial − terminal",
     "terminal − initial"
    ],
    [
     "tan⁻¹(3 ÷ −3) = −45°",
     "135° (quadrant II)"
    ],
    [
     "|u + v| = |u| + |v|",
     "only if parallel"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Dot Product",
   "kind": "example",
   "text": "⟨u \\cdot v = u_1v_1 + u_2v_2⟩ (a number).",
   "example": "u = ⟨3, 4⟩, v = ⟨2, −1⟩",
   "steps": [
    [
     "Multiply and add:",
     "6 − 4"
    ]
   ],
   "answer": "2",
   "check": {
    "num": "3*2+4*(-1)",
    "is": 2
   },
   "color": "purple"
  },
  {
   "title": "Angle Between Vectors",
   "kind": "example",
   "text": "⟨\\cos\\theta = \\tfrac{u \\cdot v}{\\|u\\|\\|v\\|}⟩",
   "example": "u = ⟨1, 0⟩, v = ⟨1, 1⟩",
   "steps": [
    [
     "cos θ:",
     "⟨\\tfrac{1}{1 \\cdot \\sqrt{2}}⟩"
    ]
   ],
   "answer": "45°",
   "check": {
    "num": "Math.acos(1/Math.SQRT2)*180/Math.PI",
    "is": 45
   },
   "color": "blue"
  },
  {
   "title": "Orthogonal and Parallel",
   "kind": "table",
   "plain": true,
   "head": [
    "Test",
    "Meaning"
   ],
   "rows": [
    [
     "u · v = 0",
     "orthogonal (perpendicular)"
    ],
    [
     "u = kv",
     "parallel"
    ],
    [
     "u · v > 0",
     "angle < 90°"
    ]
   ],
   "after": "⟨2, 3⟩ · ⟨−3, 2⟩ = 0, so they are orthogonal.",
   "check": {
    "num": "2*(-3)+3*2",
    "is": 0
   },
   "color": "green"
  },
  {
   "title": "Projection",
   "kind": "example",
   "text": "⟨\\text{proj}_v u = \\tfrac{u \\cdot v}{\\|v\\|^2}v⟩",
   "example": "u = ⟨4, 2⟩ onto v = ⟨3, 0⟩",
   "steps": [
    [
     "Scalar:",
     "⟨\\tfrac{12}{9} = \\tfrac{4}{3}⟩"
    ]
   ],
   "answer": "⟨4, 0⟩",
   "check": {
    "num": "12/9*3",
    "is": 4
   },
   "color": "orange"
  },
  {
   "title": "Work",
   "kind": "example",
   "text": "W = F · d = ⟨\\|F\\|\\|d\\|\\cos\\theta⟩",
   "example": "A 50 N force at 60° moves a box 10 m.",
   "steps": [
    [
     "Compute:",
     "50 · 10 · cos 60°"
    ]
   ],
   "answer": "250 J",
   "check": {
    "num": "50*10*Math.cos(Math.PI/3)",
    "is": 250
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "The dot product is a NUMBER, not a vector.",
    "Did I divide by |v|² for the projection?",
    "Are my angles in the right quadrant?",
    "Did I sketch the vectors?"
   ],
   "color": "teal"
  }
 ]
};
