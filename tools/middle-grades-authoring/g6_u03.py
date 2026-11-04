"""Grade 6 Unit 3 — Rational Numbers (rational-numbers)."""
from glib import *
import g7_u01 as A7, g7_u05 as F7

UNIT_ID = "rational-numbers"
ABBR = "rat"


def rq(r, L):
    """A rational number suited to the level: integer, then halves/quarters, then tenths and thirds."""
    if L == 0:
        return F(nz(r, -12, 12))
    if L == 1:
        return F(nz(r, -24, 24), pick(r, [2, 4]))
    return pick(r, [F(nz(r, -99, 99), 10), F(nz(r, -20, 20), 3)])


def qt(x):
    x = F(x)
    return D(x) if is_term(x) and x.denominator in (1, 2, 4, 5, 10) and pick_dec[0] else N(x)


pick_dec = [True]


# ============================================================== S1 Positive and Negative Numbers
@fam("012")
def s1_context(r, L):
    a = r.randint(2, 500) if L else r.randint(2, 50)
    ctx = [("a temperature {a} degrees below zero", -1), ("a deposit of ${a}", 1), ("a loss of {a} yards", -1), ("{a} feet above sea level", 1), ("{a} meters below sea level", -1),
           ("a withdrawal of ${a}", -1), ("a gain of {a} points", 1), ("an elevator going down {a} floors", -1)]
    t, s = pick(r, ctx)
    v = s * a
    if L == 2 and r.random() < 0.5:
        x = F(r.randint(1, 99), 4)
        need(x.denominator > 1)
        t, s = pick(r, ctx[:5])
        v = s * x
        t = t.replace("{a}", mixed(x))
        return Q(f"Write a rational number to represent {t}. Then state what 0 represents.", f"{mixed(v)}; 0 represents {'zero degrees' if 'temperature' in t else 'no change' if 'deposit' in t or 'loss' in t else 'sea level'}",
                 ["Above, gain, deposit → positive; below, loss → negative.", f"The number is {mixed(v)}.", "0 is the reference point."],
                 [f"{mixed(-v)}; 0 represents {'zero degrees' if 'temperature' in t else 'no change' if 'deposit' in t or 'loss' in t else 'sea level'}"],
                 PY("signed_ctx", v=N(v)), mode="sa", why=["Used the wrong sign"], tags=["modeling"])
    return Q(f"Write an integer to represent {t.format(a=a)}.", str(v), ["Below, loss, down, withdrawal → negative; above, gain, deposit → positive.", f"{v}."], [str(-v), "0", str(abs(v) + 10)], V(str(v)),
             why=["Used the wrong sign", "", ""], tags=["modeling"])


@fam("012")
def s1_opposite(r, L):
    x = rq(r, L)
    t = N(x) if L != 2 or not is_term(x) else D(x)
    if L == 2 and r.random() < 0.5:
        return Q(f"What is the opposite of the opposite of {t}?", t, [f"The opposite of {t} is {N(-x) if '/' in t else D(-x) if is_term(x) else N(-x)}.", f"The opposite of that is {t}."],
                 [N(-x) if "/" in t or not is_term(x) else D(-x), "0", N(1 / x) if x not in (1, -1) else "2"], V(f"-(-({N(x)}))"), why=["Took the opposite only once", "", "Took the reciprocal"])
    return Q(f"What is the opposite of {t}?", N(-x) if "/" in t or not is_term(x) else D(-x), ["Opposites are the same distance from 0 on opposite sides of 0.", f"The opposite of {t} is {N(-x) if '/' in t or not is_term(x) else D(-x)}."],
             [t, N(1 / x) if x not in (1, -1) else "0", N(abs(x)) if x < 0 else "0"] if True else [], V(f"-({N(x)})"), why=["Gave the same number", "Gave the reciprocal", "Gave the absolute value"])


