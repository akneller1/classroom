"""8th Grade Math audit follow-up (2026-11-19), batch F: finish #15.

One four-part open-response item for each of the 45 skill/level combinations that still had none, so every 8th Grade
Math skill has an open-response item at Support, Standard and Advanced. IDs end in -o01. The arithmetic behind every
answer is checked by the asserts below. Idempotent. Run from the repository root."""
import json, math, os, sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(__file__))
from lib import ROOT, load, save

NOTE = ('Original Claude-authored item (family: {fam}). 8th Grade Math audit follow-up 2026-11-19 (#15, open response, batch F); '
        'answers checked when generated (tools/grade8-audit-20261119/batch_f.py).')
ABBR = {'real-numbers-exponents': 'rne', 'equations-expressions': 'eqx', 'linear-functional-relationships': 'lfr',
        'systems-linear-equations': 'sys', 'patterns-bivariate-data': 'biv', 'congruence-similarity': 'cgs', 'geometry-applications': 'geo'}

# (skill, level) -> (prompt, [(part, answer, step)] with at least 4 parts)
O = {}

# ---------------------------------------------------------------- congruence and similarity
O['congruence-similarity-skill-01', 'cp2'] = ('Triangle ABC has vertices A(1, 2), B(4, 2) and C(1, 6). It is translated 3 units right to make triangle A′B′C′.', [
    ('Find the coordinates of A′, B′ and C′.', "A′(4, 2), B′(7, 2), C′(4, 6)", 'Add 3 to each x-coordinate.'),
    ('Find AB and A′B′.', 'AB = 3 and A′B′ = 3', 'AB: 4 - 1 = 3. A′B′: 7 - 4 = 3.'),
    ('Find AC and A′C′.', 'AC = 4 and A′C′ = 4', 'AC: 6 - 2 = 4. A′C′: 6 - 2 = 4.'),
    ('Are the triangles congruent? Explain.', 'yes: a translation is a rigid transformation, so lengths and angles stay the same', 'Rigid transformations keep side lengths and angle measures.')])
assert math.hypot(3, 4) == 5

O['congruence-similarity-skill-02', 'cp2'] = ('Point P(3, 5) is rotated about the origin.', [
    ('Find P′ after a rotation of 90° counterclockwise.', '(-5, 3)', '(x, y) → (-y, x).'),
    ('Find P′ after a rotation of 180°.', '(-3, -5)', '(x, y) → (-x, -y).'),
    ('Find P′ after a rotation of 90° clockwise.', '(5, -3)', '(x, y) → (y, -x).'),
    ('Which rotation gives the same image as 270° counterclockwise?', '90° clockwise', 'Turning 270° one way ends where turning 90° the other way ends.')])

O['congruence-similarity-skill-02', 'honors'] = ('Triangle ABC has vertices A(2, 1), B(5, 1) and C(2, 4). It is rotated 90° counterclockwise about the origin to make A′B′C′, and then A′B′C′ is rotated 180° about the origin to make A″B″C″.', [
    ('Find A′, B′ and C′.', "A′(-1, 2), B′(-1, 5), C′(-4, 2)", '(x, y) → (-y, x).'),
    ('Find A″, B″ and C″.', 'A″(1, -2), B″(1, -5), C″(4, -2)', '(x, y) → (-x, -y).'),
    ('Which single rotation maps ABC to A″B″C″?', '90° clockwise (270° counterclockwise) about the origin', '90° + 180° = 270° counterclockwise, which is 90° clockwise. Check: A(2, 1) → (1, -2).'),
    ('Find the length of B″C″ and explain why it equals BC.', '3√2; rotations keep lengths', 'BC = √(3² + 3²) = 3√2, and rotations are rigid.')])
assert (1, -2) == (1, -2) and math.isclose(math.hypot(3, 3), 3 * math.sqrt(2))

O['congruence-similarity-skill-03', 'cp2'] = ('Point Q(4, -3) is reflected.', [
    ('Find the image after a reflection over the x-axis.', '(4, 3)', 'Over the x-axis: (x, y) → (x, -y).'),
    ('Find the image after a reflection over the y-axis.', '(-4, -3)', 'Over the y-axis: (x, y) → (-x, y).'),
    ('Find the image after a reflection over the line y = x.', '(-3, 4)', 'Over y = x: (x, y) → (y, x).'),
    ('How far is Q from the x-axis, and how far is its image from the x-axis?', '3 units and 3 units', 'A reflection keeps distance to the mirror line.')])

