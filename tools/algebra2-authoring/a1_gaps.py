"""Algebra 1 gap-skill banks: the 12 catalog skills the legacy generators cover only partly or not at all
(per worksheet-generator/planner/lesson-skills.js). One JSON per unit, holding only those skills."""
from lib import Bank, graph
from mathlite import *
from fill import fill
import math, random, sys
import numpy as np

def fillc(B, S, target, makers, R, cap=7):
    """fill() with a per-maker cap so no single template dominates a skill."""
    from fill import skill_count
    used = {}
    for _ in range(1500):
        if skill_count(B, S) >= target: break
        live = [m for m in makers if used.get(m, 0) < cap]
        if not live: break
        m = R.choice(live); before = skill_count(B, S)
        fill(B, S, before + 1, [m], R, max_tries=3)
        if skill_count(B, S) > before: used[m] = used.get(m, 0) + 1
    return skill_count(B, S)
def L(m, b, v="x"): return pstr(P([F(b), F(m)], v))
def lvl(R): return R.choice(["cp2", "cp1", "cp1", "honors"])
def sgn(v): return "+" if v >= 0 else "-"
def nfr(v): v = F(v); return fr(v) if v >= 0 else f"({fr(v)})"

# =====================================================================================
# Unit 1 · foundations-algebra: skills 4 (operations with real numbers), 5 (properties), 7 (interpreting expressions)
# =====================================================================================
def unit_foundations():
    B = Bank("foundations-algebra", "fa", {4: ["N-RN.B.3", "7.NS.A.3"], 5: ["A-SSE.A.1", "N-RN.B.3"], 7: ["A-SSE.A.1a", "A-SSE.A.1b"]}, course="algebra", prefix="a1"); R = random.Random(101)
    lv = lambda: lvl(R)
    # ---- skill 4 ----
    def ops_int():
        a, b, c = R.randint(-15, 15), R.randint(-12, 12), R.randint(-9, 9)
        if 0 in (b, c): raise ValueError
        k = R.choice(["a-b*c", "(a-b)*c", "a/b+c", "-a^2"])
        if k == "a-b*c": e, v, w = f"{a} − ({b})({c})", a - b * c, [(a - b) * c, a + b * c, -a - b * c]
        elif k == "(a-b)*c": e, v, w = f"({a} − ({b}))·({c})", (a - b) * c, [a - b * c, (a + b) * c, -(a - b) * c]
        elif k == "a/b+c":
            a = b * R.randint(-9, 9); e, v, w = f"{a} ÷ ({b}) + ({c})", F(a, b) + c, [F(a, b + c) if b + c else 99, -F(a, b) + c, F(a, b) - c]
        else:
            a = R.randint(2, 9); e, v, w = f"−{a}² + ({c})", -a * a + c, [a * a + c, -2 * a + c, -a * a - c]
        B.mc(4, lv(), f"Evaluate {e}.", fr(v), [fr(x) for x in w], ["Order of operations: grouping, exponents, multiply/divide left to right, then add/subtract.", "Use sign rules for integers.", f"Result: {fr(v)}."], tags=["misconception"])
    def ops_frac():
        a, b = F(R.randint(-9, 9), R.choice([2, 3, 4, 5, 6, 8])), F(R.randint(1, 9), R.choice([2, 3, 4, 5, 6]))
        if a == 0: raise ValueError
        op = R.choice(["+", "−", "×", "÷"]); v = {"+": a + b, "−": a - b, "×": a * b, "÷": a / b}[op]
        bad = {"+": F(a.numerator + b.numerator, a.denominator + b.denominator), "−": a + b, "×": a * b.denominator / b.numerator if b.numerator else 0, "÷": a * b}[op]
        if R.random() < 0.5:
            B.sa(4, lv(), f"Compute {nfr(a)} {op} {nfr(b)}. Write the answer in simplest form.", fr(v), ["Common denominators for + and −; multiply across for ×; multiply by the reciprocal for ÷.", "Simplify."])
        else:
            B.mc(4, lv(), f"Compute {nfr(a)} {op} {nfr(b)}.", fr(v), [fr(bad), fr(-v), fr(v + 1)], ["Use the rule for the operation, then simplify.", "Watch the sign."], tags=["misconception"])
    def ops_dec():
        a, b = F(R.randint(-250, 250), 100), F(R.randint(-99, 99), 10)
        if b == 0 or a == 0: raise ValueError
        op = R.choice(["+", "−", "×"]); v = {"+": a + b, "−": a - b, "×": a * b}[op]
        def d(x): x = F(x); s = f"{float(x):.4f}".rstrip("0").rstrip("."); return s if x >= 0 else s
        B.sa(4, lv(), f"Compute {d(a) if a >= 0 else '(' + d(a) + ')'} {op} {d(b) if b >= 0 else '(' + d(b) + ')'}.", d(v), ["Line up decimal places (or count them when multiplying).", "Apply integer sign rules."])
    def ops_sel():
        t = R.choice([-12, -18, 24, -20, 36, -30, 15, -16])
        cands = [(f"({t // 2})·2", True), (f"{t // 3} + {t - t // 3}", True) if t // 3 != t else None, (f"−({-t})", True), (f"{-t} − {2 * -t}", -t - 2 * -t == t), (f"({t // 2})²", (t // 2) ** 2 == t), (f"{2 * t} ÷ (−2)", F(2 * t, -2) == t), (f"|{t}|", abs(t) == t)]
        cands = [c for c in cands if c]
        for e, v in cands:
            ev = eval(e.replace("−", "-").replace("·", "*").replace("÷", "/").replace("²", "**2").replace("|", "abs(", 1).replace("|", ")"))
            assert (ev == t) == v, (e, ev, t)
        R.shuffle(cands)
        B.sel(4, lv(), f"Select ALL expressions whose value is {t}.", [e for e, v in cands if v], [e for e, v in cands if not v], ["Evaluate each expression carefully, including signs and absolute value."], tags=["concept"])
    def ops_closure():
        pool = [("The sum of two rational numbers is rational", True), ("The sum of a rational number and an irrational number is irrational", True), ("The product of a nonzero rational number and an irrational number is irrational", True),
                ("The product of two irrational numbers is always irrational", False), ("The sum of two irrational numbers is always irrational", False), ("The quotient of two integers (nonzero divisor) is rational", True), ("√2 · √2 is irrational", False), ("√9 is irrational", False), ("0.333… is rational", True), ("π + 1 is rational", False)]
        st = R.sample(pool, 5)
        if sum(v for _, v in st) < 2 or all(v for _, v in st): raise ValueError
        key = tuple(sorted(s for s, _ in st))
        B.sel(4, R.choice(["cp1", "honors"]), "Select ALL true statements about real numbers" + R.choice(["", " (closure)", " and their operations", " — rational and irrational"]) + ".", [s for s, v in st if v], [s for s, v in st if not v], ["Rationals are closed under +, −, ×, ÷ (nonzero).", "Rational + irrational is irrational; irrational × irrational may be rational (√2·√2 = 2)."], tags=["concept"])
    def ops_orq():
        t0, d1, d2 = R.randint(-15, 5), R.randint(3, 12), R.randint(4, 15); d3 = F(R.randint(1, 9), 2)
        v1 = t0 - d1; v2 = v1 + d2; v3 = v2 - d3
        B.orq(4, lv(), f"At 6 a.m. the temperature was {t0}°F. It fell {d1}° by 8 a.m., rose {d2}° by noon, then fell {fr(d3)}° by 3 p.m.", [("Temperature at 8 a.m.?", f"{v1}°F"), ("Temperature at noon?", f"{v2}°F"), ("Temperature at 3 p.m.?", f"{fr(v3)}°F"), ("Total change from 6 a.m. to 3 p.m.?", f"{fr(v3 - t0)}°")], [f"{t0} − {d1}.", f"{v1} + {d2}.", f"{v2} − {fr(d3)}.", "Final − initial."], tags=["application"])
    # ---- skill 5 ----
    PROPS = ["Commutative Property of Addition", "Commutative Property of Multiplication", "Associative Property of Addition", "Associative Property of Multiplication", "Distributive Property", "Additive Identity Property", "Multiplicative Identity Property", "Additive Inverse Property", "Multiplicative Inverse Property", "Multiplication Property of Zero"]
    def prop_ex(p):
        a, b, c = R.randint(2, 15), R.randint(2, 15), R.randint(2, 9); v = R.choice("xyntm")
        return {PROPS[0]: f"{a} + {v} = {v} + {a}", PROPS[1]: f"{a}·{v} = {v}·{a}", PROPS[2]: f"({a} + {b}) + {v} = {a} + ({b} + {v})", PROPS[3]: f"({a}·{b})·{v} = {a}·({b}·{v})", PROPS[4]: f"{a}({v} + {b}) = {a}{v} + {a * b}",
                PROPS[5]: f"{v} + 0 = {v}", PROPS[6]: f"1·{a}{v} = {a}{v}", PROPS[7]: f"{a}{v} + (−{a}{v}) = 0", PROPS[8]: f"{a} · (1/{a}) = 1", PROPS[9]: f"{a}{v} · 0 = 0"}[p]
    def prop_name():
        p = R.choice(PROPS); e = prop_ex(p); near = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2], 4: [3, 1], 5: [6, 7], 6: [5, 8], 7: [8, 5], 8: [7, 6], 9: [5, 6]}[PROPS.index(p)]
        B.mc(5, lv(), f"Which property is shown? {e}", p, [PROPS[i] for i in near] + [R.choice([q for q in PROPS if q != p])], ["Commutative: order changes. Associative: grouping changes. Identity: adding 0 / multiplying by 1. Inverse: result 0 or 1."], tags=["misconception"])
    def prop_sel():
        tgt = R.choice(["Commutative", "Associative", "Identity", "Inverse"])
        pool = [(prop_ex(p), tgt in p) for p in R.sample(PROPS, 6)]
        if sum(v for _, v in pool) < 2 or all(v for _, v in pool): raise ValueError
        B.sel(5, lv(), f"Select ALL equations that illustrate {'an' if tgt[0] in 'AEIOU' else 'a'} {tgt} Property (of addition or multiplication).", [e for e, v in pool if v], [e for e, v in pool if not v], ["Commutative: order; Associative: grouping; Identity: 0 or 1 leaves a value unchanged; Inverse: produces 0 or 1."], tags=["concept"])
    def prop_steps():
        a, b, c = R.randint(2, 9), R.randint(2, 12), R.randint(2, 9)
        B.orq(5, lv(), f"Justify each step in simplifying {b} + {a}x + {c}.", [(f"{b} + {a}x + {c} = {a}x + {b} + {c}", "Commutative Property of Addition"), (f"= {a}x + ({b} + {c})", "Associative Property of Addition"), (f"= {a}x + {b + c}", "Simplify (add)"), ("Could the Commutative Property have been skipped? Explain.", f"Yes: ({b} + {a}x) + {c} could be regrouped as {b} + ({a}x + {c}) and reordered later, but some reordering is needed to combine {b} and {c}")], ["Order changed.", "Grouping changed.", "Arithmetic.", "Properties can be applied in different orders."], tags=["reasoning"])
    def prop_mental():
        k = R.random()
        if k < 0.5:
            n = R.randint(11, 99); a, b = R.choice([(25, 4), (5, 20), (50, 2), (4, 25), (2, 50), (20, 5)])
            B.orq(5, lv(), f"Use properties to compute {a} · {n} · {b} mentally.", [("Reorder the factors.", f"{a} · {b} · {n}"), ("Name the property.", "Commutative Property of Multiplication"), ("Group the friendly pair.", f"({a} · {b}) · {n} = {a * b} · {n}"), ("Find the product.", str(a * b * n))], ["Swap order.", "Commutative.", "Associative.", "Multiply."], tags=["reasoning"])
        else:
            a = R.randint(3, 9); n = R.choice([99, 98, 101, 102, 199, 49, 51])
            B.sa(5, lv(), f"Use the Distributive Property to compute {a} · {n} mentally. Show the rewritten expression.", f"{a}({round(n, -1)} {sgn(n - round(n, -1))} {abs(n - round(n, -1))}) = {a * n}", [f"{n} = {round(n, -1)} {sgn(n - round(n, -1))} {abs(n - round(n, -1))}.", f"{a}·{round(n, -1)} {sgn(n - round(n, -1))} {a}·{abs(n - round(n, -1))} = {a * n}."], tags=["reasoning"])
    def prop_counter():
        op = R.choice(["subtraction", "division"]); a, b = R.randint(5, 20), R.randint(2, 4)
        if op == "subtraction": ex = f"{a} − {b} = {a - b} but {b} − {a} = {b - a}"
        else: a = b * R.randint(2, 6); ex = f"{a} ÷ {b} = {fr(F(a, b))} but {b} ÷ {a} = {fr(F(b, a))}"
        B.mc(5, R.choice(["cp1", "honors"]), f"Is {op} commutative? Choose the best answer.", f"No; for example {ex}", [f"Yes; order never matters for {op}", f"Yes, but only for positive numbers", f"No, because {op} has no identity element"], ["One counterexample shows a property fails."], tags=["reasoning"])
    # ---- skill 7 ----
    CTX = [("A taxi ride costs {a} + {b}m dollars, where m is the number of miles.", "the fixed starting fee", "the cost per mile", "m"),
           ("A gym membership costs {a} + {b}n dollars, where n is the number of months.", "the one-time sign-up fee", "the monthly fee", "n"),
           ("A plumber charges {a} + {b}h dollars for h hours of work.", "the flat service-call fee", "the hourly rate", "h"),
           ("The water in a tank is {a} − {b}t gallons after t minutes of draining.", "the starting amount of water", "the gallons drained per minute", "t"),
           ("A phone plan costs {a} + {b}g dollars for g gigabytes of data.", "the base monthly charge", "the cost per gigabyte", "g"),
           ("A candle is {a} − {b}h centimeters tall after burning for h hours.", "the candle's starting height", "the centimeters burned per hour", "h")]
    def ctx_part():
        t, c0, r0, v = R.choice(CTX); a, b = R.randint(5, 60), R.choice([F(R.randint(1, 30), 4), R.randint(2, 15)])
        txt = t.format(a=a, b=fr(b) if F(b).denominator == 1 else f"{float(b):g}")
        part = R.choice(["a", "b", "term"])
        if part == "a": B.mc(7, lv(), f"{txt} What does {a} represent?", c0, [r0, f"the total for 1 {v}-unit", f"the value of {v}"], ["The constant term is the value when the variable is 0."], tags=["context"])
        elif part == "b": B.mc(7, lv(), f"{txt} What does {fr(b) if F(b).denominator == 1 else f'{float(b):g}'} represent?", r0, [c0, "the total cost or amount", f"the number of {v}-units"], ["The coefficient is the change per one unit of the variable."], tags=["context"])
        else: B.mc(7, lv(), f"{txt} What does the term {fr(b) if F(b).denominator == 1 else f'{float(b):g}'}{v} represent?", "the amount that depends on " + {"m": "the miles driven", "n": "the number of months", "h": "the hours", "t": "the minutes of draining", "g": "the data used"}[v], [c0, r0, "the total amount"], ["A coefficient times a variable is the variable part of the total."], tags=["context"])
    def ctx_orq():
        t, c0, r0, v = R.choice(CTX); a, b = R.randint(10, 80), R.randint(2, 15); n = R.randint(2, 12); txt = t.format(a=a, b=b)
        minus = "−" in t; val = a - b * n if minus else a + b * n
        if val < 0: raise ValueError
        B.orq(7, lv(), txt, [("Identify the terms.", f"{a} and {'−' if minus else ''}{b}{v}"), ("Identify the coefficient and the constant.", f"coefficient {'−' if minus else ''}{b}; constant {a}"), (f"Evaluate the expression for {v} = {n}.", str(val)), ("Interpret that value in context.", f"after {n} units of {v} the amount is {val}")], ["Terms are separated by + or −.", "The number multiplying the variable; the number alone.", "Substitute.", "Use the units of the situation."], tags=["context"])
    def ctx_tax():
        r = R.choice([5, 6, 7, 8, 10, 15, 20, 25]); kind = R.choice(["tax", "tip", "discount"])
        fac = F(100 + r, 100) if kind != "discount" else F(100 - r, 100); f_ = f"{float(fac):g}"
        B.sel(7, lv(), f"A store writes the final price of an item that costs p dollars as {f_}p. Select ALL correct interpretations.", [f"{f_}p means {fac.numerator * 100 // fac.denominator}% of the original price", f"{f_}p = p {'+' if kind != 'discount' else '−'} {float(F(r, 100)):g}p", f"The {kind} rate is {r}%"], [f"The {kind} is {f_} dollars", f"The {kind} rate is {f_}%", f"{f_}p = p + {f_}"], ["Factor: p ± (r/100)p = (1 ± r/100)p."], tags=["context", "concept"])
    def ctx_equiv():
        l, w = R.randint(3, 20), R.randint(2, 15); k = R.random()
        if k < 0.5:
            B.sel(7, lv(), f"A garden is l feet long and w feet wide. Select ALL expressions that give its perimeter.", ["2l + 2w", "2(l + w)", "l + w + l + w"], ["lw", "2lw", "l + w"], ["Perimeter adds all four sides; the forms are equivalent by the Distributive Property."], tags=["context", "concept"])
        else:
            n = R.randint(3, 9); c = R.randint(2, 12)
            B.mc(7, R.choice(["cp1", "honors"]), f"A class of {n} students each buy a ticket for t dollars and a snack for {c} dollars. Which expression shows the total and what does ({'t + ' + str(c)}) mean?", f"{n}(t + {c}); the cost for one student", [f"{n}t + {c}; the cost for one student", f"{n}(t + {c}); the total for all students", f"{n} + t + {c}; the number of items"], ["Each student pays t + c; multiply by the number of students."], tags=["context"])
    def ctx_compare():
        a1, b1 = R.randint(20, 60), R.randint(2, 6); a2, b2 = R.randint(0, 15), R.randint(b1 + 2, b1 + 10)
        cross = F(a1 - a2, b2 - b1)
        if cross <= 0 or cross.denominator != 1: raise ValueError
        B.orq(7, "honors", f"Plan A costs {a1} + {b1}x dollars and Plan B costs {a2} + {b2}x dollars for x visits.", [("Which plan has the larger starting cost?", "Plan A"), ("Which plan costs more per visit?", "Plan B"), ("For how many visits do they cost the same?", f"{cross} visits"), ("Which plan is cheaper for more visits than that? Why?", "Plan A, because it adds less per visit")], [f"{a1} > {a2}.", f"{b2} > {b1}.", f"{a1} + {b1}x = {a2} + {b2}x.", "Smaller rate grows more slowly."], tags=["context", "reasoning"])
    def prop_blank():
        a, b = R.randint(2, 12), R.randint(2, 12); v = R.choice("abxyz"); k = R.randrange(5)
        q = [(f"Use the Associative Property of Multiplication to complete: ({a}·{b})·{v} = ____", f"{a}·({b}·{v})"), (f"Use the Commutative Property of Addition to complete: {a}{v} + {b} = ____", f"{b} + {a}{v}"),
             (f"Use the Distributive Property to complete: {a}({v} − {b}) = ____", f"{a}{v} − {a * b}"), (f"Use the Multiplicative Inverse Property to complete: {a} · ____ = 1", f"1/{a}"), (f"Use the Additive Inverse Property to complete: −{a}{v} + ____ = 0", f"{a}{v}")][k]
        B.sa(5, lv(), q[0], q[1], ["Apply the named property exactly."])
    def prop_error():
        a, b = R.randint(2, 9), R.randint(2, 9); v = R.choice("xyn")
        q = R.choice([(f"A student wrote {a}({v} + {b}) = {a}{v} + {b}.", f"Distributive Property: the {a} must multiply both terms", [f"Commutative Property: the order is wrong", "Associative Property: the grouping is wrong", "Nothing is wrong"]),
                      (f"A student wrote {a} − ({v} − {b}) = {a} − {v} − {b}.", f"Distributive Property: the − must distribute to both terms, giving {a} − {v} + {b}", ["Associative Property of Subtraction was used correctly", "Commutative Property of Addition", "Nothing is wrong"]),
                      (f"A student wrote ({a} − {v}) − {b} = {a} − ({v} − {b}).", "Subtraction is not associative; the right side equals " + f"{a} − {v} + {b}", ["Nothing is wrong", "Commutative Property was misused", "The Identity Property was misused"])])
        B.mc(5, R.choice(["cp1", "honors"]), q[0] + " Which explanation identifies the error?", q[1], q[2], ["Check each property's exact form."], tags=["misconception"])
    makers = {4: [ops_int, ops_int, ops_frac, ops_frac, ops_dec, ops_sel, ops_closure, ops_orq], 5: [prop_name, prop_name, prop_sel, prop_steps, prop_mental, prop_counter, prop_blank, prop_error], 7: [ctx_part, ctx_part, ctx_orq, ctx_tax, ctx_equiv, ctx_compare]}
    for s, ms in makers.items(): print(B.unit, s, fillc(B, s, 32, ms, R), file=sys.stderr)
    return B

