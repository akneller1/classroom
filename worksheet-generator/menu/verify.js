/* Menu Assessment Generator — problem verification.

   verifyProblem(problem, policy) re-derives every answer from what the STUDENT sees:
   the math named by a part's `check` must appear verbatim (inside ⟨…⟩) in the student
   prompt, and is then parsed and solved by menu/mathcheck.js (independent parser and
   BigInt arithmetic; no generator code). Word problems are re-solved from the numbers
   and words printed in the prompt by the scenario checkers below.

   Result: { ok, status, issues:[…], computed:[per-part computed answer text] }
     status: 'verified' | 'mismatch' | 'invalid' | 'manual' (no automatic check possible)
*/
(function (G) {
  'use strict';
  var NS = (G.MKMENU = G.MKMENU || {});
  var C = NS.check, Q = C.Q;

  function studentText(p) {
    return [p.prompt || ''].concat((p.work || []).map(function (w) { return '⟨' + w + '⟩'; })).concat((p.parts || []).map(function (pt) { return pt.prompt || ''; })).join(' ');
  }
  function shown(p, tex) {
    return C.snippets(studentText(p)).some(function (s) { return norm(s) === norm(tex); });
  }
  // Geometry word/figure prompts can require students to formulate the equation.
  // Never bypass the independent derivation checks for variants that require them.
  function geometryDerived(p, chk) {
    if (!chk || chk.type !== 'solve' || !/^geo-/.test(p.variant || '')) return false;
    // These foundation prompts explicitly print their checked equation.
    // Keep strict equation matching so tampered printed values are rejected.
    if (/^geo-(segment|angle)-/.test(p.variant || '')) return false;
    /* Parallel lines + transversal: the equation is rebuilt from the FIGURE (which pair of positions is marked, so
       equal or supplementary) and the printed labels, never from the generator's own bookkeeping. */
    if (/^geo-transversal-/.test(p.variant || '') && p.fig && p.fig.kind === 'geo-transversal' && NS.geoFigures) {
      var mk = p.fig.marks || [], ex = null, nu = null;
      if (mk.length !== 2) return false;
      mk.forEach(function (m) { if (/x/.test(m.text)) ex = m; else nu = m; });
      if (!ex || !nu) return false;
      var em = /^\((\d*)x\+(\d+)\)°$/.exec(ex.text), nm = /^(\d+)°$/.exec(nu.text);
      if (!em || !nm) return false;
      var rel = NS.geoFigures.relationship(ex.pos, nu.pos), coef = em[1] === '' ? 1 : Number(em[1]), lhs = (coef === 1 ? 'x' : coef + 'x') + '+' + em[2];
      var want = NS.geoFigures.relationEquals(rel) ? lhs + '=' + nm[1] : NS.geoFigures.relationSupplementary(rel) ? lhs + '+' + nm[1] + '=180' : null;
      // when the prompt also prints the givens, they must agree with the figure
      if (/relevant angle measures/.test(p.prompt || '') && (p.prompt || '').indexOf('⟨' + lhs + '⟩ degrees and ' + nm[1] + ' degrees') < 0) return false;
      return want !== null && want === chk.eq;
    }
    /* Right-triangle trig investigation: every equation is rebuilt from the printed hypotenuse and sine/cosine ratios. */
    if (/^geo-right-investigation-/.test(p.variant || '')) {
      var pr = p.parts || [], rix = -1; pr.forEach(function (pt, i) { if (pt.check === chk) rix = i; });
      var hm = /hypotenuse (\d+) units/.exec(C.plainText(p.prompt || '')), fm = /\\sin\\theta=\\frac\{(\d+)\}\{(\d+)\}/.exec(p.prompt || ''), cm = pr[1] && /\\cos\\theta=\\frac\{(\d+)\}\{(\d+)\}/.exec(pr[1].prompt || '');
      if (rix < 0 || pr.length !== 4 || !hm || !fm || !cm) return false;
      var HH = Number(hm[1]), oo = Number(fm[1]), hh = Number(fm[2]), aa = Number(cm[1]);
      if (Number(cm[2]) !== hh || hh <= 0 || oo >= hh || aa >= hh || oo * oo + aa * aa !== hh * hh || HH % hh) return false;
      var kk = HH / hh, OO = oo * kk, DD = aa * kk;
      return chk.eq === [hh + '*x=' + oo + '*' + HH, hh + '*y=' + aa + '*' + HH, 'P=' + OO + '+' + DD + '+' + HH, '2*w=' + OO + '*' + DD][rix];
    }
    /* Four-part Open Response investigations: each part's equation may use only numbers printed for students,
       a standard constant, or an answer from an earlier part. A changed printed number therefore invalidates the key. */
    if (/^geo-(angles|circles|polygons|transformations|solids|congruence)-investigation-/.test(p.variant || '')) {
      var pts = p.parts || [], ix = -1; pts.forEach(function (pt, i) { if (pt.check === chk) ix = i; });
      if (ix < 0 || pts.length < 4) return false;
      if (/^geo-solids-/.test(p.variant)) {   // exact re-derivation from the printed dimensions
        var sd = /length (\d+) cm, width (\d+) cm, and height (\d+) cm/.exec(C.plainText(p.prompt || '')), sb = /base area of (\d+) square/.exec(C.plainText(pts[3].prompt || ''));
        if (!sd || !sb) return false;
        var L0 = sd[1], W0 = sd[2], H0 = sd[3], want = ['x=' + L0 + '*' + W0, 'y=' + L0 + '*' + W0 + '*' + H0, 'z=2*' + L0 + '*' + W0 + '+2*' + L0 + '*' + H0 + '+2*' + W0 + '*' + H0, sb[1] + '*k=' + (L0 * W0 * H0)];
        return chk.eq === want[ix];
      }
      /* Congruence investigations (algebra, isosceles, overlap): the loose "digit was printed somewhere" test below
         lets a changed printed number slip through whenever the old digit appears elsewhere in the text. Instead, rebuild
         each part's equation from the printed givens and the earlier answers, and require an exact match. */
      if (/^geo-congruence-investigation-(algebra|isosceles|overlap)-/.test(p.variant || '')) {
        var cpr = String(p.prompt || ''), cwant = null;
        var cans = function (j, v) { var mm = new RegExp(v + '\\s*=\\s*(-?\\d+)').exec(String((pts[j] || {}).answer || '')); return mm ? mm[1] : null; };
        var cM = '⟨([^⟩]*)⟩';
        if (/-algebra-/.test(p.variant)) {
          var am2 = new RegExp('AB = ' + cM + ' and DE = ' + cM + '\\. BC = ' + cM + ' and EF = (\\d+)\\. AC = ' + cM + '\\..*?angle C is ⟨\\(([^⟩]*)\\)⟩ degrees and the measure of angle F is ⟨\\(([^⟩]*)\\)⟩ degrees').exec(cpr);
          if (!am2) return false;
          var xA = cans(0, 'x'), yA = cans(1, 'y');
          if (ix === 0) cwant = am2[1] + '=' + am2[2];
          else if (ix === 3) cwant = am2[6] + '=' + am2[7];
          else {
            var bcm = /^(\d*)y\+x$/.exec(norm(am2[3]));
            if (!bcm) return false;
            var pcA = bcm[1] === '' ? '1' : bcm[1];
            if (ix === 1) { if (xA === null) return false; cwant = pcA + '*y+' + xA + '=' + am2[4]; }
            else {
              var abm = /^(\d*)x(?:([+-])(\d+))?$/.exec(norm(am2[1])), acm = /^(\d*)x-(\d*)y$/.exec(norm(am2[5]));
              if (!abm || !acm || xA === null || yA === null) return false;
              var a1A = abm[1] === '' ? '1' : abm[1], b1A = abm[2] ? (abm[2] === '-' ? '-' : '+') + abm[3] : '+0', uA = acm[1] === '' ? '1' : acm[1], wA = acm[2] === '' ? '1' : acm[2];
              cwant = 'w=(' + a1A + '*' + xA + b1A + ')+(' + pcA + '*' + yA + '+' + xA + ')+(' + uA + '*' + xA + '-' + wA + '*' + yA + ')';
            }
          }
        } else if (/-isosceles-/.test(p.variant)) {
          var im = new RegExp('Angle BAD measures ⟨\\(([^⟩]*)\\)⟩ degrees and angle CAD measures (\\d+) degrees').exec(cpr);
          if (!im) return false;
          cwant = ix === 0 ? im[1] + '=' + im[2] : ix === 1 ? 'w=' + im[2] + '+' + im[2] : ix === 2 ? 'w+w+' + (2 * Number(im[2])) + '=180' : 'w+w=180';
        } else {
          var om = new RegExp('AB = ' + cM + ' and CD = ' + cM + '\\. Angle ABD measures ⟨\\(([^⟩]*)\\)⟩ degrees and angle CDB measures (\\d+) degrees\\. Angle ADB measures ⟨\\(([^⟩]*)\\)⟩ degrees and angle CBD measures (\\d+) degrees').exec(cpr);
          if (!om) return false;
          cwant = ix === 0 ? om[1] + '=' + om[2] : ix === 1 ? om[3] + '=' + om[4] : ix === 2 ? om[5] + '=' + om[6] : 'w+' + om[4] + '+' + om[6] + '=180';
        }
        return cwant !== null && norm(chk.eq) === norm(cwant);
      }
      var okNum = {}; // Congruence chains print their expressions inside math, so their digits count too
      ((/^geo-congruence-/.test(p.variant || '') ? studentText(p).replace(/<[^>]+>/g, ' ') : C.plainText(studentText(p))).match(/\d+/g) || []).forEach(function (n) { okNum[String(Number(n))] = 1; });
      [0, 1, 2, 180, 360].forEach(function (n) { okNum[n] = 1; });
      for (var pj = 0; pj < ix; pj++) { var am = /=\s*(-?\d+)/.exec(String(pts[pj].answer || '')) || /^\s*⟨?\s*(-?\d+)\s*⟩?\s*$/.exec(String(pts[pj].answer || '')); if (am) okNum[String(Math.abs(Number(am[1])))] = 1; }
      return (chk.eq.match(/\d+/g) || []).every(function (n) { return okNum[String(Number(n))]; });
    }
    /* Shadow problems: x is recomputed from the printed heights and shadows (h/s = x/S), and the figure must show the same four numbers. */
    if (/^geo-sim-shadow-/.test(p.variant || '')) {
      var sw = C.plainText(p.prompt || ''), sm = /pole (\d+) feet tall casts a (\d+)-foot shadow\. A nearby tree casts a (\d+)-foot shadow/.exec(sw);
      if (!sm || !p.fig || p.fig.kind !== 'geo-shadow') return false;
      var sh = Number(sm[1]), ss = Number(sm[2]), sS = Number(sm[3]);
      if (p.fig.h !== sh || p.fig.s !== ss || p.fig.S !== sS || !p.fig.lab || p.fig.lab.H !== 'x' || p.fig.H * ss !== sh * sS) return false;
      var ssol = C.solveLinear(chk.eq, chk.v || 'x');
      return !!ssol && ssol.value && Number(ssol.value.n) * ss === sh * sS * Number(ssol.value.d);
    }
    /* Coordinate-grid transformations: the asked image coordinate is recomputed from the FIGURE (vertex positions, mirror line, drawn image)
       and the printed transformation, then compared with the solution of the checked equation. */
    /* Area, surface area and volume: the answer is recomputed from the numbers printed in the question (or, for nets and stacked solids, from the figure alone). */
    if (/^geo-measure-/.test(p.variant || '')) {
      var mv = String(p.variant).replace(/^geo-measure-/, '').replace(/-\d+$/, ''), mt = C.plainText(p.prompt || ''), mn = (mt.match(/\d+(?:\.\d+)?/g) || []).map(Number), mf = p.fig, me = null, a0 = mn[0], b0 = mn[1], c0 = mn[2];
      var need = { rectangle: 2, triangle: 2, parallelogram: 2, trapezoid: 3, 'prism-volume': 3, 'prism-surface': 3, 'cylinder-volume': 2, 'cylinder-surface': 2, pyramid: 3, 'cone-volume': 2, 'sphere-surface': 1, 'prism-height': 3, 'cylinder-height': 2 };
      if (mv === 'net') {
        if (!mf || mf.kind !== 'geo-net' || !NS.geoFigures.check(mf).ok || mn.length) return false;
        me = [2 * (mf.l * mf.w + mf.l * mf.h + mf.w * mf.h), 1];
      } else if (mv === 'stack') {
        if (!mf || mf.kind !== 'geo-stack' || !NS.geoFigures.check(mf).ok || mn.length) return false;
        me = [mf.a.l * mf.a.w * mf.a.h + mf.b.l * mf.b.w * mf.b.h, 1];
      } else if (mv === 'rotate') {
        if (!mf || mf.kind !== 'geo-rotate' || !NS.geoFigures.check(mf).ok || mn.length) return false;
        me = mf.shape === 'rect' ? [mf.a * mf.a * mf.b, 1] : mf.shape === 'tri' ? [mf.a * mf.a * mf.b, 3] : mf.shape === 'semi' ? [4 * mf.a * mf.a * mf.a, 3] : null;
      } else if (/^section-/.test(mv)) {
        var sk = mv.slice(8), sn = { cylv: 2, cylh: 2, sph: 2, cone: 2, conev: 3 };
        if (mf || sn[sk] === undefined || mn.length !== sn[sk]) return false;
        if (sk === 'sph' && !(b0 > 0 && b0 < a0)) return false;
        if (sk === 'conev' && !(c0 > 0 && c0 < b0)) return false;
        me = sk === 'cylv' ? [2 * a0 * b0, 1] : sk === 'cylh' ? [a0 * a0, 1] : sk === 'sph' ? [a0 * a0 - b0 * b0, 1] : sk === 'cone' ? [a0 * a0, 4] : [a0 * a0 * c0 * c0, b0 * b0];
        var wantText = sk === 'cylv' ? /perpendicular to its bases/ : sk === 'cylh' ? /parallel to the bases/ : sk === 'sph' ? /cuts the sphere \d+ cm from its center/ : sk === 'cone' ? /parallel to the base cuts the cone halfway up/ : /parallel to the base cuts the cone \d+ cm from the vertex/;
        if (!wantText.test(mt)) return false;
      } else if (mv === 'sphere-volume') {
        var sr = /diameter (\d+)/.exec(mt); if (mn.length !== 1) return false; me = sr ? [4 * (Number(sr[1]) / 2) * (Number(sr[1]) / 2) * (Number(sr[1]) / 2), 3] : [4 * a0 * a0 * a0, 3];
      } else {
        if (need[mv] === undefined || mn.length !== need[mv]) return false;
        me = mv === 'rectangle' || mv === 'parallelogram' ? [a0 * b0, 1] : mv === 'triangle' ? [a0 * b0, 2] : mv === 'trapezoid' ? [(a0 + b0) * c0, 2]
          : mv === 'prism-volume' ? [a0 * b0 * c0, 1] : mv === 'prism-surface' ? [2 * (a0 * b0 + a0 * c0 + b0 * c0), 1] : mv === 'cylinder-volume' ? [a0 * a0 * b0, 1]
          : mv === 'cylinder-surface' ? [2 * a0 * (a0 + b0), 1] : mv === 'pyramid' ? [a0 * b0 * c0, 3] : mv === 'cone-volume' ? [a0 * a0 * b0, 3] : mv === 'sphere-surface' ? [4 * a0 * a0, 1]
          : mv === 'prism-height' ? [c0, a0 * b0] : mv === 'cylinder-height' ? [b0, a0 * a0] : null;
      }
      if (!me) return false;
      var msol; try { msol = C.solveLinear(chk.eq, 'x'); } catch (e) { return false; }
      return !!msol && msol.kind === 'one' && Number(msol.value.n) * me[1] === me[0] * Number(msol.value.d);
    }
    /* Symmetry of a regular polygon: the number of sides is read from the FIGURE; x must equal n (lines) or satisfy n·x = 360 (rotation). */
    if (/^geo-symmetry-(lines|rotation)-/.test(p.variant || '')) {
      var yn = p.fig && p.fig.kind === 'geo-regular' ? p.fig.n : null; if (!(yn >= 3) || !NS.geoFigures.check(p.fig).ok) return false;
      var yt = C.plainText(p.prompt || ''), ysol; try { ysol = C.solveLinear(chk.eq, 'x'); } catch (e) { return false; }
      if (!ysol || ysol.kind !== 'one') return false;
      var yv = Number(ysol.value.n) / Number(ysol.value.d), yl = /^geo-symmetry-lines-/.test(p.variant);
      if (yl && !/lines of symmetry/.test(yt)) return false;
      if (!yl && !/smallest positive rotation/.test(yt)) return false;
      if (/\b\d+ sides\b/.test(yt) || /regular \d+-gon/.test(yt)) return false;
      return yl ? (yv === yn && chk.eq === 'x=' + yn) : (Math.abs(yv - 360 / yn) < 1e-9 && chk.eq === yn + '*x=360');
    }
    if (/^geo-transform-fig-compose-/.test(p.variant || '') && p.fig && p.fig.kind === 'geo-grid' && NS.geoFigures && NS.geoFigures.grid) {
      var cpre = p.fig.shapes && p.fig.shapes[0], cimg = p.fig.shapes && p.fig.shapes[2], ctx_ = String(p.prompt || ''), cm = /(x|y)-coordinate of ([A-Z])″/.exec(ctx_);
      if (!cpre || !cimg || !cpre.labels || !cm || p.fig.shapes.length !== 3) return false;
      var ci = cpre.labels.indexOf(cm[2]); if (ci < 0) return false;
      var cre = /([A-Z])\((-?\d+), (-?\d+)\)/g, cv, cseen = 0;
      while ((cv = cre.exec(ctx_))) { var cj = cpre.labels.indexOf(cv[1]); if (cj < 0 || cpre.pts[cj][0] !== Number(cv[2]) || cpre.pts[cj][1] !== Number(cv[3])) return false; cseen++; }
      if (cseen !== cpre.pts.length) return false;
      var c1 = /It is first (reflected across the x-axis|reflected across the y-axis|rotated 90° clockwise about the origin|rotated 90° counterclockwise about the origin) to form/.exec(ctx_), c2 = /and then translated (\d+) units? (right|left) and (\d+) units? (up|down) to form/.exec(ctx_);
      if (!c1 || !c2) return false;
      var ct = c1[1] === 'reflected across the x-axis' ? 'reflect-x' : c1[1] === 'reflected across the y-axis' ? 'reflect-y' : /counterclockwise/.test(c1[1]) ? 'rotate-ccw' : 'rotate-cw';
      var cdx = (c2[2] === 'left' ? -1 : 1) * Number(c2[1]), cdy = (c2[4] === 'down' ? -1 : 1) * Number(c2[3]);
      var cq = NS.geoFigures.grid.apply({ type: ct }, cpre.pts[ci]); cq = [cq[0] + cdx, cq[1] + cdy];
      var cmid = p.fig.shapes[1]; if (!cmid || cmid.of !== 'pre' || cmid.tx.type !== ct || cimg.of !== 'mid' || cimg.tx.type !== 'translate' || cimg.tx.dx !== cdx || cimg.tx.dy !== cdy) return false;
      if (cimg.pts[ci][0] !== cq[0] || cimg.pts[ci][1] !== cq[1]) return false;
      var cs; try { cs = C.solveLinear(chk.eq, 'x'); } catch (e) { return false; }
      return cs.kind === 'one' && String(cs.value.d) === '1' && String(cs.value.n) === String(cq[cm[1] === 'x' ? 0 : 1]);
    }
    if (/^geo-transform-fig-/.test(p.variant || '') && p.fig && p.fig.kind === 'geo-grid' && NS.geoFigures && NS.geoFigures.grid) {
      var gpre = p.fig.shapes && p.fig.shapes[0], gtxt = String(p.prompt || ''), gm = /(x|y)-coordinate of ([A-Z])′/.exec(gtxt);
      if (!gpre || !gpre.labels || !gm) return false;
      var gi = gpre.labels.indexOf(gm[2]); if (gi < 0) return false;
      var gre = /([A-Z])\((-?\d+), (-?\d+)\)/g, gv, gseen = 0;
      while ((gv = gre.exec(gtxt))) { var gj = gpre.labels.indexOf(gv[1]); if (gj < 0 || gpre.pts[gj][0] !== Number(gv[2]) || gpre.pts[gj][1] !== Number(gv[3])) return false; gseen++; }
      if (gseen !== gpre.pts.length) return false;
      var gk = String(p.variant).split('-')[3], gq = null, gp0 = gpre.pts[gi], GA = NS.geoFigures.grid.apply;
      if (gk === 'translate') {
        var gimg = p.fig.shapes[1]; if (!gimg || !/translated/.test(gtxt)) return false;
        var sdx = gimg.pts[0][0] - gpre.pts[0][0], sdy = gimg.pts[0][1] - gpre.pts[0][1];
        for (var gz = 0; gz < gpre.pts.length; gz++) if (gimg.pts[gz][0] - gpre.pts[gz][0] !== sdx || gimg.pts[gz][1] - gpre.pts[gz][1] !== sdy) return false;
        gq = gimg.pts[gi];
      } else if (gk === 'reflect') {
        var gl = p.fig.lines && p.fig.lines[0]; if (!gl || !/across the dashed line/.test(gtxt)) return false;
        gq = GA({ type: 'reflect-line', line: gl }, gp0);
      } else if (gk === 'rotate') {
        var gt = /counterclockwise/.test(gtxt) ? 'rotate-ccw' : /clockwise/.test(gtxt) ? 'rotate-cw' : /180°/.test(gtxt) ? 'rotate-180' : null;
        if (!gt) return false; gq = GA({ type: gt }, gp0);
      } else if (gk === 'dilate') {
        var gkm = /scale factor of (\d+)/.exec(gtxt); if (!gkm) return false; gq = GA({ type: 'dilate', k: Number(gkm[1]) }, gp0);
      } else return false;
      var gs; try { gs = C.solveLinear(chk.eq, 'x'); } catch (e) { return false; }
      return gs.kind === 'one' && String(gs.value.d) === '1' && String(gs.value.n) === String(gq[gm[1] === 'x' ? 0 : 1]);
    }
    if (/^geo-bisector-/.test(p.variant || '')) {
      var measures = /Angle ABD measures ⟨([^⟩]+)⟩ degrees, and angle DBC measures (\d+) degrees/.exec(p.prompt || '');
      return !!measures && measures[1]+'='+measures[2] === chk.eq;
    }
    if (/^geo-congruence-third-angle-/.test(p.variant || '')) {
      var angles = /angle A is ([0-9]+)° and angle C is ([0-9]+)°/.exec(p.prompt || '');
      return !!angles && chk.eq === 'x+'+angles[1]+'+'+angles[2]+'=180' && shown(p,chk.eq);
    }
    if (/^geo-circle-intercepted-expression-/.test(p.variant || '')) {
      var interceptedExpr=/inscribed angle measures ([0-9]+) degrees\. Its intercepted arc is labeled \(2x\+([0-9]+)\) degrees/.exec(p.prompt || '');
      if (!interceptedExpr) return false;
      var ia=Number(interceptedExpr[1]), io=Number(interceptedExpr[2]);
      return ia>0 && ia<90 && io>0 && io<2*ia && (2*ia-io)%2===0 &&
        chk.eq==='2*x+'+io+'='+(2*ia);
    }
    if (/^geo-circle-inscribed-expression-/.test(p.variant || '')) {
      var inscribedExpr=/inscribed angle has measure \(x\+([0-9]+)\) degrees and intercepts an arc measuring ([0-9]+) degrees/.exec(p.prompt || '');
      if (!inscribedExpr) return false;
      var ieOffset=Number(inscribedExpr[1]), ieArc=Number(inscribedExpr[2]);
      return ieOffset>0 && ieArc>0 && ieArc<360 && ieArc%2===0 && ieArc/2>ieOffset &&
        chk.eq==='2*(x+'+ieOffset+')='+ieArc;
    }
    if (/^geo-circle-central-expression-/.test(p.variant || '')) {
      var centralExpr=/minor arc has measure \(2x\+([0-9]+)\) degrees, and its central angle measures ([0-9]+) degrees/.exec(p.prompt || '');
      if (!centralExpr) return false;
      var offsetCentral=Number(centralExpr[1]), angleCentral=Number(centralExpr[2]);
      return offsetCentral>0 && angleCentral>offsetCentral && angleCentral<180 &&
        (angleCentral-offsetCentral)%2===0 &&
        chk.eq==='2*x+'+offsetCentral+'='+angleCentral;
    }
    if (/^geo-circle-expanded-radius-mixed-/.test(p.variant || '')) {
      var mixed=/equation X\^2 \+ ([0-9]+)X \+ Y\^2 - ([0-9]+)Y ([+-]) ([0-9]+) = 0/.exec(p.prompt || '');
      if (!mixed) return false;
      var mx=Number(mixed[1]), my=Number(mixed[2]), mc=(mixed[3]==='-'?-1:1)*Number(mixed[4]);
      var mr2=(mx*mx+my*my)/4-mc, mr=Math.sqrt(mr2);
      return mx>0 && my>0 && mx%2===0 && my%2===0 && mr2>0 && Number.isInteger(mr) && chk.eq==='x='+mr;
    }
    if (/^geo-circle-expanded-radius-/.test(p.variant || '')) {
      var radiusEq = /equation X\^2 - ([0-9]+)X \+ Y\^2 - ([0-9]+)Y ([+-]) ([0-9]+) = 0/.exec(p.prompt || '');
      if (!radiusEq) return false;
      var aa=Number(radiusEq[1]), bb=Number(radiusEq[2]), cc=(radiusEq[3]==='-'?-1:1)*Number(radiusEq[4]);
      var radiusSq=(aa*aa+bb*bb)/4-cc;
      var derivedRadius=Math.sqrt(radiusSq);
      return aa>0 && bb>0 && aa%2===0 && bb%2===0 && radiusSq>0 && Number.isInteger(derivedRadius) && chk.eq==='x='+derivedRadius;
    }
    if (/^geo-circle-expanded-center-/.test(p.variant || '')) {
      var expanded = /equation X\^2 - ([0-9]+)X \+ Y\^2 - ([0-9]+)Y ([+-]) ([0-9]+) = 0/.exec(p.prompt || '');
      if (!expanded) return false;
      var a=Number(expanded[1]), b=Number(expanded[2]), constant=(expanded[3]==='-'?-1:1)*Number(expanded[4]);
      var radiusSquared=(a*a+b*b)/4-constant;
      return a>0 && b>0 && a%2===0 && b%2===0 && radiusSquared>0 && Number.isInteger(Math.sqrt(radiusSquared)) && chk.eq==='2*x='+expanded[1];
    }
    if (/^geo-circle-chord-distance-inverse-/.test(p.variant || '')) {
      var invChord=/circle has radius ([0-9]+) cm and a chord of length ([0-9]+) cm/.exec(p.prompt || '');
      if (!invChord) return false;
      var ri=Number(invChord[1]), ci=Number(invChord[2]), hi=ci/2, ds=ri*ri-hi*hi;
      return ri>hi && hi>0 && ci%2===0 && ds>0 && Number.isInteger(Math.sqrt(ds)) &&
        chk.eq==='x='+Math.sqrt(ds);
    }
    if (/^geo-circle-chord-distance-/.test(p.variant || '')) {
      var chordDistance = /circle has radius ([0-9]+) cm.*perpendicular distance from the center to a chord is ([0-9]+) cm/.exec(p.prompt || '');
      if (!chordDistance) return false;
      var rr = Number(chordDistance[1]), dd = Number(chordDistance[2]);
      var halfSq = rr*rr-dd*dd, half = Math.sqrt(halfSq);
      return rr > dd && dd > 0 && Number.isInteger(half) && half > 0 && chk.eq === 'x=2*'+half;
    }
    if (/^geo-circle-coordinate-radius-squared-/.test(p.variant || '')) {
      var coords = /center \((-?[0-9]+), (-?[0-9]+)\) and passes through point \((-?[0-9]+), (-?[0-9]+)\)/.exec(p.prompt || '');
      if (!coords) return false;
      var dx = Math.abs(Number(coords[3])-Number(coords[1]));
      var dy = Math.abs(Number(coords[4])-Number(coords[2]));
      return dx > 0 && dy > 0 && chk.eq === 'x='+dx+'*'+dx+'+'+dy+'*'+dy;
    }
    if (/^geo-circle-arc-length-inverse-/.test(p.variant || '')) {
      var invArc=/radius ([0-9]+) cm.*exact length ([0-9]+) times pi centimeters/.exec(p.prompt || '');
      return !!invArc && Number(invArc[1])>0 && Number(invArc[2])>0 && chk.eq==='2*'+invArc[1]+'*x=360*'+invArc[2] && 360*Number(invArc[2])<360*2*Number(invArc[1]);
    }
    if (/^geo-circle-sector-area-inverse-/.test(p.variant || '')) {
      var invSector=/radius ([0-9]+) cm.*exact area ([0-9]+) times pi square centimeters/.exec(p.prompt || '');
      return !!invSector && Number(invSector[1])>0 && Number(invSector[2])>0 && chk.eq===invSector[1]+'*'+invSector[1]+'*x=360*'+invSector[2] && Number(invSector[2])<Number(invSector[1])*Number(invSector[1]);
    }
    if (/^geo-circle-arc-length-/.test(p.variant || '')) {
      var arc = /radius ([0-9]+) cm.*central angle ([0-9]+)°.*exact arc length is x times pi centimeters/.exec(p.prompt || '');
      return !!arc && Number(arc[2]) > 0 && Number(arc[2]) <= 180 && chk.eq === '360*x=2*'+arc[1]+'*'+arc[2];
    }
    if (/^geo-circle-sector-area-/.test(p.variant || '')) {
      var sector = /radius ([0-9]+) cm.*central angle ([0-9]+)°.*exact sector area is x times pi square centimeters/.exec(p.prompt || '');
      return !!sector && Number(sector[2]) > 0 && Number(sector[2]) < 360 && chk.eq === '360*x='+sector[1]+'*'+sector[1]+'*'+sector[2];
    }
    if (/^geo-circle-intersecting-chords-expression-/.test(p.variant || '')) {
      var chordExpr=/PA measures ([0-9]+) cm, PB measures \(x\+([0-9]+)\) cm, PC measures ([0-9]+) cm, and PD measures ([0-9]+) cm/.exec(p.prompt || '');
      return !!chordExpr && Number(chordExpr[1])>0 && Number(chordExpr[2])>0 && Number(chordExpr[3])>0 && Number(chordExpr[4])>0 &&
        chk.eq===chordExpr[1]+'*(x+'+chordExpr[2]+')='+chordExpr[3]+'*'+chordExpr[4];
    }
    if (/^geo-circle-intersecting-chords-/.test(p.variant || '')) {
      var chord = /PA measures ([0-9]+) cm, PB measures x cm, PC measures ([0-9]+) cm, and PD measures ([0-9]+) cm/.exec(p.prompt || '');
      return !!chord && chk.eq === chord[1]+'*x='+chord[2]+'*'+chord[3];
    }
    if (/^geo-circle-tangent-secant-inside-/.test(p.variant || '')) {
      var tangentInside=/tangent PT has length ([0-9]+) cm.*external segment of ([0-9]+) cm and an internal segment of x cm/.exec(p.prompt || '');
      return !!tangentInside && Number(tangentInside[1])>Number(tangentInside[2]) && Number(tangentInside[2])>0 &&
        chk.eq===tangentInside[2]+'*(x+'+tangentInside[2]+')='+tangentInside[1]+'*'+tangentInside[1];
    }
    if (/^geo-circle-tangent-secant-/.test(p.variant || '')) {
      var tangentSecant = /tangent PT has length ([0-9]+) cm.*external segment of ([0-9]+) cm and a total length of x cm/.exec(p.prompt || '');
      return !!tangentSecant && chk.eq === tangentSecant[2]+'*x='+tangentSecant[1]+'*'+tangentSecant[1];
    }
    if (/^geo-circle-two-secants-inside-/.test(p.variant || '')) {
      var insideSecants=/external segment measures ([0-9]+) cm and the segment inside the circle measures x cm.*external segment measures ([0-9]+) cm and the segment inside the circle measures ([0-9]+) cm/.exec(p.prompt || '');
      return !!insideSecants && Number(insideSecants[1])>0 && Number(insideSecants[2])>0 && Number(insideSecants[3])>0 &&
        chk.eq===insideSecants[1]+'*(x+'+insideSecants[1]+')='+insideSecants[2]+'*('+insideSecants[2]+'+'+insideSecants[3]+')';
    }
    if (/^geo-circle-two-secants-/.test(p.variant || '')) {
      var secants = /external segment measures ([0-9]+) cm and the entire secant measures x cm.*external segment measures ([0-9]+) cm and the entire secant measures ([0-9]+) cm/.exec(p.prompt || '');
      return !!secants && Number(secants[3]) > Number(secants[2]) && chk.eq === secants[1]+'*x='+secants[2]+'*'+secants[3];
    }
    if (/^geo-quad-diagonal-converse-/.test(p.variant || '')) {
      var halves = /AE measures ⟨([^⟩]+)⟩ cm, EC measures ([0-9]+) cm, BE measures ([0-9]+) cm, and ED measures ([0-9]+) cm/.exec(p.prompt || '');
      return !!halves && halves[3] === halves[4] && chk.eq === halves[1]+'='+halves[2];
    }
    if (/^geo-quad-algebraic-consecutive-/.test(p.variant || '')) {
      var pair = /consecutive angle A measures ⟨([^⟩]+)⟩ degrees and angle B measures ⟨([^⟩]+)⟩ degrees/.exec(p.prompt || '');
      return !!pair && chk.eq === pair[1]+'+'+pair[2]+'=180';
    }
    if (/^geo-quad-classify-sides-/.test(p.variant || '')) {
      var sideExpressions = /adjacent side lengths ⟨([^⟩]+)⟩ cm and ⟨([^⟩]+)⟩ cm/.exec(p.prompt || '');
      return !!sideExpressions && chk.eq === sideExpressions[1]+'='+sideExpressions[2];
    }
    if (/^geo-quad-consecutive-/.test(p.variant || '')) {
      var adjacent = /angle A measures ([0-9]+)°/.exec(p.prompt || '');
      return !!adjacent && chk.eq === 'x+'+adjacent[1]+'=180';
    }
    if (/^geo-polygon-diagonals-/.test(p.variant || '')) {
      var polygon = /convex polygon has ([0-9]+) sides/.exec(p.prompt || '');
      return !!polygon && chk.eq === '2*x='+polygon[1]+'*('+polygon[1]+'-3)';
    }
    if (/^geo-quad-rect-diagonal-/.test(p.variant || '')) {
      var rect = /Diagonal AC measures ([0-9]+) cm/.exec(p.prompt || '');
      return !!rect && chk.eq === '2*x='+rect[1];
    }
    if (/^geo-quad-rhombus-diagonal-/.test(p.variant || '')) {
      var rhom = /Segment AE measures ([0-9]+) cm/.exec(p.prompt || '');
      return !!rhom && chk.eq === 'x=2*'+rhom[1];
    }
    if (/^geo-quad-trapezoid-midsegment-/.test(p.variant || '')) {
      var trap = /parallel bases measuring ([0-9]+) cm and ([0-9]+) cm/.exec(p.prompt || '');
      return !!trap && chk.eq === '2*x='+trap[1]+'+'+trap[2];
    }
    if (/^geo-vertical-/.test(p.variant || '')) return false;
    if (/^geo-transversal-/.test(p.variant || '')) {
      var b = /angle measures are ⟨([^⟩]+)⟩ degrees and ([0-9]+) degrees/.exec(p.prompt || '');
      if (!b) return false;
      var eq = /^geo-transversal-same-side-/.test(p.variant) ? b[1]+'+'+b[2]+'=180' : b[1]+'='+b[2];
      return eq === chk.eq;
    }
    if (/^geo-(complement|supplement|linear-pair)-/.test(p.variant || '')) {
      var a = /measures? (?:are )?⟨([^⟩]+)⟩ degrees and ([0-9]+) degrees/.exec(p.prompt || '');
      var total = /^geo-complement-/.test(p.variant) ? 90 : 180;
      return !!a && a[1]+'+'+a[2]+'='+total === chk.eq;
    }
    return true;
  }
  function norm(s) { return String(s).replace(/\s+/g, ''); }
  function qText(q) { return q.isInt() ? String(q.n) : (q.n < 0n ? '-' : '') + '\\frac{' + (q.n < 0n ? -q.n : q.n) + '}{' + q.d + '}'; }
  function firstMath(markup) { var s = C.snippets(markup); return s.length ? s[0] : null; }
  function valueFromAnswer(markup, v) {
    var m = firstMath(markup);
    if (m === null) { var nums = C.numbersInText(markup); if (!nums.length) throw new C.CheckError('no number in answer'); return nums[0]; }
    if (/[=<>]/.test(m)) {
      var rel = C.parseRelation(m);
      if (v && !(rel.lhs.k === 'var' && rel.lhs.v === v)) throw new C.CheckError('answer should start with ' + v + ' =');
      return C.readNumber(texOf(rel.rhs, m));
    }
    return C.readNumber(m);
  }
  function texOf(node, whole) { return whole.slice(whole.indexOf('=') + 1); }

  /* ---------- scenario checkers (word problems) ---------- */
  var WORDS = { two: 2, three: 3, four: 4, five: 5 };
  var SCEN = {
    'fee-rate': function (p) {
      var n = C.numbersInText(p.prompt); if (n.length < 3) throw new C.CheckError('expected fee, rate and total in the text');
      var x = n[2].sub(n[0]).div(n[1]); return { n: x, ok: x.isInt() && x.n > 0n };
    },
    'spend': function (p) {
      var n = C.numbersInText(p.prompt); if (n.length < 3) throw new C.CheckError('expected start, rate and remaining amount');
      var x = n[0].sub(n[2]).div(n[1]); return { n: x, ok: x.isInt() && x.n > 0n };
    },
    'two-plans': function (p) {
      var n = C.numbersInText(p.prompt); if (n.length < 4) throw new C.CheckError('expected two fees and two rates');
      var f1 = n[0], r1 = n[1], f2 = n[2], r2 = n[3];
      if (r1.eq(r2)) return { ok: false };
      var x = f2.sub(f1).div(r1.sub(r2));
      var names = []; String(C.plainText(p.prompt)).replace(/(?:^|\.\s+)([^.]*?) charges a \$/g, function (m, nm) { names.push(nm.trim()); });
      return { n: x, cost: f1.add(r1.mul(x)), ok: x.isInt() && x.n > 0n, costAt: function (k) { return [f1.add(r1.mul(k)), f2.add(r2.mul(k))]; }, names: names };
    },
    'perimeter': function (p) {
      var t = C.plainText(p.prompt), n = C.numbersInText(p.prompt);
      var m = /is\s+(\d+)\s+\S+\s+(more|less) than\s+(\d+)\s+times its width.*?perimeter is\s+(\d+)/.exec(t);
      if (!m) throw new C.CheckError('could not read the rectangle description');
      var k = new Q(m[1]), mult = new Q(m[3]), P = new Q(m[4]); if (m[2] === 'less') k = k.neg();
      var w = P.div(new Q(2)).sub(k).div(mult.add(Q.ONE)), L = mult.mul(w).add(k);
      return { w: w, L: L, P: P, ok: w.isInt() && w.n > 0n && L.n > 0n, nums: n };
    },
    'consecutive': function (p) {
      var t = C.plainText(p.prompt), m = /sum of (\w+) consecutive (even |odd )?integers is (-?\d+)/.exec(t);
      if (!m) throw new C.CheckError('could not read the consecutive-integer sentence');
      var k = WORDS[m[1]], gap = m[2] ? 2 : 1, S = new Q(m[3]);
      var first = S.sub(new Q(gap * k * (k - 1) / 2)).div(new Q(k));
      var ok = first.isInt();
      if (ok && m[2] === 'even ') ok = first.n % 2n === 0n;
      if (ok && m[2] === 'odd ') ok = first.n % 2n !== 0n;
      var list = []; for (var i = 0; i < k; i++) list.push(first.add(new Q(gap * i)));
      return { list: list, ok: ok };
    }
  };

  /* ---------- inequalities ---------- */
  function figSet(spec) {
    if (!NS.fig) throw new C.CheckError('figures module not loaded');
    var r = NS.fig.readNumberLine(NS.fig.numberLine(spec));
    return { min: r.min, max: r.max, set: r.pieces.map(function (pc) {
      return { lo: pc.lo ? new Q(pc.lo[0], pc.lo[1]) : null, loC: !!pc.loC, hi: pc.hi ? new Q(pc.hi[0], pc.hi[1]) : null, hiC: !!pc.hiC };
    }) };
  }
  function endpoints(set) { var e = []; set.forEach(function (I) { if (I.lo) e.push(I.lo); if (I.hi) e.push(I.hi); }); return e; }
  function intEnds(set) { return endpoints(set).every(function (q) { return q.isInt(); }); }
  function fitsWindow(set, fig) {
    return endpoints(set).every(function (q) { var v = Number(q.n) / Number(q.d); return v > fig.min + 0.4 && v < fig.max - 0.4; });
  }
  /* word problems with inequalities: re-solved from the printed numbers and words */
  var ISCEN = {
    'buy-max': function (t, n) { var b = n[1].div(n[0]); return { set: C.solutionSet('x\\le ' + qText(b)), best: floorQ(b), dir: 'max' }; },
    'fee-max': function (t, n) { var b = n[2].sub(n[0]).div(n[1]); return { set: C.solutionSet('x\\le ' + qText(b)), best: floorQ(b), dir: 'max' }; },
    'save-min': function (t, n) { var b = n[2].sub(n[0]).div(n[1]); return { set: C.solutionSet('x\\ge ' + qText(b)), best: ceilQ(b), dir: 'min' }; },
    'plans': function (t, n) {
      // "Plan A … $f1 … $r1 per … Plan B … $f2 … $r2 per …" — when is the FIRST plan cheaper?
      var f1 = n[0], r1 = n[1], f2 = n[2], r2 = n[3], k = f2.sub(f1).div(r1.sub(r2));
      var set = r1.sub(r2).n > 0n ? C.solutionSet('x<' + qText(k)) : C.solutionSet('x>' + qText(k));
      var best = r1.sub(r2).n > 0n ? (k.isInt() ? k.sub(Q.ONE) : floorQ(k)) : (k.isInt() ? k.add(Q.ONE) : ceilQ(k));
      return { set: set, best: best, dir: r1.sub(r2).n > 0n ? 'max' : 'min', k: k };
    },
    'range': function (t, n) { var lo = n[2].sub(n[0]).div(n[1]), hi = n[3].sub(n[0]).div(n[1]); return { set: C.solutionSet(qText(lo) + '\\le x\\le ' + qText(hi)), lo: lo, hi: hi }; },
    'average': function (t, n) {
      var m = /average of at least (\d+)/.exec(t); var target = new Q(m[1]), scores = n.slice(0, n.length - 1), sum = Q.ZERO;
      var count = new Q(scores.length + 1); scores.forEach(function (q) { sum = sum.add(q); });
      var b = target.mul(count).sub(sum);
      return { set: C.solutionSet('x\\ge ' + qText(b)), best: ceilQ(b), dir: 'min' };
    }
  };
  function floorQ(q) { var f = q.n / q.d; if (q.n < 0n && f * q.d !== q.n) f -= 1n; return new Q(f); }
  function ceilQ(q) { var f = floorQ(q); return f.eq(q) ? f : f.add(Q.ONE); }

  /* ---------- real-number classification, verbal phrases, unit conversions ---------- */
  function classifyNumber(tex) {
    var s = String(tex).replace(/\s+/g, ''), neg = s[0] === '-', b = neg ? s.slice(1) : s, m, q = null, irr = false, sq = function (n) { var r0 = Math.round(Math.sqrt(n)); return r0 * r0 === n ? r0 : null; };
    if (/^\d+$/.test(b)) q = new Q(BigInt(b));
    else if ((m = /^\\frac\{(\d+)\}\{(\d+)\}$/.exec(b))) q = new Q(BigInt(m[1]), BigInt(m[2]));
    else if (/^\d+\.\d+$/.test(b)) q = Q.parseDecimal(b);
    else if ((m = /^(\d+)\.(\d*)\\overline\{(\d+)\}$/.exec(b))) { var pre = m[2], rep = m[3], whole = BigInt(m[1] + pre + rep) - BigInt(m[1] + pre), den = BigInt('9'.repeat(rep.length) + '0'.repeat(pre.length)); q = new Q(whole, den); }
    else if ((m = /^\\sqrt\{(\d+)\}$/.exec(b))) { var r1 = sq(+m[1]); if (r1 === null) irr = true; else q = new Q(BigInt(r1)); }
    else if ((m = /^\\sqrt\{\\frac\{(\d+)\}\{(\d+)\}\}$/.exec(b))) { var f = new Q(BigInt(m[1]), BigInt(m[2])), rn = sq(Number(f.n)), rd = sq(Number(f.d)); if (rn === null || rd === null) irr = true; else q = new Q(BigInt(rn), BigInt(rd)); }
    else if (/^(\d*)\\pi$|^\\frac\{\\pi\}\{\d+\}$/.test(b)) irr = true;
    else throw new C.CheckError('cannot classify ' + tex);
    if (irr) return ['irrational', 'real'];
    if (neg) q = q.neg();
    var out = [];
    if (q.isInt()) { if (q.n > 0n) out.push('natural'); if (q.n >= 0n) out.push('whole'); out.push('integer'); }
    return out.concat(['rational', 'real']);
  }
  function setNamesIn(text) {
    var t = C.plainText(text).toLowerCase(), out = [];
    if (/\bnatural/.test(t)) out.push('natural'); if (/\bwhole/.test(t)) out.push('whole'); if (/\bintegers?\b/.test(t)) out.push('integer');
    if (/(^|[^r])\brational/.test(t)) out.push('rational'); if (/irrational/.test(t)) out.push('irrational'); if (/\breal/.test(t)) out.push('real');
    return out;
  }
  /* English phrase → every TeX reading of it (a small grammar; the verifier keeps only phrases with one meaning) */
  var NUMW = { twice: 2, 'three times': 3, 'four times': 4, 'five times': 5, 'six times': 6 };
  function readPhrase(s) {
    s = s.trim().replace(/\.$/, '').replace(/^the\s+/i, function (w) { return w.toLowerCase(); }); var out = [], m, i;
    var splits = function (str, sep, fn) { var at = -1; while ((at = str.indexOf(sep, at + 1)) >= 0) { var A = readPhrase(str.slice(0, at)), B = readPhrase(str.slice(at + sep.length)); A.forEach(function (a) { B.forEach(function (b) { out.push(fn(a, b)); }); }); } };
    if ((m = /^a number ([a-z])$/i.exec(s)) || (m = /^([a-z])$/.exec(s))) return [m[1]];
    if (/^\d+$/.test(s)) return [s];
    if ((m = /^the sum of (.+)$/i.exec(s))) splits(m[1], ' and ', function (a, b) { return '(' + a + ')+(' + b + ')'; });
    if ((m = /^the difference of (.+)$/i.exec(s))) splits(m[1], ' and ', function (a, b) { return '(' + a + ')-(' + b + ')'; });
    if ((m = /^the product of (.+)$/i.exec(s))) splits(m[1], ' and ', function (a, b) { return '(' + a + ')(' + b + ')'; });
    if ((m = /^the quotient of (.+)$/i.exec(s))) splits(m[1], ' and ', function (a, b) { return '\\frac{' + a + '}{' + b + '}'; });
    if ((m = /^the square of (.+)$/i.exec(s))) readPhrase(m[1]).forEach(function (a) { out.push('(' + a + ')^2'); });
    for (var w in NUMW) if (s.toLowerCase().indexOf(w + ' ') === 0) readPhrase(s.slice(w.length + 1)).forEach(function (a) { out.push(NUMW[w] + '(' + a + ')'); });
    if ((m = /^(\d+) times (.+)$/i.exec(s))) readPhrase(m[2]).forEach(function (a) { out.push(m[1] + '(' + a + ')'); });
    splits(s, ' more than ', function (a, b) { return '(' + b + ')+(' + a + ')'; });
    splits(s, ' less than ', function (a, b) { return '(' + b + ')-(' + a + ')'; });
    [[', increased by ', '+'], [' increased by ', '+'], [', decreased by ', '-'], [' decreased by ', '-']].forEach(function (op) { splits(s, op[0], function (a, b) { return '(' + a + ')' + op[1] + '(' + b + ')'; }); });
    for (i = out.length - 1; i >= 0; i--) if (out.indexOf(out[i]) !== i) out.splice(i, 1);
    return out;
  }
  function phraseMeaning(s) {
    var c = readPhrase(s); if (!c.length) throw new C.CheckError('cannot read the phrase'); 
    for (var i = 1; i < c.length; i++) if (!C.equivalent(c[0], c[i])) throw new C.CheckError('the phrase has two meanings');
    return c[0];
  }
  var UNITF = { inches: ['L', 1], feet: ['L', 12], yards: ['L', 36], miles: ['L', 63360], centimeters: ['M', 1], meters: ['M', 100], kilometers: ['M', 100000],
    seconds: ['T', 1], minutes: ['T', 60], hours: ['T', 3600], cups: ['V', 1], pints: ['V', 2], quarts: ['V', 4], gallons: ['V', 16], ounces: ['W', 1], pounds: ['W', 16], grams: ['G', 1], kilograms: ['G', 1000] };
  function unitFactor(a, b) { var sq = /^square /.test(a), A = UNITF[a.replace(/^square /, '')], B = UNITF[b.replace(/^square /, '')]; if (!A || !B || A[0] !== B[0] || sq !== /^square /.test(b)) throw new C.CheckError('cannot convert ' + a + ' to ' + b); var f = A[1] / B[1]; return sq ? f * f : f; }
  function checkUnits(p, part) {
    var txt = C.plainText(p.prompt).replace(/\s+/g, ' '), ans = part.answer || '', got = C.numbersInText(ans), m, val, unit, k = null;
    if ((m = /^Convert (\d+(?:\.\d+)?) ((?:square )?[a-z]+) to ((?:square )?[a-z]+)\.$/.exec(txt))) { val = +m[1] * unitFactor(m[2], m[3]); unit = m[3]; }
    else if ((m = /works at (\d+) ([a-z]+) per hour\. Convert this rate to \2 per minute\./.exec(txt))) { val = +m[1] / 60; unit = m[2] + ' per minute'; }
    else if ((m = /^Convert (\d+) ([a-z]+) per hour to ([a-z]+) per second\. Round to the nearest tenth\.$/.exec(txt))) { val = +m[1] * unitFactor(m[2], m[3]) / 3600; unit = m[3] + ' per second'; k = 1; }
    else throw new C.CheckError('cannot read the conversion');
    if (!got.length) return { status: 'mismatch', msg: 'No number in the answer.' };
    var want = k === null ? val : Math.round(val * 10) / 10, g = Number(got[0].n) / Number(got[0].d);
    if (k === null && Math.abs(val - Math.round(val * 1e6) / 1e6) > 1e-9) return { status: 'invalid', msg: 'The answer is not exact; the problem must say how to round.' };
    if (Math.abs(g - want) > 1e-9) return { status: 'mismatch', msg: 'Correct: ' + want + ' ' + unit + '.' };
    return C.plainText(ans).toLowerCase().indexOf(unit) >= 0 ? { status: 'verified', computed: want + ' ' + unit } : { status: 'mismatch', msg: 'Give the unit: ' + unit + '.' };
  }
  function checkNumClass(p, part) {
    var chk = part.check, ans = part.answer || '';
    if (chk.num) { if (!shown(p, chk.num)) return { status: 'invalid', msg: 'The number is not printed.' }; var want = classifyNumber(chk.num), got = setNamesIn(ans);
      return want.length === got.length && want.every(function (w) { return got.indexOf(w) >= 0; }) ? { status: 'verified', computed: want.join(', ') } : { status: 'mismatch', msg: 'Correct: ' + want.join(', ') + '.' }; }
    if (!chk.list.every(function (t) { return shown(p, t); })) return { status: 'invalid', msg: 'The numbers are not printed.' };
    var yes = chk.list.filter(function (t) { var s = classifyNumber(t); return chk.want === 'rational-not-integer' ? s.indexOf('rational') >= 0 && s.indexOf('integer') < 0 : s.indexOf(chk.want) >= 0; });
    var said = C.snippets(ans).map(norm), yesN = yes.map(norm);
    return said.length === yesN.length && yesN.every(function (y) { return said.indexOf(y) >= 0; }) ? { status: 'verified', computed: yes.join(', ') } : { status: 'mismatch', msg: 'Correct: ' + yes.join(', ') + '.' };
  }
  /* ---------- transformations of linear functions ---------- */
  function lineMB(src) { var R = C.parseRelation(src), at = function (x) { return C.evalNode(R.rhs, { x: new Q(BigInt(x)) }); }; var b = at(0); return { m: at(1).sub(b), b: b }; }
  function checkLinTransform(p, part) {
    var chk = part.check, ans = part.answer || '', txt = C.plainText(ans).toLowerCase(), pr = C.plainText(p.prompt);
    if (!shown(p, chk.f)) return { status: 'invalid', msg: 'f is not printed.' };
    var F1 = lineMB(chk.f), sgn = function (q) { return C.cmpQ(q, Q.ZERO); }, absQ = function (q) { return sgn(q) < 0 ? q.neg() : q; };
    var eqAns = function (want) { var s = C.snippets(ans)[0]; if (!s) return { status: 'mismatch', msg: 'No equation.' }; var G; try { G = lineMB(s); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equation.' }; }
      if (!/^\s*(g\(x\)|y)\s*=/.test(s)) return { status: 'mismatch', msg: 'Write g(x) = mx + b.' };
      return G.m.eq(want.m) && G.b.eq(want.b) ? { status: 'verified' } : { status: 'mismatch', msg: 'g(x) = ' + qText(want.m) + 'x + ' + qText(want.b) + '.' }; };
    if (chk.want === 'describe') {
      if (!shown(p, chk.g)) return { status: 'invalid', msg: 'g is not printed.' };
      var G2 = lineMB(chk.g), refl = sgn(F1.m) * sgn(G2.m) < 0, c1 = C.cmpQ(absQ(G2.m), absQ(F1.m)), db = G2.b.sub(/x-axis/.test(txt) ? F1.b.neg() : F1.b);   // across the x-axis the intercept flips too
      var saidRefl = /reflect/.test(txt), saidSteep = /less steep/.test(txt) ? -1 : /steeper/.test(txt) ? 1 : 0;
      var sh = /(\d+) units? (up|down)/.exec(txt), saidShift = sh ? new Q(BigInt(sh[1])).mul(new Q(sh[2] === 'up' ? 1n : -1n)) : Q.ZERO;
      return saidRefl === refl && saidSteep === c1 && saidShift.eq(db) ? { status: 'verified' } : { status: 'mismatch', msg: (refl ? 'reflected; ' : '') + (c1 ? (c1 > 0 ? 'steeper; ' : 'less steep; ') : '') + 'vertical shift ' + qText(db) + '.' };
    }
    if (chk.want === 'shift-eq') { var mS = /is shifted (\d+) units? (up|down) to make/.exec(pr); if (!mS) throw new C.CheckError('cannot read the shift'); var d = new Q(BigInt(mS[1])).mul(new Q(mS[2] === 'up' ? 1n : -1n)); return eqAns({ m: F1.m, b: F1.b.add(d) }); }
    if (!shown(p, chk.rel)) return { status: 'invalid', msg: 'g is not printed.' };
    var mh = /^g\(x\)=f\(x([+-])(\d+)\)$/.exec(chk.rel.replace(/\s/g, '')); if (!mh) throw new C.CheckError('cannot read g'); var h = new Q(BigInt(mh[2])).mul(new Q(mh[1] === '-' ? 1n : -1n));
    if (chk.want === 'h-eq') return eqAns({ m: F1.m, b: F1.b.sub(F1.m.mul(h)) });
    var hw = /(\d+) units? (right|left)/.exec(txt); if (!hw) return { status: 'mismatch', msg: 'Say how many units and which way.' };
    return new Q(BigInt(hw[1])).mul(new Q(hw[2] === 'right' ? 1n : -1n)).eq(h) && !/\b(up|down)\b/.test(txt) ? { status: 'verified' } : { status: 'mismatch', msg: 'Shifted ' + qText(absQ(h)) + (sgn(h) > 0 ? ' right.' : ' left.') };
  }
  function checkPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '';
    if (!chk || chk.type === 'none') return { status: 'manual', msg: 'No automatic check for this answer.' };
    var t = chk.type;
    if (t === 'geo-proof-reason') {
      var words = C.plainText(p.prompt || '');
      var shared = /Triangles ABC and ABD share side AB/.test(words);
      var vertical = /Lines AC and BD intersect at O/.test(words);
      if (shared === vertical) return {status:'invalid',msg:'Unrecognized or ambiguous proof givens.'};
      var figOk = false;
      if (p.fig && p.fig.kind === 'geo-cong' && NS.geoFigures && NS.geoFigures.cong) figOk = NS.geoFigures.check(p.fig).ok && NS.geoFigures.cong.proofKind(p.fig) === (shared ? 'shared' : 'vertical');
      else figOk = !!(p.fig && p.fig.kind === 'geo-proof' && p.fig.case === (shared ? 'shared' : 'vertical') && NS.geoDiagram && NS.geoDiagram.validate(p.fig));
      if (!figOk) return {status:'invalid',msg:'Proof diagram conflicts with the printed givens.'};
      // The print renderer uses proofStatements instead of repeating the prompt.
      // Check that the displayed scaffold has not drifted from the givens.
      if (Array.isArray(p.proofStatements)) {
        var expectedStatements = shared ?
          ['AB is congruent to AB','triangle ABC is congruent to triangle ABD','Angle ACB is congruent to angle ADB'] :
          ['angle AOB is congruent to angle COD','triangle AOB is congruent to triangle COD','Angle OAB is congruent to angle OCD'];
        var proofVisible = /angle [A-Z]{3} = ⟨([^⟩]+)⟩ degrees and angle [A-Z]{3} = (\d+) degrees/.exec(p.prompt || '');
        var proofEq = proofVisible && proofVisible[1]+'='+proofVisible[2];
        if (p.proofStatements.length !== 4 || !proofEq ||
            expectedStatements.some(function(st,i){return p.proofStatements[i].toLowerCase() !== st.toLowerCase();}) ||
            p.proofStatements[3] !== 'Solve ⟨'+proofEq+'⟩ for x') {
          return {status:'invalid',msg:'Printed proof statements conflict with the givens or equation.'};
        }
      }
      var stage = chk.stage, expected;
      if (stage === 'first') expected = shared ? 'REFLEXIVE PROPERTY' : 'VERTICAL ANGLES THEOREM';
      else if (stage === 'congruence') expected = shared ? 'SSS' : 'SAS';
      else if (stage === 'consequence') expected = 'CPCTC';
      else return {status:'invalid',msg:'Unknown proof step.'};
      return String(ans).trim().toUpperCase() === expected
        ? {status:'verified',comp:expected}
        : {status:'mismatch',msg:'Proof reason does not follow from the printed givens.'};
    }
    if (t === 'geo-congruence-criterion') {
      var kinds = ['sss','sas','asa','aas','hl','ssa','aaa'];
      var kind = p.fig && p.fig.kind === 'geo-triangle-pair' && p.fig.criterion;
      if (p.fig && p.fig.kind === 'geo-cong' && NS.geoFigures && NS.geoFigures.cong) { var dvc = NS.geoFigures.cong.derive(p.fig); kind = dvc === 'NONE' ? null : dvc.toLowerCase(); }
      if (kinds.indexOf(kind) < 0 || !NS.geoDiagram || !NS.geoDiagram.validate(p.fig))
        return {status:'invalid',msg:'Missing or invalid triangle markings.'};
      if (!/Identify the criterion/.test(C.plainText(p.prompt || '')))
        return {status:'invalid',msg:'Student question does not refer to the diagram.'};
      var expected = (kind === 'ssa' || kind === 'aaa') ? 'NOT SUFFICIENT' : kind.toUpperCase();
      return String(ans).trim().toUpperCase() === expected
        ? {status:'verified',comp:expected}
        : {status:'mismatch',msg:'Congruence classification does not match the marked sides and angles.'};
    }
    if (t === 'geo-special-radical') {
      // Read the given side from the student prompt; do not trust generator metadata.
      var raw=C.plainText(p.prompt||'');
      var m=/A (45|30)°-(?:45°-90°|60°-90°) triangle has (?:a leg|a short leg|a long leg) of length (\d+) units/.exec(raw);
      if(!m) return {status:'invalid',msg:'Missing printed special-triangle measurements.'};
      var n=+m[2],degree=+m[1],radicand=degree===45?2:3;
      if(!(n>0 && Number.isSafeInteger(n)))return {status:'invalid',msg:'Invalid special-triangle side.'};
      var expected='x='+n+'\\sqrt{'+radicand+'}';
      var actual=firstMath(ans);
      return norm(actual)===norm(expected)?{status:'verified',computed:expected}
        :{status:'mismatch',msg:'Incorrect exact radical length.',computed:expected};
    }
    if (t === 'geo-inverse-trig') {
      // Recover the ratio and trig function from student-visible text.
      var raw = C.plainText(p.prompt || '');
      var m = /Find the acute angle x in degrees if (sin|cos|tan) x = (\d+)\/(\d+)\./.exec(raw);
      if (!m) return {status:'invalid',msg:'Missing printed inverse-trig ratio.'};
      var numerator=+m[2],denominator=+m[3];
      if (!(numerator>0 && denominator>0)) return {status:'invalid',msg:'Invalid trig ratio.'};
      var ratio=numerator/denominator,rad;
      if(m[1]==='sin')rad=Math.asin(ratio);
      else if(m[1]==='cos')rad=Math.acos(ratio);
      else rad=Math.atan(ratio);
      var degrees=rad*180/Math.PI,nearest=Math.round(degrees);
      if(chk.roundTo===1){
        if(!/nearest tenth of a degree/.test(raw))
          return {status:'invalid',msg:'Missing student-facing rounding instruction.'};
        if(!Number.isFinite(degrees)||degrees<=0||degrees>=90)
          return {status:'invalid',msg:'Expected an acute inverse-trig angle.'};
        var rounded=Math.round(degrees*10)/10;
        var roundedAnswer=valueFromAnswer(ans,'x');
        var expected=C.readNumber(rounded.toFixed(1));
        return roundedAnswer.eq(expected)?{status:'verified',computed:'x='+rounded.toFixed(1)}
          :{status:'mismatch',msg:'Incorrect rounded inverse-trig angle.',computed:'x='+rounded.toFixed(1)};
      }
      if(!Number.isFinite(degrees)||nearest<=0||nearest>=90||
         Math.abs(degrees-nearest)>1e-9)
        return {status:'invalid',msg:'Expected an exact integer acute angle.'};
      var got=valueFromAnswer(ans,'x');
      return got.eq(new Q(nearest))?{status:'verified',computed:'x='+nearest}
        :{status:'mismatch',msg:'Incorrect inverse-trig angle.',computed:'x='+nearest};
    }
    if (t === 'geo-pythagorean') {
      // Derive the length independently from the student-facing dimensions.
      // Never use a generator-provided answer or a quadratic linear-solver.
      var raw = C.plainText(p.prompt || ''), m, squared, expectedEq;
      if (chk.kind === 'hyp') {
        m = /right triangle has legs (\d+) and (\d+) units/.exec(raw);
        if (!m) return {status:'invalid',msg:'Missing printed leg lengths.'};
        squared = (+m[1])**2 + (+m[2])**2;
        expectedEq = 'x^2='+m[1]+'^2+'+m[2]+'^2';
      } else if (chk.kind === 'leg') {
        m = /hypotenuse (\d+) units and one leg (\d+) units/.exec(raw);
        if (!m) return {status:'invalid',msg:'Missing printed hypotenuse and leg.'};
        squared = (+m[1])**2 - (+m[2])**2;
        expectedEq = m[2]+'^2+x^2='+m[1]+'^2';
      } else if (chk.kind === 'distance') {
        m = /Points A\(0, 0\) and B\((\d+), (\d+)\)/.exec(raw);
        if (!m) return {status:'invalid',msg:'Missing printed coordinates.'};
        squared = (+m[1])**2 + (+m[2])**2;
        expectedEq = 'x^2='+m[1]+'^2+'+m[2]+'^2';
      } else return {status:'invalid',msg:'Unknown Pythagorean problem type.'};
      // Independently validate the hidden equation against the printed givens,
      // without showing the completed equation to students.
      if (chk.eq !== expectedEq) return {status:'invalid',msg:'Pythagorean check disagrees with printed dimensions.'};
      var length = Math.sqrt(squared);
      if (!(squared > 0) || !Number.isSafeInteger(squared) || !Number.isSafeInteger(length))
        return {status:'invalid',msg:'Expected an exact positive integer length.'};
      var got = valueFromAnswer(ans,'x');
      return got.eq(new Q(length)) ? {status:'verified',computed:'x='+length}
        : {status:'mismatch',msg:'Correct length is '+length+'.',computed:'x='+length};
    }
    if(t === 'mcas-context') {
      // Independent from the scenario generator: recover numerical inputs
      // exclusively from the STUDENT'S printed scenario, not check metadata.
      var raw = C.plainText(p.prompt || ''), nums = (raw.match(/-?\d+(?:\.\d+)?/g) || []).map(Number);
      var expected, unit = chk.unit, a = nums[0], b = nums[1], d = nums[2], e = nums[3];
      if (!Number.isInteger(chk.index) || chk.index < 0 || chk.index > 3)
        return {status:'invalid',msg:'Invalid scenario part.'};
      if (chk.variant === 'reasoning') {
        if(unit==='algebra1-foundations' && nums.length===3)
          expected=[a*b,a*d,a*(b-d),a*(b-2*d)];
        else if(unit==='algebra1-expressions-equations' && nums.length===3 && b>0 && (d-a)%b===0)
          expected=[d-a,(d-a)/b,b,d+b];
        else if(unit==='algebra1-inequalities' && nums.length===3 && d>0) {
          var free=a-b;
          expected=[free,Math.floor(free/d),free%d,free%d>=d?1:0];
        }
        else if(unit==='algebra1-systems-of-equations' && nums.length===4 && d!==e){
          var nAdult=(b-e*a)/(d-e),nStudent=a-nAdult;
          if(Number.isInteger(nAdult)&&Number.isInteger(nStudent)&&nAdult>=0&&nStudent>=0)
            expected=[nAdult,nStudent,nAdult*d,nStudent*e];
        }
        else if(unit==='algebra1-exponents-scientific-notation' && nums.length===3 && b>=0 && b<=8)
          expected=[a*10**b,a*10**b*d,2*a*10**b,a*10**b];
        else if(unit==='algebra1-polynomials' && nums.length===3)
          expected=[a+b,a*b,(d+a)*(d+b),4*d+2*a+2*b];
        else if(unit==='algebra1-factoring-zero-product' && nums.length===2){
          var delta=a*a-4*b,rt=Math.sqrt(delta);
          if(Number.isInteger(rt))expected=[(a-rt)/2,(a+rt)/2,a,rt];
        }
        else if(unit==='algebra1-quadratics' && nums.length===2)
          expected=[Math.abs(a),b,b-1,4];
      } else       if (chk.variant === 'applied') {
        if (unit === 'algebra1-foundations' && nums.length===3)
          expected=[a*b,(a-d)*b,d*b];
        else if (unit === 'algebra1-expressions-equations' && nums.length===3)
          expected=[a*b,a*b+d,a*(b+1)+d];
        else if (unit === 'algebra1-inequalities' && nums.length===3 && d>0) {
          var remaining=a-b;
          expected=[remaining,Math.floor(remaining/d),remaining%d];
        }
        else if (unit === 'algebra1-systems-of-equations' && nums.length===4 && d!==e) {
          var adultCount=(b-a*e)/(d-e),kidCount=a-adultCount;
          if (Number.isInteger(adultCount)&&Number.isInteger(kidCount)&&adultCount>=0&&kidCount>=0)
            expected=[adultCount,kidCount,kidCount*e];
        }
        else if (unit === 'algebra1-exponents-scientific-notation' && nums.length===3 && b>=0 && b<=9)
          expected=[a*Math.pow(10,b),a*Math.pow(10,b)*d,a*Math.pow(10,b)];
        else if (unit === 'algebra1-polynomials' && nums.length===3)
          expected=[a+b,a*b,(d+a)*(d+b)];
        else if (unit === 'algebra1-factoring-zero-product' && nums.length===2) {
          var discr=a*a-4*b,sqrt=Math.sqrt(discr);
          if (Number.isInteger(sqrt)) expected=[(a-sqrt)/2,(a+sqrt)/2,sqrt];
        }
        else if (unit === 'algebra1-quadratics' && nums.length===2)
          expected=[Math.abs(a),b,b-1];
      } else       if (chk.variant === 'interpret') {
        if (unit==='algebra1-relations-functions' && nums.length===7 && nums[0]===0 && nums[2]===1 && nums[4]===2) {
          var m=nums[3]-nums[1];
          if(nums[5]===nums[1]+2*m) expected=[m,nums[1]+m*nums[6],nums[1]+m*(nums[6]+1)];
        } else if(unit==='algebra1-linear-equations-slope' && nums.length===7 && nums[0]===0 && nums[2]===1 && nums[4]===2) {
          var sl=nums[3]-nums[1];
          if(nums[5]===nums[1]+2*sl) expected=[sl,nums[1]+sl*nums[6],2*sl];
        } else if(unit==='algebra1-exponential-functions' && nums.length===7 && nums[0]===0 && nums[2]===1 && nums[4]===2 && nums[1]!==0) {
          var ratio=nums[3]/nums[1];
          if(nums[5]===nums[3]*ratio) expected=[ratio,nums[1]*Math.pow(ratio,nums[6]),nums[1]*Math.pow(ratio,nums[6])*(ratio-1)];
        } else if(unit==='algebra1-statistics-data-modeling' && nums.length===5) {
          var a5=nums.slice().sort(function(x,y){return x-y;});
          expected=[a5[2],(a5[3]+a5[4]-a5[0]-a5[1])/2,a5.reduce(function(x,y){return x+y;},0)/5];
        }
      } else       if (chk.variant === 'extension') {
        if (unit === 'algebra1-foundations' && nums.length===3) expected=[a*b,a*b*d,(a+1)*b*d];
        else if (unit === 'algebra1-expressions-equations' && nums.length===3 && a>0 && (d-b)%a===0)
          expected=[d-b,(d-b)/a,d+(d-b)/a];
        else if (unit === 'algebra1-inequalities' && nums.length===3 && d>0) {
          var allowance=a-b, count=Math.floor(allowance/d);
          expected=[allowance,count,allowance-(count-1)*d];
        }
        else if (unit === 'algebra1-relations-functions' && nums.length===3)
          expected=[a+b*d,a+b*(d+2),2*b];
        else if (unit === 'algebra1-linear-equations-slope' && nums.length===3)
          expected=[a+b*d,b,a+b*(d+1)];
        else if (unit === 'algebra1-systems-of-equations' && nums.length===4 && e!==d) {
          var large=(b-a*d)/(e-d),small=a-large;
          if (Number.isInteger(large)&&Number.isInteger(small)&&large>=0&&small>=0)
            expected=[small,large,large*e];
        }
        else if (unit === 'algebra1-exponents-scientific-notation' && nums.length===3 && b>=0&&b<=8)
          expected=[a*Math.pow(10,b),a*Math.pow(10,b)*d,a*Math.pow(10,b)*(d-1)];
        else if (unit === 'algebra1-exponential-functions' && nums.length===2 && b>=0&&b<=10)
          expected=[a*Math.pow(3,b),a*Math.pow(3,b+1),3];
        else if (unit === 'algebra1-polynomials' && nums.length===3)
          expected=[(d+a)*(d+b),a+b,a*b];
        else if (unit === 'algebra1-factoring-zero-product' && nums.length===2) {
          var disc=a*a-4*b,root=Math.sqrt(disc);
          if (Number.isInteger(root)) expected=[(a-root)/2,(a+root)/2,a];
        }
        else if (unit === 'algebra1-quadratics' && nums.length===2)
          expected=[Math.abs(a),b,1];
        else if (unit === 'algebra1-statistics-data-modeling' && nums.length===5) {
          var sorted=nums.slice().sort(function(x,y){return x-y;});
          expected=[sorted[2],sorted[4]-sorted[0],sorted.reduce(function(x,y){return x+y;},0)/5];
        }
      } else       if (unit === 'algebra1-foundations' && nums.length === 3) expected=[a*b,a*b+d,2*(a*b+d)];
      else if (unit === 'algebra1-expressions-equations' && nums.length === 3 && b>0 && (d-a)%b===0)
        expected=[d-a,(d-a)/b,d+b];
      else if (unit === 'algebra1-inequalities' && nums.length === 3 && b>0)
        expected=[d-a,Math.ceil((d-a)/b),a+b*(Math.ceil((d-a)/b)-1)];
      else if (unit === 'algebra1-relations-functions' && nums.length === 3)
        expected=[a+b*d,a+b*(d+1),b];
      else if (unit === 'algebra1-linear-equations-slope' && nums.length === 3 && b>0)
        expected=[a-b*d,-b,a/b];
      else if (unit === 'algebra1-systems-of-equations' && nums.length === 4 && d!==e)
        { var adults=(b-e*a)/(d-e), students=a-adults; if(Number.isInteger(adults)&&Number.isInteger(students)&&adults>=0&&students>=0) expected=[adults,students,adults*d]; }
      else if (unit === 'algebra1-exponents-scientific-notation' && nums.length === 3 && b>=0 && b<=9)
        expected=[a*Math.pow(10,b),a*Math.pow(10,b)*d,b];
      else if (unit === 'algebra1-exponential-functions' && nums.length === 2 && b>=0 && b<=12)
        expected=[a*Math.pow(2,b),a*Math.pow(2,b+1),a*Math.pow(2,b)];
      else if (unit === 'algebra1-polynomials' && nums.length === 3)
        expected=[(d+a)*(d+b),a+b,a*b];
      else if (unit === 'algebra1-factoring-zero-product' && nums.length === 2) {
        var discriminant=a*a-4*b, sq=Math.sqrt(discriminant);
        if(Number.isInteger(sq)) expected=[(-a-sq)/2,(-a+sq)/2,b];
      } else if (unit === 'algebra1-quadratics' && nums.length === 1 && a>0)
        expected=[a,a/2,a*a/4];
      else if (unit === 'algebra1-statistics-data-modeling' && nums.length === 5)
        { var z=nums.slice().sort(function(x,y){return x-y;});expected=[z.reduce(function(x,y){return x+y;},0)/5,z[2],z[4]-z[0]]; }
      if(expected && expected.length===3) expected.push(2*expected[0]);
      if(!expected || expected.some(function(v){return !Number.isFinite(v);}))
        return {status:'invalid',msg:'Scenario inputs could not be independently verified.'};
      var given=String(C.plainText(ans)).trim().replace(/,/g,'');
      if(!/^-?\d+(?:\.\d+)?$/.test(given)) return {status:'mismatch',msg:'The answer should be a single numeric value.'};
      return Math.abs(Number(given)-expected[chk.index]) < 1e-9 ?
        {status:'verified',computed:String(expected[chk.index])} :
        {status:'mismatch',msg:'Recalculate this part using the scenario values.'};
    }
    if(t==='exp-graph-points'){
      var a=Number(chk.a),n=Number(chk.n),d=Number(chk.d),k=Number(chk.k);
      if(!Number.isInteger(k)||k<-6||k>5)return {status:'invalid',msg:'Invalid vertical shift.'};
      if(!Number.isInteger(a)||!Number.isInteger(n)||!Number.isInteger(d)||a<=0||n<=0||d<=0||n===d)return {status:'invalid',msg:'Invalid exponential graph parameters.'};
      if(p.prompt.indexOf(chk.eq)<0||!/Graph/.test(p.prompt))return {status:'invalid',msg:'Graph equation does not match the printed problem.'};
      if(a*d%n!==0||a*n%d!==0||[a*d/n+k,a+k,a*n/d+k].some(v=>Math.abs(v)>9))return {status:'invalid',msg:'The expected plot coordinates are not in the grid.'};
      return String(ans).replace(/[⟨⟩]/g,'').trim()===String(a+k)?{status:'verified'}:{status:'mismatch',msg:'The y-intercept must equal the initial value.'};
    }
    if(t === 'discrete-continuous'){
      var scenarios={
        'A student buys individual notebooks. The input is the number of notebooks purchased.':1,
        'The height of a plant is measured over elapsed time. The input is elapsed time in hours.':2,
        'Tickets sold for a school game are counted. The input is the number of tickets.':1,
        'Water flows into a tank. The input is the number of minutes elapsed.':2,
        'A classroom counts the number of students present. The input is the number of students.':1,
        'A cyclist travels along a trail. The input is the distance ridden in miles.':2,
        'A store charges per individual bag of apples. The input is the number of bags.':1,
        'A bathtub drains steadily. The input is the volume of water remaining in gallons.':2
      };
      var want=scenarios[chk.scenario];
      if(!want||p.prompt.indexOf(chk.scenario)<0||!Number.isInteger(chk.sample)||chk.sample<2||chk.sample>999||!['During the morning','During the afternoon','Yesterday','Last week'].includes(chk.subject)||p.prompt.indexOf(chk.subject+', a sample recorded input was '+chk.sample+'.')<0)return {status:'invalid',msg:'Unknown or unprinted context.'};
      return String(ans).trim()===String(want)?{status:'verified'}:{status:'mismatch',msg:'This context has a different domain type.'};
    }
    if (t === 'ineq' || t === 'read-graph' || t === 'ineq-members' || t === 'error-line' || t === 'iscenario' || t === 'model-ineq') return checkIneqPart(p, part, policy);
    if (FUNC_TYPES.indexOf(t) >= 0) return checkFuncPart(p, part, policy);
    if (t === 'compound') return checkCompound(p, part);
    if (EXP_TYPES.indexOf(t) >= 0) return checkExpPart(p, part, policy);
    if (FACT_TYPES.indexOf(t) >= 0) return checkFactorPart(p, part, policy);
    if (STAT_TYPES.indexOf(t) >= 0) return checkStatPart(p, part, policy);
    if (LINE_TYPES.indexOf(t) >= 0) return checkLinePart(p, part, policy);
    if (SYS_TYPES.indexOf(t) >= 0) return checkSysPart(p, part, policy);
    if (POW_TYPES.indexOf(t) >= 0) return checkPowPart(p, part, policy);
    if (POLY_TYPES.indexOf(t) >= 0) return checkPolyPart(p, part, policy);
    if (QUAD_TYPES.indexOf(t) >= 0) return checkQuadPart(p, part, policy);
    if ((t === 'solve' || t === 'classify' || t === 'literal' || t === 'literal-eval') && !shown(p, chk.eq) && !geometryDerived(p, chk)) return { status: 'invalid', msg: 'The equation being checked is not the one printed for students.' };
    if ((t === 'simplify' || t === 'evaluate') && !shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression being checked is not the one printed for students.' };

    if (t === 'num-class') return checkNumClass(p, part);
    if (t === 'lin-transform') return checkLinTransform(p, part);
    if (t === 'units') return checkUnits(p, part);
    if (t === 'verbal-expr') {
      var mv = /Write an algebraic expression for “([^”]+)”\./.exec(C.plainText(p.prompt)); if (!mv) throw new C.CheckError('no phrase');
      var meaning = phraseMeaning(mv[1]), av = firstMath(ans); if (av === null) return { status: 'mismatch', msg: 'No expression.' };
      var eqv; try { eqv = C.equivalent(meaning, av); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
      return eqv ? { status: 'verified', computed: meaning } : { status: 'mismatch', msg: 'The phrase means ' + meaning + '.' };
    }
    if (t === 'verbal-words') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' };
      var mw; try { mw = phraseMeaning(C.plainText(ans)); } catch (e) { return { status: 'mismatch', msg: 'The words do not read as one expression: ' + e.message + '.' }; }
      return C.equivalent(mw, chk.expr) ? { status: 'verified' } : { status: 'mismatch', msg: 'Those words mean ' + mw + '.' };
    }
    if (t === 'expr-error-line') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The original expression is not printed.' };
      var firstE = 0;
      chk.lines.forEach(function (ln, i) { if (!shown(p, ln)) throw new C.CheckError('work line not printed: ' + ln); if (!firstE && !C.equivalent(chk.expr, ln)) firstE = i + 1; });
      if (!firstE) return { status: 'invalid', msg: 'The shown work has no mistake.' };
      var mE = /line\s*(\d+)/i.exec(C.plainText(ans));
      return mE && +mE[1] === firstE ? { status: 'verified', computed: 'Line ' + firstE } : { status: 'mismatch', msg: 'The first wrong line is line ' + firstE + '.', computed: 'Line ' + firstE };
    }
    if (t === 'percent') {
      var pt = C.plainText(p.prompt).replace(/\s+/g, ' '), NUM = '(\\d+(?:\\.\\d+)?)', rd = function (x) { return Q.parseDecimal(x); }, hund = new Q(100n);
      var pc = function (x) { return rd(x).div(hund); }, mt, target, word = null;
      var R = function (re) { var m0 = new RegExp(re).exec(pt); if (!m0) throw new C.CheckError('could not read the percent problem'); return m0; };
      switch (chk.scenario) {
        case 'of': mt = R('What is ' + NUM + '% of ' + NUM + '\\?'); target = pc(mt[1]).mul(rd(mt[2])); break;
        case 'what-pct': mt = R(NUM + ' is what percent of ' + NUM + '\\?'); target = rd(mt[1]).div(rd(mt[2])).mul(hund); break;
        case 'whole': mt = R(NUM + ' is ' + NUM + '% of what number\\?'); target = rd(mt[1]).div(pc(mt[2])); break;
        case 'change': mt = R('had ' + NUM + ' members last year and has ' + NUM + ' members this year'); var o = rd(mt[1]), nw = rd(mt[2]), df = nw.sub(o);
          word = df.n > 0n ? 'increase' : 'decrease'; target = (df.n < 0n ? df.neg() : df).div(o).mul(hund); break;
        case 'discount': mt = R('costs \\$' + NUM + '\\. It is on sale for ' + NUM + '% off'); target = rd(mt[1]).mul(Q.ONE.sub(pc(mt[2]))); break;
        case 'interest': mt = R('puts \\$' + NUM + ' in an account that earns ' + NUM + '% simple interest per year\\. How much interest does she earn in ' + NUM + ' years'); target = rd(mt[1]).mul(pc(mt[2])).mul(rd(mt[3])); break;
        case 'disc-tax': mt = R('costs \\$' + NUM + '\\. It is ' + NUM + '% off, and then ' + NUM + '% sales tax is added to the sale price'); target = rd(mt[1]).mul(Q.ONE.sub(pc(mt[2]))).mul(Q.ONE.add(pc(mt[3]))); break;
        case 'original': mt = R('After an? ' + NUM + '% discount, an? [^$]* costs \\$' + NUM + '\\.'); target = rd(mt[2]).div(Q.ONE.sub(pc(mt[1]))); break;
        case 'two-changes': mt = R('that cost \\$' + NUM + ' by ' + NUM + '%\\. Later it lowers the new price by ' + NUM + '%'); var o2 = rd(mt[1]);
          target = o2.mul(Q.ONE.add(pc(mt[2]))).mul(Q.ONE.sub(pc(mt[3]))); var d2 = target.sub(o2); word = d2.n > 0n ? 'more' : d2.n < 0n ? 'less' : 'same'; break;
        default: throw new C.CheckError('unknown percent scenario');
      }
      var gotN = C.numbersInText(ans).concat(C.snippets(ans).map(function (m) { try { return C.readNumber(m); } catch (e) { return null; } }).filter(Boolean));
      if (!gotN.length) return { status: 'mismatch', msg: 'No number in the answer.' };
      var low = C.plainText(ans).toLowerCase();
      if (!gotN[0].eq(target)) return { status: 'mismatch', msg: 'Correct: ' + qText(target) + (word ? ' (' + word + ')' : '') + '.', computed: qText(target) };
      if (word && low.indexOf(word) < 0) return { status: 'mismatch', msg: 'Say whether it is ' + (word === 'increase' || word === 'decrease' ? 'an increase or a decrease' : 'more or less') + ': ' + word + '.' };
      if (word === 'increase' && /decrease/.test(low) || word === 'decrease' && /increase/.test(low) || word === 'more' && /\bless\b/.test(low) || word === 'less' && /\bmore\b/.test(low)) return { status: 'mismatch', msg: 'The direction is wrong.' };
      if (/^(what-pct|change)$/.test(chk.scenario) && !/%|percent/.test(low)) return { status: 'mismatch', msg: 'Write the answer as a percent.' };
      return { status: 'verified', computed: qText(target) };
    }
    if (t === 'solve' && /^(geo-congruence-(side|angle)|geo-parallelogram-(sides|angles))-/.test(p.variant || '')) {
      var given = firstMath(p.prompt), lhs = chk.eq.substring(0, chk.eq.indexOf('='));
      if (!given || !C.equivalent(given, lhs)) return {status:'invalid',msg:'Displayed geometric measure differs from equation.'};
    }
    if (t === 'solve') {
      // For congruence applications, the equation must follow from the
      // side lengths the student actually sees, not just a hidden check.eq.
      if (/^geo-criterion-/.test(p.variant || '')) {
        var printed = /[A-Z]{2} = ⟨([^⟩]+)⟩ units and [A-Z]{2} = (\d+) units/.exec(p.prompt || '');
        if (!printed || printed[1]+'='+printed[2] !== chk.eq) {
          return {status:'invalid',msg:'Congruence equation conflicts with the printed side lengths.'};
        }
      }
      // Independently re-derive the equation from the visible geometric
      // measure and stated numerical dimension. Merely displaying chk.eq
      // is insufficient: a student-visible measure may have been edited.
      var variant = p.variant || '', visible = firstMath(p.prompt || '');
      var tri = /^geo-triangle-(midsegment|centroid|side-angle-order|perpendicular-bisector)-/.exec(variant);
      if (tri) {
        var txt = C.plainText(p.prompt || ''), num, implied;
        if (tri[1] === 'midsegment') {
          num = /BC measures (\d+) units/.exec(txt);
          if (num) implied = visible+'='+num[1]+'/2';
        } else if (tri[1] === 'centroid') {
          num = /full median AM measures (\d+) units/.exec(txt);
          if (num) implied = '3*('+visible+')='+num[1];
        } else if (tri[1] === 'side-angle-order') {
          num = /longest side is (\d+) units/.exec(txt);
          if (num) implied = visible+'='+num[1];
        } else {
          num = /PB measures (\d+) units/.exec(txt);
          if (num) implied = visible+'='+num[1];
        }
        if (!visible || !num || !implied ||
            !C.solveLinear(implied,chk.v).value.eq(C.solveLinear(chk.eq,chk.v).value)) {
          return {status:'invalid',msg:'Visible triangle measurements do not agree with the solution equation.'};
        }
      }
      if (/^geo-structured-proof-/.test(variant)) {
        var proofMeasures = /angle [A-Z]{3} = ⟨([^⟩]+)⟩ degrees and angle [A-Z]{3} = (\d+) degrees/.exec(p.prompt || '');
        if (!proofMeasures || proofMeasures[1]+'='+proofMeasures[2] !== chk.eq) {
          return {status:'invalid',msg:'Proof equation conflicts with the visible angle measures.'};
        }
      }
      var s = C.solveLinear(chk.eq, chk.v);
      if (s.kind !== 'one') return { status: 'invalid', msg: s.kind === 'none' ? 'This equation has no solution.' : 'Every number is a solution of this equation.' };
      if (policy && policy.intOnly && !s.value.isInt()) return { status: 'invalid', msg: 'The solution is not a whole number.', computed: chk.v + '=' + qText(s.value) };
      var got = valueFromAnswer(ans, chk.v);
      return got.eq(s.value) ? { status: 'verified', computed: chk.v + '=' + qText(s.value) } : { status: 'mismatch', msg: 'Correct answer is ' + chk.v + ' = ' + s.value + '.', computed: chk.v + '=' + qText(s.value) };
    }
    if (t === 'classify') {
      var k = C.solveLinear(chk.eq, chk.v), said = C.classifyText(C.plainText(ans));
      var comp = k.kind === 'none' ? 'No solution' : k.kind === 'all' ? 'Infinitely many solutions' : 'One solution: ⟨' + chk.v + '=' + qText(k.value) + '⟩';
      if (k.kind === 'one') {
        if (said) return { status: 'mismatch', msg: 'This equation has exactly one solution.', computed: comp };
        if (policy && policy.intOnly && !k.value.isInt()) return { status: 'invalid', msg: 'The solution is not a whole number.', computed: comp };
        return valueFromAnswer(ans, chk.v).eq(k.value) ? { status: 'verified', computed: comp } : { status: 'mismatch', msg: 'Correct: ' + comp, computed: comp };
      }
      return said === k.kind ? { status: 'verified', computed: comp } : { status: 'mismatch', msg: 'Correct: ' + comp, computed: comp };
    }
    if (t === 'simplify') {
      var am = firstMath(ans); if (am === null) return { status: 'mismatch', msg: 'No simplified expression in the answer.' };
      if (!C.equivalent(chk.expr, am)) return { status: 'mismatch', msg: 'The answer is not equivalent to the expression.' };
      var form = C.simplifiedForm(am);
      if (!form.ok) return { status: 'mismatch', msg: 'The answer is not fully simplified (' + form.problems.join(', ') + ').' };
      return { status: 'verified' };
    }
    if (t === 'evaluate') {
      var env = {}, vals = chk.values || {};
      Object.keys(vals).forEach(function (v) {
        if (!shown(p, v + '=' + vals[v])) throw new C.CheckError('value ' + v + ' is not printed in the problem');
        env[v] = C.readNumber(vals[v]);
      });
      var val = C.evalNode(C.parseExpr(chk.expr), env);
      if (policy && policy.intOnly && !val.isInt()) return { status: 'invalid', msg: 'The value is not a whole number.', computed: qText(val) };
      return valueFromAnswer(ans).eq(val) ? { status: 'verified', computed: qText(val) } : { status: 'mismatch', msg: 'Correct value is ' + val + '.', computed: qText(val) };
    }
    if (t === 'literal') {
      var am2 = firstMath(ans); if (am2 === null) return { status: 'mismatch', msg: 'No equation in the answer.' };
      var lr = C.checkLiteral(chk.eq, chk.v, am2);
      return lr.ok ? { status: 'verified' } : { status: 'mismatch', msg: lr.reason };
    }
    if (t === 'literal-eval') {
      if (!shown(p, chk.given)) return { status: 'invalid', msg: 'The given values are not the ones printed.' };
      var rel = C.parseRelation(chk.eq), env2 = {};
      chk.given.split(',').forEach(function (g) { var rr = C.parseRelation(g); env2[rr.lhs.v] = C.readNumber(g.slice(g.indexOf('=') + 1)); });
      function sub(n) {
        if (n.k === 'var' && env2[n.v]) return { k: 'num', v: env2[n.v] };
        var c2 = Object.assign({}, n); if (c2.a) c2.a = sub(c2.a); if (c2.b) c2.b = sub(c2.b); return c2;
      }
      var s2 = C.solveLinear({ lhs: sub(rel.lhs), rhs: sub(rel.rhs), rel: '=' }, chk.v);
      if (s2.kind !== 'one') return { status: 'invalid', msg: 'These values do not give one answer.' };
      if (policy && policy.intOnly && !s2.value.isInt()) return { status: 'invalid', msg: 'The value is not a whole number.' };
      return valueFromAnswer(ans, chk.v).eq(s2.value) ? { status: 'verified', computed: chk.v + '=' + qText(s2.value) } : { status: 'mismatch', msg: 'Correct value: ' + chk.v + ' = ' + s2.value + '.', computed: chk.v + '=' + qText(s2.value) };
    }
    if (t === 'model-eq') {
      var sc = SCEN[chk.scenario](p); if (!sc.ok) return { status: 'invalid', msg: 'The word problem does not have a whole-number answer.' };
      var em = firstMath(ans); if (em === null) return { status: 'mismatch', msg: 'No equation in the answer.' };
      var sol = C.solveLinear(em, chk.v);
      return sol.kind === 'one' && sol.value.eq(sc.n) ? { status: 'verified' } : { status: 'mismatch', msg: 'The equation does not model the situation.' };
    }
    if (t === 'scenario') {
      var S = SCEN[chk.scenario](p); if (!S.ok) return { status: 'invalid', msg: 'The word problem does not have a whole-number answer.' };
      var nums = C.numbersInText(ans).concat(C.snippets(ans).map(function (m) { try { return valueFromAnswer('⟨' + m + '⟩'); } catch (e) { return null; } }).filter(Boolean));
      function has(q) { return nums.some(function (z) { return z.eq(q); }); }
      if (chk.want === 'n') return has(S.n) ? { status: 'verified', computed: String(S.n) } : { status: 'mismatch', msg: 'Correct answer: ' + S.n + '.' };
      if (chk.want === 'cost') return has(S.cost) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct cost: $' + S.cost + '.' };
      if (chk.want === 'compare') {
        var cs = S.costAt(new Q(chk.n)), cheaper = cs[0].n < cs[1].n ? 0 : 1, diff = cs[0].sub(cs[1]); if (diff.n < 0n) diff = diff.neg();
        var nameOk = S.names.length === 2 && C.plainText(ans).indexOf(S.names[cheaper]) === 0;
        return nameOk && has(diff) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: ' + (S.names[cheaper] || '') + ', by $' + diff + '.' };
      }
      if (chk.want === 'wl') { var a = C.numbersInText(ans); return a.length >= 2 && a[0].eq(S.w) && a[1].eq(S.L) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: width ' + S.w + ', length ' + S.L + '.' }; }
      if (chk.want === 'square') {
        var side = S.P.div(new Q(4)), sq = side.mul(side), rec = S.w.mul(S.L), d = sq.sub(rec), word = d.n > 0n ? 'square' : 'rectangle'; if (d.n < 0n) d = d.neg();
        return C.plainText(ans).toLowerCase().indexOf(word) >= 0 && has(d) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: the ' + word + ', by ' + d + '.' };
      }
      if (chk.want === 'list') {
        var got = C.numbersInText(ans);
        return got.length === S.list.length && got.every(function (g, i) { return g.eq(S.list[i]); }) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: ' + S.list.join(', ') + '.' };
      }
    }
    return { status: 'manual', msg: 'Unknown check type ' + t };
  }

  function checkIneqPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, v = chk.v || 'x', res;
    function figOk(set) {
      if (!part.answerFig) return null;
      var fs = figSet(part.answerFig);
      if (!C.setEqual(fs.set, set)) return { status: 'mismatch', msg: 'The number line in the key does not match the answer.' };
      if (!fitsWindow(set, fs)) return { status: 'invalid', msg: 'The number line in the key does not show every endpoint.' };
      return null;
    }
    function blankOk(set) {
      if (!p.fig || (p.fig.pieces && p.fig.pieces.length)) return null;
      return fitsWindow(set, figSet(p.fig)) ? null : { status: 'invalid', msg: 'The printed number line does not reach the answer’s endpoints.' };
    }
    if (t === 'ineq') {
      if (!shown(p, chk.ineq)) return { status: 'invalid', msg: 'The inequality being checked is not the one printed for students.' };
      var set = C.solutionSet(chk.ineq, v), comp = C.setText(set, v);
      if (policy && policy.intOnly && !intEnds(set)) return { status: 'invalid', msg: 'The boundary is not a whole number.', computed: comp };
      if (!chk.allowSpecial && (!set.length || (set.length === 1 && !set[0].lo && !set[0].hi))) return { status: 'invalid', msg: 'The solution is ' + comp.toLowerCase() + ' (not intended here).', computed: comp };
      var got = C.setFromAnswer(ans, v);
      if (!C.setEqual(got, set)) return { status: 'mismatch', msg: 'Correct solution: ' + comp, computed: comp };
      if (!C.solvedForm(ans, v)) return { status: 'mismatch', msg: 'The answer is not written with ' + v + ' by itself.', computed: comp };
      return figOk(set) || blankOk(set) || { status: 'verified', computed: comp };
    }
    if (t === 'read-graph') {
      if (!p.fig || !p.fig.pieces || !p.fig.pieces.length) return { status: 'invalid', msg: 'There is no graph to read.' };
      var gs = figSet(p.fig).set, gt = C.setText(gs, v);
      if (!fitsWindow(gs, figSet(p.fig))) return { status: 'invalid', msg: 'The printed graph does not show its endpoints clearly.' };
      if (policy && policy.intOnly && !intEnds(gs)) return { status: 'invalid', msg: 'The graph has a non-integer endpoint.' };
      var formOk = chk.form === 'abs' ? C.snippets(ans).some(function (x) { return /\|/.test(x); }) : C.solvedForm(ans, v);
      return C.setEqual(C.setFromAnswer(ans, v), gs) && formOk ? { status: 'verified', computed: gt } : { status: 'mismatch', msg: 'The graph shows ' + gt + (chk.form === 'abs' ? ' (answer must use absolute value)' : ''), computed: gt };
    }
    if (t === 'ineq-members') {
      if (!shown(p, chk.ineq)) return { status: 'invalid', msg: 'The inequality being checked is not the one printed for students.' };
      var cond = C.parseCondition(chk.ineq), yes = [];
      chk.values.forEach(function (vt) {
        if (!shown(p, vt)) throw new C.CheckError('value ' + vt + ' is not printed');
        var q = C.readNumber(vt); if (C.truth(cond, v, q)) yes.push(q);
      });
      var said = /none/i.test(C.plainText(ans)) && !C.snippets(ans).length ? [] : C.snippets(ans).map(function (x) { return C.readNumber(x.replace(/^[a-z]=/, '')); });
      var same = said.length === yes.length && said.every(function (q) { return yes.some(function (y) { return y.eq(q); }); });
      return same ? { status: 'verified' } : { status: 'mismatch', msg: 'Solutions: ' + (yes.length ? yes.join(', ') : 'none') + '.' };
    }
    if (t === 'error-line') {
      if (!shown(p, chk.ineq)) return { status: 'invalid', msg: 'The original inequality is not printed.' };
      var base = C.solutionSet(chk.ineq, v), first = 0;
      chk.lines.forEach(function (ln, i) { if (!shown(p, ln)) throw new C.CheckError('work line not printed: ' + ln); if (!first && !C.setEqual(C.solutionSet(ln, v), base)) first = i + 1; });
      if (!first) return { status: 'invalid', msg: 'The shown work has no mistake.' };
      var m = /line\s*(\d+)/i.exec(C.plainText(ans));
      return m && +m[1] === first ? { status: 'verified', computed: 'Line ' + first } : { status: 'mismatch', msg: 'The first wrong line is line ' + first + '.', computed: 'Line ' + first };
    }
    if (t === 'model-ineq' || t === 'iscenario') {
      var text = C.plainText(p.prompt), sc = ISCEN[chk.scenario](text, C.numbersInText(p.prompt));
      if (t === 'model-ineq') {
        var em = C.snippets(ans)[0]; if (!em) return { status: 'mismatch', msg: 'No inequality in the answer.' };
        var mset = C.solutionSet(em, chk.v);
        return C.setEqual(mset, sc.set) ? { status: 'verified' } : { status: 'mismatch', msg: 'The inequality does not model the situation.' };
      }
      if (chk.want === 'set') {
        var aset = C.setFromAnswer(ans, chk.v);
        return C.setEqual(aset, sc.set) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: ' + C.setText(sc.set, chk.v) };
      }
      var nums = C.numbersInText(ans);
      if (chk.want === 'best') {
        // the solved inequality written in the answer must also be right
        var sn = C.snippets(ans);
        if (sn.length) { var sset; try { sset = C.solutionSet(sn[0], chk.v); } catch (e) { return { status: 'mismatch', msg: 'Could not read the inequality in the answer.' }; }
          if (!C.setEqual(sset, sc.set)) return { status: 'mismatch', msg: 'The solved inequality should be ' + C.setText(sc.set, chk.v) + '.' }; }
      }
      if (chk.want === 'best') return nums.some(function (q) { return q.eq(sc.best); }) && new RegExp(sc.dir === 'max' ? 'at most|maximum|up to|no more' : 'at least|minimum|no fewer', 'i').test(C.plainText(ans)) ? { status: 'verified' } : { status: 'mismatch', msg: 'The ' + (sc.dir === 'max' ? 'most' : 'least') + ' is ' + sc.best + '.' };
      if (chk.want === 'range') { var ints = C.numbersInText(ans), a0 = ceilQ(sc.lo), b0 = floorQ(sc.hi); return ints.length >= 2 && ints[0].eq(a0) && ints[1].eq(b0) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: from ' + a0 + ' to ' + b0 + '.' }; }
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }

  /* ---------- relations and functions (Algebra 1 Unit 4) ---------- */
  var FUNC_TYPES = ['domain-range', 'is-function', 'func-eval', 'func-solve', 'func-combo', 'read-fig', 'linear-rule', 'table-fill', 'rate', 'graph-behavior', 'sequence', 'curve-behavior'];
  function qOf(pair) { return pair ? new Q(pair[0], pair[1]) : null; }
  function qStr(s) { return C.readNumber(String(s)); }
  /* ordered pairs printed in the problem, e.g. ⟨(1,\ 4),\ (2,\ -3)⟩ */
  function pairsFrom(tex) {
    var out = [], re = /\(\s*(-?[\d.]+(?:\/\d+)?)\s*,\s*(?:\\[ ,;]\s*)*(-?[\d.]+)\s*\)/g, m;
    var t = String(tex).replace(/\\[ ,;!]/g, ' ');
    while ((m = re.exec(t))) out.push([qStr(m[1]), qStr(m[2])]);
    return out;
  }
  /* What relation does the student see? Reads the drawn figure (or printed pairs). */
  function relationOf(p, chk) {
    if (chk.pairs) {
      if (!shown(p, chk.pairs)) throw new C.CheckError('the ordered pairs being checked are not printed');
      return { kind: 'discrete', pairs: pairsFrom(chk.pairs) };
    }
    var f = p.fig; if (!f) throw new C.CheckError('no figure to read');
    if (f.kind === 'table') return { kind: 'discrete', pairs: NS.fig.readTable(NS.fig.table(f)).filter(function (r) { return r[0] !== '?' && r[1] !== '?'; }).map(function (r) { return [qStr(r[0]), qStr(r[1])]; }) };
    if (f.kind === 'mapping') return { kind: 'discrete', pairs: NS.fig.readMapping(NS.fig.mapping(f)).pairs.map(function (r) { return [qStr(r[0]), qStr(r[1])]; }) };
    if (f.kind === 'plane') {
      var g = NS.fig.readPlane(NS.fig.plane(f));
      if (g.segs.length || g.curves.length) return { kind: 'graph', segs: g.segs.map(function (sg) { return { a: [qOf(sg.a[0]), qOf(sg.a[1])], b: [qOf(sg.b[0]), qOf(sg.b[1])], aEnd: sg.aEnd, bEnd: sg.bEnd }; }), curves: g.curves.map(function (c) { return c.map(function (pt) { return [qOf(pt[0]), qOf(pt[1])]; }); }), points: g.points };
      return { kind: 'discrete', pairs: g.points.map(function (pt) { return [qOf(pt.x), qOf(pt.y)]; }) };
    }
    throw new C.CheckError('cannot read this figure');
  }
  function uniqQ(list) { return C.parseCondition ? list.slice().sort(function (a, b) { return C.cmpQ(a, b); }).filter(function (q, i, arr) { return i === 0 || !arr[i - 1].eq(q); }) : list; }
  function setOfNumbers(markup) {
    var sn = C.snippets(markup).join(' ');
    var body = /\\\{([^}]*)\\\}/.exec(sn) || /\{([^}]*)\}/.exec(sn);
    if (!body) return null;
    return uniqQ(body[1].replace(/\\[ ,;!]/g, ' ').split(',').map(function (x) { return x.trim(); }).filter(Boolean).map(qStr));
  }
  function sameList(a, b) { return a.length === b.length && a.every(function (q, i) { return q.eq(b[i]); }); }
  /* domain or range of a drawn graph: union of the pieces' x- (or y-) intervals */
  function graphSpan(rel, axis) {
    var k = axis === 'x' ? 0 : 1, conds = [];
    rel.segs.forEach(function (sg) {
      var A = sg.a[k], B = sg.b[k], aIn = sg.aEnd !== 'open', bIn = sg.bEnd !== 'open', aInf = sg.aEnd === 'arrow', bInf = sg.bEnd === 'arrow';
      var lo = A, hi = B, loIn = aIn, hiIn = bIn, loInf = aInf, hiInf = bInf;
      if (C.cmpQ(A, B) > 0) { lo = B; hi = A; loIn = bIn; hiIn = aIn; loInf = bInf; hiInf = aInf; }
      if (C.cmpQ(A, B) === 0) { if (aInf || bInf) throw new C.CheckError('vertical/horizontal ray'); conds.push('v=' + qText(A)); return; }
      var parts = [];
      if (!loInf) parts.push('v' + (loIn ? '\\ge ' : '>') + qText(lo));
      if (!hiInf) parts.push('v' + (hiIn ? '\\le ' : '<') + qText(hi));
      conds.push(parts.length ? parts.join('\\text{ and }') : 'v=v');
    });
    rel.curves.forEach(function (cv) { var vals = cv.map(function (pt) { return pt[k]; }); var lo = vals.reduce(function (m, q) { return C.cmpQ(q, m) < 0 ? q : m; }), hi = vals.reduce(function (m, q) { return C.cmpQ(q, m) > 0 ? q : m; }); conds.push('v\\ge ' + qText(lo) + '\\text{ and }v\\le ' + qText(hi)); });
    // union of pieces
    var sets = conds.map(function (c) { return /v=v/.test(c) ? C.solutionSet('v>v-1', 'v') : C.solutionSet(c, 'v'); });
    return sets.reduce(function (acc, st) { return unionSets(acc, st); }, []);
  }
  function unionSets(a, b) {
    // evaluate membership on a fine set of candidate points built from both sets' endpoints
    var pts = []; a.concat(b).forEach(function (I) { if (I.lo) pts.push(I.lo); if (I.hi) pts.push(I.hi); });
    pts = uniqQ(pts);
    function inSet(S, x) { return S.some(function (I) { var lo = !I.lo || C.cmpQ(x, I.lo) > 0 || (I.loC && I.lo.eq(x)); var hi = !I.hi || C.cmpQ(x, I.hi) < 0 || (I.hiC && I.hi.eq(x)); return lo && hi; }); }
    if (!pts.length) return a.length || b.length ? [{ lo: null, loC: false, hi: null, hiC: false }] : [];
    var samples = [{ x: pts[0].sub(Q.ONE), gap: [null, pts[0]] }];
    pts.forEach(function (c, i) { samples.push({ x: c, point: c }); var nx = pts[i + 1]; samples.push(nx ? { x: c.add(nx).div(new Q(2)), gap: [c, nx] } : { x: c.add(Q.ONE), gap: [c, null] }); });
    var out = [];
    samples.forEach(function (sm) {
      if (!(inSet(a, sm.x) || inSet(b, sm.x))) return;
      var lo = sm.point || sm.gap[0], hi = sm.point || sm.gap[1], loC = !!sm.point, hiC = !!sm.point, last = out[out.length - 1];
      if (last && last.hi && lo && C.cmpQ(last.hi, lo) === 0 && (last.hiC || loC)) { last.hi = hi; last.hiC = hiC; }
      else out.push({ lo: lo, loC: lo ? loC : false, hi: hi, hiC: hi ? hiC : false });
    });
    return out;
  }
  /* y-value(s) of a drawn graph at x */
  function graphAt(rel, x) {
    var ys = [];
    rel.segs.forEach(function (sg) {
      var x1 = sg.a[0], x2 = sg.b[0]; if (x1.eq(x2)) { if (x1.eq(x)) ys.push(sg.a[1], sg.b[1]); return; }
      var t = x.sub(x1).div(x2.sub(x1)), inA = sg.aEnd !== 'open', inB = sg.bEnd !== 'open';
      var ok = (C.cmpQ(t, Q.ZERO) > 0 || (t.isZero() && inA) || (C.cmpQ(t, Q.ZERO) < 0 && sg.aEnd === 'arrow')) && (C.cmpQ(t, Q.ONE) < 0 || (t.eq(Q.ONE) && inB) || (C.cmpQ(t, Q.ONE) > 0 && sg.bEnd === 'arrow'));
      if (ok) ys.push(sg.a[1].add(sg.b[1].sub(sg.a[1]).mul(t)));
    });
    return uniqQ(ys);
  }
  function ruleRHS(rule) { var i = rule.indexOf('='); if (i < 0) throw new C.CheckError('rule needs ='); return C.parseExpr(rule.slice(i + 1)); }
  function subst(node, v, valNode) {
    if (node.k === 'var') return node.v === v ? { k: 'grp', a: valNode } : node;
    var c = Object.assign({}, node); if (c.a) c.a = subst(c.a, v, valNode); if (c.b) c.b = subst(c.b, v, valNode); return c;
  }
  /* replace printed calls like f(3) or g(-1) by their values (from the printed rules) */
  function evalCalls(expr, rules) {
    var named = {};
    rules.forEach(function (r) { var m = /^\s*([a-zA-Z])\(\s*([a-z])\s*\)\s*=/.exec(r); if (!m) throw new C.CheckError('cannot read rule ' + r); named[m[1]] = { v: m[2], rhs: ruleRHS(r), txt: r.slice(r.indexOf('=') + 1) }; });
    var out = String(expr).replace(/([a-zA-Z])\(([^()]*)\)/g, function (w, f, arg) {
      if (!named[f]) return w;
      C.parseExpr(arg);   // the argument must be readable
      var rhsTxt = named[f].txt.replace(/\\[a-zA-Z]+|[a-zA-Z]/g, function (tok) { return tok === named[f].v ? '(' + arg + ')' : tok; });
      return '(' + rhsTxt + ')';
    });
    return out;
  }
  function texOfRF(rf) { if (!rf.isPoly() || !rf.asPoly().isConst()) throw new C.CheckError('expected a number'); return qText(rf.asPoly().constVal()).replace(/^-/, '0-'); }
  function lastEq(markup) { var sn = C.snippets(markup); if (!sn.length) return null; var s = sn[sn.length - 1]; var i = s.lastIndexOf('='); return i >= 0 ? s.slice(i + 1) : s; }
  /* numbers in the answer, where one snippet may list several ("5,\\ 9") */
  function listNumbers(markup) { var out = []; C.snippets(markup).forEach(function (sn) { var i = sn.lastIndexOf('='); (i >= 0 ? sn.slice(i + 1) : sn).replace(/\\[ ;!]/g, '').split(/,|\\,/).forEach(function (x) { x = x.trim(); if (x) out.push(qStr(x)); }); }); return out; }
  function answerNumbers(markup) { return C.snippets(markup).map(function (s) { var i = s.lastIndexOf('='); return qStr((i >= 0 ? s.slice(i + 1) : s).replace(/\\[ ,;!]/g, '')); }); }

  function checkFuncPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, txt = C.plainText(ans).toLowerCase();
    if (t === 'domain-range' || t === 'is-function') {
      var rel;
      if (chk.equation) {
        if (!shown(p, chk.equation)) return { status: 'invalid', msg: 'The equation is not printed.' };
        var r = C.parseRelation(chk.equation), many = false, found = 0;
        for (var xi = -60; xi <= 60 && !many; xi++) {
          var ys = [];
          for (var yi = -40; yi <= 40; yi++) { var env = { x: new Q(xi), y: new Q(yi) }; try { if (C.evalNode(r.lhs, env).eq(C.evalNode(r.rhs, env))) ys.push(yi); } catch (e) { /* skip */ } }
          if (ys.length > 1) many = true; if (ys.length) found++;
        }
        if (!found) return { status: 'invalid', msg: 'No whole-number points to test.' };
        var isF = !many, said = /^\s*yes/.test(txt) ? true : /^\s*no/.test(txt) ? false : null;
        return said === isF ? { status: 'verified', computed: isF ? 'Yes' : 'No' } : { status: 'mismatch', msg: 'Correct: ' + (isF ? 'Yes, it is a function.' : 'No, some x has two y-values.'), computed: isF ? 'Yes' : 'No' };
      }
      rel = relationOf(p, chk);
      if (t === 'is-function') {
        var isFun = true;
        if (rel.kind === 'discrete') { var seen = {}; rel.pairs.forEach(function (pr) { var k = pr[0].toString(); if (seen[k] !== undefined && seen[k] !== pr[1].toString()) isFun = false; seen[k] = pr[1].toString(); }); }
        else {
          // vertical line test at many x-values (including every drawn x-coordinate)
          var xs = []; rel.segs.forEach(function (sg) { xs.push(sg.a[0], sg.b[0]); }); rel.curves.forEach(function (cv) { cv.forEach(function (pt) { xs.push(pt[0]); }); });
          xs = uniqQ(xs); var probes = xs.slice(); xs.forEach(function (x, i) { if (xs[i + 1]) probes.push(x.add(xs[i + 1]).div(new Q(2))); });
          probes.forEach(function (x) {
            var hits = graphAt(rel, x).length;
            rel.curves.forEach(function (cv) { for (var i = 0; i + 1 < cv.length; i++) { var a = cv[i], b = cv[i + 1]; if (C.cmpQ(a[0], b[0]) === 0) { if (a[0].eq(x)) hits += 2; continue; } var lo = C.cmpQ(a[0], b[0]) < 0 ? a[0] : b[0], hi = C.cmpQ(a[0], b[0]) < 0 ? b[0] : a[0]; if (C.cmpQ(x, lo) >= 0 && C.cmpQ(x, hi) < 0) hits++; if (i + 2 === cv.length && x.eq(hi)) hits++; } });
            if (hits > 1) isFun = false;
          });
        }
        var said2 = /^\s*yes/.test(txt) ? true : /^\s*no/.test(txt) ? false : null;
        if (rel.kind === 'graph' && C.snippets(ans).length) {
          // an explanation that names an x-value must name the one that matters
          var gx = /x=(-?[\d.\/]+)/.exec(norm(C.snippets(ans)[0]));
          if (gx) { var gq = qStr(gx[1]), nh = graphAt(rel, gq).length, isEnd = rel.segs.some(function (sg) { return (sg.a[0].eq(gq) && sg.aEnd !== 'arrow' && sg.aEnd !== 'none') || (sg.b[0].eq(gq) && sg.bEnd !== 'arrow' && sg.bEnd !== 'none'); });
            if (said2 === false ? nh < 2 : !isEnd) return { status: 'mismatch', msg: 'The explanation names the wrong x-value.' }; }
        }
        if (said2 === false && !isFun && rel.kind === 'discrete' && C.snippets(ans).length) {
          // the explanation names an input and its outputs: they must really be paired
          var sn0 = C.snippets(ans), cx = /x=(-?[\d.\/]+)/.exec(norm(sn0[0]));
          if (!cx) return { status: 'mismatch', msg: 'Name the input that has two outputs.' };
          var xq = qStr(cx[1]), outs = sn0.slice(1).map(function (z) { return qStr(z.replace(/\\[ ,;!]/g, '')); });
          var real = rel.pairs.filter(function (pr) { return pr[0].eq(xq); }).map(function (pr) { return pr[1]; });
          if (outs.length < 2 || !outs.every(function (o) { return real.some(function (y) { return y.eq(o); }); }) || outs[0].eq(outs[1])) return { status: 'mismatch', msg: 'The explanation does not match the relation.' };
        }
        return said2 === isFun ? { status: 'verified', computed: isFun ? 'Yes' : 'No' } : { status: 'mismatch', msg: 'Correct: ' + (isFun ? 'Yes.' : 'No.'), computed: isFun ? 'Yes' : 'No' };
      }
      // domain / range
      var axis = chk.want === 'domain' ? 'x' : 'y';
      if (rel.kind === 'discrete') {
        var vals = uniqQ(rel.pairs.map(function (pr) { return pr[axis === 'x' ? 0 : 1]; })), got = setOfNumbers(ans);
        if (!got) return { status: 'mismatch', msg: 'Write the ' + chk.want + ' as a set in braces.' };
        return sameList(got, vals) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct ' + chk.want + ': {' + vals.join(', ') + '}' };
      }
      var span = graphSpan(rel, axis), comp = C.setText(span, axis);
      if (policy && policy.intOnly && span.some(function (I) { return (I.lo && !I.lo.isInt()) || (I.hi && !I.hi.isInt()); })) return { status: 'invalid', msg: 'Non-integer endpoint.' };
      var aset; try { aset = C.setFromAnswer(ans, axis); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer: ' + e.message, computed: comp }; }
      return C.setEqual(aset, span) ? { status: 'verified', computed: comp } : { status: 'mismatch', msg: 'Correct ' + chk.want + ': ' + comp, computed: comp };
    }
    if (t === 'func-eval' || t === 'func-combo') {
      var rules = chk.rules || [chk.rule];
      for (var i = 0; i < rules.length; i++) if (!shown(p, rules[i])) return { status: 'invalid', msg: 'The rule is not printed.' };
      if (!shown(p, chk.expr) && !C.snippets(C.plainText ? NS.studentText(p) : '').some(function (s) { return s.replace(/\s/g, '').indexOf(chk.expr.replace(/\s/g, '')) >= 0; })) return { status: 'invalid', msg: 'The expression is not printed.' };
      var value = C.toRF(C.parseExpr(evalCalls(chk.expr, rules)));
      var ansSn = lastEq(ans); if (ansSn === null) return { status: 'mismatch', msg: 'No answer.' };
      var chain = C.snippets(ans); chain = chain[chain.length - 1].split('=');
      if (chain.length > 1 && /^[a-zA-Z]\(/.test(chain[0].trim()) && norm(chain[0]) !== norm(chk.expr)) return { status: 'mismatch', msg: 'The answer is for ' + chain[0] + ', not ' + chk.expr + '.' };
      for (var ci = 1; ci + 1 < chain.length; ci++) { var mid = C.toRF(C.parseExpr(evalCalls(chain[ci], rules))); if (!mid.sub(value).n.isZero()) return { status: 'mismatch', msg: 'A middle step is wrong.' }; }
      var got2 = C.toRF(C.parseExpr(ansSn));
      var same = got2.sub(value).n.isZero();
      if (same && chk.symbolic) { var fm = C.simplifiedForm(ansSn); if (!fm.ok) return { status: 'mismatch', msg: 'Simplify fully (' + fm.problems.join(', ') + ').' }; }
      if (!value.isPoly() || !value.asPoly().isConst()) return same ? { status: 'verified' } : { status: 'mismatch', msg: 'Not equivalent.' };
      var cv = value.asPoly().constVal();
      if (policy && policy.intOnly && !cv.isInt()) return { status: 'invalid', msg: 'The value is not a whole number.', computed: qText(cv) };
      return same ? { status: 'verified', computed: qText(cv) } : { status: 'mismatch', msg: 'Correct value: ' + cv + '.', computed: qText(cv) };
    }
    if (t === 'func-solve') {
      if (!shown(p, chk.rule)) return { status: 'invalid', msg: 'The rule is not printed.' };
      var eq = chk.rule.slice(chk.rule.indexOf('=') + 1) + '=' + chk.value;
      var s2 = C.solveLinear(eq, chk.v || 'x');
      if (s2.kind !== 'one') return { status: 'invalid', msg: 'No single solution.' };
      if (policy && policy.intOnly && !s2.value.isInt()) return { status: 'invalid', msg: 'Not a whole number.' };
      return answerNumbers(ans).some(function (q) { return q.eq(s2.value); }) ? { status: 'verified', computed: (chk.v || 'x') + '=' + qText(s2.value) } : { status: 'mismatch', msg: 'Correct: ' + (chk.v || 'x') + ' = ' + s2.value + '.', computed: (chk.v || 'x') + '=' + qText(s2.value) };
    }
    if (t === 'read-fig') {
      var rel2 = relationOf(p, chk), want = chk.want;
      if (want === 'value') {
        var at = qStr(chk.at), ys2 = rel2.kind === 'discrete' ? uniqQ(rel2.pairs.filter(function (pr) { return pr[0].eq(at); }).map(function (pr) { return pr[1]; })) : graphAt(rel2, at);
        if (ys2.length !== 1) return { status: 'invalid', msg: 'The figure does not give one value at x = ' + at + '.' };
        var calls = []; C.snippets(ans).forEach(function (sn) { var re2 = /f\((-?[\d.\/]+)\)/g, mm2; while ((mm2 = re2.exec(norm(sn)))) calls.push(qStr(mm2[1])); });
        if (chk.inner !== undefined) {
          var inner = qStr(chk.inner), iy = rel2.kind === 'discrete' ? rel2.pairs.filter(function (pr) { return pr[0].eq(inner); }).map(function (pr) { return pr[1]; }) : graphAt(rel2, inner);
          if (iy.length !== 1 || !iy[0].eq(at)) return { status: 'mismatch', msg: 'f(' + inner + ') is not ' + at + '.' };
          if (!shown(p, 'f(f(' + chk.inner + '))') && !C.snippets(studentText(p)).some(function (sn) { return norm(sn).indexOf('f(f(' + chk.inner + '))') >= 0; })) return { status: 'invalid', msg: 'f(f(' + chk.inner + ')) is not asked.' };
          if (!calls.length || !calls[0].eq(inner) || !calls[calls.length - 1].eq(at)) return { status: 'mismatch', msg: 'The inputs in the answer are wrong.' };
        } else if (calls.length && !calls[calls.length - 1].eq(at)) return { status: 'mismatch', msg: 'The answer is for a different input.' };
        return answerNumbers(ans).some(function (q) { return q.eq(ys2[0]); }) ? { status: 'verified', computed: qText(ys2[0]) } : { status: 'mismatch', msg: 'Correct: ' + ys2[0] + '.', computed: qText(ys2[0]) };
      }
      // want === 'inputs': every x with f(x) = k
      var k = qStr(chk.k), xs2 = [];
      if (rel2.kind === 'discrete') xs2 = rel2.pairs.filter(function (pr) { return pr[1].eq(k); }).map(function (pr) { return pr[0]; });
      else rel2.segs.forEach(function (sg) {
        var y1 = sg.a[1], y2 = sg.b[1]; if (y1.eq(y2)) { if (y1.eq(k)) xs2.push(null); return; }
        var tt = k.sub(y1).div(y2.sub(y1)), inA = sg.aEnd !== 'open', inB = sg.bEnd !== 'open';
        if ((C.cmpQ(tt, Q.ZERO) > 0 || (tt.isZero() && inA) || sg.aEnd === 'arrow' && C.cmpQ(tt, Q.ZERO) < 0) && (C.cmpQ(tt, Q.ONE) < 0 || (tt.eq(Q.ONE) && inB) || sg.bEnd === 'arrow' && C.cmpQ(tt, Q.ONE) > 0)) xs2.push(sg.a[0].add(sg.b[0].sub(sg.a[0]).mul(tt)));
      });
      if (xs2.some(function (x) { return x === null; }) || !xs2.length) return { status: 'invalid', msg: 'No single set of inputs for this output.' };
      xs2 = uniqQ(xs2);
      var got3 = uniqQ(answerNumbers(ans));
      return sameList(got3, xs2) ? { status: 'verified', computed: xs2.join(', ') } : { status: 'mismatch', msg: 'Correct x: ' + xs2.join(', ') + '.' };
    }
    if (t === 'linear-rule') {
      var rel3 = relationOf(p, chk), pts;
      if (rel3.kind === 'discrete') pts = rel3.pairs; else { pts = []; rel3.segs.forEach(function (sg) { pts.push(sg.a, sg.b); }); }
      var linear = true, m0 = null;
      for (var j = 1; j < pts.length; j++) { var dx = pts[j][0].sub(pts[0][0]); if (dx.isZero()) { linear = false; break; } var m1 = pts[j][1].sub(pts[0][1]).div(dx); if (m0 && !m1.eq(m0)) linear = false; m0 = m0 || m1; }
      if (!linear) {
        if (!/not linear|no/.test(txt)) return { status: 'mismatch', msg: 'The data are not linear.' };
        var lists = C.snippets(ans).filter(function (z) { return /,/.test(z); });
        if (lists.length) { var diffs = pts.slice(1).map(function (pt, i) { return pt[1].sub(pts[i][1]); }); if (!sameList(listNumbers('⟨' + lists[0] + '⟩'), diffs)) return { status: 'mismatch', msg: 'The listed changes are wrong: ' + diffs.join(', ') + '.' }; }
        return { status: 'verified', computed: 'Not linear' };
      }
      if (chk.predict !== undefined) {
        if (!shown(p, 'x=' + chk.predict)) return { status: 'invalid', msg: 'The input is not printed.' };
        var Xp = qStr(chk.predict), Yp = pts[0][1].add(m0.mul(Xp.sub(pts[0][0]))), gp = listNumbers(ans);
        return gp.length === 1 && gp[0].eq(Yp) ? { status: 'verified', computed: qText(Yp) } : { status: 'mismatch', msg: 'Correct: y = ' + Yp + '.' };
      }
      var rhs = lastEq(ans); if (rhs === null) return { status: 'mismatch', msg: 'Write the rule.' };
      var fn = C.toRF(C.parseExpr(rhs)); if (!fn.isPoly() || fn.asPoly().degreeIn('x') > 1) return { status: 'mismatch', msg: 'The rule must be linear in x.' };
      var okAll = pts.every(function (pt) { return fn.asPoly().evalAt({ x: pt[0] }).eq(pt[1]); });
      var form = C.simplifiedForm(rhs);
      return okAll && form.ok ? { status: 'verified' } : { status: 'mismatch', msg: okAll ? 'Simplify the rule.' : 'The rule does not fit every point.' };
    }
    if (t === 'table-fill') {
      if (!shown(p, chk.rule)) return { status: 'invalid', msg: 'The rule is not printed.' };
      var rows = NS.fig.readTable(NS.fig.table(p.fig)), rhsN = ruleRHS(chk.rule), v = chk.v || 'x', need = [];
      rows.forEach(function (r) {
        if (r[1] === '?' && r[0] !== '?') { var e2 = {}; e2[v] = qStr(r[0]); need.push(C.evalNode(rhsN, e2)); }
        else if (r[0] === '?' && r[1] !== '?') { var sol = C.solveLinear({ lhs: rhsN, rhs: C.parseExpr(r[1]), rel: '=' }, v); if (sol.kind !== 'one') throw new C.CheckError('missing input not unique'); need.push(sol.value); }
      });
      if (!need.length) return { status: 'invalid', msg: 'Nothing to fill in.' };
      if (policy && policy.intOnly && need.some(function (q) { return !q.isInt(); })) return { status: 'invalid', msg: 'Non-integer entry.' };
      var got4 = answerNumbers(ans);
      return sameList(got4, need) ? { status: 'verified', computed: need.join(', ') } : { status: 'mismatch', msg: 'Correct entries: ' + need.join(', ') + '.' };
    }
    if (t === 'rate') {
      var x1, y1, x2, y2;
      if (chk.rule) {
        if (!shown(p, chk.rule)) return { status: 'invalid', msg: 'The rule is not printed.' };
        var rr = ruleRHS(chk.rule), va = chk.v || 'x'; x1 = qStr(chk.from); x2 = qStr(chk.to);
        var e3 = {}; e3[va] = x1; y1 = C.evalNode(rr, e3); e3[va] = x2; y2 = C.evalNode(rr, e3);
      } else if (chk.words) {
        var nums = C.numbersInText(p.prompt); x1 = nums[chk.words[0]]; y1 = nums[chk.words[1]]; x2 = nums[chk.words[2]]; y2 = nums[chk.words[3]];
      } else {
        var rel4 = relationOf(p, chk);
        if (rel4.kind === 'discrete') {
          var A = chk.from !== undefined ? rel4.pairs.filter(function (pr) { return pr[0].eq(qStr(chk.from)); })[0] : rel4.pairs[0];
          var B = chk.to !== undefined ? rel4.pairs.filter(function (pr) { return pr[0].eq(qStr(chk.to)); })[0] : rel4.pairs[rel4.pairs.length - 1];
          if (!A || !B) return { status: 'invalid', msg: 'Interval endpoints are not in the data.' };
          if (chk.constant) { for (var q = 2; q < rel4.pairs.length; q++) { var s0 = rel4.pairs[1][1].sub(rel4.pairs[0][1]).div(rel4.pairs[1][0].sub(rel4.pairs[0][0])), sq = rel4.pairs[q][1].sub(rel4.pairs[q - 1][1]).div(rel4.pairs[q][0].sub(rel4.pairs[q - 1][0])); if (!sq.eq(s0)) return { status: 'invalid', msg: 'The rate is not constant.' }; } }
          x1 = A[0]; y1 = A[1]; x2 = B[0]; y2 = B[1];
        } else { var sg = rel4.segs[0]; x1 = sg.a[0]; y1 = sg.a[1]; x2 = sg.b[0]; y2 = sg.b[1]; }
      }
      var rate = y2.sub(y1).div(x2.sub(x1));
      if (chk.from !== undefined && !chk.words) {
        var fT = chk.from, tT = chk.to, pr2 = C.snippets(studentText(p)).map(norm);
        if (!(pr2.indexOf(norm('x=' + fT)) >= 0 && pr2.indexOf(norm('x=' + tT)) >= 0) && !pr2.some(function (z) { return z.indexOf(norm(fT + '\\le x\\le ' + tT)) >= 0; })) return { status: 'invalid', msg: 'The interval is not printed.' };
      }
      if (chk.words) { var ex2 = C.numbersInText(ans); if (!ex2.every(function (q2) { return q2.eq(rate) || q2.eq(rate.neg()); })) return { status: 'mismatch', msg: 'The explanation uses the wrong rate.' }; }
      if (chk.intervals) {
        var rel6 = relationOf(p, chk), pr3 = C.snippets(studentText(p)).map(norm), rates = chk.intervals.map(function (iv) {
          if (pr3.indexOf(norm(iv[0] + '\\le x\\le ' + iv[1])) < 0) throw new C.CheckError('interval not printed');
          var a2 = rel6.pairs.filter(function (q3) { return q3[0].eq(qStr(iv[0])); })[0], b2 = rel6.pairs.filter(function (q3) { return q3[0].eq(qStr(iv[1])); })[0];
          if (!a2 || !b2) throw new C.CheckError('interval endpoints not in the table');
          return b2[1].sub(a2[1]).div(b2[0].sub(a2[0]));
        });
        var big = C.cmpQ(rates[0], rates[1]) > 0 ? 'first' : C.cmpQ(rates[0], rates[1]) < 0 ? 'second' : 'same', gotR = listNumbers(ans);
        return txt.indexOf(big) >= 0 && gotR.length === 2 && gotR[0].eq(rates[0]) && gotR[1].eq(rates[1]) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: the ' + big + ' interval (' + rates.join(' vs. ') + ').' };
      }
      if (policy && policy.intOnly && !rate.isInt()) return { status: 'invalid', msg: 'The rate is not a whole number.' };
      var got5 = answerNumbers(ans);
      if (chk.compare) { var other = qStr(chk.compare); var bigger = C.cmpQ(rate, other) > 0 ? 'first' : C.cmpQ(rate, other) < 0 ? 'second' : 'same'; return txt.indexOf(bigger) >= 0 ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: ' + bigger + '.' }; }
      return got5.length && got5[0].eq(rate) ? { status: 'verified', computed: qText(rate) } : { status: 'mismatch', msg: 'Correct rate: ' + rate + '.', computed: qText(rate) };
    }
    if (t === 'curve-behavior') {   // monotone runs and turning points read from the drawn curve
      var relC = relationOf(p, chk); if (!relC.curves || relC.curves.length !== 1) throw new C.CheckError('need one curve');
      var cv = relC.curves[0].slice().sort(function (a, b) { return C.cmpQ(a[0], b[0]); }), runs = [], dir = 0, start = cv[0];
      for (var i = 1; i < cv.length; i++) { var dd = C.cmpQ(cv[i][1], cv[i - 1][1]); if (dd === 0) throw new C.CheckError('flat piece'); if (dir && dd !== dir) { runs.push({ lo: start[0], hi: cv[i - 1][0], up: dir > 0, end: cv[i - 1] }); start = cv[i - 1]; } dir = dd; }
      runs.push({ lo: start[0], hi: cv[cv.length - 1][0], up: dir > 0, end: cv[cv.length - 1] });
      var dom = C.snippets(studentText(p)).map(function (s4) { return /^(-?\d+)\\lex\\le(-?\d+)$/.exec(s4.replace(/\s/g, '')); }).filter(Boolean)[0];
      if (!dom || !new Q(BigInt(dom[1])).eq(cv[0][0]) || !new Q(BigInt(dom[2])).eq(cv[cv.length - 1][0])) return { status: 'invalid', msg: 'The printed domain is not the drawn curve.' };
      if (chk.want === 'extreme') {
        var tps = runs.slice(0, -1).map(function (rn) { return { x: rn.end[0], y: rn.end[1], kind: rn.up ? 'max' : 'min' }; });
        var tx = C.plainText(ans).toLowerCase(), sn = C.snippets(ans), okE = tps.length && tps.every(function (tp) {
          return sn.some(function (s, j) { var m1 = /^y=(.*)$/.exec(s.replace(/\s/g, '')); var m2 = sn[j + 1] && /^x=(.*)$/.exec(sn[j + 1].replace(/\s/g, '')); return m1 && m2 && C.readNumber(m1[1]).eq(tp.y) && C.readNumber(m2[1]).eq(tp.x); });
        }) && sn.length === 2 * tps.length && tps.every(function (tp) { return tx.indexOf(tp.kind === 'max' ? 'maximum' : 'minimum') >= 0; });
        return okE ? { status: 'verified' } : { status: 'mismatch', msg: tps.map(function (tp) { return tp.kind + ' ' + qText(tp.y) + ' at x = ' + qText(tp.x); }).join('; ') + '.' };
      }
      var wantC = runs.filter(function (rn) { return rn.up === (chk.want === 'increasing'); }).reduce(function (acc, rn) { return unionSets(acc, C.solutionSet(qText(rn.lo) + '<x<' + qText(rn.hi), 'x')); }, []);
      var piecesC = []; C.snippets(ans).forEach(function (s3) { s3.split(/\s+and\s+|\\text\{\s*and\s*\}|,/).forEach(function (x) { if (x.trim()) piecesC.push(x.trim()); }); });
      var gotC = /none|never/.test(txt) && !piecesC.length ? [] : piecesC.map(function (s3) { return C.solutionSet(s3, 'x'); }).reduce(function (acc, st) { return unionSets(acc, st); }, []);
      return C.setEqual(gotC, wantC) ? { status: 'verified', computed: C.setText(wantC) } : { status: 'mismatch', msg: 'Correct: ' + (wantC.length ? C.setText(wantC) : 'none') + '.' };
    }
    if (t === 'graph-behavior') {
      var rel5 = relationOf(p, chk), conds = [];
      rel5.segs.forEach(function (sg) {
        var dx = sg.b[0].sub(sg.a[0]), dy = sg.b[1].sub(sg.a[1]); if (dx.isZero()) return;
        var sl = dy.div(dx), kind = sl.isZero() ? 'constant' : C.cmpQ(sl, Q.ZERO) > 0 ? 'increasing' : 'decreasing';
        if (kind !== chk.want) return;
        var lo = C.cmpQ(sg.a[0], sg.b[0]) < 0 ? sg.a[0] : sg.b[0], hi = C.cmpQ(sg.a[0], sg.b[0]) < 0 ? sg.b[0] : sg.a[0];
        conds.push(C.solutionSet(qText(lo) + '<x<' + qText(hi), 'x'));
      });
      var want2 = conds.reduce(function (acc, st) { return unionSets(acc, st); }, []);
      var got6 = /none|never/.test(txt) && !C.snippets(ans).length ? [] : C.snippets(ans).map(function (s3) { return C.solutionSet(s3, 'x'); }).reduce(function (acc, st) { return unionSets(acc, st); }, []);
      return C.setEqual(got6, want2) ? { status: 'verified', computed: C.setText(want2) } : { status: 'mismatch', msg: 'Correct: ' + (want2.length ? C.setText(want2) : 'none') + '.' };
    }
    if (t === 'sequence') {
      var terms, geoWord = /geometric/.test(C.plainText(p.prompt).toLowerCase());
      if (chk.terms) { if (!shown(p, chk.terms)) return { status: 'invalid', msg: 'The terms are not printed.' }; terms = chk.terms.replace(/\\dots|\\ldots|\.\.\./g, '').replace(/\\[ ,;!]/g, ' ').split(',').map(function (x) { return x.trim(); }).filter(Boolean).map(function (x) { return C.evalNode(C.parseExpr(x), {}); }); }
      else { // two given terms "a_3=11" and "a_7=27"
        var g1 = chk.given[0], g2 = chk.given[1]; if (!shown(p, g1.tex) || !shown(p, g2.tex)) return { status: 'invalid', msg: 'The given terms are not printed.' };
        var v1 = qStr(g1.val), v2 = qStr(g2.val), gap = g2.n - g1.n;
        if (geoWord) {
          if (gap % 2 === 0) return { status: 'invalid', msg: 'An even gap leaves two possible ratios.' };
          var rq = v2.div(v1), negR = C.cmpQ(rq, Q.ZERO) < 0, root = qpowRoot(negR ? rq.neg() : rq, gap); if (!root) return { status: 'invalid', msg: 'The ratio is not rational.' };
          var rr = negR ? root.neg() : root, a1g = v1.div(rr.pow(g1.n - 1)); terms = [a1g, a1g.mul(rr), a1g.mul(rr).mul(rr)];
        } else { var dd = v2.sub(v1).div(new Q(gap)); var a1 = v1.sub(dd.mul(new Q(g1.n - 1))); terms = [a1, a1.add(dd), a1.add(dd.mul(new Q(2)))]; }
      }
      var d = terms[1].sub(terms[0]), arith = terms.every(function (q, j) { return !j || q.sub(terms[j - 1]).eq(d); });
      var ratio = terms[0].isZero() ? null : terms[1].div(terms[0]);
      var geo = !arith && !!ratio && terms.every(function (q, j) { return !j || (!terms[j - 1].isZero() && q.div(terms[j - 1]).eq(ratio)); });
      if (!arith && !geo) return { status: 'invalid', msg: 'The sequence is neither arithmetic nor geometric.' };
      if (geoWord && !geo) return { status: 'invalid', msg: 'The problem says geometric but the terms are not.' };
      var term = function (n) { return arith ? terms[0].add(d.mul(new Q(n - 1))) : terms[0].mul(ratio.pow(n - 1)); };
      var nums2 = (chk.want === 'formula' || chk.want === 'recursive') ? [] : listNumbers(ans);
      if (chk.want === 'recursive') {
        var rs = C.snippets(ans).join(',').replace(/\\[ ,;!]/g, '').replace(/\s/g, '');
        var mr = /a_\{?1\}?=(-?[\d.\/]+),a_\{?n\}?=(.+)$/.exec(rs);
        if (!mr || !qStr(mr[1]).eq(terms[0])) return { status: 'mismatch', msg: 'Write a_1 = ' + terms[0] + ' and the rule for a_n.' };
        var rhsR = mr[2].replace(/a_\{n-1\}/g, 'p'), okR = true;
        for (var nr = 2; nr <= 6; nr++) { try { if (!C.evalNode(C.parseExpr(rhsR), { p: term(nr - 1) }).eq(term(nr))) okR = false; } catch (e) { okR = false; } }
        return okR ? { status: 'verified' } : { status: 'mismatch', msg: arith ? 'a_n = a_{n-1} + ' + d + '.' : 'a_n = ' + ratio + '·a_{n-1}.' };
      }
      if (chk.want === 'next') { var nx = [term(terms.length + 1), term(terms.length + 2)]; return sameList(nums2.slice(0, 2), nx) ? { status: 'verified' } : { status: 'mismatch', msg: 'Next terms: ' + nx.join(', ') + '.' }; }
      if (chk.want === 'd') return nums2.some(function (q) { return q.eq(arith ? d : ratio); }) ? { status: 'verified' } : { status: 'mismatch', msg: (arith ? 'd = ' + d : 'r = ' + ratio) + '.' };
      if (chk.want === 'nth') { var sub = /a_\{?(-?\d+)\}?=/.exec(norm(C.snippets(ans).join(' '))); if (sub && +sub[1] !== chk.n) return { status: 'mismatch', msg: 'Wrong term number.' }; }
      if (chk.want === 'nth') return nums2.length && nums2[nums2.length - 1].eq(term(chk.n)) ? { status: 'verified' } : { status: 'mismatch', msg: 'Term ' + chk.n + ' is ' + term(chk.n) + '.' };
      if (chk.want === 'which') {
        var target = qStr(chk.value), nn = null;
        if (arith) { var nq = target.sub(terms[0]).div(d).add(Q.ONE); if (nq.isInt() && nq.n > 0n) nn = nq; }
        else for (var k2 = 1; k2 <= 80; k2++) if (term(k2).eq(target)) { nn = new Q(k2); break; }
        var isTerm = nn !== null;
        if (chk.yesno) { var sy = /^\s*yes/.test(txt); return sy === isTerm && (!isTerm || nums2.some(function (q) { return q.eq(nn); })) ? { status: 'verified' } : { status: 'mismatch', msg: isTerm ? 'Yes, term ' + nn + '.' : 'No.' }; }
        if (!isTerm) return { status: 'invalid', msg: 'That value is not a term.' };
        return nums2.some(function (q) { return q.eq(nn); }) ? { status: 'verified' } : { status: 'mismatch', msg: 'It is term ' + nn + '.' };
      }
      if (chk.want === 'formula') {
        var f2 = lastEq(ans); if (f2 === null) return { status: 'mismatch', msg: 'Write the formula.' };
        var ex = C.parseExpr(f2.replace(/a_\{?n\}?/g, 'n'));
        for (var nn2 = 1; nn2 <= 6; nn2++) { var gv; try { gv = C.evalNode(ex, { n: new Q(nn2) }); } catch (e) { return { status: 'mismatch', msg: 'Could not read the formula.' }; } if (!gv.eq(term(nn2))) return { status: 'mismatch', msg: 'The formula does not give the terms (a_' + nn2 + ' = ' + term(nn2) + ').' }; }
        return { status: 'verified' };
      }
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }


  /* ---------------- exponential functions ---------------- */
  /* ---------- compound interest (re-read from the words and numbers printed) ---------- */
  var PERIODS = { annually: 1, semiannually: 2, quarterly: 4, monthly: 12, daily: 365 };
  function balance(P, rate, how, t) { if (how === 'continuously') return P * Math.exp(rate / 100 * t); if (!PERIODS[how]) throw new C.CheckError('unknown compounding ' + how); return P * Math.pow(1 + rate / 100 / PERIODS[how], PERIODS[how] * t); }
  function moneyIn(s) { return +String(s).replace(/,/g, ''); }
  function checkCompound(p, part) {
    var chk = part.check, ans = part.answer || '', txt = C.plainText(p.prompt).replace(/\s+/g, ' '), M0 = '\\$([\\d,]+(?:\\.\\d+)?)', R0 = '(\\d+(?:\\.\\d+)?)%';
    var got = C.numbersInText(ans); if (!got.length) return { status: 'mismatch', msg: 'No amount in the answer.' };
    var cents = function (x) { return Math.round(x * 100); }, gotC = Math.round(Number(got[0].n) * 100 / Number(got[0].d));
    if (chk.want === 'compare') {
      var m = new RegExp('Account A pays ' + R0 + ' interest compounded (\\w+)\\. Account B pays ' + R0 + ' interest compounded (\\w+)\\. \\w+ deposits ' + M0 + ' in one of them for (\\d+) years').exec(txt);
      if (!m) throw new C.CheckError('could not read the two accounts');
      var P = moneyIn(m[5]), t = +m[6], a = cents(balance(P, +m[1], m[2], t)), b = cents(balance(P, +m[3], m[4], t)), win = a > b ? 'A' : 'B', d = Math.abs(a - b);
      if (a === b) return { status: 'invalid', msg: 'The accounts give the same amount.' };
      var said = /account\s*([ab])\b/i.exec(C.plainText(ans));
      if (!said || said[1].toUpperCase() !== win) return { status: 'mismatch', msg: 'Account ' + win + ' gives more.' };
      return gotC === d ? { status: 'verified', computed: 'Account ' + win + ', ' + (d / 100).toFixed(2) } : { status: 'mismatch', msg: 'Difference: $' + (d / 100).toFixed(2) + '.' };
    }
    var m2 = new RegExp('deposits ' + M0 + ' in an account that pays ' + R0 + ' interest compounded (\\w+)\\. (How much interest does the account earn in|How much is in the account after) (\\d+) years').exec(txt);
    if (!m2) throw new C.CheckError('could not read the account');
    if (!/Round to the nearest cent/.test(txt)) return { status: 'invalid', msg: 'The problem must say how to round.' };
    var P2 = moneyIn(m2[1]), A = balance(P2, +m2[2], m2[3], +m2[5]), interest = /interest does/.test(m2[4]);
    if ((chk.want === 'interest') !== interest) return { status: 'invalid', msg: 'The question asks for something else.' };
    var want = cents(A) - (interest ? Math.round(P2 * 100) : 0);
    return gotC === want ? { status: 'verified', computed: (want / 100).toFixed(2) } : { status: 'mismatch', msg: 'Correct: $' + (want / 100).toFixed(2) + '.' };
  }
  var EXP_TYPES = ['exp-identify', 'exp-features', 'exp-model', 'exp-rule', 'exp-solve', 'exp-apply'];
  function qf(q) { return Number(q.n) / Number(q.d); }
  function ruleFn(rule, v) { var rhs = ruleRHS(rule); return function (x) { var e = {}; e[v] = x instanceof Q ? x : new Q(x); return C.evalNode(rhs, e); }; }
  function hasVarExponent(node, v) { if (!node || typeof node !== 'object') return false; if (node.k === 'xpow' && C.varsOf(node.b)[v]) return true; return hasVarExponent(node.a, v) || hasVarExponent(node.b, v); }
  /* f(x) = a·b^x + k, read back by evaluating the printed rule (and confirmed at two more points) */
  function expParams(rule, v) {
    var f = ruleFn(rule, v || 'x'), f0 = f(0), f1 = f(1), f2 = f(2), den = f0.add(f2).sub(f1.mul(new Q(2)));
    if (den.isZero()) throw new C.CheckError('the rule is not exponential');
    var k = f0.mul(f2).sub(f1.mul(f1)).div(den), a = f0.sub(k);
    if (a.isZero()) throw new C.CheckError('the rule is constant');
    var b = f1.sub(k).div(a);
    if (C.cmpQ(b, Q.ZERO) <= 0 || b.eq(Q.ONE)) throw new C.CheckError('not an exponential base');
    [3, -1, -2].forEach(function (x) { if (!f(x).eq(a.mul(b.pow(x)).add(k))) throw new C.CheckError('the rule is not of the form a·b^x + k'); });
    return { a: a, b: b, k: k };
  }
  function firstWord(txt) { return (/^\s*([a-z]+)/.exec(txt) || [])[1] || ''; }
  function pctOf(q) { return q.sub(Q.ONE).mul(new Q(100)); }
  function checkExpPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, txt = C.plainText(ans).toLowerCase(), v = chk.v || 'x';
    if (chk.rule && !shown(p, chk.rule)) return { status: 'invalid', msg: 'The rule is not printed.' };
    if (t === 'exp-identify' || t === 'exp-features') {
      var E = expParams(chk.rule, v), want = chk.want, growth = C.cmpQ(E.b, Q.ONE) > 0;
      if (t === 'exp-identify' && !E.k.isZero()) return { status: 'invalid', msg: 'Use a rule of the form a·b^x.' };
      if (p.fig && p.fig.kind === 'plane') {   // a drawn graph must be the graph of the printed rule
        var gr = NS.fig.readPlane(NS.fig.plane(p.fig), true), fx = ruleFn(chk.rule, v), offGraph = false, near = function (x, y) { var xi = Math.round(x); return Math.abs(x - xi) > 0.01 || Math.abs(qf(fx(xi)) - y) < 0.05; };
        gr.points.forEach(function (pt) { if (!near(pt.x, pt.y)) offGraph = true; });
        gr.curves.forEach(function (cv) { cv.forEach(function (pt) { if (!near(pt[0], pt[1])) offGraph = true; }); if (cv.length < 4) offGraph = true; });
        if (offGraph) return { status: 'invalid', msg: 'The drawn graph does not match the rule.' };
      }
      if (want === 'kind') { var w = growth ? 'growth' : 'decay', bs = C.snippets(ans);
        if (bs.some(function (sn) { try { return !C.evalNode(C.parseExpr(sn), {}).eq(E.b); } catch (e) { return true; } })) return { status: 'mismatch', msg: 'The base is ' + E.b + '.' };
        return firstWord(txt) === w ? { status: 'verified', computed: w } : { status: 'mismatch', msg: 'Correct: ' + w + '.' }; }
      if (want === 'initial') return lastNum(ans, E.a) ? { status: 'verified', computed: qText(E.a) } : { status: 'mismatch', msg: 'Initial value: ' + E.a + '.' };
      if (want === 'factor') return lastNum(ans, E.b) ? { status: 'verified', computed: qText(E.b) } : { status: 'mismatch', msg: 'Factor: ' + E.b + '.' };
      if (want === 'rate') { var r = pctOf(E.b); if (C.cmpQ(r, Q.ZERO) < 0) r = r.neg(); var nums = C.numbersInText(ans); var w2 = growth ? 'growth' : 'decay';
        return nums.length && nums[0].eq(r) && (txt.indexOf(w2) >= 0 || txt.indexOf(growth ? 'increase' : 'decrease') >= 0) ? { status: 'verified', computed: qText(r) + '%' } : { status: 'mismatch', msg: 'Rate: ' + r + '% ' + w2 + '.' }; }
      if (want === 'intercept') { var y0 = E.a.add(E.k), pr = pairsFrom(C.snippets(ans).join(' ')); var okI = pr.length ? pr[0][0].isZero() && pr[0][1].eq(y0) : lastNum(ans, y0);
        return okI ? { status: 'verified', computed: '(0, ' + y0 + ')' } : { status: 'mismatch', msg: 'y-intercept: (0, ' + y0 + ').' }; }
      if (want === 'asymptote') { var le = lastEq(ans); var okA = le !== null && /y\s*=/.test(C.snippets(ans).join('')) && C.evalNode(C.parseExpr(le), {}).eq(E.k);
        return okA ? { status: 'verified', computed: 'y=' + qText(E.k) } : { status: 'mismatch', msg: 'Asymptote: y = ' + E.k + '.' }; }
      if (want === 'domain') return /all real/.test(txt) ? { status: 'verified' } : { status: 'mismatch', msg: 'Domain: all real numbers.' };
      if (want === 'range') { var rng = C.solutionSet('y' + (C.cmpQ(E.a, Q.ZERO) > 0 ? '>' : '<') + qText(E.k), 'y'), got; try { got = C.setFromAnswer(ans, 'y'); } catch (e) { return { status: 'mismatch', msg: 'Write the range as an inequality in y.' }; }
        return C.setEqual(got, rng) ? { status: 'verified', computed: C.setText(rng, 'y') } : { status: 'mismatch', msg: 'Range: ' + C.setText(rng, 'y') + '.' }; }
      if (want === 'behavior') { var inc = (C.cmpQ(E.a, Q.ZERO) > 0) === growth, w3 = inc ? 'increasing' : 'decreasing'; return firstWord(txt) === w3 ? { status: 'verified', computed: w3 } : { status: 'mismatch', msg: 'Correct: ' + w3 + '.' }; }
      throw new C.CheckError('unknown want ' + want);
    }
    if (t === 'exp-model') {
      var rel = relationOf(p, chk), pts = rel.pairs; if (!pts || pts.length < 3) return { status: 'invalid', msg: 'Need at least three points.' };
      var dx = pts[1][0].sub(pts[0][0]); for (var i = 2; i < pts.length; i++) if (!pts[i][0].sub(pts[i - 1][0]).eq(dx)) return { status: 'invalid', msg: 'The x-values must be equally spaced.' };
      var d = pts[1][1].sub(pts[0][1]), lin = pts.every(function (q, j) { return !j || q[1].sub(pts[j - 1][1]).eq(d); });
      var ratio = pts.every(function (q) { return !q[1].isZero(); }) ? pts[1][1].div(pts[0][1]) : null, ex = !!ratio && !ratio.eq(Q.ONE) && pts.every(function (q, j) { return !j || q[1].div(pts[j - 1][1]).eq(ratio); });
      var kind = lin ? 'linear' : ex ? 'exponential' : 'neither', fw = firstWord(txt);
      if (fw !== kind) return { status: 'mismatch', msg: 'Correct: ' + kind + '.' };
      var sn = C.snippets(ans); if (kind !== 'neither' && sn.length) { var nq = C.evalNode(C.parseExpr(lastEq(ans) || sn[0]), {}); if (!nq.eq(kind === 'linear' ? d : ratio)) return { status: 'mismatch', msg: 'The explanation uses the wrong ' + (kind === 'linear' ? 'difference' : 'factor') + '.' }; }
      return { status: 'verified', computed: kind };
    }
    if (t === 'exp-rule') {
      var rel2 = chk.pairs ? relationOf(p, chk) : relationOf(p, chk), pts2 = rel2.kind === 'discrete' ? rel2.pairs : rel2.points.map(function (q) { return [qOf(q.x), qOf(q.y)]; });
      if (chk.predict !== undefined) {   // the value of the exponential through the points at another x
        if (!shown(p, v + '=' + chk.predict)) return { status: 'invalid', msg: 'The input is not printed.' };
        var P1 = pts2[0], P2 = pts2[pts2.length - 1], gapE = Number(P2[0].sub(P1[0]).n), ratE = P2[1].div(P1[1]);
        if (C.cmpQ(ratE, Q.ZERO) <= 0) return { status: 'invalid', msg: 'Not an exponential.' };
        var bE = qpowRoot(ratE, gapE); if (!bE) return { status: 'invalid', msg: 'The factor is not rational.' };
        var aE = P1[1].div(qpowFn(bE, P1[0])); if (!pts2.every(function (q) { return aE.mul(qpowFn(bE, q[0])).eq(q[1]); })) return { status: 'invalid', msg: 'The points are not on one exponential.' };
        var want4 = aE.mul(qpowFn(bE, qStr(chk.predict))), g4 = listNumbers(ans);
        if (policy && policy.intOnly && !want4.isInt()) return { status: 'invalid', msg: 'Not a whole number.' };
        return g4.length && g4[g4.length - 1].eq(want4) ? { status: 'verified', computed: qText(want4) } : { status: 'mismatch', msg: 'Correct: ' + want4 + '.' };
      }
      var rr = lastEq(ans); if (rr === null) return { status: 'mismatch', msg: 'Write the rule.' };
      var node = C.parseExpr(rr); if (!hasVarExponent(node, v)) return { status: 'mismatch', msg: 'The rule should be exponential (the variable in the exponent).' };
      var fits = pts2.every(function (q) { var e = {}; e[v] = q[0]; try { return C.evalNode(node, e).eq(q[1]); } catch (er) { return false; } });
      if (!fits) return { status: 'mismatch', msg: 'The rule does not fit every point.' };
      if (pts2.length < 2) return { status: 'invalid', msg: 'Need two points.' };
      return { status: 'verified' };
    }
    if (t === 'exp-solve') {
      if (!shown(p, chk.eq)) return { status: 'invalid', msg: 'The equation is not printed.' };
      var R = C.parseRelation(chk.eq), env = function (x) { var e = {}; e[v] = new Q(x); return e; };
      // both sides are c·b^(linear): their logarithms are linear in x, so there is at most one solution
      function logLin(side) { var h = [0, 1, 2, 3].map(function (x) { var val = qf(C.evalNode(side, env(x))); if (!(val > 0)) throw new C.CheckError('a side is not positive'); return Math.log(val); });
        var m = h[1] - h[0]; if (Math.abs(h[2] - h[1] - m) > 1e-9 || Math.abs(h[3] - h[2] - m) > 1e-9) throw new C.CheckError('not an exponential equation'); return { m: m, c: h[0] }; }
      var L = logLin(R.lhs), Rr = logLin(R.rhs);
      if (Math.abs(L.m - Rr.m) < 1e-12) return { status: 'invalid', msg: Math.abs(L.c - Rr.c) < 1e-12 ? 'Every number is a solution.' : 'No solution.' };
      var xs = (Rr.c - L.c) / (L.m - Rr.m), got = listNumbers(ans);
      if (got.length !== 1) return { status: 'mismatch', msg: 'Give one value.' };
      var e1 = {}; e1[v] = got[0]; var exact; try { exact = C.evalNode(R.lhs, e1).eq(C.evalNode(R.rhs, e1)); } catch (er) { exact = false; }
      if (policy && policy.intOnly && Math.abs(xs - Math.round(xs)) > 1e-9) return { status: 'invalid', msg: 'Not a whole-number solution.' };
      return exact && Math.abs(qf(got[0]) - xs) < 1e-9 ? { status: 'verified', computed: v + '=' + qText(got[0]) } : { status: 'mismatch', msg: 'Correct: ' + v + ' ≈ ' + (Math.round(xs * 1e6) / 1e6) + '.' };
    }
    if (t === 'exp-apply') {
      var pr2 = C.plainText(studentText(p)).toLowerCase(), nums2 = C.numbersInText(studentText(p)), at = function (i) { if (nums2[i] === undefined) throw new C.CheckError('missing number ' + i); return nums2[i]; };
      var start = at(chk.start), factor;
      if (chk.pct !== undefined) { var pc = at(chk.pct).div(new Q(100)), up = /(increas|grow|earn|interest|rise|gain)/.test(pr2), down = /(decreas|los|decay|depreciat|drop|declin)/.test(pr2);
        if (up === down) throw new C.CheckError('cannot tell growth from decay'); factor = up ? Q.ONE.add(pc) : Q.ONE.sub(pc); }
      else { var kw = /\b(doubles|triples|quadruples|halves|half)\b/.exec(pr2); if (!kw) throw new C.CheckError('no growth word'); factor = { doubles: new Q(2), triples: new Q(3), quadruples: new Q(4), halves: new Q(1, 2), half: new Q(1, 2) }[kw[1]]; }
      var every = chk.every !== undefined ? at(chk.every) : Q.ONE;
      var valueAt = function (tq) { var n = tq.div(every); if (!n.isInt()) throw new C.CheckError('time is not a whole number of periods'); return start.mul(factor.pow(Number(n.n))); };
      if (chk.want === 'value') {
        var val2 = valueAt(at(chk.time)), g = listNumbers(ans.replace(/\$/g, '')), gv = g[g.length - 1];
        if (!gv) return { status: 'mismatch', msg: 'No value.' };
        if (chk.round !== undefined) {
          var phrase = chk.round === 2 ? /nearest cent|nearest hundredth/ : chk.round === 1 ? /nearest tenth/ : /nearest whole/;
          if (!phrase.test(pr2)) return { status: 'invalid', msg: 'The problem must say how to round.' };
          var scale = Math.pow(10, chk.round), want2 = Math.round(qf(val2) * scale) / scale;
          return Math.abs(qf(gv) - want2) < 1e-9 ? { status: 'verified', computed: String(want2) } : { status: 'mismatch', msg: 'Correct: ' + want2 + '.' };
        }
        return gv.eq(val2) ? { status: 'verified', computed: qText(val2) } : { status: 'mismatch', msg: 'Correct: ' + val2 + '.' };
      }
      if (chk.want === 'rule') {
        var rr2 = lastEq(ans); if (rr2 === null) return { status: 'mismatch', msg: 'Write the function.' };
        var nd = C.parseExpr(rr2); if (!hasVarExponent(nd, v)) return { status: 'mismatch', msg: 'The function should be exponential.' };
        for (var j2 = 0; j2 <= 3; j2++) { var tt = every.mul(new Q(j2)), e2 = {}; e2[v] = tt; var gotv; try { gotv = C.evalNode(nd, e2); } catch (er) { return { status: 'mismatch', msg: 'Could not evaluate the function.' }; } if (!gotv.eq(valueAt(tt))) return { status: 'mismatch', msg: 'The function gives the wrong value at ' + v + ' = ' + tt + '.' }; }
        return { status: 'verified' };
      }
      if (chk.want === 'when') {
        var th = at(chk.threshold), above = C.cmpQ(factor, Q.ONE) > 0, n0 = null;
        for (var tw = 0; tw <= 200; tw++) { var vv = start.mul(factor.pow(tw)); if (above ? C.cmpQ(vv, th) > 0 : C.cmpQ(vv, th) < 0) { n0 = tw; break; } }
        if (n0 === null || !every.eq(Q.ONE)) return { status: 'invalid', msg: 'No whole number of periods works.' };
        var g2 = listNumbers(ans); return g2.length && g2[g2.length - 1].eq(new Q(n0)) ? { status: 'verified', computed: String(n0) } : { status: 'mismatch', msg: 'Correct: after ' + n0 + '.' };
      }
      throw new C.CheckError('unknown want');
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }
  function qpowRoot(q, k) { try { return C.evalNode(C.parseExpr('(' + qText(q).replace(/^-/, '0-') + ')^{\\frac{1}{' + k + '}}'), {}); } catch (e) { return null; } }
  function qpowFn(b, e) { return C.evalNode({ k: 'xpow', a: { k: 'num', v: b }, b: { k: 'num', v: e } }, {}); }
  function lastNum(markup, q) { var g = listNumbers(markup); if (!g.length) g = C.numbersInText(markup); return g.length > 0 && g[g.length - 1].eq(q); }


  /* ---------------- factoring and solving by factoring ---------------- */
  var FACT_TYPES = ['factor', 'quad-roots', 'quad-apply'];
  function bigAbs(n) { return n < 0n ? -n : n; }
  function bigGcd(a, b) { a = bigAbs(a); b = bigAbs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  /* coefficients [c0, c1, …] of a polynomial in one variable */
  function coeffsOf(node, v) {
    var rf = C.toRF(node); if (!rf.isPoly()) throw new C.CheckError('not a polynomial');
    var P = rf.asPoly(); if (P.vars().some(function (x) { return x !== v; })) throw new C.CheckError('use only the variable ' + v);
    var out = []; for (var k = 0; k <= P.degreeIn(v); k++) out.push(P.coeffOf(v, k).constVal());
    while (out.length > 1 && out[out.length - 1].isZero()) out.pop();
    return out;
  }
  function polyEq(a, b) { return a.length === b.length && a.every(function (q, i) { return q.eq(b[i]); }); }
  function evalCo(co, x) { var s = Q.ZERO; for (var i = co.length - 1; i >= 0; i--) s = s.mul(x).add(co[i]); return s; }
  function deflate(co, r) { var n = co.length - 1, out = new Array(n), carry = Q.ZERO; for (var i = n; i >= 1; i--) { carry = carry.mul(r).add(co[i]); out[i - 1] = carry; } return out; }
  function divisors(n) { n = Number(bigAbs(n)); if (n > 1e7) throw new C.CheckError('numbers too large'); var d = []; for (var i = 1; i * i <= n; i++) if (n % i === 0) { d.push(i); if (i * i !== n) d.push(n / i); } return d; }
  /* all rational roots (with multiplicity) and what is left over */
  function ratRoots(co) {
    var roots = [], rest = co.slice();
    while (rest.length > 1 && rest[0].isZero()) { roots.push(Q.ZERO); rest = rest.slice(1); }
    if (rest.length <= 1) return { roots: roots, rest: rest };
    var L = rest.reduce(function (l, q) { return l * q.d / bigGcd(l, q.d); }, 1n), ints = rest.map(function (q) { return q.n * (L / q.d); });
    var cands = []; divisors(ints[0]).forEach(function (p) { divisors(ints[ints.length - 1]).forEach(function (q) { cands.push(new Q(p, q), new Q(-p, q)); }); });
    var again = true;
    while (again && rest.length > 1) { again = false; for (var i = 0; i < cands.length; i++) if (evalCo(rest, cands[i]).isZero()) { roots.push(cands[i]); rest = deflate(rest, cands[i]); again = true; break; } }
    return { roots: roots, rest: rest };
  }
  function isSquareQ(q) { if (q.n < 0n) return false; var s = function (n) { var r = BigInt(Math.round(Math.sqrt(Number(n)))); for (var d = -1n; d <= 1n; d++) if ((r + d) >= 0n && (r + d) * (r + d) === n) return true; return false; }; return s(q.n) && s(q.d); }
  /* irreducible over the integers? (degree 1 always; degree 2 by the discriminant; degree 3 by rational roots) */
  function irreducible(co) {
    var deg = co.length - 1; if (deg < 1) return false; if (deg === 1) return true;
    if (deg === 2) return !isSquareQ(co[1].mul(co[1]).sub(new Q(4).mul(co[0]).mul(co[2])));
    if (deg === 3) return ratRoots(co).roots.length === 0;
    return null;    // cannot decide: treat as "factor further"
  }
  function contentOf(co) { if (!co.every(function (q) { return q.isInt(); })) return null; return co.reduce(function (g, q) { return bigGcd(g, q.n); }, 0n); }
  /* split a product into its factors: [{node, e}] and a constant */
  function flattenProduct(node) {
    var facs = [], cst = Q.ONE;
    (function f(n, e) {
      if (n.k === 'mul') { f(n.a, e); f(n.b, e); }
      else if (n.k === 'neg') { if (e % 2) cst = cst.neg(); f(n.a, e); }
      else if (n.k === 'grp') { if (/mul|neg|pow|grp/.test(n.a.k)) f(n.a, e); else facs.push({ node: n.a, e: e }); }
      else if (n.k === 'pow') f(n.a, e * n.e);
      else if (n.k === 'num') cst = cst.mul(n.v.pow(e));
      else facs.push({ node: n, e: e });
    })(node, 1);
    return { facs: facs, cst: cst };
  }
  /* two-variable factoring: multiply back (both variables), then check each factor with y = 1 and that no factor still holds x or y */
  function subVar(n, v, val) { if (!n || typeof n !== 'object') return n; if (n.k === 'var' && n.v === v) return { k: 'num', v: val }; var o = Object.assign({}, n); if (o.a) o.a = subVar(o.a, v, val); if (o.b) o.b = subVar(o.b, v, val); return o; }
  function checkFactor2(p, chk, ans) {
    var v = chk.v || 'x', w = chk.v2;
    var sn = C.snippets(ans); if (!sn.length) return { status: 'mismatch', msg: 'No answer.' };
    var aTxt = sn[sn.length - 1], eqi = aTxt.lastIndexOf('='); if (eqi >= 0) aTxt = aTxt.slice(eqi + 1);
    var same; try { same = C.equivalent(chk.expr, aTxt); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
    if (!same) return { status: 'mismatch', msg: 'The factors do not multiply back to the polynomial.' };
    var fp = flattenProduct(C.parseExpr(aTxt)); if (!fp.cst.isInt()) return { status: 'mismatch', msg: 'Use integer factors.' };
    for (var i = 0; i < fp.facs.length; i++) {
      var nd = fp.facs[i].node; if (nd.k === 'var') continue;   // a single x or y
      var co, cc; try { co = coeffsOf(subVar(nd, w, Q.ONE), v); } catch (e) { return { status: 'mismatch', msg: e.message }; }
      cc = contentOf(co); if (co.length < 2) return { status: 'mismatch', msg: 'Collect the monomial factors.' };
      if (cc === null || cc !== 1n) return { status: 'mismatch', msg: 'A factor still has a common factor.' };
      var at0 = function (x) { try { return C.toRF(subVar(nd, x, Q.ZERO)).asPoly(); } catch (e) { return null; } };
      [v, w].forEach(function (x) { var P0 = at0(x); if (P0 && P0.isZero && P0.isZero()) cc = -1n; });
      if (cc === -1n) return { status: 'mismatch', msg: 'A factor still has a common variable factor.' };
      if (irreducible(co) !== true) return { status: 'mismatch', msg: 'Not factored completely.' };
    }
    return { status: 'verified', computed: 'factored' };
  }
  function checkFactorPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, txt = C.plainText(ans).toLowerCase(), v = chk.v || 'x';
    if (t === 'factor') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The polynomial is not printed.' };
      if (chk.v2) return checkFactor2(p, chk, ans);
      var T = coeffsOf(C.parseExpr(chk.expr), v), cT = contentOf(T);
      if (cT === null) return { status: 'invalid', msg: 'Use integer coefficients.' };
      var tIrr = irreducible(T), isPrime = cT === 1n && tIrr === true;
      var sn = C.snippets(ans);
      if (!sn.length) return /prime/.test(txt) ? (isPrime ? { status: 'verified', computed: 'prime' } : { status: 'mismatch', msg: 'It factors.' }) : { status: 'mismatch', msg: 'No answer.' };
      var aTxt = sn[sn.length - 1], eqi = aTxt.lastIndexOf('='); if (eqi >= 0) aTxt = aTxt.slice(eqi + 1);
      var A = C.parseExpr(aTxt), Aco;
      try { Aco = coeffsOf(A, v); } catch (e) { return { status: 'mismatch', msg: e.message }; }
      if (!polyEq(Aco, T)) return { status: 'mismatch', msg: 'The factors do not multiply back to the polynomial.' };
      var fp = flattenProduct(A);
      if (!fp.cst.isInt()) return { status: 'mismatch', msg: 'Use integer factors.' };
      for (var i = 0; i < fp.facs.length; i++) {
        var co = coeffsOf(fp.facs[i].node, v), cc = contentOf(co);
        if (co.length < 2) return { status: 'mismatch', msg: 'Collect the number factors.' };
        if (cc === null) return { status: 'mismatch', msg: 'Use integer coefficients in every factor.' };
        if (cc !== 1n) return { status: 'mismatch', msg: 'A factor still has a common factor ' + cc + '.' };
        if (irreducible(co) !== true) return { status: 'mismatch', msg: 'Not factored completely.' };
      }
      return { status: 'verified', computed: isPrime ? 'prime' : 'factored' };
    }
    if (t === 'quad-roots') {
      if (!shown(p, chk.eq)) return { status: 'invalid', msg: 'The equation is not printed.' };
      var R = C.parseRelation(chk.eq), co2 = coeffsOf({ k: 'sub', a: R.lhs, b: { k: 'grp', a: R.rhs } }, v);
      if (co2.length < 2) return { status: 'invalid', msg: 'Not an equation in ' + v + '.' };
      var rr = ratRoots(co2); if (rr.rest.length > 1) return { status: 'invalid', msg: 'Some solutions are not rational.' };
      var want = uniqQ(rr.roots);
      if (policy && policy.intOnly && want.some(function (q) { return !q.isInt(); })) return { status: 'invalid', msg: 'A solution is not a whole number.' };
      var got = uniqQ(listNumbers(ans));
      return sameList(got, want) ? { status: 'verified', computed: want.map(qText).join(', ') } : { status: 'mismatch', msg: 'Solutions: ' + want.join(', ') + '.' };
    }
    if (t === 'quad-apply') {
      var st = studentText(p), pr = C.plainText(st).toLowerCase(), nums = C.numbersInText(st), at = function (k) { if (nums[k] === undefined) throw new C.CheckError('missing number ' + k); return nums[k]; };
      var co3, keep, out;
      if (chk.form === 'rule') {
        if (!shown(p, chk.rule)) return { status: 'invalid', msg: 'The model is not printed.' };
        var target = chk.target !== undefined ? at(chk.target) : Q.ZERO;
        co3 = coeffsOf({ k: 'sub', a: ruleRHS(chk.rule), b: { k: 'num', v: target } }, v);
      } else if (chk.form === 'consec') {
        var step = /\b(even|odd)\b/.test(pr) ? 2 : 1, P = at(chk.p);
        co3 = [P.neg(), new Q(step), Q.ONE];   // n(n + step) = P
        keep = function (n) { return n.isInt() && C.cmpQ(n, Q.ZERO) > 0 && (step === 1 || (/even/.test(pr) ? n.n % 2n === 0n : bigAbs(n.n) % 2n === 1n)); };
        out = function (n) { return [n, n.add(new Q(step))]; };
      } else if (chk.form === 'rect') {
        var k = at(chk.k), Ar = at(chk.A), twice = /twice its width/.test(pr), more = /more than (twice )?its width/.test(pr), less = /less than (twice )?its width/.test(pr);
        if (more === less) throw new C.CheckError('cannot read the length');
        var m = twice ? new Q(2) : Q.ONE, kk = more ? k : k.neg();
        co3 = [Ar.neg(), kk, m];   // w(m·w + kk) = A
        out = function (w) { return [w, m.mul(w).add(kk)]; };
      } else if (chk.form === 'border') {
        if (!/uniform/.test(pr)) throw new C.CheckError('the border must be uniform');
        var W = at(chk.W), Lb = at(chk.L), Ab = at(chk.A);
        co3 = [W.mul(Lb).sub(Ab), W.add(Lb).mul(new Q(2)), new Q(4)];   // (W + 2x)(L + 2x) = A
      } else throw new C.CheckError('unknown form');
      var rr3 = ratRoots(co3); if (rr3.rest.length > 1) return { status: 'invalid', msg: 'The solutions are not rational.' };
      var pos = uniqQ(rr3.roots).filter(keep || function (q) { return C.cmpQ(q, Q.ZERO) > 0; });
      if (pos.length !== 1) return { status: 'invalid', msg: pos.length ? 'More than one answer makes sense.' : 'No answer makes sense.' };
      var wantList = out ? out(pos[0]) : [pos[0]], gotList = listNumbers(ans);
      return sameList(gotList, wantList) ? { status: 'verified', computed: wantList.map(qText).join(', ') } : { status: 'mismatch', msg: 'Correct: ' + wantList.join(', ') + '.' };
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }


  /* ---------------- statistics ---------------- */
  var STAT_TYPES = ['stat', 'stat-box', 'twoway', 'scatter-corr', 'stat-line', 'hist', 'lsrl', 'causation'];
  function sortQ(a) { return a.slice().sort(function (x, y) { return C.cmpQ(x, y); }); }
  function sumQ(a) { return a.reduce(function (s, q) { return s.add(q); }, Q.ZERO); }
  function meanQ(a) { return sumQ(a).div(new Q(a.length)); }
  function medianQ(s) { var n = s.length; return n % 2 ? s[(n - 1) / 2] : s[n / 2 - 1].add(s[n / 2]).div(new Q(2)); }
  /* quartiles: medians of the lower and upper halves, leaving out the median when the count is odd */
  function quartiles(a) { var s = sortQ(a), n = s.length, h = Math.floor(n / 2); return [s[0], medianQ(s.slice(0, h)), medianQ(s), medianQ(s.slice(n - h)), s[n - 1]]; }
  function madQ(a) { var m = meanQ(a); return meanQ(a.map(function (x) { var d = x.sub(m); return C.cmpQ(d, Q.ZERO) < 0 ? d.neg() : d; })); }
  function outliersQ(a) { var q = quartiles(a), iqr = q[3].sub(q[1]), lo = q[1].sub(iqr.mul(new Q(3, 2))), hi = q[3].add(iqr.mul(new Q(3, 2))); return { lo: lo, hi: hi, list: uniqQ(a.filter(function (x) { return C.cmpQ(x, lo) < 0 || C.cmpQ(x, hi) > 0; })) }; }
  function dataOf(p, chk) {
    if (chk.data) { if (!shown(p, chk.data)) throw new C.CheckError('the data are not printed'); return chk.data.replace(/\\[ ,;!]/g, ' ').split(',').map(function (x) { return qStr(x.trim()); }); }
    var f = p.fig; if (!f) throw new C.CheckError('no data');
    if (f.kind === 'dotplot') return NS.fig.readDotplot(NS.fig.dotplot(f)).map(function (v) { return qStr(String(v)); });
    throw new C.CheckError('cannot read the data');
  }
  /* compare a computed value with the answer, honouring a printed rounding instruction */
  function roundCheck(p, chk, val, got, label) {
    if (!got) return { status: 'mismatch', msg: 'No value.' };
    if (chk.round !== undefined) {
      var phrase = chk.round === 0 ? /nearest (whole|percent)/ : chk.round === 1 ? /nearest tenth/ : /nearest hundredth/;
      if (!phrase.test(C.plainText(studentText(p)).toLowerCase())) return { status: 'invalid', msg: 'The problem must say how to round.' };
      var sc = Math.pow(10, chk.round), w = Math.round(qf(val) * sc + 1e-9) / sc;
      return Math.abs(qf(got) - w) < 1e-9 ? { status: 'verified', computed: String(w) } : { status: 'mismatch', msg: (label || 'Correct') + ': ' + w + '.' };
    }
    return got.eq(val) ? { status: 'verified', computed: qText(val) } : { status: 'mismatch', msg: (label || 'Correct') + ': ' + val + '.' };
  }
  function pctNums(ans) { var t = String(ans).replace(/⟨([^⟩]*)⟩/g, ' $1 ').replace(/\\%/g, '%').replace(/−/g, '-'), out = [], re = /(-?\d+(?:\.\d+)?)\s*%/g, m; while ((m = re.exec(t))) out.push(qStr(m[1])); return out; }
  /* ---------- standard deviation, histograms, least-squares regression (float math; the problem must print how to round) ---------- */
  function sdF(a) { var n = a.length, m = a.reduce(function (s, x) { return s + x; }, 0) / n; return Math.sqrt(a.reduce(function (s, x) { return s + (x - m) * (x - m); }, 0) / n); }
  function roundF(p, k, val, got, label) {
    var phrase = k === 0 ? /nearest (whole|percent)/ : k === 1 ? /nearest tenth/ : /nearest hundredth/;
    if (!phrase.test(C.plainText(studentText(p)).toLowerCase())) return { status: 'invalid', msg: 'The problem must say how to round.' };
    if (!got) return { status: 'mismatch', msg: 'No value.' };
    var sc = Math.pow(10, k), w = Math.round(val * sc + 1e-9 * (val < 0 ? -1 : 1)) / sc;
    return Math.abs(qf(got) - w) < 1e-9 ? { status: 'verified', computed: String(w) } : { status: 'mismatch', msg: (label || 'Correct') + ': ' + w + '.' };
  }
  function checkSD(p, chk, ans) {
    var txt = C.plainText(studentText(p)), got = listNumbers(ans), last = got[got.length - 1];
    if (chk.want === 'sd-compare') {
      var A = dataOf(p, { data: chk.data }).map(qf), B = dataOf(p, { data: chk.data2 }).map(qf), sa = sdF(A), sb = sdF(B);
      if (Math.abs(sa - sb) < 0.5) return { status: 'invalid', msg: 'The spreads are too close to call by eye.' };
      var more = sa > sb ? chk.labels[0] : chk.labels[1], t0 = C.plainText(ans).toLowerCase().replace(/^\W+/, '');
      if (txt.indexOf(chk.labels[0] + ':') < 0 || txt.indexOf(chk.labels[1] + ':') < 0) return { status: 'invalid', msg: 'The data sets are not labeled.' };
      return t0.indexOf(more.toLowerCase()) === 0 ? { status: 'verified', computed: more } : { status: 'mismatch', msg: more + ' is more spread out.' };
    }
    var d = dataOf(p, chk).map(qf);
    if (!/standard deviation/.test(txt)) return { status: 'invalid', msg: 'The question must ask for the standard deviation.' };
    var tr = /Every value is (increased|multiplied) by (\d+)/.exec(txt);
    if (!!tr !== !!chk.transform) return { status: 'invalid', msg: 'The change to the data is not printed.' };
    if (tr) d = d.map(function (x) { return tr[1] === 'increased' ? x + +tr[2] : x * +tr[2]; });
    return roundF(p, chk.round, sdF(d), last, 'σ');
  }
  function checkHist(p, chk, ans) {
    if (!p.fig || p.fig.kind !== 'histogram') throw new C.CheckError('no histogram');
    var bins = NS.fig.readHistogram(NS.fig.histogram(p.fig)), txt = C.plainText(p.prompt).replace(/\s+/g, ' '), got = listNumbers(ans);
    var first = bins[0].lo, end = bins[bins.length - 1].hi, tot = bins.reduce(function (s, b) { return s + b.count; }, 0);
    var between = function (lo, hi) { var edges = bins.map(function (b) { return b.lo; }).concat([end]); if (edges.indexOf(lo) < 0 || edges.indexOf(hi) < 0) throw new C.CheckError('not a bin edge'); return bins.filter(function (b) { return b.lo >= lo && b.hi <= hi; }).reduce(function (s, b) { return s + b.count; }, 0); };
    if (chk.want === 'count' || chk.want === 'percent') {
      var m, lo, hi;
      if ((m = /from (\d+) up to (\d+)\?/.exec(txt))) { lo = +m[1]; hi = +m[2]; }
      else if ((m = /are at least (\d+)\?/.exec(txt))) { lo = +m[1]; hi = end; }
      else if ((m = /are less than (\d+)\?/.exec(txt))) { lo = first; hi = +m[1]; }
      else if (/shown in all\?/.test(txt)) { lo = first; hi = end; }
      else throw new C.CheckError('cannot read the interval');
      var k = between(lo, hi);
      if (chk.want === 'count') return got.length && got[got.length - 1].eq(new Q(k)) ? { status: 'verified', computed: String(k) } : { status: 'mismatch', msg: 'Count: ' + k + '.' };
      var pg = pctNums(ans); return roundF(p, chk.round, 100 * k / tot, pg[0], 'Percent');
    }
    if (chk.want === 'median-bin') {
      got = C.numbersInText(ans).concat(got);
      if (tot % 2 === 0) return { status: 'invalid', msg: 'Use an odd number of values.' };
      var target = (tot + 1) / 2, cum = 0, bin = null; bins.forEach(function (b) { if (!bin && cum + b.count >= target) bin = b; cum += b.count; });
      return got.length >= 2 && got[0].eq(new Q(bin.lo)) && got[1].eq(new Q(bin.hi)) ? { status: 'verified', computed: bin.lo + '–' + bin.hi } : { status: 'mismatch', msg: 'The median is in ' + bin.lo + '–' + bin.hi + '.' };
    }
    if (chk.want === 'est-mean') { var s = 0; bins.forEach(function (b) { s += b.count * (b.lo + b.hi) / 2; }); return roundF(p, chk.round, s / tot, got[got.length - 1], 'Estimated mean'); }
    throw new C.CheckError('unknown want');
  }
  /* correlation vs causation: the verifier's own table of observational studies and the lurking variables that explain them */
  var LURK = [
    [/ice cream/, /drown/, /temperature|heat|hot|warm|summer|weather|season/],
    [/shoe size/, /reading/, /\bage\b|older|grade|years old/],
    [/firefighters/, /damage/, /size of the fire|bigger fire|larger fire|how big|severity/],
    [/tvs?\b/, /life expectancy/, /wealth|rich|income|money|econom|health care/],
    [/churches/, /crimes?/, /population|size of the city|bigger cit|number of people|city size/],
    [/umbrellas/, /accidents/, /rain|weather|storm|wet/],
    [/hot chocolate/, /flu/, /cold|winter|temperature|season|weather/],
    [/miles driven/, /price/, /\bage\b|older|year|condition/],
    [/swimming pools/, /temperature/, /location|climate|region|where|latitude|geograph/]];
  function checkCausation(p, chk, ans) {
    var full = C.plainText(studentText(p)).toLowerCase(), stem = C.plainText(p.prompt).toLowerCase(), t = C.plainText(ans).toLowerCase().trim();
    var rBad = C.snippets(p.prompt).some(function (sn) { var m = /^r=(-?[\d.]+)$/.exec(sn.replace(/\s+/g, '')); return m && !(Math.abs(+m[1]) <= 1); });
    if (rBad) return { status: 'invalid', msg: 'r must be between −1 and 1.' };
    var exp = /randomly assigned/.test(stem);
    if (chk.want === 'which') {
      var segs = /study a:(.*)study b:(.*)/.exec(stem); if (!segs) return { status: 'invalid', msg: 'Two studies must be printed.' };
      var ea = /randomly assigned/.test(segs[1]), eb = /randomly assigned/.test(segs[2]); if (ea === eb) return { status: 'invalid', msg: 'Exactly one study must be an experiment.' };
      var pick = /study\s+([ab])\b/.exec(t), want = ea ? 'a' : 'b';
      if (!pick || pick[1] !== want || (/study\s+([ab])\b.*study\s+([ab])\b/.test(t) && !/random/.test(t))) return { status: 'mismatch', msg: 'Study ' + want.toUpperCase() + ' is the experiment.' };
      return /random/.test(t) ? { status: 'verified', computed: 'Study ' + want.toUpperCase() } : { status: 'mismatch', msg: 'Explain: random assignment.' };
    }
    if (chk.want === 'type') {
      var saysE = /experiment/.test(t), saysO = /observational/.test(t);
      if (saysE === saysO) return { status: 'mismatch', msg: 'Name one: observational study or experiment.' };
      return saysE === exp ? { status: 'verified', computed: exp ? 'experiment' : 'observational' } : { status: 'mismatch', msg: exp ? 'The treatments were randomly assigned: an experiment.' : 'Nothing was assigned: an observational study.' };
    }
    if (chk.want === 'cause') {
      var yes = /^yes\b/.test(t), no = /^no\b/.test(t); if (yes === no) return { status: 'mismatch', msg: 'Start with Yes or No.' };
      if (yes !== exp) return { status: 'mismatch', msg: exp ? 'Yes: it is a randomized experiment.' : 'No: it is an observational study.' };
      if (yes && !/random/.test(t)) return { status: 'mismatch', msg: 'Explain: random assignment.' };
      if (no && !/lurking|confounding|third|other variable|correlation|causation/.test(t)) return { status: 'mismatch', msg: 'Explain: correlation is not causation.' };
      return { status: 'verified', computed: exp ? 'yes' : 'no' };
    }
    if (chk.want === 'why') { if (!exp) return { status: 'invalid', msg: 'Not an experiment.' }; return /random/.test(t) ? { status: 'verified' } : { status: 'mismatch', msg: 'Random assignment.' }; }
    if (chk.want === 'lurk') {
      var hits = LURK.filter(function (L) { return L[0].test(full) && L[1].test(full); });
      if (hits.length !== 1) return { status: 'invalid', msg: 'Unknown study.' };
      return hits[0][2].test(t) ? { status: 'verified' } : { status: 'mismatch', msg: 'Not a lurking variable for this study.' };
    }
    throw new C.CheckError('unknown want');
  }
  function checkLSRL(p, chk, ans) {
    var txt = C.plainText(studentText(p)).toLowerCase(), got = []; try { got = listNumbers(ans); } catch (e) { got = []; } var last = got[got.length - 1];
    var STR = function (rv) { var a = Math.abs(rv); return [a >= 0.8 ? 'strong' : a >= 0.5 ? 'moderate' : 'weak', rv > 0 ? 'positive' : 'negative']; };
    var saysStrength = function (rv) { var w = STR(rv), t = C.plainText(ans).toLowerCase(); return t.indexOf(w[0]) >= 0 && t.indexOf(w[1]) >= 0 && ['strong', 'moderate', 'weak', 'positive', 'negative'].every(function (x) { return w.indexOf(x) >= 0 || t.indexOf(x) < 0; }); };
    if (chk.want === 'describe') { if (!shown(p, chk.r)) return { status: 'invalid', msg: 'r is not printed.' }; var rv = qf(C.readNumber(chk.r.slice(chk.r.indexOf('=') + 1)));
      return saysStrength(rv) ? { status: 'verified', computed: STR(rv).join(' ') } : { status: 'mismatch', msg: 'Correct: ' + STR(rv).join(' ') + '.' }; }
    var pts = NS.fig.readTable(NS.fig.table(p.fig)).map(function (r) { return [qf(qStr(r[0])), qf(qStr(r[1]))]; });
    var atX = function () { if (!shown(p, chk.at)) throw new C.CheckError('x is not printed'); return qf(C.readNumber(chk.at.slice(chk.at.indexOf('=') + 1))); };
    if (chk.want === 'use') { if (!shown(p, chk.line)) return { status: 'invalid', msg: 'The line is not printed.' }; var Rl = C.parseRelation(chk.line), env = {}; env.x = C.readNumber(String(atX()));
      return roundF(p, chk.round, qf(C.evalNode(Rl.rhs, env)), last, 'y'); }
    var n = pts.length, sx = 0, sy = 0, sxx = 0, sxy = 0, syy = 0; pts.forEach(function (q) { sx += q[0]; sy += q[1]; sxx += q[0] * q[0]; sxy += q[0] * q[1]; syy += q[1] * q[1]; });
    var Sxx = sxx - sx * sx / n, Sxy = sxy - sx * sy / n, Syy = syy - sy * sy / n, m = Sxy / Sxx, b = (sy - m * sx) / n, r = Sxy / Math.sqrt(Sxx * Syy);
    var r2 = function (x) { return Math.round(x * 100 + 1e-9 * (x < 0 ? -1 : 1)) / 100; }, mR = r2(m), bR = r2(b);
    if (!/least-squares regression line|correlation coefficient/.test(txt)) return { status: 'invalid', msg: 'The question must name the regression.' };
    if (chk.want === 'r') { var res = roundF(p, 2, r, last, 'r'); if (res.status === 'verified' && chk.describe && !saysStrength(r2(r))) return { status: 'mismatch', msg: 'Describe it as ' + STR(r2(r)).join(' ') + '.' }; return res; }
    if (chk.want === 'line') {
      if (!/nearest hundredth/.test(txt)) return { status: 'invalid', msg: 'The problem must say how to round.' };
      var sn = C.snippets(ans), eq0 = sn[0]; if (!eq0) return { status: 'mismatch', msg: 'No equation.' };
      var R0; try { R0 = C.parseRelation(eq0); } catch (e) { return { status: 'mismatch', msg: 'Could not read the line.' }; }
      if (!(R0.lhs.k === 'var' && R0.lhs.v === 'y')) return { status: 'mismatch', msg: 'Write y = ax + b.' };
      var at = function (x) { return qf(C.evalNode(R0.rhs, { x: C.readNumber(String(x)) })); }, gb = at(0), gm = at(1) - gb;
      return Math.abs(gb - bR) < 1e-9 && Math.abs(gm - mR) < 1e-9 ? { status: 'verified', computed: 'y=' + mR + 'x+' + bR } : { status: 'mismatch', msg: 'Correct: y = ' + mR + 'x + ' + bR + '.' };
    }
    var x0 = atX(), yhat = mR * x0 + bR;
    if (chk.want === 'predict') return roundF(p, chk.round, yhat, last, 'Prediction');
    if (chk.want === 'residual') { var pt = pts.filter(function (q) { return q[0] === x0; })[0]; if (!pt) return { status: 'invalid', msg: 'No data point at that x.' }; return roundF(p, chk.round, pt[1] - yhat, last, 'Residual'); }
    throw new C.CheckError('unknown want');
  }
  function checkStatPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, txt = C.plainText(ans).toLowerCase(), w = chk.want;
    if (t === 'hist') return checkHist(p, chk, ans);
    if (t === 'lsrl') return checkLSRL(p, chk, ans);
    if (t === 'causation') return checkCausation(p, chk, ans);
    if (t === 'stat' && (w === 'sd' || w === 'sd-compare')) return checkSD(p, chk, ans);
    if (t === 'stat') {
      var d = dataOf(p, chk), got = listNumbers(ans), last = got[got.length - 1];
      if (w === 'mean') return roundCheck(p, chk, meanQ(d), last, 'Mean');
      if (w === 'median') return roundCheck(p, chk, medianQ(sortQ(d)), last, 'Median');
      if (w === 'range') { var s0 = sortQ(d); return roundCheck(p, chk, s0[s0.length - 1].sub(s0[0]), last, 'Range'); }
      if (w === 'mad') return roundCheck(p, chk, madQ(d), last, 'MAD');
      if (w === 'mode') { var cnt = {}, best = 0; d.forEach(function (x) { cnt[x] = (cnt[x] || 0) + 1; best = Math.max(best, cnt[x]); }); if (best < 2) return { status: 'invalid', msg: 'No mode.' };
        var modes = uniqQ(d.filter(function (x) { return cnt[x] === best; })); return sameList(uniqQ(got), modes) ? { status: 'verified' } : { status: 'mismatch', msg: 'Mode: ' + modes.join(', ') + '.' }; }
      var q = quartiles(d);
      if (w === 'q1' || w === 'q3') return roundCheck(p, chk, q[w === 'q1' ? 1 : 3], last, w.toUpperCase());
      if (w === 'iqr') return roundCheck(p, chk, q[3].sub(q[1]), last, 'IQR');
      if (w === 'five') return sameList(got, q) ? { status: 'verified', computed: q.map(qText).join(', ') } : { status: 'mismatch', msg: 'Five-number summary: ' + q.join(', ') + '.' };
      if (w === 'outliers') { var o = outliersQ(d); if (!o.list.length) return /none|no outlier/.test(txt) && !got.length ? { status: 'verified', computed: 'none' } : { status: 'mismatch', msg: 'There are no outliers.' };
        return sameList(uniqQ(got), o.list) ? { status: 'verified', computed: o.list.join(', ') } : { status: 'mismatch', msg: 'Outliers: ' + o.list.join(', ') + '.' }; }
      if (w === 'fences') { var o2 = outliersQ(d); return got.length >= 2 && got[0].eq(o2.lo) && got[1].eq(o2.hi) ? { status: 'verified' } : { status: 'mismatch', msg: 'Fences: ' + o2.lo + ' and ' + o2.hi + '.' }; }
      if (w === 'better') { var o3 = outliersQ(d), pick = o3.list.length ? 'median' : 'mean'; if (got.some(function (x) { return !o3.list.some(function (y) { return y.eq(x); }); })) return { status: 'mismatch', msg: 'That value is not an outlier.' }; return firstWord(txt) === pick ? { status: 'verified', computed: pick } : { status: 'mismatch', msg: 'Better: the ' + pick + '.' }; }
      if (w === 'missing') {   // the mean of n values is M; find the missing one
        var nums = C.numbersInText(studentText(p)), M = nums[chk.mean], n = d.length + 1;
        if (!M || !nums[chk.count] || !nums[chk.count].eq(new Q(n))) return { status: 'invalid', msg: 'The count or the mean is not printed.' };
        return roundCheck(p, chk, M.mul(new Q(n)).sub(sumQ(d)), last, 'Missing value');
      }
      if (w === 'newmean' || w === 'without') {
        var nums2 = C.numbersInText(studentText(p)), d2 = d.slice();
        if (w === 'newmean') { if (!nums2[chk.add]) return { status: 'invalid', msg: 'The new value is not printed.' }; d2.push(nums2[chk.add]); }
        else { var ol = outliersQ(d).list; if (ol.length !== 1) return { status: 'invalid', msg: 'There must be exactly one outlier.' }; d2 = d.filter(function (x) { return !x.eq(ol[0]); }); }
        var stat = chk.stat === 'median' ? medianQ(sortQ(d2)) : meanQ(d2);
        return roundCheck(p, chk, stat, last, 'New ' + (chk.stat || 'mean'));
      }
      if (w === 'compare-mad') { var d1 = dataOf(p, { data: chk.data }), dB = dataOf(p, { data: chk.data2 }), m1 = madQ(d1), m2 = madQ(dB), more = C.cmpQ(m1, m2) > 0 ? chk.labels[0] : chk.labels[1];
        if (m1.eq(m2)) return { status: 'invalid', msg: 'The MADs are equal.' };
        return txt.indexOf(more.toLowerCase()) === txt.search(/[a-z]/) && sameList(got.slice(-2), [m1, m2]) ? { status: 'verified', computed: more } : { status: 'mismatch', msg: more + ' (MADs ' + m1 + ' and ' + m2 + ').' }; }
      throw new C.CheckError('unknown want ' + w);
    }
    if (t === 'stat-box') {
      var boxes = NS.fig.readBoxplot(NS.fig.boxplot(p.fig)).map(function (b) { return { label: b.label, q: b.q.map(function (v) { return qStr(String(v)); }) }; });
      var B = boxes[chk.box || 0], gotB = listNumbers(ans), lastB = gotB[gotB.length - 1];
      var val = { min: B.q[0], q1: B.q[1], median: B.q[2], q3: B.q[3], max: B.q[4], range: B.q[4].sub(B.q[0]), iqr: B.q[3].sub(B.q[1]) };
      if (val[w]) return roundCheck(p, chk, val[w], lastB, w);
      if (w === 'percent') { var idx = { min: 0, q1: 1, median: 2, q3: 3, max: 4 }, pc = (idx[chk.to] - idx[chk.from]) * 25, gp = pctNums(ans);
        if (!shown(p, chk.fromTeX) || !shown(p, chk.toTeX) || !qStr(chk.fromTeX).eq(B.q[idx[chk.from]]) || !qStr(chk.toTeX).eq(B.q[idx[chk.to]])) return { status: 'invalid', msg: 'The values asked about are not the printed quartiles.' };
        return gp.length && gp[0].eq(new Q(pc)) ? { status: 'verified', computed: pc + '%' } : { status: 'mismatch', msg: 'Correct: ' + pc + '%.' }; }
      if (w === 'compare') { var stat2 = chk.stat, f = function (b) { return stat2 === 'iqr' ? b.q[3].sub(b.q[1]) : stat2 === 'range' ? b.q[4].sub(b.q[0]) : b.q[2]; };
        var c = C.cmpQ(f(boxes[0]), f(boxes[1])); if (!c) return { status: 'invalid', msg: 'They are equal.' };
        var lab = (c > 0 ? boxes[0].label : boxes[1].label).toLowerCase(), first = txt.replace(/^\W+/, '');
        var diffOk = chk.diff ? gotB.length && gotB[gotB.length - 1].eq(f(boxes[c > 0 ? 0 : 1]).sub(f(boxes[c > 0 ? 1 : 0]))) : true;
        return first.indexOf(lab) === 0 && diffOk ? { status: 'verified', computed: lab } : { status: 'mismatch', msg: 'Correct: ' + lab + '.' }; }
      throw new C.CheckError('unknown want ' + w);
    }
    if (t === 'twoway') {
      var tw = NS.fig.readTwoway(NS.fig.twoway(p.fig)), R = tw.rows.length, Cn = tw.cols.length;
      if (!/total/i.test(tw.cols[Cn - 1]) || !/total/i.test(tw.rows[R - 1].label)) return { status: 'invalid', msg: 'The table needs total row and column.' };
      var g = tw.rows.map(function (r) { return r.cells.map(function (v) { return v === '?' ? null : qStr(v); }); }), missing = [];
      g.forEach(function (r, i) { r.forEach(function (v, j) { if (v === null) missing.push([i, j]); }); });
      for (var pass = 0; pass < 10; pass++) {   // fill from row and column totals
        for (var i = 0; i < R; i++) { var nul = g[i].filter(function (v) { return v === null; }).length; if (nul === 1) { var j0 = g[i].indexOf(null), s1 = Q.ZERO; g[i].forEach(function (v, j) { if (j < Cn - 1 && j !== j0) s1 = s1.add(v); }); g[i][j0] = j0 === Cn - 1 ? s1 : g[i][Cn - 1].sub(s1); } }
        for (var j = 0; j < Cn; j++) { var col = g.map(function (r) { return r[j]; }), nn = col.filter(function (v) { return v === null; }).length; if (nn === 1) { var i0 = col.indexOf(null), s2 = Q.ZERO; col.forEach(function (v, i) { if (i < R - 1 && i !== i0) s2 = s2.add(v); }); g[i0][j] = i0 === R - 1 ? s2 : g[R - 1][j].sub(s2); } }
      }
      if (g.some(function (r) { return r.some(function (v) { return v === null || C.cmpQ(v, Q.ZERO) < 0; }); })) return { status: 'invalid', msg: 'The table cannot be completed.' };
      for (var a = 0; a < R; a++) { var rs = Q.ZERO; for (var b = 0; b < Cn - 1; b++) rs = rs.add(g[a][b]); if (!rs.eq(g[a][Cn - 1])) return { status: 'invalid', msg: 'A row total does not add up.' }; }
      for (var b2 = 0; b2 < Cn; b2++) { var cs = Q.ZERO; for (var a2 = 0; a2 < R - 1; a2++) cs = cs.add(g[a2][b2]); if (!cs.eq(g[R - 1][b2])) return { status: 'invalid', msg: 'A column total does not add up.' }; }
      if (w === 'fill') { var want = missing.map(function (m) { return g[m[0]][m[1]]; }); return sameList(listNumbers(ans), want) ? { status: 'verified', computed: want.join(', ') } : { status: 'mismatch', msg: 'Missing values: ' + want.join(', ') + '.' }; }
      var ri = function (name) { var k = tw.rows.map(function (r) { return r.label; }).indexOf(name); if (k < 0) throw new C.CheckError('no row ' + name); return k; };
      var ci = function (name) { var k = tw.cols.indexOf(name); if (k < 0) throw new C.CheckError('no column ' + name); return k; };
      var total = g[R - 1][Cn - 1], hundred = new Q(100), gp2 = pctNums(ans);
      var pctv;
      if (w === 'joint') pctv = g[ri(chk.row)][ci(chk.col)].div(total);
      else if (w === 'marginal') pctv = chk.row ? g[ri(chk.row)][Cn - 1].div(total) : g[R - 1][ci(chk.col)].div(total);
      else if (w === 'cond-row') pctv = g[ri(chk.row)][ci(chk.col)].div(g[ri(chk.row)][Cn - 1]);    // of the people in this row, the fraction in this column
      else if (w === 'cond-col') pctv = g[ri(chk.row)][ci(chk.col)].div(g[R - 1][ci(chk.col)]);
      else if (w === 'assoc') {
        var p1 = g[ri(chk.rows[0])][ci(chk.col)].div(g[ri(chk.rows[0])][Cn - 1]).mul(hundred), p2 = g[ri(chk.rows[1])][ci(chk.col)].div(g[ri(chk.rows[1])][Cn - 1]).mul(hundred);
        var r1 = Math.round(qf(p1) + 1e-9), r2 = Math.round(qf(p2) + 1e-9), diff = Math.abs(qf(p1) - qf(p2));
        if (diff > 5 && diff < 15) return { status: 'invalid', msg: 'The percents are too close to call.' };
        var yes = diff >= 15, said = /^\s*yes/.test(txt) ? true : /^\s*no/.test(txt) ? false : null;
        return said === yes && gp2.length >= 2 && gp2[0].eq(new Q(r1)) && gp2[1].eq(new Q(r2)) ? { status: 'verified', computed: yes ? 'yes' : 'no' } : { status: 'mismatch', msg: (yes ? 'Yes' : 'No') + ' (' + r1 + '% vs ' + r2 + '%).' };
      } else throw new C.CheckError('unknown want ' + w);
      return roundCheck(p, chk, pctv.mul(hundred), gp2[0], 'Percent');
    }
    if (t === 'scatter-corr') {
      var pts = NS.fig.readScatter(NS.fig.scatter(p.fig)), n3 = pts.length, mx = 0, my = 0;
      pts.forEach(function (q2) { mx += q2[0] / n3; my += q2[1] / n3; });
      var sxy = 0, sxx = 0, syy = 0; pts.forEach(function (q2) { sxy += (q2[0] - mx) * (q2[1] - my); sxx += Math.pow(q2[0] - mx, 2); syy += Math.pow(q2[1] - my, 2); });
      var r = sxy / Math.sqrt(sxx * syy);
      var kind = r >= 0.6 ? 'positive' : r <= -0.6 ? 'negative' : Math.abs(r) <= 0.3 ? 'no' : null;
      if (!kind) return { status: 'invalid', msg: 'The association is not clear (r = ' + r.toFixed(2) + ').' };
      return firstWord(txt) === kind ? { status: 'verified', computed: kind } : { status: 'mismatch', msg: 'Correct: ' + kind + ' correlation.' };
    }
    if (t === 'stat-line') {
      var fx;
      if (chk.pairs) {   // the line through two printed points
        if (!shown(p, chk.pairs)) return { status: 'invalid', msg: 'The points are not printed.' };
        var pp = pairsFrom(chk.pairs); if (pp.length !== 2 || pp[0][0].eq(pp[1][0])) return { status: 'invalid', msg: 'Need two points.' };
        var mL = pp[1][1].sub(pp[0][1]).div(pp[1][0].sub(pp[0][0])), bL = pp[0][1].sub(mL.mul(pp[0][0])); fx = function (x) { return mL.mul(x).add(bL); };
      } else { if (!shown(p, chk.rule)) return { status: 'invalid', msg: 'The line is not printed.' }; fx = ruleFn(chk.rule, chk.v || 'x'); }
      var gl = listNumbers(ans), lastL = gl[gl.length - 1];
      if (w === 'predict') { if (!C.snippets(studentText(p)).some(function (sn) { return norm(sn).indexOf(norm((chk.v || 'x') + '=' + chk.at)) >= 0; })) return { status: 'invalid', msg: 'The input is not printed.' }; return roundCheck(p, chk, fx(qStr(chk.at)), lastL, 'Prediction'); }
      if (w === 'residual' || w === 'over-under') {
        var pt = '(' + chk.x + ',\\ ' + chk.y + ')'; if (!C.snippets(studentText(p)).some(function (sn) { return norm(sn).indexOf(norm(pt)) >= 0; })) return { status: 'invalid', msg: 'The data point is not printed.' };
        var res = qStr(chk.y).sub(fx(qStr(chk.x)));
        if (w === 'residual') return roundCheck(p, chk, res, lastL, 'Residual');
        if (res.isZero()) return { status: 'invalid', msg: 'The point is on the line.' };
        var word = C.cmpQ(res, Q.ZERO) > 0 ? 'under' : 'over';
        return txt.indexOf(word) >= 0 && txt.indexOf(word === 'under' ? 'over' : 'under') < 0 && lastL && lastL.eq(res) ? { status: 'verified', computed: word } : { status: 'mismatch', msg: 'The line ' + word + 'estimates (residual ' + res + ').' };
      }
      if (w === 'slope' || w === 'intercept') { var b0 = fx(Q.ZERO), m = fx(Q.ONE).sub(b0), want3 = w === 'slope' ? m : b0, sn3 = C.snippets(ans);
        if (!sn3.length) return { status: 'mismatch', msg: 'Give the number.' };
        var v3 = C.evalNode(C.parseExpr(sn3[w === 'intercept' ? sn3.length - 1 : 0]), {}); var dec = /decreas|less|fewer|drop|lower/.test(txt), neg0 = C.cmpQ(want3, Q.ZERO) < 0; return (dec ? neg0 && v3.eq(want3.neg()) : v3.eq(want3) && (w === 'intercept' || !neg0)) ? { status: 'verified' } : { status: 'mismatch', msg: 'The ' + w + ' is ' + want3 + '.' }; }
      throw new C.CheckError('unknown want ' + w);
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }


  /* ---------------- lines ---------------- */
  var LINE_TYPES = ['slope', 'line-eq', 'intercepts', 'line-apply'];
  /* a·x + b·y + c = 0 from a printed equation */
  function lineOf(src, vx, vy) {
    vx = vx || 'x'; vy = vy || 'y';
    var R = C.parseRelation(src); if (R.rel !== '=') throw new C.CheckError('not an equation');
    var rf = C.toRF({ k: 'sub', a: R.lhs, b: { k: 'grp', a: R.rhs } }); if (!rf.isPoly()) throw new C.CheckError('not linear');
    var P = rf.asPoly(); if (P.vars().some(function (v) { return v !== vx && v !== vy; })) throw new C.CheckError('use only ' + vx + ' and ' + vy);
    var ok = true; P.m.forEach(function (q, key) { if (key.split('*').filter(Boolean).reduce(function (d, part) { return d + (+part.split('^')[1]); }, 0) > 1) ok = false; });
    if (!ok) throw new C.CheckError('not linear');
    var L = { a: P.coeffOf(vx, 1).constVal(), b: P.coeffOf(vy, 1).constVal(), c: P.coeffOf(vx, 0).coeffOf(vy, 0).constVal() };
    if (L.a.isZero() && L.b.isZero()) throw new C.CheckError('not a line');
    return L;
  }
  function sameLine(L, M) { return L.a.mul(M.b).eq(M.a.mul(L.b)) && L.a.mul(M.c).eq(M.a.mul(L.c)) && L.b.mul(M.c).eq(M.b.mul(L.c)); }
  function slopeOfLine(L) { return L.b.isZero() ? null : L.a.neg().div(L.b); }
  function lineThrough(P1, P2) { if (P1[0].eq(P2[0]) && P1[1].eq(P2[1])) throw new C.CheckError('the points are the same'); var a = P2[1].sub(P1[1]), b = P1[0].sub(P2[0]); return { a: a, b: b, c: a.mul(P1[0]).add(b.mul(P1[1])).neg() }; }
  function lineSlopePoint(m, P1) { return m === null ? { a: Q.ONE, b: Q.ZERO, c: P1[0].neg() } : { a: m, b: Q.ONE.neg(), c: P1[1].sub(m.mul(P1[0])) }; }
  function readSlopeTeX(t) { return /undefined/i.test(t) ? null : qStr(t); }
  function onePair(p, tex) { if (!C.snippets(studentText(p)).some(function (sn) { return norm(sn).indexOf(norm(tex)) >= 0; })) throw new C.CheckError('the point is not printed'); var pr = pairsFrom(tex); if (pr.length !== 1) throw new C.CheckError('bad point'); return pr[0]; }
  /* the first math snippet printed after a word ("slope ⟨3⟩") */
  function snippetAfter(p, re) { var st = studentText(p), m = re.exec(st); if (!m) return null; var sn = C.snippets(st.slice(m.index)); return sn.length ? sn[0] : null; }
  /* the line described by what is printed */
  function targetLine(p, chk) {
    var src = chk.src;
    if (src.pairs) { if (!shown(p, src.pairs) && !C.snippets(studentText(p)).some(function (sn) { return norm(sn).indexOf(norm(src.pairs)) >= 0; })) throw new C.CheckError('the points are not printed'); var pp = pairsFrom(src.pairs); return lineThrough(pp[0], pp[1]); }
    if (src.eq) { if (!C.snippets(studentText(p)).some(function (sn) { return norm(sn) === norm(src.eq); })) throw new C.CheckError('the equation is not printed'); return lineOf(src.eq); }
    if (src.slope !== undefined) { var stS = studentText(p), hz = src.slope === '0' && /\bhorizontal\b/.test(stS), vt = /undefined/.test(src.slope) && /\bvertical\b/.test(stS);
      if (!hz && !vt) { var sS = snippetAfter(p, /slope/i); if (/undefined/.test(src.slope) ? !/slope\s+is\s+undefined|undefined\s+slope/i.test(stS) : (sS === null || norm(sS) !== norm(src.slope))) throw new C.CheckError('the slope is not printed'); }
      return lineSlopePoint(readSlopeTeX(src.slope), onePair(p, src.point)); }
    if (src.yint !== undefined) { var sM = snippetAfter(p, /slope/i), sB = snippetAfter(p, /y-intercept/i); if (sM === null || sB === null || norm(sM) !== norm(src.m) || norm(sB) !== norm(src.yint)) throw new C.CheckError('slope or intercept not printed'); return lineSlopePoint(qStr(src.m), [Q.ZERO, qStr(src.yint)]); }
    if (src.parallel || src.perp) { var base = lineOf(src.parallel || src.perp); if (!C.snippets(studentText(p)).some(function (sn) { return norm(sn) === norm(src.parallel || src.perp); })) throw new C.CheckError('the given line is not printed');
      var m0 = slopeOfLine(base), m1 = src.parallel ? m0 : (m0 === null ? Q.ZERO : m0.isZero() ? null : Q.ONE.neg().div(m0)); return lineSlopePoint(m1, onePair(p, src.point)); }
    if (src.fig) { var rel = relationOf(p, {}); if (rel.kind === 'graph') { var sg = rel.segs[0]; return lineThrough(sg.a, sg.b); } if (rel.pairs.length < 2) throw new C.CheckError('need two points'); var L0 = lineThrough(rel.pairs[0], rel.pairs[1]);
      if (!rel.pairs.every(function (q) { return L0.a.mul(q[0]).add(L0.b.mul(q[1])).add(L0.c).isZero(); })) throw new C.CheckError('the points are not on one line'); return L0; }
    throw new C.CheckError('unknown source');
  }
  function isVar(n, v) { return n.k === 'var' && n.v === v; }
  function numOf(n) { try { if (Object.keys(C.varsOf(n)).length) return null; return C.evalNode(n, {}); } catch (e) { return null; } }
  /* y − k  →  k (also y, y + k) */
  function shiftOf(n, v) { if (isVar(n, v)) return Q.ZERO; if ((n.k === 'sub' || n.k === 'add') && isVar(n.a, v)) { var k = numOf(n.b); if (k === null) return null; return n.k === 'sub' ? k : k.neg(); } return null; }
  function formOk(form, src) {
    var R = C.parseRelation(src), lhs = R.lhs, rhs = R.rhs;
    if (form === 'slope-intercept') {
      if (isVar(lhs, 'x') && numOf(rhs) !== null) return true;    // a vertical line x = c
      if (!isVar(lhs, 'y')) return false;
      var rf = C.toRF(rhs); if (!rf.isPoly() || rf.asPoly().vars().some(function (v) { return v !== 'x'; })) return false;
      return C.simplifiedForm(rhs).ok;
    }
    if (form === 'point-slope') {
      var k = shiftOf(lhs, 'y'); if (k === null) return false;
      var core = rhs, coef = Q.ONE;
      if (core.k === 'neg') { coef = coef.neg(); core = core.a; }
      if (core.k === 'mul') { var cf = numOf(core.a); if (cf === null) return false; coef = coef.mul(cf); core = core.b; }
      if (core.k !== 'grp') return false;
      var h = shiftOf(core.a, 'x'); return h !== null;
    }
    if (form === 'standard') {
      var cR = numOf(rhs); if (cR === null || !cR.isInt()) return false;
      var L = C.toRF(lhs).asPoly(), A = L.coeffOf('x', 1).constVal(), B = L.coeffOf('y', 1).constVal(), C0 = L.coeffOf('x', 0).coeffOf('y', 0).constVal();
      if (!C0.isZero() || !A.isInt() || !B.isInt()) return false;
      if (C.cmpQ(A, Q.ZERO) < 0 || (A.isZero() && C.cmpQ(B, Q.ZERO) < 0)) return false;
      var g = [A.n, B.n, cR.n].reduce(function (x, y) { return bigGcd(x, y); }, 0n); return g === 1n;
    }
    return true;
  }
  function pointOf(src) {   // the point used in a point-slope answer
    var R = C.parseRelation(src), k = shiftOf(R.lhs, 'y'), core = R.rhs; if (core.k === 'neg') core = core.a; if (core.k === 'mul') core = core.b; return [shiftOf(core.a, 'x'), k];
  }
  function checkLinePart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, txt = C.plainText(ans).toLowerCase(), w = chk.want;
    if (t === 'slope') {
      if (w === 'missing') {   // the line through (x1, ?) and (x2, y2) has slope m
        var m = qStr(chk.m), x1 = qStr(chk.x1), x2 = qStr(chk.x2), y2 = qStr(chk.y2);
        var sns = C.snippets(studentText(p)).map(norm), sm = snippetAfter(p, /has slope/i);
        if (sns.indexOf(norm('(' + chk.x1 + ',\\ k)')) < 0 || sns.indexOf(norm('(' + chk.x2 + ',\\ ' + chk.y2 + ')')) < 0 || sm === null || norm(sm) !== norm(chk.m)) return { status: 'invalid', msg: 'The points or slope are not printed as expected.' };
        var k = y2.sub(m.mul(x2.sub(x1))), g1 = listNumbers(ans); return g1.length && g1[g1.length - 1].eq(k) ? { status: 'verified', computed: qText(k) } : { status: 'mismatch', msg: 'Correct: ' + k + '.' };
      }
      if (w === 'collinear') {
        if (!shown(p, chk.pts)) return { status: 'invalid', msg: 'The points are not printed.' };
        var P3 = pairsFrom(chk.pts), Lc = lineThrough(P3[0], P3[1]), on = Lc.a.mul(P3[2][0]).add(Lc.b.mul(P3[2][1])).add(Lc.c).isZero();
        var said = /^\s*yes/.test(txt) ? true : /^\s*no/.test(txt) ? false : null;
        if (said !== on) return { status: 'mismatch', msg: on ? 'Yes, they are on one line.' : 'No.' };
        if (on && C.snippets(ans).length) { var sc = slopeOfLine(Lc), gc = listNumbers(ans); if (sc === null || !gc.length || !gc[gc.length - 1].eq(sc)) return { status: 'mismatch', msg: 'The common slope is ' + (sc === null ? 'undefined' : sc) + '.' }; }
        return { status: 'verified', computed: on ? 'yes' : 'no' };
      }
      if (w === 'relation') {   // parallel, perpendicular or neither
        var L1 = lineOf(chk.eqs[0]), L2 = lineOf(chk.eqs[1]); if (!chk.eqs.every(function (e) { return shown(p, e); })) return { status: 'invalid', msg: 'The equations are not printed.' };
        var s1 = slopeOfLine(L1), s2 = slopeOfLine(L2), rel = sameLine(L1, L2) ? 'same' : (s1 === null && s2 === null) || (s1 && s2 && s1.eq(s2)) ? 'parallel' : (s1 === null && s2 && s2.isZero()) || (s2 === null && s1 && s1.isZero()) || (s1 && s2 && s1.mul(s2).eq(Q.ONE.neg())) ? 'perpendicular' : 'neither';
        if (rel === 'same') return { status: 'invalid', msg: 'The lines are the same.' };
        return firstWord(txt) === rel ? { status: 'verified', computed: rel } : { status: 'mismatch', msg: 'Correct: ' + rel + '.' };
      }
      var L = targetLine(p, chk), sl = slopeOfLine(L);
      if (sl === null) return /undefined|no slope/.test(txt) && !C.snippets(ans).length ? { status: 'verified', computed: 'undefined' } : { status: 'mismatch', msg: 'The slope is undefined.' };
      var g2 = listNumbers(ans);
      return g2.length && g2[g2.length - 1].eq(sl) ? { status: 'verified', computed: qText(sl) } : { status: 'mismatch', msg: 'Slope: ' + sl + '.' };
    }
    if (t === 'line-eq') {
      var T = targetLine(p, chk), sn = C.snippets(ans); if (!sn.length) return { status: 'mismatch', msg: 'Write an equation.' };
      var a = sn[sn.length - 1], A;
      try { A = lineOf(a); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equation: ' + e.message }; }
      if (!sameLine(A, T)) return { status: 'mismatch', msg: 'That is a different line.' };
      if (!formOk(chk.form || 'any', a)) return { status: 'mismatch', msg: 'Write it in ' + chk.form + ' form.' };
      if (chk.form === 'point-slope' && chk.point) { var pt = pairsFrom(chk.point)[0], used = pointOf(a); if (!used[0].eq(pt[0]) || !used[1].eq(pt[1])) return { status: 'mismatch', msg: 'Use the point ' + chk.point + '.' }; }
      return { status: 'verified' };
    }
    if (t === 'intercepts') {
      var Li = targetLine(p, chk), val, which = w;
      if (which === 'x') { if (Li.a.isZero()) return { status: 'invalid', msg: 'No x-intercept.' }; val = Li.c.neg().div(Li.a); }
      else { if (Li.b.isZero()) return { status: 'invalid', msg: 'No y-intercept.' }; val = Li.c.neg().div(Li.b); }
      if (policy && policy.intOnly && !val.isInt()) return { status: 'invalid', msg: 'Not a whole number.' };
      var pr = pairsFrom(C.snippets(ans).join(' ')), okI = pr.length ? (which === 'x' ? pr[0][0].eq(val) && pr[0][1].isZero() : pr[0][0].isZero() && pr[0][1].eq(val)) : (listNumbers(ans).slice(-1)[0] || Q.ONE.neg()).eq(val);
      return okI ? { status: 'verified', computed: qText(val) } : { status: 'mismatch', msg: which + '-intercept: ' + val + '.' };
    }
    if (t === 'line-apply') {
      var st = studentText(p), pr2 = C.plainText(st).toLowerCase(), nums = C.numbersInText(st), at = function (k3) { if (nums[k3] === undefined) throw new C.CheckError('missing number ' + k3); return nums[k3]; };
      var mm, bb;
      if (chk.pts) { var A1 = [at(chk.pts[0][0]), at(chk.pts[0][1])], A2 = [at(chk.pts[1][0]), at(chk.pts[1][1])]; if (A1[0].eq(A2[0])) throw new C.CheckError('same input'); mm = A2[1].sub(A1[1]).div(A2[0].sub(A1[0])); bb = A1[1].sub(mm.mul(A1[0])); }
      else { var down = /(decreas|loses|drains|burns|spends|falls|drops|less each|melts)/.test(pr2), up = /(increas|gains|earns|grows|adds|charges|plus|more each|rises|fills)/.test(pr2);
        if (down === up) throw new C.CheckError('cannot tell if the amount goes up or down'); mm = down ? at(chk.rate).neg() : at(chk.rate); bb = at(chk.start); }
      var vx = chk.vars ? chk.vars[0] : 'x', vy = chk.vars ? chk.vars[1] : 'y';
      if (w === 'equation') { var sn2 = C.snippets(ans); if (!sn2.length) return { status: 'mismatch', msg: 'Write an equation.' }; var Ae;
        try { Ae = lineOf(sn2[sn2.length - 1], vx, vy); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equation.' }; }
        return sameLine(Ae, { a: mm, b: Q.ONE.neg(), c: bb }) ? { status: 'verified' } : { status: 'mismatch', msg: 'The model is ' + vy + ' = ' + mm + vx + ' + ' + bb + '.' }; }
      var g3 = listNumbers(ans), last3 = g3[g3.length - 1] || null;
      if (w === 'rate') return last3 && (last3.eq(mm) || (last3.eq(mm.neg()) && C.cmpQ(mm, Q.ZERO) < 0 && /decreas|less|loses|drops/.test(txt))) ? { status: 'verified', computed: qText(mm) } : { status: 'mismatch', msg: 'Rate: ' + mm + '.' };
      if (w === 'start') return last3 && last3.eq(bb) ? { status: 'verified', computed: qText(bb) } : { status: 'mismatch', msg: 'Starting value: ' + bb + '.' };
      if (w === 'value') { var vv = mm.mul(at(chk.at)).add(bb); return last3 && last3.eq(vv) ? { status: 'verified', computed: qText(vv) } : { status: 'mismatch', msg: 'Correct: ' + vv + '.' }; }
      if (w === 'when') { if (mm.isZero()) return { status: 'invalid', msg: 'Constant.' }; var xw = at(chk.target).sub(bb).div(mm); if (C.cmpQ(xw, Q.ZERO) < 0) return { status: 'invalid', msg: 'Negative time.' };
        if (policy && policy.intOnly && !xw.isInt()) return { status: 'invalid', msg: 'Not whole.' }; return last3 && last3.eq(xw) ? { status: 'verified', computed: qText(xw) } : { status: 'mismatch', msg: 'Correct: ' + xw + '.' }; }
      throw new C.CheckError('unknown want');
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }

  /* ---------- systems of equations and inequalities (Algebra 1 Unit 6) ---------- */
  var SYS_TYPES = ['system', 'sys-apply', 'ineq2', 'graph-key'];
  function solve2(L1, L2) {   // lines a·x + b·y + c = 0
    var det = L1.a.mul(L2.b).sub(L2.a.mul(L1.b));
    if (det.isZero()) return { kind: sameLine(L1, L2) ? 'infinite' : 'none' };
    var x = L1.b.mul(L2.c).sub(L2.b.mul(L1.c)).div(det), y = L2.a.mul(L1.c).sub(L1.a.mul(L2.c)).div(det);
    return { kind: 'one', x: x, y: y };
  }
  function sysLines(p, chk) {
    if (chk.eqs) { if (!chk.eqs.every(function (e) { return shown(p, e); })) throw new C.CheckError('the equations are not printed'); return chk.eqs.map(function (e) { return lineOf(e, chk.vx, chk.vy); }); }
    var rel = relationOf(p, {}); if (rel.kind !== 'graph' || rel.segs.length !== 2) throw new C.CheckError('need two drawn lines');
    return rel.segs.map(function (sg) { return lineThrough(sg.a, sg.b); });
  }
  /* (x, y) from "(3, -2)" or from "x = 3, y = -2" */
  function pairAnswer(ans, vx, vy) {
    vx = vx || 'x'; vy = vy || 'y';
    var sn = C.snippets(ans), pm = sn.length === 1 && /^\s*\((.*)\)\s*$/.exec(sn[0].replace(/\\left|\\right/g, ''));
    if (pm) { var parts = pm[1].replace(/\\[ ;!]/g, ' ').split(/,(?![^{]*\})/); if (parts.length === 2) { try { return parts.map(function (x) { return C.evalNode(C.parseExpr(x.replace(/\\,/g, '').trim()), {}); }); } catch (e) { return null; } } }
    var got = {}; sn.forEach(function (s) { s.split(/,|\\[ ,;]|\\text\{\s*and\s*\}/).forEach(function (piece) { if (!/=/.test(piece)) return; try { var R = C.parseRelation(piece); if (R.lhs.k === 'var') got[R.lhs.v] = C.evalNode(R.rhs, {}); } catch (e) { /* not x = number */ } }); });
    return got[vx] && got[vy] ? [got[vx], got[vy]] : null;
  }
  function countWord(txt) { return /^\s*one\b/.test(txt) ? 'one' : /^\s*(no\b|none)/.test(txt) ? 'none' : /^\s*infinite/.test(txt) ? 'infinite' : null; }
  function sysVerdict(S, ans, txt, vx, vy) {
    if (S.kind !== 'one') return countWord(txt) === S.kind && !pairAnswer(ans, vx, vy) ? { status: 'verified', computed: S.kind } : { status: 'mismatch', msg: S.kind === 'none' ? 'No solution (parallel lines).' : 'Infinitely many solutions (same line).' };
    var pa = pairAnswer(ans, vx, vy);
    return pa && pa[0].eq(S.x) && pa[1].eq(S.y) ? { status: 'verified', computed: '(' + qText(S.x) + ', ' + qText(S.y) + ')' } : { status: 'mismatch', msg: 'The solution is (' + S.x + ', ' + S.y + ').' };
  }
  /* a half-plane a·x + b·y + c > 0 (or ≥ 0) from a printed inequality */
  function halfOf(src, vx, vy) {
    vx = vx || 'x'; vy = vy || 'y';
    var R = C.parseRelation(src); if (R.rel === '=') throw new C.CheckError('not an inequality');
    var L = lineOf(src.replace(/\\le|\\ge|<|>|≤|≥/, '='), vx, vy);
    var neg = R.rel === '<' || R.rel === '≤';
    return { a: neg ? L.a.neg() : L.a, b: neg ? L.b.neg() : L.b, c: neg ? L.c.neg() : L.c, strict: R.rel === '<' || R.rel === '>' };
  }
  function sameHalf(H, K) { return H.strict === K.strict && sameLine(H, K) && C.cmpQ(H.a.mul(K.a).add(H.b.mul(K.b)).add(H.c.mul(K.c)), Q.ZERO) > 0; }
  function inHalf(H, pt) { var v = H.a.mul(pt[0]).add(H.b.mul(pt[1])).add(H.c); var s = C.cmpQ(v, Q.ZERO); return H.strict ? s > 0 : s >= 0; }
  function figHalves(p) {
    var f = p.fig; if (!f || f.kind !== 'plane') throw new C.CheckError('no graph');
    return NS.fig.readPlane(NS.fig.plane(f)).halfplanes.map(function (hp) {
      if (!hp.a[0] || !hp.a[1] || !hp.b[0] || !hp.b[1]) throw new C.CheckError('boundary not readable');
      var L = lineThrough([qOf(hp.a[0]), qOf(hp.a[1])], [qOf(hp.b[0]), qOf(hp.b[1])]), fl = function (q) { return Number(q.n) / Number(q.d); };
      var v = fl(L.a) * hp.inside[0] + fl(L.b) * hp.inside[1] + fl(L.c); if (Math.abs(v) < 1e-6) throw new C.CheckError('shading not readable');
      return v > 0 ? { a: L.a, b: L.b, c: L.c, strict: hp.dashed } : { a: L.a.neg(), b: L.b.neg(), c: L.c.neg(), strict: hp.dashed };
    });
  }
  function rowsFromText(p, rows) {
    var nums = C.numbersInText(studentText(p));
    var val = function (e) { if (typeof e === 'number') return new Q(BigInt(e)); if (typeof e === 'string') return qStr(e); var q = nums[e.n]; if (q === undefined) throw new C.CheckError('missing number ' + e.n); if (e.div) q = q.div(new Q(BigInt(e.div))); if (e.mul !== undefined) { if (nums[e.mul] === undefined) throw new C.CheckError('missing number ' + e.mul); q = q.mul(nums[e.mul]); } return e.s === -1 ? q.neg() : q; };
    return rows.map(function (r) { var a = val(r[0]), b = val(r[1]), c = val(r[2]); return { a: a, b: b, c: c.neg() }; });   // a·x + b·y = c
  }
  function yesNo(txt) { return /^\s*yes/.test(txt) ? true : /^\s*no\b/.test(txt) ? false : null; }
  function checkSysPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, txt = C.plainText(ans).toLowerCase(), w = chk.want || 'solve', vx = chk.vx || 'x', vy = chk.vy || 'y';
    if (t === 'system') {
      if (w === 'is-solution') { if (!shown(p, chk.point)) return { status: 'invalid', msg: 'The point is not printed.' }; var Ls = sysLines(p, chk), P0 = pairsFrom(chk.point)[0];
        var on = Ls.every(function (L) { return L.a.mul(P0[0]).add(L.b.mul(P0[1])).add(L.c).isZero(); }); return yesNo(txt) === on ? { status: 'verified', computed: on ? 'yes' : 'no' } : { status: 'mismatch', msg: on ? 'Yes, it satisfies both equations.' : 'No.' }; }
      if (w === 'param') {   // the value of k that gives chk.target ('none' or 'infinite')
        var sn = C.snippets(ans), kv = null; sn.forEach(function (s) { try { var R = C.parseRelation(s); if (R.lhs.k === 'var' && R.lhs.v === (chk.param || 'k')) kv = s.slice(s.indexOf('=') + 1); } catch (e) { /* skip */ } });
        if (kv === null) return { status: 'mismatch', msg: 'Give the value of ' + (chk.param || 'k') + '.' };
        if (!chk.eqs.every(function (e) { return shown(p, e); })) return { status: 'invalid', msg: 'The equations are not printed.' };
        var sub = chk.eqs.map(function (e) { return lineOf(e.replace(new RegExp(chk.param || 'k', 'g'), '\\left(' + kv + '\\right)'), vx, vy); });
        var Sk = solve2(sub[0], sub[1]); return Sk.kind === chk.target ? { status: 'verified', computed: kv } : { status: 'mismatch', msg: 'With that value the system has ' + (Sk.kind === 'one' ? 'one solution' : Sk.kind === 'none' ? 'no solution' : 'infinitely many solutions') + '.' };
      }
      var L2 = sysLines(p, chk), S = solve2(L2[0], L2[1]);
      if (w === 'count') { var cw = countWord(txt); if (cw !== S.kind) return { status: 'mismatch', msg: 'Correct: ' + S.kind + '.' }; var pc = pairAnswer(ans, vx, vy); if (pc && S.kind === 'one' && !(pc[0].eq(S.x) && pc[1].eq(S.y))) return { status: 'mismatch', msg: 'The intersection is (' + S.x + ', ' + S.y + ').' }; return { status: 'verified', computed: S.kind }; }
      if (policy && policy.intOnly && S.kind === 'one' && !(S.x.isInt() && S.y.isInt())) return { status: 'invalid', msg: 'Not whole numbers.' };
      return sysVerdict(S, ans, txt, vx, vy);
    }
    if (t === 'graph-key') {   // the key's graph must be the printed system; the written answer must match it
      if (!part.answerFig) return { status: 'invalid', msg: 'The key has no graph.' };
      var keyP = { fig: part.answerFig }, ansT = C.snippets(ans);
      if (chk.ineqs) {
        if (!chk.ineqs.every(function (e) { return shown(p, e); })) return { status: 'invalid', msg: 'The inequalities are not printed.' };
        var want = chk.ineqs.map(function (e) { return halfOf(e, vx, vy); }), drawn = figHalves(keyP);
        if (drawn.length !== want.length || !want.every(function (H) { return drawn.some(function (K) { return sameHalf(H, K); }); })) return { status: 'mismatch', msg: 'The key graph does not show the printed inequalities.' };
        var bLines = ansT.map(function (s) { return lineOf(s, vx, vy); });
        if (bLines.length !== want.length || !want.every(function (H) { return bLines.some(function (L) { return sameLine(H, L); }); })) return { status: 'mismatch', msg: 'The boundary lines in the answer are wrong.' };
        var words = C.plainText(ans).toLowerCase(), okW = want.every(function (H, i) { return words.indexOf(H.strict ? 'dashed' : 'solid') >= 0; });
        return okW ? { status: 'verified' } : { status: 'mismatch', msg: 'Solid or dashed is wrong.' };
      }
      if (!chk.eqs.every(function (e) { return shown(p, e); })) return { status: 'invalid', msg: 'The equations are not printed.' };
      var Ls2 = chk.eqs.map(function (e) { return lineOf(e, vx, vy); }), g2 = NS.fig.readPlane(NS.fig.plane(part.answerFig));
      var segL = g2.segs.map(function (sg) { return lineThrough([qOf(sg.a[0]), qOf(sg.a[1])], [qOf(sg.b[0]), qOf(sg.b[1])]); });
      if (segL.length !== 2 || !Ls2.every(function (L) { return segL.some(function (Sg) { return sameLine(L, Sg); }); })) return { status: 'mismatch', msg: 'The key graph does not show the printed lines.' };
      var S2 = solve2(Ls2[0], Ls2[1]); if (S2.kind !== 'one') return { status: 'invalid', msg: 'Not one solution.' };
      var pa2 = pairAnswer(ans, vx, vy);
      return pa2 && pa2[0].eq(S2.x) && pa2[1].eq(S2.y) ? { status: 'verified', computed: '(' + qText(S2.x) + ', ' + qText(S2.y) + ')' } : { status: 'mismatch', msg: 'The solution is (' + S2.x + ', ' + S2.y + ').' };
    }
    if (t === 'sys-apply') {
      var Rw = rowsFromText(p, chk.rows), Sa = solve2(Rw[0], Rw[1]);
      if (Sa.kind !== 'one') return { status: 'invalid', msg: 'The situation has no single answer.' };
      if (chk.int && !(Sa.x.isInt() && Sa.y.isInt())) return { status: 'invalid', msg: 'Not whole numbers.' };
      if (chk.pos && (C.cmpQ(Sa.x, Q.ZERO) < 0 || C.cmpQ(Sa.y, Q.ZERO) < 0)) return { status: 'invalid', msg: 'Negative amounts.' };
      if (w === 'model') { var es = C.snippets(ans).filter(function (s) { return /=/.test(s); }); if (es.length !== 2) return { status: 'mismatch', msg: 'Write two equations.' }; var ML;
        try { ML = es.map(function (e) { return lineOf(e, vx, vy); }); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equations.' }; }
        var okM = (sameLine(ML[0], Rw[0]) && sameLine(ML[1], Rw[1])) || (sameLine(ML[0], Rw[1]) && sameLine(ML[1], Rw[0])); return okM ? { status: 'verified' } : { status: 'mismatch', msg: 'The equations do not match the situation.' }; }
      var g = listNumbers(ans);
      if (w === 'x' || w === 'y') { var tv = w === 'x' ? Sa.x : Sa.y; return g.length && g[g.length - 1].eq(tv) ? { status: 'verified', computed: qText(tv) } : { status: 'mismatch', msg: 'Correct: ' + tv + '.' }; }
      return g.length === 2 && g[0].eq(Sa.x) && g[1].eq(Sa.y) ? { status: 'verified', computed: qText(Sa.x) + ', ' + qText(Sa.y) } : { status: 'mismatch', msg: 'Correct: ' + Sa.x + ' and ' + Sa.y + '.' };
    }
    if (t === 'ineq2') {
      var Hs;
      if (chk.ineqs) { if (!chk.ineqs.every(function (e) { return shown(p, e); })) return { status: 'invalid', msg: 'The inequalities are not printed.' }; Hs = chk.ineqs.map(function (e) { return halfOf(e, vx, vy); }); }
      else if (chk.hrows) { var nums2 = rowsFromText(p, chk.hrows.map(function (h) { return h.slice(0, 3); })); Hs = nums2.map(function (r, i) { var rel = chk.hrows[i][3], neg = rel === '<' || rel === 'le'; return { a: neg ? r.a.neg() : r.a, b: neg ? r.b.neg() : r.b, c: neg ? r.c.neg() : r.c, strict: rel === '<' || rel === '>' }; }); }
      else Hs = figHalves(p);
      if (w === 'is-solution') { if (!shown(p, chk.point)) return { status: 'invalid', msg: 'The point is not printed.' }; var P1 = pairsFrom(chk.point)[0], inAll = Hs.every(function (H) { return inHalf(H, P1); });
        return yesNo(txt) === inAll ? { status: 'verified', computed: inAll ? 'yes' : 'no' } : { status: 'mismatch', msg: inAll ? 'Yes.' : 'No.' }; }
      if (w === 'point-in') { var pp = pairsFrom(C.snippets(ans).join(' ')); if (pp.length !== 1) return { status: 'mismatch', msg: 'Give one point.' }; return Hs.every(function (H) { return inHalf(H, pp[0]); }) ? { status: 'verified' } : { status: 'mismatch', msg: 'That point is not in the solution region.' }; }
      if (w === 'inequality' || w === 'model') {   // the student's inequality (or system) must describe the same half-plane(s)
        var ss = C.snippets(ans).filter(function (s) { return /<|>|\\le|\\ge|≤|≥/.test(s); }), want = chk.which === undefined ? Hs : [Hs[chk.which]], SH;
        if (ss.length !== want.length) return { status: 'mismatch', msg: 'Write ' + want.length + ' inequalit' + (want.length > 1 ? 'ies' : 'y') + '.' };
        try { SH = ss.map(function (s) { return halfOf(s, vx, vy); }); } catch (e) { return { status: 'mismatch', msg: 'Could not read: ' + e.message }; }
        var used = {}, all = want.every(function (H) { for (var i = 0; i < SH.length; i++) if (!used[i] && sameHalf(SH[i], H)) { used[i] = 1; return true; } return false; });
        return all ? { status: 'verified' } : { status: 'mismatch', msg: 'That is a different region (check the boundary, the side and solid vs dashed).' };
      }
      throw new C.CheckError('unknown want');
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }

  /* ---------- exponents and scientific notation (Algebra 1 Unit 7) ---------- */
  var POW_TYPES = ['pow-simplify', 'pow-eval', 'sci', 'radical-simplify'];
  function unGrp(n) { while (n && n.k === 'grp') n = n.a; return n; }
  /* one monomial: an optional number and each variable once, with exponents 2, 3, … (no 0, 1 or negatives) */
  function powMono(n) {
    var neg = false; n = unGrp(n); if (n.k === 'neg') { neg = true; n = unGrp(n.a); }
    var fs = []; (function f(x) { if (x.k === 'mul') { f(x.a); f(x.b); } else fs.push(x); })(n);
    var coef = null, vars = {}, ok = true;
    fs.forEach(function (x) {
      if (x.k === 'neg' && x.a.k === 'num' && coef === null) { coef = x.a.v.neg(); }
      else if (x.k === 'num' || (x.k === 'div' && x.a.k === 'num' && x.b.k === 'num')) { if (coef !== null) ok = false; coef = x.k === 'num' ? x.v : x.a.v.div(x.b.v); }
      else if (x.k === 'var') { if (vars[x.v]) ok = false; vars[x.v] = 1; }
      else if (x.k === 'pow' && x.a.k === 'var' && x.e >= 2) { if (vars[x.a.v]) ok = false; vars[x.a.v] = x.e; }
      else ok = false;
    });
    if (!ok) return null;
    if (coef !== null && coef.eq(Q.ONE) && Object.keys(vars).length) return null;   // "1x"
    return { coef: coef === null ? Q.ONE : coef, vars: vars, neg: neg, hasNum: coef !== null };
  }
  function powSimplified(src) {
    var n = unGrp(C.parseExpr(src)), top = n;
    if (top.k === 'neg') top = unGrp(top.a);
    if (top.k === 'div') {
      var A = powMono(top.a), B = powMono(top.b); if (!A || !B) return 'write one fraction with a single term on top and bottom';
      if (!Object.keys(B.vars).length && B.coef.eq(Q.ONE)) return 'denominator 1';
      if (B.neg || C.cmpQ(B.coef, Q.ZERO) < 0) return 'negative denominator';
      if (!A.coef.isInt() || !B.coef.isInt()) return 'fractions inside a fraction';
      if (Object.keys(A.vars).some(function (v) { return B.vars[v]; })) return 'a variable is in both the numerator and the denominator';
      var g = bigGcd(A.coef.n < 0n ? -A.coef.n : A.coef.n, B.coef.n); if (g !== 1n) return 'the numbers are not reduced';
      if (!Object.keys(B.vars).length && !Object.keys(A.vars).length) return 'a number fraction';
      return null;
    }
    return powMono(n) ? null : 'not a single simplified monomial (positive exponents, each variable once)';
  }
  function sciParts(src) {   // a × 10^n with 1 ≤ |a| < 10
    var n = unGrp(C.parseExpr(src)), neg = false; if (n.k === 'neg') { neg = true; n = unGrp(n.a); }
    var a = Q.ONE, pw = n;
    if (n.k === 'mul') { if (n.a.k !== 'num') return null; a = n.a.v; pw = n.b; }
    if (pw.k !== 'pow' || pw.a.k !== 'num' || !pw.a.v.eq(new Q(10n))) return null;
    if (C.cmpQ(a, Q.ONE) < 0 || C.cmpQ(a, new Q(10n)) >= 0) return null;
    return { a: neg ? a.neg() : a, e: pw.e };
  }
  function lastMath(ans) { var s = C.snippets(ans); return s.length ? s[s.length - 1] : null; }
  function plainNumber(src) { var n = unGrp(C.parseExpr(src)); if (n.k === 'neg') n = unGrp(n.a); return n.k === 'num' || (n.k === 'div' && n.a.k === 'num' && n.b.k === 'num' && n.frac) ? true : false; }
  function checkPowPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, w = chk.want, am = lastMath(ans);
    if (t === 'pow-simplify') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' };
      if (am === null) return { status: 'mismatch', msg: 'No expression in the answer.' };
      var eq; try { eq = C.equivalent(chk.expr, am); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
      if (!eq) return { status: 'mismatch', msg: 'Not equivalent to the expression.' };
      var why = powSimplified(am); return why ? { status: 'mismatch', msg: 'Not fully simplified: ' + why + '.' } : { status: 'verified' };
    }
    if (t === 'radical-simplify') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' };
      if (am === null) return { status: 'mismatch', msg: 'No answer.' };
      var want, gotR; try { want = surdEval(chk.expr); } catch (e) { return { status: 'invalid', msg: 'Could not read the printed expression.' }; }
      try { gotR = surdEval(am); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
      if (!(Math.abs(gotR - want) <= 1e-9 * (1 + Math.abs(want)))) return { status: 'mismatch', msg: 'Not equal to the expression.' };
      var whyR = radicalSimplest(am); return whyR ? { status: 'mismatch', msg: 'Not in simplest radical form: ' + whyR + '.' } : { status: 'verified' };
    }
    if (t === 'pow-eval') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' };
      var v = C.evalNode(C.parseExpr(chk.expr), {}); if (am === null) return { status: 'mismatch', msg: 'Give a number.' };
      if (!plainNumber(am)) return { status: 'mismatch', msg: 'Write the value as a number or a fraction (no exponents).' };
      var got = C.evalNode(C.parseExpr(am), {}); if (got.isInt() === false && !/\\frac/.test(am) && !/\./.test(am)) return { status: 'mismatch', msg: 'Write a fraction.' };
      return got.eq(v) ? { status: 'verified', computed: qText(v) } : { status: 'mismatch', msg: 'Correct: ' + qText(v) + '.' };
    }
    if (t === 'sci') {
      var val = function (src) { if (!shown(p, src)) throw new C.CheckError('a number is not printed: ' + src); return C.evalNode(C.parseExpr(src), {}); };
      var target, form = 'sci';
      if (w === 'to-sci') target = val(chk.expr);
      else if (w === 'to-std') { target = val(chk.expr); form = 'std'; }
      else if (w === 'op') target = val(chk.expr);
      else if (w === 'apply' || w === 'ratio') { var A = val(chk.terms[0]), B = val(chk.terms[1]), op = chk.op || 'div';
        target = op === 'mul' ? A.mul(B) : op === 'add' ? A.add(B) : op === 'sub' ? A.sub(B) : A.div(B); if (chk.scale) target = target.mul(C.readNumber(String(chk.scale))); form = chk.form || 'sci'; }
      else if (w === 'compare') { var vals = chk.terms.map(val), best = 0; vals.forEach(function (x, i) { if (C.cmpQ(x, vals[best]) > 0) best = i; });
        var first = C.snippets(ans)[0]; return first && norm(first) === norm(chk.terms[best]) ? { status: 'verified', computed: chk.terms[best] } : { status: 'mismatch', msg: 'The largest is ' + chk.terms[best] + '.' }; }
      else throw new C.CheckError('unknown want');
      if (am === null) return { status: 'mismatch', msg: 'Give a number.' };
      var gv; try { gv = C.evalNode(C.parseExpr(am), {}); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
      if (chk.round !== undefined) { var sp = sciParts(am); if (!sp) return { status: 'mismatch', msg: 'Write the answer in scientific notation.' };
        var tp = target, ex = 0, ten = new Q(10n), at = C.cmpQ(tp, Q.ZERO) < 0 ? tp.neg() : tp; while (C.cmpQ(at, ten) >= 0) { at = at.div(ten); ex++; } while (C.cmpQ(at, Q.ONE) < 0) { at = at.mul(ten); ex--; }
        var scale = Math.pow(10, chk.round), rd = Math.round(Number(at.n) / Number(at.d) * scale + 1e-9) / scale; if (rd >= 10) { rd = rd / 10; ex++; }
        var want = C.readNumber(String(rd)); return sp.e === ex && sp.a.eq(C.cmpQ(tp, Q.ZERO) < 0 ? want.neg() : want) ? { status: 'verified', computed: rd + '\\times10^{' + ex + '}' } : { status: 'mismatch', msg: 'Correct: ' + rd + ' × 10^' + ex + '.' }; }
      if (!gv.eq(target)) return { status: 'mismatch', msg: 'Correct value: ' + qText(target) + '.' };
      if (form === 'sci' && !sciParts(am)) return { status: 'mismatch', msg: 'Write the answer in scientific notation (1 ≤ a < 10).' };
      if (form === 'std' && !plainNumber(am)) return { status: 'mismatch', msg: 'Write the number in standard form.' };
      return { status: 'verified', computed: qText(target) };
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }

  /* ---------- polynomials (Algebra 1 Unit 9) ---------- */
  var POLY_TYPES = ['poly-simplify', 'poly-classify', 'poly-apply', 'poly-divide', 'poly-closure'];
  function polyOf(src) { var rf = C.toRF(typeof src === 'string' ? C.parseExpr(src) : src); if (!rf.isPoly()) throw new C.CheckError('not a polynomial'); return rf.asPoly(); }
  function keyDeg(k) { return k ? k.split('*').reduce(function (s, part) { return s + (+part.split('^')[1]); }, 0) : 0; }
  function polyDeg(P) { var d = 0; P.m.forEach(function (q, k) { d = Math.max(d, keyDeg(k)); }); return d; }
  /* terms of a written expression, left to right, with their total degrees */
  function writtenTerms(src) {
    var out = []; (function f(n, s) { if (n.k === 'add') { f(n.a, s); f(n.b, s); } else if (n.k === 'sub') { f(n.a, s); f(n.b, -s); } else out.push(n); })(C.parseExpr(src), 1);
    return out.map(function (t) { return polyDeg(polyOf(t)); });
  }
  /* standard form: like terms combined, single monomials, degrees from highest to lowest */
  function polyStandard(src) {
    var form = C.simplifiedForm(src); if (!form.ok) return form.problems.join(', ');
    var d = writtenTerms(src); for (var i = 1; i < d.length; i++) if (d[i] > d[i - 1]) return 'terms are not in order from highest to lowest degree';
    return null;
  }
  /* closure: does the printed expression simplify to a polynomial? one variable; long division of numerator by denominator */
  function coefsIn(Pl, v) { var d = Pl.isZero() ? 0 : Pl.degreeIn(v), a = []; for (var k = 0; k <= d; k++) a.push(Pl.coeffOf(v, k).constVal()); return a; }
  function reducesToPoly(src, v) {
    var rf = C.toRF(C.parseExpr(src)); if (rf.isPoly()) return true;
    var vs = rf.n.vars().concat(rf.d.vars()); if (vs.some(function (u) { return u !== v; })) throw new C.CheckError('one variable only');
    var n = coefsIn(rf.n, v), d = coefsIn(rf.d, v), dl = d.length - 1;
    for (var i = n.length - 1; i >= dl; i--) { var q = n[i].div(d[dl]); for (var j = 0; j <= dl; j++) n[i - dl + j] = n[i - dl + j].sub(q.mul(d[j])); }
    return n.slice(0, dl).every(function (x) { return x.isZero(); });
  }
  function checkClosure(p, chk, ans, am, txt) {
    if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' };
    var v = chk.v || (C.varsOf ? null : null), vars = (function () { var s = {}; (function w(n) { if (!n || typeof n !== 'object') return; if (n.k === 'var') s[n.v] = 1; w(n.a); w(n.b); })(C.parseExpr(chk.expr)); return Object.keys(s); })();
    if (vars.length !== 1) throw new C.CheckError('closure needs one variable');
    var closed = reducesToPoly(chk.expr, vars[0]);
    if (chk.want === 'result') {
      if (am === null) return { status: 'mismatch', msg: 'No answer.' };
      var eq; try { eq = C.equivalent(chk.expr, am); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
      if (!eq) return { status: 'mismatch', msg: 'Not equal to the printed expression.' };
      if (!closed) return { status: 'verified' };
      var why; try { polyOf(am); why = polyStandard(am); } catch (e) { why = 'not a polynomial'; }
      return why ? { status: 'mismatch', msg: 'Write it in standard form: ' + why + '.' } : { status: 'verified' };
    }
    if (chk.want === 'closed') {
      var yes = /^\s*yes\b/.test(txt), no = /^\s*no\b/.test(txt);
      if (yes === no) return { status: 'mismatch', msg: 'Start with Yes or No.' };
      if (yes !== closed) return { status: 'mismatch', msg: closed ? 'It is a polynomial.' : 'It is not a polynomial.' };
      var top = (function () { var n = C.parseExpr(chk.expr); while (n.k === 'grp') n = n.a; return n.k; })(), opName = { add: 'addition', sub: 'subtraction', mul: 'multiplication', div: 'division' }[top] || null;
      var named = /closed under (addition|subtraction|multiplication|division)/.exec(txt);
      if (named && closed && named[1] !== opName) return { status: 'mismatch', msg: 'The operation here is ' + opName + '.' };
      if (!closed && !/denominator|negative exponent|remainder/.test(txt)) return { status: 'mismatch', msg: 'Explain why: the variable ends up in a denominator.' };
      return { status: 'verified', computed: closed ? 'yes' : 'no' };
    }
    throw new C.CheckError('unknown want');
  }
  var DEG_NAMES = ['constant', 'linear', 'quadratic', 'cubic', 'quartic', 'quintic'], TERM_NAMES = [null, 'monomial', 'binomial', 'trinomial'];
  function checkPolyPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, w = chk.want, txt = C.plainText(ans).toLowerCase(), am = (function () { var s = C.snippets(ans); return s.length ? s[s.length - 1] : null; })();
    if (t === 'poly-closure') return checkClosure(p, chk, ans, am, txt);
    if (t === 'poly-divide') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' };
      if (am === null) return { status: 'mismatch', msg: 'No answer.' };
      var eqD; try { eqD = C.equivalent(chk.expr, am); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
      if (!eqD) return { status: 'mismatch', msg: 'Not equal to the quotient.' };
      var a0 = am.replace(/\s+/g, ''), rm = /([+-])\\frac\{(\d+)\}\{([^{}]*)\}$/.exec(a0), polyPart = rm ? a0.slice(0, rm.index) : a0;
      if (/\\frac\{[^{}]*[a-z]/.test(polyPart) || /\}\{[^{}]*[a-z][^{}]*\}/.test(polyPart)) return { status: 'mismatch', msg: 'Write the quotient as a polynomial plus a remainder fraction.' };
      var whyD; try { polyOf(polyPart); whyD = polyStandard(polyPart); } catch (e) { return { status: 'mismatch', msg: 'The quotient is not a polynomial.' }; }
      return whyD ? { status: 'mismatch', msg: 'Write the quotient in standard form: ' + whyD + '.' } : { status: 'verified' };
    }
    if (t === 'poly-simplify' || t === 'poly-apply') {
      var target;
      if (t === 'poly-simplify') { if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' }; target = chk.expr; }
      else {   // the expression is built from printed side lengths: area, perimeter, outer minus inner area, or volume
        var seq = chk.sides.filter(function (sd, i) { return !(chk.square && i === 1); }), printed = C.snippets(studentText(p)).map(norm);   // the sides, in the order they are printed
        if (printed.length !== seq.length || !seq.every(function (sd, i) { return norm(sd) === printed[i]; })) return { status: 'invalid', msg: 'The side lengths are not the ones printed.' };
        var sides = chk.sides.map(function (sd) { return '\\left(' + sd + '\\right)'; });
        target = w === 'area' ? sides[0] + sides[1] : w === 'perimeter' ? '2' + sides[0] + '+2' + sides[1] : w === 'triangle' ? sides[0] + '+' + sides[1] + '+' + sides[2] : w === 'shaded' ? sides[0] + sides[1] + '-' + sides[2] + sides[3] : w === 'square' ? sides[0] + '^{2}' : w === 'volume' ? sides[0] + sides[1] + sides[2] : null;
        if (!target) throw new C.CheckError('unknown want');
      }
      if (am === null) return { status: 'mismatch', msg: 'No expression in the answer.' };
      var eq; try { eq = C.equivalent(target, am); } catch (e) { return { status: 'mismatch', msg: 'Could not read the answer.' }; }
      if (!eq) return { status: 'mismatch', msg: 'Not equivalent.' };
      var why; try { why = polyStandard(am); } catch (e) { why = 'not a polynomial in simplest form'; }
      return why ? { status: 'mismatch', msg: 'Write it in standard form: ' + why + '.' } : { status: 'verified' };
    }
    if (t === 'poly-classify') {
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The polynomial is not printed.' };
      var P0 = polyOf(chk.expr), deg = polyDeg(P0), nt = P0.m.size;
      if (w === 'degree') { var g = listNumbers(ans); return g.length && g[g.length - 1].eq(new Q(BigInt(deg))) ? { status: 'verified', computed: String(deg) } : { status: 'mismatch', msg: 'Degree ' + deg + '.' }; }
      if (w === 'name') {   // "cubic trinomial", "quartic polynomial with 4 terms"
        var dn = DEG_NAMES[deg] || null, tn = TERM_NAMES[nt] || 'polynomial';
        var wrongDeg = DEG_NAMES.filter(function (x) { return x !== dn && new RegExp('\\b' + x + '\\b').test(txt); }).length > 0, degOk = !wrongDeg && (chk.only === 'terms' || !dn || new RegExp('\\b' + dn + '\\b').test(txt));
        var termOk = new RegExp('\\b' + tn + '\\b').test(txt) && ['monomial', 'binomial', 'trinomial'].filter(function (x) { return x !== tn && new RegExp('\\b' + x + '\\b').test(txt); }).length === 0;
        return degOk && termOk ? { status: 'verified', computed: (dn ? dn + ' ' : '') + tn } : { status: 'mismatch', msg: 'It is a ' + (dn ? dn + ' ' : 'degree ' + deg + ' ') + tn + '.' };
      }
      if (w === 'leading') {   // the leading coefficient (one variable)
        var v = chk.v || 'x', lc = P0.coeffOf(v, P0.degreeIn(v)).constVal(), g2 = listNumbers(ans);
        return g2.length && g2[g2.length - 1].eq(lc) ? { status: 'verified', computed: qText(lc) } : { status: 'mismatch', msg: 'Leading coefficient ' + qText(lc) + '.' };
      }
      if (w === 'standard') {
        if (am === null) return { status: 'mismatch', msg: 'Write the polynomial.' };
        if (!C.equivalent(chk.expr, am)) return { status: 'mismatch', msg: 'Not the same polynomial.' };
        var why2 = polyStandard(am); return why2 ? { status: 'mismatch', msg: why2 + '.' } : { status: 'verified' };
      }
      throw new C.CheckError('unknown want');
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }

  /* ---------- quadratic functions and equations (Algebra 1 Unit 11) ---------- */
  var QUAD_TYPES = ['quad-solve', 'quad-feature', 'quad-disc', 'quad-vertex-eq', 'quad-proj', 'quad-ctsq', 'quad-graph', 'quad-transform', 'quad-fit'];
  var fl = function (q) { return Number(q.n) / Number(q.d); };
  /* a small float evaluator for answers with square roots: numbers, \frac, \sqrt, + − and products */
  function surdEval(src) {
    var s = String(src).replace(/\\left|\\right/g, '').replace(/\\[ ,;!]/g, '').replace(/\s+/g, '').replace(/\\cdot|\\times/g, '*'), i = 0;
    function peek() { return s[i]; }
    function expr() { var v = term(); while (peek() === '+' || peek() === '-') { var o = s[i++]; var w = term(); v = o === '+' ? v + w : v - w; } return v; }
    function term() { var v = unary(); for (;;) { if (peek() === '*') { i++; v *= unary(); } else if (peek() === '/') { i++; v /= unary(); } else if (peek() === '\\' || peek() === '(' || (peek() && /[0-9.]/.test(peek()) && false)) v *= unary(); else return v; } }
    function unary() { if (peek() === '-') { i++; return -unary(); } if (peek() === '+') { i++; return unary(); } return atom(); }
    function group() { if (s[i] !== '{') throw new C.CheckError('bad group'); i++; var v = expr(); if (s[i] !== '}') throw new C.CheckError('bad group'); i++; return v; }
    function atom() {
      if (s.slice(i, 5 + i) === '\\frac') { i += 5; var a = group(), b = group(); return a / b; }
      if (s.slice(i, 5 + i) === '\\sqrt') { i += 5; var r = group(); if (r < 0) throw new C.CheckError('square root of a negative'); return Math.sqrt(r); }
      if (peek() === '(') { i++; var v = expr(); if (s[i] !== ')') throw new C.CheckError('bad parentheses'); i++; return v; }
      var m = /^\d+(\.\d+)?/.exec(s.slice(i)); if (!m) throw new C.CheckError('cannot read ' + s.slice(i, i + 8));
      i += m[0].length; return +m[0];
    }
    var v = expr(); if (i !== s.length) throw new C.CheckError('cannot read the answer'); return v;
  }
  function squarefree(n) { for (var k = 2; k * k <= n; k++) if (n % (k * k) === 0) return false; return n > 1; }
  function gcdI(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  /* is an exact root written in simplest radical form? (p ± q√r)/s, r square-free, nothing left to reduce */
  function radicalSimplest(t) {
    var s = t.replace(/\\left|\\right/g, '').replace(/\s+/g, '').replace(/\\[ ,;!]/g, ''), neg = false;
    if (s[0] === '-' && /^-\\frac/.test(s)) { neg = true; s = s.slice(1); }
    var num = s, den = 1, fm = /^\\frac\{(.*)\}\{(\d+)\}$/.exec(s);
    if (fm) { num = fm[1]; den = +fm[2]; if (den === 1) return 'denominator 1'; }
    if (/\\frac/.test(num)) return 'a fraction inside a fraction';
    var parts = num.match(/[+-]?[^+-]+/g) || [], coefs = [];
    for (var k = 0; k < parts.length; k++) {
      var m = /^([+-]?)(\d*)(\\sqrt\{(\d+)\})?$/.exec(parts[k]); if (!m || (m[2] === '' && !m[3])) return 'cannot read ' + parts[k];
      if (m[3] && !squarefree(+m[4])) return 'the square root can be simplified';
      coefs.push(m[2] === '' ? 1 : +m[2]);
    }
    if (parts.filter(function (p) { return /sqrt/.test(p); }).length > 1 || parts.filter(function (p) { return !/sqrt/.test(p); }).length > 1) return 'combine like terms';
    if (den > 1 && coefs.reduce(gcdI, den) > 1) return 'the fraction can be reduced';
    return null;
  }
  /* the values a student wrote (± expanded), from the right side of each equation */
  function rootsWritten(ans) {
    var out = [];
    C.snippets(ans).forEach(function (sn) {
      var rhs = sn.slice(sn.lastIndexOf('=') + 1); if (/\\approx/.test(rhs)) rhs = rhs.slice(rhs.lastIndexOf('\\approx') + 7);
      rhs.split(/,(?![^{]*\})/).forEach(function (piece) { piece = piece.trim(); if (!piece) return;
        if (/\\pm/.test(piece)) { out.push(piece.replace('\\pm', '+'), piece.replace('\\pm', '-')); } else out.push(piece); });
    });
    return out.map(function (t) { return t.replace(/^\+/, '').replace(/\(\+/, '(').replace(/\{\+/, '{'); });
  }
  function quadCo(p, chk, v) {
    v = v || chk.v || 'x';
    if (chk.eq) { if (!shown(p, chk.eq)) throw new C.CheckError('the equation is not printed');
      var R = C.parseRelation(chk.eq), lhsIsFn = /^\s*[a-zA-Z](\([a-z]\))?\s*=/.test(chk.eq) && !/[a-z]/.test(chk.eq.split('=')[0].replace(/^\s*[a-zA-Z]\([a-z]\)|^\s*[a-zA-Z]/, ''));
      var node = chk.fn ? R.rhs : { k: 'sub', a: R.lhs, b: { k: 'grp', a: R.rhs } }; void lhsIsFn;
      var co = coeffsOf(node, v); while (co.length < 3) co.push(Q.ZERO); if (co.length > 3 || co[2].isZero()) throw new C.CheckError('not quadratic'); return co; }
    var f = p.fig; if (!f || f.kind !== 'plane') throw new C.CheckError('no graph');
    var g = NS.fig.readPlane(NS.fig.plane(f)); if (!g.curves.length) throw new C.CheckError('no curve');
    var pts = g.curves[0].filter(function (q) { return q[0] && q[1]; }).map(function (q) { return [qOf(q[0]), qOf(q[1])]; }); if (pts.length < 5) throw new C.CheckError('curve not readable');
    var A = pts[0], B = pts[Math.floor(pts.length / 2)], Cc = pts[pts.length - 1];   // the parabola through three read points, then every point must fit
    var d1 = B[1].sub(A[1]).div(B[0].sub(A[0])), d2 = Cc[1].sub(B[1]).div(Cc[0].sub(B[0])), a = d2.sub(d1).div(Cc[0].sub(A[0])), b = d1.sub(a.mul(A[0].add(B[0]))), c = A[1].sub(a.mul(A[0]).mul(A[0])).sub(b.mul(A[0]));
    if (!pts.every(function (q) { return a.mul(q[0]).mul(q[0]).add(b.mul(q[0])).add(c).eq(q[1]); })) throw new C.CheckError('the curve is not one parabola');
    if (a.isZero()) throw new C.CheckError('not a parabola');
    return [c, b, a];
  }
  /* "reflected …, vertically stretched by a factor of 3, shifted 4 units left and 2 units up" → {reflect, factor, h, k} */
  function transformWords(text) {
    var t = String(text).toLowerCase().replace(/−/g, '-'), out = { reflect: /reflect/.test(t), factor: Q.ONE, h: Q.ZERO, k: Q.ZERO };
    var fm = /(stretch|compress)\w* by a factor of (\d+)(?:\/(\d+))?/.exec(t); if (fm) out.factor = new Q(BigInt(fm[2]), BigInt(fm[3] || 1));
    var re = /(\d+) units? (left|right|up|down)/g, m;
    while ((m = re.exec(t))) { var q = new Q(BigInt(m[1])); if (m[2] === 'left') out.h = q.neg(); if (m[2] === 'right') out.h = q; if (m[2] === 'down') out.k = q.neg(); if (m[2] === 'up') out.k = q; }
    return out;
  }
  function checkQuadPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, w = chk.want, txt = C.plainText(ans).toLowerCase(), v = chk.v || 'x';
    if (t === 'quad-graph') {   // the key parabola must be the printed one; the vertex and points in the answer must be on it
      if (!part.answerFig) return { status: 'invalid', msg: 'The key has no graph.' };
      var coP = quadCo(p, chk), coK; try { coK = quadCo({ fig: part.answerFig }, {}); } catch (e) { return { status: 'mismatch', msg: 'The key graph is not a parabola: ' + e.message }; }
      if (!coP.every(function (q, i) { return q.eq(coK[i]); })) return { status: 'mismatch', msg: 'The key graph is not the printed parabola.' };
      var hV = coP[1].neg().div(coP[2].mul(new Q(2n))), kV = coP[0].sub(coP[1].mul(coP[1]).div(coP[2].mul(new Q(4n)))), onP = function (x, y) { return coP[2].mul(x).mul(x).add(coP[1].mul(x)).add(coP[0]).eq(y); };
      var pairs = []; C.snippets(ans).forEach(function (s) { var m = /^\s*\((.*)\)\s*$/.exec(s.replace(/\\left|\\right/g, '')); if (m) { var xy = m[1].replace(/\\[ ,;!]/g, ' ').split(','); if (xy.length === 2) pairs.push([C.readNumber(xy[0].trim()), C.readNumber(xy[1].trim())]); } });
      if (!pairs.length || !pairs[0][0].eq(hV) || !pairs[0][1].eq(kV)) return { status: 'mismatch', msg: 'The vertex is (' + qText(hV) + ', ' + qText(kV) + ').' };
      if (!pairs.every(function (q) { return onP(q[0], q[1]); })) return { status: 'mismatch', msg: 'A listed point is not on the parabola.' };
      var axS = C.snippets(ans).filter(function (s) { return /^\s*x\s*=/.test(s); })[0];
      if (!axS || !C.readNumber(axS.slice(axS.indexOf('=') + 1)).eq(hV)) return { status: 'mismatch', msg: 'The axis of symmetry is x = ' + qText(hV) + '.' };
      return { status: 'verified', computed: '(' + qText(hV) + ', ' + qText(kV) + ')' };
    }
    if (t === 'quad-transform') {
      var aT, hT, kT;
      if (!shown(p, 'y=x^{2}')) return { status: 'invalid', msg: 'The parent graph y = x² is not printed.' };
      if (w === 'describe') {
        var coT = quadCo(p, Object.assign({ fn: true }, chk)); aT = coT[2]; hT = coT[1].neg().div(aT.mul(new Q(2n))); kT = coT[0].sub(coT[1].mul(coT[1]).div(aT.mul(new Q(4n))));
        var said = transformWords(C.plainText(ans));
        var okT = said.reflect === (C.cmpQ(aT, Q.ZERO) < 0) && said.h.eq(hT) && said.k.eq(kT) && said.factor.eq(C.cmpQ(aT, Q.ZERO) < 0 ? aT.neg() : aT);
        return okT ? { status: 'verified' } : { status: 'mismatch', msg: 'a = ' + qText(aT) + ', h = ' + qText(hT) + ', k = ' + qText(kT) + '.' };
      }
      var desc = transformWords(C.plainText(p.prompt)), wantA = desc.reflect ? desc.factor.neg() : desc.factor;
      var am2 = C.snippets(ans)[0]; if (!am2) return { status: 'mismatch', msg: 'No equation.' };
      var coA; try { coA = quadCo({ prompt: ans }, { eq: am2, fn: true }); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equation.' }; }
      var wantCo = [wantA.mul(desc.h).mul(desc.h).add(desc.k), wantA.mul(desc.h).mul(new Q(-2n)), wantA];
      if (!coA.every(function (q, i) { return q.eq(wantCo[i]); })) return { status: 'mismatch', msg: 'Correct: a = ' + qText(wantA) + ', h = ' + qText(desc.h) + ', k = ' + qText(desc.k) + '.' };
      return /\)\^(\{2\}|\(2\)|2)/.test(am2.replace(/\s/g, '')) || desc.h.isZero() ? { status: 'verified' } : { status: 'mismatch', msg: 'Write it in vertex form.' };
    }
    if (t === 'quad-fit') {
      if (!p.fig || p.fig.kind !== 'table') throw new C.CheckError('no data table');
      if (!shown(p, 'y=ax^{2}+bx+c')) return { status: 'invalid', msg: 'The form y = ax² + bx + c is not printed.' };
      var ptsF = NS.fig.readTable(NS.fig.table(p.fig)).map(function (rw) { return [qStr(rw[0]), qStr(rw[1])]; });
      var rhsAt = function (src, x) { var R = C.parseRelation(src); return C.evalNode(R.rhs, { x: x }); };
      if (w === 'exact') {
        if (ptsF.length !== 3) throw new C.CheckError('need three points');
        var P1 = ptsF[0], P2 = ptsF[1], P3 = ptsF[2], d1 = P2[1].sub(P1[1]).div(P2[0].sub(P1[0])), d2 = P3[1].sub(P2[1]).div(P3[0].sub(P2[0])), aF = d2.sub(d1).div(P3[0].sub(P1[0])), bF = d1.sub(aF.mul(P1[0].add(P2[0]))), cF = P1[1].sub(aF.mul(P1[0]).mul(P1[0])).sub(bF.mul(P1[0]));
        var sF = C.snippets(ans)[0]; if (!sF) return { status: 'mismatch', msg: 'No equation.' };
        var okF; try { okF = [Q.ZERO, Q.ONE, new Q(-1n), new Q(2n)].every(function (x) { return rhsAt(sF, x).eq(aF.mul(x).mul(x).add(bF.mul(x)).add(cF)); }); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equation.' }; }
        return okF ? { status: 'verified', computed: 'y=' + qText(aF) + 'x^2+' + qText(bF) + 'x+' + qText(cF) } : { status: 'mismatch', msg: 'a = ' + qText(aF) + ', b = ' + qText(bF) + ', c = ' + qText(cF) + '.' };
      }
      if (!/quadratic regression/.test(C.plainText(p.prompt)) || !/nearest hundredth/.test(C.plainText(p.prompt))) return { status: 'invalid', msg: 'The problem must ask for quadratic regression and say how to round.' };
      var fpts = ptsF.map(function (q) { return [fl(q[0]), fl(q[1])]; }), S = [0, 0, 0, 0, 0], T = [0, 0, 0];
      fpts.forEach(function (q) { var xp = 1; for (var i = 0; i < 5; i++) { S[i] += xp; if (i < 3) T[i] += xp * q[1]; xp *= q[0]; } });
      var Mx = [[S[4], S[3], S[2], T[2]], [S[3], S[2], S[1], T[1]], [S[2], S[1], S[0], T[0]]];
      for (var i2 = 0; i2 < 3; i2++) { var pv = i2; for (var j = i2 + 1; j < 3; j++) if (Math.abs(Mx[j][i2]) > Math.abs(Mx[pv][i2])) pv = j; var tm = Mx[i2]; Mx[i2] = Mx[pv]; Mx[pv] = tm;
        for (var j2 = 0; j2 < 3; j2++) if (j2 !== i2) { var f0 = Mx[j2][i2] / Mx[i2][i2]; for (var k2 = i2; k2 < 4; k2++) Mx[j2][k2] -= f0 * Mx[i2][k2]; } }
      var r2 = function (x) { return Math.round(x * 100 + (x < 0 ? -1e-9 : 1e-9)) / 100; }, cR = [r2(Mx[0][3] / Mx[0][0]), r2(Mx[1][3] / Mx[1][1]), r2(Mx[2][3] / Mx[2][2])];
      if (w === 'reg') { var sR = C.snippets(ans)[0]; if (!sR) return { status: 'mismatch', msg: 'No equation.' };
        var v0, v1, vm; try { v0 = fl(rhsAt(sR, Q.ZERO)); v1 = fl(rhsAt(sR, Q.ONE)); vm = fl(rhsAt(sR, new Q(-1n))); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equation.' }; }
        var gA = (v1 + vm) / 2 - v0, gB = (v1 - vm) / 2;
        return Math.abs(gA - cR[0]) < 1e-9 && Math.abs(gB - cR[1]) < 1e-9 && Math.abs(v0 - cR[2]) < 1e-9 ? { status: 'verified', computed: cR.join(', ') } : { status: 'mismatch', msg: 'a = ' + cR[0] + ', b = ' + cR[1] + ', c = ' + cR[2] + '.' }; }
      if (w === 'predict') { if (!shown(p, chk.at)) return { status: 'invalid', msg: 'x is not printed.' }; var xq = fl(C.readNumber(chk.at.slice(chk.at.indexOf('=') + 1))), yq = cR[0] * xq * xq + cR[1] * xq + cR[2];
        var gq; try { gq = listNumbers(ans); } catch (e) { gq = []; } var wq = Math.round(yq * 10 + (yq < 0 ? -1e-9 : 1e-9)) / 10;
        return gq.length && Math.abs(fl(gq[gq.length - 1]) - wq) < 1e-9 ? { status: 'verified', computed: String(wq) } : { status: 'mismatch', msg: 'Prediction: ' + wq + '.' }; }
      throw new C.CheckError('unknown want');
    }
    if (t === 'quad-ctsq') {   // the number that completes the square for x² + bx
      if (!shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression is not printed.' };
      var cq = coeffsOf(C.parseExpr(chk.expr), v); if (cq.length !== 3 || !cq[2].eq(Q.ONE)) throw new C.CheckError('needs x² + bx');
      var hb = cq[1].div(new Q(2n)), tq = hb.mul(hb), gq = []; try { gq = listNumbers(ans); } catch (e) { gq = []; }
      return gq.length && gq[gq.length - 1].eq(tq) ? { status: 'verified', computed: qText(tq) } : { status: 'mismatch', msg: 'Add ' + qText(tq) + '.' };
    }
    var co = quadCo(p, chk), a = co[2], b = co[1], c = co[0], D = b.mul(b).sub(new Q(4n).mul(a).mul(c)), h = b.neg().div(new Q(2n).mul(a)), k = a.mul(h).mul(h).add(b.mul(h)).add(c);
    var Df = fl(D), roots = Df < 0 ? [] : [(-fl(b) - Math.sqrt(Df)) / (2 * fl(a)), (-fl(b) + Math.sqrt(Df)) / (2 * fl(a))].sort(function (x, y) { return x - y; });
    var rootQ = null; if (Df >= 0) { var sq = qpowRoot(D, 2); if (sq) rootQ = uniqQ([b.neg().sub(sq).div(new Q(2n).mul(a)), b.neg().add(sq).div(new Q(2n).mul(a))]); }
    function rootsVerdict(prefix) {
      if (Df < 0) return /no real|no solution/.test(txt) && !C.snippets(ans).length ? { status: 'verified', computed: 'no real solutions' } : { status: 'mismatch', msg: 'There are no real solutions.' };
      var want = (rootQ ? rootQ.map(fl) : (D.isZero() ? [roots[0]] : roots)).slice().sort(function (x, y) { return x - y; });
      var ws = rootsWritten(ans), vals;
      try { vals = ws.map(surdEval); } catch (e) { return { status: 'mismatch', msg: 'Could not read: ' + e.message }; }
      if (chk.round !== undefined) {
        var got = vals, sc = Math.pow(10, chk.round), rw = want.map(function (x) { return Math.round(x * sc + 1e-9) / sc; }).sort(function (x, y) { return x - y; }); rw = rw.filter(function (x, i) { return i === 0 || x !== rw[i - 1]; });
        got = got.slice().sort(function (x, y) { return x - y; });
        return got.length === rw.length && got.every(function (x, i) { return Math.abs(x - rw[i]) < 1e-9; }) ? { status: 'verified', computed: rw.join(', ') } : { status: 'mismatch', msg: 'Rounded: ' + rw.join(', ') + '.' };
      }
      for (var i = 0; i < ws.length; i++) { if (/[+-]\s*[+-]/.test(ws[i])) return { status: 'mismatch', msg: 'Two signs in a row.' }; var why = radicalSimplest(ws[i]); if (why) return { status: 'mismatch', msg: 'Simplest radical form: ' + why + '.' }; }
      var sv = vals.slice().sort(function (x, y) { return x - y; }).filter(function (x, i, arr) { return i === 0 || Math.abs(x - arr[i - 1]) > 1e-12; });
      return sv.length === want.length && sv.every(function (x, i) { return Math.abs(x - want[i]) < 1e-9; }) ? { status: 'verified' } : { status: 'mismatch', msg: 'The solutions are ' + want.map(function (x) { return x.toFixed(3); }).join(' and ') + ' (approximately).' };
    }
    if (t === 'quad-solve') { if (policy && policy.intOnly && chk.round === undefined && !(rootQ && rootQ.every(function (q) { return q.isInt(); })) && !chk.radical && !chk.exact && Df >= 0) return { status: 'invalid', msg: 'Not whole-number solutions.' }; return rootsVerdict(); }
    if (t === 'quad-disc') {
      if (w === 'value') { var g3 = listNumbers(ans); return g3.length && g3[g3.length - 1].eq(D) ? { status: 'verified', computed: qText(D) } : { status: 'mismatch', msg: 'Discriminant: ' + qText(D) + '.' }; }
      var cnt = C.cmpQ(D, Q.ZERO) > 0 ? 'two' : D.isZero() ? 'one' : 'no', said = /^\s*(two|2)\b/.test(txt) ? 'two' : /^\s*(one|1)\b/.test(txt) ? 'one' : /^\s*(no|none|zero|0)\b/.test(txt) ? 'no' : null;
      if (said === cnt && C.snippets(ans).length) { var gd = []; try { gd = listNumbers(ans); } catch (e) { gd = []; } if (!gd.length || !gd[gd.length - 1].eq(D)) return { status: 'mismatch', msg: 'The discriminant is ' + qText(D) + '.' }; }
      return said === cnt ? { status: 'verified', computed: cnt } : { status: 'mismatch', msg: cnt + ' real solution' + (cnt === 'one' ? '' : 's') + '.' };
    }
    if (t === 'quad-feature') {
      var lastNum = function () { var g4 = []; try { g4 = listNumbers(ans); } catch (e) { g4 = []; } return g4[g4.length - 1]; };
      if (w === 'vertex') { var pr = pairsFrom(C.snippets(ans).join(' ')); return pr.length === 1 && pr[0][0].eq(h) && pr[0][1].eq(k) ? { status: 'verified', computed: '(' + qText(h) + ', ' + qText(k) + ')' } : { status: 'mismatch', msg: 'Vertex (' + qText(h) + ', ' + qText(k) + ').' }; }
      if (w === 'axis') { var sn = C.snippets(ans)[0] || ''; var ok = false; try { var R2 = C.parseRelation(sn); ok = R2.lhs.k === 'var' && R2.lhs.v === v && C.evalNode(R2.rhs, {}).eq(h); } catch (e) { ok = false; } return ok ? { status: 'verified', computed: v + '=' + qText(h) } : { status: 'mismatch', msg: 'Axis of symmetry: ' + v + ' = ' + qText(h) + '.' }; }
      if (w === 'yint') { var pr2 = pairsFrom(C.snippets(ans).join(' ')), yv = pr2.length ? (pr2[0][0].isZero() ? pr2[0][1] : null) : lastNum(); return yv && yv.eq(c) ? { status: 'verified', computed: qText(c) } : { status: 'mismatch', msg: 'y-intercept ' + qText(c) + '.' }; }
      if (w === 'zeros') return rootsVerdict();
      if (w === 'maxmin') { var isMax = C.cmpQ(a, Q.ZERO) < 0, word = isMax ? 'maximum' : 'minimum', other = isMax ? 'minimum' : 'maximum';
        return new RegExp('\\b' + word + '\\b').test(txt) && !new RegExp('\\b' + other + '\\b').test(txt) && lastNum() && lastNum().eq(k) ? { status: 'verified', computed: word + ' ' + qText(k) } : { status: 'mismatch', msg: 'The ' + word + ' value is ' + qText(k) + '.' }; }
      if (w === 'range') { var sn2 = (C.snippets(ans)[0] || '').replace(/\s+/g, ''), ok2 = false, rm = /^y(\\le|\\ge|≤|≥)(.+)$/.exec(sn2); try { ok2 = !!rm && C.evalNode(C.parseExpr(rm[2]), {}).eq(k) && (C.cmpQ(a, Q.ZERO) < 0 ? /le|≤/.test(rm[1]) : /ge|≥/.test(rm[1])); } catch (e) { ok2 = false; } return ok2 ? { status: 'verified' } : { status: 'mismatch', msg: 'Range: y ' + (C.cmpQ(a, Q.ZERO) < 0 ? '≤ ' : '≥ ') + qText(k) + '.' }; }
      throw new C.CheckError('unknown want');
    }
    if (t === 'quad-proj') {   // a height model h(t) printed; time is the variable
      var g5 = listNumbers(ans), l5 = g5[g5.length - 1];
      if (w === 'max') return l5 && l5.eq(k) ? { status: 'verified', computed: qText(k) } : { status: 'mismatch', msg: 'Maximum height ' + qText(k) + '.' };
      if (w === 'tmax') return l5 && l5.eq(h) ? { status: 'verified', computed: qText(h) } : { status: 'mismatch', msg: 'Time ' + qText(h) + '.' };
      if (w === 'at') { var tv = C.readNumber(String(chk.at)); if (!C.numbersInText(studentText(p)).some(function (q) { return q.eq(tv); })) return { status: 'invalid', msg: 'The time is not printed.' }; var hv = a.mul(tv).mul(tv).add(b.mul(tv)).add(c); return l5 && l5.eq(hv) ? { status: 'verified', computed: qText(hv) } : { status: 'mismatch', msg: 'Height ' + qText(hv) + '.' }; }
      if (w === 'ground') { var pos = roots.filter(function (x) { return x > 1e-12; }); if (pos.length !== 1) return { status: 'invalid', msg: 'No single landing time.' };
        var sc2 = Math.pow(10, chk.round || 0), want2 = Math.round(pos[0] * sc2 + 1e-9) / sc2; return l5 && Math.abs(fl(l5) - want2) < 1e-9 ? { status: 'verified', computed: String(want2) } : { status: 'mismatch', msg: 'Lands at about ' + want2 + '.' }; }
      throw new C.CheckError('unknown want');
    }
    if (t === 'quad-vertex-eq') {   // y = a(x − h)² + k through a printed vertex and point (or the drawn parabola)
      var am = C.snippets(ans); am = am[am.length - 1]; if (!am) return { status: 'mismatch', msg: 'Write an equation.' };
      var R4; try { R4 = C.parseRelation(am); } catch (e) { return { status: 'mismatch', msg: 'Could not read the equation.' }; }
      if (!(R4.lhs.k === 'var' && R4.lhs.v === 'y')) return { status: 'mismatch', msg: 'Write y = … .' };
      var co4; try { co4 = coeffsOf(R4.rhs, v); } catch (e) { return { status: 'mismatch', msg: 'Not a quadratic in ' + v + '.' }; } while (co4.length < 3) co4.push(Q.ZERO);
      if (!(co4.length === 3 && co4[0].eq(c) && co4[1].eq(b) && co4[2].eq(a))) return { status: 'mismatch', msg: 'That is a different parabola.' };
      var vf = am.replace(/\\left|\\right/g, '').replace(/\s+/g, '').replace(/\^\(([^()]*)\)/g, '^{$1}');
      if (chk.form === 'vertex' && !/^y=-?(\d+|\\frac\{\d+\}\{\d+\})?\([a-z]([+-]\d+)?\)\^\{?2\}?([+-]\d+)?$/.test(vf)) return { status: 'mismatch', msg: 'Write it in vertex form y = a(x − h)² + k.' };
      if (chk.form === 'standard' && !/^y=[^()]*$/.test(vf)) return { status: 'mismatch', msg: 'Write it in standard form.' };
      return { status: 'verified' };
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }

  /* Worked-solution steps must agree with the problem (same solution set / same expression). */
  function checkSteps(p) {
    var issues = [], first = (p.parts || [])[0];
    if (!first || !first.check) return issues;
    (p.steps || []).forEach(function (st, i) {
      if (!st.m || st.partial) return;
      try {
        if ((first.check.type === 'solve' || first.check.type === 'classify') && /=/.test(st.m) && !/[<>]/.test(st.m)) {
          var vars = Object.keys(Object.assign(C.varsOf(C.parseRelation(st.m).lhs), C.varsOf(C.parseRelation(st.m).rhs)));
          if (vars.length === 1 && vars[0] === first.check.v) {
            var a = C.solveLinear(first.check.eq, first.check.v), b = C.solveLinear(st.m, first.check.v);
            if (a.kind !== b.kind || (a.kind === 'one' && !a.value.eq(b.value))) issues.push('Step ' + (i + 1) + ' changes the solution.');
          }
        } else if (first.check.type === 'ineq' && /[<>]|\\le|\\ge/.test(st.m)) {
          if (!C.setEqual(C.solutionSet(st.m, first.check.v || 'x'), C.solutionSet(first.check.ineq, first.check.v || 'x'))) issues.push('Step ' + (i + 1) + ' changes the solution set.');
        } else if (first.check.type === 'simplify' && !/=/.test(st.m)) {
          if (!C.equivalent(first.check.expr, st.m)) issues.push('Step ' + (i + 1) + ' is not equivalent to the expression.');
        }
      } catch (e) { issues.push('Step ' + (i + 1) + ' could not be read: ' + e.message); }
    });
    return issues;
  }

  NS.verifyProblem = function (p, policy) {
    var issues = [], computed = [], statuses = [];
    (p.parts || []).forEach(function (part, i) {
      var res;
      try { res = checkPart(p, part, policy); }
      catch (e) { res = { status: 'invalid', msg: (e && e.message) || String(e) }; }
      statuses.push(res.status); computed.push(res.computed || null);
      if (res.msg && res.status !== 'verified') issues.push(((p.parts.length > 1 && part.label) ? '(' + part.label + ') ' : '') + res.msg);
    });
    if (!p.parts || !p.parts.length) { statuses.push('manual'); issues.push('No answer has been entered.'); }
    /* A Geometry figure must be geometrically consistent with its own markings (equal ticks, right angles, parallel marks, angle sums). */
    if (p.fig && NS.geoFigures && NS.geoFigures.owns(p.fig)) {
      var fc = NS.geoFigures.check(p.fig);
      if (!fc.ok) { statuses.push('invalid'); issues.push('The figure is inconsistent: ' + fc.msg + '.'); }
      /* Congruence criteria: the marks on the figure must actually establish the criterion the question names. */
      if (/^geo-criterion-/.test(p.variant || '') && p.fig.kind === 'geo-cong' && NS.geoFigures.cong) {
        var cvk = /^geo-criterion-([a-z]+)-/.exec(p.variant)[1];
        if (NS.geoFigures.cong.derive(p.fig).toLowerCase() !== cvk) { statuses.push('invalid'); issues.push('The marks on the figure do not establish ' + cvk.toUpperCase() + '.'); }
      }
      /* Measurement figures print their dimensions from the data: every printed number must be stated in the question too, and none may be the answer's unknown. */
      else if (NS.geoFigures.printed && NS.geoFigures.printed(p.fig)) {
        var gtext = String(p.prompt || '').replace(/[,]/g, '');
        NS.geoFigures.printed(p.fig).forEach(function (pr) {
          var gre2 = new RegExp('(^|[^0-9.])' + String(pr[1]).replace('.', '\\.') + '([^0-9]|$)');
          if (!gre2.test(gtext)) { statuses.push('invalid'); issues.push('The figure shows ' + pr[0] + ' = ' + pr[1] + ', which the question does not state.'); }
        });
      }
      else if (p.fig.v && p.fig.kind === 'geo-rt') {
        var rtxt = String(p.prompt || '').replace(/[,]/g, ''), rv = p.fig.v, rc = Math.sqrt(rv.a * rv.a + rv.b * rv.b), printed = [], rk;
        (p.fig.show || []).forEach(function (k) { if (!(p.fig.lab && p.fig.lab[k] !== undefined)) printed.push([k, k === 'c' ? Math.round(rc * 1000) / 1000 : rv[k]]); });
        for (rk in (p.fig.lab || {})) { var rm = /^\s*(\d+(?:\.\d+)?)/.exec(p.fig.lab[rk]); if (rm) printed.push([rk, Number(rm[1])]); }
        for (rk in (p.fig.ang || {})) if (typeof p.fig.ang[rk] === 'number') printed.push(['angle ' + rk, p.fig.ang[rk]]);
        printed.forEach(function (pr) {
          var re = new RegExp('(^|[^0-9.])' + String(pr[1]).replace('.', '\\.') + '([^0-9]|$)');
          if (!re.test(rtxt)) { statuses.push('invalid'); issues.push('The figure shows ' + pr[0] + ' = ' + pr[1] + ', which the question does not state.'); }
        });
      }
      else if (p.fig.v && /^geo-(plane|solid)$/.test(p.fig.kind)) {
        var need = (p.fig.show || Object.keys(p.fig.v)), txt = String(p.prompt || '').replace(/[,]/g, '');
        need.forEach(function (k) {
          if (p.fig.lab && p.fig.lab[k] !== undefined) return;
          var re = new RegExp('(^|[^0-9.])' + String(p.fig.v[k]).replace('.', '\\.') + '([^0-9]|$)');
          if (!re.test(txt)) { statuses.push('invalid'); issues.push('The figure shows ' + k + ' = ' + p.fig.v[k] + ', which the question does not state.'); }
        });
      }
    }
    if (!p.edited) issues = issues.concat(checkSteps(p));
    var status = statuses.indexOf('invalid') >= 0 ? 'invalid' : statuses.indexOf('mismatch') >= 0 ? 'mismatch'
      : statuses.indexOf('manual') >= 0 ? 'manual' : 'verified';
    if (status === 'verified' && issues.length) status = 'mismatch';
    return { ok: status === 'verified', status: status, issues: issues, computed: computed };
  };
  NS.studentText = studentText;
})(typeof window !== 'undefined' ? window : globalThis);
