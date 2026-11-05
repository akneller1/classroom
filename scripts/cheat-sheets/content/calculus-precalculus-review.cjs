/* Calculus Unit 1 cheat sheet (Precalculus Review). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-precalculus-review",
 "course": "Calculus",
 "unitNo": 1,
 "unitName": "Precalculus Review",
 "focus": "functions, domain, graphs and transformations",
 "morefocus": "exponentials, logarithms and trigonometry you will need",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "function",
     "Each input has exactly one output.",
     "⟨f(x) = x^2⟩"
    ],
    [
     "domain",
     "Allowed inputs.",
     "⟨\\ln x⟩: x > 0"
    ],
    [
     "one-to-one",
     "Passes the horizontal line test.",
     "⟨x^3⟩"
    ],
    [
     "piecewise",
     "Different rules on different intervals.",
     "|x|"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Domain",
   "kind": "example",
   "text": "No zero denominators, no negative even roots, no log of 0 or negatives.",
   "example": "⟨f(x) = \\tfrac{\\sqrt{x + 2}}{x - 3}⟩",
   "steps": [
    [
     "Root:",
     "x ≥ −2"
    ],
    [
     "Denominator:",
     "x ≠ 3"
    ]
   ],
   "answer": "[−2, 3) ∪ (3, ∞)",
   "check": {
    "true": "Number.isFinite(Math.sqrt(-2+2)/(-2-3)) && !Number.isFinite(Math.sqrt(5)/(3-3))"
   },
   "color": "blue"
  },
  {
   "title": "Composition",
   "kind": "example",
   "text": "Inside function first.",
   "example": "⟨f(x) = \\sqrt{x},\\ g(x) = x^2 + 5⟩; f(g(2))",
   "steps": [
    [
     "g(2):",
     "9"
    ],
    [
     "f(9):",
     "3"
    ]
   ],
   "answer": "3",
   "check": {
    "num": "Math.sqrt(2**2+5)",
    "is": 3
   },
   "color": "green"
  },
  {
   "title": "Inverses",
   "kind": "example",
   "text": "Swap x and y, solve for y.",
   "example": "⟨f(x) = e^{x} + 1⟩",
   "steps": [
    [
     "Swap:",
     "⟨x = e^y + 1⟩"
    ]
   ],
   "answer": "⟨f^{-1}(x) = \\ln(x - 1)⟩",
   "check": {
    "num": "Math.log(Math.exp(2)+1-1)",
    "is": 2
   },
   "color": "orange"
  },
  {
   "title": "Parent Graphs",
   "kind": "table",
   "plain": true,
   "head": [
    "Function",
    "Key feature"
   ],
   "rows": [
    [
     "⟨x^2⟩",
     "vertex (0, 0)"
    ],
    [
     "⟨\\sqrt{x}⟩",
     "starts at (0, 0)"
    ],
    [
     "⟨\\tfrac{1}{x}⟩",
     "asymptotes x = 0, y = 0"
    ],
    [
     "⟨e^x⟩",
     "passes (0, 1), y = 0 asymptote"
    ],
    [
     "⟨\\ln x⟩",
     "passes (1, 0), x = 0 asymptote"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "f(x − h) shifts right.",
    "⟨f^{-1}(x) \\ne \\tfrac{1}{f(x)}⟩.",
    "Simplify before substituting."
   ],
   "bad": [
    [
     "⟨\\sqrt{a + b} = \\sqrt{a} + \\sqrt{b}⟩",
     "not true"
    ],
    [
     "⟨(a + b)^2 = a^2 + b^2⟩",
     "⟨a^2 + 2ab + b^2⟩"
    ],
    [
     "⟨\\ln(a + b) = \\ln a + \\ln b⟩",
     "⟨\\ln(ab) = \\ln a + \\ln b⟩"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Exponent and Log Rules",
   "kind": "table",
   "plain": true,
   "head": [
    "Rule",
    "Example"
   ],
   "rows": [
    [
     "⟨\\ln(ab) = \\ln a + \\ln b⟩",
     "⟨\\ln 6 = \\ln 2 + \\ln 3⟩"
    ],
    [
     "⟨\\ln a^p = p\\ln a⟩",
     "⟨\\ln x^3 = 3\\ln x⟩"
    ],
    [
     "⟨e^{\\ln x} = x⟩, ⟨\\ln e^x = x⟩",
     "⟨e^{\\ln 5} = 5⟩"
    ]
   ],
   "check": {
    "num": "Math.log(6)-Math.log(2)-Math.log(3)",
    "is": 0
   },
   "color": "purple"
  },
  {
   "title": "Solving with Logs",
   "kind": "example",
   "text": "Isolate the exponential, then take ln.",
   "example": "⟨3e^{2x} = 12⟩",
   "steps": [
    [
     "Isolate:",
     "⟨e^{2x} = 4⟩"
    ],
    [
     "ln:",
     "⟨2x = \\ln 4⟩"
    ]
   ],
   "answer": "⟨x = \\ln 2⟩ ≈ 0.693",
   "check": {
    "num": "3*Math.exp(2*Math.log(2))",
    "is": 12
   },
   "color": "blue"
  },
  {
   "title": "Unit Circle Essentials",
   "kind": "table",
   "plain": true,
   "head": [
    "θ",
    "sin · cos · tan"
   ],
   "rows": [
    [
     "⟨\\tfrac{\\pi}{6}⟩",
     "⟨\\tfrac{1}{2}⟩ · ⟨\\tfrac{\\sqrt{3}}{2}⟩ · ⟨\\tfrac{\\sqrt{3}}{3}⟩"
    ],
    [
     "⟨\\tfrac{\\pi}{4}⟩",
     "⟨\\tfrac{\\sqrt{2}}{2}⟩ · ⟨\\tfrac{\\sqrt{2}}{2}⟩ · 1"
    ],
    [
     "⟨\\tfrac{\\pi}{3}⟩",
     "⟨\\tfrac{\\sqrt{3}}{2}⟩ · ⟨\\tfrac{1}{2}⟩ · ⟨\\sqrt{3}⟩"
    ]
   ],
   "check": {
    "num": "Math.tan(Math.PI/3)",
    "is": 1.7320508075688767
   },
   "color": "green"
  },
  {
   "title": "Trig Identities",
   "kind": "table",
   "plain": true,
   "head": [
    "Identity",
    "Use"
   ],
   "rows": [
    [
     "⟨\\sin^2 x + \\cos^2 x = 1⟩",
     "simplify"
    ],
    [
     "⟨\\sin 2x = 2\\sin x\\cos x⟩",
     "double angle"
    ],
    [
     "⟨\\cos^2 x = \\tfrac{1 + \\cos 2x}{2}⟩",
     "power reduction (integrals)"
    ]
   ],
   "check": {
    "num": "Math.cos(0.3)**2-(1+Math.cos(0.6))/2",
    "is": 0
   },
   "color": "orange"
  },
  {
   "title": "Factoring Review",
   "kind": "example",
   "text": "Look for GCF, difference of squares, trinomials.",
   "example": "⟨x^3 - 9x⟩",
   "steps": [
    [
     "GCF:",
     "⟨x(x^2 - 9)⟩"
    ]
   ],
   "answer": "x(x − 3)(x + 3)",
   "check": {
    "expr": "x*(x-3)*(x+3)",
    "is": "x**3-9*x"
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Is my calculator in radians?",
    "Did I state the domain?",
    "Did I simplify fully before moving on?",
    "Did I check my answer with a graph?"
   ],
   "color": "teal"
  }
 ]
};
