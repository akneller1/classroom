# Teaching notes, units 6–9 (FTC; Applications of Integrals; Differential Equations; AP Review).
FT = 'fundamental-theorem-calculus'
AP = 'applications-integrals'
DE = 'differential-equations'
RV = 'ap-review'
R = {}

R[FT, 1] = dict(obj='use the Fundamental Theorem to connect a function’s net change to the integral of its derivative',
  idea='∫ from a to b f′(x) dx = f(b) − f(a): integrating a rate of change gives the total change.',
  voc=[['net change', 'f(b) − f(a), the overall change from a to b.'], ['Fundamental Theorem (Part 2)', '∫ from a to b f(x) dx = F(b) − F(a) when F′ = f.']],
  watch='Forgetting the starting value when asked for f(b), or subtracting in the wrong order.',
  cards=[dict(h='Total change from the rate', big='⟨\\int_a^b f\'(x)\\,dx = f(b) - f(a)⟩, so ⟨f(b) = f(a) + {{\\int_a^b f\'(x)\\,dx}}⟩.',
    steps=['⟨f(5) = -2⟩, ⟨f(6) = -20⟩: ⟨\\int_5^6 f\'(x)\\,dx = -20 - (-2) = {{-18}}⟩.', '⟨f(-3) = 2⟩ and ⟨\\int_{-3}^{5} f\' = -4⟩: ⟨f(5) = 2 + (-4) = {{-2}}⟩.'])])

R[FT, 2] = dict(obj='build and evaluate accumulation functions g(x) = ∫ from a to x f(t) dt from graphs and formulas',
  idea='g(x) adds up the signed area under f from a to x; it starts at g(a) = 0.',
  voc=[['accumulation function', 'g(x) = ∫ from a to x f(t) dt.'], ['dummy variable', 't, the variable inside the integral.']],
  watch='Forgetting to subtract the antiderivative’s value at the lower limit.',
  cards=[dict(h='From the lower limit to x', big='⟨g(x) = F(x) - F(a)⟩, so ⟨g(a) = {{0}}⟩.',
    steps=['⟨g(x) = \\int_2^x(3t^2 + 2t + 1)\\,dt = (x^3 + x^2 + x) - (8 + 4 + 2)⟩.', 'So ⟨g(x) = x^3 + x^2 + x - {{14}}⟩.'])])

R[FT, 3] = dict(obj='analyze a function defined by an integral: where it increases, has extrema and is concave up',
  idea='For g(x) = ∫ from a to x f(t) dt, g′ = f and g″ = f′: read increasing and extrema from the sign of f, concavity from the slope of f.',
  voc=[['g′(x) = f(x)', 'The Fundamental Theorem, Part 1.'], ['g″(x) = f′(x)', 'Concavity of g comes from whether f is increasing.']],
  watch='Finding where f is increasing when the question asks where g is increasing.',
  cards=[dict(h='g′ is f', big='g increases where {{f is positive}}; g is concave up where f is increasing.',
    steps=['⟨g(x) = \\int_1^x(t^2 - 6t + 5)\\,dt⟩: ⟨g\'(x) = (x - 1)(x - 5)⟩.', 'g is increasing on ⟨(-\\infty, 1) \\cup ({{5}}, \\infty)⟩ and has a relative max at ⟨x = 1⟩.', '⟨g\'\'(x) = 2x - 6 > 0⟩ for ⟨x > {{3}}⟩: concave up there.'])])

R[FT, 4] = dict(obj='differentiate integrals with variable limits using the Fundamental Theorem and the chain rule',
  idea='d/dx ∫ from a to u(x) f(t) dt = f(u(x))·u′(x); a constant lower limit adds nothing, a variable one subtracts f(v(x))·v′(x).',
  voc=[['FTC Part 1', 'd/dx ∫ from a to x f(t) dt = f(x).'], ['chain rule factor', 'u′(x) when the upper limit is u(x).']],
  watch='Substituting x for t instead of u(x), or forgetting the factor u′(x).',
  cards=[dict(h='Plug in the limit, times its derivative', big='⟨\\frac{d}{dx}\\int_a^{u(x)} f(t)\\,dt = f(u(x))\\cdot{{u\'(x)}}⟩.',
    steps=['⟨\\frac{d}{dx}\\int_1^{3x}\\sin t\\,dt = 3\\sin(3x)⟩.', '⟨\\frac{d}{dx}\\int_{-1}^{x^2} t^3\\,dt = (x^2)^3\\cdot 2x = {{2x^7}}⟩.'])])

