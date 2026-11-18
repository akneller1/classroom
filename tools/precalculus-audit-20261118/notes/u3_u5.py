# Teaching notes, units 3–5 (format as in u1_u2.py).
CO = 'conics'
TR = 'trigonometric-functions'
GT = 'general-triangle-trigonometry'
R = {}

R[CO, 1] = dict(obj='write circle equations in standard form and find the center and radius, including by completing the square',
  idea='(x − h)² + (y − k)² = r² is the set of points at distance r from (h, k); complete the square to reach this form.',
  voc=[['center', 'The fixed point (h, k).'], ['radius', 'The distance r from the center to the circle.'], ['completing the square', 'Adding (b/2)² to make a perfect-square trinomial.']],
  watch='Taking the center as (3, 5) from (x + 3)² + (y + 5)², or forgetting to take the square root of r².',
  cards=[dict(h='Circles', big='Standard form ⟨(x - h)^2 + (y - k)^2 = r^2⟩: center ⟨(h, k)⟩ (signs {{opposite}} to those shown), radius ⟨\\sqrt{r^2}⟩. From general form, group ⟨x⟩ and ⟨y⟩ terms and {{complete the square}}.',
    steps=['⟨(x + 3)^2 + (y + 5)^2 = 9⟩: center ⟨({{-3}}, {{-5}})⟩, radius ⟨{{3}}⟩.', '⟨x^2 + y^2 + 10x - 6y - 66 = 0⟩: ⟨(x + 5)^2 + (y - 3)^2 = 66 + 25 + 9 = 100⟩.', 'Radius ⟨{{10}}⟩, center ⟨(-5, 3)⟩.'])])

R[CO, 2] = dict(obj='write and graph parabolas from the focus and directrix',
  idea='A parabola is the set of points equidistant from the focus and the directrix; in (x − h)² = 4p(y − k) the vertex is (h, k) and the focus is |p| from it.',
  voc=[['focus', 'The fixed point inside the parabola.'], ['directrix', 'The fixed line; every point is as far from it as from the focus.'], ['p', 'The signed distance from the vertex to the focus.']],
  watch='Using 4p as the focal distance instead of p.',
  cards=[dict(h='Parabolas', big='⟨(x - h)^2 = 4p(y - k)⟩ opens up (p > 0) or down; ⟨(y - k)^2 = 4p(x - h)⟩ opens right or left. Focus: {{p units}} from the vertex; directrix: p units on the {{other side}}.',
    steps=['⟨(x + 4)^2 = -16y⟩: vertex ⟨({{-4}}, {{0}})⟩, ⟨4p = -16⟩, ⟨p = -4⟩, opens down.', 'Vertex (2, 2), focus (2, 3): ⟨p = 1⟩, so ⟨{{(x - 2)^2 = 4(y - 2)}}⟩.', 'Directrix for that parabola: ⟨y = {{1}}⟩.'])])

R[CO, 3] = dict(obj='graph ellipses and find their vertices, co-vertices and foci',
  idea='In x²/a² + y²/b² = 1 the larger denominator sets the major axis; the foci satisfy c² = a² − b².',
  voc=[['major axis', 'The longer axis, length 2a.'], ['minor axis', 'The shorter axis, length 2b.'], ['foci', 'Two points on the major axis, c from the center, with c² = a² − b².']],
  watch='Using c² = a² + b² (the hyperbola relation) for an ellipse.',
  cards=[dict(h='Ellipses', big='The {{larger denominator}} is ⟨a^2⟩ and its variable shows the direction of the major axis. Major axis ⟨2a⟩, minor axis ⟨2b⟩, ⟨c^2 = {{a^2 - b^2}}⟩.',
    steps=['⟨\\frac{x^2}{25} + \\frac{y^2}{9} = 1⟩: ⟨a = 5⟩, major axis ⟨{{10}}⟩ (horizontal).', '⟨c^2 = 25 - 9 = 16⟩, foci ⟨(\\pm {{4}}, 0)⟩.', '⟨\\frac{x^2}{36} + \\frac{(y + 3)^2}{100} = 1⟩: ⟨c^2 = 100 - 36 = 64⟩, ⟨c = {{8}}⟩.'])])

