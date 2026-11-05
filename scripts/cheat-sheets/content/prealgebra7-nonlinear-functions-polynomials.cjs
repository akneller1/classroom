/* Pre-Algebra (7th) Unit 13 cheat sheet (Nonlinear Functions and Polynomials). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-nonlinear-functions-polynomials",
 "course": "Pre-Algebra (7th)",
 "unitNo": 13,
 "unitName": "Nonlinear Functions and Polynomials",
 "focus": "sequences, nonlinear graphs and exponential growth and decay",
 "morefocus": "adding, subtracting and multiplying polynomials",
 "front": [
  {
   "title": "Sequences",
   "kind": "table",
   "plain": true,
   "head": [
    "Type",
    "Example"
   ],
   "rows": [
    [
     "Arithmetic (add the same number)",
     "5, 9, 13, 17 (+4)"
    ],
    [
     "Geometric (multiply by the same number)",
     "3, 6, 12, 24 (×2)"
    ],
    [
     "Neither",
     "1, 4, 9, 16 (squares)"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Next Terms",
   "kind": "example",
   "text": "Find the common difference or ratio.",
   "example": "2, 6, 18, 54, …",
   "steps": [
    [
     "Ratio:",
     "× 3"
    ]
   ],
   "answer": "162, 486",
   "check": [
    {
     "num": "54*3",
     "is": 162
    },
    {
     "num": "162*3",
     "is": 486
    }
   ],
   "color": "blue"
  },
  {
   "title": "Graphing Nonlinear Functions",
   "kind": "table",
   "plain": true,
   "head": [
    "Function",
    "Shape"
   ],
   "rows": [
    [
     "⟨y = x^2⟩",
     "U-shaped parabola"
    ],
    [
     "⟨y = |x|⟩",
     "V shape"
    ],
    [
     "⟨y = 2^x⟩",
     "exponential curve"
    ]
   ],
   "after": "Make a table: for ⟨y = x^2⟩, x = −2, 0, 2 gives y = 4, 0, 4.",
   "check": {
    "num": "(-2)**2",
    "is": 4
   },
   "color": "green"
  },
  {
   "title": "Exponential Growth",
   "kind": "example",
   "text": "⟨y = a(1 + r)^t⟩",
   "example": "$500 grows 6% per year for 3 years",
   "steps": [
    [
     "Compute:",
     "⟨500(1.06)^3⟩"
    ]
   ],
   "answer": "≈ $595.51",
   "check": {
    "num": "Math.round(500*1.06**3*100)/100",
    "is": 595.51
   },
   "color": "orange"
  },
  {
   "title": "Exponential Decay",
   "kind": "example",
   "text": "⟨y = a(1 - r)^t⟩",
   "example": "A $20,000 car loses 15% per year. Value after 2 years?",
   "steps": [
    [
     "Compute:",
     "⟨20000(0.85)^2⟩"
    ]
   ],
   "answer": "$14,450",
   "check": {
    "num": "20000*0.85**2",
    "is": 14450
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Linear: constant difference. Exponential: constant ratio.",
    "Growth uses 1 + r, decay uses 1 − r.",
    "Plot enough points to see the curve."
   ],
   "bad": [
    [
     "Treating 2, 6, 18 as +4",
     "× 3"
    ],
    [
     "Decay with 1 + r",
     "1 − r"
    ],
    [
     "Connecting a parabola with straight segments",
     "smooth curve"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "monomial",
     "A number, a variable or their product.",
     "⟨-5x^2⟩"
    ],
    [
     "polynomial",
     "A sum of monomials.",
     "⟨3x^2 + 2x - 7⟩"
    ],
    [
     "degree",
     "Largest exponent.",
     "degree of ⟨4x^3 + x⟩ is 3"
    ],
    [
     "binomial",
     "Two terms.",
     "x + 5"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Adding Polynomials",
   "kind": "example",
   "text": "Combine like terms.",
   "example": "⟨(3x^2 + 2x - 5) + (x^2 - 6x + 4)⟩",
   "steps": [
    [
     "Group:",
     "⟨(3x^2 + x^2) + (2x - 6x) + (-5 + 4)⟩"
    ]
   ],
   "answer": "⟨4x^2 - 4x - 1⟩",
   "check": {
    "expr": "(3*x**2+2*x-5)+(x**2-6*x+4)",
    "is": "4*x**2-4*x-1"
   },
   "color": "blue"
  },
  {
   "title": "Subtracting Polynomials",
   "kind": "example",
   "text": "Distribute the minus sign to EVERY term, then combine.",
   "example": "⟨(5x^2 - 3x) - (2x^2 + x - 8)⟩",
   "steps": [
    [
     "Distribute −:",
     "⟨5x^2 - 3x - 2x^2 - x + 8⟩"
    ]
   ],
   "answer": "⟨3x^2 - 4x + 8⟩",
   "check": {
    "expr": "(5*x**2-3*x)-(2*x**2+x-8)",
    "is": "3*x**2-4*x+8"
   },
   "color": "green"
  },
  {
   "title": "Polynomial × Monomial",
   "kind": "example",
   "text": "Distribute; multiply coefficients and add exponents.",
   "example": "⟨2x(3x^2 - 4x + 1)⟩",
   "steps": [
    [
     "Distribute:",
     "⟨6x^3 - 8x^2 + 2x⟩"
    ]
   ],
   "answer": "⟨6x^3 - 8x^2 + 2x⟩",
   "check": {
    "expr": "2*x*(3*x**2-4*x+1)",
    "is": "6*x**3-8*x**2+2*x"
   },
   "color": "orange"
  },
  {
   "title": "Multiplying Binomials (FOIL)",
   "kind": "example",
   "text": "First, Outer, Inner, Last, then combine.",
   "example": "(x + 4)(x − 3)",
   "steps": [
    [
     "FOIL:",
     "⟨x^2 - 3x + 4x - 12⟩"
    ]
   ],
   "answer": "⟨x^2 + x - 12⟩",
   "check": {
    "expr": "(x+4)*(x-3)",
    "is": "x**2+x-12"
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I distribute the minus to every term?",
    "Did I add exponents when multiplying?",
    "Did I combine like terms at the end?",
    "Is my answer in standard form (highest power first)?"
   ],
   "color": "teal"
  }
 ]
};
