# Teaching notes, units 4–5 (Applications of Derivatives; Antiderivatives and Definite Integrals).
AD = 'applications-derivatives'
AI = 'antiderivatives-definite-integrals'
R = {}

R[AD, 1] = dict(obj='interpret a derivative value in context with correct units',
  idea='f′(a) is a rate: (units of f) per (unit of the input), at the instant a. Its sign says whether the quantity is increasing or decreasing.',
  voc=[['rate of change', 'How fast one quantity changes per unit of another.'], ['units of a derivative', 'Output units divided by input units, such as °F per hour.']],
  watch='Reading T′(4) as a temperature, or writing the units upside down.',
  cards=[dict(h='A sentence with units', big='⟨T\'(4) = -12⟩ means: at ⟨h = 4⟩ hours, the temperature is {{decreasing}} at 12 °F per hour.',
    steps=['⟨T(h) = -3h^2 + 12h + 73⟩: ⟨T\'(h) = -6h + 12⟩, so ⟨T\'(4) = {{-12}}⟩.', 'Units: °F per {{hour}}.'])])

R[AD, 2] = dict(obj='find critical numbers and classify them with the first or second derivative test',
  idea='Critical numbers are where f′ = 0 or f′ is undefined; f′ changing sign there (or the sign of f″) tells max or min.',
  voc=[['critical number', 'x in the domain where f′(x) = 0 or f′ does not exist.'], ['first derivative test', 'f′ changes + to − at a max, − to + at a min.'], ['second derivative test', 'f′(c) = 0 and f″(c) < 0 gives a max; f″(c) > 0 a min.']],
  watch='Missing a root such as x = 0 when factoring f′, or calling every critical number an extremum.',
  cards=[dict(h='Find and classify', big='Factor ⟨f\'⟩ completely so no {{zero}} is missed, then test each one.',
    steps=['⟨f(x) = -x^3 + 3x^2 - 5⟩: ⟨f\'(x) = -3x(x - 2)⟩, so ⟨x = 0⟩ and ⟨x = {{2}}⟩.', '⟨f\'\'(x) = -6x + 6⟩: ⟨f\'\'(2) = -6 < 0⟩, so ⟨x = 2⟩ is a relative {{maximum}}.'])])

R[AD, 3] = dict(obj='find intervals where a function increases or decreases from f′ or from the graph of f′',
  idea='Every critical number splits the number line; test the sign of f′ on each piece.',
  voc=[['increasing on an interval', 'f′ > 0 there.'], ['decreasing on an interval', 'f′ < 0 there.']],
  watch='Using only one critical number, which merges intervals with different signs.',
  cards=[dict(h='Sign chart', big='List all critical numbers, then test one value in {{each interval}}.',
    steps=['⟨f(x) = 2x^3 + 15x^2 + 36x⟩: ⟨f\'(x) = 6(x + 2)(x + 3)⟩, negative only on ⟨({{-3}}, -2)⟩.', 'From the graph of ⟨f\'⟩: f decreases where the graph of f′ is {{below}} the x-axis.'])])

R[AD, 4] = dict(obj='find relative and absolute extrema, using the candidates test on a closed interval',
  idea='On a closed interval the absolute max and min are among the critical numbers and the endpoints: evaluate f at all of them.',
  voc=[['absolute maximum', 'The largest value of f on the whole interval.'], ['candidates test', 'Compare f at every critical number and endpoint.']],
  watch='Forgetting to check the endpoints.',
  cards=[dict(h='Candidates test', big='Evaluate ⟨f⟩ at the critical numbers {{and the endpoints}}; the biggest output is the absolute max.',
    steps=['⟨f(x) = -x^3 - 3x^2 + 24x⟩ on ⟨[-5, 3]⟩: critical numbers ⟨-4, 2⟩.', '⟨f(-5) = -70⟩, ⟨f(-4) = -80⟩, ⟨f(2) = 28⟩, ⟨f(3) = 18⟩: absolute max ⟨{{28}}⟩ at ⟨x = 2⟩.'])])