# =====================================================================================
# Unit 4 · relations-functions: skills 6 (sketch graphs from descriptions), 7 (discrete vs continuous, domain in context)
# =====================================================================================
SEG = {"up": "increases", "up-fast": "increases quickly", "flat": "stays constant", "down": "decreases", "down-fast": "decreases quickly"}
VERB = {"up": "increases", "up-fast": "increases", "flat": "stays the same", "down": "decreases", "down-fast": "decreases"}
def unit_relations():
    B = Bank("relations-functions", "rf", {6: ["F-IF.B.4", "8.F.B.5"], 7: ["F-IF.B.5", "N-Q.A.1"]}, course="algebra", prefix="a1"); R = random.Random(404)
    lv = lambda: lvl(R)
    STORY = {"walk": ("distance from home", {"up": "walks away from home", "up-fast": "jogs away from home", "flat": "stops to rest", "down": "walks back toward home", "down-fast": "runs back toward home"}),
             "tub": ("water in the tub", {"up": "fills slowly", "up-fast": "fills with both taps on", "flat": "sits while someone bathes", "down": "drains slowly", "down-fast": "drains quickly"}),
             "car": ("car's speed", {"up": "speeds up gradually", "up-fast": "accelerates hard", "flat": "cruises at a steady speed", "down": "slows down gradually", "down-fast": "brakes hard"})}
    def path(segs):
        y = [0 if segs[0] in ("up", "up-fast", "flat") else 6]; ys = y[0]; pts = [(0, ys)]
        for s in segs:
            d = {"up": 1.5, "up-fast": 3, "flat": 0, "down": -1.5, "down-fast": -3}[s]; ys += d
            if ys < 0 or ys > 7: raise ValueError
            pts.append((pts[-1][0] + 2, ys))
        return pts
    def good(segs):
        return all(a != b for a, b in zip(segs, segs[1:])) and not all(s == "flat" for s in segs)
    def story_text(ctx, segs):
        q, words = STORY[ctx]; who = {"walk": "Maya", "tub": "The tub", "car": "A driver"}[ctx]
        return f"{who} " + ", then ".join(words[s] for s in segs) + "."
    def mk_story_mc():
        ctx = R.choice(list(STORY)); n = R.randint(3, 4); segs = [R.choice(list(SEG)) for _ in range(n)]
        if not good(segs): raise ValueError
        pts = path(segs)
        d_ = graph(B, f"story-{len(B.qs)}", [(("seg", [p[0] for p in pts], [p[1] for p in pts]), {})], xr=(0, 2 * n), yr=(0, 8), alt=f"Piecewise linear graph of {STORY[ctx][0]} versus time with {n} pieces that " + ", then ".join(SEG[s] for s in segs) + ".", labels=False)
        wrong = []
        for _ in range(30):
            alt = segs[:]; i = R.randrange(n); alt[i] = R.choice([s for s in SEG if s != segs[i]])
            if good(alt) and alt not in wrong:
                try: path(alt); wrong.append(alt)
                except ValueError: pass
            if len(wrong) == 3: break
        if len(wrong) < 3: raise ValueError
        B.mc(6, lv(), f"The graph shows the {STORY[ctx][0]} over time. Which description matches the graph?", story_text(ctx, segs), [story_text(ctx, w) for w in wrong], ["Rising piece: increasing; flat piece: constant; falling piece: decreasing. Steeper means faster."], diagram=d_, tags=["graph", "context"])
    def mk_story_orq():
        ctx = R.choice(list(STORY)); segs = [R.choice(list(SEG)) for _ in range(3)]
        if not good(segs): raise ValueError
        path(segs); q = STORY[ctx][0]
        steep = [i + 1 for i, s in enumerate(segs) if "fast" in s]
        B.orq(6, lv(), "Sketch a graph for this story: " + story_text(ctx, segs) + f" Put time on the horizontal axis and {q} on the vertical axis.", [("Describe the first piece of your graph.", f"it {SEG[segs[0]]}" + (" (steep)" if "fast" in segs[0] else "")), ("Describe the second piece.", f"it {SEG[segs[1]]}" + (" (steep)" if "fast" in segs[1] else "")), ("Describe the third piece.", f"it {SEG[segs[2]]}" + (" (steep)" if "fast" in segs[2] else "")), ("Which piece(s) are steepest?", ", ".join(f"piece {i}" for i in steep) if steep else "none; all slopes are moderate or zero")], ["Translate each phrase into increasing, constant or decreasing.", "Rate of change ↔ steepness.", "Horizontal segments mean no change.", "'Quickly' means a steeper segment."], tags=["context"])
    def mk_story_sel():
        ctx = "walk"; segs = [R.choice(list(SEG)) for _ in range(4)]
        if not good(segs): raise ValueError
        pts = path(segs)
        d_ = graph(B, f"story-{len(B.qs)}", [(("seg", [p[0] for p in pts], [p[1] for p in pts]), {})], xr=(0, 8), yr=(0, 8), alt="Piecewise linear distance-time graph with 4 two-minute pieces that " + ", then ".join(SEG[s] for s in segs) + ".")
        st = {}
        for i, s in enumerate(segs):
            st[f"From t = {2 * i} to t = {2 * i + 2} the distance {VERB[s]}"] = True
        i = R.randrange(4); wrong = R.choice([w for w in ("increases", "decreases", "stays the same") if w != VERB[segs[i]]])
        st[f"From t = {2 * i} to t = {2 * i + 2} the distance {wrong}"] = False
        st[f"The distance at t = 8 is {pts[-1][1] + R.choice([1, 2])}"] = False
        st[f"The distance at t = 8 is {fr(F(pts[-1][1]).limit_denominator())}"] = True
        tr = [k for k, v in st.items() if v]; fl = [k for k, v in st.items() if not v]; tr = R.sample(tr, 3)
        B.sel(6, lv(), "The graph shows Maya's distance from home (in blocks) over 8 minutes. Select ALL true statements.", tr, fl, ["Read each 2-minute piece: rising, flat or falling.", "Read the final height."], diagram=d_, tags=["graph"])
    def mk_shape():
        sc = R.choice([("A ball is dropped from a roof and hits the ground.", "a curve that decreases faster and faster", ["a straight line that decreases steadily", "a curve that increases then decreases", "a horizontal line"]),
                       ("A pot of water is heated until it boils, then keeps boiling.", "increases, then levels off at a constant value", ["increases forever at a constant rate", "decreases, then levels off", "constant, then increases"]),
                       ("A cup of hot cocoa cools on a table.", "decreases quickly at first, then more slowly, leveling off near room temperature", ["decreases at a constant rate to 0", "increases, then decreases", "stays constant"]),
                       ("A plant grows slowly, then quickly, then stops growing at its full height.", "rises slowly, then steeply, then levels off", ["rises steeply, then slowly, then falls", "rises at a constant rate", "levels off, then rises"]),
                       ("The height of a Ferris-wheel seat over two full turns.", "rises and falls in a repeating wave", ["rises steadily", "rises, then stays at the top", "falls, then rises once"]),
                       ("A bank account receives the same deposit every month and nothing is withdrawn.", "a staircase or line that increases by equal steps", ["a curve that decreases", "rises, then falls", "a horizontal line"]),
                       ("A swimmer dives off a board, goes underwater, and floats back to the surface.", "drops below 0, reaches a lowest point, then rises back to 0", ["rises above the board, then lands", "drops to the bottom and stays there", "stays at 0"]),
                       ("Someone climbs stairs at a steady pace, rests on a landing, then climbs again.", "increases, then is constant, then increases", ["increases, then decreases", "constant, then decreases", "increases at one constant rate"])])
        B.mc(6, lv(), f"{sc[0]} Which describes the graph of the quantity (height, temperature, distance or amount) over time?", sc[1], sc[2], ["Match each part of the story to increasing, decreasing or constant behavior, and to fast or slow change."], tags=["context"])
    def mk_ftab():
        r = R.randint(2, 9); c = R.randint(1, 20)
        B.sa(6, lv(), f"A tank starts with {c} liters and is filled at {r} liters per minute for 6 minutes, then left alone for 4 minutes. Give the amount at t = 0, 6 and 10 minutes, and describe the graph.", f"{c}, {c + 6 * r}, {c + 6 * r} L; increasing line from (0, {c}) to (6, {c + 6 * r}), then horizontal to (10, {c + 6 * r})", ["Increase by the rate for 6 minutes.", "No change for 4 minutes: a horizontal piece."], tags=["context"])
    # ---- skill 7 ----
    DISC = [("the number of tickets sold and the money collected", True), ("the number of people in a car and the total weight of passengers' bags", True), ("the number of shirts bought and the total cost", True), ("the number of pizzas ordered and the cost", True),
            ("time spent driving and the distance traveled", False), ("the temperature during a day", False), ("the amount of gas pumped and the cost", False), ("a child's height as she grows", False), ("the water level in a draining tank over time", False), ("the number of books on a shelf and their total thickness", True)]
    def mk_disc_mc():
        s, d = R.choice(DISC); B.mc(7, lv(), f"Is the relationship between {s} best modeled as discrete or continuous?", "discrete" if d else "continuous", ["continuous" if d else "discrete", "neither — it is not a function", "both at once"], ["Counts of whole objects are discrete; measurements such as time, length, volume are continuous."], tags=["context", "concept"])
    def mk_disc_sel():
        pool = R.sample(DISC, 5)
        if sum(d for _, d in pool) < 2 or all(d for _, d in pool): raise ValueError
        B.sel(7, lv(), R.choice(["Select ALL situations that are discrete.", "Select ALL relationships best modeled with separate points (discrete).", "Which situations are discrete? Select ALL that apply.", "Select ALL situations whose input can take only whole-number values."]), [s for s, d in pool if d], [s for s, d in pool if not d], ["Discrete: the input can take only separate values (usually counts)."], tags=["concept"])
    def mk_dom():
        k = R.random()
        if k < 0.5:
            cap, p = R.randint(8, 40), R.randint(2, 15); item = R.choice([("A van holds at most {cap} riders; each pays ${p}.", "riders"), ("A box holds at most {cap} cans; each can weighs {p} oz.", "cans"), ("A teacher buys at most {cap} calculators at ${p} each.", "calculators")])
            txt = item[0].format(cap=cap, p=p)
            B.orq(7, lv(), txt + f" Let n be the number of {item[1]} and f(n) the total.", [("Write f(n).", f"f(n) = {p}n"), ("Is the function discrete or continuous?", "discrete"), ("State the domain.", f"{{0, 1, 2, …, {cap}}}"), ("State the range.", f"{{0, {p}, {2 * p}, …, {p * cap}}}")], ["Rate × count.", "Whole numbers only.", "Whole numbers up to the limit.", "Outputs for each input."], tags=["context"])
        else:
            T, r = R.randint(3, 12), R.randint(20, 70)
            B.orq(7, lv(), f"A car travels at {r} mi/h for up to {T} hours. Let d(t) be the distance after t hours.", [("Write d(t).", f"d(t) = {r}t"), ("Is it discrete or continuous?", "continuous"), ("State the domain.", f"0 ≤ t ≤ {T}"), ("State the range.", f"0 ≤ d ≤ {r * T}")], ["Rate × time.", "Time can be any value.", "All real times in the interval.", "Distances between 0 and the maximum."], tags=["context"])
    def mk_dom_mc():
        cap, p = R.randint(5, 30), R.randint(2, 12)
        B.mc(7, lv(), f"A bakery makes at most {cap} cakes per day and earns ${p} per cake. What is a reasonable domain for the earnings function E(c)?", f"whole numbers 0 to {cap}", [f"all real numbers 0 to {cap}", f"0 to {p * cap}", "all real numbers"], ["You can only sell whole cakes, up to the daily limit."], tags=["context", "misconception"])
    def mk_disc_graph():
        p = R.randint(1, 3); n = R.randint(4, 7); dots = R.random() < 0.5
        if dots: cur = []; pts = [(i, p * i, True, None) for i in range(1, n + 1)]
        else: cur = [(("seg", [0, n], [0, p * n]), {})]; pts = []
        d_ = graph(B, f"disc-{len(B.qs)}", cur, xr=(0, n + 1), yr=(0, p * n + 2), points=pts, alt=(f"Graph of y = {p}x shown as separate dots at x = 1, 2, …, {n}." if dots else f"Graph of y = {p}x for 0 ≤ x ≤ {n} shown as a solid segment."))
        B.orq(7, lv(), "Use the graph.", [("Is the function discrete or continuous?", "discrete" if dots else "continuous"), ("State the domain.", f"{{1, 2, …, {n}}}" if dots else f"0 ≤ x ≤ {n}"), ("State the range.", "{" + ", ".join(str(p * i) for i in range(1, n + 1)) + "}" if dots else f"0 ≤ y ≤ {p * n}"), ("Give a context that fits.", f"{'cost of whole items at $' + str(p) + ' each' if dots else 'distance walked at ' + str(p) + ' mi/h over time'}")], ["Dots vs connected.", "Inputs shown.", "Outputs shown.", "Counts vs measurements."], diagram=d_, tags=["graph"])
    def mk_dom_err():
        cap = R.randint(10, 50)
        B.mc(7, R.choice(["cp1", "honors"]), f"A student says the domain of 'cost of n concert tickets (n ≤ {cap})' is 0 ≤ n ≤ {cap}. What is wrong?", f"n must be a whole number, so the domain is {{0, 1, …, {cap}}}", [f"The domain should be n ≥ {cap}", "The domain should include negative numbers", "Nothing is wrong"], ["A real-number interval allows fractional tickets."], tags=["misconception", "reasoning"])
    makers = {6: [mk_story_mc, mk_story_mc, mk_story_orq, mk_story_sel, mk_shape, mk_ftab], 7: [mk_disc_mc, mk_disc_sel, mk_disc_sel, mk_dom, mk_dom_mc, mk_disc_graph, mk_dom_err]}
    for s, ms in makers.items(): print(B.unit, s, fillc(B, s, 32, ms, R), file=sys.stderr)
    return B

