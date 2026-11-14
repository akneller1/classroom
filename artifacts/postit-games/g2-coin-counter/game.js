PG.game({
  id: "g2-coin-counter", title: ["Coin", "Counter"], course: "Grade 2", unit: "Money",
  tag: "Pick coins that make the amount exactly.",
  skills: "2.MD.8 · pennies, nickels, dimes, quarters, dollars · counting on · fewest coins",
  engine: "target",
  levels: [
    "Make amounts up to 40¢ with dimes, nickels and pennies.",
    "Make amounts up to 99¢. Quarters join in.",
    "Make the amount with the FEWEST coins possible.",
    "Dollars and cents up to $2.99, with the fewest bills and coins."
  ],
  options: [{ id: "names", label: "Coin labels", type: "one", choices: [["value", "Show value (10¢)"], ["name", "Show name (dime)"]], default: "value", help: "Names only is harder: students must know each coin's value." }],
  round(c) {
    const C = { 1: ["penny", 34, "#c98457"], 5: ["nickel", 42, "#c9d1d8"], 10: ["dime", 30, "#d8dee3"], 25: ["quarter", 48, "#c3ccd4"], 100: ["dollar", 0, "#9ed36a"] };
    const money = v => v >= 100 ? "$" + (v / 100).toFixed(2) : v + "¢";
    const coin = v => {
      const [name, size, col] = C[v];
      const text = c.opt.names === "name" ? name : v === 100 ? "$1" : v + "¢";
      if (v === 100) return { html: `<svg viewBox="0 0 96 46" width="96" height="46" aria-label="one dollar bill"><rect x="2" y="2" width="92" height="42" rx="4" fill="#dfeccf" stroke="#2f6b2a" stroke-width="2"/><rect x="8" y="8" width="80" height="30" rx="3" fill="none" stroke="#2f6b2a" stroke-width="1"/><text x="48" y="29" text-anchor="middle" font-size="16" font-weight="700" fill="#2f6b2a" font-family="Rubik,sans-serif">${text}</text></svg>`, v, label: "one dollar", cls: "pic" };
      const r = size / 2;
      return { html: `<svg viewBox="0 0 52 52" width="${size + 6}" height="${size + 6}" aria-label="${name}" style="width:${Math.round((size + 6) * 1.45)}px;height:auto"><circle cx="26" cy="26" r="${r}" fill="${col}" stroke="#4a5563" stroke-width="2"/><circle cx="26" cy="26" r="${r - 4}" fill="none" stroke="#4a5563" stroke-width=".8" stroke-dasharray="2 2"/><text x="26" y="${26 + (text.length > 4 ? 3.5 : 5)}" text-anchor="middle" font-size="${text.length > 4 ? 9 : 13}" font-weight="700" fill="#1d2633" font-family="Rubik,sans-serif">${text}</text></svg>`, v, label: name, cls: "pic" };
    };
    const greedy = (T, denoms) => { const out = []; for (const d of denoms) while (T >= d) { out.push(d); T -= d; } return out; };
    const N = c.n(7), puzzles = [];
    for (let p = 0; p < N; p++) {
      let T, sol, denoms, extra;
      if (c.lvl === 0) { denoms = [10, 5, 1]; T = c.ri(8, 40); sol = []; let r = T; while (r > 0) { const d = c.pick(denoms.filter(x => x <= r)); sol.push(d); r -= d; } extra = 3; }
      else if (c.lvl === 1) { denoms = [25, 10, 5, 1]; T = c.ri(30, 99); sol = []; let r = T; while (r > 0) { const opts = denoms.filter(x => x <= r); const d = c.chance(.6) ? opts[0] : c.pick(opts); sol.push(d); r -= d; } extra = 3; }
      else if (c.lvl === 2) { denoms = [25, 10, 5, 1]; T = c.ri(30, 99); sol = greedy(T, denoms); extra = 5; }
      else { denoms = [100, 25, 10, 5, 1]; T = c.ri(105, 299); sol = greedy(T, denoms); extra = 4; }
      while (sol.length > 9) { p--; break; }
      if (sol.length > 9) continue;
      const fewest = greedy(T, denoms).length;
      const vals = sol.slice(); for (let i = 0; i < extra; i++) vals.push(c.pick(denoms));
      if (c.lvl >= 2) { vals.push(...[10, 10, 5, 5, 1, 1].slice(0, 3)); }
      const cards = c.shuffle(vals).map(coin);
      const answer = []; sol.forEach(v => answer.push(cards.findIndex((x, j) => x.v === v && !answer.includes(j))));
      puzzles.push({
        prompt: `<div><small>Make</small><div class="big">${money(T)}</div></div>${c.lvl >= 2 ? `<div><small>with the</small><b>fewest coins${c.lvl === 3 ? " and bills" : ""}</b></div>` : ""}`,
        cards, answer,
        show: v => "Total: " + money(v.reduce((a, b) => a + b, 0)) + ` (${v.length} piece${v.length > 1 ? "s" : ""})`,
        test(v) {
          const s = v.reduce((a, b) => a + b, 0);
          if (s !== T) return `Those make ${money(s)}. ${s < T ? "Add" : "Take away"} ${money(Math.abs(T - s))}.`;
          if (c.lvl >= 2 && v.length > fewest) return `That makes ${money(T)}, but with ${v.length} pieces. It can be done with ${fewest}. Try trading small coins for bigger ones.`;
          return true;
        }
      });
    }
    return { puzzles, cw: "96px", flat: false };
  }
});
