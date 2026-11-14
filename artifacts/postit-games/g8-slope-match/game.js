PG.game({
  id: "g8-slope-match", title: ["Slope", "Match"], course: "Grade 8", unit: "Linear Functions & Slope",
  tag: "Match each line to its slope or equation.",
  skills: "8.EE.5–6, 8.F.4 · slope as rise over run · negative and fractional slopes · y = mx + b from graphs, points and tables",
  engine: "match",
  levels: [
    "Graphs matched to slopes (positive, mostly whole numbers).",
    "Negative and fractional slopes.",
    "Graphs matched to equations. Some lines share a slope, some share an intercept.",
    "Two points or a table matched to an equation. No pictures!"
  ],
  options: [{ id: "style", label: "Play style", type: "one", choices: [["open", "Open cards"], ["memory", "Memory (face down)"]], default: "open" }],
  round(c) {
    const { h, Q } = c; const X = h.v("x"), Y = h.v("y"), F = h.fmt;
    const mHtml = q => h.f(q.n, q.d);
    const eqHtml = (q, b) => { const mm = q.d === 1 ? (q.n === 1 ? "" : q.n === -1 ? h.MINUS : F(q.n)) : (q.n < 0 ? h.MINUS : "") + h.frac(Math.abs(q.n), q.d); return `${Y} = ${mm}${X}` + (b ? ` ${b < 0 ? h.MINUS : "+"} ${Math.abs(b)}` : ""); };
    const graph = (q, b) => {
      const m = q.n / q.d;
      const s = PG.svg.graph([x => m * x + b], { xmin: -5, xmax: 5, ymin: -5, ymax: 5, size: 120, pad: 4, color: "#1d3a8f" });
      const P = PG.svg.plane({ xmin: -5, xmax: 5, ymin: -5, ymax: 5, size: 120, pad: 4 });
      let dots = ""; for (let x = -5; x <= 5; x++) { const y = m * x + b; if (Number.isInteger(y) && Math.abs(y) <= 5 && (x * q.d) % q.d === 0 && ((x * q.n) % q.d === 0)) dots += `<circle cx="${P.X(x)}" cy="${P.Y(y)}" r="2.6" fill="#1d3a8f"/>`; }
      return s.replace("</svg>", dots + "</svg>").replace("<svg ", `<svg aria-label="line through (0, ${b}) and (${q.d}, ${b + q.n})" `);
    };
    const slopes = c.lvl === 0 ? [[1, 1], [2, 1], [3, 1], [1, 2], [4, 1], [1, 3]] : [[-1, 1], [-2, 1], [2, 3], [-3, 4], [1, 2], [-1, 3], [3, 2], [-5, 2], [3, 1], [-4, 3], [1, 4]];
    const N = c.n(6), pairs = [], used = new Set();
    let g = 0;
    while (pairs.length < N && g++ < 600) {
      const [n, d] = c.pick(slopes), q = Q(n, d);
      let b = c.ri(-3, 3);
      if (Math.abs(q.n / q.d * 2 + b) > 5 && Math.abs(-q.n / q.d * 2 + b) > 5) continue;
      const key = c.lvl < 2 ? q.n + "/" + q.d : q.n + "/" + q.d + "|" + b;
      if (used.has(key)) continue;
      if (c.lvl === 2 && pairs.length && c.chance(.4)) { const p = c.pick(pairs); const [pn, pd] = p.q; const k2 = pn + "/" + pd + "|" + b; if (!used.has(k2) && b !== p.bi) { used.add(k2); pairs.push({ a: { html: graph(Q(pn, pd), b), cls: "pic", label: `line through (0, ${b}) and (${pd}, ${b + pn})` }, b: { html: eqHtml(Q(pn, pd), b), cls: "mth" }, q: [pn, pd], bi: b }); continue; } }
      used.add(key);
      if (c.lvl <= 1) pairs.push({ a: { html: graph(q, b), cls: "pic", label: `line through (0, ${b}) and (${q.d}, ${b + q.n})` }, b: { html: `<small style="font-family:var(--f-body);font-size:.7em">slope</small> ${mHtml(q)}`, cls: "mth", label: "slope " + q.n + " over " + q.d }, q: [q.n, q.d], bi: b });
      else if (c.lvl === 2) pairs.push({ a: { html: graph(q, b), cls: "pic", label: `line through (0, ${b}) and (${q.d}, ${b + q.n})` }, b: { html: eqHtml(q, b), cls: "mth" }, q: [q.n, q.d], bi: b });
      else {
        const x1 = c.ri(-4, 2) * q.d, x2 = x1 + q.d * c.ri(1, 2);
        const y = x => q.n * x / q.d + b;
        const a = c.chance(.5) ? { html: `through (${F(x1)}, ${F(y(x1))}) and (${F(x2)}, ${F(y(x2))})`, cls: "txt" }
          : { html: `<table class="mt"><tr><th>${X}</th>${[x1, x2, x2 + q.d].map(v => `<td>${F(v)}</td>`).join("")}</tr><tr><th>${Y}</th>${[x1, x2, x2 + q.d].map(v => `<td>${F(y(v))}</td>`).join("")}</tr></table>`, cls: "tab", label: `table x ${x1}, ${x2}, ${x2 + q.d}; y ${y(x1)}, ${y(x2)}, ${y(x2 + q.d)}` };
        pairs.push({ a, b: { html: eqHtml(q, b), cls: "mth" }, q: [q.n, q.d], bi: b });
      }
    }
    pairs.forEach(p => p.key = p.q.join("/") + (c.lvl >= 2 ? "|" + p.bi : ""));
    return { pairs, style: c.opt.style, aTitle: c.lvl === 3 ? "Points & tables" : "Graphs", bTitle: c.lvl < 2 ? "Slopes" : "Equations", cw: "150px",
      why: () => c.mode === "practice" ? "Slope = rise ÷ run. Going right, a line that goes down has a negative slope. b is where the line crosses the y-axis." : "Not a match." };
  }
});
