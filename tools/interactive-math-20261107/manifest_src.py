# Source of manifest.json (python for readability). Run: python3 manifest_src.py
import json
T = []
def tool(slug, course, unit, unitName, title, intro, description, topics, discovery, also=None):
    d = dict(slug=slug, course=course, unit=unit, unitName=unitName, title=title, intro=intro, description=description, topics=topics, discovery=discovery)
    if also: d['also'] = also
    T.append(d)
tool('math6-ratio-double-number-line', 'math6', 'ratios-rates-percent-proportions', 'Ratios, Rate, Percent and Proportions',
     'Double Number Line Ratio Explorer',
     'Slide the marker along the double number line. Watch how the two amounts change together, then test pairs to see which ones make the same ratio.',
     'Slide a marker along a double number line linked to a ratio table and a graph. Find both unit rates, test pairs for equivalence, and see why adding the same amount to both parts changes the ratio.',
     ['Equivalent ratios', 'Unit rate', 'Double number lines'],
     'Equivalent ratios come from multiplying both amounts by the same number, so the unit rate stays the same and every equivalent pair lies on one line through (0, 0).')
tool('math6-fraction-division-groups', 'math6', 'fractions-decimals-operations', 'Operations of Fractions and Decimals',
     'Fraction Division: How Many Groups?',
     'Division asks how many groups of one size fit into an amount. Build the groups, then look closely at what is left over.',
     'Model a ÷ b as “how many groups of b fit in a?” with bars cut into equal pieces. See full and partial groups, why dividing by a fraction less than 1 gives a bigger answer, and where “multiply by the reciprocal” comes from.',
     ['Dividing fractions', 'Measurement division', 'Reciprocals'],
     'a ÷ d counts how many groups of size d fit in a; the leftover is a fraction of a group, and cutting both into equal pieces shows a ÷ (n/m) = a × (m/n).')
tool('math6-area-shear-lab', 'math6', 'geometry', 'Geometry',
     'Parallelogram & Triangle Area Lab',
     'Lean a parallelogram or a triangle on the grid. Some things change and some don’t: watch which ones decide the area.',
     'Drag the top of a parallelogram or triangle to lean it, cut and slide it into a rectangle, and copy a triangle into a parallelogram to see why area depends on base and height, not on slanted sides.',
     ['Area of parallelograms', 'Area of triangles', 'Base and height'],
     'Leaning a shape keeps its base and height, so its area stays the same; a parallelogram rearranges into a rectangle, and a triangle is half of a parallelogram with the same base and height.')
tool('math6-balance-point-dot-plot', 'math6', 'data-displays', 'Data Displays',
     'Dot Plot Balance: Mean, Median & Spread',
     'Drag the dots on the dot plot. The triangle under the line is the balance point. Find out what moves it and what moves the median.',
     'Drag data values on a dot plot and watch the mean balance point, the median, the range, IQR and MAD respond. See how outliers pull the mean and why distances on each side of the mean balance.',
     ['Mean and median', 'Mean absolute deviation', 'Outliers'],
     'The mean is the balance point (distances below it equal distances above it), the median depends only on order, and MAD measures the typical distance from the mean.')
tool('prealgebra7-proportional-relationships', 'prealgebra7', 'linear-functions-graphing', 'Linear Functions and Graphing',
     'Proportional Relationship Explorer',
     'Trail mix costs the same amount per pound. Change the price, add a bag fee, and drag a point on the graph to test whether the relationship is still proportional.',
     'Link a price context, a table, a graph and an equation. Find the constant of proportionality, see why y = kx passes through (0, 0), and discover why a straight line with a starting fee is not proportional.',
     ['Constant of proportionality', 'y = kx', 'Proportional vs. non-proportional'],
     'A relationship is proportional when y/x is the same for every pair: its graph is a line through (0, 0) and its equation is y = kx; a straight line with a starting value is not proportional.')
tool('prealgebra7-percent-change-bar', 'prealgebra7', 'ratios-proportions-percentages', 'Ratios, Proportions, and Percentages',
     'Percent Change Bar Model',
     'Each bar is split into 10% sections of the amount it starts from. Apply a markup or a discount, then a second change, and watch what each percent is a percent of.',
     'Model markups, discounts, tax and two changes in a row with percent bars on one dollar scale. See why +20% then −20% does not return to the start and why percent changes multiply instead of add.',
     ['Percent of change', 'Markup and discount', 'Successive percent changes'],
     'A percent change is a percent of the starting amount, so it multiplies by (100% ± p%); in a second change the base is the new amount, so changes in a row multiply rather than add.')
tool('prealgebra7-spinner-probability-lab', 'prealgebra7', 'data-analysis-probability', 'Data Analysis and Probability',
     'Spinner Probability Lab',
     'Design a spinner, find each color’s theoretical probability, then spin it 10, 100 or 1,000 times and compare.',
     'Build a spinner from equal parts, find theoretical probabilities, and compare them with experimental results as the number of spins grows. Use expected counts and see that the spinner has no memory.',
     ['Theoretical probability', 'Experimental probability', 'Expected value'],
     'Theoretical probability is parts ÷ total parts; experimental shares vary a lot in small samples and settle near the theoretical value as the number of spins grows, and each spin is independent.')