R[CO, 4] = dict(obj='write equations of ellipses from vertices, co-vertices, foci and eccentricity',
  idea='Find the center (midpoint of the vertices), a and b from the axis lengths, then write (x − h)²/a² + (y − k)²/b² = 1 with a² under the major-axis variable.',
  voc=[['vertex', 'An endpoint of the major axis.'], ['co-vertex', 'An endpoint of the minor axis.'], ['eccentricity', 'e = c/a, between 0 and 1 for an ellipse.']],
  watch='Putting a² under the wrong variable when the major axis is vertical.',
  cards=[dict(h='Writing ellipse equations', big='Center = {{midpoint}} of the vertices. ⟨a⟩ = half the major axis, ⟨b⟩ = half the minor axis, ⟨c^2 = a^2 - b^2⟩, ⟨e = \\frac{c}{a}⟩.',
    steps=['Vertices ⟨(\\pm 10, 0)⟩, co-vertices ⟨(0, \\pm 8)⟩: ⟨{{\\frac{x^2}{100} + \\frac{y^2}{64} = 1}}⟩.', 'Major axis 26, minor 10: ⟨a = 13⟩, ⟨b = 5⟩, ⟨c = 12⟩.', '⟨e = {{\\tfrac{12}{13}}}⟩.'])])

R[CO, 5] = dict(obj='graph hyperbolas and find their vertices, foci and asymptotes',
  idea='In x²/a² − y²/b² = 1 the positive term gives the direction; the asymptotes are y − k = ±(b/a)(x − h) and c² = a² + b².',
  voc=[['transverse axis', 'The axis through the vertices, length 2a.'], ['asymptotes', 'The lines the branches approach.'], ['foci', 'Points c from the center with c² = a² + b².']],
  watch='Taking a² as the larger denominator (for a hyperbola, a² is under the positive term).',
  cards=[dict(h='Hyperbolas', big='⟨a^2⟩ is under the {{positive}} term. Vertices ⟨a⟩ from the center, foci ⟨c⟩ from it with ⟨c^2 = {{a^2 + b^2}}⟩. Asymptote slopes: ⟨\\pm \\frac{b}{a}⟩ (horizontal) or ⟨\\pm \\frac{a}{b}⟩ (vertical).',
    steps=['⟨\\frac{x^2}{64} - \\frac{y^2}{36} = 1⟩: vertices ⟨({{\\pm 8}}, 0)⟩.', '⟨c^2 = 64 + 36 = 100⟩: foci ⟨(\\pm {{10}}, 0)⟩.', 'Asymptotes ⟨y = \\pm {{\\tfrac{3}{4}}}x⟩.'])])

R[CO, 6] = dict(obj='write equations of hyperbolas and classify conics from their general equations',
  idea='From the vertices and foci find the center, a and c, then b² = c² − a². In Ax² + Cy² + … = 0 the signs of A and C classify the conic.',
  voc=[['general form', 'Ax² + Cy² + Dx + Ey + F = 0.'], ['classify', 'Same signs: ellipse (circle if A = C); opposite signs: hyperbola; one squared term: parabola.'], ['degenerate conic', 'A point, line or pair of lines from the same equation.']],
  watch='Using b² = a² − c² for a hyperbola.',
  cards=[dict(h='Hyperbola equations and classifying conics', big='Hyperbola: ⟨b^2 = {{c^2 - a^2}}⟩, positive term along the vertices. Classify ⟨Ax^2 + Cy^2⟩: ⟨AC > 0⟩ ellipse, ⟨AC < 0⟩ {{hyperbola}}, ⟨AC = 0⟩ parabola.',
    steps=['Vertices ⟨(0, \\pm 12)⟩, foci ⟨(0, \\pm 13)⟩: ⟨b^2 = 169 - 144 = 25⟩.', 'Equation: ⟨{{\\frac{y^2}{144} - \\frac{x^2}{25} = 1}}⟩.', '⟨-5x^2 + 2y^2 + 2x + 4y + 4 = 0⟩: opposite signs → {{hyperbola}}.'])])

# ------------------------------------------------------------------ trigonometric functions
R[TR, 1] = dict(obj='find coordinates on the unit circle and reference angles for any angle',
  idea='The terminal side of θ meets the unit circle at (cos θ, sin θ); the reference angle is the acute angle to the x-axis.',
  voc=[['unit circle', 'The circle of radius 1 centered at the origin.'], ['terminal side', 'The ray where an angle in standard position ends.'], ['reference angle', 'The acute angle between the terminal side and the x-axis.']],
  watch='Using the wrong signs for the quadrant of the angle.',
  cards=[dict(h='The unit circle', big='Point on the unit circle: ⟨(\\cos\\theta, \\sin\\theta)⟩. Use the {{reference angle}} for the values and the {{quadrant}} for the signs.',
    steps=['⟨\\theta = 135°⟩: reference ⟨45°⟩, Quadrant II → ⟨({{-\\tfrac{\\sqrt{2}}{2}}}, \\tfrac{\\sqrt{2}}{2})⟩.', 'Reference angle for ⟨\\tfrac{2\\pi}{3}⟩: ⟨\\pi - \\tfrac{2\\pi}{3} = {{\\tfrac{\\pi}{3}}}⟩.', 'Reference angle for ⟨150°⟩: ⟨{{30°}}⟩.'])])