R[AD, 5] = dict(obj='determine concavity and find inflection points from f″',
  idea='f″ > 0 means concave up (f′ increasing); an inflection point is where f″ changes sign, not just where f″ = 0.',
  voc=[['concave up', 'The graph bends upward; f′ is increasing; f″ > 0.'], ['point of inflection', 'A point where the concavity changes.']],
  watch='Using f′ instead of f″, or calling every zero of f″ an inflection point.',
  cards=[dict(h='Signs of f″', big='Concavity comes from the sign of the {{second derivative}}, and an inflection point needs a sign change.',
    steps=['⟨f(x) = 2x^3 + 3x^2 - 72x - 1⟩: ⟨f\'\'(x) = 6(2x + 1)⟩, zero at ⟨x = {{-\\tfrac{1}{2}}}⟩ with a sign change.', '⟨f(x) = x^4⟩: ⟨f\'\'(0) = 0⟩ but ⟨f\'\'⟩ does not change sign, so ⟨x = 0⟩ is {{not}} an inflection point.'])])

R[AD, 6] = dict(obj='solve related-rates problems by relating quantities and differentiating with respect to time',
  idea='Write an equation that holds at every moment, differentiate both sides with respect to t, then substitute the values at the moment asked about.',
  voc=[['related rates', 'Rates of change of quantities linked by an equation.'], ['implicit differentiation in t', 'Every variable that changes gets a d/dt factor.']],
  watch='Substituting the numbers before differentiating, which turns changing quantities into constants.',
  cards=[dict(h='Equation, differentiate, substitute', big='Differentiate {{before}} you plug in the values at the given moment.',
    steps=['Ladder: ⟨x^2 + y^2 = 17^2⟩, so ⟨2xx\' + 2yy\' = 0⟩.', 'At ⟨x = 8⟩, ⟨y = 15⟩, ⟨x\' = 1⟩: ⟨y\' = -\\frac{8}{15}⟩; the top slides down at ⟨{{\\tfrac{8}{15}}}⟩ ft/s.', 'Balloon: ⟨V = \\tfrac{4}{3}\\pi r^3⟩, ⟨V\' = 4\\pi r^2 r\'⟩.'])])

R[AD, 7] = dict(obj='set up and solve optimization problems and justify that the answer is a maximum or minimum',
  idea='Write the quantity to optimize in one variable using the constraint, find its critical numbers on the allowed interval, and check endpoints or use a derivative test.',
  voc=[['objective function', 'The quantity being maximized or minimized.'], ['constraint', 'The condition that links the variables.']],
  watch='Reporting the critical number when the question asks for the maximum value (or the reverse).',
  cards=[dict(h='One variable, then calculus', big='Use the {{constraint}} to write the objective in one variable.',
    steps=['Perimeter 172: ⟨y = 86 - x⟩, ⟨A = x(86 - x)⟩.', '⟨A\' = 86 - 2x = 0⟩ at ⟨x = 43⟩; ⟨A\'\' = -2 < 0⟩, so the max area is ⟨{{1849}}⟩ m².', 'Box from a 24-in sheet: ⟨V = x(24 - 2x)^2⟩ is largest at ⟨x = {{4}}⟩ in.'])])

R[AD, 8] = dict(obj='use derivatives of position to find velocity, acceleration, speed and changes of direction',
  idea='v = s′ and a = v′; the particle is at rest when v = 0, changes direction when v changes sign, and speeds up when v and a have the same sign.',
  voc=[['velocity', 'v(t) = s′(t); its sign gives the direction.'], ['speed', '|v(t)|.'], ['speeding up', 'v and a have the same sign.']],
  watch='Saying the particle speeds up whenever a > 0.',
  cards=[dict(h='Signs of v and a', big='Speeding up when ⟨v⟩ and ⟨a⟩ have the {{same sign}}; slowing down when they differ.',
    steps=['⟨s(t) = 2t^3 - 15t^2 + 24t + 1⟩: ⟨v = 6(t - 1)(t - 4)⟩, ⟨a = 6(2t - 5)⟩.', '⟨v < 0⟩ on ⟨(1, 4)⟩ and ⟨a > 0⟩ for ⟨t > \\tfrac{5}{2}⟩: speeding up on ⟨(1, \\tfrac{5}{2}) \\cup ({{4}}, \\infty)⟩.'])])

