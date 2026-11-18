"""Independent verifier for the Precalculus audit gap skills (batch P4).

For every item recorded in out/checks.json it:
  1. confirms the parameters it uses are printed in the prompt (check["show"]),
  2. recomputes the answer from those parameters with its own formulas (complex arithmetic, math.comb, …) and
     compares it with the keyed answer read back from the display text by ../mathx.py,
  3. requires every multiple-choice distractor and every find-the-mistake student answer to be wrong,
  4. requires every open-response part to be right,
  5. checks structure: exactly one correct option, four distinct options, the student answer printed in the prompt.
It never imports families.py.

Usage: python3 tools/precalculus-audit-20261118/gaps/verify.py   → prints TOTAL ERRORS n
"""
import cmath, json, math, os, re, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))
import mathx  # noqa: E402

D = math.pi / 180


def ev(t, **env):
    t = t.replace("√", "√").strip()
    return complex(mathx.ev(t, env or None))


def same(a, b, tol=1e-7):
    return abs(complex(a) - complex(b)) <= tol * max(1, abs(complex(b)))


def cis(r, deg):
    return r * cmath.exp(1j * deg * D)


def roots_list(text):
    """'x = 2 or x = -3' / 'θ = π/3 or θ = 5π/3' → sorted values."""
    parts = [p.strip() for p in re.split(r"\s+or\s+", text)]
    vals = []
    for p in parts:
        m = re.match(r"^[xθ]\s*=\s*(.+)$", p)
        if not m:
            return None
        vals.append(ev(m.group(1)).real)
    return sorted(vals)


def fn_check(text, f, xs):
    """Display-text expression in x equals f at every sample point."""
    try:
        return all(same(ev(text, x=x), f(x), 1e-6) for x in xs)
    except Exception:
        return False


