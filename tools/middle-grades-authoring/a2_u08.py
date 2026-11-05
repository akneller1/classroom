"""Algebra 2 Unit 8 — Sequences and Series (sequences-series). Top-up families."""
from hslib import *
import math

UNIT_ID = "sequences-series"
ABBR = "ss"
SUBN = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def a_(k):
    return "a" + str(k).translate(SUBN)


def ri(r, a, b):
    return rint(r, a, b, True)


def ordn(k):
    return f"{k}{'th' if 10 <= k % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def sertxt(terms):
    return " + ".join(T(t) if i == 0 or not str(T(t)).startswith("-") else f"({T(t)})" for i, t in enumerate(terms))


def seqtxt(terms):
    return ", ".join(T(t) for t in terms) + ", …"


# ============================================================== S1 Arithmetic sequences
@fam("012")
def s1_nth(r, L):
    a1, d = rint(r, -20, 30), ri(r, -9, 12) * (1 if L < 2 else pick(r, [1, sp.Rational(1, 2)]))
    k = rint(r, 10, 60)
    v = a1 + (k - 1) * d
    terms = [a1 + i * d for i in range(4)]
    return Q(f"Find the {ordn(k)} term of the arithmetic sequence {seqtxt(terms)}", T(v),
             [f"{a_(1)} = {a1}, d = {T(d)}.", f"aₙ = {a_(1)} + (n - 1)d, so {a_(k)} = {a1} + ({k} - 1)({T(d)}).", f"{a_(k)} = {T(v)}."],
             [T(a1 + k * d), T(k * d), T(a1 + (k - 1) * (-d))], H(f"{a1} + ({k} - 1)*nsimplify('{T(d)}')"),
             why=["Used n instead of n - 1", "Forgot the first term", "Used the wrong sign for the common difference"])


@fam("012")
def s1_two_terms(r, L):
    a1, d = rint(r, -15, 25), ri(r, -8, 9)
    i, j = sorted(r.sample(range(2, 15), 2))
    ai, aj = a1 + (i - 1) * d, a1 + (j - 1) * d
    ask = pick(r, ["d", "a1"]) if L < 2 else "formula"
    if ask == "d":
        return Q(f"In an arithmetic sequence, {a_(i)} = {ai} and {a_(j)} = {aj}. Find the common difference d.", str(d),
                 [f"From term {i} to term {j} there are {j - i} steps of d.", f"d = ({aj} - {par(ai)}) ÷ {j - i} = {d}."],
                 [str(aj - ai), T(sp.Rational(aj - ai, j - i + 1)) if (aj - ai) != d * (j - i + 1) else str(d + 1), T(sp.Rational(j - i, aj - ai)) if aj != ai else "0"], H(f"Rational({aj} - ({ai}), {j} - {i})"),
                 why=["Forgot to divide by the number of steps", "Counted the terms instead of the steps", "Divided in the wrong order"])
    if ask == "a1":
        return Q(f"In an arithmetic sequence, {a_(i)} = {ai} and {a_(j)} = {aj}. Find {a_(1)}.", str(a1),
                 [f"d = ({aj} - {par(ai)}) ÷ {j - i} = {d}.", f"{a_(1)} = {a_(i)} - ({i} - 1)d = {ai} - {i - 1}({d}) = {a1}."],
                 [str(ai - i * d), str(ai - d), str(ai + (i - 1) * d)], H(f"{ai} - ({i} - 1)*Rational({aj} - ({ai}), {j} - {i})"),
                 why=["Used i instead of i - 1 steps", "Subtracted only one difference", "Added instead of subtracting"])
    ans = f"aₙ = {T(d * n + (a1 - d))}"
    return Q(f"In an arithmetic sequence, {a_(i)} = {ai} and {a_(j)} = {aj}. Write an explicit formula for aₙ in simplest form.", ans,
             [f"d = ({aj} - {par(ai)}) ÷ {j - i} = {d}.", f"{a_(1)} = {ai} - {i - 1}({d}) = {a1}.", f"aₙ = {a1} + (n - 1)({d}) = {T(d * n + (a1 - d))}."],
             [f"aₙ = {T(d * n + a1)}", f"aₙ = {T(a1 * n + d)}", f"aₙ = {T(d * n + ai)}"], PY("seq_expr", expr=T(d * n + (a1 - d))),
             why=["Used a₁ as the constant without subtracting d", "Switched the first term and the difference", "Used a later term as the starting term"])