R[AD, 9] = dict(obj='compute and interpret average and instantaneous rates of change in applied problems',
  idea='Average rate uses two points; the instantaneous rate is the derivative at one point, with units of output per input.',
  voc=[['instantaneous rate', 'The derivative at a single time.'], ['exponential growth rate', 'P′(t) = kP(t) for P(t) = P₀e^(kt).']],
  watch='Giving P(t) when the question asks how fast P is changing.',
  cards=[dict(h='Average or instantaneous?', big='"How fast at t = 13" asks for the {{derivative}} at 13.',
    steps=['⟨P(t) = 142e^{0.04t}⟩: ⟨P\'(t) = 5.68e^{0.04t}⟩, so ⟨P\'(13) \\approx {{9.6}}⟩ per year.', '⟨V(t) = t^2 + 6t⟩ from 1 to 7: average rate ⟨\\frac{91 - 7}{6} = {{14}}⟩ L/min.'])])

R[AD, 10] = dict(obj='check the hypotheses of the Mean Value Theorem and find the value c it guarantees',
  idea='If f is continuous on [a, b] and differentiable on (a, b), some c in (a, b) has f′(c) equal to the average rate of change.',
  voc=[['Mean Value Theorem', 'Some tangent slope equals the secant slope on [a, b].'], ['hypotheses', 'The conditions a theorem needs before it applies.']],
  watch='Using the midpoint of the interval, or giving the average rate instead of c.',
  cards=[dict(h='Secant slope, then solve', big='Find ⟨\\frac{f(b) - f(a)}{b - a}⟩, then solve ⟨f\'(c) =⟩ that slope and keep the c {{inside the interval}}.',
    steps=['⟨f(x) = x^3 - x⟩ on ⟨[0, 2]⟩: average rate ⟨\\frac{6 - 0}{2} = 3⟩.', '⟨3c^2 - 1 = 3⟩, so ⟨c = {{\\tfrac{2\\sqrt{3}}{3}}}⟩ (the negative root is outside).'])])

R[AD, 11] = dict(obj='combine limit and derivative skills in mixed problems',
  idea='Decide first what the question asks for (a limit, a derivative value, an extremum) and then pick the rule that fits.',
  voc=[['derivative rules', 'Power, product, quotient and chain rules.'], ['candidates test', 'Comparing f at critical numbers and endpoints.']],
  watch='Applying a rule mechanically without checking which one the expression needs.',
  cards=[dict(h='Name the tool', big='Before computing, say which rule applies: product, quotient, {{chain}}, or a limit technique.',
    steps=['⟨f(x) = x^5e^{-x}⟩: product rule gives ⟨x^4(5 - x)e^{-x}⟩.', '⟨\\frac{x^2 + 1}{5x + 2}⟩: quotient rule gives ⟨\\frac{5x^2 + 4x - 5}{(5x + 2)^2}⟩, not ⟨{{\\tfrac{2x}{5}}}⟩.'])])

R[AD, 12] = dict(obj='use L’Hôpital’s Rule for limits of the forms 0/0 and ∞/∞',
  idea='Only when substitution gives 0/0 or ∞/∞: the limit of f/g equals the limit of f′/g′ (differentiate the top and bottom separately).',
  voc=[['L’Hôpital’s Rule', 'For 0/0 or ∞/∞, lim f/g = lim f′/g′.'], ['indeterminate form', '0/0 or ∞/∞.']],
  watch='Using the quotient rule on f/g, or using the rule when the form is not indeterminate.',
  cards=[dict(h='Check the form first', big='Substitute first. Use the rule only for ⟨\\tfrac{0}{0}⟩ or ⟨\\tfrac{\\infty}{\\infty}⟩, and differentiate top and bottom {{separately}}.',
    steps=['⟨\\lim_{x \\to 0}\\frac{e^{6x} - 1 - 6x}{x^2}⟩: ⟨\\tfrac{0}{0}⟩; differentiate: ⟨\\frac{6e^{6x} - 6}{2x}⟩, still ⟨\\tfrac{0}{0}⟩.', 'Again: ⟨\\frac{36e^{6x}}{2} \\to {{18}}⟩.', '⟨\\lim_{x \\to 3}\\frac{x^2 + 1}{x + 3} = \\tfrac{10}{6}⟩ by substitution; the rule does not apply.'])])

