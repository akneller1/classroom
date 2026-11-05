/* Calculus Unit 4 cheat sheet (Applications of Derivatives). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-applications-derivatives",
 "course": "Calculus",
 "unitNo": 4,
 "unitName": "Applications of Derivatives",
 "focus": "related rates, motion and linearization",
 "morefocus": "extrema, the MVT, curve sketching and optimization",
 "front": [
  {
   "title": "Related Rates",
   "kind": "example",
   "text": "Write an equation, differentiate with respect to t, THEN substitute.",
   "example": "A circle’s radius grows 2 cm/s. How fast is area growing when r = 5?",
   "steps": [
    [
     "Differentiate:",
     "⟨\\tfrac{dA}{dt} = 2\\pi r\\tfrac{dr}{dt}⟩"
    ]
   ],
   "answer": "⟨20\\pi⟩ cm²/s",
   "check": {
    "num": "2*Math.PI*5*2",
    "is": 62.83185307179586
   },
   "color": "purple"
  },
  {
   "title": "Motion",
   "kind": "table",
   "plain": true,
   "head": [
    "Quantity",
    "Meaning"
   ],
   "rows": [
    [
     "s(t)",
     "position"
    ],
    [
     "v(t) = s′(t)",
     "velocity"
    ],
    [
     "a(t) = v′(t)",
     "acceleration"
    ],
    [
     "speed",
     "|v(t)|"
    ]
   ],
   "after": "Speeding up when v and a have the same sign.",
   "color": "blue"
  },
  {
   "title": "Linearization",
   "kind": "example",
   "text": "⟨L(x) = f(a) + f\\prime(a)(x - a)⟩",
   "example": "Estimate ⟨\\sqrt{4.1}⟩.",
   "steps": [
    [
     "a = 4:",
     "⟨2 + \\tfrac{1}{4}(0.1)⟩"
    ]
   ],
   "answer": "2.025",
   "check": {
    "num": "2+0.25*0.1",
    "is": 2.025
   },
   "color": "green"
  },
  {
   "title": "Particle at Rest",
   "kind": "example",
   "text": "Set v(t) = 0.",
   "example": "⟨s(t) = t^3 - 6t^2 + 9t⟩",
   "steps": [
    [
     "v(t):",
     "⟨3t^2 - 12t + 9 = 3(t - 1)(t - 3)⟩"
    ]
   ],
   "answer": "t = 1 and t = 3",
   "check": [
    {
     "num": "3-12+9",
     "is": 0
    },
    {
     "num": "27-36+9",
     "is": 0
    }
   ],
   "color": "orange"
  },
  {
   "title": "L’Hôpital’s Rule",
   "kind": "table",
   "plain": true,
   "head": [
    "Form",
    "Do"
   ],
   "rows": [
    [
     "⟨\\tfrac{0}{0}⟩ or ⟨\\tfrac{\\infty}{\\infty}⟩",
     "⟨\\lim\\tfrac{f\\prime}{g\\prime}⟩"
    ],
    [
     "other forms",
     "rewrite first"
    ]
   ],
   "after": "⟨\\lim_{x \\to 0}\\tfrac{e^x - 1}{x} = \\lim\\tfrac{e^x}{1} = 1⟩",
   "check": {
    "true": "Math.abs((Math.exp(1e-6)-1)/1e-6-1)<1e-5"
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Substitute numbers only AFTER differentiating.",
    "Include units with rates.",
    "L’Hôpital uses f′/g′, not the quotient rule."
   ],
   "bad": [
    [
     "Plug in r = 5 before differentiating",
     "differentiate first"
    ],
    [
     "Speed = velocity",
     "|velocity|"
    ],
    [
     "L’Hôpital on 1 ÷ 0",
     "only 0/0 or ∞/∞"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Finding Extrema",
   "kind": "list",
   "items": [
    "Critical points: f′(x) = 0 or undefined.",
    "First derivative test: sign change + to − → max, − to + → min.",
    "Second derivative test: f″ > 0 → min, f″ < 0 → max.",
    "Closed interval: compare critical points AND endpoints."
   ],
   "color": "purple"
  },
  {
   "title": "Absolute Extrema",
   "kind": "example",
   "text": "Evaluate f at critical points and endpoints.",
   "example": "⟨f(x) = x^3 - 3x⟩ on [0, 2]",
   "steps": [
    [
     "f′ = 0:",
     "x = 1"
    ],
    [
     "Values:",
     "f(0) = 0, f(1) = −2, f(2) = 2"
    ]
   ],
   "answer": "max 2, min −2",
   "check": [
    {
     "num": "1-3",
     "is": -2
    },
    {
     "num": "8-6",
     "is": 2
    }
   ],
   "color": "blue"
  },
  {
   "title": "Concavity",
   "kind": "table",
   "plain": true,
   "head": [
    "f″(x)",
    "Graph"
   ],
   "rows": [
    [
     "> 0",
     "concave up (∪)"
    ],
    [
     "< 0",
     "concave down (∩)"
    ],
    [
     "changes sign",
     "point of inflection"
    ]
   ],
   "after": "⟨f(x) = x^3⟩: f″ = 6x, inflection at x = 0.",
   "color": "green"
  },
  {
   "title": "Mean Value Theorem",
   "kind": "example",
   "text": "Some c in (a, b) has ⟨f\\prime(c) = \\tfrac{f(b) - f(a)}{b - a}⟩.",
   "example": "⟨f(x) = x^2⟩ on [1, 3]",
   "steps": [
    [
     "Average slope:",
     "⟨\\tfrac{9 - 1}{2} = 4⟩"
    ],
    [
     "2c = 4:",
     "c = 2"
    ]
   ],
   "answer": "c = 2",
   "check": {
    "num": "(9-1)/2/2",
    "is": 2
   },
   "color": "orange"
  },
  {
   "title": "Optimization",
   "kind": "example",
   "text": "Write a function of ONE variable, differentiate, test.",
   "example": "Maximize area with 40 m of fence (rectangle).",
   "steps": [
    [
     "A = x(20 − x):",
     "A′ = 20 − 2x = 0"
    ]
   ],
   "answer": "10 m × 10 m, 100 m²",
   "check": {
    "num": "10*(20-10)",
    "is": 100
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I check endpoints on a closed interval?",
    "Did I justify max/min with a test?",
    "Did I answer the question asked (with units)?",
    "Did I differentiate before substituting?"
   ],
   "color": "teal"
  }
 ]
};
