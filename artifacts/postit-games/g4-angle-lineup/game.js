PG.game({
  id: "g4-angle-lineup", title: ["Angle", "Line-Up"], course: "Grade 4", unit: "Angles & Measurement",
  tag: "Order the angles from smallest turn to biggest turn.",
  skills: "4.MD.5–6, 4.G.1 · angle as a turn · acute, right, obtuse, straight · longer rays don't make bigger angles",
  engine: "order",
  levels: [
    "Four angles that are easy to tell apart.",
    "Five angles. Rays have different lengths: don't let that fool you.",
    "Six angles, turned every which way, as close as 10° apart.",
    "Six cards mixing drawings and descriptions (“a straight angle”, “⅓ of a right angle”). You check the order yourself."
  ],
  options: [{ id: "deg", label: "Show degrees after placing", type: "one", choices: [["no", "No"], ["yes", "Yes"]], default: "no" }],
  round(c) {
    const draw = (t, sameLen) => {
      const rot = c.lvl >= 2 ? c.r() * 360 : c.ri(-15, 15), L1 = sameLen ? 40 : c.ri(22, 44), L2 = sameLen ? 40 : c.ri(22, 44);
      const rad = a => a * Math.PI / 180;
      const p1 = [L1 * Math.cos(rad(rot)), -L1 * Math.sin(rad(rot))], p2 = [L2 * Math.cos(rad(rot + t)), -L2 * Math.sin(rad(rot + t))];
      const pts = [[0, 0], p1, p2]; const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
      const cx = (Math.min(...xs) + Math.max(...xs)) / 2, cy = (Math.min(...ys) + Math.max(...ys)) / 2;
      const T = ([x, y]) => [50 + x - cx, 50 + y - cy];
      const O = T([0, 0]), A = T(p1), B = T(p2);
      const r = 11, a1 = [O[0] + r * Math.cos(rad(rot)), O[1] - r * Math.sin(rad(rot))], a2 = [O[0] + r * Math.cos(rad(rot + t)), O[1] - r * Math.sin(rad(rot + t))];
      const arc = Math.abs(t - 90) < .5 ? (() => { const s = 8, u = [Math.cos(rad(rot)), -Math.sin(rad(rot))], v = [Math.cos(rad(rot + 90)), -Math.sin(rad(rot + 90))]; return `<path d="M${O[0] + s * u[0]} ${O[1] + s * u[1]} L${O[0] + s * u[0] + s * v[0]} ${O[1] + s * u[1] + s * v[1]} L${O[0] + s * v[0]} ${O[1] + s * v[1]}" fill="none" stroke="#2f5bd3" stroke-width="1.6"/>`; })()
        : `<path d="M${a1[0]} ${a1[1]} A${r} ${r} 0 ${t > 180 ? 1 : 0} 0 ${a2[0]} ${a2[1]}" fill="none" stroke="#2f5bd3" stroke-width="1.8"/>`;
      return `<svg viewBox="0 0 100 100" width="92" height="92" aria-label="angle drawing" style="width:104px;height:104px">${arc}<line x1="${O[0]}" y1="${O[1]}" x2="${A[0]}" y2="${A[1]}" stroke="#13202f" stroke-width="2.6" stroke-linecap="round"/><line x1="${O[0]}" y1="${O[1]}" x2="${B[0]}" y2="${B[1]}" stroke="#13202f" stroke-width="2.6" stroke-linecap="round"/><circle cx="${O[0]}" cy="${O[1]}" r="2.6" fill="#13202f"/></svg>`;
    };
    const n = [4, 5, 6, 6][c.lvl] + (c.len === 2 ? 1 : 0);
    const gap = [30, 20, 10, 8][c.lvl];
    const words = [[90, "a right angle"], [180, "a straight angle"], [30, "⅓ of a right angle"], [45, "half a right angle"], [120, "a right angle plus 30°"], [135, "a right angle and a half"], [60, "⅔ of a right angle"], [150, "a straight angle minus 30°"]];
    let vals = [], g = 0;
    while (vals.length < n && g++ < 500) { const v = c.lvl === 0 ? c.pick([20, 45, 60, 90, 120, 150, 170]) : 5 * c.ri(3, 35); if (vals.every(x => Math.abs(x - v) >= gap)) vals.push(v); }
    let cards = vals.map((v, i) => ({ v, html: draw(v, c.lvl === 0), cls: "pic", label: "angle drawing " + "ABCDEFG"[i] }));
    if (c.lvl === 3) {
      const ws = c.shuffle(words).filter(([v]) => vals.every(x => Math.abs(x - v) >= gap)).slice(0, 2);
      cards = cards.slice(0, n - ws.length).concat(ws.map(([v, t]) => ({ v, html: t, cls: "txt" })));
      if (cards.length < n) cards = vals.map(v => ({ v, html: draw(v, false), cls: "pic", label: "angle" }));
    }
    if (c.opt.deg === "yes") cards.forEach(cd => cd.say = cd.v + "°");
    return { cards, lo: "Smallest", hi: "Biggest", endCheck: c.lvl === 3, slotMin: 104,
      why: (card) => c.mode === "practice" && card.cls === "pic" ? "Look at the opening between the rays, not how long they are." : "" };
  }
});
