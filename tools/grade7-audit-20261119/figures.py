"""Grade 7 audit #13 (2026-11-19): figures for the new items, drawn to match the existing Grade 7 diagrams
(white background, navy ink, a blue accent, 400–600 px). Every function writes one PNG and returns its alt text."""
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'DejaVu Sans'
INK, BLUE, FILL, GRID = '#14173a', '#1f4e9a', '#c9d8f0', '#c7ccd6'
DPI = 100


def _save(fig, path):
    fig.savefig(path, dpi=DPI, facecolor='white', bbox_inches='tight', pad_inches=0.12, metadata={'Software': None})
    plt.close(fig)


def line_graph(path, pts_or_line, xmax, ymax, xlabel, ylabel, xstep=1, ystep=1, point_labels=()):
    """A first-quadrant graph of a line (two points) with grid; labelled points are marked."""
    fig, ax = plt.subplots(figsize=(4.4, 4.0))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax)
    ax.set_xticks(range(0, xmax + 1, xstep)); ax.set_yticks(range(0, ymax + 1, ystep))
    ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    (x1, y1), (x2, y2) = pts_or_line
    m = (y2 - y1) / (x2 - x1)
    xs = [0, xmax]; ys = [y1 + m * (x - x1) for x in xs]
    ax.plot(xs, ys, color=BLUE, linewidth=2.4)
    for (x, y) in point_labels:
        ax.plot([x], [y], 'o', color=INK, markersize=6)
        ax.annotate(f'({x:g}, {y:g})', (x, y), textcoords='offset points', xytext=(6, -14), fontsize=10, color=INK)
    ax.set_xlabel(xlabel, fontsize=11, color=INK); ax.set_ylabel(ylabel, fontsize=11, color=INK)
    ax.tick_params(labelsize=9, colors=INK)
    _save(fig, path)
    pts = ', '.join(f'({x:g}, {y:g})' for x, y in point_labels)
    through = 'the origin' if abs(ys[0]) < 1e-9 else f'(0, {ys[0]:g})'
    return (f'Graph of a straight line on a grid from 0 to {xmax} on the x-axis ({xlabel}) and 0 to {ymax} on the y-axis ({ylabel}). '
            f'The line passes through {through}' + (f' and the marked points {pts}.' if pts else '.'))


def angles(path, kind, labels):
    """kind 'vertical': two crossing lines with the two labelled vertical angles; 'linear': three rays on a line
    (labels for the two adjacent angles); 'right': a right angle split into two labelled adjacent angles."""
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    ax.set_aspect('equal'); ax.axis('off')
    if kind == 'vertical':
        a = math.radians(35)
        for t in (a, math.pi - a):
            ax.plot([-2 * math.cos(t), 2 * math.cos(t)], [-2 * math.sin(t), 2 * math.sin(t)], color=INK, linewidth=2)
        ax.text(1.05, 0, labels[0], ha='left', va='center', fontsize=12, color=BLUE)
        ax.text(-1.05, 0, labels[1], ha='right', va='center', fontsize=12, color=BLUE)
        alt = f'Two lines cross. The angle on the right is labelled {labels[0]} and the vertical angle on the left is labelled {labels[1]}.'
    elif kind == 'linear':
        ax.plot([-2.2, 2.2], [0, 0], color=INK, linewidth=2)
        t = math.radians(65)
        ax.plot([0, 2 * math.cos(t)], [0, 2 * math.sin(t)], color=INK, linewidth=2)
        ax.text(1.1, 0.35, labels[0], ha='left', fontsize=12, color=BLUE)
        ax.text(-0.6, 0.45, labels[1], ha='right', fontsize=12, color=BLUE)
        alt = f'A straight line with a ray from a point on it, making two adjacent angles: {labels[0]} on the right and {labels[1]} on the left.'
    else:
        ax.plot([0, 2.4], [0, 0], color=INK, linewidth=2); ax.plot([0, 0], [0, 2.4], color=INK, linewidth=2)
        ax.plot([0.25, 0.25, 0], [0, 0.25, 0.25], color=INK, linewidth=1.2)
        t = math.radians(40)
        ax.plot([0, 2.3 * math.cos(t)], [0, 2.3 * math.sin(t)], color=INK, linewidth=2)
        ax.text(0.95, 0.28, labels[0], fontsize=12, color=BLUE)
        ax.text(0.25, 1.15, labels[1], fontsize=12, color=BLUE)
        alt = f'A right angle split by a ray into two adjacent angles labelled {labels[0]} and {labels[1]}.'
    _save(fig, path)
    return alt


