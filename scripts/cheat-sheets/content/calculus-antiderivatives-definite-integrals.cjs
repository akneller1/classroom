/* Calculus Unit 5 cheat sheet (Antiderivatives and Definite Integrals). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-antiderivatives-definite-integrals",
 "course": "Calculus",
 "unitNo": 5,
 "unitName": "Antiderivatives and Definite Integrals",
 "focus": "antiderivatives, indefinite integrals and u-substitution",
 "morefocus": "Riemann sums, definite integrals and their properties",
 "front": [
  {
   "title": "Basic Antiderivatives",
   "kind": "table",
   "plain": true,
   "head": [
    "Integral",
    "Result"
   ],
   "rows": [
    [
     "⟨\\int x^n\\,dx⟩",
     "⟨\\tfrac{x^{n+1}}{n + 1} + C⟩ (n ≠ −1)"
    ],
    [
     "⟨\\int \\tfrac{1}{x}\\,dx⟩",
     "⟨\\ln|x| + C⟩"
    ],
    [
     "⟨\\int e^x\\,dx⟩",
     "⟨e^x + C⟩"
    ],
    [
     "⟨\\int \\cos x\\,dx⟩",
     "sin x + C"
    ],
    [
     "⟨\\int \\sin x\\,dx⟩",
     "−cos x + C"
    ],
    [
     "⟨\\int \\sec^2 x\\,dx⟩",
     "tan x + C"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Power Rule for Integrals",
   "kind": "example",
   "text": "Add 1 to the exponent, divide by the new exponent. +C!",
   "example": "⟨\\int (6x^2 - 4x + 3)\\,dx⟩",
   "steps": [
    [
     "Integrate:",
     "⟨2x^3 - 2x^2 + 3x⟩"
    ]
   ],
   "answer": "⟨2x^3 - 2x^2 + 3x + C⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>2*x**3-2*x**2+3*x)(t+1e-6)-(x=>2*x**3-2*x**2+3*x)(t-1e-6))/2e-6-(x=>6*x**2-4*x+3)(t))<1e-5*(1+Math.abs((x=>6*x**2-4*x+3)(t))))"
   },
   "color": "blue"
  },
  {
   "title": "u-Substitution",
   "kind": "example",
   "text": "Let u = the inside; replace dx using du.",
   "example": "⟨\\int 2x(x^2 + 1)^4\\,dx⟩",
   "steps": [
    [
     "u = x² + 1:",
     "du = 2x dx → ⟨\\int u^4\\,du⟩"
    ]
   ],
   "answer": "⟨\\tfrac{(x^2 + 1)^5}{5} + C⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>(x**2+1)**5/5)(t+1e-6)-(x=>(x**2+1)**5/5)(t-1e-6))/2e-6-(x=>2*x*(x**2+1)**4)(t))<1e-5*(1+Math.abs((x=>2*x*(x**2+1)**4)(t))))"
   },
   "color": "green"
  },
  {
   "title": "Initial Value Problem",
   "kind": "example",
   "text": "Integrate, then use the point to find C.",
   "example": "⟨f\\prime(x) = 3x^2⟩, f(1) = 5",
   "steps": [
    [
     "Integrate:",
     "⟨f(x) = x^3 + C⟩"
    ],
    [
     "1 + C = 5:",
     "C = 4"
    ]
   ],
   "answer": "⟨f(x) = x^3 + 4⟩",
   "check": {
    "num": "1+4",
    "is": 5
   },
   "color": "orange"
  },
  {
   "title": "More Integrals",
   "kind": "table",
   "plain": true,
   "head": [
    "Integral",
    "Result"
   ],
   "rows": [
    [
     "⟨\\int \\tfrac{1}{1 + x^2}\\,dx⟩",
     "⟨\\tan^{-1}x + C⟩"
    ],
    [
     "⟨\\int \\tfrac{1}{\\sqrt{1 - x^2}}\\,dx⟩",
     "⟨\\sin^{-1}x + C⟩"
    ],
    [
     "⟨\\int e^{kx}\\,dx⟩",
     "⟨\\tfrac{1}{k}e^{kx} + C⟩"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Always add + C to indefinite integrals.",
    "Check by differentiating your answer.",
    "With u-sub, every x must become u."
   ],
   "bad": [
    [
     "⟨\\int x^{-1}dx = \\tfrac{x^0}{0}⟩",
     "⟨\\ln|x|⟩"
    ],
    [
     "⟨\\int \\sin x\\,dx = \\cos x⟩",
     "−cos x + C"
    ],
    [
     "Leaving x and u mixed",
     "substitute fully"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Riemann Sums",
   "kind": "table",
   "plain": true,
   "head": [
    "Method",
    "Height from"
   ],
   "rows": [
    [
     "Left",
     "left endpoint"
    ],
    [
     "Right",
     "right endpoint"
    ],
    [
     "Midpoint",
     "midpoint"
    ],
    [
     "Trapezoid",
     "⟨\\tfrac{\\Delta x}{2}(f_0 + 2f_1 + \\dots + f_n)⟩"
    ]
   ],
   "after": "Increasing f: left underestimates, right overestimates.",
   "color": "purple"
  },
  {
   "title": "Right Riemann Sum",
   "kind": "example",
   "text": "⟨\\Delta x = \\tfrac{b - a}{n}⟩, add f(right) · Δx.",
   "example": "⟨f(x) = x^2⟩ on [0, 2], n = 4",
   "steps": [
    [
     "Δx = 0.5:",
     "0.5(0.25 + 1 + 2.25 + 4)"
    ]
   ],
   "answer": "3.75",
   "check": {
    "num": "0.5*(0.25+1+2.25+4)",
    "is": 3.75
   },
   "color": "blue"
  },
  {
   "title": "Definite Integral as Area",
   "kind": "example",
   "text": "Use geometry when the graph is a known shape.",
   "example": "⟨\\int_0^4 (x + 1)\\,dx⟩",
   "steps": [
    [
     "Trapezoid:",
     "⟨\\tfrac{1}{2}(1 + 5)(4)⟩"
    ]
   ],
   "answer": "12",
   "check": {
    "num": "0.5*(1+5)*4",
    "is": 12
   },
   "color": "green"
  },
  {
   "title": "Integral Properties",
   "kind": "table",
   "plain": true,
   "head": [
    "Property",
    "Rule"
   ],
   "rows": [
    [
     "Reverse limits",
     "⟨\\int_b^a f = -\\int_a^b f⟩"
    ],
    [
     "Same limits",
     "⟨\\int_a^a f = 0⟩"
    ],
    [
     "Split",
     "⟨\\int_a^c f = \\int_a^b f + \\int_b^c f⟩"
    ],
    [
     "Constant",
     "⟨\\int_a^b kf = k\\int_a^b f⟩"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Using Properties",
   "kind": "example",
   "text": "Combine the given pieces.",
   "example": "⟨\\int_0^3 f = 7⟩, ⟨\\int_0^5 f = 2⟩. Find ⟨\\int_3^5 f⟩.",
   "steps": [
    [
     "Split:",
     "2 − 7"
    ]
   ],
   "answer": "−5",
   "check": {
    "num": "2-7",
    "is": -5
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I add + C?",
    "Is Δx = (b − a) ÷ n?",
    "Area below the x-axis counts as negative.",
    "Did I differentiate to check?"
   ],
   "color": "teal"
  }
 ]
};
