# Teaching notes, units 1–2. Each record: obj, idea, voc [[word, meaning]…], watch, cards [{h, big, steps}].
# Math in ⟨TeX⟩ (single backslashes here; build_notes.py escapes them), {{…}} = blank on guided notes.
EQ = 'equations-inequalities'
FN = 'functions'
R = {}

R[EQ, 1] = dict(obj='write equations of lines in slope-intercept, point-slope and standard form',
  idea='A line is set by its slope and one point; slope m = (y₂ − y₁)/(x₂ − x₁), then y − y₁ = m(x − x₁) and solve for y.',
  voc=[['slope', 'Rise over run: (y₂ − y₁)/(x₂ − x₁).'], ['slope-intercept form', 'y = mx + b, with slope m and y-intercept b.'], ['point-slope form', 'y − y₁ = m(x − x₁) for a line through (x₁, y₁).']],
  watch='Subtracting the coordinates in different orders, which flips the sign of the slope.',
  cards=[dict(h='Writing linear equations', big='Find the {{slope}} from two points, put it with one point into ⟨y - y_1 = m(x - x_1)⟩, then solve for ⟨y⟩. To change ⟨Ax + By = C⟩ to slope-intercept form, solve for ⟨y⟩: ⟨m = -\\frac{A}{B}⟩.',
    steps=['Through (−6, −35) and (−1, −5): ⟨m = \\frac{-5 - (-35)}{-1 - (-6)} = \\frac{30}{5} = {{6}}⟩.', '⟨y + 5 = 6(x + 1)⟩, so ⟨y = {{6x + 1}}⟩.', '⟨4x - 5y = -9⟩: ⟨-5y = -4x - 9⟩, so ⟨y = {{\\tfrac{4}{5}x + \\tfrac{9}{5}}}⟩.'])])

R[EQ, 2] = dict(obj='write equations of parallel and perpendicular lines and classify pairs of lines',
  idea='Parallel lines have equal slopes; perpendicular lines have slopes whose product is −1 (opposite reciprocals).',
  voc=[['parallel', 'Lines in a plane that never meet; equal slopes, different intercepts.'], ['perpendicular', 'Lines that meet at a right angle; slopes m and −1/m.'], ['opposite reciprocal', 'For m = a/b, the number −b/a.']],
  watch='Using the reciprocal without changing the sign (or the opposite without taking the reciprocal) for a perpendicular slope.',
  cards=[dict(h='Parallel and perpendicular lines', big='Parallel: {{same slope}}. Perpendicular: slopes multiply to {{−1}}, so take the opposite reciprocal. Then use the given point in point-slope form.',
    steps=['Parallel to ⟨y = -2x - 3⟩ through (−5, 1): ⟨y - 1 = -2(x + 5)⟩, so ⟨y = {{-2x - 9}}⟩.', 'Perpendicular to ⟨y = \\tfrac{2}{3}x + 1⟩: slope ⟨{{-\\tfrac{3}{2}}}⟩.', '⟨y = -x - 2⟩ and ⟨y = -x + 1⟩: same slope, different intercepts → {{parallel}}.'])])

R[EQ, 3] = dict(obj='solve equations graphically by finding x-intercepts or intersection points',
  idea='The solutions of f(x) = g(x) are the x-coordinates where the graphs of y = f(x) and y = g(x) meet; for f(x) = 0 they are the x-intercepts.',
  voc=[['x-intercept', 'A point where a graph crosses the x-axis (y = 0).'], ['intersection', 'A point on both graphs.'], ['zero of a function', 'An input x with f(x) = 0.']],
  watch='Reporting the y-coordinate of the intersection point instead of its x-coordinate.',
  cards=[dict(h='Solving equations with graphs', big='Graph each side as its own function. Every crossing gives a solution: its {{x-coordinate}}. For ⟨f(x) = 0⟩, read the {{x-intercepts}}.',
    steps=['⟨x^2 - 5x + 4 = 0⟩: the parabola crosses the x-axis at ⟨x = {{1}}⟩ and ⟨x = {{4}}⟩.', '⟨-2x - 11 = -3x - 15⟩: graph both lines; they meet at ⟨({{-4}}, -3)⟩, so ⟨x = -4⟩.', 'Check by substitution: ⟨-2(-4) - 11 = -3 = -3(-4) - 15⟩ ✓.'])])

