PG.game({
  id: "g6-integer-line", title: ["Integer", "Number Line"], course: "Grade 6", unit: "Integers & Rational Numbers",
  tag: "Drop each card where its value lives on the number line.",
  skills: "6.NS.5–7 · integers and opposites · absolute value · rational numbers on the line",
  engine: "spots",
  levels: [
    "Integers from −10 to 10. Only every fifth tick is labeled.",
    "Opposites and absolute values: −(−4), |−3|, the opposite of 6.",
    "Rational numbers from −5 to 5: −2.5, 3/2, −1 1/2.",
    "Expressions: “3 less than −2”, |−7| − 9, half of −8."
  ],
  round(c) {
    const { h } = c;
    const half = c.lvl === 2;
    const lo = half ? -5 : -10, hi = half ? 5 : 10;
    const W = 680, Hh = 112, X0 = 30, X1 = 650, Y = 70;
    const X = v => X0 + (X1 - X0) * (v - lo) / (hi - lo);
    let s = `<svg viewBox="0 0 ${W} ${Hh}" role="img" aria-label="number line from ${lo} to ${hi}"><line x1="${X0 - 14}" y1="${Y}" x2="${X1 + 14}" y2="${Y}" stroke="currentColor" stroke-width="2.5"/><path d="M${X0 - 14} ${Y - 6} L${X0 - 24} ${Y} L${X0 - 14} ${Y + 6}Z M${X1 + 14} ${Y - 6} L${X1 + 24} ${Y} L${X1 + 14} ${Y + 6}Z" fill="currentColor"/>`;
    const step = half ? .5 : 1;
    for (let v = lo; v <= hi + 1e-9; v += step) { const big = half ? Number.isInteger(v) : v % 5 === 0; s += `<line x1="${X(v)}" x2="${X(v)}" y1="${Y - (big ? 11 : 6)}" y2="${Y + (big ? 11 : 6)}" stroke="currentColor" stroke-width="${big ? 2.4 : 1.4}"/>`; if (half ? Number.isInteger(v) : v % 5 === 0) s += `<text x="${X(v)}" y="${Y + 30}" text-anchor="middle" font-size="16" font-weight="700" fill="currentColor">${h.fmt(v)}</text>`; }
    s += "</svg>";
    const n = c.n(6);
    const gapMin = half ? 1 : 2;
    const vals = [];
    let g = 0;
    while (vals.length < n && g++ < 500) {
      const v = half ? c.ri(-10, 10) / 2 : c.ri(lo, hi);
      if (half && Number.isInteger(v) && c.chance(.6)) continue;
      if (vals.every(x => Math.abs(x - v) >= gapMin)) vals.push(v);
    }
    const disguise = v => {
      if (c.lvl === 0) return { html: h.fmt(v) };
      if (c.lvl === 1) { const o = [`−(${h.fmt(-v)})`, `the opposite of ${h.fmt(-v)}`]; if (v > 0) o.push(`|${h.fmt(-v)}|`, `|${v}|`); if (v < 0) o.push(`−|${-v}|`); if (c.chance(.25)) return { html: h.fmt(v) }; return { html: c.pick(o), cls: "txt" }; }
      if (c.lvl === 2) { if (Number.isInteger(v)) return { html: h.fmt(v) }; const k = Math.round(v * 2); const opts = [{ html: h.fmt(v) }, { html: h.f(k, 2), cls: "mth" }]; if (Math.abs(v) > 1) opts.push({ html: (v < 0 ? h.MINUS : "") + h.mixed(Math.floor(Math.abs(v)), 1, 2), cls: "mth" }); return c.pick(opts); }
      const F = x => h.fmt(x), P = x => x < 0 ? `(${F(x)})` : F(x);
      let a; do { a = c.ri(-8, 8); } while (a === v);
      const opts = [v > a ? `${v - a} more than ${F(a)}` : `${a - v} less than ${F(a)}`, `half of ${F(2 * v)}`];
      const k = c.ri(1, 9); if (v + k >= 0 && v + k !== 0) opts.push(`|${F(c.chance(.5) ? v + k : -(v + k))}| − ${k}`);
      const b = c.ri(1, 7); opts.push(`−(${F(-v - b)} + ${b})`);
      if (v !== 0) opts.push(`the opposite of ${P(-v)}`);
      const pick = c.pick(opts);
      return { html: pick, cls: "txt" };
    };
    const spots = vals.map((v, i) => ({ x: X(v), y: Y - 34, key: String(v), label: `Spot ${i + 1}` }));
    const cards = vals.map(v => Object.assign({ key: String(v), say: c.lvl ? `That's ${h.fmt(v).replace(h.MINUS, "−")}.` : null }, disguise(v)));
    return { svg: s, w: W, h: Hh, spots, cards, trayTitle: "Values", fill: card => h.fmt(+card.key),
      why: (card, spot) => c.mode === "practice" ? `Work out the value first: this card is ${h.fmt(+card.key)}. Negative numbers sit left of 0.` : "Work out the value, then count ticks from a labeled number." };
  }
});