R[TR, 2] = dict(obj='find exact values of the six trigonometric functions at special angles',
  idea='Exact values come from the 30-60-90 and 45-45-90 triangles; the quadrant decides the sign.',
  voc=[['special angles', '30°, 45°, 60° and their multiples.'], ['reciprocal functions', 'csc = 1/sin, sec = 1/cos, cot = 1/tan.'], ['ASTC', 'All, Sine, Tangent, Cosine: which functions are positive in Quadrants I–IV.']],
  watch='Mixing up sin 30° = 1/2 and sin 60° = √3/2.',
  cards=[dict(h='Exact trigonometric values', big='⟨\\sin 30° = \\tfrac12⟩, ⟨\\sin 45° = \\tfrac{\\sqrt2}{2}⟩, ⟨\\sin 60° = \\tfrac{\\sqrt3}{2}⟩; cosine is the reverse order. ⟨\\tan = \\frac{\\sin}{\\cos}⟩. Sign: {{ASTC}}.',
    steps=['⟨\\cos 30° = {{\\tfrac{\\sqrt3}{2}}}⟩.', '⟨\\tan 315°⟩: reference ⟨45°⟩, Quadrant IV → ⟨{{-1}}⟩.', '⟨\\sec 120° = \\frac{1}{\\cos 120°} = \\frac{1}{-1/2} = {{-2}}⟩.'])])

R[TR, 3] = dict(obj='convert between degrees and radians and find coterminal angles',
  idea='π radians = 180°: multiply by 180°/π to get degrees and by π/180 to get radians; coterminal angles differ by 360° (2π).',
  voc=[['radian', 'The angle that cuts an arc equal to the radius.'], ['coterminal angles', 'Angles with the same terminal side, differing by multiples of 360°.'], ['standard position', 'Vertex at the origin, initial side on the positive x-axis.']],
  watch='Multiplying by π/180 when converting radians to degrees.',
  cards=[dict(h='Radians and coterminal angles', big='Degrees → radians: × ⟨\\frac{\\pi}{180}⟩. Radians → degrees: × ⟨\\frac{180°}{\\pi}⟩. Add or subtract {{360°}} to find a coterminal angle.',
    steps=['⟨\\tfrac{19\\pi}{12} \\cdot \\tfrac{180°}{\\pi} = {{285°}}⟩.', '⟨345° \\cdot \\tfrac{\\pi}{180} = {{\\tfrac{23\\pi}{12}}}⟩.', 'Coterminal with ⟨-608°⟩ in ⟨[0°, 360°)⟩: ⟨-608° + 720° = {{112°}}⟩.'])])

R[TR, 4] = dict(obj='find arc length and sector area from the radius and central angle',
  idea='With θ in radians, arc length s = rθ and sector area A = ½r²θ.',
  voc=[['central angle', 'An angle with its vertex at the center of the circle.'], ['arc length', 'The distance along the circle: s = rθ.'], ['sector', 'The region bounded by two radii and an arc.']],
  watch='Using degrees in s = rθ without converting to radians.',
  cards=[dict(h='Arc length and sector area', big='Convert θ to {{radians}} first. ⟨s = r\\theta⟩, ⟨A = \\tfrac12 r^2\\theta⟩.',
    steps=['⟨r = 14⟩, ⟨\\theta = \\tfrac{\\pi}{4}⟩: ⟨s = {{\\tfrac{7\\pi}{2}}}⟩ cm.', '⟨r = 12⟩, ⟨\\theta = \\tfrac{\\pi}{6}⟩: ⟨A = \\tfrac12(144)\\tfrac{\\pi}{6} = {{12\\pi}}⟩ in².', '⟨60°⟩ is ⟨\\tfrac{\\pi}{3}⟩, so with ⟨r = 9⟩, ⟨s = {{3\\pi}}⟩.'])])

R[TR, 5] = dict(obj='solve right-triangle problems with sine, cosine and tangent, including angles of elevation',
  idea='SOH-CAH-TOA relates an acute angle to two sides; inverse functions find the angle from two sides.',
  voc=[['angle of elevation', 'The angle up from the horizontal to a line of sight.'], ['angle of depression', 'The angle down from the horizontal.'], ['inverse tangent', 'tan⁻¹(opposite/adjacent) gives the angle.']],
  watch='Using the hypotenuse with tangent, or forgetting degree mode.',
  cards=[dict(h='Right-triangle applications', big='Label the sides from the angle: {{opposite, adjacent, hypotenuse}}. Choose the ratio that uses the known side and the unknown side.',
    steps=['Kite 19 ft high, string at 23°: ⟨\\sin 23° = \\tfrac{19}{L}⟩, ⟨L = \\tfrac{19}{\\sin 23°} \\approx {{48.6}}⟩ ft.', 'Ramp rises 18 ft over 7 ft: ⟨\\theta = \\tan^{-1}\\tfrac{18}{7} \\approx {{68.7°}}⟩.', 'Shadow 30 ft, sun at 40°: height ⟨30\\tan 40° \\approx {{25.2}}⟩ ft.'])])

