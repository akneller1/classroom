import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import rec, card

K, L, M = 'right-triangles-algebra', 'data-analysis-probability', 'nonlinear-functions-polynomials'
R = {}

# ---------- Right Triangles in Algebra ----------
R[K, 1] = rec('find square roots, estimate irrational square roots and solve ⟨x^2 = p⟩',
  'A square root undoes squaring. ⟨x^2 = p⟩ has two solutions, ⟨\\pm\\sqrt{p}⟩. The square root of a non-perfect square is irrational and lies between two whole numbers.',
  [('square root', 'A number that, multiplied by itself, gives the original number.'), ('principal square root', 'The nonnegative square root, written ⟨\\sqrt{p}⟩.')],
  'Giving only the positive solution of ⟨x^2 = 36⟩.',
  'The square root of ___ is ___ because ___ squared is ___.',
  card('Roots and estimates', 'Undo the square.',
       '⟨\\sqrt{81} = {{9}}⟩', '⟨x^2 = 36⟩ → ⟨x = {{\\pm 6}}⟩', '⟨\\sqrt{30}⟩ is between 5 and {{6}}, closer to {{5}}.'))
R[K, 2] = rec('use the Pythagorean theorem and its converse to find lengths and test for right triangles',
  'In a right triangle, ⟨a^2 + b^2 = c^2⟩, where c is the hypotenuse (opposite the right angle). If the side lengths satisfy it, the triangle is a right triangle.',
  [('hypotenuse', 'The side opposite the right angle; the longest side.'), ('legs', 'The two sides that form the right angle.'), ('converse', 'If ⟨a^2 + b^2 = c^2⟩, the triangle is a right triangle.')],
  'Adding the hypotenuse squared to a leg squared when finding a missing leg.',
  'The hypotenuse is ___, so ___² + ___² = ___².',
  card('a² + b² = c²', 'Find the missing side.',
       'Legs 6 and 8: ⟨c = \\sqrt{100} = {{10}}⟩', 'Leg 5, hypotenuse 13: ⟨b = \\sqrt{169 - 25} = {{12}}⟩', '7, 8, 11: ⟨49 + 64 = 113 \\ne 121⟩, {{not}} a right triangle'))
R[K, 3] = rec('find the distance between two points and the midpoint of a segment',
  'The distance between two points is the hypotenuse of a right triangle with legs |x₂ − x₁| and |y₂ − y₁|. The midpoint averages the coordinates.',
  [('distance formula', '⟨d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}⟩.'), ('midpoint', 'The point halfway between two endpoints: the average of the x’s and of the y’s.')],
  'Subtracting x from y, or forgetting to take the square root.',
  'The legs are ___ and ___, so the distance is ___.',
  card('Draw the right triangle', 'From (1, 2) to (7, 10).',
       'Legs: 6 and {{8}}', '⟨d = \\sqrt{36 + 64} = {{10}}⟩', 'Midpoint: ({{4}}, {{6}})'))
R[K, 4] = rec('write and solve a proportion for a real situation',
  'Set up two equal ratios with matching units in matching positions, then solve. Label the units to check the setup.',
  [('proportion', 'An equation stating that two ratios are equal.'), ('unit rate', 'A rate for one unit of the second quantity.')],
  'Mixing the order of the quantities in the two ratios.',
  'Both ratios compare ___ to ___, so I write ___.',
  card('Match the units', 'A 6-ft person casts a 4-ft shadow; a tree casts a 30-ft shadow.',
       '⟨\\frac{6}{4} = \\frac{h}{30}⟩', '⟨4h = {{180}}⟩', '⟨h = {{45}}⟩ ft'))
