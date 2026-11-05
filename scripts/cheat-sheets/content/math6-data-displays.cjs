/* 6th Grade Math Unit 7 cheat sheet (Data Displays). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "math6-data-displays",
 "course": "6th Grade Math",
 "unitNo": 7,
 "unitName": "Data Displays",
 "focus": "statistical questions, dot plots, histograms and box plots",
 "morefocus": "mean, median, range, IQR, MAD and the shape of a distribution",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "statistical question",
     "Expects answers that vary.",
     "How tall are 6th graders?"
    ],
    [
     "distribution",
     "How data values are spread out.",
     "a dot plot of quiz scores"
    ],
    [
     "mean",
     "Sum ÷ number of values.",
     "mean of 2, 4, 9 is 5"
    ],
    [
     "median",
     "Middle value of ordered data.",
     "median of 2, 4, 9 is 4"
    ],
    [
     "outlier",
     "A value far from the others.",
     "45 in 10, 12, 11, 45"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Choosing a Display",
   "kind": "table",
   "plain": true,
   "head": [
    "Display",
    "Best for"
   ],
   "rows": [
    [
     "Dot plot",
     "small data sets; each value shown"
    ],
    [
     "Histogram",
     "large data in equal intervals"
    ],
    [
     "Box plot",
     "five-number summary, spread, comparing groups"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Mean",
   "kind": "example",
   "text": "Add the values, then divide by how many there are.",
   "example": "Find the mean of 8, 12, 7, 9, 14.",
   "steps": [
    [
     "Sum:",
     "50"
    ],
    [
     "Divide:",
     "50 ÷ 5"
    ]
   ],
   "answer": "10",
   "check": {
    "num": "(8+12+7+9+14)/5",
    "is": 10
   },
   "color": "green"
  },
  {
   "title": "Median",
   "kind": "example",
   "text": "Order the data. With an even count, average the two middle values.",
   "example": "Median of 3, 9, 4, 7, 10, 6.",
   "steps": [
    [
     "Order:",
     "3, 4, 6, 7, 9, 10"
    ],
    [
     "Middle two:",
     "⟨\\tfrac{6 + 7}{2}⟩"
    ]
   ],
   "answer": "6.5",
   "check": {
    "num": "(6+7)/2",
    "is": 6.5
   },
   "color": "orange"
  },
  {
   "title": "Five-Number Summary",
   "kind": "example",
   "text": "Minimum, Q1, median, Q3, maximum.",
   "example": "Data: 2, 4, 5, 7, 8, 10, 12, 15",
   "steps": [
    [
     "Median:",
     "⟨\\tfrac{7 + 8}{2} = 7.5⟩"
    ],
    [
     "Q1, Q3:",
     "medians of each half: 4.5 and 11"
    ]
   ],
   "answer": "2, 4.5, 7.5, 11, 15",
   "check": [
    {
     "num": "(7+8)/2",
     "is": 7.5
    },
    {
     "num": "(4+5)/2",
     "is": 4.5
    },
    {
     "num": "(10+12)/2",
     "is": 11
    }
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Order data before finding the median.",
    "A histogram’s bars touch; intervals must be equal.",
    "Outliers pull the mean, not the median."
   ],
   "bad": [
    [
     "Median of unordered data",
     "order it first"
    ],
    [
     "Range = largest value",
     "range = max − min"
    ],
    [
     "Reading a box plot’s box as the whole data",
     "the box is the middle 50%"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Range and IQR",
   "kind": "example",
   "text": "Range = max − min. IQR = Q3 − Q1 (spread of the middle half).",
   "example": "Using 2, 4.5, 7.5, 11, 15:",
   "steps": [
    [
     "Range:",
     "15 − 2 = 13"
    ],
    [
     "IQR:",
     "11 − 4.5 = 6.5"
    ]
   ],
   "answer": "range 13, IQR 6.5",
   "check": [
    {
     "num": "15-2",
     "is": 13
    },
    {
     "num": "11-4.5",
     "is": 6.5
    }
   ],
   "color": "purple"
  },
  {
   "title": "Mean Absolute Deviation",
   "kind": "example",
   "text": "Find the mean, the distance of each value from it, then the mean of those distances.",
   "example": "MAD of 2, 4, 6, 8.",
   "steps": [
    [
     "Mean:",
     "5"
    ],
    [
     "Distances:",
     "3, 1, 1, 3"
    ]
   ],
   "answer": "MAD = 2",
   "check": {
    "num": "(3+1+1+3)/4",
    "is": 2
   },
   "color": "blue"
  },
  {
   "title": "Shape of a Distribution",
   "kind": "table",
   "plain": true,
   "head": [
    "Shape",
    "Mean vs. median"
   ],
   "rows": [
    [
     "Symmetric",
     "about equal"
    ],
    [
     "Skewed right (long tail right)",
     "mean > median"
    ],
    [
     "Skewed left (long tail left)",
     "mean < median"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Best Measure of Center and Spread",
   "kind": "words",
   "rows": [
    [
     "Symmetric, no outliers",
     "mean and MAD"
    ],
    [
     "Skewed or has outliers",
     "median and IQR"
    ],
    [
     "Comparing two box plots",
     "medians and IQRs"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Describing a Distribution",
   "kind": "words",
   "rows": [
    [
     "Center",
     "mean or median"
    ],
    [
     "Spread",
     "range, IQR or MAD"
    ],
    [
     "Shape",
     "symmetric, skewed, clusters, gaps"
    ],
    [
     "Unusual values",
     "outliers"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Is my question statistical (answers vary)?",
    "Did I order the data first?",
    "Did I choose the center that fits the shape?",
    "Does my answer include units?"
   ],
   "color": "teal"
  }
 ]
};
