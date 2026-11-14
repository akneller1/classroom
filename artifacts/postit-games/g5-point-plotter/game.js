PG.game({
  id: "g5-point-plotter", title: ["Point", "Plotter"], course: "Grade 5", unit: "The Coordinate Plane",
  tag: "Drop each ordered pair on its point.",
  skills: "5.G.1–2 · ordered pairs · x first, then y · points on the axes · coordinates from rules",
  engine: "spots",
  levels: [
    "Points from 0 to 6.",
    "Points up to 10, with flipped pairs like (3, 7) and (7, 3).",
    "Points on the axes too, like (0, 4) and (6, 0).",
    "Pairs described by rules: “x is 4 and y is 2 more than x”."
  ],
  round(c) {
    const M = c.lvl === 0 ? 6 : 10;
    const P = PG.svg.plane({ xmin: 0, xmax: M, ymin: 0, ymax: M, size: 440, pad: 30, ink: "currentColor", gridc: "rgba(120,140,170,.35)", labels: 1, fs: 13, aw: 2 });
    let s = P.s + `<text x="${P.X(M) + 4}" y="${P.Y(0) + 4}" font-size="14" font-style="italic" fill="currentColor">x</text><text x="${P.X(0) - 4}" y="${P.Y(M) - 10}" font-size="14" font-style="italic" fill="currentColor">y</text>` + P.close;
    s = s.replace('<svg ', '<svg overflow="visible" ');
    const n = c.n([5, 7, 8, 7][c.lvl]);
    const pts = [];
    let g = 0;
    const far = (x, y) => pts.every(p => Math.abs(p[0] - x) + Math.abs(p[1] - y) >= 2);
    while (pts.length < n && g++ < 500) {
      let x = c.ri(c.lvl >= 2 ? 0 : 1, M), y = c.ri(c.lvl >= 2 ? 0 : 1, M);
      if (c.lvl === 2 && c.chance(.3)) { if (c.chance(.5)) x = 0; else y = 0; }
      if (x === 0 && y === 0) continue;
      if (!far(x, y)) continue;
      pts.push([x, y]);
      if (c.lvl >= 1 && x !== y && pts.length < n && far(y, x) && c.chance(.6)) pts.push([y, x]);
    }
    const rule = ([x, y]) => {
      const opts = [];
      if (y === x) opts.push(`x is ${x} and y equals x`);
      if (y > x) opts.push(`x is ${x} and y is ${y - x} more than x`);
      if (y < x) opts.push(`x is ${x} and y is ${x - y} less than x`);
      if (x && y === 2 * x) opts.push(`x is ${x} and y is double x`);
      if (y && x === 2 * y) opts.push(`y is ${y} and x is double y`);
      if (y === 0) opts.push(`on the x-axis, ${x} units from the origin`);
      if (x === 0) opts.push(`on the y-axis, ${y} units up`);
      opts.push(`${x} right of the y-axis, ${y} above the x-axis`);
      return c.pick(opts);
    };
    const spots = pts.map(([x, y], i) => ({ x: P.X(x), y: P.Y(y), key: x + "," + y, cls: "dot", label: `Point ${i + 1}` }));
    const cards = pts.map(([x, y]) => c.lvl === 3 ? { html: rule([x, y]), key: x + "," + y, cls: "txt", say: `(${x}, ${y})` } : { html: `(${x}, ${y})`, key: x + "," + y, label: `${x} comma ${y}` });
    return { svg: s, w: P.w, h: P.h, spots, cards, maxW: "560px", trayTitle: "Ordered pairs", fill: card => "(" + card.key.replace(",", ", ") + ")",
      why: (card, spot) => { const [x, y] = card.key.split(",").map(Number); return c.mode === "practice" ? `Start at the origin. Go ${x} right along the x-axis, then ${y} up.` : "x comes first (across), then y (up)."; } };
  }
});
