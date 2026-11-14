PG.game({
  id: "geo-volume-lineup", title: ["Volume", "Line-Up"], course: "Geometry", unit: "Volume of Solids",
  tag: "Order the solids from least to greatest volume.",
  skills: "G.GMD.3 · volume of prisms, cylinders, pyramids, cones and spheres · the ⅓ factor · radius vs diameter",
  engine: "order",
  levels: [
    "Prisms and cylinders.",
    "Cones and pyramids join in. Remember the ⅓.",
    "Spheres too, with volumes close together.",
    "Some give the diameter, some the radius. You check the order yourself."
  ],
  how: ["Work out (or estimate) each volume. Leave π as about 3.14.", "Order from least volume on the left to greatest on the right."],
  round(c) {
    const ink = "#13202f";
    const icon = t => {
      const st = `fill="#fff" stroke="${ink}" stroke-width="1.8"`;
      if (t === "prism") return `<svg viewBox="0 0 60 50" width="60" height="50" aria-hidden="true"><path d="M8 18 L36 18 L36 46 L8 46 Z" ${st}/><path d="M8 18 L20 6 L48 6 L36 18 M36 46 L48 34 L48 6" ${st}/></svg>`;
      if (t === "cyl") return `<svg viewBox="0 0 60 50" width="60" height="50" aria-hidden="true"><path d="M12 10 V40 A18 6 0 0 0 48 40 V10" ${st}/><ellipse cx="30" cy="10" rx="18" ry="6" ${st}/></svg>`;
      if (t === "cone") return `<svg viewBox="0 0 60 50" width="60" height="50" aria-hidden="true"><path d="M30 4 L12 40 A18 6 0 0 0 48 40 Z" ${st}/><path d="M12 40 A18 6 0 0 1 48 40" fill="none" stroke="${ink}" stroke-dasharray="3 3"/></svg>`;
      if (t === "pyr") return `<svg viewBox="0 0 60 50" width="60" height="50" aria-hidden="true"><path d="M30 4 L8 42 L38 46 L52 36 Z M30 4 L38 46" ${st}/></svg>`;
      return `<svg viewBox="0 0 60 50" width="60" height="50" aria-hidden="true"><circle cx="30" cy="25" r="21" ${st}/><ellipse cx="30" cy="25" rx="21" ry="6" fill="none" stroke="${ink}" stroke-dasharray="3 3"/></svg>`;
    };
    const types = c.lvl === 0 ? ["prism", "cyl"] : c.lvl === 1 ? ["prism", "cyl", "cone", "pyr"] : ["prism", "cyl", "cone", "pyr", "sph"];
    const n = [4, 5, 6, 6][c.lvl] + (c.len === 2 ? 1 : 0);
    const cards = [];
    let g = 0;
    while (cards.length < n && g++ < 1000) {
      const t = c.pick(types); let V, txt, name;
      const useD = c.lvl === 3 && c.chance(.5);
      if (t === "prism") { const l = c.ri(2, 9), w = c.ri(2, 8), hh = c.ri(2, 10); V = l * w * hh; name = "Rectangular prism"; txt = `${l} × ${w} × ${hh}`; }
      else if (t === "cyl") { const r = c.ri(1, 5), hh = c.ri(2, 10); V = Math.PI * r * r * hh; name = "Cylinder"; txt = `${useD ? "d = " + 2 * r : "r = " + r}, h = ${hh}`; }
      else if (t === "cone") { const r = c.ri(2, 6), hh = c.ri(3, 12); V = Math.PI * r * r * hh / 3; name = "Cone"; txt = `${useD ? "d = " + 2 * r : "r = " + r}, h = ${hh}`; }
      else if (t === "pyr") { const s = c.ri(3, 10), hh = c.ri(3, 12); V = s * s * hh / 3; name = "Square pyramid"; txt = `base ${s} × ${s}, h = ${hh}`; }
      else { const r = c.ri(1, 5); V = 4 / 3 * Math.PI * r ** 3; name = "Sphere"; txt = useD ? `d = ${2 * r}` : `r = ${r}`; }
      if (V > 700 || V < 6) continue;
      const gapMin = c.lvl >= 2 ? .06 : .15;
      if (cards.some(o => Math.abs(o.v - V) / Math.max(o.v, V) < gapMin)) continue;
      cards.push({ v: V, html: `${icon(t)}<div style="font:700 .78rem var(--f-body);line-height:1.2">${name}<br><span style="font-weight:500">${txt}</span></div>`, cls: "pic", label: `${name}, ${txt}`, say: `V ≈ ${+V.toFixed(1)}` });
    }
    return { cards, endCheck: c.lvl === 3, slotMin: 118, tol: 1e-6,
      why: card => c.mode === "practice" ? `This one is about ${+card.v.toFixed(1)} cubic units.` : "" };
  }
});
