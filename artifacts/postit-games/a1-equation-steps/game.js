PG.game({
  id: "a1-equation-steps", title: ["Equation", "Step Stack"], course: "Algebra 1", unit: "Solving Linear Equations",
  tag: "Stack the steps of each solution in the right order.",
  skills: "A.REI.1, A.REI.3 · inverse operations · distributing · variables on both sides · clearing fractions",
  engine: "order",
  levels: [
    "Two-step equations: four lines to order.",
    "Distribute and combine first: five lines.",
    "Variables on both sides: six lines.",
    "Fractions on both sides: cross-multiply and finish. You check the order yourself."
  ],
  how: ["The first line is the original equation. Each line after it follows from the one above.", "Put the cards in order from top (first) to bottom (last)."],
  round(c) {
    const { h } = c; const X = h.v("x"), F = h.fmt, M = h.MINUS;
    const L = (a, b) => h.terms([[a, X], [b, ""]]);
    const x = c.nz(-9, 9);
    let lines;
    if (c.lvl === 0) { const a = c.nz(-7, 7), b = c.nz(-12, 12); if (Math.abs(a) === 1) return this.round(c); const r = a * x + b; lines = [`${L(a, b)} = ${F(r)}`, `${L(a, b)} ${b > 0 ? M : "+"} ${Math.abs(b)} = ${F(r)} ${b > 0 ? M : "+"} ${Math.abs(b)}`, `${L(a, 0)} = ${F(r - b)}`, `${X} = ${F(x)}`]; }
    else if (c.lvl === 1) { const a = c.ri(2, 6), p = c.nz(-6, 6), q = c.nz(-9, 9); const r = a * (x + p) + q; lines = [`${a}(${L(1, p)}) ${q < 0 ? M : "+"} ${Math.abs(q)} = ${F(r)}`, `${L(a, a * p)} ${q < 0 ? M : "+"} ${Math.abs(q)} = ${F(r)}`, `${L(a, a * p + q)} = ${F(r)}`, `${L(a, 0)} = ${F(r - a * p - q)}`, `${X} = ${F(x)}`]; if (a * p + q === 0) return this.round(c); }
    else if (c.lvl === 2) {
      const a = c.ri(3, 8), cc = c.ri(1, a - 1), k = a - cc, p = c.nz(-6, 6), e = c.nz(-9, 9);
      if (k === 1 || a * p + e === 0) return this.round(c);
      const d = k * x + a * p + e;
      lines = [`${a}(${L(1, p)}) ${e < 0 ? M : "+"} ${Math.abs(e)} = ${L(cc, d)}`, `${h.terms([[a, X], [a * p, ""], [e, ""]])} = ${L(cc, d)}`, `${L(a, a * p + e)} = ${L(cc, d)}`, `${L(k, a * p + e)} = ${F(d)}`, `${L(k, 0)} = ${F(d - a * p - e)}`, `${X} = ${F(x)}`];
    }
    else {
      const a = c.ri(2, 5); let b; do { b = c.ri(2, 6); } while (b === a); const p = c.nz(-6, 6);
      // (x + p)/a = (x + q)/b  with solution x  ->  q = b(x + p)/a - x must be integer
      if ((b * (x + p)) % a) return this.round(c);
      const q = b * (x + p) / a - x; if (q === 0 || q === p) return this.round(c);
      lines = [`${h.frac(L(1, p), a)} = ${h.frac(L(1, q), b)}`, `${b}(${L(1, p)}) = ${a}(${L(1, q)})`, `${L(b, b * p)} = ${L(a, a * q)}`, `${L(b - a, b * p)} = ${F(a * q)}`, `${L(b - a, 0)} = ${F(a * q - b * p)}`, `${X} = ${F(x)}`];
      if (b - a === 1) lines.splice(4, 1);
    }
    const uniq = [...new Set(lines)]; if (uniq.length !== lines.length) return this.round(c);
    const cards = lines.map((t, i) => ({ html: t, v: i, cls: "mth" }));
    return { cards, vertical: true, lo: "First step", hi: "the solution", endCheck: c.lvl === 3,
      why: card => c.mode === "practice" ? "Each line should come from the line right above it by ONE move: distribute, combine, or do the same thing to both sides." : "" };
  }
});