R[FT, 5] = dict(obj='evaluate definite integrals with antiderivatives',
  idea='Find any antiderivative F, then compute F(b) − F(a); the constant C cancels.',
  voc=[['F(b) − F(a)', 'The value of ∫ from a to b f(x) dx.'], ['bracket notation', '[F(x)] from a to b means F(b) − F(a).']],
  watch='Forgetting to subtract F(a), or evaluating the integrand instead of the antiderivative.',
  cards=[dict(h='Upper minus lower', big='Evaluate the {{antiderivative}} at both limits and subtract: upper minus lower.',
    steps=['⟨\\int_{-1}^{3}(3x^2 + 6x + 8)\\,dx⟩: ⟨F(x) = x^3 + 3x^2 + 8x⟩.', '⟨F(3) = 78⟩, ⟨F(-1) = -6⟩, so the integral is ⟨78 - (-6) = {{84}}⟩.'])])

R[FT, 6] = dict(obj='integrate by substitution, including changing the limits of a definite integral',
  idea='Choose u as the inside function whose derivative also appears; rewrite the whole integral in u, integrate, and substitute back (or change the limits).',
  voc=[['u-substitution', 'Reversing the chain rule by renaming the inside as u.'], ['du', 'u′(x) dx.']],
  watch='Forgetting to adjust for a constant factor in du, such as x² dx = (1/3) du.',
  cards=[dict(h='Inside function and its derivative', big='Let ⟨u⟩ be the inside; then ⟨du = u\'(x)\\,dx⟩ must account for {{all of the remaining x’s}}.',
    steps=['⟨\\int 2x(x^2 + 6)^5\\,dx⟩: ⟨u = x^2 + 6⟩, ⟨du = 2x\\,dx⟩, so ⟨\\int u^5\\,du = \\tfrac{1}{6}u^6 + C⟩.', '⟨\\int\\frac{x^2}{\\sqrt{x^3 + 3}}\\,dx⟩: ⟨x^2\\,dx = \\tfrac{1}{3}du⟩, giving ⟨{{\\tfrac{2}{3}}}\\sqrt{x^3 + 3} + C⟩.'])])

R[FT, 7] = dict(obj='integrate rational functions by long division and by completing the square',
  idea='When the top’s degree is at least the bottom’s, divide first; a quadratic bottom with no real roots becomes (x − h)² + k², which integrates to an arctangent.',
  voc=[['long division', 'Rewriting a fraction as a polynomial plus a proper fraction.'], ['completing the square', 'x² + bx + c = (x + b/2)² + (c − b²/4).'], ['arctangent integral', '∫ 1/(u² + a²) du = (1/a)tan⁻¹(u/a) + C.']],
  watch='Dropping the remainder term or the factor 1/a.',
  cards=[dict(h='Divide or complete the square', big='⟨\\int\\frac{du}{u^2 + a^2} = \\frac{1}{a}\\tan^{-1}\\frac{u}{a} + C⟩: do not forget the {{factor 1/a}}.',
    steps=['⟨\\frac{2x + 9}{x + 2} = 2 + \\frac{5}{x + 2}⟩, so the integral is ⟨2x + {{5\\ln|x + 2|}} + C⟩.', '⟨x^2 + 4x + 8 = (x + 2)^2 + 4⟩, so ⟨\\int\\frac{dx}{x^2 + 4x + 8} = \\tfrac{1}{2}\\tan^{-1}\\frac{x + 2}{2} + C⟩.'])])

