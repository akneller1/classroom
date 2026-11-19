# Teaching notes, units 1–3. Each record: obj, idea, voc [[word, meaning]…], watch, cards [{h, big, steps}].
# Math in ⟨TeX⟩; {{…}} = blank on guided notes.
PR = 'precalculus-review'
LC = 'limits-continuity'
DV = 'derivatives'
R = {}

R[PR, 1] = dict(obj='factor polynomials completely and simplify rational expressions before doing calculus with them',
  idea='Factor out the GCF first, then look for a pattern; a factor that appears on top and bottom of a fraction cancels only when it multiplies everything.',
  voc=[['greatest common factor (GCF)', 'The largest factor every term shares, such as 2x in 4x² + 6x.'], ['difference of squares', 'a² − b² = (a − b)(a + b).'], ['sum or difference of cubes', 'a³ ± b³ = (a ± b)(a² ∓ ab + b²).']],
  watch='Canceling terms instead of factors: (x² + 3)/x is not x + 3.',
  cards=[dict(h='Factoring in order', big='Always pull out the {{GCF}} first. Then try a trinomial, a difference of squares, cubes, or grouping.',
    steps=['⟨x^2 - 8x + 15⟩: two numbers with product 15 and sum −8 are ⟨{{-3}}⟩ and ⟨-5⟩, so ⟨(x - 3)(x - 5)⟩.', '⟨27x^3 - 27 = 27(x^3 - 1) = {{27(x - 1)(x^2 + x + 1)}}⟩.', 'Grouping: ⟨x^3 + 2x^2 + 6x + 12 = x^2(x + 2) + 6(x + 2) = {{(x + 2)(x^2 + 6)}}⟩.'])])

R[PR, 2] = dict(obj='evaluate, rewrite and solve exponential expressions and equations, including those with base e',
  idea='Exponent rules let you combine powers of the same base; to solve, write both sides with the same base or take a logarithm.',
  voc=[['base e', 'The number e ≈ 2.718, the base of natural growth.'], ['exponential function', 'f(x) = abˣ with b > 0, b ≠ 1.']],
  watch='Multiplying the base instead of the exponent, as in (e²)³ = e⁵ (it is e⁶).',
  cards=[dict(h='Same base, equal exponents', big='If ⟨b^u = b^v⟩ then ⟨u = v⟩. Rewrite each side as a power of the {{same base}}.',
    steps=['⟨5^{x - 4} = 25 = 5^2⟩, so ⟨x - 4 = 2⟩ and ⟨x = {{6}}⟩.', '⟨e^{4x} \\div e^{2x} = {{e^{2x}}}⟩ because exponents subtract when dividing.', 'When the bases cannot match, take ⟨\\ln⟩ of both sides: ⟨e^{3x} = 31⟩ gives ⟨x = \\tfrac{1}{3}\\ln 31⟩.'])])

R[PR, 3] = dict(obj='evaluate logarithms and use the properties of logarithms to expand, condense and solve',
  idea='A logarithm is an exponent: log_b(N) = k means bᵏ = N. ln is log base e.',
  voc=[['logarithm', 'The exponent you put on a base to get a number.'], ['natural logarithm', 'ln x = logₑ x.'], ['power property', 'ln(Mᵖ) = p·ln M.']],
  watch='Writing ln(M + N) = ln M + ln N; the product rule is ln(MN) = ln M + ln N.',
  cards=[dict(h='Logs undo exponents', big='⟨\\log_b N = k⟩ means ⟨b^k = N⟩. So ⟨\\ln 1 = {{0}}⟩ and ⟨\\ln e = 1⟩.',
    steps=['⟨\\log_2 8 = {{3}}⟩ because ⟨2^3 = 8⟩.', 'Expand: ⟨\\ln\\frac{x^2}{y^5} = 2\\ln x - {{5\\ln y}}⟩.', 'Condense: ⟨4\\ln x - \\ln 4 = \\ln\\frac{x^4}{4}⟩.'])])

