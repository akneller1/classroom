/* Calculus Unit 2 cheat sheet (Limits and Continuity). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-limits-continuity",
 "course": "Calculus",
 "unitNo": 2,
 "unitName": "Limits and Continuity",
 "focus": "limit notation, evaluating limits algebraically and graphically",
 "morefocus": "one-sided and infinite limits, continuity and the IVT",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "limit",
     "The value f(x) approaches as x → a.",
     "⟨\\lim_{x \\to 2} x^2 = 4⟩"
    ],
    [
     "one-sided limit",
     "Approach from one side.",
     "⟨\\lim_{x \\to 0^+}⟩"
    ],
    [
     "indeterminate form",
     "Needs more work.",
     "⟨\\tfrac{0}{0}⟩"
    ],
    [
     "continuous at a",
     "⟨\\lim_{x \\to a} f(x) = f(a)⟩",
     "polynomials"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Direct Substitution",
   "kind": "example",
   "text": "Try plugging in first.",
   "example": "⟨\\lim_{x \\to 3}(2x^2 - x)⟩",
   "steps": [
    [
     "Substitute:",
     "18 − 3"
    ]
   ],
   "answer": "15",
   "check": {
    "num": "2*9-3",
    "is": 15
   },
   "color": "blue"
  },
  {
   "title": "Factor and Cancel",
   "kind": "example",
   "text": "⟨\\tfrac{0}{0}⟩ → factor, cancel, substitute.",
   "example": "⟨\\lim_{x \\to 2}\\tfrac{x^2 - 4}{x - 2}⟩",
   "steps": [
    [
     "Factor:",
     "⟨\\tfrac{(x - 2)(x + 2)}{x - 2} = x + 2⟩"
    ]
   ],
   "answer": "4",
   "check": {
    "true": "Math.abs((2.000001**2-4)/(2.000001-2)-4)<1e-5"
   },
   "color": "green"
  },
  {
   "title": "Rationalize",
   "kind": "example",
   "text": "Multiply by the conjugate.",
   "example": "⟨\\lim_{x \\to 0}\\tfrac{\\sqrt{x + 9} - 3}{x}⟩",
   "steps": [
    [
     "Conjugate:",
     "⟨\\tfrac{1}{\\sqrt{x + 9} + 3}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{1}{6}⟩",
   "check": {
    "true": "Math.abs((Math.sqrt(1e-6+9)-3)/1e-6-1/6)<1e-5"
   },
   "color": "orange"
  },
  {
   "title": "Special Trig Limits",
   "kind": "table",
   "plain": true,
   "head": [
    "Limit",
    "Value"
   ],
   "rows": [
    [
     "⟨\\lim_{x \\to 0}\\tfrac{\\sin x}{x}⟩",
     "1"
    ],
    [
     "⟨\\lim_{x \\to 0}\\tfrac{1 - \\cos x}{x}⟩",
     "0"
    ],
    [
     "⟨\\lim_{x \\to 0}\\tfrac{\\sin 5x}{x}⟩",
     "5"
    ]
   ],
   "check": {
    "true": "Math.abs(Math.sin(5e-6)/1e-6-5)<1e-6"
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "⟨\\tfrac{0}{0}⟩ means “do more work,” not “no limit.”",
    "A limit exists only if both one-sided limits agree.",
    "f(a) need not equal the limit."
   ],
   "bad": [
    [
     "⟨\\tfrac{0}{0} = 0⟩",
     "indeterminate"
    ],
    [
     "⟨\\tfrac{5}{0}⟩ → limit is 0",
     "infinite / DNE"
    ],
    [
     "Limit = f(a) always",
     "only if continuous"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "One-Sided Limits",
   "kind": "example",
   "text": "Check each side separately.",
   "example": "⟨\\lim_{x \\to 0}\\tfrac{|x|}{x}⟩",
   "steps": [
    [
     "Left:",
     "−1"
    ],
    [
     "Right:",
     "1"
    ]
   ],
   "answer": "DNE",
   "check": [
    {
     "num": "Math.abs(-1e-6)/(-1e-6)",
     "is": -1
    },
    {
     "num": "Math.abs(1e-6)/1e-6",
     "is": 1
    }
   ],
   "color": "purple"
  },
  {
   "title": "Infinite Limits",
   "kind": "example",
   "text": "Nonzero ÷ 0 → ±∞; check the sign.",
   "example": "⟨\\lim_{x \\to 3^+}\\tfrac{2}{x - 3}⟩",
   "steps": [
    [
     "Denominator:",
     "small positive"
    ]
   ],
   "answer": "+∞ (vertical asymptote x = 3)",
   "check": {
    "true": "2/(3.000001-3) > 1e6"
   },
   "color": "blue"
  },
  {
   "title": "Limits at Infinity (rational)",
   "kind": "table",
   "plain": true,
   "head": [
    "Degrees",
    "Limit"
   ],
   "rows": [
    [
     "top < bottom",
     "0"
    ],
    [
     "top = bottom",
     "ratio of leading coefficients"
    ],
    [
     "top > bottom",
     "±∞"
    ]
   ],
   "after": "⟨\\lim_{x \\to \\infty}\\tfrac{3x^2 + 1}{5x^2 - x} = \\tfrac{3}{5}⟩",
   "check": {
    "true": "Math.abs((3*1e8+1)/(5*1e8-1e4)-3/5)<1e-4"
   },
   "color": "green"
  },
  {
   "title": "Continuity at x = a",
   "kind": "list",
   "items": [
    "1. f(a) is defined.",
    "2. ⟨\\lim_{x \\to a} f(x)⟩ exists.",
    "3. The limit equals f(a).",
    "Discontinuities: removable (hole), jump, infinite (asymptote)."
   ],
   "color": "orange"
  },
  {
   "title": "Making a Piecewise Function Continuous",
   "kind": "example",
   "text": "Set the left and right pieces equal at the break.",
   "example": "f(x) = kx + 1 for x < 2, ⟨x^2⟩ for x ≥ 2",
   "steps": [
    [
     "Match:",
     "2k + 1 = 4"
    ]
   ],
   "answer": "⟨k = \\tfrac{3}{2}⟩",
   "check": {
    "num": "2*1.5+1",
    "is": 4
   },
   "color": "pink"
  },
  {
   "title": "Intermediate Value Theorem",
   "kind": "example",
   "text": "Continuous on [a, b] → hits every value between f(a) and f(b).",
   "example": "Does ⟨x^3 - x - 1 = 0⟩ have a root in [1, 2]?",
   "steps": [
    [
     "Signs:",
     "f(1) = −1, f(2) = 5"
    ]
   ],
   "answer": "Yes, by the IVT",
   "check": {
    "true": "(1-1-1) < 0 && (8-2-1) > 0"
   },
   "color": "teal"
  }
 ]
};
