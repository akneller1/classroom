"""Statistics gap skills (2026-11-16), unit statistical-inference:
"Chi-Square Goodness-of-Fit Tests", "Chi-Square Tests for Homogeneity and Independence" (APSTATS.IV.B.6)
and "Significance Tests for the Slope of a Regression Line" (APSTATS.IV.B.7).
"""
from fractions import Fraction as F
from scipy import stats as st
from core import I, Reject, need, ri, g, W, levels, safe_round

GOF = [("A candy company claims its bags are {}.", ["red", "blue", "green", "yellow"], "candies"),
       ("A school claims its students travel to school as follows: {}.", ["bus", "car", "walking", "bike"], "students"),
       ("A game says its prize wheel lands on each outcome as follows: {}.", ["small prize", "medium prize", "large prize", "no prize"], "spins"),
       ("A nursery claims its mixed tulip bulbs bloom in these proportions: {}.", ["red", "pink", "white", "purple"], "bulbs"),
       ("A streaming service claims its viewers prefer genres as follows: {}.", ["comedy", "drama", "action", "documentary"], "viewers"),
       ("A genetics model predicts offspring types in these proportions: {}.", ["type A", "type B", "type C", "type D"], "offspring")]


def scenario(r, L, kmin=3):
    sent, cats, unit = r.choice(GOF)
    k = r.choice([3, 4]) if kmin == 3 else 4
    for _ in range(100):
        ps = [5 * ri(r, 2, 10) for _ in range(k - 1)]
        last = 100 - sum(ps)
        if 10 <= last <= 60:
            ps.append(last)
            break
    else:
        raise Reject()
    cats = cats[:k]
    desc = ", ".join(f"{p}% {c}" for p, c in zip(ps[:-1], cats[:-1])) + f", and {ps[-1]}% {cats[-1]}"
    return sent.format(desc), cats, ps, unit


