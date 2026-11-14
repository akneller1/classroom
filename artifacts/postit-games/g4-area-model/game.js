PG.game({
  id: "g4-area-model", title: ["Area Model", "Multiplier"], course: "Grade 4", unit: "Multi-Digit Multiplication",
  tag: "Fill the area model with partial products, then the total.",
  skills: "4.NBT.5 · place value · partial products · area model · 4-digit × 1-digit and 2-digit × 2-digit",
  engine: "grid",
  levels: [
    "2-digit × 1-digit.",
    "3-digit × 1-digit.",
    "2-digit × 2-digit.",
    "4-digit × 1-digit or 3-digit × 2-digit, with place-value decoys (one zero too many or too few)."
  ],
  how: ["Each box is the product of its row header and column header.", "The total is the sum of all the boxes.", "Some cards are decoys and won't fit anywhere."],
  round(c) {
    const fmt = n => n.toLocaleString("en-US");
    const parts = n => { const s = String(n); return s.split("").map((d, i) => +d * 10 ** (s.length - 1 - i)).filter(Boolean); };
    let A, B;
    if (c.lvl === 0) { A = c.ri(12, 98); B = c.ri(3, 9); }
    else if (c.lvl === 1) { A = c.ri(102, 989); B = c.ri(3, 9); }
    else if (c.lvl === 2) { A = c.ri(13, 98); B = c.ri(13, 98); }
    else if (c.chance(.5)) { A = c.ri(1203, 8976); B = c.ri(3, 9); } else { A = c.ri(112, 789); B = c.ri(13, 59); }
    const cp = parts(A), rp = parts(B);
    const keys = new Set();
    const cells = rp.map(r => cp.map(col => { const v = r * col; keys.add(String(v)); return { key: String(v), html: fmt(v) }; }));
    const total = A * B;
    cells.push(cp.map((_, i) => i === 0 ? { key: "T" + total, html: fmt(total) } : null));
    const cards = [];
    rp.forEach(r => cp.forEach(col => cards.push({ key: String(r * col), html: fmt(r * col) })));
    cards.push({ key: "T" + total, html: fmt(total) });
    const nDecoy = [1, 2, 3, 4][c.lvl];
    const decoys = new Set();
    let g = 0;
    while (decoys.size < nDecoy && g++ < 200) {
      const r = c.pick(rp), col = c.pick(cp), v = r * col;
      const d = c.pick([v * 10, v / 10, v + r, v - col, total + c.pick([10, 100, -10, -100])].filter(x => Number.isInteger(x) && x > 0));
      if (!keys.has(String(d)) && d !== total && !decoys.has(d)) decoys.add(d);
    }
    decoys.forEach(d => cards.push({ key: "x" + d, html: fmt(d) }));
    return {
      corner: "×", cols: cp.map(fmt), rows: rp.map(fmt).concat(["Total"]), cells, cards, maxW: "760px",
      cellLabel: (ri, ci) => ri < rp.length ? `${fmt(rp[ri])} times ${fmt(cp[ci])}` : "Total",
      why: (card, cell, ri, ci) => ri >= rp.length ? `The total is the sum of all the boxes${c.mode === "practice" ? ": " + cells.slice(0, rp.length).flat().map(x => x.html).join(" + ") : ""}.` : `${fmt(rp[ri])} × ${fmt(cp[ci])} = ${c.mode === "practice" ? fmt(rp[ri] * cp[ci]) : "?"}. Count the zeros carefully.`,
      doneText: "Model complete. The leftover cards were decoys."
    };
  }
});