R[AP, 1] = dict(obj='explain what a definite integral of a rate means in context, with units',
  idea='The integral of a rate over a time interval is the net change in the quantity over that interval, in the quantity’s units.',
  voc=[['net change', 'Final amount minus starting amount.'], ['rate', 'A quantity per unit of time, such as gallons per minute.']],
  watch='Reading the integral as the amount at the end instead of the change.',
  cards=[dict(h='Rate × time = amount', big='Units: (people per year) × years = {{people}}.',
    steps=['⟨\\int_6^{11}P\'(t)\\,dt⟩ is the change in population from year 6 to year 11.', '⟨\\int_2^8 C\'(x)\\,dx⟩ is the additional {{cost}} of producing items 2 to 8.'])])

R[AP, 2] = dict(obj='find amounts from rates in and out using an initial value plus an integral',
  idea='Amount at time T = amount at the start + ∫ from 0 to T (rate in − rate out) dt.',
  voc=[['rate in / rate out', 'How fast something is added or removed.'], ['initial amount', 'The amount at t = 0.']],
  watch='Leaving out the initial amount or the outflow.',
  cards=[dict(h='Start plus net change', big='⟨A(T) = A(0) + \\int_0^T(\\text{in} - \\text{out})\\,dt⟩. Do not drop the {{starting amount}}.',
    steps=['158 L at the start, in ⟨2t + 8⟩, out 30: ⟨158 + \\int_0^5(2t - 22)\\,dt = 158 + (25 - 110)⟩.', '⟨= {{73}}⟩ L.'])])

R[AP, 3] = dict(obj='compute and interpret the average value of a function on an interval',
  idea='f_avg = (1/(b − a))∫ from a to b f(x) dx: the height of the rectangle with the same area as the region under f.',
  voc=[['average value', '(1/(b − a))∫ from a to b f(x) dx.'], ['average rate of change', '(f(b) − f(a))/(b − a), a different quantity.']],
  watch='Forgetting to divide by b − a, or averaging the endpoint values.',
  cards=[dict(h='Integrate, then divide', big='Average value ⟨= \\frac{1}{b - a}\\int_a^b f(x)\\,dx⟩: divide by the {{length of the interval}}.',
    steps=['⟨f(x) = 6\\cos x⟩ on ⟨[0, \\tfrac{\\pi}{3}]⟩: ⟨\\int = 6\\sin\\tfrac{\\pi}{3} = 3\\sqrt{3}⟩.', 'Divide by ⟨\\tfrac{\\pi}{3}⟩: ⟨{{\\tfrac{9\\sqrt{3}}{\\pi}}}⟩.'])])

R[AP, 4] = dict(obj='find displacement and position from velocity, including from a velocity graph',
  idea='Displacement = ∫ v(t) dt (signed area); position at T = starting position + displacement.',
  voc=[['displacement', 'Change in position, ∫ from a to b v(t) dt.'], ['position', 's(T) = s(0) + ∫ from 0 to T v(t) dt.']],
  watch='Giving the velocity at the end, or forgetting the starting position.',
  cards=[dict(h='Signed area of velocity', big='Area under ⟨v⟩ above the axis moves the particle forward; area {{below}} moves it back.',
    steps=['⟨v(t) = 2t^2 - 10t + 12⟩ on ⟨[0, 4]⟩: ⟨\\left[\\tfrac{2}{3}t^3 - 5t^2 + 12t\\right]_0^4 = {{\\tfrac{32}{3}}}⟩ m.', 'Starting at ⟨x = -3⟩ with displacement 16: ⟨x = {{13}}⟩.'])])

R[AP, 5] = dict(obj='find total distance traveled by splitting at the times velocity changes sign',
  idea='Total distance = ∫ |v(t)| dt: find where v = 0, integrate each piece, and add the absolute values.',
  voc=[['total distance', '∫ |v(t)| dt, always positive.'], ['change of direction', 'A time where v changes sign.']],
  watch='Taking the absolute value of the displacement instead of each piece.',
  cards=[dict(h='Split, then add sizes', big='Find where ⟨v(t) = 0⟩, integrate on each piece, and add the {{absolute values}}.',
    steps=['⟨v(t) = 4t - 20⟩ on ⟨[0, 6]⟩: zero at ⟨t = 5⟩.', 'Pieces: ⟨\\int_0^5 = -50⟩, ⟨\\int_5^6 = 2⟩, so the distance is ⟨50 + 2 = {{52}}⟩ ft.'])])

