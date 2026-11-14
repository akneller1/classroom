PG.game({
  id: "g3-fraction-line", title: ["Fraction", "Number Line"], course: "Grade 3", unit: "Fractions",
  tag: "Drop each fraction card on its point on the number line.",
  skills: "3.NF.2, 3.NF.3 · fractions on a number line · whole numbers as fractions · equivalent fractions",
  engine: "spots",
  levels: [
    "0 to 1 split into halves, thirds or fourths.",
    "0 to 1 split into sixths or eighths. Count the jumps carefully.",
    "0 to 2: fractions greater than 1, like 5/4 and 8/4.",
    "0 to 2 with two scales: one above the line and one below. Equivalent fractions share a point."
  ],
  how: ["Each point on the line has a spot. Count the equal jumps from 0 to find where a fraction lives.", "Only 0, 1 and 2 are labeled."],
  round(c) {
    const { h } = c;
    const W = 640, Hh = c.lvl === 3 ? 150 : 110, X0 = 30, X1 = 610, Y = c.lvl === 3 ? 75 : 62;
    const M = c.lvl >= 2 ? 2 : 1;
    const X = v => X0 + (X1 - X0) * v / M;
    let dens;
    if (c.lvl === 0) dens = [c.pick([2, 3, 4])];
    else if (c.lvl === 1) dens = [c.pick([6, 8])];
    else if (c.lvl === 2) dens = [c.pick([2, 3, 4])];
    else { const d = c.pick([2, 3, 4]); dens = [d, d * 2]; }
    let s = `<svg viewBox="0 0 ${W} ${Hh}" role="img" aria-label="number line from 0 to ${M}">`;
    s += `<line x1="${X0 - 12}" y1="${Y}" x2="${X1 + 12}" y2="${Y}" stroke="currentColor" stroke-width="2.5"/>`;
    dens.forEach((d, di) => { for (let k = 0; k <= d * M; k++) { const x = X(k / d), whole = k % d === 0; const up = di === 0; s += `<line x1="${x}" x2="${x}" y1="${up ? Y - (whole ? 16 : 10) : Y}" y2="${up ? Y : Y + (whole ? 16 : 10)}" stroke="currentColor" stroke-width="${whole ? 2.5 : 1.6}"/>`; } });
    for (let w = 0; w <= M; w++) s += `<text x="${X(w)}" y="${c.lvl === 3 ? Hh - 4 : Y + 34}" text-anchor="middle" font-size="18" font-weight="700" fill="currentColor">${w}</text>`;
    s += "</svg>";
    const spots = [], cards = [];
    const want = c.lvl === 0 ? dens[0] * M : c.n(c.lvl === 1 ? 5 : 6);
    dens.forEach((d, di) => {
      let ks = []; for (let k = 1; k <= d * M; k++) ks.push(k);
      if (c.lvl === 3) { ks = c.shuffle(ks); const keep = []; for (const k of ks) if (keep.length < Math.ceil(want / 2) && keep.every(q => Math.abs(q - k) > 1)) keep.push(k); ks = keep; }
      else if (ks.length > want) ks = c.sample(ks, want);
      ks.forEach(k => {
        const g = h.gcd(k, d), key = (k / g) + "/" + (d / g);
        spots.push({ x: X(k / d), y: c.lvl === 3 ? (di === 0 ? Y - 34 : Y + 36) : Y - 28, key, label: `Spot ${spots.length + 1} on the ${c.lvl === 3 ? (di === 0 ? "upper" : "lower") + " scale" : "line"}` });
        cards.push({ html: h.frac(k, d), label: `${k} over ${d}`, key, cls: "mth" });
      });
    });
    return { svg: s, w: W, h: Hh, spots, cards, trayTitle: "Fractions",
      why: (card, spot) => { const [n, d] = card.key.split("/").map(Number); return c.mode === "practice" ? `${PG.textify(card.html)} is ${n >= d ? "more than 1 — past the 1 mark" : "less than 1"}. Count the jumps from 0.` : "That's not where it lives. Count the jumps from 0."; } };
  }
});
