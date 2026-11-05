/* Pre-Algebra (7th) Unit 10 cheat sheet (Area and Volume). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "prealgebra7-area-volume",
 "course": "Pre-Algebra (7th)",
 "unitNo": 10,
 "unitName": "Area and Volume",
 "focus": "area of parallelograms, triangles, trapezoids and circles",
 "morefocus": "space figures, surface area and volume",
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
    ],
    [
     "Circle",
     "⟨A = \\pi r^2⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Parallelograms and Triangles",
   "kind": "example",
   "text": "Use the perpendicular height.",
   "example": "Triangle: base 14 m, height 9 m",
   "steps": [
    [
     "Half of bh:",
     "⟨\\tfrac{1}{2}(14)(9)⟩"
    ]
   ],
   "answer": "63 m²",
   "check": {
    "num": "0.5*14*9",
    "is": 63
   },
   "color": "blue"
  },
  {
   "title": "Trapezoids",
   "kind": "example",
   "text": "Average the bases times the height.",
   "example": "Bases 8 and 12 ft, height 5 ft",
   "steps": [
    [
     "Formula:",
     "⟨\\tfrac{1}{2}(8 + 12)(5)⟩"
    ]
   ],
   "answer": "50 ft²",
   "check": {
    "num": "0.5*(8+12)*5",
    "is": 50
   },
   "color": "green"
  },
  {
   "title": "Area of a Circle",
   "kind": "example",
   "text": "Square the radius first. Use π ≈ 3.14 unless told otherwise.",
   "example": "Diameter 10 in (use 3.14)",
   "steps": [
    [
     "Radius:",
     "5 in"
    ],
    [
     "Area:",
     "⟨3.14 \\cdot 5^2⟩"
    ]
   ],
   "answer": "78.5 in²",
   "check": {
    "num": "3.14*25",
    "is": 78.5
   },
   "color": "orange"
  },
  {
   "title": "Space Figures",
   "kind": "table",
   "plain": true,
   "head": [
    "Figure",
    "Faces · edges · vertices"
   ],
   "rows": [
    [
     "Cube",
     "6 · 12 · 8"
    ],
    [
     "Triangular prism",
     "5 · 9 · 6"
    ],
    [
     "Square pyramid",
     "5 · 8 · 5"
    ]
   ],
   "after": "Check Euler: F + V − E = 2.",
   "check": {
    "num": "6+8-12",
    "is": 2
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Area: square units. Volume: cubic units.",
    "Radius is half the diameter.",
    "Square the radius before multiplying by π."
   ],
   "bad": [
    [
     "Using d in ⟨\\pi r^2⟩",
     "halve it first"
    ],
    [
     "⟨(πr)^2⟩",
     "only r is squared"
    ],
    [
     "Slant height in prism volume",
     "use the perpendicular height"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Surface Area",
   "kind": "table",
   "plain": true,
   "head": [
    "Solid",
    "Surface area"
   ],
   "rows": [
    [
     "Prism",
     "sum of all faces (2B + Ph)"
    ],
    [
     "Cylinder",
     "⟨2\\pi r^2 + 2\\pi rh⟩"
    ],
    [
     "Pyramid",
     "⟨B + \\tfrac{1}{2}P\\ell⟩"
    ],
    [
     "Cone",
     "⟨\\pi r^2 + \\pi r\\ell⟩"
    ],
    [
     "Sphere",
     "⟨4\\pi r^2⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Surface Area of a Cylinder",
   "kind": "example",
   "text": "Two circles plus the curved rectangle.",
   "example": "r = 3 cm, h = 10 cm (in terms of π)",
   "steps": [
    [
     "Circles:",
     "⟨2\\pi(9) = 18\\pi⟩"
    ],
    [
     "Side:",
     "⟨2\\pi(3)(10) = 60\\pi⟩"
    ]
   ],
   "answer": "⟨78\\pi⟩ cm²",
   "check": {
    "num": "2*Math.PI*9+2*Math.PI*30",
    "is": 245.04422698000386
   },
   "color": "blue"
  },
  {
   "title": "Volume",
   "kind": "table",
   "plain": true,
   "head": [
    "Solid",
    "Volume"
   ],
   "rows": [
    [
     "Prism, cylinder",
     "V = Bh"
    ],
    [
     "Pyramid, cone",
     "⟨V = \\tfrac{1}{3}Bh⟩"
    ],
    [
     "Sphere",
     "⟨V = \\tfrac{4}{3}\\pi r^3⟩"
    ]
   ],
   "after": "B is the area of the base.",
   "color": "green"
  },
  {
   "title": "Volume of a Cone",
   "kind": "example",
   "text": "One third of the matching cylinder.",
   "example": "r = 6 in, h = 7 in (in terms of π)",
   "steps": [
    [
     "Formula:",
     "⟨\\tfrac{1}{3}\\pi(36)(7)⟩"
    ]
   ],
   "answer": "⟨84\\pi⟩ in³",
   "check": {
    "num": "Math.PI*36*7/3",
    "is": 263.89378290154264
   },
   "color": "orange"
  },
  {
   "title": "Volume of a Sphere",
   "kind": "example",
   "text": "⟨V = \\tfrac{4}{3}\\pi r^3⟩",
   "example": "r = 3 m (in terms of π)",
   "steps": [
    [
     "Cube:",
     "27"
    ],
    [
     "Multiply:",
     "⟨\\tfrac{4}{3} \\cdot 27 = 36⟩"
    ]
   ],
   "answer": "⟨36\\pi⟩ m³",
   "check": {
    "num": "4/3*Math.PI*27",
    "is": 113.09733552923255
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I use the radius, not the diameter?",
    "Did I include every face for surface area?",
    "Did I use ⅓ for pyramids and cones?",
    "Are my units squared or cubed?"
   ],
   "color": "teal"
  }
 ]
};