R[EQ, 4] = dict(obj='write and solve linear equations for mixture, motion and number problems',
  idea='Name the unknown, write each quantity in terms of it, and set up one equation from the relationship in the problem (total amount, total distance, sum).',
  voc=[['mixture problem', 'Combining solutions: amount of pure substance = concentration × volume.'], ['rate', 'Distance per unit time: d = rt.'], ['consecutive integers', 'n, n + 1, n + 2, ….']],
  watch='Adding percents directly instead of adding the amounts of pure substance.',
  cards=[dict(h='Applications of equations', big='Make a table: each row is one part, each column a quantity. The last column (amount of acid, distance, …) gives the {{equation}}.',
    steps=['Add x L of 50% acid to 2 L of 20%: ⟨0.5x + 0.2(2) = 0.26(x + 2)⟩.', '⟨0.5x + 0.4 = 0.26x + 0.52⟩, so ⟨0.24x = 0.12⟩ and ⟨x = {{\\tfrac{1}{2}}}⟩ L.', 'Cars at 30 and 45 mph going opposite ways separate at ⟨{{75}}⟩ mph: 375 miles takes ⟨{{5}}⟩ hours.'])])

R[EQ, 5] = dict(obj='solve linear, compound and polynomial inequalities and write the solutions in interval notation',
  idea='Solve like an equation, but reverse the inequality when multiplying or dividing by a negative; for polynomials, find the zeros and test each interval.',
  voc=[['compound inequality', 'Two inequalities joined by and or or, such as −12 ≤ 4x − 8 < −4.'], ['interval notation', 'Brackets [ ] include an endpoint; parentheses ( ) do not.'], ['test point', 'A value checked in each interval between zeros.']],
  watch='Forgetting to reverse the inequality sign when dividing by a negative number.',
  cards=[dict(h='Solving inequalities', big='Isolate x. Dividing by a {{negative}} reverses the sign. For ⟨p(x) > 0⟩, find the {{zeros}}, then test one point in each interval.',
    steps=['⟨-x - 6 > 7⟩: ⟨-x > 13⟩, so ⟨x < -13⟩: ⟨{{(-\\infty, -13)}}⟩.', '⟨-12 \\le 4x - 8 < -4⟩: add 8, divide by 4: ⟨-1 \\le x < 1⟩: ⟨{{[-1, 1)}}⟩.', '⟨(x - 1)(x + 3) > 0⟩: zeros −3 and 1; test 0 → negative, so ⟨{{(-\\infty, -3) \\cup (1, \\infty)}}⟩.'])])

R[EQ, 6] = dict(obj='move between inequalities, number-line graphs and interval notation',
  idea='An interval lists its left and right endpoints; a bracket means the endpoint is included (closed dot), a parenthesis means it is not (open dot), and ∞ always gets a parenthesis.',
  voc=[['closed interval', '[a, b]: both endpoints included.'], ['open interval', '(a, b): neither endpoint included.'], ['union ∪', 'Joins two intervals for an or statement.']],
  watch='Writing a bracket next to ∞, as in [−9, ∞].',
  cards=[dict(h='Interval notation', big='Closed dot → {{[ or ]}}; open dot → {{( or )}}. Infinity is never reached, so it always takes a {{parenthesis}}. "or" with two pieces is a {{union}}.',
    steps=['⟨x \\ge -9⟩ → ⟨{{[-9, \\infty)}}⟩.', '⟨-4 < x \\le 7⟩ → ⟨{{(-4, 7]}}⟩.', '⟨x < -6⟩ or ⟨x \\ge 7⟩ → ⟨{{(-\\infty, -6) \\cup [7, \\infty)}}⟩.'])])

R[EQ, 7] = dict(obj='graph linear inequalities in two variables and test points',
  idea='Graph the boundary line (dashed for < or >, solid for ≤ or ≥), then shade the side whose points make the inequality true.',
  voc=[['boundary line', 'The line y = mx + b where the two sides are equal.'], ['half-plane', 'All points on one side of a line.'], ['test point', 'A point such as (0, 0) checked in the inequality to choose the side.']],
  watch='Shading above for ≤ (or below for ≥) without testing a point.',
  cards=[dict(h='Linear inequalities in two variables', big='Draw ⟨y = mx + b⟩: {{dashed}} for ⟨<, >⟩, {{solid}} for ⟨\\le, \\ge⟩. A point is a solution when it makes the inequality true; shade that side.',
    steps=['Is (−5, 3) a solution of ⟨y < -x + 2⟩? ⟨3 < 5 + 2 = 7⟩ → {{yes}}.', 'Graph ⟨y \\ge -2x + 2⟩: solid line, test (0, 0): ⟨0 \\ge 2⟩ is false, so shade the side {{away from}} the origin.'])])

