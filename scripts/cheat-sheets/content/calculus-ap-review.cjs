/* Calculus Unit 9 cheat sheet (AP Review). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-ap-review",
 "course": "Calculus",
 "unitNo": 9,
 "unitName": "AP Review",
 "focus": "limits, derivatives and their applications",
 "morefocus": "integrals, FTC and free-response tips",
 "front": [
  {
   "title": "Limits and Continuity",
   "kind": "table",
   "plain": true,
   "head": [
    "Topic",
    "Key idea"
   ],
   "rows": [
    [
     "0/0",
     "factor, rationalize or L’Hôpital"
    ],
    [
     "Continuity",
     "f(a) = limit"
    ],
    [
     "IVT",
     "continuous → hits every value between"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Derivative Rules",
   "kind": "table",
   "plain": true,
   "head": [
    "Rule",
    "Formula"
   ],
   "rows": [
    [
     "Power",
     "⟨nx^{n-1}⟩"
    ],
    [
     "Product",
     "⟨f\\prime g + fg\\prime⟩"
    ],
    [
     "Quotient",
     "⟨\\tfrac{f\\prime g - fg\\prime}{g^2}⟩"
    ],
    [
     "Chain",
     "⟨f\\prime(g(x))g\\prime(x)⟩"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Mixed Derivative",
   "kind": "example",
   "text": "Chain inside product.",
   "example": "⟨y = x e^{2x}⟩",
   "steps": [
    [
     "Product:",
     "⟨e^{2x} + x \\cdot 2e^{2x}⟩"
    ]
   ],
   "answer": "⟨e^{2x}(1 + 2x)⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>x*Math.exp(2*x))(t+1e-6)-(x=>x*Math.exp(2*x))(t-1e-6))/2e-6-(x=>Math.exp(2*x)*(1+2*x))(t))<1e-5*(1+Math.abs((x=>Math.exp(2*x)*(1+2*x))(t))))"
   },
   "color": "green"
  },
  {
   "title": "What f′ and f″ Tell You",
   "kind": "table",
   "plain": true,
   "head": [
    "Sign",
    "f"
   ],
   "rows": [
    [
     "f′ > 0",
     "increasing"
    ],
    [
     "f′ changes + → −",
     "relative max"
    ],
    [
     "f″ > 0",
     "concave up"
    ],
    [
     "f″ changes sign",
     "inflection point"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Tangent Line Approximation",
   "kind": "example",
   "text": "⟨L(x) = f(a) + f\\prime(a)(x - a)⟩",
   "example": "f(2) = 5, f′(2) = −3. Estimate f(2.1).",
   "steps": [
    [
     "Compute:",
     "5 − 3(0.1)"
    ]
   ],
   "answer": "4.7",
   "check": {
    "num": "5-3*0.1",
    "is": 4.7
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Justify with calculus language (“because f′ changes from + to −”).",
    "Units on every answer in context.",
    "Three decimal places on the AP exam."
   ],
   "bad": [
    [
     "“The graph goes up”",
     "“f′(x) > 0 on …”"
    ],
    [
     "Rounding mid-problem",
     "store full values"
    ],
    [
     "Leaving out + C",
     "always include it"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Integral Toolkit",
   "kind": "table",
   "plain": true,
   "head": [
    "Integral",
    "Result"
   ],
   "rows": [
    [
     "⟨\\int x^n\\,dx⟩",
     "⟨\\tfrac{x^{n+1}}{n + 1} + C⟩"
    ],
    [
     "⟨\\int \\tfrac{1}{x}\\,dx⟩",
     "⟨\\ln|x| + C⟩"
    ],
    [
     "⟨\\int e^{kx}\\,dx⟩",
     "⟨\\tfrac{1}{k}e^{kx} + C⟩"
    ],
    [
     "u-substitution",
     "inside function u"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Definite Integral",
   "kind": "example",
   "text": "Antiderivative, top minus bottom.",
   "example": "⟨\\int_0^2 (3x^2 - 2x)\\,dx⟩",
   "steps": [
    [
     "Evaluate:",
     "⟨(8 - 4) - 0⟩"
    ]
   ],
   "answer": "4",
   "check": {
    "num": "8-4",
    "is": 4
   },
   "color": "blue"
  },
  {
   "title": "FTC and Accumulation",
   "kind": "table",
   "plain": true,
   "head": [
    "Idea",
    "Formula"
   ],
   "rows": [
    [
     "FTC 1",
     "⟨\\tfrac{d}{dx}\\int_a^x f(t)\\,dt = f(x)⟩"
    ],
    [
     "Net change",
     "⟨F(b) = F(a) + \\int_a^b F\\prime⟩"
    ],
    [
     "Average value",
     "⟨\\tfrac{1}{b - a}\\int_a^b f⟩"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Area and Volume",
   "kind": "table",
   "plain": true,
   "head": [
    "Find",
    "Integral"
   ],
   "rows": [
    [
     "Area",
     "⟨\\int (\\text{top} - \\text{bottom})\\,dx⟩"
    ],
    [
     "Washer",
     "⟨\\pi\\int (R^2 - r^2)\\,dx⟩"
    ],
    [
     "Cross sections",
     "⟨\\int A(x)\\,dx⟩"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Particle Motion FRQ",
   "kind": "example",
   "text": "Displacement = ∫v. Position = initial + ∫v.",
   "example": "v(t) = 2t − 4, s(0) = 3. Find s(5).",
   "steps": [
    [
     "Integrate:",
     "⟨\\int_0^5 (2t - 4)\\,dt = 25 - 20⟩"
    ]
   ],
   "answer": "s(5) = 8",
   "check": {
    "num": "3+(25-20)",
    "is": 8
   },
   "color": "pink"
  },
  {
   "title": "Free-Response Checklist",
   "kind": "list",
   "items": [
    "Show the setup: write the integral or derivative.",
    "Name the theorem (IVT, MVT, EVT, FTC) and check its conditions.",
    "Give units and interpret in context.",
    "Answer every part, even if an earlier part is wrong."
   ],
   "color": "teal"
  }
 ]
};