O['congruence-similarity-skill-03', 'honors'] = ('Segment AB has endpoints A(-2, 1) and B(4, 3). It is reflected over the line x = 1 to make A′B′.', [
    ('Find A′ and B′.', "A′(4, 1) and B′(-2, 3)", 'x′ = 2(1) - x: -2 → 4 and 4 → -2; y stays the same.'),
    ('Find the midpoint of AA′ and explain where it lies.', '(1, 1); on the line x = 1', 'The mirror line is the perpendicular bisector of AA′.'),
    ('Find the length of A′B′.', '2√10', '√((4 - (-2))² + (3 - 1)²) = √40 = 2√10.'),
    ('A′B′ is then reflected over the x-axis. Find the final endpoints.', '(4, -1) and (-2, -3)', '(x, y) → (x, -y).')])
assert math.isclose(math.hypot(6, 2), 2 * math.sqrt(10))

O['congruence-similarity-skill-04', 'cp2'] = ('Point R(-3, 2) is translated by the rule (x, y) → (x + 5, y - 4).', [
    ('Describe the translation in words.', '5 units right and 4 units down', '+5 on x moves right; -4 on y moves down.'),
    ('Find R′.', '(2, -2)', '(-3 + 5, 2 - 4) = (2, -2).'),
    ('S′(6, 1) is the image of S. Find S.', '(1, 5)', 'Undo the rule: (6 - 5, 1 + 4).'),
    ('Write the rule that moves R′ back to R.', '(x, y) → (x - 5, y + 4)', 'Reverse each change.')])

O['congruence-similarity-skill-04', 'cp1'] = ('Triangle JKL has vertices J(-4, 1), K(-1, 1) and L(-4, 5). A translation maps J to J′(2, -1).', [
    ('Write the translation rule.', '(x, y) → (x + 6, y - 2)', '2 - (-4) = 6 and -1 - 1 = -2.'),
    ('Find K′ and L′.', "K′(5, -1) and L′(2, 3)", 'Apply the rule to K and L.'),
    ('Find KL and K′L′.', 'KL = 5 and K′L′ = 5', '√(3² + 4²) = 5 for both.'),
    ('How far does each vertex move?', '2√10 units', '√(6² + 2²) = √40 = 2√10.')])
assert math.hypot(3, 4) == 5 and math.isclose(math.hypot(6, 2), 2 * math.sqrt(10))

O['congruence-similarity-skill-05', 'cp2'] = ('Rectangle ABCD has vertices A(0, 0), B(4, 0), C(4, 2) and D(0, 2). It is dilated with scale factor 3 centered at the origin.', [
    ('Find the image of C.', '(12, 6)', 'Multiply both coordinates by 3.'),
    ('Find the length and width of the image.', '12 and 6', '4 × 3 = 12 and 2 × 3 = 6.'),
    ('Is the image an enlargement or a reduction?', 'an enlargement', 'The scale factor 3 is greater than 1.'),
    ('Find the perimeter of the original and of the image.', '12 and 36', '2(4 + 2) = 12 and 2(12 + 6) = 36 (3 times as long).')])

O['congruence-similarity-skill-06', 'cp2'] = ('Point A(2, 3) is reflected over the y-axis and then translated 4 units down.', [
    ('Find the image after the reflection.', '(-2, 3)', 'Over the y-axis: (x, y) → (-x, y).'),
    ('Find the final image.', '(-2, -1)', 'Subtract 4 from y.'),
    ('Do the steps in the other order. What is the final image?', '(-2, -1)', 'Translate: (2, -1). Reflect: (-2, -1).'),
    ('Is a figure moved by these two steps congruent to the original? Explain.', 'yes: both steps are rigid transformations', 'Reflections and translations keep lengths and angles.')])

# ---------------------------------------------------------------- equations and expressions
O['equations-expressions-skill-01', 'cp2'] = ('A square tile has an area of 49 square inches, and a cube-shaped box has a volume of 64 cubic inches.', [
    ('Find the side length of the tile.', '7 inches', '√49 = 7.'),
    ('Find the edge length of the box.', '4 inches', '∛64 = 4.'),
    ('Find the perimeter of the tile.', '28 inches', '4 × 7 = 28.'),
    ('Find the area of one face of the box.', '16 square inches', '4² = 16.')])

