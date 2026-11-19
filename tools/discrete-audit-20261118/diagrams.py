"""Discrete Math audit #8 (2026-11-18): draw every graph that an item gives only as a list of vertices and edges.
Vertices sit on a circle; loops, parallel edges, arrows and edge weights are drawn as stated. Images go to
question-banks/assets/discrete/graphs-trees/drawn/<item id>.png and are attached as the item's diagram (the text list stays
in the prompt for screen readers and for checking). Run after the other batch C scripts."""
import os, re, sys, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items, ROOT

OUT = os.path.join(ROOT, 'question-banks/assets/discrete/graphs-trees/drawn')
os.makedirs(OUT, exist_ok=True)
INK = (31, 42, 68); S = 3; W = H = 320
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15 * S)
SMALL = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13 * S)


def parse(P):
    m = re.search(r'vertices ([A-Z](?:, [A-Z])*)(?:;| and) edges ([^.?]*)', P)
    if m:
        V = m.group(1).split(', '); body = m.group(2); E = []
        for tok in re.split(r',\s*(?:and\s+)?|\s+and\s+', body):
            tok = tok.strip()
            lp = re.match(r'a loop at ([A-Z])', tok)
            if lp: E.append((lp.group(1), lp.group(1), None)); continue
            e = re.match(r'([A-Z])([A-Z])(?: (\d+))?', tok)
            if e and e.group(1) in V and e.group(2) in V: E.append((e.group(1), e.group(2), e.group(3)))
        return V, E, False
    m = re.search(r'arrows ((?:[A-Z]→[A-Z](?:, )?)+)(?: and a loop at ([A-Z]))?', P) or re.search(r'Directed (?:graph|edges):? ((?:[A-Z]→[A-Z](?:, )?)+)', P)
    if m:
        E = [(a, b, None) for a, b in re.findall(r'([A-Z])→([A-Z])', m.group(1))]
        if m.lastindex and m.lastindex >= 2 and m.group(2): E.append((m.group(2), m.group(2), None))
        V = sorted({x for e in E for x in e[:2]})
        return V, E, True
    m = re.search(r'weights ((?:[A-Z]{2} \d+(?:, )?)+)', P)
    if m:
        E = [(a, b, w) for a, b, w in re.findall(r'([A-Z])([A-Z]) (\d+)', m.group(1))]
        V = sorted({x for e in E for x in e[:2]})
        return V, E, False
    return None


def draw(V, E, directed, path):
    img = Image.new('RGB', (W * S, H * S), 'white'); d = ImageDraw.Draw(img)
    cx, cy, R, r = W * S / 2, H * S / 2, 112 * S, 15 * S
    pos = {v: (cx + R * math.cos(-math.pi / 2 + 2 * math.pi * i / len(V)), cy + R * math.sin(-math.pi / 2 + 2 * math.pi * i / len(V))) for i, v in enumerate(V)}
    seen = {}
    for a, b, w in E:
        if a == b:
            x, y = pos[a]; ox, oy = (x - cx), (y - cy); L = math.hypot(ox, oy) or 1; ux, uy = ox / L, oy / L
            c = (x + ux * 24 * S, y + uy * 24 * S); d.ellipse([c[0] - 14 * S, c[1] - 14 * S, c[0] + 14 * S, c[1] + 14 * S], outline=INK, width=3 * S)
            continue
        k = tuple(sorted((a, b))); n = seen.get(k, 0); seen[k] = n + 1
        (x1, y1), (x2, y2) = pos[a], pos[b]
        bend = (0 if n == 0 else (1 if n % 2 else -1) * 44 * S * ((n + 1) // 2))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2; L = math.hypot(x2 - x1, y2 - y1); nx, ny = -(y2 - y1) / L, (x2 - x1) / L
        ctrl = (mx + nx * bend, my + ny * bend)
        pts = [((1 - t) ** 2 * x1 + 2 * (1 - t) * t * ctrl[0] + t * t * x2, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * ctrl[1] + t * t * y2) for t in [i / 30 for i in range(31)]]
        d.line(pts, fill=INK, width=3 * S)
        if directed:
            # arrowhead where the curve meets the target circle
            for i in range(len(pts) - 1, 0, -1):
                if math.hypot(pts[i][0] - x2, pts[i][1] - y2) > r + 2 * S: break
            tx, ty = pts[i]; px, py = pts[i - 1]; ang = math.atan2(ty - py, tx - px)
            hl = 13 * S; d.polygon([(tx, ty), (tx - hl * math.cos(ang - .4), ty - hl * math.sin(ang - .4)), (tx - hl * math.cos(ang + .4), ty - hl * math.sin(ang + .4))], fill=INK)
        if w:
            lx, ly = (mx + nx * (bend / 2 + 14 * S), my + ny * (bend / 2 + 14 * S))
            tw = d.textlength(w, font=SMALL); d.rectangle([lx - tw / 2 - 3 * S, ly - 9 * S, lx + tw / 2 + 3 * S, ly + 9 * S], fill='white')
            d.text((lx, ly), w, font=SMALL, fill=INK, anchor='mm')
    for v, (x, y) in pos.items():
        d.ellipse([x - r, y - r, x + r, y + r], fill='white', outline=INK, width=3 * S)
        d.text((x, y), v, font=FONT, fill=INK, anchor='mm')
    img.resize((W, H), Image.LANCZOS).convert('P', palette=Image.ADAPTIVE, colors=16).save(path, optimize=True)


def alt(V, E, directed):
    if directed:
        arr = ', '.join(f'{a}→{b}' for a, b, w in E if a != b); loops = [a for a, b, w in E if a == b]
        return f'Directed graph with vertices {", ".join(V)} and arrows {arr}' + (f' and a loop at {", ".join(loops)}' if loops else '') + '.'
    if any(w for _, _, w in E):
        return f'Weighted graph with vertices {", ".join(V)}: ' + ', '.join(f'{a}{b} {w}' for a, b, w in E) + '.'
    ed = ', '.join(f'{a}{b}' if a != b else f'loop at {a}' for a, b, w in E)
    return f'Undirected graph with vertices {", ".join(V)} and edges {ed}.'


B = load(); n = 0
for _, q in items(B):
    if q.get('diagram') or not q['skillId'].startswith('graphs-trees'):
        continue
    g = parse(q['prompt'])
    if not g or len(g[0]) < 2 or len(g[0]) > 9:
        continue
    V, E, directed = g
    f = os.path.join(OUT, q['id'] + '.png'); draw(V, E, directed, f)
    q['diagram'] = {'type': 'image', 'spec': {'src': os.path.relpath(f, ROOT).replace(os.sep, '/'), 'alt': alt(V, E, directed)}}
    n += 1
save(B)
print('drawn', n)
