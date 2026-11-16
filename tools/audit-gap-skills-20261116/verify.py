"""Independent verifier for the 2026-11-16 audit gap skills.

For every new item it:
  1. confirms the data it is about to use is printed in the prompt (check["show"]),
  2. recomputes the keyed answer from that data alone and requires an exact match,
  3. requires every multiple-choice distractor and every error-analysis "student answer" to be wrong,
  4. requires every open-response part to be right,
  5. checks the item's structure (one correct option, four distinct options, ids, levels).
It imports only fmt (the display-text evaluator) and statements.json, never the families.

Usage: python3 verify.py <repo root>   → prints TOTAL ERRORS n
"""
import json, math, os, re, sys, warnings
from fractions import Fraction as F
import numpy as np
from scipy import stats as st
from scipy.integrate import quad
from scipy.optimize import brentq
from fmt import val, close, dnum

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
ST = json.load(open(os.path.join(HERE, "statements.json"), encoding="utf-8"))
SUBD = {c: str(i) for i, c in enumerate("₀₁₂₃₄₅₆₇₈₉")}


def trim(v, dp=4):
    s = f"{float(v):.{dp}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def ev(text, **v):
    """Evaluate display text that may contain ˣ, log₂( ), log( )."""
    s = text.replace("ˣ", "^(x)")
    s = re.sub(r"log([₀-₉]+)\(", lambda m: "LOGB(" + "".join(SUBD[c] for c in m.group(1)) + ",", s)
    s = s.replace("log(", "LOGT(")
    return val(s, LOGB=lambda b, z: np.log(z) / np.log(b), LOGT=np.log10, **v)


def fnum(t):
    return float(t.replace("−", "-"))


def lead(ans):
    return fnum(ans.split()[0].rstrip("°%"))


def roots(eq, var):
    L, R = eq.split(" = ")
    f = lambda x: ev(L, **{var: x}) - ev(R, **{var: x})
    xs = np.arange(-40.000123, 260, 0.0005)
    ys = np.asarray(f(xs), dtype=float) + 0 * xs
    ok = np.isfinite(ys[:-1]) & np.isfinite(ys[1:]) & (np.sign(ys[:-1]) * np.sign(ys[1:]) < 0)
    out = []
    for i in np.nonzero(ok)[0]:
        x0 = brentq(lambda x: float(f(x)), xs[i], xs[i + 1], xtol=1e-13)
        if abs(float(f(x0))) < 1e-6 * max(1, abs(float(ev(R, **{var: x0})))):
            out.append(x0)
    return out


def tri(given, find):
    G = {k: float(v) for k, v in given.items()}
    s, a = sorted(k for k in G if k.islower()), sorted(k for k in G if k.isupper())
    T = dict(G)
    if len(s) == 3:
        for X, (p, q, o) in {"A": "bca", "B": "acb", "C": "abc"}.items():
            T[X] = math.degrees(math.acos((G[p] ** 2 + G[q] ** 2 - G[o] ** 2) / (2 * G[p] * G[q])))
    elif len(s) == 2 and len(a) == 1 and a[0].lower() not in s:
        p, q = s
        o = a[0].lower()
        T[o] = math.sqrt(G[p] ** 2 + G[q] ** 2 - 2 * G[p] * G[q] * math.cos(math.radians(G[a[0]])))
    elif len(a) == 2 and len(s) == 1:
        third = ({"A", "B", "C"} - set(a)).pop()
        T[third] = 180 - G[a[0]] - G[a[1]]
        k = G[s[0]] / math.sin(math.radians(T[s[0].upper()]))
        for X in "ABC":
            T[X.lower()] = k * math.sin(math.radians(T[X]))
    elif len(s) == 2 and len(a) == 1:          # SSA with the known angle opposite the longer known side
        big = a[0].lower()
        other = [x for x in s if x != big][0]
        if not G[other] < G[big]:
            return None
        T[other.upper()] = math.degrees(math.asin(G[other] * math.sin(math.radians(G[a[0]])) / G[big]))
    else:
        return None
    return T.get(find)


