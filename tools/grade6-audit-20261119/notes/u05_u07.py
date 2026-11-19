import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import rec, card

E, F, G = 'inequalities', 'geometry', 'data-displays'
R = {}

# ---------- Inequalities ----------
R[E, 1] = rec('write inequalities of the form x > c or x < c for real-world limits',
  'An inequality describes many values at once. “At least” means ≥, “at most” means ≤, “more than” means >, “fewer than” means <.',
  [('inequality', 'A statement that compares with <, >, ≤ or ≥.'), ('at least', 'That number or more: ≥.')],
  'Writing “at least 18” as x > 18, which leaves out 18.',
  'The words ___ mean ___, so I write ___.',
  card('Words to symbols', 'You must be at least 48 inches tall to ride.',
       '⟨h {{\\ge}} 48⟩', 'Is 48 allowed? {{yes}}'))
R[E, 2] = rec('solve one-step inequalities (extension: Grade 7 solving)',
  'Solve an inequality like an equation with inverse operations. (Dividing by a negative number reverses the sign; that is a Grade 7 idea.)',
  [('solution set', 'All the values that make an inequality true.'), ('boundary', 'The number where the solutions begin or end.')],
  'Forgetting that the solution is a set of numbers, not a single number.',
  'I ___ both sides by ___, so the solutions are ___.',
  card('Solve', '⟨x + 7 < 12⟩ and ⟨4x \\ge 20⟩',
       '⟨x < {{5}}⟩', '⟨x \\ge {{5}}⟩'))
R[E, 3] = rec('test whether given values are solutions of an inequality',
  'Substitute each value. If the statement is true, the value is a solution. An inequality usually has infinitely many solutions.',
  [('solution', 'A value that makes the inequality true.'), ('substitute', 'Replace the variable with a number.')],
  'Treating the boundary as a solution of a strict inequality.',
  'When x = ___, the statement is ___, so ___.',
  card('Which are solutions of ⟨2x > 6⟩?', 'Test 2, 3 and 4.',
       '⟨2(2) = 4 > 6⟩? {{no}}', '⟨2(3) = 6 > 6⟩? {{no}}', '⟨2(4) = 8 > 6⟩? {{yes}}'))
R[E, 4] = rec('graph the solutions of an inequality on a number line',
  'Put a dot at the boundary: closed if it is included (≤, ≥), open if not (<, >). Shade toward the solutions.',
  [('open circle', 'A dot that shows the boundary is not a solution.'), ('closed circle', 'A filled dot that shows the boundary is a solution.')],
  'Shading the wrong way when the variable is on the right: 3 < x means x > 3.',
  'I used a ___ circle at ___ and shaded to the ___.',
  card('Graph it', '⟨x \\le -2⟩',
       '{{closed}} circle at −2', 'shade to the {{left}}'))
R[E, 5] = rec('write and use inequalities to model real problems with limits',
  'Set up the inequality from the limit (at most, at least), solve it, then answer in context. Whole objects need whole-number answers, so round in the direction that keeps the limit.',
  [('constraint', 'A limit the answer must stay within.'), ('maximum', 'The greatest value allowed.')],
  'Rounding 12.9 hours to 12 when the goal is “at least $200”.',
  'The greatest (least) whole number that works is ___ because ___.',
  card('A van’s limit', 'At most 1,200 lb: a 180-lb driver and 60-lb boxes.',
       '⟨180 + 60b \\le 1{,}200⟩', '⟨60b \\le 1{,}020⟩, ⟨b \\le {{17}}⟩', 'At most {{17}} boxes'))

# ---------- Geometry ----------
R[F, 1] = rec('find the area of parallelograms, rhombuses and trapezoids',
  'Cut and rearrange: a parallelogram becomes a rectangle, so ⟨A = bh⟩. Two copies of a trapezoid make a parallelogram, so ⟨A = \\frac{1}{2}(b_1 + b_2)h⟩.',
  [('base', 'A side chosen as the bottom of a figure.'), ('height', 'The perpendicular distance from the base to the opposite side.')],
  'Using the slanted side as the height.',
  'The base is ___ and the height is ___, so the area is ___.',
  card('Trapezoid', 'Bases 6 and 10, height 4.',
       '⟨A = \\frac{1}{2}(6 + 10)(4)⟩', '⟨= \\frac{1}{2}({{16}})(4) = {{32}}⟩ square units'))
R[F, 2] = rec('find the area of right triangles as half a rectangle',
  'A right triangle is half of a rectangle with the same legs, so ⟨A = \\frac{1}{2}bh⟩.',
  [('right triangle', 'A triangle with one 90° angle.'), ('leg', 'One of the two sides that form the right angle.')],
  'Forgetting the ⟨\\frac{1}{2}⟩.',
  'The triangle is half of a ___ by ___ rectangle, so its area is ___.',
  card('Half a rectangle', 'Legs 8 and 5.',
       'Rectangle: ⟨8 \\times 5 = {{40}}⟩', 'Triangle: ⟨\\frac{40}{2} = {{20}}⟩ square units'))
