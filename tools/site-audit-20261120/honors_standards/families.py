"""Question families for whole-site audit 2, item #7 (2026-11-20): practice for honors-only standards
that had no items in the Precalculus and Algebra 2 banks.

A family is fn(r, L) -> dict(prompt, answer, steps, wrongs, check, fam) with L = 0 Support, 1 Standard, 2 Advanced.
`wrongs` is a list of (text, why) pairs. `check` holds only the parameters; verify.py recomputes the answer,
every option and every student answer from them with its own formulas and confirms that each check["show"]
string is printed in the prompt.
"""
from fractions import Fraction as F


class Reject(Exception):
    pass


def need(ok):
    if not ok:
        raise Reject()


def fr(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def dec(v):
    """Exact terminating decimal text for a Fraction (denominators of the form 2^a 5^b only)."""
    v = F(v)
    d = v.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    need(d == 1)
    s = f"{float(v):.6f}".rstrip("0").rstrip(".")
    need(F(s) == v)
    return s


def item(prompt, answer, steps, wrongs, check, fam):
    seen, ws = {answer}, []
    for t, why in wrongs:
        if t is not None and t not in seen:
            seen.add(t)
            ws.append((t, why))
    return dict(prompt=prompt, answer=answer, steps=steps, wrongs=ws, check=check, fam=fam)


NAMES = ["Ava", "Ben", "Chloe", "Diego", "Emma", "Farah", "Gabe", "Hana", "Isaac", "Jada", "Kenji", "Leah", "Mateo", "Nia", "Omar", "Priya"]


# ------------------------------------------------------------------ N-CN.C.8 polynomial identities over the complex numbers
def cn_factor(r, L):
    if L == 0 or (L == 1 and r.random() < 0.4):
        n = r.randint(2, 12)
        poly = f"x² + {n * n}"
        ans = f"(x + {n}i)(x - {n}i)"
        return item(f"Factor {poly} completely over the complex numbers.", ans,
                    [f"Use x² + b² = (x + bi)(x - bi), because (bi)² = -b².", f"{n * n} = {n}², so b = {n}.", f"{poly} = {ans}."],
                    [(f"(x + {n})(x - {n})", f"used real factors, but (x + {n})(x - {n}) = x² - {n * n}"),
                     (f"(x + {n * n}i)(x - {n * n}i)", f"used {n * n} instead of its square root {n}"),
                     (f"(x + {n}i)²", "squared one factor; that product has a middle term"),
                     (f"(x - {n}i)²", "squared one factor; that product has a middle term")],
                    dict(k="cn_factor", c=[1, 0, n * n], show=[poly]), "cn_sum_squares")
    a = r.choice([v for v in range(-6, 7) if v != 0])
    b = r.randint(1, 6 if L == 1 else 9)
    lead = 1 if L == 1 else r.choice([1, 1, 2, 3])
    B, C = -2 * a * lead, (a * a + b * b) * lead
    poly = ("" if lead == 1 else str(lead)) + "x² " + ("- " if B < 0 else "+ ") + f"{abs(B)}x + {C}"
    zp, zm = f"{a} + {b}i".replace("+ 1i", "+ i"), f"{a} - {b}i".replace("- 1i", "- i")
    ans = ("" if lead == 1 else str(lead)) + f"(x - ({zp}))(x - ({zm}))"
    return item(f"Write {poly} as a product of linear factors with complex coefficients.", ans,
                [("Factor out the leading coefficient. " if lead > 1 else "") + "Find the zeros with the quadratic formula (or by completing the square).",
                 f"x = {a} ± {b}i" if b > 1 else f"x = {a} ± i",
                 f"Each zero z gives a factor (x - z): {poly} = {ans}."],
                [(("" if lead == 1 else str(lead)) + f"(x + ({zp}))(x + ({zm}))", "used the zeros' opposites in the factors"),
                 (("" if lead == 1 else str(lead)) + f"(x - ({a} + {b * b}i))(x - ({a} - {b * b}i))".replace("+ 1i", "+ i").replace("- 1i", "- i"), f"used b² = {b * b} in place of b = {b}"),
                 (f"(x - ({zp}))(x - ({zm}))" if lead > 1 else f"(x - ({-a} + {b}i))(x - ({-a} - {b}i))".replace("+ 1i", "+ i").replace("- 1i", "- i"),
                  "left out the leading coefficient" if lead > 1 else "took the wrong sign for the real part of the zeros")],
                dict(k="cn_factor", c=[lead, B, C], show=[poly]), "cn_conjugate_factors")


# ------------------------------------------------------------------ N-VM.C.9 properties of matrix multiplication
def mtxt(M):
    return "[" + "; ".join(", ".join(str(v) for v in row) for row in M) + "]"


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]


