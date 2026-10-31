"""Print-safe geometry figures (black/white PNG) for question banks. Drawn from the true numbers unless
the caller passes schematic=True, which adds 'Not drawn to scale'."""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from lib import OUT

INK = "black"


class Fig:
    def __init__(self, w=4.2, h=3.4):
        self.f, self.ax = plt.subplots(figsize=(w, h), dpi=150)
        self.ax.set_aspect("equal"); self.ax.axis("off"); self.pts = []

    # ---- primitives ----
    def seg(self, A, B, ls="-", lw=1.6, color=INK):
        self.ax.plot([A[0], B[0]], [A[1], B[1]], ls=ls, lw=lw, color=color); self.pts += [A, B]

    def poly(self, P, lw=1.6, fill=None):
        Q = list(P) + [P[0]]
        if fill: self.ax.fill([p[0] for p in P], [p[1] for p in P], color=fill, alpha=0.35, lw=0)
        self.ax.plot([p[0] for p in Q], [p[1] for p in Q], color=INK, lw=lw); self.pts += list(P)

    def line(self, A, B, ext=0.25, arrows=True, lw=1.4):
        d = np.subtract(B, A); A2 = np.subtract(A, d * ext); B2 = np.add(B, d * ext)
        self.ax.annotate("", xy=B2, xytext=A2, arrowprops=dict(arrowstyle="<->" if arrows else "-", lw=lw, color=INK)); self.pts += [tuple(A2), tuple(B2)]

    def ray(self, A, B, lw=1.4):
        self.ax.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="->", lw=lw, color=INK)); self.pts += [A, B]

    def dot(self, P, name=None, off=(6, 6), filled=True):
        self.ax.plot(*P, "o", ms=4, mfc=INK if filled else "white", mec=INK, zorder=5); self.pts.append(P)
        if name: self.text(P, name, off)

    def text(self, P, s, off=(0, 0), size=10, ha="center"):
        self.ax.annotate(s, P, textcoords="offset points", xytext=off, ha=ha, va="center", fontsize=size, color=INK,
                         bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.4))

    def names(self, P, labels, center=None):
        c = center or (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))
        for p, l in zip(P, labels):
            d = np.subtract(p, c); n = np.hypot(*d) or 1
            self.text(p, l, off=(12 * d[0] / n, 12 * d[1] / n), size=11)

    def side(self, A, B, s, center=None, dist=10):
        m = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2); d = np.subtract(B, A); nrm = np.array([-d[1], d[0]]) / (np.hypot(*d) or 1)
        if center is not None and np.dot(nrm, np.subtract(center, m)) > 0: nrm = -nrm
        self.text(m, s, off=(dist * nrm[0], dist * nrm[1]))

    def ticks(self, A, B, n=1, size=None):
        m = np.add(A, B) / 2; d = np.subtract(B, A); L = np.hypot(*d); u = d / L; nrm = np.array([-u[1], u[0]])
        s = size or 0.04 * self.span()
        for i in range(n):
            c = m + u * (i - (n - 1) / 2) * s * 0.6
            self.ax.plot([c[0] - nrm[0] * s / 2, c[0] + nrm[0] * s / 2], [c[1] - nrm[1] * s / 2, c[1] + nrm[1] * s / 2], color=INK, lw=1.2)

    def arrows(self, A, B, n=1):
        m = np.add(A, B) / 2; d = np.subtract(B, A); u = d / np.hypot(*d); s = 0.035 * self.span()
        for i in range(n):
            c = m + u * i * s * 0.9
            self.ax.annotate("", xy=c + u * s * 0.5, xytext=c - u * s * 0.5, arrowprops=dict(arrowstyle="->", lw=1.2, color=INK))

    def angle(self, V, A, B, label=None, r=None, n=1, right=False):
        """Arc at vertex V between rays VA and VB (counter-clockwise from VA to VB along the smaller angle)."""
        r = r or 0.09 * self.span()
        a1 = math.atan2(A[1] - V[1], A[0] - V[0]); a2 = math.atan2(B[1] - V[1], B[0] - V[0])
        d = (a2 - a1) % (2 * math.pi)
        if d > math.pi: a1, a2, d = a2, a1, 2 * math.pi - d
        if right:
            u = np.array([math.cos(a1), math.sin(a1)]) * r * 0.7; w = np.array([math.cos(a2), math.sin(a2)]) * r * 0.7
            P1, P2, P3 = np.add(V, u), np.add(V, u + w), np.add(V, w)
            self.ax.plot([P1[0], P2[0], P3[0]], [P1[1], P2[1], P3[1]], color=INK, lw=1.1)
        else:
            for i in range(n):
                t = np.linspace(a1, a1 + d, 40); rr = r * (1 + 0.18 * i)
                self.ax.plot(V[0] + rr * np.cos(t), V[1] + rr * np.sin(t), color=INK, lw=1.1)
        if label:
            mid = a1 + d / 2; rr = r * (1.9 if d > 0.5 else 2.8)
            self.ax.text(V[0] + rr * math.cos(mid), V[1] + rr * math.sin(mid), label, ha="center", va="center", fontsize=9.5,
                         bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.3))

    def circle(self, C, r, lw=1.6, ls="-"):
        t = np.linspace(0, 2 * math.pi, 300); self.ax.plot(C[0] + r * np.cos(t), C[1] + r * np.sin(t), color=INK, lw=lw, ls=ls)
        self.pts += [(C[0] - r, C[1] - r), (C[0] + r, C[1] + r)]

    def ellipse(self, C, a, b, ls="-", half=None, lw=1.6):
        t = np.linspace(0, math.pi, 100) if half == "top" else np.linspace(math.pi, 2 * math.pi, 100) if half == "bottom" else np.linspace(0, 2 * math.pi, 200)
        self.ax.plot(C[0] + a * np.cos(t), C[1] + b * np.sin(t), color=INK, lw=lw, ls=ls); self.pts += [(C[0] - a, C[1] - b), (C[0] + a, C[1] + b)]

    def span(self):
        if not self.pts: return 10
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        return max(max(xs) - min(xs), max(ys) - min(ys), 1)

    def save(self, bank, name, alt, schematic=False):
        if schematic:
            self.ax.text(0.99, 0.01, "Not drawn to scale", transform=self.ax.transAxes, ha="right", va="bottom", fontsize=7.5, style="italic")
        rel = f"question-banks/assets/{bank.course}/{bank.unit}/{name}.png"
        os.makedirs(os.path.dirname(f"{OUT}/{rel}"), exist_ok=True)
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]; m = 0.12 * self.span()
        self.ax.set_xlim(min(xs) - m, max(xs) + m); self.ax.set_ylim(min(ys) - m, max(ys) + m); self.f.tight_layout(); self.f.savefig(f"{OUT}/{rel}"); plt.close(self.f)
        assert alt
        return {"type": "image", "spec": {"src": rel, "alt": alt}}


