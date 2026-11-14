PG.game({
  id: "a1-line-labeler", title: ["Line", "Labeler"], course: "Algebra 1", unit: "Linear Functions & Graphing",
  tag: "Label each line on the graph with its equation.",
  skills: "F.IF.7a, A.CED.2, F.LE.2 · slope-intercept, standard and point-slope form · horizontal and vertical lines",
  engine: "spots",
  levels: [
    "Slope-intercept form with whole-number slopes.",
    "Negative and fractional slopes, plus horizontal and vertical lines.",
    "Standard form: 2x + 3y = 6.",
    "Mixed forms, including point-slope, plus decoy equations that fit no line."
  ],
  round(c) {
    const { h, Q } = c; const X = h.v("x"), Y = h.v("y"), F = h.fmt, M = h.MINUS;
    const R = 8;
    const P = PG.svg.plane({ xmin: -R, xmax: R, ymin: -R, ymax: R, size: 520, pad: 22, ink: "currentColor", gridc: "rgba(120,140,170,.3)", labels: 2, fs: 12, aw: 1.8 });
    const styles = [["#2f5bd3", ""], ["#d6453a", "10 6"], ["#1f9d64", "3 5"], ["#b26a00", "14 5 3 5"], ["#7a4fd6", "1 0"]];
    const mStr = q => q.d === 1 ? (q.n === 1 ? "" : q.n === -1 ? M : F(q.n)) : (q.n < 0 ? M : "") + h.frac(Math.abs(q.n), q.d);
    const si = (q, b) => `${Y} = ${q.n === 0 ? F(b) : mStr(q) + X + (b ? ` ${b < 0 ? M : "+"} ${Math.abs(b)}` : "")}`;
    const stdF = (q, b) => { // y = (n/d)x + b  ->  -n x + d y = d b ; make A>0
      let A = -q.n, B = q.d, C = q.d * b; if (A < 0 || (A === 0 && B < 0)) { A = -A; B = -B; C = -C; }
      const g = h.gcd(h.gcd(A, B), C) || 1; A /= g; B /= g; C /= g;
      return `${h.terms([[A, X], [B, Y]])} = ${F(C)}`;
    };
    const ptSlope = (q, b) => { const x1 = c.ri(-3, 3) * q.d, y1 = q.n * x1 / q.d + b; return `${Y} ${y1 < 0 ? "+" : M} ${Math.abs(y1)} = ${mStr(q) || "1"}(${X} ${x1 < 0 ? "+" : M} ${Math.abs(x1)})`.replace(`${Y} ${M} 0 =`, `${Y} =`).replace(`(${X} ${M} 0)`, X); };
    const nL = c.lvl === 0 ? 3 : 4;
    const slopes = c.lvl === 0 ? [[1, 1], [2, 1], [-1, 1], [3, 1], [-2, 1]] : [[1, 2], [-2, 3], [3, 1], [-1, 1], [2, 1], [-3, 2], [1, 3], [0, 1], [-1, 2]];
    const lines = [];
    let g = 0;
    while (lines.length < nL && g++ < 400) {
      const vert = c.lvl === 1 && c.chance(.2) && !lines.some(l => l.vert);
      if (vert) { const x0 = c.nz(-6, 6); if (lines.some(l => l.vert && l.x0 === x0)) continue; lines.push({ vert: true, x0 }); continue; }
      const [n, d] = c.pick(slopes); const q = Q(n, d), b = c.ri(-5, 5);
      if (c.lvl === 0 && n === 0) continue;
      if (lines.some(l => !l.vert && l.q.n === q.n && l.q.d === q.d && l.b === b)) continue;
      if (lines.some(l => !l.vert && l.q.n === q.n && l.q.d === q.d && (c.lvl < 3 || Math.abs(l.b - b) < 3))) continue;
      lines.push({ q, b });
    }
    let svg = P.s, inner = "";
    lines.forEach((l, i) => {
      const [col, dash] = styles[i];
      if (l.vert) inner += `<line x1="${P.X(l.x0)}" x2="${P.X(l.x0)}" y1="${P.Y(R)}" y2="${P.Y(-R)}" stroke="${col}" stroke-width="3" stroke-dasharray="${dash}"/>`;
      else inner += PG.svg.curve(P, x => l.q.n / l.q.d * x + l.b, { color: col, width: 3 }).replace("/>", ` stroke-dasharray="${dash}"/>`);
    });
    svg += PG.svg.wrapClip(P, inner) + P.close;
    // label spot on each line, far from other lines and spots
    const yAt = (l, x) => l.vert ? null : l.q.n / l.q.d * x + l.b;
    const dist = (l, x, y) => l.vert ? Math.abs(x - l.x0) : Math.abs(l.q.n / l.q.d * x - y + l.b) / Math.hypot(l.q.n / l.q.d, 1);
    const spots = [];
    lines.forEach((l, i) => {
      let best = null, bs = -1;
      for (let t = -R + 1.5; t <= R - 1.5; t += .5) {
        const x = l.vert ? l.x0 : t, y = l.vert ? t : yAt(l, t);
        if (Math.abs(y) > R - 1.2 || Math.abs(x) > R - 1.2) continue;
        let sc = Math.min(...lines.filter((_, j) => j !== i).map(o => dist(o, x, y)), 99);
        sc = Math.min(sc, ...spots.map(s => Math.hypot(s.vx - x, s.vy - y) / 1.6), 99);
        if (sc > bs) { bs = sc; best = [x, y]; }
      }
      spots.push({ x: P.X(best[0]), y: P.Y(best[1]), vx: best[0], vy: best[1], key: "L" + i, label: `Label spot on the ${["solid blue", "dashed red", "dotted green", "dash-dot brown", "purple"][i]} line`, html: `<svg width="30" height="8" aria-hidden="true"><line x1="1" x2="29" y1="4" y2="4" stroke="${styles[i][0]}" stroke-width="3.5" stroke-dasharray="${styles[i][1] ? styles[i][1].split(" ").map(x => x / 2).join(" ") : ""}"/></svg>` });
    });
    const eqFor = (l, form) => {
      if (l.vert) return `${X} = ${F(l.x0)}`;
      if (l.q.n === 0) return `${Y} = ${F(l.b)}`;
      if (form === "std") return stdF(l.q, l.b);
      if (form === "pt") return ptSlope(l.q, l.b);
      return si(l.q, l.b);
    };
    const form = () => c.lvl <= 1 ? "si" : c.lvl === 2 ? "std" : c.pick(["si", "std", "pt"]);
    const cards = lines.map((l, i) => ({ html: eqFor(l, form()), key: "L" + i, cls: "mth" }));
    if (c.lvl === 3) {
      const l0 = c.pick(lines.filter(l => !l.vert && l.q.n !== 0));
      if (l0) { cards.push({ html: si(l0.q, l0.b + c.pick([2, -2, 3])), key: "decoy1", cls: "mth" }); cards.push({ html: si(Q(-l0.q.n, l0.q.d), l0.b), key: "decoy2", cls: "mth" }); }
    }
    return { svg, w: P.w, h: P.h, spots, cards, maxW: "620px", trayTitle: "Equations", fill: card => card.html,
      why: (card, spot) => c.mode === "practice" ? "Check the y-intercept (where it crosses the y-axis) and the slope (rise over run). A falling line has a negative slope." : "That equation doesn't describe that line." };
  }
});
