#!/usr/bin/env python3
"""Independent numerical verification of the NEW computed Statistics questions.

Does not import the authoring code. For every id in checks.json it recomputes the
key from the check parameters with its own formulas (pure Python; scipy.special
only for Student t and chi-free functions), then:
  * finds the question in the shipped banks,
  * confirms the recomputed numbers appear in the keyed answer (MC: the correct
    option; others: `answer`, or the joined part answers for open responses),
  * for multiple choice, confirms NO incorrect option also contains them,
  * confirms the check's numeric inputs are printed in the prompt/parts text.
Usage: python3 scripts/verification/verify_expansion.py <output_root>
"""
import json
import math
import os
import re
import statistics as S
import sys
from scipy.special import stdtr, stdtrit

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
CHECKS = json.load(open(os.path.join(ROOT, "scripts", "verification", "checks.json"), encoding="utf-8"))
Qs = {}
for u in ["exploring-data", "sampling-experimentation", "anticipating-patterns", "statistical-inference"]:
    for q in json.load(open(os.path.join(ROOT, "question-banks", "statistics", u + ".json"), encoding="utf-8"))["questions"]:
        Qs[q["id"]] = q

# ------------------------------------------------------------- math
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))


def Phi_inv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if Phi(m) < p else (lo, m)
    return (lo + hi) / 2


tcdf = lambda t, df: float(stdtr(df, t))
tinv = lambda p, df: float(stdtrit(df, p))
tstar = lambda c, df: tinv(1 - (1 - c / 100) / 2, df)
ZSTAR = {80: 1.282, 90: 1.645, 95: 1.96, 98: 2.326, 99: 2.576}
mean = lambda v: sum(v) / len(v)
med = lambda v: float(S.median(v))


