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
  var MZ = { W: 7.5, H: 8.05, g: 0.36 };
  /* long math in a small room: a smaller font so it does not run past the walls */
  function roomFont(t) { var m = (String(t).match(/⟨[^⟩]*⟩/g) || []).map(function (x) { return PR.plain(x).length; }); var L = Math.max.apply(null, [0].concat(m)); return (9.6 * Math.min(1, 17 / Math.max(17, L))).toFixed(1); }
  function mazeHtml(B, key) {
    var rw = (MZ.W - (B.C - 1) * MZ.g) / B.C, rh = (MZ.H - (B.R - 1) * MZ.g) / B.R, h = '<div class="pr-maze" style="width:' + MZ.W + 'in;height:' + MZ.H + 'in">';
    B.rooms.forEach(function (rm) {
      var x = rm.c * (rw + MZ.g), y = rm.r * (rh + MZ.g), cls = 'pr-room' + (rm.finish ? ' fin' : '') + (key && rm.step !== null ? ' path' : '');
      h += '<div class="' + cls + '" style="left:' + x + 'in;top:' + y + 'in;width:' + rw + 'in;height:' + rh + 'in">' +
        (rm.r === 0 && rm.c === 0 ? '<span class="pr-start">START</span>' : '') +
        (key && rm.step !== null && !rm.finish ? '<span class="pr-step">' + (rm.step + 1) + '</span>' : '') +
        (rm.finish ? '<b>FINISH</b><small>You made it!</small>' : '<div class="pr-rq" style="font-size:' + roomFont(rm.item.p.prompt) + 'pt">' + prompt(rm.item.p) + '</div>') + '</div>';
    });
    B.doors.forEach(function (d) {
      var vert = d.a[0] === d.b[0], cls = 'pr-door' + (vert ? ' v' : '') + (key && d.correct ? ' ok' : '');
      var cx, cy, w;
      if (vert) { cx = d.a[1] * (rw + MZ.g) + rw + MZ.g / 2; cy = d.a[0] * (rh + MZ.g) + rh / 2; w = rh * 0.84; }
      else { cx = d.a[1] * (rw + MZ.g) + rw / 2; cy = d.a[0] * (rh + MZ.g) + rh + MZ.g / 2; w = rw * 0.9; }
      var len = PR.plain(d.label).length + (/\\frac/.test(d.label) ? 3 : 0), fz = Math.max(5.6, 8.4 * Math.min(1, 15 / Math.max(1, len)));
      h += '<div class="' + cls + '" style="left:' + (cx - w / 2) + 'in;top:' + (cy - 0.18) + 'in;width:' + w + 'in;font-size:' + fz.toFixed(1) + 'pt"><span>' + mathSafe(d.label) + '</span></div>';
    });
    return h + '</div>';
  }
  function mazePages(cfg, B, v, nV, key) {
    var P = [];
    P.push(page(cfg, nV, v, key, head(cfg, nV, v, key) + (key ? '<p class="pr-note">The path is shaded and numbered; the doors on the path are highlighted. Unshaded rooms are dead ends: their answers are on none of their doors.</p>'
      : dirs('Start in the room marked START. Solve its problem, then leave through the door labeled with your answer. Keep going until you reach FINISH. If your answer is not on any door, check your work. Show your work on the next page.')) + mazeHtml(B, key)));
    if (!key) {
      var boxes = ''; for (var i = 1; i <= 15; i++) boxes += '<div class="pr-wbox"><b>Room ' + i + '</b></div>';
      P.push(page(cfg, nV, v, false, '<div class="mm-head"><div><div class="mm-title mm-t2">Show your work</div><div class="mm-sub">Number the rooms in the order you visit them.</div></div>' + verTag(nV, v) + '</div><div class="pr-wgrid">' + boxes + '</div>'));
    } else {
      var rows = B.rooms.filter(function (r) { return r.step !== null && !r.finish; }).sort(function (a, b) { return a.step - b.step; });
      var dead = B.rooms.filter(function (r) { return r.step === null; });
      var tbl = function (list, lab) { return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>' + lab + '</th><th>Problem</th><th>Answer and solution</th></tr></thead><tbody>' + list.map(function (r) {
        return '<tr><td><b>' + (r.step !== null ? r.step + 1 : '—') + '</b></td><td>' + prompt(r.item.p) + '</td><td><div class="mm-ans"><b>Answer:</b> ' + mathSafe(r.item.key) + '</div><ol class="mm-steps">' + steps(r.item.p) + '</ol></td></tr>'; }).join('') + '</tbody></table>'; };
      P = P.concat(chunkPages(cfg, nV, v, true, 'Path in order', rows, 6, function (l) { return tbl(l, 'Step'); }));
      if (dead.length) P = P.concat(chunkPages(cfg, nV, v, true, 'Dead-end rooms (not on the path)', dead, 6, function (l) { return tbl(l, ''); }));
    }
    return P;
  }
  /* Pages for a long list: as many items per page as fit (measured when the pages are drawn), at most `per`. */
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
          pg = page(p.cfg, p.nV, p.v, p.key, p.html(i, i + n));
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
  function colorGrid(B, key) {
    var cols = B.grid[0].length, cell = Math.min(6.2 / cols, 5.1 / B.grid.length);
    var h = '<div class="pr-cgrid" style="grid-template-columns:repeat(' + cols + ',' + cell + 'in);grid-auto-rows:' + cell + 'in">';
    B.cells.forEach(function (row, r) { row.forEach(function (n, c) { var ch = B.grid[r][c]; h += '<div' + (key ? ' style="background:' + B.colors[ch][1] + ';color:' + (/[KNVBD]/.test(ch) ? '#fff' : '#000') + '"' : '') + '>' + n + '</div>'; }); });
    return h + '</div>';
  }
  function colorCode(B, key) {
    return '<div class="pr-code"><div class="pr-codeh">Color code</div>' + B.code.map(function (k) {
      return '<div class="pr-ck"><div class="pr-ckn"><span class="pr-sw" style="' + (key ? 'background:' + k.hex : '') + '"></span>' + esc(k.name) + '</div><div>' + k.answers.map(function (a) { return '<span class="pr-cans">' + mathSafe(a) + '</span>'; }).join('') + '</div></div>'; }).join('') + '</div>';
  }
  function probBoxes(items, start, opts) {
    return '<div class="pr-pgrid' + (opts && opts.match ? ' tight' : '') + '">' + items.map(function (it, i) { return '<div class="pr-pbox"><div class="pr-pq"><b>' + (start + i + 1) + '.</b> ' + prompt(it.p) + '</div><div class="pr-ans">Answer: <i class="ln long"></i>' + (opts && opts.match ? ' <span class="pr-match">Match? ☐ Yes ☐ No</span>' : '') + '</div></div>'; }).join('') + '</div>';
  }
  function colorPages(cfg, B, v, nV, key) {
    var P = [];
    if (!key) {
      P.push(page(cfg, nV, v, false, head(cfg, nV, v, false) + dirs('Solve each numbered problem on the next pages. Find your answer in the color code, then color every square with that problem’s number in that color. If your answer is not in the code, check your work.') + colorGrid(B, false) + colorCode(B, false)));
      for (var i = 0; i < B.items.length; i += 8) P.push(page(cfg, nV, v, false, '<div class="mm-head"><div><div class="mm-title mm-t2">Problems' + (i ? ' (continued)' : '') + '</div><div class="mm-sub">' + esc(title(cfg)) + ' · show your work</div></div>' + verTag(nV, v) + '</div>' + probBoxes(B.items.slice(i, i + 8), i)));
    } else {
      P.push(page(cfg, nV, v, true, head(cfg, nV, v, true, lvName(cfg) + ' · picture: ' + B.pictureName) + colorGrid(B, true) + colorCode(B, true)));
      var list = B.items.map(function (it, i) { return { it: it, i: i }; });
      P = P.concat(chunkPages(cfg, nV, v, true, 'Answers and solutions', list, 6, function (l) {
        return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Problem</th><th>Answer and solution</th><th>Color</th></tr></thead><tbody>' + l.map(function (x) {
          var ch = B.colorOf[x.i]; return '<tr><td><b>' + (x.i + 1) + '</b></td><td>' + prompt(x.it.p) + '</td><td><div class="mm-ans"><b>Answer:</b> ' + mathSafe(x.it.key) + '</div><ol class="mm-steps">' + steps(x.it.p) + '</ol></td><td><span class="pr-sw" style="background:' + B.colors[ch][1] + '"></span>' + esc(B.colors[ch][0]) + '</td></tr>'; }).join('') + '</tbody></table>';
      }));
    }
    return P;
  }

  /* =========================== PARTNER CHECK =========================== */
  function partnerPages(cfg, B, v, nV, key) {
    var P = [];
    if (!key) ['A', 'B'].forEach(function (who) {
      var items = B.rows.map(function (r) { return r[who]; });
      P = P.concat(flow(cfg, nV, v, false, items, 8, function (from, to) { return (from ? '<div class="mm-head"><div><div class="mm-title mm-t2">Partner ' + who + ' (continued)</div><div class="mm-sub">' + esc(unitName(cfg)) + ': Partner Check</div></div>' + verTag(nV, v) + '</div>' : '<div class="mm-head"><div><div class="mm-title">' + esc(unitName(cfg)) + ': Partner Check</div><div class="mm-sub">' + esc(lvName(cfg)) + '</div></div><span class="pr-who">' + who + '</span>' + verTag(nV, v) + '</div>' +
        '<div class="mm-name"><span>Name <i class="ln long"></i></span><span>Partner <i class="ln long"></i></span><span>Date <i class="ln mid"></i></span></div>' +
        dirs('You are <b>Partner ' + who + '</b>. Your partner has different problems, but each one has the <b>same answer</b> as yours. Solve one problem, then compare answers. If they do not match, find the mistake together before you go on.')) + probBoxes(items.slice(from, to), from, { match: true }); }));
    });
    else P = chunkPages(cfg, nV, v, true, 'Partner Check answers', B.rows.map(function (r, i) { return { r: r, i: i }; }), 4, function (l) {
      return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Partner A</th><th>Partner B</th></tr></thead><tbody>' + l.map(function (x) {
        var cell = function (it) { return prompt(it.p) + '<div class="mm-ans"><b>Answer:</b> ' + mathSafe(it.key) + '</div><ol class="mm-steps">' + steps(it.p) + '</ol>'; };
        return '<tr><td><b>' + (x.i + 1) + '</b></td><td>' + cell(x.r.A) + '</td><td>' + cell(x.r.B) + '</td></tr>'; }).join('') + '</tbody></table>';
    });
    return P;
  }

  /* =========================== ERROR ANALYSIS =========================== */
  function workHtml(cs) {
    return '<ol class="pr-swork">' + cs.work.map(function (l) { return '<li>' + mathSafe(l.t) + (l.m ? ' ' + mathSafe('⟨' + l.m + '⟩') : '') + (l.ans ? ' ' + mathSafe(l.ans) : '') + '</li>'; }).join('') + '</ol><div class="pr-sans"><b>' + esc(cs.name) + '’s answer:</b> ' + mathSafe(cs.wrong) + '</div>';
  }
  function errorPages(cfg, B, v, nV, key) {
    var list = B.cases.map(function (cs, i) { return { cs: cs, i: i }; });
    if (!key) {
      return flow(cfg, nV, v, false, list, 3, function (from, to) { return (from ? '<div class="mm-head"><div><div class="mm-title mm-t2">' + esc(title(cfg)) + ' (continued)</div></div>' + verTag(nV, v) + '</div>' : head(cfg, nV, v, false) + dirs('Each student made one mistake. <b>A.</b> Circle the line with the mistake and explain what went wrong. <b>B.</b> Solve the problem correctly.')) +
        list.slice(from, to).map(function (x) {
          return '<div class="pr-ea"><div class="pr-ea-l"><div class="pr-eah">' + (x.i + 1) + '. ' + esc(x.cs.name) + '’s work</div><div class="pr-pq">' + prompt(x.cs.item.p) + '</div>' + workHtml(x.cs) + '</div>' +
            '<div class="pr-ea-r"><div class="pr-eah">A. What is the mistake?</div><i class="ln full"></i><i class="ln full"></i><i class="ln full"></i><div class="pr-eah">B. Correct solution</div></div></div>';
        }).join(''); });
    }
    return chunkPages(cfg, nV, v, true, 'Error Analysis answers', list, 3, function (l) {
      return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Problem and the student’s work</th><th>Correct answer and solution</th></tr></thead><tbody>' + l.map(function (x) {
        return '<tr><td><b>' + (x.i + 1) + '</b></td><td>' + prompt(x.cs.item.p) + workHtml(x.cs) + '<div class="pr-flag">The mistake is in the circled line: ' + esc(x.cs.name) + '’s answer ' + mathSafe(x.cs.wrong) + ' does not check.</div></td><td><div class="mm-ans"><b>Answer:</b> ' + mathSafe(x.cs.item.key) + '</div><ol class="mm-steps">' + steps(x.cs.item.p) + '</ol></td></tr>'; }).join('') + '</tbody></table>';
    });
  }

  /* =========================== TARSIA =========================== */
  var S3 = Math.sqrt(3);
  function orient(t) { var a = t[0], b = t[1], c = t[2]; var ax = a[0] + a[1] / 2, ay = a[1] * S3 / 2, bx = b[0] + b[1] / 2, by = b[1] * S3 / 2, cx = c[0] + c[1] / 2, cy = c[1] * S3 / 2; return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) > 0 ? [0, 1, 2] : [2, 1, 0]; }
  function tarsiaSvg(B, key) {
    var pts = []; B.pieces.forEach(function (p) { p.pts.forEach(function (q) { pts.push(q); }); });
    var X = function (q) { return q[0] + q[1] / 2; }, Y = function (q) { return -q[1] * S3 / 2; };
    var minX = Math.min.apply(null, pts.map(X)), maxX = Math.max.apply(null, pts.map(X)), minY = Math.min.apply(null, pts.map(Y)), maxY = Math.max.apply(null, pts.map(Y));
    var sIn = Math.min(7.3 / (maxX - minX), 6.5 / (maxY - minY)), s = sIn * 96, W = (maxX - minX) * s, H = (maxY - minY) * s;   // drawing units are CSS px
    var px = function (q) { return [(X(q) - minX) * s, (Y(q) - minY) * s]; };
    var fs = sIn > 1.6 ? 7.6 : 6.8;
    var out = '<svg class="pr-tsvg" width="' + (W / 96) + 'in" height="' + (H / 96) + 'in" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg">';
    var slots = key ? B.pieces.map(function (_, i) { return { piece: i, slot: i, turn: 0 }; }) : B.scrambled;
    slots.forEach(function (sl) {
      var slot = B.pieces[sl.slot].pts, pc = B.pieces[sl.piece], P = slot.map(px);
      var cx = (P[0][0] + P[1][0] + P[2][0]) / 3, cy = (P[0][1] + P[1][1] + P[2][1]) / 3;
      out += '<polygon points="' + P.map(function (q) { return q.join(','); }).join(' ') + '" fill="#fff" stroke="#000" stroke-width="1.2"/>';
      var po = orient(pc.pts), so = orient(slot), E = [[0, 1], [1, 2], [2, 0]];
      for (var k = 0; k < 3; k++) {
        var txt = pc.text[po[k]]; if (!txt) continue;
        var e = E[so[(k + sl.turn) % 3]], A = P[e[0]], Bp = P[e[1]], mx = (A[0] + Bp[0]) / 2, my = (A[1] + Bp[1]) / 2;
        var nx = cx - mx, ny = cy - my, nl = Math.sqrt(nx * nx + ny * ny); nx /= nl; ny /= nl;
        var len = Math.sqrt(Math.pow(Bp[0] - A[0], 2) + Math.pow(Bp[1] - A[1], 2)) * 0.76, d = 13, ang = Math.atan2(nx, -ny) * 180 / Math.PI;
        var ox = mx + nx * d, oy = my + ny * d, hh = 21;
        out += '<foreignObject x="' + (ox - len / 2) + '" y="' + (oy - hh / 2) + '" width="' + len + '" height="' + hh + '" transform="rotate(' + ang.toFixed(2) + ' ' + ox + ' ' + oy + ')"><div xmlns="http://www.w3.org/1999/xhtml" class="pr-tt' + (key && pc.kind[po[k]] === 'q' ? ' q' : '') + '" style="font-size:' + Math.max(6.2, fs * Math.min(1, 22 / Math.max(1, PR.plain(txt).length))).toFixed(2) + 'pt"><span>' + mathSafe(txt) + '</span></div></foreignObject>';
      }
    });
    return out + '</svg>';
  }
  function tarsiaPages(cfg, B, v, nV, key) {
    var P = [], n = B.items.length;
    if (!key) {
      P.push(page(cfg, nV, v, false, head(cfg, nV, v, false, lvName(cfg) + ' · ' + B.pieces.length + ' triangles, ' + n + ' matches') +
        dirs('Cut out the triangles. Each numbered problem matches exactly one answer. Put matching edges together to rebuild a <b>' + B.shape + '</b>. Some outside edges have answers that match nothing. Show your work for every problem on the work pages.') + '<div class="pr-tbox">' + tarsiaSvg(B, false) + '</div>'));
      var sorted = B.items.slice().sort(function (a, b) { return a.num - b.num; });
      for (var i = 0; i < n; i += 15) P.push(page(cfg, nV, v, false, '<div class="mm-head"><div><div class="mm-title mm-t2">Show your work</div><div class="mm-sub">' + esc(title(cfg)) + ' · problems ' + (i + 1) + '–' + Math.min(n, i + 15) + '</div></div>' + verTag(nV, v) + '</div><div class="pr-twork">' +
        sorted.slice(i, i + 15).map(function (it) { return '<div class="pr-wbox"><b>' + it.num + '.</b> ' + mathSafe(it.p.prompt) + '</div>'; }).join('') + '</div>'));
    } else {
      P.push(page(cfg, nV, v, true, head(cfg, nV, v, true) + '<p class="pr-note">The solved ' + esc(B.shape) + '. Problems are in bold.</p><div class="pr-tbox">' + tarsiaSvg(B, true) + '</div>'));
      var list = B.items.slice().sort(function (a, b) { return a.num - b.num; });
      P = P.concat(chunkPages(cfg, nV, v, true, 'Answers', list, 12, function (l) {
        return '<table class="mm-tbl mm-key pr-ktbl"><thead><tr><th>#</th><th>Problem</th><th>Answer</th><th>Solution</th></tr></thead><tbody>' + l.map(function (it) {
          return '<tr><td><b>' + it.num + '</b></td><td>' + mathSafe(it.p.prompt) + '</td><td>' + mathSafe(it.key) + '</td><td><ol class="mm-steps">' + steps(it.p) + '</ol></td></tr>'; }).join('') + '</tbody></table>';
      }));
    }
    return P;
  }

  PR.pages = function (cfg, B, v, nV, key) {
    return ({ maze: mazePages, color: colorPages, partner: partnerPages, error: errorPages, tarsia: tarsiaPages })[cfg.kind](cfg, B, v, nV, key);
  };
  PR.pageEls = function (cfg, B, v, nV, key) {
    var P = expandFlow(PR.pages(cfg, B, v, nV, key));
    return P.map(function (p, i) {
      var e = doc.createElement('div'); e.className = 'page mm-page pr-page';
      e.innerHTML = p.html + '<div class="mm-foot"><span>' + p.foot + '</span><span>Page ' + (i + 1) + ' of ' + P.length + '</span></div>';
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
  var cfg = null, built = [], ui = { doc: 'student', v: 0 };
  function load() {
    var raw = lsGet(KEY + ':' + unit + ':' + kind); cfg = null;
    try { var o = JSON.parse(raw); if (o && o.unitId === unit && o.kind === kind) cfg = o; } catch (e) { cfg = null; }
    if (!cfg) cfg = PR.defaultConfig(unit, kind);
    NS.skillSets[unit].skills.forEach(function (s) { if (cfg.skills[s.id] === undefined) cfg.skills[s.id] = true; });
  }
  function save() { lsSet(KEY + ':' + unit + ':' + kind, JSON.stringify(cfg)); }
  function setHash() { try { G.history.replaceState(null, '', '#unit=' + unit + '&kind=' + kind); } catch (e) { /* ignore */ } }
  function unitOptions() {
    return NS.CATALOG.map(function (g) { return '<optgroup label="' + esc(g.course) + '">' + g.units.filter(function (u) { return NS.skillSets[u[0]]; }).map(function (u) { return '<option value="' + u[0] + '"' + (u[0] === unit ? ' selected' : '') + '>' + esc(u[1]) + '</option>'; }).join('') + '</optgroup>'; }).join('');
  }
  function controls() {
    var set = NS.skillSets[unit], k = PR.kind(kind);
    var h = '<section class="card"><h2>Activity</h2><label class="field"><span class="lbl">Unit</span><select id="prUnit">' + unitOptions() + '</select></label>' +
      '<fieldset class="field pr-kinds"><legend class="lbl">Printable</legend>' + PR.KINDS.map(function (x) { return '<label class="chk"><input type="radio" name="prKind" value="' + x.id + '"' + (x.id === kind ? ' checked' : '') + '><span>' + esc(x.name) + '<small>' + esc(x.blurb) + '</small></span></label>'; }).join('') + '</fieldset></section>';
    h += '<section class="card"><h2>Level and skills</h2><div class="pr-levels">' + Object.keys(NS.LEVELS).map(function (id) { return '<label class="chk"><input type="radio" name="prLevel" value="' + id + '"' + (cfg.level === id ? ' checked' : '') + '><span>' + esc(NS.LEVELS[id].long) + '</span></label>'; }).join('') + '</div>' +
      '<p class="hint">Skills this printable cannot use are greyed out (for example, problems answered with a graph cannot go on a maze door).</p>' +
      set.skills.map(function (s) { var cap = PR.capable(unit, s.id, kind); return '<label class="chk' + (cap ? '' : ' off') + '"><input type="checkbox" class="prSkill" value="' + s.id + '"' + (cfg.skills[s.id] && cap ? ' checked' : '') + (cap ? '' : ' disabled') + '><span>' + esc(s.name) + (cap ? '' : '<small>Not available for a ' + esc(k.name.toLowerCase()) + '</small>') + '</span></label>'; }).join('') + '</section>';
    h += '<section class="card"><h2>Options</h2>' + (kind === 'color' ? '<label class="field"><span class="lbl">Picture</span><select id="prPic"><option value="auto">Surprise me</option>' + Object.keys(PR.PICTURES).map(function (id) { return '<option value="' + id + '"' + (cfg.picture === id ? ' selected' : '') + '>' + esc(PR.PICTURES[id].name) + '</option>'; }).join('') + '</select></label>' : '') +
      '<label class="field"><span class="lbl">Versions</span><select id="prVer">' + [1, 2, 3].map(function (n) { return '<option value="' + n + '"' + ((cfg.versions | 0) === n ? ' selected' : '') + '>' + ['Version A only', 'Versions A and B', 'Versions A, B and C'][n - 1] + '</option>'; }).join('') + '</select></label>' +
      '<p><button type="button" class="btn" id="prNew">↻ New problems</button></p><p class="hint">Every answer is checked independently. Every wrong label (a maze door, a Tarsia edge, a student’s wrong answer) is checked to be wrong.</p></section>';
    return h;
  }
  function render() {
    $('#prControls').innerHTML = controls();
    $('#prUnit').onchange = function (e) { unit = e.target.value; load(); setHash(); rebuild(); };
    $$('input[name=prKind]').forEach(function (r) { r.onchange = function () { kind = r.value; load(); setHash(); rebuild(); }; });
    $$('input[name=prLevel]').forEach(function (r) { r.onchange = function () { cfg.level = r.value; save(); rebuild(); }; });
    $$('.prSkill').forEach(function (b) { b.onchange = function () { cfg.skills[b.value] = b.checked; save(); rebuild(); }; });
    if ($('#prPic')) $('#prPic').onchange = function (e) { cfg.picture = e.target.value; save(); rebuild(); };
    $('#prVer').onchange = function (e) { cfg.versions = +e.target.value; save(); rebuild(); };
    $('#prNew').onclick = function () { cfg.seed = Math.floor(Math.random() * 1e9); save(); rebuild(); };
    doc.title = PR.kind(kind).name + ' Generator · Mr. K\'s Classroom';
    $('#prCrumb').textContent = 'Printable Generator · ' + PR.kind(kind).name;
  }
  function rebuild() {
    render();
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
    fit(); bindTools();
  }
  function fit() { var box = $('.pr-pages'); if (!box) return; var z = Math.min(1, (box.clientWidth - 8) / (8.5 * 96)); $$('.pr-pwrap', box).forEach(function (w) { w.style.zoom = z; }); }
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