def _box(ax, x, y, w, h, d, **kw):
    dx, dy = d * 0.6, d * 0.45
    P = lambda a, b, c: (a + c * 0.6 * dx / d if d else a, b + c * 0.45 * dy / d if d else b)
    front = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    back = [(px + dx, py + dy) for px, py in front]
    ax.plot(*zip(*front), color=INK, linewidth=1.8)
    ax.plot(*zip(*[(x + w, y), (x + w + dx, y + dy), (x + w + dx, y + h + dy), (x + w, y + h)]), color=INK, linewidth=1.8)
    ax.plot(*zip(*[(x, y + h), (x + dx, y + h + dy), (x + w + dx, y + h + dy)]), color=INK, linewidth=1.8)
    ax.plot(*zip(*[(x, y), (x + dx, y + dy), (x + w + dx, y + dy)]), color=INK, linewidth=1.2, linestyle=(0, (4, 3)))
    ax.plot(*zip(*[(x + dx, y + dy), (x + dx, y + h + dy)]), color=INK, linewidth=1.2, linestyle=(0, (4, 3)))
    return dx, dy


def slice_fig(path, solid, cut):
    """A solid with a shaded slice. solid: 'prism', 'pyramid', 'cylinder', 'cone'; cut: 'parallel' (to the base) or
    'perpendicular' (vertical, through the middle)."""
    fig, ax = plt.subplots(figsize=(3.8, 3.4))
    ax.set_aspect('equal'); ax.axis('off')
    if solid == 'prism':
        w, h, d = 3.0, 2.4, 1.6
        dx, dy = _box(ax, 0, 0, w, h, d)
        if cut == 'parallel':
            yy = h * 0.5
            poly = [(0, yy), (w, yy), (w + dx, yy + dy), (dx, yy + dy)]
        else:
            xx = w * 0.5
            poly = [(xx, 0), (xx + dx, dy), (xx + dx, h + dy), (xx, h)]
        ax.add_patch(plt.Polygon(poly, closed=True, facecolor=FILL, edgecolor=BLUE, linewidth=2, alpha=0.85))
    elif solid == 'pyramid':
        base = [(0, 0), (3, 0), (3.9, 0.7), (0.9, 0.7)]
        apex = (1.95, 3.0)
        ax.plot(*zip(*[base[0], base[1], base[2]]), color=INK, linewidth=1.8)
        ax.plot(*zip(*[base[2], base[3], base[0]]), color=INK, linewidth=1.2, linestyle=(0, (4, 3)))
        for b in base:
            ax.plot(*zip(*[b, apex]), color=INK, linewidth=1.8 if b != base[3] else 1.2, linestyle='-' if b != base[3] else (0, (4, 3)))
        if cut == 'parallel':
            t = 0.5
            poly = [(b[0] + (apex[0] - b[0]) * t, b[1] + (apex[1] - b[1]) * t) for b in base]
        else:
            m1 = ((base[0][0] + base[1][0]) / 2, (base[0][1] + base[1][1]) / 2)
            m2 = ((base[2][0] + base[3][0]) / 2, (base[2][1] + base[3][1]) / 2)
            poly = [m1, m2, apex]
        ax.add_patch(plt.Polygon(poly, closed=True, facecolor=FILL, edgecolor=BLUE, linewidth=2, alpha=0.85))
    else:
        r, h = 1.4, 2.8
        from matplotlib.patches import Ellipse
        ax.add_patch(Ellipse((0, 0), 2 * r, 0.7, fill=False, edgecolor=INK, linewidth=1.8))
        if solid == 'cylinder':
            ax.add_patch(Ellipse((0, h), 2 * r, 0.7, fill=False, edgecolor=INK, linewidth=1.8))
            ax.plot([-r, -r], [0, h], color=INK, linewidth=1.8); ax.plot([r, r], [0, h], color=INK, linewidth=1.8)
            if cut == 'parallel':
                ax.add_patch(Ellipse((0, h / 2), 2 * r, 0.7, facecolor=FILL, edgecolor=BLUE, linewidth=2, alpha=0.85))
            else:
                ax.add_patch(plt.Polygon([(-r * 0.9, 0.15), (r * 0.9, -0.15), (r * 0.9, h - 0.15), (-r * 0.9, h + 0.15)], closed=True, facecolor=FILL, edgecolor=BLUE, linewidth=2, alpha=0.85))
        else:
            ax.plot([-r, 0], [0, h], color=INK, linewidth=1.8); ax.plot([r, 0], [0, h], color=INK, linewidth=1.8)
            if cut == 'parallel':
                ax.add_patch(Ellipse((0, h / 2), r, 0.35, facecolor=FILL, edgecolor=BLUE, linewidth=2, alpha=0.85))
            else:
                ax.add_patch(plt.Polygon([(-r, 0), (r, 0), (0, h)], closed=True, facecolor=FILL, edgecolor=BLUE, linewidth=2, alpha=0.6))
        ax.set_xlim(-r - 0.4, r + 0.4)
    ax.autoscale_view()
    _save(fig, path)
    names = {'prism': 'a rectangular prism', 'pyramid': 'a square pyramid', 'cylinder': 'a cylinder', 'cone': 'a cone'}
    how = 'parallel to the base' if cut == 'parallel' else 'perpendicular to the base, through the middle' + (' and the top vertex' if solid in ('pyramid', 'cone') else '')
    return f'Drawing of {names[solid]} with a shaded slice {how}.'


