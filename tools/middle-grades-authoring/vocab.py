"""Flashcard/vocabulary entries for Grade 7 (prealgebra7) and Grade 6 (math6), in the site's MKVOCAB_BANKS format:
"term|definition|example" rows joined by ';'. Math in ⟨…⟩ uses the same TeX subset as worksheet-generator/vocabulary-data.js.
Writes worksheet-generator/vocabulary-data-middle-grades.js (loaded after vocabulary-data.js)."""
import json, os, sys

G7 = {
 "algebraic-expressions-integers": [
  ("place value", "The value of a digit based on its position in a number.", "In 4,582, the 5 is worth 500"),
  ("variable", "A letter that stands for an unknown or changing number.", "n in n + 7"),
  ("algebraic expression", "Numbers, variables, and operations with no equals sign.", "3x - 5"),
  ("order of operations", "Grouping symbols, exponents, multiply and divide left to right, add and subtract left to right.", "⟨2 + 3 \\times 4 = 14⟩"),
  ("integer", "A whole number or its opposite.", "-8, 0, 15"),
  ("absolute value", "The distance of a number from 0 on a number line.", "The absolute value of -6 is 6"),
  ("opposites", "Two numbers the same distance from 0 on opposite sides.", "7 and -7"),
  ("inductive reasoning", "Making a conjecture from a pattern of examples.", "2, 4, 6, 8 → next is 10"),
  ("counterexample", "One example that shows a statement is false.", "⟨-2 + (-3)⟩ is less than both numbers"),
  ("coordinate plane", "A plane formed by a horizontal x-axis and a vertical y-axis.", "Point (3, -2) is in Quadrant IV"),
  ("ordered pair", "A pair (x, y) that gives the location of a point.", "(-4, 5)"),
  ("quadrant", "One of the four regions of the coordinate plane.", "Quadrant II has x < 0 and y > 0")],
 "one-step-equations-inequalities": [
  ("commutative property", "Changing the order does not change a sum or product.", "⟨a + b = b + a⟩"),
  ("associative property", "Changing the grouping does not change a sum or product.", "⟨(ab)c = a(bc)⟩"),
  ("identity property", "Adding 0 or multiplying by 1 leaves a number unchanged.", "⟨7 \\times 1 = 7⟩"),
  ("distributive property", "Multiply a number by each term inside parentheses.", "⟨3(x + 4) = 3x + 12⟩"),
  ("like terms", "Terms with the same variable raised to the same power.", "5x and -2x"),
  ("equation", "A statement that two expressions are equal.", "x + 9 = 15"),
  ("inverse operations", "Operations that undo each other.", "Addition and subtraction"),
  ("solution", "A value that makes an equation or inequality true.", "x = 6 for x + 9 = 15"),
  ("inequality", "A statement that compares two expressions using <, >, ≤, ≥, or ≠.", "x ≥ 18"),
  ("closed circle", "On a number line, shows the endpoint is included (≤ or ≥).", "x ≤ 3"),
  ("open circle", "On a number line, shows the endpoint is not included (< or >).", "x > -2")],
 "decimals-equations": [
  ("rounding", "Replacing a number with a nearby number to a given place.", "3.476 ≈ 3.48"),
  ("estimate", "An approximate answer found with rounded or compatible numbers.", "19.8 × 5.1 ≈ 100"),
  ("compatible numbers", "Numbers that are easy to compute mentally.", "⟨62 \\div 9 \\approx 63 \\div 9 = 7⟩"),
  ("mean", "The sum of the data divided by the number of values.", "Mean of 2, 4, 9 is 5"),
  ("median", "The middle value of ordered data (average the two middle values if needed).", "Median of 2, 4, 9 is 4"),
  ("mode", "The value that occurs most often.", "Mode of 3, 5, 5, 8 is 5"),
  ("outlier", "A value much greater or less than the rest of the data.", "95 in 12, 14, 15, 95"),
  ("formula", "An equation that shows a relationship between quantities.", "d = rt"),
  ("metric system", "A base-10 system of measurement (meter, gram, liter).", "1 km = 1,000 m")],
 "factors-fractions-exponents": [
  ("factor", "A whole number that divides another with no remainder.", "4 is a factor of 12"),
  ("prime number", "A whole number greater than 1 with exactly two factors.", "13"),
  ("composite number", "A whole number greater than 1 with more than two factors.", "15"),
  ("prime factorization", "A number written as a product of primes.", "⟨60 = 2^2 \\cdot 3 \\cdot 5⟩"),
  ("greatest common factor (GCF)", "The greatest factor two or more numbers share.", "GCF of 18 and 24 is 6"),
  ("simplest form", "A fraction whose numerator and denominator have GCF 1.", "⟨\\tfrac{6}{8} = \\tfrac{3}{4}⟩"),
  ("exponent", "Tells how many times the base is used as a factor.", "⟨2^5 = 32⟩"),
  ("rational number", "A number that can be written as ⟨\\tfrac{a}{b}⟩ with integers a and b, b ≠ 0.", "-0.75"),
  ("irrational number", "A number whose decimal never ends and never repeats.", "⟨\\sqrt{2},\\ \\pi⟩"),
  ("scientific notation", "A number written as a × 10ⁿ with 1 ≤ a < 10.", "⟨3.2 \\times 10^5⟩"),
  ("cube root", "A number that, used as a factor three times, gives the original number.", "⟨\\sqrt[3]{64} = 4⟩")],
 "operations-fractions": [
  ("least common denominator (LCD)", "The least common multiple of the denominators.", "LCD of ⟨\\tfrac{1}{4}⟩ and ⟨\\tfrac{1}{6}⟩ is 12"),
  ("equivalent fractions", "Fractions that name the same amount.", "⟨\\tfrac{2}{3} = \\tfrac{8}{12}⟩"),
  ("mixed number", "A whole number and a fraction.", "⟨3\\tfrac{1}{2}⟩"),
  ("improper fraction", "A fraction whose numerator is greater than or equal to its denominator.", "⟨\\tfrac{7}{2}⟩"),
  ("reciprocal", "Two numbers whose product is 1.", "⟨\\tfrac{3}{4}⟩ and ⟨\\tfrac{4}{3}⟩"),
  ("terminating decimal", "A decimal that ends.", "⟨\\tfrac{3}{8} = 0.375⟩"),
  ("repeating decimal", "A decimal with a block of digits that repeats forever.", "⟨\\tfrac{1}{3} = 0.333…⟩"),
  ("customary units", "U.S. units such as inches, feet, cups, and pounds.", "12 in. = 1 ft"),
  ("power of a product", "Raise each factor to the power.", "⟨(2x)^3 = 8x^3⟩")],
 "ratios-proportions-percentages": [
  ("ratio", "A comparison of two quantities by division.", "3 : 5"),
  ("rate", "A ratio comparing quantities with different units.", "120 miles in 2 hours"),
  ("unit rate", "A rate with a denominator of 1.", "60 miles per hour"),
  ("proportion", "An equation stating that two ratios are equal.", "⟨\\tfrac{2}{3} = \\tfrac{8}{12}⟩"),
  ("scale", "The ratio of a drawing length to the actual length.", "1 in. : 10 ft"),
  ("similar figures", "Figures with the same shape whose corresponding sides are proportional.", "A 3-4-5 and a 6-8-10 triangle"),
  ("percent", "A ratio that compares a number to 100.", "35% = ⟨\\tfrac{35}{100}⟩"),
  ("percent of change", "Amount of change divided by the original amount, as a percent.", "40 to 50 is a 25% increase"),
  ("markup", "An increase from the cost to the selling price.", "$20 cost, 50% markup → $30"),
  ("discount", "A decrease from the original price.", "25% off $40 → $30"),
  ("probability", "The ratio of favorable outcomes to possible outcomes.", "P(heads) = ⟨\\tfrac{1}{2}⟩")],
 "solving-equations-inequalities": [
  ("two-step equation", "An equation that needs two inverse operations to solve.", "3x + 5 = 20"),
  ("multi-step equation", "An equation that needs several steps, such as distributing and combining like terms.", "2(x + 3) + x = 21"),
  ("variables on both sides", "Collect the variable terms on one side first.", "5x - 2 = 3x + 8"),
  ("identity", "An equation true for every value of the variable.", "2(x + 1) = 2x + 2"),
  ("no solution", "An equation that is never true.", "x + 3 = x + 5"),
  ("reverse the inequality", "Multiplying or dividing both sides by a negative number reverses the inequality sign.", "-2x < 6 → x > -3"),
  ("literal equation", "An equation with two or more variables, such as a formula.", "P = 2l + 2w"),
  ("simple interest", "Interest earned only on the principal: I = prt.", "$500 at 4% for 3 years: $60"),
  ("compound interest", "Interest earned on the principal and on earlier interest.", "⟨A = P(1 + r)^t⟩")],
 "linear-functions-graphing": [
  ("relation", "A set of ordered pairs.", "{(1, 2), (3, 4)}"),
  ("function", "A relation in which each input has exactly one output.", "y = 2x + 1"),
  ("domain", "The set of input (x) values.", "{1, 3, 5}"),
  ("range", "The set of output (y) values.", "{2, 6, 10}"),
  ("slope", "Rise over run; the rate of change of a line.", "⟨m = \\tfrac{y_2 - y_1}{x_2 - x_1}⟩"),
  ("y-intercept", "The y-coordinate where a graph crosses the y-axis.", "b in y = mx + b"),
  ("slope-intercept form", "y = mx + b.", "y = -3x + 4"),
  ("scatter plot", "A graph of paired data shown as points.", "Hours studied vs. test score"),
  ("correlation", "A relationship between two data sets: positive, negative, or none.", "Age of a car and its value: negative"),
  ("system of linear equations", "Two or more linear equations with the same variables.", "y = x + 1 and y = -x + 5"),
  ("linear inequality", "An inequality whose boundary is a line; its graph is a half-plane.", "y > 2x - 1")],
 "spatial-thinking": [
  ("segment", "Part of a line with two endpoints.", "AB"),
  ("ray", "Part of a line with one endpoint that extends forever in one direction.", "Ray AB"),
  ("complementary angles", "Two angles whose measures add to 90°.", "35° and 55°"),
  ("supplementary angles", "Two angles whose measures add to 180°.", "120° and 60°"),
  ("vertical angles", "Opposite angles formed by two intersecting lines; they are congruent.", "∠1 and ∠3"),
  ("transversal", "A line that intersects two or more lines.", "A line crossing two parallel lines"),
  ("polygon", "A closed figure formed by three or more segments.", "Hexagon"),
  ("congruent", "Having the same size and shape.", "△ABC ≅ △DEF"),
  ("circumference", "The distance around a circle: C = πd.", "d = 10 → C = 10π"),
  ("translation", "A slide of every point the same distance in the same direction.", "(x, y) → (x + 3, y - 2)"),
  ("rotation", "A turn of a figure about a fixed point.", "90° about the origin: (x, y) → (-y, x)"),
  ("line of symmetry", "A line that divides a figure into two mirror-image halves.", "A square has 4")],
 "area-volume": [
  ("area", "The number of square units inside a figure.", "Rectangle 3 × 5 → 15 units²"),
  ("parallelogram area", "A = bh, using the perpendicular height.", "b = 8, h = 3 → 24"),
  ("trapezoid area", "⟨A = \\tfrac{1}{2}(b_1 + b_2)h⟩.", "bases 4 and 6, h = 5 → 25"),
  ("circle area", "⟨A = \\pi r^2⟩.", "r = 3 → 9π"),
  ("face, edge, vertex", "A flat surface, a segment where faces meet, and a corner of a solid.", "A cube has 6 faces, 12 edges, 8 vertices"),
  ("prism", "A solid with two congruent parallel bases and rectangular faces.", "Triangular prism"),
  ("surface area", "The total area of all surfaces of a solid.", "Cube with edge 2: 24 units²"),
  ("volume", "The number of cubic units inside a solid.", "V = lwh"),
  ("cylinder volume", "⟨V = \\pi r^2 h⟩.", "r = 2, h = 5 → 20π"),
  ("cone and pyramid volume", "⟨V = \\tfrac{1}{3}Bh⟩.", "One third of the matching prism or cylinder"),
  ("sphere", "⟨SA = 4\\pi r^2⟩ and ⟨V = \\tfrac{4}{3}\\pi r^3⟩.", "r = 3 → V = 36π")],
 "right-triangles-algebra": [
  ("square root", "A number that, multiplied by itself, gives the original number.", "⟨\\sqrt{49} = 7⟩"),
  ("perfect square", "The square of a whole number.", "1, 4, 9, 16, 25"),
  ("hypotenuse", "The side opposite the right angle; the longest side.", "c in ⟨a^2 + b^2 = c^2⟩"),
  ("legs", "The two sides that form the right angle.", "a and b"),
  ("Pythagorean theorem", "In a right triangle, ⟨a^2 + b^2 = c^2⟩.", "3, 4, 5"),
  ("distance formula", "⟨d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}⟩.", "(0, 0) to (3, 4): 5"),
  ("midpoint", "The point halfway between two endpoints.", "Midpoint of (2, 4) and (6, 8) is (4, 6)"),
  ("45°-45°-90° triangle", "Hypotenuse = leg × √2.", "leg 5 → hypotenuse 5√2"),
  ("30°-60°-90° triangle", "Hypotenuse = 2 × short leg; long leg = short leg × √3.", "short leg 4 → 8 and 4√3"),
  ("sine, cosine, tangent", "Opposite ÷ hypotenuse, adjacent ÷ hypotenuse, opposite ÷ adjacent.", "SOH-CAH-TOA"),
  ("angle of elevation", "The angle from the horizontal up to a line of sight.", "Looking up at a kite")],
 "data-analysis-probability": [
  ("frequency table", "A table that shows how often each value or interval occurs.", "Scores 70–79: 6"),
  ("histogram", "A bar graph of frequencies for equal intervals, with bars touching.", "Ages 10–19, 20–29, …"),
  ("box-and-whisker plot", "A display of the minimum, quartiles, median, and maximum.", "min 2, Q1 5, median 8, Q3 11, max 15"),
  ("interquartile range (IQR)", "Q3 - Q1; the spread of the middle half of the data.", "11 - 5 = 6"),
  ("stem-and-leaf plot", "A display that splits each value into a stem and a leaf.", "Stem 3 and leaf 4 means 34"),
  ("sample space", "The set of all possible outcomes.", "{H, T}"),
  ("independent events", "Events where one outcome does not affect the other.", "Rolling a cube and flipping a coin"),
  ("dependent events", "Events where the first outcome changes the probability of the second.", "Drawing without replacement"),
  ("permutation", "An arrangement where order matters.", "1st, 2nd, 3rd place"),
  ("combination", "A selection where order does not matter.", "A 3-person committee"),
  ("experimental probability", "Times the event happened ÷ number of trials.", "18 heads in 40 tosses: ⟨\\tfrac{9}{20}⟩"),
  ("random sample", "A sample in which every member of the population has an equal chance to be chosen.", "Names drawn from a hat")],
 "nonlinear-functions-polynomials": [
  ("arithmetic sequence", "A sequence with a constant difference between terms.", "5, 8, 11, 14"),
  ("geometric sequence", "A sequence with a constant ratio between terms.", "3, 6, 12, 24"),
  ("nonlinear function", "A function whose graph is not a line.", "⟨y = x^2⟩"),
  ("exponential growth", "⟨y = a(1 + r)^x⟩ with r > 0; the amount is multiplied by the same factor each period.", "Population grows 5% per year"),
  ("exponential decay", "⟨y = a(1 - r)^x⟩; the amount decreases by the same percent each period.", "A car loses 15% of its value each year"),
  ("monomial", "A number, a variable, or a product of numbers and variables.", "⟨-4x^2⟩"),
  ("polynomial", "A monomial or a sum of monomials.", "⟨3x^2 - 2x + 7⟩"),
  ("binomial / trinomial", "A polynomial with two / three terms.", "x + 5; ⟨x^2 + 3x - 4⟩"),
  ("degree of a polynomial", "The greatest degree of any of its terms.", "⟨5x^3 + x⟩ has degree 3"),
  ("FOIL", "First, Outer, Inner, Last: a way to multiply two binomials.", "⟨(x + 2)(x + 3) = x^2 + 5x + 6⟩")],
}

