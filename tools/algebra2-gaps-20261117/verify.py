"""Independent check of the Algebra 2 batch D items (2026-11-17).

For every item written by build.py (sourceNotes name this tool), recompute the answer from the check
parameters with formulas written separately from families.py (this file never imports it), then:
- the keyed answer (or each part's answer) must equal the recomputed value;
- every multiple-choice distractor and every find-the-mistake student answer must differ from it;
- every check["show"] text must be printed in the prompt, so the parameters are the ones students see.
Prints TOTAL ERRORS 0 and exits 0 when everything passes.

Usage: python3 tools/algebra2-gaps-20261117/verify.py
"""
import glob, json, math, os, re, sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
checks = json.load(open(os.path.join(HERE, "out", "checks.json"), encoding="utf-8"))


def norm(s):
    s = str(s).strip().replace("−", "-").replace(",", "").replace("$", "").replace(" ", "")
    return s.rstrip(".")


def as_num(s):
    s = norm(s).rstrip("%")
    try:
        return Fr(s)
    except (ValueError, ZeroDivisionError):
        return None


def same(a, b):
    """Numbers compare by value (3/4 = 0.75; '12,000' = 12000); everything else as normalized text."""
    na, nb = as_num(a), as_num(b)
    if na is not None and nb is not None:
        return na == nb and str(a).strip().endswith("%") == str(b).strip().endswith("%")
    return norm(a).lower() == norm(b).lower()


def rnd(x, dp):
    return f"{x:.{dp}f}"