R[AP, 6] = dict(obj='find the area between two curves by integrating top minus bottom',
  idea='Find where the curves meet, decide which is on top between those x-values, and integrate (top − bottom).',
  voc=[['points of intersection', 'Where the two curves are equal; they are the limits of integration.'], ['top minus bottom', 'The height of each thin rectangle.']],
  watch='Integrating only one curve, or adding the curves.',
  cards=[dict(h='Meet, top, integrate', big='Area ⟨= \\int_a^b(\\text{top} - \\text{bottom})\\,dx⟩ between the {{intersection points}}.',
    steps=['⟨y = 6⟩ and ⟨y = 2x^2 - 2x - 18⟩ meet at ⟨x = -3⟩ and ⟨x = 4⟩; ⟨y = 6⟩ is on top.', '⟨\\int_{-3}^{4}(24 + 2x - 2x^2)\\,dx = {{\\tfrac{343}{3}}}⟩.'])])

R[AP, 7] = dict(obj='find volumes with known cross sections and solids of revolution (disks and washers, including about other lines)',
  idea='Volume = ∫ (area of a slice) dx. A disk has area πR²; a washer π(R² − r²) with radii measured from the axis of revolution.',
  voc=[['disk method', 'V = π∫ R² dx.'], ['washer method', 'V = π∫ (R² − r²) dx.'], ['cross section', 'A slice perpendicular to the axis, such as a square or semicircle.']],
  watch='Squaring R − r instead of subtracting the squares, or measuring radii from the x-axis when revolving about another line.',
  cards=[dict(h='Area of a slice, then integrate', big='Washer area is ⟨\\pi(R^2 - r^2)⟩, not ⟨\\pi(R - r)^2⟩; measure each radius from the {{axis of revolution}}.',
    steps=['⟨y = 2x⟩ and ⟨y = x^2⟩ about the x-axis: ⟨\\pi\\int_0^2(4x^2 - x^4)\\,dx = {{\\tfrac{64\\pi}{15}}}⟩.', 'Under ⟨y = \\sqrt{x}⟩ on ⟨[0, 4]⟩ about ⟨y = -1⟩: ⟨R = \\sqrt{x} + 1⟩, ⟨r = 1⟩.'])])

R[AP, 8] = dict(obj='use integrals to model accumulation in applied situations (rain, traffic, growth)',
  idea='When a rate is given, the total over a time interval is the integral of the rate; add any starting amount.',
  voc=[['rate model', 'A function giving a rate, such as R(t) inches per hour.'], ['accumulated amount', '∫ of the rate over the interval.']],
  watch='Giving the rate at the end, or multiplying one rate by the whole time.',
  cards=[dict(h='Integrate the rate', big='Total ⟨= \\int_0^T R(t)\\,dt⟩, not ⟨R(T)\\cdot T⟩ unless the rate is {{constant}}.',
    steps=['⟨R(t) = 0.2t + 0.4⟩ for 3 hours: ⟨\\left[0.1t^2 + 0.4t\\right]_0^3 = {{2.1}}⟩ inches.', 'A culture with ⟨N(0) = 797⟩ and ⟨N\'(t) = 159.4e^{0.2t}⟩: ⟨N(2) = 797 + 797(e^{0.4} - 1) \\approx {{1189}}⟩.'])])