# =====================================================================================
# Unit 5 · linear-equations-slope: skills 4 (graphing in slope-intercept form), 11 (comparing representations)
# =====================================================================================
def line_graph(B, name, m, b, alt, pts=()):
    return graph(B, name, [(lambda x, m=m, b=b: float(m) * x + float(b), {})], xr=(-8, 8), yr=(-8, 8), points=pts, alt=alt)
def unit_linear():
    B = Bank("linear-equations-slope", "ls", {4: ["F-IF.C.7a", "A-REI.D.10"], 11: ["F-IF.C.9", "F-LE.A.2"]}, course="algebra", prefix="a1"); R = random.Random(505)
    lv = lambda: lvl(R)
    def rm(): return R.choice([F(1), F(2), F(3), F(-1), F(-2), F(1, 2), F(-1, 2), F(2, 3), F(-2, 3), F(3, 4), F(-3, 4), F(-3), F(3, 2), F(-4, 3), F(0)])
    def mk_read():
        m, b = rm(), R.randint(-5, 5)
        d_ = line_graph(B, f"line-{len(B.qs)}", m, b, f"Line through (0, {b}) with slope {fr(m)} on a grid.", pts=[(0, b, True, None), (m.denominator, b + m.numerator, True, None)])
        B.mc(4, lv(), "Which equation is graphed?", f"y = {L(m, b)}", [f"y = {L(-m, b)}" if m else f"y = {L(1, b)}", f"y = {L(m, -b)}" if b else f"y = {L(m, 2)}", f"y = {L(1 / m if m else 2, b)}" if m not in (1, -1) else f"y = {L(m, b + 1)}"], ["Read the y-intercept where the line crosses the y-axis.", "Slope = rise/run between grid points."], diagram=d_, tags=["graph", "misconception"])
    def mk_steps():
        m, b = rm(), R.randint(-5, 5)
        if m == 0: raise ValueError
        p1 = (m.denominator, b + m.numerator); p2 = (2 * m.denominator, b + 2 * m.numerator)
        if abs(p2[1]) > 8: p2 = (-m.denominator, b - m.numerator)
        B.orq(4, lv(), f"Graph y = {L(m, b)} by hand.", [("Plot the y-intercept.", pt(0, b)), ("Use the slope to find a second point.", f"{pt(*p1)} (rise {m.numerator}, run {m.denominator})"), ("Find a third point to check.", pt(*p2)), (f"Does the line pass through ({4}, {fr(m * 4 + b)})? Explain.", f"Yes: {fr(m)}·4 + {b} = {fr(m * 4 + b)}")], ["b is the y-intercept.", "From (0, b) move rise/run.", "Repeat the slope step (or go the opposite way).", "Substitute to check."], tags=["reasoning"])
    def mk_onpt():
        m, b = rm(), R.randint(-6, 6); xs = R.sample(range(-6, 7), 5); st = {}
        for i, x in enumerate(xs):
            y = m * x + b
            if i >= 3: y = y + R.choice([1, -1, 2])
            st[pt(x, y)] = i < 3
        tr = [k for k, v in st.items() if v]; fl = [k for k, v in st.items() if not v]
        if len(set(st)) < 5: raise ValueError
        B.sel(4, lv(), f"Select ALL points on the graph of y = {L(m, b)}.", tr, fl, ["Substitute x and check whether the equation gives that y."], tags=["concept"])
    def mk_err():
        m, b = rm(), R.randint(-5, 5)
        if m in (0, 1, -1) or b == 0: raise ValueError
        B.mc(4, lv(), f"A student graphs y = {L(m, b)} by plotting (0, {b}) and moving {m.denominator} up and {abs(m.numerator)} {'right' if m > 0 else 'left'}. What went wrong?", f"The rise and run were switched: move {abs(m.numerator)} {'up' if m > 0 else 'down'} and {m.denominator} right", ["The y-intercept should be on the x-axis", "Nothing; the graph is correct", f"The slope should be {fr(-m)}"], ["Slope = rise/run: numerator vertical, denominator horizontal."], tags=["misconception", "reasoning"])
    def mk_graph_feat():
        m, b = rm(), R.randint(-6, 6)
        if m == 0: raise ValueError
        xi = -F(b) / m
        B.orq(4, lv(), f"Consider the graph of y = {L(m, b)}.", [("Is the line increasing, decreasing, or horizontal?", "increasing" if m > 0 else "decreasing"), ("Find the y-intercept.", pt(0, b)), ("Find the x-intercept.", pt(xi, 0)), ("Which is steeper: this line or y = 2x? Why?", "this line" if abs(m) > 2 else "y = 2x" if abs(m) < 2 else "equally steep")], ["Sign of m.", "x = 0.", "Set y = 0.", "Compare |m|."])
    def mk_transform():
        m, b = rm(), R.randint(-4, 4); k = R.randint(-5, 5)
        if k == 0: raise ValueError
        B.mc(4, lv(), f"How does the graph of y = {L(m, b + k)} compare to the graph of y = {L(m, b)}?", f"It is shifted {abs(k)} units {'up' if k > 0 else 'down'} (parallel line)", [f"It is shifted {abs(k)} units {'right' if k > 0 else 'left'}", "It is steeper", f"It is shifted {abs(k)} units {'down' if k > 0 else 'up'}"], ["Same slope, different y-intercept: vertical translation."], tags=["concept"])
    # ---- skill 11 ----
    def table_txt(m, b, xs): return "x: " + ", ".join(str(x) for x in xs) + " | y: " + ", ".join(fr(m * x + b) for x in xs)
    def mk_cmp():
        m1, b1 = F(R.randint(-5, 6)), R.randint(-8, 10); m2, b2 = rm(), R.randint(-8, 10)
        if m1 == m2 or m1 == 0: raise ValueError
        reps = R.choice(["table-eq", "graph-table", "words-eq"])
        xs = sorted(R.sample(range(-2, 7), 4))
        if reps == "table-eq": A_ = f"Function f is given by the table {table_txt(m1, b1, xs)}."; Btxt = f"Function g is g(x) = {L(m2, b2)}."; d_ = None
        elif reps == "graph-table":
            A_ = f"Function f is given by the table {table_txt(m1, b1, xs)}."; Btxt = "Function g is graphed."; d_ = line_graph(B, f"cmp-{len(B.qs)}", m2, b2, f"Line g with y-intercept {b2} and slope {fr(m2)}.", pts=[(0, b2, True, None), (m2.denominator, b2 + m2.numerator, True, None)])
            if abs(b2) > 7: raise ValueError
        else: A_ = f"Function f: a savings account starts with {b1} dollars and changes by {fr(m1)} dollars each week."; Btxt = f"Function g(x) = {L(m2, b2)}."; d_ = None
        xc = F(b2 - b1) / (m1 - m2)
        parts = [("Which function has the greater rate of change?", "f" if m1 > m2 else "g"), ("Which has the greater initial value (y-intercept)?", "f" if b1 > b2 else "g" if b2 > b1 else "neither (equal)"), ("Find f(10) and g(10).", f"{fr(10 * m1 + b1)} and {fr(10 * m2 + b2)}"), ("For what x are the outputs equal?", f"x = {fr(xc)}")]
        B.orq(11, lv(), f"{A_} {Btxt}", parts, ["Slope from two table rows / the coefficient / the graph.", "Value at x = 0.", "Substitute.", "Set the rules equal."], diagram=d_, tags=["graph"] if d_ else [])
    def mk_cmp_mc():
        m1 = F(R.randint(1, 8)); m2 = rm()
        if m2 == m1: raise ValueError
        xs = [0, 2, 4, 6]; b1 = R.randint(-5, 5)
        hi = "the table" if abs(m1) > abs(m2) else "the equation" if abs(m2) > abs(m1) else "neither"
        if hi == "neither": raise ValueError
        B.mc(11, lv(), f"Which function's graph is steeper: the function in the table {table_txt(m1, b1, xs)}, or y = {L(m2, R.randint(-9, 9))}?", hi, ["the table" if hi != "the table" else "the equation", "they are equally steep", "cannot be determined"], [f"Table slope = {fr(m1)}; equation slope = {fr(m2)}.", "Compare absolute values of the slopes."], tags=["misconception"])
    def mk_cmp_sel():
        m1, b1 = F(R.randint(1, 6)), R.randint(0, 10); m2, b2 = F(R.randint(1, 6)), R.randint(0, 10)
        if m1 == m2 or b1 == b2: raise ValueError
        st = {f"f has rate of change {fr(m1)}": True, f"g has initial value {b2}": True, f"f(0) = {b1}": True, f"f and g have the same rate of change": False, f"g has rate of change {fr(b2)}": b2 == m2}
        xs = [1, 2, 3, 4]
        B.sel(11, lv(), f"f is shown in the table {table_txt(m1, b1, xs)}. g is described in words: 'starts at {b2} and increases by {fr(m2)} each step.' Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Rate from the table: Δy/Δx.", "Initial value: the output at x = 0 (work backward in the table)."], tags=["concept"])
    def mk_cmp_ctx():
        c1, r1 = R.randint(20, 60), R.randint(5, 15); c2, r2 = R.randint(0, 15), R.randint(r1 + 2, r1 + 12)
        n = F(c1 - c2, r2 - r1)
        if n.denominator != 1 or n <= 0: raise ValueError
        xs = [0, 1, 2, 3]
        B.orq(11, lv(), f"Gym A's cost is shown in the table months: 0, 1, 2, 3 | cost: {', '.join(str(c1 + r1 * x) for x in xs)}. Gym B charges a {c2}-dollar fee plus {r2} dollars per month.", [("Write a rule for Gym A.", f"A(m) = {L(r1, c1, 'm')}"), ("Write a rule for Gym B.", f"B(m) = {L(r2, c2, 'm')}"), ("When do they cost the same?", f"after {n} months (${c1 + r1 * n})"), ("Which is cheaper for a year?", "Gym A" if c1 + 12 * r1 < c2 + 12 * r2 else "Gym B")], ["Initial value + rate.", "Fee + rate.", "Set equal.", "Evaluate at m = 12."], tags=["context"])
    def mk_first():
        m1, b1 = F(R.randint(2, 9)), R.randint(0, 20); m2, b2 = F(R.randint(2, 9)), R.randint(0, 20); T = R.randint(40, 120)
        if m1 == m2: raise ValueError
        t1, t2 = (T - b1) / m1, (T - b2) / m2
        if t1 == t2 or t1 < 0 or t2 < 0: raise ValueError
        xs = [0, 1, 2, 3]
        B.mc(11, lv(), f"Plant A's height (cm) after w weeks is given by the table w: 0, 1, 2, 3 | h: {', '.join(fr(m1 * x + b1) for x in xs)}. Plant B starts at {b2} cm and grows {fr(m2)} cm per week. Which plant reaches {T} cm first?", "Plant A" if t1 < t2 else "Plant B", ["Plant B" if t1 < t2 else "Plant A", "They reach it at the same time", "Neither ever reaches it"], [f"A: {b1} + {fr(m1)}w = {T} → w = {fr(t1)}.", f"B: {b2} + {fr(m2)}w = {T} → w = {fr(t2)}."], tags=["context"])
    def mk_int_cmp():
        m1, b1 = rm(), R.randint(-6, 6); m2, b2 = rm(), R.randint(-6, 6)
        if b1 == b2 or abs(b2) > 7: raise ValueError
        d_ = line_graph(B, f"cmp2-{len(B.qs)}", m2, b2, f"Line g with y-intercept {b2} and slope {fr(m2)}.", pts=[(0, b2, True, None)])
        B.mc(11, lv(), f"f(x) = {L(m1, b1)}. Function g is graphed. Which has the greater y-intercept, and by how much?", f"{'f' if b1 > b2 else 'g'}, by {abs(b1 - b2)}", [f"{'g' if b1 > b2 else 'f'}, by {abs(b1 - b2)}", f"{'f' if b1 > b2 else 'g'}, by {abs(b1 + b2) if abs(b1 + b2) != abs(b1 - b2) else abs(b1 - b2) + 1}", "they are equal"], [f"f(0) = {b1}; the graph crosses the y-axis at {b2}."], diagram=d_, tags=["graph"])
    makers = {4: [mk_read, mk_read, mk_steps, mk_onpt, mk_err, mk_graph_feat, mk_transform], 11: [mk_cmp, mk_cmp, mk_cmp_mc, mk_cmp_sel, mk_cmp_ctx, mk_first, mk_int_cmp]}
    for s, ms in makers.items(): print(B.unit, s, fillc(B, s, 32, ms, R), file=sys.stderr)
    return B

