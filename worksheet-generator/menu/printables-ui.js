/* Printable Generators — paper rendering and teacher interface (worksheet-generator/printables.html).
   Pages are Letter size (.page.mm-page from core/app.css + menu/menu.css). */
(function (G) {
  'use strict';
  var doc = G.document, NS = G.MKMENU, PR = NS.printables, WS = G.MKWS;
  var mathSafe = NS.mathSafe;
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function $(s, r) { return (r || doc).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); }
  function unitName(cfg) { return NS.skillSets[cfg.unitId].unitName; }
  function title(cfg) { return unitName(cfg) + ' ' + PR.kind(cfg.kind).name; }
  function lvName(cfg) { return (NS.LEVELS[cfg.level] || NS.LEVELS.cp1).long; }
  function verTag(n, v, key) { return n > 1 || key ? '<span class="mm-vtag' + (key ? ' mm-keytag' : '') + '">' + (key ? 'Teacher key' : '') + (n > 1 ? (key ? ' · ' : '') + 'Version ' + 'ABC'[v] : '') + '</span>' : ''; }
  function head(cfg, nV, v, key, sub, extra) {
    return '<div class="mm-head"><div><div class="mm-title">' + esc(title(cfg)) + (key ? ': Answer Key' : '') + '</div><div class="mm-sub">' + esc(sub || lvName(cfg)) + '</div></div>' + verTag(nV, v, key) + '</div>' +
      (key ? '' : '<div class="mm-name"><span>Name <i class="ln long"></i></span>' + (extra || '<span>Class / period <i class="ln mid"></i></span>') + '<span>Date <i class="ln mid"></i></span></div>');
  }
  function page(cfg, nV, v, key, inner) { return { html: '<div class="mm-body">' + inner + '</div>', foot: esc(title(cfg)) + (nV > 1 ? ' · Version ' + 'ABC'[v] : '') + (key ? ' · TEACHER KEY' : '') }; }
  function steps(p) { return (p.steps || []).filter(function (s) { return s.t || s.m; }).map(function (s) { return '<li>' + mathSafe(s.t) + (s.m ? ' ' + mathSafe('⟨' + s.m + '⟩') : '') + '</li>'; }).join(''); }
  function prompt(p) { return mathSafe(p.prompt) + (p.fig && NS.figHtml ? NS.figHtml(p.fig) : '') + (p.parts[0].prompt ? ' ' + mathSafe(p.parts[0].prompt) : ''); }
  function dirs(t) { return '<div class="mm-box mm-dirs pr-dirs"><b>Directions:</b> ' + t + '</div>'; }

  /* =========================== MAZE =========================== */
  /* Landscape, like the hand-made mazes: rounded rooms, door labels on the walls and in the corners, an
     answer grid; the key draws the path, numbers the rooms in order and outlines the doors on the path. */
  var MZ = { W: 10.15, H: 6.72, gx: 0.46, gy: 0.48 };
  function classicHead(cfg, nV, v, key, ttl, line, nameHtml) {
    return '<div class="pc-head"><div class="pc-title">' + esc(ttl) + (key ? ' <span class="pc-key">ANSWER KEY</span>' : '') + (nV > 1 ? ' <span class="pc-ver">Version ' + 'ABC'[v] + '</span>' : '') + '</div>' +
      (nameHtml === undefined ? '<div class="pc-name">Name <i class="ln long"></i> &nbsp; Period <i class="ln short"></i></div>' : nameHtml) + '</div>' + (line ? '<p class="pc-line">' + line + '</p>' : '');
  }
  /* "Find the slope of the line through ⟨…⟩." → a small instruction and the math in large type */
  function roomParts(p) {
    var t = String(p.prompt || ''), sn = t.match(/⟨[^⟩]*⟩/g) || [];
    var two = /^([^⟨]*?)[\s:]*(⟨[^⟩]*⟩) and (⟨[^⟩]*⟩)\s*\.?\s*$/.exec(t);   // "Solve the system by elimination: ⟨A⟩ and ⟨B⟩."
    if (two && !p.parts[0].prompt && PR.plain(two[2]).length <= 22 && PR.plain(two[3]).length <= 22) return { small: two[1] + ':', big: two[2] + '\n' + two[3] };
    if (sn.length !== 1 || p.parts[0].prompt || PR.plain(sn[0]).length > 30) return null;
    var at = t.indexOf(sn[0]), after = t.slice(at + sn[0].length).trim();
    if (after && after !== '.') return null;   // the math is in the middle of the sentence: print it as written
    var small = t.slice(0, at).replace(/[\s:]+$/, '');
    if (!small) return { small: '', big: sn[0] };
    return { small: small + (/\s/.test(small) ? ':' : '.'), big: sn[0] };
  }
  function roomHtml(p) {
    var rp = roomParts(p);
    if (rp) {
      var L = Math.max.apply(null, rp.big.split('\n').map(function (x) { return PR.plain(x).length; })), fz = Math.max(7, Math.min(13, 13 * 15 / Math.max(15, L)));
      return (rp.small ? '<div class="pm-small">' + mathSafe(rp.small.charAt(0).toUpperCase() + rp.small.slice(1)) + '</div>' : '') + '<div class="pm-big" style="font-size:' + fz.toFixed(1) + 'pt">' + rp.big.split('\n').map(mathSafe).join('<br>') + '</div>';
    }
    var Lm = Math.max.apply(null, [0].concat((String(p.prompt).match(/⟨[^⟩]*⟩/g) || []).map(function (x) { return PR.plain(x).length; })));
    return '<div class="pm-text" style="font-size:' + (10 * Math.min(1, 22 / Math.max(22, Lm))).toFixed(1) + 'pt">' + mathSafe(p.prompt) + (p.parts[0].prompt ? ' ' + mathSafe(p.parts[0].prompt) : '') + '</div>';
  }
  function mazeGeom(B) {
    var rw = (MZ.W - (B.C - 1) * MZ.gx) / B.C, rh = (MZ.H - (B.R - 1) * MZ.gy) / B.R;
    var X = function (c) { return c * (rw + MZ.gx); }, Y = function (r) { return r * (rh + MZ.gy); };
    return { rw: rw, rh: rh, X: X, Y: Y,
      center: function (r, c) { return [X(c) + rw / 2, Y(r) + rh * 0.45]; },
      door: function (d) {
        var r = Math.min(d.a[0], d.b[0]), c = Math.min(d.a[1], d.b[1]);
        if (d.kind === 'h') return { x: X(c) + rw + MZ.gx / 2, y: Y(r) + rh / 2, rot: -90, max: rh - 0.3 };   // door labels lie in the corridors, clear of the rooms
        if (d.kind === 'v') return { x: X(c) + rw / 2, y: Y(r) + rh + MZ.gy / 2, rot: 0, max: rw - 0.5 };
        return { x: X(c) + rw + MZ.gx / 2, y: Y(r) + rh + MZ.gy / 2, rot: d.kind === 'd' ? 45 : -45, max: 1.0 };
      } };
  }
  function mazeHtml(B, key) {
    var g = mazeGeom(B), h = '<div class="pm-maze" style="width:' + MZ.W + 'in;height:' + MZ.H + 'in">';
    if (key) {   // the path: room centers through the doors on the path
      var pts = [];
      B.path.forEach(function (q, i) {
        pts.push(g.center(q[0], q[1]));
        var nx = B.path[i + 1]; if (!nx) return;
        var d = B.doors.filter(function (x) { return x.correct && ((x.a.join() === q.join() && x.b.join() === nx.join()) || (x.b.join() === q.join() && x.a.join() === nx.join())); })[0];
        if (d) { var dp = g.door(d); pts.push([dp.x, dp.y]); }
      });
      h += '<svg class="pm-path" width="' + MZ.W + 'in" height="' + MZ.H + 'in" viewBox="0 0 ' + MZ.W * 96 + ' ' + MZ.H * 96 + '"><polyline points="' + pts.map(function (p) { return (p[0] * 96).toFixed(1) + ',' + (p[1] * 96).toFixed(1); }).join(' ') + '"/></svg>';
    }
    B.rooms.forEach(function (rm) {
      h += '<div class="pm-room' + (rm.finish ? ' fin' : '') + '" style="left:' + g.X(rm.c) + 'in;top:' + g.Y(rm.r) + 'in;width:' + g.rw + 'in;height:' + g.rh + 'in">' +
        (rm.r === 0 && rm.c === 0 ? '<span class="pm-start">START</span>' : '') +
        (rm.finish ? '<b>FINISH</b><small>You made it!</small>' : '<div class="pm-q">' + roomHtml(rm.item.p) + '</div>') + '</div>';
      if (key && rm.step !== null && !rm.finish) h += '<span class="pm-num" style="left:' + g.X(rm.c) + 'in;top:' + (g.Y(rm.r) + g.rh * 0.36) + 'in">' + (rm.step + 1) + '</span>';
    });
    B.doors.forEach(function (d) {
      var dp = g.door(d), L = PR.plain(d.label).length + (/\\frac/.test(d.label) ? 2 : 0) + 1.5, fz = Math.max(6, Math.min(8.8, dp.max * 72 / (L * 0.6)));
      h += '<div class="pm-door' + (key && d.correct ? ' ok' : '') + '" style="left:' + dp.x + 'in;top:' + dp.y + 'in;font-size:' + fz.toFixed(1) + 'pt;transform:translate(-50%,-50%) rotate(' + dp.rot + 'deg)"><span>' + mathSafe(d.label) + '</span></div>';
    });
    return h + '</div>';
  }
  function stepsInline(p) {
    var ms = (p.steps || []).filter(function (s) { return s.m; }).map(function (s) { return mathSafe('⟨' + s.m + '⟩'); });
    if (!ms.length) ms = (p.steps || []).map(function (s) { return mathSafe(s.t); });
    return ms.join(' <span class="pm-arrow">→</span> ');
  }
  function mazePages(cfg, B, v, nV, key) {
    var ttl = title(cfg), line = 'Start in the top-left room. Solve the problem, find the door with your answer, and go through it. Show your work on your answer grid.';
    var P = [{ land: true, nofoot: true, html: '<div class="mm-body pc">' + classicHead(cfg, nV, v, key, ttl, line) + mazeHtml(B, key) + '</div>' }];
    var rows = B.rooms.filter(function (r) { return r.step !== null && !r.finish; }).sort(function (a, b) { return a.step - b.step; });
    if (!key) {
      // A roomy 2-column × 5-row work grid. Longer mazes continue onto a second
      // answer page instead of squeezing boxes or omitting any room.
      for (var start = 0; start < rows.length; start += 10) {
        var part = rows.slice(start, start + 10);
        P.push({ nofoot: true, html: '<div class="mm-body pc">' +
          classicHead(cfg, nV, v, false, ttl + ': Answer Grid' + (start ? ' (continued)' : ''),
            'Show your work in each numbered box.') +
          '<div class="pm-answer-cards">' + part.map(function (r, i) {
            return '<section class="pm-answer-card"><span class="pm-answer-number">' + (start + i + 1) +
              '</span></section>';
          }).join('') + '</div></div>' });
      }
    } else {
      var rh = Math.min(0.78, 6.9 / rows.length);
      P.push({ land: true, nofoot: true, html: '<div class="mm-body pc">' +
        classicHead(cfg, nV, v, true, ttl + ': Answer Grid',
          'Answers and worked solutions for rooms on the correct path.', '') +
        '<table class="pm-grid">' + rows.map(function (r, i) {
          return '<tr style="height:' + rh + 'in"><td class="pm-gn"><span>' + (i + 1) +
            '</span></td><td class="pm-ga"><small>Answer:</small><div class="pm-gl"><b class="pc-red">' +
            mathSafe(r.item.key) + '</b></div></td><td class="pm-gw"><div class="pc-red pm-gs">' +
            stepsInline(r.item.p) + '</div></td></tr>';
        }).join('') + '</table></div>' });
    }
    if (key) {
      var dead = B.rooms.filter(function (r) { return r.step === null; });
      P.push({ land: true, nofoot: true, html: '<div class="mm-body pc">' + classicHead(cfg, nV, v, true, ttl + ': Dead-End Rooms', 'These rooms are not on the path. Their answers are on none of their doors.', '') +
        '<table class="pm-grid">' + dead.map(function (r) { return '<tr style="height:' + Math.min(1.1, 6.9 / dead.length) + 'in"><td class="pm-ga" style="width:3.6in">' + roomHtml(r.item.p) + '</td><td class="pm-ga"><b class="pc-red">' + mathSafe(r.item.key) + '</b></td><td class="pm-gw"><div class="pc-red pm-gs">' + stepsInline(r.item.p) + '</div></td></tr>'; }).join('') + '</table></div>' });
    }
    return P;
  }
  function chunkPages(cfg, nV, v, key, label, list, per, fn) {
    var headFor = function (i) { return '<div class="mm-head"><div><div class="mm-title mm-t2">' + esc(label) + (i ? ' (continued)' : '') + '</div><div class="mm-sub">' + esc(title(cfg)) + '</div></div>' + verTag(nV, v, key) + '</div>'; };
    return [{ flow: true, cfg: cfg, nV: nV, v: v, key: key, list: list, per: per, html: function (from, to) { return headFor(from) + fn(list.slice(from, to), from); } }];
  }
  function flow(cfg, nV, v, key, list, per, html) { return [{ flow: true, cfg: cfg, nV: nV, v: v, key: key, list: list, per: per, html: html }]; }
  function expandFlow(P) {
    var out = [], stage = doc.createElement('div'); stage.className = 'measure-stage'; stage.style.cssText = 'position:absolute;left:-10000px;top:0'; doc.body.appendChild(stage);
    P.forEach(function (p) {
      if (!p.flow) { out.push(p); return; }
      var i = 0;
      while (i < p.list.length) {
        var n = Math.min(p.per, p.list.length - i), pg;
        for (; n >= 1; n--) {
          pg = p.raw ? { html: p.html(i, i + n), nofoot: true } : page(p.cfg, p.nV, p.v, p.key, p.html(i, i + n));
          var e = doc.createElement('div'); e.className = 'page mm-page pr-page'; e.innerHTML = pg.html; stage.appendChild(e);
          var b = e.querySelector('.mm-body'), fits = b.scrollHeight <= b.clientHeight + 1; stage.removeChild(e);
          if (fits || n === 1) break;
        }
        out.push(pg); i += n;
      }
    });
    doc.body.removeChild(stage);
    return out;
  }

  /* =========================== COLOR BY NUMBER =========================== */
  /* Like the hand-made pages: a line drawing with numbered regions, a 10-color code (students write the problem
     number on each color's blank), and a page of problem boxes with "Color: ____" lines. */
  function sceneSvg(B, key) {
    var sc = PR.SCENES[B.scene], out = '<svg class="pc-scene" viewBox="0 0 600 560" xmlns="http://www.w3.org/2000/svg">';
    sc.groups.forEach(function (g) { out += '<g fill="' + (key ? PR.SCENE_COLORS[g.color] : '#fff') + '" stroke="#000" stroke-width="2.6" stroke-linejoin="round">' + g.shapes.join('') + '</g>'; });
    out += '<g fill="none" stroke="#000" stroke-width="2.6" stroke-linecap="round">' + (sc.extra || '') + '</g>';
    sc.groups.forEach(function (g, gi) {
      var light = !key || !/^(Black|Blue|Purple|Brown|Red|Green)$/.test(g.color);
      g.labels.forEach(function (pt) { out += '<text x="' + pt[0] + '" y="' + pt[1] + '" text-anchor="middle" dominant-baseline="middle" font-size="17" font-family="DejaVu Sans,Verdana,sans-serif" fill="' + (light ? '#000' : '#fff') + '">' + B.groupNum[gi] + '</text>'; });
    });
    return out + '</svg>';
  }
  function nameDate(key) { return '<div class="pc-nd"><span>Name: ' + (key ? '<b class="pc-redk">ANSWER KEY</b>' : '') + '<i class="ln long"></i></span><span>Date: <i class="ln mid"></i></span></div>'; }
  function colorCode(B, key) {
    return '<div class="pc-codeh">Color Code:</div><table class="pc-code"><tbody>' + [0, 1].map(function (row) {
      return '<tr>' + B.code.slice(row * 5, row * 5 + 5).map(function (k) {
        return '<td><div><span class="pc-blank">' + (key ? '<b class="pc-redk">' + k.num + '</b>' : '') + '</span> ' + esc(k.color) + '</div><div class="pc-ans">' + mathSafe(k.answer) + '</div></td>';
      }).join('') + '</tr>';
    }).join('') + '</tbody></table>';
  }
  function colorPages(cfg, B, v, nV, key) {
    var ttl = unitName(cfg) + ': Color By Number' + (nV > 1 ? ' (Version ' + 'ABC'[v] + ')' : '');
    var P = [{ nofoot: true, brand: true, html: '<div class="mm-body pc">' + nameDate(key) + '<div class="pc-ctitle">' + esc(ttl) + '</div><div class="pc-sbox">' + sceneSvg(B, key) + '</div>' + colorCode(B, key) + '</div>' }];
    if (!key) {
      P.push({ nofoot: true, brand: true, html: '<div class="mm-body pc">' + nameDate(false) + '<div class="pc-ctitle">' + esc(ttl) + '</div>' +
        '<p class="pc-dirs"><b>Directions:</b> Solve each problem and show your work in the box. Your answer matches one of the answers in the Color Code on the coloring sheet. Write the problem number on that color’s blank, then write the color on the line below. Color every part of the picture with that number. Watch out: some answers look alike!</p>' +
        '<div class="pc-boxes">' + B.items.map(function (it, i) {
          return '<div class="pc-box"><div class="pc-bq"><b>' + (i + 1) + '.</b><div>' + prompt(it.p) + '</div></div><div class="pc-bc">' + (i + 1) + '. Color: <i class="ln mid"></i></div></div>';
        }).join('') + '</div></div>' });
    } else {
      P = P.concat(chunkPages(cfg, nV, v, true, 'Answers and solutions', B.items.map(function (it, i) { return { it: it, i: i }; }), 10, function (l) {
        return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Problem</th><th>Answer and solution</th><th>Color</th></tr></thead><tbody>' + l.map(function (x) {
          var c = B.colorOf[x.i]; return '<tr><td><b>' + (x.i + 1) + '</b></td><td>' + prompt(x.it.p) + '</td><td><div class="mm-ans"><b>Answer:</b> ' + mathSafe(x.it.key) + '</div><ol class="mm-steps">' + steps(x.it.p) + '</ol></td><td><span class="pr-sw" style="background:' + PR.SCENE_COLORS[c] + '"></span>' + esc(c) + '</td></tr>'; }).join('') + '</tbody></table>';
      }));
    }
    return P;
  }

  /* =========================== PARTNER CHECK =========================== */
  function unitNo(cfg) {
    var lab = ''; NS.CATALOG.forEach(function (g) { g.units.forEach(function (u) { if (u[0] === cfg.unitId) lab = u[1]; }); });
    var m = /Units?\s+([\d–-]+)/.exec(lab); return m ? m[1] : '';
  }
  function partnerHead(cfg, nV, v, who, key) {
    var no = unitNo(cfg);
    return '<div class="pp-head"><div><div class="pp-unit">' + (no ? 'UNIT ' + no + ' • ' : '') + esc(unitName(cfg).toUpperCase()) + '</div><div class="pp-title">Partner Check: ' + esc(unitName(cfg)) +
      (key ? ' <span class="pc-key">ANSWER KEY</span>' : '') + (nV > 1 ? ' <span class="pc-ver">Version ' + 'ABC'[v] + '</span>' : '') + '</div></div>' + (who ? '<span class="pp-who">' + who + '</span>' : '') + '</div>';
  }
  function partnerPages(cfg, B, v, nV, key) {
    var P = [], no = unitNo(cfg), foot = 'Algebra Partner Check • ' + (no ? 'Unit ' + no + ': ' : '') + unitName(cfg);
    if (!key) ['A', 'B'].forEach(function (who) {
      var items = B.rows.map(function (r) { return r[who]; });
      var fl = flow(cfg, nV, v, false, items, 8, function (from, to) { return '<div class="mm-body pc pp">' + partnerHead(cfg, nV, v, who) + (from ? '' :
        '<div class="pp-names"><span>Name: <i class="ln long"></i></span><span>Partner’s name: <i class="ln long"></i></span><span>Date: <i class="ln mid"></i></span></div>' +
        '<div class="pp-dirs"><b>Directions:</b> Solve each problem. <i>Work on your own. Then compare answers with your partner after each problem. You have different problems with the same answers: if yours don’t match, find the mistake together before moving on.</i></div>' +
        '') + '<div class="pp-grid">' + items.slice(from, to).map(function (it, i0) {
          var i = from + i0;
          return '<div class="pp-box"><span class="pp-n">' + (i + 1) + '</span><div class="pp-q">' + prompt(it.p) + '</div><div class="pp-ans"><b>Answer:</b> <i class="ln long"></i><span>Match? ☐ Yes ☐ No</span></div></div>';
        }).join('') + '</div><div class="pp-foot"><span>' + esc(foot) + '</span><span>Partner ' + who + '</span></div></div>'; });
      fl[0].nofoot = true; fl[0].raw = true; P = P.concat(fl);
    });
    else P = chunkPages(cfg, nV, v, true, 'Partner Check: Answer Key', B.rows.map(function (r, i) { return { r: r, i: i }; }), 8, function (l) {
      return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Partner A</th><th>Partner B</th></tr></thead><tbody>' + l.map(function (x) {
        var cell = function (it) { return prompt(it.p) + '<div class="mm-ans"><b>Answer:</b> ' + mathSafe(it.key) + '</div><ol class="mm-steps">' + steps(it.p) + '</ol>'; };
        return '<tr><td><b>' + (x.i + 1) + '</b></td><td>' + cell(x.r.A) + '</td><td>' + cell(x.r.B) + '</td></tr>'; }).join('') + '</tbody></table>';
    });
    return P;
  }

  /* =========================== ERROR ANALYSIS =========================== */
  /* Like the hand-made pages: two problems per page, each with the original problem and the incorrect worked
     solution on the left, "A. Explain the mistake" and "B. Show correct work" on the right. */
  function workHtml(cs) {
    return '<div class="pe-lines">' + cs.work.map(function (l) { return '<div>' + mathSafe(l.t) + (l.m ? ' ' + mathSafe('⟨' + l.m + '⟩') : '') + '</div>'; }).join('') +
      (cs.work.some(function (l) { return l.bad; }) ? '' : '<div>' + (cs.work.length ? 'So the answer is ' : '') + mathSafe(cs.wrong) + '</div>') + '</div>';
  }
  function badLine(cs) { var k = -1; cs.work.forEach(function (l, i) { if (l.bad) k = i; }); return k; }
  function errorPages(cfg, B, v, nV, key) {
    var set = NS.skillSets[cfg.unitId], n = B.cases.length, pages = Math.ceil(n / 2), P = [];
    for (var pg = 0; pg < pages; pg++) {
      var h = '<div class="mm-body pc pe"><div class="pe-top"><div class="pe-title">' + esc(unitName(cfg)) + ' Error Analysis' + (key ? ' <span class="pe-badge">TEACHER KEY</span>' : '') + (nV > 1 ? ' <span class="pc-ver">Version ' + 'ABC'[v] + '</span>' : '') + '</div><span class="pe-pg">Page ' + (pg + 1) + ' of ' + pages + '</span></div>' +
        '<div class="pe-sub">Find the mistake. Explain it. Fix it.</div><div class="pe-names"><span>Name: <i class="ln long"></i></span><span>Period: <i class="ln short"></i></span><span>Date: <i class="ln mid"></i></span></div>';
      B.cases.slice(pg * 2, pg * 2 + 2).forEach(function (cs, k) {
        var no = pg * 2 + k + 1, bl = badLine(cs), sk = set.byId[cs.item.skill];
        h += '<div class="pe-box"><div class="pe-h">' + no + '. ' + esc(sk ? sk.name : 'Problem') + '</div><div class="pe-cols"><div class="pe-l">' +
          '<div class="pe-cap">Original problem</div><div class="pe-q">' + prompt(cs.item.p) + '</div><div class="pe-cap">' + esc(cs.name) + '’s incorrect worked solution</div>' + workHtml(cs) + '</div><div class="pe-r">' +
          '<div class="pe-cap">A. Explain the mistake (1 point)</div>' + (key ? '<div class="pe-green">' + (bl >= 0 ? 'Step ' + (bl + 1) + ' is wrong: it should give ' : 'The final answer is wrong; it should be ') + mathSafe(cs.item.key) + ', not ' + mathSafe(cs.wrong) + '.</div>' : '<div class="pe-hint">Describe exactly which step is wrong and why.</div><i class="ln full"></i><i class="ln full"></i><i class="ln full"></i>') +
          '<div class="pe-cap">B. Show correct work (1 point)</div>' + (key ? '<div class="pe-green"><ol class="mm-steps">' + steps(cs.item.p) + '</ol><b>Answer:</b> ' + mathSafe(cs.item.key) + '</div>' : '<i class="ln full"></i><i class="ln full"></i><i class="ln full"></i><i class="ln full"></i>') +
          '</div></div></div>';
      });
      h += '<div class="pe-foot">Scoring: Explanation = 1 point • Correct work/answer = 1 point • Total = ' + 2 * n + ' points</div></div>';
      P.push({ nofoot: true, html: h });
    }
    return P;
  }

  /* =========================== TARSIA =========================== */
  var S3 = Math.sqrt(3);
  function orient(t) { var a = t[0], b = t[1], c = t[2]; var ax = a[0] + a[1] / 2, ay = a[1] * S3 / 2, bx = b[0] + b[1] / 2, by = b[1] * S3 / 2, cx = c[0] + c[1] / 2, cy = c[1] * S3 / 2; return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) > 0 ? [0, 1, 2] : [2, 1, 0]; }
  function tarsiaSvg(B, key, layout, section) {
    layout = layout || 'standard';
    var pts = []; B.pieces.forEach(function (p) { p.pts.forEach(function (q) { pts.push(q); }); });
    var X = function (q) { return q[0] + q[1] / 2; }, Y = function (q) { return -q[1] * S3 / 2; };
    var minX = Math.min.apply(null, pts.map(X)), maxX = Math.max.apply(null, pts.map(X)), minY = Math.min.apply(null, pts.map(Y)), maxY = Math.max.apply(null, pts.map(Y));
    var large = layout === 'large';
    var sIn = large ? 3.0 : Math.min((layout === 'compact' ? 6.5 : 7.3) / (maxX - minX), (layout === 'compact' ? 5.8 : 6.5) / (maxY - minY));
    var s = sIn * 96, W = large ? 7.0 * 96 : (maxX - minX) * s, H = large ? 8.0 * 96 : (maxY - minY) * s;
    var px = function (q) { return [(X(q) - minX) * s, (Y(q) - minY) * s]; };
    var fs = large ? 13 : (sIn > 1.6 ? 8 : 7.4);
    var out = '<svg class="pr-tsvg" width="' + (W / 96) + 'in" height="' + (H / 96) + 'in" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg">';
    var slots = key ? B.pieces.map(function (_, i) { return { piece: i, slot: i, turn: 0 }; }) : B.scrambled;
    if (large) slots = slots.slice((section || 0) * 6, ((section || 0) + 1) * 6);
    slots.forEach(function (sl, si) {
      var slot = B.pieces[sl.slot].pts, pc = B.pieces[sl.piece], P = slot.map(px);
      if (large) {
        var bx = Math.min.apply(null, P.map(function (q) { return q[0]; })), by = Math.min.apply(null, P.map(function (q) { return q[1]; }));
        P = P.map(function (q) { return [q[0] - bx + (si % 2) * 3.55 * 96 + 8, q[1] - by + Math.floor(si / 2) * 2.65 * 96 + 4]; });
      }
      var cx = (P[0][0] + P[1][0] + P[2][0]) / 3, cy = (P[0][1] + P[1][1] + P[2][1]) / 3;
      out += '<polygon points="' + P.map(function (q) { return q.join(','); }).join(' ') + '" fill="#fff" stroke="#000" stroke-width="1.2"/>';
      var po = orient(pc.pts), so = orient(slot), E = [[0, 1], [1, 2], [2, 0]];
      for (var k = 0; k < 3; k++) {
        var txt = pc.text[po[k]]; if (!txt) continue;
        var e = E[so[(k + sl.turn) % 3]], A = P[e[0]], Bp = P[e[1]], mx = (A[0] + Bp[0]) / 2, my = (A[1] + Bp[1]) / 2;
        var nx = cx - mx, ny = cy - my, nl = Math.sqrt(nx * nx + ny * ny); nx /= nl; ny /= nl;
        var edge = Math.hypot(Bp[0] - A[0], Bp[1] - A[1]);
        var len = edge * 0.58, d = edge * 0.12, ang = Math.atan2(nx, -ny) * 180 / Math.PI;
        // Stacked fractions need substantially more vertical room than plain text.
        var ox = mx + nx * d, oy = my + ny * d, hh = edge * 0.13;
        out += '<foreignObject x="' + (ox - len / 2) + '" y="' + (oy - hh / 2) + '" width="' + len + '" height="' + hh + '" transform="rotate(' + ang.toFixed(2) + ' ' + ox + ' ' + oy + ')"><div xmlns="http://www.w3.org/1999/xhtml" class="pr-tt' + (key && pc.kind[po[k]] === 'q' ? ' q' : '') + '" style="font-size:' + fs.toFixed(2) + 'pt"><span>' + mathSafe(txt) + '</span></div></foreignObject>';
      }
    });
    return out + '</svg>';
  }
  function tarsiaHead(cfg, nV, v, ttl, sub, nameOn) {
    return '<div class="pt-head"><div class="pt-title">' + esc(ttl) + (nV > 1 ? ' <span class="pc-ver">Version ' + 'ABC'[v] + '</span>' : '') + '</div><div class="pt-subrow"><span>' + esc(sub) + '</span>' + (nameOn ? '<span>Name: <i class="ln long"></i></span>' : '') + '</div></div>';
  }
  function tarsiaPages(cfg, B, v, nV, key) {
    var layout = cfg.tarsiaLayout || 'standard', large = layout === 'large';
    var P = [], n = B.items.length, ttl = unitName(cfg) + ' Tarsia', shape = B.shape === 'hexagon' ? 'Hexagon' : 'Triangle';
    if (!key) {
      P.push({ nofoot: true, html: '<div class="mm-body pc pt">' + tarsiaHead(cfg, nV, v, ttl, 'Mr. K’s Classroom · ' + shape + ' of ' + B.pieces.length + ' triangles, ' + n + ' matches', true) +
        '<div class="pt-dirs"><b>Directions:</b> Solve each problem. Cut out the ' + B.pieces.length + ' triangles. Match each problem to its answer so that touching edges fit, and build a <b>' + B.shape + '</b>. Glue it on a sheet of paper. Show your work for every problem on the work pages (the number before each problem tells you where).</div>' +
        '<div class="pr-tbox">' + tarsiaSvg(B, false, layout, 0) + '</div></div>' });
      if (large) for (var ls = 1; ls < Math.ceil(B.pieces.length / 6); ls++) P.push({ nofoot: true, html: '<div class="mm-body pc pt">' + tarsiaHead(cfg, nV, v, ttl, 'Large print · Cut-out sheet ' + (ls + 1), false) + '<div class="pr-tbox">' + tarsiaSvg(B, false, layout, ls) + '</div></div>' });
      var sorted = B.items.slice().sort(function (a, b) { return a.num - b.num; });
      for (var i = 0; i < n; i += 15) P.push({ nofoot: true, html: '<div class="mm-body pc pt">' + tarsiaHead(cfg, nV, v, 'Show Your Work', ttl + ' · Problems ' + (i + 1) + '–' + Math.min(n, i + 15), true) +
        '<div class="pt-grid">' + sorted.slice(i, i + 15).map(function (it) { return '<div><b>' + it.num + '.</b><div>' + mathSafe(it.p.prompt) + '</div></div>'; }).join('') + '</div></div>' });
    } else {
      P.push({ nofoot: true, html: '<div class="mm-body pc pt">' + tarsiaHead(cfg, nV, v, ttl + ': Answer Key', 'Solved ' + B.shape + '. Each shared edge pairs a problem with its answer.', false) + '<div class="pr-tbox">' + tarsiaSvg(B, true, layout, 0) + '</div></div>' });
      if (large) for (var ks = 1; ks < Math.ceil(B.pieces.length / 6); ks++) P.push({ nofoot: true, html: '<div class="mm-body pc pt">' + tarsiaHead(cfg, nV, v, ttl + ': Answer Key', 'Large print · Solution sheet ' + (ks + 1), false) + '<div class="pr-tbox">' + tarsiaSvg(B, true, layout, ks) + '</div></div>' });
      var list = B.items.slice().sort(function (a, b) { return a.num - b.num; });
      P = P.concat(chunkPages(cfg, nV, v, true, 'Answers', list, 15, function (l) {
        return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Problem</th><th>Answer</th><th>Solution</th></tr></thead><tbody>' + l.map(function (it) {
          return '<tr><td><b>' + it.num + '</b></td><td>' + mathSafe(it.p.prompt) + '</td><td>' + mathSafe(it.key) + '</td><td><ol class="mm-steps">' + steps(it.p) + '</ol></td></tr>'; }).join('') + '</tbody></table>';
      }));
    }
    return P;
  }

  /* =========================== WHODUNNIT =========================== */
  /* Like the hand-made whodunnits: a case page with the story and case board, a Show Your Work page, and clue
     cards two to a page (cut apart and post them around the room). The key names the culprit, maps each card
     to what it clears, and gives every worked solution and every wrong choice's false clue. */
  var LET = 'ABCD';
  function whoHead(ttl, sub, nameOn, key, nV, v) {
    return '<div class="pw-row"><div><div class="pw-mono pw-ttl">' + esc(ttl) + (key ? ' <span class="pc-key">ANSWER KEY</span>' : '') + (nV > 1 ? ' <span class="pc-ver">Version ' + 'ABC'[v] + '</span>' : '') + '</div><div class="pw-sub">' + sub + '</div></div>' +
      (nameOn ? '<div class="pw-nm">Name: <i class="ln long"></i></div>' : '') + '</div><div class="pw-rule"></div>';
  }
  function cardProblem(p) { return '<div class="pw-cq">' + prompt(p) + '</div>'; }
  function whoPages(cfg, B, v, nV, key) {
    var S = B.S, no = unitNo(cfg), sub = 'Whodunnit? · ' + (no ? 'Unit ' + no + ': ' : '') + esc(unitName(cfg)), P = [];
    var clears = function (t) { return t.p !== undefined ? 'Suspect: ' + esc(S.suspects[t.p].n) + ' · Place: ' + esc(S.places[t.l].n) : 'Method: ' + esc(S.methods[t.m].n); };
    if (!key) {
      P.push({ nofoot: true, html: '<div class="mm-body pc pw">' + whoHead(S.name, sub, true, false, nV, v) +
        '<p class="pw-intro">' + S.intro + '</p><p class="pw-intro">Six people were at ' + esc(S.where) + ', each seen in a different spot, and there are six sneaky ways the thief could have gotten away. You are the lead detective. Find out <b>who</b> took it, <b>where</b> they were, and <b>how</b> they did it.</p>' +
        '<div class="pw-box"><h3>How to crack the case</h3><ol><li>Your teacher will post <b>10 clue cards</b> around the room. Each card has a math problem and four answer choices. Every choice is paired with a clue.</li><li>Solve the problem on the <b>Show Your Work</b> page. Find your answer among the choices and read the clue next to it. If your answer is not there, check your work.</li><li>Use the clue to cross out suspects, places or methods on the case board below. Write the card number beside what it cleared.</li><li>After all 10 cards, exactly one suspect, one place and one method are left. Those three name the culprit. If you end up with none, or more than one, a clue went wrong: recheck your math!</li></ol></div>' +
        '<div class="pw-board"><div><h4>The Suspects</h4>' + S.suspects.map(function (x) { return '<div class="pw-bi"><i></i><span>' + esc(x.n) + '<small>' + esc(x.r) + '</small></span></div>'; }).join('') + '</div>' +
        '<div><h4>The Places</h4>' + S.places.map(function (x) { return '<div class="pw-bi"><i></i><span>' + esc(x.n) + '</span></div>'; }).join('') + '</div>' +
        '<div><h4>The Methods</h4>' + S.methods.map(function (x) { return '<div class="pw-bi"><i></i><span>' + esc(x.n) + '</span></div>'; }).join('') + '</div></div>' +
        '<div class="pw-culprit">The culprit is <i class="ln mid"></i> in the <i class="ln mid"></i> using <i class="ln mid"></i></div></div>' });
      P.push({ nofoot: true, html: '<div class="mm-body pc pw">' + whoHead('Show Your Work', esc(S.name) + ' · Show every step in the matching box.', true, false, nV, v) +
        '<div class="pw-wgrid">' + B.cards.map(function (_, i) { return '<div>' + (i + 1) + '.<small>Choice ______</small></div>'; }).join('') + '</div></div>' });
      var fl = flow(cfg, nV, v, false, B.cards, 2, function (from, to) {
        return '<div class="mm-body pc pw">' + B.cards.slice(from, to).map(function (c, k) {
          return '<div class="pw-card">' + (k ? '<span class="pw-cut">✂ cut here</span>' : '') + '<div class="pw-ch"><span class="pw-mono">Clue #' + (from + k + 1) + '</span><span>' + esc(S.name) + '</span></div>' + cardProblem(c.item.p) +
            '<table class="pw-opts">' + c.opts.map(function (o, j) { return '<tr><td><b>' + LET[j] + '.</b> ' + mathSafe(o.a) + '</td><td>' + esc(o.clue) + '</td></tr>'; }).join('') + '</table><div class="pw-cf">Solve the problem, find your answer, and read its clue. Cross it off on your case board.</div></div>';
        }).join('') + '</div>';
      });
      fl[0].raw = true; fl[0].nofoot = true; P = P.concat(fl);
    } else {
      var C = B.culprit;
      P.push({ nofoot: true, html: '<div class="mm-body pc pw">' + whoHead(S.name, sub + ' · Teacher Guide', false, true, nV, v) +
        '<div class="pw-sol">' + esc(S.suspects[C.p].n) + ' · ' + esc(S.places[C.l].n) + ' · ' + esc(S.methods[C.m].n) + '</div>' +
        '<p><b>Setup:</b> print the clue cards (two per page), cut them apart and post them around the room. Give each student the case page and the Show Your Work page. Students can start at any card. Teams of 2–3 work well; plan on 25–40 minutes.</p>' +
        '<p><b>How it works:</b> each correct answer leads to a true clue. Five true clues clear an innocent suspect AND the place where they were; the other five clear an innocent method. Each wrong answer (every one is checked to be wrong) leads to a false clue: some clear the culprit, the crime scene or the real method, and the rest clear only innocent things. Either way the card’s true clue is missed, so a mistake leaves the board with none, or more than one, of something.</p>' +
        '<table class="pw-k"><thead><tr><th>Card</th><th>Correct choice</th><th>Clears</th></tr></thead><tbody>' + B.cards.map(function (c, i) {
          return '<tr><td><b>' + (i + 1) + '</b></td><td><b>' + LET[c.pos] + '.</b> ' + mathSafe(c.item.key) + '</td><td>' + clears(c.truth) + '</td></tr>'; }).join('') + '</tbody></table>' +
        '<p><b>Solution:</b> ' + esc(S.suspects[C.p].n) + ' was in the ' + esc(S.places[C.l].n) + ' and got away with ' + esc(S.item) + ': ' + esc(S.methods[C.m].n.toLowerCase()) + '. Every other suspect, place and method was cleared by a true clue.</p></div>' });
      P = P.concat(chunkPages(cfg, nV, v, true, 'Answer Key: worked solutions', B.cards.map(function (c, i) { return { c: c, i: i }; }), 10, function (l) {
        return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Problem</th><th>Answer and solution</th><th>True clue</th></tr></thead><tbody>' + l.map(function (x) {
          return '<tr><td><b>' + (x.i + 1) + '</b></td><td>' + prompt(x.c.item.p) + '</td><td><div class="mm-ans"><b>' + LET[x.c.pos] + '.</b> ' + mathSafe(x.c.item.key) + '</div><ol class="mm-steps">' + steps(x.c.item.p) + '</ol></td><td>' + esc(x.c.truth.text) + '</td></tr>'; }).join('') + '</tbody></table>';
      }));
      var WHAT = { p: 'clears the culprit', l: 'clears the crime scene', m: 'clears the real method', x: 'clears only innocent things, but the true clue is missed' };
      P = P.concat(chunkPages(cfg, nV, v, true, 'Wrong choices and their false clues', B.cards.map(function (c, i) { return { c: c, i: i }; }), 10, function (l) {
        return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>Card</th><th>Wrong choice</th><th>False clue</th><th>Why it misleads</th></tr></thead><tbody>' + l.map(function (x) {
          return x.c.opts.map(function (o, j) { return o.ok ? '' : '<tr><td>' + (x.i + 1) + '</td><td><b>' + LET[j] + '.</b> ' + mathSafe(o.a) + '</td><td>' + esc(o.clue) + '</td><td>' + WHAT[o.clears] + '</td></tr>'; }).join(''); }).join('') + '</tbody></table>';
      }));
    }
    return P;
  }

  /* =========================== STATIONS =========================== */
  /* Like the hand-made stations: "Algebra Review: Unit N — name", a boxed "Station i of n" title, name and date,
     problems with room to work; one key page with every answer. */
  function stationPages(cfg, B, v, nV, key) {
    var no = unitNo(cfg), hd = 'Algebra Review: ' + (no ? 'Unit ' + no + ' — ' : '') + unitName(cfg), n = B.stations.length, P = [];
    var foot = function (r) { return '<div class="ps-ft"><span>Mr. K’s Classroom • Algebra • ' + (no ? 'Unit ' + no + ': ' : '') + esc(unitName(cfg)) + '</span><span>' + r + '</span></div>'; };
    var vt = nV > 1 ? ' <span class="pc-ver">Version ' + 'ABC'[v] + '</span>' : '';
    if (!key) B.stations.forEach(function (st, si) {
      var fl = flow(cfg, nV, v, false, st.items, st.items.length, function (from, to) {
        return '<div class="mm-body pc ps"><div class="ps-hd">' + esc(hd) + vt + '</div><div class="ps-st"><b>Station ' + (si + 1) + ' of ' + n + ':</b> ' + esc(st.title) + (from ? ' (continued)' : '') + '</div>' +
          (from ? '' : '<div class="ps-nm"><span>Name: <i class="ln long"></i></span><span>Date: <i class="ln mid"></i></span></div><div class="ps-note">Show your work. Circle or box your final answer.</div>') +
          '<div class="ps-qs">' + st.items.slice(from, to).map(function (it, k) { return '<div class="ps-q"><b>' + (from + k + 1) + '.</b><div>' + prompt(it.p) + '</div></div>'; }).join('') + '</div>' + foot('Station ' + (si + 1)) + '</div>';
      });
      fl[0].raw = true; fl[0].nofoot = true; P = P.concat(fl);
    });
    else {
      var fl = flow(cfg, nV, v, true, B.stations, n, function (from, to) {
        return '<div class="mm-body pc ps"><div class="ps-hd">' + esc(hd) + vt + '<div class="ps-ak">Answer Key</div></div>' + B.stations.slice(from, to).map(function (st, k) {
          return '<h3 class="ps-kh">Station ' + (from + k + 1) + ': ' + esc(st.title) + '</h3><div class="ps-kg">' + st.items.map(function (it, i) { return '<div><b>' + (i + 1) + '.</b> ' + mathSafe(it.key) + '</div>'; }).join('') + '</div>';
        }).join('') + foot('Answer Key') + '</div>';
      });
      fl[0].raw = true; fl[0].nofoot = true; P = P.concat(fl);
      P = P.concat(chunkPages(cfg, nV, v, true, 'Worked solutions', [].concat.apply([], B.stations.map(function (st, si) { return st.items.map(function (it, i) { return { it: it, s: si, i: i }; }); })), 12, function (l) {
        return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Problem</th><th>Answer and solution</th></tr></thead><tbody>' + l.map(function (x) {
          return '<tr><td><b>' + (x.s + 1) + '.' + (x.i + 1) + '</b></td><td>' + prompt(x.it.p) + '</td><td><div class="mm-ans"><b>Answer:</b> ' + mathSafe(x.it.key) + '</div><ol class="mm-steps">' + steps(x.it.p) + '</ol></td></tr>'; }).join('') + '</tbody></table>';
      }));
    }
    return P;
  }

  PR.pages = function (cfg, B, v, nV, key) {
    return ({ maze: mazePages, color: colorPages, partner: partnerPages, error: errorPages, tarsia: tarsiaPages, who: whoPages, stations: stationPages })[cfg.kind](cfg, B, v, nV, key);
  };
  PR.pageEls = function (cfg, B, v, nV, key) {
    var P = expandFlow(PR.pages(cfg, B, v, nV, key));
    return P.map(function (p, i) {
      var e = doc.createElement('div'); e.className = 'page mm-page pr-page' + (p.land ? ' pr-land' : '') + (p.cls ? ' ' + p.cls : '');
      e.innerHTML = p.html + (p.nofoot ? (p.brand ? '<div class="pc-brand">Mr. K\'s Classroom</div>' : '') : '<div class="mm-foot"><span>' + p.foot + '</span><span>Page ' + (i + 1) + ' of ' + P.length + '</span></div>');
      return e;
    });
  };

  /* =========================== interface =========================== */
  var app = $('#prApp'); if (!app) return;
  var KEY = 'mk-printables-v1';
  function lsGet(k) { try { return G.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { G.localStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  function hashArg(n) { var m = new RegExp(n + '=([a-z0-9\\-]+)').exec(G.location.hash || ''); return m ? m[1] : null; }
  var unit = hashArg('unit'); if (!NS.skillSets[unit]) unit = doc.body.getAttribute('data-unit') || Object.keys(NS.skillSets)[0];
  var kind = hashArg('kind'); if (!PR.kind(kind)) kind = 'maze';
  /* A printable is offered for a unit only when at least one of its skills can fill it (Geometry problems carry diagrams, so Maze and Tarsia need none of them). */
  function supported(u, k) { if (k === 'vocabulary' || !PR.MODES[k]) return true; return NS.skillSets[u].skills.some(function (sk) { return PR.capable(u, sk.id, k); }); }
  function firstSupported(u, k) { if (supported(u, k)) return k; var f = PR.KINDS.filter(function (x) { return supported(u, x.id); })[0]; return f ? f.id : k; }
  kind = firstSupported(unit, kind);
  var cfg = null, built = [], ui = { doc: 'student', v: 0 };
  function load() {
    var raw = lsGet(KEY + ':' + unit + ':' + kind); cfg = null;
    try { var o = JSON.parse(raw); if (o && o.unitId === unit && o.kind === kind) cfg = o; } catch (e) { cfg = null; }
    if (!cfg) cfg = PR.defaultConfig(unit, kind);
    NS.skillSets[unit].skills.forEach(function (s) { if (cfg.skills[s.id] === undefined) cfg.skills[s.id] = true; });
    var d = PR.defaultConfig(unit, kind); ['story', 'stations', 'perStation', 'tarsiaLayout'].forEach(function (k) { if (cfg[k] === undefined) cfg[k] = d[k]; });
  }
  function save() { lsSet(KEY + ':' + unit + ':' + kind, JSON.stringify(cfg)); }
  function setHash() { try { G.history.replaceState(null, '', '#unit=' + unit + '&kind=' + kind); } catch (e) { /* ignore */ } }
  function unitOptions() {
    return NS.CATALOG.map(function (g) { return '<optgroup label="' + esc(g.course) + '">' + g.units.filter(function (u) { return NS.skillSets[u[0]]; }).map(function (u) { return '<option value="' + u[0] + '"' + (u[0] === unit ? ' selected' : '') + '>' + esc(u[1]) + '</option>'; }).join('') + '</optgroup>'; }).join('');
  }
  function controls() {
    var set = NS.skillSets[unit], k = PR.kind(kind);
    var h = '<section class="card"><h2>Activity</h2><label class="field"><span class="lbl">Unit</span><select id="prUnit">' + unitOptions() + '</select></label>' +
      '<fieldset class="field pr-kinds"><legend class="lbl">Printable</legend>' + PR.KINDS.map(function (x) { var ok = supported(unit, x.id); return '<label class="chk' + (ok ? '' : ' off') + '"><input type="radio" name="prKind" value="' + x.id + '"' + (x.id === kind ? ' checked' : '') + (ok ? '' : ' disabled') + '><span>' + esc(x.name) + '<small>' + (ok ? esc(x.blurb) : 'Not available for this unit: its problems need a diagram, and this printable has no room for one.') + '</small></span></label>'; }).join('') + '</fieldset></section>';
    if (kind === 'vocabulary') return h + '<section class="card"><h2>Vocabulary settings</h2><p class="hint">Choose terms, class level, mastery progression, activity types, and question counts in the builder on the right. Preview, print, and teacher answer keys are available there.</p></section>';
    h += '<section class="card"><h2>Level and skills</h2><div class="pr-levels">' + Object.keys(NS.LEVELS).map(function (id) { return '<label class="chk"><input type="radio" name="prLevel" value="' + id + '"' + (cfg.level === id ? ' checked' : '') + '><span>' + esc(NS.LEVELS[id].long) + '</span></label>'; }).join('') + '</div>' +
      '<p class="hint">Skills this printable cannot use are greyed out (for example, problems answered with a graph cannot go on a maze door).</p>' +
      set.skills.map(function (s) { var cap = PR.capable(unit, s.id, kind); return '<label class="chk' + (cap ? '' : ' off') + '"><input type="checkbox" class="prSkill" value="' + s.id + '"' + (cfg.skills[s.id] && cap ? ' checked' : '') + (cap ? '' : ' disabled') + '><span>' + esc(s.name) + (cap ? '' : '<small>Not available for a ' + esc(k.name.toLowerCase()) + '</small>') + '</span></label>'; }).join('') + '</section>';
    var story = kind === 'who' ? '<label class="field"><span class="lbl">Case</span><select id="prStory"><option value="auto">Surprise me</option>' + Object.keys(PR.CASES).map(function (id) { return '<option value="' + id + '"' + (cfg.story === id ? ' selected' : '') + '>' + esc(PR.CASES[id].name) + '</option>'; }).join('') + '</select></label><p class="hint">The culprit, place and method change with every new set of problems.</p>' : '';
    var st = kind === 'stations' ? '<label class="field"><span class="lbl">Stations</span><select id="prSt">' + [2, 3, 4, 5, 6].map(function (n) { return '<option value="' + n + '"' + ((cfg.stations | 0 || 4) === n ? ' selected' : '') + '>' + n + ' stations</option>'; }).join('') + '</select></label>' +
      '<label class="field"><span class="lbl">Problems per station</span><select id="prPer">' + [6, 8, 10].map(function (n) { return '<option value="' + n + '"' + ((cfg.perStation | 0 || 8) === n ? ' selected' : '') + '>' + n + ' problems</option>'; }).join('') + '</select></label><p class="hint">The checked skills are split, in order, across the stations (never more stations than skills).</p>' : '';
    h += '<section class="card"><h2>Options</h2>' + story + st + (kind === 'tarsia' ? '<label class="field"><span class="lbl">Print layout</span><select id="prTarsiaLayout">' + [['standard','Standard · full puzzle'],['large','Large Print · 6 pieces per page'],['compact','Compact · smaller full puzzle']].map(function (x) { return '<option value="' + x[0] + '"' + ((cfg.tarsiaLayout || 'standard') === x[0] ? ' selected' : '') + '>' + x[1] + '</option>'; }).join('') + '</select></label>' : '') + (kind === 'color' ? '<label class="field"><span class="lbl">Picture</span><select id="prPic"><option value="auto">Surprise me</option>' + Object.keys(PR.SCENES).map(function (id) { return '<option value="' + id + '"' + (cfg.picture === id ? ' selected' : '') + '>' + esc(PR.SCENES[id].name) + '</option>'; }).join('') + '</select></label>' : '') +
      '<label class="field"><span class="lbl">Versions</span><select id="prVer">' + [1, 2, 3].map(function (n) { return '<option value="' + n + '"' + ((cfg.versions | 0) === n ? ' selected' : '') + '>' + ['Version A only', 'Versions A and B', 'Versions A, B and C'][n - 1] + '</option>'; }).join('') + '</select></label>' +
      '<p><button type="button" class="btn" id="prNew">↻ New problems</button></p><p class="hint">Every answer is checked independently. Every wrong label (a maze door, a Tarsia edge, a student’s wrong answer) is checked to be wrong.</p></section>';
    return h;
  }
  function render() {
    $('#prControls').innerHTML = controls();
    $('#prUnit').onchange = function (e) { unit = e.target.value; kind = firstSupported(unit, kind); load(); setHash(); rebuild(); };
    $$('input[name=prKind]').forEach(function (r) { r.onchange = function () { kind = r.value; load(); setHash(); rebuild(); }; });
    $$('input[name=prLevel]').forEach(function (r) { r.onchange = function () { cfg.level = r.value; save(); rebuild(); }; });
    $$('.prSkill').forEach(function (b) { b.onchange = function () { cfg.skills[b.value] = b.checked; save(); rebuild(); }; });
    if ($('#prTarsiaLayout')) $('#prTarsiaLayout').onchange = function (e) { cfg.tarsiaLayout = e.target.value; save(); drawPreview(); };
    if ($('#prStory')) $('#prStory').onchange = function (e) { cfg.story = e.target.value; save(); rebuild(); };
    if ($('#prSt')) $('#prSt').onchange = function (e) { cfg.stations = +e.target.value; save(); rebuild(); };
    if ($('#prPer')) $('#prPer').onchange = function (e) { cfg.perStation = +e.target.value; save(); rebuild(); };
    if ($('#prPic')) $('#prPic').onchange = function (e) { cfg.picture = e.target.value; save(); rebuild(); };
    if (kind === 'vocabulary') { doc.title = 'Vocabulary Builder · Mr. K\'s Classroom'; $('#prCrumb').textContent = 'Printable Generator · Vocabulary Builder'; return; }
    $('#prVer').onchange = function (e) { cfg.versions = +e.target.value; save(); rebuild(); };
    $('#prNew').onclick = function () { cfg.seed = Math.floor(Math.random() * 1e9); save(); rebuild(); };
    doc.title = PR.kind(kind).name + ' Generator · Mr. K\'s Classroom';
    $('#prCrumb').textContent = 'Printable Generator · ' + PR.kind(kind).name;
  }
  function rebuild() {
    render();
    if (kind === 'vocabulary') { built = []; $('#prPreview').innerHTML = '<iframe title="Vocabulary Builder: worksheet settings and printable preview" src="vocabulary.html?embedded=1&unit=' + encodeURIComponent(unit) + '" style="width:100%;min-height:1420px;border:1px solid #d4dfea;border-radius:12px;background:white" loading="eager"></iframe>'; return; }
    var pv = $('#prPreview'); pv.innerHTML = '<div class="pr-busy">Making and checking problems…</div>';
    setTimeout(function () {
      built = [];
      for (var v = 0; v < (cfg.versions | 0 || 1); v++) built.push(PR.build(cfg, v));
      if (ui.v >= built.length) ui.v = 0;
      drawPreview();
    }, 30);
  }
  function drawPreview() {
    var pv = $('#prPreview'), err = built.filter(function (b) { return b.error; })[0];
    var tools = '<div class="ptool"><div class="grp" role="group" aria-label="Document"><button type="button" class="tab" data-doc="student" aria-pressed="' + (ui.doc === 'student') + '">Student copy</button><button type="button" class="tab" data-doc="key" aria-pressed="' + (ui.doc === 'key') + '">Answer key</button></div>' +
      (built.length > 1 ? '<div class="grp" role="group" aria-label="Version">' + built.map(function (_, i) { return '<button type="button" class="tab" data-ver="' + i + '" aria-pressed="' + (ui.v === i) + '">Version ' + 'ABC'[i] + '</button>'; }).join('') + '</div>' : '') +
      '<span class="sp"></span><button type="button" class="btn" id="prPrintS"' + (err ? ' disabled' : '') + '>Print student copies</button><button type="button" class="btn ghost" id="prPrintK"' + (err ? ' disabled' : '') + '>Print answer keys</button></div>';
    if (err) { pv.innerHTML = tools + '<div class="pr-err">' + esc(err.error) + '</div>'; bindTools(); return; }
    pv.innerHTML = tools + (built[ui.v].levelNote ? '<div class="pr-busy">' + esc(built[ui.v].levelNote) + '</div>' : '') + '<div class="pr-pages"></div>';
    var box = $('.pr-pages', pv);
    PR.pageEls(cfg, built[ui.v], ui.v, built.length, ui.doc === 'key').forEach(function (p) { var w = doc.createElement('div'); w.className = 'pr-pwrap'; w.appendChild(p); box.appendChild(w); });
    fit(); fitTarsiaLabels(pv); bindTools();
  }
  /* Fit the rendered KaTeX, not a character-count estimate. Keep each label inside
     its own edge strip, including rotated labels and stacked fractions. */
  function fitTarsiaLabels(root) {
    // Measure content in the edge's own unrotated coordinate system.
    $$('.pr-tsvg foreignObject', root).forEach(function (fo) {
      var el = fo.querySelector('.pr-tt'), span = el && el.querySelector('span');
      if (!span) return;
      span.style.transform = 'none';
      var w = +fo.getAttribute('width') - 8, h = +fo.getAttribute('height') - 5;
      var naturalW = Math.max(span.scrollWidth, span.offsetWidth, 1);
      var naturalH = Math.max(span.scrollHeight, span.offsetHeight, 1);
      var scale = Math.min(1, w / naturalW, h / naturalH);
      span.style.transform = 'scale(' + Math.max(0.01, scale).toFixed(4) + ')';
      // Expose problematic labels so development tests can detect them.
      fo.setAttribute('data-fit-scale', scale.toFixed(3));
      fo.setAttribute('data-readable', scale >= 0.72 ? 'true' : 'false');
    });
  }
  function fit() { var box = $('.pr-pages'); if (!box) return; $$('.pr-pwrap', box).forEach(function (w) { var pw = w.firstChild && w.firstChild.classList.contains('pr-land') ? 11 : 8.5; w.style.zoom = Math.min(1, (box.clientWidth - 8) / (pw * 96)); }); }
  function bindTools() {
    $$('[data-doc]').forEach(function (b) { b.onclick = function () { ui.doc = b.getAttribute('data-doc'); drawPreview(); }; });
    $$('[data-ver]').forEach(function (b) { b.onclick = function () { ui.v = +b.getAttribute('data-ver'); drawPreview(); }; });
    if ($('#prPrintS')) $('#prPrintS').onclick = function () { printAll(false); };
    if ($('#prPrintK')) $('#prPrintK').onclick = function () { printAll(true); };
  }
  function printAll(key) {
    var root = $('#printRoot'); root.innerHTML = '';
    built.forEach(function (B, v) { PR.pageEls(cfg, B, v, built.length, key).forEach(function (p) { root.appendChild(p); }); });
    doc.body.classList.add('printing');
    fitTarsiaLabels(root);
    var done = function () { doc.body.classList.remove('printing'); root.innerHTML = ''; G.removeEventListener('afterprint', done); };
    G.addEventListener('afterprint', done);
    setTimeout(function () { G.print(); setTimeout(function () { if (doc.body.classList.contains('printing') && !G.matchMedia('print').matches) done(); }, 1500); }, 60);
  }
  G.addEventListener('resize', fit);
  $('#themeBtn') && ($('#themeBtn').onclick = function () { var cur = doc.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; doc.documentElement.setAttribute('data-theme', cur); lsSet('mkws-theme', cur); });
  (function () { var t = lsGet('mkws-theme'); if (t) doc.documentElement.setAttribute('data-theme', t); })();
  load(); setHash(); rebuild();
  PR.app = { cfg: function () { return cfg; }, built: function () { return built; }, ui: ui };   // for tests
})(window);
