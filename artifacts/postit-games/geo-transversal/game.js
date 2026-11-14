PG.game({
  id: "geo-transversal", title: ["Parallel Lines", "Angle Fill"], course: "Geometry", unit: "Parallel Lines & Transversals",
  tag: "Fill in every angle around the transversal.",
  skills: "G.CO.9 · vertical angles · linear pairs · corresponding, alternate interior/exterior and same-side angles",
  engine: "spots",
  levels: [
    "One transversal: place the angle measures.",
    "Name the relationship of each angle to the marked angle ∠1.",
    "Two transversals crossing the parallel lines: place all the measures.",
    "Names again, but the marked angle can be anywhere, and one angle has no special name."
  ],
  round(c) {
    const W = 600, H = 330, rot = c.ri(-12, 12) * Math.PI / 180;
    const R = (x, y) => [W / 2 + x * Math.cos(rot) - y * Math.sin(rot), H / 2 + x * Math.sin(rot) + y * Math.cos(rot)];
    const yTop = -70, yBot = 70; // local coordinates (y down)
    const lineSvg = (y) => { const [x1, y1] = R(-290, y), [x2, y2] = R(290, y); return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="currentColor" stroke-width="2.5"/>` + (() => { const [ax, ay] = R(150, y); return `<path d="M${ax - 6} ${ay - 6} l7 6 l-7 6" transform="rotate(${rot * 180 / Math.PI} ${ax} ${ay})" fill="none" stroke="currentColor" stroke-width="2"/>`; })(); };
    const trans = [];
    const nT = c.lvl === 2 ? 2 : 1;
    const hit = (T, y) => T.x0 + y * (Math.cos(T.th * Math.PI / 180) / -Math.sin(T.th * Math.PI / 180));
    for (let t = 0; t < nT; t++) { let th, tries = 0, T; do { th = c.ri(40, 140); T = { th, x0: nT === 1 ? c.ri(-40, 40) : (t ? 130 : -130) }; } while (tries++ < 200 && (Math.abs(th - 90) < 12 || trans.some(o => Math.abs(o.th - th) < 25 || Math.abs(hit(o, yTop) - hit(T, yTop)) < 110 || Math.abs(hit(o, yBot) - hit(T, yBot)) < 110))); trans.push(T); }
    let svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="two parallel lines cut by ${nT === 1 ? "a transversal" : "two transversals"}">` + lineSvg(yTop) + lineSvg(yBot);
    const spots = [], cards = [];
    const QN = ["upper right", "upper left", "lower left", "lower right"];
    trans.forEach((T, ti) => {
      const th = T.th * Math.PI / 180, dx = Math.cos(th), dy = -Math.sin(th); // direction "up" along the transversal
      const P0 = y => [T.x0 + y * (dx / dy), y];
      const top = P0(yTop), bot = P0(yBot);
      const e1 = R(top[0] + 88 * dx, top[1] + 88 * dy), e2 = R(bot[0] - 88 * dx, bot[1] - 88 * dy);
      svg += `<line x1="${e1[0]}" y1="${e1[1]}" x2="${e2[0]}" y2="${e2[1]}" stroke="currentColor" stroke-width="2.5"/>`;
      // angle at quadrant q measured: UR = th, UL = 180-th, LL = th, LR = 180-th (in degrees)
      const meas = q => (q % 2 === 0 ? T.th : 180 - T.th);
      const bis = q => { const a = [T.th / 2, (T.th + 180) / 2, 180 + T.th / 2, (180 + T.th + 360) / 2][q] * Math.PI / 180; return [Math.cos(a), -Math.sin(a)]; };
      const positions = [];
      [top, bot].forEach((p, li) => [0, 1, 2, 3].forEach(q => { const [bx, by] = bis(q); const r = 37; const pt = R(p[0] + bx * r, p[1] + by * r); positions.push({ li, q, x: pt[0], y: pt[1] }); }));
      const g = c.pick(positions);
      const interior = p => (p.li === 0 ? p.q >= 2 : p.q <= 1);
      const side = p => (p.q === 0 || p.q === 3 ? "R" : "L");
      const rel = p => {
        if (p.li === g.li) return p.q === (g.q + 2) % 4 ? "vertical" : "linear";
        if (p.q === g.q) return "corresponding";
        if (p.q === (g.q + 2) % 4) return interior(p) && interior(g) ? "alt-int" : !interior(p) && !interior(g) ? "alt-ext" : "none";
        if (side(p) === side(g)) return interior(p) && interior(g) ? "ss-int" : !interior(p) && !interior(g) ? "ss-ext" : "none";
        return "none";
      };
      const NAMES = { vertical: "Vertical angle", linear: "Linear pair", corresponding: "Corresponding", "alt-int": "Alternate interior", "alt-ext": "Alternate exterior", "ss-int": "Same-side interior", "ss-ext": "Same-side exterior", none: "No special name" };
      svg += `<text x="${g.x}" y="${g.y + 5}" text-anchor="middle" font-size="15" font-weight="700" fill="#d6453a">${c.lvl === 1 || c.lvl === 3 ? "∠1" : meas(g.q) + "°"}</text>`;
      positions.forEach(p => {
        if (p === g) return;
        if (c.lvl === 1 || c.lvl === 3) {
          const r = rel(p); if (r === "none" && c.lvl === 1) return;
          spots.push({ x: p.x, y: p.y, key: r, label: `Angle at the ${p.li ? "lower" : "upper"} parallel line, ${QN[p.q]}${nT > 1 ? ", transversal " + (ti + 1) : ""}` });
          cards.push({ html: NAMES[r], key: r, cls: "txt" });
        } else {
          spots.push({ x: p.x, y: p.y, key: String(meas(p.q)), label: `Angle at the ${p.li ? "lower" : "upper"} parallel line, ${QN[p.q]}${nT > 1 ? ", transversal " + (ti + 1) : ""}` });
          cards.push({ html: meas(p.q) + "°", key: String(meas(p.q)) });
        }
      });
    });
    svg += "</svg>";
    return { svg, w: W, h: H, spots, cards, maxW: "680px", trayTitle: c.lvl % 2 ? "Relationships" : "Measures",
      fill: card => c.lvl % 2 ? card.html.split(" ").map(w => w[0]).join("").toUpperCase() : card.html,
      why: (card, spot) => c.mode === "practice" ? (c.lvl % 2 ? "Compare the position to ∠1: same corner at the other line (corresponding)? Opposite sides of the transversal, between the lines (alternate interior)?" : "Angles at one crossing are vertical (equal) or a linear pair (add to 180°). Corresponding angles match at the other crossing.") : "Not that one." };
  }
});
