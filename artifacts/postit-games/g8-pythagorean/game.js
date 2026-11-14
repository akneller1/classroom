PG.game({
  id: "g8-pythagorean", title: ["Pythagorean", "Picker"], course: "Grade 8", unit: "The Pythagorean Theorem",
  tag: "Pick the side lengths that make a right triangle.",
  skills: "8.G.6–7 · a² + b² = c² · missing hypotenuse or leg · converse of the theorem · irrational side lengths",
  engine: "target",
  levels: [
    "Find the hypotenuse from the two legs.",
    "Find the missing leg from the hypotenuse and one leg.",
    "Pick three lengths that make a right triangle (and avoid the near misses).",
    "Square roots: pick three lengths like √7, 3 and 4 that make a right triangle."
  ],
  round(c) {
    const { h } = c;
    const triples = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [9, 40, 41], [6, 8, 10], [9, 12, 15], [12, 16, 20], [15, 20, 25], [10, 24, 26], [12, 35, 37]];
    const rootHtml = sq => { const r = Math.round(Math.sqrt(sq)); if (r * r === sq) return String(r); let k = 1, m = sq; for (let i = 2; i * i <= sq; i++) while (m % (i * i) === 0) { m /= i * i; k *= i; } return (k > 1 ? k : "") + h.sqrt(m); };
    const card = sq => ({ html: rootHtml(sq), v: sq, label: PG.textify(rootHtml(sq)), cls: Math.sqrt(sq) % 1 ? "mth" : "" });
    const tri = (a, b, cc, hide) => `<svg viewBox="0 0 170 110" width="170" aria-hidden="true"><path d="M20 95 H150 V15 Z" fill="none" stroke="currentColor" stroke-width="2.5"/><path d="M140 95 V85 H150" fill="none" stroke="currentColor" stroke-width="1.5"/><text x="85" y="108" text-anchor="middle" font-size="14" font-weight="700" fill="currentColor">${hide === "a" ? "?" : a}</text><text x="158" y="58" font-size="14" font-weight="700" fill="currentColor">${hide === "b" ? "?" : b}</text><text x="72" y="48" text-anchor="end" font-size="14" font-weight="700" fill="currentColor">${hide === "c" ? "?" : cc}</text></svg>`;
    const N = c.n(7), puzzles = [];
    for (let p = 0; p < N; p++) {
      const T = c.pick(triples);
      if (c.lvl <= 1) {
        const hide = c.lvl === 0 ? "c" : c.pick(["a", "b"]);
        const ans = hide === "c" ? T[2] : hide === "a" ? T[0] : T[1];
        const nums = new Set([ans]);
        const near = hide === "c" ? [T[0] + T[1], T[2] + 1, T[2] - 1, T[2] ** 2] : [T[2] - (hide === "a" ? T[1] : T[0]), ans + 1, ans + 2, ans - 1];
        near.forEach(v => v > 0 && nums.add(v));
        const cards = c.shuffle([...nums].slice(0, 5)).map(v => ({ html: String(v), v }));
        puzzles.push({ prompt: tri(T[0], T[1], T[2], hide) + `<div><small>Pick the missing</small><b>${hide === "c" ? "hypotenuse" : "leg"}</b></div>`, cards, k: 1, answer: [cards.findIndex(x => x.v === ans)],
          test: v => v[0] === ans ? true : `Check: ${hide === "c" ? `${T[0]}² + ${T[1]}² = ${T[0] ** 2 + T[1] ** 2}, and ${v[0]}² = ${v[0] ** 2}` : `${T[2]}² − ${hide === "a" ? T[1] : T[0]}² = ${T[2] ** 2 - (hide === "a" ? T[1] : T[0]) ** 2}, and ${v[0]}² = ${v[0] ** 2}`}.`,
          say: `${T[0]}² + ${T[1]}² = ${T[2]}²` });
      } else if (c.lvl === 2) {
        const nums = new Set(T);
        while (nums.size < 7) nums.add(c.pick([T[2] + 1, T[2] - 1, T[0] + 1, T[1] + 2, T[0] + T[1], c.ri(2, 30)]));
        const cards = c.shuffle([...nums]).map(v => ({ html: String(v), v: v * v, label: String(v) }));
        puzzles.push({ prompt: `<div><small>Pick 3 lengths that make a</small><div class="big">right triangle</div></div>`, cards, k: 3, answer: T.map(t => cards.findIndex(x => x.v === t * t)),
          show: v => { const s = v.slice().sort((a, b) => a - b); return s.length === 3 ? `${Math.sqrt(s[0])}² + ${Math.sqrt(s[1])}² = ${s[0] + s[1]}, ${Math.sqrt(s[2])}² = ${s[2]}` : ""; },
          test: v => { const s = v.slice().sort((a, b) => a - b); return s[0] + s[1] === s[2] ? true : `${Math.sqrt(s[0])}² + ${Math.sqrt(s[1])}² = ${s[0] + s[1]}, but ${Math.sqrt(s[2])}² = ${s[2]}. Not a right triangle.`; } });
      } else {
        let a2, b2; do { a2 = c.ri(2, 30); b2 = c.ri(2, 30); } while (a2 === b2 || (Number.isInteger(Math.sqrt(a2)) && Number.isInteger(Math.sqrt(b2)) && Number.isInteger(Math.sqrt(a2 + b2))));
        const sqs = new Set([a2, b2, a2 + b2]);
        while (sqs.size < 7) sqs.add(c.pick([a2 + b2 + 1, a2 + b2 - 1, Math.abs(a2 - b2) || 3, a2 * 2, b2 + 1, c.ri(2, 50)]));
        const cards = c.shuffle([...sqs]).map(card);
        puzzles.push({ prompt: `<div><small>Pick 3 lengths that make a</small><div class="big">right triangle</div></div><div><small>Remember</small><b>(√n)² = n</b></div>`, cards, k: 3, answer: [a2, b2, a2 + b2].map(t => cards.findIndex(x => x.v === t)),
          show: v => { const s = v.slice().sort((a, b) => a - b); return s.length === 3 ? `squares: ${s[0]} + ${s[1]} = ${s[0] + s[1]} vs ${s[2]}` : ""; },
          test: v => { const s = v.slice().sort((a, b) => a - b); return s[0] + s[1] === s[2] ? true : `The squares are ${s.join(", ")}. ${s[0]} + ${s[1]} = ${s[0] + s[1]}, not ${s[2]}.`; } });
      }
    }
    return { puzzles, cw: "96px" };
  }
});