R[PR, 4] = dict(obj='find exact values of the six trigonometric functions at special angles in degrees and radians',
  idea='On the unit circle, the point at angle θ is (cos θ, sin θ); a reference angle and the quadrant give every special value.',
  voc=[['unit circle', 'The circle of radius 1 centered at the origin.'], ['reference angle', 'The acute angle between the terminal side and the x-axis.'], ['radian', 'The angle that cuts off an arc equal to the radius; π radians = 180°.']],
  watch='Using the wrong sign for the quadrant, such as sin(16π/3) = +√3/2 (it is −√3/2).',
  cards=[dict(h='Reference angle, then sign', big='Find the {{reference angle}}, read the value from the first quadrant, then attach the sign for the quadrant (All, Sine, Tangent, Cosine).',
    steps=['⟨\\tan 120°⟩: reference angle 60°, Quadrant II where tangent is negative, so ⟨{{-\\sqrt{3}}}⟩.', '⟨\\cos(-\\pi)⟩: the point at ⟨-\\pi⟩ is ⟨(-1, 0)⟩, so ⟨\\cos(-\\pi) = {{-1}}⟩.', '⟨\\sec\\tfrac{\\pi}{4} = \\frac{1}{\\cos(\\pi/4)} = \\sqrt{2}⟩.'])])

R[PR, 5] = dict(obj='move between graphs, tables and formulas and compute average rates of change',
  idea='The average rate of change on [a, b] is the slope of the secant line: (f(b) − f(a))/(b − a), whatever form f is given in.',
  voc=[['average rate of change', '(f(b) − f(a))/(b − a), the slope between two points.'], ['secant line', 'The line through two points of a graph.']],
  watch='Forgetting to divide by b − a, or subtracting the outputs in one order and the inputs in the other.',
  cards=[dict(h='Slope between two points', big='Average rate of change ⟨= \\frac{f(b) - f(a)}{b - a}⟩: the {{slope}} of the secant line.',
    steps=['⟨f(x) = -x^2 + 4x⟩ on ⟨[1, 7]⟩: ⟨\\frac{f(7) - f(1)}{7 - 1} = \\frac{-21 - 3}{6} = {{-4}}⟩.', 'From a table with ⟨f(2) = 31⟩ and ⟨f(4) = -20⟩: ⟨\\frac{-20 - 31}{4 - 2} = {{-\\tfrac{51}{2}}}⟩.'])])

R[LC, 1] = dict(obj='read and write limit notation, including one-sided and infinite limits',
  idea='lim (x → a) f(x) = L says f(x) gets as close to L as we like when x is close enough to a; it says nothing about f(a) itself.',
  voc=[['limit', 'The value f(x) approaches as x approaches a.'], ['one-sided limit', 'A limit from the left (x → a⁻) or the right (x → a⁺).'], ['infinite limit', 'f(x) grows without bound, written lim f(x) = ∞; the limit does not exist as a number.']],
  watch='Reading lim (x → a) f(x) as the value f(a).',
  cards=[dict(h='Reading limit notation', big='⟨\\lim_{x \\to a} f(x) = L⟩ describes what f {{approaches}} near ⟨a⟩, not its value at ⟨a⟩.',
    steps=['⟨\\lim_{x \\to 5^+} f(x) = -7⟩: as x approaches 5 from the {{right}}, f(x) approaches −7.', '⟨\\lim_{x \\to 4} f(x) = \\infty⟩: f grows without bound near 4, so x = 4 is a {{vertical asymptote}}.', 'For a polynomial, substitution works: ⟨\\lim_{x \\to 3}(2x^2 + 5x + 5) = 38⟩.'])])

R[LC, 2] = dict(obj='estimate limits from graphs and from tables of values on both sides of a point',
  idea='Read the y-value the graph heads toward from each side; in a table, use the values closest to a, not the farthest ones.',
  voc=[['open circle', 'A point the graph approaches but does not include.'], ['two-sided limit', 'Exists only when the left and right limits are equal.']],
  watch='Using f(a) (the solid dot) instead of where the graph is heading.',
  cards=[dict(h='Left, right, then compare', big='Find the {{left-hand}} and right-hand limits separately. The two-sided limit exists only if they {{match}}.',
    steps=['Table: ⟨f(-2.01) \\approx 1.99⟩, ⟨f(-1.99) \\approx 2.01⟩, so ⟨\\lim_{x \\to -2} f(x) = {{2}}⟩.', 'Graph: from the left −2, from the right −1, so the limit {{does not exist}}, whatever the solid dot shows.'])])

