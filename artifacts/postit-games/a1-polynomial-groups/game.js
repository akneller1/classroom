PG.game({
  id: "a1-polynomial-groups", title: ["Polynomial", "Groups"], course: "Algebra 1", unit: "Polynomials",
  tag: "Find the groups of expressions that are the same polynomial in disguise.",
  skills: "A.APR.1, A.SSE.2 · combining like terms · adding and subtracting polynomials · multiplying binomials",
  engine: "groups",
  levels: [
    "Three groups of three: combine like terms.",
    "Four groups of four: adding and subtracting polynomials.",
    "Products of binomials: (x + 3)(x − 2) = x² + x − 6 = x(x − 2) + 3(x − 2).",
    "Look-alikes: (x + 3)(x − 2), (x − 3)(x + 2), (x + 3)(x + 2)… and squares."
  ],
  round(c) {
    const { h } = c;
    const v = c.pick(["x", "x", "n", "t"]);
    const show = p => h.poly(p.slice().reverse(), v); // p is low->high
    const add = (a, b) => Array.from({ length: Math.max(a.length, b.length) }, (_, i) => (a[i] || 0) + (b[i] || 0));
    const sub = (a, b) => add(a, b.map(x => -x));
    const mul = (a, b) => { const r = Array(a.length + b.length - 1).fill(0); a.forEach((x, i) => b.forEach((y, j) => r[i + j] += x * y)); return r; };
    const trim = p => { p = p.slice(); while (p.length > 1 && p[p.length - 1] === 0) p.pop(); return p; };
    const bin = r => `(${h.terms([[1, h.v(v)], [r, ""]])})`;
    const rnd = deg => Array.from({ length: deg + 1 }, () => c.ri(-6, 6));
    const reverse = p => h.terms(p.map((co, i) => [co, i === 0 ? "" : i === 1 ? h.v(v) : h.v(v) + `<sup>${i}</sup>`]));
    const sumForm = p => { let q; do { q = rnd(p.length - 1); q[p.length - 1] = c.ri(1, 3) * (p[p.length - 1] >= 0 ? 1 : -1) || 1; } while (trim(sub(p, q)).every(x => x === 0)); const r = sub(p, q); return `(${show(trim(q))}) + (${show(trim(r))})`; };
    const diffForm = p => { const q = rnd(p.length - 1); const s = sub(q, p); if (trim(s).every(x => x === 0)) return null; return `(${show(trim(q))}) ${h.MINUS} (${show(trim(s))})`; };
    const splitLin = p => { const [b, a] = p; const k = c.ri(1, 6); return h.terms([[a - k, h.v(v)], [b, ""], [k, h.v(v)]]); };
    let specs = [], size = c.lvl === 0 ? 3 : 4;
    if (c.lvl === 0) specs = c.distinct(3, () => [c.nz(-9, 9), c.nz(-6, 7)], x => x.join()).map(p => ({ p, forms: () => [show(p), reverse(p), splitLin(p), h.terms([[p[1], h.v(v)], [p[0] - 4, ""], [4, ""]])] }));
    else if (c.lvl === 1) specs = c.distinct(4, () => [c.ri(-9, 9), c.nz(-6, 6), c.nz(-3, 3)], x => x.join()).map(p => ({ p, forms: () => [show(p), sumForm(p), sumForm(p), diffForm(p), reverse(p)] }));
    else {
      let roots;
      if (c.lvl === 2) roots = c.distinct(4, () => [c.nz(-6, 6), c.nz(-6, 6)], x => x.slice().sort().join());
      else { const a = c.ri(2, 6), b = c.ri(1, 5); roots = c.shuffle([[a, -b], [-a, b], [a, b], [-a, -b]]); if (a === b) roots[2] = [a, a]; }
      specs = roots.map(([r, s]) => { const p = mul([r, 1], [s, 1]); return { p, forms: () => [`${bin(r)}${bin(s)}`, `${bin(s)}${bin(r)}`, `${h.v(v)}${bin(s)} ${r < 0 ? h.MINUS : "+"} ${Math.abs(r)}${bin(s)}`, show(p), reverse(p), r === s ? `${bin(r)}<sup>2</sup>` : null] }; });
    }
    const used = new Set();
    const groups = specs.map(sp => {
      const fs = c.shuffle(sp.forms().filter(Boolean)).filter(f => { if (used.has(f)) return false; return true; });
      const items = [...new Set(fs)].slice(0, size); items.forEach(f => used.add(f));
      return { label: show(sp.p), items: items.map(f => ({ html: f, cls: "mth" })), say: `They all simplify to ${PG.textify(show(sp.p))}.` };
    });
    if (groups.some(g => g.items.length < size)) return this.round(c);
    return { groups, cw: c.lvl >= 1 ? "220px" : "170px" };
  }
});
