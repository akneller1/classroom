"""Algebra 2 Unit 11 — Probability and Statistics (probability-statistics). Top-up families."""
from hslib import *
import math
import pc_u08 as P8

UNIT_ID = "probability-statistics"
ABBR = "ps"


# ============================================================== S1 Counting principles and permutations
@fam("012")
def s1_perm(r, L):
    kind = pick(r, ["arrange", "perm", "fcp"]) if L else pick(r, ["arrange", "fcp"])
    if kind == "arrange":
        n_ = rint(r, 4, 8)
        who = pick(r, ["books be arranged on a shelf", "runners line up", "songs be played in a playlist", "students sit in a row"])
        v = math.factorial(n_)
        return Q(f"In how many different orders can {n_} {who}?", str(v), [f"Use {n_}! = {' · '.join(str(i) for i in range(n_, 0, -1))}.", f"= {v}."],
                 [str(n_ * n_), str(sum(range(1, n_ + 1))), str(2 ** n_)], H(f"factorial({n_})"), why=["Squared the number of items", "Added instead of multiplying", "Used 2ⁿ"])
    if kind == "perm":
        n_, k_ = rint(r, 6, 12), rint(r, 2, 4)
        v = math.perm(n_, k_)
        role = pick(r, [("a president, vice president, and secretary", 3), ("first, second, and third place", 3), ("a captain and co-captain", 2), ("4 different officer positions", 4)])
        k_ = role[1]
        v = math.perm(n_, k_)
        return Q(f"From {n_} people, how many ways can {role[0]} be chosen?", str(v), [f"Order matters, so use ₙPᵣ = {n_}! ÷ ({n_} - {k_})!.", f"= {' · '.join(str(n_ - i) for i in range(k_))} = {v}."],
                 [str(math.comb(n_, k_)), str(n_ ** k_), str(n_ * k_)], H(f"factorial({n_})/factorial({n_} - {k_})"),
                 why=["Used combinations even though order matters", "Allowed one person to fill more than one role", "Multiplied n by r"])
    a, b, c = rint(r, 2, 6), rint(r, 2, 5), rint(r, 2, 4)
    item = pick(r, [("shirts", "pants", "pairs of shoes", "outfits"), ("appetizers", "entrées", "desserts", "meals"), ("crusts", "sauces", "toppings", "pizzas")])
    v = a * b * c
    return Q(f"There are {a} {item[0]}, {b} {item[1]}, and {c} {item[2]}. How many different {item[3]} use one of each?", str(v), ["Fundamental counting principle: multiply the choices.", f"{a} · {b} · {c} = {v}."],
             [str(a + b + c), str(a * b + c), str(math.comb(a + b + c, 3))], H(f"{a}*{b}*{c}"), why=["Added the choices", "Multiplied only two of the choices", "Used combinations of all the items together"])


# ============================================================== S2 Combinations
@fam("012")
def s2_comb(r, L):
    n_, k_ = rint(r, 5, 15), rint(r, 2, 5)
    need(k_ < n_)
    ctx = pick(r, [("a committee of {k} from {n} students", ""), ("{k} toppings from {n} available toppings", ""), ("{k} books to read from a list of {n}", ""), ("a team of {k} players from {n} players", "")])[0]
    v = math.comb(n_, k_)
    ask = ctx.format(k=k_, n=n_)
    if L == 2 and r.random() < 0.5:
        m_ = rint(r, 3, 8)
        k2 = rint(r, 1, 3)
        need(k2 <= m_)
        v = math.comb(n_, k_) * math.comb(m_, k2)
        return Q(f"A club has {n_} juniors and {m_} seniors. How many ways can a group of {k_} juniors and {k2} seniors be chosen?", str(v),
                 [f"Juniors: ₙCᵣ = C({n_}, {k_}) = {math.comb(n_, k_)}.", f"Seniors: C({m_}, {k2}) = {math.comb(m_, k2)}.", f"Multiply: {v}."],
                 [str(math.comb(n_, k_) + math.comb(m_, k2)), str(math.comb(n_ + m_, k_ + k2)), str(math.perm(n_, k_) * math.perm(m_, k2))], H(f"binomial({n_}, {k_})*binomial({m_}, {k2})"),
                 why=["Added the two counts", "Ignored the class restriction", "Used permutations even though order does not matter"])
    return Q(f"How many ways can you choose {ask}?", str(v), ["Order does not matter, so use ₙCᵣ = n! ÷ (r!(n - r)!).", f"C({n_}, {k_}) = {v}."],
             [str(math.perm(n_, k_)), str(n_ * k_), str(math.comb(n_, k_ - 1)) if math.comb(n_, k_ - 1) != v else str(v + n_)], H(f"binomial({n_}, {k_})"),
             why=["Used permutations even though order does not matter", "Multiplied n by r", "Used r - 1 instead of r"])