R[EQ, 8] = dict(obj='solve systems of two linear equations by substitution and elimination',
  idea='Eliminate one variable — by substituting an isolated variable or by adding multiples of the equations — then back-substitute.',
  voc=[['system', 'Two or more equations solved together.'], ['substitution', 'Replacing a variable with an equal expression.'], ['elimination', 'Adding multiples of equations so one variable cancels.']],
  watch='Multiplying only one side (or one term) of an equation before adding.',
  cards=[dict(h='Systems in two variables', big='Solve one equation for a variable and {{substitute}}, or scale the equations so a variable has opposite coefficients and {{add}}. Check the pair in both equations.',
    steps=['⟨-6x + y = 22⟩ gives ⟨y = 6x + 22⟩.', 'Into ⟨3x + 2y = -1⟩: ⟨3x + 12x + 44 = -1⟩, so ⟨x = {{-3}}⟩.', '⟨y = 6(-3) + 22 = {{4}}⟩: solution ⟨(-3, 4)⟩.'])])

R[EQ, 9] = dict(obj='solve systems of three linear equations in three variables',
  idea='Use one equation to eliminate a variable from the other two, solve the resulting 2-by-2 system, then back-substitute.',
  voc=[['ordered triple', '(x, y, z), a solution of a three-variable system.'], ['back-substitution', 'Using solved values to find the remaining variables.'], ['inconsistent system', 'A system with no solution.']],
  watch='Eliminating different variables in the two new equations, which leaves three unknowns.',
  cards=[dict(h='Systems in three variables', big='Pick one variable to remove. Combine pairs of equations to get {{two equations in two variables}}, solve them, then substitute back for the third.',
    steps=['⟨x + y + z = 11⟩, ⟨x + 2z = 8⟩, ⟨y + 3z = 11⟩: ⟨x = 8 - 2z⟩, ⟨y = 11 - 3z⟩.', 'Substitute: ⟨8 - 2z + 11 - 3z + z = 11⟩, so ⟨-4z = -8⟩ and ⟨z = {{2}}⟩.', '⟨x = {{4}}⟩, ⟨y = {{5}}⟩: ⟨(4, 5, 2)⟩.'])])

R[EQ, 10] = dict(obj='graph systems of linear inequalities and find the corner points of the feasible region',
  idea='The solution of a system of inequalities is the overlap of the half-planes; its corners are where boundary lines meet.',
  voc=[['feasible region', 'The set of points that satisfy every inequality.'], ['vertex (corner point)', 'A point where two boundary lines meet on the region.'], ['bounded region', 'A region that can be enclosed in a circle.']],
  watch='Including an intersection of two lines that lies outside the region as a corner.',
  cards=[dict(h='Systems of inequalities', big='Shade each inequality; the solution is where all shadings {{overlap}}. Find each corner by solving the two boundary equations that meet there, and check it in the other inequalities.',
    steps=['⟨2x + 6y = 12⟩ and ⟨4x + 4y = 16⟩: from the second, ⟨x = 4 - y⟩.', '⟨2(4 - y) + 6y = 12⟩ → ⟨4y = 4⟩, ⟨y = 1⟩, ⟨x = 3⟩: corner ⟨({{3}}, {{1}})⟩.', 'Is (1, 1) in the region? ⟨4 + 8 \\le 32⟩ and ⟨6 + 4 \\le 24⟩ → {{yes}}.'])])

R[EQ, 11] = dict(obj='use linear programming to find the maximum or minimum of an objective function',
  idea='A linear objective function on a bounded feasible region takes its maximum and minimum at corner points.',
  voc=[['objective function', 'The quantity to optimize, such as P = 2x + 6y.'], ['constraint', 'An inequality the variables must satisfy.'], ['optimal solution', 'The corner point that gives the best value.']],
  watch='Evaluating the objective at points that are not corners, or at intersections outside the feasible region.',
  cards=[dict(h='Linear programming', big='1. Graph the constraints. 2. List the {{corner points}}. 3. Evaluate the objective at each. 4. The largest (smallest) value is the {{maximum (minimum)}}.',
    steps=['⟨P = 2x + 6y⟩ with ⟨x, y \\ge 0⟩, ⟨3x + 6y \\le 18⟩, ⟨5x + 5y \\le 25⟩.', 'Corners: (0, 0), (5, 0), (0, 3), and (4, 1) where the lines meet.', '⟨P⟩: 0, 10, 18, 14 → maximum ⟨P = {{18}}⟩ at ⟨(0, 3)⟩.'])])

