PG.game({
  id: "g7-integer-drop", title: ["Integer", "Drop"], course: "Grade 7", unit: "Operations with Rational Numbers",
  tag: "Snap every expression that equals the target. Sign errors are everywhere!",
  skills: "7.NS.1–3 · add, subtract, multiply and divide integers and rational numbers · sign rules",
  engine: "drop",
  levels: [
    "Adding and subtracting integers.",
    "Multiplying and dividing integers.",
    "Two-step expressions: −2(3 − 7), −12 ÷ 3 + 1.",
    "Rational numbers: −½ × 8, 2.5 − 6.5, −0.75 × 4."
  ],
  options: [{ id: "board", label: "Board", type: "one", choices: [["fall", "Falling cards"], ["calm", "Calm board (no motion)"]], default: "fall" }],
  round(c) {
    const { h } = c; const M = h.MINUS;
    const F = x => h.fmt(x), P = x => x < 0 ? `(${F(x)})` : F(x);
    const vals = {};
    const half = x => { const a = Math.abs(x); const s = x < 0 ? M : ""; if (a === .5) return s + "½"; if (a === .25) return s + "¼"; if (a === .75) return s + "¾"; return F(x); };
    const expr = V => {
      const L = c.lvl;
      for (let t = 0; t < 40; t++) {
        let s = null;
        if (L === 0) { const a = c.nz(-15, 15); if (c.chance(.5)) s = `${F(a)} + ${P(V - a)}`; else s = `${F(a + V)} ${M} ${P(a)}`.replace(`${M} (${M}`, `${M} (${M}`); if (c.chance(.5) && L === 0) { const b = c.nz(-12, 12); s = `${F(V + b)} ${M} ${P(b)}`; } }
        else if (L === 1) {
          if (c.chance(.5) && V !== 0) { const ds = []; for (let d = 2; d <= Math.abs(V); d++) if (V % d === 0) ds.push(d); if (!ds.length) continue; const d = c.pick(ds) * c.sign(); s = `${F(d)} × ${P(V / d)}`; }
          else { const b = c.nz(-6, 6); if (Math.abs(b) === 1) continue; s = `${F(V * b)} ÷ ${P(b)}`; }
        } else if (L === 2) {
          const k = c.ri(0, 2);
          if (k === 0 && V !== 0) { const ds = [1, 2, 3, 4, 5].filter(d => V % d === 0); const a = c.pick(ds) * c.sign(); const q = V / a, cc = c.ri(-6, 6), b = q + cc; s = `${F(a)}(${F(b)} ${M} ${P(cc)})`; }
          else if (k === 1) { const b = c.nz(-4, 4); if (Math.abs(b) === 1) continue; const cc = c.ri(-6, 6); s = `${F((V - cc) * b)} ÷ ${P(b)} + ${P(cc)}`; }
          else { const a = c.nz(-5, 5), b = c.ri(-6, 6); const r = V - a * b; s = `${F(a)} × ${P(b)} ${r < 0 ? M : "+"} ${Math.abs(r)}`; }
        } else {
          const k = c.ri(0, 2);
          if (k === 0) { const x = c.pick([.5, .25, .75, -.5, -.25, -.75]); const y = V / x; if (!Number.isInteger(y) || Math.abs(y) > 40) continue; s = `${half(x)} × ${P(y)}`; }
          else if (k === 1) { const p = c.ri(-16, 16) / 2; if (Number.isInteger(p)) continue; s = `${F(p)} ${M} ${P(p - V)}`; }
          else { const p = c.ri(-12, 12) * 1.5; if (Number.isInteger(p)) continue; s = `${F(p)} + ${P(V - p)}`; }
        }
        if (s) return s;
      }
      return `${F(V)} + 0`;
    };
    const newT = st => { st.T = c.lvl === 3 ? c.ri(-12, 12) : c.ri(-20, 20); if (st.T === 0 && c.chance(.7)) st.T = c.ri(1, 9) * c.sign(); };
    const ensure = st => { if (st.T == null) newT(st); };
    return {
      goal: c.n(18), calm: c.opt.board === "calm", size: 150, speed: .8,
      head(st) { ensure(st); return `<div><small>Snap expressions equal to</small><div class="big">${F(st.T)}</div></div>`; },
      make(st, good) {
        ensure(st);
        let V = st.T;
        if (!good) { V = c.pick([-st.T, st.T + 2, st.T - 2, st.T + 1, st.T - 1, st.T + 10, -st.T + 2]); if (V === st.T) V = st.T + 3; }
        const s = expr(V); vals[s] = V; return { html: s, key: s, cls: "mth" };
      },
      test(key, st) { ensure(st); const V = vals[key]; return V === st.T ? true : `${PG.textify(key)} = ${F(V)}, not ${F(st.T)}.`; },
      onHit(st) { if (st.found % 5 === 0) newT(st); }
    };
  }
});
