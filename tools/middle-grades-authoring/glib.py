"""Shared authoring helpers for the Grade 7 (prealgebra7) and Grade 6 (math6) banks.

Reuses the Grade 8 toolkit (tools/prealgebra-authoring/lib.py) unchanged and adds:
  Q()        problem record with misconception explanations (`why`) for error analysis
  derived extras: err_of(f) / open_of(f) turn any core family into an error-analysis
             item or a 4-part open-response item (each part independently checked)
  a few diagram helpers (number lines, figures, data displays)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "prealgebra-authoring"))
from lib import *          # noqa: F401,F403  (Grade 8 helpers: P, N, D, Rd, lin, fam, pick, need, plane_draw, ...)
from lib import P, Reject, fam, pick, need, seed_rng, plt, new_fig, save, N, NAMES
from fractions import Fraction as F
import math


def Q(prompt, ans, steps, wrong=(), chk=None, why=(), tags=(), diagram=None, mode="any", options=None, parts=None, mc_prompt=None):
    """Problem record. wrong[i] is a misconception answer; why[i] (optional) says what the student did."""
    p = P(prompt, ans, steps, [str(w) for w in wrong], chk, tags, diagram, mode, options, parts, mc_prompt)
    p["why"] = list(why)
    return p


def V(expr, **kw):
    d = {"kind": "val", "expr": expr}
    d.update(kw)
    return d


def EQ(eq, var="x"):
    return {"kind": "eq", "eq": eq, "var": var}


def PY(fn, **kw):
    assert "kind" not in kw and "fn" not in kw, "reserved check key"
    d = {"kind": "py", "fn": fn}
    d.update(kw)
    return d


def TXT(*accept):
    return {"kind": "text", "accept": list(accept)}


def EQV(expr, vars=("x",)):
    return {"kind": "equiv", "expr": expr, "vars": list(vars)}


def AP(expr, places):
    return {"kind": "approx", "expr": expr, "places": places}


def mixed(x):
    """Mixed-number text for an improper fraction: 2 1/3 (proper fractions/integers via N)."""
    x = F(x)
    if x.denominator == 1 or abs(x) < 1:
        return N(x)
    s = "-" if x < 0 else ""
    a = abs(x)
    w, rem = divmod(a.numerator, a.denominator)
    return f"{s}{w} {rem}/{a.denominator}"


def sgn(x):
    """Signed term text for chains: '+ 5' / '- 5'."""
    return f"+ {N(x)}" if F(x) >= 0 else f"- {N(-F(x))}"


def par(x):
    s = N(x)
    return f"({s})" if F(x) < 0 else s


def money(x):
    return "$" + Rd(x, 2)


def dec(x, places=None):
    return D(x, places) if places is not None else D(x)


def name(r):
    return r.choice(NAMES)


def sub_rng(r, k):
    return seed_rng("sub", r.random(), k)


# ------------------------------------------------------------------ derived extras
def err_of(core, who=None):
    """Error-analysis item derived from a core family: show a student's misconception answer
    (with the documented reason) and ask for the correct answer. Same independent check."""
    def f(r, L):
        p = core(r, L)
        cands = [(w, y) for w, y in zip(p["wrong"], p.get("why", [])) if y]
        need(cands and p["answer"] is not None and not p.get("options") and not p.get("parts"))
        w, y = r.choice(cands)
        nm = who or name(r)
        q = Q(f"{nm} answered this problem incorrectly.\n{p['prompt']}\n{nm}'s answer: {w}\nIdentify the mistake and give the correct answer.",
              p["answer"], [f"Mistake: {y}."] + p["steps"] + [f"The correct answer is {p['answer']}, not {w}."],
              [x for x in p["wrong"] if x != w], p["chk"], tags=sorted(set(p["tags"]) | {"error-analysis", "misconception"}),
              diagram=p["diagram"], mode="sa")
        return q
    f.__name__ = core.__name__ + "_error"
    f.levels, f.mode = core.levels, "sa"
    return f


def open_of(core, lead="Answer each part. Show your work.", n=4):
    """Four independently generated, independently checked instances of a core family as one open-response item."""
    def f(r, L):
        parts, seen, steps = [], set(), []
        for k in range(n * 6):
            if len(parts) == n:
                break
            try:
                p = core(sub_rng(r, k), L)
            except Reject:
                continue
            if p["answer"] is None or p.get("options") or p.get("parts") or p.get("diagram") or p["prompt"] in seen:
                continue
            seen.add(p["prompt"])
            parts.append((p["prompt"], p["answer"], p["chk"]))
            steps.append(f"({chr(96 + len(parts))}) " + " ".join(p["steps"][-2:]))
        need(len(parts) == n)
        return Q(lead, None, steps, parts=parts, tags=["multistep"])
    f.__name__ = core.__name__ + "_open"
    f.levels, f.mode = core.levels, None
    return f


def select_of(core, k_true=3, k_false=3):
    """Select-all: 'Which of these are true?' statements 'problem → answer' with correct and misconception answers.
    Checked by the custom `claims` check, which re-runs each embedded check independently."""
    def f(r, L):
        good, bad, chks = [], [], {}
        for k in range(30):
            if len(good) >= k_true and len(bad) >= k_false:
                break
            try:
                p = core(sub_rng(r, k), L)
            except Reject:
                continue
            if p["answer"] is None or p.get("options") or p.get("parts") or p.get("diagram") or "\n" in p["prompt"] or len(p["prompt"]) > 90:
                continue
            short = p.get("claim") or p["prompt"]
            if len(good) < k_true and (len(bad) >= k_false or r.random() < 0.5):
                t = f"{short} → {p['answer']}"
                ok = True
            elif [w for w in p["wrong"] if norm_key(w) != norm_key(p["answer"])]:
                t = f"{short} → {r.choice([w for w in p['wrong'] if norm_key(w) != norm_key(p['answer'])])}"
                ok = False
            else:
                continue
            if t in chks:
                continue
            chks[t] = {"chk": p["chk"], "ans": t.rsplit(" → ", 1)[1]}
            (good if ok else bad).append(t)
        need(len(good) == k_true and len(bad) == k_false)
        opts = [(t, True) for t in good] + [(t, False) for t in bad]
        return Q("Select ALL problems that are matched with the correct answer.", None, ["Work each problem and compare with the answer shown."] +
                 [f"{t}: {'correct' if ok else 'incorrect'}." for t, ok in opts],
                 options=opts, chk=PY("claims", table={t: v["chk"] for t, v in chks.items()}), tags=["reasoning"])
    f.__name__ = core.__name__ + "_sel"
    f.levels, f.mode = core.levels, None
    return f


# ------------------------------------------------------------------ diagrams
def numline_draw(lo, hi, points=(), ray=None, seg=None, step=1, label_every=1, labels=None, size=(7.5, 1.6)):
    """Number line. points: (x, text, filled). ray: (x, dir '+'/'-', closed). seg: (a, b, closed_a, closed_b)."""
    def draw_on(ax):
        ax.set_xlim(lo - step * 0.8, hi + step * 0.8)
        ax.set_ylim(-1, 1.2)
        ax.axis("off")
        ax.annotate("", xy=(hi + step * 0.7, 0), xytext=(lo - step * 0.7, 0), arrowprops=dict(arrowstyle="<|-|>", color="black", lw=1.4))
        v, i = F(lo), 0
        while v <= hi:
            ax.plot([float(v), float(v)], [-0.15, 0.15], color="black", lw=1.2)
            if i % label_every == 0:
                ax.text(float(v), -0.45, labels(v) if labels else N(v), ha="center", va="top", fontsize=11)
            v += F(step)
            i += 1
        col = "#1f4e9c"
        if ray:
            x, d, closed = ray
            end = hi + step * 0.7 if d == "+" else lo - step * 0.7
            ax.annotate("", xy=(float(end), 0.35), xytext=(float(x), 0.35), arrowprops=dict(arrowstyle="-|>", color=col, lw=3))
            ax.plot([float(x)], [0.35], "o", ms=11, mfc=col if closed else "white", mec=col, mew=2.5, zorder=5)
        if seg:
            a, b, ca, cb = seg
            ax.plot([float(a), float(b)], [0.35, 0.35], color=col, lw=3)
            ax.plot([float(a)], [0.35], "o", ms=11, mfc=col if ca else "white", mec=col, mew=2.5, zorder=5)
            ax.plot([float(b)], [0.35], "o", ms=11, mfc=col if cb else "white", mec=col, mew=2.5, zorder=5)
        for pnt in points:
            x, t = pnt[0], pnt[1]
            ax.plot([float(x)], [0], "o", ms=9, color="#b23a3a", zorder=6)
            if t:
                ax.text(float(x), 0.35, t, ha="center", va="bottom", fontsize=13, fontweight="bold", color="#b23a3a")

    def draw(path):
        fig, ax = new_fig(*size)
        draw_on(ax)
        save(fig, path)
    draw.draw_on = draw_on
    return draw


def numline_panels(drawers, labels=("A", "B", "C", "D")):
    def draw(path):
        p = plt()
        fig, axs = p.subplots(4, 1, figsize=(7.5, 6.4), dpi=100)
        for ax, d, lab in zip(axs, drawers, labels):
            d.draw_on(ax)
            ax.set_title(f"Graph {lab}", fontsize=13, fontweight="bold", loc="left")
        fig.tight_layout()
        save(fig, path)
    return draw


def poly_draw(pts, side_labels=(), vert_labels=(), right_angles=(), extra_lines=(), angle_labels=(), size=5.5, dashed=(), title=None):
    """Polygon (or open figure) on blank axes. side_labels: (i, text) labels side pts[i]->pts[i+1].
    right_angles: vertex indices with a right-angle mark. extra_lines: ((x1,y1),(x2,y2),text,dashed)."""
    def draw(path):
        fig, ax = new_fig(size, size)
        xs = [float(p[0]) for p in pts] + [float(pts[0][0])]
        ys = [float(p[1]) for p in pts] + [float(pts[0][1])]
        ax.fill(xs, ys, color="#1f4e9c", alpha=0.10)
        ax.plot(xs, ys, color="#1f4e9c", lw=2.4)
        cx, cy = sum(xs[:-1]) / len(pts), sum(ys[:-1]) / len(pts)
        span = max(max(xs) - min(xs), max(ys) - min(ys))
        for i, t in side_labels:
            a, b = pts[i], pts[(i + 1) % len(pts)]
            mx, my = (float(a[0]) + float(b[0])) / 2, (float(a[1]) + float(b[1])) / 2
            dx, dy = mx - cx, my - cy
            n = math.hypot(dx, dy) or 1
            ax.text(mx + dx / n * span * 0.07, my + dy / n * span * 0.07, t, ha="center", va="center", fontsize=13, fontweight="bold")
        for i, t in vert_labels:
            a = pts[i]
            dx, dy = float(a[0]) - cx, float(a[1]) - cy
            n = math.hypot(dx, dy) or 1
            ax.text(float(a[0]) + dx / n * span * 0.06, float(a[1]) + dy / n * span * 0.06, t, ha="center", va="center", fontsize=13, style="italic")
        for i in right_angles:
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % len(pts)]
            s = span * 0.06
            u = [float(a[0]) - float(b[0]), float(a[1]) - float(b[1])]
            v = [float(c[0]) - float(b[0]), float(c[1]) - float(b[1])]
            nu, nv = math.hypot(*u), math.hypot(*v)
            u = [u[0] / nu * s, u[1] / nu * s]
            v = [v[0] / nv * s, v[1] / nv * s]
            bx, by = float(b[0]), float(b[1])
            ax.plot([bx + u[0], bx + u[0] + v[0], bx + v[0]], [by + u[1], by + u[1] + v[1], by + v[1]], color="black", lw=1.3)
        for (p1, p2, t, d) in extra_lines:
            ax.plot([float(p1[0]), float(p2[0])], [float(p1[1]), float(p2[1])], color="#b23a3a", lw=2, ls="--" if d else "-")
            if t:
                ax.text((float(p1[0]) + float(p2[0])) / 2 + span * 0.04, (float(p1[1]) + float(p2[1])) / 2, t, fontsize=13, fontweight="bold", color="#b23a3a")
        for (x, y, t) in angle_labels:
            ax.text(float(x), float(y), t, fontsize=12, ha="center", va="center")
        ax.set_aspect("equal")
        ax.axis("off")
        m = span * 0.18
        ax.set_xlim(min(xs) - m, max(xs) + m)
        ax.set_ylim(min(ys) - m, max(ys) + m)
        if title:
            ax.set_title(title, fontsize=13)
        save(fig, path)
    return draw


def circle_draw(r_label, show="radius", size=4.5):
    def draw(path):
        fig, ax = new_fig(size, size)
        t = [i / 100 * 2 * math.pi for i in range(101)]
        ax.fill([math.cos(a) for a in t], [math.sin(a) for a in t], color="#1f4e9c", alpha=0.10)
        ax.plot([math.cos(a) for a in t], [math.sin(a) for a in t], color="#1f4e9c", lw=2.4)
        ax.plot([0], [0], "o", color="black", ms=4)
        if show == "radius":
            ax.plot([0, 1], [0, 0], color="#b23a3a", lw=2)
            ax.text(0.5, 0.08, r_label, ha="center", fontsize=13, fontweight="bold")
        else:
            ax.plot([-1, 1], [0, 0], color="#b23a3a", lw=2)
            ax.text(0, 0.08, r_label, ha="center", fontsize=13, fontweight="bold")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-1.25, 1.25)
        save(fig, path)
    return draw


def box3d_draw(l, w, h, labels=True, size=5.0):
    """Oblique drawing of a rectangular prism with labelled length, width, height."""
    def draw(path):
        fig, ax = new_fig(size, size * 0.8)
        L_, H_, W_ = 4.0, 2.6, 1.6
        dx, dy = W_ * 0.7, W_ * 0.5
        f = [(0, 0), (L_, 0), (L_, H_), (0, H_)]
        b = [(x + dx, y + dy) for x, y in f]
        for i in range(4):
            ax.plot([f[i][0], f[(i + 1) % 4][0]], [f[i][1], f[(i + 1) % 4][1]], color="#1f4e9c", lw=2.2)
            hid = i in (0, 3)
            ax.plot([b[i][0], b[(i + 1) % 4][0]], [b[i][1], b[(i + 1) % 4][1]], color="#1f4e9c", lw=1.6 if not hid else 1.2, ls="--" if hid and i == 0 else "-")
        for i in range(4):
            ax.plot([f[i][0], b[i][0]], [f[i][1], b[i][1]], color="#1f4e9c", lw=1.6, ls="--" if i == 0 else "-")
        if labels:
            ax.text(L_ / 2, -0.35, str(l), ha="center", va="top", fontsize=13, fontweight="bold")
            ax.text(L_ + dx / 2 + 0.25, dy / 2 - 0.1, str(w), ha="left", va="center", fontsize=13, fontweight="bold")
            ax.text(-0.25, H_ / 2, str(h), ha="right", va="center", fontsize=13, fontweight="bold")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.6, L_ + dx + 1.6)
        ax.set_ylim(-1.0, H_ + dy + 0.4)
        save(fig, path)
    return draw


def cyl_draw(r_label, h_label, kind="cylinder", size=4.6):
    """Cylinder or cone with labelled radius and height."""
    def draw(path):
        fig, ax = new_fig(size, size)
        t = [i / 100 * 2 * math.pi for i in range(101)]
        ex = [math.cos(a) for a in t]
        ey = [0.3 * math.sin(a) for a in t]
        H_ = 2.4
        ax.plot(ex[:51], ey[:51], color="#1f4e9c", lw=1.3, ls="--")
        ax.plot(ex[50:], ey[50:], color="#1f4e9c", lw=2.2)
        if kind == "cylinder":
            ax.plot(ex, [y + H_ for y in ey], color="#1f4e9c", lw=2.2)
            ax.plot([-1, -1], [0, H_], color="#1f4e9c", lw=2.2)
            ax.plot([1, 1], [0, H_], color="#1f4e9c", lw=2.2)
        else:
            ax.plot([-1, 0], [0, H_], color="#1f4e9c", lw=2.2)
            ax.plot([1, 0], [0, H_], color="#1f4e9c", lw=2.2)
            ax.plot([0, 0], [0, H_], color="#b23a3a", lw=1.5, ls="--")
        ax.plot([0, 1], [0, 0], color="#b23a3a", lw=2)
        ax.text(0.5, -0.12, r_label, ha="center", va="top", fontsize=13, fontweight="bold")
        ax.text(1.12 if kind == "cylinder" else 0.1, H_ / 2, h_label, ha="left", va="center", fontsize=13, fontweight="bold")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.6, 2.2)
        ax.set_ylim(-0.7, H_ + 0.6)
        save(fig, path)
    return draw


def dot_draw(values, lo, hi, step=1, xlabel=""):
    from collections import Counter

    def draw(path):
        c = Counter(values)
        fig, ax = new_fig(7.0, 2.6)
        for v, k in c.items():
            ax.plot([float(v)] * k, [i + 1 for i in range(k)], "o", color="#1f4e9c", ms=10)
        ax.set_xlim(lo - step * 0.6, hi + step * 0.6)
        ax.set_ylim(0.3, max(c.values()) + 0.7)
        ax.set_yticks([])
        ax.set_xticks([float(x) for x in frange(lo, hi, step)])
        for sp in ("left", "top", "right"):
            ax.spines[sp].set_visible(False)
        ax.set_xlabel(xlabel)
        save(fig, path)
    return draw


def bar_draw(labels, values, ylabel="", xlabel="", hist=False, ystep=None):
    def draw(path):
        fig, ax = new_fig(6.4, 4.0)
        ax.bar(range(len(values)), values, width=1.0 if hist else 0.6, color="#9db7e0", edgecolor="#1f4e9c", lw=1.5)
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels(labels, fontsize=10)
        top = max(values)
        st = ystep or max(1, (top + 4) // 5)
        ax.set_yticks(list(range(0, top + st + 1, st)))
        ax.grid(True, axis="y", color="#cccccc")
        ax.set_axisbelow(True)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        save(fig, path)
    return draw


def box_draw(five, lo, hi, step=1, xlabel="", second=None, names=("", "")):
    """Box-and-whisker plot from a five-number summary (optionally two stacked plots)."""
    def one(ax, s, y):
        mn, q1, md, q3, mx = [float(v) for v in s]
        ax.plot([mn, q1], [y, y], color="black", lw=1.8)
        ax.plot([q3, mx], [y, y], color="black", lw=1.8)
        for v in (mn, mx):
            ax.plot([v, v], [y - 0.12, y + 0.12], color="black", lw=1.8)
        ax.fill([q1, q3, q3, q1], [y - 0.25, y - 0.25, y + 0.25, y + 0.25], color="#9db7e0", alpha=0.7)
        ax.plot([q1, q3, q3, q1, q1], [y - 0.25, y - 0.25, y + 0.25, y + 0.25, y - 0.25], color="#1f4e9c", lw=1.8)
        ax.plot([md, md], [y - 0.25, y + 0.25], color="#1f4e9c", lw=2.2)

    def draw(path):
        fig, ax = new_fig(7.0, 2.4 if not second else 3.4)
        one(ax, five, 1.0)
        if second:
            one(ax, second, 2.0)
            ax.set_yticks([1, 2])
            ax.set_yticklabels(list(names))
        else:
            ax.set_yticks([])
        ax.set_xlim(lo - step * 0.5, hi + step * 0.5)
        ax.set_ylim(0.4, 2.6 if second else 1.6)
        lab = step * 2 if (hi - lo) / step > 12 else step
        ax.set_xticks([float(x) for x in frange(lo, hi, lab)])
        ax.set_xticks([float(x) for x in frange(lo, hi, step)], minor=True)
        ax.grid(True, axis="x", which="both", color="#dddddd")
        for sp in ("left", "top", "right"):
            ax.spines[sp].set_visible(False)
        ax.set_xlabel(xlabel)
        save(fig, path)
    return draw


def table_img(rows, header=True, col_w=1.15):
    """Generic table image: rows is a list of lists of strings."""
    def draw(path):
        p = plt()
        fig, ax = p.subplots(figsize=(0.4 + col_w * len(rows[0]), 0.5 + 0.42 * len(rows)), dpi=100)
        ax.axis("off")
        t = ax.table(cellText=rows, loc="center", cellLoc="center")
        t.scale(1, 1.7)
        t.set_fontsize(12)
        for (i, j), c in t.get_celld().items():
            if header and i == 0:
                c.set_facecolor("#e8eef8")
                c.get_text().set_fontweight("bold")
        save(fig, path)
    return draw


# ------------------------------------------------------------------ exact overrides of Grade 8 helpers
import re as _re
from lib import norm_key as _nk8


def D(x, places=None):
    """Exact decimal text (no float round-off). Terminating values only unless `places` is given."""
    if places is not None:
        return Rd(F(x), places)
    x = F(x)
    need(is_term(x))
    s = "-" if x < 0 else ""
    a = abs(x)
    ip, rem = divmod(a.numerator, a.denominator)
    ds = ""
    while rem:
        rem *= 10
        ds += str(rem // a.denominator)
        rem %= a.denominator
    out = s + str(ip) + ("." + ds if ds else "")
    return "0" if out == "-0" else out


def norm_key(s):
    t = _re.sub(r"(?<=\d),(?=\d{3}\b)", "", str(s))
    return _nk8(t)


def dtext(x):
    """Exact decimal text with thousands commas (12,345.678)."""
    s = D(x)
    neg = s.startswith("-")
    s = s.lstrip("-")
    ip, _, fp = s.partition(".")
    return ("-" if neg else "") + f"{int(ip):,}" + ("." + fp if fp else "")


def reuse(f, lv=(0, 1, 2), tag=""):
    """Reuse a verified family at another grade: level L of the new skill uses level lv[L] of f.
    The new name changes the random seeds, so the items differ from the original grade's items."""
    def g(r, L):
        return f(r, lv[L])
    g.__name__ = "g6_" + f.__name__ + tag
    g.levels = {L for L in range(3) if lv[L] in f.levels}
    g.mode = f.mode
    return g


def mc_of(f, tag="mc"):
    """The same verified family, used only for multiple-choice slots (short answers for Tarsia / matching activities)."""
    g = reuse(f, (0, 1, 2), tag)
    g.mode = "mc"
    return g
