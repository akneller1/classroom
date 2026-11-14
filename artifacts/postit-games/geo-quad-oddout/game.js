PG.game({
  id: "geo-quad-oddout", title: ["Quadrilateral", "Odd One Out"], course: "Geometry", unit: "Quadrilaterals & Their Properties",
  tag: "Three quadrilaterals share a property. Which one doesn't?",
  skills: "G.CO.11, G.GPE.4 · parallelograms, rectangles, rhombuses, squares, trapezoids, kites · diagonals · symmetry",
  engine: "oddout",
  levels: [
    "Labeled pictures; properties about sides and angles.",
    "Names only, and diagonal properties join in.",
    "Unlabeled pictures. Then explain your choice.",
    "Unlabeled pictures, every property in play, and you explain your choice."
  ],
  round(c) {
    const SH = ["square", "rectangle", "rhombus", "parallelogram", "trapezoid", "isosceles trapezoid", "kite"];
    const PROPS = [
      ["Both pairs of opposite sides are parallel", ["square", "rectangle", "rhombus", "parallelogram"], 0],
      ["Exactly one pair of parallel sides", ["trapezoid", "isosceles trapezoid"], 0],
      ["Four right angles", ["square", "rectangle"], 0],
      ["Four congruent sides", ["square", "rhombus"], 0],
      ["Opposite angles are congruent", ["square", "rectangle", "rhombus", "parallelogram"], 0],
      ["Diagonals are perpendicular", ["square", "rhombus", "kite"], 1],
      ["Diagonals are congruent", ["square", "rectangle", "isosceles trapezoid"], 1],
      ["Diagonals bisect each other", ["square", "rectangle", "rhombus", "parallelogram"], 1],
      ["Has at least one line of symmetry", ["square", "rectangle", "rhombus", "isosceles trapezoid", "kite"], 1],
      ["Two pairs of adjacent sides are congruent", ["square", "rhombus", "kite"], 1]
    ];
    const allowed = PROPS.filter(p => c.lvl === 0 ? p[2] === 0 : true);
    const has = (s, p) => p[1].includes(s);
    const draw = s => {
      const rot = c.r() * 360;
      let P;
      if (s === "square") P = [[0, 0], [1, 0], [1, 1], [0, 1]];
      else if (s === "rectangle") P = [[0, 0], [1.6, 0], [1.6, .9], [0, .9]];
      else if (s === "rhombus") { const a = 62 * Math.PI / 180; P = [[0, 0], [1, 0], [1 + Math.cos(a), Math.sin(a)], [Math.cos(a), Math.sin(a)]]; }
      else if (s === "parallelogram") P = [[0, 0], [1.5, 0], [1.9, .8], [.4, .8]];
      else if (s === "trapezoid") P = [[0, 0], [1.7, 0], [1.2, .8], [.25, .8]];
      else if (s === "isosceles trapezoid") P = [[0, 0], [1.7, 0], [1.3, .8], [.4, .8]];
      else P = [[0, 0], [.6, -.45], [1.6, 0], [.6, .45]];
      const r = rot * Math.PI / 180; P = P.map(([x, y]) => [x * Math.cos(r) - y * Math.sin(r), x * Math.sin(r) + y * Math.cos(r)]);
      const xs = P.map(p => p[0]), ys = P.map(p => p[1]); const sc = 70 / Math.max(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys));
      const mx = (Math.max(...xs) + Math.min(...xs)) / 2, my = (Math.max(...ys) + Math.min(...ys)) / 2;
      P = P.map(([x, y]) => [45 + (x - mx) * sc, 45 + (y - my) * sc]);
      return `<svg viewBox="0 0 90 90" width="90" height="90" aria-label="a quadrilateral"><polygon points="${P.map(p => p.map(v => v.toFixed(1)).join(",")).join(" ")}" fill="#fff" stroke="#13202f" stroke-width="2.5" stroke-linejoin="round"/></svg>`;
    };
    const N = c.n(6), puzzles = [];
    let g = 0;
    while (puzzles.length < N && g++ < 2000) {
      const P = c.pick(allowed);
      const yes = SH.filter(s => has(s, P)), no = SH.filter(s => !has(s, P));
      if (yes.length < 3 || !no.length) continue;
      const set = c.sample(yes, 3).concat([c.pick(no)]);
      // the odd card must be the only one that some property isolates
      const isolates = j => allowed.some(Q => set.every((s, k) => k === j ? !has(s, Q) : has(s, Q)));
      const iso = set.map((_, j) => isolates(j));
      if (!iso[3] || iso.slice(0, 3).some(Boolean)) continue;
      const okReasons = allowed.filter(Q => set.every((s, k) => k === 3 ? !has(s, Q) : has(s, Q)));
      const bad = c.sample(allowed.filter(Q => !okReasons.includes(Q)), 2);
      if (bad.length < 2) continue;
      const sig = set.slice().sort().join();
      if (puzzles.some(p => p.sig === sig)) continue;
      const order = c.shuffle([0, 1, 2, 3]);
      const pics = c.lvl !== 1, names = c.lvl <= 1;
      const cards = order.map(k => { const s = set[k]; return pics ? { html: draw(s) + (names ? `<div style="font:700 .78rem var(--f-body)">${s}</div>` : ""), cls: "pic", label: names ? s : "quadrilateral: " + s } : { html: s, cls: "txt" }; });
      const right = "The other three: " + P[0].toLowerCase() + ".";
      const reasons = c.shuffle([right].concat(bad.map(Q => "The other three: " + Q[0].toLowerCase() + ".")));
      puzzles.push({ sig, cards, odd: order.indexOf(3), reasons, reason: reasons.indexOf(right), why: `The ${set[3]} is the odd one out. ${P[0]}: true for ${set.slice(0, 3).join(", ")}, but not for a ${set[3]}.` });
    }
    return { puzzles, cw: "150px", reasonFrom: 2 };
  }
});