def rnd(r, lo=-5, hi=6):
    return [[r.randint(lo, hi) for _ in range(2)] for _ in range(2)]


ORD = {1: "1", 2: "2"}


def vm_props(r, L):
    i, j = r.randint(1, 2), r.randint(1, 2)
    A, B = rnd(r), rnd(r)
    AB, BA = mul(A, B), mul(B, A)
    if L == 0 or (L == 1 and r.random() < 0.5):
        v = AB[i - 1][j - 1] - BA[i - 1][j - 1]
        need(v != 0)
        return item(f"A = {mtxt(A)} and B = {mtxt(B)}. Find the entry in row {i}, column {j} of AB - BA.", str(v),
                    [f"Row {i} of A times column {j} of B: (AB) entry = {AB[i - 1][j - 1]}.", f"Row {i} of B times column {j} of A: (BA) entry = {BA[i - 1][j - 1]}.",
                     f"AB - BA has entry {AB[i - 1][j - 1]} - ({BA[i - 1][j - 1]}) = {v}. It is not 0, so AB ≠ BA: matrix multiplication is not commutative."],
                    [(str(-v), "found BA - AB instead"), ("0", "assumed AB = BA; matrix multiplication is not commutative"),
                     (str(AB[i - 1][j - 1]), "found the entry of AB only"), (str(BA[i - 1][j - 1]), "found the entry of BA only")],
                    dict(k="vm_comm", A=A, B=B, i=i, j=j, show=[mtxt(A), mtxt(B)]), "vm_commutator")
    Cm = rnd(r)
    if L == 1:
        S = mul(A, add(B, Cm))
        v = S[i - 1][j - 1]
        wrong1 = mul(A, B)[i - 1][j - 1] + Cm[i - 1][j - 1]
        wrong2 = mul(add(B, Cm), A)[i - 1][j - 1]
        return item(f"A = {mtxt(A)}, B = {mtxt(B)} and C = {mtxt(Cm)}. Use the distributive property, A(B + C) = AB + AC, to find the entry in row {i}, column {j} of A(B + C).",
                    str(v),
                    [f"(AB) entry = {mul(A, B)[i - 1][j - 1]} and (AC) entry = {mul(A, Cm)[i - 1][j - 1]}.", f"A(B + C) = AB + AC, so the entry is {mul(A, B)[i - 1][j - 1]} + {mul(A, Cm)[i - 1][j - 1]} = {v}."],
                    [(str(wrong1), "multiplied A by B but just added C"), (str(wrong2), "multiplied in the order (B + C)A; order matters"),
                     (str(v + 1), "made an arithmetic slip"), (str(v - 1), "made an arithmetic slip")],
                    dict(k="vm_dist", A=A, B=B, C=Cm, i=i, j=j, show=[mtxt(A), mtxt(B), mtxt(Cm)]), "vm_distributive")
    A, B, Cm = rnd(r, -3, 4), rnd(r, -3, 4), rnd(r, -3, 4)
    P = mul(mul(A, B), Cm)
    v = P[i - 1][j - 1]
    return item(f"A = {mtxt(A)}, B = {mtxt(B)} and C = {mtxt(Cm)}. Matrix multiplication is associative, so (AB)C = A(BC). Find the entry in row {i}, column {j} of ABC.",
                str(v),
                [f"AB = {mtxt(mul(A, B))}.", f"(AB)C = {mtxt(P)}.", f"Check with A(BC): BC = {mtxt(mul(B, Cm))} and A(BC) = {mtxt(mul(A, mul(B, Cm)))}, the same matrix.", f"The entry is {v}."],
                [(str(mul(mul(B, A), Cm)[i - 1][j - 1]), "multiplied in the order BAC; order matters"),
                 (str(mul(Cm, mul(A, B))[i - 1][j - 1]), "multiplied in the order CAB; order matters"),
                 (str(A[i - 1][j - 1] * B[i - 1][j - 1] * Cm[i - 1][j - 1]), "multiplied matching entries instead of rows by columns"),
                 (str(v + 2), "made an arithmetic slip")],
                dict(k="vm_assoc", A=A, B=B, C=Cm, i=i, j=j, show=[mtxt(A), mtxt(B), mtxt(Cm)]), "vm_associative")


