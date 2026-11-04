"""Grade 7 Unit 1 — Algebraic Expressions and Integers (algebraic-expressions-integers)."""
from glib import *

UNIT_ID = "algebraic-expressions-integers"
ABBR = "aei"

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def words3(n):
    h, t = divmod(n, 100)
    out = []
    if h:
        out.append(ONES[h] + " hundred")
    if t:
        out.append(ONES[t] if t < 20 else TENS[t // 10] + ("-" + ONES[t % 10] if t % 10 else ""))
    return " ".join(out)


def words(n):
    if n == 0:
        return "zero"
    parts = []
    for div, nm in ((10 ** 6, "million"), (1000, "thousand"), (1, "")):
        k, n = divmod(n, div)
        if k:
            parts.append(words3(k) + (" " + nm if nm else ""))
    return ", ".join(parts)


def comma(n):
    return f"{n:,}"


def dtext(x):
    """Decimal text with thousands commas."""
    s = D(x)
    ip, _, fp = s.partition(".")
    return comma(int(ip)) + ("." + fp if fp else "")


PLACE = {10 ** 6: "millions", 10 ** 5: "hundred thousands", 10 ** 4: "ten thousands", 1000: "thousands", 100: "hundreds", 10: "tens", 1: "ones",
         F(1, 10): "tenths", F(1, 100): "hundredths", F(1, 1000): "thousandths"}


# ============================================================== S1 Place Value
@fam("012")
def s1_digit_value(r, L):
    places = [10 ** k for k in range(0, 7)] + ([F(1, 10), F(1, 100), F(1, 1000)] if L else [])
    digs = [r.randint(1, 9)] + [r.randint(0, 9) for _ in range(6)]
    n = sum(d * 10 ** (6 - i) for i, d in enumerate(digs))
    x = F(n) + (F(r.randint(101, 999), 1000) if L else 0)
    p = pick(r, [q for q in places if (x // q) % 10 not in (0,) and q != 1])
    d = int((x // p) % 10)
    need(sum(1 for q in places if int((x // q) % 10) == d) == 1)
    v = d * p
    big = p * 10 if p * 10 <= 10 ** 6 else p / 100
    return Q(f"What is the value of the digit {d} in {dtext(x)}?", dtext(v),
             [f"The {d} is in the {PLACE[p]} place.", f"Value = {d} × {dtext(p)} = {dtext(v)}."],
             [str(d), dtext(d * big), dtext(d * p / 10), dtext(d * p * 100)],
             V(f"{d}*{p}"), why=["Gave the digit instead of its value", "Counted the place one position too far left", "Counted the place one position too far right", ""])


@fam("012")
def s1_expanded(r, L):
    k = r.randint(4, 6) if L < 2 else r.randint(4, 7)
    digs = [r.randint(1, 9)] + [pick(r, [0, 0] + list(range(1, 10))) for _ in range(k - 1)]
    dp = r.randint(1, 2) if L else 0
    vals = [(d, 10 ** (k - 1 - i - dp) if k - 1 - i - dp >= 0 else F(1, 10 ** (dp - (k - 1 - i)))) for i, d in enumerate(digs)]
    terms = [(d, p) for d, p in vals if d]
    need(len(terms) >= 3 and digs[-1] != 0)
    x = sum(d * p for d, p in terms)
    if L == 2:
        def pw10(p):
            e = int(round(math.log10(float(p))))
            return f"10{sup(e)}" if e != 0 else "1"
        txt = " + ".join(f"({d} × {pw10(p)})" for d, p in terms)
    else:
        txt = " + ".join(f"({d} × {dtext(p)})" for d, p in terms)
    smash = "".join(str(d) for d, p in terms)
    alt = sum(d * p * 10 for d, p in terms)
    return Q(f"Write the number in standard form: {txt}", dtext(x),
             ["Find the value of each product.", " + ".join(dtext(d * p) for d, p in terms) + ".", f"Add the place values: {dtext(x)}."],
             [smash, dtext(alt), dtext(x / 10), dtext(sum(d * p for d, p in terms[:-1]))],
             V(txt.replace("10" + "", "10")), why=["Wrote the digits next to each other and ignored the zero placeholders", "Shifted every digit one place to the left", "Shifted every digit one place to the right", "Left out the last term"],
             tags=["multiple-representations"])


@fam("012")
def s1_words(r, L):
    n = r.randint(1000, 999999) if L < 2 else r.randint(1_000_000, 9_999_999)
    need(n % 10 != 0)
    w = words(n)
    if L:
        dd = r.randint(1, 99)
        x = F(n) + F(dd, 100)
        w += f" and {words(dd)} hundredth{'s' if dd > 1 else ''}"
    else:
        x = F(n)
    wrong = [dtext(x * 10), dtext(x / 10), comma(n) + (f".{r.randint(1, 9)}" if L else "0")]
    if L:
        wrong.append(f"{comma(n)}.{dd}" if dd < 10 else comma(n * 100 + dd))
    return Q(f"Write in standard form: {w}.", dtext(x), ["Write each period (millions, thousands, ones) in order.", "Use zeros as placeholders.", f"{dtext(x)}."],
             wrong, V(str(x.numerator) + "/" + str(x.denominator)), why=["Added an extra zero", "Left out a zero placeholder", "", "Placed the hundredths in the tenths place"],
             tags=["multiple-representations"])


@fam("12")
def s1_order(r, L):
    base = r.randint(1, 9)
    nums = sorted({F(base * 100 + r.randint(0, 99), 100), F(base * 1000 + r.randint(0, 999), 1000), F(base, 10), F(base * 100 + r.randint(1, 9) * 10, 1000)} |
                  ({F(-base * 10 - r.randint(1, 9), 100)} if L == 2 else set()))
    need(len(nums) >= 4)
    items = [D(x) for x in nums]
    shown = items[:]
    r.shuffle(shown)
    need(shown != items)
    bylen = sorted(items, key=lambda s: (len(s), s))
    return Q(f"Order from least to greatest: {', '.join(shown)}", ", ".join(items),
             ["Line up the decimal points and compare place by place.", "Write zeros so every number has the same number of decimal places.", f"Least to greatest: {', '.join(items)}."],
             [", ".join(bylen), ", ".join(items[::-1]), ", ".join(sorted(items))],
             PY("order", items=items), why=["Ordered by the number of digits instead of by value", "Ordered from greatest to least", "Compared the numbers like words, digit by digit, ignoring negatives"],
             tags=["misconception"])


@fam("012")
def s1_times(r, L):
    d = r.randint(1, 9)
    e1 = r.randint(1, 4)
    gap = 1 if L == 0 else r.randint(1, 3)
    a, b = F(d) * F(10) ** (e1 - 2), F(d) * F(10) ** (e1 - 2 - gap)
    other = [k for k in range(1, 10) if k != d]
    n1 = F(pick(r, other)) * F(10) ** (e1 - 1) + a
    n2 = F(pick(r, other)) * F(10) ** (e1 - 2 - gap + 1) + b
    need(n1.denominator <= 1000 and n2.denominator <= 1000)
    need(sum(1 for c in D(n1) if c == str(d)) == 1 and sum(1 for c in D(n2) if c == str(d)) == 1)
    ratio = 10 ** gap
    return Q(f"The digit {d} appears in {D(n1)} and in {D(n2)}. The value of the {d} in {D(n1)} is how many times the value of the {d} in {D(n2)}?", comma(ratio),
             [f"In {D(n1)}, the {d} is worth {D(a)}.", f"In {D(n2)}, the {d} is worth {D(b)}.", f"{D(a)} ÷ {D(b)} = {ratio}.", "Each place is 10 times the place to its right."],
             [str(gap), comma(ratio * 10), comma(ratio // 10) if ratio > 10 else "100", "1"], V(f"{a.numerator}/{a.denominator} DIV {b.numerator}/{b.denominator}".replace("DIV", "÷")),
             why=["Counted the places instead of multiplying by 10 for each place", "Counted one place too many", "", "Thought the same digit always has the same value"],
             tags=["reasoning"])


# ============================================================== S2 Variables and Expressions
PHR = [  # (phrase template, expression template, wrong templates with reasons), {n}=variable, {a},{b}
    ("{a} more than a number {v}", "{v} + {a}", [("{a}{v}", "Multiplied instead of adding"), ("{v} - {a}", "Subtracted instead of adding"), ("{a} - {v}", "")]),
    ("{a} less than a number {v}", "{v} - {a}", [("{a} - {v}", "Reversed the order: “less than” means subtract from the number"), ("{v} + {a}", "Added instead of subtracting"), ("{a}{v}", "")]),
    ("the product of {a} and a number {v}", "{a}{v}", [("{a} + {v}", "Added instead of multiplying"), ("{v} - {a}", ""), ("{v}/{a}", "Divided instead of multiplying")]),
    ("the quotient of a number {v} and {a}", "{v}/{a}", [("{a}/{v}", "Reversed the order of division"), ("{a}{v}", "Multiplied instead of dividing"), ("{v} - {a}", "")]),
    ("a number {v} decreased by {a}", "{v} - {a}", [("{a} - {v}", "Reversed the order of subtraction"), ("{v} + {a}", ""), ("{v}/{a}", "")]),
]
PHR2 = [
    ("{b} more than {a} times a number {v}", "{a}{v} + {b}", [("{a}({v} + {b})", "Added before multiplying"), ("{b}{v} + {a}", "Switched the numbers"), ("{a} + {v} + {b}", "")]),
    ("{b} less than {a} times a number {v}", "{a}{v} - {b}", [("{b} - {a}{v}", "Reversed the subtraction"), ("{a}({v} - {b})", "Subtracted before multiplying"), ("{a}{v} + {b}", "")]),
    ("{a} times the sum of a number {v} and {b}", "{a}({v} + {b})", [("{a}{v} + {b}", "Left out the parentheses, so only the number is multiplied"), ("{a} + {v} + {b}", ""), ("{v} + {a}{b}", "")]),
    ("the quotient of a number {v} and {a}, increased by {b}", "{v}/{a} + {b}", [("({v} + {b})/{a}", "Added before dividing"), ("{a}/{v} + {b}", "Reversed the division"), ("{a}{v} + {b}", "")]),
    ("{b} decreased by twice a number {v}", "{b} - 2{v}", [("2{v} - {b}", "Reversed the subtraction"), ("{b} - {v}²", "Read “twice” as squared"), ("2({b} - {v})", "")]),
]


@fam("012")
def s2_translate(r, L):
    v = pick(r, ["n", "x", "y", "m", "k"])
    a, b = r.randint(2, 12), r.randint(2, 15)
    need(a != b)
    lst = PHR if L == 0 else PHR + PHR2 if L == 1 else PHR2
    ph, ex, wr = pick(r, lst)
    f = lambda s: s.format(a=a, b=b, v=v)
    return Q(f"Write an algebraic expression for the phrase: “{f(ph)}.”", f(ex),
             ["Identify the operation for each key word.", "Keep the order the phrase gives for subtraction and division.", f"Expression: {f(ex)}."],
             [f(w) for w, _ in wr], EQV(f(ex), [v]), why=[y for _, y in wr], tags=["multiple-representations"])


@fam("012", mode="mc")
def s2_to_words(r, L):
    v = pick(r, ["n", "x", "y"])
    a, b = r.randint(2, 12), r.randint(2, 15)
    need(a != b)
    lst = PHR if L == 0 else PHR2
    i = r.randrange(len(lst))
    ph, ex, _ = lst[i]
    f = lambda s: s.format(a=a, b=b, v=v)
    others = [lst[j] for j in range(len(lst)) if j != i]
    r.shuffle(others)
    opts = [(f(ph), True)] + [(f(o[0]), False) for o in others[:3]]
    r.shuffle(opts)
    need(len({o[0] for o in opts}) == 4)
    return Q(f"Which phrase matches the expression {f(ex)}?", f(ph), [f"{f(ex)} means: {f(ph)}."], options=opts,
             chk=PY("claims", table={f(o[0]): EQV(f(ex), [v]) for o in [lst[i]] + others[:3]}) if False else TXT(f(ph)), tags=["multiple-representations"], mode="mc")


@fam("012")
def s2_parts(r, L):
    v = pick(r, ["x", "y", "a", "t"])
    c, k = r.randint(2, 15), r.randint(2, 20)
    w = pick(r, ["coefficient", "constant"]) if L < 2 else pick(r, ["coefficient", "constant", "number of terms"])
    if L == 2 and w == "number of terms":
        c2 = r.randint(2, 9)
        e = f"{c}{v}² - {c2}{v} + {k}"
        return Q(f"How many terms are in the expression {e}?", "3", ["Terms are separated by + and - signs.", f"The terms are {c}{v}², -{c2}{v}, and {k}.", "There are 3 terms."],
                 ["2", "4", "5"], V("3"), why=["Counted only the variable terms", "Counted the subtraction sign as a term", ""])
    e = f"{c}{v} + {k}" if L == 0 else f"{k} + {c}{v}" if L == 1 else f"{k} - {c}{v}"
    if w == "coefficient":
        ans = str(-c if L == 2 else c)
        return Q(f"What is the coefficient of {v} in {e}?", ans, ["The coefficient is the number multiplying the variable.", f"The coefficient of {v} is {ans}" + (" (the subtraction sign belongs to the term)." if L == 2 else ".")],
                 [str(k), str(c) if L == 2 else str(-c), v, str(c + k)], V(ans), why=["Gave the constant term", "Ignored the sign in front of the term" if L == 2 else "", "", ""])
    return Q(f"What is the constant term in {e}?", str(k), ["The constant is the term with no variable.", f"The constant is {k}."],
             [str(c), f"{c}{v}", str(c + k)], V(str(k)), why=["Gave the coefficient", "", ""])


@fam("012")
def s2_context(r, L):
    v = pick(r, ["t", "h", "p", "w"])
    a, b = r.randint(3, 15), r.randint(5, 40)
    ctx = [(f"Movie tickets cost ${a} each. Write an expression for the cost, in dollars, of {v} tickets.", f"{a}{v}", [f"{v} + {a}", f"{v}/{a}", f"{a} - {v}"]),
           (f"Mia is {a} years older than her brother, who is {v} years old. Write an expression for Mia's age.", f"{v} + {a}", [f"{a}{v}", f"{v} - {a}", f"{a} - {v}"]),
           (f"{b} stickers are shared equally among {v} students. Write an expression for each student's share.", f"{b}/{v}", [f"{v}/{b}", f"{b}{v}", f"{b} - {v}"])]
    if L:
        ctx += [(f"A plumber charges ${b} to visit plus ${a} per hour. Write an expression for the cost of a {v}-hour job.", f"{a}{v} + {b}", [f"{b}{v} + {a}", f"{a + b}{v}", f"{a}({v} + {b})"]),
                (f"A phone plan costs ${b} per month plus ${a} for each gigabyte over the limit. Write an expression for a month with {v} extra gigabytes.", f"{b} + {a}{v}", [f"{a} + {b}{v}", f"{a + b}{v}", f"{b}{v}"])]
    if L == 2:
        ctx += [(f"A rectangle is {v} cm long and {a} cm wide. Write an expression for its perimeter.", f"2{v} + {2 * a}", [f"{a}{v}", f"{v} + {a}", f"2{v} + {a}"]),
                (f"Sam had ${b + 50}. He bought {v} books at ${a} each. Write an expression for the money he has left.", f"{b + 50} - {a}{v}", [f"{a}{v} - {b + 50}", f"({b + 50} - {a}){v}", f"{b + 50} - {v}"])]
    t, ans, wr = pick(r, ctx)
    return Q(t, ans, ["Decide what changes (the variable) and what stays the same.", "Translate the situation into operations.", f"Expression: {ans}."], wr,
             EQV(ans, [v]), why=["Reversed the quantities", "Used the wrong operation", "Applied the rate to the wrong quantity"], tags=["modeling"])


# ============================================================== S3 Order of Operations
def ev_lr(tokens):
    """Left-to-right evaluation ignoring precedence (misconception)."""
    v = F(tokens[0])
    for i in range(1, len(tokens), 2):
        op, b = tokens[i], F(tokens[i + 1])
        v = v + b if op == "+" else v - b if op == "-" else v * b if op == "×" else v / b
    return v


@fam("012")
def s3_eval(r, L):
    for _ in range(40):
        if L == 0:
            a, b, c = r.randint(2, 20), r.randint(2, 9), r.randint(2, 9)
            form = pick(r, ["a + b × c", "a - b × c", "a × b + c", "a + b ÷ c", "(a + b) × c"])
            if "÷" in form:
                b = b * c
            e = form.replace("a", str(a)).replace("b", str(b)).replace("c", str(c))
        elif L == 1:
            a, b, c, d = r.randint(2, 12), r.randint(2, 6), r.randint(2, 9), r.randint(1, 9)
            form = pick(r, ["a + b² × c", "(a - c) × b + d", "a × b - c² ÷ c", "a² - b × c + d", "[a + (b × c)] ÷ b"])
            e = form.replace("a", str(a)).replace("b", str(b)).replace("c", str(c)).replace("d", str(d))
        else:
            a, b, c, d = r.randint(2, 9), r.randint(2, 5), r.randint(2, 9), r.randint(2, 6)
            form = pick(r, ["a + 3[b² - (c - d)]", "(a + b)² ÷ (c - d) - b", "2[(a + c) × b - d²]", "a³ - [b × (c + d)] + 1"])
            e = form.replace("a", str(a)).replace("b", str(b)).replace("c", str(c)).replace("d", str(d))
        try:
            v = M_ev(e)
        except ZeroDivisionError:
            continue
        if F(v).denominator == 1 and -200 <= v <= 999:
            break
    else:
        raise Reject()
    toks = e.replace("(", "").replace(")", "").replace("[", "").replace("]", "")
    wr, why = [], []
    if "²" not in e and "³" not in e:
        tk = toks.split()
        try:
            w = ev_lr(tk)
            wr.append(N(w))
            why.append("Worked left to right without following the order of operations")
        except ZeroDivisionError:
            pass
    wr += [N(v + 2 * pick(r, [1, -1]) * r.randint(1, 4)), N(v * 2), N(abs(v) + 10)]
    why += ["Made an arithmetic error", "", ""]
    if "²" in e:
        try:
            w2 = M_ev(e.replace("²", "×2"))
            wr.insert(0, N(w2))
            why.insert(0, "Multiplied by 2 instead of squaring")
        except Exception:
            pass
    return Q(f"Evaluate: {e}", N(v), ["Grouping symbols first (innermost first).", "Then exponents.", "Then multiply and divide from left to right.", "Then add and subtract from left to right.", f"Result: {N(v)}."],
             wr, V(e.replace("[", "(").replace("]", ")")), why=why, tags=["misconception"])


def M_ev(e):
    import mathtext
    return mathtext.ev(e.replace("[", "(").replace("]", ")"))


@fam("12", mode="mc")
def s3_parens(r, L):
    a, b, c, d = r.randint(2, 9), r.randint(2, 9), r.randint(2, 6), r.randint(1, 9)
    plain = f"{a} + {b} × {c} - {d}"
    cands = [f"({a} + {b}) × {c} - {d}", f"{a} + {b} × ({c} - {d})", f"({a} + {b} × {c}) - {d}", f"{a} + ({b} × {c} - {d})"]
    vals = {x: M_ev(x) for x in cands}
    tgt = vals[cands[0]] if L == 1 else vals[cands[1]]
    need(len(set(vals.values())) == 4 and M_ev(plain) != tgt)
    opts = [(x, vals[x] == tgt) for x in cands]
    r.shuffle(opts)
    return Q(f"Where should parentheses go so that {plain} = {N(tgt)}?", [x for x, ok in opts if ok][0],
             ["Evaluate each choice using the order of operations.", f"Without parentheses the value is {N(M_ev(plain))}.", f"Only one placement gives {N(tgt)}."],
             options=opts, chk=V(N(tgt)), tags=["reasoning"], mode="mc")


@fam("012")
def s3_fraction_bar(r, L):
    b, c = r.randint(2, 9), r.randint(2, 9)
    k = r.randint(2, 6)
    num_v = k * (b + 1)
    a = num_v - b * c if L < 2 else num_v - c * c
    need(a > 0)
    num = f"{a} + {b} × {c}" if L < 2 else f"{a} + {c}²"
    den = f"{b + 1}"
    e = f"({num}) ÷ {den}"
    v = F(num_v, b + 1)
    wr = [N(F(a) + F(b * c, b + 1)) if L < 2 else N(F(a) + F(c * c, b + 1)), N((a + b) * c / F(b + 1)) if L < 2 else N(F(a + 2 * c, b + 1)), N(num_v), N(v + 1)]
    return Q(f"Evaluate: ({num}) ÷ {den}", N(v), ["The parentheses group the whole numerator.", f"Numerator: {num} = {num_v}.", f"Divide: {num_v} ÷ {den} = {N(v)}."],
             wr, V(e), why=["Divided only the last term by the divisor", "Added before multiplying" if L < 2 else "Multiplied by 2 instead of squaring", "Forgot to divide", ""])


@fam("012")
def s3_context(r, L):
    nm = name(r)
    a, b, c, d = r.randint(2, 6), r.randint(3, 12), r.randint(2, 5), r.randint(4, 15)
    e = f"{a} × {b} + {c} × {d}"
    v = a * b + c * d
    return Q(f"{nm} buys {a} notebooks at ${b} each and {c} packs of pens at ${d} each. Evaluate {e} to find the total cost in dollars.", str(v),
             [f"Multiply first: {a} × {b} = {a * b} and {c} × {d} = {c * d}.", f"Then add: {a * b} + {c * d} = {v}.", f"Total: ${v}."],
             [str((a * b + c) * d), str(a * (b + c) * d), str(a + b + c + d), str(a * b * c * d)], V(e),
             why=["Worked left to right instead of multiplying first", "Added before multiplying", "Added all the numbers", ""], tags=["modeling"])


# ============================================================== S4 Writing and Evaluating Expressions
@fam("012")
def s4_evaluate(r, L):
    x, y = r.randint(2, 9), r.randint(2, 9)
    forms = ["3x + 4", "5x - y", "x(y + 2)", "2x + 3y", "4(x - 1)"] if L == 0 else \
            ["x² + 2y", "3x² - y", "(x + y)²", "2x³ - 5", "xy - y²"] if L == 1 else \
            ["x²y - 3x", "(2x - y)² + x", "x³ - x² + y", "(x² + y²)/(x + y)", "3(x - y)² - 2x"]
    form = pick(r, forms)
    env = {"x": F(x), "y": F(y)}
    import mathtext
    try:
        v = mathtext.ev(form, env)
    except ZeroDivisionError:
        raise Reject()
    need(F(v).denominator == 1)
    sub = form.replace("x", f"({x})").replace("y", f"({y})")
    wr, why = [], []
    if "²" in form:
        wr.append(N(mathtext.ev(form.replace("²", "*2"), env)))
        why.append("Multiplied by 2 instead of squaring")
    wr += [N(mathtext.ev(form, {"x": F(y), "y": F(x)})) if "y" in form else N(v + x), N(v + 10), N(v - 1)]
    why += ["Substituted the values for the wrong variables" if "y" in form else "", "", ""]
    return Q(f"Evaluate {form} when x = {x}" + (f" and y = {y}." if "y" in form else "."), N(v), [f"Substitute: {sub}.", "Follow the order of operations.", f"Value: {N(v)}."],
             wr, V(sub), why=why)


@fam("012")
def s4_write_eval(r, L):
    v = r.randint(2, 12)
    rate, fee = r.randint(3, 25), r.randint(5, 60)
    nm = name(r)
    ctx = pick(r, [("hours", f"A bike rental costs ${fee} plus ${rate} per hour"), ("guests", f"A party costs ${fee} for the room plus ${rate} per guest"),
                   ("months", f"{nm} has ${fee} saved and adds ${rate} each month")])
    unit, lead = ctx
    if L == 0:
        p = f"{lead}. Write an expression for {v} {unit} and find the value."
        p = f"{lead}. What is the total for {v} {unit}?"
        val = fee + rate * v
        return Q(p, str(val), [f"Expression: {fee} + {rate} × {v}.", f"Multiply first: {rate} × {v} = {rate * v}.", f"Add: {fee} + {rate * v} = {val}."],
                 [str((fee + rate) * v), str(fee + rate + v), str(rate * v)], V(f"{fee} + {rate}*{v}"), why=["Added the fee and rate before multiplying", "Added all the numbers", "Forgot the starting amount"], tags=["modeling"])
    if L == 1:
        return Q(f"{lead}. Write an expression for the total after n {unit}.", f"{rate}n + {fee}", ["The amount that changes is multiplied by n.", "The starting amount is added.", f"Total: {rate}n + {fee}."],
                 [f"{fee}n + {rate}", f"{rate + fee}n", f"{rate}(n + {fee})"], EQV(f"{rate}n + {fee}", ["n"]), why=["Switched the starting amount and the rate", "Combined unlike quantities", "Multiplied the starting amount by n too"], tags=["modeling"])
    tot = fee + rate * v
    return Q(f"{lead}. The total is ${tot}. Use the expression {rate}n + {fee} to find n, the number of {unit}.", str(v),
             [f"{rate}n + {fee} = {tot}.", f"Subtract {fee}: {rate}n = {tot - fee}.", f"Divide by {rate}: n = {v}.", f"Check: {rate}({v}) + {fee} = {tot}."],
             [str(F(tot + fee, rate)) if (tot + fee) % rate == 0 else str(tot - fee), str(tot - fee), str(F(tot, rate)) if tot % rate == 0 else str(v + 1)],
             EQ(f"{rate}n + {fee} = {tot}", "n"), why=["Added the starting amount instead of subtracting", "Forgot to divide by the rate", "Divided before subtracting"], tags=["modeling", "multistep"])


@fam("12")
def s4_table(r, L):
    m, b = r.randint(2, 9), r.randint(1, 12)
    xs = sorted(r.sample(range(1, 9), 3))
    ys = [m * x + b for x in xs]
    q = r.randint(10, 20)
    return Q(f"In a table, x = {xs[0]}, {xs[1]}, {xs[2]} gives y = {ys[0]}, {ys[1]}, {ys[2]}. The rule is y = {m}x + {b}. What is y when x = {q}?", str(m * q + b),
             [f"Substitute x = {q}: {m}({q}) + {b}.", f"{m * q} + {b} = {m * q + b}."], [str(m * (q + b)), str(m + q + b), str(ys[-1] + (q - xs[-1]))],
             V(f"{m}*{q} + {b}"), why=["Added before multiplying", "Added all the numbers", "Added the change in x to the last y"], tags=["multiple-representations"])


# ============================================================== S5 Integers and Absolute Value
@fam("012")
def s5_abs(r, L):
    a, b = nz(r, -20, 20), nz(r, -20, 20)
    forms = [(f"|{a}|", abs(a)), (f"-|{a}|", -abs(a))] if L == 0 else [(f"|{a}| + |{b}|", abs(a) + abs(b)), (f"|{a}| - |{b}|", abs(a) - abs(b)), (f"-|{a}| + {b}", -abs(a) + b)] if L == 1 else \
        [(f"|{a} + {b}|", abs(a + b)), (f"|{a}| + |{b}| - |{a} + {b}|", abs(a) + abs(b) - abs(a + b)), (f"-|{a} - ({b})|", -abs(a - b))]
    e, v = pick(r, forms)
    ee = e.replace("|", "§")
    return Q(f"Evaluate: {e}", str(v), ["Absolute value is the distance from 0, so it is never negative.", "Evaluate inside the bars first.", f"Result: {v}."],
             [str(-v), str(v + 2 * abs(a) if v != -v else v + 1), str(a + b), str(abs(v) + 1)], PY("absval", expr=e),
             why=["Treated the sign incorrectly with absolute value", "", "Ignored the absolute value bars", ""])


@fam("012")
def s5_compare(r, L):
    a, b = nz(r, -15, 15), nz(r, -15, 15)
    need(a != b)
    if L == 0:
        sa, sb = str(a), str(b)
    elif L == 1:
        sa, sb = f"|{a}|", str(b)
    else:
        sa, sb = f"-|{a}|", f"|{b}|" if r.random() < 0.5 else str(-abs(b))
    import mathtext
    va = abs(a) if sa.startswith("|") else -abs(a) if sa.startswith("-|") else a
    vb = abs(b) if sb.startswith("|") else int(sb) if not sb.startswith("-|") else -abs(b)
    need(va != vb)
    ans = "<" if va < vb else ">"
    return Q(f"Compare using <, >, or =: {sa} ___ {sb}", ans, [f"{sa} = {va} and {sb} = {vb}.", "On a number line, the number farther right is greater.", f"So {sa} {ans} {sb}."],
             [">" if ans == "<" else "<", "="], PY("cmp_abs", a=sa, b=sb), why=["Compared the distances from zero instead of the values", ""], mode="sa")


@fam("012")
def s5_opposite(r, L):
    a = nz(r, -40, 40)
    if L == 0:
        return Q(f"What is the opposite of {a}?", str(-a), ["Opposites are the same distance from 0 on opposite sides.", f"The opposite of {a} is {-a}."],
                 [str(a), str(abs(a)) if a > 0 else str(-abs(a) - 1), "0"], V(f"-({a})"), why=["Gave the same number", "", ""])
    if L == 1:
        e = f"-(-{abs(a)})" if a > 0 else f"-({a})"
        return Q(f"Simplify: -(-({a}))", str(a), [f"The opposite of {a} is {-a}.", f"The opposite of that is {a}."], [str(-a), str(abs(a) + 1), "0"], V(f"-(-({a}))"),
                 why=["Took the opposite only once", "", ""])
    k = r.randint(2, 30)
    return Q(f"Two integers are opposites and are {2 * k} units apart on a number line. What is the greater integer?", str(k),
             ["Opposites are the same distance from 0.", f"Half of {2 * k} is {k}.", f"The integers are {k} and -{k}; the greater is {k}."], [str(2 * k), str(-k), str(k * k)],
             V(f"{2 * k}/2"), why=["Used the full distance instead of half", "Gave the lesser integer", ""], tags=["reasoning"])


@fam("012")
def s5_numline(r, L):
    lo = pick(r, [-10, -8, -6]) if L < 2 else pick(r, [-20, -16])
    step = 1 if L < 2 else 2
    hi = lo + (16 if L < 2 else 32)
    x = r.randrange(lo + step, hi, step)
    need(x != 0)
    lab = "P"
    alt = f"Number line from {lo} to {hi} with tick marks every {step}; only every {2 if step == 1 else 4}th unit is labelled. Point {lab} is marked at {x}."
    return Q(f"What integer is at point {lab} on the number line shown?", str(x), [f"Count the tick marks from a labelled number; each mark is {step}.", f"Point {lab} is at {x}."],
             [str(-x), str(x + step), str(x - step)], V(str(x)), why=["Read the number on the wrong side of zero", "Miscounted one tick mark", "Miscounted one tick mark"],
             diagram={"alt": alt, "draw": numline_draw(lo, hi, points=[(x, lab, True)], step=step, label_every=2)}, tags=["graph"])


@fam("12")
def s5_context(r, L):
    ctx = pick(r, [("a diver is {a} feet below sea level", -1), ("the temperature is {a} degrees below zero", -1), ("a gain of {a} yards", 1), ("a withdrawal of ${a}", -1), ("{a} meters above sea level", 1)])
    a = r.randint(3, 120)
    t, s = ctx
    v = s * a
    return Q(f"Write an integer to represent {t.format(a=a)}.", str(v), ["Below, loss, withdrawal → negative.", "Above, gain, deposit → positive.", f"The integer is {v}."],
             [str(-v), "0", str(abs(v) * 10)], V(str(v)), why=["Used the wrong sign", "", ""], tags=["modeling"])


@fam("2")
def s5_solve_abs(r, L):
    k = r.randint(1, 30)
    return Q(f"Find all integers x such that |x| = {k}. List them separated by commas.", f"{-k}, {k}", ["Two numbers are " + str(k) + " units from 0.", f"x = {-k} or x = {k}."],
             [str(k), str(-k), f"0, {k}"], PY("set_eq", items=[str(k), str(-k)]), why=["Forgot the negative solution", "Forgot the positive solution", ""], tags=["reasoning"], mode="sa")


# ============================================================== S6 / S7 / S11 integer operations
def int_terms(r, k, lo=-20, hi=20):
    return [nz(r, lo, hi) for _ in range(k)]


def chain(ts, op="+"):
    s = str(ts[0])
    for t in ts[1:]:
        s += f" {op} {par(t)}"
    return s


@fam("012")
def s6_sum(r, L):
    k = 2 if L == 0 else 3 if L == 1 else 4
    ts = int_terms(r, k, -30 if L else -12, 30 if L else 12)
    need(any(t < 0 for t in ts) and any(t > 0 for t in ts) or L == 0)
    e = chain(ts)
    v = sum(ts)
    wr = [str(sum(abs(t) for t in ts)), str(-v), str(sum(abs(t) for t in ts) * (-1 if v > 0 else 1)), str(v + 2)]
    return Q(f"Find the sum: {e}", str(v), ["Add the positive numbers and add the negative numbers.", f"Positives: {sum(t for t in ts if t > 0)}; negatives: {sum(t for t in ts if t < 0)}.",
                                             "Subtract the absolute values and keep the sign of the larger absolute value.", f"Sum: {v}."],
             wr, V(e), why=["Ignored the negative signs and added absolute values", "Gave the answer the wrong sign", "", "Made an arithmetic error"])


@fam("012")
def s6_context(r, L):
    nm = name(r)
    a, b, c = r.randint(2, 15), r.randint(3, 20), r.randint(2, 15)
    ctx = [(f"The temperature was {-a}°F at dawn and rose {b}°F by noon. What was the noon temperature?", -a + b, f"{-a} + {b}"),
           (f"An elevator starts on floor {a + 10}, goes down {b} floors, then up {c} floors. On which floor does it stop?", a + 10 - b + c, f"{a + 10} + ({-b}) + {c}"),
           (f"A football team gains {a} yards, loses {b} yards, then loses {c} more yards. What is the total change in yards?", a - b - c, f"{a} + ({-b}) + ({-c})")]
    if L == 2:
        ctx.append((f"{nm}'s account balance is ${-a * 5}. {nm} deposits ${b * 4} and then is charged a ${c} fee. What is the new balance in dollars?", -a * 5 + b * 4 - c, f"{-a * 5} + {b * 4} + ({-c})"))
    t, v, e = pick(r, ctx if L else ctx[:2])
    return Q(t, str(v), ["Write the changes as integers (up, gain, or deposit is positive; down, loss, or fee is negative).", f"Add: {e}.", f"Result: {v}."],
             [str(-v), str(abs(-a) + b + (c if L else 0)), str(v + c)], V(e), why=["Gave the answer the wrong sign", "Treated every change as positive", ""], tags=["modeling"])


@fam("12")
def s6_missing(r, L):
    a, s = nz(r, -25, 25), nz(r, -25, 25)
    x = s - a
    need(x != 0)
    return Q(f"What integer makes the equation true? {a} + n = {s}", f"n = {x}", [f"n = {s} - ({a}).", f"n = {x}.", f"Check: {a} + {par(x)} = {s}."],
             [f"n = {s + a}", f"n = {-x}", f"n = {abs(s) + abs(a)}"], EQ(f"{a} + n = {s}", "n"), why=["Added instead of subtracting", "Gave the answer the wrong sign", ""])


@fam("012")
def s7_diff(r, L):
    a, b = (nz(r, -15, 15), nz(r, -15, 15)) if L == 0 else (nz(r, -40, 40), nz(r, -40, 40))
    need(b < 0 or L == 0)
    if L == 2:
        c = nz(r, -20, 20)
        e = f"{a} - {par(b)} - {par(c)}"
        v = a - b - c
        wr = [str(a + b + c), str(a - abs(b) - abs(c)), str(-v)]
        why = ["Did not change the subtractions to adding the opposite", "Ignored the signs of the numbers", "Gave the answer the wrong sign"]
    else:
        e = f"{a} - {par(b)}"
        v = a - b
        wr = [str(a + b), str(-v), str(abs(a) - abs(b)) if abs(a) - abs(b) != v else str(v + 1)]
        why = ["Subtracted without adding the opposite", "Gave the answer the wrong sign", "Subtracted the absolute values"]
    return Q(f"Find the difference: {e}", str(v), ["To subtract an integer, add its opposite.", f"Rewrite: {e.replace('- (', '+ (-(')}" if False else "Rewrite each subtraction as adding the opposite.",
                                                   f"Add: {v}."], wr, V(e), why=why)


@fam("012")
def s7_context(r, L):
    a, b = r.randint(2, 30), r.randint(2, 40)
    ctx = [(f"The high temperature was {a}°F and the low was {-b}°F. How many degrees warmer was the high than the low?", a + b, f"{a} - ({-b})"),
           (f"A plane flies at {a * 100} feet. A submarine is at {-b * 10} feet. What is the vertical distance between them in feet?", a * 100 + b * 10, f"{a * 100} - ({-b * 10})"),
           (f"Death Valley is {-b} meters relative to sea level and a nearby peak is {a * 100} meters. How much higher is the peak in meters?", a * 100 + b, f"{a * 100} - ({-b})")]
    t, v, e = pick(r, ctx)
    return Q(t, str(v), ["Find the difference: higher value minus lower value.", f"{e} = {v}.", f"The difference is {v}."],
             [str(v - 2 * b if "°" in t else abs(a * 100 - b * 10) if "plane" in t else a * 100 - b), str(-v), str(v + 10)], V(e),
             why=["Subtracted the absolute values instead of finding the distance", "Gave a negative distance", ""], tags=["modeling"])


@fam("12")
def s7_distance(r, L):
    a, b = nz(r, -30, 30), nz(r, -30, 30)
    need(a * b < 0 or L == 2)
    v = abs(a - b)
    return Q(f"What is the distance between {a} and {b} on a number line?", str(v), [f"Distance = |{a} - ({b})|.", f"= |{a - b}| = {v}."],
             [str(abs(abs(a) - abs(b))), str(a - b if a - b != v else b - a), str(v + 1)], PY("absval", expr=f"|{a} - ({b})|"),
             why=["Subtracted the absolute values", "Gave a negative distance", ""], tags=["connections"])


@fam("012")
def s11_prod(r, L):
    if L == 0:
        a, b = nz(r, -12, 12), nz(r, -12, 12)
        need(a < 0 or b < 0)
        e, v = f"{par(a)} × {par(b)}" if r.random() < 0.5 else f"{a * b} ÷ {par(b)}", None
        v = a * b if "×" in e else a
    elif L == 1:
        a, b, c = nz(r, -9, 9), nz(r, -9, 9), nz(r, -6, 6)
        e = f"{par(a)} × {par(b)} × {par(c)}" if r.random() < 0.5 else f"{a * b * c} ÷ {par(b)} ÷ {par(c)}"
        v = a * b * c if "×" in e else a
    else:
        a, b, c = nz(r, -6, 6), nz(r, -8, 8), r.randint(2, 4)
        e = pick(r, [f"(-{abs(a)})^{c}", f"-{abs(a)}^{c}", f"{par(a)} × {par(b)} ÷ {par(-b)}", f"[{par(a * b)} ÷ {par(a)}] × (-1)^{c + 1}"])
        e = re.sub(r"\^(\d)", lambda m: sup(int(m.group(1))), e)
        v = M_ev(e)
    v = M_ev(e)
    wr = [str(-v), str(abs(v) + 1 if v != abs(v) + 1 else v + 2), str(v * 2)]
    return Q(f"Evaluate: {e}", N(v), ["Multiply or divide the absolute values.", "Same signs → positive; different signs → negative. An even number of negative factors is positive.",
                                     f"Result: {N(v)}."], wr, V(e.replace("[", "(").replace("]", ")")), why=["Used the wrong sign rule", "", ""])


@fam("012")
def s11_context(r, L):
    a, n = r.randint(2, 9), r.randint(3, 8)
    ctx = [(f"The temperature dropped {a}°F each hour for {n} hours. What was the total change in temperature?", -a * n, f"{n} × ({-a})"),
           (f"A stock lost ${a} per day for {n} days. What was the total change in value, in dollars?", -a * n, f"{n} × ({-a})"),
           (f"A diver descended {a * n} feet in {n} equal stages. What was the change in depth per stage, in feet?", -a, f"{-a * n} ÷ {n}")]
    if L == 2:
        vals = [nz(r, -12, 6) for _ in range(5)]
        s = sum(vals)
        need(s % 5 == 0)
        ctx = [(f"The low temperatures on five days were {', '.join(map(str, vals))} °C. What was the mean low temperature?", s // 5, f"({' + '.join(par(v) for v in vals)}) ÷ 5")]
    t, v, e = pick(r, ctx)
    return Q(t, str(v), ["Write the situation as a product or quotient of integers.", f"{e}.", f"Result: {v}."], [str(-v), str(v * 2), str(v + a)], V(e),
             why=["Used the wrong sign for a loss or drop", "", ""], tags=["modeling"])


@fam("12")
def s11_missing(r, L):
    a, x = nz(r, -12, 12), nz(r, -12, 12)
    p = a * x
    if r.random() < 0.5:
        return Q(f"What integer n makes the equation true? {a}n = {p}", f"n = {x}", [f"n = {p} ÷ ({a}).", f"n = {x}."], [f"n = {-x}", f"n = {p - a}", f"n = {p * a}"],
                 EQ(f"{a}n = {p}", "n"), why=["Used the wrong sign rule", "Subtracted instead of dividing", "Multiplied instead of dividing"])
    return Q(f"What integer n makes the equation true? n ÷ {par(a)} = {x}", f"n = {p}", [f"n = {x} × ({a}).", f"n = {p}."], [f"n = {-p}", f"n = {x + a}", f"n = {N(F(x, a))}"],
             EQ(f"n/({a}) = {x}", "n"), why=["Used the wrong sign rule", "Added instead of multiplying", "Divided instead of multiplying"])


# ============================================================== S8 Rounding and Estimating
@fam("012")
def s8_round(r, L):
    if L == 0:
        x = r.randint(1000, 99999)
        place = pick(r, [10, 100, 1000])
    else:
        x = F(r.randint(10000, 999999), 1000)
        place = pick(r, [1, F(1, 10), F(1, 100)] + ([10] if L == 2 else []))
    q = math.floor(x / place + F(1, 2)) * place
    tr = math.floor(x / place) * place
    nm = {10: "ten", 100: "hundred", 1000: "thousand", 1: "whole number", F(1, 10): "tenth", F(1, 100): "hundredth"}[place]
    need(q != tr or r.random() < 0.3)
    ans = D(q) if place < 1 else str(int(q))
    if place < 1:
        ans = Rd(q, {F(1, 10): 1, F(1, 100): 2}[place])
    wr = [D(tr) if tr != q else D(q + place), D(q + place) if place >= 1 else Rd(q + place, {F(1, 10): 1, F(1, 100): 2}[place]), D(x).split(".")[0] if place < 1 else str(x // 10)]
    return Q(f"Round {dtext(x) if L == 0 else D(x)} to the nearest {nm}.", ans if place < 1 else comma(int(q)) if L == 0 else ans,
             ["Find the digit in the rounding place.", "Look at the digit to its right: 5 or more rounds up; less than 5 stays.", f"Rounded: {ans}."],
             wr, PY("round_place", expr=str(x.numerator if isinstance(x, F) else x) + ("/" + str(x.denominator) if isinstance(x, F) else ""), place=str(place)),
             why=["Truncated instead of rounding" if tr != q else "", "Rounded the wrong direction", "Rounded to the wrong place"])


@fam("012")
def s8_estimate(r, L):
    place = 10 if L == 0 else pick(r, [100, 1000])
    k = 2 if L < 2 else 3
    ts = [r.randint(place + 1, place * 10 - 1) for _ in range(k)]
    need(all(t % place for t in ts))
    op = pick(r, ["+", "-"]) if L < 2 else "+"
    if op == "-":
        ts.sort(reverse=True)
    rs = [math.floor(F(t, place) + F(1, 2)) * place for t in ts]
    est = rs[0] + sum(rs[1:]) if op == "+" else rs[0] - rs[1]
    exact = ts[0] + sum(ts[1:]) if op == "+" else ts[0] - ts[1]
    need(est != exact)
    e = f" {op} ".join(comma(t) for t in ts)
    nm = {10: "ten", 100: "hundred", 1000: "thousand"}[place]
    tr = [t // place * place for t in ts]
    trv = tr[0] + sum(tr[1:]) if op == "+" else tr[0] - tr[1]
    return Q(f"Estimate {e} by first rounding each number to the nearest {nm}.", comma(est),
             [f"Round each number: {', '.join(comma(x) for x in rs)}.", f"Compute with the rounded numbers: {comma(est)}.", f"(The exact value {comma(exact)} is close to the estimate.)"],
             [comma(exact), comma(trv) if trv != est else comma(est + place), comma(est + 2 * place)], PY("est", terms=[str(t) for t in ts], place=place, op=op),
             why=["Found the exact answer instead of rounding first", "Truncated instead of rounding", ""])


@fam("12", mode="mc")
def s8_reasonable(r, L):
    price = [F(r.randint(101, 999), 100) for _ in range(3)]
    budget = math.ceil(sum(price)) + pick(r, [-1, 1])
    need(budget != sum(price))
    enough = sum(price) <= budget
    ans = "Yes" if enough else "No"
    opts = [("Yes", enough), ("No", not enough)]
    ps = ", ".join("$" + Rd(p, 2) for p in price)
    return Q(f"Items cost {ps}. Is ${budget} enough to buy all three?", ans, ["Estimate by rounding each price up to the next dollar for a safe overestimate.", f"Exact total: ${Rd(sum(price), 2)}.",
                                                                           f"${budget} is {'enough' if enough else 'not enough'}."],
             options=opts + [("Cannot be determined", False), ("Only if tax is 0", False)], chk=PY("budget", prices=[str(p) for p in price], budget=budget), mode="mc", tags=["reasoning", "modeling"])


# ============================================================== S9 Inductive Reasoning / S10 Patterns
def seq_family(r, L):
    a = r.randint(-10, 20)
    if L == 0:
        d = nz(r, -8, 9)
        return [a + d * i for i in range(5)], "arith", d
    if L == 1:
        kind = pick(r, ["arith", "geom", "squares"])
        if kind == "arith":
            d = nz(r, -12, 12)
            return [a + d * i for i in range(5)], kind, d
        if kind == "geom":
            q = pick(r, [2, 3, -2])
            a = nz(r, 1, 6)
            return [a * q ** i for i in range(5)], kind, q
        s = r.randint(0, 4)
        return [(i + s) ** 2 for i in range(1, 6)], kind, s
    kind = pick(r, ["quad", "fib", "alt", "geomfrac"])
    if kind == "quad":
        d0, dd = r.randint(1, 5), r.randint(1, 3)
        out = [a]
        for i in range(4):
            out.append(out[-1] + d0 + dd * i)
        return out, kind, dd
    if kind == "fib":
        x, y = r.randint(1, 5), r.randint(1, 7)
        out = [x, y]
        while len(out) < 6:
            out.append(out[-1] + out[-2])
        return out, kind, 0
    if kind == "alt":
        p, m = r.randint(3, 9), r.randint(1, 5)
        need(p != m)
        out = [a]
        for i in range(5):
            out.append(out[-1] + (p if i % 2 == 0 else -m))
        return out, kind, 0
    a = pick(r, [96, 160, 243, 256, 324, 625])
    q = {96: 2, 160: 2, 243: 3, 256: 4, 324: 3, 625: 5}[a]
    return [F(a, q ** i) for i in range(5)], kind, q


@fam("012")
def s9_next(r, L):
    seq, kind, k = seq_family(r, L)
    from gchecks import _rules
    rs = {v for _, v in _rules(seq)}
    need(len(rs) == 1)
    nxt = rs.pop()
    d = seq[-1] - seq[-2]
    wr = [N(seq[-1] + d) if seq[-1] + d != nxt else N(nxt + 1), N(nxt + (seq[1] - seq[0])), N(-nxt) if nxt else "1", N(seq[-1] * 2)]
    desc = {"arith": f"add {N(seq[1] - seq[0])} each time", "geom": f"multiply by {N(F(seq[1], seq[0]))} each time", "squares": "the terms are consecutive perfect squares",
            "quad": "the differences increase by the same amount each time", "fib": "each term is the sum of the two terms before it",
            "alt": "the pattern alternates between adding and subtracting", "geomfrac": f"divide by {k} each time"}[kind]
    return Q(f"Use inductive reasoning to find the next term: {', '.join(N(x) for x in seq)}, …", N(nxt),
             ["Look at how each term changes from the one before.", f"Pattern: {desc}.", f"Next term: {N(nxt)}."], wr,
             PY("next_term", seq=[N(x) for x in seq]), why=["Repeated the last difference instead of continuing the pattern", "", "Used the wrong sign", "Doubled the last term without checking the pattern"],
             tags=["reasoning"])


@fam("012", mode="mc")
def s9_counter(r, L):
    claims = [("The sum of two integers is always greater than either integer.", lambda a, b: a + b > a and a + b > b, (-9, 9)),
              ("The product of two integers is always greater than either integer.", lambda a, b: a * b > a and a * b > b, (-9, 9)),
              ("The difference of two integers is always less than the first integer.", lambda a, b: a - b < a, (-9, 9)),
              ("The square of an integer is always greater than the integer.", lambda a, b: a * a > a, (-3, 9))]
    c, fn, rg = pick(r, claims)
    pairs = [(nz(r, *rg), nz(r, *rg)) for _ in range(40)]
    bad = [p for p in pairs if not fn(*p)]
    good = [p for p in pairs if fn(*p)]
    need(bad and len({p for p in good}) >= 3)
    one = "square" in c
    fmt = (lambda p: f"{p[0]}") if one else (lambda p: f"{p[0]} and {p[1]}")
    ce = r.choice(bad)
    gs = []
    for g in good:
        if fmt(g) not in [fmt(x) for x in gs] and fmt(g) != fmt(ce):
            gs.append(g)
    need(len(gs) >= 3)
    opts = [(fmt(ce), True)] + [(fmt(g), False) for g in gs[:3]]
    r.shuffle(opts)
    return Q(f"Conjecture: “{c}” Which choice is a counterexample?", fmt(ce), ["A counterexample makes the conjecture false.", f"Test {fmt(ce)}: the statement fails.", "So the conjecture is not always true."],
             options=opts, chk=PY("counter", claim=c), tags=["reasoning"], mode="mc")


@fam("12")
def s9_conjecture(r, L):
    n = r.randint(4, 9)
    kind = pick(r, ["odd", "even", "squares"])
    if kind == "odd":
        return Q(f"1 = 1, 1 + 3 = 4, 1 + 3 + 5 = 9, 1 + 3 + 5 + 7 = 16. Use the pattern to find the sum of the first {n} odd numbers.", str(n * n),
                 ["The sums are 1², 2², 3², 4².", "Conjecture: the sum of the first n odd numbers is n².", f"{n}² = {n * n}."], [str(2 * n - 1), str(n * (n + 1)), str(2 * n)],
                 V(" + ".join(str(2 * i + 1) for i in range(n))), why=["Gave the last odd number instead of the sum", "", ""], tags=["reasoning"])
    if kind == "even":
        return Q(f"2 = 1 × 2, 2 + 4 = 2 × 3, 2 + 4 + 6 = 3 × 4. Use the pattern to find the sum of the first {n} even numbers.", str(n * (n + 1)),
                 ["The sums are 1×2, 2×3, 3×4.", "Conjecture: the sum of the first n even numbers is n(n + 1).", f"{n} × {n + 1} = {n * (n + 1)}."], [str(n * n), str(2 * n), str((n + 1) * (n + 2))],
                 V(" + ".join(str(2 * i + 2) for i in range(n))), why=["Squared the count instead", "Gave the last even number", "Used the next pattern line"], tags=["reasoning"])
    return Q(f"11 × 11 = 121, 111 × 111 = 12,321, 1,111 × 1,111 = 1,234,321. Predict 11,111 × 11,111.", "123,454,321", ["Each product counts up to the number of ones, then back down.", "Five ones → 123454321."],
             ["12,345,321", "1,234,554,321", "123,456,321"], V("11111*11111"), why=["Stopped one step too early", "", ""], tags=["reasoning"])


@fam("012")
def s10_figure(r, L):
    m, b = r.randint(2, 6), r.randint(1, 6)
    seq = [m * n + b for n in (1, 2, 3)]
    n = r.randint(6, 12) if L == 0 else r.randint(15, 40)
    thing = pick(r, ["toothpicks", "tiles", "dots", "squares"])
    if L == 2 and r.random() < 0.5:
        return Q(f"Figure 1 uses {seq[0]} {thing}, Figure 2 uses {seq[1]}, and Figure 3 uses {seq[2]}. Write an expression for the number of {thing} in Figure n.", f"{m}n + {b}",
                 [f"Each figure adds {m} {thing}.", f"Figure 1 has {m}(1) + {b}.", f"Figure n: {m}n + {b}.", f"Check n = 3: {m}(3) + {b} = {seq[2]}."],
                 [f"{m}n", f"n + {m}", f"{b}n + {m}"], PY("rule_fits", seq=seq), why=["Forgot the starting amount", "Added instead of multiplying", "Switched the rate and the start"], tags=["multiple-representations"])
    return Q(f"Figure 1 uses {seq[0]} {thing}, Figure 2 uses {seq[1]}, and Figure 3 uses {seq[2]}. If the pattern continues, how many {thing} are in Figure {n}?", str(m * n + b),
             [f"Each figure adds {m} {thing}.", f"Figure n has {m}n + {b} {thing}.", f"Figure {n}: {m}({n}) + {b} = {m * n + b}."],
             [str(seq[0] * n), str(m * n), str(seq[2] + m * (n - 2))], PY("nth_term", seq=seq, n=n), why=["Multiplied Figure 1 by the figure number", "Forgot the starting amount", "Added one too many groups"],
             tags=["modeling"])


@fam("012")
def s10_repeat(r, L):
    blk = pick(r, [["red", "blue", "green"], ["A", "B", "C", "D"], ["circle", "square", "square", "triangle"], ["▲", "●", "■", "●", "▲"]])
    n = r.randint(20, 60) if L < 2 else r.randint(100, 500)
    show = ", ".join((blk * 3)[: len(blk) * 2])
    ans = blk[(n - 1) % len(blk)]
    others = list(dict.fromkeys(b for b in blk if b != ans))
    need(len(others) >= 1)
    return Q(f"The pattern repeats: {show}, … What is item number {n}?", ans,
             [f"The pattern repeats every {len(blk)} items.", f"{n} ÷ {len(blk)} has remainder {n % len(blk)}.", f"Item {n} matches item {(n - 1) % len(blk) + 1} of the block: {ans}."],
             others, PY("repeat_pos", block=blk, n=n), mode="sa", why=["Used the quotient instead of the remainder"] * len(others), tags=["reasoning"])


@fam("12")
def s10_table_rule(r, L):
    m, b = nz(r, -5, 7), r.randint(-9, 12)
    seq = [m * n + b for n in range(1, 5)]
    rule = lin((m, "n"), (b, ""))
    return Q(f"Term numbers n = 1, 2, 3, 4 have values {', '.join(map(str, seq))}. Which expression gives the value of term n?", rule,
             [f"The values change by {m} each time, so the rule includes {m}n.", f"For n = 1: {m}(1) + ? = {seq[0]}, so add {b}.", f"Rule: {rule}."],
             [lin((m, "n")), lin((1, "n"), (m, "")), lin((m, "n"), (seq[0], ""))], PY("rule_fits", seq=seq), why=["Forgot the constant", "Added instead of multiplying", "Used the first term as the constant"],
             tags=["multiple-representations"])


# ============================================================== S12 Coordinate Plane
@fam("012")
def s12_read(r, L):
    rng_ = 5 if L == 0 else 8
    pts = []
    while len(pts) < 3:
        p = (nz(r, -rng_, rng_), nz(r, -rng_, rng_))
        if p not in pts and (L > 0 or p[0] > 0 or len(pts) > 0):
            pts.append(p)
    lab = ["A", "B", "C"]
    i = r.randrange(3)
    x, y = pts[i]
    alt = f"Coordinate plane from -{rng_} to {rng_} on both axes. " + "; ".join(f"Point {lab[k]} at ({pts[k][0]}, {pts[k][1]})" for k in range(3)) + "."
    return Q(f"What are the coordinates of point {lab[i]}?", f"({x}, {y})", ["Start at the origin.", f"Move {abs(x)} {'right' if x > 0 else 'left'} (x = {x}).", f"Move {abs(y)} {'up' if y > 0 else 'down'} (y = {y})."],
             [f"({y}, {x})", f"({-x}, {y})", f"({x}, {-y})"], PY("point", x=str(x), y=str(y)), why=["Switched the x- and y-coordinates", "Used the wrong sign for x", "Used the wrong sign for y"],
             diagram={"alt": alt, "draw": plane_draw((-rng_ - 1, rng_ + 1), (-rng_ - 1, rng_ + 1), points=[(p[0], p[1], lab[k]) for k, p in enumerate(pts)])}, tags=["graph"])


@fam("012")
def s12_quadrant(r, L):
    x, y = nz(r, -12, 12), nz(r, -12, 12)
    q = {(1, 1): "Quadrant I", (-1, 1): "Quadrant II", (-1, -1): "Quadrant III", (1, -1): "Quadrant IV"}
    if L == 2 and r.random() < 0.5:
        x = 0 if r.random() < 0.5 else x
        y = 0 if x != 0 else y
    if x == 0 or y == 0:
        ans = "y-axis" if x == 0 else "x-axis"
        return Q(f"Where is the point ({x}, {y})?", ans, ["A point with a 0 coordinate lies on an axis, not in a quadrant.", f"x = 0 → on the y-axis; y = 0 → on the x-axis.", f"({x}, {y}) is on the {ans}."],
                 ["x-axis" if ans == "y-axis" else "y-axis", "Quadrant I", "origin"], PY("quadrant", x=str(x), y=str(y)), why=["Mixed up the axes", "", ""], mode="mc")
    ans = q[(1 if x > 0 else -1, 1 if y > 0 else -1)]
    return Q(f"In which quadrant is the point ({x}, {y})?", ans, ["Quadrant I (+, +), II (-, +), III (-, -), IV (+, -).", f"x is {'positive' if x > 0 else 'negative'} and y is {'positive' if y > 0 else 'negative'}.", f"So the point is in {ans}."],
             [v for v in q.values() if v != ans], PY("quadrant", x=str(x), y=str(y)), why=["Numbered the quadrants clockwise", "", ""])


@fam("12")
def s12_distance(r, L):
    x1, y1 = nz(r, -9, 9), nz(r, -9, 9)
    if r.random() < 0.5:
        x2, y2 = nz(r, -9, 9), y1
        need(x2 != x1)
        d, e = abs(x1 - x2), f"|{x1} - ({x2})|"
    else:
        x2, y2 = x1, nz(r, -9, 9)
        need(y2 != y1)
        d, e = abs(y1 - y2), f"|{y1} - ({y2})|"
    same = "y" if y1 == y2 else "x"
    a, b = (x1, x2) if same == "y" else (y1, y2)
    return Q(f"What is the distance between ({x1}, {y1}) and ({x2}, {y2})?", f"{d} units",
             [f"The points have the same {same}-coordinate, so they are on a {'horizontal' if same == 'y' else 'vertical'} line.", f"Distance = |{a} - ({b})| = {d}.", f"The distance is {d} units."],
             [f"{abs(abs(a) - abs(b))} units" if abs(abs(a) - abs(b)) != d else f"{d + 1} units", f"{abs(a + b) if abs(a + b) != d else d + 2} units", f"{d * 2} units"],
             PY("absval", expr=e), why=["Subtracted the absolute values", "Added the coordinates", ""], tags=["connections"])


@fam("2")
def s12_reflect(r, L):
    x, y = nz(r, -9, 9), nz(r, -9, 9)
    ax = pick(r, ["x-axis", "y-axis"])
    nx, ny = (x, -y) if ax == "x-axis" else (-x, y)
    return Q(f"Point P({x}, {y}) is reflected over the {ax}. What are the coordinates of the image?", f"({nx}, {ny})",
             [f"Reflecting over the {ax} keeps the {'x' if ax == 'x-axis' else 'y'}-coordinate.", f"The other coordinate changes sign.", f"Image: ({nx}, {ny})."],
             [f"({-x if ax == 'x-axis' else x}, {y if ax == 'x-axis' else -y})", f"({-x}, {-y})", f"({y}, {x})"], PY("point", x=str(nx), y=str(ny)),
             why=["Reflected over the wrong axis", "Changed both signs", "Switched the coordinates"])


@fam("2")
def s12_rect(r, L):
    x1, y1 = r.randint(-8, -1), r.randint(-8, -1)
    w, h = r.randint(3, 9), r.randint(2, 8)
    pts = [(x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)]
    what = pick(r, ["perimeter", "area"])
    v = 2 * (w + h) if what == "perimeter" else w * h
    return Q(f"A rectangle has vertices {', '.join(f'({a}, {b})' for a, b in pts)}. What is its {what}?", f"{v} {'units' if what == 'perimeter' else 'square units'}",
             [f"Width = |{x1 + w} - ({x1})| = {w}.", f"Height = |{y1 + h} - ({y1})| = {h}.", f"{'Perimeter = 2(' + str(w) + ' + ' + str(h) + ')' if what == 'perimeter' else 'Area = ' + str(w) + ' × ' + str(h)} = {v}."],
             [f"{w * h if what == 'perimeter' else 2 * (w + h)} {'units' if what == 'perimeter' else 'square units'}", f"{w + h} {'units' if what == 'perimeter' else 'square units'}",
              f"{v + 4} {'units' if what == 'perimeter' else 'square units'}"], V(f"2*({w} + {h})" if what == "perimeter" else f"{w}*{h}"),
             why=["Found the area instead of the perimeter" if what == "perimeter" else "Found the perimeter instead of the area", "Added only two sides", ""], tags=["connections", "multistep"])


SKILLS = {
    1: dict(name="Place Value", std=["5.NBT.A.1", "5.NBT.A.3"], fams=[s1_digit_value, s1_expanded, s1_words, s1_order, s1_times], extra=[err_of(s1_digit_value), open_of(s1_expanded), err_of(s1_words)]),
    2: dict(name="Variables and Expressions", std=["6.EE.A.2a", "6.EE.A.2b"], fams=[s2_translate, s2_to_words, s2_parts, s2_context], extra=[err_of(s2_translate), open_of(s2_translate), select_of(s2_translate)]),
    3: dict(name="The Order of Operations", std=["6.EE.A.1", "5.OA.A.1"], fams=[s3_eval, s3_parens, s3_fraction_bar, s3_context], extra=[err_of(s3_eval), open_of(s3_eval), select_of(s3_eval)]),
    4: dict(name="Writing and Evaluating Expressions", std=["6.EE.A.2c", "7.EE.B.4"], fams=[s4_evaluate, s4_write_eval, s4_table], extra=[err_of(s4_evaluate), open_of(s4_evaluate), select_of(s4_evaluate)]),
    5: dict(name="Integers and Absolute Value", std=["6.NS.C.6a", "6.NS.C.7"], fams=[s5_abs, s5_compare, s5_opposite, s5_numline, s5_context, s5_solve_abs], extra=[err_of(s5_abs), open_of(s5_abs), select_of(s5_abs)]),
    6: dict(name="Adding Integers", std=["7.NS.A.1b", "7.NS.A.1d"], fams=[s6_sum, s6_context, s6_missing], extra=[err_of(s6_sum), open_of(s6_sum), select_of(s6_sum)]),
    7: dict(name="Subtracting Integers", std=["7.NS.A.1c"], fams=[s7_diff, s7_context, s7_distance], extra=[err_of(s7_diff), open_of(s7_diff), select_of(s7_diff)]),
    8: dict(name="Problem Solving: Rounding and Estimating", std=["5.NBT.A.4", "7.EE.B.3"], fams=[s8_round, s8_estimate, s8_reasonable], extra=[err_of(s8_round), open_of(s8_round), err_of(s8_estimate)]),
    9: dict(name="Inductive Reasoning", std=["8.F.A.1", "MP.3"], fams=[s9_next, s9_counter, s9_conjecture], extra=[err_of(s9_next), open_of(s9_next)]),
    10: dict(name="Patterns", std=["5.OA.B.3", "6.EE.C.9"], fams=[s10_figure, s10_repeat, s10_table_rule, s9_next], extra=[err_of(s10_figure), open_of(s10_figure)]),
    11: dict(name="Multiplying and Dividing Integers", std=["7.NS.A.2a", "7.NS.A.2b"], fams=[s11_prod, s11_context, s11_missing], extra=[err_of(s11_prod), open_of(s11_prod), select_of(s11_prod)]),
    12: dict(name="The Coordinate Plane", std=["6.NS.C.6b", "6.NS.C.8"], fams=[s12_read, s12_quadrant, s12_distance, s12_reflect, s12_rect], extra=[err_of(s12_quadrant), open_of(s12_distance), err_of(s12_distance)]),
}