# ---- composite figures ----
def tri_from_sides(a, b, c):
    """Triangle ABC with BC = a, CA = b, AB = c; returns A, B, C (B at origin, C on x-axis)."""
    assert a + b > c and a + c > b and b + c > a
    x = (c * c - b * b + a * a) / (2 * a); y = math.sqrt(max(c * c - x * x, 0))
    return (x, y), (0.0, 0.0), (float(a), 0.0)


def tri_from_angles(A_deg, B_deg, base=6.0):
    """Triangle with angle A at apex, B at left base vertex, C at right; base BC length `base`."""
    C_deg = 180 - A_deg - B_deg; assert C_deg > 0
    b_side = base * math.sin(math.radians(B_deg)) / math.sin(math.radians(A_deg))  # AC
    c_side = base * math.sin(math.radians(C_deg)) / math.sin(math.radians(A_deg))  # AB
    A = (c_side * math.cos(math.radians(B_deg)), c_side * math.sin(math.radians(B_deg)))
    return A, (0.0, 0.0), (base, 0.0)


def transversal(bank, name, labels, alt, slope_deg=62, schematic=False):
    """Two horizontal parallel lines cut by a transversal. labels: dict position→text, positions
    'a1'..'a4' at the upper intersection (1 = upper-right, 2 = upper-left, 3 = lower-left, 4 = lower-right), 'b1'..'b4' at the lower."""
    F_ = Fig(4.4, 3.6); t = math.radians(slope_deg)
    P1, P2 = (0, 2.0), (0, -2.0); P1 = (2.0 / math.tan(t), 2.0); P2 = (-2.0 / math.tan(t), -2.0)
    for y_ in (2.0, -2.0):
        F_.line((-4.5, y_), (4.5, y_), ext=0.0); F_.arrows((2.6, y_), (3.4, y_))
    F_.line(np.subtract(P2, (math.cos(t) * 1.6, math.sin(t) * 1.6)), np.add(P1, (math.cos(t) * 1.6, math.sin(t) * 1.6)), ext=0.0)
    for key, txt in labels.items():
        base = P1 if key[0] == "a" else P2; q = int(key[1])
        dirs = {1: (t / 2), 2: (t + (math.pi - t) / 2), 3: (math.pi + t / 2), 4: (math.pi + t + (math.pi - t) / 2)}
        ang = dirs[q]; F_.text((base[0] + 1.25 * math.cos(ang), base[1] + 0.7 * math.sin(ang)), txt, size=10)
    return F_.save(bank, name, alt, schematic)
