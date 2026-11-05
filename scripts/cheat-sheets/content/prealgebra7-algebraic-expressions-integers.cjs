/* Pre-Algebra (7th) Unit 1 cheat sheet (Algebraic Expressions and Integers). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-algebraic-expressions-integers",
 "course": "Pre-Algebra (7th)",
 "unitNo": 1,
 "unitName": "Algebraic Expressions and Integers",
 "focus": "place value, variables, expressions and the order of operations",
 "morefocus": "integer operations, estimation, patterns and the coordinate plane",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "variable",
     "A letter that stands for a number.",
     "n in n + 7"
    ],
    [
     "algebraic expression",
     "Numbers, variables and operations, no equals sign.",
     "3x − 5"
    ],
    [
     "integer",
     "A whole number or its opposite.",
     "−8, 0, 15"
    ],
    [
     "absolute value",
     "Distance from 0.",
     "|−6| = 6"
    ],
    [
     "opposites",
     "Same distance from 0, opposite sides.",
     "7 and −7"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Order of Operations",
   "kind": "example",
   "text": "Grouping, exponents, multiply/divide left to right, add/subtract left to right.",
   "example": "⟨20 - 3 \\cdot 4 + 6 \\div 2⟩",
   "steps": [
    [
     "Multiply, divide:",
     "12 and 3"
    ],
    [
     "Left to right:",
     "20 − 12 + 3"
    ]
   ],
   "answer": "11",
   "check": {
    "num": "20-3*4+6/2",
    "is": 11
   },
   "color": "blue"
  },
  {
   "title": "Evaluating Expressions",
   "kind": "example",
   "text": "Substitute, then simplify in order.",
   "example": "Evaluate 4a − b for a = 3, b = −2.",
   "steps": [
    [
     "Substitute:",
     "4(3) − (−2) = 12 + 2"
    ]
   ],
   "answer": "14",
   "check": {
    "num": "4*3-(-2)",
    "is": 14
   },
   "color": "green"
  },
  {
   "title": "Words to Expressions",
   "kind": "words",
   "rows": [
    [
     "7 less than a number",
     "n − 7"
    ],
    [
     "the product of 5 and a number",
     "5n"
    ],
    [
     "a number divided by 3, plus 2",
     "⟨\\tfrac{n}{3} + 2⟩"
    ],
    [
     "twice the sum of x and 4",
     "2(x + 4)"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Rounding and Estimating",
   "kind": "table",
   "plain": true,
   "head": [
    "Problem",
    "Estimate"
   ],
   "rows": [
    [
     "4,872 rounded to the nearest hundred",
     "4,900"
    ],
    [
     "398 + 512",
     "400 + 500 = 900"
    ],
    [
     "61 × 19",
     "60 × 20 = 1,200"
    ]
   ],
   "after": "Look at the digit to the right of the place you round to: 5 or more rounds up.",
   "check": {
    "num": "60*20",
    "is": 1200
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Multiply and divide before adding and subtracting.",
    "A variable can stand for any number.",
    "Estimate first, then check your exact answer against it."
   ],
   "bad": [
    [
     "20 − 3 · 4 = 68",
     "multiply first: 8"
    ],
    [
     "|−6| = −6",
     "6"
    ],
    [
     "“7 less than n” = 7 − n",
     "n − 7"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Adding and Subtracting Integers",
   "kind": "table",
   "plain": true,
   "head": [
    "Rule",
    "Example"
   ],
   "rows": [
    [
     "Same signs: add, keep the sign",
     "−5 + (−3) = −8"
    ],
    [
     "Different signs: subtract, take the sign of the larger absolute value",
     "−9 + 4 = −5"
    ],
    [
     "Subtracting: add the opposite",
     "6 − (−2) = 6 + 2 = 8"
    ]
   ],
   "check": [
    {
     "num": "-5+(-3)",
     "is": -8
    },
    {
     "num": "-9+4",
     "is": -5
    },
    {
     "num": "6-(-2)",
     "is": 8
    }
   ],
   "color": "purple"
  },
  {
   "title": "Multiplying and Dividing Integers",
   "kind": "table",
   "plain": true,
   "head": [
    "Signs",
    "Result"
   ],
   "rows": [
    [
     "same signs",
     "positive: (−4)(−5) = 20"
    ],
    [
     "different signs",
     "negative: −24 ÷ 6 = −4"
    ],
    [
     "even number of negatives",
     "positive"
    ],
    [
     "odd number of negatives",
     "negative"
    ]
   ],
   "check": [
    {
     "num": "(-4)*(-5)",
     "is": 20
    },
    {
     "num": "-24/6",
     "is": -4
    }
   ],
   "color": "blue"
  },
  {
   "title": "Mixed Integer Problem",
   "kind": "example",
   "text": "Use the order of operations with integer rules.",
   "example": "⟨-3(4 - 9) + (-12) \\div 4⟩",
   "steps": [
    [
     "Parentheses:",
     "−3(−5) = 15"
    ],
    [
     "Divide:",
     "−12 ÷ 4 = −3"
    ]
   ],
   "answer": "12",
   "check": {
    "num": "-3*(4-9)+(-12)/4",
    "is": 12
   },
   "color": "green"
  },
  {
   "title": "Patterns and Inductive Reasoning",
   "kind": "example",
   "text": "Find the rule from the examples, then extend it.",
   "example": "Next two terms: 3, 7, 11, 15, …",
   "steps": [
    [
     "Rule:",
     "add 4"
    ]
   ],
   "answer": "19, 23",
   "check": [
    {
     "num": "15+4",
     "is": 19
    },
    {
     "num": "19+4",
     "is": 23
    }
   ],
   "color": "orange"
  },
  {
   "title": "The Coordinate Plane",
   "kind": "table",
   "plain": true,
   "head": [
    "Quadrant",
    "Signs"
   ],
   "rows": [
    [
     "I",
     "(+, +)"
    ],
    [
     "II",
     "(−, +)"
    ],
    [
     "III",
     "(−, −)"
    ],
    [
     "IV",
     "(+, −)"
    ]
   ],
   "after": "Start at the origin: move along x first, then y.",
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