# ============================================================== S2 Geometric sequences
@fam("012")
def s2_nth(r, L):
    a1 = ri(r, -6, 9)
    rr = pick(r, [2, 3, -2, 4, 5]) if L == 0 else pick(r, [2, 3, -2, -3, sp.Rational(1, 2), sp.Rational(-1, 2), sp.Rational(2, 3)])
    a1 = a1 * (rr.q ** 4 if hasattr(rr, "q") and L else 1)
    k = rint(r, 5, 8)
    v = a1 * sp.sympify(rr) ** (k - 1)
    need(abs(v) < 10 ** 6)
    terms = [a1 * sp.sympify(rr) ** i for i in range(4)]
    return Q(f"Find the {ordn(k)} term of the geometric sequence {seqtxt(terms)}", T(v),
             [f"{a_(1)} = {a1}, r = {T(rr)}.", f"aₙ = {a_(1)}·r^(n - 1), so {a_(k)} = {a1}({T(rr)})^{k - 1}.", f"{a_(k)} = {T(v)}."],
             [T(a1 * sp.sympify(rr) ** k), T(a1 * sp.sympify(rr) * (k - 1)), T(sp.sympify(a1 * rr) ** (k - 1))], H(f"{a1}*nsimplify('{T(rr)}')**({k} - 1)"),
             why=["Used the exponent n instead of n - 1", "Multiplied by n - 1 instead of raising to the power", "Raised a₁ to the power as well"])


@fam("012")
def s2_ratio(r, L):
    a1 = ri(r, -9, 9)
    rr = sp.sympify(pick(r, [2, 3, -2, 4, sp.Rational(1, 2), sp.Rational(1, 3), -3]))
    a1 = a1 * (rr.q ** 3)
    terms = [a1 * rr ** i for i in range(4)]
    ask = pick(r, ["ratio", "next"])
    if ask == "ratio":
        return Q(f"Find the common ratio of the geometric sequence {seqtxt(terms)}", T(rr), [f"r = {a_(2)} ÷ {a_(1)} = {T(terms[1])} ÷ {T(terms[0])}.", f"r = {T(rr)}."],
                 [T(terms[1] - terms[0]), T(1 / rr), T(-rr)], H(f"nsimplify('{T(terms[1])}')/nsimplify('{T(terms[0])}')"),
                 why=["Found a difference instead of a ratio", "Divided in the wrong order", "Made a sign error"])
    return Q(f"Find the next term of the geometric sequence {seqtxt(terms)}", T(terms[3] * rr), [f"r = {T(terms[1])} ÷ {T(terms[0])} = {T(rr)}.", f"Next term = {T(terms[3])} · {T(rr)} = {T(terms[3] * rr)}."],
             [T(terms[3] + (terms[3] - terms[2])), T(terms[3] / rr), T(-terms[3] * rr)], H(f"nsimplify('{T(terms[3])}')*nsimplify('{T(terms[1])}')/nsimplify('{T(terms[0])}')"),
             why=["Added the last difference instead of multiplying", "Divided by the ratio", "Made a sign error"])