R[DE, 1] = dict(obj='write differential equations from verbal descriptions and evaluate slopes from them',
  idea='"Proportional to" means equals a constant k times; the slope of a solution through (x, y) is y′ evaluated there.',
  voc=[['differential equation', 'An equation involving a derivative, such as y′ = ky.'], ['proportional to', 'Equal to a constant k times the quantity.']],
  watch='Substituting the coordinates into the wrong variables.',
  cards=[dict(h='Words to equations', big='"The rate of change of A is proportional to A" is ⟨\\frac{dA}{dt} = {{kA}}⟩.',
    steps=['Cooling toward 70°F: ⟨T\' = k(T - 70)⟩.', '⟨y\' = \\tfrac{1}{2}x + \\tfrac{1}{2}y⟩ at ⟨(-2, -1)⟩: ⟨-1 - \\tfrac{1}{2} = {{-\\tfrac{3}{2}}}⟩.'])])

R[DE, 2] = dict(obj='verify that a function solves a differential equation',
  idea='Differentiate the proposed solution and substitute it into both sides; it is a solution only if the sides agree for every x.',
  voc=[['solution of a differential equation', 'A function that makes the equation true for every x.'], ['characteristic equation', 'For y = e^(kx) in y″ + by′ + cy = 0, k² + bk + c = 0.']],
  watch='Checking only one x-value.',
  cards=[dict(h='Substitute and compare', big='Compute ⟨y\'⟩ (and ⟨y\'\'⟩), substitute, and check that both sides are {{identical}}.',
    steps=['⟨y = 7x^2⟩ in ⟨xy\' = 2y⟩: ⟨x(14x) = 14x^2 = 2(7x^2)⟩, so {{yes}}.', '⟨y = e^{kx}⟩ in ⟨y\'\' + y\' - 2y = 0⟩: ⟨k^2 + k - 2 = 0⟩, so ⟨k = -2⟩ or ⟨k = {{1}}⟩.'])])

R[DE, 3] = dict(obj='estimate solutions with slope fields and (as a BC extension) Euler’s method',
  idea='A slope field draws y′ at many points; a solution curve follows the segments. Euler’s method follows them in straight steps: yₙ₊₁ = yₙ + h·f(xₙ, yₙ).',
  voc=[['slope field', 'Short segments with slope y′ at grid points.'], ['Euler’s method', 'A step-by-step estimate using the tangent slope at each step (BC topic).']],
  watch='Using the first slope for every step.',
  cards=[dict(h='Step along the slopes', big='Each Euler step: new ⟨y⟩ = old ⟨y⟩ + ⟨h⟩ × the slope at the {{current point}}.',
    steps=['⟨y\' = -3x + y⟩, ⟨y(2) = -1⟩, ⟨h = 1⟩: slope ⟨-7⟩, so ⟨y(3) \\approx -8⟩.', 'Slope at ⟨(3, -8)⟩ is ⟨-17⟩, so ⟨y(4) \\approx {{-25}}⟩.'])])

R[DE, 4] = dict(obj='separate variables in a differential equation and integrate both sides',
  idea='Move every y (with dy) to one side and every x (with dx) to the other, then integrate both sides, adding one constant.',
  voc=[['separable equation', 'One that can be written g(y) dy = h(x) dx.'], ['general solution', 'The family of solutions, with a constant C.']],
  watch='Integrating without separating, or turning ln|y| = kx + C into y = e^(kx) + C.',
  cards=[dict(h='Separate, integrate', big='⟨\\frac{1}{y}\\,dy = k\\,dx⟩ integrates to ⟨\\ln|y| = kx + C_1⟩, so ⟨y = {{Ce^{kx}}}⟩.',
    steps=['⟨y\' = -6x^2y⟩: ⟨\\frac{1}{y}dy = -6x^2dx⟩, ⟨\\ln|y| = -2x^3 + C_1⟩, ⟨y = Ce^{-2x^3}⟩.', '⟨y\' = \\frac{x}{y}⟩: ⟨y\\,dy = x\\,dx⟩, so ⟨y^2 - x^2 = {{C}}⟩.'])])

