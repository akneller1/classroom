PG.game({
  id: "g1-tens-ones", title: ["Tens & Ones", "Match"], course: "Grade 1", unit: "Place Value to 120",
  tag: "Match each number to its tens and ones.",
  skills: "1.NBT.2–3 · tens and ones · comparing digits · regrouping ten ones as a ten",
  engine: "match",
  levels: [
    "Numbers to 50 matched to base-ten blocks.",
    "Numbers to 99 matched to blocks or “tens and ones”. Watch for flipped digits like 34 and 43.",
    "Numbers to 120, including zeros (40 vs 4) and 11 tens.",
    "Tricky regrouping: “2 tens 14 ones” is 34. Every card is a disguise."
  ],
  options: [{ id: "style", label: "Play style", type: "one", choices: [["open", "Open cards"], ["memory", "Memory (face down)"]], default: "open" }],
  round(c) {
    const blocks = (t, o) => {
      const rodW = 10, gap = 4, w = Math.max(30, t * (rodW + gap) + (o ? Math.ceil(o / 5) * 12 + 6 : 0)), h = 64;
      let s = `<svg viewBox="0 0 ${w} ${h}" width="${Math.min(w * 1.15, 150)}" height="${h * 1.0}" aria-label="${t} tens and ${o} ones">`;
      for (let i = 0; i < t; i++) { const x = 2 + i * (rodW + gap); s += `<rect x="${x}" y="2" width="${rodW}" height="60" fill="#fff" stroke="#13202f" stroke-width="1.3"/>`; for (let k = 1; k < 10; k++) s += `<line x1="${x}" x2="${x + rodW}" y1="${2 + k * 6}" y2="${2 + k * 6}" stroke="#13202f" stroke-width=".6"/>`; }
      const ox = 4 + t * (rodW + gap);
      for (let i = 0; i < o; i++) s += `<rect x="${ox + Math.floor(i / 5) * 12}" y="${52 - (i % 5) * 12}" width="10" height="10" fill="#fff" stroke="#13202f" stroke-width="1.3"/>`;
      return s + "</svg>";
    };
    const words = (t, o) => `${t} ten${t === 1 ? "" : "s"} ${o} one${o === 1 ? "" : "s"}`;
    const max = [50, 99, 120, 99][c.lvl], min = [11, 11, 1, 20][c.lvl];
    const N = c.n(c.opt.style === "memory" ? 6 : 6);
    let vals = [];
    if (c.lvl === 1) { while (vals.length < N) { const t = c.ri(1, 9), o = c.ri(1, 9); if (t === o) continue; const a = t * 10 + o; if (!vals.includes(a)) vals.push(a); if (vals.length < N && c.chance(.6) && !vals.includes(o * 10 + t)) vals.push(o * 10 + t); } }
    else if (c.lvl === 2) { const pool = []; for (let i = 0; i < 40; i++) { const t = c.ri(1, 9); pool.push(t, t * 10, c.ri(100, 120)); } vals = c.distinct(N, () => c.pick(pool) + (c.chance(.3) ? c.ri(1, 9) : 0)).filter(v => v <= 120); while (vals.length < N) { const v = c.ri(min, max); if (!vals.includes(v)) vals.push(v); } }
    else vals = c.distinct(N, () => c.ri(min, max));
    vals = vals.slice(0, N);
    const pairs = vals.map(v => {
      const t = Math.floor(v / 10), o = v % 10;
      if (c.lvl === 0) return { a: { html: String(v), label: String(v) }, b: { html: blocks(t, o), label: words(t, o), cls: "pic" } };
      if (c.lvl === 1) return { a: { html: String(v) }, b: c.chance(.5) ? { html: blocks(t, o), label: words(t, o), cls: "pic" } : { html: words(t, o), cls: "txt" } };
      if (c.lvl === 2) return { a: { html: String(v) }, b: v > 99 || c.chance(.5) ? { html: words(t, o), cls: "txt" } : { html: blocks(t, o), label: words(t, o), cls: "pic" } };
      const borrow = c.ri(1, Math.min(t, 2)), tt = t - borrow, oo = o + 10 * borrow;
      const b = c.chance(.5) ? { html: words(tt, oo), cls: "txt" } : { html: `${tt * 10} + ${oo}`, cls: "txt" };
      return { a: c.chance(.3) ? { html: blocks(t, o), label: words(t, o), cls: "pic" } : { html: String(v) }, b, say: `${PG.textify(b.html)} is ${v}: ${oo} ones make ${borrow} more ten${borrow > 1 ? "s" : ""} and ${o} ones.` };
    });
    return {
      pairs, style: c.opt.style, aTitle: "Numbers", bTitle: "Tens and ones", cw: "150px",
      why: (a, b) => `Count the tens first, then the ones. That card shows ${PG.textify(b.html)}.`
    };
  }
});
