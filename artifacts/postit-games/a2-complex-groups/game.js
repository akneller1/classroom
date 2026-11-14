PG.game({
  id: "a2-complex-groups", title: ["Complex Number", "Groups"], course: "Algebra 2", unit: "Complex Numbers",
  tag: "Group the expressions that equal the same complex number.",
  skills: "N.CN.1–3 · powers of i · adding, subtracting, multiplying and dividing complex numbers · conjugates",
  engine: "groups",
  levels: [
    "Powers of i: which equal 1, −1, i or −i?",
    "Adding and subtracting complex numbers.",
    "Multiplying complex numbers (remember i² = −1).",
    "Dividing with conjugates, and look-alike answers like 3 + 2i vs 2 + 3i."
  ],
  round(c) {
    const { h } = c; const M = h.MINUS; const I = h.v("i");
    const z = (a, b) => { if (!b) return h.fmt(a); const bi = (Math.abs(b) === 1 ? "" : Math.abs(b)) + I; if (!a) return (b < 0 ? M : "") + bi; return `${h.fmt(a)} ${b < 0 ? M : "+"} ${bi}`; };
    const P = (a, b) => `(${z(a, b)})`;
    const mul = ([a, b], [cc, d]) => [a * cc - b * d, a * d + b * cc];
    const nz = () => c.nz(-6, 6);
    let groups;
    if (c.lvl === 0) {
      const vals = [[1, 0], [-1, 0], [0, 1], [0, -1]];
      groups = vals.map(([a, b], r) => {
        const rem = [0, 2, 1, 3][r];
        const ns = c.sample([0, 1, 2, 3, 4, 5, 6].map(k => 4 * k + rem).filter(n => n > 1), 3);
        const items = ns.map(n => `${I}<sup>${n}</sup>`);
        const extra = { 0: [`${I}<sup>2</sup> · ${I}<sup>2</sup>`, `(${M}${I})<sup>4</sup>`, `${I} · ${I}<sup>3</sup>`], 1: [`${I} · ${I}`, `(${M}${I})<sup>2</sup>`, `${I}<sup>3</sup> · ${I}<sup>3</sup>`], 2: [`${I}<sup>2</sup> · ${I}<sup>3</sup>`, `${I}<sup>4</sup> · ${I}`, `(${M}${I})<sup>3</sup>`], 3: [`${I}<sup>2</sup> · ${I}`, `${M}${I}<sup>5</sup>`, `(${M}${I})<sup>5</sup>`] }[r];
        items.push(c.pick(extra));
        return { label: z(a, b), items: items.map(x => ({ html: x, cls: "mth" })), say: `These all equal ${PG.textify(z(a, b))}.` };
      });
    } else {
      let vals, facs = {};
      if (c.lvl === 3) { const a = c.ri(2, 6); let b; do { b = c.ri(1, 6); } while (b === a); vals = c.shuffle([[a, b], [b, a], [a, -b], [-a, b]]); }
      else if (c.lvl === 2) { vals = []; let gg = 0; while (vals.length < 4 && gg++ < 200) { const u = [c.ri(-3, 3), c.nz(-3, 3)], w = [c.nz(-4, 4), c.ri(-3, 3)]; const v = mul(u, w); if (!v[1] || vals.some(x => x.join() === v.join())) continue; vals.push(v); facs[v.join()] = [u, w]; } }
      else vals = c.distinct(4, () => [c.ri(-8, 8), nz()], x => x.join());
      const used = new Set();
      groups = vals.map(v => {
        const forms = new Set([z(...v)]);
        const neg = q => [-q[0], -q[1]];
        if (c.lvl === 2) { const [u, w] = facs[v.join()]; c.shuffle([`${P(...u)}${P(...w)}`, `${P(...w)}${P(...u)}`, `${P(...neg(u))}${P(...neg(w))}`, `${P(...mul(u, [0, 1]))}${P(...mul(w, [0, -1]))}`]).slice(0, 2).forEach(f => forms.add(f)); }
        let guard = 0;
        while (forms.size < 4 && guard++ < 200) {
          let f;
          const t = c.lvl === 3 ? c.ri(0, 2) : -1;
          if (t === -1) {
            const u = [c.ri(-7, 7), nz()];
            if (c.chance(.5)) { const w = [v[0] - u[0], v[1] - u[1]]; f = `${P(...u)} + ${P(...w)}`; }
            else { const w = [u[0] - v[0], u[1] - v[1]]; f = `${P(...u)} ${M} ${P(...w)}`; }
          } else if (t === 0) { const u = [c.ri(1, 3), c.nz(-3, 3)]; const top = mul(v, u); f = h.frac(z(...top), z(...u)); }
          else if (t === 1) { f = `${I} · ${P(...solve(v, [0, 1]))}`; }
          else { f = `${M}${I} · ${P(...solve(v, [0, -1]))}`; }
          if (f && !used.has(f)) forms.add(f);
        }
        const items = [...forms].slice(0, 4); items.forEach(f => used.add(f));
        return { label: z(...v), items: items.map(x => ({ html: x, cls: "mth" })), say: `All equal ${PG.textify(z(...v))}.` };
      });
    }
    function solve(v, u) { // w = v / u if Gaussian integer
      const d = u[0] * u[0] + u[1] * u[1]; const n = mul(v, [u[0], -u[1]]); if (n[0] % d || n[1] % d) return null; return [n[0] / d, n[1] / d];
    }
    if (groups.some(g => g.items.length < 4)) return this.round(c);
    return { groups, cw: "200px" };
  }
});