tool('prealgebra-pythagorean-squares', 'prealgebra', 'geometry-applications', 'Geometry',
     'Pythagorean Squares Explorer',
     'Drag the corners of a triangle on the grid. A square sits on each side. When do the two smaller squares exactly fill the biggest one?',
     'Drag a triangle on a grid with a square on each side. Compare a² + b² with c² for right, acute and obtuse triangles, use the converse, and find the area of a tilted square without measuring its side.',
     ['Pythagorean theorem', 'Converse of the Pythagorean theorem', 'Square roots'],
     'In a right triangle the two smaller squares have the same total area as the square on the hypotenuse (a² + b² = c²), and only right triangles do: a² + b² > c² means acute, < means obtuse.',
     also=[['prealgebra7', 'right-triangles-algebra']])
tool('prealgebra-square-roots-number-line', 'prealgebra', 'real-numbers-exponents', 'Real Numbers and Exponents',
     'Square Roots on the Number Line',
     'A square of area A has side √A. Trap the side between two numbers by squaring them, then zoom in one decimal place at a time.',
     'Link a square’s area to its side length, trap √A between neighbors by squaring, zoom to tenths, hundredths and thousandths, and test your own estimates. Compare perfect squares with irrational square roots.',
     ['Square roots', 'Estimating irrational numbers', 'Rational vs. irrational'],
     'To place √A, find numbers whose squares trap A and refine one place value at a time; perfect squares stop with an exact whole number, while other square roots are irrational, so every decimal shown is an approximation.')
tool('precalculus-vector-explorer', 'precalculus', 'vectors', 'Vectors',
     'Vector Explorer',
     'Drag the tips of u and v. Add them tip to tail, subtract them, or stretch u by a scalar, and compare the components, magnitudes and directions.',
     'Drag two vectors to see component-wise addition, tip-to-tail and parallelogram sums, u − v as u + (−v), and scalar multiples, with live components, magnitudes and direction angles.',
     ['Vector components', 'Magnitude and direction', 'Vector addition and scalar multiples'],
     'Vectors add component by component (tip to tail), but magnitudes do not add: |u + v| ≤ |u| + |v| with equality only for vectors pointing the same way; k·u scales the length by |k| and reverses direction when k < 0.')
tool('calculus-limit-explorer', 'calculus', 'limits-continuity', 'Limits and Continuity',
     'Limit Explorer',
     'Close in on x = a from the left and the right with a table and a graph. Compare what f(x) approaches with what f(a) actually is.',
     'Approach a point from both sides with tables and graphs for a hole, a moved point, a jump, a vertical asymptote, an oscillation and a continuous function. Set f(a) separately to see that the limit does not depend on it.',
     ['One-sided limits', 'Limit vs. function value', 'Types of discontinuity'],
     'A limit describes the values of f near a, not at a: it exists only when both one-sided limits agree, f(a) can differ from it, and tables or zooming are evidence rather than proof.')
tool('calculus-secant-to-tangent', 'calculus', 'derivatives', 'Derivatives',
     'Secant to Tangent',
     'A secant line joins two points on a graph. Slide the second point closer from either side and watch the secant slopes, then build the slope graph f′.',
     'Shrink h from both sides to watch secant slopes approach the tangent slope, see why |x| has no derivative at 0, and trace the tangent slopes into the graph of the derivative.',
     ['Difference quotient', 'Tangent line slope', 'Graph of the derivative'],
     'The derivative is the limit of secant slopes as h → 0 from both sides; when the one-sided limits differ (a corner) there is no derivative, and the tangent slopes at every point form the graph of f′.')
tool('calculus-riemann-sum-lab', 'calculus', 'antiderivatives-definite-integrals', 'Antiderivatives and Definite Integrals',
     'Riemann Sum Lab',
     'Cover the region under a curve with rectangles. Change the number of rectangles, where they sample the curve, and the interval, then compare the sum with the exact integral.',
     'Build left, right, midpoint and trapezoid sums with up to 100 subintervals, compare them with the exact definite integral, and see how areas below the axis make the integral signed area rather than total area.',
     ['Riemann sums', 'Definite integral as a limit', 'Signed vs. total area'],
     'Riemann sums approach the definite integral as n grows; rectangles below the x-axis count as negative, so the integral is signed area, and left/right sums under- or overestimate depending on whether f increases or decreases.')
tool('calculus-accumulation-ftc', 'calculus', 'fundamental-theorem-calculus', 'The Fundamental Theorem of Calculus',
     'Accumulation Function Explorer',
     'Slide x to the right and watch the signed area pile up. The bottom graph records that area as A(x). Compare the slope of A with the height of f.',
     'Drag the upper limit of an accumulation function and watch A(x) = ∫ f(t) dt build up from signed area. See that the slope of A equals f(x), where A has maximums and minimums, and what changing the lower limit does.',
     ['Accumulation functions', 'Fundamental Theorem of Calculus', 'Signed area'],
     'The accumulation function A(x) = ∫ from a to x of f(t) dt increases where f > 0 and decreases where f < 0, and its slope is exactly f(x) (A′ = f); changing a shifts A by a constant.')
json.dump({'version': '20261107', 'labVersion': '20261105', 'tools': T}, open('manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(T), 'tools in manifest')
