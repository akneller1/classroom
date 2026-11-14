PG.game({
  id: "g5-fraction-match", title: ["Fraction Operation", "Match"], course: "Grade 5", unit: "Fraction Operations",
  tag: "Match each fraction problem to its answer.",
  skills: "5.NF.1, 5.NF.4, 5.NF.7 · add and subtract unlike denominators · mixed numbers · multiply and divide fractions",
  engine: "match",
  levels: [
    "Add or subtract when one denominator is a multiple of the other (1/2 + 1/4).",
    "Unlike denominators (1/3 + 1/4).",
    "Mixed numbers, with regrouping (3 1/4 − 1 2/3).",
    "Multiply and divide: fractions, whole numbers and unit fractions."
  ],
  options: [{ id: "style", label: "Play style", type: "one", choices: [["open", "Open cards"], ["memory", "Memory (face down)"]], default: "open" }],
  round(c) {
    const { h, Q } = c;
    const show = (q, mixed = true) => { if (q.d === 1) return h.fmt(q.n); if (mixed && Math.abs(q.n) > q.d) { const w = Math.trunc(q.n / q.d), r = Math.abs(q.n % q.d); return (q.n < 0 ? h.MINUS : "") + h.mixed(Math.abs(w), r, q.d); } return h.f(q.n, q.d); };
    const mx = q => { const w = Math.floor(q.n / q.d), r = q.n - w * q.d; return w ? h.mixed(w, r, q.d) : h.frac(r, q.d); };
    const N = c.n(6), pairs = [], used = new Set();
    let g = 0;
    while (pairs.length < N && g++ < 800) {
      let A, B, op, res, aH;
      if (c.lvl === 0) { const d1 = c.pick([2, 3, 4, 5]), m = c.pick([2, 3]), d2 = d1 * m; A = Q(c.ri(1, d1 - 1), d1); B = Q(c.ri(1, d2 - 1), d2); op = c.pick(["+", "−"]); }
      else if (c.lvl === 1) { const [d1, d2] = c.sample([2, 3, 4, 5, 6, 8], 2); if ((d1 % d2 === 0) || (d2 % d1 === 0)) continue; A = Q(c.ri(1, d1 - 1), d1); B = Q(c.ri(1, d2 - 1), d2); op = c.pick(["+", "−"]); }
      else if (c.lvl === 2) { const [d1, d2] = c.sample([2, 3, 4, 5, 6, 8], 2); A = Q(c.ri(1, 4) * d1 + c.ri(1, d1 - 1), d1); B = Q(c.ri(1, 3) * d2 + c.ri(1, d2 - 1), d2); op = c.pick(["+", "−"]); }
      else {
        const t = c.ri(0, 3);
        if (t === 0) { A = Q(c.ri(1, 5), c.ri(2, 8)); B = Q(c.ri(1, 5), c.ri(2, 8)); op = "×"; }
        else if (t === 1) { A = Q(c.ri(2, 12), 1); B = Q(c.ri(1, 4), c.pick([3, 4, 5, 6])); op = "×"; }
        else if (t === 2) { A = Q(c.ri(2, 9), 1); B = Q(1, c.pick([2, 3, 4, 5, 6])); op = "÷"; }
        else { A = Q(1, c.pick([2, 3, 4, 5])); B = Q(c.ri(2, 6), 1); op = "÷"; }
      }
      if (A.d === 1 && B.d === 1) continue;
      res = op === "+" ? Q.add(A, B) : op === "−" ? Q.sub(A, B) : op === "×" ? Q.mul(A, B) : Q.div(A, B);
      if (res.n <= 0) { if (op === "−") { [A, B] = [B, A]; res = Q.sub(A, B); } if (res.n <= 0) continue; }
      const key = res.n + "/" + res.d; if (used.has(key)) continue; used.add(key);
      const fa = q => c.lvl === 2 ? mx(q) : h.f(q.n, q.d);
      aH = `${fa(A)} ${op} ${fa(B)}`;
      pairs.push({ a: { html: aH, cls: "mth" }, b: { html: show(res), cls: "mth" }, say: null });
    }
    return { pairs, style: c.opt.style, aTitle: "Problems", bTitle: "Answers", cw: "150px",
      why: (a, b) => c.mode === "practice" ? (c.lvl < 3 ? "Find a common denominator first, then add or subtract the numerators." : "To multiply, multiply tops and bottoms. To divide, multiply by the reciprocal.") + " Answers are in simplest form." : "Not a match." };
  }
});