R[LC, 3] = dict(obj='evaluate limits algebraically by substitution, factoring, rationalizing and combining fractions',
  idea='Try direct substitution first. A result of 0/0 means more algebra is needed: cancel the common factor, then substitute again.',
  voc=[['indeterminate form', '0/0 (or ∞/∞): substitution does not decide the limit.'], ['removable factor', 'A factor that cancels from the top and bottom.']],
  watch='Treating 0/0 as 0, or as "does not exist".',
  cards=[dict(h='0/0 means factor and cancel', big='If substitution gives ⟨\\frac{0}{0}⟩, {{factor}} and cancel the common factor; the limit of what remains is the answer.',
    steps=['⟨\\lim_{x \\to -3}\\frac{x^2 - 9}{x + 3} = \\lim_{x \\to -3}(x - 3) = {{-6}}⟩.', '⟨\\lim_{x \\to 2}\\frac{x^3 - 8}{x - 2} = \\lim_{x \\to 2}(x^2 + 2x + 4) = {{12}}⟩.', '⟨\\lim_{x \\to 0}\\frac{\\sin(3x)}{x} = 3⟩, using ⟨\\lim_{x \\to 0}\\frac{\\sin x}{x} = 1⟩.'])])

R[LC, 4] = dict(obj='find one-sided and two-sided limits of piecewise functions and infinite one-sided limits',
  idea='Each one-sided limit uses only the piece of the function on that side of a.',
  voc=[['piecewise function', 'A function defined by different formulas on different intervals.'], ['left-hand limit', 'lim (x → a⁻), using x < a.']],
  watch='Plugging a into the wrong piece, or adding the two sides together.',
  cards=[dict(h='One piece per side', big='Left limit: use the piece for ⟨x < a⟩. Right limit: use the piece for ⟨x \\ge a⟩. Equal values mean the {{two-sided}} limit exists.',
    steps=['⟨f(x) = -3x - 1⟩ for ⟨x < -3⟩: ⟨\\lim_{x \\to -3^-} f(x) = -3(-3) - 1 = {{8}}⟩.', '⟨\\lim_{x \\to 2^+}\\frac{-2}{(x - 2)^2}⟩: the bottom is a tiny positive number, so the limit is {{negative infinity}}.'])])

R[LC, 5] = dict(obj='use limits at infinity and infinite limits to describe end behavior and asymptotes',
  idea='For rational functions, the highest powers decide the limit at infinity: equal degrees give the ratio of leading coefficients, a bigger bottom gives 0.',
  voc=[['horizontal asymptote', 'y = L where lim (x → ±∞) f(x) = L.'], ['vertical asymptote', 'x = a where f(x) → ±∞ as x → a.'], ['end behavior', 'What f(x) does as x → ±∞.']],
  watch='Using the constant terms, or assuming every limit at infinity is 0.',
  cards=[dict(h='Compare the degrees', big='As ⟨x \\to \\infty⟩ only the {{leading terms}} matter.',
    steps=['⟨\\lim_{x \\to \\infty}\\frac{6x^3 - 3x^2 + 3}{5x^3 - 1} = {{\\tfrac{6}{5}}}⟩ (equal degrees).', '⟨\\lim_{x \\to \\infty}\\frac{-6x}{4x^3} = {{0}}⟩ (bottom-heavy).', '⟨\\lim_{x \\to \\infty}\\frac{x^3 - 3x^2 + 5}{x - 3} = \\infty⟩ (top-heavy).'])])

R[LC, 6] = dict(obj='use the three-part definition of continuity to test a point and to find intervals of continuity',
  idea='f is continuous at a when f(a) exists, the limit exists, and they are equal; a parameter can be chosen to make the pieces meet.',
  voc=[['continuous at a', 'lim (x → a) f(x) = f(a).'], ['continuous on an interval', 'Continuous at every point of the interval.']],
  watch='Checking only that f(a) exists, or only that the two pieces have the same slope.',
  cards=[dict(h='Make the pieces meet', big='At the break point, set the left piece equal to the right piece and solve for the {{parameter}}.',
    steps=['⟨3x + 2⟩ for ⟨x < -1⟩ and ⟨3x + k⟩ for ⟨x \\ge -1⟩: ⟨-1 = -3 + k⟩, so ⟨k = {{2}}⟩.', '⟨2x^2 + x⟩ for ⟨x < 3⟩ and ⟨kx + 2⟩: ⟨21 = 3k + 2⟩, so ⟨k = {{\\tfrac{19}{3}}}⟩.'])])

