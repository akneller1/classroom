PG.game({
  id: "geo-trig-builder", title: ["Trig Ratio", "Builder"], course: "Geometry", unit: "Right Triangle Trigonometry",
  tag: "Build each trig ratio from the triangle's sides.",
  skills: "G.SRT.6–8 · sine, cosine and tangent · opposite, adjacent, hypotenuse · cofunctions · tan = sin ÷ cos",
  engine: "build",
  levels: [
    "Build sin, cos or tan of angle A from the side lengths.",
    "Angle A or angle B: opposite and adjacent swap!",
    "Work backwards: which function and which angle give this ratio?",
    "Identities: build tan A from sines and cosines (more than one answer works)."
  ],
  how: ["SOH-CAH-TOA: sin = opposite/hypotenuse, cos = adjacent/hypotenuse, tan = opposite/adjacent.", "Fill the boxes and press Check."],
  round(c) {
    const { h } = c;
    const triples = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [6, 8, 10], [9, 12, 15], [20, 21, 29], [12, 16, 20]];
    const N = c.n(6), puzzles = [];
    for (let p = 0; p < N; p++) {
      let [a, b, hyp] = c.pick(triples); if (c.chance(.5)) [a, b] = [b, a];
      // right angle at C; side a opposite A (BC), side b opposite B (AC)
      const flip = c.chance(.5);
      const tri = `<svg viewBox="0 0 210 130" width="210" aria-label="right triangle ABC with right angle at C; BC = ${a}, AC = ${b}, AB = ${hyp}"><path d="${flip ? "M190 110 H20 V20 Z" : "M20 110 H190 V20 Z"}" fill="none" stroke="currentColor" stroke-width="2.5"/><path d="${flip ? "M20 98 H32 V110" : "M178 110 V98 H190"}" fill="none" stroke="currentColor" stroke-width="1.5"/>
        <text x="${flip ? 198 : 8}" y="${flip ? 118 : 118}" font-size="15" font-weight="700" fill="currentColor" font-style="italic">A</text><text x="${flip ? 8 : 196}" y="${flip ? 18 : 18}" font-size="15" font-weight="700" fill="currentColor" font-style="italic">B</text><text x="${flip ? 6 : 196}" y="${flip ? 124 : 124}" font-size="15" font-weight="700" fill="currentColor" font-style="italic">C</text>
        <text x="105" y="126" text-anchor="middle" font-size="14" font-weight="700" fill="currentColor">${b}</text><text x="${flip ? 14 : 196}" y="68" text-anchor="${flip ? "end" : "start"}" font-size="14" font-weight="700" fill="currentColor">${a}</text><text x="${flip ? 120 : 90}" y="58" text-anchor="middle" font-size="14" font-weight="700" fill="currentColor">${hyp}</text></svg>`;
      const val = { sinA: a / hyp, cosA: b / hyp, tanA: a / b, sinB: b / hyp, cosB: a / hyp, tanB: b / a };
      const near = (x, y) => Math.abs(x - y) < 1e-9;
      if (c.lvl <= 1) {
        const fn = c.pick(["sin", "cos", "tan"]), ang = c.lvl === 0 ? "A" : c.pick(["A", "B"]);
        const target = val[fn + ang];
        const nums = [a, b, hyp];
        const cards = c.shuffle(nums.concat(c.lvl ? [a + b] : [])).map(v => ({ html: String(v), v }));
        const [num, den] = fn === "sin" ? (ang === "A" ? [a, hyp] : [b, hyp]) : fn === "cos" ? (ang === "A" ? [b, hyp] : [a, hyp]) : (ang === "A" ? [a, b] : [b, a]);
        puzzles.push({ prompt: tri, parts: [`${fn} ${h.v(ang)} = `, {}, " / ", {}], cards, answer: [cards.findIndex(x => x.v === num), cards.findIndex(x => x.v === den)],
          test: v => near(v[0] / v[1], target) ? true : `${v[0]}/${v[1]} isn't ${fn} ${ang}. From angle ${ang}: ${fn === "sin" ? "opposite over hypotenuse" : fn === "cos" ? "adjacent over hypotenuse" : "opposite over adjacent"}.` });
      } else if (c.lvl === 2) {
        const key = c.pick(Object.keys(val)); const target = val[key];
        const [num, den] = { sinA: [a, hyp], cosA: [b, hyp], tanA: [a, b], sinB: [b, hyp], cosB: [a, hyp], tanB: [b, a] }[key];
        const cards = c.shuffle([{ html: "sin", v: "sin", cls: "mth" }, { html: "cos", v: "cos", cls: "mth" }, { html: "tan", v: "tan", cls: "mth" }, { html: h.v("A"), v: "A", cls: "mth" }, { html: h.v("B"), v: "B", cls: "mth" }]);
        puzzles.push({ prompt: tri, parts: [{}, " ", {}, " = ", h.frac(num, den)], cards, answer: [cards.findIndex(x => x.v === key.slice(0, 3)), cards.findIndex(x => x.v === key[3])],
          test: v => { if (!["sin", "cos", "tan"].includes(v[0]) || !["A", "B"].includes(v[1])) return "Put a function (sin, cos, tan) first and an angle (A or B) second."; return near(val[v[0] + v[1]], target) ? true : `${v[0]} ${v[1]} = ${h.fmt(+val[v[0] + v[1]].toFixed(3))}, but ${num}/${den} = ${h.fmt(+target.toFixed(3))}.`; },
          say: key.slice(0, 3) === "sin" ? `Also true: cos ${key[3] === "A" ? "B" : "A"} = ${num}/${den} (cofunctions!)` : null });
      } else {
        const opts = { "sin A": val.sinA, "cos A": val.cosA, "sin B": val.sinB, "cos B": val.cosB, "tan B": val.tanB, "1": 1 };
        const cards = c.shuffle(Object.keys(opts).map(k => ({ html: k.replace(/([AB])$/, m => h.v(m)), v: k, cls: "mth" })));
        puzzles.push({ prompt: tri, parts: [`tan ${h.v("A")} = `, {}, " ÷ ", {}], cards, answer: [cards.findIndex(x => x.v === "sin A"), cards.findIndex(x => x.v === "cos A")],
          test: v => near(opts[v[0]] / opts[v[1]], val.tanA) ? true : `${v[0]} ÷ ${v[1]} = ${h.fmt(+(opts[v[0]] / opts[v[1]]).toFixed(3))}, but tan A = ${a}/${b}.`,
          say: "Other answers work too: cos B ÷ sin B, or 1 ÷ tan B." });
      }
    }
    return { puzzles };
  }
});
