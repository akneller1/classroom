"""Whole-site audit 2, item #6 (2026-11-20): question families for the Discrete Math skills that had fewer than
12 items at a level. Every answer is computed here by brute force (truth tables, enumeration, vertex checks),
and build.py re-checks each multiple-choice option against the same computation.

A family is fn(r) -> dict(fmt, prompt, answer, steps, wrongs, fam). `wrongs` are other option texts (multiple
choice only). Families named *_h are written for Advanced and use their own question templates, so no Advanced
item repeats a Support template with new numbers.
"""
import itertools, math
from fractions import Fraction as Fr


class Reject(Exception):
    pass


def need(ok):
    if not ok:
        raise Reject()


def Q(fmt, prompt, answer, steps, fam, wrongs=()):
    return dict(fmt=fmt, prompt=prompt, answer=answer, steps=list(steps), fam=fam, wrongs=[w for w in dict.fromkeys(wrongs) if w != answer])


def fr(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def roster(s):
    s = sorted(s)
    return "{" + ", ".join(str(x) for x in s) + "}" if s else "∅"


# ============================================================ logic helpers
OPS = {"¬": "not", "∧": "and", "∨": "or"}


def ev(expr, env):
    """Evaluate a formula over p, q, r written with ¬ ∧ ∨ → ↔ and parentheses."""
    s = expr.replace("↔", " == ").replace("¬", " not ").replace("∧", " and ").replace("∨", " or ")
    # implication: rewrite a → b as (not a or b) by splitting at the top-level arrow
    def imp(t):
        depth, cut = 0, -1
        for i, ch in enumerate(t):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "→" and depth == 0:
                cut = i
                break
        if cut < 0:
            inner = t
            out, i = "", 0
            while i < len(inner):
                if inner[i] == "(":
                    d, j = 1, i + 1
                    while d:
                        d += {"(": 1, ")": -1}.get(inner[j], 0)
                        j += 1
                    out += "(" + imp(inner[i + 1:j - 1]) + ")"
                    i = j
                else:
                    out += inner[i]
                    i += 1
            return out
        return "(not (" + imp(t[:cut]) + ") or (" + imp(t[cut + 1:]) + "))"
    return bool(eval(imp(s), {"__builtins__": {}}, dict(env)))


def column(expr, vs=("p", "q")):
    return "".join("T" if ev(expr, dict(zip(vs, row))) else "F" for row in itertools.product([True, False], repeat=len(vs)))


def equiv(a, b, vs=("p", "q", "r")):
    return column(a, vs) == column(b, vs)


ROWS2 = "(p, q) = TT, TF, FT, FF"

S_PAIRS = [("it snows", "school is closed"), ("a number is divisible by 4", "it is even"), ("you study", "you pass the quiz"),
           ("the store is open", "the lights are on"), ("a triangle is equilateral", "it is isosceles"), ("the alarm rings", "Dana wakes up"),
           ("x = 3", "x² = 9"), ("the battery is dead", "the phone will not turn on"), ("a figure is a square", "it is a rectangle"),
           ("the team wins", "the fans cheer"), ("it is Saturday", "the library opens late"), ("a number ends in 0", "it is divisible by 5"),
           ("the oven is preheated", "the bread rises well"), ("Leo practices", "Leo improves"), ("the plant gets sunlight", "the plant grows")]


def neg(clause):
    """Simple English negation for the phrase bank."""
    swaps = [(" is not ", " is "), (" is ", " is not "), (" are ", " are not "), (" will not ", " will "), (" wins", " does not win"), (" rings", " does not ring"),
             (" opens", " does not open"), (" wakes", " does not wake"), (" cheer", " do not cheer"), (" study", " do not study"), (" pass", " do not pass"),
             (" practices", " does not practice"), (" improves", " does not improve"), (" grows", " does not grow"), (" rises", " does not rise"), (" ends in", " does not end in"),
             (" snows", " does not snow"), (" gets", " does not get")]
    if clause.startswith("x = 3"):
        return "x ≠ 3"
    if clause.startswith("x² = 9"):
        return "x² ≠ 9"
    for a, b in swaps:
        if a in " " + clause + " " or a in clause:
            return clause.replace(a.strip() if a.startswith(" ") and clause.startswith(a.strip()) else a, b, 1) if a in clause else clause
    raise Reject()


def neg2(c):
    out = neg(c)
    need(out != c)
    return out


def cap(s):
    return s[0].upper() + s[1:]


# ---------------------------------------------------------------- compound statements
def lg04(r):
    e = r.choice(["p → ¬q", "¬p → ¬q", "¬q → ¬p", "q → ¬p", "(p ∧ q) → p", "p → (p ∨ q)", "¬(p → q)", "(p ∨ q) → q", "p → (q ∧ p)", "¬p → (p ∨ q)", "(p → q) ∧ q", "(p → q) ∨ p"])
    col = column(e)
    return Q("short-answer", f"Write the truth column of {e} in the row order {ROWS2}, as four letters such as TFTT.", col,
             ["A conditional a → b is false only when a is true and b is false.", "Row by row: " + ", ".join(f"{row}: {c}" for row, c in zip(["TT", "TF", "FT", "FF"], col)) + ".", f"The column is {col}."], "truth_column")


EQ_POOL = ["p ∨ q", "p ∧ q", "¬p ∨ q", "p ∧ ¬q", "¬p ∧ ¬q", "¬p ∨ ¬q", "q → p", "¬q → ¬p", "¬p → q", "p → (q → r)", "(p ∧ q) → r", "(p → r) ∧ (q → r)", "(p ∨ q) → r",
           "p → (q ∧ r)", "(p → q) ∧ (p → r)", "(p → q) ∨ (p → r)", "p → (q ∨ r)", "(p ∧ q) → (p ∧ r)", "¬p ∨ (q ∧ r)", "¬r → ¬(p ∧ q)", "q ∨ (p → r)", "(p ∧ ¬q) → r"]


def lg04_h(r):
    target = r.choice(["p → (q → r)", "(p ∨ q) → r", "p → (q ∧ r)", "p → (q ∨ r)", "¬(p ∧ q) ∨ r", "¬p → q"])
    good = [e for e in EQ_POOL if e != target and equiv(e, target)]
    bad = [e for e in EQ_POOL if not equiv(e, target)]
    need(good)
    ans = r.choice(good)
    wr = r.sample(bad, 3)
    return Q("multiple-choice", f"Which expression is logically equivalent to {target}? Compare truth tables over p, q and r.", ans,
             [f"Build the truth table of {target} over all 8 rows of p, q, r: column {column(target, ('p', 'q', 'r'))}.", f"{ans} has the same column in every row, so the two are equivalent.",
              "Each other choice differs in at least one row: " + "; ".join(f"{w}: {column(w, ('p', 'q', 'r'))}" for w in wr) + "."], "equivalent_forms_h", wr)


def lg05(r):
    a, b = r.choice(S_PAIRS)
    ans = f"{cap(a)} and {neg2(b)}."
    return Q("multiple-choice", f"Which is the negation of \"If {a}, then {b}.\"?", ans,
             ["The negation of p → q is p ∧ ¬q: the hypothesis happens and the conclusion does not.", f"So the negation is: {ans}"], "negate_conditional",
             [f"If {a}, then {neg2(b)}.", f"If {neg2(a)}, then {neg2(b)}.", f"{cap(neg2(a))} and {b}.", f"{cap(neg2(a))} or {b}."])


def lg05_h(r):
    target = r.choice(["¬(p → (q ∨ r))", "¬((p ∧ q) → r)", "¬(p → ¬q)", "¬((p ∨ q) → r)", "¬(p → (q ∧ r))"])
    pool = ["p ∧ ¬q ∧ ¬r", "p ∧ q ∧ ¬r", "p ∧ q", "(p ∨ q) ∧ ¬r", "p ∧ (¬q ∨ ¬r)", "¬p ∨ q ∨ r", "¬p ∧ ¬q ∧ ¬r", "p ∨ ¬q ∨ ¬r", "(p ∧ q) ∨ ¬r", "p ∧ ¬q", "¬p ∨ ¬q", "p → (¬q ∧ ¬r)"]
    good = [e for e in pool if equiv(e, target)]
    bad = [e for e in pool if not equiv(e, target)]
    need(len(good) == 1)
    wr = r.sample(bad, 3)
    return Q("multiple-choice", f"Use ¬(a → b) ≡ a ∧ ¬b and De Morgan's laws. Which expression is equivalent to {target}?", good[0],
             ["Negating a conditional keeps the hypothesis and negates the conclusion: ¬(a → b) ≡ a ∧ ¬b.", f"Apply it, then De Morgan's laws to the negated conclusion: {target} ≡ {good[0]}.",
              f"Check: both have truth column {column(target, ('p', 'q', 'r'))} over the 8 rows of p, q, r."], "negate_conditional_h", wr)


def lg06(r):
    a, b = r.choice(S_PAIRS)
    kind = r.choice(["CONVERSE", "INVERSE", "CONTRAPOSITIVE"])
    forms = {"CONVERSE": f"If {b}, then {a}.", "INVERSE": f"If {neg2(a)}, then {neg2(b)}.", "CONTRAPOSITIVE": f"If {neg2(b)}, then {neg2(a)}."}
    rule = {"CONVERSE": "The converse swaps the hypothesis and the conclusion: q → p.", "INVERSE": "The inverse negates both parts: ¬p → ¬q.", "CONTRAPOSITIVE": "The contrapositive swaps and negates both parts: ¬q → ¬p."}[kind]
    return Q("multiple-choice", f"Statement: \"If {a}, then {b}.\" Which is its {kind}?", forms[kind], [f"Here p is \"{a}\" and q is \"{b}\".", rule, f"So the {kind.lower()} is: {forms[kind]}"],
             "converse_inverse", [v for k, v in forms.items() if k != kind] + [f"If {b}, then {neg2(a)}."])


def lg06_h(r):
    hyp, con = r.choice([("p ∧ q", "r"), ("p", "q ∨ r"), ("p ∨ q", "r"), ("p", "q ∧ r"), ("¬p", "q ∧ r")])
    kind = r.choice(["contrapositive", "converse", "inverse"])
    nh = {"p ∧ q": "¬p ∨ ¬q", "p": "¬p", "p ∨ q": "¬p ∧ ¬q", "¬p": "p"}[hyp]
    nc = {"r": "¬r", "q ∨ r": "¬q ∧ ¬r", "q ∧ r": "¬q ∨ ¬r"}[con]
    par = lambda t: f"({t})" if (" ∧ " in t or " ∨ " in t) else t
    sw = lambda t: t.replace("∧", "#").replace("∨", "∧").replace("#", "∨")
    forms = {"contrapositive": f"{par(nc)} → {par(nh)}", "converse": f"{par(con)} → {par(hyp)}", "inverse": f"{par(nh)} → {par(nc)}"}
    wrong_dm = f"{par(sw(nc))} → {par(sw(nh))}" if kind == "contrapositive" else f"{par(sw(nh))} → {par(sw(nc))}"
    ans = forms[kind]
    return Q("multiple-choice", f"For the conditional {par(hyp)} → {par(con)}, which expression is its {kind}? Simplify negations with De Morgan's laws.", ans,
             [{"contrapositive": "Contrapositive: ¬(conclusion) → ¬(hypothesis).", "converse": "Converse: conclusion → hypothesis.", "inverse": "Inverse: ¬(hypothesis) → ¬(conclusion)."}[kind],
              f"¬({hyp}) = {nh} and ¬({con}) = {nc} by De Morgan's laws.", f"So the {kind} is {ans}." + (" It is equivalent to the original statement." if kind == "contrapositive" else " It is not equivalent to the original statement.")],
             "converse_inverse_h", [v for k, v in forms.items() if k != kind] + [wrong_dm, f"{par(nc)} → {par(hyp)}"])


RULES = [("Modus ponens", ["{a} → {b}", "{a}"], "{b}"), ("Modus tollens", ["{a} → {b}", "¬{b}"], "¬{a}"), ("Generalization", ["{a}"], "{a} ∨ {b}"),
         ("Specialization", ["{a} ∧ {b}"], "{b}"), ("Conjunction", ["{a}", "{b}"], "{a} ∧ {b}"), ("Elimination", ["{a} ∨ {b}", "¬{a}"], "{b}"),
         ("Transitivity", ["{a} → {b}", "{b} → {c}"], "{a} → {c}")]


def lg07(r):
    a, b, c = r.choice([("r", "s", "t"), ("s", "t", "u"), ("q", "r", "s"), ("u", "w", "p")])
    name, prem, con = r.choice(RULES)
    lines = [x.format(a=a, b=b, c=c) for x in prem]
    return Q("multiple-choice", "Name the rule of inference:\n" + "\n".join(lines) + "\n∴ " + con.format(a=a, b=b, c=c), name,
             [f"Premises: {'; '.join(lines)}. Conclusion: {con.format(a=a, b=b, c=c)}.", f"This is the pattern of {name.lower()}: " + {"Modus ponens": "from p → q and p, conclude q.",
              "Modus tollens": "from p → q and ¬q, conclude ¬p.", "Generalization": "from p, conclude p ∨ q.", "Specialization": "from p ∧ q, conclude either part.",
              "Conjunction": "from p and q, conclude p ∧ q.", "Elimination": "from p ∨ q and ¬p, conclude q.", "Transitivity": "from p → q and q → r, conclude p → r."}[name]],
             "rule_name", [n for n, _, _ in RULES if n != name] + ["Converse error"])


ARGS_H = [(["p → q", "q → r", "r"], "p"), (["p ∨ q", "p → r", "r"], "¬q"), (["p → q", "¬p", "q → r"], "¬r"), (["p ∧ q → r", "r"], "p"),
          (["p → (q ∨ r)", "p", "¬q"], "¬r"), (["p ∨ r", "q → r", "¬q"], "p"), (["p → r", "q → r", "r"], "p ∨ q"), (["¬p → q", "q"], "¬p ∧ r"),
          (["p → q", "r → q", "q"], "p ∧ r"), (["p ∨ q", "q ∨ r"], "p ∨ r")]


def lg07_h(r):
    prem, con = r.choice(ARGS_H)
    rows = list(itertools.product([True, False], repeat=3))
    tf = lambda row: "(" + ", ".join("T" if v else "F" for v in row) + ")"
    bad = [row for row in rows if all(ev(x, dict(zip("pqr", row))) for x in prem) and not ev(con, dict(zip("pqr", row)))]
    need(bad)
    good = [row for row in rows if row not in bad]
    ans = r.choice(bad)
    wr = r.sample(good, 3)
    return Q("multiple-choice", "This argument is invalid:\n" + "\n".join(prem) + "\n∴ " + con + "\nWhich assignment (p, q, r) makes every premise true and the conclusion false?", tf(ans),
             ["An argument is invalid when some row of the truth table makes all premises true and the conclusion false.",
              f"At {tf(ans)}: " + "; ".join(f"{x} is {'T' if ev(x, dict(zip('pqr', ans))) else 'F'}" for x in prem) + f"; the conclusion {con} is F.",
              "Each other choice makes a premise false or the conclusion true."], "invalid_row_h", [tf(w) for w in wr])


def lg08(r):
    a, b = r.choice(S_PAIRS)
    kind = r.choice(["conv", "inv", "mp", "mt"])
    second, concl = {"conv": (b, a), "inv": (neg2(a), neg2(b)), "mp": (a, b), "mt": (neg2(b), neg2(a))}[kind]
    ans = {"conv": "Converse error (affirming the conclusion)", "inv": "Inverse error (denying the hypothesis)", "mp": "Valid (modus ponens)", "mt": "Valid (modus tollens)"}[kind]
    return Q("multiple-choice", f"Classify the argument:\nIf {a}, then {b}. {cap(second)}. So {concl}.", ans,
             [f"Let p = \"{a}\" and q = \"{b}\"; the first premise is p → q.", {"conv": "The argument goes from q to p, which a true conditional does not allow.", "inv": "The argument goes from ¬p to ¬q, which a true conditional does not allow.",
              "mp": "From p → q and p, q follows.", "mt": "From p → q and ¬q, ¬p follows."}[kind], f"So it is: {ans}."], "fallacy_name",
             ["Converse error (affirming the conclusion)", "Inverse error (denying the hypothesis)", "Valid (modus ponens)", "Valid (modus tollens)"])


def lg08_h(r):
    a, b = r.choice(S_PAIRS)
    kind = r.choice(["conv", "inv"])
    args = {"conv": f"If {a}, then {b}. {cap(b)}. Therefore {a}.", "inv": f"If {a}, then {b}. {cap(neg2(a))}. Therefore {neg2(b)}.",
            "mp": f"If {a}, then {b}. {cap(a)}. Therefore {b}.", "mt": f"If {a}, then {b}. {cap(neg2(b))}. Therefore {neg2(a)}."}
    name = {"conv": "the converse error", "inv": "the inverse error"}[kind]
    return Q("multiple-choice", f"Which argument commits {name}?", args[kind],
             ["Converse error: from p → q and q, conclude p. Inverse error: from p → q and ¬p, conclude ¬q.", f"The argument \"{args[kind]}\" has exactly that form, so it commits {name}.",
              "Of the others, two are valid (modus ponens and modus tollens) and one is the other error."], "fallacy_pick_h", [v for k, v in args.items() if k != kind])


# ---------------------------------------------------------------- counting and probability
def cn01(r):
    n = r.choice([4, 6, 8, 10, 12])
    k = r.randint(2, 3)
    return Q("short-answer", f"A fair coin is tossed {k} times and then a fair {n}-sided die is rolled once. How many outcomes are in the sample space?", str(2 ** k * n),
             [f"Each toss has 2 outcomes and the die has {n}.", f"By the multiplication rule: 2^{k} · {n} = {2 ** k} · {n} = {2 ** k * n} outcomes."], "sample_space_size")


def cn01_h(r):
    n, cond = r.choice([(2, "the sum is 9"), (2, "at least one die shows 6"), (2, "the two dice differ by 2"), (2, "the product is a multiple of 4"),
                        (3, "all three dice show the same number"), (3, "the sum is 10"), (2, "the larger number is 4")])
    test = {"the sum is 9": lambda o: sum(o) == 9, "at least one die shows 6": lambda o: 6 in o, "the two dice differ by 2": lambda o: abs(o[0] - o[1]) == 2,
            "the product is a multiple of 4": lambda o: (o[0] * o[1]) % 4 == 0, "all three dice show the same number": lambda o: len(set(o)) == 1,
            "the sum is 10": lambda o: sum(o) == 10, "the larger number is 4": lambda o: max(o) == 4}[cond]
    outs = [o for o in itertools.product(range(1, 7), repeat=n) if test(o)]
    ex = ", ".join("(" + ", ".join(map(str, o)) + ")" for o in outs[:4])
    return Q("short-answer", f"{'Two' if n == 2 else 'Three'} fair dice are rolled{' (in order: first, second' + (', third' if n == 3 else '') + ')'}. The sample space has {6 ** n} ordered outcomes. How many outcomes are in the event \"{cond}\"?", str(len(outs)),
             [f"List the ordered outcomes in the event systematically: {ex}{', …' if len(outs) > 4 else ''}.", f"There are {len(outs)} outcomes in the event (out of {6 ** n})."], "event_count_h")


def cn03(r):
    a, b = r.randint(2, 4), r.randint(2, 4)
    x, y = r.choice([("shirt", "pair of pants"), ("bread", "filling"), ("color", "size"), ("route to the park", "route home")])
    return Q("short-answer", f"A possibility tree first branches for the choice of {x} ({a} options), then for the {y} ({b} options). How many leaves does the tree have?", str(a * b),
             [f"Each of the {a} first branches splits into {b} second branches.", f"Leaves = {a} · {b} = {a * b}."], "tree_leaves")


def cn03_h(r):
    kind = r.choice(["series", "flips"])
    if kind == "series":
        k = r.choice([2, 3, 4])
        cnt = 0
        def grow(a, b):
            nonlocal cnt
            if a == k or b == k:
                cnt += 1
                return
            grow(a + 1, b)
            grow(a, b + 1)
        grow(0, 0)
        return Q("short-answer", f"Teams X and Y play until one team has won {k} games (no ties). A possibility tree shows each game as a branch. How many leaves (complete series) does the tree have?", str(cnt),
                 ["Branch at every game: X wins or Y wins; a branch stops as soon as one team reaches " + str(k) + " wins.", f"Count the stopped branches: the series can end after {k} to {2 * k - 1} games.",
                  f"There are {cnt} leaves (each team wins in {cnt // 2} of them)."], "tree_series_h")
    m = r.choice([3, 4, 5])
    cnt = 0
    def grow(seq):
        nonlocal cnt
        if seq.endswith("HH") or len(seq) == m:
            cnt += 1
            return
        grow(seq + "H")
        grow(seq + "T")
    grow("")
    return Q("short-answer", f"A coin is tossed until two heads in a row appear or until {m} tosses have been made, whichever comes first. How many leaves does the possibility tree have?", str(cnt),
             ["Branch H or T at each toss; stop a branch when it ends in HH or reaches " + str(m) + " tosses.", f"Counting the stopped branches gives {cnt} leaves."], "tree_stop_h")


def cn04(r):
    a, b = r.randint(3, 12), r.randint(3, 12)
    x, y, z = r.choice([("one snack", "fruit cups", "granola bars"), ("one elective", "art classes", "music classes"), ("one movie", "comedies", "documentaries"),
                        ("one shirt", "T-shirts", "polo shirts"), ("one route", "bus routes", "train routes")])
    return Q("short-answer", f"Maya picks {x}: one of {a} {y} or one of {b} {z} (none is both). How many choices does she have?", str(a + b),
             ["The two groups do not overlap, so use the addition rule.", f"{a} + {b} = {a + b} choices."], "addition_rule")


def cn05(r):
    a, b, c = r.randint(2, 6), r.randint(2, 6), r.randint(2, 5)
    return Q("short-answer", f"A pizza order is one crust ({a} kinds), one sauce ({b} kinds) and one topping ({c} kinds). How many different orders are possible?", str(a * b * c),
             ["Each order is a sequence of three independent choices, so use the multiplication rule.", f"{a} · {b} · {c} = {a * b * c} orders."], "multiplication_rule")


def cn06(r):
    n, k = r.randint(4, 8), r.randint(2, 3)
    ordered = r.choice([True, False])
    v = math.perm(n, k) if ordered else math.comb(n, k)
    what = f"a president, vice president{' and secretary' if k == 3 else ''}" if ordered else f"a {k}-person team (order does not matter)"
    return Q("short-answer", f"How many ways can {what} be chosen from {n} club members?", str(v),
             ["Order matters, so count arrangements: P(n, k)." if ordered else "Order does not matter, so count combinations: C(n, k).",
              (f"P({n}, {k}) = " + " · ".join(str(n - i) for i in range(k)) if ordered else f"C({n}, {k}) = {math.perm(n, k)}/{math.factorial(k)}") + f" = {v}."], "count_systematic")


def cn06_h(r):
    kind = r.choice(["incr", "incl"])
    if kind == "incr":
        L = r.choice([3, 4])
        v = sum(1 for t in itertools.product(range(10), repeat=L) if t[0] != 0 and all(t[i] < t[i + 1] for i in range(L - 1)))
        return Q("short-answer", f"How many {L}-digit numbers have digits that strictly increase from left to right (like 1{'24' if L == 3 else '247'})?", str(v),
                 ["The first digit cannot be 0, and increasing digits can never include 0 after a nonzero digit, so the digits come from 1–9.",
                  f"Each choice of {L} different digits from 1–9 gives exactly one increasing number: C(9, {L}) = {v}."], "count_increasing_h")
    N, a, b = r.choice([100, 120, 200, 150]), r.choice([3, 4, 6]), r.choice([5, 7, 10])
    need(a != b)
    v = sum(1 for i in range(1, N + 1) if i % a == 0 or i % b == 0)
    l = a * b // math.gcd(a, b)
    return Q("short-answer", f"How many integers from 1 to {N} are divisible by {a} or by {b}?", str(v),
             [f"Multiples of {a}: {N // a}. Multiples of {b}: {N // b}. Multiples of both (of lcm {l}): {N // l}.", f"Inclusion–exclusion: {N // a} + {N // b} − {N // l} = {v}."], "inclusion_exclusion_h")


def cn07(r):
    a, b, c = r.randint(2, 7), r.randint(2, 7), r.randint(1, 6)
    col = r.choice(["red", "green"])
    v = Fr(a if col == "red" else b, a + b + c)
    return Q("short-answer", f"A bag holds {a} red, {b} green and {c} yellow tiles. One tile is drawn at random. Find P({col}). Give a fraction in lowest terms.", fr(v),
             [f"There are {a + b + c} equally likely tiles; {a if col == 'red' else b} are {col}.", f"P({col}) = {a if col == 'red' else b}/{a + b + c}" + (f" = {fr(v)}." if v.denominator != a + b + c else ", already in lowest terms.")], "equally_likely")


def cn07_h(r):
    ev_, test = r.choice([("the product is even", lambda o: o[0] * o[1] % 2 == 0), ("the sum is prime", lambda o: sum(o) in (2, 3, 5, 7, 11)),
                          ("the two numbers differ by at most 1", lambda o: abs(o[0] - o[1]) <= 1), ("the first die is greater than the second", lambda o: o[0] > o[1]),
                          ("the product is a perfect square", lambda o: int(math.isqrt(o[0] * o[1])) ** 2 == o[0] * o[1])])
    k = sum(1 for o in itertools.product(range(1, 7), repeat=2) if test(o))
    return Q("short-answer", f"Two fair dice are rolled. Find the probability that {ev_}. Give a fraction in lowest terms.", fr(Fr(k, 36)),
             ["The 36 ordered outcomes are equally likely.", f"Count the outcomes where {ev_}: {k}.", f"P = {k}/36 = {fr(Fr(k, 36))}."], "dice_event_h")


def cn08(r):
    L = r.choice([3, 4])
    kind = r.choice(["distinct", "noseven"])
    if kind == "distinct":
        v = Fr(math.perm(10, L), 10 ** L)
        return Q("short-answer", f"A {L}-digit code (digits 0–9, repetition allowed) is chosen at random. Find P(no digit repeats). Give a fraction in lowest terms.", fr(v),
                 [f"Total codes: 10^{L} = {10 ** L}. Codes with no repeat: " + " · ".join(str(10 - i) for i in range(L)) + f" = {math.perm(10, L)}.", f"P = {math.perm(10, L)}/{10 ** L} = {fr(v)}."], "count_prob")
    v = Fr(9 ** L, 10 ** L)
    return Q("short-answer", f"A {L}-digit code (digits 0–9, repetition allowed) is chosen at random. Find P(the code contains no 7). Give a fraction in lowest terms.", fr(v),
             [f"Total codes: 10^{L}. Codes without a 7 use 9 digits in each place: 9^{L} = {9 ** L}.", f"P = {9 ** L}/{10 ** L} = {fr(v)}."], "count_prob")


def cn08_h(r):
    n = r.choice([4, 5, 6])
    letters = "ABCDEF"[:n]
    kind = r.choice(["adjacent", "ends"])
    perms = list(itertools.permutations(letters))
    if kind == "adjacent":
        k = sum(1 for p in perms if abs(p.index("A") - p.index("B")) == 1)
        txt = "A and B are next to each other"
        st = f"Treat AB as one block: 2 · {n - 1}! = {2 * math.factorial(n - 1)} arrangements."
    else:
        k = sum(1 for p in perms if p[0] in "AB" and p[-1] in "AB")
        txt = "A and B are at the two ends"
        st = f"A and B fill the ends in 2 ways, the rest in {n - 2}! ways: {2 * math.factorial(n - 2)} arrangements."
    return Q("short-answer", f"The letters {', '.join(letters)} are arranged in a random order. Find the probability that {txt}. Give a fraction in lowest terms.", fr(Fr(k, len(perms))),
             [f"All {n}! = {len(perms)} arrangements are equally likely.", st, f"P = {k}/{len(perms)} = {fr(Fr(k, len(perms)))}."], "arrangement_prob_h")


# ---------------------------------------------------------------- election theory
CRIT = {"Majority criterion": "A candidate with a majority of first-place votes should win.",
        "Condorcet criterion": "A candidate who wins every head-to-head comparison should win.",
        "Monotonicity criterion": "If the winner gains support and nothing else changes, the winner should still win.",
        "Independence of irrelevant alternatives": "Removing a losing candidate should not change the winner."}


def el03(r):
    name = r.choice(list(CRIT))
    return Q("multiple-choice", f"Which fairness criterion is described here?\n\"{CRIT[name]}\"", name,
             [f"The description is the definition of the {name.lower() if name[0] != 'I' else name}.", "Majority: first-place majority wins. Condorcet: head-to-head winner wins. Monotonicity: more support cannot hurt. IIA: dropping a loser changes nothing."],
             "criterion_name", [k for k in CRIT if k != name])


def schedule(r, cands, n):
    rows = []
    for _ in range(n):
        rows.append((r.randint(2, 12), tuple(r.sample(cands, len(cands)))))
    merged = {}
    for c, rk in rows:
        merged[rk] = merged.get(rk, 0) + c
    return list(merged.items())


def el03_h(r):
    C = ["A", "B", "C"]
    for _ in range(400):
        sch = schedule(r, C, 3)
        tot = sum(v for _, v in sch)
        first = {c: sum(v for rk, v in sch if rk[0] == c) for c in C}
        top = max(first.values())
        need_ok = list(first.values()).count(top) == 1 and top * 2 <= tot
        plur = max(first, key=first.get)
        beats = lambda x, y: sum(v for rk, v in sch if rk.index(x) < rk.index(y)) * 2 > tot
        cond = [x for x in C if all(beats(x, y) for y in C if y != x)]
        if need_ok and len(cond) == 1 and cond[0] != plur:
            break
    else:
        raise Reject()
    others = [c for c in C if c not in (plur, cond[0])]
    lines = "\n".join(f"{v} voters: {' > '.join(rk)}" for rk, v in sch)
    ans = f"Plurality: {plur}; Condorcet winner: {cond[0]}"
    return Q("multiple-choice", f"Preference schedule ({tot} voters):\n{lines}\nWho wins by plurality, and who is the Condorcet winner?", ans,
             ["First-place votes: " + ", ".join(f"{c} {first[c]}" for c in C) + f", so {plur} wins by plurality.",
              f"Head to head, {cond[0]} beats each other candidate with more than {tot // 2} votes.", f"So the plurality method fails the Condorcet criterion in this election."],
             "plurality_vs_condorcet_h", [f"Plurality: {cond[0]}; Condorcet winner: {plur}", f"Plurality: {plur}; Condorcet winner: {others[0]}", f"Plurality: {plur}; there is no Condorcet winner"])


def el06(r):
    n = r.choice([3, 4, 5])
    val = n * r.randint(6, 40)
    who, item = r.choice([("Rosa", "a pizza"), ("Omar", "a garden plot"), ("Jada", "a cake"), ("Leo", "a weekend at the cabin")])
    return Q("short-answer", f"{n} friends divide {item} fairly. {who} values all of it at ${val}. What is {who}'s fair share, in dollars? (Write the number only.)", str(val // n),
             [f"A fair share is at least 1/{n} of the whole by the player's own values.", f"${val} ÷ {n} = ${val // n}."], "fair_share")


def el06_h(r):
    for _ in range(200):
        items = r.sample(["car", "boat", "piano", "cabin", "painting", "truck"], 2)
        bids = {nm: {it: r.randint(4, 40) * 50 for it in items} for nm in ("Ana", "Ben")}
        win = {it: max(bids, key=lambda nm: bids[nm][it]) for it in items}
        if any(bids["Ana"][it] == bids["Ben"][it] for it in items):
            continue
        share = {nm: Fr(sum(bids[nm].values()), 2) for nm in bids}
        got = {nm: sum(bids[nm][it] for it in items if win[it] == nm) for nm in bids}
        cash = {nm: share[nm] - got[nm] for nm in bids}
        surplus = -sum(cash.values())
        final = {nm: cash[nm] + surplus / 2 for nm in bids}
        if final["Ana"] != 0:
            break
    else:
        raise Reject()
    who = r.choice(["Ana", "Ben"])
    money = lambda v: f"{float(v):.2f}"
    lines = "\n".join(f"{nm} bids: " + ", ".join(f"{it} ${bids[nm][it]}" for it in items) for nm in bids)
    return Q("short-answer", f"Two heirs settle an estate by sealed bids:\n{lines}\nEach item goes to the higher bidder, fair shares are half of each heir's total bid, and any surplus is split equally. How much cash does {who} receive? (A negative amount means {who} pays. Write dollars and cents, like 125.00.)",
             money(final[who]),
             [f"Fair shares: Ana ${money(share['Ana'])}, Ben ${money(share['Ben'])}. Items: " + ", ".join(f"{it} to {win[it]}" for it in items) + ".",
              f"Before the surplus: Ana gets ${money(cash['Ana'])}, Ben gets ${money(cash['Ben'])}; the surplus is ${money(surplus)}, so each adds ${money(surplus / 2)}.",
              f"{who} receives ${money(final[who])}."], "sealed_bids_two_h")


def el08(r):
    kind = r.choice(["alabama", "pop", "new", "ham"])
    if kind == "ham":
        return Q("multiple-choice", "Which apportionment method can produce the Alabama paradox (a state loses a seat when the house grows)?", "Hamilton's method",
                 ["The Alabama paradox comes from ranking fractional parts, which can change order when the house size changes.", "Hamilton's method assigns extra seats by fractional parts; divisor methods (Jefferson, Webster, Adams) avoid this paradox."],
                 "paradox_method", ["Jefferson's method", "Webster's method", "Adams's method"])
    desc = {"alabama": "The house grows from 40 to 41 seats and state C drops from 5 seats to 4.", "pop": "State P grows by 8% and state Q by 2%, yet P loses a seat to Q with the same house size.",
            "new": "A new state joins with exactly its fair share of new seats, and two old states trade a seat."}[kind]
    ans = {"alabama": "Alabama paradox", "pop": "Population paradox", "new": "New-states paradox"}[kind]
    return Q("multiple-choice", f"Name the paradox:\n{desc}", ans,
             [{"alabama": "A state losing a seat only because the house grew is the Alabama paradox.", "pop": "A faster-growing state losing a seat to a slower-growing one is the population paradox.",
               "new": "Old states' seats changing when a new state is added with its fair share is the new-states paradox."}[kind], f"So this is the {ans.lower()}."],
             "paradox_name", ["Alabama paradox", "Population paradox", "New-states paradox", "Quota rule violation"])


def hamilton(pops, S):
    tot = sum(pops)
    q = [Fr(p * S, tot) for p in pops]
    base = [x.numerator // x.denominator for x in q]
    left = S - sum(base)
    order = sorted(range(len(pops)), key=lambda i: q[i] - base[i], reverse=True)
    need(len({q[i] - base[i] for i in order}) == len(order))
    for i in order[:left]:
        base[i] += 1
    return base, q


def jefferson(pops, S):
    tot = sum(pops)
    d = Fr(tot, S)
    for _ in range(100000):
        seats = [int(Fr(p) / d) for p in pops]
        if sum(seats) == S:
            return seats, d
        d -= Fr(1, 10) if sum(seats) < S else -Fr(1, 10)
    raise Reject()


def el08_h(r):
    for _ in range(300):
        pops = [r.randint(10, 99) * 100 for _ in range(3)]
        S = r.choice([10, 12, 15])
        try:
            h, q = hamilton(pops, S)
            j, d = jefferson(pops, S)
        except Reject:
            continue
        if h != j:
            break
    else:
        raise Reject()
    meth = r.choice(["Hamilton", "Jefferson"])
    seats = h if meth == "Hamilton" else j
    other = j if meth == "Hamilton" else h
    ans = ", ".join(map(str, seats))
    pl = ", ".join(f"{n} {p:,}" for n, p in zip("ABC", pops))
    st = ([f"Standard divisor {sum(pops):,}/{S} = {float(Fr(sum(pops), S)):.2f}; quotas " + ", ".join(f"{float(x):.2f}" for x in q) + ".",
           f"Give each state its lower quota, then the {S - sum(int(x) for x in q)} leftover seat(s) to the largest fractional parts: {ans}."] if meth == "Hamilton" else
          [f"Lower quotas add to less than {S}, so lower the divisor until the rounded-down quotients add to {S}.", f"With divisor about {float(d):.1f} the quotients round down to {ans}."])
    return Q("short-answer", f"Apportion {S} seats among states A, B and C (populations {pl}) by {meth}'s method. List the seats for A, B, C in order, separated by commas.", ans,
             st + [f"(Compare: the other common method gives {', '.join(map(str, other))}, so the method choice changes the outcome.)"], "apportion_compare_h")


# ---------------------------------------------------------------- graphs (described in words)
def graph(r, n, m, loops=False):
    V = "ABCDEFG"[:n]
    pairs = [(a, b) for i, a in enumerate(V) for b in V[i + 1:]]
    E = r.sample(pairs, m)
    if loops and r.random() < 0.6:
        E.append((r.choice(V), None))
    return V, E


def etext(E):
    return ", ".join(a + (b or a) for a, b in E)


def deg(E, v):
    return sum((a == v) + (b == v) + (b is None and a == v) for a, b in E)


def gr01_h(r):
    kind = r.choice(["regular", "sum"])
    if kind == "regular":
        n, d = r.choice([(6, 3), (8, 3), (7, 4), (10, 3), (9, 4), (12, 5)])
        return Q("short-answer", f"A graph has {n} vertices, and every vertex has degree {d}. How many edges does it have?", str(n * d // 2),
                 [f"By the handshake theorem, the sum of the degrees is twice the number of edges.", f"Sum of degrees = {n} · {d} = {n * d}, so there are {n * d}/2 = {n * d // 2} edges."], "handshake_h")
    V, E = graph(r, 5, r.randint(5, 7), loops=True)
    s = sum(deg(E, v) for v in V)
    return Q("short-answer", f"A graph has vertices {', '.join(V)} and edges {etext(E)} (an edge written like CC is a loop). What is the sum of the degrees of all vertices?", str(s),
             ["Each edge adds 2 to the degree sum (a loop adds 2 to its one vertex).", "Degrees: " + ", ".join(f"{v} {deg(E, v)}" for v in V) + f"; sum = {s} = 2 · {len(E)} edges."], "degree_sum_h")


def dgraph(r, n, m):
    V = "ABCDE"[:n]
    arcs = r.sample([(a, b) for a in V for b in V if a != b], m)
    return V, arcs


def gr02(r):
    V, A = dgraph(r, 4, r.randint(5, 7))
    v = r.choice(V)
    io = r.choice(["in", "out"])
    k = sum(1 for a, b in A if (b if io == "in" else a) == v)
    return Q("short-answer", f"A directed graph has vertices {', '.join(V)} and arrows {', '.join(a + '→' + b for a, b in A)}. What is the {io}-degree of {v}?", str(k),
             [f"The {io}-degree counts arcs {'ending at' if io == 'in' else 'starting at'} {v}.", f"Arcs {'into' if io == 'in' else 'out of'} {v}: " + (", ".join(a + '→' + b for a, b in A if (b if io == 'in' else a) == v) or "none") + f". So it is {k}."], "digraph_degree")


def gr02_h(r):
    V, A = dgraph(r, 5, r.randint(6, 9))
    kind = r.choice(["count", "reach"])
    if kind == "count":
        k = sum(1 for v in V if sum(b == v for _, b in A) > sum(a == v for a, _ in A))
        return Q("short-answer", f"A directed graph has vertices {', '.join(V)} and arrows {', '.join(a + '→' + b for a, b in A)}. How many vertices have in-degree greater than out-degree?", str(k),
                 ["(in, out) for each vertex: " + ", ".join(f"{v} ({sum(b == v for _, b in A)}, {sum(a == v for a, _ in A)})" for v in V) + ".", f"{k} vertices have more arcs in than out."], "digraph_compare_h")
    s = r.choice(V)
    seen, stack = {s}, [s]
    while stack:
        x = stack.pop()
        for a, b in A:
            if a == x and b not in seen:
                seen.add(b)
                stack.append(b)
    reach = sorted(seen - {s})
    return Q("short-answer", f"A directed graph has vertices {', '.join(V)} and arrows {', '.join(a + '→' + b for a, b in A)}. How many other vertices can be reached from {s} by a directed path?", str(len(reach)),
             [f"Follow arcs forward from {s}, adding each new vertex reached.", f"Reachable: {', '.join(reach) or 'none'}; that is {len(reach)} vertices."], "digraph_reach_h")


def chromatic(V, E):
    for k in range(1, len(V) + 1):
        for col in itertools.product(range(k), repeat=len(V)):
            c = dict(zip(V, col))
            if all(c[a] != c[b] for a, b in E):
                return k, c
    return len(V), None


def gr04(r):
    V, E = graph(r, 5, r.randint(5, 8))
    k, c = chromatic(V, E)
    return Q("multiple-choice", f"A graph has vertices {', '.join(V)} and edges {etext(E)}. What is its chromatic number (fewest colors so that adjacent vertices differ)?", str(k),
             ["Color greedily, then check whether fewer colors could work (a triangle needs 3; an odd cycle needs 3).", "A coloring with " + str(k) + " colors: " + ", ".join(f"{v}={c[v] + 1}" for v in V) + f"; no coloring with {k - 1} works."],
             "chromatic", [str(x) for x in (1, 2, 3, 4, 5) if x != k][:3])


def gr04_h(r):
    courses = ["Art", "Bio", "Chem", "Drama", "Econ", "French"]
    for _ in range(100):
        n = r.choice([5, 6])
        V = courses[:n]
        pairs = r.sample([(a, b) for i, a in enumerate(V) for b in V[i + 1:]], r.randint(n, n + 3))
        k, c = chromatic(V, pairs)
        if k >= 3:
            break
    return Q("short-answer", f"Final exams must be scheduled so that no student has two exams at once. These pairs of courses share a student: {', '.join(a + '–' + b for a, b in pairs)}. What is the fewest number of exam time slots needed?", str(k),
             ["Make a graph: courses are vertices and an edge joins two courses that share a student. Time slots are colors.", "A schedule with " + str(k) + " slots: " + ", ".join(f"{v} slot {c[v] + 1}" for v in V) + f". Fewer slots fail because some {k} courses are pairwise linked or an odd cycle forces it.",
              f"The minimum is the chromatic number, {k}."], "exam_coloring_h")


def connected(V, E):
    seen, st = {V[0]}, [V[0]]
    while st:
        x = st.pop()
        for a, b in E:
            for u, w in ((a, b), (b, a)):
                if u == x and w and w not in seen:
                    seen.add(w)
                    st.append(w)
    return len(seen) == len(V)


def gr05(r):
    V, E = graph(r, 5, 7)
    adj = {frozenset(e) for e in E}
    kind = r.choice(["path", "trail", "walk"])
    for _ in range(400):
        L = r.randint(4, 6)
        seq = [r.choice(V)]
        while len(seq) < L:
            nb = [b if a == seq[-1] else a for a, b in E if seq[-1] in (a, b)]
            if not nb:
                break
            seq.append(r.choice(nb))
        if len(seq) < L:
            continue
        es = [frozenset((seq[i], seq[i + 1])) for i in range(len(seq) - 1)]
        is_trail = len(set(es)) == len(es)
        is_path = len(set(seq)) == len(seq)
        closed = seq[0] == seq[-1]
        got = "path" if is_path else ("trail" if is_trail else "walk")
        if got == kind and not closed:
            break
    else:
        raise Reject()
    ans = {"path": "A path (no repeated vertex, so also a trail)", "trail": "A trail that is not a path", "walk": "A walk that is not a trail"}[kind]
    return Q("multiple-choice", f"A graph has vertices {', '.join(V)} and edges {etext(E)}. Classify the sequence {'–'.join(seq)}. (A trail repeats no edge; a path repeats no vertex.)", ans,
             [f"Edges used: {', '.join(''.join(sorted(e)) for e in es)}.", {"path": "No vertex repeats, so it is a path (and a trail).", "trail": "A vertex repeats but no edge does: a trail, not a path.", "walk": "An edge repeats, so it is only a walk."}[kind]],
             "walk_class", ["A path (no repeated vertex, so also a trail)", "A trail that is not a path", "A walk that is not a trail", "A circuit"])


def gr05_h(r):
    for _ in range(300):
        V, E = graph(r, r.choice([5, 6]), r.randint(6, 9))
        if connected(V, E):
            break
    else:
        raise Reject()
    odd = [v for v in V if deg(E, v) % 2]
    kind = r.choice(["euler", "add"])
    if kind == "euler":
        if len(odd) == 0:
            ans = "Yes: an Euler circuit (every vertex has even degree)"
        elif len(odd) == 2:
            ans = f"Yes: an Euler trail from {odd[0]} to {odd[1]}"
        else:
            ans = f"No: {len(odd)} vertices have odd degree"
        wr = ["Yes: an Euler circuit (every vertex has even degree)", f"Yes: an Euler trail from {V[0]} to {V[1]}", "No: the graph is not connected", f"No: {len(odd) + 2} vertices have odd degree"]
        return Q("multiple-choice", f"A connected graph has vertices {', '.join(V)} and edges {etext(E)}. Does it have an Euler trail or circuit?", ans,
                 ["Degrees: " + ", ".join(f"{v} {deg(E, v)}" for v in V) + ".", "A connected graph has an Euler circuit if 0 vertices have odd degree and an Euler trail (not closed) if exactly 2 do.",
                  f"Here {len(odd)} vertices have odd degree, so: {ans}."], "euler_check_h", wr)
    return Q("short-answer", f"A connected graph has vertices {', '.join(V)} and edges {etext(E)}. What is the fewest number of edges you must duplicate (add as extra copies of existing edges) so the graph has an Euler circuit? Assume the odd vertices can be paired by edges between them.",
             str(len(odd) // 2),
             ["Degrees: " + ", ".join(f"{v} {deg(E, v)}" for v in V) + f"; odd-degree vertices: {', '.join(odd) or 'none'}.", f"Each added edge fixes at most two odd vertices, so at least {len(odd)}/2 = {len(odd) // 2} edges are needed."], "eulerize_h") if all(frozenset(p) in {frozenset(e) for e in E} for p in zip(odd[0::2], odd[1::2])) else gr05_h(r)


def gr06(r):
    for _ in range(300):
        V, E = graph(r, 5, r.randint(5, 8))
        if connected(V, E):
            break
    odd = [v for v in V if deg(E, v) % 2]
    ans = "Yes: every vertex has even degree" if not odd else f"No: {', '.join(odd)} {'has' if len(odd) == 1 else 'have'} odd degree"
    return Q("multiple-choice", f"A connected graph has vertices {', '.join(V)} and edges {etext(E)}. Does it have an Euler circuit (a circuit using every edge exactly once)?", ans,
             ["Degrees: " + ", ".join(f"{v} {deg(E, v)}" for v in V) + ".", "A connected graph has an Euler circuit exactly when every vertex has even degree.", ans + "."], "euler_circuit",
             ["Yes: every vertex has even degree", "No: the graph is not connected", "Yes: there are exactly two odd vertices", f"No: {V[0]} has odd degree"])


def gr06_h(r):
    V, E = graph(r, 5, r.randint(5, 7))
    V = tuple(V)
    adj = {frozenset(e) for e in E}
    cyc = None
    for p in itertools.permutations(V[1:]):
        c = (V[0],) + p
        if all(frozenset((c[i], c[(i + 1) % len(c)])) in adj for i in range(len(c))):
            cyc = c
            break
    ans = ("Yes, for example " + "–".join(cyc + (cyc[0],))) if cyc else "No Hamiltonian circuit exists"
    fake = None
    for p in itertools.permutations(V[1:]):
        c = (V[0],) + p
        if not all(frozenset((c[i], c[(i + 1) % len(c)])) in adj for i in range(len(c))):
            fake = c
            break
    need(fake)
    wr = ["No Hamiltonian circuit exists", "Yes, for example " + "–".join(fake + (fake[0],)), "Yes, because every vertex has even degree", "No, because some vertex has odd degree"]
    return Q("multiple-choice", f"A graph has vertices {', '.join(V)} and edges {etext(E)}. Does it have a Hamiltonian circuit (a circuit through every vertex exactly once)?", ans,
             ["Try to build a cycle through all 5 vertices using only the listed edges.", ("The cycle " + "–".join(cyc + (cyc[0],)) + " uses only listed edges.") if cyc else "Every attempt gets stuck: no ordering of the vertices uses only listed edges (checked all orderings).",
              "Degree parity matters for Euler circuits, not Hamiltonian ones."], "hamilton_h", wr)


# ---------------------------------------------------------------- linear programming
CTX = [("a bakery", "loaves", "pies", "oven hours", "loaf", "pie"), ("a furniture shop", "tables", "chairs", "carpentry hours", "table", "chair"),
       ("a school store", "notebooks", "folders", "dollars of budget", "notebook", "folder"), ("a farm", "acres of corn", "acres of beans", "hours of labor", "acre of corn", "acre of beans"),
       ("a print shop", "posters", "banners", "ink cartridges", "poster", "banner")]


def ineq(a, b, op, c):
    t = lambda k, v: (v if k == 1 else f"{k}{v}")
    return f"{t(a, 'x')} + {t(b, 'y')} {op} {c}"


def lp01(r):
    ctx, X, Y, res, x1, y1 = r.choice(CTX)
    a, b = r.randint(1, 6), r.randint(1, 6)
    need(a != b)
    c = r.randint(4, 20) * 10
    op = r.choice(["≤", "≥"])
    word = "at most" if op == "≤" else "at least"
    ans = ineq(a, b, op, c)
    return Q("multiple-choice", f"In {ctx}, x = number of {X} and y = number of {Y}. Each {x1} uses {a} {res} and each {y1} uses {b}. The plan must use {word} {c} {res}. Which inequality expresses this constraint?", ans,
             [f"{res.capitalize()} used: {a}x + {b}y.", f"\"{word.capitalize()}\" means {op}, so {ans}."], "write_constraint",
             [ineq(b, a, op, c), ineq(a, b, "≥" if op == "≤" else "≤", c), ineq(a, b, "<" if op == "≤" else ">", c)])


def lp01_h(r):
    ctx, X, Y, res, x1, y1 = r.choice(CTX)
    a, b, c = r.randint(2, 5), r.randint(1, 4), r.randint(6, 20) * 10
    m = r.randint(2, 4)
    ans = f"{ineq(a, b, '≤', c)}; y ≥ {m}x; x ≥ 0; y ≥ 0"
    return Q("multiple-choice", f"In {ctx}, x = number of {X} and y = number of {Y}. Each {x1} needs {a} {res} and each {y1} needs {b}, with {c} {res} available. There must be at least {m} times as many {Y} as {X}, and amounts cannot be negative. Which system of constraints models this?", ans,
             [f"Resource: {ineq(a, b, '≤', c)}.", f"\"At least {m} times as many {Y} as {X}\": y ≥ {m}x.", "Nonnegativity: x ≥ 0, y ≥ 0."], "write_system_h",
             [f"{ineq(a, b, '≤', c)}; x ≥ {m}y; x ≥ 0; y ≥ 0", f"{ineq(a, b, '≥', c)}; y ≥ {m}x; x ≥ 0; y ≥ 0", f"{ineq(b, a, '≤', c)}; y ≤ {m}x; x ≥ 0; y ≥ 0"])


def lp04_h(r):
    ctx, X, Y, res, x1, y1 = r.choice(CTX)
    p1, p2, c1, c2 = r.randint(30, 90), r.randint(20, 70), r.randint(5, 25), r.randint(5, 20)
    need(p1 > c1 and p2 > c2)
    ans = f"Maximize P = {p1 - c1}x + {p2 - c2}y"
    return Q("multiple-choice", f"In {ctx}, x = number of {X} and y = number of {Y}. Each {x1} sells for ${p1} and costs ${c1} to make; each {y1} sells for ${p2} and costs ${c2}. What objective should the manager use to earn the most profit?", ans,
             [f"Profit per {x1}: {p1} − {c1} = {p1 - c1}. Profit per {y1}: {p2} − {c2} = {p2 - c2}.", f"Total profit is {ans[9:]}, and the goal is to maximize it."], "objective_profit_h",
             [f"Maximize P = {p1}x + {p2}y", f"Minimize C = {c1}x + {c2}y", f"Maximize P = {p1 + c1}x + {p2 + c2}y"])


def lp_solve(cons, obj, mode):
    pts = set()
    lines = cons + [(1, 0, 0), (0, 1, 0)]
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        d = a1 * b2 - a2 * b1
        if d == 0:
            continue
        x, y = Fr(c1 * b2 - c2 * b1, d), Fr(a1 * c2 - a2 * c1, d)
        if x >= 0 and y >= 0 and all(a * x + b * y <= c if mode == "max" else a * x + b * y >= c for a, b, c in cons):
            pts.add((x, y))
    vals = sorted(((obj[0] * x + obj[1] * y, (x, y)) for x, y in pts), reverse=(mode == "max"))
    need(len(vals) >= 3 and vals[0][0] != vals[1][0] and all(v.denominator == 1 for v in vals[0][1]))
    return vals


def lp06(r):
    cons = [(r.randint(1, 3), r.randint(1, 3), r.randint(6, 18)), (r.randint(1, 4), r.randint(1, 4), r.randint(8, 24))]
    obj = (r.randint(2, 6), r.randint(2, 6))
    vals = lp_solve(cons, obj, "max")
    (v, (x, y)) = vals[0]
    txt = "; ".join(ineq(a, b, "≤", c) for a, b, c in cons)
    return Q("short-answer", f"Maximize P = {obj[0]}x + {obj[1]}y subject to {txt}; x ≥ 0; y ≥ 0. Give the optimal point and value as \"(x, y), P = value\".", f"({x}, {y}), P = {v}",
             ["List the corner points of the feasible region: " + ", ".join(f"({fr(px)}, {fr(py)})" for _, (px, py) in vals) + ".", "Evaluate P at each: " + ", ".join(f"{fr(val)}" for val, _ in vals) + ".", f"The largest is P = {v} at ({x}, {y})."], "lp_max")


def lp06_h(r):
    cons = [(r.randint(1, 4), r.randint(1, 4), r.randint(8, 24)), (r.randint(1, 4), r.randint(1, 4), r.randint(8, 24))]
    obj = (r.randint(2, 9), r.randint(2, 9))
    vals = lp_solve(cons, obj, "min")
    (v, (x, y)) = vals[0]
    txt = "; ".join(ineq(a, b, "≥", c) for a, b, c in cons)
    return Q("short-answer", f"A diet mixes x units of food A and y units of food B. Minimize the cost C = {obj[0]}x + {obj[1]}y subject to {txt}; x ≥ 0; y ≥ 0. Give the optimal point and cost as \"(x, y), C = value\".", f"({x}, {y}), C = {v}",
             ["The feasible region is unbounded, so check the corner points: " + ", ".join(f"({fr(px)}, {fr(py)})" for _, (px, py) in vals) + ".", "Cost at each corner: " + ", ".join(fr(val) for val, _ in vals) + ".",
              f"The least cost is C = {v} at ({x}, {y}); moving farther out only raises the cost."], "lp_min_h")


def lp07(r):
    ctx, X, Y, res, x1, y1 = r.choice(CTX)
    a, b = r.randint(5, 40), r.randint(5, 40)
    p = r.randint(2, 9) * a + r.randint(2, 9) * b
    ans = f"Make {a} {X} and {b} {Y} for the maximum profit of ${p}"
    return Q("multiple-choice", f"In {ctx}, x = {X} and y = {Y}. The maximum profit is found at the corner point ({a}, {b}) with P = {p}. What does this mean?", ans,
             ["The coordinates of the optimal point are the amounts to make: x first, y second.", f"The objective value is the best profit: ${p}."], "interpret_optimum",
             [f"Make {b} {X} and {a} {Y} for the maximum profit of ${p}", f"Make {a} {X} and {b} {Y} for a profit of ${a + b}", f"Profit is ${p} for each item made"])


def lp07_h(r):
    ctx, X, Y, res, x1, y1 = r.choice(CTX)
    for _ in range(200):
        a, b = r.randint(2, 6), r.randint(2, 6)
        x, y = r.randint(3, 20), r.randint(3, 20)
        cap_ = a * x + b * y + r.randint(1, 30)
        break
    used = a * x + b * y
    return Q("short-answer", f"In {ctx}, the optimal plan is x = {x} {X} and y = {y} {Y}. One constraint is {ineq(a, b, '≤', cap_)} ({res}). How many {res} are left unused at the optimum?", str(cap_ - used),
             [f"{res.capitalize()} used: {a}({x}) + {b}({y}) = {used}.", f"Unused (slack) = {cap_} − {used} = {cap_ - used}. A constraint with slack is not binding."], "slack_h")


# ---------------------------------------------------------------- proof
def isprime(n):
    return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))


def np03(r):
    kind = r.choice(["sq", "prime", "root", "cube"])
    if kind == "sq":
        k = r.choice([3, 5, 7])
        cands = [k * k * j * j for j in (1, 2)]
        ans = str(min(c for c in range(10, 200) if c % k == 0 and math.isqrt(c) ** 2 == c and c > 10))
        wr = [str(int(ans) + k), str(int(ans) - 1), str(k * 10)]
        return Q("multiple-choice", f"\"There is a perfect square greater than 10 that is a multiple of {k}.\" Which number is a witness?", ans,
                 [f"A witness must be a perfect square, greater than 10 and divisible by {k}.", f"{ans} = {math.isqrt(int(ans))}² and {ans} ÷ {k} = {int(ans) // k}, so it works."], "witness",
                 [w for w in wr if not (int(w) > 10 and int(w) % k == 0 and math.isqrt(int(w)) ** 2 == int(w))])
    if kind == "prime":
        lo = r.choice([30, 50, 60, 70, 80, 90])
        ps = [p for p in range(lo, lo + 10) if isprime(p)]
        need(ps)
        ans = str(ps[0])
        wr = [str(x) for x in range(lo, lo + 10) if not isprime(x)]
        return Q("multiple-choice", f"\"There is a prime number between {lo} and {lo + 10}.\" Which number proves it?", ans,
                 [f"A witness must be prime and lie between {lo} and {lo + 10}.", f"{ans} has no divisor other than 1 and itself, so it proves the statement."], "witness", r.sample(wr, 3))
    if kind == "root":
        a, b = r.randint(-6, -1), r.randint(1, 6)
        ans = str(a).replace("-", "−")
        s, p = -(a + b), a * b
        poly = f"n² {'+' if s >= 0 else '−'} {abs(s)}n {'+' if p >= 0 else '−'} {abs(p)} = 0".replace(" 1n", " n")
        wr = [str(-a), str(-b).replace("-", "−"), str(a - 1).replace("-", "−")]
        return Q("multiple-choice", f"\"There is a negative integer n such that {poly}.\" Which value is a witness?", ans,
                 [f"Factor: (n − ({a}))(n − {b}) = 0, so n = {a} or n = {b}.", f"The negative root {ans} is the witness."], "witness", [w for w in wr if w != ans and w != str(b)])
    k = r.choice([2, 3])
    ans = str(next(n for n in range(2, 50) if (n ** 3) % 10 == 7 + 0 * k))
    return Q("multiple-choice", "\"There is a positive integer whose cube ends in the digit 7.\" Which number is a witness?", ans,
             ["Check cubes' last digits: the last digit of n³ depends only on the last digit of n.", f"{ans}³ = {int(ans) ** 3}, which ends in 7."], "witness", ["7", "17", "2"] if ans != "3" else ["7", "9", "2"])


def np03_h(r):
    stmt, test, rng_, val = r.choice([("For every integer n ≥ 1, n² + n + 41 is prime.", lambda n: isprime(n * n + n + 41), range(1, 60), lambda n: ("n² + n + 41", n * n + n + 41)),
                                 ("For every integer n ≥ 1, 2ⁿ + 1 is prime.", lambda n: isprime(2 ** n + 1), range(1, 12), lambda n: ("2ⁿ + 1", 2 ** n + 1)),
                                 ("For every integer n ≥ 2, n² − n + 11 is prime.", lambda n: isprime(n * n - n + 11), range(2, 30), lambda n: ("n² − n + 11", n * n - n + 11)),
                                 ("For every positive integer n, n² + 1 is not divisible by 5.", lambda n: (n * n + 1) % 5 != 0, range(1, 30), lambda n: ("n² + 1", n * n + 1)),
                                 ("For every integer n ≥ 1, 6n − 1 is prime.", lambda n: isprime(6 * n - 1), range(1, 20), lambda n: ("6n − 1", 6 * n - 1))])
    bad = [n for n in rng_ if not test(n)]
    good = [n for n in rng_ if test(n)]
    need(bad and len(good) >= 3)
    ans = str(bad[0])
    return Q("multiple-choice", f"The universal statement \"{stmt}\" is false. Which value of n is a counterexample?", ans,
             ["A counterexample is one allowed value of n that makes the statement false.", f"At n = {ans}: {val(int(ans))[0]} = {val(int(ans))[1]}, which " + ("is divisible by 5." if "divisible by 5" in stmt else f"is not prime ({val(int(ans))[1]} = {min(d for d in range(2, val(int(ans))[1]) if val(int(ans))[1] % d == 0)} · {val(int(ans))[1] // min(d for d in range(2, val(int(ans))[1]) if val(int(ans))[1] % d == 0)})."), "Each other choice makes the statement true, so it does not disprove it."],
             "counterexample_h", [str(x) for x in r.sample(good[: max(3, len(good))], 3)])


STRAT = [("There is an integer n with n² = 4n + 21.", "Constructive proof (give a witness)"), ("Every odd number is prime.", "Counterexample (it is false)"),
         ("For every n in {2, 3, 4}, n² < 2ⁿ⁺¹.", "Method of exhaustion"), ("The sum of any two even integers is even.", "Direct proof"),
         ("There is no largest even integer.", "Proof by contradiction"), ("If n² is odd, then n is odd.", "Proof by contrapositive"),
         ("There is a perfect square between 50 and 60.", "Constructive proof (give a witness)"), ("Every multiple of 3 is odd.", "Counterexample (it is false)"),
         ("For every n in {1, 2, 3, 4}, n! ≤ 2n².", "Method of exhaustion"), ("The product of two odd integers is odd.", "Direct proof"),
         ("√3 is irrational.", "Proof by contradiction"), ("If 3n + 2 is odd, then n is odd.", "Proof by contrapositive")]
STRATS = sorted({b for _, b in STRAT})


def np08(r):
    s, m = r.choice(STRAT)
    return Q("multiple-choice", f"Which method is the most natural way to handle this statement?\n\"{s}\"", m,
             [{"Constructive proof (give a witness)": "An existence statement is proved by exhibiting one example.", "Counterexample (it is false)": "The statement is a false universal claim; one example disproves it.",
               "Method of exhaustion": "Only finitely many cases are named, so check each one.", "Direct proof": "Assume the hypothesis about general integers and derive the conclusion.",
               "Proof by contradiction": "Assume the opposite and reach an impossibility.", "Proof by contrapositive": "The contrapositive (if n is even, then …) is easier to prove directly."}[m],
              f"So the most natural method is: {m}."], "proof_strategy", r.sample([x for x in STRATS if x != m], 3))


def np08_h(r):
    s, first, wr = r.choice([("If n² is even, then n is even.", "Suppose n is odd, so n = 2k + 1 for some integer k.", ["Suppose n² is even, so n² = 2k.", "Suppose n is even, so n = 2k.", "Suppose n² is odd and n is even."]),
                             ("If 5n + 3 is even, then n is odd.", "Suppose n is even, so n = 2k for some integer k.", ["Suppose 5n + 3 is even.", "Suppose n is odd, so n = 2k + 1.", "Suppose 5n + 3 is odd and n is odd."]),
                             ("If ab is odd, then a and b are both odd.", "Suppose a is even or b is even.", ["Suppose a and b are both odd.", "Suppose ab is odd.", "Suppose a is even and b is even."]),
                             ("If n³ is odd, then n is odd.", "Suppose n is even, so n = 2k for some integer k.", ["Suppose n³ is odd.", "Suppose n is odd, so n = 2k + 1.", "Suppose n³ is even."])])
    return Q("multiple-choice", f"A student proves \"{s}\" by contrapositive. Which sentence should begin the proof?", first,
             ["The contrapositive of \"if P, then Q\" is \"if not Q, then not P\".", f"So the proof assumes the negation of the conclusion: {first}", "Then it shows the negation of the hypothesis follows."], "contrapositive_start_h", wr)


# ---------------------------------------------------------------- relations
def rl01_h(r):
    A = sorted(r.sample(range(1, 13), r.randint(4, 5)))
    rel, test = r.choice([("a divides b and a ≠ b", lambda a, b: b % a == 0 and a != b), ("a < b", lambda a, b: a < b), ("b = a + 2", lambda a, b: b == a + 2),
                          ("a + b is a multiple of 5", lambda a, b: (a + b) % 5 == 0 and a != b)])
    R = [(a, b) for a in A for b in A if test(a, b)]
    need(2 <= len(R) <= 8)
    inv = sorted((b, a) for a, b in R)
    txt = lambda S: "{" + ", ".join(f"({a}, {b})" for a, b in S) + "}" if S else "∅"
    return Q("short-answer", f"Let A = {roster(A)} and let R be the relation on A defined by a R b if and only if {rel}. Find the inverse relation R⁻¹. List it as a set of ordered pairs, ordered by first then second coordinate.", txt(inv),
             [f"R = {txt(sorted(R))}.", "The inverse swaps each pair: (a, b) ∈ R exactly when (b, a) ∈ R⁻¹.", f"R⁻¹ = {txt(inv)}."], "inverse_relation_h")


def rl05(r):
    A = list(range(1, 7 + r.randint(0, 2)))
    kind = r.choice(["yes", "overlap", "missing", "empty"])
    els = A[:]
    r.shuffle(els)
    cuts = sorted(r.sample(range(1, len(els)), 2))
    blocks = [sorted(els[:cuts[0]]), sorted(els[cuts[0]:cuts[1]]), sorted(els[cuts[1]:])]
    if kind == "overlap":
        blocks[1] = sorted(set(blocks[1]) | {blocks[0][0]})
    elif kind == "missing":
        blocks[2] = blocks[2][1:] if len(blocks[2]) > 1 else None
        need(blocks[2])
    elif kind == "empty":
        blocks.append([])
    txt = "{" + ", ".join(roster(b) if b else "∅" for b in blocks) + "}"
    ans = {"yes": "Yes", "overlap": "No: some element is in two blocks", "missing": "No: some element of A is in no block", "empty": "No: one block is empty"}[kind]
    return Q("multiple-choice", f"Is {txt} a partition of A = {roster(A)}?", ans,
             ["A partition uses nonempty blocks that do not overlap and together contain every element of A.", {"yes": "All three conditions hold.", "overlap": "Two blocks share an element.",
              "missing": "Some element of A is in no block.", "empty": "The empty set cannot be a block."}[kind], f"Answer: {ans}."], "partition_check",
             ["Yes", "No: some element is in two blocks", "No: some element of A is in no block", "No: one block is empty"])


def rl05_h(r):
    n = r.randint(6, 10)
    A = list(range(1, n + 1))
    k = r.randint(2, 4)
    els = A[:]
    r.shuffle(els)
    cuts = sorted(r.sample(range(1, n), k - 1))
    blocks = [sorted(els[i:j]) for i, j in zip([0] + cuts, cuts + [n])]
    v = sum(len(b) ** 2 for b in blocks)
    txt = "{" + ", ".join(roster(b) for b in blocks) + "}"
    return Q("short-answer", f"The partition {txt} of A = {roster(A)} induces the relation R: a R b if and only if a and b are in the same block. How many ordered pairs are in R?", str(v),
             ["Inside a block of size s, every ordered pair (including (a, a)) is in R: s² pairs.", "Block sizes: " + ", ".join(str(len(b)) for b in blocks) + ".", f"Total = " + " + ".join(f"{len(b)}²" for b in blocks) + f" = {v}."], "induced_relation_h")


def props(A, R):
    S = set(R)
    refl = all((a, a) in S for a in A)
    sym = all((b, a) in S for a, b in S)
    tr = all((a, d) in S for a, b in S for c, d in S if b == c)
    return refl, sym, tr


def rl06(r):
    A = [1, 2, 3]
    for _ in range(500):
        R = sorted({(a, b) for a in A for b in A if r.random() < 0.45} | ({(a, a) for a in A} if r.random() < 0.6 else set()))
        p = props(A, R)
        if sum(not x for x in p) <= 1:
            break
    else:
        raise Reject()
    names = ["not reflexive", "not symmetric", "not transitive"]
    ans = "Yes" if all(p) else "No: " + names[p.index(False)]
    txt = "{" + ", ".join(f"({a}, {b})" for a, b in R) + "}"
    return Q("multiple-choice", f"On A = {{1, 2, 3}}, is R = {txt} an equivalence relation?", ans,
             [f"Reflexive: {'yes' if p[0] else 'no'}; symmetric: {'yes' if p[1] else 'no'}; transitive: {'yes' if p[2] else 'no'}.", "An equivalence relation must have all three properties.", f"Answer: {ans}."],
             "equivalence_check", ["Yes"] + ["No: " + x for x in names])


def rl07_h(r):
    n, k = r.randint(10, 30), r.randint(3, 7)
    rel = r.choice([f"a and b have the same remainder when divided by {k}", f"a ≡ b (mod {k})"])
    big = sum(1 for x in range(1, n + 1) if x % k == 1 % k)
    kind = r.choice(["count", "largest"])
    if kind == "count":
        return Q("short-answer", f"On A = {{1, 2, …, {n}}}, R is the equivalence relation \"{rel}\". How many distinct equivalence classes are there?", str(min(k, n)),
                 [f"Each class is the set of elements with one remainder 0, 1, …, {k - 1}.", f"All {k} remainders occur among 1 to {n}, so there are {k} classes."], "class_count_h")
    sizes = [sum(1 for x in range(1, n + 1) if x % k == j) for j in range(k)]
    return Q("short-answer", f"On A = {{1, 2, …, {n}}}, R is the equivalence relation \"{rel}\". How many elements are in the largest equivalence class?", str(max(sizes)),
             [f"Class sizes by remainder 0, 1, …, {k - 1}: {', '.join(map(str, sizes))}.", f"{n} = {k}·{n // k} + {n % k}, so {n % k} classes have {n // k + 1} elements and the rest have {n // k}. Largest: {max(sizes)}."], "class_size_h")


# ---------------------------------------------------------------- sequences
def sq01(r):
    a, b = r.randint(2, 7), r.randint(-5, 6)
    kind = r.choice(["lin", "sq", "frac", "alt"])
    if kind == "lin":
        f, form = (lambda n: a * n + b), f"{a}n {'+' if b >= 0 else '−'} {abs(b)}"
    elif kind == "sq":
        f, form = (lambda n: n * n - a), f"n² − {a}"
    elif kind == "frac":
        f, form = (lambda n: Fr(n, n + a)), f"n/(n + {a})"
    else:
        f, form = (lambda n: (-1) ** n * a * n), f"(−1)ⁿ · {a}n"
    terms = ", ".join(fr(f(n)) for n in range(1, 5))
    return Q("short-answer", f"Write the first four terms of a_n = {form}, starting with n = 1. Separate terms with commas (fractions as a/b).", terms,
             [f"Substitute n = 1, 2, 3, 4 into {form}.", f"The terms are {terms}."], "first_terms")


def sq02(r):
    a, rr, n = r.randint(1, 6), r.choice([2, 3]), r.randint(5, 8)
    return Q("multiple-choice", f"A geometric sequence has a₁ = {a} and common ratio r = {rr}. Find a_{n}.", str(a * rr ** (n - 1)),
             [f"a_n = a₁ · r^(n − 1).", f"a_{n} = {a} · {rr}^{n - 1} = {a * rr ** (n - 1)}."], "geometric_term", [str(a * rr ** n), str(a * rr * (n - 1)), str(a + rr * (n - 1))])


def sq03(r):
    n, k = r.randint(5, 10), r.randint(2, 4)
    need(k < n)
    return Q("short-answer", f"Evaluate C({n}, {k}) = {n}!/({k}! · {n - k}!).", str(math.comb(n, k)),
             [f"Cancel {n - k}!: C({n}, {k}) = (" + " · ".join(str(n - i) for i in range(k)) + f")/{k}!.", f"= {math.perm(n, k)}/{math.factorial(k)} = {math.comb(n, k)}."], "binomial_value")


def sq03_h(r):
    n = r.randint(5, 12)
    kind = r.choice(["perm", "comb"])
    if kind == "perm":
        v = n * (n - 1)
        return Q("short-answer", f"Find the positive integer n with n!/(n − 2)! = {v}.", str(n),
                 ["n!/(n − 2)! = n(n − 1), since the factors from (n − 2) down cancel.", f"Solve n(n − 1) = {v}: n = {n} (because {n} · {n - 1} = {v})."], "factorial_equation_h")
    v = math.comb(n, 2)
    return Q("short-answer", f"Find the positive integer n with C(n, 2) = {v}.", str(n),
             ["C(n, 2) = n(n − 1)/2.", f"n(n − 1) = {2 * v}, so n = {n}."], "factorial_equation_h")


def fib(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a


def sq04(r):
    kind = r.choice(["term", "sum"])
    if kind == "term":
        n = r.choice([8, 9, 11, 13, 14, 15])
        return Q("short-answer", f"Using F₁ = 1, F₂ = 1 and each term the sum of the two before it, what is the {n}th Fibonacci number?", str(fib(n)),
                 ["Build the list: " + ", ".join(str(fib(i)) for i in range(1, n + 1)) + ".", f"F_{n} = {fib(n)}."], "fibonacci_term")
    n = r.randint(5, 9)
    s = sum(fib(i) for i in range(1, n + 1))
    return Q("short-answer", f"Find F₁ + F₂ + … + F_{n} for the Fibonacci numbers (F₁ = F₂ = 1).", str(s),
             ["Terms: " + ", ".join(str(fib(i)) for i in range(1, n + 1)) + ".", f"Sum = {s} (check: it equals F_{n + 2} − 1 = {fib(n + 2)} − 1)."], "fibonacci_sum")


def sq05(r):
    a0, m, c = r.randint(1, 5), r.choice([1, 2, 3]), r.randint(-3, 4)
    need(not (m == 1 and c == 0))
    t = [a0]
    for _ in range(4):
        t.append(m * t[-1] + c)
    rule = ("" if m == 1 else str(m)) + "a_(n−1)" + (f" + {c}" if c > 0 else (f" − {-c}" if c < 0 else ""))
    return Q("short-answer", f"Find the first five terms of a₁ = {a0}, a_n = {rule} (for n ≥ 2). Separate terms with commas.", ", ".join(map(str, t)),
             [f"Start with a₁ = {a0} and apply the rule four times.", "a₂ = " + str(t[1]) + ", a₃ = " + str(t[2]) + ", a₄ = " + str(t[3]) + ", a₅ = " + str(t[4]) + "."], "recursive_terms")


def sq06(r):
    kind = r.choice(["arith", "geo"])
    if kind == "arith":
        a, d = r.randint(-5, 9), r.randint(2, 7)
        c = a - d
        ans = f"a_n = {d}n {'+' if c >= 0 else '−'} {abs(c)}" if c else f"a_n = {d}n"
        return Q("multiple-choice", f"Use iteration to find an explicit formula for a₁ = {a}, a_n = a_(n−1) + {d}.", ans,
                 [f"a₂ = {a} + {d}, a₃ = {a} + 2·{d}, …, a_n = {a} + (n − 1)·{d}.", f"Simplify: {ans}."], "iteration_formula",
                 [f"a_n = {a}n + {d}", f"a_n = {d}n + {a}", f"a_n = {a}·{d}ⁿ"])
    a, m = r.randint(2, 9), r.choice([3, 4, 5])
    ans = f"a_n = {a}·{m}ⁿ"
    return Q("multiple-choice", f"Use iteration to find an explicit formula for a₀ = {a}, a_n = {m}a_(n−1).", ans,
             [f"a₁ = {m}·{a}, a₂ = {m}²·{a}, …, each step multiplies by {m}.", f"So a_n = {a}·{m}ⁿ."], "iteration_formula", [f"a_n = {m}·{a}ⁿ", f"a_n = {a} + {m}n", f"a_n = {a}·{m}ⁿ⁻¹"])


IND = [("2 + 4 + … + 2n = n(n + 1)", "2 + 4 + … + 2k + 2(k + 1) = (k + 1)(k + 2)", "n = 1: 2 = 1(2)"),
       ("1² + 2² + … + n² = n(n + 1)(2n + 1)/6", "1² + … + k² + (k + 1)² = (k + 1)(k + 2)(2k + 3)/6", "n = 1: 1 = 1(2)(3)/6"),
       ("1 + 2 + 4 + … + 2ⁿ⁻¹ = 2ⁿ − 1", "1 + 2 + … + 2ᵏ⁻¹ + 2ᵏ = 2ᵏ⁺¹ − 1", "n = 1: 1 = 2¹ − 1"),
       ("3 + 7 + 11 + … + (4n − 1) = n(2n + 1)", "3 + 7 + … + (4k − 1) + (4k + 3) = (k + 1)(2k + 3)", "n = 1: 3 = 1(3)"),
       ("1 + 3 + 9 + … + 3ⁿ⁻¹ = (3ⁿ − 1)/2", "1 + 3 + … + 3ᵏ⁻¹ + 3ᵏ = (3ᵏ⁺¹ − 1)/2", "n = 1: 1 = (3 − 1)/2")]


def sq07(r):
    i = r.randrange(len(IND))
    s, step, base = IND[i]
    kind = r.choice(["step", "base"])
    others = [IND[j] for j in range(len(IND)) if j != i]
    if kind == "step":
        return Q("multiple-choice", f"In an induction proof of \"{s}\", what must be shown in the inductive step (assuming P(k))?", step,
                 ["The inductive step assumes P(k) and proves P(k + 1).", f"P(k + 1) adds the next term and replaces n by k + 1 on the right: {step}."], "induction_step",
                 [o[1] for o in r.sample(others, 2)] + [s.replace("n", "k")])
    return Q("multiple-choice", f"What is the base case for an induction proof of \"{s}\"?", base,
             ["The base case checks the first value of n, here n = 1.", f"Both sides agree: {base}."], "induction_base", [o[2] for o in r.sample(others, 3)])


def sq09(r):
    kind = r.choice(["L", "plus", "hex", "stair"])
    n = r.randint(6, 15)
    f, desc, form = {"L": (lambda n: 2 * n - 1, "an L shape with n tiles in each arm (sharing the corner tile)", "2n − 1"),
                     "plus": (lambda n: 4 * n + 1, "a plus sign with a center tile and n tiles on each of its four arms", "4n + 1"),
                     "hex": (lambda n: 5 * n + 1, "a row of n hexagons made of toothpicks, neighbors sharing a side", "5n + 1"),
                     "stair": (lambda n: n * (n + 1) // 2, "a staircase of columns with heights 1, 2, …, n tiles", "n(n + 1)/2")}[kind]
    return Q("multiple-choice", f"Figure n is {desc}. How many tiles (or toothpicks) are in figure {n}?", str(f(n)),
             [f"Count the first figures and find the rule: {form}.", f"For n = {n}: {f(n)}."], "pattern_count", [str(f(n) + 1), str(f(n - 1)), str(f(n) + n)])


# ---------------------------------------------------------------- sets
def st01(r):
    pairs = [("{1, 2, 2, 3}", "{3, 2, 1}", True), ("{∅}", "∅", False), ("{x ∈ ℤ | x² = 4}", "{−2, 2}", True), ("{x ∈ ℤ | x² = 4}", "{2}", False),
             ("{a, b, c}", "{c, b, a, a}", True), ("{1, {2}}", "{1, 2}", False), ("{n ∈ ℕ | n < 1}", "∅", True), ("{0}", "{∅}", False), ("{2, 4, 6}", "{n ∈ ℕ | n is even and n ≤ 6}", True)]
    a, b, eq = r.choice(pairs)
    ans = "Yes: they have exactly the same elements" if eq else "No: one set has an element the other does not"
    return Q("multiple-choice", f"Are the sets {a} and {b} equal?", ans,
             ["Two sets are equal when they have exactly the same elements; order and repetition do not matter.", "Compare the elements of each set.", f"Answer: {ans}."], "set_equality",
             ["Yes: they have exactly the same elements", "No: one set has an element the other does not", "No: the elements are listed in a different order", "Yes: they have the same number of elements"])


def st02(r):
    A, B = set(r.sample(range(1, 13), 5)), set(r.sample(range(1, 13), 5))
    op = r.choice(["∪", "∩", "−"])
    v = {"∪": A | B, "∩": A & B, "−": A - B}[op]
    return Q("short-answer", f"Let A = {roster(A)} and B = {roster(B)}. Find A {op} B. Write the set in roster notation, elements in increasing order (∅ if empty).", roster(v),
             [{"∪": "The union holds elements in A or B (or both).", "∩": "The intersection holds elements in both A and B.", "−": "A − B holds elements of A that are not in B."}[op], f"A {op} B = {roster(v)}."], "set_ops")


def st02_h(r):
    A, B, C = (set(r.sample(range(1, 11), 5)) for _ in range(3))
    expr, v = r.choice([("(A − B) ∪ (B − A)", (A - B) | (B - A)), ("(A ∪ B) − C", (A | B) - C), ("A ∩ (B ∪ C)", A & (B | C)), ("(A ∩ B) ∪ (A ∩ C)", (A & B) | (A & C)), ("A − (B ∩ C)", A - (B & C))])
    return Q("short-answer", f"Let A = {roster(A)}, B = {roster(B)} and C = {roster(C)}. Find {expr}. Write the set in roster notation, in increasing order (∅ if empty).", roster(v),
             ["Work inside the parentheses first.", f"{expr} = {roster(v)}."], "three_set_ops_h")


def st03_h(r):
    U = set(range(1, 11))
    A, B, C = (set(r.sample(range(1, 11), r.randint(3, 5))) for _ in range(3))
    expr, v = r.choice([("(A ∩ B)' ∩ C", (U - (A & B)) & C), ("A' ∪ (B ∩ C)", (U - A) | (B & C)), ("(A ∪ C)' ∩ B'", (U - (A | C)) & (U - B)), ("(A − B)' ∩ C", (U - (A - B)) & C)])
    return Q("short-answer", f"Universe U = {{1, 2, …, 10}}. Let A = {roster(A)}, B = {roster(B)} and C = {roster(C)}. Find {expr}. Use roster notation, ordered, ∅ if empty.", roster(v),
             ["Complements are taken in U; evaluate inner expressions first.", f"{expr} = {roster(v)}."], "complement_three_h")


def st04(r):
    n, a, b = r.randint(30, 60), r.randint(8, 25), r.randint(8, 25)
    c = r.randint(2, min(a, b) - 1)
    need(a + b - c <= n)
    return Q("short-answer", f"In a class of {n} students, {a} play soccer, {b} play basketball and {c} play both. How many play neither sport?", str(n - (a + b - c)),
             [f"Draw a two-circle Venn diagram: both {c}, soccer only {a - c}, basketball only {b - c}.", f"At least one sport: {a} + {b} − {c} = {a + b - c}. Neither: {n} − {a + b - c} = {n - (a + b - c)}."], "venn_two")


def st04_h(r):
    for _ in range(500):
        sizes = {k: r.randint(1, 12) for k in ("A", "B", "C", "AB", "AC", "BC", "ABC")}
        A = sizes["A"] + sizes["AB"] + sizes["AC"] + sizes["ABC"]
        B = sizes["B"] + sizes["AB"] + sizes["BC"] + sizes["ABC"]
        C = sizes["C"] + sizes["AC"] + sizes["BC"] + sizes["ABC"]
        AB, AC, BC, ABC = sizes["AB"] + sizes["ABC"], sizes["AC"] + sizes["ABC"], sizes["BC"] + sizes["ABC"], sizes["ABC"]
        union = sum(sizes.values())
        N = union + r.randint(0, 15)
        break
    ask = r.choice(["union", "neither", "exactly_one"])
    v = {"union": union, "neither": N - union, "exactly_one": sizes["A"] + sizes["B"] + sizes["C"]}[ask]
    q = {"union": "How many students take at least one of the three?", "neither": "How many students take none of the three?", "exactly_one": "How many students take exactly one of the three?"}[ask]
    return Q("short-answer", f"Of {N} students, {A} take art (A), {B} take band (B) and {C} take chorus (C). {AB} take A and B, {AC} take A and C, {BC} take B and C, and {ABC} take all three. {q}", str(v),
             [f"Inclusion–exclusion: |A ∪ B ∪ C| = {A} + {B} + {C} − {AB} − {AC} − {BC} + {ABC} = {union}.",
              f"Fill the Venn regions from the center out: all three {ABC}; exactly two: {sizes['AB']}, {sizes['AC']}, {sizes['BC']}; only one: {sizes['A']}, {sizes['B']}, {sizes['C']}.", f"Answer: {v}."], "venn_three_h")


def st05_h(r):
    kind = r.choice(["contains", "ppset", "size"])
    if kind == "contains":
        n = r.randint(4, 7)
        S = list("abcdefg"[:n])
        v = 2 ** (n - 2)
        return Q("short-answer", f"How many subsets of {{{', '.join(S)}}} contain a but do not contain b?", str(v),
                 ["a must be in and b must be out; each of the other elements is free (in or out).", f"There are {n - 2} free elements, so 2^{n - 2} = {v} subsets."], "power_set_count_h")
    if kind == "ppset":
        n = r.choice([1, 2])
        v = 2 ** (2 ** n)
        return Q("short-answer", f"How many elements does P(P(S)) have if S has {n} element{'s' if n > 1 else ''}?", str(v),
                 [f"P(S) has 2^{n} = {2 ** n} elements.", f"P(P(S)) has 2^{2 ** n} = {v} elements."], "power_set_count_h")
    n, k = r.randint(5, 8), r.randint(2, 3)
    return Q("short-answer", f"A set S has {n} elements. How many elements of P(S) are subsets of size {k}?", str(math.comb(n, k)),
             [f"Each {k}-element subset is a choice of {k} elements from {n}.", f"C({n}, {k}) = {math.comb(n, k)}."], "power_set_count_h")


SETFALSE = [("For all sets A and B, A ∩ B = A.", lambda A, B: A & B == A), ("For all sets A and B, A ∪ B = B.", lambda A, B: A | B == B),
            ("For all sets A and B, (A − B) ∪ B = A.", lambda A, B: (A - B) | B == A), ("For all sets A and B, if A ⊆ B then A = B.", lambda A, B: (not A <= B) or A == B),
            ("For all sets A and B, A − B = ∅.", lambda A, B: A - B == set()), ("For all sets A and B, A ∩ B ≠ ∅.", lambda A, B: bool(A & B))]
CANDS = [(set(), {1}), ({1}, set()), ({1}, {1}), ({1}, {1, 2}), ({1, 2}, {2}), ({1}, {2}), ({1, 2}, {1, 2})]


def stxt(A, B):
    t = lambda S: roster(S)
    return f"A = {t(A)}, B = {t(B)}"


def st08(r):
    s, test = r.choice(SETFALSE)
    bad = [c for c in CANDS if not test(*c)]
    good = [c for c in CANDS if test(*c)]
    need(bad and len(good) >= 3)
    ans = r.choice(bad)
    return Q("multiple-choice", f"Which choice is a counterexample to the false statement \"{s}\"?", stxt(*ans),
             ["A counterexample is one specific choice of sets that makes the statement false.", f"With {stxt(*ans)} the statement fails; check it directly.", "Each other choice makes the statement true."],
             "set_counterexample", [stxt(*c) for c in r.sample(good, 3)])


def st08_h(r):
    s, test = r.choice([("For all sets A, B, C: A − (B − C) = (A − B) − C.", lambda A, B, C: A - (B - C) == (A - B) - C),
                        ("For all sets A, B, C: A ∪ (B ∩ C) = (A ∪ B) ∩ C.", lambda A, B, C: A | (B & C) == (A | B) & C),
                        ("For all sets A, B, C: if A ∪ C = B ∪ C, then A = B.", lambda A, B, C: (A | C != B | C) or A == B)])
    trip = [(set(), set(), set()), ({1}, {1}, {1}), ({1}, set(), {1}), ({1}, {1}, set()), (set(), {1}, {1}), ({1}, {2}, {1, 2}), ({1, 2}, {1}, {2}), ({1}, {1, 2}, {2})]
    bad = [t for t in trip if not test(*t)]
    good = [t for t in trip if test(*t)]
    need(bad and len(good) >= 3)
    ans = r.choice(bad)
    tx = lambda t: f"A = {roster(t[0])}, B = {roster(t[1])}, C = {roster(t[2])}"
    return Q("multiple-choice", f"The statement \"{s}\" is false. Which three sets disprove it?", tx(ans),
             ["Test each choice by computing both sides.", f"For {tx(ans)} the two sides differ (or the hypothesis holds and the conclusion fails).", "The other choices satisfy the statement, so they do not disprove it."],
             "set_counterexample_h", [tx(t) for t in r.sample(good, 3)])


# ---------------------------------------------------------------- speaking mathematically
SENT = [("\"Every square is a rectangle.\"", "A statement that is true"), ("\"7 is an even number.\"", "A statement that is false"), ("\"Find the value of y.\"", "Not a statement: it is a question or a command"),
        ("\"2n + 1 = 9\"", "Not a statement: its truth depends on the value of a variable"), ("\"The sum of two odd numbers is odd.\"", "A statement that is false"), ("\"Is 0 an integer?\"", "Not a statement: it is a question or a command"),
        ("\"There are 12 months in a year.\"", "A statement that is true"), ("\"y < 4\"", "Not a statement: its truth depends on the value of a variable")]


def sm01(r):
    s, ans = r.choice(SENT)
    return Q("multiple-choice", f"Classify the sentence. (A statement is a sentence that is true or false, but not both.)\n{s}", ans,
             ["Ask: is the sentence a complete claim that is either true or false?", f"{s}: {ans.lower()}."], "statement_class",
             ["A statement that is true", "A statement that is false", "Not a statement: it is a question or a command", "Not a statement: its truth depends on the value of a variable"])


IFTHEN = [("We cancel the picnic whenever it rains.", "If it rains, then we cancel the picnic."), ("A number divisible by 9 is divisible by 3.", "If a number is divisible by 9, then it is divisible by 3."),
          ("All rhombuses have four equal sides.", "If a figure is a rhombus, then it has four equal sides."), ("The dog barks when the doorbell rings.", "If the doorbell rings, then the dog barks.")]


def sm03(r):
    s, ans = r.choice(IFTHEN)
    parts = ans[3:-1].split(", then ")
    return Q("multiple-choice", f"Rewrite in \"if p, then q\" form: \"{s}\"", ans,
             ["Find the condition (hypothesis) and the result (conclusion).", f"Hypothesis: {parts[0]}; conclusion: {parts[1]}. So: {ans}"], "if_then_form",
             [f"If {parts[1]}, then {parts[0]}.", f"{cap(parts[0])} and {parts[1]}.", f"{cap(parts[0])} if and only if {parts[1]}."])


NS = [("p", "q")]
NEC = [("Being a resident is necessary for voting in the town election.", "If a person votes in the town election, then the person is a resident."),
       ("Scoring 90 or more is sufficient for an A.", "If a student scores 90 or more, then the student gets an A."),
       ("A triangle is equilateral only if it is isosceles.", "If a triangle is equilateral, then it is isosceles."),
       ("The meeting starts on time unless the speaker is late.", "If the speaker is not late, then the meeting starts on time."),
       ("Having a ticket is necessary for entering the concert.", "If a person enters the concert, then the person has a ticket."),
       ("Paying the fee is sufficient for joining the club.", "If a person pays the fee, then the person can join the club."),
       ("A number is divisible by 10 only if it ends in 0.", "If a number is divisible by 10, then it ends in 0."),
       ("The game is played unless it storms.", "If it does not storm, then the game is played.")]


def sm03_h(r):
    s, ans = r.choice(NEC)
    hyp, con = ans[3:-1].split(", then ")
    word = "necessary" if "necessary" in s else ("sufficient" if "sufficient" in s else ("only if" if "only if" in s else "unless"))
    rule = {"necessary": "\"p is necessary for q\" means \"if q, then p\".", "sufficient": "\"p is sufficient for q\" means \"if p, then q\".",
            "only if": "\"p only if q\" means \"if p, then q\".", "unless": "\"p unless q\" means \"if not q, then p\"."}[word]
    return Q("multiple-choice", f"Which conditional has the same meaning as \"{s}\"?", ans,
             [rule, f"So the statement means: {ans}"], "necessary_sufficient_h", [f"If {con}, then {hyp}.", f"If {hyp}, then it is not true that {con}.", f"{cap(hyp)} if and only if {con}."])


def sm04_h(r):
    S, ans, wr = r.choice([("{3, 6, 9, 12, 15}", "{3k | k ∈ ℤ and 1 ≤ k ≤ 5}", ["{k + 3 | k ∈ ℤ and 1 ≤ k ≤ 5}", "{3k | k ∈ ℤ and 0 ≤ k ≤ 5}", "{n ∈ ℤ | 3 ≤ n ≤ 15}"]),
                           ("{1, 4, 9, 16}", "{k² | k ∈ ℤ and 1 ≤ k ≤ 4}", ["{2k | k ∈ ℤ and 1 ≤ k ≤ 4}", "{k² | k ∈ ℤ and 0 ≤ k ≤ 4}", "{n ∈ ℤ | 1 ≤ n ≤ 16}"]),
                           ("{−1, 1, 3, 5}", "{2k + 1 | k ∈ ℤ and −1 ≤ k ≤ 2}", ["{2k − 1 | k ∈ ℤ and −1 ≤ k ≤ 2}", "{2k + 1 | k ∈ ℤ and 0 ≤ k ≤ 3}", "{n ∈ ℤ | −1 ≤ n ≤ 5}"]),
                           ("{2, 4, 8, 16, 32}", "{2ᵏ | k ∈ ℤ and 1 ≤ k ≤ 5}", ["{2k | k ∈ ℤ and 1 ≤ k ≤ 5}", "{2ᵏ | k ∈ ℤ and 0 ≤ k ≤ 5}", "{k² | k ∈ ℤ and 1 ≤ k ≤ 5}"])])
    return Q("multiple-choice", f"Which set-builder description equals {S}?", ans,
             ["Generate each candidate's elements and compare with the roster.", f"{ans} produces exactly {S}."], "set_builder_match_h", wr)


def sm05_h(r):
    A, x, ans, wr = r.choice([("{1, {1}, {1, 2}}", "{1}", "Both: {1} ∈ A and {1} ⊆ A", ["Only {1} ∈ A", "Only {1} ⊆ A", "Neither"]),
                              ("{∅, {2}, 3}", "∅", "Both: ∅ ∈ A and ∅ ⊆ A", ["Only ∅ ⊆ A", "Only ∅ ∈ A", "Neither"]),
                              ("{{2}, 3}", "{3}", "Only {3} ⊆ A", ["Both: {3} ∈ A and {3} ⊆ A", "Only {3} ∈ A", "Neither"]),
                              ("{1, 2, {3}}", "{3}", "Only {3} ∈ A", ["Both: {3} ∈ A and {3} ⊆ A", "Only {3} ⊆ A", "Neither"]),
                              ("{{1, 2}, 3}", "{1, 2}", "Only {1, 2} ∈ A", ["Both: {1, 2} ∈ A and {1, 2} ⊆ A", "Only {1, 2} ⊆ A", "Neither"])])
    return Q("multiple-choice", f"Let A = {A}. Which is true about X = {x}: is X ∈ A (X is an element), is X ⊆ A (every element of X is in A), both, or neither?", ans,
             ["X ∈ A asks whether X itself is listed as an element of A.", "X ⊆ A asks whether each element of X is an element of A (∅ is a subset of every set).", f"So: {ans}."], "member_subset_h", wr)


def sm06_h(r):
    A = sorted(r.sample(range(1, 9), r.randint(3, 4)))
    B = sorted(r.sample(range(1, 9), r.randint(3, 4)))
    k = sum(1 for a in A for b in B if a < b)
    return Q("short-answer", f"Let A = {roster(A)} and B = {roster(B)}. How many ordered pairs (a, b) in A × B have a < b?", str(k),
             [f"A × B has {len(A)} · {len(B)} = {len(A) * len(B)} pairs.", "For each a, count the b's larger than a: " + ", ".join(f"{a}: {sum(1 for b in B if a < b)}" for a in A) + f". Total {k}."], "cartesian_count_h")


def sm07_h(r):
    n, k = r.randint(4, 7), r.randint(1, 3)
    kind = r.choice(["exact", "start"])
    if kind == "exact":
        return Q("short-answer", f"How many strings of length {n} over the alphabet {{a, b}} contain exactly {k} a's?", str(math.comb(n, k)),
                 [f"Choose which {k} of the {n} positions hold a; the rest are b.", f"C({n}, {k}) = {math.comb(n, k)}."], "string_count_h")
    m = r.choice([2, 3])
    v = m ** (n - 2)
    return Q("short-answer", f"How many strings of length {n} over the alphabet {{{', '.join('xyz'[:m])}}} begin with xy?", str(v),
             [f"The first two characters are fixed; each of the other {n - 2} positions has {m} choices.", f"{m}^{n - 2} = {v}."], "string_count_h")


# skill -> (cp2/cp1 family, honors family)
FAMILIES = {
    "compound-statements-logic-skill-04": (lg04, lg04_h), "compound-statements-logic-skill-05": (lg05, lg05_h), "compound-statements-logic-skill-06": (lg06, lg06_h),
    "compound-statements-logic-skill-07": (lg07, lg07_h), "compound-statements-logic-skill-08": (lg08, lg08_h),
    "counting-probability-skill-01": (cn01, cn01_h), "counting-probability-skill-03": (cn03, cn03_h), "counting-probability-skill-04": (cn04, None), "counting-probability-skill-05": (cn05, None),
    "counting-probability-skill-06": (cn06, cn06_h), "counting-probability-skill-07": (cn07, cn07_h), "counting-probability-skill-08": (cn08, cn08_h),
    "election-theory-skill-03": (el03, el03_h), "election-theory-skill-06": (el06, el06_h), "election-theory-skill-08": (el08, el08_h),
    "graphs-trees-skill-01": (None, gr01_h), "graphs-trees-skill-02": (gr02, gr02_h), "graphs-trees-skill-04": (gr04, gr04_h), "graphs-trees-skill-05": (gr05, gr05_h), "graphs-trees-skill-06": (gr06, gr06_h),
    "linear-programming-skill-01": (lp01, lp01_h), "linear-programming-skill-04": (None, lp04_h), "linear-programming-skill-06": (lp06, lp06_h), "linear-programming-skill-07": (lp07, lp07_h),
    "number-theory-proof-skill-03": (np03, np03_h), "number-theory-proof-skill-08": (np08, np08_h),
    "properties-relations-skill-01": (None, rl01_h), "properties-relations-skill-05": (rl05, rl05_h), "properties-relations-skill-06": (rl06, None), "properties-relations-skill-07": (None, rl07_h),
    "sequences-induction-recursion-skill-01": (sq01, None), "sequences-induction-recursion-skill-02": (sq02, None), "sequences-induction-recursion-skill-03": (sq03, sq03_h),
    "sequences-induction-recursion-skill-04": (sq04, None), "sequences-induction-recursion-skill-05": (sq05, None), "sequences-induction-recursion-skill-06": (sq06, None),
    "sequences-induction-recursion-skill-07": (sq07, None), "sequences-induction-recursion-skill-09": (sq09, None),
    "set-theory-skill-01": (st01, None), "set-theory-skill-02": (st02, st02_h), "set-theory-skill-03": (None, st03_h), "set-theory-skill-04": (st04, st04_h), "set-theory-skill-05": (None, st05_h),
    "set-theory-skill-08": (st08, st08_h),
    "speaking-mathematically-skill-01": (sm01, None), "speaking-mathematically-skill-03": (sm03, sm03_h), "speaking-mathematically-skill-04": (None, sm04_h),
    "speaking-mathematically-skill-05": (None, sm05_h), "speaking-mathematically-skill-06": (None, sm06_h), "speaking-mathematically-skill-07": (None, sm07_h),
}
