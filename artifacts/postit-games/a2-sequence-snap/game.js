PG.game({
  id: "a2-sequence-snap", title: ["Sequence", "Snap"], course: "Algebra 2", unit: "Sequences & Series",
  tag: "Snap the next term of the sequence before it falls.",
  skills: "F.BF.2, F.LE.2 · arithmetic and geometric sequences · negative and fractional ratios · recursive rules",
  engine: "drop",
  levels: [
    "Arithmetic sequences.",
    "Geometric sequences with whole-number ratios.",
    "Fractional and negative ratios, and arithmetic with fractions.",
    "Recursive and quadratic patterns: aₙ = 2aₙ₋₁ + 1, Fibonacci-style, n² + 1…"
  ],
  options: [{ id: "board", label: "Board", type: "one", choices: [["fall", "Falling cards"], ["calm", "Calm board (no motion)"]], default: "fall" }],
  round(c) {
    const { h } = c; const F = x => h.fmt(+x.toFixed(4));
    const newSeq = st => {
      const L = c.lvl; let t = [];
      if (L === 0) { const a = c.ri(-10, 20), d = c.nz(-9, 9); for (let i = 0; i < 12; i++) t.push(a + d * i); st.rule = `add ${F(d)}`; }
      else if (L === 1) { const a = c.nz(-5, 5), r = c.pick([2, 3, 2, -2, 4]); for (let i = 0; i < 9; i++) t.push(a * r ** i); st.rule = `multiply by ${F(r)}`; }
      else if (c.chance(.6)) { const r = c.pick([.5, -.5, -3, -2, 1.5]); const a = r === 1.5 ? 16 : r === .5 || r === -.5 ? c.pick([64, 96, 128, -64]) : c.nz(-3, 3); for (let i = 0; i < 8; i++) t.push(a * r ** i); st.rule = `multiply by ${F(r)}`; }
      else { const a = c.ri(-4, 4), d = c.pick([.5, -.5, 1.5, -2.5, .25]); for (let i = 0; i < 12; i++) t.push(a + d * i); st.rule = `add ${F(d)}`; }
      if (L === 3) {
        const k = c.ri(0, 3);
        if (k === 0) { let x = c.ri(1, 4); t = []; for (let i = 0; i < 9; i++) { t.push(x); x = 2 * x + 1; } st.rule = "double, then add 1"; }
        else if (k === 1) { let a = c.ri(1, 3), b = c.ri(2, 5); t = [a, b]; for (let i = 2; i < 11; i++) t.push(t[i - 1] + t[i - 2]); st.rule = "add the two previous terms"; }
        else if (k === 2) { const s = c.ri(0, 3), q = c.ri(-2, 2); t = []; for (let n = 1; n < 12; n++) t.push(n * n + q * n + s); st.rule = "second differences are constant (quadratic)"; }
        else { let x = c.ri(2, 5); t = []; for (let i = 0; i < 9; i++) { t.push(x); x = 3 * x - 2; } st.rule = "triple, then subtract 2"; }
      }
      st.t = t; st.k = 4;
    };
    const ensure = st => { if (!st.t) newSeq(st); };
    return {
      goal: c.n(16), calm: c.opt.board === "calm", size: 120, speed: .85,
      ready: "Look at the sequence above the board. Tap only the NEXT term.",
      head(st) { ensure(st); return `<div><small>Next term?</small><div class="big">${st.t.slice(0, st.k).map(F).join(", ")}, ?</div></div>`; },
      make(st, good) {
        ensure(st); const nx = st.t[st.k], pv = st.t[st.k - 1], d = pv - st.t[st.k - 2];
        if (good) return { html: F(nx), key: F(nx) };
        const opts = [pv + d, nx + d, nx - d, pv * 2, -nx, nx + 1, nx - 1, st.t[st.k + 1], pv].filter(v => v != null && isFinite(v) && F(v) !== F(nx));
        const v = c.pick(opts); return v == null ? null : { html: F(v), key: F(v) };
      },
      test(key, st) { ensure(st); return key === F(st.t[st.k]) ? true : `The rule is “${st.rule}”, so the next term is ${F(st.t[st.k])}.`; },
      onHit(st) { st.k++; if (st.k >= Math.min(st.t.length, 7)) newSeq(st); }
    };
  }
});