# ============================================================== S3 Recursive and explicit formulas
@fam("012")
def s3_rec_terms(r, L):
    a1 = rint(r, -9, 12)
    kind = pick(r, ["arith", "geom", "mixed"]) if L else pick(r, ["arith", "geom"])
    if kind == "arith":
        d = ri(r, -7, 9)
        rule, f = f"aₙ = aₙ₋₁ {'+' if d > 0 else '-'} {abs(d)}", lambda p: p + d
    elif kind == "geom":
        m = pick(r, [2, 3, -2, -1])
        rule, f = f"aₙ = {m}aₙ₋₁" if m != -1 else "aₙ = -aₙ₋₁", lambda p: m * p
        a1 = ri(r, -6, 6)
    else:
        m, d = pick(r, [2, 3, -1]), ri(r, -5, 5)
        rule, f = f"aₙ = {m if m != -1 else '-'}aₙ₋₁ {'+' if d > 0 else '-'} {abs(d)}", lambda p: m * p + d
        a1 = ri(r, -5, 5)
    k = pick(r, [4, 5]) if L else 4
    vals = [a1]
    for _ in range(k - 1):
        vals.append(f(vals[-1]))
    need(abs(vals[-1]) < 5000)
    return Q(f"A sequence is defined by {a_(1)} = {a1} and {rule} for n ≥ 2. Find {a_(k)}.", str(vals[-1]),
             [f"Apply the rule one term at a time.", ", ".join(f"{a_(i + 1)} = {v}" for i, v in enumerate(vals)) + "."],
             [str(vals[-2]), str(f(vals[-1])), str(vals[-1] + (1 if kind != "geom" else vals[0]))], PY("recur", a1=a1, rule=rule, k=k),
             why=["Stopped one term too early", "Went one term too far", "Made an arithmetic error in the last step"])


@fam("012")
def s3_to_explicit(r, L):
    kind = pick(r, ["arith", "geom"]) if L else "arith"
    a1 = ri(r, -9, 12)
    if kind == "arith":
        d = ri(r, -8, 9)
        rule = f"aₙ = aₙ₋₁ {'+' if d > 0 else '-'} {abs(d)}"
        ex = d * n + (a1 - d)
        ans = f"aₙ = {T(ex)}"
        wr = [f"aₙ = {T(d * n + a1)}", f"aₙ = {T(a1 * n + d)}", f"aₙ = {T(-d * n + (a1 + d))}"]
        why = ["Did not subtract d from the first term", "Switched the first term and the difference", "Used the wrong sign for the difference"]
        st = [f"The sequence is arithmetic with {a_(1)} = {a1} and d = {d}.", f"aₙ = {a1} + (n - 1)({d}).", f"{ans}."]
    else:
        m = pick(r, [2, 3, 4, -2, 5])
        rule = f"aₙ = {m}aₙ₋₁"
        ex = a1 * sp.Integer(m) ** (n - 1)
        ans = f"aₙ = {a1}({m})^(n - 1)" if a1 != 1 else f"aₙ = ({m})^(n - 1)"
        wr = [f"aₙ = {a1}({m})ⁿ", f"aₙ = {m}({a1})^(n - 1)" if abs(a1) != 1 else f"aₙ = {m * a1}(n - 1)", f"aₙ = {a1} + {m}(n - 1)"]
        why = ["Used the exponent n instead of n - 1", "Switched the first term and the ratio", "Wrote an arithmetic formula for a geometric sequence"]
        st = [f"The sequence is geometric with {a_(1)} = {a1} and r = {m}.", f"aₙ = {a_(1)}·r^(n - 1).", f"{ans}."]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Write an explicit formula for the sequence {a_(1)} = {a1}, {rule} (n ≥ 2).", ans, st, wr, PY("seq_expr", expr=str(ex).replace("**", "^")), why=why)


# ============================================================== S4 Arithmetic series
@fam("012")
def s4_sum(r, L):
    a1, d = rint(r, -10, 20), ri(r, -5, 9)
    k = rint(r, 8, 40)
    an = a1 + (k - 1) * d
    S = sp.Rational(k * (a1 + an), 2)
    terms = [a1 + i * d for i in range(3)]
    q = f"Find the sum of the first {k} terms of the arithmetic series {sertxt(terms)} + …" if L < 2 else f"Find the sum of the arithmetic series with {a_(1)} = {a1}, d = {d}, and n = {k} terms."
    return Q(q, T(S), [f"{a_(k)} = {a1} + ({k} - 1)({d}) = {an}.", f"Sₙ = n({a_(1)} + aₙ)/2 = {k}({a1} + {par(an)})/2.", f"S = {T(S)}."],
             [T(k * (a1 + an)), T(sp.Rational(k * (a1 + an + d), 2)), T(k * an)], H(f"summation({a1} + (k - 1)*({d}), (k, 1, {k}))"),
             why=["Forgot to divide by 2", "Used the wrong last term", "Multiplied the last term by n"])


