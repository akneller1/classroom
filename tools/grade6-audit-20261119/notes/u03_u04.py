import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import rec, card

C, D = 'rational-numbers', 'expressions-equations'
R = {}

# ---------- Rational Numbers ----------
R[C, 1] = rec('use positive and negative numbers to describe quantities in real situations',
  'Positive and negative numbers describe values on opposite sides of 0: above and below sea level, deposits and withdrawals, gains and losses. 0 is neither positive nor negative.',
  [('negative number', 'A number less than 0.'), ('opposite', 'The number the same distance from 0 on the other side, such as 5 and −5.')],
  'Treating a loss or a depth as a positive number.',
  'The situation shows ___, so I use a ___ number: ___.',
  card('Numbers for situations', '0 is the reference point.',
       '40 feet below sea level: {{−40}}', 'a deposit of $25: {{+25}}', 'the opposite of −7: {{7}}'))
R[C, 2] = rec('place positive and negative numbers, including fractions and decimals, on a number line',
  'Numbers increase to the right. A negative number is the same distance to the left of 0 as its opposite is to the right. The opposite of the opposite is the number itself.',
  [('number line', 'A line with numbers placed in order at equal intervals.'), ('rational number', 'A number that can be written as a fraction of two integers.')],
  'Placing ⟨-2\\frac{1}{2}⟩ between −2 and −1 instead of between −3 and −2.',
  '___ is between ___ and ___ because ___.',
  card('Place the point', '⟨-2\\frac{1}{2}⟩ and its opposite',
       'Between {{−3}} and {{−2}}', 'Opposite: ⟨{{2\\frac{1}{2}}}⟩', '⟨-(-3) = {{3}}⟩'))
R[C, 3] = rec('compare and order rational numbers',
  'On a number line, the number farther right is greater. Among negative numbers, the one closer to 0 is greater.',
  [('greater than', 'Farther right on the number line; symbol >.'), ('less than', 'Farther left on the number line; symbol <.')],
  'Thinking −9 > −2 because 9 > 2.',
  '___ is greater than ___ because it is farther ___.',
  card('Order from least to greatest', '−1.5, 0.75, −3, ⟨-\\frac{1}{2}⟩',
       'Farthest left: {{−3}}', '−3, −1.5, ⟨{{-\\frac{1}{2}}}⟩, 0.75'))
R[C, 4] = rec('write and explain inequality statements about rational numbers in real situations',
  'An inequality such as −3 > −7 tells the order of two numbers. In context it says which value is warmer, higher or larger.',
  [('inequality', 'A statement that compares two values with <, >, ≤ or ≥.'), ('order', 'The position of numbers from least to greatest.')],
  'Reading −3 °C > −7 °C as “−3 is colder”.',
  'Because ___ is to the right of ___, ___ is ___.',
  card('An inequality in context', 'It is −3 °C in Boston and −7 °C in Montreal.',
       '⟨-3 {{>}} -7⟩', '{{Boston}} is warmer'))
R[C, 5] = rec('find and interpret absolute value as distance from 0',
  'The absolute value of a number is its distance from 0, so it is never negative. In context it is a size without a direction, such as a debt of $30 for a balance of −$30.',
  [('absolute value', 'The distance of a number from 0, written |a|.'), ('magnitude', 'The size of a quantity without its sign.')],
  'Writing |−8| = −8.',
  'The distance from ___ to 0 is ___, so the absolute value is ___.',
  card('Distance from 0', '|−8|, |5|, |0|',
       '|−8| = {{8}}', '|5| = {{5}}', '|0| = {{0}}'))
R[C, 6] = rec('use absolute value to compare magnitudes and order numbers',
  'A larger absolute value means a larger size. For negative numbers, a larger absolute value means a smaller number: a balance of −$40 is a bigger debt but less money than −$20.',
  [('debt', 'Money owed; a negative balance.'), ('elevation', 'Height above or below sea level.')],
  'Saying a balance below −30 dollars is a debt of less than 30 dollars.',
  'The balance is ___, which means a debt of more than ___.',
  card('Size vs. order', 'Balances: −$40 and −$20.',
       'Bigger debt: {{−40}} (|−40| = 40)', 'Less money: {{−40}} because −40 < −20'))
R[C, 7] = rec('locate points in all four quadrants and describe reflections across the axes',
  'The first coordinate tells how far left or right, the second how far up or down. Reflecting across the x-axis changes the sign of y; across the y-axis, the sign of x.',
  [('quadrant', 'One of the four regions the axes divide the coordinate plane into.'), ('reflection', 'A flip across a line that makes a mirror image.')],
  'Changing the wrong coordinate when reflecting across the x-axis.',
  'The point is ___ units ___ and ___ units ___, so it is in Quadrant ___.',
  card('Signs and reflections', 'Point (−4, 3)',
       'Quadrant {{II}}', 'Across the x-axis: (−4, {{−3}})', 'Across the y-axis: ({{4}}, 3)'))
R[C, 8] = rec('plot and name ordered pairs, including points on the axes',
  'An ordered pair (x, y) starts at the origin. A point with x = 0 is on the y-axis; a point with y = 0 is on the x-axis.',
  [('ordered pair', 'A pair of numbers (x, y) that names a point.'), ('origin', 'The point (0, 0), where the axes meet.')],
  'Plotting (2, 5) at 2 up and 5 across.',
  'I moved ___ across and ___ up or down.',
  card('Plot the pair', '(−2, 5), (0, −4), (3, 0)',
       '(−2, 5): left {{2}}, up {{5}}', '(0, −4) is on the {{y}}-axis', '(3, 0) is on the {{x}}-axis'))