R[F, 3] = rec('find the area of any triangle using a base and its height',
  'Every triangle is half of a parallelogram, so ⟨A = \\frac{1}{2}bh⟩. The height may fall outside an obtuse triangle.',
  [('altitude', 'The perpendicular segment from a vertex to the line containing the opposite side.'), ('obtuse triangle', 'A triangle with one angle greater than 90°.')],
  'Pairing a base with a height that is not perpendicular to it.',
  'The height ___ is perpendicular to the base ___.',
  card('Any triangle', 'Base 12, height 7.',
       '⟨A = \\frac{1}{2}(12)(7)⟩', '⟨= {{42}}⟩ square units'))
R[F, 4] = rec('find the area of composite polygons by splitting them into rectangles and triangles',
  'Decompose the figure into shapes you know, find each area, and add. Or find a larger rectangle and subtract the missing piece.',
  [('composite figure', 'A figure made of two or more simple shapes.'), ('decompose', 'Break a figure into simpler parts.')],
  'Counting an overlapping region twice.',
  'I split the figure into ___ and ___, then ___ their areas.',
  card('Split and add', 'An L shape: 10 by 4 and 3 by 5.',
       '⟨10 \\times 4 = {{40}}⟩', '⟨3 \\times 5 = {{15}}⟩', 'Total: {{55}} square units'))
R[F, 5] = rec('find the volume of right rectangular prisms with fractional edge lengths',
  'Volume counts unit cubes. Packing with cubes of side ⟨\\frac{1}{2}⟩ unit gives the same result as ⟨V = lwh⟩.',
  [('volume', 'The number of unit cubes that fill a solid.'), ('cubic unit', 'A cube with edges 1 unit long.')],
  'Adding the edge lengths instead of multiplying.',
  'The prism holds ___ layers of ___ cubes, so the volume is ___.',
  card('Fractional edges', '⟨3\\frac{1}{2} \\times 2 \\times 1\\frac{1}{2}⟩ ft',
       '⟨\\frac{7}{2} \\times 2 = {{7}}⟩', '⟨7 \\times \\frac{3}{2} = {{10\\frac{1}{2}}}⟩ cubic feet'))
R[F, 6] = rec('draw polygons on the coordinate plane and find side lengths from coordinates',
  'Plot the vertices in order and connect them. For a horizontal or vertical side, the length is the difference of the coordinates that change.',
  [('vertex', 'A corner point of a polygon.'), ('polygon', 'A closed figure made of straight sides.')],
  'Subtracting coordinates across an axis without using absolute values.',
  'Side ___ is horizontal, so its length is ___.',
  card('Side lengths', 'A(−3, −2), B(4, −2), C(4, 3)',
       'AB: ⟨|-3| + |4| = {{7}}⟩ units', 'BC: ⟨3 - (-2) = {{5}}⟩ units'))
R[F, 7] = rec('find perimeter and area of polygons drawn on the coordinate plane',
  'Find each side from the coordinates, then add for the perimeter or use an area formula; split irregular shapes.',
  [('perimeter', 'The distance around a figure.'), ('area', 'The number of square units inside a figure.')],
  'Mixing up perimeter (units) and area (square units).',
  'The width is ___ and the height is ___, so the perimeter is ___ and the area is ___.',
  card('Rectangle on the grid', 'A(−4, −3), B(3, −3), C(3, 2), D(−4, 2)',
       'Width {{7}}, height {{5}}', 'Perimeter ⟨2(7 + 5) = {{24}}⟩', 'Area ⟨7 \\times 5 = {{35}}⟩'))
R[F, 8] = rec('use nets to find the surface area of prisms and pyramids',
  'A net unfolds a solid into flat faces. Surface area is the sum of the areas of all faces. A rectangular prism has three pairs of matching faces.',
  [('net', 'A flat pattern that folds into a solid.'), ('surface area', 'The total area of all the faces of a solid.')],
  'Counting only three faces instead of all six.',
  'The net has ___ pairs of faces with areas ___, so the surface area is ___.',
  card('Box 4 by 3 by 2', 'Pairs: 4×3, 4×2, 3×2',
       '⟨12 + 8 + 6 = {{26}}⟩', '⟨2 \\times 26 = {{52}}⟩ square units'))