# ============================================================== S4 Conditional probability
@fam("012")
def s4_cond(r, L):
    pB = sp.Rational(rint(r, 2, 9), 10)
    pAB = sp.Rational(rint(r, 1, int(pB * 10) - 1), 10) if pB > sp.Rational(1, 10) else sp.Rational(1, 20)
    v = pAB / pB
    a_ev, b_ev = pick(r, [("a student plays a sport", "the student takes art"), ("a customer buys a drink", "the customer buys a sandwich"), ("it rains", "it is cloudy"), ("a car is red", "the car is an SUV")])
    return Q(f"P({b_ev}) = {D(F(pB.p, pB.q))} and P({a_ev} and {b_ev}) = {D(F(pAB.p, pAB.q))}. Find the probability that {a_ev}, given that {b_ev}.", T(v),
             ["P(A | B) = P(A and B) ÷ P(B).", f"= {D(F(pAB.p, pAB.q))} ÷ {D(F(pB.p, pB.q))} = {T(v)}."],
             [T(pAB * pB), T(pB / pAB), D(F(pAB.p, pAB.q))], H(f"nsimplify('{D(F(pAB.p, pAB.q))}')/nsimplify('{D(F(pB.p, pB.q))}')"),
             why=["Multiplied instead of dividing", "Divided in the wrong order", "Gave P(A and B) instead of the conditional probability"])


# ============================================================== S5 Probability distributions
@fam("012")
def s5_missing(r, L):
    k_ = rint(r, 3, 5)
    ps = [sp.Rational(rint(r, 5, 30), 100) for _ in range(k_ - 1)]
    need(sum(ps) < sp.Rational(95, 100))
    miss = 1 - sum(ps)
    xs = list(range(k_))
    i = r.randrange(k_)
    allp = ps[:i] + [miss] + ps[i:]
    tbl = "; ".join(f"P(X = {xv}) = {'p' if j == i else D(F(pv.p, pv.q))}" for j, (xv, pv) in enumerate(zip(xs, allp)))
    return Q(f"A probability distribution has {tbl}. Find p.", D(F(miss.p, miss.q)), ["The probabilities in a distribution add to 1.", f"p = 1 - ({' + '.join(D(F(q.p, q.q)) for q in ps)}) = {D(F(miss.p, miss.q))}."],
             [D(F(sum(ps).p, sum(ps).q)), D(F((miss * 100).p, (miss * 100).q)) if (miss * 100) != miss else "0", D(F((1 - ps[0]).p, (1 - ps[0]).q))], H(f"1 - ({' + '.join(D(F(q.p, q.q)) for q in ps)})"),
             why=["Gave the sum of the known probabilities", "Wrote the probability as a percent number", "Subtracted only one probability"])


