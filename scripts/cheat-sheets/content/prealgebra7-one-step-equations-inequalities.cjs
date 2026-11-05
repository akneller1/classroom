/* Pre-Algebra (7th) Unit 2 cheat sheet (Solving One-Step Equations and Inequalities). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-one-step-equations-inequalities",
 "course": "Pre-Algebra (7th)",
 "unitNo": 2,
 "unitName": "Solving One-Step Equations and Inequalities",
 "focus": "number properties, the distributive property and simplifying",
 "morefocus": "one-step equations and inequalities and their graphs",
 "front": [
  {
   "title": "Properties of Numbers",
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
     "(a + b) + c = a + (b + c)"
    ],
    [
     "Identity",
     "a + 0 = a, a · 1 = a"
    ],
    [
     "Zero property",
     "a · 0 = 0"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "The Distributive Property",
   "kind": "example",
   "text": "Multiply the outside number by EACH term inside.",
   "example": "−3(2x − 5)",
   "steps": [
    [
     "Distribute:",
     "−3 · 2x and −3 · (−5)"
    ]
   ],
   "answer": "−6x + 15",
   "check": {
    "expr": "-3*(2*x-5)",
    "is": "-6*x+15"
   },
   "color": "blue"
  },
  {
   "title": "Simplifying Expressions",
   "kind": "example",
   "text": "Combine like terms: same variable, same exponent.",
   "example": "5x + 8 − 2x + 3",
   "steps": [
    [
     "Group:",
     "(5x − 2x) + (8 + 3)"
    ]
   ],
   "answer": "3x + 11",
   "check": {
    "expr": "5*x+8-2*x+3",
    "is": "3*x+11"
   },
   "color": "green"
  },
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "like terms",
     "Same variable part.",
     "4y and −y"
    ],
    [
     "inverse operations",
     "Undo each other.",
     "+ and −, × and ÷"
    ],
    [
     "solution",
     "Makes the equation true.",
     "x = 4 for x + 3 = 7"
    ],
    [
     "inequality",
     "Compares with <, >, ≤, ≥.",
     "n ≥ 2"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Guess, Check, and Revise",
   "kind": "example",
   "text": "Make a guess, test it, and adjust up or down.",
   "example": "Two numbers add to 30 and one is 6 more than the other.",
   "steps": [
    [
     "Try 10 and 20:",
     "difference 10, too big"
    ],
    [
     "Try 12 and 18:",
     "difference 6 ✓"
    ]
   ],
   "answer": "12 and 18",
   "check": {
    "true": "12+18===30 && 18-12===6"
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Distribute to every term in the parentheses.",
    "Only combine like terms.",
    "Keep the sign in front of each term."
   ],
   "bad": [
    [
     "−3(2x − 5) = −6x − 15",
     "+15 (negative × negative)"
    ],
    [
     "5x + 3 = 8x",
     "not like terms"
    ],
    [
     "Dropping a negative sign",
     "circle each sign first"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Adding or Subtracting to Solve",
   "kind": "example",
   "text": "Use the inverse operation on both sides.",
   "example": "x − 14 = −6",
   "steps": [
    [
     "Add 14:",
     "x = −6 + 14"
    ]
   ],
   "answer": "x = 8",
   "check": {
    "num": "-6+14",
    "is": 8
   },
   "color": "purple"
  },
  {
   "title": "Multiplying or Dividing to Solve",
   "kind": "example",
   "text": "Divide (or multiply) both sides.",
   "example": "⟨\\tfrac{y}{-4} = 7⟩",
   "steps": [
    [
     "Multiply by −4:",
     "y = 7(−4)"
    ]
   ],
   "answer": "y = −28",
   "check": {
    "num": "7*(-4)",
    "is": -28
   },
   "color": "blue"
  },
  {
   "title": "Graphing Inequalities",
   "kind": "words",
   "rows": [
    [
     "x > −2",
     "open circle at −2, shade right"
    ],
    [
     "x ≤ 5",
     "closed circle at 5, shade left"
    ],
    [
     "n ≥ 0",
     "closed circle at 0, shade right"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Inequalities by Adding or Subtracting",
   "kind": "example",
   "text": "Solve like an equation; the sign does not change.",
   "example": "n + 9 ≤ 4",
   "steps": [
    [
     "Subtract 9:",
     "n ≤ −5"
    ]
   ],
   "answer": "n ≤ −5",
   "check": {
    "true": "-5+9 <= 4 && !(-4.9+9 <= 4)"
   },
   "color": "orange"
  },
  {
   "title": "Inequalities by Multiplying or Dividing",
   "kind": "example",
   "text": "Dividing or multiplying by a NEGATIVE flips the inequality sign.",
   "example": "−3x < 12",
   "steps": [
    [
     "Divide by −3 and flip:",
     "x > −4"
    ]
   ],
   "answer": "x > −4",
   "check": {
    "true": "-3*(-3.9) < 12 && !(-3*(-4) < 12)"
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
