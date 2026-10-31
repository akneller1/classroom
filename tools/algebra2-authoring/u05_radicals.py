from lib import Bank, graph
from mathlite import *
import math

STD = {1: ["N-RN.A.2"], 2: ["N-RN.A.2"], 3: ["N-RN.A.1", "N-RN.A.2"], 4: ["N-RN.A.1"], 5: ["A-REI.A.2"], 6: ["A-REI.A.2"],
       7: ["F-IF.C.7b"], 8: ["F-BF.B.3", "F-IF.C.7b"]}
B = Bank("radicals-rational-exponents", "rr", STD)
sq = math.sqrt


def cbfree(n):
    s = -1 if n < 0 else 1; n = abs(n); k, m, p = 1, n, 2
    while p ** 3 <= m:
        while m % p ** 3 == 0: m //= p ** 3; k *= p
        p += 1
    return s * k, m


def crad(n):
    k, m = cbfree(n)
    return str(k) if m == 1 else (f"{'' if k == 1 else '-' if k == -1 else k}∛{m}")


def num_ok(s, v):
    return abs(peval(s.replace("∛", "cbrt")) - v) < 1e-9 if "∛" not in s else True


# ---------------- Skill 1: simplifying radicals ----------------
S = 1
for n_, lvl in [(48, "cp2"), (75, "cp2"), (98, "cp2"), (180, "cp1"), (200, "cp2"), (128, "cp1"), (243, "cp1"), (500, "cp1")]:
    k, m = sqfree(n_); assert k * k * m == n_
    B.sa(S, lvl, f"Simplify √{n_}.", rad(n_), [f"Largest perfect-square factor: {k * k}.", f"√{n_} = √{k * k}·√{m} = {rad(n_)}."])
for n_ in [54, -24, 250, 40, -128, 81]:
    k, m = cbfree(n_); assert k ** 3 * m == n_
    B.sa(S, "cp1", f"Simplify ∛({n_}).", crad(n_), [f"Largest perfect-cube factor: {k ** 3}.", f"∛({n_}) = {crad(n_)}."])
for n_, d in [(5, 3), (7, 2), (2, 5)]:
    ans = f"√{n_ * d}/{d}"
    B.mc(S, "cp1", f"Rationalize the denominator: √{n_}/√{d}.", ans, [f"√{n_}/{d}", f"{n_}/{d}", f"√{n_ * d}"], [f"Multiply numerator and denominator by √{d}.", f"√{n_}·√{d}/{d} = {ans}."])
    assert abs(sq(n_) / sq(d) - sq(n_ * d) / d) < 1e-12
for e, ans, chk in [("√(50x³), x ≥ 0", "5x√(2x)", lambda v: 5 * v * sq(2 * v) - sq(50 * v ** 3)), ("√(72x⁴y⁵), y ≥ 0", "6x²y²√(2y)", None),
                    ("∛(16x⁵)", "2x∛(2x²)", lambda v: 2 * v * (2 * v * v) ** (1 / 3) - (16 * v ** 5) ** (1 / 3)), ("√(45a²b), a ≥ 0", "3a√(5b)", None),
                    ("∜(32x⁸)", "2x²∜2", lambda v: 2 * v * v * 2 ** 0.25 - (32 * v ** 8) ** 0.25)]:
    if chk: assert abs(chk(1.7)) < 1e-9
    B.sa(S, "honors" if "y" in e or "∜" in e else "cp1", f"Simplify {e}.", ans, ["Split each factor into the largest perfect power for the index and a remainder.", f"Take the perfect powers out: {ans}."])
B.mc(S, "cp1", "A student writes √(9 + 16) = √9 + √16 = 7. What is correct?", "√25 = 5", ["7", "√7", "25"], ["√(a + b) ≠ √a + √b in general.", "Add first: √25 = 5."], tags=["error-analysis", "misconception"])
B.mc(S, "cp2", "Which radical is in simplest form?", "√30", ["√12", "√50", "√18"], ["30 = 2·3·5 has no square factor > 1.", "12 = 4·3, 50 = 25·2, 18 = 9·2."])
sel_auto(B, S, "cp1", "Select ALL expressions equal to 6√2.", ["√72", "2√18", "3√8", "√36·√2", "√12", "6√4", "12√1/2"],
         lambda s: abs(peval(s.replace("12√1/2", "12*sqrt(1/2)")) - 6 * sq(2)) < 1e-9, ["6√2 = √(36·2) = √72.", "2√18 = 2·3√2; 3√8 = 3·2√2; 12√(1/2) = 12/√2 = 6√2."])
sel_auto(B, S, "honors", "Select ALL expressions that are already in simplest radical form.", ["√15", "3√7", "√(2/3)", "1/√5", "√27", "∛4", "∛16"],
         lambda s: s in ("√15", "3√7", "∛4"), ["Simplest form: no perfect-power factors under the radical, no fractions under the radical, no radicals in a denominator.", "√(2/3) and 1/√5 need rationalizing; √27 = 3√3; ∛16 = 2∛2."], tags=["reasoning"])
B.sa(S, "honors", "Rationalize: 6/(3 - √3).", "3 + √3", ["Multiply by the conjugate (3 + √3).", "6(3 + √3)/(9 - 3) = 3 + √3."])
assert abs(6 / (3 - sq(3)) - (3 + sq(3))) < 1e-12
B.sa(S, "honors", "Rationalize: (1 + √2)/(1 - √2).", "-3 - 2√2", ["Multiply by (1 + √2)/(1 + √2).", "(1 + √2)²/(1 - 2) = -(3 + 2√2)."])
assert abs((1 + sq(2)) / (1 - sq(2)) - (-3 - 2 * sq(2))) < 1e-12
B.sa(S, "honors", "Rationalize: 5/∛2.", "5∛4/2", ["Multiply by ∛4/∛4 so the denominator is ∛8 = 2."])
assert abs(5 / 2 ** (1 / 3) - 5 * 4 ** (1 / 3) / 2) < 1e-12
B.orq(S, "cp1", "Simplify √288 step by step.",
      [("Write 288 as a product of primes.", "2⁵·3²"), ("Find the largest perfect-square factor.", "144"), ("Simplify √288.", "12√2"), ("Approximate to the nearest tenth.", "17.0")],
      ["288 = 32·9 = 2⁵·3².", "2⁴·3² = 144.", "√144·√2.", f"12·1.414… ≈ {12 * sq(2):.1f}."])
B.orq(S, "honors", "Compare √(a²) and (√a)².",
      [("Evaluate √((-5)²).", "5"), ("Is (√(-5))² a real number computation?", "No; √(-5) is not real"), ("Write √(x²) for any real x.", "|x|"), ("Simplify √(x² - 6x + 9) for x < 3.", "3 - x")],
      ["√25 = 5.", "√(-5) = i√5 is not real.", "The principal root is nonnegative.", "√((x - 3)²) = |x - 3| = 3 - x when x < 3."], tags=["reasoning", "challenge"])
B.sa(S, "cp2", "Simplify √(x⁶) for x ≥ 0.", "x³", ["(x³)² = x⁶."])

# ---------------- Skill 2: operations with radicals ----------------
S = 2
for a, b, c, d, lvl in [(3, 2, 5, 2, "cp2"), (4, 3, -7, 3, "cp2"), (2, 12, 1, 27, "cp1"), (1, 50, 3, 8, "cp1"), (5, 20, -2, 45, "cp1"), (2, 18, -1, 32, "cp1")]:
    k1, m1 = sqfree(b); k2, m2 = sqfree(d); assert m1 == m2
    tot = a * k1 + c * k2; ans = rad(m1, tot) if tot not in (0,) else "0"
    expr = f"{a if a != 1 else ''}√{b} {'+' if c > 0 else '-'} {abs(c) if abs(c) != 1 else ''}√{d}"
    B.sa(S, lvl, f"Simplify {expr}.", ans, ["Simplify each radical first.", f"{a}√{b} = {rad(b, a)} and {c}√{d} = {rad(d, c)}.", f"Combine like radicals: {ans}."])
    assert abs(a * sq(b) + c * sq(d) - tot * sq(m1)) < 1e-9
