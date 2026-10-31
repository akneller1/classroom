"""Offline authoring helpers for Algebra 2 question banks (not a site engine).
Produces static JSON matching schemas/question-bank.schema.json."""
import json, os, re, random, hashlib
from fractions import Fraction as F
try:
    import sympy as sp
except ImportError:  # sympy unavailable (session 2): mathlite.py supplies exact helpers
    sp = None
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if sp: x, y, t, n = sp.symbols("x y t n")
OUT = "/home/claude/a2/out"
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")

def fmt(e, var=None, order="lex"):
    """Plain-text math (site renders text, not TeX)."""
    if isinstance(e, (int, F)):
        e = sp.nsimplify(e)
    if isinstance(e, sp.Basic) and var is not None and e.is_polynomial(var):
        e = sp.Poly(e, var).as_expr()
    s = sp.sstr(e, order=order) if isinstance(e, sp.Basic) else str(e)
    s = s.replace("sqrt(", "√(").replace("I", "i").replace("pi", "π")
    s = re.sub(r"√\((\d+|[a-z])\)", r"√\1", s)
    s = re.sub(r"√(\d+)\*(?=[a-z(])", r"√\1·", s)
    s = re.sub(r"\*\*(\d+)", lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r"\*\*\((-\d+)\)", lambda m: m.group(1).translate(SUP), s)
    s = re.sub(r"\*\*\(([^()]+)\)", r"^(\1)", s)
    s = re.sub(r"\*\*", "^", s)
    s = re.sub(r"(?<=[\d)²³⁴⁵])\*(?=[a-zA-Zπ√(])", "", s)
    s = re.sub(r"(?<=[a-z])\*(?=[a-z(√])", "", s)
    s = s.replace("*", "·")
    s = s.replace("exp(", "e^(")
    s = re.sub(r"\blog\(", "ln(", s)
    return s

def num(v):
    """Pretty number: ints plain, Fractions a/b, floats trimmed."""
    if isinstance(v, F):
        return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"
    if isinstance(v, float):
        return f"{v:.4f}".rstrip("0").rstrip(".")
    if isinstance(v, sp.Basic):
        return fmt(v)
    return str(v)

def lin(m, b, var="x"):
    """m·x + b as text with sign handling (m, b may be Fractions)."""
    return fmt(sp.nsimplify(m) * sp.Symbol(var) + sp.nsimplify(b), sp.Symbol(var))

def pt(a, b):
    return f"({num(a)}, {num(b)})"


def clean(t):
    if not isinstance(t, str): return t
    t = re.sub(r" - -(\d)", r" - (-\1)", t)
    t = re.sub(r" \+ -(\d)", r" - \1", t)
    t = re.sub(r"(?<![\d.\w])1([xy])\b", r"\1", t)
    t = re.sub(r"(?<=\S)  +", " ", t)
    return t


