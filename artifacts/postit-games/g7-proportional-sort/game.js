PG.game({
  id: "g7-proportional-sort", title: ["Proportional", "or Not?"], course: "Grade 7", unit: "Proportional Relationships",
  tag: "Is it a proportional relationship? Sort equations, tables, graphs and stories.",
  skills: "7.RP.2 · constant of proportionality · y = kx · graphs through the origin · tables with a constant ratio",
  engine: "sort",
  levels: [
    "Equations and tables.",
    "Graphs join in: straight AND through the origin?",
    "Stories too, plus tables that look proportional but aren't.",
    "Find k: sort into k > 1, 0 < k < 1, or not proportional."
  ],
  options: [{ id: "deal", label: "Cards", type: "one", choices: [["deal", "One at a time"], ["all", "All at once"]], default: "deal" }],
  round(c) {
    const { h } = c;
    const X = h.v("x"), Y = h.v("y");
    const kHtml = k => Number.isInteger(k) ? String(k) : k === .5 ? h.frac(1, 2) : k === .25 ? h.frac(1, 4) : k === .75 ? h.frac(3, 4) : k === 1.5 ? h.frac(3, 2) : k === 2.5 ? h.frac(5, 2) : String(k);
    const table = (xs, f) => `<table class="mt"><tr><th>${X}</th>${xs.map(x => `<td>${h.fmt(x)}</td>`).join("")}</tr><tr><th>${Y}</th>${xs.map(x => `<td>${h.fmt(+f(x).toFixed(2))}</td>`).join("")}</tr></table>`;
    const graph = (f, lbl) => ({ html: PG.svg.graph(f, { xmin: 0, xmax: 6, ymin: 0, ymax: 6, size: 110, pad: 6, color: "#1d3a8f" }).replace("<svg ", `<svg aria-label="${lbl}" `), cls: "pic", label: lbl });
    const ks = [2, 3, 4, 5, 1.5, 2.5, .5, .25, .75];
    const make = () => {
      const k = c.pick(ks), b = c.nz(1, 6), kind = c.pick(c.lvl === 0 ? ["eq", "tab"] : c.lvl === 1 ? ["eq", "tab", "gr"] : ["eq", "tab", "gr", "story"]);
      const prop = c.chance(.5);
      let card;
      if (kind === "eq") {
        if (prop) card = { html: `${Y} = ${k === 1 ? "" : kHtml(k)}${X}`, cls: "mth" };
        else card = c.pick([{ html: `${Y} = ${kHtml(k)}${X} + ${b}`, cls: "mth", why: `The “+ ${b}” means y isn't 0 when x is 0.` }, { html: `${Y} = ${X}<sup>2</sup>`, cls: "mth", why: "y = x² isn't a straight line, so the ratio y/x keeps changing." }, { html: `${X}${Y} = ${b * 6}`, cls: "mth", why: "When x goes up, y goes down: that's inverse, not proportional." }, { html: `${Y} = ${b + 2}`, cls: "mth", why: "y never changes, so y/x isn't constant." }]);
      } else if (kind === "tab") {
        const start = c.ri(1, 3), xs = [start, start + c.ri(1, 2), start + c.ri(3, 4), start + c.ri(5, 7)];
        if (prop) card = { html: table(xs, x => k * x), cls: "tab", label: "table" };
        else { const tr = c.lvl >= 2 ? c.ri(0, 1) : 0; card = tr ? { html: table(xs, x => x * x), cls: "tab", label: "table", why: "Check y ÷ x for each column: it changes." } : { html: table(xs, x => k * x + b), cls: "tab", label: "table", why: `Check y ÷ x: it isn't the same in every column (the pattern has a +${b}).` }; }
      } else if (kind === "gr") {
        if (prop) card = graph(x => k * x, `straight line through the origin and the point (2, ${h.fmt(2 * k)})`);
        else card = c.pick([Object.assign(graph(x => k * x + b, "straight line that crosses the y-axis above 0"), { why: "Straight, but it doesn't go through the origin (0, 0)." }), Object.assign(graph(x => .3 * x * x, "curve through the origin"), { why: "It goes through (0, 0) but isn't a straight line." })]);
      } else {
        const p = c.ri(2, 9);
        if (prop) card = { html: c.pick([`Total cost for tickets at $${p} each`, `Miles driven at ${p * 10} miles per hour`, `Pay for hours worked at $${p + 10} per hour`, `Cups of flour: ${p} cups per batch`]), cls: "txt" };
        else card = c.pick([{ html: `A taxi charges $${p} plus $2 per mile`, cls: "txt", why: `The $${p} starting fee means 0 miles still costs money.` }, { html: `A gym costs $${p * 5} to join and $${p} per visit`, cls: "txt", why: "The joining fee breaks the constant ratio." }, { html: `A plant is ${p} cm tall and grows 2 cm per week`, cls: "txt", why: `It starts at ${p} cm, not 0.` }]);
      }
      card.prop = prop; card.k = prop && kind !== "story" ? k : null; card.kind = kind;
      return card;
    };
    const N = c.n(12);
    let cards = [], g = 0;
    while (cards.length < N && g++ < 400) { const cd = make(); if (c.lvl === 3 && cd.prop && cd.k == null) continue; if (cards.some(x => x.html === cd.html)) continue; cards.push(cd); }
    let bins;
    if (c.lvl < 3) { bins = [{ id: "p", label: "Proportional" }, { id: "n", label: "Not proportional" }]; cards.forEach(cd => { cd.bin = cd.prop ? "p" : "n"; if (cd.prop) cd.why = "y ÷ x is the same every time, and the graph is a straight line through (0, 0)."; }); }
    else { bins = [{ id: "big", label: "Proportional", sub: "k > 1" }, { id: "small", label: "Proportional", sub: "0 < k < 1" }, { id: "n", label: "Not proportional" }]; cards.forEach(cd => { cd.bin = !cd.prop ? "n" : cd.k > 1 ? "big" : "small"; if (cd.prop) cd.why = `The constant of proportionality is k = ${cd.k}.`; }); }
    return { bins, cards, deal: c.opt.deal === "deal" };
  }
});