R[DE, 5] = dict(obj='solve separable differential equations and write general solutions',
  idea='After separating and integrating, solve for y when possible; the arbitrary constant can absorb other constants.',
  voc=[['arbitrary constant', 'C stands for any number; 2C or e^C can be renamed C.'], ['implicit solution', 'An equation in x and y, such as 8y² + 7x² = C.']],
  watch='Losing the negative in ∫ y⁻² dy = −1/y.',
  cards=[dict(h='Solve for y if you can', big='⟨y\' = ky^2⟩: ⟨y^{-2}dy = k\\,dx⟩, ⟨-\\frac{1}{y} = kx + C⟩, so ⟨y = {{-\\frac{1}{kx + C}}}⟩.',
    steps=['⟨y\' = 11y^2⟩: ⟨y = -\\frac{1}{11x + C}⟩.', '⟨y\' = -\\frac{7x}{8y}⟩: ⟨8y\\,dy = -7x\\,dx⟩, so ⟨8y^2 + 7x^2 = {{C}}⟩.'])])

R[DE, 6] = dict(obj='find particular solutions from initial conditions, including exponential growth and decay models',
  idea='Use the initial condition to find C; dy/dt = ky always gives y = y(0)e^(kt), and a half-life or doubling time gives k.',
  voc=[['particular solution', 'The one solution that meets the initial condition.'], ['exponential model', 'dy/dt = ky, with solution y = y₀e^(kt).'], ['half-life', 'The time for the amount to fall by half.']],
  watch='Adding the initial value instead of multiplying, or forgetting to add the room temperature back in Newton’s law of cooling.',
  cards=[dict(h='General, then C', big='⟨\\frac{dP}{dt} = kP⟩ gives ⟨P(t) = P(0)\\,{{e^{kt}}}⟩.',
    steps=['⟨P(0) = 60⟩, ⟨P(4) = 180⟩: ⟨e^{4k} = 3⟩, so ⟨P(8) = 60\\cdot 3^2 = {{540}}⟩.', 'Cooling: ⟨T - 72 = 94e^{-0.2t}⟩, so ⟨T(4) = 72 + 94e^{-0.8} \\approx 114.2⟩°F.'])])

R[RV, 1] = dict(obj='review limits and continuity in AP-style problems',
  idea='Most limit questions are settled by substitution, algebra, one-sided pieces, or comparing degrees; continuity needs the limit to equal the value.',
  voc=[['limit', 'What f(x) approaches near a point.'], ['continuity', 'lim (x → a) f(x) = f(a).']],
  watch='Using the wrong piece of a piecewise function.',
  cards=[dict(h='Choose the technique', big='Substitute first; if you get ⟨\\tfrac{0}{0}⟩, {{factor}} or use a known limit.',
    steps=['⟨\\lim_{x \\to 3^-}⟩ of ⟨x^2 - 3⟩ (for ⟨x < 3⟩) is ⟨{{6}}⟩.', '⟨\\lim_{x \\to -2}\\frac{x^2 + 6x + 8}{x + 2} = -2 + 4 = {{2}}⟩.'])])

R[RV, 2] = dict(obj='review derivative rules and their applications',
  idea='Recognize the structure (sum, product, quotient, composition), apply the matching rule, then interpret the result as a slope or rate.',
  voc=[['related rates', 'Differentiate an equation with respect to t.'], ['tangent slope', 'f′(a).']],
  watch='Dividing derivatives for a quotient instead of using the quotient rule.',
  cards=[dict(h='Structure first', big='A product needs the {{product rule}}; a quotient needs the quotient rule; a composition needs the chain rule.',
    steps=['⟨f(x) = 3x^4 - x⟩: ⟨f\'(x) = 12x^3 - 1⟩.', '⟨f(x) = x\\ln(6x)⟩: ⟨f\'(x) = \\ln(6x) + {{1}}⟩.'])])

R[RV, 3] = dict(obj='review definite integrals, the Fundamental Theorem and substitution',
  idea='An antiderivative evaluated at the limits gives the integral; substitution reverses the chain rule.',
  voc=[['FTC', '∫ from a to b f(x) dx = F(b) − F(a).'], ['substitution', 'u = inside function.']],
  watch='Subtracting F(b) − F(a) in the wrong order.',
  cards=[dict(h='F(b) − F(a)', big='Upper limit {{minus}} lower limit.',
    steps=['⟨\\int_{-2}^{0}(3x^2 + 8)\\,dx = 0 - (-24) = {{24}}⟩.', '⟨\\int_0^2 2xe^{x^2}\\,dx = e^4 - 1⟩.'])])

