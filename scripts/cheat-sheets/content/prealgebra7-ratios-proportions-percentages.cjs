/* Pre-Algebra (7th) Unit 6 cheat sheet (Ratios, Proportions, and Percentages). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-ratios-proportions-percentages",
 "course": "Pre-Algebra (7th)",
 "unitNo": 6,
 "unitName": "Ratios, Proportions, and Percentages",
 "focus": "ratios, unit rates, proportions, scale drawings and probability",
 "morefocus": "percents, percent of change, markup, discount and tables",
 "front": [
  {
   "title": "Unit Rates",
   "kind": "example",
   "text": "Divide to get an amount per 1 unit.",
   "example": "$4.32 for 12 ounces",
   "steps": [
    [
     "Divide:",
     "⟨\\tfrac{4.32}{12}⟩"
    ]
   ],
   "answer": "$0.36 per ounce",
   "check": {
    "num": "4.32/12",
    "is": 0.36
   },
   "color": "purple"
  },
  {
   "title": "Solving Proportions",
   "kind": "example",
   "text": "Cross products are equal.",
   "example": "⟨\\tfrac{x}{12} = \\tfrac{15}{20}⟩",
   "steps": [
    [
     "Cross multiply:",
     "20x = 180"
    ]
   ],
   "answer": "x = 9",
   "check": {
    "num": "12*15/20",
    "is": 9
   },
   "color": "blue"
  },
  {
   "title": "Scale Drawings",
   "kind": "example",
   "text": "Set up a proportion: drawing to actual.",
   "example": "Scale 1 in : 8 ft. A wall is 3.5 in on the plan.",
   "steps": [
    [
     "Proportion:",
     "3.5 × 8"
    ]
   ],
   "answer": "28 ft",
   "check": {
    "num": "3.5*8",
    "is": 28
   },
   "color": "green"
  },
  {
   "title": "Similar Figures",
   "kind": "example",
   "text": "Corresponding sides are proportional.",
   "example": "Sides 4 and 6 in one figure; the matching side to 4 is 10. Find x matching 6.",
   "steps": [
    [
     "Scale factor:",
     "⟨\\tfrac{10}{4} = 2.5⟩"
    ]
   ],
   "answer": "x = 15",
   "check": {
    "num": "6*10/4",
    "is": 15
   },
   "color": "orange"
  },
  {
   "title": "Probability",
   "kind": "example",
   "text": "P(event) = ⟨\\tfrac{\\text{favorable outcomes}}{\\text{total outcomes}}⟩",
   "example": "A bag has 3 red, 5 blue, 2 green. P(blue)?",
   "steps": [
    [
     "Count:",
     "5 of 10"
    ]
   ],
   "answer": "⟨\\tfrac{1}{2}⟩",
   "check": {
    "num": "5/10",
    "is": 0.5
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Keep units in the same order in both ratios.",
    "Similar figures: same shape, proportional sides.",
    "Probability is between 0 and 1."
   ],
   "bad": [
    [
     "Mixing up the order in a proportion",
     "match drawing:actual on both sides"
    ],
    [
     "Adding a constant to scale",
     "multiply by the scale factor"
    ],
    [
     "P(event) > 1",
     "check your count"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Fractions, Decimals, Percents",
   "kind": "table",
   "plain": true,
   "head": [
    "Fraction",
    "Decimal · Percent"
   ],
   "rows": [
    [
     "⟨\\tfrac{3}{5}⟩",
     "0.6 · 60%"
    ],
    [
     "⟨\\tfrac{1}{8}⟩",
     "0.125 · 12.5%"
    ],
    [
     "⟨\\tfrac{5}{4}⟩",
     "1.25 · 125%"
    ]
   ],
   "check": [
    {
     "num": "3/5",
     "is": 0.6
    },
    {
     "num": "1/8",
     "is": 0.125
    }
   ],
   "color": "purple"
  },
  {
   "title": "Percent Equations",
   "kind": "example",
   "text": "part = percent × whole.",
   "example": "45 is what percent of 60?",
   "steps": [
    [
     "Divide:",
     "⟨\\tfrac{45}{60} = 0.75⟩"
    ]
   ],
   "answer": "75%",
   "check": {
    "num": "45/60*100",
    "is": 75
   },
   "color": "blue"
  },
  {
   "title": "Percent of Change",
   "kind": "example",
   "text": "⟨\\tfrac{\\text{new} - \\text{original}}{\\text{original}}⟩; positive = increase.",
   "example": "A price rises from $40 to $52.",
   "steps": [
    [
     "Change:",
     "⟨\\tfrac{12}{40} = 0.3⟩"
    ]
   ],
   "answer": "30% increase",
   "check": {
    "num": "(52-40)/40*100",
    "is": 30
   },
   "color": "green"
  },
  {
   "title": "Markup and Discount",
   "kind": "example",
   "text": "Sale price = original − discount. Selling price = cost + markup.",
   "example": "A $65 jacket is 20% off.",
   "steps": [
    [
     "Discount:",
     "0.20 × 65 = 13"
    ],
    [
     "Sale price:",
     "65 − 13"
    ]
   ],
   "answer": "$52",
   "check": {
    "num": "65*0.8",
    "is": 52
   },
   "color": "orange"
  },
  {
   "title": "Using Tables",
   "kind": "table",
   "plain": true,
   "head": [
    "Hours",
    "Earnings ($)"
   ],
   "rows": [
    [
     "2",
     "27"
    ],
    [
     "4",
     "54"
    ],
    [
     "6",
     "81"
    ]
   ],
   "after": "Constant ratio: $13.50 per hour, so the relationship is proportional.",
   "check": {
    "num": "27/2",
    "is": 13.5
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Is my rate “per 1”?",
    "Did I divide by the ORIGINAL for percent change?",
    "Is my sale price less than the original?",
    "Are my ratios set up in the same order?"
   ],
   "color": "teal"
  }
 ]
};