# ----------------------------------------------------------------- functions
R[FN, 1] = dict(obj='find slopes, intercepts and zeros of linear functions from equations and graphs',
  idea='For y = mx + b the slope is m and the y-intercept is (0, b); the zero is where y = 0, at x = −b/m.',
  voc=[['y-intercept', 'The point where a graph crosses the y-axis, (0, b).'], ['zero', 'The x-value where f(x) = 0.'], ['rate of change', 'The slope: change in y per unit change in x.']],
  watch='Giving b as the x-intercept, or reading the slope from Ax + By = C as A.',
  cards=[dict(h='Linear graphs', big='Slope ⟨m⟩ = {{rise over run}}. y-intercept: set ⟨x = 0⟩. Zero (x-intercept): set ⟨y = 0⟩. For ⟨Ax + By = C⟩ solve for ⟨y⟩ first.',
    steps=['⟨f(x) = -6x - 1⟩: y-intercept ⟨({{0}}, {{-1}})⟩.', '⟨5x + 4y = -6⟩: ⟨y = -\\tfrac{5}{4}x - \\tfrac{3}{2}⟩, slope ⟨{{-\\tfrac{5}{4}}}⟩.', 'Zero of ⟨2x - 8⟩: ⟨2x - 8 = 0⟩, ⟨x = {{4}}⟩.'])])

R[FN, 2] = dict(obj='add, subtract, multiply, divide and compose functions',
  idea='(f ∘ g)(x) = f(g(x)): evaluate the inner function first and use its output as the input of the outer one.',
  voc=[['composition', '(f ∘ g)(x) = f(g(x)).'], ['inner function', 'The function applied first (g in f(g(x))).'], ['domain of a quotient', 'Excludes x where the denominator is 0.']],
  watch='Multiplying f(x)·g(x) when the question asks for f(g(x)), or composing in the wrong order.',
  cards=[dict(h='Operations and composition', big='⟨(f+g)(x) = f(x) + g(x)⟩, ⟨(fg)(x) = f(x)g(x)⟩, and ⟨(f \\circ g)(x) = f(g(x))⟩: work from the {{inside out}}.',
    steps=['⟨f(x) = 2x + 9⟩, ⟨g(x) = 2x + 5⟩: ⟨(g \\circ f)(-1) = g(f(-1)) = g(7) = {{19}}⟩.', '⟨f(x) = -x + 8⟩, ⟨g(x) = 2x + 2⟩: ⟨(f \\cdot g)(x) = (-x + 8)(2x + 2) = {{-2x^2 + 14x + 16}}⟩.', '⟨f(x) = -4x - 5⟩, ⟨g(x) = x - 2⟩: ⟨f(g(x)) = -4(x - 2) - 5 = {{-4x + 3}}⟩.'])])

R[FN, 3] = dict(obj='iterate a function from a starting value and describe the pattern of the iterates',
  idea='Iteration feeds each output back in as the next input: x₁ = f(x₀), x₂ = f(x₁), x₃ = f(x₂).',
  voc=[['iterate', 'An output of repeated application: xₙ = f(xₙ₋₁).'], ['seed', 'The starting value x₀.'], ['fixed point', 'A value with f(x) = x; iterates there stay there.']],
  watch='Stopping one step early (giving x₂ for x₃) or multiplying x₁ by 3.',
  cards=[dict(h='Function iteration', big='Start at the {{seed}} ⟨x_0⟩ and apply ⟨f⟩ repeatedly, using each {{output as the next input}}.',
    steps=['⟨f(x) = -3x + 2⟩, ⟨x_0 = 2⟩: ⟨x_1 = -4⟩, ⟨x_2 = 14⟩, ⟨x_3 = {{-40}}⟩.', '⟨f(x) = x^2 + 1⟩, ⟨x_0 = 1⟩: ⟨x_1 = 2⟩, ⟨x_2 = 5⟩, ⟨x_3 = {{26}}⟩.', 'Fixed point of ⟨f(x) = -x + 3⟩: ⟨x = -x + 3⟩, ⟨x = {{1.5}}⟩.'])])

R[FN, 4] = dict(obj='recognize the twelve basic functions and state their domains, ranges and key features',
  idea='Each basic function has a signature shape and domain: x, x², x³, √x, |x|, 1/x, eˣ, ln x, sin x, cos x, ⌊x⌋ and the logistic 1/(1 + e⁻ˣ).',
  voc=[['domain', 'All allowed inputs.'], ['range', 'All outputs the function takes.'], ['bounded', 'Its outputs stay between two numbers.']],
  watch='Including 0 (or negatives) in the domain of ln x, or giving 1/x a domain that includes 0.',
  cards=[dict(h='The basic functions', big='Domains: ⟨\\sqrt{x}⟩ needs {{x ≥ 0}}, ⟨\\ln x⟩ needs {{x > 0}}, ⟨\\tfrac{1}{x}⟩ needs {{x ≠ 0}}; the others accept all reals. Ranges: ⟨e^x⟩ is ⟨(0, \\infty)⟩, ⟨|x|⟩ and ⟨x^2⟩ are ⟨[0, \\infty)⟩, sine and cosine are ⟨[-1, 1]⟩.',
    steps=['Domain of ⟨f(x) = \\tfrac{1}{x + 4}⟩: ⟨x \\ne -4⟩, so ⟨{{(-\\infty, -4) \\cup (-4, \\infty)}}⟩.', 'Domain ⟨(0, \\infty)⟩ and through (1, 0): {{ln x}}.', 'Range ⟨(0, \\infty)⟩ and through (0, 1): {{eˣ}}.'])])

