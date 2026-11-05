/* Pre-Algebra (7th) Unit 12 cheat sheet (Data Analysis and Probability). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-data-analysis-probability",
 "course": "Pre-Algebra (7th)",
 "unitNo": 12,
 "unitName": "Data Analysis and Probability",
 "focus": "frequency tables, histograms, box plots and stem-and-leaf plots",
 "morefocus": "probability, independent and dependent events, counting and sampling",
 "front": [
  {
   "title": "Choosing a Display",
   "kind": "table",
   "plain": true,
   "head": [
    "Display",
    "Shows"
   ],
   "rows": [
    [
     "Frequency table / line plot",
     "how often each value occurs"
    ],
    [
     "Histogram",
     "frequencies in equal intervals"
    ],
    [
     "Box-and-whisker plot",
     "five-number summary"
    ],
    [
     "Stem-and-leaf plot",
     "every value, grouped by tens"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Box-and-Whisker Plot",
   "kind": "example",
   "text": "Find the minimum, Q1, median, Q3, maximum.",
   "example": "3, 5, 6, 8, 9, 11, 14",
   "steps": [
    [
     "Median:",
     "8"
    ],
    [
     "Q1, Q3:",
     "5 and 11"
    ]
   ],
   "answer": "3, 5, 8, 11, 14",
   "check": [
    {
     "num": "11-5",
     "is": 6
    }
   ],
   "color": "blue"
  },
  {
   "title": "Stem-and-Leaf Plot",
   "kind": "example",
   "text": "Stem = tens digit, leaf = ones digit. Include a key.",
   "example": "Stems 2 | 1 4 7 and 3 | 0 5: median?",
   "steps": [
    [
     "Values:",
     "21, 24, 27, 30, 35"
    ]
   ],
   "answer": "27",
   "check": {
    "num": "27",
    "is": 27
   },
   "color": "green"
  },
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "outcome",
     "One possible result.",
     "rolling a 4"
    ],
    [
     "sample space",
     "All possible outcomes.",
     "{1, 2, 3, 4, 5, 6}"
    ],
    [
     "theoretical probability",
     "Expected chance from counting.",
     "P(4) = ⟨\\tfrac{1}{6}⟩"
    ],
    [
     "experimental probability",
     "Results of trials.",
     "9 heads in 20 flips"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Counting Outcomes",
   "kind": "example",
   "text": "Multiply the number of choices for each step.",
   "example": "4 shirts, 3 pants, 2 shoes: outfits?",
   "steps": [
    [
     "Multiply:",
     "4 · 3 · 2"
    ]
   ],
   "answer": "24 outfits",
   "check": {
    "num": "4*3*2",
    "is": 24
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Histogram bars touch; bar graph bars do not.",
    "Include a key on stem-and-leaf plots.",
    "Experimental probability approaches theoretical with many trials."
   ],
   "bad": [
    [
     "Median without ordering",
     "order first"
    ],
    [
     "P = favorable ÷ unfavorable",
     "favorable ÷ total"
    ],
    [
     "Adding choices to count outcomes",
     "multiply"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Independent Events",
   "kind": "example",
   "text": "P(A and B) = P(A) · P(B).",
   "example": "Flip a coin and roll a die: P(heads and 6)?",
   "steps": [
    [
     "Multiply:",
     "⟨\\tfrac{1}{2} \\cdot \\tfrac{1}{6}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{1}{12}⟩",
   "check": {
    "num": "1/2*1/6",
    "is": 0.08333333333333333
   },
   "color": "purple"
  },
  {
   "title": "Dependent Events",
   "kind": "example",
   "text": "The first draw changes the second (no replacement).",
   "example": "3 red, 2 blue marbles. P(red, then red)?",
   "steps": [
    [
     "Multiply:",
     "⟨\\tfrac{3}{5} \\cdot \\tfrac{2}{4}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{3}{10}⟩",
   "check": {
    "num": "3/5*2/4",
    "is": 0.3
   },
   "color": "blue"
  },
  {
   "title": "Permutations and Combinations",
   "kind": "table",
   "plain": true,
   "head": [
    "Type",
    "Example"
   ],
   "rows": [
    [
     "Permutation (order matters)",
     "⟨_5P_2 = 5 \\cdot 4 = 20⟩"
    ],
    [
     "Combination (order does not)",
     "⟨_5C_2 = \\tfrac{20}{2} = 10⟩"
    ]
   ],
   "after": "Ranking or arranging → permutation. Choosing a group → combination.",
   "check": [
    {
     "num": "5*4",
     "is": 20
    },
    {
     "num": "5*4/2",
     "is": 10
    }
   ],
   "color": "green"
  },
  {
   "title": "Experimental Probability",
   "kind": "example",
   "text": "⟨\\tfrac{\\text{times it happened}}{\\text{total trials}}⟩",
   "example": "A spinner lands on red 18 times in 60 spins.",
   "steps": [
    [
     "Divide:",
     "⟨\\tfrac{18}{60}⟩"
    ]
   ],
   "answer": "0.3 (30%)",
   "check": {
    "num": "18/60",
    "is": 0.3
   },
   "color": "orange"
  },
  {
   "title": "Random Samples and Surveys",
   "kind": "words",
   "rows": [
    [
     "Survey every 10th student entering school",
     "random (systematic)"
    ],
    [
     "Ask only the soccer team about favorite sports",
     "biased"
    ],
    [
     "Draw names from a hat",
     "random"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did the first event change the second?",
    "Does order matter?",
    "Is my probability between 0 and 1?",
    "Is my sample random and representative?"
   ],
   "color": "teal"
  }
 ]
};