R[K, 5] = rec('use the side ratios of 45°-45°-90° and 30°-60°-90° triangles',
  'In a 45°-45°-90° triangle the hypotenuse is ⟨\\sqrt{2}⟩ times a leg. In a 30°-60°-90° triangle the hypotenuse is twice the short leg and the long leg is ⟨\\sqrt{3}⟩ times the short leg.',
  [('45°-45°-90° triangle', 'An isosceles right triangle; sides in the ratio 1 : 1 : ⟨\\sqrt{2}⟩.'), ('30°-60°-90° triangle', 'Half of an equilateral triangle; sides in the ratio 1 : ⟨\\sqrt{3}⟩ : 2.')],
  'Putting ⟨\\sqrt{3}⟩ on the hypotenuse instead of the long leg.',
  'The short leg is ___, so the hypotenuse is ___ and the long leg is ___.',
  card('Special ratios', 'Use the patterns.',
       '45°-45°-90°, leg 5: hypotenuse ⟨{{5\\sqrt{2}}}⟩', '30°-60°-90°, short leg 4: hypotenuse {{8}}', 'Long leg: ⟨{{4\\sqrt{3}}}⟩'))
R[K, 6] = rec('find sine, cosine and tangent ratios and use them to find side lengths',
  'For an acute angle of a right triangle: sin = opposite ÷ hypotenuse, cos = adjacent ÷ hypotenuse, tan = opposite ÷ adjacent (SOH-CAH-TOA).',
  [('sine', 'opposite ÷ hypotenuse.'), ('cosine', 'adjacent ÷ hypotenuse.'), ('tangent', 'opposite ÷ adjacent.')],
  'Labeling opposite and adjacent from the wrong angle.',
  'For angle ___, the opposite side is ___ and the adjacent side is ___.',
  card('SOH-CAH-TOA', 'Right triangle with legs 3 and 4, hypotenuse 5; angle A opposite the side 3.',
       '⟨\\sin A = {{\\frac{3}{5}}}⟩', '⟨\\tan A = {{\\frac{3}{4}}}⟩', '⟨x = 10\\sin 30° = {{5}}⟩'))
R[K, 7] = rec('solve problems with angles of elevation and depression',
  'An angle of elevation is measured up from the horizontal; an angle of depression is measured down from the horizontal. Draw the right triangle, then use a trig ratio.',
  [('angle of elevation', 'The angle from the horizontal up to the line of sight.'), ('angle of depression', 'The angle from the horizontal down to the line of sight.')],
  'Measuring the angle of depression from the vertical.',
  'The angle is ___ and I know the ___ side, so I use ___.',
  card('Draw the triangle', 'From 40 m away, the angle of elevation to a tower top is 35°.',
       '⟨\\tan 35° = \\frac{h}{40}⟩', '⟨h = 40\\tan 35° \\approx {{28.0}}⟩ m', 'Angles of elevation and depression between two points are {{equal}}.'))

# ---------- Data Analysis and Probability ----------
R[L, 1] = rec('organize data in frequency tables, line plots, histograms and two-way tables',
  'A frequency table counts how often each value or interval occurs; a histogram graphs those counts with touching bars. A two-way table shows counts for two categorical variables, and its row or column relative frequencies show association.',
  [('frequency', 'The number of times a value or interval occurs.'), ('histogram', 'A bar graph of frequencies for equal intervals, with no gaps between bars.'), ('two-way table', 'A table of counts for two categorical variables.')],
  'Using unequal intervals in a histogram, or comparing counts in a two-way table instead of relative frequencies.',
  'Of the ___, ___% are ___, compared with ___% of the ___.',
  card('Two-way table', '50 students: 30 play a sport (18 also play music); 20 do not (6 play music).',
       'Of the athletes, ⟨\\frac{18}{30} = {{60}}\\%⟩ play music.', 'Of the non-athletes, ⟨\\frac{6}{20} = {{30}}\\%⟩ play music.', 'The rates differ, so there is {{an association}}.'))
R[L, 2] = rec('make and read box-and-whisker plots',
  'A box plot shows the five-number summary: minimum, Q1, median, Q3 and maximum. The box holds the middle half of the data, and its length is the interquartile range.',
  [('quartile', 'A value that divides ordered data into quarters.'), ('interquartile range (IQR)', 'Q3 − Q1, the spread of the middle half of the data.'), ('five-number summary', 'Minimum, Q1, median, Q3 and maximum.')],
  'Reading the longer section of the plot as having more data; each section holds about a quarter of the values.',
  'The median is ___ and the IQR is ___, so the middle half of the data is between ___ and ___.',
  card('Five numbers', '3, 5, 7, 8, 10, 12, 15, 18.',
       'Median: ⟨\\frac{8 + 10}{2} = {{9}}⟩', 'Q1 = {{6}}, Q3 = {{13.5}}', 'IQR: {{7.5}}'))