R[FN, 5] = dict(obj='evaluate and graph piecewise, step and absolute value functions',
  idea='A piecewise function uses a different rule on each part of its domain: find which condition the input satisfies, then use that rule.',
  voc=[['piecewise function', 'A function defined by different rules on different intervals.'], ['greatest integer ⌊x⌋', 'The greatest integer less than or equal to x.'], ['absolute value', '|x| = x for x ≥ 0 and −x for x < 0.']],
  watch='Rounding a negative number toward zero with ⌊x⌋ (⌊−3.75⌋ is −4, not −3).',
  cards=[dict(h='Piecewise and step functions', big='First check the {{condition}} the input meets, then evaluate only that piece. ⌊x⌋ always rounds {{down}}.',
    steps=['⟨f(x) = -4x + 2⟩ if ⟨x < 2⟩; ⟨-4x - 6⟩ if ⟨x \\ge 2⟩. ⟨f(4)⟩: ⟨4 \\ge 2⟩, so ⟨-16 - 6 = {{-22}}⟩.', '⟨\\lfloor -3.75 \\rfloor = {{-4}}⟩ and ⟨\\lfloor 2.9 \\rfloor = {{2}}⟩.', '⟨|x - 3|⟩ at ⟨x = 1⟩: ⟨|-2| = {{2}}⟩.'])])

R[FN, 6] = dict(obj='write and describe transformations of parent functions',
  idea='y = a·f(x − h) + k moves the parent graph h units horizontally and k vertically, stretches it by |a|, and reflects it in the x-axis when a < 0.',
  voc=[['translation', 'A shift left/right or up/down.'], ['vertical stretch', 'Multiplying outputs by |a| > 1.'], ['reflection', 'A flip across an axis (a < 0 flips over the x-axis).']],
  watch='Shifting the wrong way horizontally: f(x − 4) moves right 4, not left.',
  cards=[dict(h='Graph transformations', big='Inside the function (with ⟨x⟩) acts {{horizontally and opposite}} to the sign; outside acts {{vertically and as written}}.',
    steps=['⟨\\sqrt{x}⟩ shifted 2 up: ⟨g(x) = {{\\sqrt{x} + 2}}⟩.', '⟨|x|⟩ left 3, then up 5: ⟨g(x) = {{|x + 3| + 5}}⟩.', '⟨y = (x - 4)^2 - 1⟩ is ⟨x^2⟩ moved {{4 right and 1 down}}.'])])

R[FN, 7] = dict(obj='find images of points and describe families of graphs under transformations',
  idea='Under y = a·f(b(x − h)) + k, a point (x, y) on f goes to (x/b + h, a·y + k).',
  voc=[['image point', 'Where a point lands after a transformation.'], ['horizontal compression', 'f(bx) with |b| > 1 squeezes the graph toward the y-axis by 1/b.'], ['family of graphs', 'Graphs that are transformations of one parent.']],
  watch='Applying the inside operations to the x-coordinate in the written order instead of undoing them.',
  cards=[dict(h='Images of points', big='For ⟨y = a\\,f(b(x - h)) + k⟩: new ⟨x = \\frac{x}{b} + h⟩, new ⟨y = a\\,y + k⟩. Undo the inside, apply the outside.',
    steps=['(2, 0) on ⟨f⟩; ⟨y = f(x - 2) + 4⟩: ⟨({{4}}, {{4}})⟩.', '(4, 6) on ⟨f⟩; ⟨y = -2f(\\tfrac{1}{2}(x - 4)) + 1⟩: ⟨x = 4 \\cdot 2 + 4 = {{12}}⟩, ⟨y = -12 + 1 = {{-11}}⟩.', '⟨y = |x - 2| - 3⟩ is ⟨|x|⟩ moved {{2 right and 3 down}}.'])])

