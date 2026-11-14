PG.game({
  id: "geo-congruence-sort", title: ["Congruence", "Criteria Sort"], course: "Geometry", unit: "Triangle Congruence",
  tag: "Read the markings. Which shortcut proves the triangles congruent, if any?",
  skills: "G.CO.7–8, G.SRT.5 · SSS, SAS, ASA, AAS, HL · why SSA and AAA don't work · shared sides and vertical angles",
  engine: "sort",
  levels: [
    "SSS, SAS, or not enough information.",
    "ASA and AAS join in. Is the side between the angles?",
    "HL for right triangles, plus SSA and AAA traps.",
    "Triangles that share a side or vertical angles: the figure gives you a free part."
  ],
  how: ["Tick marks show congruent sides. Arcs show congruent angles. A square corner is a right angle.", "Matching numbers of ticks (or arcs) go together."],
  options: [{ id: "deal", label: "Cards", type: "one", choices: [["deal", "One at a time"], ["all", "All at once"]], default: "deal" }],
  round(c) {
    const ink = "#13202f", mark = "#1d3a8f";
    const fmt = v => v.toFixed(1);
    const ticks = (P, Q, k) => { const mx = (P[0] + Q[0]) / 2, my = (P[1] + Q[1]) / 2, dx = Q[0] - P[0], dy = Q[1] - P[1], L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L, nx = -uy, ny = ux; let s = ""; for (let i = 0; i < k; i++) { const o = (i - (k - 1) / 2) * 4; const cx = mx + ux * o, cy = my + uy * o; s += `<line x1="${fmt(cx - nx * 5)}" y1="${fmt(cy - ny * 5)}" x2="${fmt(cx + nx * 5)}" y2="${fmt(cy + ny * 5)}" stroke="${mark}" stroke-width="1.7"/>`; } return s; };
    const arcs = (V, A, B, k) => { const a1 = Math.atan2(A[1] - V[1], A[0] - V[0]), a2 = Math.atan2(B[1] - V[1], B[0] - V[0]); let d = a2 - a1; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; let s = ""; for (let i = 0; i < k; i++) { const r = 9 + i * 3.5; const p1 = [V[0] + r * Math.cos(a1), V[1] + r * Math.sin(a1)], p2 = [V[0] + r * Math.cos(a1 + d), V[1] + r * Math.sin(a1 + d)]; s += `<path d="M${fmt(p1[0])} ${fmt(p1[1])} A${r} ${r} 0 0 ${d > 0 ? 1 : 0} ${fmt(p2[0])} ${fmt(p2[1])}" fill="none" stroke="${mark}" stroke-width="1.5"/>`; } return s; };
    const box = (V, A, B) => { const u = [A[0] - V[0], A[1] - V[1]], w = [B[0] - V[0], B[1] - V[1]], lu = Math.hypot(...u), lw = Math.hypot(...w), s = 7; const p = [V[0] + u[0] / lu * s, V[1] + u[1] / lu * s], q = [V[0] + w[0] / lw * s, V[1] + w[1] / lw * s], r = [p[0] + w[0] / lw * s, p[1] + w[1] / lw * s]; return `<path d="M${fmt(p[0])} ${fmt(p[1])} L${fmt(r[0])} ${fmt(r[1])} L${fmt(q[0])} ${fmt(q[1])}" fill="none" stroke="${mark}" stroke-width="1.5"/>`; };
    const poly = P => `<path d="M${P.map(p => fmt(p[0]) + " " + fmt(p[1])).join(" L")} Z" fill="#fff" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>`;
    const fit = (polys, W, H, pad = 10) => { const all = polys.flat(); const xs = all.map(p => p[0]), ys = all.map(p => p[1]); const mnx = Math.min(...xs), mxx = Math.max(...xs), mny = Math.min(...ys), mxy = Math.max(...ys); const s = Math.min((W - 2 * pad) / (mxx - mnx), (H - 2 * pad) / (mxy - mny)); const ox = (W - (mxx - mnx) * s) / 2, oy = (H - (mxy - mny) * s) / 2; return polys.map(P => P.map(([x, y]) => [ox + (x - mnx) * s, oy + (y - mny) * s])); };
    const scalene = right => { for (let t = 0; t < 200; t++) { let P; if (right) { const a = c.ri(30, 60), b = c.ri(40, 80); P = [[0, 0], [a, 0], [0, -b]]; } else { const A = c.ri(38, 80) * Math.PI / 180, B = c.ri(38, 80) * Math.PI / 180; if (Math.abs(A - B) < .15 || Math.PI - A - B < .5 || Math.abs(Math.PI - A - B - A) < .15 || Math.abs(Math.PI - A - B - B) < .15) continue; const base = 70; const h = base / (1 / Math.tan(A) + 1 / Math.tan(B)); P = [[0, 0], [base, 0], [h / Math.tan(A), -h]]; } return P; } return [[0, 0], [70, 0], [20, -45]]; };
    const iso = (P, flip, rot, dx) => P.map(([x, y]) => { if (flip) x = -x; const cs = Math.cos(rot), sn = Math.sin(rot); return [x * cs - y * sn + dx, x * sn + y * cs]; });
    // parts spec: sides s0..s2 (P0P1, P1P2, P2P0), angles a0..a2
    const drawPair = (spec, right) => {
      const T = scalene(right);
      const T2 = iso(T, c.chance(.5), c.r() * Math.PI * 2, 0);
      const gap = Math.max(...T.map(p => p[0])) - Math.min(...T2.map(p => p[0])) + 28;
      const my1 = (Math.max(...T.map(p => p[1])) + Math.min(...T.map(p => p[1]))) / 2, my2 = (Math.max(...T2.map(p => p[1])) + Math.min(...T2.map(p => p[1]))) / 2;
      let [A, B] = fit([T, T2.map(([x, y]) => [x + gap, y - my2 + my1])], 240, 112, 8);
      const side = (P, i) => [P[i], P[(i + 1) % 3]];
      let s = `<svg viewBox="0 0 240 112" width="240" aria-label="${spec.label}">` + poly(A) + poly(B);
      [A, B].forEach(P => {
        spec.sides.forEach(([i, k]) => { const [p, q] = side(P, i); s += ticks(p, q, k); });
        spec.angles.forEach(([i, k]) => { s += arcs(P[i], P[(i + 1) % 3], P[(i + 2) % 3], k); });
        if (right) s += box(P[0], P[1], P[2]);
      });
      return s + "</svg>";
    };
    const sideNames = ["side", "side", "side"];
    const make = kind => {
      const i = c.ri(0, 2), n1 = (i + 1) % 3, n2 = (i + 2) % 3;
      const K = c.shuffle([1, 2, 3]), KA = c.shuffle([1, 2, 3]);
      let sides = [], angles = [], right = false, bin = kind, why = "";
      if (kind === "SSS") { sides = [[0, K[0]], [1, K[1]], [2, K[2]]]; why = "All three pairs of sides are marked: SSS."; }
      else if (kind === "SAS") { sides = [[i, K[0]], [n1, K[1]]]; angles = [[n1, KA[0]]]; why = "Two sides and the angle BETWEEN them: SAS."; }
      else if (kind === "ASA") { angles = [[i, KA[0]], [n1, KA[1]]]; sides = [[i, K[0]]]; why = "Two angles and the side BETWEEN them: ASA."; }
      else if (kind === "AAS") { angles = [[i, KA[0]], [n1, KA[1]]]; sides = [[n1, K[0]]]; why = "Two angles and a side that is NOT between them: AAS."; }
      else if (kind === "HL") { right = true; sides = [[1, K[0]], [c.pick([0, 2]), K[1]]]; why = "Right triangles with a congruent hypotenuse and leg: HL."; }
      else if (kind === "SSA") { sides = [[i, K[0]], [n1, K[1]]]; angles = [[i, KA[0]]]; bin = "N"; why = "Two sides and an angle that is NOT between them (SSA) doesn't prove congruence."; }
      else if (kind === "AAA") { angles = [[0, KA[0]], [1, KA[1]], [2, KA[2]]]; bin = "N"; why = "Three angles (AAA) only proves the shapes are similar, not congruent. Size could differ."; }
      else if (kind === "SS") { sides = [[i, K[0]], [n1, K[1]]]; bin = "N"; why = "Only two pairs of parts are marked. That's not enough."; }
      const label = `two triangles; ${sides.length} pairs of congruent sides marked, ${angles.length} pairs of congruent angles marked${right ? ", both right triangles" : ""}`;
      return { html: drawPair({ sides, angles, label }, right || kind === "HL"), cls: "pic", bin, why, label };
    };
    // Expert: shared side (kite) and vertical angles (bowtie)
    const shared = kind => {
      const W = 220, H = 120; let s, label, bin, why, bins = null;
      if (c.chance(.5)) {
        const w = c.ri(55, 80), t = c.ri(35, 48), b = c.ri(38, 50);
        const B = [110, 60 - t], D = [110, 60 + b], A = [110 - w, 60], C = [110 + w, 60];
        s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" aria-label="LABEL">` + poly([A, B, D]) + poly([C, B, D]);
        const pick = c.pick(["SSS", "SAS", "ASA", "AAS", "N1"]);
        if (pick === "SSS") { s += ticks(A, B, 1) + ticks(C, B, 1) + ticks(A, D, 2) + ticks(C, D, 2); bin = "SSS"; why = "Two pairs of sides are marked and the shared side matches itself: SSS."; label = "kite split by a shared diagonal; two pairs of sides marked"; }
        else if (pick === "SAS") { s += ticks(A, B, 1) + ticks(C, B, 1) + arcs(B, A, D, 1) + arcs(B, C, D, 1); bin = "SAS"; why = "A side, the angle at the top, and the shared side between them: SAS."; label = "kite split by a shared diagonal; top sides and top angles marked"; }
        else if (pick === "ASA") { s += arcs(B, A, D, 1) + arcs(B, C, D, 1) + arcs(D, A, B, 2) + arcs(D, C, B, 2); bin = "ASA"; why = "Two angles and the shared side between them: ASA."; label = "kite split by a shared diagonal; angles at both ends of the diagonal marked"; }
        else if (pick === "AAS") { s += arcs(A, B, D, 1) + arcs(C, B, D, 1) + arcs(B, A, D, 2) + arcs(B, C, D, 2); bin = "AAS"; why = "Two angles and the shared side, which is not between them: AAS."; label = "kite split by a shared diagonal; side-vertex angles and top angles marked"; }
        else { s += ticks(A, B, 1) + ticks(C, B, 1) + arcs(A, B, D, 1) + arcs(C, B, D, 1); bin = "N"; why = "With the shared side that's two sides and a non-included angle (SSA): not enough."; label = "kite split by a shared diagonal; top sides and side-vertex angles marked"; }
      } else {
        const E = [110, 60], a = c.ri(60, 90), h1 = c.ri(30, 48), b2 = c.ri(-20, 25);
        const A = [E[0] - a, E[1] - h1], Bp = [E[0] - a + b2 + 40, E[1] + h1 - 4], C = [2 * E[0] - A[0], 2 * E[1] - A[1]], D = [2 * E[0] - Bp[0], 2 * E[1] - Bp[1]];
        s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" aria-label="LABEL">` + poly([A, E, Bp]) + poly([C, E, D]);
        const pick = c.pick(["SAS", "ASA", "AAS", "N2", "SSS"]);
        if (pick === "SAS") { s += ticks(A, E, 1) + ticks(C, E, 1) + ticks(Bp, E, 2) + ticks(D, E, 2); bin = "SAS"; why = "Two pairs of sides plus the vertical angles between them: SAS."; label = "two triangles meeting at a point (vertical angles); the sides at the point marked"; }
        else if (pick === "ASA") { s += ticks(A, E, 1) + ticks(C, E, 1) + arcs(A, E, Bp, 1) + arcs(C, E, D, 1); bin = "ASA"; why = "An angle, the side, then the vertical angles: ASA."; label = "two triangles meeting at a point; one side pair and the far-end angles at that side marked"; }
        else if (pick === "AAS") { s += ticks(A, E, 1) + ticks(C, E, 1) + arcs(Bp, A, E, 1) + arcs(D, C, E, 1); bin = "AAS"; why = "Vertical angles, another angle pair, and a side that isn't between them: AAS."; label = "two triangles meeting at a point; one side pair and the angles across from it marked"; }
        else if (pick === "SSS") { s += ticks(A, E, 1) + ticks(C, E, 1) + ticks(Bp, E, 2) + ticks(D, E, 2) + ticks(A, Bp, 3) + ticks(C, D, 3); bin = "SSS"; bins = ["SSS", "SAS"]; why = "All three side pairs are marked: SSS works (and so does SAS with the vertical angles)."; label = "two triangles meeting at a point; all three side pairs marked"; }
        else { s += arcs(A, E, Bp, 1) + arcs(C, E, D, 1) + arcs(Bp, A, E, 2) + arcs(D, C, E, 2); bin = "N"; why = "Every angle matches (AAA), but no side is marked: not enough."; label = "two triangles meeting at a point; angle pairs marked but no sides"; }
      }
      return { html: s.replace("LABEL", label) + "</svg>", cls: "pic", bin, bins, why, label };
    };
    let kinds, bins;
    if (c.lvl === 0) { kinds = ["SSS", "SAS", "SSA", "AAA", "SS"]; bins = ["SSS", "SAS", "N"]; }
    else if (c.lvl === 1) { kinds = ["SSS", "SAS", "ASA", "AAS", "SSA", "AAA"]; bins = ["SSS", "SAS", "ASA", "AAS", "N"]; }
    else { kinds = ["SSS", "SAS", "ASA", "AAS", "HL", "SSA", "AAA"]; bins = ["SSS", "SAS", "ASA", "AAS", "HL", "N"]; }
    const N = c.n(10), cards = [];
    for (let k = 0; k < N; k++) cards.push(c.lvl === 3 && c.chance(.6) ? shared() : make(kinds[k % kinds.length]));
    const LBL = { SSS: "SSS", SAS: "SAS", ASA: "ASA", AAS: "AAS", HL: "HL", N: "Not enough" };
    return { bins: bins.map(b => ({ id: b, label: LBL[b] })), cards: c.shuffle(cards), deal: c.opt.deal === "deal", cols: 6 };
  }
});