R[TR, 6] = dict(obj='find the amplitude and period of sine and cosine functions',
  idea='For y = a sin(bx) or a cos(bx), the amplitude is |a| and the period is 2π/|b|.',
  voc=[['amplitude', 'Half the distance from maximum to minimum: |a|.'], ['period', 'The length of one cycle: 2π/|b|.'], ['frequency', 'Cycles per unit: |b|/(2π).']],
  watch='Giving a negative amplitude, or using b itself as the period.',
  cards=[dict(h='Amplitude and period', big='Amplitude = ⟨|a|⟩ (always {{positive}}). Period = ⟨\\frac{2\\pi}{|b|}⟩.',
    steps=['⟨y = -2\\sin(3x)⟩: amplitude ⟨{{2}}⟩, period ⟨{{\\tfrac{2\\pi}{3}}}⟩.', '⟨y = \\cos(4x)⟩: amplitude ⟨{{1}}⟩, period ⟨\\tfrac{\\pi}{2}⟩.', 'Period ⟨\\pi⟩ means ⟨|b| = {{2}}⟩.'])])

R[TR, 7] = dict(obj='graph sine functions with amplitude, period, phase shift and midline, and match graphs to equations',
  idea='y = a sin(b(x − h)) + k has midline y = k, maximum k + |a|, minimum k − |a|, period 2π/b and phase shift h.',
  voc=[['midline', 'The horizontal line y = k halfway between max and min.'], ['phase shift', 'The horizontal shift h.'], ['cycle', 'One complete repetition of the graph.']],
  watch='Reading the phase shift from sin(bx − c) as c instead of c/b.',
  cards=[dict(h='Graphs of sine', big='Midline ⟨y = k⟩, max ⟨k + |a|⟩, min ⟨k - |a|⟩. Factor out ⟨b⟩ to read the {{phase shift}}: ⟨\\sin(2x - \\pi) = \\sin 2(x - \\tfrac{\\pi}{2})⟩.',
    steps=['⟨y = 4\\sin(\\tfrac12 x) - 4⟩: midline ⟨y = {{-4}}⟩, max ⟨{{0}}⟩.', 'Period ⟨\\frac{2\\pi}{1/2} = {{4\\pi}}⟩.', '⟨y = 3\\sin(\\tfrac12(x - \\tfrac{\\pi}{4})) + 1⟩: phase shift ⟨{{\\tfrac{\\pi}{4}}}⟩ right.'])])

R[TR, 8] = dict(obj='write and graph cosine functions from amplitude, period and midline',
  idea='A cosine graph starts a cycle at a maximum (a > 0); build y = a cos(bx) + d from the amplitude a, b = 2π/period and midline d.',
  voc=[['maximum', 'k + |a|, where cosine starts when a > 0.'], ['b', '2π divided by the period.'], ['vertical shift', 'd, the midline value.']],
  watch='Writing the period itself in place of b.',
  cards=[dict(h='Graphs of cosine', big='⟨y = a\\cos(bx) + d⟩: amplitude ⟨a⟩, ⟨b = \\frac{2\\pi}{\\text{period}}⟩, midline ⟨y = d⟩. With ⟨a > 0⟩ the graph starts at its {{maximum}}.',
    steps=['Amplitude 4, period ⟨\\pi⟩, midline ⟨y = -1⟩: ⟨b = 2⟩, ⟨{{y = 4\\cos(2x) - 1}}⟩.', 'Max ⟨3⟩, min ⟨-1⟩: amplitude ⟨{{2}}⟩, midline ⟨y = {{1}}⟩.', 'Period 6: ⟨b = {{\\tfrac{\\pi}{3}}}⟩.'])])