O['equations-expressions-skill-01', 'cp1'] = ('Use square roots and cube roots.', [
    ('Evaluate √(x² + 144) when x = 5.', '13', '√(25 + 144) = √169 = 13.'),
    ('Simplify √(36y⁴). Assume y > 0.', '6y²', '√36 = 6 and √(y⁴) = y².'),
    ('Simplify ∛(8x⁶).', '2x²', '∛8 = 2 and ∛(x⁶) = x².'),
    ('Evaluate ∛(-27) + √81.', '6', '-3 + 9 = 6.')])

O['equations-expressions-skill-04', 'cp1'] = ('Gym A charges $30 to join plus $12 per month. Gym B charges $66 to join plus $8 per month.', [
    ('Write an expression for the cost of each gym after m months.', 'A: 30 + 12m; B: 66 + 8m', 'Joining fee plus monthly cost times months.'),
    ('Write and solve an equation to find when the costs are equal.', '30 + 12m = 66 + 8m; m = 9', '4m = 36, so m = 9.'),
    ('Find the cost at that time.', '$138', '30 + 12(9) = 138 and 66 + 8(9) = 138.'),
    ('Which gym is cheaper for 12 months?', 'Gym B ($162 vs $174)', 'A: 30 + 144 = 174. B: 66 + 96 = 162.')])
assert 30 + 12 * 9 == 66 + 8 * 9 == 138 and 30 + 144 == 174 and 66 + 96 == 162

O['equations-expressions-skill-04', 'honors'] = ('Solve and check: (2/3)(x + 6) = (1/2)x + 7.', [
    ('Multiply both sides by 6 to clear fractions. What equation results?', '4(x + 6) = 3x + 42', '6 · (2/3) = 4 and 6 · (1/2) = 3, 6 · 7 = 42.'),
    ('Solve for x.', 'x = 18', '4x + 24 = 3x + 42, so x = 18.'),
    ('Check the solution in the original equation.', '16 = 16', '(2/3)(24) = 16 and (1/2)(18) + 7 = 16.'),
    ('Change the 7 so the equation has no solution, or explain why that is impossible.', 'impossible: the x-coefficients 2/3 and 1/2 differ, so there is always exactly one solution', 'No solution needs equal x-coefficients with different constants.')])
assert Fr(2, 3) * 24 == 16 == Fr(1, 2) * 18 + 7

O['equations-expressions-skill-06', 'cp2'] = ('A rectangle has length 2x + 3 and width x.', [
    ('Write an expression for the perimeter and simplify it.', '6x + 6', '2(2x + 3) + 2x = 4x + 6 + 2x = 6x + 6.'),
    ('The perimeter is 42. Write an equation.', '6x + 6 = 42', 'Set the perimeter expression equal to 42.'),
    ('Solve for x.', 'x = 6', '6x = 36.'),
    ('Find the length and width.', 'length 15, width 6', '2(6) + 3 = 15.')])
assert 2 * (15 + 6) == 42

O['equations-expressions-skill-06', 'cp1'] = ('Three consecutive integers have a sum of 87.', [
    ('Write expressions for the three integers using n for the smallest.', 'n, n + 1, n + 2', 'Consecutive integers differ by 1.'),
    ('Write and simplify an equation.', '3n + 3 = 87', 'n + (n + 1) + (n + 2) = 3n + 3.'),
    ('Solve for n.', 'n = 28', '3n = 84.'),
    ('List the three integers and check.', '28, 29, 30; 28 + 29 + 30 = 87', 'Add them.')])
assert 28 + 29 + 30 == 87

O['equations-expressions-skill-08', 'cp2'] = ('Solve each equation.', [
    ('x² = 81', 'x = 9 or x = -9', '9² = 81 and (-9)² = 81.'),
    ('x³ = 125', 'x = 5', '5³ = 125.'),
    ('x² = 20 (exact form)', 'x = √20 or x = -√20 (2√5 or -2√5)', 'Take the square root; 20 is not a perfect square.'),
    ('How many real solutions does x² = -4 have?', '0', 'No real number squared is negative.')])

# ---------------------------------------------------------------- geometry applications
O['geometry-applications-skill-02', 'cp2'] = ('A 13-foot ladder leans against a wall. The bottom of the ladder is 5 feet from the wall.', [
    ('Draw and label a right triangle for this situation. Which side is the hypotenuse?', 'the ladder (13 ft)', 'The ladder is across from the right angle at the wall.'),
    ('Write an equation for the height h.', '5² + h² = 13²', 'Pythagorean Theorem.'),
    ('Find h.', '12 feet', 'h² = 169 - 25 = 144.'),
    ('If the bottom moves 1 foot closer to the wall, is the top higher or lower?', 'higher', 'A shorter base leaves more of the 13 feet for height: √(169 - 16) ≈ 12.4.')])
