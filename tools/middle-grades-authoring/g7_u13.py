"""Grade 7 Unit 13 — Nonlinear Functions and Polynomials (nonlinear-functions-polynomials)."""
from glib import *

UNIT_ID = "nonlinear-functions-polynomials"
ABBR = "nfp"


def poly(terms, v="x"):
    """terms: {exp: coef} → standard-form text."""
    out = []
    for e in sorted(terms, reverse=True):
        c = F(terms[e])
        if c == 0:
            continue
        body = (v + (sup(e) if e > 1 else "")) if e else ""
        ct = N(abs(c)) if (abs(c) != 1 or not body) else ""
        t = ct + body
        out.append(("-" if c < 0 else "") + t if not out else (" - " if c < 0 else " + ") + t)
    return "".join(out) or "0"


def rpoly(r, deg, lo=-9, hi=9, full=True):
    t = {e: nz(r, lo, hi) for e in range(deg + 1)}
    if not full:
        for e in range(deg):
            if r.random() < 0.3:
                t[e] = 0
    return t


# ============================================================== S1 Patterns and Sequences
@fam("012")
def s1_nth(r, L):
    a, d = r.randint(-10, 20), nz(r, -9, 9)
    n = r.randint(10, 30) if L < 2 else r.randint(40, 100)
    seq = [a + d * i for i in range(4)]
    return Q(f"Find term {n} of the arithmetic sequence {', '.join(map(str, seq))}, …", str(a + d * (n - 1)), [f"Common difference d = {d}.", f"aₙ = a₁ + (n - 1)d = {a} + ({n} - 1)({d}).", f"a{''.join('₀₁₂₃₄₅₆₇₈₉'[int(c)] for c in str(n))} = {a + d * (n - 1)}."],
             [str(a + d * n), str(d * n), str(seq[-1] + d * (n - 4) + d)], PY("nth_term", seq=seq, n=n), why=["Used n instead of n - 1", "Forgot the first term", "Counted one term too many"])