R[TR, 9] = dict(obj='solve basic trigonometric equations on [0, 2π)',
  idea='Isolate the trig function, find the reference angle, then list every angle in [0, 2π) in the quadrants with the right sign.',
  voc=[['solution interval', 'The interval, such as [0, 2π), in which solutions are listed.'], ['general solution', 'All solutions, written with + 2πk (or + πk for tangent).'], ['reference angle', 'The acute angle that gives the value.']],
  watch='Giving only one solution when the function takes the value twice per cycle.',
  cards=[dict(h='Trigonometric equations', big='Isolate ⟨\\sin x⟩, ⟨\\cos x⟩ or ⟨\\tan x⟩. Find the reference angle, then use the {{sign}} to pick quadrants. Sine and cosine usually give {{two}} solutions per cycle.',
    steps=['⟨\\cos x = \\tfrac12⟩: ⟨x = {{\\tfrac{\\pi}{3}}}⟩ or ⟨{{\\tfrac{5\\pi}{3}}}⟩.', '⟨3\\sin x = -\\tfrac32⟩: ⟨\\sin x = -\\tfrac12⟩ → ⟨x = \\tfrac{7\\pi}{6}⟩ or ⟨\\tfrac{11\\pi}{6}⟩.', '⟨\\tan x = \\tfrac{\\sqrt3}{3}⟩: ⟨x = \\tfrac{\\pi}{6}⟩ or ⟨{{\\tfrac{7\\pi}{6}}}⟩.'])])

R[TR, 10] = dict(obj='evaluate inverse sine, cosine and tangent exactly and describe their graphs',
  idea='sin⁻¹ and tan⁻¹ return angles in [−π/2, π/2]; cos⁻¹ returns angles in [0, π].',
  voc=[['principal value', 'The single angle an inverse trig function returns.'], ['arcsin', 'sin⁻¹ x, the angle in [−π/2, π/2] with sine x.'], ['arccos', 'cos⁻¹ x, the angle in [0, π] with cosine x.']],
  watch='Giving an angle outside the inverse function’s range, such as cos⁻¹(−½) = −60°.',
  cards=[dict(h='Inverse trigonometric functions', big='Ranges: ⟨\\sin^{-1}, \\tan^{-1}⟩ in ⟨[-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}]⟩; ⟨\\cos^{-1}⟩ in ⟨[0, \\pi]⟩. Answer “which {{angle in that range}} has this value?”',
    steps=['⟨\\sin^{-1}\\tfrac12 = {{30°}}⟩.', '⟨\\cos^{-1}(-\\tfrac{\\sqrt3}{2}) = {{\\tfrac{5\\pi}{6}}}⟩ (Quadrant II, inside ⟨[0, \\pi]⟩).', '⟨\\tan^{-1}\\sqrt3 = {{\\tfrac{\\pi}{3}}}⟩.'])])

R[TR, 11] = dict(obj='use technology to find principal values of inverse trigonometric functions and solve equations',
  idea='A calculator in the right mode gives the principal value; use symmetry to find the other solutions in a cycle.',
  voc=[['radian mode', 'Calculator setting for angles in radians.'], ['principal value', 'The value the inverse function key returns.'], ['second solution', 'For sine, π − θ; for cosine, 2π − θ.']],
  watch='Leaving the calculator in degree mode for a radian answer.',
  cards=[dict(h='Principal values and technology', big='Set the mode first ({{radian}} or degree). The calculator gives one angle; for ⟨\\sin x = c⟩ the other is ⟨\\pi - x⟩, for ⟨\\cos x = c⟩ it is ⟨2\\pi - x⟩.',
    steps=['⟨\\sin^{-1}(-0.6) \\approx {{-0.644}}⟩ rad.', '⟨\\tan^{-1}(-3.15) \\approx {{-1.263}}⟩ rad.', '⟨\\sin x = 0.4⟩ on ⟨[0, 2\\pi)⟩: ⟨x \\approx 0.412⟩ or ⟨\\pi - 0.412 \\approx {{2.730}}⟩.'])])

R[TR, 12] = dict(obj='use the Pythagorean, reciprocal and quotient identities to find trigonometric values',
  idea='sin²θ + cos²θ = 1 gives the missing value; the quadrant decides its sign.',
  voc=[['Pythagorean identity', 'sin²θ + cos²θ = 1.'], ['quotient identity', 'tan θ = sin θ / cos θ.'], ['identity', 'An equation true for every allowed value of the variable.']],
  watch='Taking the positive square root without checking the quadrant.',
  cards=[dict(h='Fundamental identities', big='From one value, use ⟨\\sin^2\\theta + \\cos^2\\theta = 1⟩ for the other, choose the {{sign from the quadrant}}, then use quotient and reciprocal identities.',
    steps=['⟨\\cos\\theta = \\tfrac{20}{29}⟩, Quadrant IV: ⟨\\sin\\theta = -\\tfrac{21}{29}⟩.', '⟨\\tan\\theta = \\frac{-21/29}{20/29} = {{-\\tfrac{21}{20}}}⟩.', '⟨\\cos\\theta = -\\tfrac{21}{29}⟩, Quadrant II: ⟨\\sin\\theta = {{\\tfrac{20}{29}}}⟩.'])])

