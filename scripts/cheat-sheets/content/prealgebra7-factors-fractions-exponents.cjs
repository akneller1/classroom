/* Pre-Algebra (7th) Unit 4 cheat sheet (Factors, Fractions, and Exponents). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-factors-fractions-exponents",
 "course": "Pre-Algebra (7th)",
 "unitNo": 4,
 "unitName": "Factors, Fractions, and Exponents",
 "focus": "divisibility, prime factorization, GCF and simplifying fractions",
 "morefocus": "rational and irrational numbers, exponent rules, scientific notation and cube roots",
 "front": [
  {
   "title": "Divisibility Rules",
   "kind": "table",
   "plain": true,
   "head": [
    "Divisible by",
    "If …"
   ],
   "rows": [
    [
     "2",
     "the last digit is even"
    ],
    [
     "3",
     "the digit sum is divisible by 3"
    ],
    [
     "5",
     "the last digit is 0 or 5"
    ],
    [
     "9",
     "the digit sum is divisible by 9"
    ],
    [
     "10",
     "the last digit is 0"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Prime Factorization",
   "kind": "example",
   "text": "Use a factor tree until every branch ends in a prime.",
   "example": "Prime factorization of 72",
   "steps": [
    [
     "Tree:",
     "72 = 8 · 9 = 2 · 2 · 2 · 3 · 3"
    ]
   ],
   "answer": "⟨2^3 \\cdot 3^2⟩",
   "check": {
    "num": "2**3*3**2",
    "is": 72
   },
   "color": "blue"
  },
  {
   "title": "Greatest Common Factor",
   "kind": "example",
   "text": "Multiply the primes the numbers share.",
   "example": "GCF of 36 and 60",
   "steps": [
    [
     "Primes:",
     "⟨36 = 2^2 \\cdot 3^2⟩, ⟨60 = 2^2 \\cdot 3 \\cdot 5⟩"
    ],
    [
     "Shared:",
     "⟨2^2 \\cdot 3⟩"
    ]
   ],
   "answer": "12",
   "check": {
    "num": "2**2*3",
    "is": 12
   },
   "color": "green"
  },
  {
   "title": "Simplifying Fractions",
   "kind": "example",
   "text": "Divide the numerator and denominator by their GCF.",
   "example": "Simplify ⟨\\tfrac{36}{60}⟩.",
   "steps": [
    [
     "Divide by 12:",
     "⟨\\tfrac{3}{5}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{3}{5}⟩",
   "check": {
    "num": "36/60",
    "is": 0.6
   },
   "color": "orange"
  },
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "prime",
     "Exactly two factors: 1 and itself.",
     "2, 3, 5, 7, 11"
    ],
    [
     "composite",
     "More than two factors.",
     "4, 9, 12"
    ],
    [
     "rational",
     "Can be written as a fraction of integers.",
     "⟨-\\tfrac{2}{3}⟩, 0.25"
    ],
    [
     "irrational",
     "Non-ending, non-repeating decimal.",
     "⟨\\sqrt{2}⟩, π"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "1 is neither prime nor composite.",
    "Use exponents to group repeated prime factors.",
    "⟨\\sqrt{n}⟩ is irrational unless n is a perfect square."
   ],
   "bad": [
    [
     "Calling 51 prime",
     "51 = 3 · 17"
    ],
    [
     "GCF = product of all primes",
     "only the shared ones"
    ],
    [
     "Writing ⟨\\tfrac{36}{60} = \\tfrac{6}{10}⟩ as final",
     "keep dividing: ⟨\\tfrac{3}{5}⟩"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Exponent Rules",
   "kind": "table",
   "plain": true,
   "head": [
    "Rule",
    "Example"
   ],
   "rows": [
    [
     "⟨a^m \\cdot a^n = a^{m+n}⟩",
     "⟨x^3 \\cdot x^4 = x^7⟩"
    ],
    [
     "⟨\\tfrac{a^m}{a^n} = a^{m-n}⟩",
     "⟨\\tfrac{5^6}{5^2} = 5^4⟩"
    ],
    [
     "⟨a^0 = 1⟩",
     "⟨9^0 = 1⟩"
    ],
    [
     "⟨a^{-n} = \\tfrac{1}{a^n}⟩",
     "⟨2^{-3} = \\tfrac{1}{8}⟩"
    ]
   ],
   "check": [
    {
     "num": "5**6/5**2",
     "is": 625
    },
    {
     "num": "2**-3",
     "is": 0.125
    }
   ],
   "color": "purple"
  },
  {
   "title": "Exponents and Multiplication",
   "kind": "example",
   "text": "Multiply coefficients and add exponents of the same base.",
   "example": "⟨(3x^2)(4x^5)⟩",
   "steps": [
    [
     "Coefficients:",
     "3 · 4 = 12"
    ],
    [
     "Exponents:",
     "2 + 5 = 7"
    ]
   ],
   "answer": "⟨12x^7⟩",
   "check": {
    "expr": "(3*x**2)*(4*x**5)",
    "is": "12*x**7"
   },
   "color": "blue"
  },
  {
   "title": "Exponents and Division",
   "kind": "example",
   "text": "Divide coefficients and subtract exponents.",
   "example": "⟨\\tfrac{18y^9}{6y^3}⟩",
   "steps": [
    [
     "Divide:",
     "18 ÷ 6 = 3"
    ],
    [
     "Subtract:",
     "9 − 3 = 6"
    ]
   ],
   "answer": "⟨3y^6⟩",
   "check": {
    "expr": "18*y**9/(6*y**3)",
    "is": "3*y**6"
   },
   "color": "green"
  },
  {
   "title": "Scientific Notation",
   "kind": "table",
   "plain": true,
   "head": [
    "Standard form",
    "Scientific notation"
   ],
   "rows": [
    [
     "5,600,000",
     "⟨5.6 \\times 10^6⟩"
    ],
    [
     "0.00043",
     "⟨4.3 \\times 10^{-4}⟩"
    ],
    [
     "72,000",
     "⟨7.2 \\times 10^4⟩"
    ]
   ],
   "after": "⟨a \\times 10^n⟩ with ⟨1 \\le a < 10⟩.",
   "check": [
    {
     "num": "5.6e6",
     "is": 5600000
    },
    {
     "num": "4.3e-4",
     "is": 0.00043
    }
   ],
   "color": "orange"
  },
  {
   "title": "Cube Roots",
   "kind": "table",
   "plain": true,
   "head": [
    "Find",
    "Answer"
   ],
   "rows": [
    [
     "⟨\\sqrt[3]{64}⟩",
     "4"
    ],
    [
     "⟨\\sqrt[3]{-125}⟩",
     "−5"
    ],
    [
     "⟨x^3 = 27⟩",
     "x = 3"
    ],
    [
     "⟨\\sqrt[3]{\\tfrac{8}{27}}⟩",
     "⟨\\tfrac{2}{3}⟩"
    ]
   ],
   "after": "A negative number has a negative cube root.",
   "check": [
    {
     "num": "Math.cbrt(64)",
     "is": 4
    },
    {
     "num": "Math.cbrt(-125)",
     "is": -5
    }
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I follow the order of operations?",
    "Did I do the same thing to both sides?",
    "Did I check my answer in the original problem?",
    "Does my answer have the right sign and units?"
   ],
   "color": "teal"
  }
 ]
};
