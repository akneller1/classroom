"""8th Grade Math audit #15 (2026-11-19): one multi-part open-response item per level for the 23 skills that had none.
IDs end in -o01 (for example pa8-geo-s05-cp2-o01). Idempotent. Run from the repository root."""
import json, os, sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from lib import ROOT, load, save

NOTE = ('Original Claude-authored item (family: {fam}). 8th Grade Math audit 2026-11-19 (#15, open response); '
        'answers recomputed by scripts/test-grade8-audit.cjs.')
ABBR = {'real-numbers-exponents': 'rne', 'equations-expressions': 'eqx', 'linear-functional-relationships': 'lfr',
        'systems-linear-equations': 'sys', 'patterns-bivariate-data': 'biv', 'congruence-similarity': 'cgs', 'geometry-applications': 'geo'}
LV = ['cp2', 'cp1', 'honors']

# skill -> [ (prompt, [(part prompt, answer, step)], ) for cp2, cp1, honors ]
O = {}
O['congruence-similarity-skill-07'] = [
    ('Two angles of a triangle measure 48° and 67°.',
     [('Find the third angle.', '65°', '180 - 48 - 67 = 65.'),
      ('Find the exterior angle at the third vertex.', '115°', 'Exterior angle = sum of the two remote interior angles: 48 + 67 = 115.'),
      ('Show that the three interior angles add to 180°.', '48 + 67 + 65 = 180', '48 + 67 + 65 = 180.')]),
    ('The angles of a triangle measure x°, (2x)° and (x + 20)°.',
     [('Write an equation for the angle sum.', 'x + 2x + x + 20 = 180', 'The angles of a triangle add to 180°.'),
      ('Solve for x.', 'x = 40', '4x + 20 = 180, so 4x = 160 and x = 40.'),
      ('Find the largest angle.', '80°', 'The angles are 40°, 80° and 60°; the largest is 80°.')]),
    ('In a triangle, two interior angles measure (3x - 5)° and (2x + 10)°. The exterior angle at the third vertex measures 125°.',
     [('Write an equation using the exterior angle theorem.', '3x - 5 + 2x + 10 = 125', 'An exterior angle equals the sum of the two remote interior angles.'),
      ('Solve for x.', 'x = 24', '5x + 5 = 125, so x = 24.'),
      ('Find the two interior angles.', '67° and 58°', '3(24) - 5 = 67 and 2(24) + 10 = 58.'),
      ('Find the third interior angle.', '55°', '180 - 125 = 55 (a linear pair with the exterior angle); check: 67 + 58 + 55 = 180.')]),
]
O['congruence-similarity-skill-08'] = [
    ('Triangle ABC ~ triangle DEF with AB = 6, BC = 8, CA = 10 and DE = 9.',
     [('Find the scale factor from ABC to DEF.', '3/2', '9 ÷ 6 = 3/2.'),
      ('Find EF.', '12', '8 × 3/2 = 12.'),
      ('Find the perimeters of both triangles.', '24 and 36', 'ABC: 6 + 8 + 10 = 24. DEF: 24 × 3/2 = 36.')]),
    ('A 5-foot student casts a 3-foot shadow. At the same time a tree casts a 21-foot shadow.',
     [('Explain why the two triangles are similar.', 'AA: both have a right angle and the same angle of the sun', 'Both triangles have a right angle and the sun makes the same angle with the ground (AA).'),
      ('Write a proportion for the tree height h.', '5/3 = h/21', 'Heights and shadows are proportional.'),
      ('Find the height of the tree.', '35 feet', 'h = 21 × 5/3 = 35.')]),
    ('In triangle ACE, segment BD is parallel to CE, with B on AC and D on AE. AB = 4, BC = 6 and BD = 5.',
     [('Explain why triangle ABD is similar to triangle ACE.', 'AA: angle A is shared and corresponding angles are congruent', 'Angle A is in both triangles; BD ∥ CE makes corresponding angles ABD and ACE congruent.'),
      ('Find AC.', '10', 'AC = AB + BC = 4 + 6 = 10.'),
      ('Find the scale factor from ABD to ACE.', '5/2', '10 ÷ 4 = 5/2.'),
      ('Find CE.', '12.5', '5 × 5/2 = 12.5.')]),
]
O['congruence-similarity-skill-09'] = [
    ('Lines m and n are parallel and t is a transversal. At line m the angles are ∠1 (upper left), ∠2 (upper right), ∠3 (lower left) and ∠4 (lower right); ∠5 to ∠8 are in the same positions at line n. ∠1 = 65°.',
     [('Find ∠4 and name the angle pair.', '65°, vertical angles', '∠1 and ∠4 are vertical angles, so they are equal.'),
      ('Find ∠2.', '115°', '∠1 and ∠2 form a linear pair: 180 - 65 = 115.'),
      ('Find ∠5 and name the angle pair.', '65°, corresponding angles', '∠1 and ∠5 are corresponding angles, so they are equal.')]),
    ('Lines m and n are parallel and t is a transversal (angles numbered as usual: ∠1 to ∠4 at m, ∠5 to ∠8 at n, upper left, upper right, lower left, lower right). ∠3 = (4x + 10)° and ∠6 = (6x - 20)°.',
     [('Name the angle pair ∠3 and ∠6.', 'alternate interior angles', 'Both are between the lines, on opposite sides of t.'),
      ('Write and solve an equation for x.', '4x + 10 = 6x - 20; x = 15', 'Alternate interior angles are equal: 30 = 2x, so x = 15.'),
      ('Find ∠3.', '70°', '4(15) + 10 = 70.')]),
    ('Lines m and n are parallel and t is a transversal (angles numbered as usual: ∠1 to ∠4 at m, ∠5 to ∠8 at n, upper left, upper right, lower left, lower right). ∠4 = (3x + 5)° and ∠6 = (2x + 25)°.',
     [('Name the angle pair ∠4 and ∠6 and how they are related.', 'same-side interior angles; supplementary', 'Both are between the lines on the same side of t, so they add to 180°.'),
      ('Write and solve an equation for x.', '3x + 5 + 2x + 25 = 180; x = 30', '5x + 30 = 180, so x = 30.'),
      ('Find ∠4 and ∠6.', '95° and 85°', '3(30) + 5 = 95 and 2(30) + 25 = 85; 95 + 85 = 180.')]),
]
O['equations-expressions-skill-02'] = [
    ('Let A = 3x⁴ and B = 2x³.',
     [('Simplify A · B.', '6x⁷', '3 · 2 = 6 and x⁴ · x³ = x⁷.'),
      ('Simplify A².', '9x⁸', '3² = 9 and (x⁴)² = x⁸.'),
      ('Evaluate A · B when x = 1.', '6', '6(1)⁷ = 6.')]),
    ('Let A = 4a³b² and B = 2ab⁵.',
     [('Simplify A · B.', '8a⁴b⁷', '4 · 2 = 8, a³ · a = a⁴, b² · b⁵ = b⁷.'),
      ('Simplify A ÷ B with positive exponents.', '2a²/b³', '4 ÷ 2 = 2, a³ ÷ a = a², b² ÷ b⁵ = b⁻³ = 1/b³.'),
      ('Simplify A².', '16a⁶b⁴', '4² = 16, (a³)² = a⁶, (b²)² = b⁴.')]),
    ('Let A = (2x²y)³ and B = 4x⁵y².',
     [('Simplify A.', '8x⁶y³', '2³ = 8, (x²)³ = x⁶, y³.'),
      ('Simplify A ÷ B.', '2xy', '8 ÷ 4 = 2, x⁶ ÷ x⁵ = x, y³ ÷ y² = y.'),
      ('Simplify (A ÷ B)².', '4x²y²', '(2xy)² = 4x²y².')]),
]
O['equations-expressions-skill-05'] = [
    ('Solve 3(x + 4) = 27 step by step.',
     [('Distribute.', '3x + 12 = 27', 'Multiply 3 by both terms in the parentheses.'),
      ('Isolate the x-term.', '3x = 15', 'Subtract 12 from both sides.'),
      ('Solve and check.', 'x = 5; 3(5 + 4) = 27', 'Divide by 3. Check: 3 · 9 = 27.')]),
    ('Solve 4(2x - 3) = 2(x + 9) step by step.',
     [('Distribute on both sides.', '8x - 12 = 2x + 18', '4 · 2x - 4 · 3 and 2 · x + 2 · 9.'),
      ('Collect the x-terms and the constants.', '6x = 30', 'Subtract 2x and add 12.'),
      ('Solve and check.', 'x = 5; 4(7) = 2(14)', 'x = 5. Check: 28 = 28.')]),
    ('Solve (1/2)(6x + 8) - 3(x - 2) = 2x + 4 step by step.',
     [('Distribute.', '3x + 4 - 3x + 6 = 2x + 4', '(1/2)(6x) = 3x, (1/2)(8) = 4, and -3(x - 2) = -3x + 6.'),
      ('Simplify the left side.', '10 = 2x + 4', 'The x-terms cancel: 3x - 3x = 0, and 4 + 6 = 10.'),
      ('Solve.', 'x = 3', '2x = 6, so x = 3.'),
      ('Check.', '(1/2)(26) - 3(1) = 10 = 2(3) + 4', 'Left: 13 - 3 = 10. Right: 6 + 4 = 10.')]),
]
O['equations-expressions-skill-07'] = [
    ('Consider the equation 2(x + 3) = 2x + k.',
     [('How many solutions are there when k = 6?', 'infinitely many solutions', '2x + 6 = 2x + 6 is true for every x.'),
      ('How many solutions are there when k = 5?', 'no solution', '2x + 6 = 2x + 5 gives 6 = 5, which is false.'),
      ('Change the right side to 3x + 6. How many solutions now?', 'one solution: x = 0', '2x + 6 = 3x + 6 gives x = 0.')]),
    ('Consider 5x - 3(x - 2) = 2x + 6.',
     [('Simplify the left side.', '2x + 6', '5x - 3x + 6 = 2x + 6.'),
      ('How many solutions does the equation have?', 'infinitely many solutions', 'Both sides are 2x + 6, so every x works.'),
      ('Change the 6 on the right side to make the equation have no solution. Give one possible new equation.', '5x - 3(x - 2) = 2x + 7', 'Same x-coefficient, different constant: 6 ≠ 7.')]),
    ('Consider ax + 4 = 3x - b, where a and b are numbers.',
     [('For which values does the equation have infinitely many solutions?', 'a = 3 and b = -4', 'The sides must match: a = 3 and 4 = -b.'),
      ('For which values does it have no solution?', 'a = 3 and b ≠ -4', 'Same x-coefficients with different constants.'),
      ('For which values does it have exactly one solution?', 'a ≠ 3 (any b)', 'Different x-coefficients always give one solution.'),
      ('Find the solution when a = 5 and b = 2.', 'x = -3', '5x + 4 = 3x - 2, so 2x = -6 and x = -3.')]),
]
O['geometry-applications-skill-01'] = [
    ('A right triangle has legs 9 cm and 12 cm.',
     [('Find the hypotenuse.', '15 cm', '9² + 12² = 81 + 144 = 225, and √225 = 15.'),
      ('Find the perimeter.', '36 cm', '9 + 12 + 15 = 36.'),
      ('Find the area.', '54 square cm', '(1/2)(9)(12) = 54.')]),
    ('A triangle has sides 10, 24 and 26.',
     [('Use the converse of the Pythagorean theorem to decide whether it is a right triangle.', 'yes: 10² + 24² = 676 = 26²', '100 + 576 = 676 = 26².'),
      ('Which side is across from the right angle?', 'the side of length 26', 'The hypotenuse is the longest side.'),
      ('Find the area.', '120 square units', 'The legs are 10 and 24: (1/2)(10)(24) = 120.')]),
    ('A right triangle has legs x and x + 7 and hypotenuse 13.',
     [('Write an equation.', 'x² + (x + 7)² = 13²', 'Pythagorean theorem with the two legs.'),
      ('Find x by testing whole numbers.', 'x = 5', '5² + 12² = 25 + 144 = 169 = 13².'),
      ('Find the area of the triangle.', '30 square units', '(1/2)(5)(12) = 30.')]),
]
O['geometry-applications-skill-05'] = [
    ('A cylinder has radius 3 cm and height 10 cm.',
     [('Find its volume in terms of π.', '90π cubic cm', 'V = πr²h = π(9)(10) = 90π.'),
      ('Find its volume using 3.14 for π.', '282.6 cubic cm', '90 × 3.14 = 282.6.'),
      ('A cone has the same radius and height. Find its volume in terms of π.', '30π cubic cm', 'V = (1/3)π(9)(10) = 30π, one third of the cylinder.')]),
    ('A ball (sphere) has radius 6 cm and fits exactly in a cylindrical can with radius 6 cm and height 12 cm.',
     [('Find the volume of the ball in terms of π.', '288π cubic cm', '(4/3)π(6³) = (4/3)(216)π = 288π.'),
      ('Find the volume of the can in terms of π.', '432π cubic cm', 'π(6²)(12) = 432π.'),
      ('What fraction of the can does the ball fill?', '2/3', '288π ÷ 432π = 2/3.')]),
    ('A cone has radius 5 m and height 12 m.',
     [('Find its volume in terms of π.', '100π cubic m', '(1/3)π(25)(12) = 100π.'),
      ('Find its slant height.', '13 m', '√(5² + 12²) = √169 = 13.'),
      ('If the radius is doubled and the height stays the same, what is the new volume?', '400π cubic m', 'The radius is squared, so the volume is multiplied by 4: 400π.')]),
]
O['geometry-applications-skill-07'] = [
    ('A solid is a cylinder (radius 2 in., height 6 in.) with a cone (radius 2 in., height 3 in.) on top.',
     [('Find the volume of the cylinder in terms of π.', '24π cubic in.', 'π(2²)(6) = 24π.'),
      ('Find the volume of the cone in terms of π.', '4π cubic in.', '(1/3)π(2²)(3) = 4π.'),
      ('Find the total volume in terms of π.', '28π cubic in.', '24π + 4π = 28π.')]),
    ('A grain silo is a cylinder (radius 3 m, height 10 m) topped by a hemisphere with the same radius.',
     [('Find the volume of the cylinder in terms of π.', '90π cubic m', 'π(3²)(10) = 90π.'),
      ('Find the volume of the hemisphere in terms of π.', '18π cubic m', '(1/2)(4/3)π(3³) = 18π.'),
      ('Find the total volume using 3.14 for π.', '339.1 cubic m', '108π ≈ 108 × 3.14 = 339.12 ≈ 339.1.')]),
    ('A cone (radius 4 cm, height 6 cm) is drilled out of a cylinder (radius 4 cm, height 9 cm), with the same circular base.',
     [('Find the volume of the cylinder in terms of π.', '144π cubic cm', 'π(4²)(9) = 144π.'),
      ('Find the volume of the cone in terms of π.', '32π cubic cm', '(1/3)π(4²)(6) = 32π.'),
      ('Find the volume that remains in terms of π.', '112π cubic cm', '144π - 32π = 112π.'),
      ('What percent of the cylinder was removed, to the nearest tenth?', '22.2%', '32 ÷ 144 ≈ 0.2222 = 22.2%.')]),
]
O['linear-functional-relationships-skill-04'] = [
    ('A line passes through (1, 2) and (4, 11).',
     [('Find the rise and the run from the first point to the second.', 'rise 9, run 3', '11 - 2 = 9 and 4 - 1 = 3.'),
      ('Find the slope.', '3', '9 ÷ 3 = 3.'),
      ('Find the y-value of the point on the line with x = 6.', '17', 'From (4, 11), 2 more units right: 11 + 2 · 3 = 17.')]),
    ('A linear function has this table: x: 2, 4, 6; y: 7, 4, 1.',
     [('Find the slope.', '-3/2', '(4 - 7) ÷ (4 - 2) = -3/2.'),
      ('Is the function increasing or decreasing?', 'decreasing', 'The slope is negative.'),
      ('Find y when x = 10.', '-5', 'From (6, 1), 4 more units: 1 + 4(-3/2) = -5.')]),
    ('A line through (-2, k) and (4, 7) has slope 3/2.',
     [('Write an equation for k using the slope formula.', '(7 - k) ÷ (4 - (-2)) = 3/2', 'slope = rise ÷ run.'),
      ('Find k.', 'k = -2', '7 - k = 9, so k = -2.'),
      ('Find the y-intercept of the line.', '1', 'From (4, 7): 7 - 4(3/2) = 1.')]),
]
O['linear-functional-relationships-skill-05'] = [
    ('A line has slope 2 and passes through (3, 11).',
     [('Find the y-intercept.', 'b = 5', '11 = 2(3) + b, so b = 5.'),
      ('Write the equation in slope-intercept form.', 'y = 2x + 5', 'y = mx + b.'),
      ('Find y when x = 10.', '25', '2(10) + 5 = 25.')]),
    ('A line passes through (-2, 9) and (4, -3).',
     [('Find the slope.', '-2', '(-3 - 9) ÷ (4 - (-2)) = -12 ÷ 6 = -2.'),
      ('Write the equation in slope-intercept form.', 'y = -2x + 5', '9 = -2(-2) + b, so b = 5.'),
      ('Find the x-intercept.', '(5/2, 0)', '0 = -2x + 5, so x = 5/2.')]),
    ('A gym\'s total cost is linear in the number of months. After 3 months the total is $115; after 8 months it is $240.',
     [('Find the monthly rate.', '$25 per month', '(240 - 115) ÷ (8 - 3) = 25.'),
      ('Find the sign-up fee.', '$40', '115 - 3(25) = 40.'),
      ('Write an equation for the cost C after m months.', 'C = 25m + 40', 'Rate times months plus the fee.'),
      ('After how many months is the total $440?', '16 months', '25m + 40 = 440, so m = 16.')]),
]
O['linear-functional-relationships-skill-07'] = [
    ('A linear function has this table: x: 0, 1, 2, 3; y: 4, 7, 10, 13.',
     [('Find the rate of change.', '3', 'y goes up 3 each time x goes up 1.'),
      ('Find the starting value (y when x = 0).', '4', 'Read it from the table.'),
      ('Write the rule and find y when x = 10.', 'y = 3x + 4; 34', '3(10) + 4 = 34.')]),
    ('A linear function has this table: x: 2, 5, 8, 11; y: 1, 7, 13, 19.',
     [('Find the rate of change.', '2', 'Δy ÷ Δx = 6 ÷ 3 = 2.'),
      ('Write the rule.', 'y = 2x - 3', '1 = 2(2) + b, so b = -3.'),
      ('Find x when y = 37.', 'x = 20', '2x - 3 = 37, so x = 20.')]),
    ('A linear function has this table: x: -4, 0, 6, 10; y: 11, 5, -4, -10.',
     [('Find the rate of change.', '-3/2', '(5 - 11) ÷ (0 - (-4)) = -6/4 = -3/2; the other pairs agree.'),
      ('Write the rule.', 'y = -(3/2)x + 5', 'The table gives y = 5 at x = 0.'),
      ('Find the x-intercept.', '(10/3, 0)', '-(3/2)x + 5 = 0, so x = 10/3.')]),
]
O['linear-functional-relationships-skill-08'] = [
    ('A function is made of segments joining (0, 1), (3, 7), (5, 7) and (9, -1).',
     [('Over which interval is it increasing?', 'from x = 0 to x = 3', 'The graph rises from (0, 1) to (3, 7).'),
      ('Over which interval is it constant?', 'from x = 3 to x = 5', 'y stays 7.'),
      ('Over which interval is it decreasing?', 'from x = 5 to x = 9', 'The graph falls from (5, 7) to (9, -1).'),
      ('What are the maximum and minimum values?', 'maximum 7, minimum -1', 'Highest y = 7; lowest y = -1.')]),
    ('A function is made of segments joining (-4, 2), (-1, -4), (2, 5) and (6, 1).',
     [('Over which interval is it increasing?', 'from x = -1 to x = 2', 'The graph rises from (-1, -4) to (2, 5).'),
      ('Over which intervals is it decreasing?', 'from x = -4 to x = -1 and from x = 2 to x = 6', 'The graph falls on both pieces.'),
      ('What is the maximum value, and where?', '5, at x = 2', 'The highest point is (2, 5).'),
      ('What is the minimum value?', '-4', 'The lowest point is (-1, -4).')]),
    ('A function is made of segments joining (-6, 0), (-2, 6), (1, 6), (4, -3) and (7, 3).',
     [('Over which intervals is it increasing?', 'from x = -6 to x = -2 and from x = 4 to x = 7', 'The graph rises on these pieces.'),
      ('What are the maximum and minimum values?', 'maximum 6, minimum -3', 'Highest y = 6; lowest y = -3.'),
      ('Find the rate of change from x = 1 to x = 4.', '-3', '(-3 - 6) ÷ (4 - 1) = -3.')]),
]
O['linear-functional-relationships-skill-09'] = [
    ('Ann types w = 45m words in m minutes. Ben types 96 words in 2 minutes and 192 words in 4 minutes, at a constant rate.',
     [('Find Ann\'s rate.', '45 words per minute', 'The coefficient of m.'),
      ('Find Ben\'s rate.', '48 words per minute', '(192 - 96) ÷ (4 - 2) = 48.'),
      ('Who types faster, and by how much?', 'Ben, by 3 words per minute', '48 - 45 = 3.')]),
    ('Car A travels y = 28x miles on x gallons. Car B travels 87 miles on 3 gallons.',
     [('Find each car\'s miles per gallon.', 'Car A: 28; Car B: 29', '87 ÷ 3 = 29.'),
      ('Which car is more efficient?', 'Car B', '29 > 28.'),
      ('How many more miles does Car B go on 10 gallons?', '10 miles', '290 - 280 = 10.')]),
    ('Phone plan A costs C = 0.10t + 15 dollars for t minutes. Plan B: 100 minutes cost $32 and 300 minutes cost $48, and the cost is linear.',
     [('Find plan B\'s rate and starting fee.', '$0.08 per minute; $24', '(48 - 32) ÷ 200 = 0.08 and 32 - 0.08(100) = 24.'),
      ('Which plan is cheaper for 200 minutes?', 'Plan A ($35 vs $40)', 'A: 0.10(200) + 15 = 35. B: 0.08(200) + 24 = 40.'),
      ('For how many minutes do the plans cost the same?', '450 minutes', '0.10t + 15 = 0.08t + 24, so 0.02t = 9 and t = 450.')]),
]
O['patterns-bivariate-data-skill-01'] = [
    ('Hours studied: 1, 2, 3, 4, 5; test score: 60, 65, 72, 78, 84.',
     [('Write the ordered pairs to plot.', '(1, 60), (2, 65), (3, 72), (4, 78), (5, 84)', 'Pair the lists in order.'),
      ('Which variable goes on the x-axis?', 'hours studied', 'Hours explain the score.'),
      ('Describe the association.', 'positive', 'Scores rise as hours rise.')]),
    ('Outside temperature (°F): 50, 60, 70, 80, 90; drinks sold: 12, 18, 25, 33, 40.',
     [('Write the ordered pairs to plot.', '(50, 12), (60, 18), (70, 25), (80, 33), (90, 40)', 'Pair the lists in order.'),
      ('Choose a y-axis scale that fits the data.', '0 to 40 by 5', 'All values are from 12 to 40.'),
      ('Describe the association.', 'positive linear', 'The points rise at about the same rate.')]),
    ('x: 2, 3, 4, 5, 6, 7; y: 5, 7, 9, 30, 13, 15.',
     [('Write the ordered pairs to plot.', '(2, 5), (3, 7), (4, 9), (5, 30), (6, 13), (7, 15)', 'Pair the lists in order.'),
      ('Which point is an outlier?', '(5, 30)', 'The other points rise by 2 each step; 30 is far from that pattern.'),
      ('What y-value would fit the pattern at x = 5?', '11', '9 + 2 = 11.')]),
]
O['patterns-bivariate-data-skill-03'] = [
    ('Hours of TV: 0, 1, 2, 3, 4; hours of sleep: 10, 9.5, 9, 8.5, 8.',
     [('Is the association positive, negative or none?', 'negative', 'Sleep goes down as TV goes up.'),
      ('Is it linear or nonlinear?', 'linear', 'Sleep drops by 0.5 for each hour of TV.'),
      ('Predict sleep for 5 hours of TV.', '7.5 hours', '8 - 0.5 = 7.5.')]),
    ('Age of a car (years): 1, 2, 3, 4, 5; value ($1,000s): 24, 20, 17, 15, 14.',
     [('Is the association positive, negative or none?', 'negative', 'Value goes down as age goes up.'),
      ('Find the drops in value from year to year.', '4, 3, 2, 1', '24 - 20, 20 - 17, 17 - 15, 15 - 14.'),
      ('Is the association linear or nonlinear? Explain.', 'nonlinear: the drops are not equal', 'A linear pattern would drop by the same amount each year.')]),
    ('Side length of a square (cm): 1, 2, 3, 4, 5; area (square cm): 1, 4, 9, 16, 25.',
     [('Is the association positive, negative or none?', 'positive', 'Area rises as the side rises.'),
      ('Find the increases in area.', '3, 5, 7, 9', 'Differences of consecutive areas.'),
      ('Is the association linear or nonlinear? Explain.', 'nonlinear: the increases grow', 'Equal steps in x give larger and larger steps in y.')]),
]
O['patterns-bivariate-data-skill-04'] = [
    ('A line of best fit for test score y after x hours of study is y = 4x + 30.',
     [('What does the slope mean?', 'the score rises about 4 points per hour studied', 'Slope = change in y per 1 unit of x.'),
      ('What does the y-intercept mean?', 'a predicted score of 30 with 0 hours of study', 'y when x = 0.'),
      ('Predict the score for 5 hours.', '50', '4(5) + 30 = 50.')]),
    ('A line of fit on a scatter plot passes through (2, 50) and (8, 80).',
     [('Find the slope.', '5', '(80 - 50) ÷ (8 - 2) = 5.'),
      ('Write the equation of the line.', 'y = 5x + 40', '50 = 5(2) + b, so b = 40.'),
      ('Predict y when x = 10.', '90', '5(10) + 40 = 90.')]),
    ('A car\'s value y (thousands of dollars) after x years is modeled by y = -2.5x + 60.',
     [('Predict the value after 8 years.', '$40,000', '-2.5(8) + 60 = 40.'),
      ('After how many years is the predicted value $35,000?', '10 years', '-2.5x + 60 = 35, so x = 10.'),
      ('What does the slope mean?', 'the value drops about $2,500 per year', 'Slope -2.5 thousand dollars per year.'),
      ('Why is the model not reasonable for 30 years?', 'it predicts a negative value (-15)', '-2.5(30) + 60 = -15, but a car cannot be worth less than $0.')]),
]
O['patterns-bivariate-data-skill-05'] = [
    ('Of 50 students, 30 are in grade 7 and 20 are in grade 8. 18 grade 7 students and 8 grade 8 students have a pet.',
     [('How many grade 7 students have no pet?', '12', '30 - 18 = 12.'),
      ('How many grade 8 students have no pet?', '12', '20 - 8 = 12.'),
      ('Find the column totals for "pet" and "no pet".', '26 and 24', '18 + 8 = 26; 12 + 12 = 24; check 26 + 24 = 50.')]),
    ('In a survey of 80 students, 45 like soccer. 25 of the students who like soccer are girls, and 20 girls do not like soccer.',
     [('How many boys like soccer?', '20', '45 - 25 = 20.'),
      ('How many girls were surveyed?', '45', '25 + 20 = 45.'),
      ('How many boys do not like soccer?', '15', '80 - 45 = 35 boys; 35 - 20 = 15.')]),
    ('Of 120 students, 70 ride the bus. 30 of the bus riders are in grade 8, and 35 of the students who do not ride the bus are in grade 7.',
     [('How many grade 7 students ride the bus?', '40', '70 - 30 = 40.'),
      ('How many grade 8 students do not ride the bus?', '15', '120 - 70 = 50 do not ride; 50 - 35 = 15.'),
      ('Find the totals for grade 7 and for grade 8.', '75 and 45', '40 + 35 = 75; 30 + 15 = 45; check 75 + 45 = 120.')]),
]
O['patterns-bivariate-data-skill-06'] = [
    ('Grade 7: 12 students are in band and 18 are not. Grade 8: 15 are in band and 15 are not.',
     [('What percent of grade 7 students are in band?', '40%', '12 ÷ 30 = 0.4.'),
      ('What percent of grade 8 students are in band?', '50%', '15 ÷ 30 = 0.5.'),
      ('Is there an association between grade and band? Explain.', 'yes: a greater share of grade 8 students are in band', '50% is noticeably more than 40%.')]),
    ('Juniors: 24 have a job and 16 do not. Seniors: 30 have a job and 10 do not.',
     [('What percent of juniors have a job?', '60%', '24 ÷ 40 = 0.6.'),
      ('What percent of seniors have a job?', '75%', '30 ÷ 40 = 0.75.'),
      ('Of the students with jobs, what fraction are seniors?', '5/9', '30 ÷ 54 = 5/9.')]),
    ('Grade 7: 18 of 45 students eat breakfast at school. Grade 8: 22 of 55 students eat breakfast at school.',
     [('Find the relative frequency for grade 7.', '40%', '18 ÷ 45 = 0.4.'),
      ('Find the relative frequency for grade 8.', '40%', '22 ÷ 55 = 0.4.'),
      ('Is there an association between grade and eating breakfast at school? Explain.', 'no: both grades are 40%', 'Equal relative frequencies show no association.')]),
]
O['real-numbers-exponents-skill-04'] = [
    ('Consider the numbers √36, √40, 0.75 and π.',
     [('Which are rational?', '√36 and 0.75', '√36 = 6 and 0.75 = 3/4.'),
      ('Which are irrational?', '√40 and π', 'Their decimals never end or repeat.'),
      ('Explain why √40 is irrational.', '40 is not a perfect square', '6² = 36 and 7² = 49, so √40 is not a whole number.')]),
    ('Consider 0.121212… (12 repeats), √(9/16), ∛10 and 22/7.',
     [('Which numbers are rational?', '0.121212…, √(9/16) and 22/7', 'A repeating decimal and ratios of integers are rational.'),
      ('Which number is irrational?', '∛10', '10 is not a perfect cube.'),
      ('Write 0.121212… as a fraction in simplest form.', '4/33', '100n - n = 12, so n = 12/99 = 4/33.')]),
    ('A square has area 50 square units.',
     [('Write its side length exactly.', '√50', 'side² = 50.'),
      ('Is the side length rational or irrational?', 'irrational', '50 is not a perfect square.'),
      ('Between which two whole numbers is the side length?', '7 and 8', '7² = 49 and 8² = 64.'),
      ('Is 7.07 the exact side length? Explain.', 'no: 7.07² = 49.9849', 'An irrational number has no exact terminating decimal.')]),
]
O['real-numbers-exponents-skill-10'] = [
    ('Use scientific notation.',
     [('Write 4,500,000 in scientific notation.', '4.5 × 10⁶', 'Move the decimal point 6 places left.'),
      ('Write 0.00032 in scientific notation.', '3.2 × 10⁻⁴', 'Move the decimal point 4 places right.'),
      ('Which number is greater?', '4.5 × 10⁶', 'A positive power of 10 is greater than a negative one.')]),
    ('The Sun is about 1.5 × 10⁸ km from Earth, and the Moon is about 3.8 × 10⁵ km from Earth.',
     [('Write both distances in standard form.', '150,000,000 km and 380,000 km', 'Move the decimal point 8 and 5 places right.'),
      ('Which is farther?', 'the Sun', '10⁸ > 10⁵.'),
      ('About how many times farther is the Sun? Round to one significant figure.', 'about 400 times', '1.5 × 10⁸ ÷ (3.8 × 10⁵) ≈ 395, about 4 × 10².')]),
    ('A dust grain is 0.000062 m wide. A grain of sand is 5.9 × 10⁻⁴ m wide.',
     [('Write the dust grain\'s width in scientific notation.', '6.2 × 10⁻⁵ m', 'Move the decimal point 5 places right.'),
      ('Rewrite 62 × 10⁻⁶ in scientific notation.', '6.2 × 10⁻⁵', '62 = 6.2 × 10¹, so 6.2 × 10⁻⁵.'),
      ('Which grain is wider?', 'the grain of sand', '10⁻⁴ > 10⁻⁵.'),
      ('About how many times wider? Round to the nearest whole number.', 'about 10 times', '5.9 × 10⁻⁴ ÷ (6.2 × 10⁻⁵) ≈ 9.5, about 10.')]),
]
O['systems-linear-equations-skill-01'] = [
    ('Graph y = 2x - 3.',
     [('Find the slope and the y-intercept.', 'slope 2, y-intercept -3', 'y = mx + b with m = 2 and b = -3.'),
      ('Which point do you plot first?', '(0, -3)', 'Start at the y-intercept.'),
      ('Use the slope to find two more points.', '(1, -1) and (2, 1)', 'Up 2, right 1, twice.')]),
    ('Graph 3x + 2y = 8.',
     [('Rewrite the equation in slope-intercept form.', 'y = -(3/2)x + 4', '2y = -3x + 8, then divide by 2.'),
      ('Find the slope and the y-intercept.', 'slope -3/2, y-intercept 4', 'Read m and b.'),
      ('Find a second point to plot.', '(2, 1)', 'From (0, 4): down 3, right 2.')]),
    ('A line passes through (0, -2) and is parallel to 4x - 2y = 6.',
     [('Find the slope of 4x - 2y = 6.', '2', '-2y = -4x + 6, so y = 2x - 3.'),
      ('Write the equation of the new line.', 'y = 2x - 2', 'Parallel lines have the same slope; the y-intercept is -2.'),
      ('Does the new line pass through (-1, -4)? Explain.', 'yes: 2(-1) - 2 = -4', 'Substitute x = -1.')]),
]
O['systems-linear-equations-skill-03'] = [
    ('Solve y = 2x + 1 and 3x + y = 16 by substitution.',
     [('Substitute for y.', '3x + (2x + 1) = 16', 'Replace y with 2x + 1.'),
      ('Solve for x.', 'x = 3', '5x + 1 = 16, so x = 3.'),
      ('Find y and write the solution.', '(3, 7)', 'y = 2(3) + 1 = 7.'),
      ('Check in both equations.', '7 = 2(3) + 1 and 3(3) + 7 = 16', 'Both are true.')]),
    ('Solve x = 4y - 5 and 2x - 3y = 10 by substitution.',
     [('Substitute for x.', '2(4y - 5) - 3y = 10', 'Replace x with 4y - 5.'),
      ('Solve for y.', 'y = 4', '8y - 10 - 3y = 10, so 5y = 20.'),
      ('Find x and write the solution.', '(11, 4)', 'x = 4(4) - 5 = 11.')]),
    ('A school sold adult and child tickets. There were 15 more adult tickets than child tickets, adult tickets cost $12, child tickets cost $8, and sales were $680.',
     [('Write a system using a for adult tickets and c for child tickets.', 'a = c + 15 and 12a + 8c = 680', 'One equation compares the counts; one gives the money.'),
      ('Substitute and solve for c.', 'c = 25', '12(c + 15) + 8c = 680, so 20c + 180 = 680 and c = 25.'),
      ('Find a.', 'a = 40', 'a = 25 + 15.'),
      ('Check the money.', '12(40) + 8(25) = 680', '480 + 200 = 680.')]),
]