for p_, q_ in [((2, 3), (1, 3)), ((1, 5), (-1, 5)), ((3, 2), (2, 2)), ((2, 1), (3, -1))]:
    # (p0 + p1√m)(q0 + q1√m) with m=7
    m = 7 if p_ != (2, 1) else 3
    A0, A1 = p_; C0, C1 = q_
    real = A0 * C0 + A1 * C1 * m; irr = A0 * C1 + A1 * C0
    ans = f"{real}" + ("" if irr == 0 else (f" + {irr if irr != 1 else ''}√{m}" if irr > 0 else f" - {-irr if irr != -1 else ''}√{m}"))
    B.sa(S, "cp1", f"Multiply: ({A0} + {A1 if A1 != 1 else ''}√{m})({C0} {'+' if C1 > 0 else '-'} {abs(C1) if abs(C1) != 1 else ''}√{m}).", ans,
         ["Use FOIL.", f"√{m}·√{m} = {m}.", f"Combine: {ans}."])
    assert abs((A0 + A1 * sq(m)) * (C0 + C1 * sq(m)) - (real + irr * sq(m))) < 1e-9
for a, b in [(6, 10), (3, 15), (12, 6), (5, 20)]:
    pr = a * b
    B.mc(S, "cp2", f"Simplify √{a}·√{b}.", rad(pr), [f"√{a + b}", f"{pr}", f"{sqfree(pr)[0] + 1}√{sqfree(pr)[1]}"], ["√a·√b = √(ab) for a, b ≥ 0.", f"√{pr} = {rad(pr)}."])