@fam("012", mode="mc")
def s1_type(r, L):
    kind = pick(r, ["arithmetic", "geometric", "neither"])
    a = r.randint(1, 6)
    if kind == "arithmetic":
        d = nz(r, -7, 7)
        seq = [a + d * i for i in range(5)]
    elif kind == "geometric":
        q = pick(r, [2, 3, -2, 4])
        seq = [a * q ** i for i in range(5)]
    else:
        seq = [(i + a) ** 2 for i in range(5)] if r.random() < 0.5 else [a + i * (i + 1) // 2 * 3 for i in range(5)]
    opts = [(k, k == kind) for k in ["arithmetic", "geometric", "neither"]] + [("both arithmetic and geometric", False)]
    return Q(f"Is the sequence {', '.join(map(str, seq))}, … arithmetic, geometric, or neither?", kind, ["Arithmetic: constant difference. Geometric: constant ratio.", f"Differences: {', '.join(str(b - c) for c, b in zip(seq, seq[1:]))}.", f"The sequence is {kind}."],
             options=opts, chk=PY("seq_type", seq=seq), mode="mc")


@fam("012")
def s1_ratio(r, L):
    a = nz(r, -5, 6)
    q = pick(r, [2, 3, -2, -3, 5]) if L < 2 else pick(r, [F(1, 2), F(-1, 2), F(3, 2)])
    seq = [F(a * (24 if L == 2 else 1)) * F(q) ** i for i in range(4)]
    need(all(x.denominator == 1 for x in seq))
    nxt = seq[-1] * q
    return Q(f"Find the common ratio and the next term of the geometric sequence {', '.join(N(x) for x in seq)}, …. Give the next term.", N(nxt),
             [f"Common ratio = {N(seq[1])} ÷ {N(seq[0])} = {N(F(q))}.", f"Next term = {N(seq[-1])} × {N(F(q))} = {N(nxt)}."], [N(seq[-1] + (seq[-1] - seq[-2])), N(-nxt), N(seq[-1] * 2) if q != 2 else N(seq[-1] * 3)],
             PY("next_term", seq=[N(x) for x in seq]), why=["Used a common difference instead of a ratio", "Made a sign error", "Multiplied by the wrong ratio"])


# ============================================================== S2 Graphing Nonlinear Functions
NL = [("y = x²", lambda x: x * x), ("y = -x²", lambda x: -x * x), ("y = |x|", lambda x: abs(x)), ("y = x² - 3", lambda x: x * x - 3), ("y = x³", lambda x: x ** 3), ("y = 2|x| - 1", lambda x: 2 * abs(x) - 1)]


@fam("012")
def s2_table(r, L):
    f, fn = pick(r, NL if L else NL[:4])
    x = nz(r, -4, 4)
    v = fn(x)
    rhs = f.split("= ")[1]
    ex = rhs.replace("x", f"({x})").replace("|", "§")
    return Q(f"For {f}, find y when x = {x}.", str(v), [f"Substitute x = {x}.", f"{rhs.replace('x', par(x))} = {v}."], [str(-v) if v else "1", str(2 * x if "²" in f else 3 * x if "³" in f else x), str(v + 1)],
             PY("absval", expr=rhs.replace("x", f"({x})")), why=["Made a sign error (for example, (-a)² vs -a²)", "Multiplied by the exponent instead of using it as a power", ""])


def curve_draw(fn):
    xs = [i / 10 for i in range(-50, 51)]
    pts = [(x, fn(x)) for x in xs if -7 <= fn(x) <= 7]
    return plane_draw((-6, 6), (-7, 7), polys=[(pts, None, None, False)])


@fam("12", mode="mc")
def s2_choose(r, L):
    idx = r.sample(range(len(NL)), 4)
    ans_i = r.randrange(4)
    f = NL[idx[ans_i]][0]
    labs = "ABCD"
    alt = "Four graphs. " + " ".join(f"Graph {labs[k]}: {NL[i][0]}." for k, i in enumerate(idx))
    drawers = []
    for i in idx:
        fn = NL[i][1]
        pts = [(x / 10, fn(x / 10)) for x in range(-50, 51) if -7 <= fn(x / 10) <= 7]
        drawers.append(plane_draw((-6, 6), (-7, 7), polys=[(pts, "#1f4e9c", None, False)], label_every=2))
    for d in drawers:
        orig = d.draw_on

        def wrapped(ax, orig=orig):
            orig(ax)
            for ln in ax.get_lines():
                ln.set_marker("")
        d.draw_on = wrapped
    return Q(f"Which graph shows {f}?", f"Graph {labs[ans_i]}", [f"Make a table for {f}: x = -2, -1, 0, 1, 2.", "Plot the points and compare the shape (U-shape, V-shape, or S-shape) and the y-intercept.", f"Graph {labs[ans_i]} matches."],
             options=[(f"Graph {labs[k]}", k == ans_i) for k in range(4)], chk=PY("graph_choice", f=f, graphs={f"Graph {labs[k]}": NL[i][0] for k, i in enumerate(idx)}), mode="mc", tags=["graph"],
             diagram={"alt": alt, "draw": panels_draw(drawers)})


@fam("012", mode="mc")
def s2_linear(r, L):
    m, b = nz(r, -5, 5), r.randint(-5, 5)
    lin_ = f"y = {lin((m, 'x'), (b, ''))}"
    nonl = r.sample(["y = x² + 1", "y = 3x²", f"y = {abs(m) + 1}ˣ" if False else "y = 2x³", "y = |x| + 2", "y = x² - 4x"], 3)
    ask = pick(r, ["linear", "nonlinear"])
    if ask == "linear":
        opts = [(lin_, True)] + [(n, False) for n in nonl]
    else:
        lins = [f"y = {lin((nz(r, -5, 5), 'x'), (r.randint(-5, 5), ''))}" for _ in range(3)]
        need(len(set(lins)) == 3)
        opts = [(nonl[0], True)] + [(x, False) for x in lins]
    r.shuffle(opts)
    return Q(f"Which function is {ask}?", [o for o, t in opts if t][0], ["A linear function has the form y = mx + b (x to the first power only).", "Squares, cubes, and absolute values make a function nonlinear."], options=opts,
             chk=PY("is_linear_fn", want=ask), mode="mc")


# ============================================================== S3 Exponential Growth and Decay
@fam("012")
def s3_eval(r, L):
    a = r.randint(2, 50) * 10
    pc = pick(r, [10, 20, 25, 50, 5, 8, 15])
    t = r.randint(2, 4) if L < 2 else r.randint(3, 8)
    up = r.random() < 0.6
    v = a * (1 + F(pc, 100) if up else 1 - F(pc, 100)) ** t
    ctx = f"A town of {a:,} people grows {pc}% per year" if up else f"A ${a:,} car loses {pc}% of its value each year"
    q = f"{ctx}. What is the {'population' if up else 'value'} after {t} years? Round to the nearest {'whole number' if up else 'cent'}."
    ans = Rd(v, 0) if up else "$" + Rd(v, 2)
    ex = f"{a}*(1 {'+' if up else '-'} {pc}/100)^{t}"
    lin_v = a * (1 + F(pc * t, 100)) if up else a * (1 - F(pc * t, 100))
    return Q(q, ans, [f"y = a(1 {'+' if up else '-'} r)ᵗ.", f"y = {a}({D(1 + F(pc, 100) if up else 1 - F(pc, 100))}){sup(t)}.", f"y ≈ {ans}."],
             [Rd(lin_v, 0) if up else "$" + Rd(lin_v, 2), Rd(a * (1 - F(pc, 100) if up else 1 + F(pc, 100)) ** t, 0) if up else "$" + Rd(a * (1 + F(pc, 100)) ** t, 2), Rd(a * F(pc, 100) ** t, 0) if up else "$" + Rd(a * F(pc, 100) ** t, 2)],
             AP(ex, 0 if up else 2), why=["Added the same amount each year (linear thinking)", "Used decay instead of growth" if up else "Used growth instead of decay", "Used the rate as the growth factor"], tags=["modeling"])


@fam("012", mode="mc")
def s3_classify(r, L):
    a = r.randint(2, 100)
    b = pick(r, [F(3, 2), 2, F(5, 4), F(1, 2), F(3, 4), F(9, 10), 3, F(1, 3)])
    f = f"y = {a}({D(b) if is_term(b) else N(b)})ˣ"
    kind = "exponential growth" if b > 1 else "exponential decay"
    opts = [("exponential growth", b > 1), ("exponential decay", b < 1), ("linear growth", False), ("linear decay", False)]
    return Q(f"Does {f} show exponential growth or exponential decay?", kind, ["In y = a·bˣ, b > 1 means growth and 0 < b < 1 means decay.", f"b = {D(b) if is_term(b) else N(b)}, so it is {kind}."], options=opts,
             chk=PY("growth_decay", b=str(b)), mode="mc")


@fam("12")
def s3_doubling(r, L):
    a, t, d = r.randint(2, 20) * 50, pick(r, [2, 3, 4, 5, 6]), r.randint(3, 6)
    T = t * d
    return Q(f"A bacteria sample of {a} cells doubles every {t} hours. How many cells are there after {T} hours?", f"{a * 2 ** d:,}", [f"Number of doublings: {T} ÷ {t} = {d}.", f"{a} × 2{sup(d)} = {a} × {2 ** d}.", f"= {a * 2 ** d:,} cells."],
             [f"{a * 2 * d:,}", f"{a * 2 ** T:,}" if T < 20 else f"{a * 2 ** (d + 1):,}", f"{a + 2 ** d:,}"], V(f"{a}*2^({T}/{t})"), why=["Multiplied by 2 times the number of doublings", "Used hours instead of doublings", "Added instead of multiplying"],
             tags=["modeling", "multistep"])


# ============================================================== S4 Polynomials
@fam("012")
def s4_degree(r, L):
    deg = r.randint(1, 5)
    t = rpoly(r, deg, full=False)
    if L == 2:
        y = pick(r, ["y", "z"])
        e1, e2 = r.randint(1, 4), r.randint(1, 4)
        c = nz(r, -9, 9)
        p_ = f"{c}x{sup(e1) if e1 > 1 else ''}{y}{sup(e2) if e2 > 1 else ''} + {poly(t)}"
        dg = max(e1 + e2, deg)
        return Q(f"What is the degree of the polynomial {p_}?", str(dg), ["The degree of a term is the sum of the exponents of its variables.", f"The term with x and {y} has degree {e1} + {e2} = {e1 + e2}.", f"The polynomial's degree is the greatest: {dg}."],
                 [str(max(e1, e2, deg)) if max(e1, e2, deg) != dg else str(dg + 1), str(len(t) + 1), str(c)], PY("poly_degree", p=p_), why=["Used the greatest single exponent", "Counted the terms", "Gave a coefficient"])
    p_ = poly(t)
    return Q(f"What is the degree of {p_}?", str(deg), ["The degree is the greatest exponent of the variable.", f"The greatest exponent is {deg}."],
             [str(sum(1 for c in t.values() if c)), str(t[deg]), str(deg + 1)], PY("poly_degree", p=p_), why=["Counted the terms", "Gave the leading coefficient", ""])


@fam("012", mode="mc")
def s4_classify(r, L):
    k = r.randint(1, 3)
    deg = r.randint(k - 1, 4)
    exps = sorted(r.sample(range(0, deg + 1), k), reverse=True) if deg + 1 >= k else None
    need(exps is not None)
    p_ = poly({e: nz(r, -9, 9) for e in exps})
    nm = {1: "monomial", 2: "binomial", 3: "trinomial"}[k]
    opts = [(x, x == nm) for x in ["monomial", "binomial", "trinomial"]] + [("not a polynomial", False)]
    return Q(f"Classify {p_} by its number of terms.", nm, [f"{p_} has {k} term{'s' if k > 1 else ''}.", f"It is a {nm}."], options=opts, chk=PY("poly_terms", p=p_), mode="mc")


@fam("012")
def s4_eval(r, L):
    t = rpoly(r, 2 if L < 2 else 3, -6, 6)
    x = nz(r, -3, 4)
    p_ = poly(t)
    v = sum(c * x ** e for e, c in t.items())
    return Q(f"Evaluate {p_} when x = {x}.", str(v), [f"Substitute x = {x}: " + " + ".join(f"{c}({x}){sup(e) if e > 1 else ''}" if e else str(c) for e, c in sorted(t.items(), reverse=True)) + ".", "Evaluate powers, then multiply, then add.", f"= {v}."],
             [str(sum(c * x * e for e, c in t.items()) + t.get(0, 0)), str(sum(c * (-x) ** e for e, c in t.items())), str(v + 2)], EQV(p_) if False else V(p_.replace("x", f"({x})")),
             why=["Multiplied by the exponent instead of raising to a power", "Made a sign error with the negative value", ""])


# ============================================================== S5 Add/subtract polynomials
@fam("012")
def s5_addsub(r, L):
    deg = 1 if L == 0 else 2
    a, b = rpoly(r, deg), rpoly(r, deg)
    op = pick(r, ["+", "-"]) if L else "+"
    res = {e: a.get(e, 0) + (b.get(e, 0) if op == "+" else -b.get(e, 0)) for e in range(deg + 1)}
    need(any(res.values()))
    pa, pb = poly(a), poly(b)
    e = f"({pa}) {op} ({pb})"
    wrong1 = {k: a.get(k, 0) - b.get(k, 0) if op == "+" else a.get(k, 0) + b.get(k, 0) for k in range(deg + 1)}
    wrong2 = {k: (a.get(k, 0) - b.get(k, 0) if k == deg else a.get(k, 0) + b.get(k, 0)) if op == "-" else res[k] + (1 if k == 0 else 0) for k in range(deg + 1)}
    wrong3 = {k + 1 if k else 0: v for k, v in res.items()}
    return Q(f"Simplify: {e}", poly(res), ["Remove the parentheses (for subtraction, change the sign of every term in the second polynomial)." if op == "-" else "Remove the parentheses.", "Combine like terms.", f"Result: {poly(res)}."],
             [poly(wrong1), poly(wrong2), poly(wrong3)], PY("poly_std", expr=e), why=["Used the wrong operation", "Subtracted only the first term of the second polynomial" if op == "-" else "Made an arithmetic error", "Added the exponents when combining"])


@fam("12")
def s5_perimeter(r, L):
    a, b = rpoly(r, 1, 1, 9), rpoly(r, 1, 1, 9)
    res = {e: 2 * a[e] + 2 * b[e] for e in (0, 1)}
    return Q(f"A rectangle has length ({poly(a)}) and width ({poly(b)}). Write a simplified expression for its perimeter.", poly(res), ["P = 2l + 2w.", f"2({poly(a)}) + 2({poly(b)}).", f"= {poly(res)}."],
             [poly({e: a[e] + b[e] for e in (0, 1)}), poly({2: a[1] * b[1], 1: a[1] * b[0] + a[0] * b[1], 0: a[0] * b[0]}), poly({e: 2 * a[e] + b[e] for e in (0, 1)})],
             PY("poly_std", expr=f"2({poly(a)}) + 2({poly(b)})"), why=["Added only one length and one width", "Found the area", "Doubled only the length"], tags=["connections"])


# ============================================================== S6 Polynomial × monomial
@fam("012")
def s6_mult(r, L):
    c, k = nz(r, -6, 6), r.randint(0, 2) if L else 0
    if L == 0:
        c = r.randint(2, 8)
    t = rpoly(r, 1 if L == 0 else 2, -7, 7)
    mono = (N(c) if abs(c) != 1 or k == 0 else ("-" if c < 0 else "")) + ("x" + (sup(k) if k > 1 else "") if k else "")
    res = {e + k: c * v for e, v in t.items()}
    e = f"{mono}({poly(t)})"
    w1 = {e + k: c * v if e == max(t) else v for e, v in t.items()}
    w2 = {e * (k if k else 1) + (0 if k else 0): c * v for e, v in t.items()} if k > 1 else {e + k: c * v + (1 if e == 0 else 0) for e, v in t.items()}
    w3 = {e + k: -c * v if e == 0 else c * v for e, v in t.items()}
    return Q(f"Simplify: {e}", poly(res), ["Distribute the monomial to every term.", "Multiply coefficients and add exponents of x.", f"Result: {poly(res)}."], [poly(w1), poly(w2), poly(w3)],
             PY("poly_std", expr=e), why=["Multiplied only the first term", "Multiplied the exponents" if k > 1 else "Made an arithmetic error", "Made a sign error"])


@fam("12")
def s6_area(r, L):
    a, b = r.randint(2, 9), r.randint(1, 9)
    return Q(f"A rectangle has width {a}x and length (x + {b}). Write a simplified expression for its area.", poly({2: a, 1: a * b}), [f"A = {a}x(x + {b}).", f"= {a}x² + {a * b}x."],
             [poly({1: a + 1, 0: b}), poly({2: a, 0: a * b}), poly({1: 2 * a + 2, 0: 2 * b})], PY("poly_std", expr=f"{a}x(x + {b})"), why=["Added instead of multiplying", "Forgot the x on the second term", "Found the perimeter"],
             tags=["connections"])


# ============================================================== S7 Multiplying binomials
@fam("012")
def s7_foil(r, L):
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    p, q = (1, 1) if L < 2 else (r.randint(1, 4), r.randint(1, 4))
    if L == 0:
        a, b = r.randint(1, 9), r.randint(1, 9)
    e = f"({poly({1: p, 0: a})})({poly({1: q, 0: b})})"
    res = {2: p * q, 1: p * b + q * a, 0: a * b}
    return Q(f"Multiply: {e}", poly(res), ["Use FOIL (or an area model): First, Outer, Inner, Last.", f"F: {poly({2: p * q})}; O: {poly({1: p * b})}; I: {poly({1: q * a})}; L: {a * b}.", f"Combine like terms: {poly(res)}."],
             [poly({2: p * q, 0: a * b}), poly({2: p * q, 1: a * b, 0: a + b}), poly({2: p * q, 1: p * b + q * a, 0: a + b})], PY("poly_std", expr=e),
             why=["Multiplied only the first terms and last terms", "Switched the middle and last terms", "Added the last terms instead of multiplying"])


@fam("12")
def s7_square(r, L):
    a = nz(r, -9, 9)
    e = f"({poly({1: 1, 0: a})})²"
    res = {2: 1, 1: 2 * a, 0: a * a}
    return Q(f"Expand: {e}", poly(res), [f"{e} = ({poly({1: 1, 0: a})})({poly({1: 1, 0: a})}).", "Multiply with FOIL.", f"= {poly(res)}."], [poly({2: 1, 0: a * a}), poly({2: 1, 1: a, 0: a * a}), poly({2: 1, 1: 2 * a, 0: 2 * a})],
             PY("poly_std", expr=e), why=["Squared each term and forgot the middle term", "Did not double the middle term", "Doubled the constant instead of squaring"], tags=["misconception"])


# ============================================================== S8 Using Multiple Strategies
@fam("012")
def s8_problem(r, L):
    kind = pick(r, ["area", "consec", "ages", "coins"]) if L else pick(r, ["ages", "coins"])
    if kind == "area":
        w, d = r.randint(2, 12), r.randint(1, 8)
        A = w * (w + d)
        return Q(f"A rectangle's length is {d} more than its width. Its area is {A} square units. Find the width. (Try a table or guess and check.)", f"{w} units",
                 ["Let the width be w; the length is w + " + str(d) + ".", f"Make a table of w and w(w + {d}), or guess and check.", f"w = {w}: {w} × {w + d} = {A}.", f"The width is {w} units."],
                 [f"{w + d} units", f"{N(F(A, 2))} units" if A % 2 == 0 else f"{w + 1} units", f"{N(F(A - d, 2))} units" if (A - d) % 2 == 0 else f"{w - 1} units"], PY("conds", vars=["w"], conds=[f"w*(w + {d}) = {A}", "w > 0"]),
                 why=["Gave the length", "Divided the area by 2", ""], tags=["reasoning"])
    if kind == "consec":
        n = r.randint(3, 20)
        return Q(f"The product of two consecutive positive integers is {n * (n + 1)}. What is the smaller integer?", str(n), ["Estimate: the integers are close to √" + str(n * (n + 1)) + ".", f"Test: {n} × {n + 1} = {n * (n + 1)}.", f"The smaller integer is {n}."],
                 [str(n + 1), str(n * (n + 1) // 2), str(n - 1)], PY("conds", vars=["n"], conds=[f"n*(n + 1) = {n * (n + 1)}", "n > 0"]), why=["Gave the larger integer", "Divided by 2", ""], tags=["reasoning"])
    if kind == "ages":
        k, c = r.randint(2, 4), r.randint(3, 15)
        tot = c * (k + 1)
        return Q(f"A mother is {k} times as old as her son. The sum of their ages is {tot}. How old is the son?", str(c), [f"Strategy 1 (equation): s + {k}s = {tot}, so {k + 1}s = {tot}.", f"Strategy 2 (table): try ages until the sum is {tot}.", f"s = {c}."],
                 [str(c * k), str(tot // k), str(tot - c)], PY("conds", vars=["s"], conds=[f"s + {k}s = {tot}"]), why=["Gave the mother's age", "Divided by the multiplier only", ""], tags=["modeling"])
    q, d = r.randint(2, 12), r.randint(2, 12)
    return Q(f"A jar has {q + d} quarters and dimes worth ${Rd(F(25 * q + 10 * d, 100), 2)}. How many quarters are there?", str(q),
             [f"Equation: 0.25q + 0.10({q + d} - q) = {Rd(F(25 * q + 10 * d, 100), 2)}.", "Or make a table of possible numbers of quarters.", f"q = {q}."], [str(d), str(q + 1), str((25 * q + 10 * d) // 25)],
             PY("conds", vars=["q"], conds=[f"25q + 10({q + d} - q) = {25 * q + 10 * d}"]), why=["Gave the number of dimes", "", "Divided the total by 25 cents"], tags=["modeling"])


SKILLS = {
    1: dict(name="Patterns and Sequences", std=["F-BF.A.2", "F-LE.A.2"], fams=[s1_nth, s1_type, s1_ratio], extra=[err_of(s1_nth), open_of(s1_nth)]),
    2: dict(name="Graphing Nonlinear Functions", std=["8.F.A.3", "F-IF.C.7"], fams=[s2_table, s2_choose, s2_linear], extra=[err_of(s2_table), open_of(s2_table)]),
    3: dict(name="Exponential Growth and Decay", std=["F-LE.A.1", "F-LE.A.2"], fams=[s3_eval, s3_classify, s3_doubling], extra=[err_of(s3_eval), open_of(s3_doubling)]),
    4: dict(name="Polynomials", std=["A-SSE.A.1"], fams=[s4_degree, s4_classify, s4_eval], extra=[err_of(s4_eval), open_of(s4_eval)]),
    5: dict(name="Adding and Subtracting Polynomials", std=["A-APR.A.1"], fams=[s5_addsub, s5_perimeter], extra=[err_of(s5_addsub), open_of(s5_addsub), select_of(s5_addsub)]),
    6: dict(name="Multiplying a Polynomial by a Monomial", std=["A-APR.A.1"], fams=[s6_mult, s6_area], extra=[err_of(s6_mult), open_of(s6_mult)]),
    7: dict(name="Multiplying Binomials", std=["A-APR.A.1"], fams=[s7_foil, s7_square], extra=[err_of(s7_foil), open_of(s7_foil), select_of(s7_foil)]),
    8: dict(name="Using Multiple Strategies", std=["MP.1", "7.EE.B.3"], fams=[s8_problem], extra=[err_of(s8_problem), open_of(s8_problem)]),
}