# ============================================================== S2 On the number line
@fam("012")
def s2_read(r, L):
    den = 1 if L == 0 else pick(r, [2, 4]) if L == 1 else pick(r, [3, 4, 5])
    lo = -4 if L else -8
    hi = lo + (8 if L else 16)
    k = r.randint(lo * den + 1, hi * den - 1)
    need(k % den != 0 or den == 1)
    x = F(k, den)
    need(x != 0)
    lab = "A"
    alt = f"Number line from {lo} to {hi} with tick marks every {N(F(1, den))}; whole numbers are labelled. Point A is at {mixed(x)}."
    ans = mixed(x) if den > 1 else str(k)
    return Q(f"What number is at point A on the number line shown?", ans, [f"Each tick mark is {N(F(1, den))} unit.", f"Count from the nearest labelled whole number.", f"A = {ans}."],
             [mixed(-x), mixed(x + F(1, den)), mixed(x - F(1, den))], V(N(x)), why=["Read on the wrong side of zero", "Miscounted a tick mark", "Miscounted a tick mark"],
             diagram={"alt": alt, "draw": numline_draw(lo, hi, points=[(x, lab, True)], step=F(1, den), label_every=den, labels=lambda v: N(v))}, tags=["graph"])


@fam("012", mode="mc")
def s2_between(r, L):
    a = r.randint(-9, 8)
    x = F(a) + pick(r, [F(1, 2), F(1, 4), F(3, 4)]) if L else F(a) + F(1, 2)
    xs = mixed(x)
    good = f"{math.floor(x)} and {math.floor(x) + 1}"
    bad = [f"{math.floor(x) - 1} and {math.floor(x)}", f"{math.floor(x) + 1} and {math.floor(x) + 2}", f"{-math.floor(x) - 1} and {-math.floor(x)}"]
    opts = [(good, True)] + [(b, False) for b in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Between which two consecutive integers is {xs} on the number line?", good, [f"{xs} = {D(x)}.", f"It lies between {good}."], options=opts, chk=PY("between_ints", num=N(x)), mode="mc")


# ============================================================== S3 Comparing and ordering
@fam("012")
def s3_compare(r, L):
    a, b = rq(r, L), rq(r, L)
    need(a != b)
    sa = N(a) if a.denominator != 1 and (L == 1 or r.random() < 0.5) else (D(a) if is_term(a) else N(a))
    sb = N(b) if b.denominator != 1 and (L == 1 or r.random() < 0.5) else (D(b) if is_term(b) else N(b))
    ans = "<" if a < b else ">"
    return Q(f"Compare using <, >, or =: {sa} ___ {sb}", ans, ["Think of a number line: numbers to the right are greater.", f"{sa} is to the {'left' if a < b else 'right'} of {sb}.", f"{sa} {ans} {sb}."],
             [">" if ans == "<" else "<", "="], PY("cmp", a=N(a), b=N(b)), mode="sa", why=["Compared the absolute values instead", ""])


@fam("012")
def s3_order(r, L):
    vals = set()
    while len(vals) < 4:
        vals.add(rq(r, L))
    vals = sorted(vals)
    txt = [mixed(v) if v.denominator > 1 and r.random() < 0.6 else (D(v) if is_term(v) else N(v)) for v in vals]
    need(len(set(txt)) == 4)
    shown = txt[:]
    r.shuffle(shown)
    need(shown != txt)
    by_abs = [t for _, t in sorted(zip(vals, txt), key=lambda p: abs(p[0]))]
    return Q(f"Order from least to greatest: {', '.join(shown)}", ", ".join(txt), ["Place the numbers on a number line.", "The farther left, the lesser the number.", f"{', '.join(txt)}."],
             [", ".join(txt[::-1]), ", ".join(by_abs) if by_abs != txt else ", ".join(txt[1:] + txt[:1]), ", ".join(sorted(txt))], PY("order", items=txt),
             why=["Ordered from greatest to least", "Ordered by distance from 0", "Ordered the digits as text"])


@fam("012")
def s3_count_ints(r, L):
    a = F(nz(r, -12, 12), pick(r, [2, 4, 3] if L == 2 else [2, 4]))
    b = F(nz(r, -12, 12), pick(r, [2, 4, 3] if L == 2 else [2, 4]))
    lo, hi = min(a, b), max(a, b)
    need(hi - lo >= 2 and lo.denominator > 1 and hi.denominator > 1)
    n = math.floor(hi) - math.ceil(lo) + 1
    extra = [] if L < 2 else [f"Write the endpoints as mixed numbers or decimals: {mixed(lo)} ≈ {Rd(lo, 2)} and {mixed(hi)} ≈ {Rd(hi, 2)}.", "Neither endpoint is an integer, so no endpoint is counted.",
                              f"Count: {math.floor(hi)} - ({math.ceil(lo)}) + 1 = {n}."]
    return Q(f"How many integers are between {mixed(lo)} and {mixed(hi)}?" + (" Use a number line to justify your count." if L == 2 else ""), str(n),
             extra[:2] + [f"The least integer greater than {mixed(lo)} is {math.ceil(lo)}.", f"The greatest integer less than {mixed(hi)} is {math.floor(hi)}.", f"Count from {math.ceil(lo)} to {math.floor(hi)}: {n} integers."] + extra[2:],
             [str(n + 1), str(n - 1), str(math.floor(hi) - math.floor(lo))] if math.floor(hi) - math.floor(lo) not in (n, n + 1, n - 1) else [str(n + 1), str(n - 1), str(n + 2)],
             PY("count_ints", lo=N(lo), hi=N(hi)), why=["Counted one extra integer", "Left out an integer at an end", ""], tags=["reasoning"])


# ============================================================== S4 Writing and interpreting inequality statements
@fam("012")
def s4_statement(r, L):
    a, b = rq(r, L), rq(r, L)
    need(a != b)
    ctx = pick(r, ["temperature", "elevation", "account"])
    if ctx == "temperature":
        t = f"The temperature in Town A is {N(a)}°C and in Town B is {N(b)}°C. Write an inequality comparing A to B, and say which town is warmer."
        warm = "Town A" if a > b else "Town B"
    elif ctx == "elevation":
        t = f"A fish is at {N(a)} m and a diver is at {N(b)} m relative to sea level. Write an inequality comparing the fish to the diver, and say which is higher."
        warm = "the fish" if a > b else "the diver"
    else:
        t = f"Ava's balance is ${N(a)} and Ben's is ${N(b)}. Write an inequality comparing Ava to Ben, and say who has more money."
        warm = "Ava" if a > b else "Ben"
    op = ">" if a > b else "<"
    ans = f"{N(a)} {op} {N(b)}; {warm}"
    other = {"Town A": "Town B", "Town B": "Town A", "the fish": "the diver", "the diver": "the fish", "Ava": "Ben", "Ben": "Ava"}[warm]
    return Q(t, ans, [f"On a number line, {N(a)} is to the {'right' if a > b else 'left'} of {N(b)}.", f"{N(a)} {op} {N(b)}.", f"So {warm} is greater."],
             [f"{N(a)} {'<' if op == '>' else '>'} {N(b)}; {other}", f"{N(a)} {op} {N(b)}; {other}", f"{N(a)} {'<' if op == '>' else '>'} {N(b)}; {warm}"], PY("ineq_stmt", a=N(a), b=N(b), win=warm, lose=other),
             why=["Compared the absolute values", "Wrote the right inequality but chose the wrong one", "Reversed the inequality"], tags=["modeling"])


@fam("012", mode="mc")
def s4_interpret(r, L):
    a, b = sorted(r.sample(range(-20, 0), 2))
    good = f"{a}°F is colder than {b}°F."
    opts = [(good, True), (f"{a}°F is warmer than {b}°F.", False), (f"{b}°F is colder than {a}°F.", False), ("The temperatures are equal.", False)]
    r.shuffle(opts)
    return Q(f"Which statement explains {a} < {b} in terms of temperature?", good, [f"{a} is to the left of {b} on a number line.", "A lesser temperature is colder."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


# ============================================================== S5 / S6 Absolute value
@fam("012")
def s5_abs(r, L):
    x = rq(r, L)
    t = N(x) if x.denominator > 1 or r.random() < 0.5 else D(x)
    if L == 2 and r.random() < 0.5:
        y = rq(r, L)
        e = f"|{N(x)}| + |{N(y)}|"
        v = abs(x) + abs(y)
        return Q(f"Evaluate: {e}", N(v), ["Absolute value is distance from 0, so it is never negative.", f"|{N(x)}| = {N(abs(x))} and |{N(y)}| = {N(abs(y))}.", f"Sum: {N(v)}."],
                 [N(x + y) if x + y != v else N(v + 1), N(-v), N(abs(x + y)) if abs(x + y) != v else N(v + 2)], PY("absval", expr=e), why=["Ignored the absolute value bars", "Made the answer negative", "Added before taking absolute values"])
    return Q(f"What is |{t}|?", N(abs(x)) if "/" in t else D(abs(x)) if is_term(x) else N(abs(x)), ["Absolute value is the distance from 0.", f"|{t}| = {N(abs(x))}."],
             [N(-abs(x)), N(1 / abs(x)) if abs(x) != 1 else "2", "0", N(abs(x) + 1)], PY("absval", expr=f"|{N(x)}|"), why=["Thought absolute value makes a number negative", "Took the reciprocal", "", ""])


@fam("012")
def s6_order_abs(r, L):
    vals = set()
    while len(vals) < 4:
        vals.add(rq(r, L))
    vals = list(vals)
    need(len({abs(v) for v in vals}) == 4)
    srt = sorted(vals, key=abs)
    txt = {v: N(v) for v in vals}
    shown = [txt[v] for v in vals]
    return Q(f"Order by absolute value, from least to greatest: {', '.join(shown)}", ", ".join(txt[v] for v in srt), ["Find each absolute value (distance from 0).", ", ".join(f"|{txt[v]}| = {N(abs(v))}" for v in srt) + ".", "Order by those distances."],
             [", ".join(txt[v] for v in sorted(vals)), ", ".join(txt[v] for v in srt[::-1]), ", ".join(sorted(shown))], PY("order_abs", items=shown),
             why=["Ordered by value instead of absolute value", "Ordered from greatest to least", "Ordered as text"])


@fam("012")
def s6_context(r, L):
    a, b = r.sample(range(5, 90), 2)
    nm1, nm2 = r.sample(NAMES, 2)
    return Q(f"{nm1}'s account balance is -${a} and {nm2}'s is -${b}. Who owes more money, and how much more?", f"{nm1 if a > b else nm2}, ${abs(a - b)}",
             [f"A debt of ${a} is |-{a}| = {a}; a debt of ${b} is {b}.", f"The greater absolute value is the greater debt: {max(a, b)}.", f"{nm1 if a > b else nm2} owes ${abs(a - b)} more."],
             [f"{nm2 if a > b else nm1}, ${abs(a - b)}", f"{nm1 if a > b else nm2}, ${a + b}", f"{nm2 if a > b else nm1}, ${a + b}"], PY("debt", a=a, b=b, n1=nm1, n2=nm2),
             why=["Thought the greater negative number is the larger debt", "Added the debts", ""], tags=["modeling"])


@fam("012")
def s6_count_abs(r, L):
    k = r.randint(2, 6)
    kind = pick(r, ["<", "≤"]) if L else "<"
    n = 2 * k - 1 if kind == "<" else 2 * k + 1
    extra = [] if L < 2 else ["Positive integers that work: " + ", ".join(str(x) for x in range(1, k + (0 if kind == "<" else 1))) + ".", "Each has an opposite that also works, and 0 works too.",
                              f"Count: 2 × {k - (1 if kind == '<' else 0)} + 1 = {n}."]
    lead = "" if L < 2 else "Think about distance from 0 on a number line. "
    return Q(f"{lead}How many integers n make |n| {kind} {k} true?", str(n), [f"|n| {kind} {k} means n is {'less than' if kind == '<' else 'at most'} {k} units from 0.",
                                                                     f"The integers are {', '.join(str(x) for x in range(-k + (1 if kind == '<' else 0), k + (0 if kind == '<' else 1)))}."] + extra + [f"There are {n}."],
             [str(k), str(2 * k), str(n + 2) if kind == "<" else str(2 * k - 1)], PY("count_abs", k=k, op=kind), why=["Counted only the positive integers", "Left out 0 or an endpoint", "Included the endpoints"], tags=["reasoning"])


# ============================================================== S7-S9 coordinate plane
@fam("012", mode="mc")
def s7_reflect_desc(r, L):
    x, y = nz(r, -9, 9), nz(r, -9, 9)
    ax = pick(r, ["x-axis", "y-axis", "both axes"])
    nx, ny = (x, -y) if ax == "x-axis" else (-x, y) if ax == "y-axis" else (-x, -y)
    good = f"({nx}, {ny})"
    opts = [(good, True)] + [(f"({a}, {b})", False) for a, b in {(x, -y), (-x, y), (-x, -y), (y, x)} - {(nx, ny)}][:3]
    r.shuffle(opts)
    return Q(f"Point ({x}, {y}) is reflected across the {ax}. What are the coordinates of the image?", good,
             ["Reflecting across the x-axis changes the sign of y; across the y-axis changes the sign of x; across both changes both.", f"Image: {good}."], options=opts, chk=PY("point", x=str(nx), y=str(ny)), mode="mc")


SKILLS = {
    1: dict(name="Positive and Negative Numbers", std=["6.NS.C.5"], fams=[s1_context, s1_opposite], extra=[err_of(s1_opposite), open_of(s1_opposite)]),
    2: dict(name="Positive and Negative Numbers on the Number Line", std=["6.NS.C.6a", "6.NS.C.6c"], fams=[s2_read, s2_between, reuse(A7.s5_numline), s3_count_ints], extra=[err_of(s2_read), err_of(reuse(A7.s5_opposite, (0, 1, 1)))]),
    3: dict(name="Comparing and Ordering Rational Numbers", std=["6.NS.C.7a"], fams=[s3_compare, s3_order, s3_count_ints], extra=[err_of(s3_order), open_of(s3_order), select_of(s3_count_ints)]),
    4: dict(name="Writing and Interpreting Inequality Statements", std=["6.NS.C.7b"], fams=[s4_statement, s4_interpret], extra=[err_of(s4_statement), open_of(s4_statement)]),
    5: dict(name="Absolute Value of Rational Numbers", std=["6.NS.C.7c"], fams=[s5_abs, reuse(A7.s5_solve_abs, (2, 2, 2)), s6_count_abs], extra=[err_of(s5_abs), open_of(s5_abs), select_of(s5_abs)]),
    6: dict(name="Absolute Value and Ordering Numbers", std=["6.NS.C.7d"], fams=[s6_order_abs, s6_context, s6_count_abs], extra=[err_of(s6_order_abs), open_of(s6_order_abs)]),
    7: dict(name="Rational Numbers and the Coordinate Plane", std=["6.NS.C.6b"], fams=[reuse(A7.s12_quadrant), s7_reflect_desc, reuse(A7.s12_reflect, (2, 2, 2))], extra=[err_of(reuse(A7.s12_quadrant, (0, 1, 2), "e")), open_of(reuse(A7.s12_reflect, (2, 2, 2), "o"))]),
    8: dict(name="Ordered Pairs on the Coordinate Plane", std=["6.NS.C.6c", "6.NS.C.8"], fams=[reuse(A7.s12_read)], extra=[err_of(reuse(A7.s12_read, (0, 1, 2), "e")), err_of(reuse(A7.s12_quadrant, (0, 1, 2), "q"))]),
    9: dict(name="Distance on the Coordinate Plane", std=["6.NS.C.8"], fams=[reuse(A7.s12_distance, (1, 1, 2)), reuse(A7.s12_rect, (2, 2, 2))], extra=[err_of(reuse(A7.s12_distance, (1, 1, 2), "e")), open_of(reuse(A7.s12_distance, (1, 1, 2), "o"))]),
}
