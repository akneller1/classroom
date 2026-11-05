/* Precalculus Unit 2 cheat sheet (Functions). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-functions",
 "course": "Precalculus",
 "unitNo": 2,
 "unitName": "Functions",
 "focus": "domain, range, graphs and transformations",
 "morefocus": "combinations, inverses, polynomial, rational, exponential and logarithmic functions",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "domain",
     "All allowed inputs.",
     "⟨\\sqrt{x - 2}⟩: x ≥ 2"
    ],
    [
     "range",
     "All outputs.",
     "⟨x^2⟩: y ≥ 0"
    ],
    [
     "even function",
     "f(−x) = f(x); y-axis symmetry.",
     "⟨x^2⟩, cos x"
    ],
    [
     "odd function",
     "f(−x) = −f(x); origin symmetry.",
     "⟨x^3⟩, sin x"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Transformations of f(x)",
   "kind": "table",
   "plain": true,
   "head": [
    "Form",
    "Effect"
   ],
   "rows": [
    [
     "f(x) + k",
     "up k"
    ],
    [
     "f(x − h)",
     "right h"
    ],
    [
     "−f(x)",
     "reflect over x-axis"
    ],
    [
     "f(−x)",
     "reflect over y-axis"
    ],
    [
     "a·f(x)",
     "vertical stretch by a"
    ],
    [
     "f(bx)",
     "horizontal shrink by ⟨\\tfrac{1}{b}⟩"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Composition",
   "kind": "example",
   "text": "(f ∘ g)(x) = f(g(x)): inside first.",
   "example": "⟨f(x) = x^2 + 1,\\ g(x) = 3x - 2⟩; find (f ∘ g)(2).",
   "steps": [
    [
     "Inside:",
     "g(2) = 4"
    ],
    [
     "Outside:",
     "f(4) = 17"
    ]
   ],
   "answer": "17",
   "check": {
    "num": "(3*2-2)**2+1",
    "is": 17
   },
   "color": "green"
  },
  {
   "title": "Inverse Functions",
   "kind": "example",
   "text": "Swap x and y, then solve for y.",
   "example": "⟨f(x) = \\tfrac{2x + 1}{3}⟩",
   "steps": [
    [
     "Swap:",
     "3x = 2y + 1"
    ]
   ],
   "answer": "⟨f^{-1}(x) = \\tfrac{3x - 1}{2}⟩",
   "check": {
    "num": "(3*((2*5+1)/3)-1)/2",
    "is": 5
   },
   "color": "orange"
  },
  {
   "title": "Average Rate of Change",
   "kind": "example",
   "text": "⟨\\tfrac{f(b) - f(a)}{b - a}⟩",
   "example": "⟨f(x) = x^3⟩ on [1, 3]",
   "steps": [
    [
     "Compute:",
     "⟨\\tfrac{27 - 1}{2}⟩"
    ]
   ],
   "answer": "13",
   "check": {
    "num": "(27-1)/2",
    "is": 13
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "f(x − h) moves RIGHT, not left.",
    "⟨f^{-1}(x) \\ne \\tfrac{1}{f(x)}⟩.",
    "Only one-to-one functions have inverses."
   ],
   "bad": [
    [
     "(f ∘ g)(x) = f(x) · g(x)",
     "plug g into f"
    ],
    [
     "f(x + 3) shifts right 3",
     "left 3"
    ],
    [
     "Domain of ⟨\\tfrac{1}{x - 4}⟩ is all reals",
     "x ≠ 4"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Polynomial End Behavior",
   "kind": "table",
   "plain": true,
   "head": [
    "Degree · lead coefficient",
    "Ends"
   ],
   "rows": [
    [
     "even · positive",
     "both up"
    ],
    [
     "even · negative",
     "both down"
    ],
    [
     "odd · positive",
     "down left, up right"
    ],
    [
     "odd · negative",
     "up left, down right"
    ]
   ],
   "after": "A degree-n polynomial has at most n − 1 turning points.",
   "color": "purple"
  },
  {
   "title": "Rational Function Asymptotes",
   "kind": "table",
   "plain": true,
   "head": [
    "Compare degrees n (top), d (bottom)",
    "Horizontal asymptote"
   ],
   "rows": [
    [
     "n < d",
     "y = 0"
    ],
    [
     "n = d",
     "y = ratio of leading coefficients"
    ],
    [
     "n = d + 1",
     "slant asymptote"
    ]
   ],
   "after": "Vertical asymptotes: zeros of the reduced denominator. For ⟨\\tfrac{2x + 1}{x - 3}⟩: x = 3, y = 2.",
   "color": "blue"
  },
  {
   "title": "Log Properties",
   "kind": "table",
   "plain": true,
   "head": [
    "Property",
    "Rule"
   ],
   "rows": [
    [
     "Product",
     "⟨\\log_b(MN) = \\log_b M + \\log_b N⟩"
    ],
    [
     "Quotient",
     "⟨\\log_b \\tfrac{M}{N} = \\log_b M - \\log_b N⟩"
    ],
    [
     "Power",
     "⟨\\log_b M^p = p\\log_b M⟩"
    ],
    [
     "Change of base",
     "⟨\\log_b M = \\tfrac{\\ln M}{\\ln b}⟩"
    ]
   ],
   "check": {
    "num": "Math.log(8)/Math.log(2)",
    "is": 3
   },
   "color": "green"
  },
  {
   "title": "Exponential Equations",
   "kind": "example",
   "text": "Match bases, or take a log of both sides.",
   "example": "⟨5^{x - 1} = 125⟩",
   "steps": [
    [
     "Match bases:",
     "⟨5^{x - 1} = 5^3⟩"
    ]
   ],
   "answer": "x = 4",
   "check": {
    "num": "5**(4-1)",
    "is": 125
   },
   "color": "orange"
  },
  {
   "title": "Logarithmic Equations",
   "kind": "example",
   "text": "Rewrite in exponential form; check the domain.",
   "example": "⟨\\log_2(x + 3) = 5⟩",
   "steps": [
    [
     "Exponential form:",
     "⟨x + 3 = 2^5⟩"
    ]
   ],
   "answer": "x = 29",
   "check": {
    "num": "Math.log2(29+3)",
    "is": 5
   },
   "color": "pink"
  },
  {
   "title": "Exponential Growth Model",
   "kind": "example",
   "text": "⟨A = Pe^{rt}⟩ for continuous growth.",
   "example": "$2,000 at 4% compounded continuously for 5 years",
   "steps": [
    [
     "Compute:",
     "⟨2000e^{0.2}⟩"
    ]
   ],
   "answer": "≈ $2,442.81",
   "check": {
    "num": "Math.round(2000*Math.exp(0.2)*100)/100",
    "is": 2442.81
   },
   "color": "teal"
  }
 ]
};