def which_law(given):
    s, a = [k for k in given if k.islower()], [k for k in given if k.isupper()]
    return "Law of Cosines" if len(s) == 3 or (len(s) == 2 and len(a) == 1 and a[0].lower() not in s) else "Law of Sines"


def cond_expected(c):
    s = ST[c["sid"]]
    mk = lambda p, q: f"If {s['s']} {p}, then {s['it']} {q}."
    fam = c["fam"]
    if fam == "parts":
        return f"{s['s']} {s['p']}" if c["part"] == "hypothesis" else f"{s['it']} {s['q']}"
    if fam == "converse":
        return mk(s["q"], s["p"])
    if fam == "inverse":
        return mk(s["np"], s["nq"])
    if fam in ("contrapositive", "equiv"):
        return mk(s["nq"], s["np"])
    if fam == "truth":
        return "True" if s["conv"] else f"False; counterexample: {s['cx']}."
    if fam == "bicond":
        return f"Yes; {s['s']} {s['p']} if and only if {s['it']} {s['q']}." if s["conv"] else "No; the converse is false."


def coefs(e):
    xs = np.arange(-6, 7).astype(float)
    ys = np.array([float(val(e, x=x)) for x in xs])
    return [int(round(c)) for c in np.linalg.lstsq(np.vander(xs, 13), ys, rcond=None)[0]][::-1]   # index = power


def which_test(text):
    if re.search(r"claims|claim that|a model predicts", text):
        return "Chi-square goodness-of-fit test"
    if re.search(r"[Ss]eparate random samples|[Ii]ndependent random samples|randomly assigned", text):
        return "Chi-square test for homogeneity"
    if re.search(r"[Oo]ne random sample|single random sample", text):
        return "Chi-square test for independence"


def tp(t, df, tail):
    return 2 * st.t.sf(abs(t), df) if tail == "two" else st.t.sf(t, df) if tail == "greater" else st.t.cdf(t, df)


TAILS = {"two": "β ≠ 0", "greater": "β > 0", "less": "β < 0"}


