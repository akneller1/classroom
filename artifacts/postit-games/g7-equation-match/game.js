PG.game({
  id: "g7-equation-match", title: ["Equation", "Solution Match"], course: "Grade 7", unit: "Equations & Inequalities",
  tag: "Match each equation or inequality to its solution.",
  skills: "7.EE.4 · two-step equations · distributive property · inequalities and the sign flip · graphing solutions",
  engine: "match",
  levels: [
    "Two-step equations with positive whole numbers.",
    "Two-step equations with negatives.",
    "Parentheses and fractions: 3(x − 2) = 12, x/4 + 3 = 5.",
    "Inequalities matched to number-line graphs. Dividing by a negative flips the sign!"
  ],
  options: [{ id: "style", label: "Play style", type: "one", choices: [["open", "Open cards"], ["memory", "Memory (face down)"]], default: "open" }],
  round(c) {
    const { h } = c; const M = h.MINUS; const X = h.v("x");
    const F = h.fmt, P = x => x < 0 ? `(${F(x)})` : F(x);
    const lin = (a, b) => h.terms([[a, X], [b, ""]]);
    const nl = (v, op) => {
      const W = 220, lo = v - 5, X0 = 12, X1 = 208, x = t => X0 + (X1 - X0) * (t - lo) / 10, Yy = 26, open = op === "<" || op === ">", left = op === "<" || op === "≤";
      let s = `<svg viewBox="0 0 ${W} 44" width="${W}" aria-label="number line: ${open ? "open" : "closed"} circle at ${v}, arrow ${left ? "left" : "right"}">`;
      s += `<line x1="4" x2="${W - 4}" y1="${Yy}" y2="${Yy}" stroke="#13202f" stroke-width="1.5"/>`;
      for (let t = lo; t <= lo + 10; t++) s += `<line x1="${x(t)}" x2="${x(t)}" y1="${Yy - 4}" y2="${Yy + 4}" stroke="#13202f" stroke-width="1"/>` + ((t - v) % 2 === 0 ? `<text x="${x(t)}" y="${Yy + 15}" font-size="9" text-anchor="middle" fill="#13202f">${F(t)}</text>` : "");
      const end = left ? 4 : W - 4;
      s += `<line x1="${x(v)}" x2="${end}" y1="${Yy}" y2="${Yy}" stroke="#2f5bd3" stroke-width="4"/><path d="M${end} ${Yy} l${left ? 8 : -8} -6 v12z" fill="#2f5bd3"/><circle cx="${x(v)}" cy="${Yy}" r="5" fill="${open ? "#fff" : "#2f5bd3"}" stroke="#2f5bd3" stroke-width="2.4"/>`;
      return s + "</svg>";
    };
    const N = c.n(6), pairs = [], used = new Set();
    let g = 0;
    while (pairs.length < N && g++ < 600) {
      let eq, sol, b, key, say = null;
      const x = c.lvl === 0 ? c.ri(1, 12) : c.ri(-10, 10);
      if (used.has(x) && c.lvl < 3) continue;
      if (c.lvl === 0) { const a = c.ri(2, 9), k = c.ri(1, 20); eq = `${lin(a, k)} = ${a * x + k}`; }
      else if (c.lvl === 1) { const a = c.nz(-9, 9), k = c.ri(-15, 15); if (Math.abs(a) === 1) continue; eq = `${lin(a, k)} = ${F(a * x + k)}`; }
      else if (c.lvl === 2) {
        const t = c.ri(0, 2);
        if (t === 0) { const a = c.nz(-5, 5), k = c.nz(-6, 6); if (Math.abs(a) === 1) continue; eq = `${F(a)}(${lin(1, k)}) = ${F(a * (x + k))}`; }
        else if (t === 1) { const d = c.pick([2, 3, 4, 5]); if (x % d) continue; const k = c.ri(-8, 8); eq = `${h.frac(X, d)} ${k < 0 ? M : "+"} ${Math.abs(k)} = ${F(x / d + k)}`; }
        else { const k = c.nz(-6, 6); eq = `${M}(${lin(1, k)}) = ${F(-(x + k))}`; }
      } else {
        const a = c.nz(-6, 6), k = c.ri(-9, 9); if (Math.abs(a) === 1) continue;
        const op = c.pick(["<", ">", "≤", "≥"]);
        const flip = a < 0; const sop = flip ? { "<": ">", ">": "<", "≤": "≥", "≥": "≤" }[op] : op;
        key = sop + x; if (used.has(key)) continue; used.add(key);
        eq = `${lin(a, k)} ${op} ${F(a * x + k)}`;
        pairs.push({ a: { html: eq, cls: "mth" }, b: { html: nl(x, sop), cls: "pic", label: `x ${sop} ${x}` }, key, say: `x ${sop} ${F(x)}${flip ? " (the sign flipped when dividing by a negative)" : ""}.` });
        continue;
      }
      used.add(x);
      pairs.push({ a: { html: eq, cls: "mth" }, b: { html: `${X} = ${F(x)}`, cls: "mth" } });
    }
    return { pairs, style: c.opt.style, aTitle: c.lvl === 3 ? "Inequalities" : "Equations", bTitle: "Solutions", cw: c.lvl === 3 ? "230px" : "160px",
      why: (a, b) => c.mode === "practice" ? (c.lvl === 3 ? "Solve like an equation. If you multiply or divide by a negative, flip the inequality sign. Open circle for < or >, closed for ≤ or ≥." : "Substitute the solution back in: does it make the equation true?") : "Not a match." };
  }
});