R[LC, 7] = dict(obj='classify discontinuities as removable, jump or infinite and locate holes',
  idea='A factor that cancels gives a hole (removable); a factor left in the denominator gives a vertical asymptote (infinite); unequal one-sided limits give a jump.',
  voc=[['removable discontinuity', 'A hole: the limit exists but f(a) is missing or different.'], ['jump discontinuity', 'The one-sided limits exist but are different.'], ['infinite discontinuity', 'f(x) → ±∞ near a.']],
  watch='Using a zero of the numerator as the hole, or giving the hole a y-value of 0.',
  cards=[dict(h='Find the hole', big='Factor, cancel the common factor, and substitute into what remains to get the hole’s {{y-value}}.',
    steps=['⟨\\frac{x^2 + 7x + 10}{x + 2} = x + 5⟩ for ⟨x \\ne -2⟩, so the hole is at ⟨({{-2}}, 3)⟩.', '⟨\\frac{2x^2 - 6x}{x^2 - 5x} = \\frac{2(x - 3)}{x - 5}⟩: hole at ⟨x = 0⟩ with ⟨y = \\tfrac{6}{5}⟩; ⟨x = 5⟩ is a {{vertical asymptote}}.'])])

R[LC, 8] = dict(obj='apply the Intermediate Value Theorem and the Extreme Value Theorem and state their conditions',
  idea='Continuity on a closed interval is the key hypothesis: the IVT guarantees every value between f(a) and f(b), and the EVT guarantees an absolute maximum and minimum.',
  voc=[['Intermediate Value Theorem', 'If f is continuous on [a, b], it takes every value between f(a) and f(b).'], ['Extreme Value Theorem', 'If f is continuous on [a, b], it has an absolute max and min there.']],
  watch='Using the IVT to count solutions exactly; it only guarantees at least as many as there are sign changes.',
  cards=[dict(h='Count the guaranteed solutions', big='Each pair of consecutive table values on opposite sides of the target guarantees {{at least one}} solution between them.',
    steps=['f(2) = 6, f(5) = −4, f(7) = 5, f(9) = −4, target −3: three sign changes, so the IVT guarantees at least {{3}} solutions.', 'f(x) = 1/(x − 1/2) on [−2, 3]: not {{continuous}} at x = 1/2, so the EVT does not apply.'])])

R[DV, 1] = dict(obj='find derivatives from the limit definition and recognize a limit as a derivative',
  idea='f′(a) = lim (h → 0) (f(a + h) − f(a))/h is the slope of the tangent line: the limit of secant slopes.',
  voc=[['difference quotient', '(f(a + h) − f(a))/h, the slope of a secant line.'], ['derivative at a', 'f′(a), the limit of the difference quotient as h → 0.']],
  watch='Forgetting to divide by h, or expanding (a + h)² as a² + h².',
  cards=[dict(h='The definition step by step', big='Expand ⟨f(a + h) - f(a)⟩, {{divide by h}}, then let ⟨h \\to 0⟩.',
    steps=['⟨f(x) = -2x^2 + 2x - 2⟩, ⟨a = 1⟩: ⟨f(1 + h) - f(1) = -2h^2 - 2h⟩.', 'Divide by ⟨h⟩: ⟨-2h - 2⟩. Let ⟨h \\to 0⟩: ⟨f\'(1) = {{-2}}⟩.', '⟨\\lim_{h \\to 0}\\frac{(2 + h)^4 - 16}{h}⟩ is ⟨f\'(2)⟩ for ⟨f(x) = x^4⟩, which is ⟨{{32}}⟩.'])])

R[DV, 2] = dict(obj='estimate derivatives from tables and graphs using difference quotients',
  idea='With data on both sides of a point, the symmetric difference quotient (f(b) − f(a))/(b − a) estimates the derivative at the middle point.',
  voc=[['symmetric difference quotient', '(f(a + h) − f(a − h))/(2h), the slope across a point.'], ['estimate', 'An approximation, not an exact value.']],
  watch='Reporting a function value instead of a slope.',
  cards=[dict(h='Slope across the point', big='Use the closest table values on {{either side}} of the point and compute their slope.',
    steps=['f(6) = 58, f(15) = −14: ⟨f\'(7) \\approx \\frac{-14 - 58}{15 - 6} = {{-8}}⟩.', 'With ⟨h = 0.001⟩: ⟨f\'(2) \\approx \\frac{f(2.001) - f(1.999)}{0.002}⟩.'])])