# =====================================================================================
# Unit 6 · systems-of-equations: skill 10 (modeling with constraints)
# =====================================================================================
def unit_systems():
    B = Bank("systems-of-equations", "se", {10: ["A-CED.A.3", "A-REI.D.12"]}, course="algebra", prefix="a1"); R = random.Random(606)
    lv = lambda: lvl(R)
    CT = [("A bake sale sells cookies for ${p} and brownies for ${q}. They want at least ${T} and can bake at most {N} items.", "cookies", "brownies"),
          ("A school sells student tickets for ${p} and adult tickets for ${q}. It needs at least ${T}, and the gym holds at most {N} people.", "student tickets", "adult tickets"),
          ("A farmer plants corn earning ${p} per acre and beans earning ${q} per acre on at most {N} acres, and wants at least ${T}.", "acres of corn", "acres of beans"),
          ("A student works x hours tutoring at ${p}/h and y hours at a store at ${q}/h. She can work at most {N} hours and wants at least ${T}.", "tutoring hours", "store hours")]
    def setup():
        t, xn, yn = R.choice(CT); p, q = R.randint(2, 12), R.randint(2, 12); N = R.randint(10, 40); T = R.randint(p * N // 4, max(p, q) * N * 2 // 3)
        if p == q or T <= 0: raise ValueError
        return t.format(p=p, q=q, T=T, N=N), xn, yn, p, q, N, T
    def mk_write():
        txt, xn, yn, p, q, N, T = setup()
        B.orq(10, lv(), txt + f" Let x = {xn} and y = {yn}.", [("Write the money constraint.", f"{p}x + {q}y ≥ {T}"), ("Write the quantity constraint.", f"x + y ≤ {N}"), ("Write the non-negativity constraints.", "x ≥ 0, y ≥ 0"), ("Must x and y be whole numbers here? Explain.", "Yes; you cannot sell part of an item" if "acres" not in xn and "hours" not in xn else "No; fractional acres or hours make sense")], ["Revenue at least the goal.", "Capacity at most N.", "Counts cannot be negative.", "Discrete vs continuous."], tags=["context"])
    def mk_test():
        txt, xn, yn, p, q, N, T = setup(); pts = []
        for _ in range(60):
            x, y = R.randint(0, N), R.randint(0, N)
            ok = p * x + q * y >= T and x + y <= N
            if (x, y) not in [a for a, _ in pts] and (len([1 for _, o in pts if o == ok]) < 3): pts.append(((x, y), ok))
            if len(pts) == 5: break
        if len(pts) < 5 or sum(o for _, o in pts) < 2 or all(o for _, o in pts): raise ValueError
        B.sel(10, lv(), txt + f" Let x = {xn}, y = {yn}. Select ALL combinations (x, y) that meet both constraints.", [pt(*a) for a, o in pts if o], [pt(*a) for a, o in pts if not o], [f"Check {p}x + {q}y ≥ {T} and x + y ≤ {N} for each point."], tags=["context"])
    def mk_graph():
        p, q = R.randint(2, 6), R.randint(2, 6); N = R.randint(6, 12); T = R.randint(p * N // 3, min(p, q) * N)
        if p == q or T <= min(p, q): raise ValueError
        top = max(N, T // min(p, q)) + 2
        d_ = graph(B, f"feas-{len(B.qs)}", [(lambda x: N - x, {}), (lambda x: (T - p * x) / q, {"color": "#555555"})], xr=(0, top), yr=(0, top), alt=f"First-quadrant graph of x + y = {N} (blue, solid) and {p}x + {q}y = {T} (gray, solid); the region on or above the gray line and on or below the solid line is shaded.",
                   shade=lambda X, Y: (X + Y <= N) & (p * X + q * Y >= T) & (X >= 0) & (Y >= 0), step=2 if top > 14 else 1)
        cand = [(x, y) for x in range(0, N + 1) for y in range(0, N + 1) if x + y <= N and p * x + q * y >= T]
        if not cand: raise ValueError
        best = max(cand, key=lambda c: (c[0] + c[1], c[0])); cx = R.choice(cand); bad = (N, N)
        B.orq(10, lv(), f"The shaded region shows the solutions of x + y ≤ {N}, {p}x + {q}y ≥ {T}, x ≥ 0, y ≥ 0.", [("Is the boundary x + y = " + str(N) + " included? How can you tell?", "Yes: solid line and ≤"), (f"Is the boundary {p}x + {q}y = {T} included?", "Yes: solid line and ≥"), ("Name one whole-number solution.", f"for example {pt(*cx)}"), (f"Is {pt(*bad)} a solution? Why?", f"No: {N} + {N} = {2 * N} > {N}")], ["≤/≥ include the line.", "≥ includes the line.", "Any lattice point in the region.", "Test both inequalities."], diagram=d_, tags=["graph", "context"])
    def mk_opt():
        p, q = R.randint(2, 9), R.randint(2, 9); N = R.randint(8, 30); xmax = R.randint(2, N - 2)
        if p == q: raise ValueError
        V = [(0, 0), (xmax, 0), (xmax, N - xmax), (0, N)]; P_ = [p * x + q * y for x, y in V]; i = max(range(4), key=lambda j: P_[j])
        brute = max(p * x + q * y for x in range(0, xmax + 1) for y in range(0, N - x + 1)); assert brute == P_[i]
        B.orq(10, "honors", f"A shop makes x chairs and y stools. It can make at most {N} items per week and at most {xmax} chairs. Profit is ${p} per chair and ${q} per stool.", [("Write the constraints.", f"x + y ≤ {N}, x ≤ {xmax}, x ≥ 0, y ≥ 0"), ("List the vertices of the feasible region.", ", ".join(pt(*v) for v in V)), ("Evaluate the profit at each vertex.", ", ".join(f"{pt(*v)}: ${w}" for v, w in zip(V, P_))), ("Find the maximum profit and the plan.", f"${P_[i]} with {V[i][0]} chairs and {V[i][1]} stools")], ["Translate each limit.", "Intersect boundary lines.", f"P = {p}x + {q}y.", "The maximum of a linear objective occurs at a vertex."], tags=["challenge", "context"])
    def mk_interp():
        p, q = R.randint(3, 15), R.randint(3, 15); T = R.randint(50, 300); x0 = R.randint(1, 10)
        if p == q: raise ValueError
        y0 = F(T - p * x0, q)
        if y0 < 0: raise ValueError
        ylo = math.ceil(y0)
        B.mc(10, lv(), f"A club sells shirts (x) for ${p} and hats (y) for ${q} and needs {p}x + {q}y ≥ {T}. If they sell {x0} shirts, what is the fewest hats they must sell?", str(ylo), [fr(y0) if y0.denominator != 1 else str(ylo + 1), str(max(ylo - 1, 0)), str(math.floor(F(T, q)))], [f"{q}y ≥ {T} − {p * x0} = {T - p * x0}.", f"y ≥ {fr(y0)}, so round UP to a whole number: {ylo}."], tags=["context", "misconception"])
    def mk_viable():
        p, q, N, T = R.randint(2, 8), R.randint(2, 8), R.randint(10, 30), R.randint(30, 150)
        if p == q: raise ValueError
        x, y = F(R.randint(1, 2 * N), 2), F(R.randint(1, 2 * N), 2)
        ok_ineq = p * x + q * y >= T and x + y <= N; ok = ok_ineq and x.denominator == 1 and y.denominator == 1
        B.mc(10, lv(), f"x = number of small boxes, y = number of large boxes; constraints {p}x + {q}y ≥ {T}, x + y ≤ {N}. Is ({fr(x)}, {fr(y)}) a viable option?", "Yes: it satisfies both and uses whole boxes" if ok else ("No: boxes must be whole numbers" if ok_ineq else "No: it fails at least one inequality"), [o for o in ["Yes: it satisfies both and uses whole boxes", "No: boxes must be whole numbers", "No: it fails at least one inequality", "Yes, because any point on the graph is viable"] if o != ("Yes: it satisfies both and uses whole boxes" if ok else ("No: boxes must be whole numbers" if ok_ineq else "No: it fails at least one inequality"))], [f"Check {p}·{fr(x)} + {q}·{fr(y)} = {fr(p * x + q * y)} vs {T} and {fr(x)} + {fr(y)} = {fr(x + y)} vs {N}.", "Viable also means it makes sense in context."], tags=["context", "reasoning"])
    makers = {10: [mk_write, mk_test, mk_graph, mk_opt, mk_interp, mk_viable]}
    for s, ms in makers.items(): print(B.unit, s, fillc(B, s, 32, ms, R), file=sys.stderr)
    return B

# =====================================================================================
# Unit 8 · exponential-functions: skill 8 (comparing linear and exponential models)
# =====================================================================================
def unit_exponential():
    B = Bank("exponential-functions", "ef", {8: ["F-LE.A.1", "F-LE.A.3"]}, course="algebra", prefix="a1"); R = random.Random(808)
    lv = lambda: lvl(R)
    def overtake(a, b, m, c):
        for x in range(0, 200):
            if a * F(b) ** x > m * x + c:
                if x > 0 and all(a * F(b) ** t <= m * t + c for t in range(0, x)) or x == 0: return x
        raise ValueError
    def mk_over():
        a, b = R.randint(1, 5), R.choice([2, 3, F(3, 2)]); m, c = R.randint(5, 40), R.randint(5, 60)
        if a * 1 > c: raise ValueError
        x = overtake(a, b, m, c)
        if x < 2 or x > 25: raise ValueError
        B.orq(8, lv(), f"f(x) = {m}x + {c} and g(x) = {a}({fr(b)})ˣ for whole numbers x ≥ 0.", [("Which is greater at x = 0?", "f"), (f"Find f({x - 1}) and g({x - 1}).", f"{m * (x - 1) + c} and {fr(a * F(b) ** (x - 1))}"), (f"Find f({x}) and g({x}).", f"{m * x + c} and {fr(a * F(b) ** x)}"), ("When does g first exceed f? What happens after?", f"at x = {x}; g stays greater and the gap keeps growing")], ["Compare initial values.", "Evaluate.", "Evaluate.", "Exponential growth eventually exceeds linear growth."], tags=["reasoning"])
    def mk_type():
        k = R.random(); xs = [0, 1, 2, 3, 4]
        if k < 0.5:
            m, c = R.randint(-6, 9), R.randint(1, 30)
            if m == 0: raise ValueError
            ys = [m * x + c for x in xs]; ans = f"linear: constant difference of {m}"; wr = [f"exponential: constant ratio of {fr(F(ys[1], ys[0]))}", "neither", "exponential: constant difference"]
        else:
            a, b = R.randint(2, 20), R.choice([2, 3, F(1, 2), F(3, 2), 4]); ys = [a * F(b) ** x for x in xs]
            if any(y.denominator != 1 for y in ys): raise ValueError
            ans = f"exponential: constant ratio of {fr(b)}"; wr = [f"linear: constant difference of {fr(ys[1] - ys[0])}", "neither", "linear: constant ratio"]
        B.mc(8, lv(), f"Which model fits the table? x: 0, 1, 2, 3, 4 | y: {', '.join(fr(y) for y in ys)}", ans, wr, ["Equal differences over equal intervals → linear.", "Equal ratios over equal intervals → exponential."], tags=["concept"])
    def mk_sel():
        st = {"A linear function grows by equal differences over equal intervals": True, "An exponential function grows by equal factors over equal intervals": True, "An increasing exponential function eventually exceeds any increasing linear function": True,
              "A linear function always stays above an exponential function": False, "An exponential function has a constant rate of change": False, "A quantity growing 5% per year is linear": False, "A quantity growing $5 per year is linear": True}
        ks = R.sample(list(st), 5)
        if sum(st[k] for k in ks) < 2 or all(st[k] for k in ks): raise ValueError
        B.sel(8, lv(), "Select ALL true statements about linear and exponential models" + R.choice(["", " (equal intervals)", " over time", " in context"]) + ".", [k for k in ks if st[k]], [k for k in ks if not st[k]], ["Linear: add a constant. Exponential: multiply by a constant."], tags=["concept"])
    def mk_ctx():
        P0 = R.choice([500, 1000, 2000, 5000]); r = R.choice([3, 4, 5, 6, 8, 10]); d = R.randint(20, 300); n = R.randint(5, 30)
        A = P0 + d * n; Bv = P0 * (1 + r / 100) ** n
        better = "Option A (linear)" if A > Bv else "Option B (exponential)"
        B.orq(8, lv(), f"You invest ${P0}. Option A adds ${d} per year. Option B grows {r}% per year.", [("Write a model for A.", f"A(t) = {P0} + {d}t"), ("Write a model for B.", f"B(t) = {P0}({1 + r / 100:g})ᵗ"), (f"Find both values after {n} years (nearest dollar).", f"A = ${A:,}; B ≈ ${round(Bv):,}"), (f"Which is better after {n} years? Which grows faster in the long run?", f"{better}; Option B (exponential)")], ["Linear: start + rate·t.", "Exponential: start·(1 + r)ᵗ.", "Evaluate.", "Exponential growth eventually wins."], tags=["context"])
    def mk_ctx_mc():
        c = R.choice([("A town's population increases by 250 people each year.", "linear"), ("A town's population increases by 3% each year.", "exponential"), ("A car loses $1,800 of value each year.", "linear"), ("A car loses 15% of its value each year.", "exponential"),
                      ("A bacteria culture doubles every hour.", "exponential"), ("A pool drains 40 gallons per minute.", "linear"), ("Each year a salary rises by 2%.", "exponential"), ("Each year a salary rises by $2,000.", "linear"), ("A medicine dose halves in the bloodstream every 6 hours.", "exponential"), ("A plant grows 1.5 cm per week.", "linear")])
        B.mc(8, lv(), f"{c[0]} Which model fits?", c[1], ["exponential" if c[1] == "linear" else "linear", "quadratic", "neither"], ["Constant amount → linear; constant percent/factor → exponential."], tags=["context"])
    def mk_interval():
        a, b = R.randint(2, 10), R.choice([2, 3]); m = R.randint(2, 10); x1, x2 = sorted(R.sample(range(0, 7), 2))
        avg_l = m; avg_e = F(a * b ** x2 - a * b ** x1, x2 - x1)
        B.sa(8, R.choice(["cp1", "honors"]), f"Find the average rate of change of f(x) = {m}x + 1 and g(x) = {a}·{b}ˣ on {x1} ≤ x ≤ {x2}. Which is greater?", f"f: {avg_l}; g: {fr(avg_e)}; {'g' if avg_e > avg_l else 'f' if avg_l > avg_e else 'equal'}", ["(f(x₂) − f(x₁))/(x₂ − x₁).", "The linear rate is constant; the exponential rate grows."])
    makers = {8: [mk_over, mk_over, mk_type, mk_sel, mk_ctx, mk_ctx_mc, mk_interval]}
    for s, ms in makers.items(): print(B.unit, s, fillc(B, s, 32, ms, R), file=sys.stderr)
    return B

# =====================================================================================
# Unit 11 · quadratics: skills 4 (factored form / connecting forms), 5 (solving by graphing), 12 (comparing models)
# =====================================================================================
def unit_quadratics():
    B = Bank("quadratics", "qd", {4: ["A-SSE.B.3", "F-IF.C.8a"], 5: ["A-REI.D.11", "F-IF.C.7a"], 12: ["F-LE.A.1", "F-LE.A.3"]}, course="algebra", prefix="a1"); R = random.Random(1111)
    lv = lambda: lvl(R)
    def fac(a, r1, r2):
        def f1(r): return "x" if r == 0 else f"(x {'-' if r > 0 else '+'} {abs(r)})"
        co = "" if a == 1 else "-" if a == -1 else str(a)
        return f"{co}{f1(r1)}{f1(r2)}" if r1 != r2 else f"{co}{f1(r1)}²"
    def vform(a, h, k):
        co = "" if a == 1 else "-" if a == -1 else fr(a); inner = "x" if h == 0 else f"(x {'-' if h > 0 else '+'} {abs(h)})"
        return f"{co}{inner}²" + ("" if k == 0 else f" {'+' if k > 0 else '-'} {fr(abs(k))}")
    def mk_f2s():
        a = R.choice([1, 1, 2, -1, 3, -2]); r1, r2 = R.randint(-8, 8), R.randint(-8, 8); p = P.roots([r1, r2], a)
        h = F(r1 + r2, 2); k = sum(c * h ** i for i, c in enumerate(p.c))
        B.orq(4, lv(), f"f(x) = {fac(a, r1, r2)}.", [("Find the zeros.", f"x = {r1} and x = {r2}" if r1 != r2 else f"x = {r1} (double zero)"), ("Find the axis of symmetry.", f"x = {fr(h)}"), ("Find the vertex.", pt(h, k)), ("Write f in standard form and in vertex form.", f"y = {pstr(p)}; y = {vform(a, h, k)}")], ["Zero Product Property.", "Midpoint of the zeros.", "Evaluate f at the axis.", "Multiply out; use a, h, k."], tags=["reasoning"])
    def mk_s2f():
        a = R.choice([1, 1, 1, 2, -1]); r1, r2 = R.randint(-9, 9), R.randint(-9, 9)
        if r1 == r2: raise ValueError
        p = P.roots([r1, r2], a)
        B.mc(4, lv(), f"Which is the factored form of y = {pstr(p)}?", f"y = {fac(a, r1, r2)}", [f"y = {fac(a, -r1, -r2)}", f"y = {fac(a, r1, -r2)}" if r2 != 0 else f"y = {fac(a, r1, r2 + 1)}", f"y = {fac(-a, r1, r2)}"], ["Find two numbers with the right product and sum; factor out a first.", "Check by multiplying."], tags=["misconception"])
    def mk_v2s():
        a = R.choice([1, -1, 2, -2, F(1, 2)]); h, k = R.randint(-6, 6), R.randint(-9, 9)
        p = P([a * h * h + k, -2 * a * h, a])
        B.sa(4, lv(), f"Write y = {vform(a, h, k)} in standard form.", f"y = {pstr(p)}", [f"Expand (x {'-' if h >= 0 else '+'} {abs(h)})² and multiply by {fr(a)}.", f"Add {k}."])
    def mk_equiv_sel():
        a = R.choice([1, 2, -1]); r1, r2 = R.randint(-7, 7), R.randint(-7, 7)
        if r1 == r2: raise ValueError
        p = P.roots([r1, r2], a); h = F(r1 + r2, 2); k = sum(c * h ** i for i, c in enumerate(p.c))
        q = P.roots([-r1, r2], a); wrong2 = P([p.c[0] + 1, p.c[1], p.c[2]])
        B.sel(4, lv(), f"Select ALL expressions equivalent to {pstr(p)}.", [fac(a, r1, r2), vform(a, h, k), pstr(p)], [fac(a, -r1, r2) if r1 != 0 else fac(a, r1 + 1, r2), vform(a, -h, k) if h != 0 else vform(a, h, k + 1), pstr(wrong2)], ["Expand each candidate (or compare zeros and vertex)."], tags=["concept"])
    def mk_which_form():
        q = R.choice([("the zeros", "factored form"), ("the vertex", "vertex form"), ("the y-intercept", "standard form"), ("the maximum or minimum value", "vertex form"), ("the x-intercepts", "factored form")])
        B.mc(4, lv(), f"Which form of a quadratic shows {q[0]} most directly?", q[1], [f for f in ["factored form", "vertex form", "standard form", "slope-intercept form"] if f != q[1]], ["Factored: a(x − r)(x − s). Vertex: a(x − h)² + k. Standard: ax² + bx + c (c is the y-intercept)."], tags=["concept"])
    # ---- skill 5 ----
    def para_graph(name, a, h, k, alt, hl=None):
        m = 8; cur = [(lambda x, a=a, h=h, k=k: float(a) * (x - h) ** 2 + float(k), {})]
        if hl is not None: cur.append((lambda x, hl=hl: hl + 0 * x, {"ls": "--", "color": "#444444"}))
        return graph(B, name, cur, xr=(-m, m), yr=(-m, m), alt=alt)
    def mk_read_zeros():
        a = R.choice([1, -1, F(1, 2), F(-1, 2)]); r1, r2 = sorted(R.sample(range(-6, 7), 2))
        h = F(r1 + r2, 2); k = a * (h - r1) * (h - r2)
        if abs(k) > 7.5: raise ValueError
        d_ = para_graph(f"pz-{len(B.qs)}", a, h, k, f"Parabola with x-intercepts at {r1} and {r2} and vertex {pt(h, k)}.")
        p = P.roots([r1, r2], a)
        B.orq(5, lv(), f"The graph shows y = {pstr(p)}.", [("Read the solutions of " + pstr(p) + " = 0 from the graph.", f"x = {r1} and x = {r2}"), ("Check one solution by substitution.", f"f({r1}) = 0"), ("How many real solutions are there? How can you tell?", "2: the graph crosses the x-axis twice"), ("Read the vertex.", pt(h, k))], ["Zeros are x-intercepts.", "Substitute.", "Count x-intercepts.", "Turning point."], diagram=d_, tags=["graph"])
    def mk_count():
        a = R.choice([1, -1]); h = R.randint(-4, 4); k = R.choice([-5, -3, -1, 0, 1, 3, 5])
        n = 2 if (a > 0 and k < 0) or (a < 0 and k > 0) else 1 if k == 0 else 0
        d_ = para_graph(f"pc-{len(B.qs)}", a, h, k, f"Parabola opening {'up' if a > 0 else 'down'} with vertex {pt(h, k)}.")
        B.mc(5, lv(), "How many real solutions does f(x) = 0 have for the graphed function?", str(n), [str(v) for v in (0, 1, 2, 3) if v != n], ["Count where the graph meets the x-axis."], diagram=d_, tags=["graph"])
    def mk_hline():
        a = 1; h = R.randint(-3, 3); k = R.randint(-6, -1); c = R.randint(k + 1, 6)
        d = c - k; s = math.isqrt(d)
        if s * s != d: raise ValueError
        d_ = para_graph(f"ph-{len(B.qs)}", a, h, k, f"Parabola y = {vform(1, h, k)} and dashed horizontal line y = {c}.", hl=c)
        B.sa(5, lv(), f"Use the graph to solve {vform(1, h, k)} = {c}.", f"x = {h - s} or x = {h + s}", ["Find where the parabola meets the line y = " + str(c) + ".", f"Check: ({h + s} − {h})² + ({k}) = {c}."], diagram=d_, tags=["graph"])
    def mk_approx():
        a = 1; h = R.randint(-3, 3); k = -R.choice([2, 3, 5, 6, 7, 8]); s = math.sqrt(-k)
        lo1, lo2 = math.floor(h - s), math.floor(h + s)
        d_ = para_graph(f"pa-{len(B.qs)}", a, h, k, f"Parabola with vertex {pt(h, k)} crossing the x-axis between grid lines.")
        p = P([h * h + k, -2 * h, 1])
        B.orq(5, "honors", f"The graph shows y = {pstr(p)}.", [("Between which consecutive integers is each zero?", f"{lo1} and {lo1 + 1}; {lo2} and {lo2 + 1}"), ("Estimate the zeros to the nearest tenth.", f"x ≈ {h - s:.1f} and x ≈ {h + s:.1f}"), ("Give the exact zeros.", f"x = {h} ± √{-k}"), ("Why can a graph give only an estimate here?", "The zeros are irrational, so they fall between grid lines")], ["Sign change.", "Zoom/table.", "Square roots.", "Irrational values."], diagram=d_, tags=["graph", "challenge"])
    def mk_graph_sel():
        a = R.choice([1, -1]); r1, r2 = sorted(R.sample(range(-5, 6), 2)); p = P.roots([r1, r2], a); h = F(r1 + r2, 2); k = a * (h - r1) * (h - r2)
        if abs(k) > 7.5: raise ValueError
        d_ = para_graph(f"ps-{len(B.qs)}", a, h, k, f"Parabola through ({r1}, 0) and ({r2}, 0) with vertex {pt(h, k)}.")
        st = {f"x = {r1} is a solution of f(x) = 0": True, f"x = {r2} is a solution of f(x) = 0": True, f"x = {r1 + r2} is a solution": (r1 + r2) in (r1, r2), f"f(x) = {fr(k)} has exactly one solution": True, f"f(x) = {fr(k + (1 if a > 0 else -1))} has no solutions": False}
        B.sel(5, lv(), "Select ALL true statements about the graphed function f.", [s for s, v in st.items() if v], [s for s, v in st.items() if not v], ["x-intercepts are solutions of f(x) = 0.", "A horizontal line through the vertex meets the graph once; beyond the vertex (inside the opening) it meets twice."], diagram=d_, tags=["graph"])
    # ---- skill 12 ----
    def mk_tbl_type():
        xs = [0, 1, 2, 3, 4]; k = R.choice(["lin", "exp", "quad"])
        if k == "lin": m, c = R.randint(-5, 8), R.randint(-5, 10); ys = [m * x + c for x in xs]; ans = "linear"
        elif k == "exp": a, b = R.randint(1, 6), R.choice([2, 3]); ys = [a * b ** x for x in xs]; ans = "exponential"
        else: a, b_, c = R.choice([1, 2, -1, 3]), R.randint(-4, 4), R.randint(-5, 5); ys = [a * x * x + b_ * x + c for x in xs]; ans = "quadratic"
        d1 = [ys[i + 1] - ys[i] for i in range(4)]; d2 = [d1[i + 1] - d1[i] for i in range(3)]
        if k == "lin" and d1[0] == 0: raise ValueError
        B.orq(12, lv(), f"x: 0, 1, 2, 3, 4 | y: {', '.join(str(y) for y in ys)}", [("Find the first differences.", ", ".join(str(d) for d in d1)), ("Find the second differences.", ", ".join(str(d) for d in d2)), ("Find the ratios of consecutive y-values (when defined).", ", ".join(fr(F(ys[i + 1], ys[i])) for i in range(4)) if all(ys[i] for i in range(4)) else "not all defined (a y-value is 0)"), ("Which model fits: linear, quadratic or exponential?", ans)], ["Δy.", "Δ(Δy).", "y₂/y₁.", "Constant first differences → linear; constant second differences → quadratic; constant ratios → exponential."], tags=["reasoning"])
    def mk_tbl_mc():
        xs = [0, 1, 2, 3, 4]; k = R.choice(["lin", "exp", "quad"])
        if k == "lin": m, c = R.randint(1, 8), R.randint(0, 10); ys = [m * x + c for x in xs]
        elif k == "exp": a, b = R.randint(1, 6), R.choice([2, 3]); ys = [a * b ** x for x in xs]
        else: a, c = R.choice([1, 2, 3]), R.randint(0, 5); ys = [a * x * x + c for x in xs]
        ans = {"lin": "linear", "exp": "exponential", "quad": "quadratic"}[k]
        B.mc(12, lv(), f"Which type of function best fits x: 0, 1, 2, 3, 4 | y: {', '.join(str(y) for y in ys)}?", ans, [t for t in ("linear", "exponential", "quadratic", "absolute value") if t != ans], ["Check first differences, second differences and ratios."], tags=["concept"])
    def mk_eventual():
        m, c = R.randint(10, 100), R.randint(0, 50); a = R.choice([1, 2]); b = R.choice([2, 3])
        f = lambda x: m * x + c; g = lambda x: a * x * x; h = lambda x: b ** x
        X = next(x for x in range(1, 100) if h(x) > g(x) and h(x) > f(x) and all(h(t) > g(t) and h(t) > f(t) for t in range(x, x + 30)))
        B.orq(12, lv(), f"Compare f(x) = {m}x + {c}, g(x) = {fac(a, 0, 0)}, and h(x) = {b}ˣ for x ≥ 0.", [("Which is greatest at x = 1?", max([("f", f(1)), ("g", g(1)), ("h", h(1))], key=lambda t: t[1])[0]), (f"Evaluate all three at x = {X}.", f"f = {f(X)}, g = {g(X)}, h = {h(X)}"), ("Which grows fastest for large x?", "h (exponential)"), ("Order their growth rates for large x.", "exponential > quadratic > linear")], ["Evaluate.", "Evaluate.", "Exponential eventually dominates.", "Exponential, then quadratic, then linear."], tags=["reasoning"])
    def mk_cmp_sel():
        st = {"An increasing exponential function eventually exceeds any quadratic function": True, "A quadratic with a > 0 eventually exceeds any linear function": True, "A linear function has constant first differences": True, "A quadratic function has constant second differences": True,
              "A quadratic function has constant ratios": False, "An exponential function has constant second differences": False, "A linear function eventually exceeds an increasing exponential function": False}
        ks = R.sample(list(st), 5)
        if sum(st[k] for k in ks) < 2 or all(st[k] for k in ks): raise ValueError
        B.sel(12, lv(), "Select ALL true statements" + R.choice(["", " about growth", " about function families", " comparing models"]) + ".", [k for k in ks if st[k]], [k for k in ks if not st[k]], ["Patterns in tables identify the family; exponential growth eventually dominates."], tags=["concept"])
    def mk_ctx_q():
        c = R.choice([("The height of a thrown ball over time", "quadratic"), ("The area of a square as its side length grows", "quadratic"), ("Money in an account earning 4% per year", "exponential"), ("Cost of apples at $2 per pound", "linear"),
                      ("The number of handshakes when everyone in a group shakes hands once", "quadratic"), ("A virus spreading so cases triple each week", "exponential"), ("Distance traveled at a constant 55 mph", "linear"), ("The stopping distance of a car versus its speed", "quadratic")])
        B.mc(12, lv(), f"{c[0]}: which model is most appropriate?", c[1], [t for t in ("linear", "exponential", "quadratic") if t != c[1]] + ["constant"], ["Constant rate → linear; constant factor → exponential; area, falling objects, pairs → quadratic."], tags=["context"])
    makers = {4: [mk_f2s, mk_f2s, mk_s2f, mk_v2s, mk_equiv_sel, mk_which_form], 5: [mk_read_zeros, mk_read_zeros, mk_count, mk_hline, mk_approx, mk_graph_sel], 12: [mk_tbl_type, mk_tbl_mc, mk_eventual, mk_cmp_sel, mk_ctx_q]}
    for s, ms in makers.items(): print(B.unit, s, fillc(B, s, 32, ms, R), file=sys.stderr)
    return B

if __name__ == "__main__":
    for fn in (unit_foundations, unit_relations, unit_linear, unit_systems, unit_exponential, unit_quadratics):
        B = fn(); p = B.write(); print(p, len(B.qs))
        for k, v in B.counts().items(): print(" ", k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