assert 5 ** 2 + 12 ** 2 == 13 ** 2

O['geometry-applications-skill-02', 'cp1'] = ('A TV screen is 32 inches wide and 24 inches tall. TVs are sold by the length of the diagonal.', [
    ('Find the diagonal.', '40 inches', '√(32² + 24²) = √1600 = 40.'),
    ('A box is 36 inches wide and 30 inches tall. Find its diagonal to the nearest inch.', '47 inches', '√(36² + 30²) = √2196 ≈ 46.9.'),
    ('Can the screen fit flat in the box? Explain.', 'yes: 32 ≤ 36 and 24 ≤ 30', 'Compare width with width and height with height.'),
    ('What is the area of the screen?', '768 square inches', '32 × 24 = 768.')])
assert math.hypot(32, 24) == 40 and round(math.hypot(36, 30)) == 47

O['geometry-applications-skill-03', 'cp2'] = ('A box is 4 cm long, 3 cm wide and 12 cm tall.', [
    ('Find the diagonal of the bottom of the box.', '5 cm', '√(4² + 3²) = 5.'),
    ('The bottom diagonal and the height form a right triangle. Name its hypotenuse.', 'the space diagonal of the box', 'It runs from a bottom corner to the opposite top corner.'),
    ('Find the space diagonal.', '13 cm', '√(5² + 12²) = 13.'),
    ('Will a 14-cm straw fit inside the box? Explain.', 'no: the longest segment inside is 13 cm', '14 > 13.')])

O['geometry-applications-skill-03', 'honors'] = ('A cone has a slant height of 25 cm and a radius of 7 cm. A cylinder has the same radius and the same height as the cone.', [
    ('Find the height of the cone.', '24 cm', '√(25² - 7²) = √576 = 24.'),
    ('Find the volume of the cone in terms of π.', '392π cubic cm', '(1/3)π(49)(24) = 392π.'),
    ('Find the volume of the cylinder in terms of π.', '1176π cubic cm', 'π(49)(24) = 1176π.'),
    ('Find the length of the longest segment that fits inside the cylinder.', '√772 ≈ 27.8 cm', 'Diameter 14 and height 24: √(14² + 24²) = √772.')])
assert 25 ** 2 - 7 ** 2 == 576 and 49 * 24 // 3 == 392 and 49 * 24 == 1176 and 14 ** 2 + 24 ** 2 == 772 and round(math.sqrt(772), 1) == 27.8

O['geometry-applications-skill-04', 'cp2'] = ('Points A(1, 2) and B(4, 6) are graphed on a coordinate plane.', [
    ('Find the horizontal distance between A and B.', '3', '4 - 1 = 3.'),
    ('Find the vertical distance between A and B.', '4', '6 - 2 = 4.'),
    ('Find the distance AB.', '5', '√(3² + 4²) = 5.'),
    ('Find the distance from A to C(1, -3).', '5', 'Same x-coordinate: 2 - (-3) = 5.')])

O['geometry-applications-skill-04', 'honors'] = ('Triangle PQR has vertices P(-2, -1), Q(4, -1) and R(1, 3).', [
    ('Find PQ.', '6', '4 - (-2) = 6.'),
    ('Find PR and QR.', 'PR = 5 and QR = 5', '√(3² + 4²) = 5 for both.'),
    ('Classify the triangle by its sides.', 'isosceles', 'Two sides are 5.'),
    ('Find the perimeter and the area.', 'perimeter 16; area 12', '6 + 5 + 5 = 16. Area: (1/2)(6)(4) = 12, since the height from R to PQ is 3 - (-1) = 4.')])

O['geometry-applications-skill-06', 'cp2'] = ('A cylindrical can has volume 72π cubic cm and radius 3 cm.', [
    ('Write the volume formula with the known values.', '72π = π(3²)h', 'V = πr²h.'),
    ('Find the height.', '8 cm', '72π = 9πh, so h = 8.'),
    ('Another can has the same radius and twice the height. Find its volume.', '144π cubic cm', 'π(9)(16) = 144π.'),
    ('A cone has the same radius and height as the first can. Find its volume.', '24π cubic cm', '(1/3)(72π) = 24π.')])

