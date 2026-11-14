PG.game({
  id: "g8-function-sort", title: ["Function", "or Not?"], course: "Grade 8", unit: "Functions",
  tag: "Does every input have exactly one output? Sort fast.",
  skills: "8.F.1, 8.F.3 · definition of a function · mapping diagrams · vertical line test · linear vs nonlinear",
  engine: "sort",
  levels: [
    "Sets of ordered pairs and tables.",
    "Mapping diagrams join in.",
    "Graphs and equations too: x = y², circles, vertical lines…",
    "Three boxes: linear function, nonlinear function, or not a function."
  ],
  options: [{ id: "deal", label: "Cards", type: "one", choices: [["deal", "One at a time"], ["all", "All at once"]], default: "deal" }],
  round(c) {
    const { h } = c; const X = h.v("x"), Y = h.v("y"), F = h.fmt;
    const rel = type => {
      const xs = c.sample([-3, -2, -1, 0, 1, 2, 3, 4, 5], 4).sort((a, b) => a - b);
      if (type === "lin") { const m = c.nz(-3, 3), b = c.ri(-4, 4); return { pts: xs.map(x => [x, m * x + b]), fn: true, lin: true }; }
      if (type === "non") { const f = c.pick([x => x * x, x => x * x - 2, x => Math.abs(x) * 2, x => 2 ** Math.abs(x)]); let pts = xs.map(x => [x, f(x)]); const ok = pts.length >= 3 && !pts.every((p, i) => i < 2 || (p[1] - pts[0][1]) * (pts[1][0] - pts[0][0]) === (pts[1][1] - pts[0][1]) * (p[0] - pts[0][0])); if (!ok) return rel("non"); return { pts, fn: true, lin: false }; }
      const m = c.nz(-2, 2), b = c.ri(-3, 3); const pts = xs.slice(0, 3).map(x => [x, m * x + b]); const dx = pts[c.ri(0, 2)][0]; let y2; do { y2 = c.ri(-6, 8); } while (pts.some(p => p[0] === dx && p[1] === y2)); pts.splice(c.ri(0, 3), 0, [dx, y2]); return { pts, fn: false, lin: false };
    };
    const asPairs = r => ({ html: "{" + r.pts.map(p => `(${F(p[0])}, ${F(p[1])})`).join(", ") + "}", cls: "txt" });
    const asTable = r => ({ html: `<table class="mt"><tr><th>${X}</th><th>${Y}</th></tr>${r.pts.map(p => `<tr><td>${F(p[0])}</td><td>${F(p[1])}</td></tr>`).join("")}</table>`, cls: "tab", label: "table: " + r.pts.map(p => `x ${p[0]}, y ${p[1]}`).join("; ") });
    const asMap = r => {
      const xs = [...new Set(r.pts.map(p => p[0]))], ys = [...new Set(r.pts.map(p => p[1]))].sort((a, b) => a - b);
      const H = Math.max(xs.length, ys.length) * 22 + 16;
      let s = `<svg viewBox="0 0 150 ${H}" width="150" aria-label="mapping diagram: ${r.pts.map(p => `${p[0]} to ${p[1]}`).join(", ")}"><ellipse cx="30" cy="${H / 2}" rx="24" ry="${H / 2 - 2}" fill="#fff" stroke="#13202f" stroke-width="1.4"/><ellipse cx="120" cy="${H / 2}" rx="24" ry="${H / 2 - 2}" fill="#fff" stroke="#13202f" stroke-width="1.4"/>`;
      const yx = i => H / 2 + (i - (xs.length - 1) / 2) * 22, yy = i => H / 2 + (i - (ys.length - 1) / 2) * 22;
      xs.forEach((x, i) => s += `<text x="30" y="${yx(i) + 4}" font-size="12" text-anchor="middle" fill="#13202f">${F(x)}</text>`);
      ys.forEach((y, i) => s += `<text x="120" y="${yy(i) + 4}" font-size="12" text-anchor="middle" fill="#13202f">${F(y)}</text>`);
      r.pts.forEach(([x, y]) => { const a = yx(xs.indexOf(x)), b = yy(ys.indexOf(y)); s += `<line x1="40" y1="${a}" x2="104" y2="${b}" stroke="#2f5bd3" stroke-width="1.5" marker-end="url(#ah)"/>`; });
      s = s.replace(`<ellipse`, `<defs><marker id="ah" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L6 3 L0 6z" fill="#2f5bd3"/></marker></defs><ellipse`);
      return { html: s + "</svg>", cls: "pic" };
    };
    const G = (fs, lbl) => ({ html: PG.svg.graph(fs, { xmin: -5, xmax: 5, ymin: -5, ymax: 5, size: 110, pad: 4, color: "#1d3a8f" }).replace("<svg ", `<svg aria-label="${lbl}" `), cls: "pic", label: lbl });
    const graphs = [
      () => { const m = c.pick([1, 2, -1, .5, -2]), b = c.ri(-2, 2); return Object.assign(G(x => m * x + b, "graph of a slanted line"), { fn: true, lin: true }); },
      () => Object.assign(G(x => .5 * x * x - 3, "graph of a U-shaped parabola"), { fn: true, lin: false }),
      () => Object.assign(G([{ draw: P => S2(P, t => [3 * Math.cos(t), 3 * Math.sin(t)]) }], "graph of a circle"), { fn: false, why: "A vertical line crosses the circle twice." }),
      () => Object.assign(G([{ draw: P => S2(P, t => [t * t / 2 - 3, t], -3.4, 3.4) }], "graph of a sideways parabola"), { fn: false, why: "A vertical line crosses it twice." }),
      () => Object.assign(G([{ draw: P => `<line x1="${P.X(2)}" x2="${P.X(2)}" y1="${P.Y(-5)}" y2="${P.Y(5)}" stroke="#1d3a8f" stroke-width="2.4"/>` }], "graph of a vertical line"), { fn: false, why: "x = 2 gives every y: one input, infinitely many outputs." }),
      () => Object.assign(G(x => 3, "graph of a horizontal line"), { fn: true, lin: true, why: "A horizontal line passes the vertical line test: every x has one y." }),
      () => Object.assign(G(x => .15 * x * x * x, "graph of an S-shaped cubic curve"), { fn: true, lin: false })
    ];
    function S2(P, f, t0 = 0, t1 = Math.PI * 2) { let d = ""; for (let i = 0; i <= 80; i++) { const t = t0 + (t1 - t0) * i / 80, [x, y] = f(t); d += (i ? "L" : "M") + P.X(x).toFixed(1) + " " + P.Y(y).toFixed(1); } return `<path d="${d}" fill="none" stroke="#1d3a8f" stroke-width="2.4"/>`; }
    const eqs = [
      [`${Y} = 2${X} + 1`, true, true], [`${Y} = ${X}<sup>2</sup>`, true, false], [`${X} = ${Y}<sup>2</sup>`, false, false, "For x = 4, y could be 2 or −2."], [`${X} = 3`, false, false, "x = 3 pairs one input with every y."],
      [`${Y} = |${X}|`, true, false], [`${X}<sup>2</sup> + ${Y}<sup>2</sup> = 9`, false, false, "That's a circle: some x-values have two y-values."], [`${Y} = ${h.MINUS}4`, true, true], [`${Y} = ${h.frac(1, 2)}${X} ${h.MINUS} 3`, true, true], [`${Y} = 2<sup>${X}</sup>`, true, false]
    ].map(([html, fn, lin, why]) => ({ html, cls: "mth", fn, lin, why }));
    const kinds = c.lvl === 0 ? ["pairs", "table"] : c.lvl === 1 ? ["pairs", "table", "map"] : ["pairs", "table", "map", "graph", "eq"];
    const N = c.n(12), cards = [];
    let g = 0;
    while (cards.length < N && g++ < 300) {
      const k = c.pick(kinds); let card;
      if (k === "graph") card = c.pick(graphs)();
      else if (k === "eq") card = Object.assign({}, c.pick(eqs));
      else { const r = rel(c.pick(c.lvl === 3 ? ["lin", "non", "not"] : ["lin", "non", "not", "not"])); card = Object.assign(k === "pairs" ? asPairs(r) : k === "table" ? asTable(r) : asMap(r), { fn: r.fn, lin: r.lin }); if (!r.fn) { const rep = r.pts.find((p, i) => r.pts.some((q, j) => j !== i && q[0] === p[0])); card.why = `The input ${F(rep[0])} has two different outputs.`; } }
      if (cards.some(x => x.html === card.html)) continue;
      cards.push(card);
    }
    let bins;
    if (c.lvl < 3) { bins = [{ id: "f", label: "Function" }, { id: "n", label: "Not a function" }]; cards.forEach(cd => { cd.bin = cd.fn ? "f" : "n"; if (cd.fn && !cd.why) cd.why = "Every input has exactly one output, so it IS a function."; }); }
    else { bins = [{ id: "l", label: "Linear function" }, { id: "nl", label: "Nonlinear function" }, { id: "n", label: "Not a function" }]; cards.forEach(cd => { cd.bin = !cd.fn ? "n" : cd.lin ? "l" : "nl"; if (cd.fn) cd.why = cd.lin ? "It's a function with a constant rate of change: linear." : "It's a function, but the rate of change isn't constant: nonlinear."; }); }
    return { bins, cards, deal: c.opt.deal === "deal" };
  }
});
