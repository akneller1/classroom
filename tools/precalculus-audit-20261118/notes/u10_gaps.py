# Teaching notes for the standards-gap skills added in batch P4 (format as in u1_u2.py).
FN = 'functions'
VE = 'vectors'
SQ = 'sequences-series-limits'
R = {}

R[FN, 19] = dict(obj='simplify, add and divide rational expressions and decompose fractions into partial fractions',
  idea='Factor first: cancel only common factors, use a common denominator to add, multiply by the reciprocal to divide; a fraction over (x − p)(x − q) splits into A/(x − p) + B/(x − q).',
  voc=[['rational expression', 'A quotient of two polynomials.'], ['excluded value', 'An x that makes a denominator 0.'], ['partial fractions', 'Simpler fractions whose sum is the original fraction.']],
  watch='Cancelling terms instead of factors, as in (x + 6)/(x + 5) → 6/5.',
  cards=[dict(h='Rational expressions', big='{{Factor}} every numerator and denominator, then cancel only common {{factors}}. To add, rewrite over a common denominator; to divide, multiply by the {{reciprocal}}.',
    steps=['⟨\\frac{x^2 + 5x - 6}{x^2 + 11x + 30} = \\frac{(x + 6)(x - 1)}{(x + 6)(x + 5)} = {{\\frac{x - 1}{x + 5}}}⟩.', '⟨\\frac{2}{x - 1} + \\frac{3}{x + 2} = \\frac{2(x + 2) + 3(x - 1)}{(x - 1)(x + 2)} = {{\\frac{5x + 1}{(x - 1)(x + 2)}}}⟩.', 'Undefined where the denominator is 0: ⟨x = {{1}}⟩ or ⟨x = {{-2}}⟩.']),
    dict(h='Partial fractions', big='Write ⟨\\frac{Ax + B}{(x - p)(x - q)} = \\frac{A}{x - p} + \\frac{B}{x - q}⟩, multiply through, then substitute ⟨x = p⟩ and ⟨x = q⟩.',
    steps=['⟨\\frac{5x + 1}{(x - 1)(x + 2)} = \\frac{A}{x - 1} + \\frac{B}{x + 2}⟩, so ⟨5x + 1 = A(x + 2) + B(x - 1)⟩.', '⟨x = 1⟩: ⟨6 = 3A⟩, ⟨A = {{2}}⟩.', '⟨x = -2⟩: ⟨-9 = -3B⟩, ⟨B = {{3}}⟩.'])])

R[FN, 20] = dict(obj='verify inverses by composition, read inverse values from tables and graphs, and restrict domains to make functions invertible',
  idea='f and g are inverses when f(g(x)) = x and g(f(x)) = x; f⁻¹(b) = a exactly when f(a) = b; a function that is not one-to-one gets an inverse after its domain is restricted.',
  voc=[['inverse function', 'f⁻¹ undoes f: f⁻¹(f(x)) = x.'], ['one-to-one', 'Each output comes from exactly one input; passes the horizontal line test.'], ['restricted domain', 'A smaller domain chosen so the function is one-to-one.']],
  watch='Evaluating f(b) when the question asks for f⁻¹(b).',
  cards=[dict(h='Inverses: verify, read and restrict', big='Check ⟨f(g(x)) = {{x}}⟩. Read ⟨f^{-1}(b)⟩ as "the input that gives ⟨b⟩". For a parabola, keep {{one side of the vertex}}.',
    steps=['⟨f(x) = 3x - 6⟩, ⟨g(x) = \\frac{x + 6}{3}⟩: ⟨f(g(x)) = 3 \\cdot \\frac{x + 6}{3} - 6 = {{x}}⟩ ✓.', 'Table: ⟨f(2) = -4⟩, so ⟨f^{-1}(-4) = {{2}}⟩.', '⟨f(x) = (x + 4)^2 + 9⟩, ⟨x \\ge -4⟩: ⟨f^{-1}(10)⟩ solves ⟨(x + 4)^2 = 1⟩, ⟨x = {{-3}}⟩ (not ⟨-5⟩).'])])