R[C, 9] = rec('find distances between points with the same first or second coordinate',
  'If two points share an x- or y-coordinate, the distance is the difference of the other coordinates. If they are on opposite sides of an axis, add the absolute values.',
  [('distance', 'How far apart two points are; never negative.'), ('vertical', 'Up and down; points on a vertical line have the same x-coordinate.')],
  'Subtracting −3 from 4 as 4 − 3 = 1 instead of 4 + 3 = 7.',
  'The points share ___, so the distance is |___| + |___| = ___.',
  card('Across an axis', '(5, 4) and (5, −3)',
       'Same {{x}}-coordinate', '⟨|4| + |-3| = {{7}}⟩ units'))

# ---------- Expressions and Equations ----------
R[D, 1] = rec('write and evaluate numerical expressions with whole-number exponents',
  'An exponent tells how many times the base is used as a factor: ⟨2^5 = 2 \\cdot 2 \\cdot 2 \\cdot 2 \\cdot 2 = 32⟩.',
  [('exponent', 'The small raised number that tells how many times the base is a factor.'), ('base', 'The number being multiplied repeatedly.')],
  'Multiplying the base by the exponent: ⟨2^5⟩ is not 10.',
  'The base ___ is used as a factor ___ times, so the value is ___.',
  card('Exponents', '⟨3^4⟩ and ⟨\\left(\\frac{1}{2}\\right)^3⟩',
       '⟨3 \\cdot 3 \\cdot 3 \\cdot 3 = {{81}}⟩', '⟨\\frac{1}{2} \\cdot \\frac{1}{2} \\cdot \\frac{1}{2} = {{\\frac{1}{8}}}⟩'))
R[D, 2] = rec('write expressions with variables from words and contexts, name their parts, and evaluate them',
  'A variable stands for a number. Terms are separated by + and −; a coefficient multiplies a variable. To evaluate, substitute each value in parentheses.',
  [('term', 'A part of an expression separated by + or −.'), ('coefficient', 'The number multiplying a variable in a term.'), ('variable', 'A letter that stands for a number.')],
  'Writing “5 less than n” as 5 − n.',
  'The expression has ___ terms, and the coefficient of ___ is ___.',
  card('Write, name, evaluate', 'A pizza costs $11 plus $2 for each topping, t.',
       'Expression: ⟨11 + {{2t}}⟩', 'Terms: {{2}}; coefficient of t: {{2}}', '⟨t = 3: 11 + 2(3) = {{17}}⟩'))
R[D, 3] = rec('use the order of operations, including exponents and grouping symbols',
  'Grouping symbols first, then exponents, then multiply and divide left to right, then add and subtract left to right.',
  [('order of operations', 'The agreed order for evaluating an expression.'), ('grouping symbols', 'Parentheses, brackets and fraction bars.')],
  'Multiplying before dividing even when the division comes first.',
  'First I ___ because ___.',
  card('Step by step', '⟨2 + 3^2 \\times (8 - 6)⟩',
       '⟨= 2 + 3^2 \\times {{2}}⟩', '⟨= 2 + {{9}} \\times 2⟩', '⟨= 2 + 18 = {{20}}⟩'))
R[D, 4] = rec('generate equivalent expressions with the distributive property and by combining like terms',
  'Equivalent expressions have the same value for every value of the variable. ⟨3(x + 4) = 3x + 12⟩, and ⟨7k + 6k = 13k⟩.',
  [('equivalent expressions', 'Expressions that are equal for every value of the variable.'), ('like terms', 'Terms with the same variable part.')],
  'Multiplying only the first term: ⟨3(x + 4) \\ne 3x + 4⟩.',
  'I distributed ___ to each term and combined ___.',
  card('Distribute and combine', '⟨2(n - 3) + 5n⟩',
       '⟨= 2n - {{6}} + 5n⟩', '⟨= {{7n - 6}}⟩'))
R[D, 5] = rec('decide whether a number is a solution of an equation or inequality by substitution',
  'A solution makes the equation or inequality true. Substitute the number and check.',
  [('solution', 'A value of the variable that makes the statement true.'), ('substitute', 'Replace the variable with a number.')],
  'Substituting into only one side.',
  'When ___ = ___, the left side is ___, so it ___ a solution.',
  card('Is it a solution?', '⟨3x + 2 = 17⟩, x = 5?',
       '⟨3(5) + 2 = {{17}}⟩', '17 = 17, so 5 {{is}} a solution'))
R[D, 6] = rec('write and solve one-step equations of the form x + p = q and px = q',
  'Undo the operation with its inverse on both sides: subtract to undo adding, divide to undo multiplying.',
  [('inverse operation', 'An operation that undoes another, such as subtraction for addition.'), ('equation', 'A statement that two expressions are equal.')],
  'Doing the inverse on only one side.',
  'To undo ___, I ___ both sides by ___.',
  card('Solve and check', '⟨11n = 605⟩',
       '⟨\\frac{11n}{11} = \\frac{605}{11}⟩', '⟨n = {{55}}⟩', 'Check: ⟨11 \\times 55 = {{605}}⟩'))
R[D, 7] = rec('write an equation for a dependent variable and connect it to a table and a graph',
  'The independent variable changes on its own and goes on the horizontal axis; the dependent variable depends on it. A table, an equation and a graph all show the same relationship.',
  [('independent variable', 'The input that changes freely, graphed on the x-axis.'), ('dependent variable', 'The output whose value depends on the input, graphed on the y-axis.')],
  'Mixing up the variables: the total cost depends on the number of tickets, not the other way round.',
  '___ depends on ___, so ___ is the dependent variable.',
  card('Table, equation, graph', 'Tickets cost $6 each.',
       'Equation: ⟨c = {{6t}}⟩', 't = 2, 4: c = 12, {{24}}', 'Graph: a line through (0, 0) and (4, {{24}})'))