# ---------- Data Displays ----------
R[G, 1] = rec('recognize statistical questions and describe data by center and spread',
  'A statistical question expects answers that vary. A measure of center summarizes the data with one number; a measure of variation describes how spread out it is.',
  [('statistical question', 'A question answered by collecting data that vary.'), ('variability', 'How much the data values differ from each other.')],
  'Calling “How tall is Ana?” a statistical question.',
  'This question ___ statistical because the answers ___.',
  card('Statistical or not?', '“How many hours do students in my class sleep?”',
       'The answers {{vary}}, so it is {{statistical}}', '“How many hours did I sleep?” is {{not}} statistical'))
R[G, 2] = rec('display numerical data in dot plots, histograms and box plots',
  'A dot plot shows every value; a histogram groups values into equal intervals; a box plot shows the five-number summary.',
  [('histogram', 'A bar graph of counts for equal intervals of numbers.'), ('box plot', 'A display of the minimum, quartiles, median and maximum.')],
  'Leaving gaps or unequal intervals in a histogram.',
  'I chose a ___ because ___.',
  card('Five-number summary', '2, 3, 5, 6, 8, 9, 12',
       'Min 2, Q1 {{3}}, median {{6}}', 'Q3 {{9}}, max 12'))
R[G, 3] = rec('find the mean and median and say which better describes the center',
  'The mean is the total shared equally; the median is the middle value. An outlier pulls the mean toward it but barely moves the median.',
  [('mean', 'The sum of the values divided by the number of values.'), ('median', 'The middle value when the data are in order.')],
  'Finding the median without ordering the data first.',
  'The ___ is a better measure because ___.',
  card('Mean vs. median', '12, 13, 13, 14, 14, 15, 16, 41',
       'Mean ⟨\\frac{138}{8} = {{17.25}}⟩', 'Median ⟨\\frac{14 + 14}{2} = {{14}}⟩', 'The outlier {{41}} pulls the mean up'))
R[G, 4] = rec('find the range and interquartile range',
  'The range is maximum − minimum. The IQR is Q3 − Q1, the spread of the middle half, so it is not affected by outliers.',
  [('range', 'The difference between the greatest and least values.'), ('interquartile range', 'Q3 − Q1, the range of the middle half of the data.')],
  'Including the median in both halves when finding the quartiles of an odd data set.',
  'The middle half of the data spans ___, so the IQR is ___.',
  card('Range and IQR', '2, 3, 5, 6, 8, 9, 12',
       'Range ⟨12 - 2 = {{10}}⟩', 'IQR ⟨9 - 3 = {{6}}⟩'))
R[G, 5] = rec('find and interpret the mean absolute deviation',
  'The MAD is the average distance from the mean. A small MAD means the values sit close to the mean.',
  [('mean absolute deviation', 'The mean of the distances of the data values from the mean.'), ('deviation', 'How far a value is from the mean.')],
  'Averaging the signed differences, which always gives 0.',
  'On average, the values are ___ away from the mean of ___.',
  card('MAD of 4, 6, 8, 10', 'Mean = 7',
       'Distances: 3, 1, 1, 3', 'MAD ⟨\\frac{8}{4} = {{2}}⟩'))
R[G, 6] = rec('compare two data displays by center and spread (extension: Grade 7 comparison of populations)',
  'Compare the centers (mean or median) and the spreads (MAD or IQR). Saying how many spreads apart the centers are is a Grade 7 idea.',
  [('compare', 'Tell how two data sets are alike and different.'), ('overlap', 'How much two distributions share the same values.')],
  'Comparing only the maximums.',
  'Group ___ has the greater center, and group ___ is more spread out.',
  card('Two classes', 'Medians 80 and 80; IQRs 20 and 6.',
       'Centers: {{the same}}', 'Class with IQR {{20}} is more spread out'))
R[G, 7] = rec('describe the shape of a distribution and connect it to center',
  'A distribution can be symmetric, skewed left or skewed right, and can have peaks, gaps, clusters and outliers. In a skewed distribution the mean is pulled toward the tail.',
  [('symmetric', 'Having the same shape on both sides of the center.'), ('skewed', 'Having a long tail on one side.')],
  'Naming the skew by the side with the peak instead of the side with the tail.',
  'The data are skewed ___ because the tail is on the ___.',
  card('Shape and center', 'Most values are 2–5, with a few at 12 and 15.',
       'Tail on the {{right}}: skewed {{right}}', 'The mean is {{greater}} than the median'))
R[G, 8] = rec('summarize a data set: the number of observations, the attribute and its units, and center, spread and shape',
  'A full summary says how many observations there are, what was measured and in what units, a measure of center, a measure of variation and the overall shape.',
  [('observation', 'One data value, for one individual.'), ('attribute', 'The characteristic that is measured, such as height in inches.')],
  'Giving a center without saying what was measured or in what units.',
  'There are ___ observations of ___, measured in ___.',
  card('Describe the data', 'A dot plot of 11 students’ practice hours.',
       '{{11}} observations', 'attribute: {{hours practiced}}', 'center: median; spread: {{IQR}}'))
