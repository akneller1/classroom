PG.game({
  id: "g3-array-match", title: ["Array", "Match"], course: "Grade 3", unit: "Multiplication & Division",
  tag: "Match each array or fact to its partner.",
  skills: "3.OA.1, 3.OA.6, 3.OA.7, 3.OA.5 · arrays · repeated addition · unknown factors · break-apart (distributive) strategy",
  engine: "match",
  levels: [
    "Arrays matched to multiplication facts (rows × columns).",
    "Arrays matched to repeated addition.",
    "Unknown-factor facts matched to division (? × 6 = 42 goes with 42 ÷ 6).",
    "Break-apart facts: 7 × 8 matches 7 × 5 + 7 × 3. Every product is different."
  ],
  options: [{ id: "style", label: "Play style", type: "one", choices: [["open", "Open cards"], ["memory", "Memory (face down)"]], default: "open" }],
  round(c) {
    const arr = (r, k) => { const g = 13, w = k * g + 6, h = r * g + 6; let s = `<svg viewBox="0 0 ${w} ${h}" width="${Math.min(w * 1.3, 140)}" aria-label="array of ${r} rows of ${k}">`; for (let i = 0; i < r; i++) for (let j = 0; j < k; j++) s += `<circle cx="${3 + g / 2 + j * g}" cy="${3 + g / 2 + i * g}" r="4.6" fill="#13202f"/>`; return s + "</svg>"; };
    const N = c.n(6), pairs = [], seen = new Set();
    let guard = 0;
    while (pairs.length < N && guard++ < 500) {
      if (c.lvl <= 1) {
        const r = c.ri(2, c.lvl ? 6 : 5), k = c.ri(2, c.lvl ? 7 : 6); const key = [Math.min(r, k), Math.max(r, k)].join("x"); if (seen.has(key) || (c.lvl === 1 && r * k > 30)) continue; seen.add(key);
        const b = c.lvl === 0 ? { html: `${r} × ${k}` } : { html: Array(r).fill(k).join(" + "), cls: r > 4 ? "txt" : "" };
        pairs.push({ a: { html: arr(r, k), label: `${r} rows of ${k}`, cls: "pic" }, b, say: `${r} rows of ${k} is ${r} × ${k} = ${r * k}.` });
      } else if (c.lvl === 2) {
        const a = c.ri(2, 9), b = c.ri(3, 9), p = a * b; if (seen.has(p) || seen.has("q" + a)) continue; seen.add(p); seen.add("q" + a);
        const form = c.pick([`? × ${b} = ${p}`, `${b} × ? = ${p}`]);
        pairs.push({ a: { html: form }, b: { html: `${p} ÷ ${b}` }, say: `${form.replace("?", a)}, so ${p} ÷ ${b} = ${a}.` });
      } else {
        const a = c.ri(3, 9), b = c.ri(6, 9), p = a * b; if (seen.has(p)) continue;
        const s1 = c.ri(2, b - 2), s2 = b - s1; seen.add(p);
        const split = c.chance(.5) ? `${a} × ${s1} + ${a} × ${s2}` : `${s1} × ${a} + ${s2} × ${a}`;
        pairs.push({ a: { html: `${a} × ${b}` }, b: { html: split, cls: "txt" }, say: `${a} × ${b} = ${a * s1} + ${a * s2} = ${p}.` });
      }
    }
    return { pairs, style: c.opt.style, aTitle: c.lvl <= 1 ? "Arrays" : "Facts", bTitle: "Partners", cw: "150px",
      why: (a, b) => c.lvl <= 1 ? "Count the rows, then how many are in each row." : "Check: do both cards use the same numbers in a true fact family?" };
  }
});