class Bank:
    def __init__(self, unit_id, short, standards, fresh=True):
        self.unit, self.short, self.std = unit_id, short, standards
        self.qs, self.meta, self.seen = [], {}, set()
        self.count = {}
        self.rng = random.Random(__import__("zlib").crc32(unit_id.encode()) % 10_000)  # deterministic across runs
        if fresh:  # drop stale images from earlier runs of this unit's script
            import shutil; shutil.rmtree(f"{OUT}/question-banks/assets/algebra2/{unit_id}", ignore_errors=True)

    @classmethod
    def resume(cls, unit_id, short, standards, bank_path, tags_path):
        """Load an existing bank so new items append with continuing IDs (top-up passes)."""
        b = cls(unit_id, short, standards, fresh=False)
        d = json.load(open(bank_path)); b.qs = d["questions"]; b.meta = json.load(open(tags_path))
        for q in b.qs:
            b.seen.add(re.sub(r"\s+", " ", q["prompt"].strip().lower()) + (q["diagram"]["spec"]["src"] if "diagram" in q else ""))
            m = re.match(r".*-s(\d+)-(cp2|cp1|honors)-(\d+)$", q["id"])
            k = (int(m.group(1)), m.group(2)); b.count[k] = max(b.count.get(k, 0), int(m.group(3)))
        return b

    def _id(self, skill, level):
        k = (skill, level)
        self.count[k] = self.count.get(k, 0) + 1
        return f"a2-{self.short}-s{skill:02d}-{level}-{self.count[k]:03d}"

    def add(self, skill, level, fmt_, prompt, answer, steps, options=None, parts=None,
            diagram=None, tags=()):
        assert level in ("cp2", "cp1", "honors"), level
        key = re.sub(r"\s+", " ", prompt.strip().lower()) + (diagram["spec"]["src"] if diagram else "")
        assert key not in self.seen, f"duplicate prompt: {prompt[:80]}"
        self.seen.add(key)
        assert steps and all(s.strip() for s in steps)
        prompt = clean(prompt); steps = [clean(s_) for s_ in steps]
        answer = [clean(a_) for a_ in answer] if isinstance(answer, list) else clean(answer)
        if options: options = [{"text": clean(o["text"]), "correct": o["correct"]} for o in options]
        if parts: parts = [{"prompt": clean(p_["prompt"]), "answer": clean(p_["answer"])} for p_ in parts]
        q = {"id": self._id(skill, level),
             "skillId": f"{self.unit}-skill-{skill:02d}",
             "level": level, "format": fmt_, "prompt": prompt.strip(),
             "answer": answer, "solutionSteps": steps}
        if fmt_ in ("multiple-choice", "select-all"):
            texts = [o["text"] for o in options]
            assert len(texts) == len(set(texts)), f"repeated option text: {texts}"
            nc = sum(o["correct"] for o in options)
            assert (nc == 1) if fmt_ == "multiple-choice" else (nc >= 2 and nc < len(options)), prompt
            q["options"] = options
        if fmt_ == "open-response":
            assert parts and len(parts) >= 4
            q["parts"] = parts
        if diagram:
            q["diagram"] = diagram
        if self.std.get(skill):
            q["standards"] = self.std[skill]
        q["sourceNotes"] = "Original Claude-authored item; answer computed and checked in authoring script. Awaiting human review."
        self.qs.append(q)
        self.meta[q["id"]] = sorted(set(tags))
        return q

    # -------- format builders --------
    def mc(self, skill, level, prompt, correct, wrong, steps, tags=(), diagram=None):
        correct = str(correct)
        wrong = [str(w) for w in wrong]
        wrong = [w for i, w in enumerate(wrong) if w != correct and w not in wrong[:i]]
        assert len(wrong) >= 2, f"need 2+ distinct distractors: {prompt}"
        opts = [{"text": correct, "correct": True}] + [{"text": w, "correct": False} for w in wrong[:3]]
        self.rng.shuffle(opts)
        return self.add(skill, level, "multiple-choice", prompt, correct, steps, options=opts,
                        tags=tags, diagram=diagram)

    def sa(self, skill, level, prompt, answer, steps, tags=(), diagram=None):
        return self.add(skill, level, "short-answer", prompt, answer if isinstance(answer, (int, float)) and not isinstance(answer, bool) else str(answer), steps, tags=tags, diagram=diagram)

    def sel(self, skill, level, prompt, right, wrong, steps, tags=(), diagram=None):
        right = [str(r) for r in right]; wrong = [str(w) for w in wrong]
        assert len(right) >= 2 and len(wrong) >= 1
        opts = [{"text": r, "correct": True} for r in right] + [{"text": w, "correct": False} for w in wrong]
        self.rng.shuffle(opts)
        return self.add(skill, level, "select-all", prompt, right, steps, options=opts,
                        tags=tags, diagram=diagram)

    def orq(self, skill, level, prompt, parts, steps, tags=(), diagram=None):
        parts = [{"prompt": p, "answer": a if isinstance(a, (int, float)) else str(a)} for p, a in parts]
        ans = "; ".join(f"({chr(97+i)}) {p['answer']}" for i, p in enumerate(parts))
        return self.add(skill, level, "open-response", prompt, ans, steps, parts=parts,
                        tags=tags, diagram=diagram)

    # -------- output --------
    def write(self):
        d = f"{OUT}/question-banks/algebra2"
        os.makedirs(d, exist_ok=True)
        with open(f"{d}/{self.unit}.json", "w") as f:
            json.dump({"schemaVersion": 1, "courseId": "algebra2", "unitId": self.unit,
                       "questions": self.qs}, f, ensure_ascii=False, indent=1)
        md = f"{OUT}/question-banks/algebra2/meta"
        os.makedirs(md, exist_ok=True)
        with open(f"{md}/{self.unit}.tags.json", "w") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=0)
        return f"{d}/{self.unit}.json"

    def counts(self):
        c = {}
        for q in self.qs:
            s = q["skillId"]
            c.setdefault(s, {"cp2": 0, "cp1": 0, "honors": 0, "formats": {}})
            c[s][q["level"]] += 1
            c[s]["formats"][q["format"]] = c[s]["formats"].get(q["format"], 0) + 1
        return c


