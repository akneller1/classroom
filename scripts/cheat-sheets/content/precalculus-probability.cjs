/* Precalculus Unit 8 cheat sheet (Probability). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-probability",
 "course": "Precalculus",
 "unitNo": 8,
 "unitName": "Probability",
 "focus": "counting, permutations, combinations and basic probability",
 "morefocus": "conditional probability, independence, the binomial theorem and expected value",
 "front": [
  {
   "title": "Fundamental Counting Principle",
   "kind": "example",
   "text": "Multiply the number of choices at each stage.",
   "example": "A code: 2 letters then 3 digits",
   "steps": [
    [
     "Multiply:",
     "⟨26^2 \\cdot 10^3⟩"
    ]
   ],
   "answer": "676,000",
   "check": {
    "num": "26**2*1000",
    "is": 676000
   },
   "color": "purple"
  },
  {
   "title": "Permutations and Combinations",
   "kind": "table",
   "plain": true,
   "head": [
    "Type",
    "Formula"
   ],
   "rows": [
    [
     "Permutation (order matters)",
     "⟨_nP_r = \\tfrac{n!}{(n - r)!}⟩"
    ],
    [
     "Combination (order does not)",
     "⟨_nC_r = \\tfrac{n!}{r!(n - r)!}⟩"
    ],
    [
     "Repeated letters",
     "⟨\\tfrac{n!}{n_1!\\,n_2!\\cdots}⟩"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Permutations",
   "kind": "example",
   "text": "Order matters: president, VP, treasurer.",
   "example": "Choose 3 officers from 10 people.",
   "steps": [
    [
     "Compute:",
     "10 · 9 · 8"
    ]
   ],
   "answer": "720",
   "check": {
    "num": "10*9*8",
    "is": 720
   },
   "color": "green"
  },
  {
   "title": "Combinations",
   "kind": "example",
   "text": "Order does not matter: a committee.",
   "example": "Choose a 3-person committee from 10.",
   "steps": [
    [
     "Divide by 3!:",
     "⟨\\tfrac{720}{6}⟩"
    ]
   ],
   "answer": "120",
   "check": {
    "num": "720/6",
    "is": 120
   },
   "color": "orange"
  },
  {
   "title": "Probability Rules",
   "kind": "table",
   "plain": true,
   "head": [
    "Rule",
    "Formula"
   ],
   "rows": [
    [
     "Complement",
     "P(A') = 1 − P(A)"
    ],
    [
     "Addition",
     "P(A or B) = P(A) + P(B) − P(A and B)"
    ],
    [
     "Mutually exclusive",
     "P(A and B) = 0"
    ]
   ],
   "after": "Draw a card: P(heart or king) = 13/52 + 4/52 − 1/52 = 16/52.",
   "check": {
    "num": "(13+4-1)/52",
    "is": 0.3076923076923077
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Ask: does order matter?",
    "0! = 1.",
    "Probabilities are between 0 and 1."
   ],
   "bad": [
    [
     "Using P for a committee",
     "C (order does not matter)"
    ],
    [
     "P(A or B) = P(A) + P(B) always",
     "subtract the overlap"
    ],
    [
     "P(at least one) by listing all cases",
     "1 − P(none)"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Conditional Probability",
   "kind": "example",
   "text": "⟨P(A \\mid B) = \\tfrac{P(A \\text{ and } B)}{P(B)}⟩",
   "example": "P(B) = 0.5, P(A and B) = 0.2",
   "steps": [
    [
     "Divide:",
     "⟨\\tfrac{0.2}{0.5}⟩"
    ]
   ],
   "answer": "0.4",
   "check": {
    "num": "0.2/0.5",
    "is": 0.4
   },
   "color": "purple"
  },
  {
   "title": "Independent Events",
   "kind": "example",
   "text": "A and B independent ⇔ P(A and B) = P(A)P(B).",
   "example": "P(A) = 0.3, P(B) = 0.6, P(A and B) = 0.18",
   "steps": [
    [
     "Check:",
     "0.3 · 0.6 = 0.18 ✓"
    ]
   ],
   "answer": "Independent",
   "check": {
    "true": "Math.abs(0.3*0.6-0.18)<1e-12"
   },
   "color": "blue"
  },
  {
   "title": "At Least One",
   "kind": "example",
   "text": "Use the complement.",
   "example": "P(at least one 6 in 3 rolls)",
   "steps": [
    [
     "Complement:",
     "⟨1 - (\\tfrac{5}{6})^3⟩"
    ]
   ],
   "answer": "⟨\\tfrac{91}{216}⟩ ≈ 0.421",
   "check": {
    "num": "1-(5/6)**3",
    "is": 0.4212962962962963
   },
   "color": "green"
  },
  {
   "title": "Binomial Probability",
   "kind": "example",
   "text": "⟨P(X = k) = {_nC_k}\\,p^k(1 - p)^{n - k}⟩",
   "example": "Exactly 2 heads in 5 fair flips",
   "steps": [
    [
     "Compute:",
     "⟨10 \\cdot (\\tfrac{1}{2})^5⟩"
    ]
   ],
   "answer": "⟨\\tfrac{10}{32} = \\tfrac{5}{16}⟩",
   "check": {
    "num": "10*0.5**5",
    "is": 0.3125
   },
   "color": "orange"
  },
  {
   "title": "Binomial Theorem",
   "kind": "example",
   "text": "Term k + 1 of ⟨(a + b)^n⟩: ⟨_nC_k\\,a^{n - k}b^k⟩",
   "example": "Coefficient of ⟨x^2⟩ in ⟨(x + 3)^4⟩",
   "steps": [
    [
     "k = 2:",
     "⟨_4C_2 \\cdot 3^2 = 6 \\cdot 9⟩"
    ]
   ],
   "answer": "54",
   "check": {
    "num": "6*9",
    "is": 54
   },
   "color": "pink"
  },
  {
   "title": "Expected Value",
   "kind": "example",
   "text": "E(X) = Σ x · P(x).",
   "example": "Win $10 with P = 0.2, lose $3 with P = 0.8.",
   "steps": [
    [
     "Compute:",
     "10(0.2) + (−3)(0.8)"
    ]
   ],
   "answer": "−$0.40 per play",
   "check": {
    "num": "10*0.2-3*0.8",
    "is": -0.4
   },
   "color": "teal"
  }
 ]
};
