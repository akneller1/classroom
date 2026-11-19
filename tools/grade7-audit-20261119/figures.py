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