R[L, 3] = rec('make and read stem-and-leaf plots, including back-to-back plots',
  'A stem-and-leaf plot keeps every value: the stem is all but the last digit and the leaf is the last digit. Back-to-back plots compare two data sets on one stem.',
  [('stem', 'The digits of a value except the last one.'), ('leaf', 'The last digit of a value.'), ('key', 'A note showing how to read the plot, such as 4 | 7 = 47.')],
  'Leaving out a stem with no leaves, which hides a gap in the data.',
  'The key shows ___ means ___, so the values are ___.',
  card('Read the plot', 'Stems 2, 3, 4; leaves 2 | 5 8, 3 | 1 1 6, 4 | 0.',
       'Values: 25, 28, 31, 31, 36, {{40}}', 'Mode: {{31}}', 'Median: {{31}}'))
R[L, 4] = rec('count outcomes with lists, tree diagrams and the counting principle, and find probabilities',
  'If one choice has m outcomes and a second has n, together they have m × n outcomes. With equally likely outcomes, probability is favorable ÷ total.',
  [('sample space', 'The set of all possible outcomes.'), ('counting principle', 'If one event has m outcomes and another has n, together there are m · n outcomes.'), ('tree diagram', 'A diagram that branches to show every outcome.')],
  'Adding the numbers of choices instead of multiplying them.',
  'There are ___ × ___ = ___ outcomes, and ___ of them are favorable.',
  card('Multiply the choices', 'Roll a number cube and flip a coin.',
       'Outcomes: ⟨6 \\times 2 = {{12}}⟩', 'P(even and heads) = ⟨\\frac{3}{12} = {{\\frac{1}{4}}}⟩', '3 shirts and 4 pants make {{12}} outfits.'))
R[L, 5] = rec('find probabilities of independent and dependent compound events',
  'For independent events, P(A and B) = P(A) · P(B). If the first event changes the second (drawing without replacement), use the new probability for the second.',
  [('independent events', 'Events where one does not affect the probability of the other.'), ('dependent events', 'Events where the outcome of one changes the probability of the other.'), ('compound event', 'An event made of two or more simple events.')],
  'Using the original totals for the second draw when there is no replacement.',
  'After the first draw there are ___ left, so P(second) = ___.',
  card('With and without replacement', 'A bag has 4 red and 6 blue marbles. Draw two.',
       'With replacement: ⟨\\frac{4}{10} \\cdot \\frac{4}{10} = {{\\frac{4}{25}}}⟩', 'Without: ⟨\\frac{4}{10} \\cdot {{\\frac{3}{9}}}⟩', '⟨= {{\\frac{2}{15}}}⟩'))
R[L, 6] = rec('count permutations and combinations',
  'In a permutation order matters; in a combination it does not. A combination count is the permutation count divided by the number of orders of the chosen items.',
  [('permutation', 'An arrangement in which order matters.'), ('combination', 'A selection in which order does not matter.'), ('factorial', 'n! = n(n − 1)(n − 2)⋯1.')],
  'Using a permutation when choosing a committee, where order does not matter.',
  'Order ___ matter, so I count ___.',
  card('Does order matter?', '8 runners.',
       'Gold, silver, bronze: ⟨8 \\cdot 7 \\cdot 6 = {{336}}⟩', 'Any 3 to advance: ⟨\\frac{336}{3!} = {{56}}⟩', '⟨5! = {{120}}⟩'))
R[L, 7] = rec('find experimental probabilities, compare them with theoretical ones and design simulations',
  'Experimental probability is the fraction of trials in which the event happened. With more trials it tends to get closer to the theoretical probability. A simulation models a chance situation with a tool such as random numbers.',
  [('experimental probability', 'The number of times an event happens ÷ the number of trials.'), ('simulation', 'A model of a chance situation using coins, cubes, spinners or random numbers.'), ('trial', 'One repetition of an experiment.')],
  'Expecting a small number of trials to match the theoretical probability exactly.',
  'The event happened ___ times in ___ trials, so the experimental probability is ___.',
  card('Experiment and simulate', 'A free throw is made 70% of the time.',
       'In 50 trials, 32 makes: ⟨\\frac{32}{50} = {{64}}\\%⟩', 'Simulate with digits 0–9: let 0–6 be a {{make}}.', 'More trials should bring the result closer to {{70%}}.'))
