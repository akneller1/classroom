/* Pre-Algebra (7th) Unit 5 cheat sheet (Operations with Fractions). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-operations-fractions",
 "course": "Pre-Algebra (7th)",
 "unitNo": 5,
 "unitName": "Operations with Fractions",
 "focus": "comparing rational numbers, fractions and decimals, the four operations",
 "morefocus": "customary units, fraction equations and powers of quotients",
 "front": [
  {
   "title": "Comparing and Ordering",
   "kind": "example",
   "text": "Use a common denominator or change to decimals.",
   "example": "Order ⟨\\tfrac{2}{3},\\ 0.6,\\ \\tfrac{5}{8}⟩ from least to greatest.",
   "steps": [
    [
     "Decimals:",
     "⟨0.\\overline{6}⟩, 0.6, 0.625"
    ]
   ],
   "answer": "⟨0.6,\\ \\tfrac{5}{8},\\ \\tfrac{2}{3}⟩",
   "check": {
    "true": "0.6 < 5/8 && 5/8 < 2/3"
   },
   "color": "purple"
  },
  {
   "title": "Fractions and Decimals",
   "kind": "table",
   "plain": true,
   "head": [
    "Fraction",
    "Decimal"
   ],
   "rows": [
    [
     "⟨\\tfrac{3}{8}⟩",
     "0.375 (terminating)"
    ],
    [
     "⟨\\tfrac{2}{9}⟩",
     "⟨0.\\overline{2}⟩ (repeating)"
    ],
    [
     "⟨\\tfrac{7}{20}⟩",
     "0.35"
    ]
   ],
   "after": "Fraction → decimal: divide the numerator by the denominator.",
   "check": [
    {
     "num": "3/8",
     "is": 0.375
    },
    {
     "num": "7/20",
     "is": 0.35
    }
   ],
   "color": "blue"
  },
  {
   "title": "Adding and Subtracting Fractions",
   "kind": "example",
   "text": "Use a common denominator; add or subtract numerators only.",
   "example": "⟨\\tfrac{5}{6} - \\tfrac{3}{8}⟩",
   "steps": [
    [
     "LCD 24:",
     "⟨\\tfrac{20}{24} - \\tfrac{9}{24}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{11}{24}⟩",
   "check": {
    "num": "5/6-3/8",
    "is": 0.4583333333333333
   },
   "color": "green"
  },
  {
   "title": "Mixed Numbers",
   "kind": "example",
   "text": "Rename as improper fractions (or regroup), then add or subtract.",
   "example": "⟨3\\tfrac{1}{4} - 1\\tfrac{2}{3}⟩",
   "steps": [
    [
     "Improper:",
     "⟨\\tfrac{13}{4} - \\tfrac{5}{3} = \\tfrac{39}{12} - \\tfrac{20}{12}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{19}{12} = 1\\tfrac{7}{12}⟩",
   "check": {
    "num": "13/4-5/3",
    "is": 1.5833333333333333
   },
   "color": "orange"
  },
  {
   "title": "Multiplying and Dividing",
   "kind": "example",
   "text": "Multiply straight across. To divide, multiply by the reciprocal.",
   "example": "⟨-\\tfrac{4}{5} \\div \\tfrac{2}{3}⟩",
   "steps": [
    [
     "Reciprocal:",
     "⟨-\\tfrac{4}{5} \\cdot \\tfrac{3}{2} = -\\tfrac{12}{10}⟩"
    ]
   ],
   "answer": "⟨-\\tfrac{6}{5}⟩",
   "check": {
    "num": "(-4/5)/(2/3)",
    "is": -1.2
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Add numerators only; keep the common denominator.",
    "Simplify your final answer.",
    "Signs follow the integer rules."
   ],
   "bad": [
    [
     "⟨\\tfrac{1}{2} + \\tfrac{1}{3} = \\tfrac{2}{5}⟩",
     "common denominator: ⟨\\tfrac{5}{6}⟩"
    ],
    [
     "Flipping the first fraction to divide",
     "flip the divisor"
    ],
    [
     "Multiplying mixed numbers part by part",
     "convert first"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Customary Units",
   "kind": "table",
   "plain": true,
   "head": [
    "Unit",
    "Equivalent"
   ],
   "rows": [
    [
     "1 ft",
     "12 in"
    ],
    [
     "1 yd",
     "3 ft"
    ],
    [
     "1 mi",
     "5,280 ft"
    ],
    [
     "1 lb",
     "16 oz"
    ],
    [
     "1 gal",
     "4 qt = 8 pt = 16 c"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Converting Customary Units",
   "kind": "example",
   "text": "Multiply by a conversion fraction so units cancel.",
   "example": "Convert ⟨2\\tfrac{1}{2}⟩ gallons to quarts.",
   "steps": [
    [
     "Multiply:",
     "⟨\\tfrac{5}{2} \\times 4⟩"
    ]
   ],
   "answer": "10 quarts",
   "check": {
    "num": "2.5*4",
    "is": 10
   },
   "color": "blue"
  },
  {
   "title": "Adding or Subtracting Fractions to Solve",
   "kind": "example",
   "text": "Use the inverse operation; find common denominators.",
   "example": "⟨x + \\tfrac{2}{3} = \\tfrac{5}{6}⟩",
   "steps": [
    [
     "Subtract:",
     "⟨\\tfrac{5}{6} - \\tfrac{4}{6}⟩"
    ]
   ],
   "answer": "⟨x = \\tfrac{1}{6}⟩",
   "check": {
    "num": "5/6-2/3",
    "is": 0.16666666666666666
   },
   "color": "green"
  },
  {
   "title": "Multiplying Fractions to Solve",
   "kind": "example",
   "text": "Multiply both sides by the reciprocal of the coefficient.",
   "example": "⟨\\tfrac{3}{4}y = 12⟩",
   "steps": [
    [
     "Multiply by ⟨\\tfrac{4}{3}⟩:",
     "⟨y = 12 \\cdot \\tfrac{4}{3}⟩"
    ]
   ],
   "answer": "y = 16",
   "check": {
    "num": "12*4/3",
    "is": 16
   },
   "color": "orange"
  },
  {
   "title": "Powers of Products and Quotients",
   "kind": "table",
   "plain": true,
   "head": [
    "Rule",
    "Example"
   ],
   "rows": [
    [
     "⟨(ab)^n = a^n b^n⟩",
     "⟨(2x)^3 = 8x^3⟩"
    ],
    [
     "⟨(\\tfrac{a}{b})^n = \\tfrac{a^n}{b^n}⟩",
     "⟨(\\tfrac{2}{3})^2 = \\tfrac{4}{9}⟩"
    ],
    [
     "⟨(a^m)^n = a^{mn}⟩",
     "⟨(x^2)^4 = x^8⟩"
    ]
   ],
   "check": {
    "num": "(2/3)**2",
    "is": 0.4444444444444444
   },
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