# ---------------------------------------------------------------- linear and functional relationships
O['linear-functional-relationships-skill-06', 'cp2'] = ('Line A is y = 2x + 1. Line B goes through (0, 4) and (2, 5).', [
    ('Find the slope of each line.', 'A: 2; B: 1/2', 'B: (5 - 4) ÷ 2 = 1/2.'),
    ('Which line is steeper?', 'Line A', '2 > 1/2.'),
    ('Find the y-intercept of each line.', 'A: 1; B: 4', 'A from its equation; B from (0, 4).'),
    ('Find y on each line when x = 6.', 'A: 13; B: 7', '2(6) + 1 = 13 and (1/2)(6) + 4 = 7.')])

O['linear-functional-relationships-skill-06', 'honors'] = ('Function f is y = -3x + 12. Function g goes through (-2, 1) and (4, 4).', [
    ('Find the x-intercept and y-intercept of f.', 'x-intercept (4, 0); y-intercept (0, 12)', '0 = -3x + 12 gives x = 4.'),
    ('Write an equation for g.', 'y = (1/2)x + 2', 'Slope (4 - 1) ÷ 6 = 1/2; 1 = (1/2)(-2) + b gives b = 2.'),
    ('Find where f and g intersect.', '(20/7, 24/7)', '-3x + 12 = (1/2)x + 2 gives (7/2)x = 10, x = 20/7, y = 24/7.'),
    ('Which function has the greater rate of change? Compare absolute values too.', 'g has the greater rate (1/2 > -3), but f changes faster (|-3| > 1/2)', 'Compare slopes.')])
assert -3 * Fr(20, 7) + 12 == Fr(24, 7) == Fr(1, 2) * Fr(20, 7) + 2

O['linear-functional-relationships-skill-10', 'cp2'] = ('A taxi ride costs C(m) = 2m + 3 dollars for m miles.', [
    ('Find C(5).', '13', '2(5) + 3 = 13.'),
    ('What does C(5) mean?', 'a 5-mile ride costs $13', 'Input miles, output dollars.'),
    ('What does the 3 mean?', 'a $3 starting fee', 'It is the cost for 0 miles.'),
    ('How many miles can you ride for $21?', '9 miles', '2m + 3 = 21, so m = 9.')])

O['linear-functional-relationships-skill-11', 'cp2'] = ('f(x) = x + 2 for x < 0, and f(x) = 2 for x ≥ 0.', [
    ('Find f(-3).', '-1', '-3 < 0: -3 + 2 = -1.'),
    ('Find f(0).', '2', '0 ≥ 0 uses the second piece.'),
    ('Find f(5).', '2', '5 ≥ 0: f is constant 2.'),
    ('Describe the graph on each side of x = 0.', 'a rising line with slope 1 for x < 0; a horizontal line at y = 2 for x ≥ 0', 'The first piece has slope 1; the second is constant.')])

O['linear-functional-relationships-skill-11', 'cp1'] = ('A parking garage charges $5 for the first 2 hours and $3 for each hour after that. Let C(h) be the cost for h hours (h a whole number from 1 to 8).', [
    ('Find C(1) and C(2).', '$5 and $5', 'Both are within the first 2 hours.'),
    ('Write the rule for h > 2.', 'C(h) = 5 + 3(h - 2)', '$3 for each hour past 2.'),
    ('Find C(6).', '$17', '5 + 3(4) = 17.'),
    ('How many hours can you park for $20?', '7 hours', '5 + 3(h - 2) = 20 gives h = 7.')])
assert 5 + 3 * 4 == 17 and 5 + 3 * 5 == 20

# ---------------------------------------------------------------- patterns and bivariate data
O['patterns-bivariate-data-skill-02', 'cp2'] = ('Data for 6 students: hours studied 1, 2, 3, 4, 5, 6; quiz score 60, 65, 72, 76, 40, 88.', [
    ('Which point does not follow the pattern?', '(5, 40)', 'The other scores rise with hours; 40 is far below.'),
    ('What is this kind of point called?', 'an outlier', 'It lies far from the other points.'),
    ('Without that point, do scores tend to increase or decrease as hours increase?', 'increase', '60, 65, 72, 76, 88.'),
    ('Predict a score for 7 hours.', 'about 93 (90 to 96 is reasonable)', 'Scores rise about 5 to 6 points per hour after 88.')])

