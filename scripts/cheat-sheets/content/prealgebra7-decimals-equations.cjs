/* Pre-Algebra (7th) Unit 3 cheat sheet (Decimals and Equations). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-decimals-equations",
 "course": "Pre-Algebra (7th)",
 "unitNo": 3,
 "unitName": "Decimals and Equations",
 "focus": "rounding, estimating and measures of center",
 "morefocus": "formulas, decimal equations and the metric system",
 "front": [
  {
   "title": "Rounding Decimals",
   "kind": "example",
   "text": "Find the place, look one digit to the right: 5 or more rounds up.",
   "example": "Round 6.4782 to the nearest hundredth.",
   "steps": [
    [
     "Hundredths digit:",
     "7; next digit 8 rounds up"
    ]
   ],
   "answer": "6.48",
   "check": {
    "num": "Math.round(6.4782*100)/100",
    "is": 6.48
   },
   "color": "purple"
  },
  {
   "title": "Estimating Products and Quotients",
   "kind": "example",
   "text": "Round to compatible numbers first.",
   "example": "Estimate 39.6 × 5.1 and 63.5 ÷ 8.2.",
   "steps": [
    [
     "Round:",
     "40 × 5 and 64 ÷ 8"
    ]
   ],
   "answer": "≈ 200 and ≈ 8",
   "check": [
    {
     "num": "40*5",
     "is": 200
    },
    {
     "num": "64/8",
     "is": 8
    }
   ],
   "color": "blue"
  },
  {
   "title": "Measures of Center",
   "kind": "table",
   "plain": true,
   "head": [
    "Measure",
    "How to find it"
   ],
   "rows": [
    [
     "Mean",
     "sum ÷ number of values"
    ],
    [
     "Median",
     "middle value of ordered data"
    ],
    [
     "Mode",
     "most frequent value"
    ]
   ],
   "after": "Data 2.5, 3, 3, 4.5: mean 3.25, median 3, mode 3",
   "check": {
    "num": "(2.5+3+3+4.5)/4",
    "is": 3.25
   },
   "color": "green"
  },
  {
   "title": "Mean of Decimal Data",
   "kind": "example",
   "text": "Add, then divide by the count.",
   "example": "Times: 12.4, 11.8, 13.1, 12.7 s",
   "steps": [
    [
     "Sum:",
     "50.0"
    ],
    [
     "Divide by 4:",
     "12.5"
    ]
   ],
   "answer": "12.5 s",
   "check": {
    "num": "(12.4+11.8+13.1+12.7)/4",
    "is": 12.5
   },
   "color": "orange"
  },
  {
   "title": "Using Formulas",
   "kind": "example",
   "text": "Substitute the known values into the formula.",
   "example": "d = rt with r = 55.5 mph, t = 2.4 h",
   "steps": [
    [
     "Multiply:",
     "55.5 × 2.4"
    ]
   ],
   "answer": "133.2 miles",
   "check": {
    "num": "55.5*2.4",
    "is": 133.2
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Line up decimal points to add or subtract.",
    "Count decimal places when multiplying.",
    "An outlier changes the mean more than the median."
   ],
   "bad": [
    [
     "Rounding 6.4782 to 6.47",
     "the 8 rounds the 7 up: 6.48"
    ],
    [
     "Median of unordered data",
     "order first"
    ],
    [
     "Forgetting units in formulas",
     "write units every step"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Adding or Subtracting Decimals",
   "kind": "example",
   "text": "Undo the operation on both sides.",
   "example": "x + 3.75 = 10.2",
   "steps": [
    [
     "Subtract 3.75:",
     "x = 10.2 − 3.75"
    ]
   ],
   "answer": "x = 6.45",
   "check": {
    "num": "10.2-3.75",
    "is": 6.45
   },
   "color": "purple"
  },
  {
   "title": "Multiplying or Dividing Decimals",
   "kind": "example",
   "text": "Divide both sides by the coefficient.",
   "example": "1.6m = 9.6",
   "steps": [
    [
     "Divide:",
     "⟨m = \\tfrac{9.6}{1.6}⟩"
    ]
   ],
   "answer": "m = 6",
   "check": {
    "num": "9.6/1.6",
    "is": 6
   },
   "color": "blue"
  },
  {
   "title": "Division Equations",
   "kind": "example",
   "text": "Multiply both sides by the divisor.",
   "example": "⟨\\tfrac{k}{0.4} = 15⟩",
   "steps": [
    [
     "Multiply by 0.4:",
     "k = 15 × 0.4"
    ]
   ],
   "answer": "k = 6",
   "check": {
    "num": "15*0.4",
    "is": 6
   },
   "color": "green"
  },
  {
   "title": "Metric Prefixes",
   "kind": "table",
   "plain": true,
   "head": [
    "Prefix",
    "Meaning"
   ],
   "rows": [
    [
     "kilo- (k)",
     "1,000"
    ],
    [
     "centi- (c)",
     "⟨\\tfrac{1}{100}⟩"
    ],
    [
     "milli- (m)",
     "⟨\\tfrac{1}{1000}⟩"
    ]
   ],
   "after": "Bigger unit → smaller unit: multiply. Smaller → bigger: divide.",
   "color": "orange"
  },
  {
   "title": "Metric Conversions",
   "kind": "table",
   "plain": true,
   "head": [
    "Convert",
    "Answer"
   ],
   "rows": [
    [
     "3.2 km to m",
     "3,200 m"
    ],
    [
     "450 cm to m",
     "4.5 m"
    ],
    [
     "2.5 L to mL",
     "2,500 mL"
    ],
    [
     "760 mg to g",
     "0.76 g"
    ]
   ],
   "check": [
    {
     "num": "3.2*1000",
     "is": 3200
    },
    {
     "num": "450/100",
     "is": 4.5
    },
    {
     "num": "760/1000",
     "is": 0.76
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
