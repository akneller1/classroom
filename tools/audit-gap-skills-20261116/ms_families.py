"""Middle-grades gap skills (2026-11-16).

Grade 8, linear-functional-relationships: "Proportional relationships, unit rate, and slope" (8.EE.B.5).
Accelerated Grade 7, ratios-proportions-percentages: "Rewriting Expressions in Context" (7.EE.A.2).
"""
from fractions import Fraction as F
from core import I, Reject, need, ri, g, W, levels

# (y plural, x plural, x singular, sentence with {y} {x} for a constant-rate situation, thing name A, thing name B)
CTX = [
    ("miles", "hours", "hour", "A cyclist rides {y} miles in {x} hours at a constant speed.", "Rider A", "Rider B"),
    ("dollars", "pounds", "pound", "A store sells {x} pounds of almonds for {y} dollars.", "Store A", "Store B"),
    ("pages", "minutes", "minute", "A printer prints {y} pages in {x} minutes at a constant rate.", "Printer A", "Printer B"),
    ("gallons", "minutes", "minute", "A pump moves {y} gallons of water in {x} minutes at a constant rate.", "Pump A", "Pump B"),
    ("meters", "seconds", "second", "A robot travels {y} meters in {x} seconds at a constant speed.", "Robot A", "Robot B"),
    ("dollars", "hours", "hour", "A shop charges {y} dollars for {x} hours of bike rental.", "Shop A", "Shop B"),
    ("words", "minutes", "minute", "A student types {y} words in {x} minutes at a constant rate.", "Typist A", "Typist B"),
    ("cups", "batches", "batch", "A recipe uses {y} cups of flour for {x} batches of muffins.", "Recipe A", "Recipe B"),
]


def rate(r, L):
    if L == 0:
        return F(ri(r, 2, 12))
    if L == 1:
        return F(r.choice([3, 5, 7, 9, 11, 13, 15, 25, 35]), 2) if r.random() < 0.6 else F(ri(r, 13, 60))
    return r.choice([F(5, 4), F(9, 4), F(13, 4), F(7, 5), F(12, 5), F(17, 4), F(45, 2), F(7, 2), F(18, 5), F(27, 4), F(33, 4), F(31, 2)])


def xs3(r, L):
    pool = [2, 3, 4, 5, 6, 8, 10] if L < 2 else [4, 5, 8, 10, 12, 15, 20]
    return sorted(r.sample(pool, 3))


def lst(v):
    return ", ".join(g(x) for x in v)


def p_table(r, L):
    yn, xn, x1, _, _, _ = r.choice(CTX)
    k = rate(r, L)
    xs = xs3(r, L)
    ys = [k * x for x in xs]
    prompt = f"The table shows a proportional relationship between {xn} (x) and {yn} (y). x: {lst(xs)}; y: {lst(ys)}. Find the unit rate in {yn} per {x1}."
    ans = f"{g(k)} {yn} per {x1}"
    wr = [(f"{g(1 / k)} {yn} per {x1}", "divided x by y instead of y by x"),
          (f"{g(ys[1] - ys[0])} {yn} per {x1}", "subtracted two y-values without dividing by the change in x"),
          (f"{g(ys[0])} {yn} per {x1}", f"used the first y-value, which goes with x = {xs[0]}, not x = 1"),
          (f"{g(ys[2] - xs[2])} {yn} per {x1}", "subtracted x from y instead of dividing")]
    steps = [f"The unit rate is y ÷ x for any pair in the table.", f"{g(ys[0])} ÷ {xs[0]} = {g(k)}, and the other pairs give the same value.", f"The unit rate is {ans}."]
    return I(prompt, ans, steps, wr, dict(k="rate", xs=[g(x) for x in xs], ys=[g(y) for y in ys], show=[f"x: {lst(xs)}", f"y: {lst(ys)}"]), "prop_table")


