"""Offline authoring helpers for the Grade 8 Pre-Algebra question banks.

This is an authoring tool, not a site engine. It materialises static JSON that
matches schemas/question-bank.schema.json. Student-facing math is plain text in
the site's display mini-syntax: a/b (rendered as a stacked fraction by
worksheet-generator/core/math-display.js), unicode superscripts, √, ∛, π, ·, ×, ÷.
"""
import math, os, random, re, hashlib
from fractions import Fraction as F

ROOT = os.environ.get("PA8_OUT", "/home/claude/work/pkg")
COURSE = "prealgebra"
SUPMAP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
TAGS = {"modeling", "misconception", "challenge", "graph", "reasoning", "error-analysis",
        "connections", "multiple-representations", "multistep"}
LEVELS = ["cp2", "cp1", "honors"]          # Remedial, Standard, Advanced (Grade 8 labels)
LABEL = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}


class Reject(Exception):
    """Raised by a family when a random case is invalid/ambiguous; the builder retries."""


def need(cond):
    if not cond:
        raise Reject()


# ---------------------------------------------------------------- formatting
def sup(n):
    return str(n).translate(SUPMAP)


def N(x):
    """Exact number text: 5, -5, 3/4, -3/4."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ("-" if x < 0 else "") + f"{abs(x.numerator)}/{x.denominator}"


def is_term(x):
    x = F(x)
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def D(x, places=None):
    """Decimal text of an exact value (terminating) or rounded to `places`."""
    if places is not None:
        q = F(x)
        s = f"{round_half_up(q, places):.{places}f}"
        return s
    x = F(x)
    need(is_term(x))
    s = f"{float(x):.12f}".rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s


def round_half_up(q, places):
    q = F(q)
    m = F(10) ** places
    v = q * m
    r = math.floor(abs(v) + F(1, 2))
    return (r if v >= 0 else -r) / float(m) if places else float(r if v >= 0 else -r)


def Rd(x, places):
    """Round a float/Fraction half-up to text with exactly `places` decimals."""
    q = F(x) if not isinstance(x, float) else F(repr(x))
    m = 10 ** places
    v = q * m
    r = math.floor(abs(v) + F(1, 2))
    r = r if v >= 0 else -r
    if places == 0:
        return str(r)
    s = f"{abs(r):0{places + 1}d}"
    return ("-" if r < 0 else "") + s[:-places] + "." + s[-places:]


def money(x):
    return "$" + Rd(x, 2)


def pw(v, e):
    """Power text with exponent 1 omitted."""
    return v if e == 1 else f"{v}{sup(e)}"


def coef_text(c, var):
    """Coefficient times variable: x, -x, 3x, (2/3)x."""
    c = F(c)
    if c == 1:
        return var
    if c == -1:
        return "-" + var
    if c.denominator == 1:
        return f"{c.numerator}{var}"
    return ("-" if c < 0 else "") + f"({abs(c.numerator)}/{c.denominator}){var}"


def lin(*terms):
    """Linear combination text. terms: (coef, var) pairs; var '' for constant.
    Zero terms dropped; signs joined as ' + ' / ' - '."""
    out = []
    for c, v in terms:
        c = F(c)
        if c == 0:
            continue
        t = coef_text(abs(c), v) if v else N(abs(c))
        if not out:
            out.append(("-" if c < 0 else "") + t)
        else:
            out.append((" - " if c < 0 else " + ") + t)
    return "".join(out) if out else "0"


def mx_b(m, b, x="x"):
    return lin((m, x), (b, ""))


def pt(a, b):
    return f"({N(a)}, {N(b)})"


def ptd(a, b):
    return f"({D(a)}, {D(b)})"


def paren(x):
    """Number in parentheses when negative, for substitution steps."""
    s = N(x)
    return f"({s})" if F(x) < 0 or "/" in s else s


def sci(mant, exp):
    return f"{mant} × 10{sup(exp)}"


def ordinal(n):
    return {1: "first", 2: "second", 3: "third", 4: "fourth"}[n]


def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


# ---------------------------------------------------------------- problem record
class P(dict):
    """One authored problem before format assembly.

    prompt, answer (string), steps (list), wrong (plausible misconception answers),
    chk (independent-verification spec), tags, diagram (dict with draw/alt), mode:
    'any' (SA or MC), 'sa' (no meaningful distractors), 'mc' (only makes sense with choices).
    For select-all: options=[(text, bool)], answer list. For open-response: parts=[(prompt, answer, chk)].
    """

    def __init__(self, prompt, answer=None, steps=None, wrong=(), chk=None, tags=(), diagram=None,
                 mode="any", options=None, parts=None, mc_prompt=None, eq_key=None):
        super().__init__(prompt=prompt, answer=answer, steps=list(steps or []), wrong=list(wrong),
                         chk=chk, tags=list(tags), diagram=diagram, mode=mode, options=options,
                         parts=parts, mc_prompt=mc_prompt, eq_key=eq_key)


def norm_key(s):
    """Normalization for distractor distinctness (numeric when possible)."""
    t0 = str(s).strip()
    if re.fullmatch(r"[-−\d\s./()√∛π·×÷⁰¹²³⁴⁵⁶⁷⁸⁹⁻+]+", t0) and t0:
        try:
            return ("n", round(fval(t0), 9))
        except Exception:
            pass
    t = t0.replace("−", "-").replace(" ", "")
    try:
        return ("n", F(t))
    except (ValueError, ZeroDivisionError):
        pass
    if re.fullmatch(r"-?\d+/[1-9]\d*", t):
        a, b = t.split("/")
        return ("n", F(int(a), int(b)))
    return ("s", t.lower())


# ---------------------------------------------------------------- diagrams
_plt = None


def plt():
    global _plt
    if _plt is None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as p
        p.rcParams.update({"font.size": 12, "font.family": "DejaVu Sans"})
        _plt = p
    return _plt


def new_fig(w=6.3, h=6.3):
    p = plt()
    fig, ax = p.subplots(figsize=(w, h), dpi=100)
    return fig, ax


def save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=100, bbox_inches="tight", facecolor="white")
    plt().close(fig)


def grid_axes(ax, xr, yr, step=1, xlabel="x", ylabel="y", label_every=1):
    """Coordinate plane with labelled integer grid."""
    x0, x1 = xr
    y0, y1 = yr
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal" if (x1 - x0) / max(1, (y1 - y0)) < 2.2 and (y1 - y0) / max(1, (x1 - x0)) < 2.2 and step == 1 else "auto")
    xs = [x for x in range(int(x0), int(x1) + 1) if x % step == 0]
    ys = [y for y in range(int(y0), int(y1) + 1) if y % step == 0]
    for x in xs:
        ax.axvline(x, color="#bbbbbb", lw=0.8, zorder=0)
    for y in ys:
        ax.axhline(y, color="#bbbbbb", lw=0.8, zorder=0)
    ax.axhline(0, color="black", lw=1.4, zorder=1)
    ax.axvline(0, color="black", lw=1.4, zorder=1)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    yl = 0 if y0 <= 0 <= y1 else y0
    xl = 0 if x0 <= 0 <= x1 else x0
    for i, x in enumerate(xs):
        if x != 0 and (x // step) % label_every == 0:
            ax.text(x, yl - (y1 - y0) * 0.035, str(x), ha="center", va="top", fontsize=10)
    for y in ys:
        if y != 0 and (y // step) % label_every == 0:
            ax.text(xl - (x1 - x0) * 0.02, y, str(y), ha="right", va="center", fontsize=10)
    if x0 <= 0 <= x1 and y0 <= 0 <= y1:
        ax.text(-(x1 - x0) * 0.02, -(y1 - y0) * 0.035, "0", ha="right", va="top", fontsize=10)
    ax.annotate("", xy=(x1, yl), xytext=(x1 - 0.01, yl), arrowprops=dict(arrowstyle="-|>", color="black"))
    ax.annotate("", xy=(xl, y1), xytext=(xl, y1 - 0.01), arrowprops=dict(arrowstyle="-|>", color="black"))
    ax.text(x1, yl + (y1 - y0) * 0.02, " " + xlabel, ha="left", va="bottom", fontsize=12, style="italic")
    ax.text(xl + (x1 - x0) * 0.015, y1, ylabel, ha="left", va="bottom", fontsize=12, style="italic")


def data_axes(ax, xr, yr, xstep, ystep, xlabel, ylabel):
    """First-quadrant axes for data displays with labelled scales."""
    ax.set_xlim(*xr)
    ax.set_ylim(*yr)
    ax.set_xticks(list(frange(xr[0], xr[1], xstep)))
    ax.set_yticks(list(frange(yr[0], yr[1], ystep)))
    ax.grid(True, color="#cccccc", lw=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)


def frange(a, b, s):
    v = a
    while v <= b + 1e-9:
        yield round(v, 6)
        v += s


def seed_rng(*parts):
    h = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def pick(r, seq, k=None):
    seq = list(seq)
    if not seq or (k is not None and len(seq) < k):
        raise Reject()
    return r.choice(seq) if k is None else r.sample(seq, k)


def nz(r, a, b):
    """Random nonzero integer in [a, b]."""
    while True:
        v = r.randint(a, b)
        if v:
            return v


NAMES = ["Ava", "Ben", "Carmen", "Dev", "Elena", "Femi", "Grace", "Hiro", "Isla", "Jamal", "Kai", "Lena",
         "Marco", "Nia", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tariq", "Uma", "Vic", "Wren", "Yusuf", "Zoe"]


def fam(levels="012", mode=None):
    """Mark a problem family: levels it serves (0 Remedial, 1 Standard, 2 Advanced) and format mode."""
    def wrap(f):
        f.levels = {int(c) for c in levels}
        f.mode = mode
        return f
    return wrap


def rep_text(x, min_digits=4):
    """Decimal text for a rational: terminating '0.375' or repeating '0.5833… (3 repeats)'."""
    x = F(x)
    sign = "-" if x < 0 else ""
    x = abs(x)
    ip, rem = divmod(x.numerator, x.denominator)
    digits, seen = [], {}
    while rem and rem not in seen:
        seen[rem] = len(digits)
        rem *= 10
        digits.append(str(rem // x.denominator))
        rem %= x.denominator
    if not rem:
        return sign + str(ip) + ("." + "".join(digits) if digits else "")
    s = seen[rem]
    nonrep, block = "".join(digits[:s]), "".join(digits[s:])
    shown = nonrep + block
    while len(shown) < len(nonrep) + max(min_digits, 2 * len(block)):
        shown += block
    return f"{sign}{ip}.{shown}… ({block} repeats)"


def chk_val(expr, **kw):
    d = {"kind": "val", "expr": expr}
    d.update(kw)
    return d


def chk_py(fn, **kw):
    d = {"kind": "py", "fn": fn}
    d.update(kw)
    return d


def fval(text):
    """Authoring-side float value of a displayed number (python eval translation; the verifier uses its own parser)."""
    t = str(text)
    m = re.match(r"^(-?\d+\.\d+)… \((\d+) repeats\)$", t)
    if m:
        return float(m.group(1) + m.group(2) * 6)
    t = t.replace("−", "-").replace("·", "*").replace("×", "*").replace("÷", "/").replace("π", "(math.pi)")
    t = re.sub("([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)", lambda mm: "**(" + mm.group(1).translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")) + ")", t)
    t = re.sub(r"√\(([^()]*)\)", r"math.sqrt(\1)", t)
    t = re.sub(r"√(\d+(?:\.\d+)?)", r"math.sqrt(\1)", t)
    t = re.sub(r"∛\((-?[^()]*)\)", r"math.copysign(abs(\1)**(1/3), \1)", t)
    t = re.sub(r"∛(\d+)", r"(\1**(1/3))", t)
    t = re.sub(r"(\d)\s*\(", r"\1*(", t)
    t = re.sub(r"(\d)(math)", r"\1*\2", t)
    t = re.sub(r"\)(\d|m)", r")*\1", t)
    return float(eval(t, {"math": math}))


COLORS = ["#1f4e9c", "#b23a3a", "#2e7d32", "#7b3fa0"]


def plane_draw(xr=(-8, 8), yr=(-8, 8), lines=(), polys=(), points=(), step=1, label_every=1, xlabel="x", ylabel="y",
               size=6.3, data=False, xstep=None, ystep=None, panel=None, title=None, open_pts=()):
    """Return draw(path) for a coordinate-plane figure.
    lines: (m, b, color, label) drawn across the window (m None => vertical line x=b)
    polys: (pts, color, label, closed) polyline/polygon through exact vertices
    points: (x, y, text, color) labelled dots."""
    def draw_on(ax):
        if data:
            data_axes(ax, xr, yr, xstep, ystep, xlabel, ylabel)
        else:
            grid_axes(ax, xr, yr, step, xlabel, ylabel, label_every)
        for i, ln in enumerate(lines):
            m, b, col = ln[0], ln[1], ln[2] if len(ln) > 2 and ln[2] else COLORS[i % 4]
            lab = ln[3] if len(ln) > 3 else None
            if m is None:
                ax.plot([b, b], list(yr), color=col, lw=2.4, ls="-" if i == 0 else "--")
                continue
            xs = [xr[0], xr[1]]
            ax.plot(xs, [float(m) * x + float(b) for x in xs], color=col, lw=2.4, ls="-" if i % 2 == 0 else "--", label=lab)
        for i, pl in enumerate(polys):
            pts, col = pl[0], (pl[1] or COLORS[i % 4])
            lab = pl[2] if len(pl) > 2 else None
            closed = pl[3] if len(pl) > 3 else False
            xs = [float(p[0]) for p in pts] + ([float(pts[0][0])] if closed else [])
            ys = [float(p[1]) for p in pts] + ([float(pts[0][1])] if closed else [])
            ax.plot(xs, ys, color=col, lw=2.4, label=lab, marker="o" if not closed else None, ms=5)
            if closed:
                ax.fill(xs, ys, color=col, alpha=0.12)
        for p in points:
            x, y, t = p[0], p[1], p[2]
            col = p[3] if len(p) > 3 else "black"
            ax.plot([float(x)], [float(y)], "o", color=col, ms=7, zorder=5)
            if t:
                ax.annotate(t, (float(x), float(y)), textcoords="offset points", xytext=(7, 7), fontsize=12, fontweight="bold", color=col)
        for p in open_pts:
            ax.plot([float(p[0])], [float(p[1])], "o", mfc="white", mec=p[2] if len(p) > 2 else "black", ms=8, zorder=6)
        if any(len(l) > 3 and l[3] for l in lines) or any(len(p) > 2 and p[2] for p in polys):
            ax.legend(loc="upper left", fontsize=11, framealpha=0.95)
        if title:
            ax.set_title(title, fontsize=13)

    def draw(path):
        fig, ax = new_fig(size, size if not data else size * 0.8)
        draw_on(ax)
        save(fig, path)
    draw.draw_on = draw_on
    return draw


def panels_draw(drawers, labels=("A", "B", "C", "D")):
    """2x2 panel of plane drawers (each made by plane_draw), labelled A-D."""
    def draw(path):
        p = plt()
        fig, axs = p.subplots(2, 2, figsize=(8.4, 8.4), dpi=100)
        for ax, d, lab in zip(axs.flat, drawers, labels):
            d.draw_on(ax)
            ax.set_title(f"Graph {lab}", fontsize=14, fontweight="bold")
        fig.tight_layout()
        save(fig, path)
    return draw


def table_text(xs, ys, xn="x", yn="y"):
    """Horizontal input-output table as text: 'x | 1 | 2 | 3 ; y | 4 | 6 | 8' rendered inline."""
    return f"{xn}: " + ", ".join(N(x) if not isinstance(x, str) else x for x in xs) + f"; {yn}: " + ", ".join(N(y) if not isinstance(y, str) else y for y in ys)


def table_draw(xs, ys, xn="x", yn="y"):
    def draw(path):
        p = plt()
        fig, ax = p.subplots(figsize=(1.2 + 1.0 * len(xs), 1.3), dpi=100)
        ax.axis("off")
        cells = [[xn] + [N(x) if not isinstance(x, str) else x for x in xs], [yn] + [N(y) if not isinstance(y, str) else y for y in ys]]
        t = ax.table(cellText=cells, loc="center", cellLoc="center")
        t.scale(1, 2)
        t.set_fontsize(13)
        for (i, j), c in t.get_celld().items():
            if j == 0:
                c.set_facecolor("#e8eef8")
                c.get_text().set_fontweight("bold")
        save(fig, path)
    return draw
