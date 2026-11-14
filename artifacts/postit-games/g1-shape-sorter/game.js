PG.game({
  id: "g1-shape-sorter", title: ["Shape", "Sorter"], course: "Grade 1", unit: "Geometry: Shapes & Attributes",
  tag: "Sort shapes by sides, corners and other attributes.",
  skills: "1.G.1, 2.G.1 · defining attributes · sides and corners · turned shapes are the same shape",
  engine: "sort",
  levels: [
    "Sort by sides: 3 sides, 4 sides, or curved. Some shapes are turned or stretched.",
    "Sort by number of corners: 3, 4, 5 or 6.",
    "Venn diagram: 4 sides? All sides the same length? Both? Neither?",
    "Fast sort, one card at a time: has a square corner? more than 4 corners?"
  ],
  how: ["Look at each shape carefully. A turned square is still a square.", "Drag the shape to its box, or tap it and then tap the box. Number keys work too."],
  round(c) {
    const R = (x, y, a) => [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)];
    const regular = (n, a0 = 0) => Array.from({ length: n }, (_, i) => [Math.cos(a0 + i * 2 * Math.PI / n), Math.sin(a0 + i * 2 * Math.PI / n)]);
    const lens = p => p.map((q, i) => { const r = p[(i + 1) % p.length]; return Math.hypot(q[0] - r[0], q[1] - r[1]); });
    const hasRight = p => p.some((q, i) => { const a = p[(i + p.length - 1) % p.length], b = p[(i + 1) % p.length]; const u = [a[0] - q[0], a[1] - q[1]], v = [b[0] - q[0], b[1] - q[1]]; return Math.abs(u[0] * v[0] + u[1] * v[1]) / (Math.hypot(...u) * Math.hypot(...v)) < 0.02; });
    const nearRight = p => p.some((q, i) => { const a = p[(i + p.length - 1) % p.length], b = p[(i + 1) % p.length]; const u = [a[0] - q[0], a[1] - q[1]], v = [b[0] - q[0], b[1] - q[1]]; const cs = Math.abs(u[0] * v[0] + u[1] * v[1]) / (Math.hypot(...u) * Math.hypot(...v)); return cs >= 0.02 && cs < 0.22; });
    const draw = (pts, curved) => {
      const rot = c.r() * Math.PI * 2;
      let P = pts.map(([x, y]) => R(x, y, rot));
      const xs = P.map(p => p[0]), ys = P.map(p => p[1]);
      const mnx = Math.min(...xs), mxx = Math.max(...xs), mny = Math.min(...ys), mxy = Math.max(...ys);
      const sc = 78 / Math.max(mxx - mnx, mxy - mny);
      P = P.map(([x, y]) => [50 + (x - (mnx + mxx) / 2) * sc, 50 + (y - (mny + mxy) / 2) * sc]);
      return `<svg viewBox="0 0 100 100" width="76" height="76"><polygon points="${P.map(p => p.map(v => v.toFixed(1)).join(",")).join(" ")}" fill="#fff" stroke="#13202f" stroke-width="3" stroke-linejoin="round"/></svg>`;
    };
    const curvedSvg = kind => {
      const a = Math.round(c.r() * 360);
      if (kind === "circle") return `<svg viewBox="0 0 100 100" width="76" height="76"><circle cx="50" cy="50" r="38" fill="#fff" stroke="#13202f" stroke-width="3"/></svg>`;
      if (kind === "oval") return `<svg viewBox="0 0 100 100" width="76" height="76"><ellipse cx="50" cy="50" rx="42" ry="${c.ri(18, 28)}" transform="rotate(${a} 50 50)" fill="#fff" stroke="#13202f" stroke-width="3"/></svg>`;
      return `<svg viewBox="0 0 100 100" width="76" height="76"><path d="M12 62 A38 38 0 0 1 88 62 Z" transform="rotate(${a} 50 50)" fill="#fff" stroke="#13202f" stroke-width="3" stroke-linejoin="round"/></svg>`;
    };
    const jit = (p, j) => p.map(([x, y]) => [x + (c.r() - .5) * j, y + (c.r() - .5) * j]);
    const makers = {
      equilateral: () => ({ pts: regular(3), name: "triangle (all sides equal)" }),
      scalene: () => { const p = [[0, 0], [1 + c.r(), 0], [.3 + c.r() * .5, .6 + c.r() * .6]]; return { pts: p, name: "triangle" }; },
      rightTri: () => ({ pts: [[0, 0], [.6 + c.r(), 0], [0, .5 + c.r()]], name: "right triangle" }),
      square: () => ({ pts: [[0, 0], [1, 0], [1, 1], [0, 1]], name: "square" }),
      rect: () => { const h = c.pick([.35, .45, .55, .65]); return { pts: [[0, 0], [1, 0], [1, h], [0, h]], name: "rectangle" }; },
      rhombus: () => { const a = c.pick([50, 60, 65, 70]) * Math.PI / 180; return { pts: [[0, 0], [1, 0], [1 + Math.cos(a), Math.sin(a)], [Math.cos(a), Math.sin(a)]], name: "rhombus" }; },
      trapezoid: () => ({ pts: [[0, 0], [1.2, 0], [.85, .55], [.25, .55]], name: "trapezoid" }),
      quad: () => ({ pts: jit(regular(4, .3), .5), name: "4-sided shape" }),
      pentagon: () => ({ pts: regular(5), name: "pentagon (all sides equal)" }),
      oddPent: () => ({ pts: jit(regular(5, .2), .55), name: "5-sided shape" }),
      house: () => ({ pts: [[0, 0], [1, 0], [1, .7], [.5, 1.2], [0, .7]], name: "house shape (5 sides)" }),
      hexagon: () => ({ pts: regular(6), name: "hexagon (all sides equal)" }),
      oddHex: () => ({ pts: jit(regular(6, .1), .5), name: "6-sided shape" }),
      L: () => ({ pts: [[0, 0], [1, 0], [1, .4], [.4, .4], [.4, 1.1], [0, 1.1]], name: "L shape (6 sides)" })
    };
    const make = k => {
      if (["circle", "oval", "semi"].includes(k)) return { html: curvedSvg(k), cls: "pic", sides: k === "semi" ? 1 : 0, corners: k === "semi" ? 2 : 0, curved: true, equal: false, right: false, label: k === "semi" ? "half circle" : k };
      let m = makers[k](), tries = 0;
      while (tries++ < 30 && nearRight(m.pts)) m = makers[k]();
      const L = lens(m.pts); const eq = Math.max(...L) / Math.min(...L) < 1.03;
      return { html: draw(m.pts), cls: "pic", sides: m.pts.length, corners: m.pts.length, curved: false, equal: eq, right: hasRight(m.pts), label: m.name };
    };
    const N = c.n(12);
    const pickKinds = list => Array.from({ length: N }, (_, i) => list[i % list.length]);
    let bins, cards, venn = null, deal = false;
    if (c.lvl === 0) {
      bins = [{ id: "3", label: "3 sides" }, { id: "4", label: "4 sides" }, { id: "c", label: "Curved", sub: "has a curved side" }];
      cards = c.shuffle(pickKinds(c.shuffle(["equilateral", "scalene", "rightTri", "square", "rect", "rhombus", "trapezoid", "quad", "circle", "oval", "semi"]))).map(make);
      cards.forEach(s => { s.bin = s.curved ? "c" : String(s.sides); s.why = s.curved ? "This shape has a curved side." : `Count the straight sides: this shape has ${s.sides}.`; });
    } else if (c.lvl === 1) {
      bins = [3, 4, 5, 6].map(n => ({ id: String(n), label: n + " corners" }));
      cards = pickKinds(c.shuffle(["equilateral", "scalene", "rightTri", "square", "rect", "rhombus", "trapezoid", "quad", "pentagon", "oddPent", "house", "hexagon", "oddHex", "L"])).map(make);
      cards.forEach(s => { s.bin = String(s.corners); s.why = `Count the corners: this one has ${s.corners}.`; });
    } else {
      deal = c.lvl === 3;
      if (c.lvl === 2) {
        venn = { A: "4 sides", B: "All sides equal" };
        cards = pickKinds(c.shuffle(["square", "rhombus", "rect", "trapezoid", "quad", "equilateral", "pentagon", "hexagon", "scalene", "oddPent", "circle", "rightTri"])).map(make);
        cards.forEach(s => { const a = !s.curved && s.sides === 4, b = !s.curved && s.equal; s.bin = a && b ? "AB" : a ? "A" : b ? "B" : "N"; s.why = `This is a ${s.label}: ${a ? "it has 4 sides" : "it does not have 4 sides"} and ${b ? "all its sides are equal" : "its sides are not all equal"}.`; });
      } else {
        venn = { A: "Has a square corner", B: "More than 4 corners" };
        cards = pickKinds(c.shuffle(["square", "rect", "rightTri", "L", "house", "pentagon", "hexagon", "oddHex", "scalene", "rhombus", "trapezoid", "equilateral"])).map(make);
        cards.forEach(s => { const a = s.right, b = s.corners > 4; s.bin = a && b ? "AB" : a ? "A" : b ? "B" : "N"; s.why = `This ${s.label} ${a ? "has" : "has no"} square corner and ${b ? "more than 4" : s.corners} corners.`; });
      }
      bins = [];
    }
    return { bins, cards: c.shuffle(cards), venn, deal };
  }
});
