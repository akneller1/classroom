/* Calculus Unit 3 cheat sheet (Derivatives). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-derivatives",
 "course": "Calculus",
 "unitNo": 3,
 "unitName": "Derivatives",
 "focus": "the definition of the derivative and basic rules",
 "morefocus": "product, quotient and chain rules, implicit and higher derivatives",
 "front": [
  {
   "title": "Limit Definition",
   "kind": "example",
   "text": "⟨f\\prime(x) = \\lim_{h \\to 0}\\tfrac{f(x + h) - f(x)}{h}⟩",
   "example": "⟨f(x) = x^2⟩",
   "steps": [
    [
     "Expand:",
     "⟨\\tfrac{2xh + h^2}{h} = 2x + h⟩"
    ]
   ],
   "answer": "⟨f\\prime(x) = 2x⟩",
   "check": {
    "true": "Math.abs(((3+1e-6)**2-9)/1e-6-6)<1e-4"
   },
   "color": "purple"
  },
  {
   "title": "Basic Rules",
   "kind": "table",
   "plain": true,
   "head": [
    "Function",
    "Derivative"
   ],
   "rows": [
    [
     "c",
     "0"
    ],
    [
     "⟨x^n⟩",
     "⟨nx^{n-1}⟩"
    ],
    [
     "⟨e^x⟩",
     "⟨e^x⟩"
    ],
    [
     "⟨\\ln x⟩",
     "⟨\\tfrac{1}{x}⟩"
    ],
    [
     "⟨a^x⟩",
     "⟨a^x\\ln a⟩"
    ]
   ],
   "color": "blue"
  },
  {
   "title": "Trig Derivatives",
   "kind": "table",
   "plain": true,
   "head": [
    "Function",
    "Derivative"
   ],
   "rows": [
    [
     "sin x",
     "cos x"
    ],
    [
     "cos x",
     "−sin x"
    ],
    [
     "tan x",
     "⟨\\sec^2 x⟩"
    ],
    [
     "sec x",
     "sec x tan x"
    ],
    [
     "csc x",
     "−csc x cot x"
    ],
    [
     "cot x",
     "⟨-\\csc^2 x⟩"
    ]
   ],
   "color": "green"
  },
  {
   "title": "Power Rule",
   "kind": "example",
   "text": "Rewrite roots and fractions as powers first.",
   "example": "⟨y = 4x^3 - \\tfrac{2}{x} + \\sqrt{x}⟩",
   "steps": [
    [
     "Rewrite:",
     "⟨4x^3 - 2x^{-1} + x^{1/2}⟩"
    ]
   ],
   "answer": "⟨12x^2 + \\tfrac{2}{x^2} + \\tfrac{1}{2\\sqrt{x}}⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>4*x**3-2/x+Math.sqrt(x))(t+1e-6)-(x=>4*x**3-2/x+Math.sqrt(x))(t-1e-6))/2e-6-(x=>12*x**2+2/x**2+1/(2*Math.sqrt(x)))(t))<1e-5*(1+Math.abs((x=>12*x**2+2/x**2+1/(2*Math.sqrt(x)))(t))))"
   },
   "color": "orange"
  },
  {
   "title": "Tangent Line",
   "kind": "example",
   "text": "⟨y - f(a) = f\\prime(a)(x - a)⟩",
   "example": "⟨f(x) = x^3⟩ at x = 2",
   "steps": [
    [
     "f(2), f′(2):",
     "8 and 12"
    ]
   ],
   "answer": "y − 8 = 12(x − 2)",
   "check": {
    "num": "3*2**2",
    "is": 12
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Derivative = slope of the tangent = instantaneous rate.",
    "Rewrite before differentiating.",
    "Differentiable ⇒ continuous (not the reverse)."
   ],
   "bad": [
    [
     "⟨(fg)\\prime = f\\prime g\\prime⟩",
     "⟨f\\prime g + fg\\prime⟩"
    ],
    [
     "⟨\\tfrac{d}{dx}e^{3x} = e^{3x}⟩",
     "⟨3e^{3x}⟩"
    ],
    [
     "Corners are differentiable",
     "not at a corner or cusp"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Product and Quotient Rules",
   "kind": "table",
   "plain": true,
   "head": [
    "Rule",
    "Formula"
   ],
   "rows": [
    [
     "Product",
     "⟨(fg)\\prime = f\\prime g + fg\\prime⟩"
    ],
    [
     "Quotient",
     "⟨(\\tfrac{f}{g})\\prime = \\tfrac{f\\prime g - fg\\prime}{g^2}⟩"
    ],
    [
     "Chain",
     "⟨(f(g(x)))\\prime = f\\prime(g(x))\\,g\\prime(x)⟩"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Product Rule",
   "kind": "example",
   "text": "First′ · second + first · second′.",
   "example": "⟨y = x^2 \\sin x⟩",
   "steps": [
    [
     "Apply:",
     "⟨2x\\sin x + x^2\\cos x⟩"
    ]
   ],
   "answer": "⟨2x\\sin x + x^2\\cos x⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>x**2*Math.sin(x))(t+1e-6)-(x=>x**2*Math.sin(x))(t-1e-6))/2e-6-(x=>2*x*Math.sin(x)+x**2*Math.cos(x))(t))<1e-5*(1+Math.abs((x=>2*x*Math.sin(x)+x**2*Math.cos(x))(t))))"
   },
   "color": "blue"
  },
  {
   "title": "Quotient Rule",
   "kind": "example",
   "text": "“Low d-high minus high d-low, over low squared.”",
   "example": "⟨y = \\tfrac{x}{x + 1}⟩",
   "steps": [
    [
     "Apply:",
     "⟨\\tfrac{(x + 1) - x}{(x + 1)^2}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{1}{(x + 1)^2}⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>x/(x+1))(t+1e-6)-(x=>x/(x+1))(t-1e-6))/2e-6-(x=>1/(x+1)**2)(t))<1e-5*(1+Math.abs((x=>1/(x+1)**2)(t))))"
   },
   "color": "green"
  },
  {
   "title": "Chain Rule",
   "kind": "example",
   "text": "Outside derivative (inside unchanged) × inside derivative.",
   "example": "⟨y = (3x^2 + 1)^5⟩",
   "steps": [
    [
     "Apply:",
     "⟨5(3x^2 + 1)^4 \\cdot 6x⟩"
    ]
   ],
   "answer": "⟨30x(3x^2 + 1)^4⟩",
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>(3*x**2+1)**5)(t+1e-6)-(x=>(3*x**2+1)**5)(t-1e-6))/2e-6-(x=>30*x*(3*x**2+1)**4)(t))<1e-5*(1+Math.abs((x=>30*x*(3*x**2+1)**4)(t))))"
   },
   "color": "orange"
  },
  {
   "title": "Implicit Differentiation",
   "kind": "example",
   "text": "Differentiate both sides; multiply y-terms by ⟨\\tfrac{dy}{dx}⟩.",
   "example": "⟨x^2 + y^2 = 25⟩",
   "steps": [
    [
     "Differentiate:",
     "⟨2x + 2y\\tfrac{dy}{dx} = 0⟩"
    ]
   ],
   "answer": "⟨\\tfrac{dy}{dx} = -\\tfrac{x}{y}⟩",
   "check": {
    "num": "-3/4",
    "is": -0.75
   },
   "color": "pink"
  },
  {
   "title": "Inverse Trig Derivatives",
   "kind": "table",
   "plain": true,
   "head": [
    "Function",
    "Derivative"
   ],
   "rows": [
    [
     "⟨\\sin^{-1}x⟩",
     "⟨\\tfrac{1}{\\sqrt{1 - x^2}}⟩"
    ],
    [
     "⟨\\tan^{-1}x⟩",
     "⟨\\tfrac{1}{1 + x^2}⟩"
    ],
    [
     "⟨\\cos^{-1}x⟩",
     "⟨-\\tfrac{1}{\\sqrt{1 - x^2}}⟩"
    ]
   ],
   "check": {
    "true": "[0.7,1.3,2.2].every(t=>Math.abs(((x=>Math.atan(x))(t+1e-6)-(x=>Math.atan(x))(t-1e-6))/2e-6-(x=>1/(1+x**2))(t))<1e-5*(1+Math.abs((x=>1/(1+x**2))(t))))"
   },
   "color": "teal"
  }
 ]
};
