PG.game({
  id: "g6-fdp-oddout", title: ["Fraction · Decimal · Percent", "Odd One Out"], course: "Grade 6", unit: "Percents",
  tag: "Three cards are worth the same. Find the impostor.",
  skills: "6.RP.3c, 6.NS · fractions, decimals and percents · common conversion mistakes",
  engine: "oddout",
  levels: [
    "The odd card is clearly different.",
    "The odd card is a classic mistake (¼ is NOT 0.4).",
    "Eighths and harder values. Then explain: what do the other three equal?",
    "Over 100%, under 1%, ratio language… and you explain your choice."
  ],
  round(c) {
    const { h } = c;
    const base = c.lvl === 0 ? [[1, 2], [1, 4], [3, 4], [1, 5], [2, 5], [1, 10], [3, 10]] : c.lvl === 1 ? [[1, 4], [3, 4], [2, 5], [3, 5], [4, 5], [7, 10], [1, 20], [3, 20], [9, 10]] : c.lvl === 2 ? [[1, 8], [3, 8], [5, 8], [7, 8], [3, 20], [7, 20], [6, 25], [9, 25], [11, 20]] : [[5, 4], [3, 2], [7, 4], [1, 200], [1, 40], [9, 8], [11, 10], [1, 400]];
    const pct = (n, d) => +(100 * n / d).toFixed(3) + "%";
    const dec = (n, d) => String(+(n / d).toFixed(4));
    const forms = (n, d) => {
      const out = [{ html: h.frac(n, d), cls: "mth", label: `${n} over ${d}` }, { html: dec(n, d) }, { html: pct(n, d) }];
      const m = c.pick([2, 3, 4, 5].filter(k => d * k <= 200)); if (m) out.push({ html: h.frac(n * m, d * m), cls: "mth", label: `${n * m} over ${d * m}` });
      if (c.lvl >= 2 && 100 % d === 0) out.push({ html: `${n * 100 / d} out of 100`, cls: "txt" });
      if (c.lvl === 3) out.push({ html: `${n} : ${d}`, label: `${n} to ${d}` }, { html: `${n} out of ${d}`, cls: "txt" });
      return out;
    };
    const mistakes = (n, d) => {
      const out = [];
      out.push(`0.${n}${d}`, `${n}.${d}`, `${n}${d}%`, `${d}%`, `0.${d}`, `${n}%`);
      const v = n / d; out.push(String(+(v * 10).toFixed(4)), String(+(v / 10).toFixed(4)), +(v * 1000).toFixed(2) + "%", +(v * 10).toFixed(2) + "%");
      return out.filter(x => { const num = x.endsWith("%") ? parseFloat(x) / 100 : parseFloat(x); return Math.abs(num - v) > 1e-9; });
    };
    const N = c.n(6), puzzles = [];
    const bs = c.shuffle(base);
    for (let i = 0; i < N; i++) {
      const [n, d] = bs[i % bs.length];
      const same = c.sample(forms(n, d), 3);
      let odd;
      if (c.lvl === 0) { const [n2, d2] = c.pick(base.filter(b => b[0] / b[1] !== n / d)); odd = c.pick(forms(n2, d2)); }
      else odd = { html: c.pick(mistakes(n, d)) };
      const oddVal = (() => { if (odd.html.includes("frac")) { const m = odd.html.match(/<span>(\d+)<\/span><span>(\d+)<\/span>/); return m[1] / m[2]; } return odd.html.endsWith("%") ? parseFloat(odd.html) / 100 : parseFloat(odd.html); })();
      if (Math.abs(oddVal - n / d) < 1e-9) { i--; continue; }
      const cards = c.shuffle(same.concat([odd]));
      const oi = cards.indexOf(odd);
      const right = `The other three all equal ${pct(n, d)}`;
      const wrong1 = `The other three all equal ${+(oddVal * 100).toFixed(3)}%`;
      let alt; do { const [a2, b2] = c.pick(base); alt = pct(a2, b2); } while (alt === pct(n, d) || alt === +(oddVal * 100).toFixed(3) + "%");
      const reasons = c.shuffle([right, wrong1, `The other three all equal ${alt}`]);
      puzzles.push({ cards, odd: oi, reasons, reason: reasons.indexOf(right), why: `${PG.textify(odd.html)} = ${+(oddVal * 100).toFixed(3)}%, but the others are ${pct(n, d)}.` });
    }
    return { puzzles, cw: "150px", reasonFrom: 2 };
  }
});
