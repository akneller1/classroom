PG.game({
  id: "g3-area-perimeter", title: ["Area or", "Perimeter?"], course: "Grade 3", unit: "Area & Perimeter",
  tag: "Sort the shapes by their area, their perimeter, or both.",
  skills: "3.MD.5–8 · area by counting squares and multiplying · perimeter · same area, different perimeter",
  engine: "sort",
  levels: [
    "Count the squares: sort rectangles by area.",
    "Labeled sides: sort rectangles by perimeter.",
    "Venn diagram: area = ?, perimeter = ?, both, or neither.",
    "Venn diagram with L-shapes. Cutting a corner out changes the area… but what about the perimeter?"
  ],
  round(c) {
    const rect = (l, w, grid, cut) => {
      const sc = Math.min(120 / l, 80 / w), W = l * sc, H = w * sc, ox = 24, oy = 20;
      let s = `<svg viewBox="0 0 ${W + 44} ${H + 40}" width="${Math.round(W + 44)}" aria-label="${cut ? `L-shape ${l} by ${w} with a ${cut[0]} by ${cut[1]} corner cut out` : `rectangle ${l} by ${w}`}">`;
      if (cut) {
        const [a, b] = cut, ca = a * sc, cb = b * sc;
        s += `<path d="M${ox} ${oy} H${ox + W - ca} V${oy + cb} H${ox + W} V${oy + H} H${ox} Z" fill="#fff" stroke="#13202f" stroke-width="2"/>`;
        const t = (x, y, v, anch = "middle") => `<text x="${x}" y="${y}" font-size="12" font-weight="700" text-anchor="${anch}" fill="#13202f">${v}</text>`;
        s += t(ox + (W - ca) / 2, oy - 5, l - a) + t(ox + W / 2, oy + H + 15, l) + t(ox - 5, oy + H / 2 + 4, w, "end") + t(ox + W + 5, oy + cb + (H - cb) / 2 + 4, w - b, "start") + t(ox + W - ca / 2, oy + cb + 14, a) + t(ox + W - ca - 4, oy + cb / 2 + 4, b, "end");
      } else {
        s += `<rect x="${ox}" y="${oy}" width="${W}" height="${H}" fill="#fff" stroke="#13202f" stroke-width="2"/>`;
        if (grid) { for (let i = 1; i < l; i++) s += `<line x1="${ox + i * sc}" x2="${ox + i * sc}" y1="${oy}" y2="${oy + H}" stroke="#13202f" stroke-width=".7"/>`; for (let j = 1; j < w; j++) s += `<line y1="${oy + j * sc}" y2="${oy + j * sc}" x1="${ox}" x2="${ox + W}" stroke="#13202f" stroke-width=".7"/>`; }
        else s += `<text x="${ox + W / 2}" y="${oy - 5}" font-size="12" font-weight="700" text-anchor="middle" fill="#13202f">${l}</text><text x="${ox - 5}" y="${oy + H / 2 + 4}" font-size="12" font-weight="700" text-anchor="end" fill="#13202f">${w}</text>`;
      }
      return s + "</svg>";
    };
    const pairsFor = A => { const out = []; for (let w = 1; w * w <= A; w++) if (A % w === 0 && A / w <= 12) out.push([A / w, w]); return out; };
    const N = c.n(10);
    if (c.lvl === 0) {
      const areas = c.sample([6, 8, 10, 12, 15, 16, 18, 20, 24], 3).sort((a, b) => a - b);
      const cards = []; let i = 0;
      while (cards.length < N && i++ < 200) { const A = areas[cards.length % 3]; const [l, w] = c.pick(pairsFor(A)); const flip = c.chance(.5); cards.push({ html: rect(flip ? w : l, flip ? l : w, true), cls: "pic", bin: "a" + A, label: `rectangle with ${l * w} squares`, why: `Count the squares: ${l} rows of ${w}${w === 1 ? "" : ""}… that's ${l} × ${w} = ${l * w}.` }); }
      return { bins: areas.map(A => ({ id: "a" + A, label: `Area = ${A}`, sub: "square units" })), cards: c.shuffle(cards) };
    }
    if (c.lvl === 1) {
      const pers = c.sample([10, 12, 14, 16, 18, 20], 3).sort((a, b) => a - b);
      const cards = [];
      while (cards.length < N) { const P = pers[cards.length % 3]; const l = c.ri(1, P / 2 - 1), w = P / 2 - l; cards.push({ html: rect(Math.max(l, w), Math.min(l, w), false), cls: "pic", bin: "p" + P, label: `rectangle ${l} by ${w}`, why: `Perimeter is the distance around: ${l} + ${w} + ${l} + ${w} = ${2 * (l + w)}.` }); }
      return { bins: pers.map(P => ({ id: "p" + P, label: `Perimeter = ${P}`, sub: "units" })), cards: c.shuffle(cards) };
    }
    // Venn
    let A, P, both;
    for (let t = 0; t < 100; t++) { A = c.pick([12, 16, 18, 20, 24, 30, 36]); const pr = c.pick(pairsFor(A)); P = 2 * (pr[0] + pr[1]); both = pr; if (pairsFor(A).length >= 2) break; }
    const pool = [];
    for (let l = 1; l <= 12; l++) for (let w = 1; w <= Math.min(l, 9); w++) pool.push({ l, w, area: l * w, per: 2 * (l + w) });
    if (c.lvl === 3) for (let l = 3; l <= 10; l++) for (let w = 3; w <= 8; w++) for (let a = 2; a < l - 1; a++) for (let b = 2; b < w; b++) if ((a + b) % 2 === 0 || c.chance(.2)) pool.push({ l, w, cut: [a, b], area: l * w - a * b, per: 2 * (l + w) });
    const region = s => (s.area === A ? 1 : 0) + (s.per === P ? 2 : 0);
    const want = { 3: 2, 1: 3, 2: 3, 0: 3 };
    const chosen = [];
    [3, 1, 2, 0].forEach(r => { const opts = c.shuffle(pool.filter(s => region(s) === r && (c.lvl < 3 || r === 0 || c.chance(.6) || !s.cut))); for (const s of opts) { if (chosen.filter(x => region(x) === r).length >= Math.round(want[r] * N / 11)) break; if (!chosen.some(x => x.l === s.l && x.w === s.w && JSON.stringify(x.cut) === JSON.stringify(s.cut))) chosen.push(s); } });
    if (c.lvl === 3 && !chosen.some(s => s.cut)) { const s = c.pick(pool.filter(s => s.cut && region(s) >= 2)); if (s) chosen.push(s); }
    const ids = { 3: "AB", 1: "A", 2: "B", 0: "N" };
    const cards = chosen.map(s => ({ html: rect(s.l, s.w, false, s.cut), cls: "pic", bin: ids[region(s)], label: s.cut ? `L-shape, outer ${s.l} by ${s.w}, corner ${s.cut[0]} by ${s.cut[1]} removed` : `rectangle ${s.l} by ${s.w}`,
      why: `Area = ${s.cut ? `${s.l} × ${s.w} − ${s.cut[0]} × ${s.cut[1]}` : `${s.l} × ${s.w}`} = ${s.area}. Perimeter = ${s.per}.` }));
    return { venn: { A: `Area = ${A}`, B: `Perimeter = ${P}` }, bins: [], cards: c.shuffle(cards) };
  }
});
