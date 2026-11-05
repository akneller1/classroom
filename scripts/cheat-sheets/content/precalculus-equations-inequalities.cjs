/* Precalculus Unit 1 cheat sheet (Equations and Inequalities). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-equations-inequalities",
 "course": "Precalculus",
 "unitNo": 1,
 "unitName": "Equations and Inequalities",
 "focus": "linear, absolute value and quadratic equations",
 "morefocus": "polynomial, rational and radical equations and inequalities",
 "front": [
  {
   "title": "Linear Equations",
   "kind": "example",
   "text": "Distribute, collect variable terms, then isolate.",
   "example": "4(x − 3) = 2x + 10",
   "steps": [
    [
     "Distribute:",
     "4x − 12 = 2x + 10"
    ],
    [
     "Collect:",
     "2x = 22"
    ]
   ],
   "answer": "x = 11",
   "check": {
    "num": "4*(11-3)-(2*11+10)",
    "is": 0
   },
   "color": "purple"
  },
  {
   "title": "Absolute Value Equations",
   "kind": "example",
   "text": "Isolate the absolute value, then split into two cases.",
   "example": "|2x − 5| = 9",
   "steps": [
    [
     "Cases:",
     "2x − 5 = 9 or 2x − 5 = −9"
    ]
   ],
   "answer": "x = 7 or x = −2",
   "check": [
    {
     "num": "Math.abs(2*7-5)",
     "is": 9
    },
    {
     "num": "Math.abs(2*(-2)-5)",
     "is": 9
    }
   ],
   "color": "blue"
  },
  {
   "title": "Absolute Value Inequalities",
   "kind": "example",
   "text": "|u| < a → −a < u < a. |u| > a → u < −a or u > a.",
   "example": "|x + 1| ≤ 4",
   "steps": [
    [
     "Compound:",
     "−4 ≤ x + 1 ≤ 4"
    ]
   ],
   "answer": "−5 ≤ x ≤ 3",
   "check": {
    "true": "Math.abs(-5+1)<=4 && Math.abs(3+1)<=4 && Math.abs(3.1+1)>4"
   },
   "color": "green"
  },
  {
   "title": "Quadratic Formula",
   "kind": "example",
   "text": "⟨x = \\tfrac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}⟩",
   "example": "⟨2x^2 - 3x - 5 = 0⟩",
   "steps": [
    [
     "Discriminant:",
     "9 + 40 = 49"
    ],
    [
     "Roots:",
     "⟨\\tfrac{3 \\pm 7}{4}⟩"
    ]
   ],
   "answer": "⟨x = \\tfrac{5}{2}⟩ or x = −1",
   "check": [
    {
     "num": "2*2.5**2-3*2.5-5",
     "is": 0
    },
    {
     "num": "2*1+3-5",
     "is": 0
    }
   ],
   "color": "orange"
  },
  {
   "title": "The Discriminant",
   "kind": "table",
   "plain": true,
   "head": [
    "⟨b^2 - 4ac⟩",
    "Roots"
   ],
   "rows": [
    [
     "> 0",
     "two real"
    ],
    [
     "= 0",
     "one real (double)"
    ],
    [
     "< 0",
     "two complex conjugates"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Isolate |…| before splitting into cases.",
    "Set quadratics equal to 0 before factoring.",
    "Check solutions in the original equation."
   ],
   "bad": [
    [
     "|x − 3| = −2 has solutions",
     "no solution"
    ],
    [
     "|u| > a written as −a < u < a",
     "two separate rays"
    ],
    [
     "Dividing both sides by x",
     "factor instead: you lose x = 0"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Polynomial Equations",
   "kind": "example",
   "text": "Factor completely and use the zero-product property.",
   "example": "⟨x^3 - 4x^2 - 5x = 0⟩",
   "steps": [
    [
     "Factor:",
     "x(x − 5)(x + 1) = 0"
    ]
   ],
   "answer": "x = 0, 5, −1",
   "check": [
    {
     "num": "125-100-25",
     "is": 0
    },
    {
     "num": "-1-4+5",
     "is": 0
    }
   ],
   "color": "purple"
  },
  {
   "title": "Polynomial Inequalities",
   "kind": "example",
   "text": "Find zeros, test each interval with a sign chart.",
   "example": "⟨x^2 - x - 6 > 0⟩",
   "steps": [
    [
     "Zeros:",
     "(x − 3)(x + 2): −2 and 3"
    ],
    [
     "Signs:",
     "+ | − | +"
    ]
   ],
   "answer": "x < −2 or x > 3",
   "check": {
    "true": "(-3)**2+3-6>0 && !(0-0-6>0) && 16-4-6>0"
   },
   "color": "blue"
  },
  {
   "title": "Rational Equations",
   "kind": "example",
   "text": "Multiply by the LCD; reject values that make a denominator 0.",
   "example": "⟨\\tfrac{3}{x - 2} = \\tfrac{x}{x - 2} - 1⟩",
   "steps": [
    [
     "Multiply by x − 2:",
     "3 = x − (x − 2) = 2 ✗"
    ]
   ],
   "answer": "No solution",
   "check": {
    "true": "3 !== 2"
   },
   "color": "green"
  },
  {
   "title": "Rational Inequalities",
   "kind": "example",
   "text": "Critical points: zeros of the top AND bottom. The bottom’s zeros are never included.",
   "example": "⟨\\tfrac{x - 1}{x + 3} \\le 0⟩",
   "steps": [
    [
     "Critical:",
     "1 and −3"
    ],
    [
     "Signs:",
     "+ | − | +"
    ]
   ],
   "answer": "−3 < x ≤ 1",
   "check": {
    "true": "(0-1)/(0+3)<=0 && (1-1)/(1+3)<=0 && (-4-1)/(-4+3)>0"
   },
   "color": "orange"
  },
  {
   "title": "Radical Equations",
   "kind": "example",
   "text": "Isolate the radical, square both sides, CHECK for extraneous roots.",
   "example": "⟨\\sqrt{x + 7} = x + 1⟩",
   "steps": [
    [
     "Square:",
     "⟨x + 7 = x^2 + 2x + 1⟩"
    ],
    [
     "Factor:",
     "(x + 3)(x − 2) = 0"
    ]
   ],
   "answer": "x = 2 (x = −3 is extraneous)",
   "check": [
    {
     "num": "Math.sqrt(2+7)-(2+1)",
     "is": 0
    },
    {
     "true": "Math.sqrt(-3+7) !== -3+1"
    }
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I check every root in the original equation?",
    "Did I exclude zeros of the denominator?",
    "Did I test every interval on my sign chart?",
    "Did I flip the inequality when multiplying by a negative?"
   ],
   "color": "teal"
  }
 ]
};
