PG.game({
  id: "g6-data-designer", title: ["Data Set", "Designer"], course: "Grade 6", unit: "Statistics",
  tag: "Build a data set that has exactly the stats on the order.",
  skills: "6.SP.3, 6.SP.5 · mean, median, mode and range · how one value changes a statistic",
  engine: "build",
  levels: [
    "Three values with a given mean.",
    "Five values with a given median and range.",
    "Five values with a given mean AND median.",
    "Six values with a given mean, median and mode."
  ],
  how: ["Drag number cards into the boxes. The order of the boxes doesn't matter.", "Press Check when every box is full. Many data sets can work!"],
  round(c) {
    const st = v => { const s = v.slice().sort((a, b) => a - b), n = s.length; const mean = s.reduce((a, b) => a + b, 0) / n; const med = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; const cnt = {}; s.forEach(x => cnt[x] = (cnt[x] || 0) + 1); const mx = Math.max(...Object.values(cnt)); const modes = Object.keys(cnt).filter(k => cnt[k] === mx).map(Number); return { mean, med, range: s[n - 1] - s[0], mode: mx > 1 && modes.length === 1 ? modes[0] : null }; };
    const f = x => String(+x.toFixed(2));
    const N = c.n(5), puzzles = [];
    let g = 0;
    while (puzzles.length < N && g++ < 3000) {
      const k = [3, 5, 5, 6][c.lvl];
      const data = Array.from({ length: k }, () => c.ri(1, 15));
      const S = st(data);
      if (!Number.isInteger(S.mean) && c.lvl !== 1) continue;
      if (c.lvl === 3 && (S.mode == null || !Number.isInteger(S.med))) continue;
      if (S.range === 0) continue;
      const need = c.lvl === 0 ? ["mean"] : c.lvl === 1 ? ["med", "range"] : c.lvl === 2 ? ["mean", "med"] : ["mean", "med", "mode"];
      const NAME = { mean: "Mean", med: "Median", range: "Range", mode: "Mode" };
      const decoys = []; while (decoys.length < (c.lvl ? 4 : 3)) { const d = c.ri(1, 18); decoys.push(d); }
      const cards = c.shuffle(data.concat(decoys)).map(v => ({ html: String(v), v }));
      const answer = []; data.forEach(v => answer.push(cards.findIndex((x, j) => x.v === v && !answer.includes(j))));
      const parts = ["{ "]; for (let i = 0; i < k; i++) { parts.push({}); if (i < k - 1) parts.push(", "); } parts.push(" }");
      puzzles.push({
        prompt: need.map(s => `<div><small>${NAME[s]}</small><div class="big">${f(S[s])}</div></div>`).join(""),
        parts, cards, answer,
        show: v => { const vv = v.filter(x => x != null); if (vv.length < 2) return ""; const s2 = st(vv); return need.filter(s => s !== "mode" || vv.length === k).map(s => `${NAME[s]} so far: ${s2[s] == null ? "none" : f(s2[s])}`).join(" · "); },
        test: v => { const s2 = st(v); const bad = need.filter(s => s2[s] == null || Math.abs(s2[s] - S[s]) > 1e-9); return bad.length ? bad.map(s => `${NAME[s]} is ${s2[s] == null ? "none (no single most common value)" : f(s2[s])}, needs to be ${f(S[s])}.`).join(" ") : true; },
        say: "That data set fits the order!"
      });
    }
    return { puzzles, note: "Order doesn't matter: the stats are worked out from the sorted list." };
  }
});
