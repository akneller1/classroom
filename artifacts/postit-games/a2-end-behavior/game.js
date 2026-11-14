PG.game({
  id: "a2-end-behavior", title: ["End Behavior", "Sort"], course: "Algebra 2", unit: "Polynomial Functions",
  tag: "Where do the ends of the graph go? Sort each polynomial.",
  skills: "F.IF.7c, A.APR.3 · degree and leading coefficient · end behavior · factored form · reading graphs",
  engine: "sort",
  levels: [
    "Standard form, leading term first.",
    "Standard form, terms scrambled (the leading term is hiding).",
    "Factored form: multiply the leading pieces in your head.",
    "Factored forms with powers and flipped factors like (3 − x), plus graphs."
  ],
  options: [{ id: "deal", label: "Cards", type: "one", choices: [["deal", "One at a time"], ["all", "All at once"]], default: "deal" }],
  round(c) {
    const { h } = c; const X = h.v("x"), M = h.MINUS;
    const term = (a, p, first) => { const s = a < 0 ? (first ? M : ` ${M} `) : (first ? "" : " + "); const A = Math.abs(a); const body = p === 0 ? String(A) : (A === 1 ? "" : A) + X + (p > 1 ? `<sup>${p}</sup>` : ""); return s + body; };
    const BINS = [{ id: "uu", label: "↖ … ↗", sub: "up left, up right" }, { id: "dd", label: "↙ … ↘", sub: "down left, down right" }, { id: "du", label: "↙ … ↗", sub: "down left, up right" }, { id: "ud", label: "↖ … ↘", sub: "up left, down right" }];
    const binOf = (deg, lead) => deg % 2 === 0 ? (lead > 0 ? "uu" : "dd") : (lead > 0 ? "du" : "ud");
    const why = (deg, lead) => `Degree ${deg} (${deg % 2 ? "odd: the ends go opposite ways" : "even: the ends go the same way"}), leading coefficient ${lead > 0 ? "positive" : "negative"}.`;
    const N = c.n(12), cards = [];
    let g = 0;
    while (cards.length < N && g++ < 400) {
      let html, deg, lead, cls = "mth", label;
      const kind = c.lvl <= 1 ? "std" : c.lvl === 2 ? "fac" : c.pick(["fac", "fac", "graph"]);
      if (kind === "std") {
        deg = c.ri(1, 6); lead = c.nz(-5, 5);
        const ts = [[lead, deg]]; for (let p = deg - 1; p >= 0; p--) if (c.chance(.5)) ts.push([c.nz(-9, 9), p]);
        const order = c.lvl === 1 ? c.shuffle(ts) : ts;
        if (c.lvl === 1 && order[0][1] === deg && order.length > 1) order.push(order.shift());
        html = `${h.v("f")}(${X}) = ` + order.map((t, i) => term(t[0], t[1], i === 0)).join("");
      } else if (kind === "fac") {
        const nf = c.ri(2, 3); let fs = [], k = c.pick([1, 1, 2, -1, -2, 3, -3]);
        for (let i = 0; i < nf; i++) { const r = c.nz(-5, 5), m = c.lvl === 3 ? c.pick([1, 1, 2, 3]) : 1, flip = c.lvl === 3 && c.chance(.35); fs.push({ r, m, flip }); }
        deg = fs.reduce((s, f) => s + f.m, 0); lead = k * fs.reduce((s, f) => s * (f.flip ? (-1) ** f.m : 1), 1);
        const fac = f => { const inner = f.flip ? `${Math.abs(f.r)} ${M} ${X}` : `${X} ${f.r > 0 ? M : "+"} ${Math.abs(f.r)}`; return `(${inner})${f.m > 1 ? `<sup>${f.m}</sup>` : ""}`; };
        html = `${h.v("f")}(${X}) = ${k === 1 ? "" : k === -1 ? M : k}${fs.map(fac).join("")}`;
        if (c.lvl === 3 && c.chance(.3)) { html = `${h.v("f")}(${X}) = ${k === 1 ? "" : k === -1 ? M : k}${X}${fs.map(fac).join("")}`; deg += 1; }
      } else {
        deg = c.ri(2, 5); lead = c.pick([1, -1]); const roots = Array.from({ length: deg }, () => c.ri(-3, 3) + c.r() * .6);
        const f = x => lead * roots.reduce((s, r) => s * (x - r), 1) / 4;
        html = PG.svg.graph(f, { xmin: -5, xmax: 5, ymin: -6, ymax: 6, size: 120, pad: 4, color: "#1d3a8f" }); cls = "pic";
        label = `graph that goes ${binOf(deg, lead) === "uu" ? "up on both ends" : binOf(deg, lead) === "dd" ? "down on both ends" : binOf(deg, lead) === "du" ? "down on the left and up on the right" : "up on the left and down on the right"}`;
        html = html.replace("<svg ", `<svg aria-label="${label}" `);
      }
      if (cards.some(x => x.html === html)) continue;
      cards.push({ html, cls, label, bin: binOf(deg, lead), why: kind === "graph" ? "Look at the far left and far right of the graph." : why(deg, lead) });
    }
    return { bins: BINS, cards, deal: c.opt.deal === "deal" };
  }
});