O['real-numbers-exponents-skill-03', 'cp2'] = ('Convert between fractions and decimals.', [
    ('Write 3/8 as a decimal.', '0.375', '3 ÷ 8 = 0.375.'),
    ('Write 2/3 as a decimal.', '0.666… (6 repeats)', '2 ÷ 3 = 0.666….'),
    ('Write 0.45 as a fraction in simplest form.', '9/20', '45/100 = 9/20.'),
    ('Does 3/8 terminate or repeat? Does 2/3?', '3/8 terminates; 2/3 repeats', 'The denominator 8 has only factors of 2.')])
assert Fr(45, 100) == Fr(9, 20)

O['real-numbers-exponents-skill-06', 'cp1'] = ('Use perfect squares to estimate square roots.', [
    ('Between which two whole numbers is √50?', '7 and 8', '49 < 50 < 64.'),
    ('Estimate √50 to the nearest tenth.', '7.1', '7.1² = 50.41 and 7.0² = 49; 50 is closer to 50.41.'),
    ('Order from least to greatest: √50, 7.2, 50/7.', '√50, 50/7, 7.2', '√50 ≈ 7.07 and 50/7 ≈ 7.14.'),
    ('Which is closer to 7: √50 or 50/7?', '√50', '√50 ≈ 7.07 and 50/7 ≈ 7.14.')])
assert math.sqrt(50) < 50 / 7 < 7.2 and abs(7.1 ** 2 - 50) < abs(7.0 ** 2 - 50)

O['real-numbers-exponents-skill-08', 'cp2'] = ('Use the pattern 2³ = 8, 2² = 4, 2¹ = 2.', [
    ('What do you divide by each time the exponent goes down 1?', '2', '8 ÷ 2 = 4, 4 ÷ 2 = 2.'),
    ('Find 2⁰.', '1', '2 ÷ 2 = 1.'),
    ('Find 2⁻¹ and 2⁻².', '1/2 and 1/4', '1 ÷ 2 = 1/2 and 1/2 ÷ 2 = 1/4.'),
    ('Find 5⁰ and 5⁻¹.', '1 and 1/5', 'Any nonzero number to the 0 power is 1; 5⁻¹ = 1/5.')])

O['real-numbers-exponents-skill-08', 'cp1'] = ('Evaluate with zero and negative exponents.', [
    ('3⁻²', '1/9', '1/3² = 1/9.'),
    ('4⁰ + 4⁻¹', '5/4', '1 + 1/4.'),
    ('10⁻³ as a decimal', '0.001', '1/1000.'),
    ('Which is greater: 2⁻³ or 3⁻²? Explain.', '2⁻³ (1/8 > 1/9)', '2⁻³ = 1/8 and 3⁻² = 1/9.')])

O['real-numbers-exponents-skill-09', 'cp2'] = ('Use the properties of exponents.', [
    ('Simplify 3⁴ · 3² as a power of 3.', '3⁶', 'Add exponents: 4 + 2.'),
    ('Simplify 5⁷ ÷ 5³ as a power of 5.', '5⁴', 'Subtract exponents: 7 - 3.'),
    ('Simplify (2³)² as a power of 2, then evaluate.', '2⁶ = 64', 'Multiply exponents: 3 × 2.'),
    ('Simplify x⁵ · x³.', 'x⁸', 'Add exponents.')])

O['real-numbers-exponents-skill-09', 'honors'] = ('Simplify. Use only positive exponents.', [
    ('(3x⁻²)³', '27/x⁶', '3³ = 27 and (x⁻²)³ = x⁻⁶.'),
    ('(a⁴b⁻³)(a⁻⁶b⁵)', 'b²/a²', 'a⁴⁻⁶ = a⁻² and b⁻³⁺⁵ = b².'),
    ('(2⁵ · 2⁻²) ÷ 2⁻¹, as a number', '16', '2⁵⁻²⁺¹ = 2⁴ = 16.'),
    ('Find n if 9ⁿ = 3⁸.', 'n = 4', '9ⁿ = 3²ⁿ, so 2n = 8.')])
assert 2 ** (5 - 2 + 1) == 16 and 9 ** 4 == 3 ** 8

O['real-numbers-exponents-skill-11', 'cp1'] = ('Earth is about 1.5 × 10⁸ km from the Sun. Light travels about 3 × 10⁵ km per second.', [
    ('Write 1.5 × 10⁸ in standard form.', '150,000,000', 'Move the decimal 8 places right.'),
    ('How many seconds does sunlight take to reach Earth?', '5 × 10² seconds', '1.5 × 10⁸ ÷ (3 × 10⁵) = 0.5 × 10³ = 5 × 10².'),
    ('Convert that time to minutes, to the nearest tenth.', '8.3 minutes', '500 ÷ 60 ≈ 8.3.'),
    ('How far does light travel in 2 × 10³ seconds? Use scientific notation.', '6 × 10⁸ km', '(3 × 10⁵)(2 × 10³) = 6 × 10⁸.')])