R[DV, 3] = dict(obj='differentiate polynomials, powers, exponentials, logarithms and trig functions with the sum, product and quotient rules',
  idea='Rewrite roots and reciprocals as powers, then use the power rule term by term; use the product and quotient rules for products and quotients.',
  voc=[['power rule', 'd/dx xⁿ = nxⁿ⁻¹.'], ['product rule', '(uv)′ = u′v + uv′.'], ['quotient rule', '(u/v)′ = (u′v − uv′)/v².']],
  watch='Differentiating a product factor by factor, (uv)′ = u′v′.',
  cards=[dict(h='Rewrite, then differentiate', big='⟨\\sqrt{x} = x^{1/2}⟩ and ⟨\\frac{1}{x} = x^{-1}⟩. Then ⟨\\frac{d}{dx}x^n = {{nx^{n-1}}}⟩.',
    steps=['⟨f(x) = 5\\sqrt{x} - \\frac{2}{x}⟩: ⟨f\'(x) = \\frac{5}{2\\sqrt{x}} + {{\\frac{2}{x^2}}}⟩.', '⟨f(x) = x^2 e^{-2x}⟩: ⟨f\'(x) = 2xe^{-2x} - 2x^2e^{-2x}⟩.', '⟨\\frac{d}{dx}\\ln x = {{\\frac{1}{x}}}⟩ and ⟨\\frac{d}{dx}\\sin x = \\cos x⟩.'])])

R[DV, 4] = dict(obj='find second and higher derivatives and use them for acceleration',
  idea='Each derivative is the rate of change of the one before: s′ = v and s″ = v′ = a.',
  voc=[['second derivative', 'f″, the derivative of f′.'], ['acceleration', 'a(t) = v′(t) = s″(t).']],
  watch='Stopping after one derivative, or dropping a negative sign along the way.',
  cards=[dict(h='Differentiate again', big='⟨f\'\'⟩ is the derivative of {{the first derivative}}.',
    steps=['⟨f(x) = -5x^4 - 8x⟩: ⟨f\'(x) = -20x^3 - 8⟩, ⟨f\'\'(x) = {{-60x^2}}⟩.', '⟨s(t) = -2t^3 + 4t^2 + 9t + 14⟩: ⟨a(t) = s\'\'(t) = -12t + 8⟩, so ⟨a(1) = {{-4}}⟩ m/s².'])])

R[DV, 5] = dict(obj='explain the link between differentiability and continuity and decide where a function is differentiable',
  idea='Differentiable implies continuous, but not the reverse: corners, cusps, vertical tangents and jumps all block differentiability.',
  voc=[['differentiable at a', 'f′(a) exists: the one-sided slopes match and are finite.'], ['cusp', 'A sharp point where the slopes go to +∞ on one side and −∞ on the other.'], ['corner', 'A point where the left and right slopes are different numbers.']],
  watch='Thinking a continuous function must be differentiable (|x| at 0 is not).',
  cards=[dict(h='Match the values, then the slopes', big='For ⟨f⟩ to be differentiable at a break point, the pieces must meet ({{continuity}}) and have the same slope.',
    steps=['⟨x^2⟩ for ⟨x \\le 3⟩, ⟨mx + b⟩ for ⟨x > 3⟩: slopes ⟨m = 2(3) = {{6}}⟩.', 'Values: ⟨6(3) + b = 9⟩, so ⟨b = {{-9}}⟩.', '⟨(x - 2)^{2/3}⟩ at ⟨x = 2⟩: continuous but has a cusp, so not differentiable.'])])

R[DV, 6] = dict(obj='write the equation of a tangent line and use it to approximate values (local linearization)',
  idea='The tangent line at a is L(x) = f(a) + f′(a)(x − a); near a, L(x) is close to f(x).',
  voc=[['tangent line', 'The line through (a, f(a)) with slope f′(a).'], ['local linearization', 'Using L(x) to approximate f(x) near a.']],
  watch='Using f(a) as the y-intercept instead of using point-slope form.',
  cards=[dict(h='Point and slope', big='⟨L(x) = f(a) + f\'(a)(x - a)⟩: the point is ⟨(a, f(a))⟩ and the slope is {{the derivative at a}}.',
    steps=['⟨f(x) = -5x^2 - 8x⟩ at ⟨x = -1⟩: ⟨f(-1) = 3⟩, ⟨f\'(-1) = 2⟩, so ⟨y = 2x + {{5}}⟩.', '⟨\\sqrt{9.3} \\approx 3 + \\frac{1}{6}(0.3) = {{3.05}}⟩, an overestimate because ⟨\\sqrt{x}⟩ is concave down.'])])

