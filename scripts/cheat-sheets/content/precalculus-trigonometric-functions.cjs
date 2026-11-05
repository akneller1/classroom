/* Precalculus Unit 4 cheat sheet (Trigonometric Functions). Every worked example is checked by build.cjs. */
module.exports = {
 "name": "precalculus-trigonometric-functions",
 "course": "Precalculus",
 "unitNo": 4,
 "unitName": "Trigonometric Functions",
 "focus": "angles, radians, the unit circle and graphs",
 "morefocus": "inverse trig functions, identities and trig equations",
 "front": [
  {
   "title": "Degrees and Radians",
   "kind": "example",
   "text": "Multiply by ⟨\\tfrac{\\pi}{180}⟩ or ⟨\\tfrac{180}{\\pi}⟩.",
   "example": "Convert 150° and ⟨\\tfrac{5\\pi}{4}⟩.",
   "steps": [
    [
     "150° · π ÷ 180:",
     "⟨\\tfrac{5\\pi}{6}⟩"
    ]
   ],
   "answer": "⟨\\tfrac{5\\pi}{6}⟩ and 225°",
   "check": [
    {
     "num": "150*Math.PI/180",
     "is": 2.6179938779914944
    },
    {
     "num": "5/4*180",
     "is": 225
    }
   ],
   "color": "purple"
  },
  {
   "title": "Unit Circle Values",
   "kind": "table",
   "plain": true,
   "head": [
    "θ",
    "cos θ · sin θ"
   ],
   "rows": [
    [
     "0",
     "1 · 0"
    ],
    [
     "⟨\\tfrac{\\pi}{6}⟩",
     "⟨\\tfrac{\\sqrt{3}}{2}⟩ · ⟨\\tfrac{1}{2}⟩"
    ],
    [
     "⟨\\tfrac{\\pi}{4}⟩",
     "⟨\\tfrac{\\sqrt{2}}{2}⟩ · ⟨\\tfrac{\\sqrt{2}}{2}⟩"
    ],
    [
     "⟨\\tfrac{\\pi}{3}⟩",
     "⟨\\tfrac{1}{2}⟩ · ⟨\\tfrac{\\sqrt{3}}{2}⟩"
    ],
    [
     "⟨\\tfrac{\\pi}{2}⟩",
     "0 · 1"
    ]
   ],
   "after": "ASTC: All, Sin, Tan, Cos positive in quadrants I–IV.",
   "check": {
    "num": "Math.sin(Math.PI/6)",
    "is": 0.5
   },
   "color": "blue"
  },
  {
   "title": "Reference Angles",
   "kind": "example",
   "text": "Use the reference angle, then the quadrant sign.",
   "example": "⟨\\cos\\tfrac{2\\pi}{3}⟩",
   "steps": [
    [
     "Reference:",
     "⟨\\tfrac{\\pi}{3}⟩, quadrant II (cos −)"
    ]
   ],
   "answer": "⟨-\\tfrac{1}{2}⟩",
   "check": {
    "num": "Math.cos(2*Math.PI/3)",
    "is": -0.5
   },
   "color": "green"
  },
  {
   "title": "Sinusoid Graphs",
   "kind": "table",
   "plain": true,
   "head": [
    "⟨y = A\\sin(B(x - C)) + D⟩",
    "Meaning"
   ],
   "rows": [
    [
     "|A|",
     "amplitude"
    ],
    [
     "⟨\\tfrac{2\\pi}{B}⟩",
     "period"
    ],
    [
     "C",
     "phase shift"
    ],
    [
     "D",
     "midline y = D"
    ]
   ],
   "after": "⟨y = 3\\sin 2x - 1⟩: amplitude 3, period π, midline y = −1.",
   "color": "orange"
  },
  {
   "title": "Arc Length and Sector Area",
   "kind": "example",
   "text": "⟨s = r\\theta⟩, ⟨A = \\tfrac{1}{2}r^2\\theta⟩ (θ in radians).",
   "example": "r = 6, ⟨\\theta = \\tfrac{\\pi}{3}⟩",
   "steps": [
    [
     "Arc:",
     "⟨6 \\cdot \\tfrac{\\pi}{3}⟩"
    ],
    [
     "Area:",
     "⟨\\tfrac{1}{2}(36)\\tfrac{\\pi}{3}⟩"
    ]
   ],
   "answer": "⟨s = 2\\pi⟩, ⟨A = 6\\pi⟩",
   "check": [
    {
     "num": "6*Math.PI/3",
     "is": 6.283185307179586
    },
    {
     "num": "0.5*36*Math.PI/3",
     "is": 18.84955592153876
    }
   ],
   "color": "pink"
  },
  {
   "title": "Quick Reminders & Common Mistakes",
   "kind": "mistakes",
   "good": [
    "Check degree/radian mode.",
    "tan θ = ⟨\\tfrac{\\sin\\theta}{\\cos\\theta}⟩.",
    "Period of tan is π, not 2π."
   ],
   "bad": [
    [
     "Period of sin 2x = 4π",
     "π"
    ],
    [
     "s = rθ with θ in degrees",
     "radians"
    ],
    [
     "cos 120° = ½",
     "−½ (quadrant II)"
    ]
   ],
   "color": "teal"
  }
 ],
 "back": [
  {
   "title": "Inverse Trig Ranges",
   "kind": "table",
   "plain": true,
   "head": [
    "Function",
    "Range"
   ],
   "rows": [
    [
     "⟨\\sin^{-1}x⟩",
     "⟨[-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}]⟩"
    ],
    [
     "⟨\\cos^{-1}x⟩",
     "[0, π]"
    ],
    [
     "⟨\\tan^{-1}x⟩",
     "⟨(-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2})⟩"
    ]
   ],
   "after": "⟨\\cos^{-1}(-\\tfrac{1}{2}) = \\tfrac{2\\pi}{3}⟩",
   "check": {
    "num": "Math.acos(-0.5)",
    "is": 2.0943951023931953
   },
   "color": "purple"
  },
  {
   "title": "Fundamental Identities",
   "kind": "table",
   "plain": true,
   "head": [
    "Type",
    "Identity"
   ],
   "rows": [
    [
     "Pythagorean",
     "⟨\\sin^2\\theta + \\cos^2\\theta = 1⟩"
    ],
    [
     "",
     "⟨1 + \\tan^2\\theta = \\sec^2\\theta⟩"
    ],
    [
     "Reciprocal",
     "⟨\\csc\\theta = \\tfrac{1}{\\sin\\theta}⟩, ⟨\\sec\\theta = \\tfrac{1}{\\cos\\theta}⟩"
    ],
    [
     "Even/odd",
     "cos(−θ) = cos θ, sin(−θ) = −sin θ"
    ]
   ],
   "check": {
    "num": "Math.sin(1)**2+Math.cos(1)**2",
    "is": 1
   },
   "color": "blue"
  },
  {
   "title": "Sum and Double-Angle",
   "kind": "table",
   "plain": true,
   "head": [
    "Formula",
    "Expansion"
   ],
   "rows": [
    [
     "sin(A ± B)",
     "sin A cos B ± cos A sin B"
    ],
    [
     "cos(A ± B)",
     "cos A cos B ∓ sin A sin B"
    ],
    [
     "sin 2θ",
     "2 sin θ cos θ"
    ],
    [
     "cos 2θ",
     "⟨\\cos^2\\theta - \\sin^2\\theta = 1 - 2\\sin^2\\theta⟩"
    ]
   ],
   "check": {
    "num": "Math.sin(2*0.7)-2*Math.sin(0.7)*Math.cos(0.7)",
    "is": 0
   },
   "color": "green"
  },
  {
   "title": "Verifying an Identity",
   "kind": "example",
   "text": "Work one side; rewrite in sines and cosines.",
   "example": "⟨\\tan\\theta\\cos\\theta = \\sin\\theta⟩",
   "steps": [
    [
     "Rewrite:",
     "⟨\\tfrac{\\sin\\theta}{\\cos\\theta} \\cdot \\cos\\theta⟩"
    ]
   ],
   "answer": "sin θ ✓",
   "check": {
    "num": "Math.tan(0.4)*Math.cos(0.4)-Math.sin(0.4)",
    "is": 0
   },
   "color": "orange"
  },
  {
   "title": "Solving Trig Equations",
   "kind": "example",
   "text": "Isolate the trig function; find ALL solutions in [0, 2π).",
   "example": "⟨2\\sin\\theta - 1 = 0⟩",
   "steps": [
    [
     "sin θ = ½:",
     "quadrants I and II"
    ]
   ],
   "answer": "⟨\\theta = \\tfrac{\\pi}{6}, \\tfrac{5\\pi}{6}⟩",
   "check": [
    {
     "num": "2*Math.sin(Math.PI/6)-1",
     "is": 0
    },
    {
     "num": "2*Math.sin(5*Math.PI/6)-1",
     "is": 0
    }
   ],
   "color": "pink"
  },
  {
   "title": "Check Yourself",
   "kind": "list",
   "items": [
    "Did I find every solution in the interval?",
    "Is my inverse-trig answer in the right range?",
    "Did I keep θ in radians where needed?",
    "Did I avoid dividing by a trig function (losing solutions)?"
   ],
   "color": "teal"
  }
 ]
};