# ============================================================== S8 Sampling, inference, and statistical models
@fam("012")
def s8_moe(r, L):
    n_ = pick(r, [100, 400, 625, 900, 1600, 2500, 1000, 1200])
    p_hat = rint(r, 20, 80)
    moe = 1 / math.sqrt(n_)
    ask = pick(r, ["moe", "interval"]) if L else "moe"
    if ask == "moe":
        return Q(f"A random survey of {n_} people finds {p_hat}% support a proposal. Use 1/(√n) to estimate the margin of error, as a percent to the nearest tenth.", f"{Rd(moe * 100, 1)}%",
                 ["Margin of error ≈ 1/(√n).", f"1/(√{n_}) ≈ {Rd(moe, 4)} = {Rd(moe * 100, 1)}%."], [f"{Rd(100 / n_, 1)}%", f"{Rd(math.sqrt(n_) / 100, 1)}%", f"{Rd(moe * 100 * 2, 1)}%"],
                 PY("pct_round", code=f"1/sqrt({n_})", places=1), why=["Used 1 ÷ n instead of 1 ÷ √n", "Used √n ÷ 100", "Doubled the margin of error"], tags=["modeling"])
    lo, hi = p_hat - moe * 100, p_hat + moe * 100
    return Q(f"A random survey of {n_} people finds {p_hat}% support a proposal. Using a margin of error of 1/(√n), give the interval of likely values, in percent to the nearest tenth.", f"{Rd(lo, 1)}% to {Rd(hi, 1)}%",
             [f"Margin of error ≈ 1/(√{n_}) = {Rd(moe * 100, 1)}%.", f"{p_hat}% ± {Rd(moe * 100, 1)}% gives {Rd(lo, 1)}% to {Rd(hi, 1)}%."],
             [f"{Rd(p_hat - 100 / n_, 1)}% to {Rd(p_hat + 100 / n_, 1)}%", f"{p_hat}% to {Rd(hi, 1)}%", f"{Rd(p_hat - 2 * moe * 100, 1)}% to {Rd(p_hat + 2 * moe * 100, 1)}%"],
             PY("moe_interval", n=n_, p=p_hat), why=["Used 1 ÷ n instead of 1 ÷ √n", "Only added the margin of error", "Doubled the margin of error"], tags=["modeling"])


@fam("012", mode="mc")
def s8_type(r, L):
    items = [("A researcher randomly assigns 60 volunteers to take a new vitamin or a placebo and compares their sleep.", "experiment"),
             ("A scientist records the diets and heart health of 500 adults without changing their habits.", "observational study"),
             ("A school emails a questionnaire to a random sample of 200 parents about lunch options.", "sample survey"),
             ("A coach randomly assigns half the team to a new warm-up routine and compares sprint times.", "experiment"),
             ("A city records how many people use each bus route during one week.", "observational study"),
             ("A pollster calls 1,000 randomly selected voters to ask about a ballot question.", "sample survey"),
             ("A teacher randomly assigns two class sections to different review methods before a test and compares scores.", "experiment"),
             ("Researchers compare test scores of students who chose to join a study club with those who did not.", "observational study")]
    s, typ = pick(r, items)
    opts = [(t, t == typ) for t in ["sample survey", "observational study", "experiment", "census"]]
    return Q(f"Identify the type of study: {s}", typ, ["An experiment imposes a treatment; an observational study records without intervening; a sample survey asks a sample questions.", f"This is {'an' if typ[0] in 'aeiou' else 'a'} {typ}."],
             options=opts, chk=TXT(typ), mode="mc")


rr = lambda f, lv=(0, 1, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Counting principles and permutations", fams=[s1_perm, rr(P8.s3_count)], extra=[err_of(s1_perm), err_of(rr(P8.s3_count, tag="e")), open_of(s1_perm)]),
    2: dict(name="Combinations", fams=[s2_comb, rr(P8.s3_prob, (1, 1, 2))], extra=[err_of(s2_comb), open_of(s2_comb)]),
    3: dict(name="Independent and dependent events", fams=[rr(P8.s2_draw), rr(P8.s2_classify)], extra=[err_of(rr(P8.s2_draw, tag="e")), open_of(rr(P8.s2_draw, tag="o"))]),
    4: dict(name="Conditional probability", fams=[s4_cond, rr(P8.s4_table), rr(P8.s4_or)], extra=[err_of(s4_cond), err_of(rr(P8.s4_or, tag="e")), open_of(s4_cond)]),
    5: dict(name="Probability distributions", fams=[s5_missing, rr(P8.s1_basic), rr(P8.s1_ev)], extra=[err_of(s5_missing), err_of(rr(P8.s1_basic, tag="e")), open_of(s5_missing)]),
    6: dict(name="Expected value", fams=[rr(P8.s1_ev, tag="v"), rr(P8.s5_game)], extra=[err_of(rr(P8.s5_game, tag="e")), err_of(rr(P8.s1_ev, tag="e")), open_of(rr(P8.s5_game, tag="o"))]),
    7: dict(name="Normal distributions and z-scores", fams=[rr(P8.s8_empirical), rr(P8.s8_z)], extra=[err_of(rr(P8.s8_z, tag="e")), open_of(rr(P8.s8_z, tag="o"))]),
    8: dict(name="Sampling, inference, and statistical models", fams=[s8_moe, s8_type], extra=[err_of(s8_moe), open_of(s8_moe)]),
}
