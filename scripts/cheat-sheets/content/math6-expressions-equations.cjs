/* 6th Grade Math Unit 4 cheat sheet (Expressions and Equations). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "math6-expressions-equations",
 "course": "6th Grade Math",
 "unitNo": 4,
 "unitName": "Expressions and Equations",
 "focus": "exponents, the order of operations and algebraic expressions",
 "morefocus": "equivalent expressions, one-step equations and variables",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "exponent",
     "How many times the base is a factor.",
     "⟨2^3 = 2 \\cdot 2 \\cdot 2⟩"
    ],
    [
     "variable",
     "A letter for an unknown number.",
     "n"
    ],
    [
     "coefficient",
     "The number multiplied by a variable.",
     "7 in 7x"
    ],
    [
     "term",
     "Parts of an expression separated by + or −.",
     "3x and 5 in 3x + 5"
    ],
    [
     "equation",
     "A statement that two expressions are equal.",
     "x + 4 = 11"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Exponents",
   "kind": "example",
   "text": "Multiply the base by itself, exponent times.",
   "example": "Evaluate ⟨4^3⟩ and ⟨(\\tfrac{1}{2})^2⟩.",
   "steps": [
    [
     "Expand:",
     "4 · 4 · 4 and ⟨\\tfrac{1}{2} \\cdot \\tfrac{1}{2}⟩"
    ]
   ],
   "answer": "64 and ⟨\\tfrac{1}{4}⟩",
   "check": [
    {
     "num": "4**3",
     "is": 64
    },
    {
     "num": "0.5**2",
     "is": 0.25
    }
   ],
   "color": "blue"
  },
  {
   "title": "Order of Operations",
   "kind": "example",
   "text": "Parentheses, Exponents, Multiply/Divide left to right, Add/Subtract left to right.",
   "example": "⟨18 - 2 \\cdot (1 + 2)^2⟩",
   "steps": [
    [
     "Parentheses:",
     "⟨(3)^2 = 9⟩"
    ],
    [
     "Multiply:",
     "2 · 9 = 18"
    ],
    [
     "Subtract:",
     "18 − 18"
    ]
   ],
   "answer": "0",
   "check": {
    "num": "18-2*(1+2)**2",
    "is": 0
   },
   "color": "green"
  },
  {
   "title": "Words to Expressions",
   "kind": "words",
   "rows": [
    [
     "5 more than a number",
     "n + 5"
    ],
    [
     "twice a number, decreased by 3",
     "2n − 3"
    ],
    [
     "the quotient of a number and 4",
     "⟨\\tfrac{n}{4}⟩"
    ],
    [
     "8 less than y",
     "y − 8"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Evaluating Expressions",
   "kind": "example",
   "text": "Substitute the value, then use the order of operations.",
   "example": "Evaluate ⟨3x^2 - 4⟩ for x = 5.",
   "steps": [
    [
     "Substitute:",
     "⟨3(5)^2 - 4 = 3 \\cdot 25 - 4⟩"
    ]
   ],
   "answer": "71",
   "check": {
    "num": "3*5**2-4",
    "is": 71
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "3x means 3 times x.",
    "Exponents come before multiplying.",
    "“Less than” reverses the order: 8 less than y is y − 8."
   ],
   "bad": [
    [
     "⟨2^3 = 6⟩",
     "it is 2 · 2 · 2 = 8"
    ],
    [
     "Adding before multiplying",
     "multiply first"
    ],
    [
     "8 less than y = 8 − y",
     "y − 8"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Equivalent Expressions",
   "kind": "example",
   "text": "Use the distributive property and combine like terms.",
   "example": "Simplify 4(x + 3) + 2x.",
   "steps": [
    [
     "Distribute:",
     "4x + 12 + 2x"
    ],
    [
     "Combine:",
     "6x + 12"
    ]
   ],
   "answer": "6x + 12",
   "check": {
    "expr": "4*(x+3)+2*x",
    "is": "6*x+12"
   },
   "color": "purple"
  },
  {
   "title": "Properties",
   "kind": "table",
   "plain": true,
   "head": [
    "Property",
    "Example"
   ],
   "rows": [
    [
     "Commutative",
     "a + b = b + a"
    ],
    [
     "Associative",
     "(ab)c = a(bc)"
    ],
    [
     "Distributive",
     "a(b + c) = ab + ac"
    ],
    [
     "Identity",
     "a + 0 = a, a · 1 = a"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Solving One-Step Equations",
   "kind": "example",
   "text": "Undo the operation with its inverse. Do the same to both sides.",
   "example": "x + 9 = 23",
   "steps": [
    [
     "Subtract 9:",
     "x = 23 − 9"
    ]
   ],
   "answer": "x = 14",
   "check": {
    "num": "23-9",
    "is": 14
   },
   "color": "green"
  },
  {
   "title": "Multiplication Equations",
   "kind": "example",
   "text": "Divide both sides by the coefficient.",
   "example": "6m = 42",
   "steps": [
    [
     "Divide by 6:",
     "⟨m = \\tfrac{42}{6}⟩"
    ]
   ],
   "answer": "m = 7",
   "check": {
    "num": "42/6",
    "is": 7
   },
   "color": "orange"
  },
  {
   "title": "Independent and Dependent Variables",
   "kind": "table",
   "plain": true,
   "head": [
    "Situation",
    "Independent → dependent"
   ],
   "rows": [
    [
     "Hours worked → pay",
     "h → p"
    ],
    [
     "Gallons bought → cost",
     "g → c"
    ],
    [
     "Minutes running → distance",
     "m → d"
    ]
   ],
   "after": "Rule example: p = 15h (pay depends on hours).",
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I use PEMDAS in order?",
    "Did I do the same thing to both sides?",
    "Did I check by substituting my answer?",
    "Did I combine only like terms?"
   ],
   "color": "teal"
  }
 ]
};
