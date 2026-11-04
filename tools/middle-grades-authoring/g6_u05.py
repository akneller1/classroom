"""Grade 6 Unit 5 — Inequalities (inequalities)."""
from glib import *
import g7_u02 as E7

UNIT_ID = "inequalities"
ABBR = "ineq"
FLIP = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}
OC = {"<": "≤", ">": "≥", "≤": "<", "≥": ">"}


# ============================================================== S1 Inequalities
@fam("012", mode="mc")
def s1_meaning(r, L):
    op = pick(r, ["<", ">", "≤", "≥"])
    words = {"<": "is less than", ">": "is greater than", "≤": "is less than or equal to", "≥": "is greater than or equal to"}
    b = r.randint(-10, 30)
    v = pick(r, ["x", "t", "n"])
    good = f"{v} {words[op]} {b}"
    opts = [(good, True)] + [(f"{v} {words[o]} {b}", False) for o in (FLIP[op], OC[op], FLIP[OC[op]])]
    r.shuffle(opts)
    return Q(f"Which statement means the same as {v} {op} {b}?", good, ["< less than; > greater than; ≤ less than or equal to; ≥ greater than or equal to.", f"{v} {op} {b}: {good}."],
             options=opts, chk=TXT(good), mode="mc")


# ============================================================== S2 Solving one-variable inequalities (positive coefficients, rational numbers)
@fam("012")
def s2_solve(r, L):
    v = pick(r, ["x", "n", "y", "m"])
    op = pick(r, ["<", ">", "≤", "≥"])
    if L == 0:
        x, a = r.randint(1, 30), r.randint(2, 20)
    elif L == 1:
        x, a = F(r.randint(1, 40), pick(r, [1, 2, 10])), F(r.randint(1, 30), pick(r, [1, 2, 10]))
    else:
        x, a = F(r.randint(1, 40), pick(r, [3, 4, 5])), F(r.randint(2, 20), pick(r, [3, 4, 5]))
    if r.random() < 0.5:
        full = f"{v} + {N(a)} {op} {N(F(x) + F(a))}"
        wr = [f"{v} {op} {N(F(x) + 2 * F(a))}", f"{v} {FLIP[op]} {N(x)}", f"{v} {op} {N(F(x) + F(a))}"]
        why = ["Added instead of subtracting", "Reversed the sign unnecessarily", "Did not undo the addition"]
        st = [f"Subtract {N(a)} from both sides.", f"{v} {op} {N(F(x) + F(a))} - {N(a)}.", f"{v} {op} {N(x)}."]
    else:
        need(F(a) != 1)
        full = f"{N(a)}{v} {op} {N(F(x) * F(a))}" if F(a).denominator == 1 else f"({N(a)}){v} {op} {N(F(x) * F(a))}"
        wr = [f"{v} {op} {N(F(x) * F(a) * F(a))}", f"{v} {FLIP[op]} {N(x)}", f"{v} {op} {N(F(x) * F(a) - F(a))}"]
        why = ["Multiplied instead of dividing", "Reversed the sign when dividing by a positive number", "Subtracted instead of dividing"]
        st = [f"Divide both sides by {N(a)} (a positive number, so the sign stays).", f"{v} {op} {N(x)}."]
    return Q(f"Solve: {full}", f"{v} {op} {N(x)}", st + ["Check a value in the solution set."], wr, PY("ineq", ineq=full, var=v), why=why)


# ============================================================== S3 Solutions of inequalities
@fam("012")
def s3_select(r, L):
    b = r.randint(-5, 12)
    op = pick(r, ["<", ">", "≤", "≥"])
    vals = sorted(r.sample(range(b - 6, b + 7), 6) + ([b] if r.random() < 0.6 else []))
    vals = sorted(set(vals))
    good = [x for x in vals if {"<": x < b, ">": x > b, "≤": x <= b, "≥": x >= b}[op]]
    need(2 <= len(good) < len(vals))
    return Q(f"Which of these values are solutions of x {op} {b}? {', '.join(map(str, vals))}. List them in order.", ", ".join(map(str, good)),
             [f"Test each value in x {op} {b}.", f"{'Include' if op in ('≤', '≥') else 'Do not include'} {b} itself.", f"Solutions: {', '.join(map(str, good))}."],
             [", ".join(map(str, [x for x in vals if x not in good])), ", ".join(map(str, [x for x in vals if {'<': x <= b, '>': x >= b, '≤': x < b, '≥': x > b}[op]])), ", ".join(map(str, vals))],
             PY("sol_list", ineq=f"x {op} {b}", vals=vals), why=["Chose the values on the wrong side", "Included or excluded the boundary incorrectly", "Listed every value"])


