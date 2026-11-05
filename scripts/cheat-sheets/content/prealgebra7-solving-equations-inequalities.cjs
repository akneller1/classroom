/* Pre-Algebra (7th) Unit 7 cheat sheet (Solving Equations and Inequalities). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-solving-equations-inequalities",
 "course": "Pre-Algebra (7th)",
 "unitNo": 7,
 "unitName": "Solving Equations and Inequalities",
 "focus": "two-step and multi-step equations, fractions and decimals",
 "morefocus": "variables on both sides, two-step inequalities, formulas and interest",
 "front": [
  {
   "title": "Two-Step Equations",
   "kind": "example",
   "text": "Undo addition or subtraction first, then multiplication or division.",
   "example": "5x − 7 = 18",
   "steps": [
    [
     "Add 7:",
     "5x = 25"
    ],
    [
     "Divide by 5:",
     "x = 5"
    ]
   ],
   "answer": "x = 5",
   "check": {
    "num": "(18+7)/5",
    "is": 5
   },
   "color": "purple"
  },
  {
   "title": "Multi-Step Equations",
   "kind": "example",
   "text": "Distribute, combine like terms, then solve.",
   "example": "3(x + 4) − x = 20",
   "steps": [
    [
     "Distribute:",
     "3x + 12 − x = 20"
    ],
    [
     "Combine:",
     "2x + 12 = 20"
    ]
   ],
   "answer": "x = 4",
   "check": {
    "num": "(20-12)/2",
    "is": 4
   },
   "color": "blue"
  },
  {
   "title": "Equations with Fractions",
   "kind": "example",
   "text": "Multiply every term by the LCD to clear fractions.",
   "example": "⟨\\tfrac{x}{3} + \\tfrac{1}{2} = \\tfrac{7}{6}⟩",
   "steps": [
    [
     "Multiply by 6:",
     "2x + 3 = 7"
    ]
   ],
   "answer": "x = 2",
   "check": {
    "num": "2/3+1/2",
    "is": 1.1666666666666667
   },
   "color": "green"
  },
  {
   "title": "Equations with Decimals",
   "kind": "example",
   "text": "Multiply by 10 or 100 to clear decimals, or solve directly.",
   "example": "0.4x + 1.2 = 3.6",
   "steps": [
    [
     "Subtract 1.2:",
     "0.4x = 2.4"
    ]
   ],
   "answer": "x = 6",
   "check": {
    "num": "(3.6-1.2)/0.4",
    "is": 6
   },
   "color": "orange"
  },
  {
   "title": "Write an Equation",
   "kind": "example",
   "text": "Define a variable, translate the words, solve.",
   "example": "A gym charges $25 to join and $15 a month. Total $160. How many months?",
   "steps": [
    [
     "Equation:",
     "25 + 15m = 160"
    ]
   ],
   "answer": "9 months",
   "check": {
    "num": "(160-25)/15",
    "is": 9
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Undo operations in reverse order.",
    "Distribute to every term.",
    "Multiply EVERY term by the LCD."
   ],
   "bad": [
    [
     "5x − 7 = 18 → 5x = 11",
     "add 7: 25"
    ],
    [
     "3(x + 4) = 3x + 4",
     "3x + 12"
    ],
    [
     "Clearing only one fraction",
     "multiply every term"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Variables on Both Sides",
   "kind": "example",
   "text": "Collect variable terms on one side first.",
   "example": "7x + 3 = 2x + 28",
   "steps": [
    [
     "Subtract 2x:",
     "5x + 3 = 28"
    ],
    [
     "Solve:",
     "5x = 25"
    ]
   ],
   "answer": "x = 5",
   "check": {
    "num": "(28-3)/5",
    "is": 5
   },
   "color": "purple"
  },
  {
   "title": "Two-Step Inequalities",
   "kind": "example",
   "text": "Solve like an equation; flip the sign if you multiply or divide by a negative.",
   "example": "−2x + 5 > 13",
   "steps": [
    [
     "Subtract 5:",
     "−2x > 8"
    ],
    [
     "Divide by −2, flip:",
     "x < −4"
    ]
   ],
   "answer": "x < −4",
   "check": {
    "true": "-2*(-4.1)+5 > 13 && !(-2*(-4)+5 > 13)"
   },
   "color": "blue"
  },
  {
   "title": "Transforming Formulas",
   "kind": "example",
   "text": "Solve for the requested variable using inverse operations.",
   "example": "Solve P = 2l + 2w for w.",
   "steps": [
    [
     "Subtract 2l:",
     "P − 2l = 2w"
    ]
   ],
   "answer": "⟨w = \\tfrac{P - 2l}{2}⟩",
   "check": {
    "expr": "(20-2*x)/2",
    "is": "10-x"
   },
   "color": "green"
  },
  {
   "title": "Simple Interest",
   "kind": "example",
   "text": "I = Prt (r as a decimal, t in years).",
   "example": "$800 at 4% for 3 years",
   "steps": [
    [
     "Multiply:",
     "800 × 0.04 × 3"
    ]
   ],
   "answer": "$96",
   "check": {
    "num": "800*0.04*3",
    "is": 96
   },
   "color": "orange"
  },
  {
   "title": "Compound Interest",
   "kind": "example",
   "text": "⟨B = P(1 + r)^t⟩ when interest is added yearly.",
   "example": "$1,000 at 5% for 2 years",
   "steps": [
    [
     "Compute:",
     "⟨1000(1.05)^2⟩"
    ]
   ],
   "answer": "$1,102.50",
   "check": {
    "num": "1000*1.05**2",
    "is": 1102.5
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I check by substituting my solution?",
    "Did I flip the sign for a negative divisor?",
    "Did I convert the percent to a decimal?",
    "Did I collect variables on one side first?"
   ],
   "color": "teal"
  }
 ]
};