# ------------------------------------------------------------------ F-TF.A.4 symmetry and periodicity on the unit circle
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
QUAD = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}
TRANS = {0: ["-θ"], 1: ["-θ", "θ + 2π", "θ - 2π", "θ + π"], 2: ["-θ", "θ + π", "π - θ", "θ + 2π", "θ - π"]}


def tf_symmetry(r, L):
    a, b, c = r.choice(TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    q = 1 if L == 0 else r.randint(1, 4)
    cx, sy = QUAD[q][0] * b, QUAD[q][1] * a  # cos θ = cx/c, sin θ = sy/c
    fn = r.choice(["sin", "cos", "tan"] if L else ["sin", "cos"])
    tr = r.choice(TRANS[L])
    val = {"sin": F(sy, c), "cos": F(cx, c), "tan": F(sy, cx)}
    # values after the transformation, from the unit-circle point (cos, sin)
    pt = {"-θ": (cx, -sy), "θ + 2π": (cx, sy), "θ - 2π": (cx, sy), "θ + π": (-cx, -sy), "θ - π": (-cx, -sy), "π - θ": (-cx, sy)}[tr]
    out = {"sin": F(pt[1], c), "cos": F(pt[0], c), "tan": F(pt[1], pt[0])}[fn]
    why = {"-θ": "The point for -θ is the reflection of (cos θ, sin θ) across the x-axis: (cos θ, -sin θ). So cosine is even and sine and tangent are odd.",
           "θ + 2π": "Adding 2π makes one full turn, so θ + 2π ends at the same point: every trig function has period 2π.",
           "θ - 2π": "Subtracting 2π makes one full turn back, so θ - 2π ends at the same point: every trig function has period 2π.",
           "θ + π": "Adding π makes a half turn, so the point is reflected through the origin: (-cos θ, -sin θ). Tangent keeps its value (period π).",
           "θ - π": "Subtracting π makes a half turn, so the point is reflected through the origin: (-cos θ, -sin θ). Tangent keeps its value (period π).",
           "π - θ": "The point for π - θ is the reflection of (cos θ, sin θ) across the y-axis: (-cos θ, sin θ)."}[tr]
    qn = ["", "I", "II", "III", "IV"][q]
    given = f"sin θ = {fr(F(sy, c))} and cos θ = {fr(F(cx, c))}"
    expr = f"{fn}({tr})"
    return item(f"An angle θ in Quadrant {qn} has {given}. Use the unit circle to find {expr}.", fr(out),
                [f"θ ends at the point ({fr(F(cx, c))}, {fr(F(sy, c))}) on the unit circle.", why, f"{expr} = {fr(out)}."],
                [(fr(-out), "used the wrong sign for the reflected point"), (fr(val[fn]) if val[fn] != out else fr(-out), "assumed the value does not change"),
                 (fr(1 / out), "took the reciprocal"), (fr({"sin": F(pt[0], c), "cos": F(pt[1], c), "tan": F(pt[0], pt[1])}[fn]), "switched the x- and y-coordinates")],
                dict(k="tf_sym", fn=fn, tr=tr, cos=fr(F(cx, c)), sin=fr(F(sy, c)), show=[given, expr]), "tf_symmetry")


# ------------------------------------------------------------------ S-MD.A.2 expected value from theoretical probabilities
def md_theory(r, L):
    kind = r.choice(["coins", "die", "draws"] if L else ["coins", "die"])
    if kind == "coins":
        n = r.randint(2, 6 if L < 2 else 12)
        ev = F(n, 2)
        return item(f"X is the number of heads when {n} fair coins are tossed. Find the expected value E(X).", fr(ev),
                    ["Each coin lands heads with probability 1/2.", f"For a binomial random variable, E(X) = np = {n} · 1/2.", f"E(X) = {fr(ev)}."],
                    [(fr(F(1, 2)), "gave the probability of heads for one coin"), (str(n), "counted every toss as heads"), (fr(F(n, 4)), "used probability 1/4"),
                     (fr(F(n + 1, 2)), "averaged the values 1 to " + str(n))],
                    dict(k="md_coins", n=n, show=[f"{n} fair coins"]), "md_coins")
    if kind == "die":
        n = r.choice([4, 6, 8, 10, 12, 20])
        ev = F(n + 1, 2)
        return item(f"X is the number showing when a fair {n}-sided die (faces 1 to {n}) is rolled. Find the expected value E(X).", dec(ev),
                    [f"Each face has probability 1/{n}.", f"E(X) = (1 + 2 + … + {n})/{n} = ({n}·{n + 1}/2)/{n}.", f"E(X) = {dec(ev)}."],
                    [(dec(F(n, 2)), f"divided {n} by 2"), (str(n), "used the largest face"), (dec(F(n + 1, 2) + 1), "made an arithmetic slip"),
                     (dec(F(n * (n + 1), 2)), "added the faces but did not divide")],
                    dict(k="md_die", n=n, show=[f"fair {n}-sided die"]), "md_die")
    red, blue, n = r.randint(1, 6), r.randint(1, 8), r.randint(2, 10)
    need(red != blue)
    ev = F(n * red, red + blue)
    return item(f"A bag holds {red} red and {blue} blue marbles. A marble is drawn, its color is recorded, and it is put back; this is done {n} times. X is the number of red marbles recorded. Find E(X).",
                fr(ev),
                [f"P(red) = {red}/{red + blue} on every draw (the marble is replaced).", f"E(X) = np = {n} · {red}/{red + blue}.", f"E(X) = {fr(ev)}."],
                [(fr(F(red, red + blue)), "gave the probability for one draw"), (fr(F(n * red, blue)), f"used {red}/{blue}, a ratio, instead of a probability"),
                 (fr(F(n * blue, red + blue)), "counted blue marbles"), (fr(F(n, 2)), "assumed red and blue are equally likely")],
                dict(k="md_draws", red=red, blue=blue, n=n, show=[f"{red} red and {blue} blue", f"{n} times"]), "md_draws")


# ------------------------------------------------------------------ S-MD.A.4 expected value from empirical probabilities
SURVEYS = [("cars", "car", "households", "household"), ("pets", "pet", "families", "family"), ("TVs", "TV", "apartments", "apartment"),
           ("siblings", "sibling", "students", "student"), ("books borrowed", "book borrowed", "library visitors", "visitor")]


def md_empirical(r, L):
    N = r.choice([20, 25, 40, 50, 80, 100, 200])
    k = 4 if L < 2 else 5
    cuts = sorted(r.sample(range(1, N), k - 1))
    counts = [b - a for a, b in zip([0] + cuts, cuts + [N])]
    need(min(counts) >= 1)
    many, one, group, unit = r.choice(SURVEYS)
    rows = ", ".join(f"{x} {many if x != 1 else one}: {cnt}" for x, cnt in enumerate(counts))
    ev = F(sum(x * cnt for x, cnt in enumerate(counts)), N)
    base = f"A survey of {N} {group} recorded the number of {many} for each {unit}: {rows}."
    if L == 2 and r.random() < 0.5:
        M = N * r.choice([5, 10, 20, 50])
        hits = counts[2] + counts[3] + counts[4]
        ans = M * hits // N
        return item(base + f" Use these results as probabilities. In a group of {M} {group} like these, how many would you expect to have at least 2 {many}?", str(ans),
                    [f"P(X ≥ 2) = ({counts[2]} + {counts[3]} + {counts[4]})/{N} = {fr(F(hits, N))}.", f"Expected number = {M} · {fr(F(hits, N))} = {ans}."],
                    [(str(M * (counts[2]) // N) if M * counts[2] % N == 0 else None, "counted only exactly 2"),
                     (str(M * (hits + counts[1]) // N) if M * (hits + counts[1]) % N == 0 else None, "counted at least 1"),
                     (str(hits), "gave the survey count, not the expected count for the new group"), (str(M - ans), "counted fewer than 2")],
                    dict(k="md_emp_count", counts=counts, N=N, M=M, show=[f"survey of {N}", rows, f"group of {M}"]), "md_emp_count")
    return item(base + f" Use these results as probabilities. Find the exact expected number of {many} per {unit}.", dec(ev),
                [f"P(X = x) = count/{N}.", "E(X) = Σ x · P(x) = (" + " + ".join(f"{x}·{cnt}" for x, cnt in enumerate(counts)) + f")/{N}.", f"E(X) = {dec(ev)}."],
                [(dec(F(k - 1, 2)), "averaged the possible values without weighting them"), (dec(F(sum(x * cnt for x, cnt in enumerate(counts)), k)) if L else None, "divided by the number of categories"),
                 (str(sum(x * cnt for x, cnt in enumerate(counts))), f"did not divide by {N}"), (dec(F(N, k)), "averaged the counts")],
                dict(k="md_emp_ev", counts=counts, N=N, show=[f"survey of {N}", rows]), "md_emp_ev")


# ------------------------------------------------------------------ S-MD.B.6 fair decisions with random devices
def md_fair(r, L):
    if L == 0 or r.random() < 0.5:
        k = r.randint(3, 7)
        N = r.choice([v for v in (10, 12, 15, 20, 25, 30, 50, 100) if v % k and v > k])
        each, extra = N // k, N % k
        who, one = r.choice([("students share one prize", "student"), ("teams need to choose who presents first", "team"), ("friends choose who picks first", "friend")])
        ask = r.choice(["each", "reroll"]) if L else "each"
        q = (f"{k} {who}. A random number generator gives a whole number from 1 to {N}, each equally likely. To keep the choice fair, every {one} gets the same number of values, as many as possible, and any other value means generate again. "
             + (f"How many values does each {one} get?" if ask == "each" else "How many of the values mean generate again?"))
        ans = each if ask == "each" else extra
        return item(q, str(ans),
                    [f"{N} ÷ {k} = {each} remainder {extra}.", f"Each {one} gets {each} values ({each * k} values in all), so each has probability {each}/{each * k} = 1/{k}.",
                     f"The other {extra} values mean generate again, so the choice stays fair."],
                    [(str(each + 1), "rounded up, so some people would get more values than others"), (str(extra if ask == "each" else each), "mixed up the quotient and the remainder"),
                     (str(N - k), f"subtracted {k} from {N}"), (str(k), "gave the number of choices")],
                    dict(k="md_fair_split", n=k, N=N, ask=ask, show=[f"{k} ", f"from 1 to {N}"]), "md_fair_split")
    s = r.randint(3, 11)
    a, b = r.sample(NAMES, 2)
    win = sum(1 for x in range(1, 7) for y in range(1, 7) if x + y <= s)
    p = F(win, 36)
    return item(f"{a} and {b} roll two fair dice to decide who goes first. {a} goes first if the sum is {s} or less; otherwise {b} goes first. What is the probability that {a} goes first?",
                fr(p),
                ["There are 36 equally likely outcomes.", f"{win} of them have a sum of {s} or less.", f"P = {win}/36 = {fr(p)}" + (". The method is fair only if this is 1/2." if p != F(1, 2) else ", so the method is fair.")],
                [(fr(F(s - 1, 11)), "treated the 11 sums from 2 to 12 as equally likely"), (fr(1 - p) if p != F(1, 2) else None, f"found {b}'s probability"),
                 (fr(F(win - 1, 36)) if win > 1 else None, "left out one outcome"), (fr(F(1, 2)) if p != F(1, 2) else None, "assumed the method is fair")],
                dict(k="md_fair_dice", s=s, show=[f"sum is {s} or less"]), "md_fair_dice")


# ------------------------------------------------------------------ S-MD.B.7 decisions from probability: screening tests
def md_screen(r, L):
    N = 10000
    prev = r.choice([1, 2, 4, 5, 10])
    sens = r.choice([90, 95, 98])
    spec = r.choice([90, 95, 98, 99])
    sick = N * prev // 100
    tp = sick * sens // 100
    fp = (N - sick) * (100 - spec) // 100
    stem = (f"A screening test is given to {N:,} people. {prev}% of them have the condition. The test is positive for {sens}% of people who have the condition "
            f"and negative for {spec}% of people who do not.")
    show = [f"{N:,} people", f"{prev}% of them", f"positive for {sens}%", f"negative for {spec}%"]
    ask = 0 if L == 0 else r.choice([1, 2] if L == 1 else [2, 2, 3])
    if ask == 0:
        return item(stem + " How many people who have the condition test positive?", f"{tp:,}",
                    [f"People with the condition: {prev}% of {N:,} = {sick:,}.", f"{sens}% of them test positive: {tp:,}."],
                    [(f"{sick:,}", "gave everyone who has the condition"), (f"{sick - tp:,}", "found the people the test misses"),
                     (f"{N * sens // 100:,}", f"took {sens}% of everyone"), (f"{fp:,}", "found the false positives")],
                    dict(k="md_screen", N=N, prev=prev, sens=sens, spec=spec, ask="tp", show=show), "md_screen_tp")
    if ask == 1:
        return item(stem + " How many people who do not have the condition test positive (false positives)?", f"{fp:,}",
                    [f"People without the condition: {N:,} - {sick:,} = {N - sick:,}.", f"{100 - spec}% of them test positive: {fp:,}."],
                    [(f"{(N - sick) * spec // 100:,}", "found the true negatives"), (f"{N * (100 - spec) // 100:,}", f"took {100 - spec}% of everyone"),
                     (f"{tp:,}", "found the true positives"), (f"{tp + fp:,}", "found every positive test")],
                    dict(k="md_screen", N=N, prev=prev, sens=sens, spec=spec, ask="fp", show=show), "md_screen_fp")
    if ask == 2:
        return item(stem + " How many people in all test positive?", f"{tp + fp:,}",
                    [f"With the condition: {sick:,}; {sens}% test positive: {tp:,}.", f"Without it: {N - sick:,}; {100 - spec}% test positive: {fp:,}.", f"Total positives: {tp + fp:,}."],
                    [(f"{tp:,}", "counted only true positives"), (f"{fp:,}", "counted only false positives"), (f"{sick:,}", "assumed the test is perfect"),
                     (f"{tp + (N - sick) * spec // 100:,}", "added the true negatives")],
                    dict(k="md_screen", N=N, prev=prev, sens=sens, spec=spec, ask="pos", show=show), "md_screen_pos")
    pct = F(100 * tp, tp + fp)
    t = pct * 10
    need(abs(t - (t.numerator // t.denominator) - F(1, 2)) > F(1, 1000))
    ans = f"{round(float(pct), 1):.1f}%"
    return item(stem + " A person tests positive. What is the probability that this person has the condition? Give a percent to the nearest tenth.", ans,
                [f"True positives: {tp:,}. False positives: {fp:,}.", f"P(condition | positive) = {tp:,}/({tp:,} + {fp:,}).", f"≈ {ans}. A positive result alone is weak evidence when the condition is rare, so a second test is a sensible decision."],
                [(f"{sens:.1f}%", "gave P(positive | condition) instead"), (f"{round(100 * fp / (tp + fp), 1):.1f}%", "gave the share of false positives"),
                 (f"{prev:.1f}%", "gave the prevalence"), (f"{round(100 * tp / N, 1):.1f}%", f"divided by all {N:,} people")],
                dict(k="md_screen", N=N, prev=prev, sens=sens, spec=spec, ask="ppv", show=show), "md_screen_ppv")


# (course, unit, skill index, id prefix, id tag, standards, family)
PLAN = [
    ("precalculus", "vectors", 1, "pc-vec", "x", ["N-CN.C.8"], cn_factor),
    ("precalculus", "matrices", 2, "pc-mat", "x", ["N-VM.C.9"], vm_props),
    ("precalculus", "trigonometric-functions", 2, "pc-trg", "x", ["F-TF.A.4"], tf_symmetry),
    ("precalculus", "probability", 1, "pc-prb", "x", ["S-MD.A.2"], md_theory),
    ("precalculus", "probability", 1, "pc-prb", "y", ["S-MD.A.4"], md_empirical),
    ("precalculus", "probability", 5, "pc-prb", "x", ["S-MD.B.6"], md_fair),
    ("algebra2", "probability-statistics", 6, "a2-ps", "x", ["S-MD.B.6"], md_fair),
    ("algebra2", "probability-statistics", 6, "a2-ps", "y", ["S-MD.B.7"], md_screen),
]
