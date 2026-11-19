"""Figures for Statistics audit #9 (2026-11-18, batch S2): experiment design diagrams and shaded standard Normal curves.
Drawn with matplotlib (Agg, no metadata) so a rebuild gives identical PNG files."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from scipy import stats

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
REL = 'question-banks/assets/statistics/audit'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})


def _box(ax, x, y, w, h, text, fc='#eef4fb'):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.02', fc=fc, ec='#1f4e79', lw=1.4))
    ax.text(x, y, text, ha='center', va='center', fontsize=10.5, wrap=True)


def _arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color='#1f4e79', lw=1.3))


def _save(fig, qid):
    os.makedirs(os.path.join(ROOT, REL), exist_ok=True)
    rel = f'{REL}/{qid}.png'
    fig.savefig(os.path.join(ROOT, rel), dpi=110, metadata={'Software': None}, facecolor='white')
    plt.close(fig)
    return rel


def design(qid, spec):
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    k = spec['kind']
    if k == 'crd':
        gs = spec['groups']
        _box(ax, 1.3, 3, 2.2, 1.1, f"{spec['total']} {spec['units']}")
        _box(ax, 3.7, 3, 1.6, 1.0, 'Random\nassignment', '#fff4e0')
        _arrow(ax, 2.4, 3, 2.9, 3)
        ys = np.linspace(5.1, 0.9, len(gs))
        for (t, n), y in zip(gs, ys):
            _arrow(ax, 4.5, 3, 5.4, y)
            _box(ax, 7.0, y, 3.0, 0.9, f'{t}\n{n} {spec["units"]}', '#e8f5e9')
        ax.text(9.3, 3, spec['response'], rotation=90, ha='center', va='center', fontsize=10)
        alt = (f"Design diagram: {spec['total']} {spec['units']} go to random assignment, which splits them into "
               + ', '.join(f'a group of {n} that gets {t}' for t, n in gs) + f". Then: {spec['response'].lower()}.")
    elif k == 'block':
        bl = spec['blocks']
        trts = spec['treatments']
        total = sum(n for _, n in bl)
        _box(ax, 1.0, 3, 1.7, 1.0, f"{total} {spec['units']}")
        ys = [4.6, 1.4]
        for (b, n), y in zip(bl, ys):
            _arrow(ax, 1.85, 3, 2.35, y)
            _box(ax, 3.3, y, 1.9, 0.9, f'Block: {b}\n({n})', '#fdecea')
            _box(ax, 5.35, y, 1.5, 0.8, 'Random\nassignment', '#fff4e0')
            _arrow(ax, 4.25, y, 4.6, y)
            for t, dy in zip(trts, [0.6, -0.6]):
                _arrow(ax, 6.1, y, 6.75, y + dy)
                _box(ax, 7.9, y + dy, 2.2, 0.6, f'{t} ({n // len(trts)})', '#e8f5e9')
        ax.text(9.6, 3, spec['response'], rotation=90, ha='center', va='center', fontsize=10)
        alt = (f"Design diagram: {total} {spec['units']} are first split into blocks ({', '.join(f'{b}, {n}' for b, n in bl)}); within each block they are randomly assigned to "
               + ' or '.join(trts) + f". Then: {spec['response'].lower()}.")
    else:
        trts = spec['treatments']
        _box(ax, 1.3, 3, 2.2, 1.0, f"{spec['n']} {spec['units']}")
        _box(ax, 3.9, 3, 2.0, 1.0, 'Each gets both\ntreatments', '#ffffff')
        _arrow(ax, 2.4, 3, 2.9, 3)
        _box(ax, 6.2, 3, 1.6, 1.0, 'Random\norder', '#fff4e0')
        _arrow(ax, 4.9, 3, 5.4, 3)
        _box(ax, 8.4, 4.2, 2.6, 0.7, f'{trts[0]} then {trts[1]}', '#e8f5e9')
        _box(ax, 8.4, 1.8, 2.6, 0.7, f'{trts[1]} then {trts[0]}', '#e8f5e9')
        _arrow(ax, 7.0, 3, 7.1, 4.2)
        _arrow(ax, 7.0, 3, 7.1, 1.8)
        ax.text(8.4, 0.6, spec['response'], ha='center', fontsize=10)
        alt = (f"Design diagram: {spec['n']} {spec['units']}; each receives both {trts[0]} and {trts[1]} in a random order. Then: {spec['response'].lower()}.")
    return {'type': 'image', 'spec': {'src': _save(fig, qid), 'alt': alt}}


def normal(qid, spec):
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    x = np.linspace(-3.6, 3.6, 721)
    y = stats.norm.pdf(x)
    ax.plot(x, y, color='#1f4e79', lw=1.8)
    a = spec['a']
    if spec['shade'] == 'right':
        m = x >= a
        ax.fill_between(x[m], y[m], color='#4f81bd', alpha=0.55)
        ax.axvline(a, color='#1f4e79', lw=1, ls='--')
    elif spec['shade'] == 'left':
        m = x <= a
        ax.fill_between(x[m], y[m], color='#4f81bd', alpha=0.55)
        ax.axvline(a, color='#1f4e79', lw=1, ls='--')
    else:
        for m in (x >= abs(a), x <= -abs(a)):
            ax.fill_between(x[m], y[m], color='#4f81bd', alpha=0.55)
        ax.axvline(abs(a), color='#1f4e79', lw=1, ls='--')
        ax.axvline(-abs(a), color='#1f4e79', lw=1, ls='--')
    ax.set_yticks([])
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    for s in ('left', 'right', 'top'):
        ax.spines[s].set_visible(False)
    ax.set_xlabel('z')
    ax.set_title(spec['label'], fontsize=11)
    side = {'right': f'to the right of z = {a:g}', 'left': f'to the left of z = {a:g}'.replace('-', '−'), 'both': f'in both tails, beyond z = ±{abs(a):g}'}[spec['shade']]
    alt = f'A standard Normal curve with the area {side} shaded.'
    return {'type': 'image', 'spec': {'src': _save(fig, qid), 'alt': alt}}