# A fourth part for every item that had three (the bank schema needs at least four parts).
EXTRA = {
    ('congruence-similarity-skill-07', 0): ('Is the triangle acute, right or obtuse? Explain.', 'acute: every angle is less than 90°', 'The angles are 48°, 67° and 65°.'),
    ('congruence-similarity-skill-07', 1): ('Find the exterior angle next to the 80° angle.', '100°', '180 - 80 = 100, which also equals 40 + 60.'),
    ('congruence-similarity-skill-08', 0): ('How does the ratio of the perimeters compare with the scale factor?', 'they are equal: 36/24 = 3/2', 'Every length, including the perimeter, is multiplied by 3/2.'),
    ('congruence-similarity-skill-08', 1): ('How long is the shadow of a 15-foot flagpole at the same time?', '9 feet', 'Shadow = height × 3/5 = 15 × 3/5 = 9.'),
    ('congruence-similarity-skill-09', 0): ('Find ∠7 and name its relationship to ∠2.', '115°, alternate exterior angles', '∠2 and ∠7 are outside the lines on opposite sides of t, so they are equal.'),
    ('congruence-similarity-skill-09', 1): ('Find ∠5.', '110°', '∠5 and ∠6 form a linear pair: 180 - 70 = 110.'),
    ('congruence-similarity-skill-09', 2): ('Find ∠8.', '95°', '∠5 = 180 - 85 = 95 (a linear pair with ∠6), and ∠8 = ∠5 (vertical angles).'),
    ('equations-expressions-skill-02', 0): ('Simplify A ÷ B.', '3x/2', '3 ÷ 2 = 3/2 and x⁴ ÷ x³ = x.'),
    ('equations-expressions-skill-02', 1): ('Evaluate A ÷ B when a = 2 and b = 1.', '8', '2(2²)/1³ = 8.'),
    ('equations-expressions-skill-02', 2): ('Evaluate (A ÷ B)² when x = 1 and y = 3.', '36', '4(1²)(3²) = 36.'),
    ('equations-expressions-skill-05', 0): ('Solve the same equation a second way: divide both sides by 3 first.', 'x + 4 = 9, so x = 5', '27 ÷ 3 = 9, then subtract 4.'),
    ('equations-expressions-skill-05', 1): ('Divide both sides by 2 first. What equation do you get, and does it give the same x?', '2(2x - 3) = x + 9; yes, x = 5', '4x - 6 = x + 9, so 3x = 15 and x = 5.'),
    ('equations-expressions-skill-07', 0): ('Explain why k = 5 gives no solution.', 'the x-terms cancel and 6 = 5 is false', 'Subtracting 2x from both sides leaves 6 = 5.'),
    ('equations-expressions-skill-07', 1): ('Change the right side so the equation has exactly one solution, and solve it.', 'for example 5x - 3(x - 2) = 3x + 6; x = 0', '2x + 6 = 3x + 6 gives x = 0.'),
    ('geometry-applications-skill-01', 0): ('A triangle has sides 9, 12 and 16. Is it a right triangle?', 'no: 81 + 144 = 225 ≠ 256', '9² + 12² = 225 and 16² = 256.'),
    ('geometry-applications-skill-01', 1): ('Find the length of the altitude to the side of length 26, to the nearest tenth.', '9.2', 'Area 120 = (1/2)(26)h, so h = 240/26 ≈ 9.2.'),
    ('geometry-applications-skill-01', 2): ('Find the perimeter of the triangle.', '30 units', '5 + 12 + 13 = 30.'),
    ('geometry-applications-skill-05', 0): ('A sphere has the same radius. Find its volume in terms of π.', '36π cubic cm', '(4/3)π(3³) = 36π.'),
    ('geometry-applications-skill-05', 1): ('How much space in the can is empty, in terms of π?', '144π cubic cm', '432π - 288π = 144π.'),
    ('geometry-applications-skill-05', 2): ('A cylinder has the same radius and height as the original cone. Find its volume in terms of π.', '300π cubic m', 'π(25)(12) = 300π, three times the cone.'),
    ('geometry-applications-skill-07', 0): ('Find the total volume using 3.14 for π, to the nearest tenth.', '87.9 cubic in.', '28 × 3.14 = 87.92.'),
    ('geometry-applications-skill-07', 1): ('What percent of the silo\'s volume is in the hemisphere, to the nearest tenth?', '16.7%', '18π ÷ 108π = 1/6 ≈ 16.7%.'),
    ('linear-functional-relationships-skill-04', 0): ('Is the line increasing or decreasing?', 'increasing', 'The slope 3 is positive.'),
    ('linear-functional-relationships-skill-04', 1): ('Find y when x = 0.', '10', 'From (2, 7), 2 units left: 7 + 2(3/2) = 10.'),
    ('linear-functional-relationships-skill-04', 2): ('Does the line pass through (8, 13)? Explain.', 'yes: 13 = (3/2)(8) + 1', '(3/2)(8) + 1 = 13.'),
    ('linear-functional-relationships-skill-05', 0): ('Find x when y = 0.', 'x = -5/2', '2x + 5 = 0, so x = -5/2.'),
    ('linear-functional-relationships-skill-05', 1): ('Does the line pass through (1, 3)? Explain.', 'yes: -2(1) + 5 = 3', 'Substitute x = 1.'),
    ('linear-functional-relationships-skill-07', 0): ('Find x when y = 31.', 'x = 9', '3x + 4 = 31, so x = 9.'),
    ('linear-functional-relationships-skill-07', 1): ('Find the missing value: x = 14, y = ?', '25', '2(14) - 3 = 25.'),
    ('linear-functional-relationships-skill-07', 2): ('Find y when x = 2.', '2', '-(3/2)(2) + 5 = 2.'),
    ('linear-functional-relationships-skill-08', 2): ('Over which interval is the function constant?', 'from x = -2 to x = 1', 'y stays 6.'),
    ('linear-functional-relationships-skill-09', 0): ('How many more words does Ben type in 10 minutes?', '30 words', '480 - 450 = 30.'),
    ('linear-functional-relationships-skill-09', 1): ('How many gallons does Car A need for 140 miles?', '5 gallons', '140 ÷ 28 = 5.'),
    ('linear-functional-relationships-skill-09', 2): ('Which plan is cheaper for 600 minutes?', 'Plan B ($72 vs $75)', 'A: 0.10(600) + 15 = 75. B: 0.08(600) + 24 = 72.'),
    ('patterns-bivariate-data-skill-01', 0): ('Predict the score for 6 hours if the pattern continues.', 'about 90', 'Scores rise about 6 points per hour: 84 + 6 = 90.'),
    ('patterns-bivariate-data-skill-01', 1): ('About how many drinks are sold each time the temperature rises 10°F?', 'about 7', '(40 - 12) ÷ 4 = 7.'),
    ('patterns-bivariate-data-skill-01', 2): ('Describe the association of the other five points.', 'positive linear', 'They rise by 2 for each step of 1.'),
    ('patterns-bivariate-data-skill-03', 0): ('Does watching TV cause less sleep? Explain.', 'not necessarily: association does not show cause', 'Another factor, such as staying up late, could explain both.'),
    ('patterns-bivariate-data-skill-03', 1): ('Predict the drop from year 5 to year 6 if the pattern continues.', 'about $1,000 or less', 'The drops are shrinking: 4, 3, 2, 1.'),
    ('patterns-bivariate-data-skill-03', 2): ('Predict the area for a side length of 6 cm.', '36 square cm', '6² = 36 (the next increase is 11).'),
    ('patterns-bivariate-data-skill-04', 0): ('Predict the score for 12 hours. Is the prediction reasonable?', '78; reasonable (below 100)', '4(12) + 30 = 78.'),
    ('patterns-bivariate-data-skill-04', 1): ('What does the slope mean if x is hours and y is score?', 'about 5 more points per hour', 'Slope = change in y per 1 unit of x.'),
    ('patterns-bivariate-data-skill-05', 0): ('What percent of all students have a pet?', '52%', '26 ÷ 50 = 0.52.'),
    ('patterns-bivariate-data-skill-05', 1): ('How many students do not like soccer?', '35', '80 - 45 = 35 (20 girls and 15 boys).'),
    ('patterns-bivariate-data-skill-05', 2): ('What percent of grade 7 students ride the bus, to the nearest whole percent?', '53%', '40 ÷ 75 ≈ 0.533.'),
    ('patterns-bivariate-data-skill-06', 0): ('Of the students in band, what fraction are in grade 8?', '5/9', '15 ÷ 27 = 5/9.'),
    ('patterns-bivariate-data-skill-06', 1): ('Is there an association between grade and having a job? Explain.', 'yes: 75% of seniors vs 60% of juniors', 'The relative frequencies differ.'),
    ('patterns-bivariate-data-skill-06', 2): ('What percent of all students eat breakfast at school?', '40%', '(18 + 22) ÷ 100 = 0.4.'),
    ('real-numbers-exponents-skill-04', 0): ('Between which two whole numbers is √40?', '6 and 7', '36 < 40 < 49.'),
    ('real-numbers-exponents-skill-04', 1): ('Between which two whole numbers is ∛10?', '2 and 3', '2³ = 8 < 10 < 27 = 3³.'),
    ('real-numbers-exponents-skill-10', 0): ('How many times greater is 4.5 × 10⁶ than 4.5 × 10⁻⁴?', '10¹⁰ times', '10⁶ ÷ 10⁻⁴ = 10¹⁰.'),
    ('real-numbers-exponents-skill-10', 1): ('Write the Moon\'s distance in meters in scientific notation (1 km = 10³ m).', '3.8 × 10⁸ m', '3.8 × 10⁵ × 10³ = 3.8 × 10⁸.'),
    ('systems-linear-equations-skill-01', 0): ('Find the x-intercept.', '(3/2, 0)', '2x - 3 = 0, so x = 3/2.'),
    ('systems-linear-equations-skill-01', 1): ('Does the line pass through (4, -2)? Explain.', 'yes: 3(4) + 2(-2) = 8', 'Substitute into 3x + 2y = 8.'),
    ('systems-linear-equations-skill-01', 2): ('Do the two lines intersect? Explain.', 'no: same slope, different y-intercepts', 'y = 2x - 2 and y = 2x - 3 are parallel.'),
    ('systems-linear-equations-skill-03', 1): ('Check the solution in both equations.', '11 = 4(4) - 5 and 2(11) - 3(4) = 10', 'Both are true.'),
}