B.mc(S, "cp1", "A student writes 3√2 + 4√3 = 7√5. What is correct?", "It cannot be combined; 3√2 + 4√3 is simplest", ["7√5", "7√6", "12√6"], ["Only like radicals (same index and radicand) combine."], tags=["error-analysis", "misconception"])
B.mc(S, "cp1", "Which expression equals (√5 + √2)²?", "7 + 2√10", ["7", "5 + 2", "7 + √10"], ["(a + b)² = a² + 2ab + b².", "5 + 2√10 + 2."], tags=["misconception"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to 4√3.", ["√3 + 3√3", "2√12", "√48", "√12 + √12", "√3·√4", "2√6", "4 + √3", "√27 - √3 + √12"],
         lambda s: abs(peval(s) - 4 * sq(3)) < 1e-9, ["Simplify each expression to a multiple of √3.", "√48 = 4√3; √12 + √12 = 4√3; √27 - √3 + √12 = 3√3 - √3 + 2√3."])
sel_auto(B, S, "honors", "Select ALL expressions that are rational numbers.", ["(3 + √2)(3 - √2)", "(√5)²", "√8·√2", "√2 + √2", "(1 + √3)²", "√12/√3", "∛4·∛2"],
         lambda s: abs(peval(s.replace("∛4·∛2", "2")) - round(peval(s.replace("∛4·∛2", "2")).real)) < 1e-9 or s == "∛4·∛2",
         ["Conjugate products and perfect squares give rational numbers: 7, 5, 4, 2, 2.", "√2 + √2 = 2√2 and (1 + √3)² = 4 + 2√3 are irrational."], tags=["reasoning"])
for a, b, c in [(2, 5, 3), (1, 7, 2), (4, 2, 1)]:
    ev = f"({a} + √{b})({a} - √{b})"; val = a * a - b
    B.sa(S, "cp1", f"Multiply {ev}.", str(val), ["Conjugates: (x + y)(x - y) = x² - y².", f"{a * a} - {b} = {val}."])
B.sa(S, "honors", "Simplify (√6 + √2)/(√6 - √2).", "2 + √3", ["Multiply by the conjugate (√6 + √2).", "(6 + 2√12 + 2)/(6 - 2) = (8 + 4√3)/4."])
assert abs((sq(6) + sq(2)) / (sq(6) - sq(2)) - (2 + sq(3))) < 1e-12
B.sa(S, "honors", "Simplify 2∛54 - ∛16 + ∛250.", "9∛2", ["2·3∛2 - 2∛2 + 5∛2.", "(6 - 2 + 5)∛2 = 9∛2."])
assert abs(2 * 54 ** (1 / 3) - 16 ** (1 / 3) + 250 ** (1 / 3) - 9 * 2 ** (1 / 3)) < 1e-9
B.orq(S, "cp1", "A rectangle has length 3 + √5 cm and width 3 - √5 cm.",
      [("Find the area.", "4 cm²"), ("Find the perimeter.", "12 cm"), ("Find the length of a diagonal.", "2√7 cm"), ("Is the area rational or irrational?", "rational")],
      ["(3 + √5)(3 - √5) = 9 - 5.", "2(3 + √5 + 3 - √5) = 12.", "d² = (3 + √5)² + (3 - √5)² = 14 + 14 = 28; d = 2√7.", "4 is rational."], tags=["modeling", "connections"])
assert abs((3 + sq(5)) ** 2 + (3 - sq(5)) ** 2 - 28) < 1e-9
B.orq(S, "honors", "Let a = 2 + √3.",
      [("Find a².", "7 + 4√3"), ("Find 1/a in simplest form.", "2 - √3"), ("Find a + 1/a.", "4"), ("Find a² + 1/a².", "14")],
      ["(2 + √3)² = 4 + 4√3 + 3.", "Multiply by the conjugate; denominator 4 - 3 = 1.", "(2 + √3) + (2 - √3).", "(a + 1/a)² - 2 = 16 - 2."], tags=["challenge"])
B.sa(S, "cp2", "Simplify √3·√27.", "9", ["√81 = 9."])
B.sa(S, "cp2", "Simplify 5√7 - 2√7 + √7.", "4√7", ["Combine coefficients: 5 - 2 + 1 = 4."])

# ---------------- Skill 3: rational exponents ----------------
S = 3
for b, p, q, lvl in [(27, 2, 3, "cp2"), (16, 3, 4, "cp2"), (32, 2, 5, "cp1"), (81, 3, 4, "cp1"), (125, -2, 3, "cp1"), (64, -5, 6, "honors"), (F(8, 27), 2, 3, "honors"), (F(9, 4), -3, 2, "honors")]:
    val = F(b) ** F(p, q) if False else None
    rt = round(float(b) ** (1 / q)) if F(b).denominator == 1 else F(round(F(b).numerator ** (1 / q)), round(F(b).denominator ** (1 / q)))
    val = F(rt) ** p
    assert abs(float(b) ** (p / q) - float(val)) < 1e-9
    B.sa(S, lvl, f"Evaluate {frp(b)}^({p}/{q}).", fr(val), [f"Take the {q}th root first: {fr(rt)}.", f"Raise to the power {p}: {fr(val)}." + (" A negative exponent means reciprocal." if p < 0 else "")])
for e, ans, chk in [("x^(1/2)·x^(1/3)", "x^(5/6)", (1 / 2 + 1 / 3, 5 / 6)), ("(x^(2/3))³", "x²", (2, 2)), ("x^(3/4)/x^(1/4)", "x^(1/2)", (0.5, 0.5)), ("(8x⁶)^(1/3)", "2x²", None),
                    ("(16x⁴y⁸)^(1/4)", "2xy²", None), ("x^(-2/3)·x^(5/3)", "x", (1, 1)), ("(x^(1/2)y^(-1))²", "x/y²", None), ("(27x^(-3))^(-1/3)", "x/3", None)]:
    for v in (1.3, 2.7):
        lhs = peval(e.replace("^", "**").replace("**(", "**("), x=v, y=1.9); rhs = peval(ans, x=v, y=1.9)
        assert same(lhs, rhs, 1e-7), (e, lhs, rhs)
    B.sa(S, "cp1" if "y" not in e else "honors", f"Simplify {e}. Assume variables are positive.", ans, ["Use exponent rules: add exponents when multiplying, subtract when dividing, multiply for a power of a power.", f"Result: {ans}."])
B.mc(S, "cp1", "A student evaluates 16^(-1/2) = -4. What is correct?", "1/4", ["-4", "-1/4", "8"], ["A negative exponent means reciprocal, not a negative number.", "16^(-1/2) = 1/√16 = 1/4."], tags=["error-analysis", "misconception"])
B.mc(S, "cp1", "Which is NOT a real number?", "(-16)^(1/4)", ["(-8)^(1/3)", "16^(-1/4)", "(-32)^(1/5)"], ["Even roots of negative numbers are not real.", "(-8)^(1/3) = -2, 16^(-1/4) = 1/2, (-32)^(1/5) = -2."])
sel_auto(B, S, "cp1", "Select ALL expressions equal to 4.", ["64^(1/3)", "8^(2/3)", "16^(1/2)", "2^(4/2)", "32^(2/5)", "(1/2)^(-2)", "256^(1/2)", "4^(1/2)"],
         lambda s: abs(peval(s) - 4) < 1e-9, ["Rewrite each as a root then a power.", "64^(1/3) = 4, 8^(2/3) = 4, 16^(1/2) = 4, 2² = 4, 32^(2/5) = 4, (1/2)^(-2) = 4."])
sel_auto(B, S, "honors", "Select ALL expressions equivalent to x^(3/2) for x > 0.", ["(√x)³", "√(x³)", "x√x", "x³/²·1" if False else "(x³)^(1/2)", "∛(x²)", "x^(3)/x^(1/2)", "x^(2/3)"],
         lambda s: abs(peval(s.replace("∛(x²)", "x**(2/3)"), x=2.3) - 2.3 ** 1.5) < 1e-9, ["x^(m/n) = (ⁿ√x)^m = ⁿ√(x^m).", "x√x = x^(1 + 1/2); x³/x^(1/2) = x^(5/2)."])
B.sa(S, "honors", "Solve x^(3/2) = 27.", "x = 9", ["Raise both sides to the 2/3 power.", "27^(2/3) = 9."])
B.sa(S, "honors", "Solve x^(2/3) = 16.", "x = ±64", ["Raise both sides to the 3/2 power with ± (even power).", "(x^(1/3))² = 16 → x^(1/3) = ±4 → x = ±64."], tags=["challenge"])
assert (-64) ** 2 == 64 ** 2 and round(64 ** (1 / 3)) == 4
B.orq(S, "cp1", "Explore 8^(2/3).",
      [("Write it as a root of a power.", "∛(8²) = ∛64"), ("Write it as a power of a root.", "(∛8)²"), ("Evaluate.", "4"), ("Which form is easier mentally? Why?", "(∛8)²: take the root first to keep numbers small")],
      ["a^(m/n) = ⁿ√(a^m).", "a^(m/n) = (ⁿ√a)^m.", "∛8 = 2; 2² = 4.", "Smaller intermediate numbers."])
B.orq(S, "honors", "Show the exponent rules are consistent with roots.",
      [("Use (a^(1/2))² = a to explain why a^(1/2) = √a.", "Both square to a and are nonnegative"), ("Evaluate 9^(1/2)·9^(1/2).", "9"), ("Evaluate (9^(1/2))^4.", "81"), ("Explain why (-8)^(2/6) ≠ (-8)^(1/3) using real roots.", "(-8)^(2/6) = ⁶√64 = 2 but (-8)^(1/3) = -2")],
      ["Power rule.", "9^(1/2 + 1/2) = 9.", "3⁴ = 81.", "Rational exponent rules require base ≥ 0 or fractions in lowest terms."], tags=["reasoning", "challenge"])

# ---------------- Skill 4: converting between radicals and exponents ----------------
S = 4
for rexp, eexp in [("√x", "x^(1/2)"), ("∛(x²)", "x^(2/3)"), ("⁵√(x³)", "x^(3/5)"), ("(∜x)³", "x^(3/4)"), ("1/√x", "x^(-1/2)"), ("√(x⁵)", "x^(5/2)"), ("1/∛(x⁴)", "x^(-4/3)"), ("∜(x⁸)", "x²")]:
    B.sa(S, "cp2" if rexp in ("√x", "∛(x²)", "(∜x)³") else "cp1", f"Write {rexp} using a rational exponent.", eexp, ["ⁿ√(x^m) = x^(m/n); a radical in a denominator gives a negative exponent.", f"{rexp} = {eexp}."])
for eexp, rexp in [("x^(2/5)", "⁵√(x²)"), ("y^(3/2)", "√(y³)"), ("7^(1/3)", "∛7"), ("(2x)^(3/4)", "∜((2x)³)"), ("x^(-1/3)", "1/∛x"), ("5x^(1/2)", "5√x")]:
    wrong = [rexp.replace("⁵√(x²)", "√(x⁵)"), "(" + eexp + ")" if False else "∛(x²)" if "2/5" in eexp else rexp + "²"]
    B.mc(S, "cp1", f"Which radical form equals {eexp}?", rexp, [
        {"x^(2/5)": "√(x⁵)", "y^(3/2)": "∛(y²)", "7^(1/3)": "√(7³)", "(2x)^(3/4)": "2∜(x³)", "x^(-1/3)": "-∛x", "5x^(1/2)": "√(5x)"}[eexp],
        {"x^(2/5)": "2⁵√x", "y^(3/2)": "(3/2)y", "7^(1/3)": "7/3", "(2x)^(3/4)": "∛((2x)⁴)", "x^(-1/3)": "∛(-x)", "5x^(1/2)": "5x/2"}[eexp],
        {"x^(2/5)": "x²/5", "y^(3/2)": "√y·3", "7^(1/3)": "1/∛7", "(2x)^(3/4)": "(2x)³/4", "x^(-1/3)": "x³", "5x^(1/2)": "√5·x"}[eexp]],
         ["Denominator of the exponent = index; numerator = power.", "A coefficient outside parentheses is not under the radical." if "5x" in eexp or "(2x)" in eexp else "Negative exponent → reciprocal." if "-" in eexp else "x^(m/n) = ⁿ√(x^m)."])
B.sa(S, "cp1", "Write √x·∛x as a single power of x.", "x^(5/6)", ["x^(1/2)·x^(1/3) = x^(3/6 + 2/6)."])
B.sa(S, "honors", "Write ∜(x·√x) as a single power of x.", "x^(3/8)", ["x·x^(1/2) = x^(3/2).", "(x^(3/2))^(1/4) = x^(3/8)."], tags=["challenge"])
assert abs((2.2 * sq(2.2)) ** 0.25 - 2.2 ** (3 / 8)) < 1e-12
B.sa(S, "honors", "Write √(x∛x) as a single power of x.", "x^(2/3)", ["x·x^(1/3) = x^(4/3).", "(x^(4/3))^(1/2) = x^(2/3)."])
B.sa(S, "cp1", "Write ∛(x⁴)/√x as a single power of x.", "x^(5/6)", ["x^(4/3 - 1/2) = x^(8/6 - 3/6)."])
sel_auto(B, S, "cp1", "Select ALL expressions equal to ∛(x²) for x > 0.", ["x^(2/3)", "(∛x)²", "(x²)^(1/3)", "x^(3/2)", "(x^(1/3))²", "x²/3", "√(x³)"],
         lambda s: abs(peval(s.replace("∛x", "x**(1/3)"), x=2.9) - 2.9 ** (2 / 3)) < 1e-9, ["ⁿ√(x^m) = x^(m/n) = (ⁿ√x)^m."])
sel_auto(B, S, "honors", "Select ALL expressions equal to 1/√(x³) for x > 0.", ["x^(-3/2)", "(x^(-1/2))³", "1/(x√x)", "x^(-2/3)", "-x^(3/2)", "(1/x)^(3/2)"],
         lambda s: abs(peval(s, x=1.7) - 1.7 ** -1.5) < 1e-9, ["Radical in the denominator → negative exponent.", "x√x = x^(3/2)."])
B.mc(S, "cp1", "A student rewrites 4x^(1/2) as √(4x). What is the error?", "Only x is raised to 1/2: 4x^(1/2) = 4√x", ["No error", "It equals 2√x", "It equals √4·x"], ["The exponent applies only to x.", "√(4x) = 2√x ≠ 4√x."], tags=["error-analysis"])
B.orq(S, "cp1", "Rewrite and simplify (√x)³·∛(x²) for x > 0.",
      [("Write (√x)³ with a rational exponent.", "x^(3/2)"), ("Write ∛(x²) with a rational exponent.", "x^(2/3)"), ("Multiply.", "x^(13/6)"), ("Write the result as a radical.", "⁶√(x¹³) = x²·⁶√x")],
      ["(x^(1/2))³.", "Index 3, power 2.", "3/2 + 2/3 = 13/6.", "x^(13/6) = x^(2 + 1/6)."])
B.orq(S, "honors", "A cube has volume V cm³.",
      [("Write the edge length using a radical.", "∛V"), ("Write it with a rational exponent.", "V^(1/3)"), ("Write the surface area in terms of V.", "6V^(2/3)"), ("Find the surface area when V = 64.", "96 cm²")],
      ["s³ = V.", "∛V = V^(1/3).", "6s² = 6(V^(1/3))².", "6·16 = 96."], tags=["modeling"])
B.mc(S, "cp2", "Which equals x^(1/4)?", "∜x", ["x/4", "4√x", "x⁴"], ["The denominator 4 is the index."])

# ---------------- Skill 5: solving radical equations ----------------
S = 5
for a, b, c, lvl in [(1, 3, 5, "cp2"), (2, -1, 3, "cp2"), (3, 1, 4, "cp1"), (1, -6, 2, "cp2"), (5, 4, 7, "cp1")]:
    xv = F(c * c - b, a)
    B.sa(S, lvl, f"Solve √({a if a != 1 else ''}x {'+' if b > 0 else '-'} {abs(b)}) = {c}.", f"x = {fr(xv)}", ["Square both sides.", f"{a}x + {b} = {c * c} → x = {fr(xv)}.", "Check: the radicand is nonnegative and the root equals the right side."])
for a, b, c in [(1, 2, 3), (2, -3, -2), (1, -1, 4), (3, 0, 2)]:
    xv = F(c ** 3 - b, a)
    B.sa(S, "cp1", f"Solve ∛({a if a != 1 else ''}x{'' if b == 0 else (' + ' if b > 0 else ' - ') + str(abs(b))}) = {c}.", f"x = {fr(xv)}", ["Cube both sides.", f"x = {fr(xv)}.", "Cube roots allow negative values, so no extraneous solutions arise from cubing."])
    assert a * xv + b == c ** 3
for c, r1, r2 in [(0, 4, 1), (-1, 5, 2), (2, 2, -1), (-3, 7, 4), (1, 3, 0)]:
    a = r1 + r2 + 2 * c; b = c * c - r1 * r2; sols = [r for r in (r1, r2) if r + c >= 0]
    rhs = "x" if c == 0 else f"x {'+' if c > 0 else '-'} {abs(c)}"
    lhs = f"√({a if a != 1 else ''}x {'+' if b >= 0 else '-'} {abs(b)})" if b != 0 else f"√({a}x)"
    for r in (r1, r2):
        assert (a * r + b >= 0) and ((sq(a * r + b) - (r + c)) < 1e-9 if r + c >= 0 else True)
    ans = " or ".join(f"x = {s}" for s in sorted(sols)) if sols else "no solution"
    B.sa(S, "cp1" if len(sols) == 2 else "honors", f"Solve {lhs} = {rhs}.", ans,
         ["Square both sides.", f"{P.coeffs(1, 2 * c - a, c * c - b)} = 0 → x = {r1} or x = {r2}.", "Check each in the original equation; " + ("both work." if len(sols) == 2 else f"keep {ans}.")])
B.sa(S, "cp1", "Solve 2√(x - 1) + 3 = 11.", "x = 17", ["Isolate the radical: √(x - 1) = 4.", "x - 1 = 16 → x = 17."])
B.sa(S, "cp1", "Solve √(3x + 1) = √(x + 9).", "x = 4", ["Square: 3x + 1 = x + 9 → x = 4.", "Check: √13 = √13."])
B.sa(S, "honors", "Solve √(x + 7) - √x = 1.", "x = 9", ["√(x + 7) = 1 + √x; square: x + 7 = 1 + 2√x + x.", "√x = 3 → x = 9; check: 4 - 3 = 1."], tags=["challenge"])
B.sa(S, "honors", "Solve (x + 2)^(2/3) = 9.", "x = 25 or x = -29", ["(x + 2) = ±9^(3/2) = ±27.", "x = 25 or x = -29."])
for v in (25, -29): assert abs(abs(v + 2) ** (2 / 3) - 9) < 1e-9
B.mc(S, "cp1", "What is the first step to solve √(x + 5) - 2 = 4?", "Add 2 to both sides to isolate the radical", ["Square both sides", "Subtract 5", "Divide by √x"], ["Isolate the radical before squaring; otherwise squaring creates a cross term."])
sel_auto(B, S, "cp1", "Select ALL solutions of √(4x + 5) = x + 2.", ["1", "-1", "5", "-5", "0", "-2"], lambda s: (4 * int(s) + 5 >= 0) and abs(sq(4 * int(s) + 5) - int(s) - 2) < 1e-9,
         ["Square: 4x + 5 = x² + 4x + 4 → x² = 1 → x = ±1.", "Check: √9 = 3 = 1 + 2 ✓; √1 = 1 = -1 + 2 ✓.", "-2 makes the radicand negative; 0, 5, -5 fail."], tags=["error-analysis"])
B.orq(S, "cp1", "Solve √(x + 10) = x - 2.",
      [("Square both sides.", "x + 10 = x² - 4x + 4"), ("Solve the quadratic.", "x = 6 or x = -1"), ("Check x = 6.", "√16 = 4 = 6 - 2 ✓"), ("Check x = -1 and state the solution set.", "√9 = 3 ≠ -3; solution x = 6")],
      ["(x - 2)² = x² - 4x + 4.", "x² - 5x - 6 = (x - 6)(x + 1).", "Works.", "Extraneous."], tags=["multistep"])
B.orq(S, "honors", "The period of a pendulum is T = 2π√(L/9.8) seconds (L in meters).",
      [("Solve the formula for L.", "L = 9.8(T/(2π))²"), ("Find L for T = 2 s (nearest hundredth).", f"{9.8 * (2 / (2 * math.pi)) ** 2:.2f} m"), ("By what factor must L change to double T?", "4"), ("Find T for L = 1 m (nearest hundredth).", f"{2 * math.pi * sq(1 / 9.8):.2f} s")],
      ["Divide by 2π, square, multiply by 9.8.", "Substitute.", "T ∝ √L.", "Substitute."], tags=["modeling"])

# ---------------- Skill 6: extraneous solutions ----------------
S = 6
for c, r1, r2 in [(-2, 6, 1), (0, 3, -2), (-4, 9, 5), (1, 2, -3), (-1, 4, -2), (3, 1, -6)]:
    a = r1 + r2 + 2 * c; b = c * c - r1 * r2
    rhs = "x" if c == 0 else f"x {'+' if c > 0 else '-'} {abs(c)}"
    lhs = f"√({a if a != 1 else ''}x {'+' if b >= 0 else '-'} {abs(b)})"
    good = [r for r in (r1, r2) if r + c >= 0]; bad = [r for r in (r1, r2) if r + c < 0]
    if not bad or a == 0: continue
    B.mc(S, "cp1", f"Solving {lhs} = {rhs} by squaring gives x = {r1} and x = {r2}. Which is extraneous?", f"x = {bad[0]}",
         [f"x = {good[0]}" if good else f"x = {r1 + 1}", "Neither", "Both"], [f"Check x = {bad[0]}: the right side is {bad[0] + c} < 0, but a square root is never negative.", f"So x = {bad[0]} is extraneous."])
B.mc(S, "cp2", "What is an extraneous solution?", "A solution of a transformed equation that does not satisfy the original equation", ["A solution that is a fraction", "A complex solution", "A solution larger than 100"], ["Squaring can introduce solutions that fail the original."])
B.mc(S, "cp1", "Why can squaring both sides create extraneous solutions?", "a² = b² is true when a = -b, not only when a = b", ["Squaring changes the domain to all reals", "Squaring always doubles the number of solutions", "Squaring is not allowed with radicals"], ["(-3)² = 3², so equations with opposite sides become equal after squaring."], tags=["reasoning"])
for eq, ans, steps in [("√(x + 4) = -3", "no solution", ["A principal square root cannot be negative.", "Squaring gives x = 5, but √9 = 3 ≠ -3."]),
                       ("√(x - 3) + 5 = 2", "no solution", ["√(x - 3) = -3, impossible.", "x = 12 from squaring is extraneous."]),
                       ("x = √(6 - x)", "x = 2", ["x² + x - 6 = 0 → x = 2 or -3.", "x = -3 gives -3 = 3 ✗."]),
                       ("√(4x + 5) = x + 2", "x = -1 or x = 1", ["4x + 5 = x² + 4x + 4 → x² = 1.", "Both check: √1 = 1 and √9 = 3."]),
                       ("√(x + 2) = x - 4", "x = 7", ["x + 2 = x² - 8x + 16 → x² - 9x + 14 = 0 → x = 7 or 2.", "x = 2: √4 = 2 ≠ -2 ✗."]),
                       ("√(2x - 1) = √(x - 4)", "no solution", ["2x - 1 = x - 4 → x = -3.", "x = -3 makes both radicands negative ✗."]),
                       ("√(x + 1) + √(x - 4) = 5", "x = 8", ["√(x + 1) = 5 - √(x - 4); square: x + 1 = 25 - 10√(x - 4) + x - 4.", "√(x - 4) = 2 → x = 8; check 3 + 2 = 5."]),
                       ("x - √x - 6 = 0", "x = 9", ["Let u = √x: u² - u - 6 = 0 → u = 3 or u = -2.", "√x = -2 is impossible; x = 9."])]:
    B.sa(S, "cp1" if "+ √" not in eq and "u" not in steps[0] else "honors", f"Solve {eq}. Identify any extraneous solutions.", ans, steps)
for xx in (-1, 1): assert sq(4 * xx + 5) == xx + 2
assert sq(9) + sq(4) == 5 and 9 - 3 - 6 == 0
sel_auto(B, S, "cp1", "Select ALL equations that have NO real solution.", ["√x = -4", "√(x - 1) + 3 = 0", "√x + 2 = 5", "∛x = -2", "√(x² + 1) = 0", "√(x + 9) = 1"],
         lambda s: s in ("√x = -4", "√(x - 1) + 3 = 0", "√(x² + 1) = 0"), ["Isolate the root: a principal square root cannot be negative; x² + 1 > 0 always.", "∛x = -2 → x = -8 works; √x = 3 → x = 9; √(x + 9) = 1 → x = -8."], tags=["reasoning"])
sel_auto(B, S, "honors", "Squaring √(x + 3) = x + 1 gives x² + x - 2 = 0. Select ALL true statements.", ["x = 1 is a solution", "x = -2 is extraneous", "The equation has exactly one solution", "x = -2 is a solution", "Both roots are extraneous"],
         lambda s: s in ("x = 1 is a solution", "x = -2 is extraneous", "The equation has exactly one solution"), ["x² + x - 2 = (x + 2)(x - 1).", "x = 1: √4 = 2 ✓; x = -2: √1 = 1 ≠ -1 ✗."])
B.mc(S, "honors", "A student solves √(x + 6) = x and reports x = 3 and x = -2. What should the student have done?", "Checked both: x = -2 gives √4 = 2 ≠ -2, so only x = 3", ["Nothing; both are correct", "Rejected x = 3 because it is odd", "Rejected both because squaring is invalid"], ["Always substitute into the original equation."], tags=["error-analysis"])
B.orq(S, "honors", "Explore √(x + k) = x.",
      [("For k = 2, solve.", "x = 2"), ("For k = 2, which squared-equation root is extraneous?", "x = -1"), ("For k = 0, solve.", "x = 0 or x = 1"), ("For what k does √(x + k) = x have no real solution?", "k < -1/4")],
      ["x² - x - 2 = 0 → 2 or -1.", "√1 = 1 ≠ -1.", "x² = x.", "x² - x - k = 0 needs discriminant 1 + 4k ≥ 0; when -1/4 ≤ k < 0 roots are positive and valid, so none only when k < -1/4."], tags=["challenge", "reasoning"])
B.orq(S, "cp1", "Solve 3 + √(2x - 5) = x.",
      [("Isolate the radical.", "√(2x - 5) = x - 3"), ("Square and simplify to a quadratic.", "x² - 8x + 14 = 0"), ("Solve the quadratic.", "x = 4 ± √2"), ("Check and state the solution.", "x = 4 + √2 (x = 4 - √2 is extraneous)")],
      ["Subtract 3.", "2x - 5 = x² - 6x + 9.", "Quadratic formula.", "4 - √2 - 3 = 1 - √2 < 0."])
for v, ok in ((4 + sq(2), True), (4 - sq(2), False)): assert (abs(3 + sq(2 * v - 5) - v) < 1e-9) == ok
B.sa(S, "cp2", "Is x = 9 a solution of √x = -3?", "No", ["√9 = 3, not -3; the principal root is nonnegative."])
B.sa(S, "cp2", "Solve √x + 1 = 7 and check.", "x = 36", ["√x = 6 → x = 36; √36 + 1 = 7 ✓."])

# ---------------- Skill 7: graphing square-root and cube-root functions ----------------
S = 7
for fn, lab, dom, rng_, pts in [(lambda v: sq(v) if v >= 0 else float("nan"), "y = √x", "x ≥ 0", "y ≥ 0", [(0, 0), (1, 1), (4, 2)]),
                                (lambda v: math.copysign(abs(v) ** (1 / 3), v), "y = ∛x", "all real numbers", "all real numbers", [(-8, -2), (-1, -1), (0, 0), (1, 1), (8, 2)])]:
    dg = graph(B, f"s07-parent-{'sqrt' if '√' in lab and '∛' not in lab else 'cbrt'}", [(fn, {})], xr=(-9, 9), yr=(-4, 4), step=1, points=pts,
               alt=f"Graph of the parent function {lab} through " + ", ".join(pt(*p) for p in pts) + ".")
    B.orq(S, "cp2", f"The graph shows {lab}.", [("State the domain.", dom), ("State the range.", rng_), ("Name two points on the graph.", ", ".join(pt(*p) for p in pts[-2:])), ("Is the function increasing or decreasing?", "increasing")],
          ["Read the x-values the graph covers.", "Read the y-values.", "Points from the graph.", "It rises left to right."], diagram=dg, tags=["graph"])
    B.mc(S, "cp2", "Which equation matches the graph?", lab, [l for l in ["y = √x", "y = ∛x", "y = x²", "y = x³"] if l != lab][:3], ["Look at the domain and shape: √x starts at the origin; ∛x extends in both directions."], diagram=dg, tags=["graph"])
for a, h, k in [(1, 2, 0), (1, 0, -3), (-1, 0, 2), (2, -1, 1), (1, -3, -2), (F(1, 2), 4, 0)]:
    dom = f"x ≥ {h}"; rng_ = f"y ≥ {k}" if a > 0 else f"y ≤ {k}"
    f = f"y = {'' if a == 1 else '-' if a == -1 else fr(a)}√({'x' if h == 0 else f'x {chr(45) if h > 0 else chr(43)} {abs(h)}'}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}".replace("√(x)", "√x")
    B.sa(S, "cp1", f"State the domain and range of {f}.", f"domain {dom}; range {rng_}", [f"Radicand ≥ 0: x ≥ {h}.", f"Starting point ({h}, {k}); the graph goes {'up' if a > 0 else 'down'} from there."])
for c, h in [(1, 0), (-2, 3), (4, -1)]:
    f = f"y = ∛({'x' if h == 0 else f'x - {h}' if h > 0 else f'x + {-h}'}){'' if c == 0 else (' + ' if c > 0 else ' - ') + str(abs(c))}"
    B.mc(S, "cp1", f"What is the point of symmetry (center) of {f}?", pt(h, c), [pt(-h, c), pt(h, -c), pt(c, h)], ["Parent ∛x has center (0, 0).", f"Shift right {h}, up {c}." if h >= 0 else f"Shift left {-h}, up {c}."])
sel_auto(B, S, "cp1", "Select ALL points on the graph of y = √(x + 4) - 1.", ["(-4, -1)", "(0, 1)", "(5, 2)", "(12, 3)", "(4, 1)", "(-3, 1)"],
         lambda s: (lambda xv, yv: xv + 4 >= 0 and abs(sq(xv + 4) - 1 - yv) < 1e-9)(*[int(t) for t in s.strip("()").split(", ")]), ["Substitute each x and compare."])
sel_auto(B, S, "honors", "Select ALL functions whose range is all real numbers.", ["y = ∛x", "y = -∛(x + 2)", "y = 3∛x - 5", "y = √x", "y = -√(x - 1)", "y = √(-x)"],
         lambda s: "∛" in s, ["Cube-root functions take every real value.", "Square-root functions are bounded on one side."], tags=["reasoning"])
B.sa(S, "cp1", "Find the x-intercept of y = √(x - 1) - 3.", "(10, 0)", ["0 = √(x - 1) - 3 → √(x - 1) = 3 → x = 10."])
B.sa(S, "honors", "Find the x-intercept of y = 2∛(x + 1) + 4.", "(-9, 0)", ["∛(x + 1) = -2 → x + 1 = -8 → x = -9."])
B.sa(S, "cp1", "Find the average rate of change of f(x) = √x from x = 4 to x = 9.", "1/5", ["(√9 - √4)/(9 - 4) = 1/5."])
B.sa(S, "honors", "Compare the average rates of change of f(x) = √x on [0, 1] and [1, 4]. What does this show?", "1 and 1/3; the graph gets less steep as x increases", ["(1 - 0)/1 = 1; (2 - 1)/3 = 1/3."], tags=["reasoning"])
B.orq(S, "cp1", "Make a table for y = ∛x - 1 using x = -8, -1, 0, 1, 8.",
      [("Find y at x = -8.", "-3"), ("Find y at x = 0.", "-1"), ("Find y at x = 8.", "1"), ("State domain and range.", "all real numbers; all real numbers")],
      ["∛(-8) - 1.", "0 - 1.", "2 - 1.", "Cube roots are defined everywhere."], tags=["multiple-representations"])

# ---------------- Skill 8: radical function transformations ----------------
S = 8
specs = [(1, 3, 0, "s"), (1, 0, 2, "s"), (-1, 0, 0, "s"), (2, 1, -2, "s"), (1, -2, 1, "c"), (-1, 1, -1, "c"), (1, -4, -2, "s"), (3, 0, 0, "c")]
for a, h, k, kind in specs:
    r = "√" if kind == "s" else "∛"; inner = "x" if h == 0 else (f"x - {h}" if h > 0 else f"x + {-h}")
    eq = f"y = {'' if a == 1 else '-' if a == -1 else a}{r}({inner}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}".replace(f"{r}(x)", f"{r}x")
    desc = []
    if a < 0: desc.append("reflect over the x-axis")
    if abs(a) != 1: desc.append(f"vertical stretch by {abs(a)}")
    if h: desc.append(f"shift {'right' if h > 0 else 'left'} {abs(h)}")
    if k: desc.append(f"shift {'up' if k > 0 else 'down'} {abs(k)}")
    d = ", ".join(desc)
    wrong = [d.replace("right", "LEFT").replace("left", "right").replace("LEFT", "left") if h else d.replace("up", "DOWN").replace("down", "up").replace("DOWN", "down") if k else d + ", shift up 1",
             d.replace("x-axis", "y-axis") if a < 0 else (d.replace("up", "DOWN").replace("down", "up").replace("DOWN", "down") if k and h else "reflect over the x-axis, " + d),
             d.replace("vertical stretch", "horizontal stretch") if abs(a) != 1 else ("shift up " + str(abs(h)) if h else "shift right " + str(abs(k)) if k else "vertical stretch by 2")]
    B.mc(S, "cp2" if abs(a) == 1 and not (h and k) else "cp1", f"Describe the transformation from y = {r}x to {eq}.", d, wrong, ["Inside changes (x - h) shift horizontally, opposite the sign.", "Outside changes: a stretches/reflects; k shifts vertically.", d + "."])
    fn = (lambda v, a=a, h=h, k=k: a * sq(v - h) + k if v >= h else float("nan")) if kind == "s" else (lambda v, a=a, h=h, k=k: a * math.copysign(abs(v - h) ** (1 / 3), v - h) + k)
    if (a, h, k) in [(1, 3, 0), (2, 1, -2), (-1, 1, -1), (1, -4, -2)]:
        p1 = (h, k); p2 = (h + 1, a + k); p3 = (h + (4 if kind == "s" else 8), a * 2 + k)
        dg = graph(B, f"s08-{kind}-{a}-{h}-{k}".replace("-", "m").replace("s08m", "s08-"), [(fn, {})], xr=(-7, 9), yr=(-8, 8), step=1, points=[p1, p2, p3],
                   alt=f"Graph of a transformed {'square' if kind == 's' else 'cube'}-root function through {pt(*p1)}, {pt(*p2)}, and {pt(*p3)}.")
        wrongs = [eq.replace(inner, (f"x + {h}" if h > 0 else f"x - {-h}") if h else inner), eq.replace(" - " + str(abs(k)), " + " + str(abs(k))) if k < 0 else eq.replace(" + " + str(abs(k)), " - " + str(abs(k))),
                  eq.replace("y = ", "y = -") if a > 0 else eq.replace("y = -", "y = ")]
        B.mc(S, "cp1", "Which equation matches the graph?", eq, wrongs, [f"Key point {pt(*p1)} gives h = {h}, k = {k}.", f"From {pt(*p1)} to {pt(*p2)} the graph changes by {a}, so a = {a}."], diagram=dg, tags=["graph"])
for a, h, k, r in [(1, -5, 3, "√"), (-2, 0, 4, "√"), (1, 6, -1, "∛"), (F(1, 2), 2, 0, "√"), (-1, -3, -2, "∛")]:
    inner = "x" if h == 0 else (f"x - {h}" if h > 0 else f"x + {-h}")
    ans = f"y = {'' if a == 1 else '-' if a == -1 else fr(a)}{r}({inner}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}".replace(f"{r}(x)", f"{r}x")
    parts = (["reflected over the x-axis"] if a < 0 else []) + ([f"vertically {'stretched' if abs(a) > 1 else 'compressed'} by a factor of {fr(abs(a))}"] if abs(a) != 1 else []) + \
            ([f"shifted {'left' if h < 0 else 'right'} {abs(h)}"] if h else []) + ([f"shifted {'up' if k > 0 else 'down'} {abs(k)}"] if k else [])
    B.sa(S, "cp1", f"Write the equation of y = {r}x after it is " + ", then ".join(parts) + ".", ans, ["Apply a outside, (x - h) inside, + k outside.", ans + "."])
B.sa(S, "honors", "Describe how y = √(4x) relates to y = √x in two different ways.", "horizontal compression by 1/4, or vertical stretch by 2", ["√(4x) = 2√x."], tags=["reasoning", "connections"])
B.sa(S, "honors", "Write g(x) = √(9x - 18) + 1 as a vertical stretch and shifts of √x.", "g(x) = 3√(x - 2) + 1: stretch by 3, right 2, up 1", ["√(9(x - 2)) = 3√(x - 2)."], tags=["challenge"])
assert abs(sq(9 * 5.3 - 18) - 3 * sq(5.3 - 2)) < 1e-12
sel_auto(B, S, "cp1", "g(x) = -√(x + 2) + 3. Select ALL true statements.", ["The domain is x ≥ -2", "The range is y ≤ 3", "The starting point is (-2, 3)", "g is decreasing", "The domain is x ≥ 2", "The range is y ≥ 3", "g(2) = 1"],
         lambda s: s in ("The domain is x ≥ -2", "The range is y ≤ 3", "The starting point is (-2, 3)", "g is decreasing", "g(2) = 1"), ["x + 2 ≥ 0.", "Reflection makes outputs ≤ 3.", "g(2) = -2 + 3 = 1."])
sel_auto(B, S, "honors", "Select ALL functions whose graphs pass through (1, 2).", ["y = √(x + 3)", "y = ∛(x - 1) + 2", "y = 2√x", "y = -√(x + 8) + 5", "y = √(x - 1) - 2", "y = ∛(x + 7)"],
         lambda s: abs(peval(s.split("= ")[1].replace("∛(x - 1)", "0").replace("∛(x + 7)", "2"), x=1) - 2) < 1e-9, ["Substitute x = 1 into each."])
B.orq(S, "honors", "Let f(x) = √x and g(x) = -2√(x + 1) + 4.",
      [("List the transformations from f to g in order.", "left 1, vertical stretch by 2, reflect over x-axis, up 4"), ("Find the starting point of g.", "(-1, 4)"),
       ("Find the x-intercept of g.", "(3, 0)"), ("State the domain and range of g.", "x ≥ -1; y ≤ 4")],
      ["Inside then outside.", "(0, 0) → (-1, 4).", "-2√(x + 1) + 4 = 0 → √(x + 1) = 2 → x = 3.", "From the starting point."], tags=["multistep"])
B.orq(S, "cp1", "The graph of y = √x is shifted so its starting point is (3, -2).",
      [("Write the new equation.", "y = √(x - 3) - 2"), ("Find the y-value when x = 7.", "0"), ("State the domain.", "x ≥ 3"), ("State the range.", "y ≥ -2")],
      ["h = 3, k = -2.", "√4 - 2.", "Radicand ≥ 0.", "Starts at -2 and rises."])

# ================= additions: format balance =================
# Skill 2
for a, b in [(2, 3), (5, 2), (3, 6)]:
    e = f"(√{a} + √{b})²"; val = a + b + 2 * sq(a * b)
    sel_auto(B, 2, "cp1", f"Select ALL expressions equal to {e}.", [f"{a + b} + 2√{a * b}", f"{a + b}", f"{a + b} + √{a * b}", f"{a} + {b} + 2√{a}·√{b}", f"(√{a} + √{b})(√{b} + √{a})", f"{a * b} + 2√{a + b}"],
             lambda s: abs(peval(s) - val) < 1e-9, ["(√a + √b)² = a + 2√(ab) + b.", "The middle term cannot be dropped."], tags=["misconception"])
B.orq(2, "honors", "Let p = √7 + √3 and q = √7 - √3.", [("Find p + q.", "2√7"), ("Find pq.", "4"), ("Find p² + q².", "20"), ("Find p/q in simplest form.", "(5 + √21)/2")],
      ["Add.", "7 - 3.", "(p + q)² - 2pq = 28 - 8.", "Multiply by p/p: p²/(pq) = (10 + 2√21)/4."], tags=["challenge"])
assert abs((sq(7) + sq(3)) / (sq(7) - sq(3)) - (5 + sq(21)) / 2) < 1e-12
# Skill 3
for b, cands in [(8, ["8^(1/3)", "8^(2/3)", "(8^(1/3))²", "∛64", "8^(-2/3)", "(1/8)^(-2/3)", "64^(1/3)"]), (81, ["81^(3/4)", "(∜81)³", "27", "81^(-3/4)", "(81^3)^(1/4)", "(1/81)^(-3/4)", "9^(3/2)"])]:
    target = 4 if b == 8 else 27
    sel_auto(B, 3, "cp1", f"Select ALL expressions whose value is {target}.", cands, lambda s: abs(peval(s.replace("∛64", "4").replace("(∜81)³", "27")) - target) < 1e-9,
             ["a^(m/n) = (ⁿ√a)^m.", "A negative exponent gives a reciprocal; (1/a)^(-r) = a^r."])
for e, ans in [("(x^(2/3)y^(1/2))⁶", "x⁴y³"), ("x^(1/2)(x^(3/2) - x^(-1/2))", "x² - 1"), ("(a^(-1/2)b^(1/4))^(-4)", "a²/b"), ("(x^(1/3) + 1)(x^(1/3) - 1)", "x^(2/3) - 1")]:
    for v in (1.4, 2.6): assert same(peval(e.replace("a", "x").replace("b", "y"), x=v, y=1.7), peval(ans.replace("a", "x").replace("b", "y"), x=v, y=1.7), 1e-7)
    B.sa(3, "honors", f"Simplify {e}. Assume all variables are positive.", ans, ["Apply the power rule and distribute exponents.", f"Result: {ans}."])
B.mc(3, "cp1", "Order from least to greast: 16^(1/2), 27^(2/3), 32^(3/5).".replace("greast", "greatest"), "16^(1/2) < 32^(3/5) < 27^(2/3)", ["27^(2/3) < 16^(1/2) < 32^(3/5)", "32^(3/5) < 16^(1/2) < 27^(2/3)", "16^(1/2) < 27^(2/3) < 32^(3/5)"], ["Values: 4, 9, 8."])
B.orq(3, "cp1", "A cell culture grows so that its mass after t days is M = 100·4^(t/2) mg.", [("Find M at t = 1.", "200 mg"), ("Find M at t = 3.", "800 mg"), ("Find M at t = 5.", "3200 mg"), ("By what factor does M grow each day?", "2")],
      ["4^(1/2) = 2.", "4^(3/2) = 8.", "4^(5/2) = 32.", "4^(1/2) = 2 per day."], tags=["modeling", "connections"])
# Skill 4
for r_, e_, cands in [("√(x³)", "x^(3/2)", ["x^(3/2)", "x^(2/3)", "x·√x", "(√x)³", "x³/2", "x^(-3/2)"]), ("∛(x⁵)", "x^(5/3)", ["x^(5/3)", "x^(3/5)", "x·∛(x²)", "(∛x)⁵", "x^(5/3)·x^0" if False else "x^(-5/3)", "5x/3"]),
                     ("1/∜(x³)", "x^(-3/4)", ["x^(-3/4)", "x^(-4/3)", "1/x^(3/4)", "(x^(-1/4))³", "-x^(3/4)", "x^(3/4)"])]:
    sel_auto(B, 4, "cp1", f"Select ALL expressions equivalent to {r_} for x > 0.", cands, lambda s, e_=e_: abs(peval(s.replace("∛(x²)", "x**(2/3)").replace("(∛x)⁵", "x**(5/3)"), x=2.7) - peval(e_, x=2.7)) < 1e-9,
             ["ⁿ√(x^m) = x^(m/n); a radical in the denominator makes the exponent negative.", "Swapping the numerator and denominator of the exponent is a common error."], tags=["misconception"])
B.orq(4, "honors", "Simplify ⁶√(x⁴)·∛x for x > 0.", [("Write ⁶√(x⁴) as a power.", "x^(2/3)"), ("Write ∛x as a power.", "x^(1/3)"), ("Multiply.", "x"), ("Explain why the product has no radical.", "Exponents add to 1")],
      ["4/6 = 2/3.", "Index 3.", "2/3 + 1/3 = 1.", "x¹ = x."])
B.mc(4, "honors", "Which expression equals ⁶√8?", "√2", ["∛2", "2", "8^6"], ["8^(1/6) = (2³)^(1/6) = 2^(1/2)."], tags=["connections"])
B.sa(4, "cp1", "Write 5^(3/4) in radical form.", "∜(5³) = ∜125", ["Index 4, power 3."])
B.sa(4, "cp2", "Write ∛y using a rational exponent.", "y^(1/3)", ["Index 3 → exponent 1/3."])
# Skill 5
for c, r1, r2 in [(1, 3, 2), (0, 5, 2), (2, 1, 0)]:
    a = r1 + r2 + 2 * c; b = c * c - r1 * r2
    rhs = "x" if c == 0 else f"x + {c}"; lhs = f"√({a if a != 1 else ''}x {'+' if b >= 0 else '-'} {abs(b)})"
    for r in (r1, r2): assert abs(sq(a * r + b) - (r + c)) < 1e-9
    B.orq(5, "cp1", f"Solve {lhs} = {rhs}.", [("Square both sides.", f"{a if a != 1 else ''}x {'+' if b >= 0 else '-'} {abs(b)} = {'x²' if c == 0 else f'x² + {2 * c}x + {c * c}'}"),
          ("Write the quadratic in standard form.", f"{P.coeffs(1, 2 * c - a, c * c - b)} = 0"), ("Solve it.", f"x = {r2} or x = {r1}"), ("Check both and state the solution set.", f"both check: x = {r2}, {r1}")],
          ["Squaring removes the radical.", "Collect terms.", "Factor.", "Substitute into the original."])
sel_auto(B, 5, "cp1", "Select ALL equations whose solution is x = 5.", ["√(x + 4) = 3", "√(2x - 1) = 3", "∛(x + 3) = 2", "√x = 25", "∛(5x + 2) = 3", "√(x - 1) = 4"],
         lambda s: abs(peval(s.split(" = ")[0].replace("∛(x + 3)", "(x+3)**(1/3)").replace("∛(5x + 2)", "(5*x+2)**(1/3)"), x=5) - peval(s.split(" = ")[1])) < 1e-9, ["Substitute x = 5 into each equation."])
sel_auto(B, 5, "honors", "Select ALL equations that have exactly two real solutions.", ["x^(2/3) = 4", "x⁴ = 16", "√(x²) = 3", "x^(3/2) = 8", "∛x = -1", "x^(1/2) = -2"],
         lambda s: s in ("x^(2/3) = 4", "x⁴ = 16", "√(x²) = 3"), ["x^(2/3) = 4 → x = ±8; x⁴ = 16 → ±2; |x| = 3 → ±3.", "x^(3/2) = 8 → x = 4 only; ∛x = -1 → -1 only; x^(1/2) = -2 has none."], tags=["reasoning"])
B.mc(5, "cp1", "Solve ∛(2x - 1) + 4 = 1.", "x = -13", ["x = 14", "x = -1", "no solution"], ["∛(2x - 1) = -3 → 2x - 1 = -27 → x = -13.", "Cube roots can be negative, so this is valid."], tags=["misconception"])
B.mc(5, "cp1", "Which equation is equivalent to √(x - 2) = x - 4 after squaring?", "x - 2 = x² - 8x + 16", ["x - 2 = x² + 16", "x - 2 = x² - 16", "x² - 4 = x - 4"], ["(x - 4)² = x² - 8x + 16."], tags=["misconception"])
B.sa(5, "honors", "Solve √(2x + 5) = √(x + 2) + 1.", "x = -2 or x = 2", ["Square: 2x + 5 = x + 3 + 2√(x + 2) → x + 2 = 2√(x + 2).", "Square: x² + 4x + 4 = 4x + 8 → x² = 4.", "Check: x = 2: 3 = 2 + 1 ✓; x = -2: 1 = 0 + 1 ✓."], tags=["challenge"])
for v in (2, -2): assert abs(sq(2 * v + 5) - sq(v + 2) - 1) < 1e-12
B.sa(5, "cp1", "The speed (mph) of a car that skids d feet is s = √(30fd) with f = 0.75. Find d when s = 45.", "d = 90 ft", ["45² = 22.5d → 2025 = 22.5d.", "d = 90."], tags=["modeling"])
# Skill 6
for c, r1, r2 in [(-2, 6, 1), (-3, 7, 2), (0, 4, -3)]:
    a = r1 + r2 + 2 * c; b = c * c - r1 * r2
    rhs = "x" if c == 0 else f"x - {-c}"; lhs = f"√({a if a != 1 else ''}x {'+' if b >= 0 else '-'} {abs(b)})"
    good, bad = [r for r in (r1, r2) if r + c >= 0], [r for r in (r1, r2) if r + c < 0]; assert len(good) == 1 and len(bad) == 1
    B.orq(6, "cp1" if c else "cp2", f"Solve {lhs} = {rhs} and identify any extraneous solutions.",
          [("Square and write a quadratic equation.", f"{P.coeffs(1, 2 * c - a, c * c - b)} = 0"), ("Solve the quadratic.", f"x = {r1} or x = {r2}"),
           ("Check each value.", f"x = {good[0]} works; x = {bad[0]} gives a negative right side"), ("State the solution.", f"x = {good[0]} ({bad[0]} is extraneous)")],
          ["Square both sides.", "Factor.", "Substitute into the original equation.", "Keep only values that check."], tags=["error-analysis"])
sel_auto(B, 6, "cp1", "For √(x + 12) = x, select ALL true statements.", ["x = 4 is a solution", "x = -3 is extraneous", "Squaring gives x² - x - 12 = 0", "x = -3 is a solution", "There are two solutions"],
         lambda s: s in ("x = 4 is a solution", "x = -3 is extraneous", "Squaring gives x² - x - 12 = 0"), ["x² - x - 12 = (x - 4)(x + 3).", "√16 = 4 ✓; √9 = 3 ≠ -3 ✗."])
sel_auto(B, 6, "honors", "Select ALL operations that can introduce extraneous solutions.", ["Squaring both sides", "Raising both sides to the 4th power", "Multiplying both sides by an expression containing x", "Cubing both sides", "Adding 5 to both sides", "Dividing both sides by 3"],
         lambda s: s in ("Squaring both sides", "Raising both sides to the 4th power", "Multiplying both sides by an expression containing x"), ["Even powers lose sign information.", "Multiplying by an expression that can be 0 can add solutions.", "Cubing, adding, dividing by a nonzero constant are reversible."], tags=["reasoning"])
B.mc(6, "cp1", "Which value of x is extraneous for √(x + 3) = x - 3?", "x = 1", ["x = 6", "x = -3", "There is none"], ["Squaring: x² - 7x + 6 = 0 → x = 6 or 1.", "x = 1: √4 = 2 ≠ -2."])
B.mc(6, "honors", "For which k does √(x - 1) = x - k have an extraneous root at x = 2?", "k = 3", ["k = 1", "k = 2", "k = 0"], ["At x = 2 the left side is 1; extraneous means 2 - k = -1 → k = 3.", "Check: squaring x - 1 = (x - 3)² gives roots 2 and 5; x = 5: 2 = 2 ✓, x = 2: 1 ≠ -1."], tags=["challenge"])
assert sorted(r for r in (2, 5) if abs((r - 1) - (r - 3) ** 2) < 1e-9) == [2, 5]
B.sa(6, "cp1", "Solve x = √(5x + 6) and check.", "x = 6", ["x² - 5x - 6 = 0 → x = 6 or -1.", "x = -1 is extraneous (-1 ≠ 1)."])
B.sa(6, "cp1", "Solve √(x + 5) + 1 = x and check.", "x = 4", ["√(x + 5) = x - 1 → x² - 3x - 4 = 0 → x = 4 or -1.", "x = -1: 2 + 1 ≠ -1."])
# Skill 7
for name, fn, pts_ in [("y = √(x + 3)", lambda v: sq(v + 3) if v >= -3 else float("nan"), [(-3, 0), (1, 2), (6, 3)]), ("y = -√x + 4", lambda v: -sq(v) + 4 if v >= 0 else float("nan"), [(0, 4), (4, 2), (9, 1)]),
                     ("y = ∛(x - 2)", lambda v: math.copysign(abs(v - 2) ** (1 / 3), v - 2), [(-6, -2), (1, -1), (2, 0), (3, 1)]), ("y = 2∛x", lambda v: 2 * math.copysign(abs(v) ** (1 / 3), v), [(-1, -2), (0, 0), (1, 2), (8, 4)])]:
    dg = graph(B, "s07-" + name.replace("y = ", "").replace("√", "r").replace("∛", "c").replace(" ", "").replace("(", "").replace(")", "").replace("+", "p").replace("-", "m"), [(fn, {})], xr=(-8, 10), yr=(-6, 6), step=1, points=pts_,
               alt=f"Graph of {name} through " + ", ".join(pt(*p) for p in pts_) + ".")
    for p_ in pts_: assert abs(fn(p_[0]) - p_[1]) < 1e-9
    isq = "∛" not in name
    dom = "all real numbers" if not isq else ("x ≥ -3" if "+ 3" in name else "x ≥ 0"); rng_ = "all real numbers" if not isq else ("y ≥ 0" if "+ 3" in name else "y ≤ 4")
    B.orq(7, "cp1", f"The graph shows {name}.", [("State the domain.", dom), ("State the range.", rng_), ("Find the y-intercept.", fr(fn(0)) if fn(0) == int(fn(0)) else f"{fn(0):.2f}"), ("Increasing or decreasing?", "decreasing" if "-√" in name else "increasing")],
          ["Read the x-extent.", "Read the y-extent.", "Evaluate at x = 0.", "Read the direction."], diagram=dg, tags=["graph"])
    cands = [pt(*p) for p in pts_[:3]] + [pt(pts_[0][0], pts_[0][1] + 1), pt(-pts_[1][0] if pts_[1][0] else 5, pts_[1][1])]
    sel_auto(B, 7, "cp2", f"Select ALL points that lie on the graph of {name}.", cands, lambda s, fn=fn: (lambda a, b: (not math.isnan(fn(a))) and abs(fn(a) - b) < 1e-9)(*[int(t) for t in s.strip("()").split(", ")]),
             ["Substitute the x-coordinate and compare the y-coordinate."], diagram=dg, tags=["graph"])
B.mc(7, "honors", "Which function has domain x ≤ 2?", "y = √(2 - x)", ["y = √(x - 2)", "y = ∛(2 - x)", "y = -√(x + 2)"], ["2 - x ≥ 0 → x ≤ 2."], tags=["reasoning"])
B.sa(7, "honors", "Find the domain of f(x) = √(x² - 9).", "x ≤ -3 or x ≥ 3", ["x² - 9 ≥ 0 → |x| ≥ 3."], tags=["challenge"])
# Skill 8
for a, h, k in [(1, 2, 3), (-1, -1, 0), (3, 0, -4)]:
    eq = f"y = {'' if a == 1 else '-' if a == -1 else a}√({'x' if h == 0 else (f'x - {h}' if h > 0 else f'x + {-h}')}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}".replace("√(x)", "√x")
    st = {f"The starting point is ({h}, {k})": True, f"The domain is x ≥ {h}": True, f"The range is y {'≥' if a > 0 else '≤'} {k}": True,
          f"The starting point is ({-h}, {k})": h == 0, f"The range is y {'≤' if a > 0 else '≥'} {k}": False, f"The graph passes through ({h + 1}, {a + k})": True, f"The graph passes through ({h + 4}, {a + k})": False}
    B.sel(8, "cp1", f"Select ALL true statements about {eq}.", [s_ for s_, t_ in st.items() if t_], [s_ for s_, t_ in st.items() if not t_], ["Starting point (h, k); domain x ≥ h.", f"Range from k {'up' if a > 0 else 'down'}.", f"At x = h + 1: y = a + k = {a + k}; at x = h + 4: y = 2a + k = {2 * a + k}."])
B.orq(8, "honors", "g(x) = ∛(8x + 16) - 1.", [("Factor inside the radical.", "∛(8(x + 2))"), ("Rewrite g as a stretch of ∛x.", "g(x) = 2∛(x + 2) - 1"), ("Find the center point.", "(-2, -1)"), ("Find the x-intercept.", "(-15/8, 0)")],
      ["8x + 16 = 8(x + 2).", "∛8 = 2.", "h = -2, k = -1.", "∛(x + 2) = 1/2 → x + 2 = 1/8."], tags=["challenge"])
assert abs(2 * (float(F(-15, 8)) + 2) ** (1 / 3) - 1) < 1e-9 and 8 * F(-15, 8) + 16 == 1
B.mc(8, "cp1", "The graph of y = √x is reflected over the y-axis. What is the new equation?", "y = √(-x)", ["y = -√x", "y = √x - 1", "y = 1/√x"], ["Reflecting over the y-axis replaces x with -x."], tags=["misconception"])
B.mc(8, "cp2", "How does y = √x + 5 differ from y = √(x + 5)?", "The first shifts up 5; the second shifts left 5", ["Both shift up 5", "Both shift left 5", "The first shifts right 5; the second shifts down 5"], ["Outside → vertical; inside → horizontal (opposite sign)."], tags=["misconception"])

B.sa(8, "honors", "The graph of y = a√(x - h) + k starts at (2, -3) and passes through (6, 5). Find a, h, and k.", "a = 4, h = 2, k = -3", ["Starting point gives h = 2, k = -3.", "5 = a√4 - 3 → a = 4."])
B.sa(8, "cp1", "Write the equation of y = ∛x shifted right 4 and down 6.", "y = ∛(x - 4) - 6", ["Right 4: x - 4 inside; down 6: - 6 outside."])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