def story_graph(path, segs, ylabel, xlabel='time', y0=0.0):
    """A qualitative graph made of straight pieces; segs is a list of (dx, dy). No numbers on the axes."""
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    x, y, xs, ys = 0.0, y0, [0.0], [y0]
    for dx, dy in segs:
        x += dx; y += dy; xs.append(x); ys.append(y)
    ax.plot(xs, ys, color=BLUE, linewidth=2.6)
    ax.set_xlim(0, x * 1.05); ax.set_ylim(0, max(max(ys), 1) * 1.2)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(xlabel, fontsize=11, color=INK); ax.set_ylabel(ylabel, fontsize=11, color=INK)
    _save(fig, path)
    words = {1: 'rises', 0: 'stays level', -1: 'falls'}
    parts = [words[(dy > 0) - (dy < 0)] + (' steeply' if abs(dy) / dx > 1.5 and dy else ' slowly' if dy and abs(dy) / dx < 0.6 else '') for dx, dy in segs]
    return f'Graph of {ylabel} against {xlabel} with no numbers. From left to right the graph ' + ', then '.join(parts) + '.'


# ---- Grade 7 audit G4 (#13, the rest): polygons, congruence marks, circles, scale drawings, side-by-side dot plots ----

def polygon(path, labels, name):
    """A convex polygon with one label per vertex angle (numbers or expressions). Not drawn to scale."""
    n = len(labels)
    fig, ax = plt.subplots(figsize=(3.8, 3.4))
    ax.set_aspect('equal'); ax.axis('off')
    jit = [1.0, 0.9, 1.08, 0.95, 1.05, 0.92, 1.0, 1.06]
    pts = [(jit[i] * math.cos(math.pi / 2 + 2 * math.pi * i / n), jit[i] * math.sin(math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
    ax.add_patch(plt.Polygon(pts, closed=True, facecolor='#eef3fb', edgecolor=INK, linewidth=2))
    for (x, y), lab in zip(pts, labels):
        ax.text(x * 0.6, y * 0.6, lab, ha='center', va='center', fontsize=10.5, color=BLUE)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    ax.text(0, -1.25, 'Not drawn to scale', ha='center', fontsize=8, color='#4a4f78')
    _save(fig, path)
    return f'A {name} with its interior angles labelled ' + ', '.join(labels) + '. Not drawn to scale.'


def _ticks(ax, p, q, k, size=0.07):
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    for j in range(k):
        o = (j - (k - 1) / 2) * 0.06
        cx, cy = mx + ux * o, my + uy * o
        ax.plot([cx - nx * size, cx + nx * size], [cy - ny * size, cy + ny * size], color=INK, linewidth=1.6)


def congruent_triangles(path, names, side_labels, angle_labels):
    """Two congruent triangles, the second reflected and moved; matching sides carry 1, 2, 3 tick marks.
    names: ('ABC', 'DEF'); side_labels: {(tri, i): text} for side i (0 = first-second vertex, 1 = second-third, 2 = third-first);
    angle_labels: {(tri, i): text} at vertex i."""
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.set_aspect('equal'); ax.axis('off')
    T1 = [(0, 0), (2.2, 0), (0.6, 1.5)]
    T2 = [(5.4 - x, y) for x, y in T1]
    for t, (T, nm) in enumerate(((T1, names[0]), (T2, names[1]))):
        ax.add_patch(plt.Polygon(T, closed=True, facecolor='#eef3fb', edgecolor=INK, linewidth=2))
        cx, cy = sum(p[0] for p in T) / 3, sum(p[1] for p in T) / 3
        for i, (x, y) in enumerate(T):
            ax.text(x + (x - cx) * 0.18, y + (y - cy) * 0.22, nm[i], ha='center', va='center', fontsize=12, color=INK, fontweight='bold')
            if (t, i) in angle_labels:
                ax.text(x + (cx - x) * (0.68 if len(angle_labels[(t, i)]) > 5 else 0.5), y + (cy - y) * 0.5, angle_labels[(t, i)], ha='center', va='center', fontsize=9, color=BLUE)
        for i in range(3):
            p, q = T[i], T[(i + 1) % 3]
            _ticks(ax, p, q, i + 1)
            if (t, i) in side_labels:
                mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                ax.text(mx + (mx - cx) * 0.75, my + (my - cy) * 0.75, side_labels[(t, i)], ha='center', va='center', fontsize=10, color=BLUE)
    ax.set_xlim(-0.8, 6.2); ax.set_ylim(-0.5, 1.9)
    _save(fig, path)
    sides = '; '.join(f'{v} on side {names[t][i]}{names[t][(i + 1) % 3]}' for (t, i), v in side_labels.items())
    angs = '; '.join(f'{v} at {names[t][i]}' for (t, i), v in angle_labels.items())
    return (f'Two triangles, {names[0]} and the mirror-image {names[1]}. Matching sides have the same tick marks: '
            f'{names[0][0]}{names[0][1]} and {names[1][0]}{names[1][1]} one tick, {names[0][1]}{names[0][2]} and {names[1][1]}{names[1][2]} two ticks, '
            f'{names[0][2]}{names[0][0]} and {names[1][2]}{names[1][0]} three ticks.' + (f' Labels: {sides}.' if sides else '') + (f' Angles: {angs}.' if angs else ''))


def circle_fig(path, kind, label):
    """kind 'radius' or 'diameter': a circle with that segment labelled; 'semicircle': a semicircle with its diameter labelled;
    'quarter': a quarter circle with its radius labelled."""
    from matplotlib.patches import Circle, Wedge
    fig, ax = plt.subplots(figsize=(3.2, 3.0 if kind in ('radius', 'diameter') else 2.2))
    ax.set_aspect('equal'); ax.axis('off')
    if kind in ('radius', 'diameter'):
        ax.add_patch(Circle((0, 0), 1, facecolor='#eef3fb', edgecolor=INK, linewidth=2))
        ax.plot([0], [0], 'o', color=INK, markersize=4)
        x0 = -1 if kind == 'diameter' else 0
        ax.plot([x0, 1], [0, 0], color=BLUE, linewidth=2.2)
        ax.text((x0 + 1) / 2, 0.1, label, ha='center', va='bottom', fontsize=12, color=BLUE)
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
        alt = f'A circle with a {kind} drawn and labelled {label}.'
    elif kind == 'semicircle':
        ax.add_patch(Wedge((0, 0), 1, 0, 180, facecolor='#eef3fb', edgecolor=INK, linewidth=2))
        ax.text(0, -0.14, label, ha='center', va='top', fontsize=12, color=BLUE)
        ax.set_xlim(-1.2, 1.2); ax.set_ylim(-0.4, 1.15)
        alt = f'A semicircle whose straight side (the diameter) is labelled {label}.'
    else:
        ax.add_patch(Wedge((0, 0), 1, 0, 90, facecolor='#eef3fb', edgecolor=INK, linewidth=2))
        ax.plot([0.12, 0.12, 0], [0, 0.12, 0.12], color=INK, linewidth=1.2)
        ax.text(0.5, -0.1, label, ha='center', va='top', fontsize=12, color=BLUE)
        ax.set_xlim(-0.2, 1.2); ax.set_ylim(-0.35, 1.1)
        alt = f'A quarter circle; each straight side is a radius labelled {label}.'
    _save(fig, path)
    return alt


def floor_plan(path, w_label, h_label, scale, w=3.0, h=2.0, title='Room'):
    """A rectangle on a scale drawing with its two drawing lengths and the scale written under it."""
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(plt.Rectangle((0, 0), w, h, facecolor='#eef3fb', edgecolor=INK, linewidth=2.2))
    ax.text(w / 2, h / 2, title, ha='center', va='center', fontsize=12, color=INK)
    ax.text(w / 2, -0.15, w_label, ha='center', va='top', fontsize=11, color=BLUE)
    ax.text(w + 0.12, h / 2, h_label, ha='left', va='center', fontsize=11, color=BLUE)
    ax.text(w / 2, -0.62, f'Scale: {scale}', ha='center', va='top', fontsize=10.5, color=INK)
    ax.set_xlim(-0.3, w + 1.1); ax.set_ylim(-1.0, h + 0.25)
    _save(fig, path)
    return f'Scale drawing of a rectangular {title.lower()}: {w_label} long and {h_label} wide on the drawing. Scale: {scale}.'


def dot_plots(path, a, b, names, lo, hi, xlabel):
    """Two dot plots on the same number line, one above the other."""
    fig, axs = plt.subplots(2, 1, figsize=(5.2, 3.6), sharex=True)
    for ax, data, nm in zip(axs, (a, b), names):
        cnt = {}
        for v in data:
            cnt[v] = cnt.get(v, 0) + 1
            ax.plot([v], [cnt[v]], 'o', color=BLUE, markersize=7)
        ax.set_ylim(0.3, max(max(cnt.values()), 4) + 0.7); ax.set_yticks([])
        for s in ('top', 'right', 'left'):
            ax.spines[s].set_visible(False)
        ax.set_title(nm, loc='left', fontsize=10.5, color=INK)
        ax.set_xlim(lo - 0.5, hi + 0.5); ax.set_xticks(range(lo, hi + 1)); ax.tick_params(labelsize=9, colors=INK)
    axs[1].set_xlabel(xlabel, fontsize=10.5, color=INK)
    fig.tight_layout()
    _save(fig, path)
    fmt = lambda d: ', '.join(str(v) for v in sorted(d))
    return f'Two dot plots on the same scale ({xlabel}, {lo} to {hi}). {names[0]}: {fmt(a)}. {names[1]}: {fmt(b)}.'
