"""PNG figures for the Discrete Math banks (matplotlib, white background, print friendly).
Each function writes question-banks/assets/discrete/<unit>/<name>.png and returns the repo-relative path."""
import os, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
INK = '#1f2a44'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12})


def _save(fig, unit, name):
    rel = 'question-banks/assets/discrete/%s/%s.png' % (unit, name)
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=110, facecolor='white', bbox_inches='tight', pad_inches=0.08)
    plt.close(fig)
    return rel


def venn(unit, name, regions, labels=('A', 'B', 'C'), universe='U', shade=()):
    """regions: dict keyed by membership string over the sets, e.g. for 2 sets 'AB','A','B','' (outside).
    shade: list of region keys to shade lightly."""
    n = len(labels)
    fig, ax = plt.subplots(figsize=(4.2, 3.2 if n == 2 else 3.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8 if n == 3 else 7); ax.axis('off'); ax.set_aspect('equal')
    H = 8 if n == 3 else 7
    ax.add_patch(Rectangle((0.2, 0.2), 9.6, H - 0.4, fill=False, lw=1.6, ec=INK))
    ax.text(0.5, H - 0.75, universe, fontsize=13, color=INK, style='italic')
    if n == 2:
        centers = [(3.9, 3.5), (6.1, 3.5)]
        r = 2.4
        pos = {labels[0] + labels[1]: (5.0, 3.5), labels[0]: (2.8, 3.5), labels[1]: (7.2, 3.5), '': (8.9, 1.0)}
        lab = [(1.6, 6.0), (8.4, 6.0)]
    else:
        centers = [(3.9, 4.9), (6.1, 4.9), (5.0, 3.0)]
        r = 2.25
        A, B, Cc = labels
        pos = {A + B + Cc: (5.0, 4.25), A + B: (5.0, 5.75), A + Cc: (3.85, 3.6), B + Cc: (6.15, 3.6), A: (3.05, 5.5), B: (6.95, 5.5), Cc: (5.0, 1.65), '': (9.0, 0.8)}
        lab = [(1.5, 6.9), (8.5, 6.9), (5.0, 0.35)]
    if shade:
        import numpy as np
        xs, ys = np.meshgrid(np.linspace(0.25, 9.75, 380), np.linspace(0.25, H - 0.25, 300))
        mask = np.zeros_like(xs, dtype=bool)
        for key in shade:
            m = np.ones_like(xs, dtype=bool)
            for (cx, cy), L in zip(centers, labels):
                inside = (xs - cx) ** 2 + (ys - cy) ** 2 <= r * r
                m &= inside if L in key else ~inside
            mask |= m
        ax.contourf(xs, ys, mask.astype(float), levels=[0.5, 1.5], colors=['#cfe0f5'])
    for (cx, cy), L, (lx, ly) in zip(centers, labels, lab):
        ax.add_patch(Circle((cx, cy), r, fill=False, lw=1.8, ec=INK))
        ax.text(lx, ly, L, fontsize=15, fontweight='bold', color=INK, ha='center', va='center')
    for key, txt in regions.items():
        if txt is None or txt == '':
            continue
        x, y = pos[key]
        ax.text(x, y, str(txt), ha='center', va='center', fontsize=11 if len(str(txt)) < 9 else 9.5, color='#111')
    return _save(fig, unit, name)


def graph(unit, name, vertices, edges, pos=None, directed=False, loops_ok=True, weights=None, colors=None, size=(4.0, 3.2), highlight=()):
    """edges: list of (u, v); repeated pairs are drawn as curved parallel edges; (u, u) is a loop."""
    fig, ax = plt.subplots(figsize=size)
    ax.axis('off'); ax.set_aspect('equal')
    if pos is None:
        k = len(vertices)
        pos = {v: (math.cos(math.pi / 2 + 2 * math.pi * i / k), math.sin(math.pi / 2 + 2 * math.pi * i / k)) for i, v in enumerate(vertices)}
    seen = {}
    for idx, (u, v) in enumerate(edges):
        key = tuple(sorted((u, v))) if not directed else (u, v)
        cnt = seen.get(key, 0)
        seen[key] = cnt + 1
        lw = 3.2 if (u, v) in highlight or (v, u) in highlight else 1.6
        col = '#c0392b' if lw > 2 else INK
        if u == v:
            x, y = pos[u]
            cx, cy = x * 1.0, y
            ang = math.atan2(y, x) if (x, y) != (0, 0) else math.pi / 2
            lx, ly = x + 0.22 * math.cos(ang), y + 0.22 * math.sin(ang)
            ax.add_patch(Circle((lx, ly), 0.16 + 0.07 * cnt, fill=False, lw=lw, ec=col))
            if directed:
                ax.annotate('', xy=(lx + 0.02, ly - 0.16 - 0.07 * cnt), xytext=(lx - 0.06, ly - 0.15 - 0.07 * cnt), arrowprops=dict(arrowstyle='-|>', color=col, lw=1.2))
            continue
        rad = 0.0 if cnt == 0 else (0.25 * ((cnt + 1) // 2) * (1 if cnt % 2 else -1))
        if directed and (v, u) in edges and u != v:
            rad = 0.18 if rad == 0 else rad
        p = FancyArrowPatch(pos[u], pos[v], connectionstyle='arc3,rad=%s' % rad, arrowstyle='-|>' if directed else '-', mutation_scale=16,
                            lw=lw, color=col, shrinkA=13, shrinkB=13)
        ax.add_patch(p)
        if weights:
            w = weights[idx]
            mx, my = (pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2
            dx, dy = pos[v][0] - pos[u][0], pos[v][1] - pos[u][1]
            L = math.hypot(dx, dy) or 1
            off = 0.09 + abs(rad) * L * 0.5
            sgn = 1 if rad >= 0 else -1
            ax.text(mx - dy / L * off * sgn, my + dx / L * off * sgn, str(w), fontsize=10, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'))
    for v in vertices:
        x, y = pos[v]
        fc = (colors or {}).get(v, 'white')
        ax.add_patch(Circle((x, y), 0.11, fc=fc, ec=INK, lw=1.6, zorder=3))
        ax.text(x, y, str(v), ha='center', va='center', fontsize=11, fontweight='bold', zorder=4, color=INK)
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - 0.45, max(xs) + 0.45); ax.set_ylim(min(ys) - 0.45, max(ys) + 0.45)
    return _save(fig, unit, name)


def region(unit, name, constraints, xmax, ymax, vertices=None, objective_line=None, labels=True, size=(4.2, 3.6)):
    """constraints: list of (a, b, c, label) meaning a·x + b·y <= c (use negative to flip). Shades the feasible
    set (x, y >= 0 always added) and marks vertices."""
    import numpy as np
    fig, ax = plt.subplots(figsize=size)
    xs, ys = np.meshgrid(np.linspace(0, xmax, 500), np.linspace(0, ymax, 500))
    ok = (xs >= 0) & (ys >= 0)
    for a, b, c, _ in constraints:
        ok &= a * xs + b * ys <= c + 1e-9
    ax.contourf(xs, ys, ok.astype(float), levels=[0.5, 1.5], colors=['#d5e6f7'])
    t = np.linspace(0, xmax, 200)
    for a, b, c, lab in constraints:
        if abs(b) > 1e-12:
            ax.plot(t, (c - a * t) / b, color=INK, lw=1.4)
        else:
            ax.axvline(c / a, color=INK, lw=1.4)
    if objective_line:
        a, b, c = objective_line
        ax.plot(t, (c - a * t) / b, color='#c0392b', lw=1.4, ls='--')
    for (x, y) in (vertices or []):
        ax.plot([x], [y], 'o', color=INK, ms=5)
        if labels:
            ax.annotate('(%s, %s)' % (fmtn(x), fmtn(y)), (x, y), textcoords='offset points', xytext=(5, 5), fontsize=9)
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.grid(True, color='#e3e6ec', lw=0.6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    return _save(fig, unit, name)


def fmtn(x):
    from fractions import Fraction
    x = Fraction(x).limit_denominator(1000)
    return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)


def tree(unit, name, levels, size=(5.0, 3.2)):
    """Possibility tree. levels: list of lists of branch labels per stage (same branching at each node)."""
    fig, ax = plt.subplots(figsize=size)
    ax.axis('off')
    leaves = 1
    for L in levels:
        leaves *= len(L)
    depth = len(levels)
    def draw(x, y0, y1, d):
        y = (y0 + y1) / 2
        if d == depth:
            return
        k = len(levels[d])
        for i, lab in enumerate(levels[d]):
            a = y0 + (y1 - y0) * i / k
            b = y0 + (y1 - y0) * (i + 1) / k
            ny = (a + b) / 2
            ax.plot([x, x + 1], [y, ny], color=INK, lw=1.2)
            ax.text(x + 1.05, ny, lab, va='center', fontsize=9 if leaves > 12 else 11)
            draw(x + 1.5, a, b, d + 1)
    draw(0, 0, leaves, 0)
    ax.plot([0], [leaves / 2], 'o', color=INK)
    ax.set_xlim(-0.2, 1.5 * depth + 0.6); ax.set_ylim(-0.3, leaves + 0.3)
    return _save(fig, unit, name)


def matrix_table(unit, name, header, rows, size=None, title=None):
    """Plain table image (used for preference schedules and data tables)."""
    nr, nc = len(rows) + 1, len(header)
    fig, ax = plt.subplots(figsize=size or (0.95 * nc + 0.6, 0.38 * nr + 0.3))
    ax.axis('off')
    tb = ax.table(cellText=[[str(c) for c in r] for r in rows], colLabels=header, loc='center', cellLoc='center')
    tb.auto_set_font_size(False); tb.set_fontsize(11); tb.scale(1, 1.35)
    for (i, j), cell in tb.get_celld().items():
        cell.set_edgecolor(INK)
        if i == 0:
            cell.set_text_props(fontweight='bold'); cell.set_facecolor('#eef3fa')
    if title:
        ax.set_title(title, fontsize=11)
    return _save(fig, unit, name)