# ============================================================== S5 Geometric series
@fam("012")
def s5_sum(r, L):
    a1 = ri(r, -5, 8)
    rr = pick(r, [2, 3, -2]) if L == 0 else pick(r, [2, 3, -2, 4, sp.Rational(1, 2), -3])
    rr = sp.sympify(rr)
    k = rint(r, 4, 8)
    a1 = a1 * rr.q ** (k - 1)
    S = a1 * (1 - rr ** k) / (1 - rr)
    need(abs(S) < 10 ** 6)
    terms = [a1 * rr ** i for i in range(3)]
    return Q(f"Find the sum of the first {k} terms of the geometric series {sertxt(terms)} + …", T(S),
             [f"{a_(1)} = {T(a1)}, r = {T(rr)}, n = {k}.", f"Sₙ = {a_(1)}(1 - rⁿ)/(1 - r) = {T(a1)}(1 - ({T(rr)}){sup(k)})/(1 - ({T(rr)})).", f"S = {T(S)}."],
             [T(a1 * (1 - rr ** (k - 1)) / (1 - rr)), T(a1 * rr ** (k - 1)), T(a1 * (1 + rr ** k) / (1 - rr))], H(f"summation({T(a1)}*nsimplify('{T(rr)}')**(k - 1), (k, 1, {k}))"),
             why=["Used n - 1 terms", "Gave the last term instead of the sum", "Made a sign error in the formula"])


# ============================================================== S6 Sigma notation
@fam("012")
def s6_eval(r, L):
    lo, hi = (1, rint(r, 4, 8)) if L < 2 else (rint(r, 1, 3), rint(r, 6, 12))
    kind = pick(r, ["lin", "geo"]) if L else "lin"
    if kind == "lin":
        a, b = ri(r, -6, 7), rint(r, -9, 9)
        body = T(a * k + b)
        expr = a * k + b
    else:
        c, m = ri(r, -4, 5), pick(r, [2, 3, -2])
        body = f"{c}({m})^(k - 1)" if c not in (1, -1) else f"({m})^(k - 1)" if c == 1 else f"-({m})^(k - 1)"
        expr = c * sp.Integer(m) ** (k - 1)
    S = sp.summation(expr, (k, lo, hi))
    txt = f"Σ (k = {lo} to {hi}) ({body})"
    wrongs = [sp.summation(expr, (k, lo, hi - 1)), expr.subs(k, hi), sp.summation(expr, (k, lo + 1, hi)) if lo + 1 <= hi else S + 1]
    return Q(f"Evaluate {txt}.", T(S), [f"Substitute k = {lo}, {lo + 1}, …, {hi} into {body}.", f"There are {hi - lo + 1} terms.", f"Add them: {T(S)}."],
             [T(w) for w in wrongs], H(f"summation({str(expr)}, (k, {lo}, {hi}))"), why=["Stopped one term early", "Gave only the last term", "Started at the wrong index"])


