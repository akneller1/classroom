PG.game({
  id: "a1-factor-builder", title: ["Factor", "Builder"], course: "Algebra 1", unit: "Factoring",
  tag: "Drag number cards into the factors so they multiply back to the polynomial.",
  skills: "A.SSE.2, A.SSE.3a · factoring trinomials · a ≠ 1 · greatest common factor · difference of squares",
  engine: "build",
  levels: [
    "x² + bx + c with positive numbers.",
    "x² + bx + c with negatives (signed cards).",
    "ax² + bx + c: four boxes to fill.",
    "Factor completely: pull out the GCF first, or spot a difference of squares."
  ],
  how: ["Fill the boxes, then press Check. Your factors are multiplied out and compared with the polynomial.", "Order doesn't matter: (x + 2)(x + 3) and (x + 3)(x + 2) are both right."],
  round(c) {
    const { h } = c; const X = h.v("x"); const M = h.MINUS;
    const sgn = n => (n < 0 ? M + Math.abs(n) : "+" + n);
    const poly = (a, b, cc) => h.poly([a, b, cc]);
    const N = c.n(6), puzzles = [];
    const deck = (need, extra, signed) => {
      const nums = need.slice(); let g = 0;
      while (nums.length < need.length + extra && g++ < 300) { const base = c.pick(need); const d = c.pick([1, -1, 2, -2]) * (c.chance(.5) ? 1 : base || 1); let x = signed && c.chance(.4) ? -base : base + c.pick([1, -1, 2, -2, 3]); if (!signed && x <= 0) continue; if (x === 0 || Math.abs(x) > 15) continue; if (nums.filter(y => y === x).length >= 1) continue; nums.push(x); }
      const cards = c.shuffle(nums).map(v => ({ html: signed ? sgn(v) : String(v), v }));
      const answer = []; need.forEach(v => answer.push(cards.findIndex((x, j) => x.v === v && !answer.includes(j))));
      return { cards, answer };
    };
    let g = 0;
    while (puzzles.length < N && g++ < 500) {
      if (c.lvl <= 1) {
        const p = c.lvl === 0 ? c.ri(1, 9) : c.nz(-9, 9), q = c.lvl === 0 ? c.ri(1, 9) : c.nz(-9, 9);
        const B = p + q, C = p * q; if (B === 0 && c.lvl === 0) continue;
        const { cards, answer } = deck([p, q], 4, c.lvl === 1);
        const parts = c.lvl === 0 ? ["(", X, " + ", {}, ")(", X, " + ", {}, ")"] : ["(", X, " ", {}, ")(", X, " ", {}, ")"];
        puzzles.push({ prompt: `<div class="big mth">${poly(1, B, C)}</div>`, parts, cards, answer,
          show: v => v.every(x => x != null) ? `Multiplies to ${poly(1, v[0] + v[1], v[0] * v[1])}` : "",
          test: v => v[0] + v[1] === B && v[0] * v[1] === C ? true : `That multiplies to ${poly(1, v[0] + v[1], v[0] * v[1])}. You need two numbers that multiply to ${h.fmt(C)} and add to ${h.fmt(B)}.` });
      } else if (c.lvl === 2) {
        const a1 = c.pick([1, 2, 3]), a2 = c.pick([2, 3, 5]), b1 = c.nz(-5, 5), b2 = c.nz(-5, 5);
        if (h.gcd(a1, b1) > 1 || h.gcd(a2, b2) > 1) continue;
        const A = a1 * a2, B = a1 * b2 + a2 * b1, C = b1 * b2; if (B === 0) continue;
        const need = [a1, b1, a2, b2];
        const coefs = [a1, a2]; while (coefs.length < 3) { const x = c.pick([1, 2, 3, 4, 5, 6]); if (!coefs.includes(x)) coefs.push(x); }
        const consts = [b1, b2]; let gg = 0; while (consts.length < 5 && gg++ < 50) { const x = c.pick([-b1, -b2, b1 + 1, b2 - 1, b1 * b2, c.nz(-6, 6)]); if (x && !consts.includes(x) && Math.abs(x) < 20) consts.push(x); }
        const cards = c.shuffle(coefs.map(v => ({ html: String(v), v })).concat(consts.map(v => ({ html: sgn(v), v, kind: "b" }))));
        const answer = []; need.forEach((v, i) => answer.push(cards.findIndex((x, j) => x.v === v && (i % 2 === 1) === (x.kind === "b") && !answer.includes(j))));
        puzzles.push({ prompt: `<div class="big mth">${poly(A, B, C)}</div>`, parts: ["(", {}, X, " ", {}, ")(", {}, X, " ", {}, ")"], cards, answer,
          show: v => v.every(x => x != null) ? `Multiplies to ${poly(v[0] * v[2], v[0] * v[3] + v[1] * v[2], v[1] * v[3])}` : "",
          test: v => { const a = v[0] * v[2], b = v[0] * v[3] + v[1] * v[2], cc = v[1] * v[3]; return a === A && b === B && cc === C ? true : `That multiplies to ${poly(a, b, cc)}.${a !== A ? " Check the x² term first." : cc !== C ? " Check the constants." : " The outer + inner terms don't add up to the middle term."}`; } });
      } else {
        if (c.chance(.5)) {
          const k = c.ri(2, 5), p = c.nz(-6, 6), q = c.nz(-6, 6); if (p + q === 0) continue;
          const need = [k, p, q]; const { cards, answer } = deck(need, 4, true); // Keep signed cards: a coefficient value can also occupy a binomial constant slot.
          puzzles.push({ prompt: `<div class="big mth">${poly(k, k * (p + q), k * p * q)}</div><div><small>factor</small><b>completely</b></div>`, parts: [{}, "(", X, " ", {}, ")(", X, " ", {}, ")"], cards, answer,
            show: v => v.every(x => x != null) ? `Multiplies to ${poly(v[0], v[0] * (v[1] + v[2]), v[0] * v[1] * v[2])}` : "",
            test: v => v[0] === k && v[1] + v[2] === p + q && v[1] * v[2] === p * q ? true : v[0] * 1 !== k && v[0] * (v[1] + v[2]) === k * (p + q) && v[0] * v[1] * v[2] === k * p * q ? "Equal, but not factored completely: pull out the greatest common factor." : `That multiplies to ${poly(v[0], v[0] * (v[1] + v[2]), v[0] * v[1] * v[2])}.` });
        } else {
          const a = c.ri(1, 5), b = c.ri(1, 9); if (h.gcd(a, b) > 1) continue;
          const need = [a, b, a, b];
          const nums = [a, b, a, b, a + 1, b + 1, a * a, b * b].filter((x, i, arr) => i < 4 || !arr.slice(0, i).includes(x));
          const cards = c.shuffle(nums).map(v => ({ html: String(v), v }));
          const answer = []; need.forEach(v => answer.push(cards.findIndex((x, j) => x.v === v && !answer.includes(j))));
          puzzles.push({ prompt: `<div class="big mth">${h.terms([[a * a, X + "<sup>2</sup>"], [-b * b, ""]])}</div><div><small>difference of</small><b>squares</b></div>`, parts: ["(", {}, X, " + ", {}, ")(", {}, X, " " + M + " ", {}, ")"], cards, answer,
            show: v => v.every(x => x != null) ? `Multiplies to ${poly(v[0] * v[2], v[1] * v[2] - v[0] * v[3], -v[1] * v[3])}` : "",
            test: v => { const A2 = v[0] * v[2], B2 = -v[0] * v[3] + v[1] * v[2], C2 = -v[1] * v[3]; return A2 === a * a && B2 === 0 && C2 === -b * b ? true : `That multiplies to ${poly(A2, B2, C2)}.`; } });
        }
      }
    }
    return { puzzles };
  }
});
