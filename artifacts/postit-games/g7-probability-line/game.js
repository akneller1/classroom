PG.game({
  id: "g7-probability-line", title: ["Probability", "Line"], course: "Grade 7", unit: "Probability",
  tag: "Place each event on the probability line from impossible to certain.",
  skills: "7.SP.5–8 · probability from 0 to 1 · theoretical probability · complements · compound events",
  engine: "spots",
  levels: [
    "Coins and number cubes.",
    "Spinners and bags of marbles.",
    "Bags with “not” and “or” (simplify the fraction!).",
    "Compound events: two coins, two dice, three coins…"
  ],
  round(c) {
    const { h } = c;
    const red = (n, d) => { const g = h.gcd(n, d); return [n / g, d / g]; };
    const ev = [];
    const add = (text, n, d) => { const [a, b] = red(n, d); ev.push({ text, v: a / b, key: a + "/" + b }); };
    if (c.lvl === 0) {
      add("Roll a number less than 7 on a number cube", 1, 1); add("Roll an 8 on a number cube", 0, 1); add("Flip a coin: heads", 1, 2);
      add("Roll a 6", 1, 6); add("Roll a number greater than 2", 4, 6); add("Roll a 1 or a 2", 2, 6); add("Roll anything but a 6", 5, 6); add("Roll an even number", 3, 6);
    } else if (c.lvl === 1) {
      for (let i = 0; i < 14; i++) {
        if (c.chance(.5)) { const n = c.pick([4, 5, 6, 8, 10]), m = c.ri(0, n); add(`Spinner with ${n} equal parts, ${m} blue: land on blue`, m, n); }
        else { const r = c.ri(1, 6), b = c.ri(1, 8); add(`Bag with ${r} red and ${b} blue marbles: pick red`, r, r + b); }
      }
    } else if (c.lvl === 2) {
      for (let i = 0; i < 14; i++) {
        const r = c.ri(1, 6), b = c.ri(1, 6), g = c.ri(1, 6), T = r + b + g;
        const t = c.ri(0, 2);
        if (t === 0) add(`Bag: ${r} red, ${b} blue, ${g} green. P(not green)`, r + b, T);
        else if (t === 1) add(`Bag: ${r} red, ${b} blue, ${g} green. P(red or blue)`, r + b, T);
        else add(`Bag: ${r} red, ${b} blue, ${g} green. P(green)`, g, T);
      }
      add("Pick a number 1–10: it's a multiple of 3", 3, 10); add("Pick a letter of MATH: it's a vowel", 1, 4);
    } else {
      add("Flip two coins: both heads", 1, 4); add("Flip two coins: at least one head", 3, 4); add("Flip two coins: one head and one tail", 1, 2);
      add("Flip three coins: all heads", 1, 8); add("Flip three coins: at least one tail", 7, 8); add("Roll two number cubes: doubles", 6, 36);
      add("Roll two number cubes: the sum is 13", 0, 36); add("Roll two number cubes: the sum is 2 through 12", 36, 36); add("Roll two cubes: both even", 9, 36);
      add("Roll two cubes: the sum is 7", 6, 36); add("Flip a coin and roll a cube: heads and a 6", 1, 12); add("Roll two cubes: the sum is more than 3", 33, 36);
      add("Flip a coin and roll a cube: tails or a 6 (or both)", 7, 12); add("Roll two cubes: neither is a 6", 25, 36);
    }
    const n = c.n(c.lvl === 0 ? 5 : 6);
    const chosen = [];
    for (const e of c.shuffle(ev)) { if (chosen.length >= n) break; if (chosen.every(o => Math.abs(o.v - e.v) >= .085)) chosen.push(e); }
    const W = 680, Hh = 130, X0 = 40, X1 = 640, Y = 66;
    const X = v => X0 + (X1 - X0) * v;
    let s = `<svg viewBox="0 0 ${W} ${Hh}" role="img" aria-label="probability line from 0 to 1"><defs><linearGradient id="pg" x1="0" x2="1"><stop offset="0" stop-color="#d6453a" stop-opacity=".25"/><stop offset=".5" stop-color="#e0a21b" stop-opacity=".25"/><stop offset="1" stop-color="#1f9d64" stop-opacity=".25"/></linearGradient></defs><rect x="${X0}" y="${Y - 6}" width="${X1 - X0}" height="12" rx="6" fill="url(#pg)"/><line x1="${X0}" x2="${X1}" y1="${Y}" y2="${Y}" stroke="currentColor" stroke-width="2.5"/>`;
    for (let i = 0; i <= 12; i++) { const v = i / 12; s += `<line x1="${X(v)}" x2="${X(v)}" y1="${Y - (i % 6 ? 6 : 12)}" y2="${Y + (i % 6 ? 6 : 12)}" stroke="currentColor" stroke-width="${i % 6 ? 1.2 : 2.4}"/>`; }
    [[0, "0", "Impossible"], [.25, "", "Unlikely"], [.5, h.fmt(.5), "Equally likely"], [.75, "", "Likely"], [1, "1", "Certain"]].forEach(([v, t, w]) => { if (t) s += `<text x="${X(v)}" y="${Y + 30}" text-anchor="middle" font-size="15" font-weight="700" fill="currentColor">${t === "0.5" ? "½" : t}</text>`; s += `<text x="${X(v)}" y="${Y + 50}" text-anchor="middle" font-size="12" fill="currentColor" opacity=".75">${w}</text>`; });
    s += "</svg>";
    const spots = chosen.map((e, i) => ({ x: X(e.v), y: Y - 34, key: e.key, label: `Spot ${i + 1}` }));
    const cards = chosen.map(e => ({ html: e.text, cls: "txt", key: e.key, say: `P = ${e.key === "0/1" ? "0" : e.key === "1/1" ? "1" : e.key}` }));
    return { svg: s, w: W, h: Hh, spots, cards, trayTitle: "Events", fill: card => card.key === "0/1" ? "0" : card.key === "1/1" ? "1" : h.frac(...card.key.split("/")),
      why: card => c.mode === "practice" ? `Count: favorable outcomes ÷ total outcomes. This one is ${card.key === "0/1" ? "0" : card.key === "1/1" ? "1" : card.key}.` : "Count favorable outcomes and total outcomes." };
  }
});