@fam("12")
def s6_write(r, L):
    a1, d = rint(r, -5, 12), ri(r, -6, 9)
    k_ = rint(r, 5, 12)
    terms = [a1 + i * d for i in range(3)] + [a1 + (k_ - 1) * d]
    body = T(d * k + (a1 - d))
    ans = f"Σ (k = 1 to {k_}) ({body})"
    wr = [f"Σ (k = 1 to {k_}) ({T(d * k + a1)})", f"Σ (k = 1 to {k_ - 1}) ({body})", f"Σ (k = 0 to {k_}) ({body})"]
    return Q(f"Write the series {sertxt(terms[:3])} + … + {sertxt([terms[3]]) if terms[3] >= 0 else '(' + str(terms[3]) + ')'} in sigma notation.", ans,
             [f"Common difference {d}, first term {a1}: the k-th term is {a1} + (k - 1)({d}) = {body}.", f"Solve {body} = {terms[3]}: k = {k_}.", f"{ans}."],
             wr, PY("sigma_eq", expr=str(d * k + (a1 - d)), lo=1, hi=k_), why=["Did not adjust the constant term for k starting at 1", "Counted one term too few", "Started the index at 0 without changing the formula"])


# ============================================================== S7 Finite and infinite geometric series
@fam("012")
def s7_infinite(r, L):
    rr = sp.sympify(pick(r, [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 3), sp.Rational(-1, 2), sp.Rational(3, 4), sp.Rational(1, 4), sp.Rational(-1, 3), 2, -2, sp.Rational(3, 2)]))
    a1 = ri(r, -8, 20) * rr.q ** 2
    terms = [a1 * rr ** i for i in range(3)]
    conv = abs(rr) < 1
    ans = T(a1 / (1 - rr)) if conv else "The series diverges (no sum)."
    wr = [T(a1 / (1 + rr)), T(a1 * rr / (1 - rr)), "The series diverges (no sum)."] if conv else [T(a1 / (1 - rr)), T(a1 / (1 - 1 / rr)), "0"]
    return Q(f"Find the sum of the infinite geometric series {sertxt(terms)} + …, or state that it diverges.", ans,
             [f"r = {T(rr)}.", "An infinite geometric series converges only when |r| < 1; then S = a₁ ÷ (1 - r)." if conv else f"|r| = {T(abs(rr))} ≥ 1, so the terms do not shrink.", (f"S = {T(a1)} ÷ (1 - ({T(rr)})) = {ans}." if conv else ans)],
             wr, PY("inf_geo", a1=str(a1), r=str(rr)), why=(["Used 1 + r in the denominator", "Started the sum at the second term", "Thought the series diverges even though |r| < 1"] if conv else
                                                           ["Applied the formula even though |r| ≥ 1", "Used the reciprocal of r", "Thought the terms cancel to 0"]))


