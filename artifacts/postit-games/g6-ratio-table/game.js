PG.game({
  id: "g6-ratio-table", title: ["Ratio Table", "Fill-In"], course: "Grade 6", unit: "Ratios & Rates",
  tag: "Complete the ratio tables. Watch out for adding instead of multiplying!",
  skills: "6.RP.1–3 · equivalent ratios · ratio tables · unit rates · multiplicative (not additive) reasoning",
  engine: "grid",
  levels: [
    "Whole-number ratios that count up by the same amount.",
    "Columns out of order. Finding the unit rate (the “1” column) helps.",
    "Scale factors that aren't whole numbers (4 : 10 → 2 : 5 → 6 : 15).",
    "Decimals, a unit rate column, and a Total row to fill in too."
  ],
  how: ["Every column in a table is an equivalent ratio: multiply or divide BOTH numbers by the same thing.", "Some leftover cards are traps made by adding instead of multiplying."],
  round(c) {
    const ctxs = [["Cups of flour", "Cookies"], ["Minutes", "Miles"], ["Pounds of apples", "Dollars"], ["Red paint (cups)", "Blue paint (cups)"], ["Laps", "Minutes"], ["Tickets", "Dollars"], ["Teaspoons of salt", "Quarts of water"], ["Hours", "Pages read"]];
    const fmt = v => String(+v.toFixed(2));
    const T = c.len === 0 ? 1 : c.len === 2 ? 3 : 2;
    const names = c.sample(ctxs, T);
    const rows = [], cells = [], cards = [], keys = new Set(), traps = [];
    const COLS = 5;
    names.forEach((nm, ti) => {
      let a, b, ms;
      if (c.lvl === 0) { a = c.ri(1, 5); b = c.ri(2, 9); if (a === b) b++; ms = [1, 2, 3, 4, 5]; }
      else if (c.lvl === 1) { a = c.ri(1, 4); b = c.ri(2, 7); if (a === b) b++; ms = [c.pick([2, 3])].concat(c.sample([1, 4, 5, 6, 7, 8, 10], 4)); }
      else if (c.lvl === 2) { a = c.pick([2, 4]); b = c.pick([5, 3, 7]); ms = [2].concat(c.sample([.5, 1.5, 3, 5, 2.5, 4], 4)); }
      else { a = c.pick([2, 4, 5]); b = c.pick([3, 7, 9]); ms = [2].concat(c.sample([.5, 1.5, 2.5, 3, 4, 1 / a], 4)); }
      ms = ms.slice(0, COLS);
      const rowsHere = c.lvl === 3 ? [nm[0], nm[1], "Total"] : [nm[0], nm[1]];
      const vals = rowsHere.map((_, r) => ms.map(m => r === 0 ? a * m : r === 1 ? b * m : (a + b) * m));
      const given = new Set(); // one known entry in every later column fixes its scale factor
      for (let ci = 1; ci < COLS; ci++) given.add(ci * 10 + c.ri(0, rowsHere.length - 1));
      rowsHere.forEach((rn, r) => {
        rows.push(rn);
        cells.push(vals[r].map((v, ci) => {
          const isGiven = (ci === 0 && r < 2) || given.has(ci * 10 + r);
          const html = fmt(v);
          if (isGiven) return { given: true, html };
          keys.add(html); cards.push({ key: html, html });
          return { key: html, html };
        }));
      });
      // additive-thinking traps
      ms.forEach((m, ci) => { if (ci) { const t = fmt(b + (a * m - a)); traps.push(t); } });
      if (ti < T - 1) { rows.push(""); cells.push(Array(COLS).fill(null)); }
    });
    const nTrap = [1, 2, 3, 3][c.lvl];
    c.shuffle(traps).filter(t => !keys.has(t) && +t > 0).slice(0, nTrap).forEach(t => { keys.add(t); cards.push({ key: "trap" + t, html: t }); });
    return { cols: Array.from({ length: COLS }, () => ""), rows, cells, cards, corner: "", noHead: true, rowW: "minmax(120px,1.6fr) ", maxW: "820px",
      why: (card, cell) => "Check the scale factor: what did the top number get multiplied by? Multiply the bottom by the same thing.",
      doneText: "Tables complete. Leftover cards came from adding instead of multiplying." };
  }
});