R[VE, 12] = dict(obj='use conjugates to find moduli, reciprocals and quotients of complex numbers',
  idea='(a + bi)(a − bi) = a² + b² = |z|², so multiplying by the conjugate makes a denominator real; |z₁/z₂| = |z₁|/|z₂|.',
  voc=[['complex conjugate', 'z̄ = a − bi for z = a + bi.'], ['modulus', '|z| = √(a² + b²).'], ['quotient', 'The result of dividing one complex number by another.']],
  watch='Dividing the real parts and the imaginary parts separately.',
  cards=[dict(h='Conjugates and quotients', big='⟨z\\bar z = a^2 + b^2 = {{|z|^2}}⟩. To divide, multiply the numerator and denominator by the {{conjugate}} of the denominator.',
    steps=['⟨(3 + 4i)(3 - 4i) = 9 + 16 = {{25}}⟩.', '⟨\\frac{-4 - 8i}{1 + i} \\cdot \\frac{1 - i}{1 - i} = \\frac{-12 - 4i}{2} = {{-6 - 2i}}⟩.', '⟨\\left|\\frac{12 - 9i}{-3 + 4i}\\right| = \\frac{15}{5} = {{3}}⟩.'])])

R[VE, 13] = dict(obj='multiply, divide and raise complex numbers to powers in polar form and find their roots',
  idea='Multiply the moduli and add the angles; divide the moduli and subtract the angles; De Moivre: [r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ); the n nth roots are spaced 360°/n apart.',
  voc=[['polar (trigonometric) form', 'r(cos θ + i sin θ).'], ['argument', 'The angle θ of a complex number.'], ["De Moivre's Theorem", 'zⁿ = rⁿ(cos nθ + i sin nθ).']],
  watch='Multiplying the angle by n but forgetting to raise the modulus to the nth power.',
  cards=[dict(h="Polar form and De Moivre's Theorem", big='Product: ⟨r_1r_2⟩ and ⟨\\theta_1 + \\theta_2⟩. Quotient: ⟨\\frac{r_1}{r_2}⟩ and {{⟨\\theta_1 - \\theta_2⟩}}. Power: ⟨r^n⟩ and ⟨n\\theta⟩. Roots: ⟨\\sqrt[n]{r}⟩ and ⟨\\frac{\\theta + 360°k}{n}⟩.',
    steps=['⟨2(\\cos 40° + i\\sin 40°) \\cdot 3(\\cos 50° + i\\sin 50°) = 6(\\cos 90° + i\\sin 90°) = {{6i}}⟩.', '⟨(1 + i)^4⟩: ⟨1 + i = \\sqrt2(\\cos 45° + i\\sin 45°)⟩, so ⟨(\\sqrt2)^4(\\cos 180° + i\\sin 180°) = {{-4}}⟩.', 'Cube roots of ⟨8(\\cos 90° + i\\sin 90°)⟩: the first is ⟨2(\\cos 30° + i\\sin 30°) = {{\\sqrt3 + i}}⟩.'])])

