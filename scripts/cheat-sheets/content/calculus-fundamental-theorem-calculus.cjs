/* Calculus Unit 6 cheat sheet (The Fundamental Theorem of Calculus). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-fundamental-theorem-calculus",
 "course": "Calculus",
 "unitNo": 6,
 "unitName": "The Fundamental Theorem of Calculus",
 "focus": "FTC part 1 and part 2",
 "morefocus": "average value, accumulation functions and net change",
 "front": [
  {
   "title": "The Fundamental Theorem",
   "kind": "table",
   "plain": true,
   "head": [
    "Part",
    "Statement"
   ],
   "rows": [
    [
     "Part 1",
     "⟨\\tfrac{d}{dx}\\int_a^x f(t)\\,dt = f(x)⟩"
    ],
    [
     "Part 2",
     "⟨\\int_a^b f(x)\\,dx = F(b) - F(a)⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Evaluating with FTC 2",
   "kind": "example",
   "text": "Antiderivative, then top minus bottom.",
   "example": "⟨\\int_1^3 (2x + 1)\\,dx⟩",
   "steps": [
    [
     "Antiderivative:",
     "⟨x^2 + x⟩"
    ],
    [
     "Evaluate:",
     "(9 + 3) − (1 + 1)"
    ]
   ],
   "answer": "10",
   "check": {
    "num": "(9+3)-(1+1)",
    "is": 10
   },
   "color": "blue"
  },
  {
   "title": "Trig Integral",
   "kind": "example",
   "text": "Use exact values.",
   "example": "⟨\\int_0^{\\pi/2} \\cos x\\,dx⟩",
   "steps": [
    [
     "sin x:",
     "⟨\\sin\\tfrac{\\pi}{2} - \\sin 0⟩"
    ]
   ],
   "answer": "1",
   "check": {
    "num": "Math.sin(Math.PI/2)-Math.sin(0)",
    "is": 1
   },
   "color": "green"
  },
  {
   "title": "FTC 1 with a Chain",
   "kind": "example",
   "text": "Plug in the upper limit and multiply by its derivative.",
   "example": "⟨\\tfrac{d}{dx}\\int_2^{x^3} \\sqrt{t}\\,dt⟩",
   "steps": [
    [
     "Apply:",
     "⟨\\sqrt{x^3} \\cdot 3x^2⟩"
    ]
   ],
   "answer": "⟨3x^{7/2}⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>x**4.5*2/3)(t+1e-6)-(x=>x**4.5*2/3)(t-1e-6))/2e-6-(x=>Math.sqrt(x**3)*3*x**2)(t))<1e-5*(1+Math.abs((x=>Math.sqrt(x**3)*3*x**2)(t))))"
   },
   "color": "orange"
  },
  {
   "title": "Definite u-Substitution",
   "kind": "example",
   "text": "Change the limits to u-values.",
   "example": "⟨\\int_0^1 2x e^{x^2}\\,dx⟩",
   "steps": [
    [
     "u = x²:",
     "⟨\\int_0^1 e^u\\,du⟩"
    ]
   ],
   "answer": "e − 1",
   "check": {
    "num": "Math.E-1",
    "is": 1.718281828459045
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "FTC 2: F(b) − F(a), top minus bottom.",
    "FTC 1: the derivative undoes the integral.",
    "Change limits when substituting."
   ],
   "bad": [
    [
     "F(a) − F(b)",
     "F(b) − F(a)"
    ],
    [
     "Forgetting the chain factor",
     "multiply by the inner derivative"
    ],
    [
     "Keeping x-limits after u-sub",
     "convert them"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Average Value",
   "kind": "example",
   "text": "⟨f_{avg} = \\tfrac{1}{b - a}\\int_a^b f(x)\\,dx⟩",
   "example": "⟨f(x) = x^2⟩ on [0, 3]",
   "steps": [
    [
     "Integral:",
     "9"
    ],
    [
     "Divide by 3:",
     "3"
    ]
   ],
   "answer": "3",
   "check": {
    "num": "9/3",
    "is": 3
   },
   "color": "purple"
  },
  {
   "title": "Accumulation Function",
   "kind": "example",
   "text": "⟨g(x) = \\int_a^x f(t)\\,dt⟩; g′ = f.",
   "example": "⟨g(x) = \\int_0^x (t^2 - 4)\\,dt⟩: where is g increasing?",
   "steps": [
    [
     "g′(x) = x² − 4 > 0:",
     "|x| > 2"
    ]
   ],
   "answer": "x < −2 or x > 2",
   "check": {
    "true": "9-4>0 && !(1-4>0)"
   },
   "color": "blue"
  },
  {
   "title": "Net Change",
   "kind": "example",
   "text": "⟨F(b) = F(a) + \\int_a^b F\\prime(t)\\,dt⟩",
   "example": "Water: 50 gal at t = 0, rate r(t) = 4t gal/min. Amount at t = 3?",
   "steps": [
    [
     "Integrate:",
     "⟨\\int_0^3 4t\\,dt = 18⟩"
    ]
   ],
   "answer": "68 gal",
   "check": {
    "num": "50+2*9",
    "is": 68
   },
   "color": "green"
  },
  {
   "title": "Displacement vs. Distance",
   "kind": "table",
   "plain": true,
   "head": [
    "Quantity",
    "Integral"
   ],
   "rows": [
    [
     "Displacement",
     "⟨\\int_a^b v(t)\\,dt⟩"
    ],
    [
     "Total distance",
     "⟨\\int_a^b |v(t)|\\,dt⟩"
    ]
   ],
   "after": "v(t) = t − 2 on [0, 4]: displacement 0, distance 4.",
   "check": [
    {
     "num": "(16/2-8)-0",
     "is": 0
    },
    {
     "num": "2+2",
     "is": 4
    }
   ],
   "color": "orange"
  },
  {
   "title": "Reading g from the Graph of f",
   "kind": "table",
   "plain": true,
   "head": [
    "f",
    "g"
   ],
   "rows": [
    [
     "f > 0",
     "g increasing"
    ],
    [
     "f changes + to −",
     "g has a max"
    ],
    [
     "f increasing",
     "g concave up"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I include the initial amount for net change?",
    "Distance uses |v|, displacement does not.",
    "Did I divide by (b − a) for average value?",
    "Units: rate × time = amount."
   ],
   "color": "teal"
  }
 ]
};