G6 = {}  # filled in g6 vocab section below


def bank_js(course, data):
    out = {}
    for unit, rows in data.items():
        rows = [tuple(x.replace("; ", ", ").replace(" / ", " or ") for x in row) for row in rows]
        for t, d, e in rows:
            for s in (t, d, e):
                assert "|" not in s and ";" not in s, (unit, s)
        out[f"{course}-{unit}"] = ";".join(f"{t}|{d}|{e}" for t, d, e in rows)
    return out


def write(path, courses):
    banks = {}
    for c, d in courses:
        banks.update(bank_js(c, d))
    js = ("/* Grade 6 (math6), Grade 7 (prealgebra7), Precalculus and Calculus vocabulary for flashcards and vocabulary activities.\n"
          "   Generated by tools/middle-grades-authoring/vocab.py. Load after vocabulary-data.js. */\n"
          "window.MKVOCAB_BANKS=window.MKVOCAB_BANKS||{};\nObject.assign(window.MKVOCAB_BANKS," + json.dumps(banks, ensure_ascii=False, indent=1) + ");\n")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(js)
    return {k: v.count(";") + 1 for k, v in banks.items()}


if __name__ == "__main__":
    out = sys.argv[1]
    which = sys.argv[2:] or ["prealgebra7"]
    import vocab_g6, vocab_hs
    courses = [(c, {"prealgebra7": G7, "math6": vocab_g6.G6, "precalculus": vocab_hs.PC, "calculus": vocab_hs.CA}[c]) for c in which]
    print(write(out, courses))
