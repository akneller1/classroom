PG.game({
  id: "g1-number-bonds", title: ["Number Bond", "Builder"], course: "Grade 1", unit: "Addition & Subtraction within 20",
  tag: "Pick the cards that add up to the target number.",
  skills: "1.OA.6 · make ten · sums to 20 · meaning of the equal sign",
  engine: "target",
  levels: [
    "Two cards make the target. Six cards to pick from.",
    "Two cards make the target, with near-miss cards mixed in.",
    "Three cards make the target.",
    "Equal sums: find a different pair with the same total (8 + 7 = ? + ?)."
  ],
  how: ["Tap cards to pick them. When you've picked enough, they're checked for you.", "The running total shows on Easy and Medium (and in Practice).", "Ten-frame cards show the number with dots."],
  options: [
    { id: "pool", label: "Targets", type: "multi", choices: [["ten", "Make 10"], ["small", "5 to 9"], ["teen", "11 to 20"]], default: ["ten", "small", "teen"] },
    { id: "look", label: "Card faces", type: "one", choices: [["num", "Numbers"], ["frame", "Ten-frames"], ["mix", "Mixed"]], default: "num" }
  ],
  round(c) {
    const { h } = c;
    const frame = n => {
      const w = 92, cell = 17; let s = `<svg viewBox="0 0 ${w} ${n > 10 ? 82 : 42}" width="${w}" height="${n > 10 ? 82 : 42}" aria-label="${n}">`;
      for (let f = 0; f < (n > 10 ? 2 : 1); f++) for (let i = 0; i < 10; i++) {
        const x = 2 + (i % 5) * cell, y = 2 + Math.floor(i / 5) * cell + f * 40;
        s += `<rect x="${x}" y="${y}" width="${cell}" height="${cell}" fill="#fff" stroke="#13202f" stroke-width="1.2"/>`;
        if (f * 10 + i < n) s += `<circle cx="${x + cell / 2}" cy="${y + cell / 2}" r="5.5" fill="#13202f"/>`;
      }
      return s + "</svg>";
    };
    const card = v => {
      const useFrame = c.opt.look === "frame" || (c.opt.look === "mix" && c.chance(.5));
      return useFrame ? { html: frame(v), label: String(v), v, cls: "pic" } : { html: String(v), label: String(v), v };
    };
    const pool = [];
    if (c.opt.pool.includes("ten")) pool.push(10, 10, 10);
    if (c.opt.pool.includes("small")) pool.push(5, 6, 7, 8, 9);
    if (c.opt.pool.includes("teen")) pool.push(11, 12, 13, 14, 15, 16, 17, 18, 19, 20);
    const N = c.n(8), puzzles = [];
    for (let p = 0; p < N; p++) {
      let T = c.pick(pool); if (c.lvl === 3 && T > 18) T = c.ri(11, 18);
      let sol, prompt, k = 2, extra = 4, avoid = null;
      if (c.lvl <= 1) { const a = c.ri(Math.max(0, T - 10), Math.min(10, T)); sol = [a, T - a]; extra = c.lvl ? 6 : 4; }
      else if (c.lvl === 2) { k = 3; const a = c.ri(1, Math.min(9, T - 2)); const b = c.ri(1, Math.min(9, T - a - 1)); sol = [a, b, T - a - b]; extra = 5; if (sol[2] > 10) { sol = [Math.ceil(T / 3), Math.floor(T / 3), T - Math.ceil(T / 3) - Math.floor(T / 3)]; } }
      else {
        const a = c.ri(Math.max(1, T - 9), Math.min(9, T - 1)); avoid = [a, T - a];
        let b, g = 0; do { b = c.ri(Math.max(0, T - 10), Math.min(10, T)); } while ((b === a || b === T - a) && g++ < 100);
        sol = [b, T - b]; extra = 4;
      }
      const nums = sol.slice();
      if (avoid) nums.push(...avoid);
      let guard = 0;
      while (nums.length < sol.length + extra + (avoid ? 2 : 0) && guard++ < 200) {
        const near = c.lvl >= 1 && c.chance(.6) ? c.pick(sol) + c.pick([-1, 1, 2, -2]) : c.ri(1, Math.min(10, T));
        if (near < 1 || near > 10 || nums.filter(x => x === near).length >= 2) continue;
        nums.push(near);
      }
      const cards = c.shuffle(nums).map(card);
      const answer = [];
      sol.forEach(v => { const i = cards.findIndex((cc, j) => cc.v === v && !answer.includes(j)); answer.push(i); });
      prompt = avoid
        ? `<div><small>Same total as</small><div class="big">${avoid[0]} + ${avoid[1]}</div></div><div class="big">= ? + ?</div>`
        : `<div><small>Make</small><div class="big">${T}</div></div><div><small>using</small><b>${k} cards</b></div>`;
      puzzles.push({
        prompt, cards, k, answer,
        show: vals => vals.join(" + ") + " = " + vals.reduce((a, b) => a + b, 0),
        test(vals) {
          const s = vals.reduce((a, b) => a + b, 0);
          if (s !== T) return `${vals.join(" + ")} = ${s}. ${s < T ? "Too small" : "Too big"}. You need ${T}.`;
          if (avoid && vals.slice().sort((x, y) => x - y).join() === avoid.slice().sort((x, y) => x - y).join()) return `That's the same pair. Find a different pair that also makes ${T}.`;
          return true;
        },
        say: avoid ? `Yes! ${avoid[0]} + ${avoid[1]} = ${sol[0]} + ${sol[1]}. Both make ${T}.` : null
      });
    }
    return { puzzles, cw: c.opt.look === "num" ? "90px" : "120px" };
  }
});