R[VE, 14] = dict(obj='graph and classify limaçons and cardioids and find key points of their graphs',
  idea='For r = a ± b cos θ or a ± b sin θ (a, b > 0): a/b < 1 inner loop, a/b = 1 cardioid, 1 < a/b < 2 dimpled, a/b ≥ 2 convex; cosine graphs are symmetric about the polar axis, sine graphs about θ = π/2.',
  voc=[['limaçon', 'The graph of r = a ± b cos θ or r = a ± b sin θ.'], ['cardioid', 'A heart-shaped limaçon with a = b; it passes through the pole once.'], ['pole', 'The origin of the polar plane.']],
  watch='Classifying by b/a instead of a/b.',
  cards=[dict(h='Limaçons and cardioids', big='Compare ⟨a⟩ with ⟨b⟩: ⟨\\frac{a}{b} < 1⟩ {{inner loop}}, ⟨= 1⟩ {{cardioid}}, between 1 and 2 dimpled, ⟨\\ge 2⟩ convex. Farthest point from the pole: ⟨a + b⟩.',
    steps=['⟨r = 3 + 3\\cos\\theta⟩: ⟨\\frac{a}{b} = 1⟩ → {{cardioid}}, through the pole at ⟨\\theta = \\pi⟩.', '⟨r = 2 + 4\\sin\\theta⟩: inner loop; ⟨r = 0⟩ when ⟨\\sin\\theta = -\\tfrac12⟩: ⟨\\theta = {{\\tfrac{7\\pi}{6}}}⟩ or ⟨\\tfrac{11\\pi}{6}⟩.', '⟨r = 7 + 5\\cos\\theta⟩ at ⟨\\theta = \\tfrac{\\pi}{3}⟩: ⟨7 + \\tfrac52 = {{\\tfrac{19}{2}}}⟩; greatest distance ⟨{{12}}⟩.'])])

R[SQ, 6] = dict(obj='expand binomials and find specific terms and coefficients with the Binomial Theorem',
  idea='(a + b)ⁿ = Σ C(n, k)aⁿ⁻ᵏbᵏ for k = 0 to n; the coefficients are row n of Pascal’s triangle, and the term number is k + 1.',
  voc=[['binomial coefficient', 'C(n, k) = n!/(k!(n − k)!).'], ["Pascal's triangle", 'Each entry is the sum of the two above it; row n holds C(n, 0) … C(n, n).'], ['Binomial Theorem', 'The formula for expanding (a + b)ⁿ.']],
  watch='Forgetting to raise the coefficient of x (and its sign) to the power.',
  cards=[dict(h='The Binomial Theorem', big='Term ⟨k + 1⟩ of ⟨(a + b)^n⟩ is ⟨\\binom{n}{k}a^{n - k}b^k⟩. Raise the {{whole}} first term, including its coefficient, and keep the {{sign}} of the second.',
    steps=['⟨(x + 2)^3 = x^3 + 3x^2(2) + 3x(2)^2 + 2^3 = {{x^3 + 6x^2 + 12x + 8}}⟩.', 'Coefficient of ⟨x^2⟩ in ⟨(2x - 1)^5⟩: ⟨\\binom{5}{2}(2)^2(-1)^3 = {{-40}}⟩.', 'Sum of the coefficients of ⟨(2x - 3)^6⟩: ⟨(2 - 3)^6 = {{1}}⟩.'])])

R[SQ, 7] = dict(obj='find one-sided limits, decide whether limits exist and make functions continuous',
  idea='The limit at c exists when the left and right limits are equal; f is continuous at c when the limit exists and equals f(c).',
  voc=[['one-sided limit', 'The value f(x) approaches as x → c⁻ (from the left) or x → c⁺ (from the right).'], ['continuous', 'No break: lim f(x) = f(c).'], ['removable discontinuity', 'A hole that can be filled by redefining one value.']],
  watch='Using the wrong piece of a piecewise function for a one-sided limit.',
  cards=[dict(h='Continuity and one-sided limits', big='Left limit: use the piece for ⟨x < c⟩; right limit: the piece for ⟨x > c⟩. The limit exists only if they {{agree}}; continuity also needs ⟨f(c)⟩ {{equal to the limit}}.',
    steps=['⟨f(x) = 2x - 7⟩ for ⟨x < 2⟩, ⟨4x + 7⟩ for ⟨x \\ge 2⟩: left ⟨-3⟩, right ⟨15⟩ → the limit {{does not exist}}.', '⟨x^2 + 4⟩ for ⟨x < 2⟩, ⟨kx - 8⟩ for ⟨x \\ge 2⟩: ⟨8 = 2k - 8⟩, ⟨k = {{8}}⟩.', '⟨\\frac{x^2 - 5x - 6}{x - 6} = x + 1⟩ for ⟨x \\ne 6⟩: define ⟨f(6) = {{7}}⟩.'])])
