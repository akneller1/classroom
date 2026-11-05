/* Calculus Unit 7 cheat sheet (Applications of Integrals). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-applications-integrals",
 "course": "Calculus",
 "unitNo": 7,
 "unitName": "Applications of Integrals",
 "focus": "area between curves",
 "morefocus": "volumes by discs, washers and cross sections",
 "front": [
  {
   "title": "Area Between Curves",
   "kind": "example",
   "text": "⟨\\int_a^b (\\text{top} - \\text{bottom})\\,dx⟩",
   "example": "⟨y = x⟩ and ⟨y = x^2⟩",
   "steps": [
    [
     "Intersect:",
     "x = 0, 1"
    ],
    [
     "Integrate:",
     "⟨\\int_0^1 (x - x^2)\\,dx⟩"
    ]
   ],
   "answer": "⟨\\tfrac{1}{6}⟩",
   "check": {
    "num": "1/2-1/3",
    "is": 0.16666666666666666
   },
   "color": "purple"
  },
  {
   "title": "Integrating in y",
   "kind": "example",
   "text": "⟨\\int_c^d (\\text{right} - \\text{left})\\,dy⟩",
   "example": "⟨x = y^2⟩ and x = 4",
   "steps": [
    [
     "Limits:",
     "y = −2 to 2"
    ],
    [
     "Integrate:",
     "⟨\\int_{-2}^{2}(4 - y^2)\\,dy⟩"
    ]
   ],
   "answer": "⟨\\tfrac{32}{3}⟩",
   "check": {
    "num": "(8-8/3)-(-8+8/3)",
    "is": 10.666666666666666
   },
   "color": "blue"
  },
  {
   "title": "Setting Up Area",
   "kind": "list",
   "items": [
    "Sketch the region.",
    "Find the intersection points (limits).",
    "Decide dx (top − bottom) or dy (right − left).",
    "If the curves cross, split the integral."
   ],
   "color": "green"
  },
  {
   "title": "Curves That Cross",
   "kind": "example",
   "text": "Split at each crossing so every piece is positive.",
   "example": "⟨\\int_0^{2\\pi} |\\sin x|\\,dx⟩",
   "steps": [
    [
     "Split:",
     "2 + 2"
    ]
   ],
   "answer": "4",
   "check": {
    "num": "2+2",
    "is": 4
   },
   "color": "orange"
  },
  {
   "title": "Choosing dx or dy",
   "kind": "words",
   "rows": [
    [
     "Top and bottom curves are functions of x",
     "dx"
    ],
    [
     "Left and right curves are functions of y",
     "dy"
    ],
    [
     "Would need two integrals in x",
     "try dy"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Area is always positive.",
    "Use intersection points as limits.",
    "Top minus bottom, right minus left."
   ],
   "bad": [
    [
     "Bottom − top",
     "top − bottom"
    ],
    [
     "Using x-limits with dy",
     "y-limits"
    ],
    [
     "Not splitting where curves cross",
     "split the integral"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Volume Formulas",
   "kind": "table",
   "plain": true,
   "head": [
    "Method",
    "Volume"
   ],
   "rows": [
    [
     "Disc",
     "⟨\\pi\\int_a^b R(x)^2\\,dx⟩"
    ],
    [
     "Washer",
     "⟨\\pi\\int_a^b (R^2 - r^2)\\,dx⟩"
    ],
    [
     "Cross sections",
     "⟨\\int_a^b A(x)\\,dx⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Disc Method",
   "kind": "example",
   "text": "Radius = distance from the axis to the curve.",
   "example": "Rotate ⟨y = \\sqrt{x}⟩, 0 ≤ x ≤ 4, about the x-axis.",
   "steps": [
    [
     "Integrate:",
     "⟨\\pi\\int_0^4 x\\,dx⟩"
    ]
   ],
   "answer": "⟨8\\pi⟩",
   "check": {
    "num": "Math.PI*8",
    "is": 25.132741228718345
   },
   "color": "blue"
  },
  {
   "title": "Washer Method",
   "kind": "example",
   "text": "Outer radius squared minus inner radius squared.",
   "example": "Region between y = x and ⟨y = x^2⟩ about the x-axis.",
   "steps": [
    [
     "Integrate:",
     "⟨\\pi\\int_0^1 (x^2 - x^4)\\,dx⟩"
    ]
   ],
   "answer": "⟨\\tfrac{2\\pi}{15}⟩",
   "check": {
    "num": "Math.PI*(1/3-1/5)",
    "is": 0.41887902047863906
   },
   "color": "green"
  },
  {
   "title": "Rotating About Another Line",
   "kind": "example",
   "text": "Radius = |curve − axis|.",
   "example": "Rotate ⟨y = x^2⟩, 0 ≤ x ≤ 1, about y = −1.",
   "steps": [
    [
     "Radii:",
     "R = x² + 1 (outer), r = 1 (inner)"
    ]
   ],
   "answer": "⟨\\pi\\int_0^1 ((x^2 + 1)^2 - 1)\\,dx = \\tfrac{13\\pi}{15}⟩",
   "check": {
    "num": "Math.PI*(1/5+2/3)",
    "is": 2.7227136331111543
   },
   "color": "orange"
  },
  {
   "title": "Cross-Section Areas",
   "kind": "table",
   "plain": true,
   "head": [
    "Shape (side s)",
    "Area"
   ],
   "rows": [
    [
     "Square",
     "⟨s^2⟩"
    ],
    [
     "Equilateral triangle",
     "⟨\\tfrac{\\sqrt{3}}{4}s^2⟩"
    ],
    [
     "Semicircle (diameter s)",
     "⟨\\tfrac{\\pi}{8}s^2⟩"
    ]
   ],
   "after": "Squares on y = √x, 0 ≤ x ≤ 4: V = ∫ x dx = 8.",
   "check": {
    "num": "16/2",
    "is": 8
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I square each radius separately (R² − r²)?",
    "Is my radius measured from the axis of rotation?",
    "Did I include π for discs and washers?",
    "Does my sketch match my setup?"
   ],
   "color": "teal"
  }
 ]
};
