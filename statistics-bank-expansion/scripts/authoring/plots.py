"""Draw print-legible PNG figures for image diagrams (question-banks/assets/statistics/)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

OUT = None  # set by build script
DRAWN = []


def _save(fig, name):
    path = os.path.join(OUT, name + ".png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    DRAWN.append(name + ".png")
    return f"question-banks/assets/statistics/{name}.png"


def _style(ax, xlabel, ylabel=None, title=None):
    ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    if title:
        ax.set_title(title, fontsize=13)
    ax.tick_params(labelsize=11)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def dotplot(name, data, xlabel, title=None, xticks=None):
    fig, ax = plt.subplots(figsize=(7, 2.6))
    c = Counter(data)
    for v, k in c.items():
        ax.scatter([v] * k, range(1, k + 1), s=60, color="black")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    lo, hi = min(data), max(data)
    ax.set_xticks(xticks if xticks is not None else range(int(lo), int(hi) + 1))
    ax.set_ylim(0.3, max(c.values()) + 0.8)
    _style(ax, xlabel, title=title)
    return _save(fig, name)


def histogram(name, edges, counts, xlabel, title=None):
    fig, ax = plt.subplots(figsize=(7, 3.4))
    w = edges[1] - edges[0]
    ax.bar(edges[:-1], counts, width=w, align="edge", edgecolor="black", color="#cfd8e6")
    ax.set_xticks(edges)
    ax.set_yticks(range(0, max(counts) + 2))
    ax.grid(axis="y", color="#bbbbbb", linewidth=0.6)
    ax.set_axisbelow(True)
    _style(ax, xlabel, "Frequency", title)
    return _save(fig, name)


def boxplots(name, groups, xlabel, title=None):
    """groups: list of (label, (min,q1,med,q3,max), outliers)."""
    fig, ax = plt.subplots(figsize=(7, 1.2 + 0.9 * len(groups)))
    stats = []
    for lab, (mn, q1, m, q3, mx), outs in groups:
        stats.append({"label": lab, "whislo": mn, "q1": q1, "med": m, "q3": q3, "whishi": mx, "fliers": outs})
    ax.bxp(stats, vert=False, showfliers=True, widths=0.5,
           flierprops=dict(marker="*", markersize=10, markerfacecolor="black"), medianprops=dict(color="black", linewidth=2.5))
    ax.grid(axis="x", color="#bbbbbb", linewidth=0.6)
    _style(ax, xlabel, title=title)
    return _save(fig, name)


def scatter(name, x, y, xlabel, ylabel, title=None, line=None, hline0=False):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x, y, s=40, color="black")
    if line:
        a, b = line
        xs = [min(x), max(x)]
        ax.plot(xs, [a + b * v for v in xs], color="black", linewidth=1)
    if hline0:
        ax.axhline(0, color="black", linewidth=1)
    ax.grid(color="#cccccc", linewidth=0.6)
    _style(ax, xlabel, ylabel, title)
    return _save(fig, name)


def image(src, alt, caption=None):
    spec = {"src": src, "alt": alt}
    if caption:
        spec["caption"] = caption
    return {"type": "image", "spec": spec}
