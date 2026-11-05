/* 6th Grade Math Unit 5 cheat sheet (Inequalities). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "math6-inequalities",
 "course": "6th Grade Math",
 "unitNo": 5,
 "unitName": "Inequalities",
 "focus": "inequality symbols, solutions and graphs",
 "morefocus": "solving one-step inequalities and applications",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "inequality",
     "Compares two values with <, >, ≤, ≥.",
     "x > 4"
    ],
    [
     "solution",
     "A value that makes it true.",
     "6 is a solution of x > 4"
    ],
    [
     "solution set",
     "All values that make it true.",
     "every number greater than 4"
    ],
    [
     "open circle",
     "Endpoint not included (< or >).",
     "x < 2"
    ],
    [
     "closed circle",
     "Endpoint included (≤ or ≥).",
     "x ≥ −1"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Symbols in Words",
   "kind": "table",
   "plain": true,
   "head": [
    "Words",
    "Symbol"
   ],
   "rows": [
    [
     "at least, no less than",
     "≥"
    ],
    [
     "at most, no more than",
     "≤"
    ],
    [
     "more than, exceeds",
     ">"
    ],
    [
     "fewer than, below",
     "<"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Testing Solutions",
   "kind": "example",
   "text": "Substitute; if the statement is true, the value is a solution.",
   "example": "Is 7 a solution of 3x − 5 ≥ 16?",
   "steps": [
    [
     "Substitute:",
     "3(7) − 5 = 16"
    ],
    [
     "Check:",
     "16 ≥ 16 is true"
    ]
   ],
   "answer": "Yes",
   "check": {
    "true": "3*7-5 >= 16"
   },
   "color": "green"
  },
  {
   "title": "Graphing on a Number Line",
   "kind": "words",
   "rows": [
    [
     "x > 3",
     "open circle at 3, arrow right"
    ],
    [
     "x ≤ −2",
     "closed circle at −2, arrow left"
    ],
    [
     "y ≥ 0",
     "closed circle at 0, arrow right"
    ],
    [
     "n < 5",
     "open circle at 5, arrow left"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Writing Inequalities from Graphs",
   "kind": "words",
   "rows": [
    [
     "Closed circle at 4, arrow left",
     "x ≤ 4"
    ],
    [
     "Open circle at −1, arrow right",
     "x > −1"
    ],
    [
     "Open circle at 0, arrow left",
     "x < 0"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "The arrow points the way the solutions go.",
    "Many values can be solutions.",
    "Check one value from your graph."
   ],
   "bad": [
    [
     "Closed circle for <",
     "use an open circle"
    ],
    [
     "“At least 10” as x < 10",
     "x ≥ 10"
    ],
    [
     "Only listing one solution",
     "describe all of them"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Solving by Adding or Subtracting",
   "kind": "example",
   "text": "Undo with the inverse operation on both sides.",
   "example": "x + 8 < 15",
   "steps": [
    [
     "Subtract 8:",
     "x < 7"
    ]
   ],
   "answer": "x < 7",
   "check": {
    "true": "6+8 < 15 && !(7+8 < 15)"
   },
   "color": "purple"
  },
  {
   "title": "Solving by Multiplying or Dividing",
   "kind": "example",
   "text": "Divide or multiply both sides by a positive number.",
   "example": "4n ≥ 36",
   "steps": [
    [
     "Divide by 4:",
     "n ≥ 9"
    ]
   ],
   "answer": "n ≥ 9",
   "check": {
    "true": "4*9 >= 36 && !(4*8.9 >= 36)"
   },
   "color": "blue"
  },
  {
   "title": "Fractions in Inequalities",
   "kind": "example",
   "text": "Multiply both sides by the denominator.",
   "example": "⟨\\tfrac{y}{3} \\le 5⟩",
   "steps": [
    [
     "Multiply by 3:",
     "y ≤ 15"
    ]
   ],
   "answer": "y ≤ 15",
   "check": {
    "true": "15/3 <= 5 && !(15.1/3 <= 5)"
   },
   "color": "green"
  },
  {
   "title": "Applications",
   "kind": "example",
   "text": "Write the inequality from the words, then solve.",
   "example": "You have $40 and tickets cost $6 each. How many can you buy?",
   "steps": [
    [
     "Inequality:",
     "6t ≤ 40"
    ],
    [
     "Divide:",
     "⟨t \\le 6.\\overline{6}⟩"
    ]
   ],
   "answer": "at most 6 tickets",
   "check": {
    "true": "6*6 <= 40 && 6*7 > 40"
   },
   "color": "orange"
  },
  {
   "title": "Whole-Number Answers",
   "kind": "table",
   "plain": true,
   "head": [
    "Context",
    "Round"
   ],
   "rows": [
    [
     "Tickets, people, buses",
     "Whole numbers only"
    ],
    [
     "“At most” money left",
     "Round down"
    ],
    [
     "“At least” buses needed",
     "Round up"
    ]
   ],
   "after": "Always reread the question to decide.",
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I pick the right symbol for the words?",
    "Open or closed circle?",
    "Does a number from my graph make the inequality true?",
    "Does my answer make sense in the story?"
   ],
   "color": "teal"
  }
 ]
};
