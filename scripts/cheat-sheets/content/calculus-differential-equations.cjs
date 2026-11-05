/* Calculus Unit 8 cheat sheet (Differential Equations). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "calculus-differential-equations",
 "course": "Calculus",
 "unitNo": 8,
 "unitName": "Differential Equations",
 "focus": "slope fields and verifying solutions",
 "morefocus": "separation of variables and exponential growth and decay",
 "front": [
  {
   "title": "Key Vocabulary",
   "kind": "vocab",
   "rows": [
    [
     "differential equation",
     "Relates a function and its derivatives.",
     "⟨\\tfrac{dy}{dx} = 2y⟩"
    ],
    [
     "general solution",
     "Contains + C.",
     "⟨y = Ce^{2x}⟩"
    ],
    [
     "particular solution",
     "C found from an initial condition.",
     "⟨y = 3e^{2x}⟩"
    ],
    [
     "slope field",
     "Small slope segments at grid points.",
     "shows solution curves"
    ]
   ],
   "color": "purple"
  },
  {
   "title": "Verifying a Solution",
   "kind": "example",
   "text": "Differentiate and substitute.",
   "example": "Is ⟨y = e^{3x}⟩ a solution of y′ = 3y?",
   "steps": [
    [
     "y′:",
     "⟨3e^{3x} = 3y⟩ ✓"
    ]
   ],
   "answer": "Yes",
   "check": {
    "num": "3*Math.exp(0.6)-3*Math.exp(0.6)",
    "is": 0
   },
   "color": "blue"
  },
  {
   "title": "Slope at a Point",
   "kind": "example",
   "text": "Plug the point into dy/dx.",
   "example": "⟨\\tfrac{dy}{dx} = x - y⟩ at (3, 1)",
   "steps": [
    [
     "Compute:",
     "3 − 1"
    ]
   ],
   "answer": "slope 2",
   "check": {
    "num": "3-1",
    "is": 2
   },
   "color": "green"
  },
  {
   "title": "Reading Slope Fields",
   "kind": "words",
   "rows": [
    [
     "Slopes depend only on x",
     "same along vertical columns"
    ],
    [
     "Slopes depend only on y",
     "same along horizontal rows"
    ],
    [
     "dy/dx = 0",
     "horizontal segments (equilibrium if y = c)"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Euler’s Method",
   "kind": "example",
   "text": "⟨y_{new} = y + \\tfrac{dy}{dx}\\Delta x⟩",
   "example": "⟨\\tfrac{dy}{dx} = x + y⟩, y(0) = 1, Δx = 0.1. Estimate y(0.1).",
   "steps": [
    [
     "Step:",
     "1 + (0 + 1)(0.1)"
    ]
   ],
   "answer": "1.1",
   "check": {
    "num": "1+1*0.1",
    "is": 1.1
   },
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Slope fields show slope, not y-values.",
    "Particular solution: solve for C.",
    "Check the solution by differentiating."
   ],
   "bad": [
    [
     "Forgetting + C",
     "add C right after integrating"
    ],
    [
     "Plugging the point in before integrating",
     "integrate first"
    ],
    [
     "Confusing x and y in the slope",
     "use (x, y) in order"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Separation of Variables",
   "kind": "list",
   "items": [
    "1. Get all y’s with dy, all x’s with dx.",
    "2. Integrate both sides (+ C on one side).",
    "3. Use the initial condition to find C.",
    "4. Solve for y if possible."
   ],
   "color": "purple"
  },
  {
   "title": "Separating Variables",
   "kind": "example",
   "text": "Divide by y, multiply by dx.",
   "example": "⟨\\tfrac{dy}{dx} = xy⟩, y(0) = 2",
   "steps": [
    [
     "Separate:",
     "⟨\\int \\tfrac{dy}{y} = \\int x\\,dx⟩"
    ],
    [
     "Integrate:",
     "⟨\\ln|y| = \\tfrac{x^2}{2} + C⟩"
    ]
   ],
   "answer": "⟨y = 2e^{x^2/2}⟩",
   "check": {
    "num": "2*Math.exp(0)",
    "is": 2
   },
   "color": "blue"
  },
  {
   "title": "Another Separable Equation",
   "kind": "example",
   "text": "Separate, integrate, solve.",
   "example": "⟨\\tfrac{dy}{dx} = \\tfrac{x}{y}⟩, y(0) = 3",
   "steps": [
    [
     "Integrate:",
     "⟨\\tfrac{y^2}{2} = \\tfrac{x^2}{2} + C⟩"
    ],
    [
     "C:",
     "⟨\\tfrac{9}{2}⟩"
    ]
   ],
   "answer": "⟨y = \\sqrt{x^2 + 9}⟩",
   "check": {
    "num": "Math.sqrt(0+9)",
    "is": 3
   },
   "color": "green"
  },
  {
   "title": "Exponential Growth and Decay",
   "kind": "table",
   "plain": true,
   "head": [
    "Model",
    "Solution"
   ],
   "rows": [
    [
     "⟨\\tfrac{dy}{dt} = ky⟩",
     "⟨y = y_0e^{kt}⟩"
    ],
    [
     "k > 0",
     "growth"
    ],
    [
     "k < 0",
     "decay"
    ]
   ],
   "color": "orange"
  },
  {
   "title": "Half-Life",
   "kind": "example",
   "text": "Use the half-life to find k: ⟨\\tfrac{1}{2} = e^{kT}⟩.",
   "example": "Half-life 10 years; 80 g at t = 0. Amount at t = 30?",
   "steps": [
    [
     "Three half-lives:",
     "⟨80(\\tfrac{1}{2})^3⟩"
    ]
   ],
   "answer": "10 g",
   "check": {
    "num": "80*0.5**3",
    "is": 10
   },
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I separate before integrating?",
    "Did I add + C and solve for it?",
    "Is my k positive for growth, negative for decay?",
    "Does my solution pass through the initial point?"
   ],
   "color": "teal"
  }
 ]
};