# -------- graphs (PNG; shared games need raster images) --------
def graph(bank, name, curves, xr=(-6, 6), yr=(-6, 6), points=(), alt="", vlines=(), hlines=(),
          shade=None, labels=True, step=1):
    """curves: list of (callable f(x) | ('param', fx, fy, trange) | ('implicit', F), style dict).
    Returns diagram dict with relative src."""
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=150)
    ax.set_xlim(*xr); ax.set_ylim(*yr); ax.set_aspect("equal" if (xr[1]-xr[0]) == (yr[1]-yr[0]) else "auto")
    ax.set_xticks(np.arange(np.ceil(xr[0]/step)*step, xr[1]+1e-9, step))
    ax.set_yticks(np.arange(np.ceil(yr[0]/step)*step, yr[1]+1e-9, step))
    ax.grid(True, color="#bbbbbb", lw=0.6)
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero"); ax.spines[s].set_color("black")
    for s in ("right", "top"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)
    ax.set_xticklabels([("" if abs(v) < 1e-9 else f"{v:g}") for v in ax.get_xticks()])
    ax.set_yticklabels([("" if abs(v) < 1e-9 else f"{v:g}") for v in ax.get_yticks()])
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False, ms=4)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, ms=4)
    ax.text(1.0, 0.0, " x", transform=ax.get_yaxis_transform(), va="center", fontsize=9)
    ax.text(0.0, 1.0, "y ", transform=ax.get_xaxis_transform(), ha="right", va="bottom", fontsize=9)
    for v in vlines: ax.axvline(v, ls="--", color="black", lw=1)
    for h in hlines: ax.axhline(h, ls="--", color="black", lw=1)
    for c, style in curves:
        st = {"color": "#1f4e9e", "lw": 2}; st.update(style or {})
        if isinstance(c, tuple) and c[0] == "param":
            tt = np.linspace(*c[3], 2000); ax.plot(c[1](tt), c[2](tt), **st)
        elif isinstance(c, tuple) and c[0] == "implicit":
            X, Y = np.meshgrid(np.linspace(*xr, 600), np.linspace(*yr, 600))
            ax.contour(X, Y, c[1](X, Y), [0], colors=st["color"], linewidths=st["lw"])
        elif isinstance(c, tuple) and c[0] == "seg":
            ax.plot(c[1], c[2], **st)
        else:
            dom = style.pop("_dom", xr) if style else xr
            st.pop("_dom", None)
            xs = np.linspace(dom[0], dom[1], 3000)
            with np.errstate(all="ignore"):
                ys = np.array([c(v) for v in xs], dtype=float)
            ys[np.abs(ys) > 1e3] = np.nan
            jump = np.abs(np.diff(ys)) > (yr[1]-yr[0])
            ys[1:][jump] = np.nan
            ax.plot(xs, ys, **st)
    if shade:
        X, Y = np.meshgrid(np.linspace(*xr, 400), np.linspace(*yr, 400))
        ax.contourf(X, Y, shade(X, Y).astype(float), levels=[0.5, 1.5], colors=["#9ab8e8"], alpha=0.45)
    for p in points:
        px, py = p[0], p[1]; filled = p[2] if len(p) > 2 else True
        ax.plot(px, py, "o", ms=5, mfc="black" if filled else "white", mec="black", zorder=5)
        if len(p) > 3 and p[3]:
            ax.annotate(p[3], (px, py), textcoords="offset points", xytext=(5, 5), fontsize=8,
                        bbox=dict(fc="white", ec="none", alpha=0.8, pad=0.5))
    rel = f"question-banks/assets/algebra2/{bank.unit}/{name}.png"
    os.makedirs(os.path.dirname(f"{OUT}/{rel}"), exist_ok=True)
    fig.tight_layout(); fig.savefig(f"{OUT}/{rel}"); plt.close(fig)
    assert alt
    return {"type": "image", "spec": {"src": rel, "alt": alt}}

def roots_txt(sols, var="x"):
    """'x = a ± b' for conjugate/irrational pairs, else 'x = r1 or x = r2' (ascending)."""
    sols = [sp.nsimplify(sp.radsimp(s)) for s in sols]
    if len(sols) == 2:
        s = sp.nsimplify((sols[0] + sols[1]) / 2); d = sp.simplify(sols[0] - s)
        if s.is_rational and not d.is_rational:
            if d.could_extract_minus_sign(): d = -d
            if d.has(sp.I) and sp.re(d) == 0 and (sp.im(d)).could_extract_minus_sign(): d = -d
            dtxt = fmt(d)
            return f"{var} = ±{dtxt}" if s == 0 else f"{var} = {fmt(s)} ± {dtxt}"
    try:
        sols = sorted(sols, key=lambda v: float(v))
    except TypeError:
        pass
    return " or ".join(f"{var} = {fmt(v)}" for v in sols)

def fmt_terms(e, main, *others):
    """Polynomial text ordered by descending powers of `main`, then ascending powers of others."""
    P = sp.Poly(sp.expand(e), main, *others)
    out = ""
    for mon, c in sorted(P.terms(), key=lambda t: (-t[0][0], sum(t[0][1:]))):
        term = sp.Mul(abs(c), *[g**d for g, d in zip(P.gens, mon)])
        s = fmt(term)
        out += (s if not out else (" - " if c < 0 else " + ") + s) if out or c > 0 else "-" + s
    return out