R[FN, 8] = dict(obj='solve absolute value and nonlinear inequalities and write the solutions in interval notation',
  idea='|u| < c means −c < u < c (one interval); |u| > c means u < −c or u > c (two pieces).',
  voc=[['absolute value inequality', 'An inequality containing |u|.'], ['"less than" case', '|u| < c becomes a single compound inequality.'], ['"greater than" case', '|u| > c becomes a union of two rays.']],
  watch='Writing |x − 7| > 10 as −10 > x − 7 > 10, which has no solutions.',
  cards=[dict(h='Absolute value inequalities', big='⟨|u| < c⟩ → ⟨{{-c < u < c}}⟩. ⟨|u| > c⟩ → ⟨{{u < -c}}⟩ or ⟨{{u > c}}⟩. Keep ⟨\\le, \\ge⟩ as closed brackets.',
    steps=['⟨|x - 7| > 10⟩: ⟨x - 7 < -10⟩ or ⟨x - 7 > 10⟩ → ⟨{{(-\\infty, -3) \\cup (17, \\infty)}}⟩.', '⟨|x - 5| \\le 3⟩: ⟨-3 \\le x - 5 \\le 3⟩ → ⟨{{[2, 8]}}⟩.', '⟨|3x + 6| > 4⟩: ⟨x < -\\tfrac{10}{3}⟩ or ⟨x > -\\tfrac{2}{3}⟩.'])])

R[FN, 9] = dict(obj='find inverse functions algebraically and evaluate f⁻¹ at a point',
  idea='Swap x and y and solve for y; f⁻¹ undoes f, so f⁻¹(b) = a exactly when f(a) = b.',
  voc=[['inverse function', 'f⁻¹ with f⁻¹(f(x)) = x and f(f⁻¹(x)) = x.'], ['one-to-one', 'Each output comes from one input, so an inverse function exists.'], ['horizontal line test', 'A graph is one-to-one if no horizontal line meets it twice.']],
  watch='Writing f⁻¹(x) as 1/f(x).',
  cards=[dict(h='Inverse functions', big='Write ⟨y = f(x)⟩, {{swap x and y}}, solve for ⟨y⟩. To evaluate ⟨f^{-1}(b)⟩, solve ⟨f(x) = b⟩.',
    steps=['⟨f(x) = -4x - 2⟩: ⟨x = -4y - 2⟩, ⟨y = {{-\\tfrac{1}{4}x - \\tfrac{1}{2}}}⟩.', '⟨f(x) = -2x^3 + 5⟩, ⟨f^{-1}(21)⟩: ⟨-2x^3 + 5 = 21⟩, ⟨x^3 = -8⟩, ⟨x = {{-2}}⟩.', 'Check: ⟨f(-2) = 16 + 5 = 21⟩ ✓.'])])

R[FN, 10] = dict(obj='write and use direct, inverse and joint variation models',
  idea='Direct: y = kx. Inverse: y = k/x. Joint: y = kxz. Find k from one data point, then use it.',
  voc=[['constant of variation', 'The fixed number k in the model.'], ['direct variation', 'y = kx: y doubles when x doubles.'], ['inverse variation', 'y = k/x: y halves when x doubles.']],
  watch='Using the direct model for an inverse-variation situation (more workers, less time).',
  cards=[dict(h='Variation', big='Write the model, substitute the known pair to find {{k}}, then substitute the new value.',
    steps=['Direct, ⟨y = 4⟩ when ⟨x = 2⟩: ⟨k = 2⟩; when ⟨x = 10⟩, ⟨y = {{20}}⟩.', 'Inverse, ⟨y = \\tfrac{9}{8}⟩ when ⟨x = 8⟩: ⟨k = 9⟩; when ⟨x = 6⟩, ⟨y = {{\\tfrac{3}{2}}}⟩.', 'Joint ⟨z = kxy⟩, ⟨z = 24⟩ when ⟨x = 2, y = 3⟩: ⟨k = {{4}}⟩.'])])

R[FN, 11] = dict(obj='solve quadratic equations and equations in quadratic form',
  idea='Set the equation equal to 0 and factor, complete the square, or use the quadratic formula; for quadratic form, substitute u for the repeated expression.',
  voc=[['quadratic formula', 'x = (−b ± √(b² − 4ac))/(2a).'], ['discriminant', 'b² − 4ac: tells the number and kind of solutions.'], ['quadratic form', 'An equation like u² + bu + c = 0 with u = x², √x or x^(1/3).']],
  watch='Dividing both sides by x and losing the solution x = 0.',
  cards=[dict(h='Quadratic equations', big='Get 0 on one side; factor if you can, otherwise use ⟨x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}⟩. For quadratic form, let ⟨u⟩ be the {{repeated expression}}, solve for ⟨u⟩, then for ⟨x⟩.',
    steps=['⟨x^2 - 8x = 0⟩: ⟨x(x - 8) = 0⟩ → ⟨x = {{0}}⟩ or ⟨x = {{8}}⟩.', '⟨x - 5\\sqrt{x} + 4 = 0⟩: ⟨u = \\sqrt{x}⟩, ⟨(u - 1)(u - 4) = 0⟩ → ⟨x = {{1}}⟩ or ⟨{{16}}⟩.', '⟨x^2 + x - 30 = 0⟩: ⟨(x + 6)(x - 5) = 0⟩ → ⟨x = -6⟩ or ⟨5⟩.'])])