R[RV, 4] = dict(obj='review separable differential equations, slope fields and particular solutions',
  idea='Separate and integrate for the general solution; use the initial condition for C; read slope fields by evaluating y′.',
  voc=[['general solution', 'Contains C.'], ['particular solution', 'C fixed by an initial condition.']],
  watch='Putting the constant in the wrong place (y = e^x + C for y′ = y).',
  cards=[dict(h='Separate, integrate, then C', big='For ⟨y\' = y⟩ the solution is ⟨y = {{Ce^x}}⟩, not ⟨e^x + C⟩.',
    steps=['⟨y\' = \\frac{x}{2y}⟩: ⟨2y\\,dy = x\\,dx⟩, so ⟨2y^2 - x^2 = C⟩.', '⟨y\' = 3y⟩, ⟨y(0) = 10⟩: ⟨y = {{10}}e^{3x}⟩.'])])

R[RV, 5] = dict(obj='connect graphs, tables, formulas and verbal descriptions of the same function',
  idea='The same calculus question can be asked four ways; translate to whichever form makes it easiest (slope from a table, area from a graph, an antiderivative from a formula).',
  voc=[['representation', 'A graph, table, formula or sentence describing a function.'], ['trapezoidal sum', 'Width times average height on each piece.']],
  watch='Assuming equal widths in a table with uneven spacing.',
  cards=[dict(h='Pick the easiest form', big='From a table: slopes come from {{difference quotients}}; integrals come from Riemann or trapezoidal sums.',
    steps=['f(0) = 10, f(2) = 1, f(4) = −9, f(6) = 5, f(8) = 20: trapezoids ⟨11 + (-8) + (-4) + 25 = {{24}}⟩.', '⟨f\'(6) \\approx \\frac{f(8) - f(4)}{8 - 4} = \\tfrac{29}{4}⟩.'])])

R[RV, 6] = dict(obj='justify conclusions by naming a theorem or test and showing its conditions hold',
  idea='A justification names the reason (IVT, MVT, EVT, a derivative test, the definition of inflection) and states the condition that makes it apply.',
  voc=[['justification', 'A reason that cites a definition or theorem whose conditions are met.'], ['hypothesis', 'A condition a theorem needs.']],
  watch='Stating f′(c) = 0 as proof of an extremum, or leaving out continuity.',
  cards=[dict(h='Reason + condition', big='"f has a relative max at x = 2 because ⟨f\'⟩ changes from positive to {{negative}} there."',
    steps=['IVT: "T is continuous on [0, 6] and 55 is between T(0) and T(6), so T(c) = 55 for some c."', 'Inflection: ⟨f\'\'(c) = 0⟩ alone is not enough; ⟨f\'\'⟩ must {{change sign}}.'])])

R[RV, 7] = dict(obj='read and write calculus notation and interpret results in sentences with units',
  idea='Every symbol has a meaning and a unit: f′(a) is a rate at a, ∫ f′ is a net change, and (1/(b − a))∫ f is an average value.',
  voc=[['notation', 'f′(a), d²y/dx², ∫ from a to b f(x) dx, lim (x → a).'], ['units', 'What the number measures, such as feet per second.']],
  watch='Confusing the average value of f with the average rate of change of f.',
  cards=[dict(h='Say it with units', big='If ⟨H⟩ is in feet and ⟨t⟩ in seconds, ⟨H\'(t)⟩ is in feet per second and ⟨H\'\'(t)⟩ is in {{feet per second per second}}.',
    steps=['⟨T\'(3) = -2⟩: at ⟨t = 3⟩ hours, the temperature is decreasing at 2 °F per hour.', 'Average value of ⟨P⟩ on ⟨[7, 9]⟩: ⟨\\tfrac{1}{2}\\int_7^9 P(t)\\,dt⟩, not ⟨\\frac{P(9) - P(7)}{2}⟩, which is the average {{rate of change}}.'])])