R[TR, 13] = dict(obj='use double-angle and half-angle identities to find exact values and rewrite expressions',
  idea='sin 2θ = 2 sin θ cos θ and cos 2θ = cos²θ − sin²θ = 2cos²θ − 1 = 1 − 2sin²θ.',
  voc=[['double-angle identity', 'A formula for sin 2θ, cos 2θ or tan 2θ.'], ['half-angle identity', 'sin(θ/2) = ±√((1 − cos θ)/2).'], ['power reduction', 'Rewriting cos²θ as (1 + cos 2θ)/2.']],
  watch='Writing sin 2θ = 2 sin θ (forgetting the cos θ factor).',
  cards=[dict(h='Double- and half-angle identities', big='⟨\\sin 2\\theta = 2\\sin\\theta\\cos\\theta⟩; ⟨\\cos 2\\theta = {{1 - 2\\sin^2\\theta}}⟩ (or ⟨2\\cos^2\\theta - 1⟩). Find ⟨\\sin\\theta⟩ and ⟨\\cos\\theta⟩ first.',
    steps=['⟨\\sin\\theta = \\tfrac{24}{25}⟩: ⟨\\cos 2\\theta = 1 - 2\\left(\\tfrac{576}{625}\\right) = {{-\\tfrac{527}{625}}}⟩.', '⟨2\\cos^2(4x) - 1 = {{\\cos(8x)}}⟩.', '⟨\\sin 15° = \\sqrt{\\tfrac{1 - \\cos 30°}{2}} = {{\\tfrac{\\sqrt6 - \\sqrt2}{4}}}⟩.'])])

R[TR, 14] = dict(obj='solve trigonometric equations that need identities or factoring',
  idea='Use an identity to write the equation in one function (and one angle), factor, and solve each factor on [0, 2π).',
  voc=[['factoring', 'Writing an expression as a product to use the zero-product property.'], ['quadratic in sin x', 'An equation like 2sin²x − sin x − 1 = 0.'], ['extraneous', 'A value from a step (like squaring) that does not solve the original.']],
  watch='Dividing both sides by a trig function and losing the solutions where it equals 0.',
  cards=[dict(h='Equations with identities', big='Rewrite in {{one function}}, set to 0, {{factor}}, and solve each factor. Never divide by ⟨\\sin x⟩ or ⟨\\cos x⟩.',
    steps=['⟨2(2\\sin^2 x - 1) = 0⟩: ⟨\\sin^2 x = \\tfrac12⟩, ⟨\\sin x = \\pm\\tfrac{\\sqrt2}{2}⟩.', '⟨x = {{\\tfrac{\\pi}{4}, \\tfrac{3\\pi}{4}, \\tfrac{5\\pi}{4}, \\tfrac{7\\pi}{4}}}⟩.', '⟨\\sin 2x = \\sin x⟩: ⟨\\sin x(2\\cos x - 1) = 0⟩ → ⟨x = 0, \\pi, \\tfrac{\\pi}{3}, \\tfrac{5\\pi}{3}⟩.'])])

# ------------------------------------------------------------------ general triangles
R[GT, 1] = dict(obj='find the area of a triangle from two sides and the included angle, and state the Law of Sines',
  idea='Area = ½ab sin C; the Law of Sines a/sin A = b/sin B = c/sin C relates each side to its opposite angle.',
  voc=[['included angle', 'The angle between the two given sides.'], ['Law of Sines', 'a/sin A = b/sin B = c/sin C.'], ['oblique triangle', 'A triangle with no right angle.']],
  watch='Using an angle that is not between the two given sides in ½ab sin C.',
  cards=[dict(h='Triangle area and the Law of Sines', big='Area = ⟨\\tfrac12 ab\\sin C⟩ with ⟨C⟩ {{between}} ⟨a⟩ and ⟨b⟩. Law of Sines: ⟨\\frac{a}{\\sin A} = \\frac{b}{\\sin B}⟩ — each side over the sine of its {{opposite}} angle.',
    steps=['Sides 4 cm and 16 cm, angle 84°: ⟨\\tfrac12(4)(16)\\sin 84° \\approx {{31.8}}⟩ cm².', '⟨A = 72°⟩, ⟨B = 55°⟩: ⟨{{\\frac{a}{\\sin 72°} = \\frac{b}{\\sin 55°}}}⟩.', 'Parallelogram, sides 18 and 19, angle 78°: ⟨18 \\cdot 19 \\sin 78° \\approx {{334.5}}⟩ m².'])])

