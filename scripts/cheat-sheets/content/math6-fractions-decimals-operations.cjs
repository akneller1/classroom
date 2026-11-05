/* 6th Grade Math Unit 2 cheat sheet (Operations of Fractions and Decimals). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "math6-fractions-decimals-operations",
 "course": "6th Grade Math",
 "unitNo": 2,
 "unitName": "Operations of Fractions and Decimals",
 "focus": "dividing fractions and mixed numbers",
 "morefocus": "multi-digit decimals, GCF, LCM and the distributive property",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "reciprocal",
     "Flip a fraction; the product is 1.",
     "⟨\\tfrac{3}{5}⟩ and ⟨\\tfrac{5}{3}⟩"
    ],
    [
     "quotient",
     "The answer to a division.",
     "12 ÷ 4 = 3"
    ],
    [
     "mixed number",
     "A whole number and a fraction.",
     "⟨2\\tfrac{1}{3}⟩"
    ],
    [
     "dividend / divisor",
     "In a ÷ b, a is the dividend, b the divisor.",
     "36 ÷ 4"
    ],
    [
     "improper fraction",
     "Numerator greater than or equal to the denominator.",
     "⟨\\tfrac{7}{3}⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Dividing Fractions",
   "kind": "example",
   "text": "Keep the first fraction, change ÷ to ×, flip the second.",
   "example": "⟨\\tfrac{3}{4} \\div \\tfrac{2}{5}⟩",
   "steps": [
    [
     "Flip and multiply:",
     "⟨\\tfrac{3}{4} \\times \\tfrac{5}{2} = \\tfrac{15}{8}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{15}{8} = 1\\tfrac{7}{8}⟩",
   "check": {
    "num": "(3/4)/(2/5)",
    "is": 1.875
   },
   "color": "blue"
  },
  {
   "title": "Whole Numbers and Fractions",
   "kind": "example",
   "text": "Write the whole number over 1 first.",
   "example": "⟨6 \\div \\tfrac{3}{4}⟩",
   "steps": [
    [
     "Rewrite:",
     "⟨\\tfrac{6}{1} \\times \\tfrac{4}{3} = \\tfrac{24}{3}⟩"
    ]
   ],
   "answer": "8",
   "check": {
    "num": "6/(3/4)",
    "is": 8
   },
   "color": "green"
  },
  {
   "title": "Mixed Numbers",
   "kind": "example",
   "text": "Change mixed numbers to improper fractions before dividing.",
   "example": "⟨2\\tfrac{1}{2} \\div 1\\tfrac{1}{4}⟩",
   "steps": [
    [
     "Improper:",
     "⟨\\tfrac{5}{2} \\div \\tfrac{5}{4}⟩"
    ],
    [
     "Flip:",
     "⟨\\tfrac{5}{2} \\times \\tfrac{4}{5} = 2⟩"
    ]
   ],
   "answer": "2",
   "check": {
    "num": "2.5/1.25",
    "is": 2
   },
   "color": "orange"
  },
  {
   "title": "Long Division",
   "kind": "example",
   "text": "Divide, multiply, subtract, bring down. Repeat.",
   "example": "1,428 ÷ 12",
   "steps": [
    [
     "12 into 14:",
     "1 R 2, bring down 2 → 22"
    ],
    [
     "Continue:",
     "22 → 1 R 10, 108 → 9"
    ]
   ],
   "answer": "119",
   "check": {
    "num": "1428/12",
    "is": 119
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Only flip the SECOND fraction.",
    "Dividing by a fraction less than 1 makes the answer bigger.",
    "Simplify before multiplying when you can."
   ],
   "bad": [
    [
     "Flipping the first fraction",
     "keep, change, flip the second"
    ],
    [
     "Dividing mixed numbers part by part",
     "convert to improper first"
    ],
    [
     "Forgetting to simplify",
     "⟨\\tfrac{8}{12} = \\tfrac{2}{3}⟩"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Adding and Subtracting Decimals",
   "kind": "example",
   "text": "Line up the decimal points; add zeros as placeholders.",
   "example": "23.5 − 7.28",
   "steps": [
    [
     "Line up:",
     "23.50 − 7.28"
    ]
   ],
   "answer": "16.22",
   "check": {
    "num": "23.5-7.28",
    "is": 16.22
   },
   "color": "purple"
  },
  {
   "title": "Multiplying Decimals",
   "kind": "example",
   "text": "Multiply as whole numbers, then count the decimal places in both factors.",
   "example": "3.4 × 0.25",
   "steps": [
    [
     "Whole numbers:",
     "34 × 25 = 850"
    ],
    [
     "3 decimal places:",
     "0.850"
    ]
   ],
   "answer": "0.85",
   "check": {
    "num": "3.4*0.25",
    "is": 0.85
   },
   "color": "blue"
  },
  {
   "title": "Dividing Decimals",
   "kind": "example",
   "text": "Move the decimal in the divisor to make it whole; move the dividend the same number of places.",
   "example": "7.56 ÷ 0.6",
   "steps": [
    [
     "Shift one place:",
     "75.6 ÷ 6"
    ]
   ],
   "answer": "12.6",
   "check": {
    "num": "7.56/0.6",
    "is": 12.6
   },
   "color": "green"
  },
  {
   "title": "GCF and LCM",
   "kind": "table",
   "plain": true,
   "head": [
    "Find",
    "Example: 12 and 18"
   ],
   "rows": [
    [
     "Factors of each",
     "12: 1, 2, 3, 4, 6, 12 · 18: 1, 2, 3, 6, 9, 18"
    ],
    [
     "GCF (greatest common factor)",
     "6"
    ],
    [
     "Multiples",
     "12, 24, 36 … · 18, 36 …"
    ],
    [
     "LCM (least common multiple)",
     "36"
    ]
   ],
   "after": "GCF: sharing equally. LCM: when things line up again.",
   "check": [
    {
     "num": "12*18/6",
     "is": 36
    }
   ],
   "color": "orange"
  },
  {
   "title": "The Distributive Property",
   "kind": "example",
   "text": "Use the GCF to factor a sum: a·b + a·c = a(b + c).",
   "example": "Write 24 + 36 as a product using the GCF.",
   "steps": [
    [
     "GCF of 24 and 36:",
     "12"
    ],
    [
     "Factor:",
     "12(2 + 3)"
    ]
   ],
   "answer": "12(2 + 3)",
   "check": {
    "num": "12*(2+3)",
    "is": 60
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I flip only the divisor?",
    "Did I line up the decimal points?",
    "Does my decimal answer have the right number of places?",
    "Is my GCF a factor of BOTH numbers?"
   ],
   "color": "teal"
  }
 ]
};
