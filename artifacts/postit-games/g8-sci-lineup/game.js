PG.game({
  id: "g8-sci-lineup", title: ["Scientific Notation", "Line-Up"], course: "Grade 8", unit: "Exponents & Scientific Notation",
  tag: "Order very big and very small numbers.",
  skills: "8.EE.3–4 · scientific notation · negative exponents · comparing magnitudes · multiplying and dividing in scientific notation",
  engine: "order",
  levels: [
    "Positive powers of ten.",
    "Positive and negative exponents (3 × 10⁴ vs 3 × 10⁻⁴).",
    "Scientific notation, standard form and “not-quite” scientific notation (34 × 10³), close together.",
    "Products and quotients like (2 × 10³)(4 × 10⁵). You check the order yourself."
  ],
  options: [{ id: "dir", label: "Order", type: "one", choices: [["up", "Least to greatest"], ["down", "Greatest to least"]], default: "up" }],
  round(c) {
    const { h } = c; const M = h.MINUS;
    const E = e => (e < 0 ? M + Math.abs(e) : String(e));
    const sci = (m, e) => `${h.fmt(m)} × 10<sup>${E(e)}</sup>`;
    const std = x => { if (x >= 1) return Math.round(x).toLocaleString("en-US"); const s = x.toFixed(12).replace(/0+$/, ""); return s; };
    const n = [5, 6, 7, 7][c.lvl] + (c.len === 2 ? 1 : 0) - (c.len === 0 ? 1 : 0);
    const cards = [], seen = new Set();
    let g = 0;
    while (cards.length < n && g++ < 800) {
      let m = c.ri(10, 99) / 10, e, html, val;
      if (c.lvl === 0) { e = c.ri(2, 9); html = sci(m, e); val = m * 10 ** e; }
      else if (c.lvl === 1) { e = c.ri(-7, 7); if (e === 0) continue; if (cards.length && c.chance(.4)) { const p = c.pick(cards); m = p.m; } html = sci(m, e); val = m * 10 ** e; }
      else if (c.lvl === 2) {
        e = c.pick([-4, -3, 3, 4, 5]) + c.ri(0, 1); val = m * 10 ** e;
        const t = c.ri(0, 2);
        if (t === 0) html = sci(m, e);
        else if (t === 1 && e >= -6 && e <= 6) html = std(val);
        else { const mm = Math.round(m * 10); html = `${mm} × 10<sup>${E(e - 1)}</sup>`; }
        if (!html) html = sci(m, e);
      } else {
        const t = c.ri(0, 2);
        const a = c.ri(1, 9), b = c.ri(1, 9), e1 = c.ri(-6, 8), e2 = c.ri(-6, 8);
        if (t === 0) { html = `(${a} × 10<sup>${E(e1)}</sup>)(${b} × 10<sup>${E(e2)}</sup>)`; val = a * b * 10 ** (e1 + e2); }
        else if (t === 1) { const q = c.ri(1, 4); html = `(${a * q} × 10<sup>${E(e1)}</sup>) ÷ (${q} × 10<sup>${E(e2)}</sup>)`; val = a * 10 ** (e1 - e2); }
        else { html = sci(m, c.ri(-8, 12)); val = m * 10 ** +html.match(/<sup>(.*?)<\/sup>/)[1].replace(M, "-"); }
        m = null;
      }
      const lv = Math.log10(val), k = lv.toFixed(6);
      if (seen.has(k) || [...seen].some(s => Math.abs(+s - lv) < 0.01)) continue;
      seen.add(k); cards.push({ html, v: lv, m, cls: "mth" });
    }
    const down = c.opt.dir === "down";
    return { cards, desc: down, lo: down ? "Greatest" : "Least", hi: down ? "Least" : "Greatest", endCheck: c.lvl === 3, slotMin: c.lvl === 3 ? 150 : 120, tol: 1e-6,
      why: card => c.mode === "practice" ? "Compare the exponents first (a negative exponent means a tiny number), then the front numbers." : "" };
  }
});