R[AI, 1] = dict(obj='find antiderivatives by reversing derivatives and use an initial condition to find C',
  idea='F is an antiderivative of f when F′ = f; every antiderivative differs by a constant, which one known value pins down.',
  voc=[['antiderivative', 'A function F with F′ = f.'], ['constant of integration', 'The + C that every antiderivative family carries.'], ['initial condition', 'A known value such as F(1) = 5 that fixes C.']],
  watch='Differentiating instead of antidifferentiating, or adding the initial value instead of solving for C.',
  cards=[dict(h='Antidifferentiate, then solve for C', big='Find the general antiderivative with ⟨+ C⟩, then use the given value to solve for {{C}}.',
    steps=['⟨F\'(x) = 20x^4 + 6⟩: ⟨F(x) = 4x^5 + 6x + C⟩.', '⟨F(1) = 10 + C = 5⟩, so ⟨C = {{-5}}⟩ and ⟨F(x) = 4x^5 + 6x - 5⟩.'])])

R[AI, 2] = dict(obj='find indefinite integrals of powers, exponentials, 1/x and trig functions',
  idea='Reverse each derivative rule: add one to the exponent and divide by it, except for 1/x, whose antiderivative is ln|x|.',
  voc=[['indefinite integral', '∫ f(x) dx, the family of all antiderivatives.'], ['reverse power rule', '∫ xⁿ dx = xⁿ⁺¹/(n + 1) + C for n ≠ −1.']],
  watch='Multiplying by the new exponent instead of dividing, or forgetting + C.',
  cards=[dict(h='Reverse the rules', big='⟨\\int x^n\\,dx = \\frac{x^{n+1}}{n+1} + C⟩ for ⟨n \\ne -1⟩, and ⟨\\int\\frac{1}{x}\\,dx = {{\\ln|x|}} + C⟩.',
    steps=['⟨\\int(21x^6 - 5)\\,dx = {{3x^7}} - 5x + C⟩.', '⟨\\int 30e^{5x}\\,dx = 6e^{5x} + C⟩.', '⟨\\int(6\\sqrt{x} - x^{-2})\\,dx = 4x^{3/2} + \\frac{1}{x} + C⟩.'])])

R[AI, 3] = dict(obj='approximate area with left, right and midpoint Riemann sums and see the definite integral as their limit',
  idea='A Riemann sum adds rectangle areas f(xₖ)Δx; as the rectangles get thinner the sums approach the definite integral.',
  voc=[['Riemann sum', 'Σ f(xₖ)Δx, a sum of rectangle areas.'], ['Δx', '(b − a)/n, the width of each rectangle.'], ['definite integral', 'The limit of Riemann sums as n → ∞.']],
  watch='Using the wrong endpoints, or forgetting to multiply by Δx.',
  cards=[dict(h='Width times height, then add', big='⟨\\Delta x = \\frac{b - a}{n}⟩; left sums use left endpoints, right sums use {{right endpoints}}.',
    steps=['⟨\\int_1^3(2x + 3)\\,dx⟩, left sum, ⟨n = 2⟩: ⟨1\\cdot[f(1) + f(2)] = 5 + 7 = {{12}}⟩.', 'For ⟨f(x) = 2x⟩ on ⟨[0, 3]⟩, ⟨R_n = 9 + \\tfrac{9}{n} \\to {{9}}⟩, which is ⟨\\int_0^3 2x\\,dx⟩.'])])