# ------------------------------------------------------------------ expected answers, from the check data only
def expect(c):
    """Return a predicate on the answer text."""
    k = c["k"]
    if k == "ra_simplify":
        a, p, q, s = c["a"], c["p"], c["q"], c["s"]
        f = lambda x: (a * x * x + a * (p + q) * x + a * p * q) / (x * x + (p + s) * x + p * s)
        xs = [x for x in (0.37, 1.91, -2.43, 5.17) if abs(x + p) > 1e-3 and abs(x + s) > 1e-3]
        return lambda t: fn_check(t, f, xs)
    if k == "ra_add":
        a, b, p, q = c["a"], c["b"], c["p"], c["q"]
        f = lambda x: a / (x + p) + b / (x + q)
        return lambda t: fn_check(t, f, [0.37, 1.91, -2.43, 7.17])
    if k == "pf_coef":
        A, B = c["top"]
        p, q = c["p"], c["q"]
        # residue at x = p of (Ax + B)/((x - p)(x - q))
        val = (A * p + B) / (p - q) if c["ask"] == "A" else (A * q + B) / (q - p)
        return lambda t: same(ev(t), val)
    if k == "ra_excluded":
        roots = sorted([c["p"], c["q"]])
        return lambda t: roots_list(t) is not None and len(roots_list(t)) == 2 and all(abs(u - v) < 1e-9 for u, v in zip(roots_list(t), roots))
    if k == "ra_value":
        p, q, x0 = c["p"], c["q"], c["x0"]
        val = ((x0 * x0 - p * p) / (x0 + q)) / ((x0 - p) / (x0 + q))
        return lambda t: same(ev(t), val)
    if k == "inv_table":
        ans = c["xs"][c["ys"].index(c["v"])]
        return lambda t: same(ev(t), ans)
    if k == "inv_restrict_value":
        a, h, kk, cc = c["a"], c["h"], c["kk"], c["c"]
        root = math.sqrt((cc - kk) / a)
        ans = h + root if c["side"] == ">=" else h - root
        return lambda t: same(ev(t), ans)
    if k == "inv_rational":
        a, b, cc = c["a"], c["b"], c["c"]
        v = float(Fraction(c["v"]))
        ans = (cc * v + b) / (v - a)  # solve (ax + b)/(x - c) = v
        return lambda t: same(ev(t), ans)
    if k == "inv_compose":
        m, b = c["m"], c["b"]
        # f(g(x)) = x for all x  ⇔  k = m (both the linear and the cube-root case)
        def ok(t):
            kv = ev(t).real
            g = (lambda x: ((x - b) / kv) ** (1 / 3) if (x - b) / kv >= 0 else -((-(x - b) / kv) ** (1 / 3))) if c["cube"] else (lambda x: (x - b) / kv)
            f = (lambda x: m * x ** 3 + b) if c["cube"] else (lambda x: m * x + b)
            return all(abs(f(g(x)) - x) < 1e-6 for x in (-3.3, 0.7, 4.1, 11.9))
        return ok
    if k == "inv_which_restrict":
        return lambda t: t.strip() == f"x ≥ {c['h']}"
    if k == "cj_product":
        z = complex(c["a"], c["b"])
        return lambda t: same(ev(t), z * z.conjugate())
    if k == "cj_quotient":
        z = complex(*c["t"]) / complex(*c["d"])
        return lambda t: same(ev(t), z)
    if k == "cj_modq":
        z1, z2 = complex(*c["z1"]), complex(*c["z2"])
        val = abs(z1 / z2) if c["op"] == "÷" else abs(z1 * z2)
        return lambda t: same(ev(t), val)
    if k == "cj_recip":
        return lambda t: same(ev(t), 1 / complex(c["a"], c["b"]))
    if k == "cj_solve":
        z = complex(c["a"], c["b"])
        return lambda t: same(ev(t), z + z.conjugate() if c["which"] == "sum" else z - z.conjugate())
    if k == "pol_mult":
        return lambda t: same(ev(t), cis(c["r"][0], c["t"][0]) * cis(c["r"][1], c["t"][1]))
    if k == "pol_div":
        return lambda t: same(ev(t), cis(c["r"][0], c["t"][0]) / cis(c["r"][1], c["t"][1]))
    if k == "dm_power":
        return lambda t: same(ev(t), cis(c["r"], c["t"]) ** c["n"])
    if k == "dm_rect_power":
        z = complex(c["a"], c["b"])
        if c["sq3"]:
            # the base is 1 ± √3 i, -1 + √3 i, √3 ± i: the part shown with 3 in the data is √3
            z = complex(math.copysign(math.sqrt(3), c["a"]) if abs(c["a"]) == 3 else c["a"], math.copysign(math.sqrt(3), c["b"]) if abs(c["b"]) == 3 else c["b"])
        return lambda t: same(ev(t), z ** c["n"], 1e-6)
    if k == "dm_modulus":
        return lambda t: same(ev(t), abs(complex(c["a"], c["b"])) ** c["n"], 1e-9)
    if k == "dm_root":
        n = c["n"]
        roots = [cis(c["R"] ** (1 / n), (c["T"] + 360 * j) / n) for j in range(n)]
        best = min(roots, key=lambda z: (cmath.phase(z) % (2 * math.pi)) if abs(cmath.phase(z) % (2 * math.pi)) > 1e-9 else 99)
        return lambda t: same(ev(t), best, 1e-9) and same(ev(t) ** n, cis(c["R"], c["T"]), 1e-6)
    if k == "lim_classify":
        ratio = c["a"] / abs(c["b"])
        name = ("a limaçon with an inner loop" if ratio < 1 else "a cardioid" if ratio == 1 else "a dimpled limaçon" if ratio < 2 else "a convex limaçon")
        return lambda t: t == name
    if k == "lim_max":
        a, b = c["a"], c["b"]
        m = max(abs(a + b * math.cos(th / 1000)) for th in range(0, 6284))
        return lambda t: same(ev(t), m, 1e-5)
    if k == "lim_value":
        f = math.cos if c["fn"] == "cos" else math.sin
        return lambda t: same(ev(t), c["a"] + c["b"] * f(c["deg"] * D), 1e-9)
    if k in ("lim_pole", "lim_pole2"):
        f = math.cos if c["fn"] == "cos" else math.sin
        sols = sorted(j * math.pi / 12 for j in range(24) if abs(c["a"] + c["b"] * f(j * math.pi / 12)) < 1e-9)
        return lambda t: roots_list(t) is not None and len(roots_list(t)) == len(sols) and all(abs(u - v) < 1e-9 for u, v in zip(roots_list(t), sols))
    if k == "lim_symmetry":
        return lambda t: t == ("the polar axis (the x-axis)" if c["fn"] == "cos" else "the line θ = π/2 (the y-axis)")
    if k == "bn_coef":
        n, kk, a, b = c["n"], c["kk"], c["a"], c["b"]
        # coefficient of xᵏ in (ax + b)ⁿ by expanding the polynomial product directly
        coeffs = [1]
        for _ in range(n):
            nxt = [0] * (len(coeffs) + 1)
            for i, v in enumerate(coeffs):
                nxt[i] += v * b
                nxt[i + 1] += v * a
            coeffs = nxt
        return lambda t: same(ev(t), coeffs[kk])
    if k == "bn_term":
        n, tt, a, b = c["n"], c["t"], c["a"], c["b"]
        coeffs = [1]
        for _ in range(n):
            nxt = [0] * (len(coeffs) + 1)
            for i, v in enumerate(coeffs):
                nxt[i] += v * b
                nxt[i + 1] += v * a
            coeffs = nxt
        p = n - (tt - 1)  # descending powers: term t has x^(n - t + 1)
        return lambda t: fn_check(t, lambda x: coeffs[p] * x ** p, [1.3, -0.7, 2.1])
    if k == "bn_pascal":
        row = [1]
        for _ in range(c["n"]):
            row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
        return lambda t: same(ev(t), row[c["kk"]])
    if k == "bn_sum":
        return lambda t: same(ev(t), (c["a"] + c["b"]) ** c["n"])
    if k == "bn_expand":
        a, b, n = c["a"], c["b"], c["n"]
        return lambda t: fn_check(t, lambda x: (a * x + b) ** n, [1.3, -0.7, 2.1, 0.4, -1.9])
    if k == "cn_onesided":
        m1, b1, m2, b2 = c["p"]
        x = c["c"] + (-1e-9 if c["side"] == "-" else 1e-9)
        val = m1 * x + b1 if x < c["c"] else m2 * x + b2
        return lambda t: t != "does not exist" and same(ev(t), val, 1e-6)
    if k == "cn_param":
        cc, a, b = c["c"], c["a"], c["b"]
        return lambda t: abs(cc * cc + a - (ev(t).real * cc + b)) < 1e-9
    if k == "cn_removable":
        p, q = c["p"], c["q"]
        h = 1e-7
        val = (((p + h) ** 2 - (p + q) * (p + h) + p * q) / h)
        return lambda t: not t.startswith("no value") and same(ev(t), val, 1e-5)
    if k == "cn_infinite":
        a, cc, pw = c["a"], c["c"], c["pw"]
        x = cc + (1e-9 if c["side"] == "+" else -1e-9)
        v = a / (x - cc) ** pw
        return lambda t: t == ("∞" if v > 0 else "-∞")
    if k == "cn_exists":
        m1, b1, m2, b2 = c["p"]
        l1, l2 = m1 * c["c"] + b1, m2 * c["c"] + b2
        if l1 == l2:
            return lambda t: not t.startswith("The limit does not") and re.fullmatch(r"-?\d+", t) is not None and same(ev(t), l1)
        return lambda t: t == "The limit does not exist."
    raise KeyError(k)


