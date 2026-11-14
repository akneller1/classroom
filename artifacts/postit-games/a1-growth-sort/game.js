PG.game({
  id: "a1-growth-sort", title: ["Linear or", "Exponential?"], course: "Algebra 1", unit: "Exponential Functions",
  tag: "Sort tables, equations, graphs and stories by how they grow.",
  skills: "F.LE.1–2, F.IF.8b · equal differences vs equal ratios · growth and decay · percent change",
  engine: "sort",
  levels: [
    "Linear or exponential: tables and equations.",
    "A third box for neither (quadratics and others).",
    "Stories and graphs join in: “5% per year”, “$20 per month”.",
    "Four boxes: linear up, linear down, exponential growth, exponential decay."
  ],
  options: [{ id: "deal", label: "Cards", type: "one", choices: [["deal", "One at a time"], ["all", "All at once"]], default: "deal" }],
  round(c) {
    const { h } = c; const X = h.v("x"), Y = h.v("y"), F = h.fmt;
    const table = f => { const xs = [0, 1, 2, 3, 4]; return { html: `<table class="mt"><tr><th>${X}</th>${xs.map(x => `<td>${x}</td>`).join("")}</tr><tr><th>${Y}</th>${xs.map(x => `<td>${F(+f(x).toFixed(3))}</td>`).join("")}</tr></table>`, cls: "tab", label: "table: y values " + xs.map(x => F(+f(x).toFixed(3))).join(", ") }; };
    const graph = (f, lbl, ymin = -1, ymax = 12) => ({ html: PG.svg.graph(f, { xmin: -1, xmax: 6, ymin, ymax, size: 110, pad: 4, color: "#1d3a8f" }).replace("<svg ", `<svg aria-label="${lbl}" `), cls: "pic", label: lbl });
    const make = () => {
      const type = c.pick(c.lvl === 0 ? ["lin", "exp"] : ["lin", "exp", "exp", "lin", "nei"]);
      const up = c.chance(.6);
      const kinds = c.lvl <= 1 ? ["tab", "eq"] : ["tab", "eq", "story", "graph"];
      const kind = c.pick(kinds);
      let card;
      if (type === "lin") {
        const m = (up ? 1 : -1) * c.ri(2, 9), b = c.ri(up ? 1 : 30, up ? 20 : 60);
        if (kind === "tab") card = Object.assign(table(x => m * x + b), { why: `The y-values change by ${F(m)} each step: equal differences mean linear.` });
        else if (kind === "eq") card = { html: `${Y} = ${h.terms([[m, X], [b, ""]])}`, cls: "mth", why: "y = mx + b is linear." };
        else if (kind === "story") card = c.pick([{ html: `A savings account starts at $${b * 10} and ${up ? "grows" : "drops"} by $${Math.abs(m) * 5} each month`, cls: "txt" }, { html: `A candle is ${b} cm tall and ${up ? "(somehow) gains" : "loses"} ${Math.abs(m) / 2} cm per hour`, cls: "txt" }]);
        else card = graph(x => (m / 4) * x + (up ? 1 : 10), up ? "straight line going up" : "straight line going down");
        if (!card.why) card.why = "A constant amount added (or subtracted) each step is linear.";
      } else if (type === "exp") {
        const r = up ? c.pick([2, 3, 1.5, 1.1]) : c.pick([.5, .9, .8, 1 / 3]), a = up ? c.pick([1, 2, 3, 5, 10]) : c.pick([64, 81, 100, 160]);
        if (kind === "tab") card = Object.assign(table(x => a * r ** x), { why: `Each y is multiplied by ${F(+r.toFixed(3))}: equal ratios mean exponential.` });
        else if (kind === "eq") card = { html: `${Y} = ${a}(${r === 1 / 3 ? h.frac(1, 3) : F(r)})<sup>${X}</sup>`, cls: "mth", why: "The variable is in the exponent: exponential." };
        else if (kind === "story") { const p = Math.round(Math.abs(r - 1) * 100); card = c.pick([{ html: `A town of ${a * 1000} people ${up ? "grows" : "shrinks"} by ${p}% each year`, cls: "txt" }, { html: `A car worth $${a * 300} ${up ? "gains" : "loses"} ${p}% of its value every year`, cls: "txt" }, up ? { html: `A bacteria count doubles every hour`, cls: "txt" } : { html: `Half of a medicine leaves the body every 6 hours`, cls: "txt" }]); }
        else card = graph(up ? x => .6 * 1.8 ** x : x => 11 * .55 ** x, up ? "curve rising faster and faster" : "curve falling and leveling off toward zero");
        if (!card.why) card.why = "Multiplying by the same factor (a percent change) each step is exponential.";

      } else {
        const k = c.ri(1, 4);
        if (kind === "tab") card = Object.assign(table(x => k * x * x + 1), { why: "Differences aren't equal and ratios aren't equal: neither." });
        else if (kind === "eq") card = c.pick([{ html: `${Y} = ${k === 1 ? "" : k}${X}<sup>2</sup> + 1`, cls: "mth" }, { html: `${Y} = ${X}<sup>3</sup>`, cls: "mth" }, { html: `${Y} = ${h.frac(12, X)}`, cls: "mth" }]);
        else if (kind === "story") card = { html: "The area of a square as its side length grows", cls: "txt" };
        else card = graph(x => (x - 2.5) ** 2 + 1, "U-shaped curve");
        if (!card.why) card.why = "That's not a constant difference or a constant ratio: neither linear nor exponential.";
      }
      return Object.assign(card, { type, up });
    };
    const N = c.n(12), cards = [];
    let g = 0;
    while (cards.length < N && g++ < 400) { const cd = make(); if (c.lvl === 3 && cd.type === "nei") continue; if (cards.some(x => x.html === cd.html)) continue; cards.push(cd); }
    let bins;
    if (c.lvl === 0) bins = [{ id: "lin", label: "Linear" }, { id: "exp", label: "Exponential" }];
    else if (c.lvl < 3) bins = [{ id: "lin", label: "Linear" }, { id: "exp", label: "Exponential" }, { id: "nei", label: "Neither" }];
    else bins = [{ id: "lu", label: "Linear", sub: "increasing" }, { id: "ld", label: "Linear", sub: "decreasing" }, { id: "eg", label: "Exponential", sub: "growth" }, { id: "ed", label: "Exponential", sub: "decay" }];
    cards.forEach(cd => { cd.bin = c.lvl < 3 ? cd.type : (cd.type === "lin" ? (cd.up ? "lu" : "ld") : (cd.up ? "eg" : "ed")); });
    return { bins, cards, deal: c.opt.deal === "deal" };
  }
});