R[DV, 7] = dict(obj='connect the graph and sign of f′ to where f increases and decreases',
  idea='f increases where f′ > 0 and decreases where f′ < 0; f′ changes sign at the turning points of f.',
  voc=[['sign chart', 'A number line showing where f′ is positive or negative.'], ['critical number', 'An x where f′ = 0 or f′ is undefined.']],
  watch='Reading where f′ is increasing instead of where f′ is positive.',
  cards=[dict(h='Signs of f′', big='Factor ⟨f\'⟩, mark its zeros, and test each interval: positive means f is {{increasing}}.',
    steps=['⟨f\'(x) = x^2 - 2x - 8 = (x + 2)(x - 4)⟩: negative on ⟨({{-2}}, 4)⟩, so f decreases there.', '⟨f\'(x) = x^2(x - 3)⟩: the square does not change sign, so f increases only on ⟨({{3}}, \\infty)⟩.'])])

R[DV, 8] = dict(obj='differentiate compositions with the chain rule, including from tables',
  idea='Differentiate the outside function, keep the inside, then multiply by the derivative of the inside.',
  voc=[['composition', 'f(g(x)): g is the inside function, f the outside.'], ['chain rule', '(f(g(x)))′ = f′(g(x))·g′(x).']],
  watch='Forgetting the factor g′(x), or evaluating f′ at x instead of at g(x).',
  cards=[dict(h='Outside, inside, times inside′', big='⟨\\frac{d}{dx}f(g(x)) = f\'(g(x))\\cdot{{g\'(x)}}⟩.',
    steps=['⟨\\frac{d}{dx}e^{3x - 3} = {{3}}e^{3x - 3}⟩.', '⟨(x^2 + 3)^5⟩: ⟨5(x^2 + 3)^4 \\cdot 2x = 10x(x^2 + 3)^4⟩.', 'Table: ⟨h = f\\circ g⟩, ⟨g(-3) = 5⟩, ⟨g\'(-3) = 3⟩, ⟨f\'(5) = -6⟩: ⟨h\'(-3) = f\'(5)\\cdot 3 = {{-18}}⟩.'])])

R[DV, 9] = dict(obj='differentiate implicitly to find dy/dx and second derivatives of implicit relations',
  idea='Differentiate both sides with respect to x, treating y as a function of x: every y-term picks up a factor dy/dx.',
  voc=[['implicit relation', 'An equation in x and y not solved for y, such as x² + y² = 25.'], ['implicit differentiation', 'Differentiating both sides and solving for dy/dx.']],
  watch='Forgetting the product rule on terms like xy, or losing the negative sign when solving for dy/dx.',
  cards=[dict(h='Every y gets a y′', big='⟨\\frac{d}{dx}(y^2) = 2y\\,{{\\frac{dy}{dx}}}⟩; then collect the ⟨\\frac{dy}{dx}⟩ terms and solve.',
    steps=['⟨x^2 + y^2 = 169⟩: ⟨2x + 2yy\' = 0⟩, so ⟨y\' = {{-\\frac{x}{y}}}⟩.', '⟨x^2 + xy + y^2 = 3⟩: ⟨2x + y + xy\' + 2yy\' = 0⟩, so ⟨y\' = -\\frac{2x + y}{x + 2y}⟩.', 'At ⟨(6, 8)⟩ on ⟨x^2 + y^2 = 100⟩: ⟨y\'\' = -\\frac{100}{y^3} = {{-\\tfrac{25}{128}}}⟩.'])])

R[DV, 10] = dict(obj='find derivatives of inverse functions and of inverse trigonometric functions',
  idea='If g is the inverse of f, then g′(b) = 1/f′(g(b)): the slopes at matching points are reciprocals.',
  voc=[['inverse function', 'g undoes f: g(f(x)) = x.'], ['arctangent', 'tan⁻¹ x, with derivative 1/(1 + x²).']],
  watch='Forgetting to take the reciprocal, or using f′(b) instead of f′(g(b)).',
  cards=[dict(h='Reciprocal slope at the matching point', big='⟨g\'(b) = \\frac{1}{f\'(g(b))}⟩: first find ⟨g(b)⟩, the {{x-value}} with ⟨f(x) = b⟩.',
    steps=['⟨f(1) = 4⟩, ⟨f\'(1) = 4⟩: ⟨g(4) = 1⟩, so ⟨g\'(4) = {{\\tfrac{1}{4}}}⟩.', '⟨f(x) = x^3 + 3x + 2⟩: ⟨f(1) = 6⟩, ⟨f\'(1) = 6⟩, so ⟨(f^{-1})\'(6) = {{\\tfrac{1}{6}}}⟩.', '⟨\\frac{d}{dx}\\tan^{-1}(6x) = \\frac{6}{1 + 36x^2}⟩.'])])