@fam("12", mode="mc")
def s3_true_false(r, L):
    b = r.randint(-8, 8)
    op = pick(r, ["<", ">", "≤", "≥"])
    good = r.choice([x for x in range(b - 8, b + 9) if {"<": x < b, ">": x > b, "≤": x <= b, "≥": x >= b}[op]])
    bads = r.sample([x for x in range(b - 8, b + 9) if not {"<": x < b, ">": x > b, "≤": x <= b, "≥": x >= b}[op]], 3)
    opts = [(str(good), True)] + [(str(x), False) for x in bads]
    r.shuffle(opts)
    return Q(f"Which number is a solution of x {op} {b}?", str(good), [f"Substitute each choice into x {op} {b}.", f"{good} {op} {b} is true."], options=opts, chk=PY("in_ineq", ineq=f"x {op} {b}"), mode="mc")


@fam("2")
def s3_infinite(r, L):
    b = r.randint(-5, 10)
    op = pick(r, ["<", ">"])
    v = F(2 * b + (1 if op == ">" else -1), 2)
    return Q(f"Give a solution of x {op} {b} that is not a whole number.", mixed(v) if v.denominator > 1 else N(v), [f"Any number {'greater' if op == '>' else 'less'} than {b} works, including fractions and decimals.", f"For example, {mixed(v)}."],
             [str(b), mixed(F(2 * b + (-1 if op == ">" else 1), 2)), str(b + (1 if op == ">" else -1))], PY("in_ineq_nonwhole", ineq=f"x {op} {b}"), why=["Used the boundary", "Chose a value on the wrong side", "Gave a whole number"], tags=["reasoning"])


SKILLS = {
    1: dict(name="Inequalities", std=["6.EE.B.8"], fams=[reuse(E7.s8_words), s1_meaning, reuse(E7.s8_check)], extra=[err_of(reuse(E7.s8_words, (0, 1, 2), "e")), open_of(reuse(E7.s8_words, (0, 1, 2), "o"))]),
    2: dict(name="Solving One-Variable Inequalities", std=["6.EE.B.8", "6.EE.B.5"], fams=[s2_solve, reuse(E7.s9_solve, (0, 0, 0)), reuse(E7.s10_solve, (0, 0, 0))], extra=[err_of(s2_solve), open_of(s2_solve), select_of(s2_solve)]),
    3: dict(name="Solutions of Inequalities", std=["6.EE.B.5"], fams=[s3_select, s3_true_false, reuse(E7.s8_check, (0, 1, 2), "b"), s3_infinite], extra=[err_of(s3_select), open_of(reuse(E7.s8_check, (0, 1, 2), "o"))]),
    4: dict(name="Solutions of Inequalities on the Number Line", std=["6.EE.B.8"], fams=[reuse(E7.s8_from_graph), reuse(E7.s8_choose_graph, (1, 1, 2))], extra=[err_of(reuse(E7.s8_from_graph, (0, 1, 2), "e")), err_of(reuse(E7.s8_from_graph, (0, 1, 2), "f"))]),
    5: dict(name="Applications of Inequalities", std=["6.EE.B.8"], fams=[reuse(E7.s9_context), reuse(E7.s10_context), reuse(E7.s8_words, (1, 1, 2), "c")], extra=[err_of(reuse(E7.s10_context, (0, 1, 2), "e")), open_of(reuse(E7.s9_context, (0, 1, 2), "o"))]),
}