R[L, 8] = rec('choose representative samples and use them to make predictions about a population',
  'A random sample gives every member of the population an equal chance, so it tends to be representative. Use the sample proportion to predict for the population, and expect variation between samples.',
  [('population', 'The whole group you want to know about.'), ('sample', 'Part of the population that is studied.'), ('random sample', 'A sample in which every member has an equal chance of being chosen.'), ('inference', 'A conclusion about a population drawn from a sample.')],
  'Trusting a convenience sample (friends, one class, volunteers) to represent everyone.',
  'The sample is (not) representative because ___. I predict ___.',
  card('Predict from a sample', '60 random students: 21 prefer pizza. The school has 900 students.',
       'Sample rate: ⟨\\frac{21}{60} = {{35}}\\%⟩', 'Prediction: ⟨0.35 \\times 900 = {{315}}⟩', 'Asking only the soccer team would be {{biased}}.'))
R[L, 9] = rec('compare two populations using measures of center and variability',
  'Compare two groups by their centers and spreads. The difference in centers, measured in units of spread (such as the MAD), shows how much the groups overlap.',
  [('mean absolute deviation (MAD)', 'The average distance of the data values from the mean.'), ('overlap', 'How much the values of two data sets share the same range.')],
  'Comparing only the means and ignoring how spread out the data are.',
  'The means differ by ___, which is about ___ MADs, so the overlap is ___.',
  card('Center and spread', 'Team A mean 62 in., MAD 2; Team B mean 68 in., MAD 2.',
       'Difference of means: {{6}} in.', '⟨\\frac{6}{2} = {{3}}⟩ MADs', 'Large difference, so the groups {{overlap little}}.'))

# ---------- Nonlinear Functions and Polynomials ----------
R[M, 1] = rec('identify arithmetic and geometric sequences and write their rules',
  'An arithmetic sequence adds the same number each time (common difference); a geometric sequence multiplies by the same number (common ratio).',
  [('arithmetic sequence', 'A sequence with a common difference between terms.'), ('geometric sequence', 'A sequence with a common ratio between terms.'), ('common ratio', 'The number each term is multiplied by to get the next.')],
  'Calling a sequence arithmetic because it increases, without checking the differences.',
  'Each term is ___ the one before, so the sequence is ___.',
  card('Add or multiply?', 'Check differences and ratios.',
       '5, 9, 13, 17: arithmetic, difference {{4}}', '3, 6, 12, 24: geometric, ratio {{2}}', 'Next term of 3, 6, 12, 24: {{48}}'))
R[M, 2] = rec('graph quadratic and other nonlinear functions from tables and recognize them',
  'A function is linear only if equal steps in x give equal changes in y. Squares and absolute values make U- and V-shaped graphs that are not straight lines.',
  [('nonlinear function', 'A function whose graph is not a straight line.'), ('parabola', 'The U-shaped graph of a quadratic function such as ⟨y = x^2⟩.')],
  'Connecting points with straight segments and calling the graph linear.',
  'The changes in y are ___, so the function is ___.',
  card('Equal steps?', 'Table for ⟨y = x^2 - 1⟩.',
       'x = −2, −1, 0, 1, 2 → y = 3, 0, {{−1}}, 0, 3', 'Changes in y: −3, −1, 1, 3, {{not}} equal', 'The graph is a {{parabola}}.'))
R[M, 3] = rec('model exponential growth and decay',
  'Exponential models multiply by the same factor each period: ⟨y = a \\cdot b^x⟩. Growth has b > 1; decay has 0 < b < 1. A growth rate r gives b = 1 + r.',
  [('exponential growth', 'An increase by the same percent each period; b > 1.'), ('exponential decay', 'A decrease by the same percent each period; 0 < b < 1.'), ('growth factor', 'The number b that the amount is multiplied by each period.')],
  'Adding the rate each period (linear) instead of multiplying by the factor.',
  'The amount is multiplied by ___ each ___, so the model is ___.',
  card('Multiply each period', 'Population 500 grows 10% a year.',
       '⟨y = 500(1.1)^x⟩', 'After 2 years: ⟨500(1.21) = {{605}}⟩', 'A car worth $20,000 loses 15% a year: ⟨y = 20000({{0.85}})^x⟩'))
