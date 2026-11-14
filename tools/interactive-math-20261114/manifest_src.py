# Source of manifest.json for the 2026-11-14 Interactive Math tools (the units that had none).
# Run: cd tools/interactive-math-20261114 && python3 manifest_src.py
import json
T = []
def tool(slug, course, unit, unitName, title, intro, description, topics, discovery):
    T.append(dict(slug=slug, course=course, unit=unit, unitName=unitName, title=title, intro=intro, description=description, topics=topics, discovery=discovery))

tool('math6-rational-number-line', 'math6', 'rational-numbers', 'Rational Numbers',
     'Rational Numbers: Opposites, Absolute Value & the Plane',
     'Drag the points on the number line, then move to the coordinate plane. Watch what stays the same when a number becomes its opposite.',
     'Drag rational numbers on a number line to see opposites as reflections across 0, absolute value as distance from 0, and order. On the coordinate plane, reflect points across the axes and find distances between points that share a coordinate.',
     ['Opposites and absolute value', 'Comparing rational numbers', 'Coordinate plane distance'],
     'A number and its opposite are the same distance from 0 on opposite sides, so they have the same absolute value; farther right means greater, even for negatives; reflecting across an axis changes the sign of one coordinate, and points that share a coordinate are |difference| apart.')
tool('algebra2-rational-exponent-explorer', 'algebra2', 'radicals-rational-exponents', 'Radicals & Rational Exponents',
     'Rational Exponent Explorer',
     'Choose a base and a fractional exponent m/n. Compare taking the root first with raising to the power first, then look at the graph of y = x^(m/n).',
     'Evaluate b^(m/n) as (ⁿ√b)^m and as ⁿ√(bᵐ), see why equivalent fractions give the same power, what a negative exponent does, and when a negative base has a real root. Graph y = x^(m/n) and compare it with √x, ∛x and x².',
     ['Rational exponents', 'nth roots', 'Graphs of power functions'],
     'b^(m/n) means the nth root raised to the m: (ⁿ√b)^m = ⁿ√(bᵐ); the denominator is the root and the numerator is the power, a negative exponent gives a reciprocal, and a negative base has a real value only when n is odd.')
tool('precalculus-ambiguous-case', 'precalculus', 'general-triangle-trigonometry', 'Trigonometry of General Triangles',
     'Law of Sines: The Ambiguous Case',
     'You know angle A, side b next to it, and side a across from it. Swing side a like a compass and count how many triangles it can make.',
     'Model SSA with a swinging side: compare a with the height h = b sin A to see when there are zero, one or two triangles, solve each triangle with the Law of Sines, and see why an obtuse angle allows at most one.',
     ['Law of Sines', 'Ambiguous case (SSA)', 'Solving triangles'],
     'With A acute: no triangle if a < b sin A, one right triangle if a = b sin A, two triangles if b sin A < a < b, and one if a ≥ b; with A obtuse there is one triangle only when a > b. The two solutions have supplementary angles B and 180° − B.')
tool('precalculus-matrix-transformations', 'precalculus', 'matrices', 'Matrices',
     'Matrix Transformation Explorer',
     'Each 2 × 2 matrix moves every point of the plane. Change the four entries and watch where the unit square and the letter F land.',
     'Change the entries of a 2 × 2 matrix and watch the unit square and a shape transform. The columns show where (1, 0) and (0, 1) go, the determinant gives the area scale and whether the shape flips, and presets show rotations, reflections, dilations and shears.',
     ['Matrix transformations', 'Determinants', 'Rotations, reflections and shears'],
     'The columns of the matrix are the images of (1, 0) and (0, 1); the determinant ad − bc is the factor that multiplies every area, a negative determinant flips orientation, and a determinant of 0 squashes the plane onto a line.')
tool('calculus-optimization-box', 'calculus', 'applications-derivatives', 'Applications of Derivatives',
     'Optimization: Open-Top Box',
     'Cut equal squares from the corners of a sheet and fold up the sides. How big should the squares be to hold the most?',
     'Cut squares of side x from a sheet, fold an open box and track its volume V(x) on a graph. Use V′(x) to find the critical point, test it with the sign of V′, and compare it with the endpoints of the domain.',
     ['Optimization', 'Critical points', 'First derivative test'],
     'The volume is largest where V′(x) = 0 and V′ changes from positive to negative; the best cut is not at the ends of the domain, and changing the sheet changes the critical point.')
tool('calculus-area-volume-lab', 'calculus', 'applications-integrals', 'Applications of Integrals',
     'Area Between Curves & Solids of Revolution',
     'Slice the region between two curves into thin strips, then spin it around the x-axis and slice the solid into washers. Compare the sums with the exact integrals.',
     'Approximate the area between two curves with rectangles of height top − bottom, then the volume of the solid made by rotating the region about the x-axis with washers. Watch both sums approach ∫(top − bottom) dx and π∫(top² − bottom²) dx.',
     ['Area between curves', 'Washer method', 'Riemann sums'],
     'Each strip has height top − bottom, so the area is ∫(f − g) dx between the intersections; each washer has area π(R² − r²), so the volume is π∫(f² − g²) dx, which is not π times the square of the area.')
tool('calculus-slope-field', 'calculus', 'differential-equations', 'Differential Equations',
     'Slope Field Explorer',
     'Each tiny segment shows the slope dy/dx at that point. Drop a starting point and follow the field, then compare Euler’s method with the exact solution.',
     'Choose a differential equation, see its slope field, drag an initial condition and watch the solution curve. Step along with Euler’s method, change the step size, and find equilibrium solutions where the slopes are 0.',
     ['Slope fields', 'Euler’s method', 'Equilibrium solutions'],
     'A solution curve is tangent to the slope field at every point; Euler’s method follows tangent lines in steps, so smaller steps get closer to the exact solution, and horizontal rows of zero slope are equilibrium solutions.')

json.dump({'version': '20261114', 'labVersion': '20261105', 'tools': T}, open('manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(T), 'tools in manifest')
