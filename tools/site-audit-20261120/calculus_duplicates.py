"""Whole-site audit 2, item #5 (2026-11-20): replace the repeated Calculus items.

38 Calculus questions appeared two to five times in the same skill (identical prompt and answer). The first copy of
each stays; every later copy is rewritten in place as a new problem of the same kind (same id, skill, level, format
and standards). Each new answer is recomputed numerically below before anything is written, and
tools/calculus-audit-20261118/verify_keys.py rechecks the bank with sympy in CI.

Usage: python3 tools/site-audit-20261120/calculus_duplicates.py      (safe to re-run)
"""
import glob, json, math, os, re
from collections import OrderedDict

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
E, PI = math.e, math.pi


def integ(f, a, b, n=20000):
    h = (b - a) / n
    return h / 3 * (f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n)))


def deriv(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


def dist(v, a, b):
    return integ(lambda t: abs(v(t)), a, b, 40000)


def ode_ok(F, y, xs, C=0.7):
    """y(x, C) solves y′ = F(x, y) at the sample points."""
    return all(abs(deriv(lambda s: y(s, C), x0) - F(x0, y(x0, C))) < 1e-5 * max(1, abs(F(x0, y(x0, C)))) for x0 in xs)


def mvt_steps(c):
    return ["The MVT applies: f is continuous on the closed interval and differentiable on the open interval.",
            "Find the average rate (f(b) − f(a))/(b − a), then solve f′(c) = that rate.", f"{c}, which is inside the interval."]


SEP = ["Separate the variables: put every y on the left with dy and every x on the right with dx.", "Integrate both sides and add one constant C."]

# id: (prompt, answer, steps, wrong options for multiple choice or None, numeric check returning True)
NEW = OrderedDict()
NEW["cal-int-s03-cp2-004"] = ("For f(x) = 4x on [0, 2], the right Riemann sum with n equal subintervals simplifies to Rₙ = 8 + 8/n. Which statement is true?",
    "lim (n → ∞) Rₙ = 8, which equals ∫ from 0 to 2 4x dx",
    ["Each term with n in the denominator goes to 0 as n → ∞.", "So lim (n → ∞) Rₙ = 8.", "This limit is the definite integral ∫ from 0 to 2 4x dx; check: the triangle under y = 4x from 0 to 2: (1/2)(2)(8) = 8.",
     "f is increasing on [0, 2], so each right sum overestimates: Rₙ is greater than the integral for every n."],
    ["lim (n → ∞) Rₙ does not exist because Rₙ changes with n", "lim (n → ∞) Rₙ = 16, which equals ∫ from 0 to 2 4x dx", "Rₙ is less than ∫ from 0 to 2 4x dx for every n"],
    lambda: all(abs(sum(4 * (2 * k / n) * (2 / n) for k in range(1, n + 1)) - (8 + 8 / n)) < 1e-9 for n in (3, 7, 20)) and abs(integ(lambda x: 4 * x, 0, 2) - 8) < 1e-9)
NEW["cal-int-s03-honors-003"] = ("For f(x) = x³ on [0, 3], the right Riemann sum with n equal subintervals simplifies to Rₙ = 81/4 + 81/(2n) + 81/(4n²). Find lim (n → ∞) Rₙ.",
    "81/4", ["Each term with n in the denominator goes to 0 as n → ∞.", "So lim (n → ∞) Rₙ = 81/4.", "This limit is the definite integral ∫ from 0 to 3 x³ dx; check: ∫ from 0 to 3 x³ dx = 3⁴/4 = 81/4."], None,
    lambda: all(abs(sum((3 * k / n) ** 3 * (3 / n) for k in range(1, n + 1)) - (81 / 4 + 81 / (2 * n) + 81 / (4 * n * n))) < 1e-9 for n in (3, 7, 20)))
NEW["cal-int-s03-honors-004"] = ("For f(x) = x² on [0, 3], the right Riemann sum with n equal subintervals simplifies to Rₙ = 9 + 27/(2n) + 9/(2n²). Which statement is true?",
    "lim (n → ∞) Rₙ = 9, which equals ∫ from 0 to 3 x² dx",
    ["Each term with n in the denominator goes to 0 as n → ∞.", "So lim (n → ∞) Rₙ = 9.", "This limit is the definite integral ∫ from 0 to 3 x² dx; check: ∫ from 0 to 3 x² dx = 3³/3 = 9.",
     "f is increasing on [0, 3], so each right sum overestimates: Rₙ is greater than the integral for every n."],
    ["lim (n → ∞) Rₙ does not exist because Rₙ changes with n", "lim (n → ∞) Rₙ = 27, which equals ∫ from 0 to 3 x² dx", "Rₙ is less than ∫ from 0 to 3 x² dx for every n"],
    lambda: all(abs(sum((3 * k / n) ** 2 * (3 / n) for k in range(1, n + 1)) - (9 + 27 / (2 * n) + 9 / (2 * n * n))) < 1e-9 for n in (3, 7, 20)))
NEW["cal-int-s04-cp2-010"] = ("Evaluate lim (n → ∞) Σ (k = 1 to n) 6(2k/n) · (2/n) by writing it as a definite integral.", "12",
    ["Δx = 2/n, so the interval has width b − a = 2.", "xₖ = kΔx starts at x = 0, so a = 0 and b = 0 + 2 = 2.", "The function applied to xₖ is f(x) = 6x, so the limit equals ∫ from 0 to 2 6x dx.",
     "Antiderivative: F(x) = 3x². F(2) = 12 and F(0) = 0.", "12 − 0 = 12."], None,
    lambda: abs(sum(6 * (2 * k / 4000) * (2 / 4000) for k in range(1, 4001)) - 12) < 0.01)
NEW["cal-int-s04-cp2-013"] = ("Evaluate lim (n → ∞) Σ (k = 1 to n) (2k/n)² · (2/n) by writing it as a definite integral.", "8/3",
    ["Δx = 2/n, so the interval has width b − a = 2.", "xₖ = kΔx starts at x = 0, so a = 0 and b = 0 + 2 = 2.", "The function applied to xₖ is f(x) = x², so the limit equals ∫ from 0 to 2 x² dx.",
     "Antiderivative: F(x) = (1/3)x³. F(2) = 8/3 and F(0) = 0.", "8/3 − 0 = 8/3."], None,
    lambda: abs(sum((2 * k / 4000) ** 2 * (2 / 4000) for k in range(1, 4001)) - 8 / 3) < 0.01)
# critical numbers
NEW["cal-app-s02-honors-007"] = ("Find the critical numbers of f(x) = x³e^(-x).", "x = 0 or x = 3",
    ["f′(x) = x²(3 - x)e^(-x).", "f′ is defined for every x in the domain, so solve f′(x) = 0.", "x = 0 or x = 3."], ["x = 0", "x = -3 or x = 0", "x = 3"],
    lambda: all(abs(deriv(lambda x: x ** 3 * math.exp(-x), c)) < 1e-6 for c in (0, 3)))
NEW["cal-app-s02-honors-013"] = ("Find the critical numbers of f(x) = x⁴e^x.", "x = -4 or x = 0",
    ["f′(x) = x³(x + 4)e^x.", "f′ is defined for every x in the domain, so solve f′(x) = 0.", "x = -4 or x = 0."], None,
    lambda: all(abs(deriv(lambda x: x ** 4 * math.exp(x), c)) < 1e-6 for c in (-4, 0)))
NEW["cal-app-s02-honors-012"] = ("Find the critical numbers of f(x) = x - 3ln(x).", "x = 3",
    ["f′(x) = (x - 3)/x.", "f′ is defined for every x in the domain, so solve f′(x) = 0.", "x = 3."], None,
    lambda: abs(deriv(lambda x: x - 3 * math.log(x), 3)) < 1e-6)
# increasing intervals
NEW["cal-app-s03-honors-006"] = ("On what interval(s) is f(x) = x + 16/x increasing?", "(-∞, -4) ∪ (4, ∞)",
    ["f′(x) = (x + 4)(x - 4)/(x²).", "f′(x) = 0 at x = -4, 4 (and f′ or f is undefined at x = 0).", "Test the sign of f′ on each interval of the domain.", "f is increasing on (-∞, -4) ∪ (4, ∞)."],
    ["(-4, 0) ∪ (0, 4)", "(0, ∞)", "(-∞, ∞)"],
    lambda: all((deriv(lambda x: x + 16 / x, p) > 0) == (abs(p) > 4) for p in (-6, -4.5, -2, -0.5, 0.5, 2, 4.5, 6)))
NEW["cal-app-s03-honors-005"] = ("On what interval(s) is f(x) = x³e^x increasing?", "(-3, ∞)",
    ["f′(x) = x²(x + 3)e^x.", "f′(x) = 0 at x = -3, 0.", "Test the sign of f′ on each interval of the domain: f′ is negative only for x < -3.", "f is increasing on (-3, ∞)."], None,
    lambda: all((deriv(lambda x: x ** 3 * math.exp(x), p) > 0) == (p > -3) for p in (-6, -4, -2, -0.5, 0.5, 2)))
NEW["cal-app-s03-honors-011"] = ("On what interval(s) is f(x) = xe^(-x) increasing?", "(-∞, 1)",
    ["f′(x) = (1 - x)e^(-x).", "f′(x) = 0 at x = 1.", "Test the sign of f′ on each interval of the domain.", "f is increasing on (-∞, 1)."], None,
    lambda: all((deriv(lambda x: x * math.exp(-x), p) > 0) == (p < 1) for p in (-3, 0, 0.9, 1.1, 4)))
NEW["cal-app-s03-honors-013"] = ("On what interval(s) is f(x) = x²e^(-x) increasing?", "(0, 2)",
    ["f′(x) = x(2 - x)e^(-x).", "f′(x) = 0 at x = 0, 2.", "Test the sign of f′ on each interval of the domain.", "f is increasing on (0, 2)."], None,
    lambda: all((deriv(lambda x: x * x * math.exp(-x), p) > 0) == (0 < p < 2) for p in (-3, -0.1, 0.1, 1, 1.9, 2.1, 5)))
# absolute maxima
NEW["cal-app-s04-honors-005"] = ("Find the absolute maximum of f(x) = x³ - 12x on [-3, 5]. Give the value and where it occurs.", "65 at x = 5",
    ["f′(x) = 3x² - 12; critical number(s) in the interval: -2, 2.", "Candidates test: f(-3) = 9; f(-2) = 16; f(2) = -16; f(5) = 65.", "Absolute maximum: 65 at x = 5."], None,
    lambda: abs(max((-3 + 8 * i / 8000) ** 3 - 12 * (-3 + 8 * i / 8000) for i in range(8001)) - 65) < 1e-9)
NEW["cal-app-s04-honors-013"] = ("Find the absolute maximum of f(x) = x + 2cos(x) on [0, π]. Give the value and where it occurs.", "π/6 + √3 at x = π/6",
    ["f′(x) = 1 - 2sin(x); critical number(s) in the interval: π/6, 5π/6.", "Candidates test: f(0) = 2; f(π/6) = π/6 + √3; f(5π/6) = 5π/6 - √3; f(π) = π - 2.", "Absolute maximum: π/6 + √3 at x = π/6."], None,
    lambda: abs(max(i * PI / 10000 + 2 * math.cos(i * PI / 10000) for i in range(10001)) - (PI / 6 + math.sqrt(3))) < 1e-6)
NEW["cal-app-s04-honors-010"] = ("Find the absolute maximum of f(x) = 4√x - x on [0, 9]. Give the value and where it occurs.", "4 at x = 4",
    ["f′(x) = -1 + 2x^(-1/2); critical number(s) in the interval: 4.", "Candidates test: f(0) = 0; f(4) = 4; f(9) = 3.", "Absolute maximum: 4 at x = 4."], None,
    lambda: abs(max(4 * math.sqrt(9 * i / 9000) - 9 * i / 9000 for i in range(9001)) - 4) < 1e-9)
NEW["cal-app-s04-honors-012"] = ("Find the absolute maximum of f(x) = xe^(-x) on [0, 5]. Give the value and where it occurs.", "e^(-1) at x = 1",
    ["f′(x) = (1 - x)e^(-x); critical number(s) in the interval: 1.", "Candidates test: f(0) = 0; f(1) = e^(-1); f(5) = 5e^(-5).", "Absolute maximum: e^(-1) at x = 1."], None,
    lambda: abs(max(5 * i / 9000 * math.exp(-5 * i / 9000) for i in range(9001)) - 1 / E) < 1e-9)
# particle motion (applications)
NEW["cal-app-s08-honors-003"] = ("A particle moves along a line with position s(t) = 4√t + 2t meters at time t seconds, for t ≥ 0. Find the velocity at t = 1.", "4 m/s",
    ["v(t) = s′(t) = 2 + 2/(√t).", "v(1) = 4 m/s."], None, lambda: abs(deriv(lambda t: 4 * math.sqrt(t) + 2 * t, 1) - 4) < 1e-6)
NEW["cal-app-s08-honors-012"] = ("A particle moves along a line with position s(t) = 6√t + t meters at time t seconds, for t ≥ 0. Find the velocity at t = 9.", "2 m/s",
    ["v(t) = s′(t) = 1 + 3/(√t).", "v(9) = 2 m/s."], ["27 m/s", "4 m/s", "1 m/s"], lambda: abs(deriv(lambda t: 6 * math.sqrt(t) + t, 9) - 2) < 1e-6)
NEW["cal-app-s08-honors-013"] = ("A particle moves along a line with position s(t) = 8√t - t meters at time t seconds, for t ≥ 0. Find the velocity at t = 4.", "1 m/s",
    ["v(t) = s′(t) = -1 + 4/(√t).", "v(4) = 1 m/s."], None, lambda: abs(deriv(lambda t: 8 * math.sqrt(t) - t, 4) - 1) < 1e-6)
NEW["cal-app-s08-honors-007"] = ("A particle moves along a line with position s(t) = 4sin(πt/6) meters at time t seconds, for t ≥ 0. Find the velocity at t = 2.", "π/3 m/s",
    ["v(t) = s′(t) = 2cos(tπ/6)π/3.", "v(2) = π/3 m/s."], None, lambda: abs(deriv(lambda t: 4 * math.sin(PI * t / 6), 2) - PI / 3) < 1e-6)
NEW["cal-app-s08-honors-010"] = ("A particle moves along a line with position s(t) = 6sin(πt/3) meters at time t seconds, for t ≥ 0. Find the velocity at t = 1.", "π m/s",
    ["v(t) = s′(t) = 2πcos(tπ/3).", "v(1) = π m/s."], ["-π m/s", "3√3 m/s", "2π m/s"], lambda: abs(deriv(lambda t: 6 * math.sin(PI * t / 3), 1) - PI) < 1e-6)
NEW["cal-app-s08-honors-009"] = ("A particle moves along a line with position s(t) = 2sin(πt/2) meters at time t seconds, for t ≥ 0. Find the acceleration at t = 1.", "-(π)²/2 m/s²",
    ["v(t) = s′(t) = πcos(tπ/2).", "a(t) = v′(t) = -(π)²sin(tπ/2)/2.", "a(1) = -(π)²/2 m/s²."], None,
    lambda: abs(deriv(lambda t: deriv(lambda s: 2 * math.sin(PI * s / 2), t, 1e-4), 1, 1e-3) + PI ** 2 / 2) < 1e-4)
NEW["cal-app-s08-honors-008"] = ("A particle moves along a line with position s(t) = t²e^(-t) meters at time t seconds, for t ≥ 0. Find the velocity at t = 3.", "-3e^(-3) m/s",
    ["v(t) = s′(t) = t(2 - t)e^(-t).", "v(3) = -3e^(-3) m/s."], ["3e^(-3) m/s", "9e^(-3) m/s", "-e^(-3) m/s"], lambda: abs(deriv(lambda t: t * t * math.exp(-t), 3) + 3 * math.exp(-3)) < 1e-8)
NEW["cal-app-s08-honors-011"] = ("A particle moves along a line with position s(t) = te^(-t) meters at time t seconds, for t ≥ 0. Find the velocity at t = 2.", "-e^(-2) m/s",
    ["v(t) = s′(t) = (1 - t)e^(-t).", "v(2) = -e^(-2) m/s."], None, lambda: abs(deriv(lambda t: t * math.exp(-t), 2) + math.exp(-2)) < 1e-8)
# Mean Value Theorem
NEW["cal-app-s10-honors-007"] = ("Find the value of c guaranteed by the Mean Value Theorem for f(x) = √x on [0, 4].", "c = 1", mvt_steps("c = 1"), ["c = 2", "c = 1/4", "c = 1/2"],
    lambda: abs(1 / (2 * math.sqrt(1)) - (2 - 0) / 4) < 1e-12)
NEW["cal-app-s10-honors-011"] = ("Find the value of c guaranteed by the Mean Value Theorem for f(x) = √x on [1, 9].", "c = 4", mvt_steps("c = 4"), None,
    lambda: abs(1 / (2 * math.sqrt(4)) - (3 - 1) / 8) < 1e-12)
NEW["cal-app-s10-honors-010"] = ("Find the value of c guaranteed by the Mean Value Theorem for f(x) = ln(x) on [1, e²].", "c = (e² - 1)/2", mvt_steps("c = (e² - 1)/2"), None,
    lambda: abs(1 / ((E * E - 1) / 2) - 2 / (E * E - 1)) < 1e-12 and 1 < (E * E - 1) / 2 < E * E)
NEW["cal-app-s10-honors-013"] = ("Find the value of c guaranteed by the Mean Value Theorem for f(x) = e^x on [0, 2].", "c = ln((e² - 1)/2)", mvt_steps("c = ln((e² - 1)/2)"), None,
    lambda: abs(math.exp(math.log((E * E - 1) / 2)) - (E * E - 1) / 2) < 1e-12 and 0 < math.log((E * E - 1) / 2) < 2)
# displacement
NEW["cal-aoi-s04-honors-009"] = ("A particle moves with velocity v(t) = 1/(t + 2) m/s. Find its displacement from t = 0 to t = 4.", "ln(3) m",
    ["Displacement = ∫ from 0 to 4 v(t) dt.", "an antiderivative is s(t) = ln(t + 2).", "s(4) = ln(6) and s(0) = ln(2).", "s(4) − s(0) = ln(6) − ln(2) = ln(3).", "Displacement = ln(3) m."], None,
    lambda: abs(integ(lambda t: 1 / (t + 2), 0, 4) - math.log(3)) < 1e-9)
NEW["cal-aoi-s04-honors-004"] = ("A particle moves with velocity v(t) = 3√t - 2 m/s. Find its displacement from t = 0 to t = 4.", "8 m",
    ["Displacement = ∫ from 0 to 4 v(t) dt.", "an antiderivative is s(t) = 2t^(3/2) - 2t.", "s(4) = 8 and s(0) = 0.", "s(4) − s(0) = 8 − 0 = 8.", "Displacement = 8 m."], ["-8 m", "4 m", "16 m"],
    lambda: abs(integ(lambda t: 3 * math.sqrt(t) - 2, 0, 4, 200000) - 8) < 1e-4)
NEW["cal-aoi-s04-honors-005"] = ("A particle moves with velocity v(t) = 3√t - 1 m/s. Find its displacement from t = 0 to t = 9.", "45 m",
    ["Displacement = ∫ from 0 to 9 v(t) dt.", "an antiderivative is s(t) = 2t^(3/2) - t.", "s(9) = 45 and s(0) = 0.", "s(9) − s(0) = 45 − 0 = 45.", "Displacement = 45 m."], None,
    lambda: abs(integ(lambda t: 3 * math.sqrt(t) - 1, 0, 9, 200000) - 45) < 1e-4)
NEW["cal-aoi-s04-honors-013"] = ("A particle moves with velocity v(t) = 2sin(t) + t m/s. Find its displacement from t = 0 to t = π.", "4 + (π)²/2 m",
    ["Displacement = ∫ from 0 to π v(t) dt.", "an antiderivative is s(t) = t²/2 - 2cos(t).", "s(π) = (π)²/2 + 2 and s(0) = -2.", "s(π) − s(0) = (π)²/2 + 2 − (-2) = 4 + (π)²/2.", "Displacement = 4 + (π)²/2 m."], None,
    lambda: abs(integ(lambda t: 2 * math.sin(t) + t, 0, PI) - (4 + PI ** 2 / 2)) < 1e-9)
# total distance
NEW["cal-aoi-s05-honors-004"] = ("A particle moves with velocity v(t) = t³ - 9t ft/s. Find the total distance traveled from t = 0 to t = 4.", "65/2 ft",
    ["v(t) = 0 at t = 3, so the particle changes direction there.", "Antiderivative: s(t) = t⁴/4 - 9t²/2.", "From t = 0 to t = 3: s(3) − s(0) = -81/4.", "From t = 3 to t = 4: s(4) − s(3) = 49/4.", "Total distance = 81/4 + 49/4 = 65/2 ft."],
    ["8 ft", "-8 ft", "81/4 ft"], lambda: abs(dist(lambda t: t ** 3 - 9 * t, 0, 4) - 32.5) < 1e-5)
NEW["cal-aoi-s05-honors-007"] = ("A particle moves with velocity v(t) = t² - 1 ft/s. Find the total distance traveled from t = 0 to t = 3.", "22/3 ft",
    ["v(t) = 0 at t = 1, so the particle changes direction there.", "Antiderivative: s(t) = t³/3 - t.", "From t = 0 to t = 1: s(1) − s(0) = -2/3.", "From t = 1 to t = 3: s(3) − s(1) = 20/3.", "Total distance = 2/3 + 20/3 = 22/3 ft."], None,
    lambda: abs(dist(lambda t: t * t - 1, 0, 3) - 22 / 3) < 1e-5)
NEW["cal-aoi-s05-honors-008"] = ("A particle moves with velocity v(t) = 2cos(πt/2) ft/s. Find the total distance traveled from t = 0 to t = 2.", "8/π ft",
    ["v(t) = 0 at t = 1, so the particle changes direction there.", "Antiderivative: s(t) = 4sin(tπ/2)/π.", "From t = 0 to t = 1: s(1) − s(0) = 4/π.", "From t = 1 to t = 2: s(2) − s(1) = -4/π.", "Total distance = 4/π + 4/π = 8/π ft."],
    ["0 ft", "4/π ft", "16/π ft"], lambda: abs(dist(lambda t: 2 * math.cos(PI * t / 2), 0, 2) - 8 / PI) < 1e-5)
NEW["cal-aoi-s05-honors-006"] = ("A particle moves with velocity v(t) = 6cos(πt/3) ft/s. Find the total distance traveled from t = 0 to t = 3.", "36/π ft",
    ["v(t) = 0 at t = 3/2, so the particle changes direction there.", "Antiderivative: s(t) = 18sin(tπ/3)/π.", "From t = 0 to t = 3/2: s(3/2) − s(0) = 18/π.", "From t = 3/2 to t = 3: s(3) − s(3/2) = -18/π.", "Total distance = 18/π + 18/π = 36/π ft."],
    ["0 ft", "18/π ft", "72/π ft"], lambda: abs(dist(lambda t: 6 * math.cos(PI * t / 3), 0, 3) - 36 / PI) < 1e-5)
NEW["cal-aoi-s05-honors-009"] = ("A particle moves with velocity v(t) = 2cos(πt) ft/s. Find the total distance traveled from t = 0 to t = 1.", "4/π ft",
    ["v(t) = 0 at t = 1/2, so the particle changes direction there.", "Antiderivative: s(t) = 2sin(tπ)/π.", "From t = 0 to t = 1/2: s(1/2) − s(0) = 2/π.", "From t = 1/2 to t = 1: s(1) − s(1/2) = -2/π.", "Total distance = 2/π + 2/π = 4/π ft."], None,
    lambda: abs(dist(lambda t: 2 * math.cos(PI * t), 0, 1) - 4 / PI) < 1e-5)
NEW["cal-aoi-s05-honors-011"] = ("A particle moves with velocity v(t) = t² - 4t + 3 ft/s. Find the total distance traveled from t = 0 to t = 4.", "4 ft",
    ["v(t) = 0 at t = 1, 3, so the particle changes direction there.", "Antiderivative: s(t) = t³/3 - 2t² + 3t.", "From t = 0 to t = 1: s(1) − s(0) = 4/3.", "From t = 1 to t = 3: s(3) − s(1) = -4/3.", "From t = 3 to t = 4: s(4) − s(3) = 4/3.", "Total distance = 4/3 + 4/3 + 4/3 = 4 ft."], None,
    lambda: abs(dist(lambda t: t * t - 4 * t + 3, 0, 4) - 4) < 1e-5)
NEW["cal-aoi-s05-honors-013"] = ("A particle moves with velocity v(t) = t² - 7t + 6 ft/s. Find the total distance traveled from t = 0 to t = 7.", "53/2 ft",
    ["v(t) = 0 at t = 1, 6, so the particle changes direction there.", "Antiderivative: s(t) = t³/3 - 7t²/2 + 6t.", "From t = 0 to t = 1: s(1) − s(0) = 17/6.", "From t = 1 to t = 6: s(6) − s(1) = -125/6.", "From t = 6 to t = 7: s(7) − s(6) = 17/6.", "Total distance = 17/6 + 125/6 + 17/6 = 53/2 ft."], None,
    lambda: abs(dist(lambda t: t * t - 7 * t + 6, 0, 7) - 53 / 2) < 1e-5)
# acceleration (derivatives unit)
NEW["cal-der-s04-honors-011"] = ("A particle's position is s(t) = e^(-2t) + 3t meters. Find its acceleration at t = 0 seconds.", "4 m/s²",
    ["v(t) = s′(t) = 3 - 2e^(-2t).", "a(t) = v′(t) = 4e^(-2t).", "a(0) = 4 m/s²."], None, lambda: abs(deriv(lambda t: deriv(lambda s: math.exp(-2 * s) + 3 * s, t, 1e-4), 0, 1e-3) - 4) < 1e-4)
NEW["cal-der-s04-honors-008"] = ("A particle's position is s(t) = √t meters. Find its acceleration at t = 9 seconds.", "-1/108 m/s²",
    ["v(t) = s′(t) = 1/(2√t).", "a(t) = v′(t) = -1/(4t^(3/2)).", "a(9) = -1/108 m/s²."], None, lambda: abs(-1 / (4 * 9 ** 1.5) + 1 / 108) < 1e-15 and abs(deriv(lambda t: 1 / (2 * math.sqrt(t)), 9) + 1 / 108) < 1e-8)
# separable differential equations
for qid, F, ans, y, wr in [
        ("cal-deq-s04-honors-006", "ysin(x)", "y = Ce^(-cos(x))", lambda x, C: C * math.exp(-math.cos(x)), None),
        ("cal-deq-s04-honors-010", "2xy", "y = Ce^(x²)", lambda x, C: C * math.exp(x * x), None),
        ("cal-deq-s04-honors-012", "3x²y", "y = Ce^(x³)", lambda x, C: C * math.exp(x ** 3), None),
        ("cal-deq-s05-honors-013", "ye^x", "y = Ce^(e^x)", lambda x, C: C * math.exp(math.exp(x)), None),
        ("cal-deq-s05-honors-009", "x²y²", "y = -3/(x³ + C)", lambda x, C: -3 / (x ** 3 + C), None),
        ("cal-deq-s05-honors-011", "y²cos(x)", "y = -1/(sin(x) + C)", lambda x, C: -1 / (math.sin(x) + C + 2), None),
        ("cal-deq-s04-honors-013", "cos(x)e^(-y)", "y = ln(sin(x) + C)", lambda x, C: math.log(math.sin(x) + C + 1), None),
        ("cal-deq-s05-honors-003", "e^(2x - y)", "y = ln(e^(2x)/2 + C)", lambda x, C: math.log(math.exp(2 * x) / 2 + C), ["y = ln(e^(2x) + C)", "y = Ce^(2x)", "y = 2x + C"]),
        ("cal-deq-s05-honors-012", "e^(3x - y)", "y = ln(e^(3x)/3 + C)", lambda x, C: math.log(math.exp(3 * x) / 3 + C), None),
        ("cal-deq-s04-honors-011", "2y/x", "y = Cx²", lambda x, C: C * x * x, None),
        ("cal-deq-s05-honors-010", "4x√y", "y = (x² + C)²", lambda x, C: (x * x + C + 1) ** 2, None),
        ("cal-deq-s05-honors-007", "2(1 + y²)", "y = tan(2x + C)", lambda x, C: math.tan(2 * x + C), ["y = tan(x + C)", "y = Ce^(2x)", "y = 2x + C"])]:
    fpy = {"ysin(x)": lambda x, v: v * math.sin(x), "2xy": lambda x, v: 2 * x * v, "3x²y": lambda x, v: 3 * x * x * v, "ye^x": lambda x, v: v * math.exp(x),
           "x²y²": lambda x, v: x * x * v * v, "y²cos(x)": lambda x, v: v * v * math.cos(x), "cos(x)e^(-y)": lambda x, v: math.cos(x) * math.exp(-v), "e^(2x - y)": lambda x, v: math.exp(2 * x - v),
           "e^(3x - y)": lambda x, v: math.exp(3 * x - v), "2y/x": lambda x, v: 2 * v / x, "4x√y": lambda x, v: 4 * x * math.sqrt(v), "2(1 + y²)": lambda x, v: 2 * (1 + v * v)}[F]
    NEW[qid] = (f"Find the general solution of y′ = {F}.", ans, SEP + [f"Solve for y: {ans}."], wr, (lambda fpy=fpy, y=y: ode_ok(fpy, y, (0.3, 0.5, 0.8, 1.1))))
NEW["cal-ftc-s02-honors-004"] = ("Find a formula for g(x) = ∫ from 0 to x (3t²e^(t³)) dt.", "g(x) = e^(x³) - 1",
    ["An antiderivative of 3t²e^(t³) is e^(t³).", "g(x) = [e^(t³)] evaluated from t = 0 to t = x = (e^(x³)) − (1).", "g(x) = e^(x³) - 1."], ["g(x) = e^(x³)", "g(x) = 3x²e^(x³)", "g(x) = e^(x³) + 1"],
    lambda: all(abs(integ(lambda t: 3 * t * t * math.exp(t ** 3), 0, x0) - (math.exp(x0 ** 3) - 1)) < 1e-7 for x0 in (0.5, 1, 1.2)))
NEW["cal-lim-s05-honors-011"] = ("Evaluate lim (x → ∞) (3x + cos(x))/x.", "3",
    ["Look at how the top and bottom grow as x moves away from 0.", "Split: 3 + cos(x)/x, and -1/x ≤ cos(x)/x ≤ 1/x → 0 by the Squeeze Theorem.", "The limit is 3."], ["4", "0", "∞"],
    lambda: abs((3 * 1e7 + math.cos(1e7)) / 1e7 - 3) < 1e-6)
NEW["cal-lim-s05-honors-013"] = ("Evaluate lim (x → ∞) (x³ + 1)/e^x.", "0",
    ["Look at how the top and bottom grow as x moves away from 0.", "e^x grows faster than any polynomial (L’Hôpital three times gives 6/e^x → 0).", "The limit is 0."], None,
    lambda: (60 ** 3 + 1) / math.exp(60) < 1e-20)
NEW["cal-lim-s05-honors-009"] = ("Evaluate lim (x → ∞) ln(x)/√x.", "0",
    ["Look at how the top and bottom grow as x moves away from 0.", "ln(x) grows more slowly than √x (L’Hôpital: (1/x)/(1/(2√x)) = 2/√x → 0).", "The limit is 0."], None,
    lambda: math.log(1e30) / 1e15 < 1e-12)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "question-banks", "calculus", "*.json")))
    for qid, (_, _, _, _, ok) in NEW.items():
        assert ok(), qid
    banks, prompts, changed = {}, {}, 0
    for f in files:
        raw = open(f, encoding="utf-8").read()
        banks[f] = (json.loads(raw, object_pairs_hook=OrderedDict), raw)
    for f, (b, _) in banks.items():
        for q in b["questions"]:
            prompts.setdefault(re.sub(r"\s+", " ", q["prompt"]), []).append(q["id"])
    seen = set()
    for f, (b, raw) in banks.items():
        touched = False
        for q in b["questions"]:
            if q["id"] not in NEW:
                continue
            seen.add(q["id"])
            p, a, steps, wrongs, _ = NEW[q["id"]]
            if q["prompt"] == p and q["answer"] == a:
                continue
            others = [i for i in prompts.get(p, []) if i != q["id"]]
            assert not others, (q["id"], others)
            assert (wrongs is None) == (q["format"] != "multiple-choice"), q["id"]
            q["prompt"], q["answer"], q["solutionSteps"] = p, a, steps
            if wrongs:
                assert len(set(wrongs + [a])) == 4, q["id"]
                pos = sum(map(ord, q["id"])) % 4
                opts = [OrderedDict(text=w, correct=False) for w in wrongs]
                opts.insert(pos, OrderedDict(text=a, correct=True))
                q["options"] = opts
            q["sourceNotes"] = (q.get("sourceNotes", "") + " Rewritten 2026-11-20 (whole-site audit 2 #5) to replace a repeated question; answer recomputed by tools/site-audit-20261120/calculus_duplicates.py.").strip()
            touched = True
            changed += 1
        if touched:
            ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(b, fh, ensure_ascii=False, indent=ind)
                if raw.endswith("\n"):
                    fh.write("\n")
    assert seen == set(NEW), set(NEW) - seen
    print(f"{len(NEW)} replacements defined, {changed} written")


if __name__ == "__main__":
    main()
