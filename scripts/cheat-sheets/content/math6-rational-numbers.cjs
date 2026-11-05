/* 6th Grade Math Unit 3 cheat sheet (Rational Numbers). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "math6-rational-numbers",
 "course": "6th Grade Math",
 "unitNo": 3,
 "unitName": "Rational Numbers",
 "focus": "positive and negative numbers, the number line, comparing and ordering",
 "morefocus": "absolute value and the coordinate plane",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "integer",
     "A whole number or its opposite.",
     "−4, 0, 7"
    ],
    [
     "opposites",
     "Same distance from 0, opposite sides.",
     "5 and −5"
    ],
    [
     "rational number",
     "Can be written as a fraction of integers.",
     "⟨-\\tfrac{3}{4}⟩, 0.5, −2"
    ],
    [
     "absolute value",
     "Distance from 0 (never negative).",
     "|−8| = 8"
    ],
    [
     "ordered pair",
     "(x, y) gives a point’s location.",
     "(−3, 2)"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Positive and Negative in Context",
   "kind": "table",
   "plain": true,
   "head": [
    "Situation",
    "Number"
   ],
   "rows": [
    [
     "10 feet below sea level",
     "−10"
    ],
    [
     "A deposit of $25",
     "+25"
    ],
    [
     "4 degrees below zero",
     "−4"
    ],
    [
     "A gain of 6 yards",
     "+6"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Comparing on a Number Line",
   "kind": "example",
   "text": "Numbers increase to the right. The number farther right is greater.",
   "example": "Compare −7 and −3.",
   "steps": [
    [
     "Position:",
     "−3 is to the right of −7"
    ]
   ],
   "answer": "−7 < −3",
   "check": {
    "true": "-7 < -3"
   },
   "color": "green"
  },
  {
   "title": "Ordering Rational Numbers",
   "kind": "example",
   "text": "Change to decimals, then place them on a number line.",
   "example": "Order ⟨-1.5,\\ \\tfrac{1}{2},\\ -\\tfrac{3}{4},\\ 0⟩ from least to greatest.",
   "steps": [
    [
     "Decimals:",
     "−1.5, 0.5, −0.75, 0"
    ]
   ],
   "answer": "⟨-1.5,\\ -\\tfrac{3}{4},\\ 0,\\ \\tfrac{1}{2}⟩",
   "check": {
    "true": "-1.5 < -0.75 && -0.75 < 0 && 0 < 0.5"
   },
   "color": "orange"
  },
  {
   "title": "Inequality Statements",
   "kind": "words",
   "rows": [
    [
     "The temperature is at least −5°F.",
     "t ≥ −5"
    ],
    [
     "The depth is less than −20 m.",
     "d < −20"
    ],
    [
     "−2 is greater than −9.",
     "−2 > −9"
    ]
   ],
   "check": {
    "true": "-2 > -9"
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Every negative number is less than every positive number.",
    "Opposites have the same absolute value.",
    "0 is neither positive nor negative."
   ],
   "bad": [
    [
     "−8 > −2 because 8 > 2",
     "−8 is farther left, so −8 < −2"
    ],
    [
     "|−6| = −6",
     "distance is positive: 6"
    ],
    [
     "Reading (x, y) as (y, x)",
     "x first: across, then up or down"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Absolute Value",
   "kind": "example",
   "text": "Count the distance from 0 on a number line.",
   "example": "Find |−12| + |5|.",
   "steps": [
    [
     "Distances:",
     "12 and 5"
    ]
   ],
   "answer": "17",
   "check": {
    "num": "Math.abs(-12)+Math.abs(5)",
    "is": 17
   },
   "color": "purple"
  },
  {
   "title": "Absolute Value in Context",
   "kind": "words",
   "rows": [
    [
     "An account balance of −$30 is a debt of …",
     "$30"
    ],
    [
     "Which is farther from 0: −9 or 7?",
     "−9"
    ],
    [
     "Elevation −45 m is how far below sea level?",
     "45 m"
    ]
   ],
   "check": {
    "num": "Math.abs(-9)",
    "is": 9
   },
   "color": "blue"
  },
  {
   "title": "The Four Quadrants",
   "kind": "table",
   "plain": true,
   "head": [
    "Quadrant",
    "Signs (x, y)"
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
   "after": "Points on an axis are in no quadrant.",
   "color": "green"
  },
  {
   "title": "Reflections",
   "kind": "example",
   "text": "Reflect over the x-axis: change the sign of y. Over the y-axis: change the sign of x.",
   "example": "Reflect (4, −3) over the y-axis.",
   "steps": [
    [
     "Change x:",
     "4 → −4"
    ]
   ],
   "answer": "(−4, −3)",
   "check": {
    "num": "-4",
    "is": -4
   },
   "color": "orange"
  },
  {
   "title": "Distance on a Grid",
   "kind": "example",
   "text": "Same x or same y: subtract the other coordinates and take the absolute value.",
   "example": "Distance from (2, −5) to (2, 3)?",
   "steps": [
    [
     "Same x:",
     "|3 − (−5)|"
    ]
   ],
   "answer": "8 units",
   "check": {
    "num": "Math.abs(3-(-5))",
    "is": 8
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I use the number line to compare negatives?",
    "Is my absolute value a distance (not negative)?",
    "Did I move across (x) before up or down (y)?",
    "Does my sign match the context (above or below, gain or loss)?"
   ],
   "color": "teal"
  }
 ]
};