R[AI, 4] = dict(obj='convert between limits of Riemann sums and definite integrals',
  idea='In lim Σ f(a + kΔx)Δx, the factor Δx gives the width b − a, the start of the inside gives a, and what is applied to it is f.',
  voc=[['Δx = (b − a)/n', 'The factor multiplying each term.'], ['xₖ = a + kΔx', 'The right endpoint of the k-th subinterval.']],
  watch='Taking b to be the width, or using Δx = 1/n when the factor is 3/n.',
  cards=[dict(h='Read a, b and f', big='From ⟨\\Delta x = \\tfrac{3}{n}⟩ the width is 3; the inside ⟨1 + \\tfrac{3k}{n}⟩ starts at ⟨a = {{1}}⟩.',
    steps=['⟨\\lim_{n \\to \\infty}\\sum_{k=1}^{n}\\left(1 + \\frac{3k}{n}\\right)^2\\frac{3}{n} = \\int_1^4 x^2\\,dx⟩. The upper limit is ⟨b = {{4}}⟩.', 'Evaluate: ⟨\\frac{64}{3} - \\frac{1}{3} = {{21}}⟩.'])])

R[AI, 5] = dict(obj='approximate integrals from tables with Riemann and trapezoidal sums, including unequal widths',
  idea='Each subinterval contributes width × height (rectangles) or width × average of the two heights (trapezoids); widths can differ.',
  voc=[['trapezoidal sum', 'Σ (Δxₖ)(f(xₖ₋₁) + f(xₖ))/2.'], ['unequal subintervals', 'Table points that are not evenly spaced.']],
  watch='Assuming every width is the same, or averaging the table values.',
  cards=[dict(h='Each piece separately', big='Use each subinterval’s {{own width}}.',
    steps=['f(0) = 2, f(2) = 8, f(4) = 8, f(6) = 7: trapezoids ⟨2\\cdot 5 + 2\\cdot 8 + 2\\cdot 7.5 = {{41}}⟩.', 'Calculator active: ⟨\\int_0^1 e^{-x^2}\\,dx \\approx 0.747⟩ (no elementary antiderivative).'])])

R[AI, 6] = dict(obj='evaluate definite integrals with area formulas, counting area below the axis as negative',
  idea='∫ from a to b f(x) dx is the signed area: triangles, rectangles, trapezoids and circles above the axis add, those below subtract.',
  voc=[['signed area', 'Area above the x-axis counts positive, below counts negative.'], ['semicircle', 'y = √(r² − x²) is the top half of a circle of radius r.']],
  watch='Counting area below the axis as positive, or using a full circle for a semicircle.',
  cards=[dict(h='Shapes and signs', big='Split the region into shapes; area {{below the axis}} gets a minus sign.',
    steps=['⟨\\int_0^6\\sqrt{36 - x^2}\\,dx⟩ is a quarter disk of radius 6: ⟨\\tfrac{1}{4}\\pi(36) = {{9\\pi}}⟩.', '⟨\\int_{-1}^{2}|x|\\,dx = \\tfrac{1}{2} + 2 = {{\\tfrac{5}{2}}}⟩.'])])

R[AI, 7] = dict(obj='use the properties of definite integrals: additivity, reversal, linearity and odd/even symmetry',
  idea='Integrals over adjacent intervals add, reversing the limits changes the sign, constants factor out, and an odd function integrates to 0 over [−a, a].',
  voc=[['additivity', '∫ from a to b + ∫ from b to c = ∫ from a to c.'], ['reversal', '∫ from b to a = −∫ from a to b.'], ['odd function', 'f(−x) = −f(x); its integral over [−a, a] is 0.']],
  watch='Subtracting adjacent pieces, or subtracting a constant k instead of k(b − a).',
  cards=[dict(h='Four properties', big='Reverse: change the sign. Adjacent: {{add}}. Constant k: ⟨\\int_a^b k\\,dx = k(b - a)⟩.',
    steps=['⟨\\int_2^4 f = -11⟩, so ⟨\\int_4^2 f = {{11}}⟩.', '⟨\\int_0^2 (f(x) - 1)\\,dx = -9 - 2 = {{-11}}⟩ when ⟨\\int_0^2 f = -9⟩.'])])