def judge(c, ans):
    k = c["k"]
    try:
        if k == "rate":
            rs = {F(y) / F(x) for x, y in zip(c["xs"], c["ys"])}
            return len(rs) == 1 and F(str(lead(ans))) == rs.pop()
        if k == "predict":
            return F(ans) == F(c["y"]) / F(c["x"]) * F(c["x2"])
        if k == "propEq":
            m = re.fullmatch(r"y = ([\d.]+)x", ans)
            return bool(m) and F(m.group(1)) == F(c["y"]) / F(c["x"])
        if k == "compare":
            rs = {F(y) / F(x) for x, y in zip(c["xs"], c["ys"])}
            kb, ka = rs.pop(), F(c["a"])
            if rs or ka == kb:
                return "BAD SETUP"
            return ans == f"{c['A'] if ka > kb else c['B']}, by {trim(abs(ka - kb))} {c['unit']}"
        if k == "unitpoint":
            return ans == f"(1, {c['r']})"
        if k == "ident":
            v = c["var"]
            return all(close(val(c["e"], **{v: x0}), val(ans, **{v: x0}), 1e-9) for x0 in (0.37, 1.3, 2.9, 7.1))
        if k == "pct":
            return ans == trim(abs(F(c["factor"]) - 1) * 100) + "%"
        if k == "gofE":
            return ans == trim(F(c["n"] * c["p"], 100))
        if k == "gofDf":
            return ans == str(c["cats"] - 1)
        if k == "chi":
            return ans == f"{float(sum((F(o) - F(e)) ** 2 / F(e) for o, e in zip(c['obs'], c['exp']))):.2f}"
        if k == "chiP":
            return ans == f"{st.chi2.sf(float(c['chi']), c['df']):.4f}"
        if k == "gofLC":
            m = F(c["n"] * min(c["ps"]), 100)
            return sum(c["ps"]) == 100 and ans == (f"Yes; the smallest expected count is {trim(m)}, which is at least 5." if m >= 5 else f"No; the smallest expected count is {trim(m)}, which is less than 5.")
        if k == "twoE":
            return ans == trim(F(c["row"] * c["col"], c["n"]), 2)
        if k == "twoDf":
            return ans == str((c["r"] - 1) * (c["c"] - 1))
        if k == "chi2way":
            t = np.array(c["t"], dtype=float)
            e = np.outer(t.sum(1), t.sum(0)) / t.sum()
            return e.min() >= 5 and ans == f"{((t - e) ** 2 / e).sum():.2f}"
        if k == "twoP":
            return ans == f"{st.chi2.sf(float(c['chi']), (c['r'] - 1) * (c['c'] - 1)):.4f}"
        if k == "which":
            return ans == which_test(c["show"][0])
        if k == "h0":
            return ans == (f"Hₐ: There is an association between {c['a']} and {c['b']} for {c['pop']}." if c["alt"] else f"H₀: There is no association between {c['a']} and {c['b']} for {c['pop']}.")
        if k == "decide":
            p = tp(float(c["t"]), c["df"], "two") if c["kind"] == "slope" else st.chi2.sf(float(c["chi"]), c["df"])
            if f"{p:.4f}" != c["pshown"]:
                return "P-VALUE SHOWN IS WRONG"
            rej = p < float(c["alpha"])
            tail = {"gof": "that the distribution differs from the claimed distribution.", "ind": f"of an association between {c.get('a')} and {c.get('b')}.", "slope": f"of a linear relationship between {c.get('a')} and {c.get('b')}."}[c["kind"]]
            return ans == ("Reject H₀; there is convincing evidence " if rej else "Fail to reject H₀; there is not convincing evidence ") + tail
        if k == "slopeT":
            return ans == f"{float(c['b']) / float(c['se']):.2f}".replace("-", "−")
        if k == "slopeDf":
            return ans == str(c["n"] - 2)
        if k == "slopeP":
            return ans == f"{tp(float(c['t']), c['n'] - 2, c['tail']):.4f}"
        if k == "slopeHyp":
            return ans == f"H₀: β = 0; Hₐ: {TAILS[c['tail']]}"
        if k == "slopeFull":
            t = float(c["b"]) / float(c["se"])
            p = tp(t, c["n"] - 2, "two")
            return ans == f"t ≈ {t:.2f}".replace("-", "−") + f", P-value ≈ {p:.4f}; {'reject H₀' if p < float(c['alpha']) else 'fail to reject H₀'}"
        if k == "coefOf":
            return ans == str(coefs(c["e"])[c["p"]])
        if k == "termOf":
            cs = coefs(c["e"])
            n = max(i for i, v in enumerate(cs) if v)
            p = n - (c["idx"] - 1)
            return all(close(val(ans, x=x0), cs[p] * x0 ** p, 1e-9) for x0 in (0.7, 1.9, -2.3))
        if k == "pascal":
            return ans == ", ".join(str(math.comb(c["n"], i)) for i in range(c["n"] + 1))
        if k == "choose":
            return ans == str(math.factorial(c["n"]) // (math.factorial(c["kk"]) * math.factorial(c["n"] - c["kk"])))
        if k == "sumCoef":
            return ans == str(int(round(float(val(c["e"], x=1.0)))))
        if k == "solve":
            v = c["var"]
            rs = roots(c["eq"], v)
            a = ans[: -len(c["unit"]) - 1] if c.get("unit") and ans.endswith(" " + c["unit"]) else ans
            if a == "no solution":
                return not rs
            parts = a.split(" or ")
            if len(parts) != len(rs):
                return False
            got = []
            for p in parts:
                m = re.fullmatch(rf"{v} (=|≈) (.+)", p)
                if not m:
                    return False
                if m.group(1) == "≈":
                    dp = c.get("dp")
                    if dp is None or not re.fullmatch(rf"-?\d+\.\d{{{dp}}}", m.group(2)):
                        return False
                    hit = [x for x in rs if f"{x:.{dp}f}" == m.group(2)]
                else:
                    if c.get("dp") is not None:
                        return False
                    x1 = complex(ev(m.group(2)))
                    hit = [x for x in rs if np.isfinite(x1) and abs(x1 - x) < 1e-7 * max(1, abs(x))]
                if len(hit) != 1:
                    return False
                got.append(hit[0])
            return len(set(got)) == len(rs)
        if k == "anti":
            F_ = ans.replace(" + C", "")
            if F_ == ans:
                return False
            return all(close(dnum(lambda x: val(F_, x=x), x0), val(c["g"], x=x0), 1e-5) for x0 in (0.12, 0.19, 0.26, 0.33))
        if k == "defint":
            v, _ = quad(lambda x: float(val(c["g"], x=x)), c["lo"], c["hi"], epsabs=1e-12, epsrel=1e-12)
            return close(val(ans), v, 1e-8)
        if k == "tri":
            v = tri(c["given"], c["find"])
            if v is None:
                return "BAD SETUP"
            return ans == f"{v:.{c['dp']}f}" + ("°" if c["find"].isupper() else "") + (" " + c["unit"] if c.get("unit") else "")
        if k == "whichLaw":
            return ans == which_law(c["given"])
        if k == "cond":
            return ans == cond_expected(c)
    except Exception as e:
        return False
    return f"UNKNOWN KIND {k}"


def main():
    checks = json.load(open(os.path.join(HERE, "out", "checks.json"), encoding="utf-8"))
    banks, errs, n = {}, [], 0
    for qid, c in checks.items():
        key = tuple(c["bank"])
        if key not in banks:
            banks[key] = {q["id"]: q for q in json.load(open(os.path.join(ROOT, "question-banks", key[0], key[1] + ".json"), encoding="utf-8"))["questions"]}
        q = banks[key].get(qid)
        if q is None:
            errs.append((qid, "missing from bank"))
            continue
        n += 1
        bad = lambda msg: errs.append((qid, msg))
        if q["level"] not in ("cp2", "cp1", "honors") or not q.get("standards") or not q.get("solutionSteps"):
            bad("structure")
        if q["format"] == "open-response":
            if len(q["parts"]) != 4:
                bad("parts")
            for p, pc in zip(q["parts"], c["parts"]):
                for sh in pc.get("show", []):
                    if sh not in p["prompt"]:
                        bad(f"not shown: {sh}")
                if judge(pc, p["answer"]) is not True:
                    bad(f"part answer not verified: {p['prompt']} => {p['answer']} ({judge(pc, p['answer'])})")
            continue
        for sh in c.get("show", []):
            if sh not in q["prompt"]:
                bad(f"not shown: {sh!r}")
        r = judge(c, q["answer"])
        if r is not True:
            bad(f"answer not verified ({r}): {q['prompt']} => {q['answer']}")
        if q["format"] == "multiple-choice":
            o = q["options"]
            if len(o) != 4 or len({x["text"] for x in o}) != 4 or sum(x["correct"] for x in o) != 1 or [x["text"] for x in o if x["correct"]] != [q["answer"]]:
                bad("options structure")
            for x in o:
                if not x["correct"] and judge(c, x["text"]) is not False:
                    bad(f"distractor not rejected: {q['prompt']} :: {x['text']}")
        if "student" in c:
            if judge(c, c["student"]) is not False:
                bad(f"student answer not rejected: {c['student']}")
            if f"answer: {c['student']}\n" not in q["prompt"]:
                bad("student answer not in prompt")
    for e in errs[:60]:
        print("ERROR", *e)
    print(f"checked {n} items")
    print("TOTAL ERRORS", len(errs))
    sys.exit(1 if errs else 0)


main()