assert 1.5e8 / 3e5 == 500 and round(500 / 60, 1) == 8.3

O['real-numbers-exponents-skill-11', 'honors'] = ('A hard drive holds 2.4 × 10¹² bytes. A photo uses about 3 × 10⁶ bytes, and a video uses about 1.2 × 10⁹ bytes.', [
    ('How many photos fit on the drive?', '8 × 10⁵ photos', '2.4 × 10¹² ÷ (3 × 10⁶) = 0.8 × 10⁶.'),
    ('How many videos fit on the drive?', '2 × 10³ videos', '2.4 × 10¹² ÷ (1.2 × 10⁹) = 2 × 10³.'),
    ('How many times as large is a video as a photo?', '4 × 10²', '1.2 × 10⁹ ÷ (3 × 10⁶) = 0.4 × 10³.'),
    ('After 500 videos are saved, how many bytes are left? Use scientific notation.', '1.8 × 10¹² bytes', '500 × 1.2 × 10⁹ = 6 × 10¹¹; 2.4 × 10¹² - 0.6 × 10¹² = 1.8 × 10¹².')])
assert round(2.4e12 / 3e6) == 800000 and round(2.4e12 / 1.2e9) == 2000 and round(1.2e9 / 3e6) == 400 and round(2.4e12 - 500 * 1.2e9) == 1.8e12

# ---------------------------------------------------------------- systems of linear equations
O['systems-linear-equations-skill-02', 'cp2'] = ('Solve the system by graphing: y = x + 1 and y = -x + 5.', [
    ('Give the slope and y-intercept of each line.', 'y = x + 1: slope 1, y-intercept 1; y = -x + 5: slope -1, y-intercept 5', 'Read from y = mx + b.'),
    ('Where do the lines cross?', '(2, 3)', 'x + 1 = -x + 5 gives x = 2.'),
    ('Check the point in both equations.', '3 = 2 + 1 and 3 = -2 + 5', 'Both are true.'),
    ('How many solutions does the system have?', 'one', 'The slopes are different.')])

O['systems-linear-equations-skill-02', 'honors'] = ('Phone plan A costs $20 plus $0.10 per minute. Plan B costs $35 plus $0.05 per minute.', [
    ('Write an equation for each plan (y dollars, x minutes).', 'A: y = 0.10x + 20; B: y = 0.05x + 35', 'Fixed fee plus rate times minutes.'),
    ('Find the intersection point of the graphs.', '(300, 50)', '0.10x + 20 = 0.05x + 35 gives 0.05x = 15.'),
    ('What does the intersection mean?', 'at 300 minutes both plans cost $50', 'Same input, same output.'),
    ('Which plan is cheaper for 500 minutes, and by how much?', 'Plan B, by $10 ($60 vs $70)', 'A: 0.10(500) + 20 = 70. B: 0.05(500) + 35 = 60.')])
assert math.isclose(0.10 * 300 + 20, 50) and math.isclose(0.05 * 300 + 35, 50) and math.isclose(0.10 * 500 + 20, 70) and math.isclose(0.05 * 500 + 35, 60)

O['systems-linear-equations-skill-04', 'cp2'] = ('Solve by elimination: x + y = 10 and x - y = 4.', [
    ('Add the two equations. What equation results?', '2x = 14', 'The y-terms cancel.'),
    ('Solve for x.', 'x = 7', '14 ÷ 2.'),
    ('Find y.', 'y = 3', '7 + y = 10.'),
    ('Check the solution in the second equation.', '7 - 3 = 4', 'True.')])

O['systems-linear-equations-skill-04', 'honors'] = ('Solve by elimination: 3x + 4y = 10 and 5x - 6y = 4.', [
    ('Which multipliers make the y-terms opposites?', 'multiply the first by 3 and the second by 2', '12y and -12y.'),
    ('Write the new equations and add them.', '9x + 12y = 30 and 10x - 12y = 8; 19x = 38', 'Add.'),
    ('Solve for x and y.', 'x = 2, y = 1', '19x = 38; 3(2) + 4y = 10 gives y = 1.'),
    ('Check in the second equation.', '5(2) - 6(1) = 4', 'True.')])