def g_expected(r, L):
    intro, cats, ps, unit = scenario(r, L)
    n = r.choice([60, 80, 100, 120, 200] if L == 0 else [50, 90, 130, 150, 250] if L == 1 else [70, 110, 170, 230, 330])
    i = ri(r, 0, len(cats) - 1)
    e = F(n * ps[i], 100)
    prompt = f"{intro} A random sample of {n} {unit} is taken. What is the expected count for {cats[i]}?"
    ans = g(e)
    wr = [(g(ps[i]), "gave the percent instead of multiplying by the sample size"), (g(F(n, len(cats))), "split the sample equally among the categories"), (g(n - e), "found the count for all the other categories"), (g(F(ps[i], 100)), "gave the proportion instead of a count")]
    steps = [f"Expected count = n · p = {n} · {g(F(ps[i], 100))}.", f"Expected count = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="gofE", n=n, p=ps[i], show=[f"{ps[i]}% {cats[i]}", f"sample of {n} "]), "gof_expected")


def g_df(r, L):
    k = ri(r, 3, 9)
    n = 10 * ri(r, 6, 40)
    what = r.choice(["colors", "categories", "outcomes", "age groups", "flavors", "regions"])
    prompt = f"A chi-square goodness-of-fit test uses a random sample of {n} observations sorted into {k} {what}. How many degrees of freedom does the test have?"
    ans = str(k - 1)
    wr = [(str(k), "used the number of categories without subtracting 1"), (str(n - 1), "used the sample size minus 1, as in a t-test"), (str(n - k), "subtracted the number of categories from the sample size"), (str(k - 2), "subtracted 2, as for regression")]
    steps = ["For a goodness-of-fit test, df = number of categories − 1.", f"df = {k} − 1 = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="gofDf", cats=k, show=[f"into {k} "]), "gof_df")


def g_component(r, L):
    e = F(r.choice([12, 15, 16, 20, 24, 25, 30, 36, 40, 45, 50]) if L < 2 else F(r.choice([25, 35, 45, 55, 75, 125]), 2))
    o = int(e) + r.choice([-9, -8, -7, -6, -5, -4, -3, 3, 4, 5, 6, 7, 8, 9, 11])
    need(o > 0)
    v = (o - e) ** 2 / e
    safe_round(v, 2)
    prompt = f"In a chi-square test, one category has an observed count of {o} and an expected count of {g(e)}. Find this category's contribution, (O − E)²/E, to the chi-square statistic. Round to two decimal places."
    ans = f"{float(v):.2f}"
    wr = [(f"{float((o - e) ** 2 / o):.2f}", "divided by the observed count instead of the expected count"), (f"{float(abs(o - e) / e):.2f}", "did not square the difference"), (f"{float((o - e) ** 2):.2f}", "did not divide by the expected count"), (f"{float((o - e) / e):.2f}", "did not square the difference")]
    steps = [f"O − E = {o} − {g(e)} = {g(o - e)}.", f"(O − E)² = {g((o - e) ** 2)}.", f"{g((o - e) ** 2)} ÷ {g(e)} ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="chi", obs=[o], exp=[g(e)], show=[f"observed count of {o} ", f"expected count of {g(e)}."]), "gof_component")


def g_stat(r, L):
    k = 3 if L == 0 else r.choice([3, 4])
    if L == 0:
        e = [r.choice([20, 25, 30, 40, 50])] * k
    else:
        intro, cats, ps, unit = scenario(r, L, 3 if k == 3 else 4)
        need(len(ps) == k)
        n = r.choice([100, 200, 300])
        e = [F(n * p, 100) for p in ps]
    tot = sum(e)
    o = [int(x) + ri(r, -8, 8) for x in e[:-1]]
    o.append(int(tot) - sum(o))
    need(min(o) >= 5 and any(a != b for a, b in zip(o, e)))
    chi = sum((a - b) ** 2 / b for a, b in zip(o, e))
    safe_round(chi, 2)
    ol, el = ", ".join(map(str, o)), ", ".join(g(x) for x in e)
    prompt = f"A goodness-of-fit test has observed counts {ol} and expected counts {el} (in the same order). Compute the chi-square statistic. Round to two decimal places."
    ans = f"{float(chi):.2f}"
    wr = [(f"{float(sum((a - b) ** 2 / a for a, b in zip(o, e))):.2f}", "divided each squared difference by the observed count"), (f"{float(sum(abs(a - b) / b for a, b in zip(o, e))):.2f}", "did not square the differences"),
          (f"{float(sum((a - b) ** 2 for a, b in zip(o, e))):.2f}", "did not divide by the expected counts"), (f"{float(chi / k):.2f}", "averaged the contributions instead of adding them")]
    steps = ["χ² = Σ (O − E)²/E.", " + ".join(f"({a} − {g(b)})²/{g(b)}" for a, b in zip(o, e)), f"χ² ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="chi", obs=o, exp=[g(x) for x in e], show=[f"observed counts {ol} ", f"expected counts {el} "]), "gof_statistic")


def chi_draw(r, df):
    p = r.choice([0.004, 0.012, 0.021, 0.034, 0.047, 0.058, 0.074, 0.11, 0.16, 0.23, 0.31, 0.44]) * r.uniform(0.85, 1.15)
    return round(float(st.chi2.isf(p, df)), 2)


def g_pvalue(r, L):
    df = ri(r, 2, 4) if L == 0 else ri(r, 2, 7)
    chi = chi_draw(r, df)
    p = st.chi2.sf(chi, df)
    need(p >= 0.001)
    safe_round(p, 4)
    k = df + 1
    prompt = f"A chi-square goodness-of-fit test with {k} categories gives χ² = {chi:.2f}. Find the P-value. Round to four decimal places."
    ans = f"{p:.4f}"
    wr = [(f"{1 - p:.4f}", "found the area to the left of χ² instead of the right-tail area"), (f"{st.chi2.sf(chi, k):.4f}", f"used df = {k} instead of {k} − 1"), (f"{p / 2:.4f}", "halved the right-tail area; chi-square tests use the full right tail"), (f"{min(2 * p, 0.9999):.4f}", "doubled the right-tail area as if the test were two-sided")]
    steps = [f"df = {k} − 1 = {df}.", f"P-value = P(χ² ≥ {chi:.2f}) with df = {df}.", f"P-value ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="chiP", chi=f"{chi:.2f}", df=df, show=[f"with {k} categories", f"χ² = {chi:.2f}."]), "gof_pvalue")


def alpha(r, L):
    return r.choice([0.05] if L == 0 else [0.05, 0.01, 0.10])


def g_decide(r, L):
    df = ri(r, 2, 6)
    chi = chi_draw(r, df)
    p = st.chi2.sf(chi, df)
    a = alpha(r, L)
    need(p >= 0.001 and abs(p - a) > 0.004)
    safe_round(p, 4)
    thing = r.choice(["the colors in a bag of candy", "the days on which customers shop", "the blood types of donors", "the grades in a large course", "the birth months of students", "the flavors customers choose"])
    prompt = f"A goodness-of-fit test about {thing} gives χ² = {chi:.2f} with df = {df}, so the P-value is about {p:.4f}. Using α = {a:.2f}, what is the conclusion?"
    R = "Reject H₀; there is convincing evidence that the distribution differs from the claimed distribution."
    Fr = "Fail to reject H₀; there is not convincing evidence that the distribution differs from the claimed distribution."
    ans, opp = (R, Fr) if p < a else (Fr, R)
    wr = [(opp, f"compared the P-value {p:.4f} with α = {a:.2f} incorrectly"), ("Accept H₀; the claimed distribution has been proven correct.", "treated failing to reject as proof of H₀"),
          ("Reject H₀; there is not convincing evidence that the distribution differs from the claimed distribution." if p < a else "Fail to reject H₀; there is convincing evidence that the distribution differs from the claimed distribution.", "matched the decision with the wrong conclusion")]
    steps = [f"Compare the P-value with α: {p:.4f} {'<' if p < a else '>'} {a:.2f}.", ("A P-value below α means the data would be unusual if H₀ were true." if p < a else "A P-value above α means the data are consistent with H₀."), ans]
    return I(prompt, ans, steps, wr, dict(k="decide", kind="gof", chi=f"{chi:.2f}", df=df, alpha=f"{a:.2f}", pshown=f"{p:.4f}", show=[f"χ² = {chi:.2f} with df = {df}", f"about {p:.4f}", f"α = {a:.2f}"]), "gof_conclusion")


def g_conditions(r, L):
    intro, cats, ps, unit = scenario(r, L)
    n = r.choice([20, 30, 40, 50, 60, 80, 100])
    m = F(n * min(ps), 100)
    need(m != 5 or r.random() < 0.3)
    prompt = f"{intro} A random sample of {n} {unit} will be used for a chi-square goodness-of-fit test. Is the Large Counts condition (every expected count is at least 5) met?"
    yes = f"Yes; the smallest expected count is {g(m)}, which is at least 5."
    no = f"No; the smallest expected count is {g(m)}, which is less than 5."
    ans, opp = (yes, no) if m >= 5 else (no, yes)
    wr = [(opp, "compared the smallest expected count with 5 incorrectly"), (f"Yes; the sample size {n} is at least 30." if m < 5 else f"No; the sample size {n} is less than 10% of the population.", "checked a different condition"),
          ("No; the expected counts are not all equal." if m >= 5 else "Yes; the percents add to 100%.", "used a rule that is not part of the Large Counts condition")]
    steps = [f"The smallest claimed percent is {min(ps)}%.", f"Smallest expected count = {n} · {g(F(min(ps), 100))} = {g(m)}.", ans]
    return I(prompt, ans, steps, wr, dict(k="gofLC", n=n, ps=ps, show=[f"sample of {n} "] + [f"{p}% " for p in ps]), "gof_large_counts")


# ---------------------------------------------------------------- two-way tables
TW = [("grade level", "preferred lunch option", ["9th graders", "10th graders", "11th graders"], ["pizza", "salad", "sandwich"]),
      ("age group", "preferred news source", ["Under 30", "30 to 50", "Over 50"], ["online", "television", "print"]),
      ("type of treatment", "outcome", ["Treatment A", "Treatment B", "Placebo"], ["improved", "no change", "worse"]),
      ("region", "favorite sport", ["North", "South", "West"], ["soccer", "basketball", "baseball"]),
      ("class year", "study location", ["Juniors", "Seniors", "Sophomores"], ["library", "home", "cafe"]),
      ("work shift", "job satisfaction", ["Day shift", "Night shift", "Swing shift"], ["satisfied", "neutral", "dissatisfied"])]


def t_expected(r, L):
    n = r.choice([100, 120, 150, 200, 240, 300] if L < 2 else [130, 170, 210, 260, 350])
    row = r.choice([x for x in range(20, n - 10, 10 if L == 0 else 5)])
    col = r.choice([x for x in range(20, n - 10, 10 if L == 0 else 5)])
    e = F(row * col, n)
    if L == 0:
        need(e.denominator == 1)
    safe_round(e, 2)
    a, b, rows, cols = r.choice(TW)
    rn, cn = r.choice(rows), r.choice(cols)
    prompt = f"A two-way table classifies {n} people by {a} and {b}. The row total for \"{rn}\" is {row} and the column total for \"{cn}\" is {col}. If H₀ is true, what is the expected count for the cell \"{rn}\" and \"{cn}\"? Round to two decimal places if needed."
    ans = g(e, 2)
    wr = [(g(F(row + col, 2), 2), "averaged the row and column totals"), (g(F(n, 4), 2), "split the grand total equally among four cells"), (g(F(row * col, n * n), 4), "divided by the grand total twice, giving a proportion"), (g(F(min(row, col), 2), 2), "halved the smaller total")]
    steps = ["Expected count = (row total · column total) ÷ grand total.", f"({row} · {col}) ÷ {n} = {g(F(row * col), 2)} ÷ {n}.", f"Expected count ≈ {ans}." if e.denominator != 1 else f"Expected count = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="twoE", n=n, row=row, col=col, show=[f"classifies {n} people", f"is {row} and", f"is {col}."]), "twoway_expected")


def t_df(r, L):
    rr, cc = ri(r, 2, 5), ri(r, 2, 6)
    a, b, _, _ = r.choice(TW)
    prompt = f"A chi-square test uses a two-way table of {a} and {b} with {rr} rows and {cc} columns (not counting totals). How many degrees of freedom does the test have?"
    ans = str((rr - 1) * (cc - 1))
    wr = [(str(rr * cc - 1), "used the number of cells minus 1"), (str(rr * cc), "multiplied rows by columns without subtracting 1 from each"), (str(rr + cc - 2), "added (rows − 1) and (columns − 1) instead of multiplying"), (str(rr + cc), "added the rows and columns")]
    steps = ["df = (rows − 1)(columns − 1).", f"df = ({rr} − 1)({cc} − 1) = {rr - 1} · {cc - 1} = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="twoDf", r=rr, c=cc, show=[f"{rr} rows and {cc} columns"]), "twoway_df")


def t_stat(r, L):
    a, b, rows, cols = r.choice(TW)
    nc = 2 if L < 2 else 3
    rows, cols = r.sample(rows, 2), r.sample(cols, nc)
    for _ in range(300):
        t = [[ri(r, 8, 45) for _ in range(nc)] for _ in range(2)]
        rt, ct = [sum(x) for x in t], [sum(t[i][j] for i in range(2)) for j in range(nc)]
        n = sum(rt)
        ex = [[F(rt[i] * ct[j], n) for j in range(nc)] for i in range(2)]
        if all((x * 100).denominator == 1 for row in ex for x in row) and min(min(row) for row in ex) >= 5:
            break
    else:
        raise Reject()
    chi = sum((t[i][j] - ex[i][j]) ** 2 / ex[i][j] for i in range(2) for j in range(nc))
    need(chi > 0.05)
    safe_round(chi, 2)
    lines = "; ".join(f"{rows[i]}: " + ", ".join(f"{t[i][j]} {cols[j]}" for j in range(nc)) for i in range(2))
    prompt = f"A study records {a} and {b}. Observed counts: {lines}. Compute the chi-square statistic for a test of association. Round to two decimal places."
    ans = f"{float(chi):.2f}"
    half = sum((t[0][j] - ex[0][j]) ** 2 / ex[0][j] for j in range(nc))
    wr = [(f"{float(half):.2f}", "added the contributions from the first row only"), (f"{float(sum((t[i][j] - ex[i][j]) ** 2 / t[i][j] for i in range(2) for j in range(nc))):.2f}", "divided by the observed counts instead of the expected counts"),
          (f"{float(sum(abs(t[i][j] - ex[i][j]) / ex[i][j] for i in range(2) for j in range(nc))):.2f}", "did not square the differences"), (f"{float(sum((t[i][j] - ex[i][j]) ** 2 for i in range(2) for j in range(nc))):.2f}", "did not divide by the expected counts")]
    steps = [f"Row totals: {rt[0]} and {rt[1]}; column totals: {', '.join(map(str, ct))}; grand total: {n}.",
             "Expected counts (row total · column total ÷ grand total): " + "; ".join(f"{rows[i]}: " + ", ".join(g(ex[i][j], 2) for j in range(nc)) for i in range(2)) + ".",
             f"χ² = Σ (O − E)²/E ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="chi2way", t=t, show=[lines]), "twoway_statistic")


def t_pvalue(r, L):
    rr, cc = (2, ri(r, 2, 4)) if L == 0 else (ri(r, 2, 4), ri(r, 2, 5))
    df = (rr - 1) * (cc - 1)
    chi = chi_draw(r, df)
    p = st.chi2.sf(chi, df)
    need(p >= 0.001)
    safe_round(p, 4)
    prompt = f"A chi-square test on a two-way table with {rr} rows and {cc} columns gives χ² = {chi:.2f}. Find the P-value. Round to four decimal places."
    ans = f"{p:.4f}"
    wr = [(f"{1 - p:.4f}", "found the area to the left of χ² instead of the right-tail area"), (f"{st.chi2.sf(chi, rr * cc - 1):.4f}", f"used df = {rr * cc - 1} (cells − 1) instead of (rows − 1)(columns − 1)"),
          (f"{p / 2:.4f}", "halved the right-tail area"), (f"{st.chi2.sf(chi, df + 1):.4f}", f"used df = {df + 1}")]
    steps = [f"df = ({rr} − 1)({cc} − 1) = {df}.", f"P-value = P(χ² ≥ {chi:.2f}) with df = {df}.", f"P-value ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="twoP", r=rr, c=cc, chi=f"{chi:.2f}", show=[f"{rr} rows and {cc} columns", f"χ² = {chi:.2f}."]), "twoway_pvalue")


WHICH = [("A researcher takes one random sample of 400 adults and classifies each person by age group and by preferred news source.", "independence"),
         ("A school takes a single random sample of 250 students and records each student's grade level and whether the student plays a sport.", "independence"),
         ("One random sample of 300 shoppers is surveyed; each shopper is classified by gender and by payment method.", "independence"),
         ("A single random sample of 500 voters is classified by region and by opinion on a ballot question.", "independence"),
         ("A clinic takes one random sample of 180 patients and records each patient's blood type and whether the patient has allergies.", "independence"),
         ("Separate random samples of 100 freshmen, 100 sophomores, and 100 juniors are asked to name their favorite lunch option.", "homogeneity"),
         ("Independent random samples of 150 customers from each of three stores are asked to rate their service as good, fair, or poor.", "homogeneity"),
         ("Patients are randomly assigned to one of three treatments, and each patient's outcome is recorded as improved, unchanged, or worse.", "homogeneity"),
         ("Separate random samples of 200 teachers and 200 parents are asked whether they support, oppose, or are unsure about a later start time.", "homogeneity"),
         ("Independent random samples of 80 residents from each of four neighborhoods are asked which of three park designs they prefer.", "homogeneity"),
         ("A company claims its candy is 30% red, 20% blue, and 50% green. A student counts the colors in one random sample of 200 candies.", "gof"),
         ("A die is rolled 120 times to check the claim that all six faces are equally likely.", "gof"),
         ("A geneticist compares the counts of four offspring types in one random sample with the 9:3:3:1 ratio a model predicts.", "gof")]
NAMES = {"independence": "Chi-square test for independence", "homogeneity": "Chi-square test for homogeneity", "gof": "Chi-square goodness-of-fit test"}


def t_which(r, L):
    i = ri(r, 0, len(WHICH) - 1)
    text, kind = WHICH[i]
    prompt = f"{text} Which chi-square test is appropriate?"
    ans = NAMES[kind]
    why = {"independence": "one sample classified on two variables calls for a test for independence", "homogeneity": "separate samples or treatment groups compared on one variable call for a test for homogeneity", "gof": "one sample compared with a claimed distribution calls for a goodness-of-fit test"}[kind]
    wr = [(NAMES[k2], "did not notice how the data were collected: " + why) for k2 in NAMES if k2 != kind] + [("Two-sample t-test for a difference in means", "chose a test for quantitative data; these data are counts in categories")]
    steps = [{"independence": "There is one random sample, and each individual is classified on two categorical variables.", "homogeneity": "There are separate samples (or treatment groups), and one categorical variable is compared across them.", "gof": "There is one sample and one categorical variable, compared with a claimed distribution."}[kind], f"Use the {ans[0].lower() + ans[1:]}."]
    return I(prompt, ans, steps, wr, dict(k="which", show=[text]), "twoway_which_test")


PAIRS = [("grade level", "preferred lunch option", "students at a large high school"), ("age group", "preferred news source", "adults in a city"), ("region", "favorite sport", "fans in a country"),
         ("work shift", "job satisfaction", "employees at a company"), ("gender", "payment method", "shoppers at a mall"), ("blood type", "allergy status", "patients at a clinic"),
         ("class year", "study location", "students at a college"), ("exercise habit", "sleep quality", "adults in a town")]


def t_hyp(r, L):
    a, b, pop = r.choice(PAIRS)
    alt = r.random() < 0.5
    prompt = f"A chi-square test for independence uses one random sample of {pop}, classified by {a} and {b}. State the {'alternative' if alt else 'null'} hypothesis."
    h0 = f"H₀: There is no association between {a} and {b} for {pop}."
    ha = f"Hₐ: There is an association between {a} and {b} for {pop}."
    ans = ha if alt else h0
    wr = [((h0.replace("H₀", "Hₐ") if alt else ha.replace("Hₐ", "H₀")), "switched the null and alternative hypotheses"),
          (f"{'Hₐ' if alt else 'H₀'}: The mean {a} equals the mean {b} for {pop}.", "wrote a hypothesis about means; the variables are categorical"),
          (f"{'Hₐ' if alt else 'H₀'}: In the sample, {a} and {b} are {'associated' if alt else 'not associated'}.", "wrote the hypothesis about the sample instead of the population")]
    steps = ["The null hypothesis says the two variables are independent (no association) in the population.", "The alternative says there is an association.", ans]
    return I(prompt, ans, steps, wr, dict(k="h0", a=a, b=b, pop=pop, alt=alt, show=[f"{a} and {b}", pop, "alternative" if alt else "null"]), "twoway_hypotheses")


def t_decide(r, L):
    a, b, pop = r.choice(PAIRS)
    rr, cc = ri(r, 2, 3), ri(r, 2, 4)
    df = (rr - 1) * (cc - 1)
    chi = chi_draw(r, df)
    p = st.chi2.sf(chi, df)
    al = alpha(r, L)
    need(p >= 0.001 and abs(p - al) > 0.004)
    safe_round(p, 4)
    prompt = f"A chi-square test for independence between {a} and {b} for {pop} gives χ² = {chi:.2f} with df = {df}, so the P-value is about {p:.4f}. Using α = {al:.2f}, what is the conclusion?"
    R = f"Reject H₀; there is convincing evidence of an association between {a} and {b}."
    Fr = f"Fail to reject H₀; there is not convincing evidence of an association between {a} and {b}."
    ans, opp = (R, Fr) if p < al else (Fr, R)
    wr = [(opp, f"compared the P-value {p:.4f} with α = {al:.2f} incorrectly"), (f"Accept H₀; {a} and {b} have been proven independent.", "treated failing to reject as proof of H₀"),
          (f"Reject H₀; {a} causes {b}.", "claimed causation, which a test of association from a sample survey cannot show")]
    steps = [f"Compare the P-value with α: {p:.4f} {'<' if p < al else '>'} {al:.2f}.", ("A P-value below α means the data would be unusual if the variables were independent." if p < al else "A P-value above α means the data are consistent with independence."), ans]
    return I(prompt, ans, steps, wr, dict(k="decide", kind="ind", a=a, b=b, chi=f"{chi:.2f}", df=df, alpha=f"{al:.2f}", pshown=f"{p:.4f}", show=[f"between {a} and {b} ", f"χ² = {chi:.2f} with df = {df}", f"about {p:.4f}", f"α = {al:.2f}"]), "twoway_conclusion")


# ---------------------------------------------------------------- slope t-test
XY = [("hours of study", "exam score"), ("advertising spending", "weekly sales"), ("temperature", "ice cream sales"), ("years of experience", "salary"), ("car weight", "fuel efficiency"),
      ("hours of screen time", "hours of sleep"), ("fertilizer amount", "plant height"), ("practice time", "free-throw percentage")]


def slope_draw(r, L):
    n = ri(r, 10, 30) if L < 2 else ri(r, 8, 45)
    se = r.choice([0.05, 0.08, 0.12, 0.15, 0.2, 0.25, 0.4, 0.5, 0.75, 1.2])
    t = r.choice([0.6, 0.9, 1.2, 1.5, 1.8, 2.0, 2.2, 2.4, 2.7, 3.1, 3.6]) * r.uniform(0.9, 1.1) * r.choice([1, 1, 1, -1])
    b = round(se * t, 2 if se >= 0.2 else 3)
    need(b != 0)
    return n, b, se


def bt(b):
    return str(b).replace("-", "−")


def s_t(r, L):
    n, b, se = slope_draw(r, L)
    t = b / se
    safe_round(t, 2)
    x, y = r.choice(XY)
    prompt = f"A regression of {y} on {x} (n = {n}) gives slope b = {bt(b)} with SE_b = {se}. Compute the t statistic for testing H₀: β = 0. Round to two decimal places."
    ans = bt(f"{t:.2f}")
    wr = [(bt(f"{se / b:.2f}"), "divided the standard error by the slope"), (bt(f"{b * se:.2f}"), "multiplied the slope by the standard error"), (bt(f"{b / (se / n ** 0.5):.2f}"), "divided the standard error by √n; SE_b is already the standard error of the slope"), (bt(f"{-t:.2f}"), "lost the sign of the slope")]
    steps = ["t = (b − 0) ÷ SE_b.", f"t = {bt(b)} ÷ {se} ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="slopeT", b=str(b), se=str(se), show=[f"b = {bt(b)} ", f"SE_b = {se}."]), "slope_t_statistic")


def s_df(r, L):
    n = ri(r, 8, 60)
    x, y = r.choice(XY)
    prompt = f"A significance test for the slope of the regression line relating {y} to {x} uses {n} data points. How many degrees of freedom does the t distribution have?"
    ans = str(n - 2)
    wr = [(str(n - 1), "subtracted 1, as for a one-sample t-test"), (str(n), "used the number of points"), (str(2 * n - 2), "used the two-sample formula n₁ + n₂ − 2"), ("2", "gave the number of estimated parameters")]
    steps = ["Regression estimates two parameters (intercept and slope), so df = n − 2.", f"df = {n} − 2 = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="slopeDf", n=n, show=[f"uses {n} data points"]), "slope_df")


TAILS = {"two": "β ≠ 0", "greater": "β > 0", "less": "β < 0"}


def pval(t, df, tail):
    return 2 * st.t.sf(abs(t), df) if tail == "two" else st.t.sf(t, df) if tail == "greater" else st.t.cdf(t, df)


def s_p(r, L):
    n = ri(r, 10, 30)
    tail = "two" if L == 0 else r.choice(["two", "two", "greater", "less"])
    t = round(r.choice([1.1, 1.4, 1.7, 1.9, 2.1, 2.3, 2.6, 2.9, 3.3]) * r.uniform(0.92, 1.08), 2)
    if tail == "less" or (tail == "two" and r.random() < 0.3):
        t = -t
    p = pval(t, n - 2, tail)
    need(p >= 0.001)
    safe_round(p, 4)
    prompt = f"A test of H₀: β = 0 against Hₐ: {TAILS[tail]} for a regression slope gives t = {bt(f'{t:.2f}')} from n = {n} data points. Find the P-value. Round to four decimal places."
    ans = f"{p:.4f}"
    other = p / 2 if tail == "two" else min(2 * p, 0.9999)
    wr = [(f"{other:.4f}", "used one tail instead of two" if tail == "two" else "doubled the tail area for a one-sided test"), (f"{pval(t, n - 1, tail):.4f}", f"used df = {n - 1} instead of n − 2 = {n - 2}"), (f"{1 - p:.4f}", "found the area on the wrong side of t"), (f"{pval(t, n, tail):.4f}", f"used df = {n}")]
    steps = [f"df = n − 2 = {n - 2}.", ("P-value = 2 · P(T ≥ |t|)" if tail == "two" else "P-value = P(T ≥ t)" if tail == "greater" else "P-value = P(T ≤ t)") + f" with t = {bt(f'{t:.2f}')}.", f"P-value ≈ {ans}."]
    return I(prompt, ans, steps, wr, dict(k="slopeP", t=f"{t:.2f}", n=n, tail=tail, show=[f"Hₐ: {TAILS[tail]} ", f"t = {bt(f'{t:.2f}')} ", f"n = {n} "]), "slope_pvalue")


def s_hyp(r, L):
    x, y = r.choice(XY)
    tail = r.choice(["two", "greater", "less"])
    q = {"two": f"whether there is a linear relationship between {x} and {y}", "greater": f"whether {y} tends to increase as {x} increases (a positive linear relationship)", "less": f"whether {y} tends to decrease as {x} increases (a negative linear relationship)"}[tail]
    prompt = f"A researcher wants to test {q}. State the hypotheses in terms of the slope β of the population regression line."
    ans = f"H₀: β = 0; Hₐ: {TAILS[tail]}"
    o1, o2 = [TAILS[k] for k in TAILS if k != tail]
    wr = [(f"H₀: b = 0; Hₐ: {TAILS[tail].replace('β', 'b')}", "wrote the hypotheses about the sample slope b instead of the population slope β"), (f"H₀: {TAILS[tail]}; Hₐ: β = 0", "switched the null and alternative hypotheses"), (f"H₀: β = 0; Hₐ: {o1}", "chose the wrong direction for the alternative"), (f"H₀: β = 0; Hₐ: {o2}", "chose the wrong direction for the alternative")]
    steps = ["The null hypothesis says there is no linear relationship, so H₀: β = 0.", {"two": "No direction is stated, so the alternative is two-sided.", "greater": "A positive relationship means a positive slope.", "less": "A negative relationship means a negative slope."}[tail], ans]
    return I(prompt, ans, steps, wr, dict(k="slopeHyp", tail=tail, show=[q]), "slope_hypotheses")


def s_decide(r, L):
    x, y = r.choice(XY)
    n = ri(r, 10, 30)
    t = round(r.choice([1.2, 1.5, 1.8, 2.0, 2.2, 2.5, 2.8, 3.2]) * r.uniform(0.92, 1.08), 2)
    p = pval(t, n - 2, "two")
    al = alpha(r, L)
    need(p >= 0.001 and abs(p - al) > 0.004)
    safe_round(p, 4)
    prompt = f"A two-sided test for the slope of the regression line relating {y} to {x} gives t = {t:.2f} with df = {n - 2}, so the P-value is about {p:.4f}. Using α = {al:.2f}, what is the conclusion?"
    R = f"Reject H₀; there is convincing evidence of a linear relationship between {x} and {y}."
    Fr = f"Fail to reject H₀; there is not convincing evidence of a linear relationship between {x} and {y}."
    ans, opp = (R, Fr) if p < al else (Fr, R)
    wr = [(opp, f"compared the P-value {p:.4f} with α = {al:.2f} incorrectly"), (f"Accept H₀; there is no relationship between {x} and {y}.", "treated failing to reject as proof of H₀"), (f"Reject H₀; changes in {x} cause changes in {y}.", "claimed causation from an observational regression")]
    steps = [f"Compare the P-value with α: {p:.4f} {'<' if p < al else '>'} {al:.2f}.", ("A P-value below α means a slope this far from 0 would be unusual if β = 0." if p < al else "A P-value above α means the sample slope is consistent with β = 0."), ans]
    return I(prompt, ans, steps, wr, dict(k="decide", kind="slope", a=x, b=y, t=f"{t:.2f}", df=n - 2, alpha=f"{al:.2f}", pshown=f"{p:.4f}", show=[f"relating {y} to {x} ", f"t = {t:.2f} with df = {n - 2}", f"about {p:.4f}", f"α = {al:.2f}"]), "slope_conclusion")


def s_full(r, L):
    levels(L, 1, 2)
    n, b, se = slope_draw(r, L)
    t = b / se
    df = n - 2
    p = pval(t, df, "two")
    al = alpha(r, L)
    need(p >= 0.001 and abs(p - al) > 0.006 and f"{pval(round(t, 2), df, 'two'):.4f}" == f"{p:.4f}")
    safe_round(t, 2)
    safe_round(p, 4)
    x, y = r.choice(XY)
    prompt = f"A regression of {y} on {x} (n = {n}) gives slope b = {bt(b)} with SE_b = {se}. Test H₀: β = 0 against Hₐ: β ≠ 0 at α = {al:.2f}. Give t (two decimal places), the P-value (four decimal places), and the decision."
    dec = "reject H₀" if p < al else "fail to reject H₀"
    ans = f"t ≈ {bt(f'{t:.2f}')}, P-value ≈ {p:.4f}; {dec}"
    wr = [(f"t ≈ {bt(f'{t:.2f}')}, P-value ≈ {p:.4f}; {'fail to reject H₀' if p < al else 'reject H₀'}", "compared the P-value with α incorrectly"), (f"t ≈ {bt(f'{t:.2f}')}, P-value ≈ {p / 2:.4f}; {'reject H₀' if p / 2 < al else 'fail to reject H₀'}", "used a one-sided P-value for a two-sided test"),
          (f"t ≈ {bt(f'{se / b:.2f}')}, P-value ≈ {pval(se / b, df, 'two'):.4f}; {'reject H₀' if pval(se / b, df, 'two') < al else 'fail to reject H₀'}", "divided SE_b by b to get t")]
    steps = [f"t = {bt(b)} ÷ {se} ≈ {bt(f'{t:.2f}')}.", f"df = {n} − 2 = {df}; P-value = 2 · P(T ≥ {abs(t):.2f}) ≈ {p:.4f}.", f"{p:.4f} {'<' if p < al else '>'} {al:.2f}, so {dec}."]
    return I(prompt, ans, steps, wr, dict(k="slopeFull", b=str(b), se=str(se), n=n, alpha=f"{al:.2f}", show=[f"(n = {n})", f"b = {bt(b)} ", f"SE_b = {se}.", f"α = {al:.2f}"]), "slope_full_test")


U = "statistical-inference"
SKILLS = {
    ("statistics", U, "Chi-Square Goodness-of-Fit Tests"): dict(fns=[g_expected, g_df, g_component, g_stat, g_pvalue, g_decide, g_conditions], stds=["APSTATS.IV.B.6"], prefix="stat-u4"),
    ("statistics", U, "Chi-Square Tests for Homogeneity and Independence"): dict(fns=[t_expected, t_df, t_stat, t_pvalue, t_which, t_hyp, t_decide], stds=["APSTATS.IV.B.6"], prefix="stat-u4"),
    ("statistics", U, "Significance Tests for the Slope of a Regression Line"): dict(fns=[s_t, s_df, s_p, s_hyp, s_decide, s_full], stds=["APSTATS.IV.B.7"], prefix="stat-u4"),
}
