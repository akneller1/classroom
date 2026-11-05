/* 6th Grade Math Unit 1 cheat sheet (Ratios, Rate, Percent and Proportions). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "math6-ratios-rates-percent-proportions",
 "course": "6th Grade Math",
 "unitNo": 1,
 "unitName": "Ratios, Rate, Percent and Proportions",
 "focus": "ratios, unit rates, equivalent ratios and tables",
 "morefocus": "proportions, percents and unit conversions",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "ratio",
     "Compares two quantities.",
     "3 to 5, 3 : 5, ⟨\\tfrac{3}{5}⟩"
    ],
    [
     "rate",
     "A ratio of two different units.",
     "150 miles in 3 hours"
    ],
    [
     "unit rate",
     "A rate for 1 unit.",
     "50 miles per hour"
    ],
    [
     "equivalent ratios",
     "Same comparison; multiply or divide both parts by the same number.",
     "2 : 3 = 8 : 12"
    ],
    [
     "proportion",
     "Two equal ratios.",
     "⟨\\tfrac{2}{5} = \\tfrac{6}{15}⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Finding a Unit Rate",
   "kind": "example",
   "text": "Divide the first quantity by the second so the second becomes 1.",
   "example": "$7.20 for 6 pounds of apples. Price per pound?",
   "steps": [
    [
     "Divide:",
     "⟨\\tfrac{7.20}{6} = 1.20⟩"
    ]
   ],
   "answer": "$1.20 per pound",
   "check": {
    "num": "7.20/6",
    "is": 1.2
   },
   "color": "blue"
  },
  {
   "title": "Ratio Tables",
   "kind": "table",
   "plain": true,
   "head": [
    "Cups of flour",
    "Cookies"
   ],
   "rows": [
    [
     "2",
     "24"
    ],
    [
     "4",
     "48"
    ],
    [
     "6",
     "72"
    ],
    [
     "1",
     "12"
    ]
   ],
   "after": "Multiply or divide BOTH columns by the same number. Each row is an equivalent ratio.",
   "check": [
    {
     "num": "24/2",
     "is": 12
    },
    {
     "num": "72/6",
     "is": 12
    }
   ],
   "color": "green"
  },
  {
   "title": "Comparing Ratios",
   "kind": "example",
   "text": "Write each as a unit rate (or find a common term), then compare.",
   "example": "Which is the better buy: 12 oz for $3 or 20 oz for $4.40?",
   "steps": [
    [
     "Unit prices:",
     "⟨\\tfrac{3}{12} = 0.25⟩, ⟨\\tfrac{4.40}{20} = 0.22⟩ dollars per oz"
    ]
   ],
   "answer": "20 oz for $4.40",
   "check": [
    {
     "num": "3/12",
     "is": 0.25
    },
    {
     "num": "4.40/20",
     "is": 0.22
    }
   ],
   "color": "orange"
  },
  {
   "title": "Solving a Proportion",
   "kind": "example",
   "text": "Use equivalent ratios or cross products.",
   "example": "⟨\\tfrac{3}{4} = \\tfrac{x}{20}⟩",
   "steps": [
    [
     "Scale:",
     "4 × 5 = 20, so 3 × 5 = ⟨x⟩"
    ]
   ],
   "answer": "⟨x = 15⟩",
   "check": {
    "num": "3*20/4",
    "is": 15
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Order matters: 3 boys to 5 girls is 3 : 5, not 5 : 3.",
    "Units belong in the answer of a rate.",
    "A unit rate always has 1 in the second quantity."
   ],
   "bad": [
    [
     "Adding to both parts: 2 : 3 → 4 : 5",
     "multiply, do not add"
    ],
    [
     "Dividing the wrong way for a unit price",
     "price ÷ amount"
    ],
    [
     "Mixing units",
     "convert first"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Percent Basics",
   "kind": "table",
   "plain": true,
   "head": [
    "Percent",
    "Fraction / decimal"
   ],
   "rows": [
    [
     "50%",
     "⟨\\tfrac{1}{2}⟩ = 0.5"
    ],
    [
     "25%",
     "⟨\\tfrac{1}{4}⟩ = 0.25"
    ],
    [
     "10%",
     "⟨\\tfrac{1}{10}⟩ = 0.1"
    ],
    [
     "75%",
     "⟨\\tfrac{3}{4}⟩ = 0.75"
    ],
    [
     "120%",
     "1.2"
    ]
   ],
   "after": "Percent means “per 100.”",
   "color": "purple"
  },
  {
   "title": "Percent of a Number",
   "kind": "example",
   "text": "Change the percent to a decimal, then multiply.",
   "example": "Find 35% of 80.",
   "steps": [
    [
     "Decimal:",
     "35% = 0.35"
    ],
    [
     "Multiply:",
     "0.35 × 80"
    ]
   ],
   "answer": "28",
   "check": {
    "num": "0.35*80",
    "is": 28
   },
   "color": "blue"
  },
  {
   "title": "Finding the Whole",
   "kind": "example",
   "text": "part = percent × whole, so whole = part ÷ percent.",
   "example": "18 is 30% of what number?",
   "steps": [
    [
     "Divide:",
     "⟨\\tfrac{18}{0.30}⟩"
    ]
   ],
   "answer": "60",
   "check": {
    "num": "18/0.30",
    "is": 60
   },
   "color": "green"
  },
  {
   "title": "A Fraction as a Percent",
   "kind": "example",
   "text": "Make the denominator 100, or divide and multiply by 100.",
   "example": "Write ⟨\\tfrac{7}{20}⟩ as a percent.",
   "steps": [
    [
     "Scale:",
     "⟨\\tfrac{7}{20} = \\tfrac{35}{100}⟩"
    ]
   ],
   "answer": "35%",
   "check": {
    "num": "7/20*100",
    "is": 35
   },
   "color": "orange"
  },
  {
   "title": "Converting Units",
   "kind": "table",
   "plain": true,
   "head": [
    "Conversion",
    "Use the ratio"
   ],
   "rows": [
    [
     "1 ft = 12 in",
     "⟨\\tfrac{12 \\text{ in}}{1 \\text{ ft}}⟩"
    ],
    [
     "1 yd = 3 ft",
     "⟨\\tfrac{3 \\text{ ft}}{1 \\text{ yd}}⟩"
    ],
    [
     "1 gal = 4 qt",
     "⟨\\tfrac{4 \\text{ qt}}{1 \\text{ gal}}⟩"
    ],
    [
     "1 m = 100 cm",
     "⟨\\tfrac{100 \\text{ cm}}{1 \\text{ m}}⟩"
    ]
   ],
   "after": "Example: 5 ft × 12 in per ft = 60 in.",
   "check": {
    "num": "5*12",
    "is": 60
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I write the ratio in the order the words say?",
    "Is my unit rate “per 1”?",
    "Does my percent answer make sense (less than the whole when under 100%)?",
    "Did my units cancel when converting?"
   ],
   "color": "teal"
  }
 ]
};
