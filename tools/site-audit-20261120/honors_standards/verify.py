"""Independent check of the whole-site audit 2 #7 items (honors-only standards).

Every answer, multiple-choice option and printed parameter is recomputed from out/checks.json with formulas
written separately from families.py. Must print TOTAL ERRORS 0.

Usage: python3 tools/site-audit-20261120/honors_standards/verify.py
"""
import cmath, json, math, os, re, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def frac(t):
    t = t.strip().replace("−", "-").replace(",", "")
    return Fraction(t)


def poly_text(t):
    """Evaluate a factored polynomial such as 3(x - (-5 + 8i))(x - (-5 - 8i)) as a Python function of x."""
    s = t.replace("−", "-").replace("²", "**2").replace(" ", "")
    if not re.fullmatch(r"[0-9x()+\-i*]+", s):
        raise ValueError(t)
    s = re.sub(r"(\d)i", r"\1*1j", s)
    s = re.sub(r"(?<![\d*])i", "1j", s)
    s = s.replace(")(", ")*(")
    s = re.sub(r"^(\d+)\(", r"\1*(", s)
    s = re.sub(r"\)x", ")*x", s)
    code = compile(s, "<answer>", "eval")
    return lambda x: eval(code, {"__builtins__": {}}, {"x": x})


def matmul(A, B):
    n = len(A)
    return [[sum(A[i][t] * B[t][j] for t in range(n)) for j in range(n)] for i in range(n)]


def expect(c):
    k = c["k"]
    if k == "cn_factor":
        a, b, cc = c["c"]
        f = lambda x: a * x * x + b * x + cc
        pts = [0.3 + 0.7j, -1.1 + 2j, 2.5 - 0.4j, 4]
        def ok(t):
            g = poly_text(t)
            return all(abs(g(x) - f(x)) < 1e-6 * max(1, abs(f(x))) for x in pts) and "i" in t and t.count("(") >= 2
        return ok
    if k in ("vm_comm", "vm_dist", "vm_assoc"):
        A, B, i, j = c["A"], c["B"], c["i"] - 1, c["j"] - 1
        if k == "vm_comm":
            AB, BA = matmul(A, B), matmul(B, A)
            want = AB[i][j] - BA[i][j]
        elif k == "vm_dist":
            C = c["C"]
            S = [[B[r][s] + C[r][s] for s in range(2)] for r in range(2)]
            want = matmul(A, S)[i][j]
        else:
            want = matmul(A, matmul(B, c["C"]))[i][j]
        return lambda t: frac(t) == want
    if k == "tf_sym":
        cs, sn = float(frac(c["cos"])), float(frac(c["sin"]))
        assert abs(cs * cs + sn * sn - 1) < 1e-12
        th = math.atan2(sn, cs)
        arg = {"-θ": -th, "θ + 2π": th + 2 * math.pi, "θ - 2π": th - 2 * math.pi, "θ + π": th + math.pi, "θ - π": th - math.pi, "π - θ": math.pi - th}[c["tr"]]
        want = getattr(math, c["fn"])(arg)
        return lambda t: abs(float(frac(t)) - want) < 1e-9
    if k == "md_coins":
        n = c["n"]
        want = sum(h * Fraction(math.comb(n, h), 2 ** n) for h in range(n + 1))
        return lambda t: frac(t) == want
    if k == "md_die":
        n = c["n"]
        want = sum(Fraction(f, n) for f in range(1, n + 1))
        return lambda t: frac(t) == want
    if k == "md_draws":
        p, n = Fraction(c["red"], c["red"] + c["blue"]), c["n"]
        want = sum(h * math.comb(n, h) * p ** h * (1 - p) ** (n - h) for h in range(n + 1))
        return lambda t: frac(t) == want
    if k == "md_emp_ev":
        cnt, N = c["counts"], c["N"]
        assert sum(cnt) == N
        want = sum(Fraction(x * v, N) for x, v in enumerate(cnt))
        return lambda t: frac(t) == want
    if k == "md_emp_count":
        cnt, N, M = c["counts"], c["N"], c["M"]
        assert sum(cnt) == N
        want = M * Fraction(sum(v for x, v in enumerate(cnt) if x >= 2), N)
        return lambda t: frac(t) == want
    if k == "md_fair_split":
        n, N = c["n"], c["N"]
        best = max(e for e in range(N + 1) if e * n <= N)
        want = best if c["ask"] == "each" else N - best * n
        assert N - best * n > 0
        return lambda t: frac(t) == want
    if k == "md_fair_dice":
        want = Fraction(sum(1 for x in range(1, 7) for y in range(1, 7) if x + y <= c["s"]), 36)
        return lambda t: frac(t) == want
    if k == "md_screen":
        N, prev, sens, spec = c["N"], Fraction(c["prev"], 100), Fraction(c["sens"], 100), Fraction(c["spec"], 100)
        tp, fp = N * prev * sens, N * (1 - prev) * (1 - spec)
        assert tp.denominator == 1 and fp.denominator == 1
        if c["ask"] == "ppv":
            v = 100 * tp / (tp + fp)
            want = Fraction(math.floor(v * 10 + Fraction(1, 2)), 10)
            return lambda t: t.endswith("%") and frac(t[:-1]) == want and re.fullmatch(r"\d+\.\d%", t) is not None
        want = {"tp": tp, "fp": fp, "pos": tp + fp}[c["ask"]]
        return lambda t: frac(t) == want
    raise KeyError(k)


def right(pred, text):
    try:
        return bool(pred(text))
    except Exception:
        return False


def main():
    checks = json.load(open(os.path.join(HERE, "out", "checks.json"), encoding="utf-8"))
    items = {}
    for course in sorted({c["course"] for c in checks.values()}):
        d = os.path.join(ROOT, "question-banks", course)
        for f in os.listdir(d):
            if f.endswith(".json"):
                for q in json.load(open(os.path.join(d, f), encoding="utf-8"))["questions"]:
                    items[(course, q["id"])] = q
    errors, n = [], 0
    for qid, c in checks.items():
        q = items.get((c["course"], qid))
        if q is None:
            errors.append(f"{qid}: not in the banks")
            continue
        n += 1
        for s in c.get("show", []):
            if s not in q["prompt"]:
                errors.append(f"{qid}: {s!r} not printed")
        pred = expect(c)
        if not right(pred, q["answer"]):
            errors.append(f"{qid}: answer {q['answer']!r} is wrong ({q['prompt'][:90]!r})")
        if q["format"] == "multiple-choice":
            opts = q["options"]
            if len(opts) != 4 or len({o["text"] for o in opts}) != 4:
                errors.append(f"{qid}: needs four distinct options")
            if [o["text"] for o in opts if o["correct"]] != [q["answer"]]:
                errors.append(f"{qid}: exactly one correct option, equal to the answer")
            for o in opts:
                if not o["correct"] and right(pred, o["text"]):
                    errors.append(f"{qid}: distractor {o['text']!r} is also right")
    for e in errors[:60]:
        print(e)
    print(f"checked {n} items")
    print(f"TOTAL ERRORS {len(errors)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
