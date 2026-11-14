PG.game({
  id: "g6-expression-groups", title: ["Equivalent Expression", "Groups"], course: "Grade 6", unit: "Expressions",
  tag: "Group the expressions that are equal for every value of the variable.",
  skills: "6.EE.3–4 · distributive property · combining like terms · factoring out a GCF",
  engine: "groups",
  levels: [
    "Three groups of three: combining like terms.",
    "Four groups of four: the distributive property.",
    "Factoring out common factors: 12x + 18 = 6(2x + 3) = 3(4x + 6).",
    "Look-alike groups with subtraction: 3(x − 4), 3x − 4, 3(x + 4)…"
  ],
  round(c) {
    const { h } = c;
    const v = c.pick(["x", "n", "y", "a"]);
    const V = h.v(v);
    const lin = (a, b) => h.terms([[a, V], [b, ""]]);
    const linR = (a, b) => h.terms([[b, ""], [a, V]]);
    const forms = (a, b) => {
      const out = new Set();
      out.add(lin(a, b)); if (b) out.add(linR(a, b));
      for (let g = 2; g <= 12; g++) if (a % g === 0 && b % g === 0 && b !== 0) { out.add(`${g}(${lin(a / g, b / g)})`); if (c.lvl === 3) out.add(`${g}(${linR(a / g, b / g)})`); }
      if (a >= 2 && a <= 4) out.add(Array(a).fill(V).join(" + ") + (b ? (b > 0 ? " + " : " " + h.MINUS + " ") + Math.abs(b) : ""));
      const k = c.ri(1, Math.max(1, a - 1)); if (a > 1) out.add(h.terms([[a - k, V], [b, ""], [k, V]]));
      if (b) { const m = c.ri(1, 6); out.add(h.terms([[a, V], [b - m, ""], [m, ""]])); }
      if (a > 2) out.add(h.terms([[a + 1, V], [b, ""], [-1, V]]));
      return [...out];
    };
    let specs;
    if (c.lvl === 0) specs = c.distinct(3, () => [c.ri(2, 5), c.ri(0, 1) ? c.ri(1, 9) : 0], x => x.join());
    else if (c.lvl === 1) specs = c.distinct(4, () => { const g = c.ri(2, 6), p = c.ri(1, 4), q = c.ri(1, 7); return [g * p, g * q]; }, x => x.join());
    else if (c.lvl === 2) specs = c.distinct(4, () => { const g = c.pick([4, 6, 8, 12]), p = c.ri(1, 3), q = c.ri(1, 5); return [g * p, g * q]; }, x => x.join());
    else { const a = c.ri(2, 5), b = c.ri(3, 6); specs = c.shuffle([[a, -a * b], [a, -b], [a, a * b], [a, b - a]]).filter((x, i, arr) => arr.findIndex(y => y.join() === x.join()) === i); while (specs.length < 4) { const s2 = [c.ri(2, 6), -c.ri(2, 20)]; if (!specs.some(y => y.join() === s2.join())) specs.push(s2); } }
    const size = c.lvl === 0 ? 3 : 4;
    const used = new Set();
    const groups = specs.map(([a, b]) => {
      let fs = c.shuffle(forms(a, b)).filter(f => !used.has(f));
      if (c.lvl >= 1) { const fac = fs.filter(f => f.includes("(")); const rest = fs.filter(f => !f.includes("(")); fs = fac.slice(0, 2).concat(rest); }
      const items = fs.slice(0, size); items.forEach(f => used.add(f));
      return { label: lin(a, b).replace(/<[^>]+>/g, ""), items: items.map(f => ({ html: f, cls: "mth" })), say: `Every card in that group simplifies to ${PG.textify(lin(a, b))}.` };
    });
    if (groups.some(g => g.items.length < size)) return this.round(c);
    return { groups, cw: "180px" };
  }
});
