"""Teaching notes for the 59 8th Grade Math skills (8th Grade Math audit #1, 2026-11-19).
Each record: obj (objective, completes "Students will be able to …"), idea (key idea), voc ([term, meaning] pairs),
watch (common mistake) and one explanation card (h, big, steps; {{…}} marks a blank on guided notes).
Run: python3 tools/grade8-audit-20261119/notes.py  → worksheet-generator/planner/notes-teach-prealgebra.js"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def R(obj, idea, voc, watch, h, big, steps):
    return {'obj': obj, 'idea': idea, 'voc': voc, 'watch': watch, 'cards': [{'h': h, 'big': big, 'steps': steps}]}


N = {}
# ======================================================================= Real Numbers and Exponents
u = 'real-numbers-exponents-skill-'
N[u + '01'] = R('classify numbers as natural, whole, integer and rational, and order rational numbers',
    'A rational number can be written as a fraction a/b of integers with b ≠ 0; every integer, terminating decimal and repeating decimal is rational, and the sets nest: natural ⊂ whole ⊂ integer ⊂ rational.',
    [['rational number', 'A number that can be written as a/b with integers a and b, b ≠ 0.'], ['integer', 'A whole number or its opposite: …, −2, −1, 0, 1, 2, ….'], ['whole number', '0, 1, 2, 3, ….']],
    'Thinking a negative number or a decimal cannot be rational, or ordering negatives by their absolute values (−4 > −1).',
    'Classifying and ordering', 'Classify −6 and order −1.6, −0.5, 4/5, −4.',
    ['−6 is an {{integer}} and a {{rational}} number, but not a whole number.', 'On a number line, farther left is smaller: {{−4 < −1.6 < −0.5 < 4/5}}.', 'Halfway between 1/6 and 4/5: (1/6 + 4/5) ÷ 2 = {{29/60}}.'])
N[u + '02'] = R('add, subtract, multiply and divide rational numbers, including negatives',
    'Use the integer sign rules with fractions and decimals: same signs multiply or divide to a positive, different signs to a negative; to subtract, add the opposite.',
    [['additive inverse', 'The opposite of a number; a + (−a) = 0.'], ['reciprocal', 'The number you multiply by to get 1; the reciprocal of a/b is b/a.'], ['absolute value', 'Distance from 0 on a number line.']],
    'Adding numerators and denominators (−3/4 − 4/9 ≠ −7/13), or forgetting to flip the divisor when dividing fractions.',
    'Operations with rational numbers', 'Evaluate 5/4 ÷ (−1/3) and −3/4 − 4/9.',
    ['Multiply by the reciprocal: 5/4 · (−3) = {{−15/4}}.', 'Common denominator 36: −27/36 − 16/36 = {{−43/36}}.', 'A diver at −23 ft rises 4.5 ft/min for 7 min: −23 + 31.5 = {{8.5 ft}}.'])
N[u + '03'] = R('convert between fractions and decimals, including repeating decimals',
    'Divide to turn a fraction into a decimal: it terminates when the simplified denominator has only factors 2 and 5, otherwise it repeats. To turn a repeating decimal into a fraction, multiply by a power of 10 and subtract.',
    [['terminating decimal', 'A decimal that ends, such as 0.125.'], ['repeating decimal', 'A decimal with a block of digits that repeats forever, such as 0.0833… .'], ['bar notation', 'A bar over the digits that repeat.']],
    'Writing 0.333… as 33/100, or thinking 1/12 terminates because 12 is even.',
    'Repeating decimal to fraction', 'Write n = 0.4545… (45 repeats) as a fraction.',
    ['Two digits repeat, so multiply by 100: 100n = {{45.4545…}}.', 'Subtract n: 99n = {{45}}.', 'n = 45/99 = {{5/11}}.'])
N[u + '04'] = R('identify irrational numbers and explain why they are irrational',
    'An irrational number cannot be written as a ratio of integers; its decimal never ends or repeats. The square root of a whole number that is not a perfect square is irrational, and so is π.',
    [['irrational number', 'A real number that is not rational; its decimal never terminates or repeats.'], ['perfect square', 'The square of an integer: 1, 4, 9, 16, ….'], ['real numbers', 'All rational and irrational numbers.']],
    'Calling √60 rational because 60 is a whole number, or calling 3.14 or 22/7 irrational because they approximate π.',
    'Rational or irrational?', 'Classify √49, √50, 0.1010010001… and −1/3.',
    ['√49 = 7, so it is {{rational}}.', '50 is not a perfect square, so √50 is {{irrational}}.', '0.1010010001… never repeats: {{irrational}}; −1/3 is a ratio of integers: {{rational}}.'])
N[u + '05'] = R('decide whether sums and products involving irrational numbers are rational or irrational',
    'Rational + irrational is always irrational, and a nonzero rational times an irrational is irrational; two irrationals can combine to give a rational (√2 · √2 = 2), so check each case.',
    [['closure', 'A set is closed under an operation when the result is always in the set.'], ['counterexample', 'One example that shows a general claim is false.'], ['nonzero', 'Not equal to 0.']],
    'Assuming the product or sum of two irrational numbers must be irrational.',
    'Sums and products', 'Decide whether each value is rational.',
    ['8 + √11: rational + irrational = {{irrational}}.', '√7 · √63 = √441 = {{21}}, rational.', '0 · √5 = 0 is rational, so the rule needs a {{nonzero}} rational.'])
N[u + '06'] = R('compare and order irrational numbers by estimating them',
    'Estimate a square root by trapping it between consecutive perfect squares, then refine to tenths; compare squares when both numbers are positive.',
    [['estimate', 'A close value found by reasoning rather than exact computation.'], ['between', 'Greater than one number and less than another.'], ['number line', 'A line on which every real number has a point.']],
    'Comparing √50 and 7.1 by the digits instead of squaring: 7.1² = 50.41 > 50.',
    'Comparing with squares', 'Which is greater, √50 or 7.1? Order 2.1, √10, 7/4, √15.',
    ['7.1² = {{50.41}} > 50, so {{7.1}} is greater.', '√10 ≈ 3.16 and √15 ≈ 3.87; 7/4 = 1.75.', 'Order: {{7/4, 2.1, √10, √15}}.'])
N[u + '07'] = R('evaluate square and cube roots of perfect squares and cubes, and approximate other roots',
    '√a is the nonnegative number whose square is a; ∛a is the number whose cube is a (it can be negative). A non-perfect root lies between the roots of the nearest perfect squares.',
    [['square root', '√a: the nonnegative number whose square is a.'], ['cube root', '∛a: the number whose cube is a.'], ['perfect cube', 'The cube of an integer: 1, 8, 27, 64, ….']],
    'Writing √(9 + 16) = √9 + √16 = 7, or saying ∛(−8) has no value.',
    'Roots', 'Evaluate and estimate.',
    ['√196 = {{14}} because 14² = 196.', '∛(−125) = {{−5}}.', '√143 is between {{11 and 12}}, close to 12 because 143 is close to 144.'])
N[u + '08'] = R('evaluate and rewrite powers with zero and negative integer exponents',
    'Each step down in the exponent divides by the base, so a⁰ = 1 and a⁻ⁿ = 1/aⁿ for a ≠ 0; a negative exponent makes a reciprocal, not a negative number.',
    [['exponent', 'The number of times the base is used as a factor.'], ['negative exponent', 'a⁻ⁿ = 1/aⁿ.'], ['zero exponent', 'a⁰ = 1 for any a ≠ 0.']],
    'Reading 2⁻³ as −8 or −6, or moving the coefficient as well (8x⁻³ ≠ 1/(8x³)).',
    'Negative exponents', 'Continue 2² = 4, 2¹ = 2, 2⁰ = 1, ….',
    ['2⁻¹ = {{1/2}}, 2⁻² = {{1/4}}, 2⁻³ = {{1/8}}.', 'Write 1/25 as a power of 5: {{5⁻²}}.', 'Rewrite 8x⁻³ with positive exponents: {{8/x³}}.'])
N[u + '09'] = R('simplify expressions with integer exponents using the exponent rules',
    'Multiply powers of the same base by adding exponents, divide by subtracting, and raise a power to a power by multiplying; then write the result with positive exponents.',
    [['product of powers', 'aᵐ · aⁿ = aᵐ⁺ⁿ.'], ['quotient of powers', 'aᵐ ÷ aⁿ = aᵐ⁻ⁿ.'], ['power of a power', '(aᵐ)ⁿ = aᵐⁿ.']],
    'Multiplying exponents when multiplying powers (x⁻² · x⁶ ≠ x⁻¹²), or not raising the coefficient to the power.',
    'Exponent rules', 'Simplify with positive exponents.',
    ['x⁻² · x⁶ = x^(−2 + 6) = {{x⁴}}.', '(2x⁻⁴)⁻² = 2⁻² · x⁸ = {{x⁸/4}}.', '(3⁻²)⁻² = 3⁴ = {{81}}.'])
N[u + '10'] = R('write numbers in scientific notation and standard form and compare them',
    'Scientific notation is a × 10ⁿ with 1 ≤ a < 10: move the decimal point until one nonzero digit is left of it, and count the moves (negative for numbers less than 1).',
    [['scientific notation', 'a × 10ⁿ with 1 ≤ a < 10 and n an integer.'], ['standard form', 'The number written out with all its digits.'], ['order of magnitude', 'The power of 10 that a number is closest to.']],
    'Using a positive exponent for a small number (0.0007 = 7 × 10⁴), or leaving a first factor of 10 or more (54.3 × 10³).',
    'Scientific notation', 'Convert and compare.',
    ['0.0071 = {{7.1 × 10⁻³}}.', '54.3 × 10³ = 5.43 × 10¹ × 10³ = {{5.43 × 10⁴}}.', '9 × 10⁸ is {{900}} times as large as 1 × 10⁶.'])
N[u + '11'] = R('multiply, divide, add and subtract numbers in scientific notation',
    'Multiply or divide the first factors and add or subtract the exponents; to add or subtract, first write both numbers with the same power of 10. Normalize the result so the first factor is from 1 to 10.',
    [['first factor', 'The number a in a × 10ⁿ.'], ['normalize', 'Rewrite so that 1 ≤ a < 10.'], ['power of 10', '10ⁿ.']],
    'Multiplying the exponents, or adding first factors with different powers of 10.',
    'Operations in scientific notation', 'Compute and normalize.',
    ['(3 × 10²)(4 × 10⁴) = 12 × 10⁶ = {{1.2 × 10⁷}}.', '(1 × 10⁻³) ÷ (2 × 10⁻¹) = 0.5 × 10⁻² = {{5 × 10⁻³}}.', '3 × 10⁶ + 5.2 × 10⁵ = 3 × 10⁶ + 0.52 × 10⁶ = {{3.52 × 10⁶}}.'])

# ======================================================================= Equations and Expressions
u = 'equations-expressions-skill-'
N[u + '01'] = R('evaluate and simplify expressions with square and cube roots',
    'Squaring and taking a square root undo each other for nonnegative numbers, and cubing and taking a cube root undo each other for all numbers; evaluate what is under a root sign before taking the root.',
    [['radicand', 'The expression under a root sign.'], ['inverse operations', 'Operations that undo each other, such as squaring and taking a square root.'], ['radical', 'An expression with a root sign.']],
    'Taking roots term by term (√(9² + 12²) ≠ 9 + 12), or forgetting that √(x²) = |x|.',
    'Roots in expressions', 'Evaluate and simplify.',
    ['5² − ∛216 = 25 − 6 = {{19}}.', '√(9² + 12²) = √225 = {{15}}.', 'A cube has volume 64x⁹: edge = ∛(64x⁹) = {{4x³}}.'])
N[u + '02'] = R('simplify expressions with integer exponents, including monomials with coefficients',
    'Apply the exponent rules to each base separately and multiply or divide the coefficients; a power of a product raises every factor.',
    [['monomial', 'A number, a variable, or a product of numbers and variables.'], ['coefficient', 'The number multiplying the variables.'], ['base', 'The number or variable being raised to a power.']],
    'Writing −6² = 36 (the exponent applies only to 6), or adding like powers as if multiplying (x⁶ + x⁶ ≠ x¹²).',
    'Simplifying monomials', 'Simplify each.',
    ['(3a⁵)(6a⁴) = {{18a⁹}}.', '(3y⁵)³ = 3³y¹⁵ = {{27y¹⁵}}.', '−6² = −(6²) = {{−36}}.'])
N[u + '03'] = R('write linear equations to model situations',
    'Name the unknown, find the starting amount and the rate, and write start + rate × unknown = total; check the equation with a reasonable value.',
    [['variable', 'A letter that stands for an unknown number.'], ['equation', 'A statement that two expressions are equal.'], ['rate', 'An amount per one unit, such as dollars per hour.']],
    'Attaching the variable to the fixed fee instead of the rate, or adding the total to the fee (20h = 62 + 22).',
    'Writing an equation', 'A rental costs $22 plus $20 per hour; the total was $62.',
    ['Let h = number of {{hours}}.', 'Equation: {{22 + 20h = 62}}.', 'Solve: 20h = 40, h = {{2}} hours.'])
N[u + '04'] = R('solve linear equations with variables on both sides',
    'Collect the variable terms on one side and the constants on the other with inverse operations, keeping the equation balanced, then divide by the coefficient and check.',
    [['inverse operation', 'An operation that undoes another.'], ['solution', 'A value that makes the equation true.'], ['like terms', 'Terms with the same variable part.']],
    'Moving a term without changing its sign, or dividing by the wrong number in the last step.',
    'Variables on both sides', 'Solve 9x + 6 = 4x + 56.',
    ['Subtract 4x: {{5x + 6 = 56}}.', 'Subtract 6: 5x = {{50}}.', 'x = {{10}}. Check: 96 = 96.'])
N[u + '05'] = R('solve linear equations that need the distributive property',
    'Distribute to clear parentheses, multiplying every term inside, then combine like terms and solve; with a fraction in front, you can multiply both sides by its reciprocal first.',
    [['distributive property', 'a(b + c) = ab + ac.'], ['simplify', 'Rewrite with fewer terms or no parentheses.'], ['coefficient', 'The number multiplying a variable.']],
    'Multiplying only the first term inside the parentheses: 5(x + 2) → 5x + 2.',
    'Distribute first', 'Solve 6(x + 6) = 66.',
    ['Distribute: {{6x + 36 = 66}}.', 'Subtract 36: 6x = {{30}}.', 'x = {{5}}. (Or divide both sides by 6 first: x + 6 = 11.)'])
N[u + '06'] = R('solve linear equations by combining like terms',
    'Combine like terms on each side first (watch the sign in front of each term), then solve the simpler equation.',
    [['like terms', 'Terms with the same variable raised to the same power.'], ['combine', 'Add or subtract like terms.'], ['consecutive integers', 'Integers that follow each other: n, n + 1, n + 2.']],
    'Losing the sign of a term: 4x + 2 − 5x becomes 9x + 2 instead of −x + 2.',
    'Combine, then solve', 'Solve 3x + 7 + 2x = 57.',
    ['Combine: {{5x + 7 = 57}}.', '5x = {{50}}.', 'x = {{10}}.'])
N[u + '07'] = R('decide whether a linear equation has one solution, no solution or infinitely many solutions',
    'Simplify both sides to ax + b = cx + d. Different x-coefficients give one solution; same coefficients and different constants give no solution; identical sides give infinitely many.',
    [['no solution', 'No value makes the equation true; it simplifies to a false statement such as 0 = 2.'], ['infinitely many solutions', 'Every value works; it simplifies to a true statement such as 0 = 0.'], ['identity', 'An equation true for every value of the variable.']],
    'Reading 0 = 0 as "x = 0", or stopping at "0 = 2" without saying there is no solution.',
    'How many solutions?', 'Classify each.',
    ['6x − 6 = 6x − 8: same x-terms, different constants → {{no solution}}.', '4(x + 3) = 4x + 12 simplifies to 0 = 0 → {{infinitely many}}.', '2x + 8 = 4x + 5: different x-coefficients → {{one solution}}.'])
N[u + '08'] = R('solve equations of the form x² = p and x³ = p',
    'Isolate the square or cube, then take a root: x² = p has two solutions ±√p when p > 0, one when p = 0 and none when p < 0; x³ = p always has exactly one real solution ∛p.',
    [['square root', 'Each positive number has two square roots, √p and −√p.'], ['cube root', 'Each number has exactly one real cube root.'], ['real solution', 'A solution that is a real number.']],
    'Giving only the positive solution of x² = 64, or giving two solutions for x³ = 64.',
    'Squares and cubes', 'Solve each.',
    ['x² + 10 = 110 → x² = 100 → x = {{10 or −10}}.', 'x³ + 4 = 68 → x³ = 64 → x = {{4}}.', 'x² = −25 has {{0}} real solutions.'])

# ======================================================================= Linear and Functional Relationships
u = 'linear-functional-relationships-skill-'
N[u + '01'] = R('decide whether a relation is a function and write function rules',
    'A function assigns exactly one output to each input: in a list of ordered pairs no x-value repeats with a different y-value, and on a graph every vertical line meets the graph at most once.',
    [['function', 'A rule that assigns exactly one output to each input.'], ['input / output', 'The x-value and the y-value it is matched with.'], ['domain and range', 'The set of inputs and the set of outputs.']],
    'Rejecting a relation because two inputs share the same output, which is allowed.',
    'Is it a function?', 'Decide for {(2, 1), (4, −6), (5, 1), (2, 0)}.',
    ['Look for a repeated x: {{2}} is paired with 1 and with 0.', 'So it is {{not}} a function.', 'Rule for x: 0, 1, 2, 3 and y: 1, 4, 7, 10: {{y = 3x + 1}}.'])
N[u + '02'] = R('graph functions from rules and tables, and read values from a graph',
    'Make a table of inputs, compute each output, plot the ordered pairs and connect them; f(a) is the y-value of the graph at x = a.',
    [['function notation', 'f(x) names the output for input x.'], ['ordered pair', '(x, y), an input with its output.'], ['graph of a function', 'All points (x, f(x)).']],
    'Plotting (y, x) instead of (x, y), or reading f(−4) at y = −4.',
    'Table to graph', 'Graph y = −x + 5.',
    ['x = −2, 0, 2 give y = {{7, 5, 3}}.', 'Plot (−2, 7), (0, 5), (2, 3); the points lie on a {{line}}.', 'f(4) = {{1}}.'])
N[u + '03'] = R('distinguish linear functions from nonlinear functions using equations, tables and graphs',
    'A linear function has a constant rate of change: equal steps in x give equal changes in y, its graph is a straight line, and its rule can be written y = mx + b.',
    [['linear function', 'A function with a constant rate of change; y = mx + b.'], ['nonlinear function', 'A function whose rate of change is not constant.'], ['rate of change', 'Change in y divided by change in x.']],
    'Calling a table nonlinear because the x-values are out of order or skip, without comparing Δy/Δx.',
    'Linear or not?', 'Check x: 0, 1, 2, 3 and y: 2, 4, 8, 16.',
    ['Differences in y: {{2, 4, 8}}.', 'They are not constant, so the function is {{nonlinear}}.', 'y = 4x² + 5 is nonlinear because x is {{squared}}.'])
N[u + '04'] = R('find the slope (rate of change) of a line from two points, a table or a graph',
    'Slope = rise ÷ run = (y₂ − y₁) ÷ (x₂ − x₁), using the same order in both differences; a horizontal line has slope 0 and a vertical line has undefined slope.',
    [['slope', 'The constant rate of change of a line, (y₂ − y₁) ÷ (x₂ − x₁).'], ['rise / run', 'Vertical change / horizontal change.'], ['undefined slope', 'The slope of a vertical line (the run is 0).']],
    'Putting the x-difference on top, or subtracting in opposite orders in the numerator and denominator.',
    'Slope from two points', 'Find the slope through (−5, 4) and (1, 0).',
    ['Rise: 0 − 4 = {{−4}}.', 'Run: 1 − (−5) = {{6}}.', 'Slope = −4/6 = {{−2/3}}.'])
N[u + '05'] = R('write the equation of a line from its slope and a point, from two points, or from a context',
    'Find the slope m first, then substitute a point into y = mx + b and solve for b; in context, m is the rate and b is the starting value.',
    [['slope-intercept form', 'y = mx + b.'], ['y-intercept', 'b, the value of y when x = 0.'], ['initial value', 'The starting amount in a context.']],
    'Solving for b with the wrong sign (b = y + mx), or using a point as (y, x).',
    'Two points to an equation', 'Write the line through (−2, 0) and (1, 3).',
    ['m = (3 − 0) ÷ (1 − (−2)) = {{1}}.', '0 = 1(−2) + b, so b = {{2}}.', 'Equation: {{y = x + 2}}.'])
N[u + '06'] = R('graph lines and read slope and intercepts from graphs and equations',
    'From y = mx + b, plot (0, b) and use the slope to step to a second point; from a graph, read the y-intercept and count rise over run between two grid points. Intercepts come from setting x or y to 0.',
    [['x-intercept', 'Where a graph crosses the x-axis (y = 0).'], ['y-intercept', 'Where a graph crosses the y-axis (x = 0).'], ['steeper', 'Having a greater absolute value of slope.']],
    'Swapping the slope and the y-intercept when reading y = 4x + 1.',
    'Reading a graph', 'A line passes through (0, 6) and (1, 7).',
    ['The y-intercept is {{6}}.', 'Rise 1, run 1, so m = {{1}}.', 'Equation: {{y = x + 6}}.'])
N[u + '07'] = R('write rules for linear functions given in tables and find missing values',
    'Find the rate as Δy ÷ Δx (watch for x-steps that are not 1), then use a pair to find the starting value; a missing entry follows the same constant rate.',
    [['table of values', 'Inputs and their outputs listed side by side.'], ['constant rate', 'The same change in y for each change of 1 in x.'], ['starting value', 'The output when x = 0.']],
    'Using the change in y as the slope when x goes up by 2 each time.',
    'Rule from a table', 'x: 0, 2, 4, 6; y: 6, 16, 26, 36.',
    ['Δy ÷ Δx = 10 ÷ 2 = {{5}}.', 'At x = 0, y = {{6}}.', 'Rule: {{y = 5x + 6}}.'])
N[u + '08'] = R('describe where a function is increasing, decreasing or constant and find its maximum and minimum',
    'Read a graph from left to right: it is increasing where it rises, decreasing where it falls and constant where it is flat; the maximum and minimum are the highest and lowest y-values.',
    [['increasing', 'y gets larger as x gets larger.'], ['decreasing', 'y gets smaller as x gets larger.'], ['maximum / minimum', 'The greatest / least output.']],
    'Giving an interval of y-values instead of x-values, or the x-value instead of the maximum value.',
    'Reading behaviour', 'A graph goes from (1, 0) up to (6, 5), then down to (9, 2).',
    ['Increasing from x = 1 to x = {{6}}.', 'Decreasing from x = 6 to x = {{9}}.', 'Maximum value: {{5}}.'])
N[u + '09'] = R('compare and interpret rates of change of functions given in different forms',
    'Turn every representation into a rate (unit rate, slope) with the same units, then compare; the rate tells how much the output changes for each one-unit increase in the input.',
    [['unit rate', 'A rate per one unit, such as pages per hour.'], ['representation', 'A way of showing a function: equation, table, graph or words.'], ['compare', 'Decide which rate is greater and by how much.']],
    'Comparing totals or starting values instead of rates.',
    'Who is faster?', 'Ava: p = 20h + 6. Hiro: 13, 26, 39 pages after 1, 2, 3 hours.',
    ['Ava reads {{20}} pages per hour.', 'Hiro reads (26 − 13) ÷ 1 = {{13}} pages per hour.', '{{Ava}} is faster by 7 pages per hour.'])
N[u + '10'] = R('interpret graphs of functions in context, including distance–time graphs',
    'Each part of a graph tells a story: a rising piece is increasing, a flat piece is no change, a steeper piece is a faster rate; label what x and y mean before reading values.',
    [['qualitative graph', 'A graph that shows the shape of a relationship without exact values.'], ['interval', 'A stretch of x-values.'], ['rate', 'How fast the output changes.']],
    'Reading a distance–time graph as a map, or calling a flat piece "stopped" on a speed–time graph.',
    'Telling the story', 'A hiker\'s distance from camp rises to 20 km at t = 2, stays flat until t = 5, then falls to 0 at t = 9.',
    ['Greatest distance: {{20 km}}.', 'Stopped for 5 − 2 = {{3}} hours.', 'Returning speed: 20 ÷ 4 = {{5}} km per hour.'])
N[u + '11'] = R('sketch and read graphs of functions made of line segments from a description',
    'Break the story into time intervals; each interval with its own constant rate becomes one segment, a rate of 0 is horizontal, and the end of one segment starts the next.',
    [['piecewise function', 'A function made of different pieces on different intervals.'], ['segment', 'A straight piece of the graph.'], ['endpoint', 'Where a segment starts or stops.']],
    'Starting a new segment back at 0 instead of where the last one ended.',
    'Sketching from a story', 'A tank fills at 3 L/min for 4 min, then stops for 4 min.',
    ['Segment 1 rises from (0, 0) to (4, {{12}}).', 'Segment 2 is {{horizontal}} from (4, 12) to (8, 12).', 'So the graph has {{2}} segments.'])
N[u + '12'] = R('graph proportional relationships, find the unit rate as the slope, and compare proportional relationships',
    'A proportional relationship y = kx is a line through the origin; the unit rate k is its slope and the y-value at x = 1. Compare two relationships by their unit rates, whatever form they are given in.',
    [['proportional relationship', 'A relationship y = kx; y ÷ x is the same for every pair.'], ['constant of proportionality', 'k, the unit rate.'], ['origin', 'The point (0, 0).']],
    'Treating a line with a starting fee (y = 2x + 5) as proportional, or reading the unit rate as x ÷ y.',
    'Unit rate on a graph', 'A line through (0, 0) and (4, 50) shows miles y in x hours.',
    ['Unit rate = 50 ÷ 4 = {{12.5}} miles per hour.', 'Equation: {{y = 12.5x}}.', 'The point (1, {{12.5}}) shows the unit rate.'])

# ======================================================================= Systems of Linear Equations
u = 'systems-linear-equations-skill-'
N[u + '01'] = R('graph linear equations in slope-intercept form, rewriting other forms first',
    'Solve for y to get y = mx + b, plot the y-intercept (0, b), then use rise over run to plot more points and draw the line.',
    [['slope-intercept form', 'y = mx + b.'], ['standard form', 'Ax + By = C.'], ['y-intercept', 'The point (0, b).']],
    'Plotting the slope as the y-intercept, or forgetting to divide every term when solving for y.',
    'Graphing from y = mx + b', 'Graph 4x − 4y = −12.',
    ['Solve for y: −4y = −4x − 12, so {{y = x + 3}}.', 'Plot (0, {{3}}).', 'Slope 1: up 1, right 1 to {{(1, 4)}}.'])
N[u + '02'] = R('solve systems of linear equations by graphing and check the solution',
    'The solution of a system is the point that lies on both lines: graph both, read the intersection, and check it in both equations. Parallel lines mean no solution; the same line means infinitely many.',
    [['system of equations', 'Two or more equations with the same variables.'], ['solution of a system', 'An ordered pair that makes every equation true.'], ['intersection', 'The point where graphs cross.']],
    'Reading a y-intercept as the solution, or not checking a point that only looks like the crossing.',
    'Solving by graphing', 'Solve y = x + 5 and y = −2x − 4.',
    ['The lines cross at {{(−3, 2)}}.', 'Check: 2 = −3 + 5 ✓ and 2 = −2(−3) − 4 ✓.', 'So the solution is {{(−3, 2)}}.'])
N[u + '03'] = R('solve systems by substitution',
    'Solve one equation for a variable (or use one already solved), substitute that expression into the other equation, solve, then substitute back for the second variable.',
    [['substitution', 'Replacing a variable with an equal expression.'], ['ordered pair', 'The solution (x, y).'], ['isolate', 'Get a variable alone on one side.']],
    'Forgetting the parentheses when substituting, so only the first term is multiplied.',
    'Substitution', 'Solve y = −4x + 6 and −4x − 3y = 6.',
    ['Substitute: −4x − 3({{−4x + 6}}) = 6.', '−4x + 12x − 18 = 6, so 8x = 24 and x = {{3}}.', 'y = −4(3) + 6 = {{−6}}; solution (3, −6).'])
N[u + '04'] = R('solve systems by elimination',
    'Add or subtract the equations so one variable cancels, multiplying an equation first if needed; solve for the remaining variable, then substitute back.',
    [['elimination', 'Adding or subtracting equations to cancel a variable.'], ['opposite coefficients', 'Coefficients like 2y and −2y that add to 0.'], ['multiply through', 'Multiply every term of an equation by the same number.']],
    'Adding the variable terms but subtracting the constants (or the reverse).',
    'Elimination', 'Solve 3x + y = −5 and 5x − y = 5.',
    ['Add: 8x = {{0}}.', 'x = {{0}}.', '3(0) + y = −5, so y = {{−5}}; solution (0, −5).'])
N[u + '05'] = R('decide by inspection whether a system has one solution, no solution or infinitely many solutions',
    'Write both equations in slope-intercept form: different slopes give one solution; same slope and different intercepts give no solution (parallel lines); the same line gives infinitely many.',
    [['parallel lines', 'Lines with the same slope and different intercepts; they never meet.'], ['coincident lines', 'Two equations for the same line.'], ['inspection', 'Deciding by looking at slopes and intercepts, without solving.']],
    'Calling equations that look different (y = 4x + 1 and −8x + 2y = 2) different lines without rewriting them.',
    'By inspection', 'Classify each system.',
    ['y = 4x + 5 and y = 5 + 4x: same line → {{infinitely many}}.', 'y = 2x − 2 and y = 2x + 3: same slope, different intercepts → {{no solution}}.', 'y = 3x and y = −x + 4: different slopes → {{one solution}}.'])
N[u + '06'] = R('write and solve systems of linear equations to model real-world problems',
    'Define two variables, write one equation for the count and one for the value (or the two plans), solve, and answer in the words and units of the problem.',
    [['define variables', 'Say what each letter stands for, with units.'], ['constraint', 'A condition an answer must satisfy.'], ['reasonable', 'Makes sense in the situation (for example, whole numbers of tickets).']],
    'Mixing up the count equation and the value equation (x + y = 117 and 4x + y = 45).',
    'Two equations from a story', '26 books sold for $260; hardcovers cost $12 and paperbacks $8.',
    ['Count: {{h + p = 26}}. Value: {{12h + 8p = 260}}.', 'Substitute p = 26 − h: 12h + 208 − 8h = 260, so h = {{13}}.', 'So 13 hardcovers and {{13}} paperbacks.'])

# ======================================================================= Patterns and Bivariate Data
u = 'patterns-bivariate-data-skill-'
N[u + '01'] = R('construct scatter plots from two-variable data',
    'Pair the two lists in order (the first value of each list is one point), put the explanatory variable on the x-axis, choose scales that fit all the data, and plot each pair as a dot.',
    [['bivariate data', 'Data with two variables measured for each individual.'], ['scatter plot', 'A graph of bivariate data as points.'], ['scale', 'The spacing of values along an axis.']],
    'Pairing values by size instead of by position, or putting the variables on the wrong axes.',
    'Building a scatter plot', 'Hours studied: 0, 3, 7; test score: 50, 63, 76.',
    ['The points are (0, 50), (3, {{63}}) and (7, {{76}}).', 'Hours go on the {{x}}-axis.', 'A y-axis from 40 to 80 by {{10}}s fits the scores.'])
N[u + '02'] = R('describe patterns in scatter plots, including clusters and outliers, and make informal predictions',
    'Describe the overall pattern (direction, form, strength), then anything unusual: a cluster is a group of points close together and an outlier is far from the pattern. A trend is not proof of cause.',
    [['cluster', 'A group of points close together.'], ['outlier', 'A point far from the overall pattern.'], ['trend', 'The general direction of the data.']],
    'Concluding that one variable causes the other because they are associated.',
    'Describing a scatter plot', 'More ice cream sales go with more sunburns.',
    ['The association is {{positive}}.', 'A third variable, {{hot weather}}, can explain both.', 'So the data do {{not}} show that ice cream causes sunburn.'])
N[u + '03'] = R('classify associations as positive, negative or none, and linear or nonlinear',
    'Positive: y tends to increase as x increases; negative: y tends to decrease; none: no clear pattern. Linear when the points follow a straight line, nonlinear when they follow a curve.',
    [['positive association', 'As x increases, y tends to increase.'], ['negative association', 'As x increases, y tends to decrease.'], ['linear association', 'The points cluster around a line.']],
    'Calling a curved pattern linear because it is increasing.',
    'Classifying an association', 'Age of car vs value: points fall steadily from left to right.',
    ['Direction: {{negative}}.', 'Form: the points follow a {{line}}, so it is linear.', 'Shoe size vs spelling score with no pattern: {{no association}}.'])
N[u + '04'] = R('fit a line to data, write its equation and use it to predict and interpret slope and intercept',
    'A line of fit follows the trend with about as many points above as below; its slope is the predicted change in y per unit of x and its y-intercept is the predicted y when x = 0.',
    [['line of best fit', 'A line that models the trend in a scatter plot.'], ['prediction', 'A value estimated from the model.'], ['interpret', 'Explain in the words of the situation.']],
    'Interpreting the slope as a total instead of a change per one unit of x.',
    'Using a line of fit', 'Test score y = 11x + 44 for x hours studied.',
    ['Predict at x = 3: 33 + 44 = {{77}}.', 'Slope: the score rises about {{11}} points per hour.', 'y-intercept: a predicted score of {{44}} with 0 hours.'])
N[u + '05'] = R('construct two-way tables from categorical data and find row and column totals',
    'Put one variable\'s categories in the rows and the other\'s in the columns; each cell is a count, rows add across, columns add down, and both lead to the same grand total.',
    [['categorical data', 'Data in groups, such as yes/no or grade level.'], ['two-way table', 'A table of counts for two categorical variables.'], ['marginal total', 'A row or column total.']],
    'Adding a row and a column total together, or putting the same count in two cells.',
    'Building a two-way table', 'Grade 7: 12 play a sport, 8 do not. Grade 8: 18 play, 10 do not.',
    ['Grade 7 row total: {{20}}.', '"Play a sport" column total: {{30}}.', 'Grand total: 20 + 28 = {{48}}.'])
N[u + '06'] = R('interpret two-way tables with relative frequencies and decide whether variables are associated',
    'Divide a cell by its row (or column) total to get a relative frequency; if the relative frequencies differ a lot between rows, the variables are associated.',
    [['relative frequency', 'A count divided by a total, as a fraction or percent.'], ['row relative frequency', 'A cell divided by its row total.'], ['association', 'A connection between two variables.']],
    'Dividing by the grand total when the question is about one row.',
    'Relative frequency', 'Juniors: 11 have a job, 7 do not. Seniors: 6 have a job, 8 do not.',
    ['Juniors with a job: 11 ÷ 18 ≈ {{61%}}.', 'Seniors with a job: 6 ÷ 14 ≈ {{43%}}.', 'The percents differ, so grade and having a job {{are}} associated.'])

# ======================================================================= Congruence and Similarity
u = 'congruence-similarity-skill-'
N[u + '01'] = R('identify translations, reflections, rotations and dilations from coordinates or graphs',
    'Compare a vertex with its image: a slide is a translation, a mirror flip a reflection, a turn about a point a rotation, and a change of size from a center a dilation. The first three keep size and shape; a dilation keeps only shape.',
    [['transformation', 'A rule that moves or changes a figure.'], ['image', 'The figure after a transformation, labeled with primes (A′).'], ['rigid motion', 'A translation, reflection or rotation; it preserves lengths and angles.']],
    'Calling a reflection over the y-axis a reflection over the x-axis because "the triangle flipped".',
    'Naming the transformation', 'A(4, 5) → A′(−4, 5), B(6, 6) → B′(−6, 6).',
    ['x changes sign and y stays the same.', 'That is a reflection over the {{y-axis}}.', 'The image is {{congruent}} to the original.'])
N[u + '02'] = R('rotate figures 90°, 180° and 270° about the origin and use the properties of rotations',
    'About the origin: 90° counterclockwise sends (x, y) to (−y, x), 180° sends it to (−x, −y), and 90° clockwise sends it to (y, −x). Rotations preserve lengths, angles and orientation.',
    [['rotation', 'A turn about a fixed point.'], ['center of rotation', 'The fixed point.'], ['counterclockwise', 'Opposite to the way clock hands turn; the positive direction.']],
    'Mixing up the clockwise and counterclockwise rules, or changing only one sign for 90°.',
    'Rotation rules', 'Rotate P(7, 2) about the origin.',
    ['90° counterclockwise: {{(−2, 7)}}.', '180°: {{(−7, −2)}}.', '90° clockwise: {{(2, −7)}}.'])
N[u + '03'] = R('reflect figures over the axes and other lines and use the properties of reflections',
    'Over the x-axis (x, y) → (x, −y); over the y-axis (x, y) → (−x, y); over y = x the coordinates swap. The line of reflection is the perpendicular bisector of each segment PP′, and reflections reverse orientation.',
    [['reflection', 'A flip over a line.'], ['line of reflection', 'The mirror line.'], ['orientation', 'The clockwise or counterclockwise order of the vertices.']],
    'Changing the sign of the wrong coordinate.',
    'Reflection rules', 'Reflect P(−4, 3).',
    ['Over the x-axis: {{(−4, −3)}}.', 'Over the y-axis: {{(4, 3)}}.', 'Over y = x: {{(3, −4)}}.'])
N[u + '04'] = R('translate figures with coordinate rules and use the properties of translations',
    'A translation slides every point the same distance in the same direction: (x, y) → (x + a, y + b), with a for left/right and b for up/down. Lengths, angles and orientation stay the same.',
    [['translation', 'A slide of every point by the same amount.'], ['coordinate rule', 'A rule such as (x, y) → (x − 3, y + 2).'], ['congruent', 'Same size and shape.']],
    'Adding the horizontal change to y (or the vertical change to x).',
    'Translation rule', 'Translate P(4, −5) 5 units right and 2 units up.',
    ['Rule: (x, y) → ({{x + 5}}, {{y + 2}}).', 'P′ = {{(9, −3)}}.', 'Two translations combine into one: 4 left then 1 right = {{3 left}}.'])
N[u + '05'] = R('dilate figures by a scale factor about the origin and describe the effect on lengths and angles',
    'A dilation with scale factor k about the origin sends (x, y) to (kx, ky): lengths and perimeters are multiplied by k, areas by k², and angles stay the same. k > 1 enlarges, 0 < k < 1 reduces.',
    [['dilation', 'A transformation that enlarges or reduces a figure from a center.'], ['scale factor', 'The number every length is multiplied by.'], ['similar', 'Same shape, possibly a different size.']],
    'Adding the scale factor to the coordinates, or multiplying the area by k instead of k².',
    'Dilation', 'Dilate P(2, 6) by scale factor 3 about the origin.',
    ['P′ = {{(6, 18)}}.', 'A perimeter of 44 cm with k = 5/2 becomes {{110 cm}}.', 'An angle of 58° stays {{58°}}.'])
N[u + '06'] = R('describe sequences of transformations and decide whether the image is congruent or similar',
    'Apply transformations in order, using each image as the next input; rigid motions only give a congruent image, and any dilation with k ≠ 1 gives a similar one. Order can change the final position.',
    [['sequence of transformations', 'Two or more transformations done one after another.'], ['congruent figures', 'Figures related by rigid motions.'], ['similar figures', 'Figures related by rigid motions and dilations.']],
    'Doing the steps in the wrong order, or calling a figure congruent after a dilation.',
    'Sequences', 'P(3, 6): translate 3 units right, then rotate 180° about the origin.',
    ['After the translation: {{(6, 6)}}.', 'After the rotation: {{(−6, −6)}}.', 'Only rigid motions were used, so the image is {{congruent}}.'])
N[u + '07'] = R('use the triangle angle sum and the exterior angle theorem to find angles',
    'The three angles of a triangle add to 180°, and an exterior angle equals the sum of the two remote interior angles.',
    [['triangle angle sum', 'The interior angles of a triangle add to 180°.'], ['exterior angle', 'An angle formed by one side and the extension of another.'], ['remote interior angles', 'The two interior angles not next to the exterior angle.']],
    'Using 360° for a triangle, or adding the adjacent interior angle to find an exterior angle.',
    'Angle sum', 'Two angles of a triangle measure 53° and 50°.',
    ['Third angle: 180 − 53 − 50 = {{77°}}.', 'The exterior angle at the third vertex: 53 + 50 = {{103°}}.', '(x + 10) + (2x + 16) + 124 = 180 gives x = {{10}}.'])
N[u + '08'] = R('use angle-angle similarity and proportions to find missing sides of similar triangles',
    'Two triangles with two pairs of congruent angles are similar (AA); in similar triangles corresponding sides are proportional, so a scale factor or a proportion gives a missing side.',
    [['AA similarity', 'Two pairs of congruent angles make triangles similar.'], ['corresponding sides', 'Sides in matching positions.'], ['proportion', 'An equation saying two ratios are equal.']],
    'Adding the difference between sides instead of multiplying by the scale factor.',
    'Missing side', 'Triangle ABC ~ triangle DEF with AB = 11, BC = 6 and DE = 33.',
    ['Scale factor: 33 ÷ 11 = {{3}}.', 'EF = 3 × 6 = {{18}}.', 'A 4-ft person casts an 8-ft shadow; a 24-ft shadow belongs to a {{12-ft}} building.'])
N[u + '09'] = R('use the angle pairs formed by parallel lines and a transversal to find angle measures',
    'When parallel lines are cut by a transversal, corresponding, alternate interior and alternate exterior angles are congruent, and same-side interior angles are supplementary.',
    [['transversal', 'A line that crosses two or more lines.'], ['alternate interior angles', 'Angles between the parallel lines on opposite sides of the transversal.'], ['supplementary', 'Adding to 180°.']],
    'Setting same-side interior angles equal instead of supplementary.',
    'Parallel lines', 'm ∥ n; ∠3 = 44°, where ∠3 and ∠5 are same-side interior angles.',
    ['∠5 = 180 − 44 = {{136°}}.', 'The angle alternate interior to ∠3 is {{44°}}.', '(5x − 1) = (2x + 29) for alternate interior angles gives x = {{10}}.'])

# ======================================================================= Geometry Applications
u = 'geometry-applications-skill-'
N[u + '01'] = R('use the Pythagorean theorem and its converse',
    'In a right triangle a² + b² = c², where c is the hypotenuse (the side across from the right angle). Conversely, if the two shorter sides satisfy a² + b² = c², the triangle is a right triangle.',
    [['hypotenuse', 'The longest side, across from the right angle.'], ['legs', 'The two sides that form the right angle.'], ['converse', 'The theorem with the if and then parts switched.']],
    'Adding the squares to find a leg (√(5² + 13²)) instead of subtracting.',
    'Pythagorean theorem', 'Legs 8 and 15; then a leg with hypotenuse 13 and other leg 5.',
    ['c² = 64 + 225 = 289, so c = {{17}}.', 'b² = 169 − 25 = 144, so b = {{12}}.', 'Do 24, 25, 7 form a right triangle? 49 + 576 = 625: {{yes}}.'])
N[u + '02'] = R('apply the Pythagorean theorem to real-world problems in two dimensions',
    'Sketch the situation, find the right angle, label the legs and the hypotenuse, then use a² + b² = c² and answer with units.',
    [['right angle', 'A 90° angle.'], ['diagonal', 'A segment joining opposite corners.'], ['sketch', 'A quick labeled drawing.']],
    'Adding the side lengths ("walk along both sides") instead of using the theorem.',
    'Ladders and diagonals', 'A 10-ft ladder has its base 8 ft from a wall.',
    ['The ladder is the {{hypotenuse}}.', 'h² + 8² = 10², so h² = {{36}}.', 'The ladder reaches {{6 ft}} up the wall.'])
N[u + '03'] = R('apply the Pythagorean theorem in three dimensions',
    'Use the theorem twice: first find a diagonal of a face, then use it as a leg with the third edge to find the space diagonal (d² = l² + w² + h²); slant heights of cones and pyramids come from a right triangle inside the solid.',
    [['space diagonal', 'A segment through the inside of a box joining opposite corners.'], ['slant height', 'The distance from the apex down the side of a cone or pyramid.'], ['face diagonal', 'A diagonal of one face of a box.']],
    'Stopping at the face diagonal, which is not the longest segment in the box.',
    'Space diagonal', 'A box is 1 ft by 4 ft by 8 ft.',
    ['Bottom diagonal² = 1 + 16 = {{17}}.', 'Space diagonal² = 17 + 64 = {{81}}.', 'Space diagonal = {{9 ft}}.'])
N[u + '04'] = R('find the distance between two points on the coordinate plane with the Pythagorean theorem',
    'Draw the right triangle whose legs are the horizontal and vertical distances between the points, then d = √((x₂ − x₁)² + (y₂ − y₁)²).',
    [['distance', 'The length of the segment joining two points.'], ['horizontal / vertical change', 'The differences in x and in y.'], ['exact value', 'An answer left as a simplified radical instead of a decimal.']],
    'Adding the horizontal and vertical distances (6 + 8 = 14) instead of using the theorem.',
    'Distance', 'Find the distance between (−5, −1) and (1, 7).',
    ['Horizontal leg: {{6}}. Vertical leg: {{8}}.', 'd² = 36 + 64 = {{100}}.', 'd = {{10}} units.'])
N[u + '05'] = R('find volumes of cylinders, cones and spheres',
    'Cylinder V = πr²h; cone V = (1/3)πr²h, one third of the cylinder with the same base and height; sphere V = (4/3)πr³. Use the radius, not the diameter, and give cubic units.',
    [['radius', 'Half the diameter.'], ['volume', 'The amount of space inside a solid, in cubic units.'], ['in terms of π', 'An exact answer such as 192π.']],
    'Using the diameter as the radius, or forgetting the 1/3 for a cone.',
    'Volume formulas', 'Radius 6, height 5.',
    ['Cylinder: π(6²)(5) = {{180π}}.', 'Cone: (1/3)π(6²)(5) = {{60π}}.', 'Sphere of radius 6: (4/3)π(216) = {{288π}}.'])
N[u + '06'] = R('solve for a missing dimension of a cylinder, cone or sphere from its volume',
    'Substitute the volume and the known dimension into the formula, simplify the numbers, then undo the operations: divide for h, take a square root for r in a cylinder or cone, a cube root for r in a sphere.',
    [['missing dimension', 'An unknown radius or height.'], ['solve for', 'Isolate the unknown variable.'], ['cube root', 'Undoes cubing; used to find a sphere\'s radius.']],
    'Forgetting to square the radius (dividing by 6 instead of 36), or forgetting the 1/3 in a cone.',
    'Working backward', 'A cone has volume 72π cubic in. and radius 6 in.',
    ['72π = (1/3)π(36)h = {{12π}}h.', 'h = 72 ÷ 12 = {{6 in.}}', 'A sphere with volume 36π: r³ = 27, r = {{3}}.'])
N[u + '07'] = R('find volumes of composite solids',
    'Split the solid into cylinders, cones, spheres and hemispheres, find each volume with its own height and radius, then add (or subtract for a hollowed-out part).',
    [['composite solid', 'A solid made of simpler solids.'], ['hemisphere', 'Half of a sphere: (2/3)πr³.'], ['decompose', 'Break into simpler parts.']],
    'Using the total height for every part, which treats a cone like a cylinder.',
    'Adding the parts', 'A cylinder (r = 4, h = 4) with a cone (same r, h = 3) on top.',
    ['Cylinder: π(16)(4) = {{64π}}.', 'Cone: (1/3)π(16)(3) = {{16π}}.', 'Total: {{80π}} cubic units.'])


if __name__ == '__main__':
    out = ['/* Teaching notes for the 8th Grade Math lesson planner (see notes-teach.js for the format).',
           '   Generated by tools/grade8-audit-20261119/notes.py (8th Grade Math audit #1, 2026-11-19); edit that file, then rerun.',
           '   Records are keyed by catalog skill id: obj (objective), idea (key idea), voc (vocabulary with meanings),',
           '   watch (common mistake) and cards (the explanation cards). */',
           '(function (G) {', "  'use strict';", '  var T = (G.MKPLAN_TEACH = G.MKPLAN_TEACH || {}), N = T.prealgebra = T.prealgebra || {};']
    order = ['real-numbers-exponents', 'equations-expressions', 'linear-functional-relationships', 'systems-linear-equations',
             'patterns-bivariate-data', 'congruence-similarity', 'geometry-applications']
    unit = None
    for k in sorted(N, key=lambda s: (order.index(s.rsplit('-skill-', 1)[0]), s)):
        un = k.rsplit('-skill-', 1)[0]
        if un != unit:
            out.append(f'  /* ---------- {un} ---------- */'); unit = un
        out.append(f'  N[{json.dumps(k)}] = {json.dumps(N[k], ensure_ascii=False)};')
    out.append("})(typeof window !== 'undefined' ? window : globalThis);")
    open(os.path.join(ROOT, 'worksheet-generator/planner/notes-teach-prealgebra.js'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(len(N), 'records')
