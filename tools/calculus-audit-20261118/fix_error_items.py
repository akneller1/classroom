"""Calculus audit #1 (2026-11-18): every find-the-mistake diagnosis names what the student actually did.

LABELS maps an item id to its new diagnosis and, where the old student answer was garbled or could not come
from the named mistake, a new student answer. REWRITE replaces the four duplicated items and the two tank
items whose key was a negative amount of water. Run once; it is idempotent.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import lib

# id: (diagnosis, new student answer or None)
LABELS = {
    'cal-pcr-s01-honors-016': ('Used + x instead of − x in the second factor: x³ + 1 = (x + 1)(x² − x + 1).', '(x + 1)(x² + x + 1)'),
    'cal-pcr-s03-cp2-016': ('Confused ln(1) with ln(e). Since e⁰ = 1, ln(1) = 0.', None),
    'cal-pcr-s03-honors-014': ('Added the logarithms. Division inside a log becomes subtraction: ln(x²) − ln(y⁵).', None),
    'cal-pcr-s03-honors-016': ('Added ln(y) instead of subtracting it; − ln(y) puts y in the denominator.', None),
    'cal-pcr-s04-cp2-016': ('Used the value of tan(45°). tan(180°) = sin(180°) ÷ cos(180°) = 0 ÷ (−1) = 0.', None),
    'cal-pcr-s04-honors-016': ('Used sine instead of cosine: sin(−π) = 0, but cos(−π) = −1.', None),
    'cal-pcr-s05-cp2-016': ('Added f(4) and f(1) instead of subtracting them.', None),
    'cal-pcr-s05-honors-016': ('Added f(7) and f(1) instead of subtracting them.', None),
    'cal-lim-s01-cp1-014': ('Substituted x = 2 instead of x = −2.', '-34'),
    'cal-lim-s01-honors-016': ('Substituted x = 0 instead of x = −1.', None),
    'cal-lim-s03-honors-016': ('Stopped at 0 ÷ 0. Use lim (x → 0) sin(kx)/x = k.', None),
    'cal-lim-s04-cp1-014': ('Substituted x = 0 into 3x − 2 instead of x = 1.', '-2'),
    'cal-lim-s04-cp2-016': ('Added the left-hand and right-hand values; a one-sided limit uses one piece only.', None),
    'cal-lim-s04-cp1-016': ('Added the left-hand and right-hand values; a one-sided limit uses one piece only.', None),
    'cal-lim-s04-honors-014': ('Thought the limit does not exist because the formula changes at x = −1. Both one-sided limits equal 4, so the limit is 4.', 'does not exist'),
    'cal-lim-s04-honors-016': ('Thought the limit does not exist because the formula changes at x = 3. A left-hand limit uses only the piece for x < 3.', None),
    'cal-lim-s05-cp2-014': ('Treated the degrees as unequal. Both are degree 3, so the limit is the ratio of leading coefficients.', None),
    'cal-lim-s05-cp2-016': ('Treated the degrees as unequal. Both are degree 1, so the limit is the ratio of leading coefficients.', None),
    'cal-lim-s06-cp2-014': ('Made a sign error solving −3 + k = −1.', None),
    'cal-lim-s06-cp2-016': ('Made a sign error solving 4 + k = −3.', None),
    'cal-lim-s06-cp1-014': ('Made a sign error solving −2k + 3 = 6.', None),
    'cal-lim-s07-cp1-014': ('Read the factor (x − 2) as giving x = −2; the hole is where x − 2 = 0.', None),
    'cal-lim-s07-honors-014': ('Used x = 1 instead of the zero of the common factor x.', None),
    'cal-lim-s08-cp2-014': ('Counted the four table values. Count only consecutive values on opposite sides of 4.', None),
    'cal-lim-s08-honors-014': ('Counted the four table values. Count only consecutive values on opposite sides of 4.', None),
    'cal-lim-s08-honors-016': ('Counted the four table values. Count only consecutive values on opposite sides of 1.', None),
    'cal-der-s01-honors-014': ('Made an arithmetic error: f′(2) = 4(2)³ = 32.', None),
    'cal-der-s01-honors-016': ('Made an arithmetic error: f′(16) = 3(16)² = 768.', None),
    'cal-der-s03-cp2-014': ('Changed the sign of every term. d/dx(−5x⁵) = −25x⁴ and d/dx(4x) = 4.', None),
    'cal-der-s03-cp2-016': ('Added an extra + 1. Neither term differentiates to a constant.', None),
    'cal-der-s03-cp1-014': ('Doubled the exponent and halved the log term. d/dx e^(2x) = 2e^(2x) and d/dx ln(x) = 1/x.', None),
    'cal-der-s03-cp1-016': ('Made sign errors: d/dx e^(−x) = −e^(−x) and d/dx ln(x) = +1/x.', None),
    'cal-der-s03-honors-014': ('Added a negative sign. The derivative of sin(u) is +cos(u)·u′.', None),
    'cal-der-s03-honors-016': ('Added a negative sign. d/dx ln(u) = u′/u, and u′ = 2x is positive here.', None),
    'cal-der-s04-cp2-016': ('Dropped the negative sign: f′(x) = −20x³, so f″(x) = −60x².', None),
    'cal-der-s04-cp1-014': ('Made a sign error: d/dx sec²(x) = 2sec²(x)tan(x), which is positive here.', None),
    'cal-der-s05-cp2-014': ('Made a sign error solving 4 = 8 + b; b = −4.', None),
    'cal-der-s05-cp1-014': ('Set b = f(3) = 9. Continuity needs 6(3) + b = 9, so b = −9.', None),
    'cal-der-s05-honors-016': ('Set b = f(−1) = 3. Continuity needs −6(−1) + b = 3, so b = −3.', None),
    'cal-der-s06-cp2-014': ('Used f(1) = 8 as the y-intercept instead of using point-slope form.', None),
    'cal-der-s06-cp2-016': ('Used x + 2 instead of x − 2 in point-slope form.', None),
    'cal-der-s06-cp1-016': ('Left out the shift: y − 0 = −2(x − 2), not y = −2x.', None),
    'cal-der-s06-honors-016': ('Used f(−1) = 1/4 as the y-intercept instead of using point-slope form.', None),
    'cal-der-s09-cp2-014': ('Dropped the negative in dy/dx = −x/y; x/y = −5/12.', None),
    'cal-app-s02-cp2-014': ('Missed x = 0. f′(x) = −3x(x − 2) is also zero at x = 0.', None),
    'cal-app-s02-cp1-014': ('Added x = 0, but f′(0) = −12, not 0.', None),
    'cal-app-s02-cp1-016': ('Missed x = 0. f′(x) = 6x(x + 2) is also zero at x = 0.', None),
    'cal-app-s02-honors-016': ('Missed x = 0. f′(x) = −6x(x + 4) is also zero at x = 0.', None),
    'cal-app-s04-cp2-014': ('Made an arithmetic error: f(−3) = −54 + 81 − 4 = 23.', None),
    'cal-app-s04-cp2-016': ('Made an arithmetic error: f(2) = −8 − 12 + 48 = 28.', None),
    'cal-app-s04-cp1-016': ('Made an arithmetic error: f(−4) = 128 − 48 − 288 − 4 = −212.', None),
    'cal-app-s04-honors-016': ('Made an arithmetic error: f(2) = 8 − 24 + 4 = −12.', None),
    'cal-app-s07-cp2-014': ('Used A = x(268 − x). The perimeter counts each side twice, so y = 134 − x.', '17956 m²'),
    'cal-app-s07-cp1-014': ('Used A = x(240 − x). The perimeter counts each side twice, so y = 120 − x.', '14400 m²'),
    'cal-app-s10-cp1-014': ('Used the midpoint of the interval instead of solving f′(c) = 6.', None),
    'cal-app-s10-honors-014': ('Used the midpoint of the interval instead of solving f′(c) = 3.', None),
    'cal-app-s10-honors-016': ('Used the midpoint of the interval instead of solving f′(c) = 142.', None),
    'cal-app-s11-cp2-014': ('Dropped the sign: d/dx(−2/x) = +2/x².', '-2/x² + 3/(√x)'),
    'cal-app-s11-cp2-016': ('Changed the sign of every term. d/dx(5√x) = 5/(2√x) and d/dx(−3/x) = +3/x².', None),
    'cal-app-s11-cp1-014': ('Changed the sign of every term. The product rule gives 3(x² + 3) + (3x − 2)(2x) = 9x² − 4x + 9.', None),
    'cal-app-s11-cp1-016': ('Reversed the quotient rule: wrote uv′ − u′v instead of u′v − uv′.', '(2x² + 8x - 4)/(x² + 2)²'),
    'cal-app-s11-honors-014': ('Reversed the quotient rule: wrote uv′ − u′v instead of u′v − uv′.', '-((x - 1)(x + 5))/(2(x + 2)²)'),
    'cal-app-s11-honors-016': ('Lost the negative sign: d/dx cos(x) = −sin(x).', None),
    'cal-int-s02-cp2-016': ('Multiplied by the new exponent instead of dividing by it.', '-9x³ - 4x² - 9x + C'),
    'cal-int-s02-cp1-014': ('Integrated 3/x as 3. ∫ (1/x) dx = ln|x|.', None),
    'cal-int-s02-cp1-016': ('Multiplied by 3/2 instead of dividing by 3/2: ∫ 6x^(1/2) dx = 4x^(3/2).', '9x√x + 1/x + C'),
    'cal-int-s03-cp2-016': ('Used left endpoints instead of right endpoints.', None),
    'cal-int-s03-cp1-014': ('Used right endpoints instead of left endpoints.', None),
    'cal-int-s03-honors-016': ('Used right endpoints instead of left endpoints.', None),
    'cal-int-s04-cp2-014': ('Used left endpoints instead of right endpoints.', None),
    'cal-int-s04-cp2-016': ('Used left endpoints instead of right endpoints.', None),
    'cal-int-s05-cp2-014': ('Used a left Riemann sum instead of trapezoids.', None),
    'cal-int-s05-cp1-014': ('Used left endpoints instead of right endpoints.', None),
    'cal-int-s05-cp1-016': ('Used a left Riemann sum instead of trapezoids.', None),
    'cal-int-s05-honors-014': ('Used a left Riemann sum instead of trapezoids.', None),
    'cal-int-s06-cp2-014': ('Gave the opposite sign. Most of the region is below the x-axis, so the integral is negative.', None),
    'cal-int-s06-cp2-016': ('Gave the opposite sign. Most of the region is above the x-axis, so the integral is positive.', None),
    'cal-int-s06-cp1-014': ('Subtracted the triangle left of 0. |x| is never negative, so both triangles add: 1/2 + 2.', None),
    'cal-int-s07-cp2-014': ('Used the wrong piece: reversed ∫ from 3 to 6 instead of ∫ from 2 to 3.', None),
    'cal-int-s07-cp2-016': ('Subtracted the two pieces. Adjacent intervals add: 4 + 5 = 9.', None),
    'cal-int-s07-cp1-014': ('Used ∫ from 5 to 6 instead of reversing ∫ from 0 to 5.', None),
    'cal-int-s07-cp1-016': ('Used ∫ from 8 to 9 instead of reversing ∫ from 4 to 8.', None),
    'cal-int-s07-honors-014': ('Subtracted 1 instead of ∫ from 0 to 2 of 1 dx = 2.', None),
    'cal-int-s07-honors-016': ('Used the g integral. ∫ from −2 to 9 f(x) dx = −4 + (−1) = −5, and −4(−5) = 20.', None),
    'cal-ftc-s01-cp2-014': ('Gave f(8) instead of f(8) − f(0).', None),
    'cal-ftc-s04-honors-014': ('Subtracted f(1) = 2 for the lower limit. A constant lower limit adds nothing to the derivative.', None),
    'cal-ftc-s04-honors-016': ('Added 1 for the lower limit. A constant lower limit adds nothing to the derivative.', None),
    'cal-ftc-s07-cp2-014': ('Made a sign error on the remainder.', None),
    'cal-ftc-s07-cp2-016': ('Left out the factor 1/2.', None),
    'cal-ftc-s07-cp1-014': ('Left out the integral of the remainder term.', None),
    'cal-ftc-s07-cp1-016': ('Did not subtract 16 after adding it to complete the square.', None),
    'cal-ftc-s07-honors-014': ('Left out the factor 1/6.', None),
    'cal-ftc-s07-honors-016': ('Left out the factor 1/6.', None),
    'cal-aoi-s03-cp1-014': ('Averaged the endpoint values f(1) = 4 and f(e) = 4/e instead of integrating.', '2 + 2/e'),
    'cal-aoi-s05-cp2-014': ('Took the absolute value of the displacement. The particle turns around at t = 2.', '63/2 ft'),
    'cal-aoi-s05-cp1-016': ('Took the absolute value of the displacement. The particle turns around at t = 3 and t = 4.', '85/6 ft'),
    'cal-aoi-s07-cp2-016': ('Doubled the volume: used 2π∫ x² dx instead of π∫ x² dx.', None),
    'cal-aoi-s07-cp1-014': ('Squared the difference: used π∫ (R − r)² dx instead of π∫ (R² − r²) dx.', None),
    'cal-aoi-s07-cp1-016': ('Squared the difference: used π∫ (R − r)² dx instead of π∫ (R² − r²) dx.', None),
    'cal-aoi-s07-honors-014': ('Used disks (πx²) instead of squares (x²) for the cross sections.', None),
    'cal-aoi-s07-honors-016': ('Integrated the base length x² instead of the semicircle area (π/8)(x²)².', None),
    'cal-deq-s01-cp2-016': ('Switched x and y: used x = −1 and y = 0.', '-4'),
    'cal-deq-s01-honors-014': ('Left out the factor 1/2: (−1) + (−1) = −2.', '-2'),
    'cal-deq-s03-cp1-016': ('Used the first slope (1) for both steps. Recompute the slope at (−0.9, 3.1).', '3.2'),
    'cal-deq-s03-honors-014': ('Used the first slope (1) for all three steps. Recompute the slope after each step.', '1.3'),
    'cal-deq-s04-cp2-014': ('Made a sign error moving x² to the left side: y² − x² = C.', None),
    'cal-deq-s04-cp2-016': ('Wrote Cx⁷ instead of Ce^(7x). ∫ (1/y) dy = ln|y|, so y = Ce^(7x).', None),
    'cal-deq-s04-cp1-014': ('Made a sign error moving 9x² to the left side: 7y² − 9x² = C.', None),
    'cal-deq-s04-cp1-016': ('Differentiated −20x³ instead of integrating it. ∫ −20x³ dx = −5x⁴.', 'y = Ce^(-60x²)'),
    'cal-deq-s04-honors-014': ('Integrated x/2 and treated y as a constant instead of separating variables.', 'y = (1/4)x² + C'),
    'cal-deq-s04-honors-016': ('Lost the negative sign: ∫ y⁻² dy = −1/y.', None),
    'cal-deq-s05-cp2-014': ('Left out the exponential. ln|y| = x² + C gives y = Ce^(x²).', None),
    'cal-deq-s05-cp2-016': ('Integrated the right side without separating variables first.', 'y = 3x⁴ + C'),
    'cal-deq-s05-cp1-016': ('Forgot to divide by 3 when integrating: ∫ −3x² dx = −x³.', None),
    'cal-deq-s05-honors-014': ('Treated y′ = 11y² like y′ = 11y. Separate: y⁻² dy = 11 dx.', None),
    'cal-deq-s05-honors-016': ('Added C outside the fraction. −1/y = x + C gives y = −1/(x + C).', 'y = -1/x + C'),
    'cal-deq-s06-cp2-016': ('Left out the negative in the exponent: 14e³ ≈ 281.20.', '281.20'),
    'cal-apr-s01-cp2-016': ('Substituted x = 3 instead of x = −3 after canceling.', '7'),
    'cal-apr-s01-cp1-014': ('Factored x³ − 8 as (x − 2)(x² + 4). The second factor is x² + 2x + 4.', '8'),
    'cal-apr-s01-honors-016': ('Factored x³ − 125 as (x − 5)(x² + 25). The second factor is x² + 5x + 25.', '50'),
    'cal-apr-s02-cp2-014': ('Doubled the coefficient: d/dx(−x²) = −2x, not −4x.', None),
    'cal-apr-s02-cp2-016': ('Doubled the coefficient: d/dx(x²) = 2x, not 4x.', None),
    'cal-apr-s02-cp1-014': ('Doubled the exponent and halved the log term. d/dx e^(6x) = 6e^(6x) and d/dx ln(x) = 1/x.', None),
    'cal-apr-s02-cp1-016': ('Doubled the exponent and halved the log term. d/dx e^(4x) = 4e^(4x) and d/dx ln(x) = 1/x.', None),
    'cal-apr-s02-honors-014': ('Lost the negative sign: d/dx cos(x) = −sin(x), so f′(x) = −2sin(x)cos(x) = −sin(2x).', None),
    'cal-apr-s02-honors-016': ('Divided the derivative of the numerator by the derivative of the denominator. Use the quotient rule.', None),
    'cal-apr-s05-cp2-014': ('Averaged the two endpoint values instead of using the trapezoidal sum.', None),
    'cal-apr-s06-cp2-014': ('Made a sign error solving −2c − 6 = −8.', None),
    'cal-apr-s06-cp1-016': ('Used the midpoint of the interval instead of solving f′(c) = 38.', None),
    'cal-apr-s06-honors-014': ('Used the midpoint of the interval instead of solving f′(c) = 146.', None),
    'cal-apr-s06-honors-016': ('Chose the negative root of c² = 4/3, which is outside [0, 2].', None),
    'cal-apr-s07-cp2-016': ('Subtracted the two pieces. Adjacent intervals add: 6 + 4 = 10.', None),
    'cal-apr-s07-cp1-014': ('Subtracted the two pieces. Adjacent intervals add: 9 + 5 = 14.', None),
    'cal-apr-s07-cp1-016': ('Used ∫ from 7 to 8 instead of reversing ∫ from 4 to 7.', None),
    'cal-apr-s07-honors-016': ('Subtracted 2 instead of ∫ from −3 to 3 of 2 dx = 12.', None),
}

NAME = re.compile(r"^(\w+) answered this problem incorrectly\.")


def item(name, problem, student, key, label, work, standards, base):
    q = dict(base)
    q['prompt'] = f"{name} answered this problem incorrectly.\n{problem}\n{name}'s answer: {student}\nIdentify the mistake and give the correct answer."
    q['answer'] = key
    q['solutionSteps'] = ['Mistake: ' + label] + work + [f'The correct answer is {key}, not {student}.']
    q['standards'] = standards
    return q


def rewrite(q):
    i, b = q['id'], q
    if i == 'cal-pcr-s03-cp1-016':
        return item('Yusuf', 'Evaluate ln(1/e).', '1', '-1', 'Made a sign error: 1/e = e⁻¹, so ln(1/e) = −1.',
                    ['Write 1/e as a power of e: 1/e = e⁻¹.', 'ln(e⁻¹) = −1 because ln and eˣ are inverse functions.'], b['standards'], b)
    if i == 'cal-der-s05-cp1-016':
        return item('Isla', 'f(x) = x² for x ≤ 4 and f(x) = mx + b for x > 4. Find m and b so that f is differentiable at x = 4.',
                    'm = 8, b = 16', 'm = 8, b = -16', 'Set b = f(4) = 16. Continuity needs 8(4) + b = 16, so b = −16.',
                    ['Differentiable: the slopes match, so m = 2x at x = 4 = 8.', 'Continuous: 8(4) + b = 4² = 16.', '32 + b = 16, so b = −16.'], b['standards'], b)
    if i == 'cal-app-s07-honors-014':
        return item('Hiro', 'Equal squares are cut from the corners of a 24-in by 24-in sheet, and the sides are folded up to make an open box. What cut size gives the largest volume, and what is that volume?',
                    'x = 12 in; V = 0 in³', 'x = 4 in; V = 1024 in³', 'Used the critical number x = 12, which gives V = 0. Check which critical number gives the largest volume.',
                    ['V = x(24 − 2x)² for 0 < x < 12.', 'V′ = (24 − 2x)(24 − 6x) = 0, so x = 4 or x = 12.', 'V(4) = 4(16)² = 1024 in³; V(12) = 0.'], b['standards'], b)
    if i == 'cal-app-s10-cp1-016':
        return item('Kai', 'Find the value of c guaranteed by the Mean Value Theorem for f(x) = x³ - 3x on [0, 6].',
                    'c = 3', 'c = 2√3', 'Used the midpoint of the interval instead of solving f′(c) = 33.',
                    ['Average rate: (f(6) − f(0)) ÷ (6 − 0) = (198 − 0) ÷ 6 = 33.', 'Solve f′(c) = 3c² − 3 = 33, so c² = 12.', 'c = 2√3 ≈ 3.46, which is in (0, 6).'], b['standards'], b)
    if i == 'cal-aoi-s02-honors-011':
        q = dict(b)
        q['prompt'] = 'A tank holds 52 L at t = 0. Water enters at E(t) = 2t + 4 L/min and leaves at a constant 11 L/min. How much water is in the tank at t = 4 minutes?'
        q['answer'] = '40 L'
        q['solutionSteps'] = ['Amount = 52 + ∫ from 0 to 4 (E(t) − 11) dt = 52 + ∫ from 0 to 4 (2t − 7) dt.',
                              'Antiderivative: t² − 7t. At t = 4: 16 − 28 = −12. At t = 0: 0.', 'Amount = 52 + (−12) = 40 L.']
        return q
    if i == 'cal-aoi-s02-honors-016':
        return item('Nia', 'A tank holds 74 L at t = 0. Water enters at E(t) = 2t + 2 L/min and leaves at a constant 15 L/min. How much water is in the tank at t = 4 minutes?',
                    '-36 L', '38 L', 'Forgot the initial amount of 74 L.',
                    ['Amount = 74 + ∫ from 0 to 4 (E(t) − 15) dt = 74 + ∫ from 0 to 4 (2t − 13) dt.', 'Antiderivative: t² − 13t. At t = 4: 16 − 52 = −36. At t = 0: 0.', 'Amount = 74 + (−36) = 38 L.'], b['standards'], b)
    if i == 'cal-deq-s03-honors-014':
        q = item('Marco', "Use Euler's method with step size 0.1 and 3 steps to approximate y(-1.7) for y′ = xy + 3, y(-2) = 1.", '1.3', '1.27662',
                 LABELS[i][0], ['yₙ₊₁ = yₙ + h·f(xₙ, yₙ).', 'Step 1: slope (−2)(1) + 3 = 1, so y ≈ 1 + 0.1(1) = 1.1 at x = −1.9.',
                                'Step 2: slope (−1.9)(1.1) + 3 = 0.91, so y ≈ 1.1 + 0.091 = 1.191 at x = −1.8.',
                                'Step 3: slope (−1.8)(1.191) + 3 = 0.8562, so y ≈ 1.191 + 0.08562 = 1.27662 at x = −1.7.'], b['standards'], b)
        return q
    return None


def apply(q):
    if q['id'] in ('cal-pcr-s03-cp1-016', 'cal-der-s05-cp1-016', 'cal-app-s07-honors-014', 'cal-app-s10-cp1-016',
                   'cal-aoi-s02-honors-011', 'cal-aoi-s02-honors-016', 'cal-deq-s03-honors-014'):
        return rewrite(q)
    if q['id'] not in LABELS:
        # names in the labels of the long-division family become plain diagnoses everywhere
        q['solutionSteps'] = [re.sub(r'^Mistake: (?:Ava|Ben|Chloe|Hana|Kenji|Omar|Dev|Elena|Femi|Hiro|Isla|Kai|Lena|Marco|Nia|Priya|Quinn|Rosa|Sam|Tariq|Uma|Vic|Wren|Yusuf|Zoe|Jamal|Leah) (made|left|did)', lambda m: 'Mistake: ' + m.group(1).capitalize(), s) for s in q['solutionSteps']]
        return q
    label, student = LABELS[q['id']]
    steps = q['solutionSteps']
    steps[[k for k, s in enumerate(steps) if s.startswith('Mistake:')][0]] = 'Mistake: ' + label
    if student is not None:
        name = NAME.match(q['prompt']).group(1)
        old = re.search(re.escape(name) + r"'s answer: (.*)", q['prompt']).group(1)
        q['prompt'] = q['prompt'].replace(f"{name}'s answer: {old}", f"{name}'s answer: {student}")
        steps[-1] = f"The correct answer is {q['answer']}, not {student}."
    return q


if __name__ == '__main__':
    banks = lib.load()
    for u, d in banks.items():
        d['questions'] = [apply(q) if ('answered this problem incorrectly' in q['prompt'] or q['id'] == 'cal-aoi-s02-honors-011') else q for q in d['questions']]
    lib.save(banks)
    print('labels', len(LABELS))