def right(pred, text):
    try:
        return bool(pred(text))
    except Exception:
        return False


def main():
    checks = json.load(open(os.path.join(HERE, "out", "checks.json"), encoding="utf-8"))
    items = {}
    for f in os.listdir(os.path.join(ROOT, "question-banks", "precalculus")):
        if f.endswith(".json"):
            for q in json.load(open(os.path.join(ROOT, "question-banks", "precalculus", f), encoding="utf-8"))["questions"]:
                items[q["id"]] = q
    errors, n = [], 0
    for qid, c in checks.items():
        q = items.get(qid)
        if q is None:
            errors.append(f"{qid}: not in the banks")
            continue
        n += 1
        if q["format"] == "open-response":
            for i, (part, pc) in enumerate(zip(q["parts"], c["parts"])):
                for s in pc.get("show", []):
                    if s not in part["prompt"]:
                        errors.append(f"{qid} part {i}: {s!r} not printed")
                if not right(expect(pc), part["answer"]):
                    errors.append(f"{qid} part {i}: answer {part['answer']!r} is wrong")
            continue
        for s in c.get("show", []):
            if s not in q["prompt"]:
                errors.append(f"{qid}: {s!r} not printed")
        pred = expect(c)
        if not right(pred, q["answer"]):
            errors.append(f"{qid}: answer {q['answer']!r} is wrong ({q['prompt'][:80]!r})")
        if q["format"] == "multiple-choice":
            opts = q["options"]
            if len(opts) != 4 or len({o["text"] for o in opts}) != 4:
                errors.append(f"{qid}: needs four distinct options")
            if [o["text"] for o in opts if o["correct"]] != [q["answer"]]:
                errors.append(f"{qid}: exactly one correct option, equal to the answer")
            for o in opts:
                if not o["correct"] and right(pred, o["text"]):
                    errors.append(f"{qid}: distractor {o['text']!r} is also right")
        if "student" in c:
            if right(pred, c["student"]):
                errors.append(f"{qid}: the student answer {c['student']!r} is right")
            if f"answer: {c['student']}\n" not in q["prompt"]:
                errors.append(f"{qid}: the student answer is not printed")
    for e in errors[:60]:
        print(e)
    print(f"checked {n} items")
    print(f"TOTAL ERRORS {len(errors)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