def bisect(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(lo) < 0) == (f(mid) < 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def solve(c):
    k = c["k"]
    if k == "cmp_rate":
        def fx(x):
            f = c["f"]
            if f["t"] == "lin":
                return Fr(f["m"]) * x + f["b"]
            if f["t"] == "quad":
                return Fr(f["a"]) * (x - f["h"]) ** 2 + f["k"]
            return Fr(f["a"]) * Fr(f["b"]) ** x
        gx = {x: c["n"] * x + c["c"] for x in c["xs"]}
        d = c["x2"] - c["x1"]
        return str(abs((fx(c["x2"]) - fx(c["x1"])) / d - Fr(gx[c["x2"]] - gx[c["x1"]], d)))
    if k == "cmp_max":
        return str(max(c["kk"], max(c["gv"])))  # a < 0, so f's maximum is kk; g's maximum is its largest table value at the axis
    if k == "cmp_cross":
        (x1, y1), (x2, y2) = c["p1"], c["p2"]
        m1 = Fr(y2 - y1, x2 - x1)
        b1 = y1 - m1 * x1
        return str((c["b2"] - b1) / (m1 - c["m2"]))
    if k == "cmp_plans":
        xs, bv = c["xs"], c["bv"]
        rb = Fr(bv[1] - bv[0], xs[1] - xs[0])
        fb = bv[0] - rb * xs[0]
        return str((fb - c["F1"]) / (c["r1"] - rb))
    if k == "cmp_zero":
        xs, gv = c["xs"], c["gv"]
        zg = [x for x, v in zip(xs, gv) if v == 0]
        return str(max([c["p"], c["q"]] + zg))
    if k == "par_point":
        t = c["t0"]
        y = c["c"] * t * t + c["d"] if c["sq"] else c["c"] * t + c["d"]
        return f"({c['a'] * t + c['b']}, {y})"
    if k == "par_t":
        t = Fr(c["X"] - c["b"], c["a"])
        return str(c["c"] * t * t + c["d"] if c["sq"] else c["c"] * t + c["d"])
    if k == "par_elim":
        # t = (x - h)/a; y = ma·t + c = (ma/a)x + c - (ma/a)h
        return str(c["c"] - Fr(c["ma"], c["a"]) * c["h"])
    if k == "par_land":
        a, b, cc = -16, c["vy"], c["h0"]
        T = max((-b + s * math.sqrt(b * b - 4 * a * cc)) / (2 * a) for s in (1, -1))
        return str(round(c["vx"] * T, 9)).rstrip("0").rstrip(".")
    if k in ("par_max", "qmax"):
        a, b, cc = (-16, c["vy"], c["h0"]) if k == "par_max" else (c["a"], c["b"], c["c"])
        return str(Fr(cc) - Fr(b * b, 4 * a))
    if k == "ie_growth":
        return str((Fr(c["fac"]) - 1) * 100) + "%"
    if k == "ie_decay":
        return str((1 - Fr(c["fac"])) * 100) + "%"
    if k == "ie_initial":
        return str(c["A"])
    if k == "ie_double":
        return str(c["d"])
    if k == "ie_monthly":
        return rnd((float(Fr(c["fac"])) ** (1 / 12) - 1) * 100, 2) + "%"
    if k == "ie_items":
        return str(c["N"] - c["c"] * c["p"])
    if k == "ie_vertex":
        return str(c["top"])
    if k in ("fact",):
        return c["key"]
    if k == "fg_quad":
        a, b, cc = c["f"]
        B, C = b - c["m"], cc - c["c"]
        disc = B * B - 4 * a * C
        r = math.isqrt(disc)
        assert r * r == disc
        roots = sorted({Fr(-B - r, 2 * a), Fr(-B + r, 2 * a)})
        return " and ".join(f"x = {x}" for x in roots)
    if k == "fg_count":
        xs = [i / 1000 for i in range(-40000, 40001)]
        # Evaluate the printed function numerically and count sign changes of f - c (plus touching points).
        f = lambda x: evalf(c["ft"], x) - c["c"]
        cnt, prev = 0, f(xs[0])
        for x in xs[1:]:
            v = f(x)
            if v == 0 or (prev < 0) != (v < 0) and prev != 0:
                cnt += 1
            prev = v
        return str(cnt)
    if k == "fg_between":
        f = lambda x: c["b"] ** x - x - c["c"]
        x = bisect(f, 0.0, 20.0)
        return str(math.floor(x))
    if k == "fg_sqrt":
        return f"({(c['kk'] - c['b']) ** 2 - c['a']}, {c['kk']})"
    if k == "fg_log":
        return f"({c['base'] ** c['kk'] + c['a']}, {c['kk']})"
    if k == "fg_calc":
        return rnd(bisect(lambda x: c["b"] ** x + x - c["c"], -5.0, 10.0), 2)
    if k == "fg_towns":
        t = 0
        while not c["B0"] * Fr(1 + Fr(c["gr"])) ** t > c["A0"] + c["d"] * t:
            t += 1
        return str(t)
    if k == "ratio":
        return str(float(Fr(c["num"], c["den"]))).rstrip("0").rstrip(".") if c["num"] else "0"
    if k == "product":
        return str(c["a"] * Fr(c["b"]))
    if k == "dot_frac":
        k_ = sum(f for v, f in zip(c["vals"], c["freqs"]) if v >= c["cut"])
        return str(Fr(k_, sum(c["freqs"])))
    if k in ("decide", "decide_lt"):
        p = Fr(c["num"], c["den"])
        unusual = p < Fr(1, 20)
        if k == "decide":  # is the model consistent with the data?
            return c["no"] if unusual else c["yes"]
        return c["yes"] if unusual else c["no"]  # is the treatment difference significant?
    if k == "binsd":
        p = Fr(c["p"])
        return rnd(math.sqrt(c["n"] * p * (1 - p)), 2)
    if k == "diffmean":
        return str(Fr(sum(c["t"]), len(c["t"])) - Fr(sum(c["c"]), len(c["c"])))
    if k == "diffprop":
        return str(float(Fr(c["a"] - c["b"], c["n"]))).rstrip("0").rstrip(".")
    if k == "moe_end":
        return f"{c['p'] - c['m'] if c['lo'] else c['p'] + c['m']}%"
    if k == "majority":
        return c["yes"] if c["p"] - c["m"] > 50 else c["no"]
    if k == "pctchange":
        return str(Fr(c["b"] - c["a"], c["a"]) * 100) + "%"
    if k == "risk":
        return str(c["y"] - c["x"]) if c["ask"] == "abs" else str(Fr(c["y"] - c["x"], c["x"]) * 100) + "%"
    if k == "axis":
        return rnd((c["b"] - c["a"]) / c["a"] * 100, 1) + "%"
    if k == "qroot":
        a, b, cc = c["a"], c["b"], c["c"]
        d = math.sqrt(b * b - 4 * a * cc)
        T = max((-b + d) / (2 * a), (-b - d) / (2 * a))
        return str(round(T, 9)).rstrip("0").rstrip(".")
    if k == "fence":
        # x(F - 2x) against a wall; x(F/2 - x) for a closed rectangle; maximize by checking the vertex numerically
        Fl = c["F"]
        f = (lambda x: x * (Fl - 2 * x)) if c["wall"] else (lambda x: x * (Fl / 2 - x))
        return str(round(max(f(i / 100) for i in range(0, Fl * 100))))
    if k == "revenue":
        best = max(range(0, 200), key=lambda x: (c["P"] + x) * (c["N"] - c["c"] * x))
        return f"${c['P'] + best}"
    if k == "box":
        x = c["x"]
        return str(x * (c["L"] - 2 * x) * (c["W"] - 2 * x))
    if k == "boxsolve":
        f = lambda x: x * (x + c["a"]) * (x + c["b"]) - c["V"]
        pos = [i for i in range(1, 200) if f(i) == 0]
        assert len(pos) == 1 and bisect(f, 0.0, 200.0) - pos[0] < 1e-6
        return str(pos[0])
    if k == "cube":
        e = round(c["V"] ** (1 / 3))
        assert e ** 3 == c["V"]
        return str(e - c["c"])
    if k == "skid":
        return str(Fr(c["s"] ** 2) / (30 * Fr(c["f"])))
    if k == "horizon_h":
        return str(Fr(c["d"] ** 2) / Fr(3, 2))
    if k == "horizon_d":
        v = math.sqrt(1.5 * c["h"])
        assert abs(v - round(v)) < 1e-9
        return str(round(v))
    if k == "pendulum":
        return rnd(2 * math.pi * math.sqrt(c["L"] / 32), 2)
    if k == "work":
        return str(1 / (Fr(1, c["a"]) + Fr(1, c["b"])))
    if k == "work_other":
        return str(1 / (Fr(1, c["t"]) - Fr(1, c["a"])))
    if k == "avgcost":
        return str(Fr(c["F"], c["c"] - c["v"]))
    if k == "mix":
        return str(Fr(c["V"] * (c["q"] - c["p"]), 100 - c["q"]))
    if k == "inverse":
        return str(Fr(c["n1"] * c["t1"], c["n2"]))
    if k == "dish":
        return str(Fr((c["w"] / 2) ** 2) / (4 * c["d"])) if c["w"] % 2 == 0 else None
    if k in ("dist", "dist2"):
        d2 = (c["q"][0] - c["p"][0]) ** 2 + (c["q"][1] - c["p"][1]) ** 2
        if k == "dist2":
            return str(d2)
        assert math.isqrt(d2) ** 2 == d2
        return str(math.isqrt(d2))
    if k == "arch":
        a = Fr(c["H"], (c["W"] // 2) ** 2)
        return str(c["H"] - a * c["d"] ** 2)
    if k == "aterm":
        return f"{c['a'] + (c['n'] - 1) * c['d']:,}"
    if k == "aseries":
        return f"{sum(c['a'] + i * c['d'] for i in range(c['n'])):,}"
    if k == "gterm":
        return f"{c['a'] * c['r'] ** (c['n'] - 1):,}"
    if k == "ball":
        q = Fr(c["q"])
        return str(c["h"] + 2 * c["h"] * q / (1 - q))
    if k == "ferris":
        return str(round(c["C"] - c["R"] * math.cos(2 * math.pi * c["t"] / c["T"])))
    if k == "temp":
        vals = [c["A"] * math.sin(math.pi / 6 * (m - 4)) + c["M"] for m in [i / 100 for i in range(0, 1300)]]
        hi, lo = round(max(vals), 6), round(min(vals), 6)
        return str(round({"max": hi, "min": lo, "range": hi - lo}[c["ask"]]))
    if k == "tickets":
        # a + s = T, A·a + C·s = R  →  a = (R - C·T)/(A - C)
        return str(Fr(c["R"] - c["C"] * c["T"], c["A"] - c["C"]))
    if k == "breakeven":
        return str(Fr(c["F"], c["p"] - c["v"]))
    if k == "taxi":
        rate = (Fr(c["f2"]) - Fr(c["f1"])) / (c["m2"] - c["m1"])
        v = Fr(c["f1"]) - rate * c["m1"] if c["ask"] == "base" else rate
        return f"{float(v):.2f}"
    if k == "tide":
        return str(2 * c["kk"])
    raise KeyError(k)


def evalf(text, x):
    """Evaluate the printed f(x) text for fg_count (|...|, (...)², b^x, + k)."""
    s = text.replace("²", "**2").replace("^x", "**x")
    s = re.sub(r"\|([^|]+)\|", r"abs(\1)", s)
    return eval(s, {"__builtins__": {}, "abs": abs, "x": x})


errors = 0
n = 0
for path in sorted(glob.glob(os.path.join(ROOT, "question-banks", "algebra2", "*.json"))):
    for q in json.load(open(path, encoding="utf-8"))["questions"]:
        if "algebra2-gaps-20261117" not in q.get("sourceNotes", ""):
            continue
        n += 1
        c = checks.get(q["id"])
        if c is None:
            print("NO CHECK", q["id"]); errors += 1; continue
        try:
            if "parts" in c:
                for i, (pc, part) in enumerate(zip(c["parts"], q["parts"])):
                    want = solve(pc)
                    if not same(want, part["answer"]):
                        print("PART", q["id"], i, part["answer"], "!=", want); errors += 1
                    for s in pc.get("show", []):
                        if s not in part["prompt"]:
                            print("SHOW", q["id"], i, s); errors += 1
                continue
            want = solve(c)
            if want is None or not same(want, q["answer"]):
                print("KEY", q["id"], q["answer"], "!=", want); errors += 1
            for s in c.get("show", []):
                if s not in q["prompt"]:
                    print("SHOW", q["id"], s); errors += 1
            for o in q.get("options", []):
                if o["correct"] != same(o["text"], want):
                    print("OPTION", q["id"], o); errors += 1
            if "student" in c and (same(c["student"], want) or f"answer: {c['student']}" not in q["prompt"]):
                print("STUDENT", q["id"], c["student"]); errors += 1
        except Exception as e:  # noqa: BLE001
            print("ERROR", q["id"], type(e).__name__, e); errors += 1
print(f"checked {n} items")
print(f"TOTAL ERRORS {errors}")
sys.exit(1 if errors or n == 0 else 0)