R[FN, 12] = dict(obj='find vertical and horizontal asymptotes and holes of rational functions',
  idea='Vertical asymptotes come from zeros of the denominator that do not cancel; the horizontal asymptote compares the degrees of numerator and denominator.',
  voc=[['vertical asymptote', 'x = a where the function grows without bound.'], ['horizontal asymptote', 'y = L that the graph approaches as |x| → ∞.'], ['hole', 'A removable gap where a common factor cancels.']],
  watch='Calling a canceled factor a vertical asymptote instead of a hole.',
  cards=[dict(h='Rational functions', big='Factor and cancel first (cancelled factors give {{holes}}). Equal degrees → ⟨y⟩ = {{ratio of the leading coefficients}}; top degree lower → ⟨y = 0⟩; top degree higher → no horizontal asymptote.',
    steps=['⟨f(x) = \\frac{4x + 4}{x + 2}⟩: degrees equal, ⟨y = {{4}}⟩; vertical ⟨x = {{-2}}⟩.', '⟨\\frac{x^2 - 1}{x - 1} = x + 1⟩ for ⟨x \\ne 1⟩: hole at ⟨({{1}}, {{2}})⟩.', '⟨\\frac{3}{x^2 + 1}⟩: top degree lower → ⟨y = {{0}}⟩.'])])

R[FN, 13] = dict(obj='use the Remainder and Factor Theorems to find remainders and test factors',
  idea='The remainder when P(x) is divided by x − c is P(c); x − c is a factor exactly when P(c) = 0.',
  voc=[['Remainder Theorem', 'P(x) ÷ (x − c) has remainder P(c).'], ['Factor Theorem', 'x − c is a factor of P(x) if and only if P(c) = 0.'], ['synthetic division', 'A shortcut for dividing by x − c.']],
  watch='Substituting −c instead of c (dividing by x + 2 means using c = −2).',
  cards=[dict(h='Remainder and Factor Theorems', big='Divide by ⟨x - c⟩ → evaluate ⟨P(c)⟩. If ⟨P(c) = 0⟩, then ⟨x - c⟩ is a {{factor}}.',
    steps=['⟨P(x) = -2x^2 - 4x - 3⟩ ÷ ⟨(x - 1)⟩: ⟨P(1) = -2 - 4 - 3 = {{-9}}⟩.', '⟨P(x) = 3x^2 - x - 6⟩ ÷ ⟨(x - 2)⟩: ⟨P(2) = 12 - 2 - 6 = {{4}}⟩.', 'Is ⟨x + 1⟩ a factor of ⟨x^3 + 1⟩? ⟨P(-1) = 0⟩ → {{yes}}.'])])

R[FN, 14] = dict(obj='find all zeros of a polynomial given one zero, and locate real zeros',
  idea='Divide out a known zero to reduce the degree, then factor or use the quadratic formula on the quotient.',
  voc=[['depressed polynomial', 'The quotient after dividing out a known factor.'], ['Rational Root Theorem', 'Possible rational zeros are ±(factors of the constant)/(factors of the leading coefficient).'], ['Intermediate Value Theorem', 'A sign change on [a, b] means a zero between a and b.']],
  watch='Stopping after the given zero, or dropping the remainder check in synthetic division.',
  cards=[dict(h='Locating polynomial zeros', big='Use synthetic division with the known zero; the remainder must be {{0}}. Solve the {{quotient}} for the rest.',
    steps=['⟨x = -1⟩ is a zero of ⟨x^3 - 6x^2 + 3x + 10⟩: quotient ⟨x^2 - 7x + 10⟩.', '⟨x^2 - 7x + 10 = (x - 2)(x - 5)⟩ → ⟨x = {{2}}⟩ or ⟨{{5}}⟩.', '⟨f(1) = -2⟩, ⟨f(2) = 3⟩ → a zero lies between {{1 and 2}}.'])])

