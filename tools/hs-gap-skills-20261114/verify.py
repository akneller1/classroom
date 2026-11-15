"""Independent numeric verifier for the 2026-11-14 HS gap skills.

For every new item it:
  1. confirms the check data (function, equation, numbers) is printed in the prompt,
  2. judges the keyed answer TRUE from that data alone (numerically, with NumPy/SciPy),
  3. judges every multiple-choice distractor, error-analysis "student answer" and wrong option FALSE,
  4. judges every open-response part TRUE.
It imports only hsfmt (display-text evaluator), never the families.

Usage: python3 verify.py <repo root>   → prints TOTAL ERRORS n
"""
import json, os, re, sys, warnings
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from hsfmt import val, close, dnum

warnings.filterwarnings("ignore")
ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))


def isnum(t):
    try:
        v = val(t)
        return np.isfinite(complex(v))
    except Exception:
        return False


def split_top(e, ch):
    depth = 0
    for i, c in enumerate(e):
        depth += c == "("
        depth -= c == ")"
        if c == ch and depth == 0:
            return e[:i], e[i + 1:]
    return None


PTS = [0.31, 0.47, 0.73, 1.13, 1.61, 2.27]


def judge(c, ans):
    k = c["k"]
    try:
        if k == "deriv":
            pts = {"small": [0.05, 0.08, 0.11, 0.14], "neg": [-0.4, -0.9, -1.3, -2.1]}.get(c.get("dom"), PTS)
            ok = 0
            for x0 in pts:
                d = dnum(lambda x: val(c["f"], x=x), x0)
                a = val(ans, x=x0)
                if not (np.isfinite(d) and np.isfinite(a)):
                    continue
                if not close(d, a, 1e-5):
                    return False
                ok += 1
            return ok >= 3
        if k == "derivval":
            return close(dnum(lambda x: val(c["f"], x=x), float(c["a"])), val(ans), 1e-6)
        if k == "table":
            v = c["fpga"] * c["gpa"] if c["kind"] == "fg" else c["n"] * c["ga"] ** (c["n"] - 1) * c["gpa"]
            return isnum(ans) and close(val(ans), v)
        if k in ("implicit", "implicitval"):
            L, R = [s.strip() for s in c["eq"].split("=")]
            Fn = lambda x, y: val(L, x=x, y=y) - val(R, x=x, y=y)
            def slope(x0, y0):
                fx = dnum(lambda x: Fn(x, y0), x0)
                fy = dnum(lambda y: Fn(x0, y), y0)
                return -fx / fy
            if k == "implicitval":
                x0, y0 = c["x"], c["y"]
                if abs(Fn(x0, y0)) > 1e-9:
                    return "OFF CURVE"
                return isnum(ans) and close(val(ans), slope(x0, y0), 1e-6)
            for x0, y0 in [(0.7, 1.3), (1.4, 0.6), (0.9, 2.1), (2.2, 1.7)]:
                if not close(val(ans, x=x0, y=y0), slope(x0, y0), 1e-5):
                    return False
            return True
        if k == "invpoint":
            f = lambda x: val(c["f"], x=x)
            xs = np.linspace(-10, 10, 2001)
            if not np.all(np.diff([f(x) for x in xs]) > 0):
                return "NOT ONE-TO-ONE"
            a = brentq(lambda x: f(x) - c["b"], -10, 10, xtol=1e-14)
            return isnum(ans) and close(val(ans), 1 / dnum(f, a), 1e-6)
        if k == "invtable":
            return isnum(ans) and close(val(ans), 1 / c["fpa"])
        if k == "limit":
            f = lambda x: val(c["e"], x=x)
            if ans == "∞" and c["at"] == "∞":
                return f(1e6) > 1e5 and f(1e7) > f(1e6)
            if not isnum(ans):
                return False
            if c["at"] == "∞":
                big = [f(x) for x in (1e5, 1e6, 1e7)] if "e^x" not in c["e"] else [f(x) for x in (200.0, 400.0, 600.0)]
                return close(big[-1], val(ans), 1e-4) or (abs(val(ans)) < 1e-9 and abs(big[-1]) < 1e-4)
            a = float(val(c["at"]))
            est = [(f(a + h) + f(a - h)) / 2 for h in (4e-3, 2e-3)]
            lim = est[1] + (est[1] - est[0]) / 3  # Richardson (error ~ h²)
            n, d = split_top(c["e"], "/")
            n0, d0 = val(n, x=a), val(d, x=a)
            if not (abs(n0) < 1e-9 and abs(d0) < 1e-9):
                return "NOT 0/0"
            return close(lim, val(ans), 1e-5)
        if k == "lhform":
            n, d = split_top(c["e"], "/")
            a = float(val(c["at"]))
            zero = abs(val(n, x=a)) < 1e-9 and abs(val(d, x=a)) < 1e-9
            return ans == ("Yes, substitution gives 0/0." if zero else "No, substitution does not give 0/0 or ∞/∞.")
        if k == "anti":
            F_ = ans.replace(" + C", "")
            if F_ == ans:
                return False
            for x0 in (0.12, 0.19, 0.26, 0.33):
                if not close(dnum(lambda x: val(F_, x=x), x0), val(c["g"], x=x0), 1e-5):
                    return False
            return True
        if k == "defint":
            v, _ = quad(lambda x: val(c["g"], x=x), float(val(c["lo"])), float(val(c["hi"])), epsabs=1e-12, epsrel=1e-12)
            return isnum(ans) and close(val(ans), v, 1e-8)
        if k == "trigval":
            v = float(val(c["v"]))
            fn = {"sin": np.arcsin, "cos": np.arccos, "tan": np.arctan}[c["given"]]
            b0 = fn(v)
            cands = {"sin": [b0, np.pi - b0], "cos": [b0, -b0], "tan": [b0, b0 + np.pi]}[c["given"]]
            lo = (c["quad"] - 1) * np.pi / 2
            th = [t % (2 * np.pi) for t in cands if lo < t % (2 * np.pi) < lo + np.pi / 2]
            if len(th) != 1:
                return "BAD SETUP"
            return isnum(ans) and close(val(ans), val(c["want"], t=th[0]), 1e-9)
        if k == "ident":
            for x0 in (0.13, 0.29, 0.41, 0.57, 1.03, 2.51):
                if not close(val(c["e"], x=x0), val(ans, x=x0), 1e-9):
                    return False
            return True
        if k == "trigeq":
            L_, R_ = c["eq"].split(" = ")
            g = lambda x: val(L_, x=x) - val(R_, x=x)
            if not ans.startswith("x = "):
                return False
            got = sorted(float(val(t)) for t in ans[4:].split(", "))
            from scipy.optimize import minimize_scalar
            xs = np.linspace(0, 2 * np.pi, 200001)
            gv = g(xs)
            cand = []
            for i in range(len(xs) - 1):
                a0, a1 = gv[i], gv[i + 1]
                if np.isfinite(a0) and np.isfinite(a1):
                    if a0 == 0:
                        cand.append(xs[i])
                    elif a0 * a1 < 0:
                        cand.append(brentq(g, xs[i], xs[i + 1], xtol=1e-15))
            ag = np.abs(gv)
            for i in range(1, len(xs) - 1):
                if ag[i] <= ag[i - 1] and ag[i] <= ag[i + 1] and ag[i] < 1e-2:
                    m_ = minimize_scalar(lambda x: abs(g(x)), bounds=(xs[i - 1], xs[i + 1]), method="bounded", options={"xatol": 1e-13})
                    cand.append(m_.x)
            true = []
            for x in cand:
                x = x % (2 * np.pi)
                if abs(g(x)) < 1e-7 and not any(min(abs(x - y), 2 * np.pi - abs(x - y)) < 1e-5 for y in true):
                    true.append(x)
            if len(true) != len(got):
                return False
            return all(any(min(abs(x - y), 2 * np.pi - abs(x - y)) < 1e-5 for y in true) and abs(g(x)) < 1e-9 and 0 <= x < 2 * np.pi for x in got)
        if k in ("polar", "petals", "rmax"):
            eq = c["eq"].replace("θ", "t")
            L_, R_ = eq.split(" = ")
            pts = []
            for t0 in np.linspace(0.05, 2 * np.pi - 0.05, 97):
                if L_ == "r":
                    rv = val(R_, t=t0)
                else:
                    h = lambda rr: val(L_, r=rr, t=t0) - val(R_, t=t0)
                    rr_ = [x for x in np.linspace(0.01, 60, 6000)]
                    hv = [h(x) for x in rr_]
                    rv = None
                    for i in range(len(rr_) - 1):
                        if np.isfinite(hv[i]) and np.isfinite(hv[i + 1]) and hv[i] * hv[i + 1] < 0:
                            rv = brentq(h, rr_[i], rr_[i + 1], xtol=1e-14)
                            break
                    if rv is None:
                        continue
                if np.isfinite(rv):
                    pts.append((t0, rv))
            if k == "rmax":
                tt = np.linspace(0, 2 * np.pi, 200001)
                return isnum(ans) and close(np.max(np.abs(val(R_, t=tt))), val(ans), 1e-6)
            if k == "petals":
                tt = np.linspace(0, 2 * np.pi, 400001)[:-1]
                rr = val(R_, t=tt)
                m = np.max(np.abs(rr))
                tips = []
                ar = np.abs(rr)
                n_ = len(tt)
                for i in range(n_):
                    if ar[i] >= ar[i - 1] and ar[i] >= ar[(i + 1) % n_] and ar[i] > 0.999 * m:
                        pt = (rr[i] * np.cos(tt[i]), rr[i] * np.sin(tt[i]))
                        if not any(abs(pt[0] - q[0]) < 1e-2 and abs(pt[1] - q[1]) < 1e-2 for q in tips):
                            tips.append(pt)
                return isnum(ans) and close(val(ans), len(tips))
            A, B = ans.split(" = ")
            if len(pts) < 20:
                return "TOO FEW POINTS"
            return all(close(val(A, x=r0 * np.cos(t0), y=r0 * np.sin(t0)), val(B, x=r0 * np.cos(t0), y=r0 * np.sin(t0)), 1e-7) for t0, r0 in pts)
        if k == "param":
            if " = " not in ans:
                return False
            A, B = ans.split(" = ")
            for t0 in (-1.7, -0.6, 0.3, 0.8, 1.9, 2.6):
                x0, y0 = val(c["x"], t=t0), val(c["y"], t=t0)
                if not close(val(A, x=x0, y=y0), val(B, x=x0, y=y0), 1e-9):
                    return False
            return True
        if k == "parpt":
            m = re.fullmatch(r"\((.+), (.+)\)", ans)
            if not m:
                return False
            return close(val(m.group(1)), val(c["x"], t=c["t"]), 1e-9) and close(val(m.group(2)), val(c["y"], t=c["t"]), 1e-9)
        if k in ("seqterm", "seqsum", "seqinf"):
            from fractions import Fraction as Fr
            ts = [Fr(t) for t in c["terms"]]
            d = {ts[i + 1] - ts[i] for i in range(3)}
            q = {ts[i + 1] / ts[i] for i in range(3)} if all(ts) else set()
            if k == "seqinf":
                if len(q) != 1:
                    return "NOT GEOMETRIC"
                q = q.pop()
                if abs(q) >= 1:
                    return ans == "The series diverges."
                return isnum(ans) and close(val(ans), float(ts[0] / (1 - q)), 1e-12)
            n = c["n"]
            if len(d) == 1:
                d = d.pop()
                seq = [ts[0] + i * d for i in range(n)]
            elif len(q) == 1:
                q = q.pop()
                seq = [ts[0] * q ** i for i in range(n)]
            else:
                return "NO PATTERN"
            v = seq[-1] if k == "seqterm" else sum(seq)
            return isnum(ans) and close(val(ans), float(v), 1e-12)
        if k == "sigma":
            tot = sum(val(c["e"], k=kk) for kk in range(c["lo"], c["hi"] + 1))
            return isnum(ans) and close(val(ans), tot, 1e-12)
        if k == "limitdne":
            f = lambda x: val(c["e"], x=x)
            a = float(val(c["at"]))
            right, left = f(a + 1e-7), f(a - 1e-7)
            dne = not close(right, left, 1e-4)
            return ans == "The limit does not exist." if dne else (isnum(ans) and close(val(ans), right, 1e-5))
    except Exception as e:
        return f"ERROR {e}"
    # ---- Pre-Algebra: comparing two populations (data printed in the prompt; plain statistics)
    if k in ("meandiff", "mad", "mediandiff", "ratio", "ratio_data"):
        try:
            a = float(ans)
        except ValueError:
            return False
        A = np.array(c.get("A", []), float)
        B = np.array(c.get("B", []), float)
        if k == "meandiff":
            want = abs(A.mean() - B.mean())
        elif k == "mad":
            want = np.abs(A - A.mean()).mean()
        elif k == "mediandiff":
            want = abs(np.median(A) - np.median(B))
        elif k == "ratio":
            want = (c["hi"] - c["lo"]) / c["mad"]
        else:
            ma, mb = np.abs(A - A.mean()).mean(), np.abs(B - B.mean()).mean()
            if abs(ma - mb) > 1e-9:
                return False
            want = abs(A.mean() - B.mean()) / ma
        return bool(abs(a - want) < 0.05 + 1e-9)
    if k == "claim":
        ratio = (c["hi"] - c["lo"]) / c["mad"]
        return ans == (c["big"] if ratio >= 2 else c["small"])
    return f"UNKNOWN CHECK {k}"