R[M, 4] = rec('classify polynomials and write them in standard form',
  'A polynomial is a sum of monomials. Standard form lists terms from highest to lowest degree; name it by its degree and its number of terms.',
  [('monomial', 'A number, a variable, or a product of numbers and variables with whole-number exponents.'), ('degree', 'The greatest exponent of the variable in a polynomial.'), ('binomial / trinomial', 'A polynomial with two terms / three terms.')],
  'Finding the degree from the first term written instead of the greatest exponent.',
  'The degree is ___ and there are ___ terms, so it is a ___.',
  card('Standard form', 'Rewrite ⟨4 + 3x^2 - 7x^3⟩.',
       '⟨-7x^3 + 3x^2 + {{4}}⟩', 'Degree: {{3}}', 'Three terms: a cubic {{trinomial}}'))
R[M, 5] = rec('add and subtract polynomials',
  'Add polynomials by combining like terms. To subtract, add the opposite of every term of the second polynomial.',
  [('like terms', 'Terms with the same variables raised to the same powers.'), ('opposite of a polynomial', 'The polynomial with every term’s sign changed.')],
  'Changing the sign of only the first term when subtracting.',
  'I change the sign of every term in ___ and combine ___.',
  card('Combine like terms', 'Subtract ⟨(5x^2 + 2x - 3) - (2x^2 - 4x + 1)⟩.',
       '⟨= 5x^2 + 2x - 3 - 2x^2 + {{4x}} - 1⟩', '⟨= {{3x^2 + 6x - 4}}⟩', 'Add ⟨(x^2 + 1) + (3x^2 - 5) = {{4x^2 - 4}}⟩'))
R[M, 6] = rec('multiply a polynomial by a monomial and factor out a common monomial',
  'Use the distributive property: multiply the monomial by every term, adding exponents of like bases. Factoring reverses this by taking out the GCF.',
  [('monomial', 'A single term such as ⟨3x^2⟩.'), ('greatest common factor', 'The greatest monomial that divides every term.')],
  'Multiplying only the first term, or multiplying the exponents.',
  'I multiply ___ by each term: ___.',
  card('Distribute the monomial', 'Multiply ⟨3x(2x^2 - 5x + 4)⟩.',
       '⟨= 6x^3 - {{15x^2}} + 12x⟩', 'Factor ⟨8x^3 + 12x^2⟩: GCF {{4x^2}}', '⟨= 4x^2(2x + {{3}})⟩'))
R[M, 7] = rec('multiply two binomials',
  'Every term of the first binomial multiplies every term of the second (distribute twice, or FOIL), then combine like terms.',
  [('binomial', 'A polynomial with two terms.'), ('FOIL', 'First, Outer, Inner, Last: the four products when multiplying two binomials.')],
  'Writing ⟨(x + 3)^2 = x^2 + 9⟩ and leaving out the middle term.',
  'The four products are ___, ___, ___ and ___.',
  card('Four products', 'Multiply ⟨(x + 3)(x - 5)⟩.',
       '⟨x^2 - 5x + 3x - 15⟩', '⟨= {{x^2 - 2x - 15}}⟩', '⟨(x + 3)^2 = x^2 + {{6x}} + 9⟩'))
R[M, 8] = rec('choose and combine strategies to solve multi-step problems',
  'Many problems can be solved several ways: a table, an equation, a diagram, working backward. Pick one, then check the answer with a second strategy.',
  [('strategy', 'A plan for solving a problem.'), ('work backward', 'Start from the result and undo each step.')],
  'Stopping at the first answer without checking it against the conditions.',
  'I used ___ and checked with ___.',
  card('Two ways', 'After spending half her money and then $6, Mia has $9. How much did she start with?',
       'Work backward: ⟨9 + 6 = {{15}}⟩, ⟨15 \\times 2 = {{30}}⟩', 'Equation: ⟨\\frac{x}{2} - 6 = 9⟩, ⟨x = {{30}}⟩', 'Both strategies give {{$30}}.'))
