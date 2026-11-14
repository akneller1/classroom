PG.game({
  id: "a2-transform-match", title: ["Transformation", "Match"], course: "Algebra 2", unit: "Functions & Transformations",
  tag: "Match each transformed function to its graph or description.",
  skills: "F.BF.3, F.IF.7 · shifts, reflections and stretches of x², |x|, √x, x³ and 2ˣ · inside vs outside changes",
  engine: "match",
  levels: [
    "Shifts only: y = f(x − h) + k.",
    "Reflections join the shifts.",
    "Stretches and compressions too, across all five parent functions.",
    "No graphs: match equations to words. Inside changes go the opposite way!"
  ],
  options: [{ id: "style", label: "Play style", type: "one", choices: [["open", "Open cards"], ["memory", "Memory (face down)"]], default: "open" }],
  round(c) {
    const { h } = c; const X = h.v("x"), Y = h.v("y"), M = h.MINUS;
    const parents = {
      sq: { f: x => x * x, name: "x²", wrap: s => `(${s})<sup>2</sup>` },
      ab: { f: x => Math.abs(x), name: "|x|", wrap: s => `|${s}|` },
      rt: { f: x => (x < 0 ? NaN : Math.sqrt(x)), name: "√x", wrap: s => h.sqrt(s) },
      cu: { f: x => x * x * x, name: "x³", wrap: s => `(${s})<sup>3</sup>` },
      ex: { f: x => 2 ** x, name: "2ˣ", wrap: s => `2<sup>${s}</sup>` }
    };
    const inner = hh => hh === 0 ? X : `${X} ${hh > 0 ? M : "+"} ${Math.abs(hh)}`;
    const aStr = a => a === 1 ? "" : a === -1 ? M : a === .5 ? h.frac(1, 2) : a === -.5 ? M + h.frac(1, 2) : h.fmt(a);
    const eq = (p, a, hh, k) => { let w = parents[p].wrap(inner(hh)); if (p === "ex" && hh === 0) w = `2<sup>${X}</sup>`; if (p === "sq" && hh === 0) w = `${X}<sup>2</sup>`; if (p === "cu" && hh === 0) w = `${X}<sup>3</sup>`; return `${Y} = ${aStr(a)}${w}${k ? ` ${k < 0 ? M : "+"} ${Math.abs(k)}` : ""}`; };
    const words = (p, a, hh, k) => { const parts = []; if (hh) parts.push(`${hh > 0 ? "right" : "left"} ${Math.abs(hh)}`); if (a < 0) parts.push("reflect over the x-axis"); if (Math.abs(a) === 2) parts.push("vertical stretch by 2"); if (Math.abs(a) === .5) parts.push("vertical shrink by ½"); if (k) parts.push(`${k > 0 ? "up" : "down"} ${Math.abs(k)}`); return `${parents[p].name}: ${parts.join(", ") || "no change"}`; };
    const graph = (p, a, hh, k) => PG.svg.graph(x => a * parents[p].f(x - hh) + k, { xmin: -6, xmax: 6, ymin: -6, ymax: 6, size: 130, pad: 4, color: "#1d3a8f" }).replace("<svg ", `<svg aria-label="graph of ${PG.textify(words(p, a, hh, k))}" `);
    const keys = c.lvl === 0 ? c.sample(["sq", "ab", "rt", "cu", "ex"], 2) : Object.keys(parents);
    const N = c.n(6), pairs = [], used = new Set();
    let g = 0;
    while (pairs.length < N && g++ < 800) {
      const p = c.pick(keys);
      const a = c.lvl === 0 ? 1 : c.lvl === 1 ? c.pick([1, -1]) : c.pick([1, -1, 2, -2, .5, -.5]);
      const hh = c.ri(-3, 3), k = c.ri(-3, 3);
      if (!hh && !k && a === 1) continue;
      const key = [p, a, hh, k].join();
      if (used.has(key)) continue;
      if (c.lvl < 3 && [...used].some(u => { const [p2, a2, h2, k2] = u.split(","); return p2 === p && +h2 === hh && +k2 === k; })) continue;
      used.add(key);
      const A = { html: eq(p, a, hh, k), cls: "mth" };
      const B = c.lvl < 3 ? { html: graph(p, a, hh, k), cls: "pic", label: "graph: " + PG.textify(words(p, a, hh, k)) } : { html: words(p, a, hh, k), cls: "txt" };
      pairs.push({ a: A, b: B, key, say: c.lvl < 3 ? words(p, a, hh, k) : null });
    }
    // Expert traps: add a description that swaps left/right for one pair
    const extraB = [];
    if (c.lvl === 3) { const p0 = pairs.find(p => /right|left/.test(p.b.html)); if (p0) extraB.push({ html: p0.b.html.replace(/right|left/, m => m === "right" ? "left" : "right"), cls: "txt", key: "trap" }); }
    return { pairs, extraB, style: c.opt.style, aTitle: "Equations", bTitle: c.lvl < 3 ? "Graphs" : "Descriptions", cw: "150px",
      why: () => c.mode === "practice" ? "Changes inside the function move it sideways in the OPPOSITE direction: (x − 2) moves right. Outside changes move it up/down and stretch or flip it." : "Not a match." };
  }
});
