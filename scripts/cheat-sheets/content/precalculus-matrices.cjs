/* Precalculus Unit 6 cheat sheet (Matrices). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-matrices",
 "course": "Precalculus",
 "unitNo": 6,
 "unitName": "Matrices",
 "focus": "matrix operations and multiplication",
 "morefocus": "determinants, inverses and solving systems",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "dimensions",
     "rows × columns.",
     "2 × 3 matrix"
    ],
    [
     "identity matrix",
     "1s on the diagonal, 0s elsewhere.",
     "AI = A"
    ],
    [
     "scalar",
     "A single number multiplying every entry.",
     "3A"
    ],
    [
     "square matrix",
     "Same rows and columns.",
     "2 × 2"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Adding and Scalar Multiplication",
   "kind": "example",
   "text": "Add matching entries. A scalar multiplies every entry.",
   "example": "⟨2\\begin{bmatrix}1 & -3\\\\ 4 & 0\\end{bmatrix} + \\begin{bmatrix}2 & 5\\\\ -1 & 6\\end{bmatrix}⟩",
   "steps": [
    [
     "Scale:",
     "⟨\\begin{bmatrix}2 & -6\\\\ 8 & 0\\end{bmatrix}⟩"
    ]
   ],
   "answer": "⟨\\begin{bmatrix}4 & -1\\\\ 7 & 6\\end{bmatrix}⟩",
   "check": [
    {
     "num": "2*1+2",
     "is": 4
    },
    {
     "num": "2*(-3)+5",
     "is": -1
    }
   ],
   "color": "blue"
  },
  {
   "title": "Matrix Multiplication",
   "kind": "example",
   "text": "Row of the first times column of the second. Inner dimensions must match.",
   "example": "⟨\\begin{bmatrix}1 & 2\\\\ 3 & 4\\end{bmatrix}\\begin{bmatrix}5\\\\ 6\\end{bmatrix}⟩",
   "steps": [
    [
     "Row 1:",
     "1·5 + 2·6 = 17"
    ],
    [
     "Row 2:",
     "3·5 + 4·6 = 39"
    ]
   ],
   "answer": "⟨\\begin{bmatrix}17\\\\ 39\\end{bmatrix}⟩",
   "check": [
    {
     "num": "1*5+2*6",
     "is": 17
    },
    {
     "num": "3*5+4*6",
     "is": 39
    }
   ],
   "color": "green"
  },
  {
   "title": "When Can You Multiply?",
   "kind": "table",
   "plain": true,
   "head": [
    "A × B",
    "Result"
   ],
   "rows": [
    [
     "(2 × 3)(3 × 4)",
     "2 × 4"
    ],
    [
     "(3 × 2)(3 × 2)",
     "undefined"
    ],
    [
     "(1 × 3)(3 × 1)",
     "1 × 1"
    ]
   ],
   "after": "Matrix multiplication is NOT commutative: AB ≠ BA in general.",
   "color": "orange"
  },
  {
   "title": "Matrices in Context",
   "kind": "words",
   "rows": [
    [
     "Inventory × prices",
     "total cost per store"
    ],
    [
     "Transformation matrix",
     "rotates or reflects points"
    ],
    [
     "Adjacency matrix",
     "connections in a network"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Write dimensions before multiplying.",
    "Add only matrices of the same size.",
    "Order matters in multiplication."
   ],
   "bad": [
    [
     "Multiplying entry by entry",
     "row × column"
    ],
    [
     "AB = BA",
     "usually not"
    ],
    [
     "Adding a 2 × 2 to a 2 × 3",
     "undefined"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "2 × 2 Determinant",
   "kind": "example",
   "text": "⟨\\det\\begin{bmatrix}a & b\\\\ c & d\\end{bmatrix} = ad - bc⟩",
   "example": "⟨\\begin{bmatrix}4 & 3\\\\ 2 & 5\\end{bmatrix}⟩",
   "steps": [
    [
     "ad − bc:",
     "20 − 6"
    ]
   ],
   "answer": "14",
   "check": {
    "num": "4*5-3*2",
    "is": 14
   },
   "color": "purple"
  },
  {
   "title": "2 × 2 Inverse",
   "kind": "example",
   "text": "⟨A^{-1} = \\tfrac{1}{ad - bc}\\begin{bmatrix}d & -b\\\\ -c & a\\end{bmatrix}⟩",
   "example": "⟨\\begin{bmatrix}4 & 3\\\\ 2 & 5\\end{bmatrix}⟩",
   "steps": [
    [
     "Swap a and d, negate b and c:",
     "divide by det = 14"
    ]
   ],
   "answer": "⟨\\tfrac{1}{14}\\begin{bmatrix}5 & -3\\\\ -2 & 4\\end{bmatrix}⟩",
   "check": {
    "num": "(4*5+3*(-2))/14",
    "is": 1
   },
   "color": "blue"
  },
  {
   "title": "Solving AX = B",
   "kind": "example",
   "text": "⟨X = A^{-1}B⟩ (multiply on the LEFT).",
   "example": "4x + 3y = 10, 2x + 5y = 12",
   "steps": [
    [
     "Multiply:",
     "⟨\\tfrac{1}{14}(5 \\cdot 10 - 3 \\cdot 12,\\ -2 \\cdot 10 + 4 \\cdot 12)⟩"
    ]
   ],
   "answer": "x = 1, y = 2",
   "check": [
    {
     "num": "4*1+3*2",
     "is": 10
    },
    {
     "num": "2*1+5*2",
     "is": 12
    }
   ],
   "color": "green"
  },
  {
   "title": "3 × 3 Determinant (expand row 1)",
   "kind": "table",
   "plain": true,
   "head": [
    "Term",
    "Sign"
   ],
   "rows": [
    [
     "⟨a_{11}\\cdot\\text{minor}_{11}⟩",
     "+"
    ],
    [
     "⟨a_{12}\\cdot\\text{minor}_{12}⟩",
     "−"
    ],
    [
     "⟨a_{13}\\cdot\\text{minor}_{13}⟩",
     "+"
    ]
   ],
   "after": "If det = 0, the matrix has no inverse (singular).",
   "color": "orange"
  },
  {
   "title": "Cramer’s Rule",
   "kind": "example",
   "text": "⟨x = \\tfrac{\\det A_x}{\\det A}⟩: replace the x-column with the constants.",
   "example": "4x + 3y = 10, 2x + 5y = 12",
   "steps": [
    [
     "det A_x:",
     "10·5 − 3·12 = 14"
    ]
   ],
   "answer": "⟨x = \\tfrac{14}{14} = 1⟩",
   "check": {
    "num": "(10*5-3*12)/14",
    "is": 1
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Is det ≠ 0 before I invert?",
    "Did I multiply A⁻¹ on the LEFT of B?",
    "Did I check my solution in the original system?",
    "Do the dimensions allow this product?"
   ],
   "color": "teal"
  }
 ]
};