def sd(v):
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def quart(v):
    s = sorted(v)
    n = len(s)
    return med(s[: n // 2]), med(s[(n + 1) // 2:])


def corr(x, y):
    mx, my, sx, sy = mean(x), mean(y), sd(x), sd(y)
    return sum((a - mx) / sx * (b - my) / sy for a, b in zip(x, y)) / (len(x) - 1)


def fit(x, y):
    mx, my = mean(x), mean(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    return my - b * mx, b


def bpmf(n, p, k):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def bcdf(n, p, k):
    return sum(bpmf(n, p, i) for i in range(0, k + 1))


def tail(z, alt):
    return {"gt": 1 - Phi(z), "lt": Phi(z), "ne": 2 * (1 - Phi(abs(z)))}[alt]


def ttail(t, df, alt):
    return {"gt": 1 - tcdf(t, df), "lt": tcdf(t, df), "ne": 2 * (1 - tcdf(abs(t), df))}[alt]


EMP = {-3: 0.15, -2: 2.5, -1: 16, 0: 50, 1: 84, 2: 97.5, 3: 99.85}


def K(c):
    """Return list of expected numbers (as they should appear in the key)."""
    k = c["kind"]
    g = c.get
    if k == "count_ge": return [sum(1 for x in c["data"] if x >= c["c"])]
    if k == "count_between": return [sum(1 for x in c["data"] if c["lo"] <= x <= c["hi"])]
    if k == "median": return [med(c["data"])]
    if k == "mean": return [mean(c["data"])]
    if k == "hist_pct_ge":
        n = sum(c["counts"]); return [100 * sum(ct for e, ct in zip(c["edges"], c["counts"]) if e >= c["c"]) / n]
    if k in ("hist_median_bin", "hist_rank_bin"):
        n = sum(c["counts"]); ranks = [c["rank"]] if k == "hist_rank_bin" else ([(n + 1) // 2] if n % 2 else [n // 2, n // 2 + 1])
        cum, bins = 0, set()
        for e, ct in zip(c["edges"], c["counts"]):
            for r in ranks:
                if cum < r <= cum + ct: bins.add(e)
            cum += ct
        assert bins == {c["key_lo"]}, bins
        w = c["edges"][1] - c["edges"][0]
        return [c["key_lo"], c["key_lo"] + w]
    if k == "cum_diff_count": return [round((c["hi"] - c["lo"]) * c["n"])]
    if k == "freq":
        e = c["edges"]; out = [sum(1 for x in c["data"] if e[i] <= x < e[i + 1]) for i in range(len(e) - 1)]
        assert out == c["expect"], out
        return out
    if k == "outliers":
        q1, q3 = quart(c["data"]); i = q3 - q1
        o = [x for x in c["data"] if x < q1 - 1.5 * i or x > q3 + 1.5 * i]; assert o == c["expect"], o; return o
    if k == "fences_outliers":
        q1, q3 = quart(c["data"]); i = q3 - q1
        o = [x for x in c["data"] if x < q1 - 1.5 * i or x > q3 + 1.5 * i]
        assert sorted(o) == sorted(c["expect_out"]), o
        return [q1 - 1.5 * i, q3 + 1.5 * i] + o
    if k == "upper_fence_floor":
        q1, q3 = quart(c["data"]); v = math.floor(q3 + 1.5 * (q3 - q1)); assert v == c["expect"]; return [v]
    if k == "upper_fence": return [c["q3"] + 1.5 * (c["q3"] - c["q1"])]
    if k == "salary_or":
        d = c["data"]; q1, q3 = quart(d); w = [x for x in d if x != max(d)]
        return [mean(d), med(d), q1, q3, q3 - q1, q3 + 1.5 * (q3 - q1), mean(w), med(w)]
    if k == "mean_range": return [mean(c["data"]), max(c["data"]) - min(c["data"])]
    if k == "mean_after_add": return [(c["n"] * c["mean"] + c["new"]) / (c["n"] + 1)]
    if k == "sd_sample": return [sd(c["data"])]
    if k == "mean_median": return [mean(c["data"]), med(c["data"])]
    if k == "mean_sd": return [mean(c["data"]), sd(c["data"])]
    if k == "lin_both": return [c["a"] + c["b"] * c["mean"], abs(c["b"]) * c["sd"]]
    if k == "argmax_sd":
        v = [sd(s) for s in c["sets"]]; assert v.index(max(v)) == c["expect"] and sorted(v)[-1] > sorted(v)[-2]; return []
    if k == "five_iqr":
        d = c["data"]; q1, q3 = quart(d); return [min(d), q1, med(d), q3, max(d), q3 - q1]
    if k == "percentile_below": return [100 * sum(1 for x in c["data"] if x < c["value"]) / len(c["data"])]
    if k == "iqr_pair":
        a, b = quart(c["a"]), quart(c["b"]); return [a[1] - a[0], b[1] - b[0]]
    if k == "five_pair":
        out = []
        for d in (c["a"], c["b"]):
            q1, q3 = quart(d); out += [min(d), q1, med(d), q3, max(d)]
        for d in (c["a"], c["b"]):
            q1, q3 = quart(d); out += [q3 - q1]
        for d in (c["a"], c["b"]):
            q1, q3 = quart(d); i = q3 - q1; out += [q1 - 1.5 * i, q3 + 1.5 * i]
        return out
    if k == "zscore": return [(c["x"] - c["mean"]) / c["sd"]]
    if k == "x_from_z": return [c["mean"] + c["z"] * c["sd"]]
    if k == "empirical":
        lo = 0 if c["lo_k"] is None else EMP[c["lo_k"]]; hi = 100 if c["hi_k"] is None else EMP[c["hi_k"]]; return [hi - lo]
    if k == "normal_area":
        za = round((c["a"] - c["mean"]) / c["sd"], 2)
        if c["type"] == "lt": return [Phi(za)]
        if c["type"] == "gt": return [1 - Phi(za)]
        zb = round((c["b"] - c["mean"]) / c["sd"], 2); return [Phi(zb) - Phi(za)]
    if k == "normal_inverse": return [c["mean"] + Phi_inv(c["area_left"]) * c["sd"]]
    if k == "solve_mean": return [c["x"] - Phi_inv(c["area_left"]) * c["sd"]]
    if k == "uniform_area": return [(c["hi"] - c["lo"]) / (c["b"] - c["a"])]
    if k == "z_or":
        za = (c["a"][0] - c["a"][1]) / c["a"][2]; zb = (c["b"][0] - c["b"][1]) / c["b"][2]; return [za, zb, 1 - Phi(round(za, 2))]
    if k == "twoway":
        t = c["table"]; N = sum(map(sum, t)); rows = [sum(r) for r in t]; cols = [sum(r[j] for r in t) for j in range(len(t[0]))]
        ty = c["type"]
        v = {"marginal_col": lambda: cols[c["col"]] / N, "marginal_row": lambda: rows[c["row"]] / N, "joint": lambda: t[c["row"]][c["col"]] / N,
             "cond_given_row": lambda: t[c["row"]][c["col"]] / rows[c["row"]], "cond_given_col": lambda: t[c["row"]][c["col"]] / cols[c["col"]]}[ty]()
        return [100 * v if g("pct") else v]
    if k == "twoway_count_pct": return [c["count"], 100 * c["count"] / c["total"]]
    if k == "twoway_or":
        t = c["table"]; N = sum(map(sum, t)); cols = [sum(r[j] for r in t) for j in range(len(t[0]))]
        out = [100 * x / N for x in cols]
        for r in t: out += [100 * x / sum(r) for x in r]
        return out
    if k == "equal_rates":
        return [] if (c["a"][0] / c["a"][1] == c["b"][0] / c["b"][1]) == c["expect"] else [float("nan")]
    if k == "simpson":
        a, b = c["a"], c["b"]
        ov = lambda h: 100 * (h[0][0] + h[1][0]) / (h[0][1] + h[1][1])
        return [ov(a), ov(b), 100 * a[0][0] / a[0][1], 100 * b[0][0] / b[0][1], 100 * a[1][0] / a[1][1], 100 * b[1][0] / b[1][1]]
    if k == "correlation": return [corr(c["x"], c["y"])]
    if k == "r_pair": return [corr(c["x"], c["y"]), corr(c["x"][:-1], c["y"][:-1])]
    if k == "predict": return [c["a"] + c["b"] * c["x"]]
    if k == "pred_resid":
        yh = c["a"] + c["b"] * c["x"]; return [yh, c["y"] - yh]
    if k == "residual": return [c["y"] - (c["a"] + c["b"] * c["x"])]
    if k == "r_squared": return [c["r"] ** 2]
    if k == "lsrl_summary_both":
        b = c["r"] * c["sy"] / c["sx"]; return [c["my"] - b * c["mx"], abs(b)]
    if k == "product":
        p = 1
        for v in c["values"]: p *= v
        return [p]
    if k == "sqrt": return [math.sqrt(c["v"])]
    if k == "lsrl_r2":
        a, b = fit(c["x"], c["y"]); r = corr(c["x"], c["y"]); return [a, b, r * r, 100 * r * r]
    if k == "reverse_slope": return [c["r"] ** 2 / c["b"]]
    if k == "resid_s":
        a, b = fit(c["x"], c["y"]); res = [yy - (a + b * xx) for xx, yy in zip(c["x"], c["y"])]
        i = c["x"].index(c["at"]); return [res[i], math.sqrt(sum(e * e for e in res) / (len(res) - 2))]
    if k == "slope_pair": return [fit(c["x"], c["y"])[1], fit(c["x"][:-1], c["y"][:-1])[1]]
    if k == "actual_from_resid": return [c["a"] + c["b"] * c["x"], c["a"] + c["b"] * c["x"] + c["resid"]]
    if k == "freq_median":
        vals = [v for v, n in zip(c["values"], c["counts"]) for _ in range(n)]; return [med(vals)]
    if k == "freq_mean":
        vals = [v for v, n in zip(c["values"], c["counts"]) for _ in range(n)]; return [mean(vals)]
    if k == "ratio_pct": return [100 * c["num"] / c["den"]]
    # ---------------- unit 2 ----------------
    if k == "count_product":
        p = 1
        for v in c["levels"]: p *= v
        return [p * c.get("reps", 1)]
    if k == "random_digits":
        digs = re.sub(r"\D", "", c["digits"]); w = c["width"]; out = []
        for i in range(0, len(digs) - w + 1, w):
            v = int(digs[i:i + w])
            if c["lo"] <= v <= c["hi"] and v not in out: out.append(v)
            if len(out) == c["n"]: break
        return out
    if k == "alloc":
        N = sum(c["sizes"]); return [c["n"] * s / N for s in c["sizes"]]
    if k == "ratio": return [c["num"] / c["den"]]
    # ---------------- unit 3 ----------------
    if k == "union": return [c["pa"] + c["pb"] - c["pab"]]
    if k == "neither": return [1 - (c["pa"] + c["pb"] - c["pab"])]
    if k == "indep_and": return [c["pa"] * c["pb"]]
    if k == "atleast": return [1 - (1 - c["p"]) ** c["n"]]
    if k == "power": return [c["p"] ** c["n"]]
    if k == "cond": return [c["pab"] / c["pb"]]
    if k == "tree":
        j = c["pa"] * c["pba"]; tot = j + (1 - c["pa"]) * c["pbna"]
        return {"total": [tot], "bayes": [j / tot], "both": [tot, j / tot]}[c["type"]]
    if k == "rv":
        m = sum(x * p for x, p in zip(c["x"], c["p"])); v = sum(p * (x - m) ** 2 for x, p in zip(c["x"], c["p"]))
        out = {"mean": [m], "sd": [math.sqrt(v)], "both": [m, math.sqrt(v)]}[c.get("out", "both")]
        return out
    if k == "rv_cum":
        return [sum(p for x, p in zip(c["x"], c["p"]) if eval(c["cond"], {"x": x}))]
    if k == "missing_p": return [1 - sum(c["p"])]
    if k == "lin_rv": return [c["a"] + c["b"] * c["mean"], abs(c["b"]) * c["sd"]]
    if k == "combine":
        m = sum(s * m_ for s, m_ in zip(c["signs"], c["means"]))
        v = sum((abs(s) ** 2) * sd_ ** 2 for s, sd_ in zip(c["signs"], c["sds"]))
        return [m, math.sqrt(v)]
    if k == "combine_prob":
        m = sum(s * m_ for s, m_ in zip(c["signs"], c["means"])); s_ = math.sqrt(sum((abs(s) ** 2) * x ** 2 for s, x in zip(c["signs"], c["sds"])))
        z = round((c["c"] - m) / s_, 2)
        return [1 - Phi(z)] if c["type"] == "gt" else [Phi(z)]
    if k == "binom":
        n, p, kk = c["n"], c["p"], c["k"]
        return [{"eq": bpmf(n, p, kk), "le": bcdf(n, p, kk), "ge": 1 - bcdf(n, p, kk - 1), "lt": bcdf(n, p, kk - 1), "gt": 1 - bcdf(n, p, kk)}[c["type"]]]
    if k == "binom_ms": return [c["n"] * c["p"], math.sqrt(c["n"] * c["p"] * (1 - c["p"]))]
    if k == "geom":
        q = 1 - c["p"]; kk = c["k"]
        return [{"eq": q ** (kk - 1) * c["p"], "le": 1 - q ** kk, "gt": q ** kk}[c["type"]]]
    if k == "geom_mean": return [1 / c["p"]]
    if k == "phat_ms": return [c["p"], math.sqrt(c["p"] * (1 - c["p"]) / c["n"])]
    if k == "xbar_ms": return [c["mu"], c["sigma"] / math.sqrt(c["n"])]
    if k == "phat_prob":
        s_ = math.sqrt(c["p"] * (1 - c["p"]) / c["n"]); z = round((c["c"] - c["p"]) / s_, 2)
        return [1 - Phi(z) if c["type"] == "gt" else Phi(z)]
    if k == "xbar_prob":
        s_ = c["sigma"] / math.sqrt(c["n"]); z = round((c["c"] - c["mu"]) / s_, 2)
        return [1 - Phi(z) if c["type"] == "gt" else Phi(z)]
    if k == "n_for_sd": return [math.ceil((c["sigma"] / c["target"]) ** 2)]
    if k == "large_counts": return [c["n"] * c["p"], c["n"] * (1 - c["p"])]
    if k == "sum_dice_prob":
        cnt = sum(1 for a in range(1, 7) for b in range(1, 7) if eval(c["cond"], {"s": a + b, "a": a, "b": b})); return [cnt / 36]
    # ---------------- unit 4 ----------------
    if k == "ci_prop":
        ph = c["x"] / c["n"]; me = ZSTAR[c["conf"]] * math.sqrt(ph * (1 - ph) / c["n"]); return [ph - me, ph + me]
    if k == "ci_prop_parts":
        ph = c["x"] / c["n"]; se = math.sqrt(ph * (1 - ph) / c["n"]); me = ZSTAR[c["conf"]] * se; return [ph, se, me]
    if k == "phat_se":
        ph = c["x"] / c["n"]; return [ph, math.sqrt(ph * (1 - ph) / c["n"])]
    if k == "se_prop": return [math.sqrt(c["ph"] * (1 - c["ph"]) / c["n"])]
    if k == "me_from_ci": return [(c["lo"] + c["hi"]) / 2, (c["hi"] - c["lo"]) / 2]
    if k == "samp_size":
        n = 1
        while ZSTAR[c["conf"]] * math.sqrt(c["p"] * (1 - c["p"]) / n) > c["me"] + 1e-12: n += 1
        return [n]
    if k == "samp_size_mean":
        n = 1
        while ZSTAR[c["conf"]] * c["sigma"] / math.sqrt(n) > c["me"] + 1e-12: n += 1
        return [n]
    if k == "tstar": return [tstar(c["conf"], c["df"])]
    if k == "ci_mean":
        me = tstar(c["conf"], c["n"] - 1) * c["s"] / math.sqrt(c["n"]); return [c["xbar"] - me, c["xbar"] + me]
    if k == "ci_mean_data":
        d = c["data"]; n = len(d); me = tstar(c["conf"], n - 1) * sd(d) / math.sqrt(n); return [mean(d), sd(d), mean(d) - me, mean(d) + me]
    if k == "z_test":
        ph = c["x"] / c["n"]; z = (ph - c["p0"]) / math.sqrt(c["p0"] * (1 - c["p0"]) / c["n"]); return [z, tail(z, c["alt"])]
    if k == "z_stat":
        ph = c["x"] / c["n"]; return [(ph - c["p0"]) / math.sqrt(c["p0"] * (1 - c["p0"]) / c["n"])]
    if k == "z_p_only": return [tail(c["z"], c["alt"])]
    if k == "t_test":
        t = (c["xbar"] - c["mu0"]) / (c["s"] / math.sqrt(c["n"])); return [t, ttail(t, c["n"] - 1, c["alt"])]
    if k == "t_stat":
        return [(c["xbar"] - c["mu0"]) / (c["s"] / math.sqrt(c["n"]))]
    if k == "t_p_only": return [ttail(c["t"], c["df"], c["alt"])]
    if k == "two_prop_ci":
        p1, p2 = c["x1"] / c["n1"], c["x2"] / c["n2"]; me = ZSTAR[c["conf"]] * math.sqrt(p1 * (1 - p1) / c["n1"] + p2 * (1 - p2) / c["n2"])
        return [p1 - p2 - me, p1 - p2 + me]
    if k == "two_prop_test":
        p1, p2 = c["x1"] / c["n1"], c["x2"] / c["n2"]; pc = (c["x1"] + c["x2"]) / (c["n1"] + c["n2"])
        z = (p1 - p2) / math.sqrt(pc * (1 - pc) * (1 / c["n1"] + 1 / c["n2"])); return [pc, z, tail(z, c["alt"])]
    if k == "two_t_ci":
        se = math.sqrt(c["s1"] ** 2 / c["n1"] + c["s2"] ** 2 / c["n2"]); df = min(c["n1"], c["n2"]) - 1; me = tstar(c["conf"], df) * se
        d = c["m1"] - c["m2"]; return [d - me, d + me]
    if k == "two_t_test":
        se = math.sqrt(c["s1"] ** 2 / c["n1"] + c["s2"] ** 2 / c["n2"]); df = min(c["n1"], c["n2"]) - 1; t = (c["m1"] - c["m2"]) / se
        return [t, ttail(t, df, c["alt"])]
    if k == "paired":
        d = [a - b for a, b in zip(c["a"], c["b"])]; n = len(d); t = mean(d) / (sd(d) / math.sqrt(n))
        out = [mean(d), sd(d)]
        if c.get("out") == "ci":
            me = tstar(c["conf"], n - 1) * sd(d) / math.sqrt(n); return out + [mean(d) - me, mean(d) + me]
        return out + [t, ttail(t, n - 1, c["alt"])]
    if k == "paired_summary":
        t = c["dbar"] / (c["sd"] / math.sqrt(c["n"])); return [t, ttail(t, c["n"] - 1, c["alt"])]
    if k == "slope_ci":
        me = tstar(c["conf"], c["n"] - 2) * c["se"]; return [c["b"] - me, c["b"] + me]
    if k == "slope_t":
        t = c["b"] / c["se"]; return [t, ttail(t, c["n"] - 2, c["alt"])]
    if k == "power_calc":
        # one-sided upper z test for a proportion: reject if p-hat > p0 + z*·SD0; power at pa
        sd0 = math.sqrt(c["p0"] * (1 - c["p0"]) / c["n"]); crit = c["p0"] + ZSTAR[{0.05: 90, 0.01: 98}[c["alpha"]]] * sd0
        sda = math.sqrt(c["pa"] * (1 - c["pa"]) / c["n"]); return [crit, 1 - Phi((crit - c["pa"]) / sda)]
    if k == "expr":
        env = {"corr": corr, "Phi": Phi, "Phi_inv": Phi_inv, "tstar": tstar, "tcdf": tcdf, "sqrt": math.sqrt,
               "comb": math.comb, "ceil": math.ceil, "__builtins__": {}}
        return [eval(c["expr"], env)]
    raise KeyError(k)


NUM = re.compile(r"(?<![A-Za-z_\d])[−-]?\d[\d,]*(?:\.\d+)?")


def numbers(text):
    out = []
    for m in NUM.findall(text):
        t = m.replace("−", "-").replace(",", "")
        d = len(t.split(".")[1]) if "." in t else 0
        out.append((float(t), d))
    return out


def contains_all(text, exp, tol, key_decimals=None):
    got = numbers(text)
    if key_decimals is not None:  # judge distractors at the key's displayed precision
        got = [(v, max(d, key_decimals)) for v, d in got]
    if "%" in text:
        got = got + [(v / 100, d + 2) for v, d in got]
    for e in exp:
        ok = False
        for v, d in got:
            t = max(tol, 0.5 * 10 ** (-d) + 1e-9)
            if abs(v - e) <= t or (e < 0 and abs(v + e) <= t and "−" in text):
                ok = True
                break
        if not ok:
            return False
    return True


def printed(q, c):
    text = q["prompt"] + " " + " ".join(p["prompt"] for p in q.get("parts", []))
    if q.get("diagram"):
        text += " " + q["diagram"]["spec"].get("alt", "")
    if c.get("no_print_check"):
        return []
    vals = [v for v, _ in numbers(text)]
    miss = []
    for key, val in c.items():
        if key in ("kind", "type", "alt", "expect", "expect_out", "key_lo", "out", "tol", "pct", "cond", "sets", "signs", "rank", "digits", "width", "row", "col", "expr", "lo_k", "hi_k", "verify_only", "skip_distractors", "no_print_check"):
            continue
        flat = val if isinstance(val, list) else [val]
        fl = []
        for x in flat:
            fl += x if isinstance(x, list) else [x]
        for x in fl:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                continue
            if not any(abs(x - v) < 1e-9 or abs(abs(x) - abs(v)) < 1e-9 or abs(100 * x - v) < 1e-7 for v in vals):
                miss.append(f"{key}={x}")
    return miss


fails, warns, n_ok = [], [], 0
for qid, c in CHECKS.items():
    q = Qs.get(qid)
    if q is None:
        fails.append(f"{qid}: not in banks"); continue
    try:
        exp = K(c)
    except AssertionError as e:
        fails.append(f"{qid}: internal expectation mismatch {e}"); continue
    except Exception as e:
        fails.append(f"{qid}: compute error {e!r}"); continue
    if any(isinstance(x, float) and math.isnan(x) for x in exp):
        fails.append(f"{qid}: expected property false"); continue
    tol = c.get("tol", 0.0)
    if c.get("verify_only"):
        ev = c["expect"] if isinstance(c["expect"], list) else [c["expect"]]
        if len(ev) != len(exp) or any(abs(a - b) > max(tol, 1e-6) for a, b in zip(ev, exp)):
            fails.append(f"{qid}: property check {exp} vs stated {ev}")
        n_ok += 1
        continue
    if q["format"] == "multiple-choice":
        key = next(o["text"] for o in q["options"] if o["correct"])
        if exp and not contains_all(key, exp, tol):
            fails.append(f"{qid}: MC key {key!r} does not show {[round(x, 5) for x in exp]}")
        for o in q["options"]:
            kd = max((d for _, d in numbers(key)), default=0)
            if not o["correct"] and not c.get("skip_distractors") and exp and contains_all(o["text"], exp, tol, kd) and numbers(o["text"]):
                fails.append(f"{qid}: distractor {o['text']!r} also matches")
    else:
        text = q["answer"] if isinstance(q["answer"], str) else " ".join(map(str, q["answer"]))
        if q["format"] == "open-response":
            text += " " + " ".join(str(p["answer"]) for p in q["parts"])
        if exp and not contains_all(text, exp, tol):
            fails.append(f"{qid}: answer {text[:120]!r} does not show {[round(x, 5) for x in exp]}")
    for m in printed(q, c):
        warns.append(f"{qid}: input {m} not found in printed text")
    n_ok += 1

# Partner Check pairs: exactly one A and one B per pair id, same skill/level, same answer,
# different prompts.
pairs = {}
for q in Qs.values():
    m = re.search(r"Partner Check pair (\S+) \((A|B)\)", q.get("sourceNotes", ""))
    if m:
        pairs.setdefault(m.group(1), {})[m.group(2)] = q
for pid, d in pairs.items():
    if set(d) != {"A", "B"}:
        fails.append(f"{pid}: pair incomplete {sorted(d)}"); continue
    a, b = d["A"], d["B"]
    if a["answer"] != b["answer"]:
        fails.append(f"{pid}: answers differ {a['answer']!r} vs {b['answer']!r}")
    if (a["skillId"], a["level"]) != (b["skillId"], b["level"]):
        fails.append(f"{pid}: pair spans different skill/level")
    if a["prompt"].split(". ", 1)[-1] == b["prompt"].split(". ", 1)[-1]:
        fails.append(f"{pid}: partners have identical problems")
print(f"partner pairs checked: {len(pairs)}")
print(f"checked {n_ok}/{len(CHECKS)} computed items")
for w in warns:
    print("WARN", w)
for f in fails:
    print("FAIL", f)
print("ALL NUMERICAL CHECKS PASSED" if not fails else f"{len(fails)} FAILURES")
sys.exit(1 if fails else 0)