def run():
    banks = load()
    added = 0
    tagsf = {u: os.path.join(ROOT, 'question-banks', 'prealgebra', 'meta', u + '.tags.json') for u in banks}
    tags = {u: json.load(open(f, encoding='utf-8')) for u, f in tagsf.items()}
    for skill, levels in O.items():
        unit, n = skill.rsplit('-skill-', 1)
        bank = banks[unit]['questions']
        std = next(q['standards'] for q in bank if q['skillId'] == skill)
        for li, (L, (prompt, parts)) in enumerate(zip(LV, levels)):
            if len(parts) < 4:
                parts = parts + [EXTRA[(skill, li)]]
            qid = f'pa8-{ABBR[unit]}-s{n}-{L}-o01'
            q = {'id': qid, 'skillId': skill, 'level': L, 'format': 'open-response', 'prompt': prompt,
                 'parts': [{'prompt': p, 'answer': a} for p, a, _ in parts],
                 'answer': '; '.join(f'({chr(97 + i)}) {a}' for i, (_, a, _) in enumerate(parts)),
                 'solutionSteps': [s for _, _, s in parts], 'standards': std,
                 'sourceNotes': NOTE.format(fam=f's{int(n)}_open_audit')}
            old = next((x for x in bank if x['id'] == qid), None)
            if old:
                old.clear(); old.update(q)
            else:
                idx = max(i for i, x in enumerate(bank) if x['skillId'] == skill and x['level'] == L)
                bank.insert(idx + 1, q)
                added += 1
            tags[unit][qid] = ['multistep', 'reasoning']
    for u, f in tagsf.items():
        with open(f, 'w', encoding='utf-8') as fh:
            json.dump(tags[u], fh, ensure_ascii=False, indent=0)
    save(banks)
    return added


if __name__ == '__main__':
    print('open response added', run())