R[GT, 2] = dict(obj='solve triangles with the Law of Sines (AAS and ASA)',
  idea='Find the third angle from 180°, then use a/sin A = b/sin B to find each missing side.',
  voc=[['AAS / ASA', 'Two angles and a side: exactly one triangle.'], ['solve a triangle', 'Find all three sides and all three angles.'], ['angle sum', 'A + B + C = 180°.']],
  watch='Inverting the ratio: b = a·sin A / sin B instead of a·sin B / sin A.',
  cards=[dict(h='Solving triangles with the Law of Sines', big='Third angle: ⟨C = 180° - A - B⟩. Then ⟨b = \\frac{a\\sin B}{\\sin A}⟩: the unknown side goes with the sine of {{its own opposite angle}} on top.',
    steps=['⟨A = 77°⟩, ⟨B = 59°⟩: ⟨C = {{44°}}⟩.', '⟨A = 82°⟩, ⟨B = 75°⟩, ⟨a = 10⟩: ⟨b = \\frac{10\\sin 75°}{\\sin 82°} \\approx {{9.8}}⟩.', '⟨A = 71°⟩, ⟨B = 26°⟩, ⟨a = 6⟩: ⟨b = \\frac{6\\sin 26°}{\\sin 71°} \\approx {{2.8}}⟩.'])])

R[GT, 3] = dict(obj='decide whether SSA data give zero, one or two triangles and solve each',
  idea='Compare the side a opposite the given angle with the height h = b sin A: a < h none, a = h one right triangle, h < a < b two, a ≥ b one.',
  voc=[['ambiguous case', 'SSA information, which may give 0, 1 or 2 triangles.'], ['height h', 'b sin A, the shortest distance from C to the other side.'], ['supplement', '180° − B, the second possible angle.']],
  watch='Forgetting the second triangle with B₂ = 180° − B₁.',
  cards=[dict(h='The ambiguous case', big='Compute ⟨h = b\\sin A⟩. ⟨a < h⟩: {{0}} triangles. ⟨a = h⟩ or ⟨a \\ge b⟩: {{1}}. ⟨h < a < b⟩: {{2}} — use ⟨B⟩ and ⟨180° - B⟩.',
    steps=['⟨A = 21°⟩, ⟨a = 1⟩, ⟨b = 6⟩: ⟨h = 6\\sin 21° \\approx 2.15 > 1⟩ → {{0}} triangles.', '⟨A = 39°⟩, ⟨a = 12⟩, ⟨b = 14⟩: ⟨h \\approx 8.8 < 12 < 14⟩ → two triangles.', '⟨\\sin B = \\tfrac{14\\sin 39°}{12}⟩: ⟨B \\approx {{47.2°}}⟩ or ⟨{{132.8°}}⟩.'])])

R[GT, 4] = dict(obj='use the Law of Cosines to find a side (SAS) or an angle (SSS)',
  idea='c² = a² + b² − 2ab cos C generalizes the Pythagorean Theorem; solve it for cos C to find an angle.',
  voc=[['Law of Cosines', 'c² = a² + b² − 2ab cos C.'], ['SAS', 'Two sides and the included angle.'], ['SSS', 'Three sides.']],
  watch='Combining a² + b² − 2ab before multiplying by cos C.',
  cards=[dict(h='The Law of Cosines', big='Side: ⟨c^2 = a^2 + b^2 - 2ab\\cos C⟩. Angle: ⟨\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}⟩. Find the {{largest angle}} first (opposite the longest side).',
    steps=['Hikers 4 km and 5 km apart at 126°: ⟨d^2 = 16 + 25 - 40\\cos 126° \\approx 64.5⟩, ⟨d \\approx {{8.0}}⟩ km.', 'Sides 13, 23, 29, angle ⟨A⟩: ⟨\\cos A = \\frac{23^2 + 29^2 - 13^2}{2(23)(29)}⟩, ⟨A \\approx {{25.8°}}⟩.', 'Sides 7, 15, 19: ⟨19^2 > 7^2 + 15^2⟩ → largest angle {{obtuse}}.'])])

R[GT, 5] = dict(obj='find triangle areas with Heron’s formula and with the Law of Cosines',
  idea='Heron: with s = (a + b + c)/2, Area = √(s(s − a)(s − b)(s − c)).',
  voc=[['semiperimeter', 's = (a + b + c)/2.'], ['Heron’s formula', 'Area = √(s(s − a)(s − b)(s − c)).'], ['SAS area', '½ab sin C.']],
  watch='Using the full perimeter instead of the semiperimeter s.',
  cards=[dict(h='Heron’s formula', big='Find the {{semiperimeter}} ⟨s⟩, then ⟨A = \\sqrt{s(s - a)(s - b)(s - c)}⟩. For SAS, use ⟨\\tfrac12 ab\\sin C⟩ instead.',
    steps=['Sides 4, 13, 15: ⟨s = 16⟩, ⟨A = \\sqrt{16 \\cdot 12 \\cdot 3 \\cdot 1} = \\sqrt{576} = {{24}}⟩.', 'Sides 20 m and 6 m at 66°: third side ⟨\\approx 18.4⟩ m (Law of Cosines).', 'Area ⟨\\tfrac12(20)(6)\\sin 66° \\approx {{54.8}}⟩ m².'])])

