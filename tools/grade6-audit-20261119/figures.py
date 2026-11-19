"""Grade 6 audit (2026-11-19): figures for the new Grade 6 items, drawn to match the existing middle-grades diagrams
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



def tape_diagram(path, labels, parts, total=None, unit_label=None):
    """One bar per quantity, each split into equal unit boxes (parts[i] boxes), lined up so a box is the same size in every bar."""
    n = max(parts)
    fig, ax = plt.subplots(figsize=(1.6 + 0.5 * n, 0.9 + 0.62 * len(parts)))
    ax.set_aspect('equal'); ax.axis('off')
    for i, (lab, k) in enumerate(zip(labels, parts)):
        y = (len(parts) - 1 - i) * 1.25
        ax.text(-0.2, y + 0.4, lab, ha='right', va='center', fontsize=11, color=INK)
        for j in range(k):
            ax.add_patch(plt.Rectangle((j, y), 1, 0.8, facecolor=FILL if i == 0 else '#f3e3c3', edgecolor=INK, linewidth=1.6))
            if unit_label:
                ax.text(j + 0.5, y + 0.4, unit_label, ha='center', va='center', fontsize=9, color=BLUE)
    if total:
        top = (len(parts) - 1) * 1.25 + 0.8
        ax.annotate('', xy=(n + 0.55, -0.05), xytext=(n + 0.55, top + 0.05), arrowprops=dict(arrowstyle='<->', color=BLUE, linewidth=1.4))
        ax.text(n + 0.75, top / 2, total, ha='left', va='center', fontsize=11, color=BLUE)
    ax.set_xlim(-2.2, n + 2.6); ax.set_ylim(-0.3, (len(parts) - 1) * 1.25 + 1.1)
    _save(fig, path)
    bars = '; '.join(f'{lab}: {k} equal boxes' for lab, k in zip(labels, parts))
    return f'Tape diagram. {bars}.' + (f' Each box is labelled {unit_label}.' if unit_label else '') + (f' A bracket shows a total of {total}.' if total else '')


def double_number_line(path, top_label, top, bottom_label, bottom):
    """Two number lines with matching tick marks; values are strings and may be '?'."""
    n = len(top)
    fig, ax = plt.subplots(figsize=(1.2 + 0.95 * n, 1.9))
    ax.axis('off')
    for y, vals in ((1.0, top), (0.0, bottom)):
        ax.plot([-0.3, n - 0.4], [y, y], color=INK, linewidth=1.8)
        for i, v in enumerate(vals):
            ax.plot([i, i], [y - 0.09, y + 0.09], color=INK, linewidth=1.6)
            ax.text(i, y + (0.2 if y == 1.0 else -0.2), v, ha='center', va='bottom' if y == 1.0 else 'top', fontsize=11, color=BLUE if v == '?' else INK, fontweight='bold' if v == '?' else 'normal')
    ax.text(-0.45, 1.0, top_label, ha='right', va='center', fontsize=10.5, color=INK)
    ax.text(-0.45, 0.0, bottom_label, ha='right', va='center', fontsize=10.5, color=INK)
    ax.set_xlim(-2.2, n); ax.set_ylim(-0.6, 1.6)
    _save(fig, path)
    return f'Double number line. {top_label}: {", ".join(top)}. {bottom_label}: {", ".join(bottom)}. Values in the same position match.'


def fraction_bars(path, wholes, denom, shaded, group):
    """Fraction-division model: `wholes` bars each split into `denom` parts; the first `shaded` parts are shaded and outlined
    in groups of `group` parts."""
    fig, ax = plt.subplots(figsize=(1.0 + 1.6 * wholes, 1.6))
    ax.set_aspect('auto'); ax.axis('off')
    W = 1.5
    for b in range(wholes):
        for j in range(denom):
            k = b * denom + j
            ax.add_patch(plt.Rectangle((b * (W + 0.15) + j * W / denom, 0), W / denom, 0.6, facecolor=FILL if k < shaded else 'white', edgecolor=INK, linewidth=1.2))
        ax.text(b * (W + 0.15) + W / 2, 0.75, '1 whole', ha='center', fontsize=9.5, color=INK)
    k, gi = 0, 0
    while k + group <= shaded:
        x0 = (k // denom) * (W + 0.15) + (k % denom) * W / denom
        x1 = ((k + group - 1) // denom) * (W + 0.15) + ((k + group - 1) % denom + 1) * W / denom
        ax.plot([x0, x0, x1, x1], [-0.05, -0.18, -0.18, -0.05], color=BLUE, linewidth=1.6)
        gi += 1; k += group
    ax.set_xlim(-0.1, wholes * (W + 0.15)); ax.set_ylim(-0.35, 0.95)
    _save(fig, path)
    return (f'Fraction model: {wholes} whole bar{"s" if wholes > 1 else ""}, each cut into {denom} equal parts. {shaded} parts are shaded, and brackets '
            f'under the shaded parts mark {gi} group{"s" if gi != 1 else ""} of {group} part{"s" if group > 1 else ""}' + (f' with {shaded - gi * group} part{"s" if shaded - gi * group != 1 else ""} left over.' if shaded - gi * group else '.'))


def prism_net(path, l, w, h, unit):
    """Net of a rectangular prism (cross shape) with the three dimensions labelled."""
    fig, ax = plt.subplots(figsize=(4.6, 3.8))
    ax.set_aspect('equal'); ax.axis('off')
    L, W, H = float(l), float(w), float(h)
    rects = [(H, 0, L, W), (H, W, L, H), (H, W + H, L, W), (H, 2 * W + H, L, H), (0, W, H, H), (H + L, W, H, H)]
    for x, y, a, b in rects:
        ax.add_patch(plt.Rectangle((x, y), a, b, facecolor='#eef3fb', edgecolor=INK, linewidth=1.8))
    ax.text(H + L / 2, -0.25 * max(L, W, H) / 4, f'{l} {unit}', ha='center', va='top', fontsize=10.5, color=BLUE)
    ax.text(H + L + 0.08, W / 2, f'{w} {unit}', ha='left', va='center', fontsize=10.5, color=BLUE)
    ax.text(H + L + H / 2, W + H + 0.08, f'{h} {unit}', ha='center', va='bottom', fontsize=10.5, color=BLUE)
    ax.set_xlim(-0.3, 2 * H + L + 0.8); ax.set_ylim(-0.6, 2 * W + 2 * H + 0.3)
    _save(fig, path)
    return f'Net of a rectangular prism: six rectangles in a cross shape. Labels: length {l} {unit}, width {w} {unit}, height {h} {unit}.'


def coord_polygon(path, pts, names, lo=-6, hi=6):
    """A polygon on a coordinate grid with labelled vertices."""
    fig, ax = plt.subplots(figsize=(4.0, 4.0))
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect('equal')
    ax.set_xticks(range(lo, hi + 1)); ax.set_yticks(range(lo, hi + 1))
    ax.grid(True, color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    ax.axhline(0, color=INK, linewidth=1.2); ax.axvline(0, color=INK, linewidth=1.2)
    ax.tick_params(labelsize=7.5, colors=INK)
    ax.add_patch(plt.Polygon(pts, closed=True, facecolor=FILL, edgecolor=BLUE, linewidth=2.2, alpha=0.8))
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    for (x, y), nm in zip(pts, names):
        ax.plot([x], [y], 'o', color=INK, markersize=5)
        ax.text(x + (0.35 if x >= cx else -0.35), y + (0.35 if y >= cy else -0.45), nm, ha='center', va='center', fontsize=11, color=INK, fontweight='bold')
    _save(fig, path)
    return f'Coordinate grid from {lo} to {hi} on both axes with polygon ' + ''.join(names) + ': ' + ', '.join(f'{nm}({x}, {y})' for (x, y), nm in zip(pts, names)) + '.'


def dot_plot(path, data, lo, hi, xlabel):
    fig, ax = plt.subplots(figsize=(5.0, 2.2))
    cnt = {}
    for v in data:
        cnt[v] = cnt.get(v, 0) + 1
        ax.plot([v], [cnt[v]], 'o', color=BLUE, markersize=8)
    ax.set_ylim(0.3, max(max(cnt.values()), 3) + 0.7); ax.set_yticks([])
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.set_xlim(lo - 0.5, hi + 0.5); ax.set_xticks(range(lo, hi + 1)); ax.tick_params(labelsize=9, colors=INK)
    ax.set_xlabel(xlabel, fontsize=10.5, color=INK)
    _save(fig, path)
    return f'Dot plot of {xlabel} from {lo} to {hi}. Values: ' + ', '.join(str(v) for v in sorted(data)) + '.'
