"""High-school (Precalculus / Calculus) authoring helpers built on glib.

T(e)      sympy expression -> student-facing text in the site's display syntax
          (√, π, e^( ), superscript integer powers, stacked fractions written so math-display.js
          parses them correctly: (3√2)/2, 5π/6, (3/2)x²).
H(code, ans_mode=...)   independent check spec evaluated by hschecks.py with SymPy. `code` restates the
          problem in SymPy, normally applying an operation to the DISPLAYED text via P('...').
"""
from glib import *  # noqa
import sympy as sp

x, y, t, n, k, h, r_, theta = sp.symbols("x y t n k h r theta", real=True)
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _atom(e):
    s = T(e)
    if isinstance(e, (sp.Integer, sp.Symbol)) or (e.is_Integer) or e in (sp.pi, sp.E) or (isinstance(e, sp.Integer) and e >= 0):
        return s
    if isinstance(e, sp.Function) or (isinstance(e, sp.Pow) and not e.exp.is_negative):
        return s
    return f"({s})"


def T(e):
    e = sp.sympify(e)
    if e is sp.oo:
        return "∞"
    if e is sp.zoo or e is sp.nan:
        raise Reject()
    if e == sp.pi:
        return "π"
    if e == sp.E:
        return "e"
    if e.is_Integer:
        return str(int(e))
    if e.is_Rational:
        return ("-" if e < 0 else "") + f"{abs(e.p)}/{e.q}"
    if e.is_Float:
        return D(F(str(e)).limit_denominator(10 ** 9))
    if e.is_Symbol:
        return {"theta": "θ"}.get(e.name, e.name)
    if isinstance(e, sp.Add):
        def deg(tm):
            if not tm.free_symbols:
                return -1
            try:
                return sp.Poly(tm, *sorted(tm.free_symbols, key=str)).total_degree() if tm.is_polynomial() else 0.5
            except Exception:
                return 0.5
        terms = sorted(e.as_ordered_terms(), key=lambda tm: -deg(tm))
        out = T(terms[0])
        for tm in terms[1:]:
            s = T(tm)
            out += (" - " + s[1:]) if s.startswith("-") else (" + " + s)
        return out
    if isinstance(e, sp.Pow):
        b, ex = e.base, e.exp
        if ex == sp.Rational(1, 2):
            return "√" + (T(b) if (b.is_Integer and b > 0) or b.is_Symbol else f"({T(b)})")
        if ex == sp.Rational(1, 3):
            return "∛" + (T(b) if b.is_Integer or b.is_Symbol else f"({T(b)})")
        if ex.is_negative:
            return T(sp.Mul(1, sp.Pow(b, ex, evaluate=False), evaluate=False)) if False else ("1/" + (lambda dt: f"({dt})" if ("√" in dt or "∛" in dt or " " in dt) and not dt.startswith("(") else dt)(T(sp.Pow(b, -ex)) if not (b.is_Add) or (-ex).is_Integer and False else _atom(sp.Pow(b, -ex)) if (-ex).is_Integer else T(sp.Pow(b, -ex))))
        if ex.is_Integer:
            return ("e" if b == sp.E else _atom(b)) + str(int(ex)).translate(SUP)
        if b == sp.E:
            return "e^" + (T(ex) if ex.is_Symbol else f"({T(ex)})")
        if ex.is_Rational and ex.q in (2, 3) and ex > 0:
            k_, rem = int(ex.p // ex.q), int(ex.p % ex.q)
            bt = T(b) if (b.is_Symbol or (b.is_Integer and b > 0)) else f"({T(b)})"
            root = ("√" + bt) if ex.q == 2 else ("∛" + (bt if rem == 1 else f"({bt}²)" if False else "(" + T(b ** rem) + ")"))
            if ex.q == 3 and rem == 1:
                root = "∛" + bt
            pre = "" if k_ == 0 else (bt if k_ == 1 else bt + str(k_).translate(SUP))
            return pre + root
        return _atom(b) + ("^" + T(ex) if ex.is_Symbol else "^(" + T(ex) + ")")
    if isinstance(e, sp.Mul):
        c, rest = e.as_coeff_Mul()
        if c < 0:
            return "-" + T(-e)
        facs = sp.Mul.make_args(rest)
        num = [f_ for f_ in facs if not (isinstance(f_, sp.Pow) and f_.exp.is_negative)]
        den = [1 / f_ for f_ in facs if isinstance(f_, sp.Pow) and f_.exp.is_negative]
        def body(fs):
            fs = sorted(fs, key=lambda f_: (0 if f_.is_number else 1, sp.default_sort_key(f_)))
            out = ""
            for f_ in fs:
                s = _atom(f_) if isinstance(f_, sp.Add) else T(f_)
                if out and (out[-1].isdigit() and s[0].isdigit()):
                    out += "·"
                out += s
            return out
        nb = body(num) if num else ""
        if den:
            numtxt = (T(c.p) if c.p != 1 or not nb else "") + nb if c.is_Rational else T(c) + nb
            d = sp.Mul(*den) * (c.q if c.is_Rational else 1)
            wrapped = numtxt.startswith("(") and numtxt.endswith(")") and numtxt.count("(") == 1
            dt = _atom(d)
            if ("√" in dt or "∛" in dt) and not (dt.startswith("(") and dt.endswith(")")):
                dt = f"({dt})"
            return (numtxt if wrapped else f"({numtxt or '1'})") + f"/{dt}" if (" " in numtxt or "√" in numtxt) else f"{numtxt or '1'}/{dt}"
        if c == 1:
            return nb
        if c.is_Rational and c.q != 1:
            if nb.startswith("√") or nb.startswith("∛"):
                return f"({c.p if c.p != 1 else ''}{nb})/{c.q}" if c.p != 1 else f"{nb}/{c.q}" if False else f"({'' if c.p == 1 else c.p}{nb})/{c.q}"
            if nb in ("π",) or nb.startswith("π"):
                return f"{'' if c.p == 1 else c.p}{nb}/{c.q}"
            return f"({c.p}/{c.q}){nb}"
        return T(c) + ("·" if nb[:1].isdigit() else "") + nb
    if isinstance(e, sp.Abs):
        return f"|{T(e.args[0])}|"
    if isinstance(e, sp.log):
        return f"ln({T(e.args[0])})"
    if isinstance(e, sp.exp):
        return T(sp.Pow(sp.E, e.args[0], evaluate=False))
    if isinstance(e, sp.Function):
        nm = {"asin": "sin⁻¹", "acos": "cos⁻¹", "atan": "tan⁻¹"}.get(e.func.__name__, e.func.__name__)
        return f"{nm}({', '.join(T(a) for a in e.args)})"
    raise ValueError(f"no text for {e!r}")


def H(code, mode="expr", **kw):
    d = {"kind": "py", "fn": "hs", "code": code, "mode": mode}
    d.update(kw)
    return d


def ivl(a, b, lc, rc):
    """Interval text: (-∞, 3]."""
    return f"{'[' if lc else '('}{T(a) if a != -sp.oo else '-∞'}, {T(b) if b != sp.oo else '∞'}{']' if rc else ')'}"


def set_text(s):
    s = sp.sympify(s)
    if isinstance(s, sp.Union):
        return " ∪ ".join(set_text(a) for a in s.args)
    if isinstance(s, sp.Interval):
        return ivl(s.start, s.end, not s.left_open, not s.right_open)
    if s == sp.S.Reals:
        return "(-∞, ∞)"
    if s is sp.S.EmptySet:
        return "no solution"
    raise ValueError(s)


def mat_text(m):
    m = sp.Matrix(m)
    return "[" + "; ".join(", ".join(T(v) for v in m.row(i)) for i in range(m.rows)) + "]"


def vec_text(v):
    return "⟨" + ", ".join(T(a) for a in v) + "⟩"


def polyx(coeffs, var=x):
    """coeffs high→low."""
    deg = len(coeffs) - 1
    return sp.expand(sum(sp.nsimplify(c) * var ** (deg - i) for i, c in enumerate(coeffs)))


def rint(r, a, b, nonzero=False):
    while True:
        v = r.randint(a, b)
        if v or not nonzero:
            return v


def deg_text(d):
    return f"{T(sp.nsimplify(d))}°"


def curve_draw(curves, xr=(-10, 10), yr=(-10, 10), pts=(), step=1, label_every=2, legend=None):
    """curves: list of (xs, ys, style) with style 'solid'/'dashed'. pts: list of (x, y, label)."""
    def draw(path):
        fig, ax = new_fig(5.8, 5.8 * (yr[1] - yr[0]) / (xr[1] - xr[0]) if (yr[1] - yr[0]) <= (xr[1] - xr[0]) else 5.8)
        grid_axes(ax, xr, yr, step, label_every=label_every)
        for xs, ys, st in curves:
            seg_x, seg_y = [], []
            for a, b in zip(xs, ys):
                if xr[0] - 0.5 <= a <= xr[1] + 0.5 and yr[0] - 0.5 <= b <= yr[1] + 0.5:
                    seg_x.append(a); seg_y.append(b)
                else:
                    if len(seg_x) > 1:
                        ax.plot(seg_x, seg_y, color="#1f4e9c" if st == "solid" else "#777777", lw=2.3 if st == "solid" else 1.4, ls="-" if st == "solid" else "--")
                    seg_x, seg_y = [], []
            if len(seg_x) > 1:
                ax.plot(seg_x, seg_y, color="#1f4e9c" if st == "solid" else "#777777", lw=2.3 if st == "solid" else 1.4, ls="-" if st == "solid" else "--")
        for pt in pts:
            px, py, lab = pt[:3]
            opn = len(pt) > 3 and pt[3]
            ax.plot([float(px)], [float(py)], "o", color="#1f4e9c" if opn else "black", mfc="white" if opn else "black", ms=7 if opn else 5.5, mew=2, zorder=6)
            if lab:
                ax.annotate(lab, (float(px), float(py)), textcoords="offset points", xytext=(6, 6), fontsize=11, fontweight="bold", bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
        ax.set_xlim(*xr); ax.set_ylim(*yr)
        save(fig, path)
    return draw


def conic_curves(kind, h, k, a, b=None, vertical=False, N=500):
    """Parametric samples. ellipse/hyperbola: a = semi-axis along the main axis, b = other. parabola: a = p (focal length)."""
    h, k, a = float(h), float(k), float(a)
    out = []
    if kind == "circle":
        out.append(([h + a * math.cos(2 * math.pi * i / N) for i in range(N + 1)], [k + a * math.sin(2 * math.pi * i / N) for i in range(N + 1)], "solid"))
    elif kind == "ellipse":
        b = float(b)
        ax_, by_ = (b, a) if vertical else (a, b)
        out.append(([h + ax_ * math.cos(2 * math.pi * i / N) for i in range(N + 1)], [k + by_ * math.sin(2 * math.pi * i / N) for i in range(N + 1)], "solid"))
    elif kind == "parabola":
        ts = [-30 + 60 * i / N for i in range(N + 1)]
        if vertical:
            out.append(([h + t_ for t_ in ts], [k + t_ * t_ / (4 * a) for t_ in ts], "solid"))
        else:
            out.append(([h + t_ * t_ / (4 * a) for t_ in ts], [k + t_ for t_ in ts], "solid"))
    elif kind == "hyperbola":
        b = float(b)
        ts = [-3 + 6 * i / N for i in range(N + 1)]
        for sgn in (1, -1):
            if vertical:
                out.append(([h + b * math.sinh(t_) for t_ in ts], [k + sgn * a * math.cosh(t_) for t_ in ts], "solid"))
            else:
                out.append(([h + sgn * a * math.cosh(t_) for t_ in ts], [k + b * math.sinh(t_) for t_ in ts], "solid"))
        m = (a / b) if vertical else (b / a)
        L = [-40 + 80 * i / 200 for i in range(201)]
        for sgn in (1, -1):
            out.append(([h + u for u in L], [k + sgn * m * u for u in L], "dashed"))
    return out


def pts_text(ps):
    return ", ".join(f"({T(sp.nsimplify(a))}, {T(sp.nsimplify(b))})" for a, b in ps)


def trig_draw(fn, xmin=0.0, xmax=2 * math.pi, ymin=-4, ymax=4, xstep_frac=2, pts=()):
    """Graph of fn(x) (float->float) with x ticks at multiples of π/xstep_frac, labeled with π."""
    def lab(i):
        f_ = sp.Rational(i, xstep_frac)
        if f_ == 0:
            return "0"
        return "$" + ("-" if f_ < 0 else "") + (r"\frac{" + (("" if abs(f_.p) == 1 else str(abs(f_.p))) + r"\pi}{" + str(f_.q) + "}") if f_.q != 1 else (("" if abs(f_.p) == 1 else str(abs(f_.p))) + r"\pi")) + "$"

    def draw(path):
        fig, ax = new_fig(7.2, 4.6)
        i0, i1 = math.ceil(xmin / (math.pi / xstep_frac) - 1e-9), math.floor(xmax / (math.pi / xstep_frac) + 1e-9)
        for i in range(i0, i1 + 1):
            ax.axvline(i * math.pi / xstep_frac, color="#d0d0d0", lw=0.8, zorder=0)
        for v in range(int(ymin), int(ymax) + 1):
            ax.axhline(v, color="#d0d0d0", lw=0.8, zorder=0)
        ax.axhline(0, color="black", lw=1.3)
        ax.axvline(0, color="black", lw=1.3) if xmin <= 0 <= xmax else None
        xs = [xmin + (xmax - xmin) * j / 800 for j in range(801)]
        ys = [fn(v) for v in xs]
        ax.plot(xs, ys, color="#1f4e9c", lw=2.4)
        for px, py in pts:
            ax.plot([px], [py], "o", color="black", ms=5.5, zorder=6)
        ax.set_xticks([i * math.pi / xstep_frac for i in range(i0, i1 + 1)])
        ax.set_xticklabels([lab(i) for i in range(i0, i1 + 1)], fontsize=12)
        ax.set_yticks(list(range(int(ymin), int(ymax) + 1)))
        ax.tick_params(labelsize=11)
        ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
        for s_ in ax.spines.values():
            s_.set_visible(False)
        save(fig, path)
    return draw


def tri_draw(labels, angle_mark=None):
    """Right triangle with right angle at bottom-left C, A at top-left, B at bottom-right.
    labels: dict with keys 'AC' (vertical leg), 'CB' (horizontal leg), 'AB' (hypotenuse), 'A', 'B' (angle labels)."""
    def draw(path):
        fig, ax = new_fig(5.6, 4.2)
        A, B, C = (0, 3), (4.4, 0), (0, 0)
        ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color="#1f4e9c", lw=2.4)
        ax.plot([0, 0.32, 0.32], [0.32, 0.32, 0], color="black", lw=1.2)
        fs = 13
        if labels.get("AC"):
            ax.text(-0.18, 1.5, labels["AC"], ha="right", va="center", fontsize=fs)
        if labels.get("CB"):
            ax.text(2.2, -0.2, labels["CB"], ha="center", va="top", fontsize=fs)
        if labels.get("AB"):
            ax.text(2.35, 1.72, labels["AB"], ha="left", va="bottom", fontsize=fs)
        if labels.get("B"):
            ax.text(3.45, 0.18, labels["B"], ha="center", va="bottom", fontsize=fs)
        if labels.get("A"):
            ax.text(0.22, 2.25, labels["A"], ha="left", va="center", fontsize=fs)
        ax.set_xlim(-1.4, 5.2); ax.set_ylim(-0.8, 3.5); ax.set_aspect("equal"); ax.axis("off")
        save(fig, path)
    return draw


def obl_draw(a, b, c, labels):
    """Triangle ABC with side lengths a (BC), b (CA), c (AB) — only the shape uses them.
    labels: keys 'A','B','C' (angle text), 'a','b','c' (side text)."""
    def draw(path):
        a_, b_, c_ = float(a), float(b), float(c)
        Ax, Ay = 0.0, 0.0
        Bx, By = c_, 0.0
        cosA = (b_ * b_ + c_ * c_ - a_ * a_) / (2 * b_ * c_)
        cosA = max(-1, min(1, cosA))
        Cx, Cy = b_ * cosA, b_ * math.sqrt(1 - cosA * cosA)
        s = 5.0 / max(c_, abs(Cx) + 1e-9, abs(Cx - Bx), Cy)
        P_ = {"A": (Ax * s, Ay * s), "B": (Bx * s, By * s), "C": (Cx * s, Cy * s)}
        fig, ax = new_fig(5.8, 4.4)
        xs = [P_["A"][0], P_["B"][0], P_["C"][0], P_["A"][0]]
        ys = [P_["A"][1], P_["B"][1], P_["C"][1], P_["A"][1]]
        ax.plot(xs, ys, color="#1f4e9c", lw=2.4)
        gx, gy = sum(xs[:3]) / 3, sum(ys[:3]) / 3
        for V in "ABC":
            vx, vy = P_[V]
            dx, dy = vx - gx, vy - gy
            n_ = math.hypot(dx, dy) or 1
            ax.text(vx + 0.38 * dx / n_, vy + 0.38 * dy / n_, V, ha="center", va="center", fontsize=14, fontweight="bold")
            if labels.get(V):
                U_, W_ = [P_[o] for o in "ABC" if o != V]
                u1 = ((U_[0] - vx) / math.hypot(U_[0] - vx, U_[1] - vy), (U_[1] - vy) / math.hypot(U_[0] - vx, U_[1] - vy))
                w1 = ((W_[0] - vx) / math.hypot(W_[0] - vx, W_[1] - vy), (W_[1] - vy) / math.hypot(W_[0] - vx, W_[1] - vy))
                bx, by = u1[0] + w1[0], u1[1] + w1[1]
                bn = math.hypot(bx, by) or 1
                half = math.acos(max(-1, min(1, u1[0] * w1[0] + u1[1] * w1[1]))) / 2
                d_ = min(2.6, 0.5 / max(math.sin(half), 0.17))
                ax.text(vx + d_ * bx / bn, vy + d_ * by / bn, labels[V], ha="center", va="center", fontsize=12, color="#8a1c1c")
        for side, (U, W) in {"a": ("B", "C"), "b": ("C", "A"), "c": ("A", "B")}.items():
            if labels.get(side):
                mx, my = (P_[U][0] + P_[W][0]) / 2, (P_[U][1] + P_[W][1]) / 2
                dx, dy = mx - gx, my - gy
                n_ = math.hypot(dx, dy) or 1
                ax.text(mx + 0.42 * dx / n_, my + 0.42 * dy / n_, labels[side], ha="center", va="center", fontsize=12.5)
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(min(xs) - 1, max(xs) + 1); ax.set_ylim(min(ys) - 0.8, max(ys) + 0.8)
        save(fig, path)
    return draw