R[GT, 6] = dict(obj='derive the Law of Sines, the Law of Cosines and the area formula from the altitude and coordinates',
  idea='Dropping an altitude gives h = b sin A = a sin B, which leads to the Law of Sines; placing the triangle on axes and using the distance formula gives the Law of Cosines.',
  voc=[['altitude', 'A perpendicular segment from a vertex to the opposite side (or its extension).'], ['derivation', 'A chain of reasoning that proves a formula.'], ['Pythagorean identity', 'sin²A + cos²A = 1.']],
  watch='Treating the derivation as memorization rather than following each equal step.',
  cards=[dict(h='Deriving the laws', big='Altitude from ⟨C⟩: ⟨h = b\\sin A⟩ and ⟨h = a\\sin B⟩, so ⟨\\frac{a}{\\sin A} = \\frac{b}{\\sin B}⟩. Coordinates ⟨C = (b\\cos A, b\\sin A)⟩, ⟨B = (c, 0)⟩ and ⟨{{\\sin^2 A + \\cos^2 A = 1}}⟩ give ⟨a^2 = b^2 + c^2 - 2bc\\cos A⟩.',
    steps=['With ⟨b = 29⟩, ⟨A = 74°⟩: altitude ⟨h = 29\\sin 74° \\approx {{27.9}}⟩.', 'If ⟨C = 90°⟩, ⟨\\cos C = 0⟩ and the Law of Cosines becomes ⟨{{c^2 = a^2 + b^2}}⟩.', 'Area ⟨= \\tfrac12 \\cdot a \\cdot (b\\sin C)⟩ because the height on base ⟨a⟩ is ⟨{{b\\sin C}}⟩.'])])

R[GT, 7] = dict(obj='use sum and difference identities to find exact values and simplify expressions',
  idea='sin(α ± β) = sin α cos β ± cos α sin β and cos(α ± β) = cos α cos β ∓ sin α sin β.',
  voc=[['sum identity', 'A formula for the trig function of α + β.'], ['difference identity', 'A formula for the trig function of α − β.'], ['exact value', 'A value written with radicals and fractions, not a decimal.']],
  watch='Writing cos(α − β) = cos α − cos β, or using the wrong sign in the cosine formula.',
  cards=[dict(h='Sum and difference identities', big='Write the angle as a sum or difference of {{special angles}}, then use ⟨\\cos(\\alpha - \\beta) = \\cos\\alpha\\cos\\beta + \\sin\\alpha\\sin\\beta⟩ (the sign {{switches}} for cosine).',
    steps=['⟨\\cos 15° = \\cos(60° - 45°) = \\tfrac12 \\cdot \\tfrac{\\sqrt2}{2} + \\tfrac{\\sqrt3}{2} \\cdot \\tfrac{\\sqrt2}{2}⟩.', '⟨= {{\\tfrac{\\sqrt6 + \\sqrt2}{4}}}⟩.', '⟨\\sin 75° = \\sin(45° + 30°) = {{\\tfrac{\\sqrt6 + \\sqrt2}{4}}}⟩.'])])

R[GT, 8] = dict(obj='rotate points with angle-sum identities and rotation matrices',
  idea='Rotating (x, y) by θ about the origin gives (x cos θ − y sin θ, x sin θ + y cos θ), the product of the matrix [cos θ, −sin θ; sin θ, cos θ] with the point.',
  voc=[['rotation matrix', '[cos θ, −sin θ; sin θ, cos θ].'], ['counterclockwise', 'The positive direction of rotation.'], ['image', 'The point after the rotation.']],
  watch='Putting −sin θ in the bottom row (that rotates clockwise).',
  cards=[dict(h='Rotations', big='⟨R(\\theta) = \\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}⟩. Image ⟨= R(\\theta)\\begin{bmatrix} x \\\\ y \\end{bmatrix}⟩.',
    steps=['⟨R(90°) = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}⟩: ⟨(3, 6) \\to ({{-6}}, {{3}})⟩.', '⟨(-5, 3)⟩ by 135°: ⟨x\' = -5(-\\tfrac{\\sqrt2}{2}) - 3(\\tfrac{\\sqrt2}{2}) = {{\\sqrt2}}⟩.', '⟨y\' = -5(\\tfrac{\\sqrt2}{2}) + 3(-\\tfrac{\\sqrt2}{2}) = {{-4\\sqrt2}}⟩.'])])