# ============================================================== S8 Applications of sequences
@fam("012")
def s8_apps(r, L):
    kind = pick(r, ["seats", "salary", "bounce"] if L else ["seats", "salary"])
    if kind == "seats":
        a1, d, k_ = rint(r, 12, 30), rint(r, 2, 4), rint(r, 10, 30)
        ask = pick(r, ["row", "total"]) if L else "row"
        if ask == "row":
            v = a1 + (k_ - 1) * d
            return Q(f"A theater has {a1} seats in the first row, and each row has {d} more seats than the row in front of it. How many seats are in row {k_}?", f"{v} seats",
                     [f"Arithmetic: {a_(1)} = {a1}, d = {d}.", f"{a_(k_)} = {a1} + ({k_} - 1)({d}) = {v}."], [f"{a1 + k_ * d} seats", f"{a1 * k_} seats", f"{k_ * d} seats"],
                     H(f"{a1} + ({k_} - 1)*{d}"), why=["Used n instead of n - 1", "Multiplied the first row by the number of rows", "Forgot the first row's seats"], tags=["modeling"])
        S = k_ * (2 * a1 + (k_ - 1) * d) // 2
        return Q(f"A theater has {a1} seats in the first row, and each row has {d} more seats than the row in front of it. There are {k_} rows. How many seats are there in all?", f"{S} seats",
                 [f"Last row: {a1} + ({k_} - 1)({d}) = {a1 + (k_ - 1) * d}.", f"Sum = {k_}({a1} + {a1 + (k_ - 1) * d})/2 = {S}."], [f"{k_ * (2 * a1 + (k_ - 1) * d)} seats", f"{a1 + (k_ - 1) * d} seats", f"{a1 * k_} seats"],
                 H(f"summation({a1} + (k - 1)*{d}, (k, 1, {k_}))"), why=["Forgot to divide by 2", "Gave only the last row", "Ignored the extra seats in each row"], tags=["modeling"])
    if kind == "salary":
        s0, pct, yr = rint(r, 35, 70) * 1000, pick(r, [2, 3, 4, 5]), rint(r, 3, 12)
        v = s0 * (1 + pct / 100) ** (yr - 1)
        return Q(f"A job pays ${s0:,} in year 1, with a {pct}% raise each year. What is the salary in year {yr}, to the nearest dollar?", f"${round(v):,}",
                 [f"Geometric: {a_(1)} = {s0}, r = {1 + pct / 100}.", f"{a_(yr)} = {s0}({1 + pct / 100})^{yr - 1} ≈ {round(v):,}."],
                 [f"${round(s0 * (1 + pct / 100) ** yr):,}", f"${round(s0 * (1 + pct * (yr - 1) / 100)):,}", f"${round(s0 * pct / 100 * yr + s0 * 0 + s0 * (yr - 1) * 0):,}"],
                 H(f"{s0}*(1 + Rational({pct}, 100))**({yr} - 1)", "round", places=0), why=["Used n instead of n - 1", "Used simple (arithmetic) raises", "Found only the raise amounts"], tags=["modeling"])
    h0, frac_, b = pick(r, [8, 10, 12, 15, 16, 20, 24, 27, 32]), pick(r, [sp.Rational(1, 2), sp.Rational(3, 4), sp.Rational(2, 3)]), rint(r, 2, 5)
    need((h0 * frac_ ** b).q == 1)
    v = h0 * frac_ ** b
    return Q(f"A ball is dropped from {h0} feet and rebounds to {T(frac_)} of its previous height each bounce. How high does it rise after the {ordn(b)} bounce?" if b > 3 else
             f"A ball is dropped from {h0} feet and rebounds to {T(frac_)} of its previous height each bounce. How high does it rise after bounce number {b}?", f"{T(v)} feet",
             [f"Each bounce multiplies the height by {T(frac_)}.", f"Height = {h0}({T(frac_)}){sup(b)} = {T(v)}."], [f"{T(h0 * frac_ ** (b - 1))} feet", f"{T(h0 - b * frac_ * h0) if h0 - b * frac_ * h0 > 0 else T(h0 * frac_ / b)} feet", f"{T(h0 * frac_ * b)} feet"],
             H(f"{h0}*Rational({frac_.p}, {frac_.q})**{b}"), why=["Used one bounce too few", "Subtracted a fixed amount each bounce", "Multiplied by the number of bounces"], tags=["modeling"])


SKILLS = {
    1: dict(name="Arithmetic sequences", fams=[s1_nth, s1_two_terms], extra=[err_of(s1_nth), err_of(s1_two_terms), open_of(s1_nth)]),
    2: dict(name="Geometric sequences", fams=[s2_nth, s2_ratio], extra=[err_of(s2_nth), err_of(s2_ratio), open_of(s2_nth)]),
    3: dict(name="Recursive and explicit formulas", fams=[s3_rec_terms, s3_to_explicit], extra=[err_of(s3_rec_terms), err_of(s3_to_explicit), open_of(s3_rec_terms)]),
    4: dict(name="Arithmetic series and sums", fams=[s4_sum], extra=[err_of(s4_sum), open_of(s4_sum)]),
    5: dict(name="Geometric series and sums", fams=[s5_sum], extra=[err_of(s5_sum), open_of(s5_sum)]),
    6: dict(name="Sigma notation", fams=[s6_eval, s6_write], extra=[err_of(s6_eval), err_of(s6_write), open_of(s6_eval)]),
    7: dict(name="Finite and infinite geometric series", fams=[s7_infinite, s5_sum], extra=[err_of(s7_infinite), open_of(s7_infinite)]),
    8: dict(name="Applications of sequences", fams=[s8_apps], extra=[err_of(s8_apps), open_of(s8_apps)]),
}