R[FN, 15] = dict(obj='evaluate and interpret exponential and logistic growth and decay models',
  idea='f(x) = a·bˣ starts at a and multiplies by b each step (growth if b > 1, decay if 0 < b < 1); a logistic model L/(1 + Ae^(−kt)) levels off at the carrying capacity L.',
  voc=[['growth factor', 'The base b; the rate is b − 1.'], ['logistic model', 'Growth that slows as it nears a limit L.'], ['carrying capacity', 'The limit L a logistic model approaches.']],
  watch='Using the percent rate as the base: 4% growth means b = 1.04, not 4 or 0.04.',
  cards=[dict(h='Exponential and logistic models', big='⟨f(x) = a\\,b^x⟩: {{initial value}} ⟨a⟩, growth factor ⟨b = 1 + r⟩. Logistic ⟨P(t) = \\frac{L}{1 + Ae^{-kt}}⟩: ⟨P(0) = \\frac{L}{1 + A}⟩ and the {{carrying capacity}} is ⟨L⟩.',
    steps=['⟨f(4)⟩ for ⟨300(3)^x⟩: ⟨300 \\cdot 81 = {{24\\,300}}⟩.', 'Town of 12,000 growing 3% a year: ⟨P(t) = 12\\,000(1.03)^t⟩.', '⟨P(t) = \\frac{4200}{1 + 11e^{-0.2t}}⟩: ⟨P(0) = \\frac{4200}{12} = {{350}}⟩, capacity ⟨{{4200}}⟩.'])])

R[FN, 16] = dict(obj='use the number e in continuous growth and solve simple equations with eˣ',
  idea='Continuous compounding gives A = Pe^(rt); natural logs undo e: if e^(kx) = c then x = ln(c)/k.',
  voc=[['e', 'The irrational number ≈ 2.71828, the limit of (1 + 1/n)ⁿ.'], ['continuous compounding', 'Interest compounded at every instant: A = Pe^(rt).'], ['natural logarithm', 'ln x, the inverse of eˣ.']],
  watch='Using A = P(1 + r)ᵗ (annual compounding) for continuous growth.',
  cards=[dict(h='The number e', big='⟨A = Pe^{rt}⟩ with ⟨r⟩ as a {{decimal}}. To solve ⟨e^{kx} = c⟩, take ⟨\\ln⟩ of both sides: ⟨x = \\frac{\\ln c}{k}⟩.',
    steps=['$2,400 at 4% for 10 years: ⟨A = 2400e^{0.4} \\approx {{\\$3580.38}}⟩.', '⟨e^{4x} = 10⟩: ⟨4x = \\ln 10⟩, ⟨x = {{\\tfrac{\\ln 10}{4}}}⟩.', '⟨e^{0} = {{1}}⟩, so every ⟨Pe^{rt}⟩ starts at ⟨P⟩.'])])

R[FN, 17] = dict(obj='evaluate logarithms, find their domains and graph logarithmic functions',
  idea='log_b(x) = y means bʸ = x; logarithms are defined only for positive arguments.',
  voc=[['logarithm', 'log_b x: the exponent that gives x with base b.'], ['common log', 'log x, base 10.'], ['natural log', 'ln x, base e.']],
  watch='Allowing zero or negative arguments in the domain of a log function.',
  cards=[dict(h='Logarithmic functions', big='⟨\\log_b x = y \\iff b^y = x⟩. Domain of ⟨\\log_b(u)⟩: {{u > 0}}. The graph of ⟨\\log_b x⟩ passes through ⟨(1, 0)⟩ and has the vertical asymptote ⟨x = 0⟩.',
    steps=['⟨\\log_5 25 = {{2}}⟩ because ⟨5^2 = 25⟩.', 'Domain of ⟨\\ln(-x + 3)⟩: ⟨-x + 3 > 0⟩, ⟨x < 3⟩: ⟨{{(-\\infty, 3)}}⟩.', '⟨\\log_2 \\tfrac{1}{8} = {{-3}}⟩.'])])

R[FN, 18] = dict(obj='solve exponential and logarithmic equations exactly and with technology',
  idea='Rewrite both sides with the same base when you can; otherwise take a logarithm of both sides. For log equations, rewrite in exponential form and check the domain.',
  voc=[['one-to-one property', 'b^m = b^n means m = n; log_b m = log_b n means m = n.'], ['change of base', 'log_b x = ln x / ln b.'], ['extraneous solution', 'A result that makes an original log argument ≤ 0.']],
  watch='Keeping a solution that makes a logarithm’s argument negative.',
  cards=[dict(h='Exponential and logarithmic equations', big='Same base → set {{exponents}} equal. Otherwise isolate the power and take ⟨\\ln⟩. Log equations: rewrite as ⟨b^y = x⟩ and {{check}} the answer.',
    steps=['⟨2^{x - 4} = 8 = 2^3⟩ → ⟨x - 4 = 3⟩, ⟨x = {{7}}⟩.', '⟨e^x = 89⟩ → ⟨x = \\ln 89 \\approx {{4.489}}⟩.', '⟨\\log_3(x + 1) = 2⟩ → ⟨x + 1 = 9⟩, ⟨x = {{8}}⟩.'])])