def p_point(r, L):
    k = rate(r, L)
    x = r.choice([2, 4, 5, 6, 8] if L < 2 else [4, 8, 10, 12, 20])
    y = k * x
    prompt = f"The graph of a proportional relationship is a line through the origin and the point ({x}, {g(y)}). What is the slope of the line?"
    ans = g(k)
    wr = [(g(1 / k), "divided the x-coordinate by the y-coordinate"), (g(y - x), "subtracted the coordinates instead of dividing"), (g(y), "gave the y-coordinate instead of the slope"), (g(x * y), "multiplied the coordinates")]
    steps = [f"From (0, 0) to ({x}, {g(y)}) the rise is {g(y)} and the run is {x}.", f"Slope = {g(y)} ÷ {x} = {ans}.", "For a proportional relationship, the slope equals the unit rate."]
    return I(prompt, ans, steps, wr, dict(k="rate", xs=[g(x)], ys=[g(y)], show=[f"({x}, {g(y)})"]), "prop_point_slope")


def p_predict(r, L):
    k = rate(r, L)
    x1 = r.choice([2, 4, 5] if L < 2 else [4, 8, 10])
    x2 = r.choice([x for x in ([6, 7, 9, 10, 12] if L < 2 else [12, 16, 20, 30]) if x != x1])
    y1, y2 = k * x1, k * x2
    prompt = f"A proportional relationship includes the point ({x1}, {g(y1)}). Find the value of y when x = {x2}."
    ans = g(y2)
    wr = [(g(y1 + (x2 - x1)), "added the change in x to y instead of multiplying by the unit rate"), (g(F(x1, 1) / y1 * x2), "used x ÷ y as the unit rate"), (g(y1 * x2), "multiplied y by the new x without first finding the unit rate")]
    steps = [f"Unit rate: {g(y1)} ÷ {x1} = {g(k)}.", f"y = {g(k)}x, so when x = {x2}, y = {g(k)} · {x2} = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="predict", x=g(x1), y=g(y1), x2=g(x2), show=[f"({x1}, {g(y1)})", f"x = {x2}"]), "prop_predict")


def p_equation(r, L):
    yn, xn, x1, sent, _, _ = r.choice(CTX)
    k = rate(r, L)
    x = r.choice([2, 3, 4, 5, 6] if L < 2 else [4, 8, 12, 20])
    y = k * x
    prompt = sent.format(x=x, y=g(y)) + f" Write an equation that gives the number of {yn}, y, for x {xn}."
    ans = f"y = {g(k)}x"
    wr = [(f"y = {g(1 / k)}x", "divided x by y to get the unit rate"), (f"y = x + {g(y - x)}" if y > x else f"y = {g(x + y)}x", "used addition instead of a constant ratio"), (f"y = {g(y)}x", f"used the total {g(y)} as the unit rate"), (f"y = {x}x", "used the x-value as the unit rate")]
    steps = [f"Unit rate: {g(y)} ÷ {x} = {g(k)} {yn} per {x1}.", f"A proportional relationship has the form y = kx, so {ans}."]
    return I(prompt, ans, steps, wr, dict(k="propEq", x=g(x), y=g(y), show=[g(y) + " ", f"{x} "]), "prop_equation")


def p_compare(r, L):
    yn, xn, x1, _, A, B = r.choice(CTX)
    ka = rate(r, L)
    kb = rate(r, L)
    need(ka != kb)
    xs = xs3(r, L)
    ys = [kb * x for x in xs]
    prompt = (f"{A} is described by the equation y = {g(ka)}x, where x is the number of {xn} and y is the number of {yn}. {B} is described by the table. "
              f"x: {lst(xs)}; y: {lst(ys)}. Which has the greater unit rate, and by how much?")
    win, lose = (A, B) if ka > kb else (B, A)
    d = abs(ka - kb)
    need(d != 1)
    ans = f"{win}, by {g(d)} {yn} per {x1}"
    wr = [(f"{lose}, by {g(d)} {yn} per {x1}", "compared the unit rates in the wrong order"),
          (f"{B}, by {g(abs(ys[0] - ka))} {yn} per {x1}", f"compared the first table value {g(ys[0])} with {g(ka)} instead of finding the table's unit rate"),
          (f"{win}, by {g(ka + kb)} {yn} per {x1}", "added the unit rates instead of subtracting"),
          ("They have the same unit rate", "did not compute the unit rate from the table")]
    wr = [(t, w) for t, w in wr if ", by 1 " not in t]
    steps = [f"{A}: the unit rate is the coefficient of x, {g(ka)} {yn} per {x1}.", f"{B}: {g(ys[0])} ÷ {xs[0]} = {g(kb)} {yn} per {x1}.", f"{g(max(ka, kb))} − {g(min(ka, kb))} = {g(d)}, so the answer is {ans}."]
    return I(prompt, ans, steps, wr, dict(k="compare", a=g(ka), xs=[g(x) for x in xs], ys=[g(y) for y in ys], A=A, B=B, unit=f"{yn} per {x1}", show=[f"y = {g(ka)}x", f"x: {lst(xs)}", f"y: {lst(ys)}"]), "prop_compare")


def p_unitpoint(r, L):
    yn, xn, x1, _, _, _ = r.choice(CTX)
    k = rate(r, L)
    need(k != 1)
    prompt = f"A proportional relationship has a unit rate of {g(k)} {yn} per {x1}. On its graph (x = {xn}, y = {yn}), which point shows the unit rate?"
    ans = f"(1, {g(k)})"
    wr = [(f"({g(k)}, 1)", "switched the coordinates"), (f"(0, {g(k)})", "put the unit rate on the y-axis; a proportional graph passes through (0, 0)"), (f"({g(k)}, {g(k)})", "used the unit rate for both coordinates")]
    steps = ["The unit rate is the value of y when x = 1.", f"So the point is {ans}."]
    return I(prompt, ans, steps, wr, dict(k="unitpoint", r=g(k), show=[f"unit rate of {g(k)} "]), "prop_unit_point")


p_unitpoint.mc_only = True

# ---------------------------------------------------------------- 7.EE.A.2
UP = [("A store raises the price of a jacket that costs {v} dollars by {p}%.", "p", "new price"),
      ("Maya leaves a {p}% tip on a meal that costs {v} dollars.", "m", "total cost"),
      ("A town's population of {v} people grows by {p}% in one year.", "n", "new population"),
      ("A worker who earns {v} dollars per week gets a {p}% raise.", "w", "new weekly pay"),
      ("Sales tax of {p}% is added to an item that costs {v} dollars.", "c", "total cost")]
DOWN = [("A coat that costs {v} dollars is on sale for {p}% off.", "p", "sale price"),
        ("A phone that costs {v} dollars loses {p}% of its value in a year.", "v", "value after one year"),
        ("A club with {v} members loses {p}% of its members.", "m", "number of members left"),
        ("A tank holding {v} gallons loses {p}% of its water.", "w", "amount of water left"),
        ("A coupon takes {p}% off a bill of {v} dollars.", "b", "amount paid")]


def pct(r, L):
    if L == 0:
        return F(r.choice([10, 20, 25, 30, 40, 50]))
    if L == 1:
        return F(r.choice([5, 8, 12, 15, 35, 45, 60, 6, 4]))
    return r.choice([F(15, 2), F(25, 2), F(13, 2), F(9, 2), F(7, 4), F(33), F(18), F(125, 10), F(5, 2)])


def e_increase(r, L):
    sent, v, what = r.choice(UP)
    p = pct(r, L)
    d = p / 100
    prompt = sent.format(v=v, p=g(p)) + f" The {what} is {v} + {g(d)}{v}. Write the {what} as a single term."
    ans = f"{g(1 + d)}{v}"
    wr = [(f"{g(d)}{v}", "wrote only the amount of the increase"), (f"{g(1 + d * 10)}{v}", "misplaced the decimal point in the percent"),
          (f"{g(p)}{v}", "used the percent as a whole number"), (f"{g(1 - d)}{v}", "subtracted the percent instead of adding")]
    steps = [f"{v} is the same as 1{v}.", f"1{v} + {g(d)}{v} = {ans}.", f"Multiplying by {g(1 + d)} is the same as increasing by {g(p)}%."]
    return I(prompt, ans, steps, wr, dict(k="ident", var=v, e=f"{v} + {g(d)}{v}", show=[f"{v} + {g(d)}{v}"]), "expr_percent_increase")


def e_decrease(r, L):
    sent, v, what = r.choice(DOWN)
    p = pct(r, L)
    d = p / 100
    prompt = sent.format(v=v, p=g(p)) + f" The {what} is {v} - {g(d)}{v}. Write the {what} as a single term."
    ans = f"{g(1 - d)}{v}"
    wr = [(f"{g(d)}{v}", "wrote only the amount taken off"), (f"{g(1 + d)}{v}", "added the percent instead of subtracting"),
          (f"{g(p)}{v}", "used the percent as a whole number"), (f"-{g(d)}{v}", "dropped the original amount")]
    steps = [f"{v} is the same as 1{v}.", f"1{v} - {g(d)}{v} = {ans}.", f"Multiplying by {g(1 - d)} is the same as decreasing by {g(p)}%."]
    return I(prompt, ans, steps, wr, dict(k="ident", var=v, e=f"{v} - {g(d)}{v}", show=[f"{v} - {g(d)}{v}"]), "expr_percent_decrease")


def e_meaning_up(r, L):
    sent, v, what = r.choice(UP)
    p = pct(r, L)
    f = 1 + p / 100
    prompt = f"The expression {g(f)}{v} gives the {what} following a percent increase, where {v} is the original amount. What is the percent increase?"
    ans = f"{g(p)}%"
    wr = [(f"{g(f * 100)}%", "read the whole multiplier as the percent increase"), (f"{g(p / 100)}%", "did not convert the decimal to a percent"), (f"{g(f)}%", "wrote the multiplier with a percent sign"), (f"{g(100 - p)}%", "subtracted from 100")]
    steps = [f"{g(f)}{v} = 1{v} + {g(f - 1)}{v}.", f"The extra {g(f - 1)}{v} is {g(p)}% of the original amount.", f"The increase is {ans}."]
    return I(prompt, ans, steps, wr, dict(k="pct", factor=g(f), show=[f"{g(f)}{v}", "percent increase"]), "expr_meaning_increase")


def e_meaning_down(r, L):
    sent, v, what = r.choice(DOWN)
    p = pct(r, L)
    f = 1 - p / 100
    prompt = f"The expression {g(f)}{v} gives the {what} following a percent decrease, where {v} is the original amount. What is the percent decrease?"
    ans = f"{g(p)}%"
    wr = [(f"{g(f * 100)}%", "gave the percent that remains instead of the percent decrease"), (f"{g(p / 100)}%", "did not convert the decimal to a percent"), (f"{g(f)}%", "wrote the multiplier with a percent sign"), (f"{g(100 + p)}%", "added to 100")]
    steps = [f"{g(f)}{v} = 1{v} - {g(1 - f)}{v}.", f"The amount removed, {g(1 - f)}{v}, is {g(p)}% of the original amount.", f"The decrease is {ans}."]
    return I(prompt, ans, steps, wr, dict(k="pct", factor=g(f), show=[f"{g(f)}{v}", "percent decrease"]), "expr_meaning_decrease")


def e_combine(r, L):
    a, b = ri(r, 3, 15), ri(r, 2, 9)
    need(a != b)
    kind = r.choice(["tickets", "team", "garden"])
    if kind == "tickets":
        prompt = f"Each of n friends pays {a} dollars for a movie ticket and {b} dollars for a snack. The total cost is {a}n + {b}n. Write the total cost as a single term."
        e, v = f"{a}n + {b}n", "n"
    elif kind == "team":
        prompt = f"A coach buys a jersey for {a} dollars and a hat for {b} dollars for each of t players. The total cost is {a}t + {b}t. Write the total cost as a single term."
        e, v = f"{a}t + {b}t", "t"
    else:
        prompt = f"A gardener plants {a} tulips and {b} daisies in each of r rows. The total number of flowers is {a}r + {b}r. Write the total as a single term."
        e, v = f"{a}r + {b}r", "r"
    ans = f"{a + b}{v}"
    wr = [(f"{a * b}{v}", "multiplied the coefficients instead of adding"), (f"{a + b}{v}²", "added the coefficients but also multiplied the variables"), (f"{a + b}", "dropped the variable"), (f"{a}{b}{v}", "wrote the coefficients side by side")]
    steps = [f"Both terms have the variable {v}, so add the coefficients.", f"{a} + {b} = {a + b}, so {e} = {ans}.", f"Each {'friend' if v == 'n' else 'player' if v == 't' else 'row'} accounts for {a + b} in all."]
    return I(prompt, ans, steps, wr, dict(k="ident", var=v, e=e, show=[e]), "expr_combine_context")


def e_factor(r, L):
    k = r.choice([2, 3, 4, 5, 6])
    a = ri(r, 2, 9)
    kind = r.choice(["order", "fence"])
    if kind == "order":
        prompt = f"An order of {k} identical boxes costs {k}x + {k * a} dollars in all, where x is the price of the item in each box. Write the total cost in factored form to show the cost of one box."
        v = "x"
    else:
        prompt = f"The total length of {k} equal fence sections is {k}x + {k * a} feet. Write the total length in factored form to show the length of one section."
        v = "x"
    e = f"{k}{v} + {k * a}"
    ans = f"{k}({v} + {a})"
    wr = [(f"{k}({v} + {k * a})", "factored the first term only"), (f"{k}{v} + {a}", "divided only the constant by the common factor"), (f"{k + k * a}{v}", "combined unlike terms"), (f"({v} + {a})", "dropped the common factor")]
    steps = [f"Both terms are divisible by {k}.", f"{k}{v} + {k * a} = {k}·{v} + {k}·{a} = {ans}.", f"One {'box costs' if kind == 'order' else 'section is'} {v} + {a}."]
    return I(prompt, ans, steps, wr, dict(k="ident", var=v, e=e, show=[e]), "expr_factor_context")


def e_expand(r, L):
    levels(L, 1, 2)
    k = ri(r, 2, 6)
    a, b = ri(r, 4, 25), ri(r, 5, 40)
    kind = r.choice(["gym", "taxi"])
    if kind == "gym":
        prompt = f"A gym charges a {b}-dollar sign-up fee plus {a} dollars per month. The total cost for {k} friends who each stay n months is {k}({a}n + {b}). Write the total cost in expanded form."
    else:
        prompt = f"A ride costs a {b}-dollar base fare plus {a} dollars per mile. The total cost of {k} rides of n miles each is {k}({a}n + {b}). Write the total cost in expanded form."
    e = f"{k}({a}n + {b})"
    ans = f"{k * a}n + {k * b}"
    wr = [(f"{k * a}n + {b}", "multiplied only the first term by the factor"), (f"{a}n + {k * b}", "multiplied only the second term by the factor"), (f"{k + a}n + {k + b}", "added the factor instead of multiplying"), (f"{k * a + k * b}n", "combined unlike terms after distributing")]
    steps = [f"Distribute {k} to both terms.", f"{k}·{a}n + {k}·{b} = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="ident", var="n", e=e, show=[e]), "expr_expand_context")


def e_double(r, L):
    levels(L, 2)
    p1, p2 = r.choice([10, 20, 25, 50]), r.choice([10, 20, 30, 40, 50])
    up1, up2 = r.random() < 0.6, r.random() < 0.5
    f1 = 1 + F(p1, 100) if up1 else 1 - F(p1, 100)
    f2 = 1 + F(p2, 100) if up2 else 1 - F(p2, 100)
    w1, w2 = ("raised" if up1 else "lowered"), ("raised" if up2 else "lowered")
    prompt = f"A price p is {w1} by {p1}% and the result is then {w2} by {p2}%. The final price is {g(f2)}({g(f1)}p). Write the final price as a single term."
    ans = f"{g(f1 * f2)}p"
    naive = 1 + (F(p1, 100) if up1 else -F(p1, 100)) + (F(p2, 100) if up2 else -F(p2, 100))
    wr = [(f"{g(naive)}p", "added the two percent changes instead of multiplying the factors"), (f"{g(f1 + f2)}p", "added the two multipliers"), (f"{g(f1)}p", "ignored the second change"), (f"{g(f2)}p", "ignored the first change")]
    steps = [f"Multiply the two factors: {g(f2)} · {g(f1)} = {g(f1 * f2)}.", f"The final price is {ans}.", "Percent changes applied one after another multiply; they do not add."]
    return I(prompt, ans, steps, wr, dict(k="ident", var="p", e=f"{g(f2)}({g(f1)}p)", show=[f"{g(f2)}({g(f1)}p)"]), "expr_two_changes")


SKILLS = {
    ("prealgebra", "linear-functional-relationships", "Proportional relationships, unit rate, and slope"): dict(fns=[p_table, p_point, p_predict, p_equation, p_compare, p_unitpoint], stds=["8.EE.B.5"], prefix="pa8-lfr"),
    ("prealgebra7", "ratios-proportions-percentages", "Rewriting Expressions in Context"): dict(fns=[e_increase, e_decrease, e_meaning_up, e_meaning_down, e_combine, e_factor, e_expand, e_double], stds=["7.EE.A.2"], prefix="pa7-rpp"),
}
