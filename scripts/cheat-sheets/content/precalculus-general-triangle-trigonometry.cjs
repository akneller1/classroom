/* Precalculus Unit 5 cheat sheet (Trigonometry of General Triangles). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-general-triangle-trigonometry",
 "course": "Precalculus",
 "unitNo": 5,
 "unitName": "Trigonometry of General Triangles",
 "focus": "right-triangle trig and the Law of Sines",
 "morefocus": "the Law of Cosines, the ambiguous case and triangle area",
 "front": [
  {
   "title": "Right-Triangle Ratios",
   "kind": "table",
   "plain": true,
   "head": [
    "Ratio",
    "Definition"
   ],
   "rows": [
    [
     "sin θ",
     "⟨\\tfrac{\\text{opp}}{\\text{hyp}}⟩"
    ],
    [
     "cos θ",
     "⟨\\tfrac{\\text{adj}}{\\text{hyp}}⟩"
    ],
    [
     "tan θ",
     "⟨\\tfrac{\\text{opp}}{\\text{adj}}⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Solving a Right Triangle",
   "kind": "example",
   "text": "Pick the ratio connecting the known side to the unknown.",
   "example": "Angle 35°, hypotenuse 12. Opposite side?",
   "steps": [
    [
     "sin 35° = x ÷ 12:",
     "x = 12 sin 35°"
    ]
   ],
   "answer": "≈ 6.88",
   "check": {
    "num": "Math.round(12*Math.sin(35*Math.PI/180)*100)/100",
    "is": 6.88
   },
   "color": "blue"
  },
  {
   "title": "The Law of Sines",
   "kind": "table",
   "plain": true,
   "head": [
    "Use when you know",
    "Formula"
   ],
   "rows": [
    [
     "AAS or ASA",
     "⟨\\tfrac{a}{\\sin A} = \\tfrac{b}{\\sin B} = \\tfrac{c}{\\sin C}⟩"
    ],
    [
     "SSA (ambiguous)",
     "check for 0, 1 or 2 triangles"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Law of Sines (AAS)",
   "kind": "example",
   "text": "Find the third angle, then use the ratio.",
   "example": "A = 40°, B = 60°, a = 10. Find b.",
   "steps": [
    [
     "Ratio:",
     "⟨b = \\tfrac{10\\sin 60°}{\\sin 40°}⟩"
    ]
   ],
   "answer": "≈ 13.47",
   "check": {
    "num": "Math.round(10*Math.sin(Math.PI/3)/Math.sin(40*Math.PI/180)*100)/100",
    "is": 13.47
   },
   "color": "orange"
  },
  {
   "title": "Angles of Elevation and Depression",
   "kind": "words",
   "rows": [
    [
     "Elevation",
     "measured UP from the horizontal"
    ],
    [
     "Depression",
     "measured DOWN from the horizontal"
    ],
    [
     "They are equal",
     "alternate interior angles"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Side a is opposite angle A.",
    "Angles in a triangle sum to 180°.",
    "Keep full precision until the end."
   ],
   "bad": [
    [
     "Using sine law with SAS",
     "use the Law of Cosines"
    ],
    [
     "Calculator in radian mode",
     "degree mode"
    ],
    [
     "Rounding early",
     "round at the end"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "The Law of Cosines",
   "kind": "table",
   "plain": true,
   "head": [
    "Use when you know",
    "Formula"
   ],
   "rows": [
    [
     "SAS",
     "⟨c^2 = a^2 + b^2 - 2ab\\cos C⟩"
    ],
    [
     "SSS",
     "⟨\\cos C = \\tfrac{a^2 + b^2 - c^2}{2ab}⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Law of Cosines (SAS)",
   "kind": "example",
   "text": "Use the included angle.",
   "example": "a = 7, b = 9, C = 50°. Find c.",
   "steps": [
    [
     "Compute:",
     "⟨49 + 81 - 126\\cos 50°⟩"
    ]
   ],
   "answer": "≈ 7.00",
   "check": {
    "num": "Math.round(Math.sqrt(49+81-126*Math.cos(50*Math.PI/180))*100)/100",
    "is": 7.0
   },
   "color": "blue"
  },
  {
   "title": "Law of Cosines (SSS)",
   "kind": "example",
   "text": "Find the largest angle first (opposite the longest side).",
   "example": "a = 5, b = 7, c = 8. Find C.",
   "steps": [
    [
     "cos C:",
     "⟨\\tfrac{25 + 49 - 64}{70} = \\tfrac{1}{7}⟩"
    ]
   ],
   "answer": "≈ 81.8°",
   "check": {
    "num": "Math.round(Math.acos(1/7)*180/Math.PI*10)/10",
    "is": 81.8
   },
   "color": "green"
  },
  {
   "title": "The Ambiguous Case (SSA, A acute)",
   "kind": "table",
   "plain": true,
   "head": [
    "Condition",
    "Triangles"
   ],
   "rows": [
    [
     "a < b sin A",
     "0"
    ],
    [
     "a = b sin A",
     "1 (right)"
    ],
    [
     "b sin A < a < b",
     "2"
    ],
    [
     "a ≥ b",
     "1"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Triangle Area",
   "kind": "table",
   "plain": true,
   "head": [
    "Given",
    "Area"
   ],
   "rows": [
    [
     "two sides + included angle",
     "⟨\\tfrac{1}{2}ab\\sin C⟩"
    ],
    [
     "three sides (Heron)",
     "⟨\\sqrt{s(s - a)(s - b)(s - c)}⟩, ⟨s = \\tfrac{a + b + c}{2}⟩"
    ]
   ],
   "after": "Sides 5, 7, 8: s = 10, area = √300 ≈ 17.32.",
   "check": {
    "num": "Math.sqrt(10*5*3*2)",
    "is": 17.320508075688775
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "SAS / SSS → Law of Cosines; AAS / ASA → Law of Sines.",
    "For SSA, did I check for a second triangle?",
    "Is the longest side opposite the largest angle?",
    "Do my angles add to 180°?"
   ],
   "color": "teal"
  }
 ]
};