def numtxt(v):
    return str(int(v)) if float(v) == int(v) else str(v)


def printed(c, prompt):
    if c.get("k") in ("meandiff", "mad", "mediandiff", "ratio", "ratio_data", "claim"):
        need_ = [", ".join(str(x) for x in c[kk]) for kk in ("A", "B") if kk in c]
        need_ += [numtxt(c[kk]) for kk in ("hi", "lo", "mad") if kk in c]
        return all(v in prompt for v in need_)
    keys = [v for kk, v in c.items() if kk in ("f", "eq", "e", "g")]
    keys += [str(c[kk]) for kk in ("b", "a", "fpa", "fpga", "gpa", "ga", "x", "y", "v", "t", "lo", "hi", "n") if kk in c]
    keys += [t.lstrip("-") for t in c.get("terms", [])]
    return all(str(v) in prompt for v in keys)


def main():
    checks = json.load(open(os.path.join(HERE, "out", "checks.json"), encoding="utf-8"))
    errors, n = [], 0
    banks = {}
    for qid, c in checks.items():
        course, unit = c["bank"]
        if (course, unit) not in banks:
            d = json.load(open(os.path.join(ROOT, "question-banks", course, unit + ".json"), encoding="utf-8"))
            banks[(course, unit)] = {q["id"]: q for q in d["questions"]}
        q = banks[(course, unit)].get(qid)
        if not q:
            errors.append(f"{qid}: missing from bank")
            continue
        n += 1
        if q["format"] == "open-response":
            for part, pc in zip(q["parts"], c["parts"]):
                if not printed(pc, part["prompt"]):
                    errors.append(f"{qid}: part data not printed")
                if judge(pc, part["answer"]) is not True:
                    errors.append(f"{qid}: part answer fails: {part['answer']}")
            continue
        if not printed(c, q["prompt"]):
            errors.append(f"{qid}: check data not printed in prompt")
        res = judge(c, q["answer"])
        if res is not True:
            errors.append(f"{qid}: keyed answer fails ({res}): {q['answer']}")
        for o in q.get("options", []):
            r_ = judge(c, o["text"])
            if (r_ is True) != o["correct"]:
                errors.append(f"{qid}: option judged {r_} but flagged {o['correct']}: {o['text']}")
        m = re.search(r"(?:answer|answered): (.+)\n", q["prompt"])
        if c.get("student"):
            if judge(c, c["student"]) is True:
                errors.append(f"{qid}: student answer is actually correct")
            if c["student"] not in q["prompt"]:
                errors.append(f"{qid}: student answer not printed")
    # duplicates within each bank
    for (course, unit), qs in banks.items():
        seen = {}
        for q in qs.values():
            if q["format"] == "open-response":
                continue
            key = (q["skillId"], q["prompt"])
            if key in seen and (q["id"] in checks or seen[key] in checks):
                errors.append(f"{q['id']}: duplicate prompt of {seen[key]}")
            seen[key] = q["id"]
    for e in errors:
        print(e)
    print(f"checked {n} new items; TOTAL ERRORS {len(errors)}")
    return len(errors)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
