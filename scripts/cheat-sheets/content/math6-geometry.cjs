/* 6th Grade Math Unit 6 cheat sheet (Geometry). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "math6-geometry",
 "course": "6th Grade Math",
 "unitNo": 6,
 "unitName": "Geometry",
 "focus": "area of quadrilaterals, triangles and composite polygons",
 "morefocus": "volume, polygons on the coordinate plane, nets and surface area",
 "front": [
  {
   "title": "Area Formulas",
   "kind": "table",
   "plain": true,
   "head": [
    "Figure",
    "Area"
   ],
   "rows": [
    [
     "Rectangle",
     "A = lw"
    ],
    [
     "Parallelogram",
     "A = bh"
    ],
    [
     "Triangle",
     "⟨A = \\tfrac{1}{2}bh⟩"
    ],
    [
     "Trapezoid",
     "⟨A = \\tfrac{1}{2}(b_1 + b_2)h⟩"
    ]
   ],
   "after": "The height is perpendicular to the base.",
   "color": "purple"
  },
  {
   "title": "Parallelograms",
   "kind": "example",
   "text": "Use the base and the perpendicular height, not the slanted side.",
   "example": "Base 9 cm, height 5 cm, slanted side 6 cm.",
   "steps": [
    [
     "A = bh:",
     "9 · 5"
    ]
   ],
   "answer": "45 cm²",
   "check": {
    "num": "9*5",
    "is": 45
   },
   "color": "blue"
  },
  {
   "title": "Triangles",
   "kind": "example",
   "text": "A triangle is half of a parallelogram.",
   "example": "Base 12 in, height 7 in.",
   "steps": [
    [
     "Half of bh:",
     "⟨\\tfrac{1}{2} \\cdot 12 \\cdot 7⟩"
    ]
   ],
   "answer": "42 in²",
   "check": {
    "num": "0.5*12*7",
    "is": 42
   },
   "color": "green"
  },
  {
   "title": "Trapezoids",
   "kind": "example",
   "text": "Average the two bases, then multiply by the height.",
   "example": "Bases 6 m and 10 m, height 4 m.",
   "steps": [
    [
     "Formula:",
     "⟨\\tfrac{1}{2}(6 + 10)(4)⟩"
    ]
   ],
   "answer": "32 m²",
   "check": {
    "num": "0.5*(6+10)*4",
    "is": 32
   },
   "color": "orange"
  },
  {
   "title": "Composite Figures",
   "kind": "example",
   "text": "Split into rectangles and triangles, then add (or subtract a missing piece).",
   "example": "A 10 × 6 rectangle with a triangle (base 10, height 3) on top.",
   "steps": [
    [
     "Rectangle:",
     "60"
    ],
    [
     "Triangle:",
     "⟨\\tfrac{1}{2} \\cdot 10 \\cdot 3 = 15⟩"
    ]
   ],
   "answer": "75 units²",
   "check": {
    "num": "10*6+0.5*10*3",
    "is": 75
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Area is in square units (cm²).",
    "Volume is in cubic units (cm³).",
    "Height makes a right angle with the base."
   ],
   "bad": [
    [
     "Using the slanted side as height",
     "use the perpendicular height"
    ],
    [
     "Forgetting the ½ for triangles",
     "⟨\\tfrac{1}{2}bh⟩"
    ],
    [
     "Square units for volume",
     "cubic units"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Volume of a Rectangular Prism",
   "kind": "example",
   "text": "V = lwh (works for fractional edges too).",
   "example": "⟨2\\tfrac{1}{2}⟩ ft by 4 ft by 3 ft",
   "steps": [
    [
     "Multiply:",
     "2.5 · 4 · 3"
    ]
   ],
   "answer": "30 ft³",
   "check": {
    "num": "2.5*4*3",
    "is": 30
   },
   "color": "purple"
  },
  {
   "title": "Polygons on the Coordinate Plane",
   "kind": "example",
   "text": "Find side lengths by subtracting coordinates on the same line.",
   "example": "Rectangle with vertices (−2, 1), (4, 1), (4, 5), (−2, 5). Area?",
   "steps": [
    [
     "Length:",
     "4 − (−2) = 6"
    ],
    [
     "Width:",
     "5 − 1 = 4"
    ]
   ],
   "answer": "24 units²",
   "check": {
    "num": "(4-(-2))*(5-1)",
    "is": 24
   },
   "color": "blue"
  },
  {
   "title": "Perimeter on a Grid",
   "kind": "example",
   "text": "Add all side lengths.",
   "example": "Same rectangle: perimeter?",
   "steps": [
    [
     "Add:",
     "6 + 4 + 6 + 4"
    ]
   ],
   "answer": "20 units",
   "check": {
    "num": "2*(6+4)",
    "is": 20
   },
   "color": "green"
  },
  {
   "title": "Nets and Surface Area",
   "kind": "example",
   "text": "Unfold the solid into its faces and add their areas.",
   "example": "Surface area of a 5 × 3 × 2 box.",
   "steps": [
    [
     "Pairs of faces:",
     "2(15) + 2(10) + 2(6)"
    ]
   ],
   "answer": "62 units²",
   "check": {
    "num": "2*(5*3+5*2+3*2)",
    "is": 62
   },
   "color": "orange"
  },
  {
   "title": "Which Measure?",
   "kind": "table",
   "plain": true,
   "head": [
    "Question",
    "Measure"
   ],
   "rows": [
    [
     "Fence around a garden",
     "Perimeter"
    ],
    [
     "Carpet for a floor",
     "Area"
    ],
    [
     "Wrapping paper for a box",
     "Surface area"
    ],
    [
     "Water in a tank",
     "Volume"
    ]
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I use the perpendicular height?",
    "Did I include every face in the net?",
    "Are my units squared or cubed correctly?",
    "Did I split the composite figure without overlapping pieces?"
   ],
   "color": "teal"
  }
 ]
};
