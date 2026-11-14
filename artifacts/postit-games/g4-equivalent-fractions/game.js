PG.game({
  id: "g4-equivalent-fractions", title: ["Equivalent Fraction", "Groups"], course: "Grade 4", unit: "Fraction Equivalence",
  tag: "Find the groups of fractions that are worth the same amount.",
  skills: "4.NF.1, 4.NF.5–6 · equivalent fractions · fraction models · tenths and hundredths as decimals",
  engine: "groups",
  levels: [
    "Three groups of three, with fraction bars to help.",
    "Four groups of four. One model in each group.",
    "Fractions, hundredths and decimals: 3/4 = 75/100 = 0.75.",
    "Look-alikes: 2/3, 3/4, 4/5 and friends. Adding the same number to top and bottom does NOT make an equivalent fraction."
  ],
  round(c) {
    const { h } = c;
    const bar = (n, d) => { const w = 132, cw = w / d; let s = `<svg viewBox="0 0 ${w + 4} 30" width="${w + 4}" aria-label="bar split into ${d} equal parts with ${n} shaded">`; for (let i = 0; i < d; i++) s += `<rect x="${2 + i * cw}" y="3" width="${cw}" height="24" fill="${i < n ? "#2f5bd3" : "#fff"}" stroke="#13202f" stroke-width="1.4"/>`; return s + "</svg>"; };
    const F = (n, d) => ({ html: h.frac(n, d), label: `${n} over ${d}`, cls: "mth" });
    let bases, groups;
    if (c.lvl === 0) bases = c.sample([[1, 2], [1, 3], [1, 4], [2, 3], [3, 4], [2, 5]], 3);
    else if (c.lvl === 1) bases = c.sample([[1, 2], [1, 3], [2, 3], [1, 4], [3, 4], [2, 5], [3, 5], [5, 6], [3, 8]], 4);
    else if (c.lvl === 2) bases = c.sample([[1, 2], [1, 4], [3, 4], [1, 5], [2, 5], [3, 5], [4, 5], [7, 10], [3, 10], [9, 20], [3, 25]], 4);
    else bases = c.sample([[2, 3], [3, 4], [4, 5], [3, 5], [5, 6], [5, 8], [2, 5]], 4);
    groups = bases.map(([n, d]) => {
      let items;
      const ms = c.lvl === 3 ? c.shuffle([2, 3, 4, 5, 6, 7]) : c.shuffle([2, 3, 4, 5, 6].filter(m => d * m <= 30));
      if (c.lvl === 0) items = [F(n, d), F(n * ms[0], d * ms[0]), { html: bar(n * (d <= 4 ? 2 : 1), d * (d <= 4 ? 2 : 1)), cls: "pic", label: `bar with ${n * (d <= 4 ? 2 : 1)} of ${d * (d <= 4 ? 2 : 1)} parts shaded` }];
      else if (c.lvl === 1) { const mm = c.pick([1, 2].filter(m => d * m <= 12)); items = [F(n, d), F(n * ms[0], d * ms[0]), F(n * ms[1], d * ms[1]), { html: bar(n * mm, d * mm), cls: "pic", label: `bar with ${n * mm} of ${d * mm} parts shaded` }]; }
      else if (c.lvl === 2) { const hund = 100 / d * n; const opt = [F(n, d), F(hund, 100), { html: (hund / 100).toFixed(2).replace(/0$/, "").replace(/\.$/, ""), label: String(hund / 100) }]; const m2 = ms.find(m => 100 % (d * m) !== 0 || d * m !== 100) || 2; opt.push(d * m2 === 100 ? F(n * 3, d * 3) : F(n * m2, d * m2)); items = opt; }
      else items = [F(n * ms[0], d * ms[0]), F(n * ms[1], d * ms[1]), F(n * ms[2], d * ms[2]), F(n * ms[3] || n * 7, d * ms[3] || d * 7)];
      return { label: `Equal to ${n}/${d}`, items, say: `All equal ${n}/${d}: multiply top and bottom by the same number.` };
    });
    // ensure no duplicate html across the whole board
    const seen = new Set(); let dup = false; groups.forEach(g => g.items.forEach(it => { if (seen.has(it.html)) dup = true; seen.add(it.html); }));
    if (dup) groups.forEach((g, gi) => g.items.forEach((it, ii) => { if ([...groups.slice(0, gi).flatMap(x => x.items)].some(o => o.html === it.html)) { const [n, d] = bases[gi]; it.html = h.frac(n * (7 + ii), d * (7 + ii)); it.label = `${n * (7 + ii)} over ${d * (7 + ii)}`; } }));
    return { groups, cw: "150px" };
  }
});