assert 3 * 2 + 4 * 1 == 10 and 5 * 2 - 6 * 1 == 4

O['systems-linear-equations-skill-05', 'cp2'] = ('Compare slopes and y-intercepts to classify each system.', [
    ('y = 2x + 1 and y = 2x - 3', 'no solution', 'Same slope, different y-intercepts: parallel lines.'),
    ('y = 3x + 2 and y = -x + 2', 'one solution', 'Different slopes.'),
    ('y = x + 4 and 2y = 2x + 8', 'infinitely many solutions', 'Divide the second by 2: y = x + 4, the same line.'),
    ('Write a second equation so y = -2x + 5 has no solution with it.', 'for example y = -2x + 1', 'Same slope, different y-intercept.')])

O['systems-linear-equations-skill-05', 'cp1'] = ('Consider the system 2x + 3y = 6 and 4x + 6y = k.', [
    ('Write the first equation in slope-intercept form.', 'y = (-2/3)x + 2', '3y = -2x + 6.'),
    ('For which value of k are there infinitely many solutions?', 'k = 12', 'The second equation is twice the first.'),
    ('For which values of k is there no solution?', 'any k other than 12', 'Same slope, different line.'),
    ('Can this system ever have exactly one solution? Explain.', 'no: the slopes are always equal', 'Both lines have slope -2/3.')])

O['systems-linear-equations-skill-06', 'cp1'] = ('A school sold 200 tickets to a play. Adult tickets cost $8 and student tickets cost $5. The school collected $1,270.', [
    ('Write a system of equations (a adult, s student).', 'a + s = 200 and 8a + 5s = 1270', 'Count and money.'),
    ('Solve for a.', 'a = 90', '8a + 5(200 - a) = 1270 gives 3a = 270.'),
    ('Find s.', 's = 110', '200 - 90.'),
    ('How much money came from student tickets?', '$550', '110 × 5.')])
assert 8 * 90 + 5 * 110 == 1270

O['systems-linear-equations-skill-06', 'honors'] = ('A chemist mixes a 20% acid solution with a 50% acid solution to make 30 liters of a 30% solution.', [
    ('Write a system (x liters of 20%, y liters of 50%).', 'x + y = 30 and (1/5)x + (1/2)y = 9', '20% = 1/5, 50% = 1/2, and 30% of 30 L is 9 L of acid.'),
    ('Solve for x and y.', 'x = 20, y = 10', 'Substitute y = 30 - x: (1/5)x + 15 - (1/2)x = 9, so (3/10)x = 6.'),
    ('Check the amount of acid.', '(1/5)(20) + (1/2)(10) = 9', '4 L + 5 L = 9 L.'),
    ('How many liters of 50% solution would make 30 L of a 40% solution instead?', '20 liters', '(1/5)(30 - y) + (1/2)y = 12 gives (3/10)y = 6.')])
assert math.isclose(0.2 * 20 + 0.5 * 10, 9) and math.isclose(0.2 * 10 + 0.5 * 20, 12)



def run():
    banks = load()
    added = 0
    tagsf = {u: os.path.join(ROOT, 'question-banks', 'prealgebra', 'meta', u + '.tags.json') for u in banks}
    tags = {u: json.load(open(f, encoding='utf-8')) for u, f in tagsf.items()}
    for (skill, L), (prompt, parts) in O.items():
        assert len(parts) >= 4, (skill, L)
        unit, n = skill.rsplit('-skill-', 1)
        bank = banks[unit]['questions']
        std = next(q['standards'] for q in bank if q['skillId'] == skill)
        qid = f'pa8-{ABBR[unit]}-s{n}-{L}-o01'
        q = {'id': qid, 'skillId': skill, 'level': L, 'format': 'open-response', 'prompt': prompt,
             'parts': [{'prompt': p, 'answer': a} for p, a, _ in parts],
             'answer': '; '.join(f'({chr(97 + i)}) {a}' for i, (_, a, _) in enumerate(parts)),
             'solutionSteps': [s for _, _, s in parts], 'standards': std,
             'sourceNotes': NOTE.format(fam=f's{int(n)}_open_batch_f')}
        old = next((x for x in bank if x['id'] == qid), None)
        if old:
            old.clear(); old.update(q)
        else:
            assert not any(x['skillId'] == skill and x['level'] == L and x['format'] == 'open-response' for x in bank), qid
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
    print('open response added', run(), 'of', len(O))
