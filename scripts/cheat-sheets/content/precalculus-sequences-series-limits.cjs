/* Precalculus Unit 9 cheat sheet (Sequences, Series, and Limits). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-sequences-series-limits",
 "course": "Precalculus",
 "unitNo": 9,
 "unitName": "Sequences, Series, and Limits",
 "focus": "arithmetic and geometric sequences, finite series and sigma notation",
 "morefocus": "infinite geometric series and an introduction to limits",
 "front": [
  {
   "title": "Arithmetic vs Geometric",
   "kind": "table",
   "plain": true,
   "head": ["Type", "nth term"],
   "rows": [
    ["Arithmetic: add the same d", "⟨a_n = a_1 + (n - 1)d⟩"],
    ["Geometric: multiply by the same r", "⟨a_n = a_1 r^{\\,n-1}⟩"],
    ["Test", "equal differences → arithmetic; equal ratios → geometric"]
   ],
   "color": "purple"
  },
  {
   "title": "Arithmetic nth Term",
   "kind": "example",
   "text": "Find d, then use n − 1 steps.",
   "example": "7, 11, 15, 19, … Find the 30th term.",
   "steps": [["d = 4:", "⟨a_{30} = 7 + 29 \\cdot 4⟩"]],
   "answer": "123",
   "check": {"num": "7+29*4", "is": 123},
   "color": "blue"
  },
  {
   "title": "Geometric nth Term",
   "kind": "example",
   "text": "Find r by dividing a term by the one before it.",
   "example": "3, 6, 12, 24, … Find the 8th term.",
   "steps": [["r = 2:", "⟨a_8 = 3 \\cdot 2^7⟩"]],
   "answer": "384",
   "check": {"num": "3*2**7", "is": 384},
   "color": "green"
  },
  {
   "title": "Arithmetic Series",
   "kind": "example",
   "text": "Average of the first and last term, times the number of terms.",
   "example": "Sum of the first 20 terms of 5 + 8 + 11 + …",
   "steps": [["Last term:", "⟨a_{20} = 5 + 19 \\cdot 3 = 62⟩"], ["Sum:", "⟨S_{20} = \\tfrac{20(5 + 62)}{2}⟩"]],
   "answer": "670",
   "check": {"num": "20*(5+62)/2", "is": 670},
   "color": "orange"
  },
  {
   "title": "Geometric Series",
   "kind": "example",
   "text": "⟨S_n = \\tfrac{a_1(1 - r^n)}{1 - r}⟩, r ≠ 1.",
   "example": "Sum of the first 6 terms of 2 + 6 + 18 + …",
   "steps": [["r = 3:", "⟨S_6 = \\tfrac{2(1 - 3^6)}{1 - 3}⟩"]],
   "answer": "728",
   "check": {"num": "2*(1-3**6)/(1-3)", "is": 728},
   "color": "pink"
  },
  {
   "title": "Sigma Notation",
   "kind": "example",
   "text": "Substitute each k from the bottom value to the top value and add.",
   "example": "⟨\\sum_{k=1}^{5} (2k + 1)⟩",
   "steps": [["Terms:", "3 + 5 + 7 + 9 + 11"]],
   "answer": "35",
   "check": {"num": "3+5+7+9+11", "is": 35},
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Infinite Geometric Series",
   "kind": "example",
   "text": "Converges only when |r| < 1: ⟨S = \\tfrac{a_1}{1 - r}⟩.",
   "example": "12 + 6 + 3 + 1.5 + …",
   "steps": [["r = 1/2:", "⟨S = \\tfrac{12}{1 - 1/2}⟩"]],
   "answer": "24",
   "check": {"num": "12/(1-1/2)", "is": 24},
   "color": "purple"
  },
  {
   "title": "Converge or Diverge?",
   "kind": "words",
   "rows": [
    ["r = 2/3", "converges"],
    ["r = −1/2", "converges (terms alternate)"],
    ["r = 3/2", "diverges"],
    ["r = −1", "diverges"],
    ["arithmetic, d ≠ 0", "diverges"]
   ],
   "color": "blue"
  },
  {
   "title": "Limits by Factoring",
   "kind": "example",
   "text": "If substitution gives 0/0, factor, cancel, then substitute.",
   "example": "⟨\\lim_{x \\to 3} \\tfrac{x^2 - 9}{x - 3}⟩",
   "steps": [["Factor:", "⟨\\tfrac{(x - 3)(x + 3)}{x - 3} = x + 3⟩"], ["Substitute:", "3 + 3"]],
   "answer": "6",
   "check": {"num": "3+3", "is": 6},
   "color": "green"
  },
  {
   "title": "Limits at Infinity",
   "kind": "table",
   "plain": true,
   "head": ["Degrees of top and bottom", "Limit as x → ∞"],
   "rows": [
    ["top < bottom", "0"],
    ["top = bottom", "ratio of leading coefficients"],
    ["top > bottom", "∞ or −∞ (no finite limit)"]
   ],
   "color": "orange"
  },
  {
   "title": "Conjugates and One-Sided Limits",
   "kind": "example",
   "text": "Multiply by the conjugate to clear a square root.",
   "example": "⟨\\lim_{x \\to 0} \\tfrac{\\sqrt{x + 4} - 2}{x}⟩",
   "steps": [["Conjugate:", "⟨\\tfrac{1}{\\sqrt{x + 4} + 2}⟩"], ["Substitute:", "⟨\\tfrac{1}{2 + 2}⟩"]],
   "answer": "1/4",
   "check": {"num": "1/(2+2)", "is": 0.25},
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Check differences and ratios before choosing a formula.",
    "Use n − 1 steps from the first term to the nth term.",
    "A limit exists only if both one-sided limits agree."
   ],
   "bad": [
    ["a₁/(1 − r) with r = 2", "diverges"],
    ["0/0 → no limit", "factor first"],
    ["Σ k = 2 to 10 → 10 terms", "9 terms"]
   ],
   "color": "teal"
  }
 ]
};
