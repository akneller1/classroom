/* Seating Chart Maker engine: furniture geometry, drawing, the auto-seat solver,
   rule checks, roster parsing and export helpers. Used by ../seating-chart.html.
   Runs in the browser (window.SEAT) and in node (module.exports) for tests. */
(function (root) {
'use strict';
var S = {};

/* ---------- constants ---------- */
var FT = S.FT = 32;                 // drawing units per foot
var NEAR = S.NEAR = 150;            // seat centers closer than this (about 4.7 ft) count as neighbors
S.FONT = "'Avenir Next','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif";
var P = S.P = {
  paper:'#FFFFFF', grid:'#E8EEF5', wall:'#2B3A4A',
  desk:'#F5E6C6', deskLine:'#A57A43', divider:'#CDAE7E',
  chair:'#CBD5E1', chairLine:'#8494A7',
  ink:'#1B2430', muted:'#6B7785',
  teacher:'#DCE7F3', teacherLine:'#4F6A8B',
  bar:'#2B3A4A', barInk:'#FFFFFF',
  window:'#D6ECFA', windowLine:'#4C86B4',
  note:'#FFF7D6', noteLine:'#C29B1E',
  sel:'#2F6FE4', emptySeat:'#8DAACB', drop:'#FFD84D', picked:'#E0A400', warn:'#D93025', tag:'#2B3A4A'
};
S.LABELS = {
  front:{label:'Front of room', text:'Front of room', w:520, h:34},
  back:{label:'Back of room', text:'Back of room', w:520, h:34},
  board:{label:'Whiteboard', text:'Whiteboard', w:340, h:30},
  door:{label:'Door', text:'Door', w:80, h:80},
  window:{label:'Windows', text:'Windows', w:240, h:24},
  note:{label:'Custom label', text:'Label', w:150, h:40}
};
S.NEEDS = [
  ['front', 'Near the front'],
  ['teacher', "Near the teacher's desk"],
  ['door', 'Near the door'],
  ['back', 'Near the back'],
  ['nowindow', 'Away from the windows']
];
S.TAG_COLORS = ['#2F6FE4','#D9480F','#2B8A3E','#AE3EC9','#0B7285','#C2255C','#5C940D','#E67700'];
S.PAPER = { letter:{w:792, h:612, label:'US Letter'}, a4:{w:842, h:595, label:'A4'} };

/* ---------- small helpers ---------- */
function uid() { return Math.random().toString(36).slice(2, 9); }
function r1(v) { return Math.round(v * 10) / 10; }
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function rotPt(x, y, deg) { var a = deg * Math.PI / 180, c = Math.cos(a), s = Math.sin(a); return {x:x*c - y*s, y:x*s + y*c}; }
function normDeg(d) { d %= 360; if (d < 0) d += 360; return d; }
function signedDeg(d) { d = normDeg(d); return d > 180 ? d - 360 : d; }
function upright(d) { d = normDeg(d); if (d > 90 && d <= 270) d -= 180; if (d > 180) d -= 360; return d; }
function sideways(deg) { var d = normDeg(deg) % 180; return d > 45 && d < 135; }
function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
S.uid = uid; S.esc = esc; S.r1 = r1; S.rotPt = rotPt; S.normDeg = normDeg; S.signedDeg = signedDeg; S.shuffle = shuffle;

/* ---------- text measuring and fitting ---------- */
var mctx = null;
try { if (typeof document !== 'undefined') mctx = document.createElement('canvas').getContext('2d'); } catch (e) { mctx = null; }
function textW(t, fs, wt) {
  if (!mctx) return t.length * fs * 0.56;
  mctx.font = (wt || 600) + ' ' + fs + 'px ' + S.FONT;
  return mctx.measureText(t).width;
}
S.textW = textW;
function pieces(t) {
  var out = [], buf = '';
  for (var i = 0; i < t.length; i++) {
    var ch = t[i];
    if (ch === ' ') { if (buf) out.push({w:buf, sep:' '}); buf = ''; }
    else if (ch === '-' && buf) { out.push({w:buf + '-', sep:''}); buf = ''; }
    else buf += ch;
  }
  if (buf) out.push({w:buf, sep:' '});
  return out;
}
function joinP(ps) { var s = ''; ps.forEach(function (p, i) { s += p.w + (i < ps.length - 1 ? p.sep : ''); }); return s; }
function splitN(t, n, fs) {
  var ps = pieces(t); if (ps.length < n) return null;
  var best = null, bw = 1e9;
  (function rec(start, left, acc) {
    if (left === 1) {
      var l = acc.concat([joinP(ps.slice(start))]);
      var w = Math.max.apply(null, l.map(function (x) { return textW(x, fs); }));
      if (w < bw) { bw = w; best = l; }
      return;
    }
    for (var i = start + 1; i <= ps.length - left + 1; i++) rec(i, left - 1, acc.concat([joinP(ps.slice(start, i))]));
  })(0, n, []);
  return best ? {lines:best, w:bw} : null;
}
function fitText(t, maxW, maxH, maxFs, minFs) {
  maxFs = maxFs || 15; minFs = minFs || 8;
  for (var fs = maxFs; fs >= minFs; fs -= 0.5) {
    if (textW(t, fs) <= maxW && fs * 1.15 <= maxH) return {fs:fs, lines:[t]};
    for (var n = 2; n <= 3; n++) {
      if (fs * (1.12 * n + 0.05) > maxH) break;
      var sp = splitN(t, n, fs);
      if (sp && sp.w <= maxW) return {fs:fs, lines:sp.lines};
    }
  }
  var two = splitN(t, 2, minFs);
  var lines = (two && minFs * 2.3 <= maxH) ? two.lines : [t];
  lines = lines.map(function (l) { var s = l; while (s.length > 1 && textW(s + '…', minFs) > maxW) s = s.slice(0, -1); return s === l ? l : s + '…'; });
  return {fs:minFs, lines:lines};
}
S.fitText = fitText;
function textSvg(x, y, fit, opt) {
  opt = opt || {};
  var lh = fit.fs * 1.12, n = fit.lines.length, y0 = -((n - 1) * lh) / 2 + fit.fs * 0.35;
  var s = '<text text-anchor="middle" font-size="' + fit.fs + '" font-weight="' + (opt.weight || 600) + '" fill="' + (opt.fill || P.ink) +
    '" transform="translate(' + r1(x) + ' ' + r1(y) + ')' + (opt.rot ? ' rotate(' + r1(opt.rot) + ')' : '') + '">';
  fit.lines.forEach(function (l, i) { s += '<tspan x="0" y="' + r1(y0 + i * lh) + '">' + esc(l) + '</tspan>'; });
  return s + '</text>';
}

/* ---------- names ---------- */
S.shownName = function (name, style) {
  var parts = name.trim().split(/\s+/);
  if (style === 'first') return parts[0];
  if (style === 'initial' && parts.length > 1) return parts[0] + ' ' + parts[parts.length - 1].charAt(0) + '.';
  return name.trim();
};
S.lastFirst = function (name) { var p = name.trim().split(/\s+/); return (p[p.length - 1] + ' ' + p.slice(0, -1).join(' ')).toLowerCase(); };

/* ---------- furniture ---------- */
/* Item types:
   desk    {n, rows:1|2, sw, sh}  one row: chairs behind (students face -y, the front); two rows: face to face
   round   {n}                    round table with n seats around it
   teacher {w, h}
   label   {kind, text, w, h}     front, back, board, door, window, note */
var ROUND_R = {3:72, 4:80, 5:84, 6:90, 7:100, 8:110, 9:120, 10:130};
function geom(it) {
  var t = it.type, i, x;
  if (t === 'desk') {
    var n = Math.max(1, it.n || 1), rows = (it.rows === 2 && n >= 2) ? 2 : 1, sw = it.sw || 76, sh = it.sh || 52;
    var seats = [], chairs = [], div = [], W;
    if (rows === 1) {
      W = n * sw;
      for (i = 0; i < n; i++) {
        x = -W / 2 + sw * (i + 0.5);
        seats.push([x, 0, sw, sh]); chairs.push([x, sh / 2 + 10]);
        if (i) div.push([-W / 2 + sw * i, -sh / 2, -W / 2 + sw * i, sh / 2]);
      }
      return {kind:'desk', seats:seats, chairs:chairs, div:div, body:[-W / 2, -sh / 2, W, sh], w:W, h:sh + 32};
    }
    var top = Math.ceil(n / 2), bot = n - top; W = top * sw; var bsw = W / bot;
    for (i = 0; i < top; i++) {
      x = -W / 2 + sw * (i + 0.5);
      seats.push([x, -sh / 2, sw, sh]); chairs.push([x, -sh - 10]);
      if (i) div.push([-W / 2 + sw * i, -sh, -W / 2 + sw * i, 0]);
    }
    for (i = 0; i < bot; i++) {
      x = -W / 2 + bsw * (i + 0.5);
      seats.push([x, sh / 2, bsw, sh]); chairs.push([x, sh + 10]);
      if (i) div.push([-W / 2 + bsw * i, 0, -W / 2 + bsw * i, sh]);
    }
    div.push([-W / 2, 0, W / 2, 0]);
    return {kind:'desk', seats:seats, chairs:chairs, div:div, body:[-W / 2, -sh, W, 2 * sh], w:W, h:2 * sh + 32};
  }
  if (t === 'round') {
    var m = Math.max(3, Math.min(10, it.n || 6)), R = ROUND_R[m], ps = [], mx = 0, my = 0;
    for (i = 0; i < m; i++) {
      var a = (-90 + i * 360 / m) * Math.PI / 180, px = r1(R * Math.cos(a)), py = r1(R * Math.sin(a));
      ps.push([px, py, 78, 30]); mx = Math.max(mx, Math.abs(px)); my = Math.max(my, Math.abs(py));
    }
    return {kind:'round', seats:ps, chairs:[], div:[], r:R - 38, w:2 * (mx + 39), h:2 * (my + 15)};
  }
  if (t === 'teacher') {
    var tw = it.w || 150, th = it.h || 70;
    return {kind:'teacher', seats:[], chairs:[[0, th / 2 + 12]], div:[], body:[-tw / 2, -th / 2, tw, th], w:tw, h:th + 40};
  }
  var L = S.LABELS[it.kind] || S.LABELS.note, lw = it.w || L.w;
  return {kind:'label', seats:[], chairs:[], div:[], w:lw, h:it.kind === 'door' ? lw : (it.h || L.h)};
}
S.geom = geom;
S.seatCount = function (it) { return geom(it).seats.length; };
S.itemBox = function (it) {
  var g = geom(it), a = (it.rot || 0) * Math.PI / 180;
  var bw = Math.abs(g.w * Math.cos(a)) + Math.abs(g.h * Math.sin(a));
  var bh = Math.abs(g.w * Math.sin(a)) + Math.abs(g.h * Math.cos(a));
  return {x1:it.x - bw / 2, y1:it.y - bh / 2, x2:it.x + bw / 2, y2:it.y + bh / 2};
};
S.itemName = function (it) {
  if (it.type === 'teacher') return "Teacher's desk";
  if (it.type === 'label') return (S.LABELS[it.kind] || S.LABELS.note).label;
  if (it.type === 'round') return 'Round table of ' + (it.n || 6);
  var n = it.n || 1;
  if (n === 1) return 'Single desk';
  if (n === 2 && it.rows !== 2) return 'Pair desk';
  return (it.rows === 2 ? 'Group of ' : 'Table of ') + n;
};
/* Older charts used fixed type names. */
S.migrateItem = function (it) {
  var map = { single:{n:1, rows:1}, pair:{n:2, rows:1}, group4:{n:4, rows:2}, group6:{n:6, rows:2} };
  if (map[it.type]) { it.n = map[it.type].n; it.rows = map[it.type].rows; it.type = 'desk'; }
  if (it.type === 'round6') { it.type = 'round'; it.n = 6; }
  return it;
};
S.validItem = function (it) {
  return it && typeof it.x === 'number' && typeof it.y === 'number' &&
    (it.type === 'desk' || it.type === 'round' || it.type === 'teacher' || (it.type === 'label' && S.LABELS[it.kind]));
};

/* ---------- desks and seats in reading order ---------- */
S.dims = function (st) { return {w:st.roomW || 1024, h:st.roomH || 768}; };
S.deskOrder = function (st) {
  var list = st.items.filter(function (it) { return it.type !== 'label' && geom(it).seats.length; });
  list.sort(function (a, b) { return a.y - b.y; });
  var rows = [], row = null;
  list.forEach(function (it) {
    if (!row || it.y - row.y0 > 45) { row = {y0:it.y, items:[]}; rows.push(row); }
    row.items.push(it);
  });
  var out = [];
  rows.forEach(function (rw) { rw.items.sort(function (a, b) { return a.x - b.x; }); out = out.concat(rw.items); });
  return out;
};
S.seatList = function (st) {
  var out = [];
  S.deskOrder(st).forEach(function (it, n) {
    var g = geom(it);
    g.seats.forEach(function (q, i) {
      var c = rotPt(q[0], q[1], it.rot || 0);
      out.push({key:it.id + ':' + i, item:it, i:i, desk:n + 1, letter:String.fromCharCode(65 + i),
                multi:g.seats.length > 1, size:g.seats.length, x:it.x + c.x, y:it.y + c.y, q:q});
    });
  });
  return out;
};
S.seatLabel = function (info) { return 'Desk ' + info.desk + (info.multi ? ', seat ' + info.letter : ''); };
S.seatOf = function (st, sid) { for (var k in st.seats) if (st.seats[k] === sid) return k; return null; };
S.student = function (st, id) { for (var i = 0; i < st.students.length; i++) if (st.students[i].id === id) return st.students[i]; return null; };
S.cleanSeats = function (st) {
  var valid = {}, ids = {};
  st.items.forEach(function (it) { if (it.type !== 'label') geom(it).seats.forEach(function (q, i) { valid[it.id + ':' + i] = 1; }); });
  st.students.forEach(function (s) { ids[s.id] = 1; });
  var used = {};
  for (var k in st.seats) {
    var sid = st.seats[k];
    if (!valid[k] || !ids[sid] || used[sid]) delete st.seats[k]; else used[sid] = 1;
  }
  st.rules = (st.rules || []).filter(function (r) { return ids[r.a] && ids[r.b] && r.a !== r.b; });
};

/* neighbor strength between seats: 2 = same desk or table, 1 = close by, 0 = apart */
S.neighborMatrix = function (seats) {
  var N = seats.length, m = new Int8Array(N * N);
  for (var i = 0; i < N; i++) for (var j = i + 1; j < N; j++) {
    var w = seats[i].item === seats[j].item ? 2 : (Math.hypot(seats[i].x - seats[j].x, seats[i].y - seats[j].y) < NEAR ? 1 : 0);
    m[i * N + j] = w; m[j * N + i] = w;
  }
  return m;
};
S.neighborPairs = function (st) {
  var seats = S.seatList(st), m = S.neighborMatrix(seats), N = seats.length, out = [];
  for (var i = 0; i < N; i++) for (var j = i + 1; j < N; j++) {
    var a = st.seats[seats[i].key], b = st.seats[seats[j].key];
    if (a && b && m[i * N + j]) out.push([a, b, m[i * N + j]]);
  }
  return out;
};

/* ---------- seat needs: 0 = best seat in the room, 1 = worst ---------- */
function segDist(px, py, it) {
  var g = geom(it), half = (it.type === 'label' && it.kind !== 'door') ? g.w / 2 : 0;
  var a = rotPt(-half, 0, it.rot || 0), b = rotPt(half, 0, it.rot || 0);
  var ax = it.x + a.x, ay = it.y + a.y, bx = it.x + b.x, by = it.y + b.y;
  var dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy, t = L2 ? ((px - ax) * dx + (py - ay) * dy) / L2 : 0;
  t = Math.max(0, Math.min(1, t));
  return Math.hypot(px - (ax + t * dx), py - (ay + t * dy));
}
function ranks(vals) {
  var N = vals.length, order = vals.map(function (v, i) { return i; }).sort(function (a, b) { return vals[a] - vals[b]; });
  var pct = new Array(N), start = 0;
  for (var k = 0; k < N; k++) {
    if (k && vals[order[k]] - vals[order[start]] > 6) start = k;
    pct[order[k]] = N > 1 ? start / (N - 1) : 0;
  }
  return pct;
}
S.needScores = function (st, seats) {
  var D = S.dims(st), out = {};
  function nearest(filter) {
    var targets = st.items.filter(filter);
    if (!targets.length) return null;
    return seats.map(function (s) { return Math.min.apply(null, targets.map(function (t) { return segDist(s.x, s.y, t); })); });
  }
  var lab = function (k) { return function (it) { return it.type === 'label' && it.kind === k; }; };
  var front = nearest(lab('front')) || nearest(lab('board'));
  out.front = ranks(front || seats.map(function (s) { return s.y; }));
  var back = nearest(lab('back'));
  out.back = ranks(back || seats.map(function (s) { return D.h - s.y; }));
  var door = nearest(lab('door')); if (door) out.door = ranks(door);
  var teacher = nearest(function (it) { return it.type === 'teacher'; }); if (teacher) out.teacher = ranks(teacher);
  var win = nearest(lab('window')); if (win) out.nowindow = ranks(win.map(function (d) { return -d; }));
  return out;
};
S.NEED_MET = 0.34;
S.needText = function (k) { for (var i = 0; i < S.NEEDS.length; i++) if (S.NEEDS[i][0] === k) return S.NEEDS[i][1]; return k; };

/* ---------- checking the current seating ---------- */
S.check = function (st) {
  var seats = S.seatList(st), N = seats.length, idx = {}, m = S.neighborMatrix(seats), sc = S.needScores(st, seats);
  seats.forEach(function (s, i) { idx[s.key] = i; });
  var problems = [], notes = [], rulesN = 0, rulesOk = 0, needsN = 0, needsOk = 0;
  function pos(sid) { var k = S.seatOf(st, sid); return k != null && idx[k] != null ? idx[k] : -1; }
  function nm(sid) { var s = S.student(st, sid); return s ? s.name : '?'; }
  (st.rules || []).forEach(function (r) {
    var a = pos(r.a), b = pos(r.b);
    if (a < 0 || b < 0) return;
    rulesN++;
    var w = m[a * N + b];
    if (r.type === 'apart' && w) problems.push({text:nm(r.a) + ' and ' + nm(r.b) + ' are ' + (w === 2 ? 'at the same desk' : 'sitting close together') + ' (keep apart).', keys:[seats[a].key, seats[b].key]});
    else if (r.type === 'together' && !w) problems.push({text:nm(r.a) + ' and ' + nm(r.b) + ' are not near each other (work well together).', keys:[seats[a].key, seats[b].key]});
    else rulesOk++;
  });
  var missing = {};
  st.students.forEach(function (stu) {
    (stu.needs || []).forEach(function (k) {
      if (!sc[k]) { missing[k] = 1; return; }
      var p = pos(stu.id); if (p < 0) return;
      needsN++;
      if (sc[k][p] <= S.NEED_MET) needsOk++;
      else problems.push({text:stu.name + ' is not ' + S.needText(k).toLowerCase().replace(/^near/, 'near').replace(/^away/, 'away') + '.', keys:[seats[p].key]});
    });
  });
  var what = {door:'a door', teacher:"a teacher's desk", nowindow:'windows'};
  for (var k in missing) notes.push('Add ' + what[k] + ' to the room so “' + S.needText(k).toLowerCase() + '” can be used.');
  return {problems:problems, notes:notes, rules:rulesN, rulesOk:rulesOk, needs:needsN, needsOk:needsOk};
};

/* ---------- the auto-seat solver ----------
   opts: mode 'all' | 'empty'; spread 'any' | 'front' | 'even'; rules, needs, fresh, balance (booleans)
   Pinned students (and, in 'empty' mode, everyone already seated) stay where they are. */
S.solve = function (st, o) {
  o = o || {};
  var seats = S.seatList(st), N = seats.length, idx = {};
  seats.forEach(function (s, i) { idx[s.key] = i; });
  var m = S.neighborMatrix(seats), sc = S.needScores(st, seats);
  var fixed = {}, movers = [];
  st.students.forEach(function (stu) {
    var k = S.seatOf(st, stu.id), i = k != null ? idx[k] : undefined;
    if (i != null && (o.mode === 'empty' || stu.pin)) fixed[stu.id] = i; else movers.push(stu.id);
  });
  var taken = {}; for (var f in fixed) taken[fixed[f]] = 1;
  var free = []; for (var i = 0; i < N; i++) if (!taken[i]) free.push(i);
  shuffle(free);
  if (o.spread === 'front' && movers.length < free.length) {
    free.sort(function (a, b) { return sc.front[a] - sc.front[b]; });
    free = free.slice(0, movers.length);
  }
  var slots = free.slice(); while (slots.length < movers.length) slots.push(-1);
  var L = slots.length;

  // what the cost function looks at
  var exists = {}; st.students.forEach(function (s) { exists[s.id] = 1; });
  var rules = o.rules === false ? [] : (st.rules || []).filter(function (r) { return exists[r.a] && exists[r.b]; });
  var needs = [];
  if (o.needs !== false) st.students.forEach(function (s) { (s.needs || []).forEach(function (k) { if (sc[k]) needs.push([s.id, sc[k]]); }); });
  var histPairs = [];
  if (o.fresh && st.history && st.history.length) {
    var acc = {};
    st.history.slice().reverse().forEach(function (h, age) {
      var wt = Math.pow(0.75, age);
      (h.pairs || []).forEach(function (p) { if (exists[p[0]] && exists[p[1]]) { var key = p[0] < p[1] ? p[0] + '|' + p[1] : p[1] + '|' + p[0]; acc[key] = (acc[key] || 0) + wt * (p[2] === 2 ? 1 : 0.6); } });
    });
    for (var key in acc) { var ab = key.split('|'); histPairs.push([ab[0], ab[1], acc[key]]); }
  }
  // groups: desks and tables with two or more seats
  var gid = {}, groups = [], groupOf = new Int16Array(N).fill(-1);
  seats.forEach(function (s, i) {
    if (!s.multi) return;
    if (gid[s.item.id] == null) { gid[s.item.id] = groups.length; groups.push(s.size); }
    groupOf[i] = gid[s.item.id];
  });
  var G = groups.length, tagIds = [], tagged = {};
  if (o.balance && G > 1) (st.tags || []).forEach(function (t) {
    var who = {}; var any = false;
    st.students.forEach(function (s) { if ((s.tags || []).indexOf(t.id) >= 0) { who[s.id] = 1; any = true; } });
    if (any) { tagIds.push(t.id); tagged[t.id] = who; }
  });
  var even = o.spread === 'even' && G > 0;
  var hasCost = rules.length || needs.length || histPairs.length || tagIds.length || even;

  var pos = {};
  for (var fs in fixed) pos[fs] = fixed[fs];
  var occ = new Array(L);
  function place() { for (var k = 0; k < L; k++) if (occ[k]) pos[occ[k]] = slots[k]; }
  var gOcc = new Float64Array(G), gTag = new Float64Array(G);
  function cost() {
    var c = 0, k, a, b, w;
    for (k = 0; k < rules.length; k++) {
      a = pos[rules[k].a]; b = pos[rules[k].b];
      if (a == null || b == null || a < 0 || b < 0) continue;
      w = m[a * N + b];
      if (rules[k].type === 'apart') c += w === 2 ? 40 : w === 1 ? 25 : 0;
      else c += w === 2 ? 0 : w === 1 ? 5 : 14;
    }
    for (k = 0; k < needs.length; k++) { a = pos[needs[k][0]]; if (a >= 0) c += Math.max(0, needs[k][1][a] - 0.12) * 16; }
    for (k = 0; k < histPairs.length; k++) {
      a = pos[histPairs[k][0]]; b = pos[histPairs[k][1]];
      if (a == null || b == null || a < 0 || b < 0) continue;
      w = m[a * N + b]; if (w) c += (w === 2 ? 6 : 3) * histPairs[k][2];
    }
    if (even || tagIds.length) {
      gOcc.fill(0); var seated = 0, inGroups = 0;
      for (var sid in pos) { var p = pos[sid]; if (p >= 0) { seated++; if (groupOf[p] >= 0) { gOcc[groupOf[p]]++; inGroups++; } } }
      if (even) { var cap = 0; for (k = 0; k < G; k++) cap += groups[k]; for (k = 0; k < G; k++) { var tgt = inGroups * groups[k] / cap; c += 1.5 * (gOcc[k] - tgt) * (gOcc[k] - tgt); } }
      for (var t = 0; t < tagIds.length; t++) {
        gTag.fill(0); var tot = 0, who = tagged[tagIds[t]];
        for (var sid2 in who) { var p2 = pos[sid2]; if (p2 >= 0 && groupOf[p2] >= 0) { gTag[groupOf[p2]]++; tot++; } }
        if (!tot || !inGroups) continue;
        for (k = 0; k < G; k++) { var ex = tot * gOcc[k] / inGroups; c += 4 * (gTag[k] - ex) * (gTag[k] - ex); }
      }
    }
    return c;
  }
  var best = null, bestC = Infinity, restarts = hasCost ? 3 : 1;
  for (var r = 0; r < restarts; r++) {
    var order = shuffle(movers.slice());
    for (var k = 0; k < L; k++) occ[k] = order[k] || null;
    shuffle(occ);
    for (var mv = 0; mv < movers.length; mv++) pos[movers[mv]] = -1;
    place();
    var cur = hasCost ? cost() : 0;
    if (hasCost && L > 1) {
      var iters = 3000 + 80 * L, T = 8, decay = Math.pow(0.02 / 8, 1 / iters);
      for (var it = 0; it < iters; it++, T *= decay) {
        var x = Math.floor(Math.random() * L), y = Math.floor(Math.random() * L);
        if (x === y || (!occ[x] && !occ[y])) continue;
        var ox = occ[x], oy = occ[y];
        occ[x] = oy; occ[y] = ox;
        if (oy) pos[oy] = slots[x]; if (ox) pos[ox] = slots[y];
        var nc = cost(), d = nc - cur;
        if (d <= 0 || Math.random() < Math.exp(-d / T)) cur = nc;
        else { occ[x] = ox; occ[y] = oy; if (ox) pos[ox] = slots[x]; if (oy) pos[oy] = slots[y]; }
        if (cur === 0) break;
      }
    }
    if (cur < bestC) { bestC = cur; best = occ.slice(); }
    if (bestC === 0) break;
  }
  var out = {};
  for (var fx in fixed) out[seats[fixed[fx]].key] = fx;
  for (var q = 0; q < L; q++) if (best[q] && slots[q] >= 0) out[seats[slots[q]].key] = best[q];
  return {seats:out, cost:bestC};
};

/* ---------- drawing ---------- */
function chairSvg(c) { return '<rect x="' + r1(c[0] - 21) + '" y="' + r1(c[1] - 6) + '" width="42" height="12" rx="6" fill="' + P.chair + '" stroke="' + P.chairLine + '" stroke-width="1.2"/>'; }
S.itemGeoSvg = function (it) {
  var g = geom(it), s = '', b = g.body;
  if (g.kind === 'label') return labelGeo(it, g);
  g.chairs.forEach(function (c) { s += chairSvg(c); });
  if (g.kind === 'round') {
    s += '<circle r="' + g.r + '" fill="' + P.desk + '" stroke="' + P.deskLine + '" stroke-width="2"/>';
    g.seats.forEach(function (q) { s += '<rect x="' + r1(q[0] - q[2] / 2) + '" y="' + r1(q[1] - q[3] / 2) + '" width="' + q[2] + '" height="' + q[3] + '" rx="8" fill="' + P.desk + '" stroke="' + P.deskLine + '" stroke-width="1.6"/>'; });
  } else if (g.kind === 'teacher') {
    s += '<rect x="' + b[0] + '" y="' + b[1] + '" width="' + b[2] + '" height="' + b[3] + '" rx="5" fill="' + P.teacher + '" stroke="' + P.teacherLine + '" stroke-width="2"/>';
  } else {
    s += '<rect x="' + r1(b[0]) + '" y="' + r1(b[1]) + '" width="' + r1(b[2]) + '" height="' + r1(b[3]) + '" rx="4" fill="' + P.desk + '" stroke="' + P.deskLine + '" stroke-width="2"/>';
    g.div.forEach(function (l) { s += '<line x1="' + r1(l[0]) + '" y1="' + r1(l[1]) + '" x2="' + r1(l[2]) + '" y2="' + r1(l[3]) + '" stroke="' + P.divider + '" stroke-width="1.4"/>'; });
  }
  return s;
};
function labelGeo(it, g) {
  var w = g.w, h = g.h, s = '';
  if (it.kind === 'front' || it.kind === 'back') s += '<rect x="' + (-w / 2) + '" y="' + (-h / 2) + '" width="' + w + '" height="' + h + '" rx="6" fill="' + P.bar + '"/>';
  else if (it.kind === 'board') s += '<rect x="' + (-w / 2) + '" y="' + (-h / 2) + '" width="' + w + '" height="' + h + '" rx="3" fill="#FFFFFF" stroke="' + P.wall + '" stroke-width="3"/>';
  else if (it.kind === 'window') {
    s += '<rect x="' + (-w / 2) + '" y="' + (-h / 2) + '" width="' + w + '" height="' + h + '" fill="' + P.window + '" stroke="' + P.windowLine + '" stroke-width="2"/>';
    s += '<line x1="' + (-w / 2) + '" y1="0" x2="' + (w / 2) + '" y2="0" stroke="' + P.windowLine + '" stroke-width="1" opacity=".5"/>';
  } else if (it.kind === 'door') {
    var a = w / 2;
    s += '<rect x="' + (-a) + '" y="' + (-a) + '" width="' + w + '" height="' + w + '" fill="#fff" fill-opacity="0"/>';
    s += '<line x1="' + a + '" y1="' + (-a) + '" x2="' + (-a) + '" y2="' + (-a) + '" stroke="' + P.wall + '" stroke-width="3" stroke-linecap="round"/>';
    s += '<path d="M' + (-a) + ' ' + (-a) + ' A' + w + ' ' + w + ' 0 0 0 ' + a + ' ' + a + '" fill="none" stroke="' + P.wall + '" stroke-width="1.4" stroke-dasharray="5 4"/>';
  } else s += '<rect x="' + (-w / 2) + '" y="' + (-h / 2) + '" width="' + w + '" height="' + h + '" rx="8" fill="' + P.note + '" stroke="' + P.noteLine + '" stroke-width="1.6" stroke-dasharray="6 4"/>';
  return s;
}
function view(st, p) { var D = S.dims(st); return st.view === 'bottom' ? {x:D.w - p.x, y:D.h - p.y} : p; }
S.view = view;
function itemTexts(st, it, o) {
  var flip = st.view === 'bottom' ? 180 : 0, g = geom(it), s = '', p;
  if (it.type === 'label') {
    var L = S.LABELS[it.kind], txt = it.text != null ? it.text : L.text;
    if (!txt) return '';
    var c = it.kind === 'door' ? rotPt(g.w * 0.08, -g.w * 0.08, it.rot || 0) : {x:0, y:0};
    p = view(st, {x:it.x + c.x, y:it.y + c.y});
    var maxW = it.kind === 'door' ? g.w * 0.9 : g.w - 14, maxH = it.kind === 'door' ? 30 : g.h - 4;
    var big = {front:17, back:17, board:15, window:12.5, door:13, note:15}[it.kind];
    var fit = fitText(txt, maxW, Math.max(maxH, 12), big, 8);
    if (it.kind !== 'note' && fit.lines.length > 1) fit = {fs:fit.fs, lines:[fit.lines.join(' ')]};
    return textSvg(p.x, p.y, fit, {fill:(it.kind === 'front' || it.kind === 'back') ? P.barInk : P.ink,
      weight:(it.kind === 'window' || it.kind === 'door') ? 600 : 700, rot:upright((it.rot || 0) + flip)});
  }
  if (it.type === 'teacher') {
    p = view(st, it);
    return textSvg(p.x, p.y, fitText('Teacher', (sideways(it.rot || 0) ? g.body[3] : g.body[2]) - 16, 40, 15, 9), {fill:P.teacherLine, weight:700});
  }
  var side = sideways(it.rot || 0), tagColors = {};
  (st.tags || []).forEach(function (t) { tagColors[t.id] = t.color; });
  g.seats.forEach(function (q, i) {
    var sid = st.seats[it.id + ':' + i]; if (!sid) return;
    var stu = S.student(st, sid); if (!stu) return;
    var c = rotPt(q[0], q[1], it.rot || 0), pp = view(st, {x:it.x + c.x, y:it.y + c.y});
    var w = side ? q[3] : q[2], h = side ? q[2] : q[3];
    var dots = o.tags ? (stu.tags || []).filter(function (t) { return tagColors[t]; }) : [];
    var fit = fitText(S.shownName(stu.name, st.nameStyle), w - 10, h - (dots.length ? 12 : 6), o.big ? 22 : 15, 8);
    s += textSvg(pp.x, pp.y + (dots.length ? 3 : 0), fit, {});
    dots.forEach(function (t, k) {
      var dx = (k - (dots.length - 1) / 2) * 9;
      var top = view(st, {x:it.x + c.x, y:it.y + c.y}), yy = top.y - h / 2 + 7;
      s += '<circle cx="' + r1(top.x + dx) + '" cy="' + r1(yy) + '" r="3.6" fill="' + tagColors[t] + '"/>';
    });
  });
  return s;
}
function deskTags(st) {
  if (!st.deskNums) return '';
  var s = '';
  S.deskOrder(st).forEach(function (it, n) {
    var g = geom(it), c = g.kind === 'round' ? {x:0, y:0} : rotPt(g.body[0], g.body[1], it.rot || 0);
    var p = view(st, {x:it.x + c.x, y:it.y + c.y}), label = String(n + 1), rr = label.length > 1 ? 11 : 9.5;
    s += '<circle cx="' + r1(p.x) + '" cy="' + r1(p.y) + '" r="' + rr + '" fill="' + P.tag + '"/>';
    s += '<text x="' + r1(p.x) + '" y="' + r1(p.y + 3.8) + '" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">' + label + '</text>';
  });
  return s;
}
/* o: interactive, mode ('arrange'|'students'), sel (ids), grid, mini, big, hl {key:'drop'|'flash'}, warn {key:1},
      pick (seat key), tags (bool), marquee {x1,y1,x2,y2} in display coords */
S.roomSvg = function (st, o) {
  o = o || {};
  var D = S.dims(st), s = '', g = '', sel = o.sel || [];
  s += '<rect x="0" y="0" width="' + D.w + '" height="' + D.h + '" fill="' + P.paper + '"/>';
  if (o.grid) s += '<rect x="0" y="0" width="' + D.w + '" height="' + D.h + '" fill="url(#mkgrid)"/>';
  st.items.forEach(function (it) {
    g += '<g data-item="' + it.id + '" transform="translate(' + r1(it.x) + ' ' + r1(it.y) + ') rotate(' + r1(it.rot || 0) + ')">' + S.itemGeoSvg(it);
    if (o.interactive && o.mode === 'arrange' && sel.indexOf(it.id) >= 0) {
      var gm = geom(it), b = 8;
      g += '<rect x="' + r1(-gm.w / 2 - b) + '" y="' + r1(-gm.h / 2 - b) + '" width="' + r1(gm.w + 2 * b) + '" height="' + r1(gm.h + 2 * b) + '" rx="8" fill="none" stroke="' + P.sel + '" stroke-width="2" stroke-dasharray="6 4"/>';
      if (sel.length === 1) {
        var hy = -gm.h / 2 - b;
        g += '<line x1="0" y1="' + r1(hy) + '" x2="0" y2="' + r1(hy - 22) + '" stroke="' + P.sel + '" stroke-width="2"/>';
        g += '<circle data-handle="rotate" cx="0" cy="' + r1(hy - 30) + '" r="9" fill="#fff" stroke="' + P.sel + '" stroke-width="2.5"/>';
        g += '<circle data-handle="rotate" cx="0" cy="' + r1(hy - 30) + '" r="20" fill="#fff" fill-opacity="0"/>';
      }
    }
    g += '</g>';
  });
  // seat layer (students mode) and highlights, in reading order so Tab moves front to back
  var hl = o.hl || {}, warn = o.warn || {}, lay = '';
  if (o.interactive && o.mode === 'students' || Object.keys(hl).length) {
    S.seatList(st).forEach(function (si) {
      var it = si.item, q = si.q, key = si.key, filled = !!st.seats[key];
      var inner = '';
      var x = r1(q[0] - q[2] / 2 + 3), y = r1(q[1] - q[3] / 2 + 3), w = q[2] - 6, h = q[3] - 6;
      if (hl[key]) inner += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="5" fill="' + P.drop + '" fill-opacity="' + (hl[key] === 'flash' ? 0.95 : 0.7) + '"' + (hl[key] === 'flash' ? ' stroke="' + P.picked + '" stroke-width="4"' : '') + '/>';
      if (o.interactive && o.mode === 'students') {
        var stroke = 'none', dash = '', sw = 1.3;
        if (!filled) { stroke = P.emptySeat; dash = ' stroke-dasharray="4 3"'; }
        if (warn[key]) { stroke = P.warn; dash = ' stroke-dasharray="5 3"'; sw = 2.4; }
        if (o.pick === key) { stroke = P.picked; dash = ''; sw = 3.5; }
        var stu = filled ? S.student(st, st.seats[key]) : null;
        inner += '<rect data-seat="' + key + '" tabindex="0" role="button" aria-label="' + esc(S.seatLabel(si) + ', ' + (stu ? stu.name : 'empty')) + '" x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="5" fill="#fff" fill-opacity="0" stroke="' + stroke + '" stroke-width="' + sw + '"' + dash + '/>';
      }
      if (inner) lay += '<g transform="translate(' + r1(it.x) + ' ' + r1(it.y) + ') rotate(' + r1(it.rot || 0) + ')">' + inner + '</g>';
    });
  }
  var both = g + lay;
  s += st.view === 'bottom' ? '<g transform="rotate(180 ' + D.w / 2 + ' ' + D.h / 2 + ')">' + both + '</g>' : both;
  if (!o.mini) {
    st.items.forEach(function (it) { s += itemTexts(st, it, o); });
    s += deskTags(st);
  }
  s += '<rect x="0" y="0" width="' + D.w + '" height="' + D.h + '" fill="none" stroke="' + P.wall + '" stroke-width="6" pointer-events="none"/>';
  if (o.marquee) {
    var mq = o.marquee;
    s += '<rect x="' + r1(mq.x1) + '" y="' + r1(mq.y1) + '" width="' + r1(mq.x2 - mq.x1) + '" height="' + r1(mq.y2 - mq.y1) + '" fill="' + P.sel + '" fill-opacity=".08" stroke="' + P.sel + '" stroke-width="1.5" stroke-dasharray="5 4" pointer-events="none"/>';
  }
  return s;
};
S.exportSvg = function (st, o) {
  o = o || {};
  var D = S.dims(st), pad = 36, title = (st.title || '').trim() || st.name, note = (st.note || '').trim();
  var top = note ? 104 : 80, W = D.w + pad * 2, H = D.h + top + pad;
  var s = '<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" font-family="' + S.FONT + '">';
  s += '<rect width="' + W + '" height="' + H + '" fill="#fff"/>';
  s += '<text x="' + pad + '" y="52" font-size="30" font-weight="700" fill="' + P.ink + '">' + esc(title) + '</text>';
  if (note) s += '<text x="' + pad + '" y="80" font-size="17" fill="' + P.muted + '">' + esc(note) + '</text>';
  s += '<g transform="translate(' + pad + ' ' + top + ')">' + S.roomSvg(st, {big:o.big, tags:o.tags}) + '</g></svg>';
  return s;
};

/* Substitute notes: returns one or more page-shaped SVGs (same aspect as the paper). */
S.notesSvgs = function (st, paper) {
  var pw = 1100, ph = Math.round(1100 * paper.h / paper.w), m = 56, colW = pw - 2 * m;
  var pages = [], cur = null, y = 0;
  var seats = S.seatList(st), info = {};
  seats.forEach(function (s) { info[s.key] = s; });
  function newPage() { cur = []; pages.push(cur); y = m; }
  function need(h) { if (!cur || y + h > ph - m) newPage(); }
  function wrap(text, fs, maxW, wt) {
    var words = String(text).split(/\s+/), lines = [], line = '';
    words.forEach(function (w) { var t = line ? line + ' ' + w : w; if (textW(t, fs, wt || 400) > maxW && line) { lines.push(line); line = w; } else line = t; });
    if (line) lines.push(line);
    return lines;
  }
  function para(text, fs, wt, color, x, w) {
    String(text).split(/\n/).forEach(function (ln) {
      var lines = ln.trim() ? wrap(ln, fs, w || colW, wt) : [''];
      lines.forEach(function (l) { need(fs * 1.45); cur.push('<text x="' + (x || m) + '" y="' + r1(y + fs) + '" font-size="' + fs + '" font-weight="' + (wt || 400) + '" fill="' + (color || P.ink) + '">' + esc(l) + '</text>'); y += fs * 1.45; });
    });
  }
  function heading(t) { need(60); y += 14; para(t, 21, 700); y += 4; }
  newPage();
  var title = (st.title || '').trim() || st.name;
  para('Notes for a substitute', 30, 700);
  para(title + ((st.note || '').trim() ? ', ' + st.note.trim() : ''), 17, 400, P.muted);
  y += 6;
  if ((st.subNotes || '').trim()) { heading('From the teacher'); para(st.subNotes.trim(), 16); }
  var nm = function (sid) { var s = S.student(st, sid); return s ? s.name : '?'; };
  var where = function (sid) { var k = S.seatOf(st, sid); return k && info[k] ? S.seatLabel(info[k]) : 'Not seated'; };
  var noted = st.students.filter(function (s) { return (s.note || '').trim() || (s.needs || []).length; });
  noted.sort(function (a, b) { return S.lastFirst(a.name).localeCompare(S.lastFirst(b.name)); });
  if (noted.length) {
    heading('Students to know about');
    noted.forEach(function (s) {
      var bits = (s.needs || []).map(S.needText);
      if ((s.note || '').trim()) bits.push(s.note.trim());
      need(30);
      cur.push('<text x="' + m + '" y="' + r1(y + 16) + '" font-size="16" font-weight="700" fill="' + P.ink + '">' + esc(s.name) + '</text>');
      cur.push('<text x="' + (m + 250) + '" y="' + r1(y + 16) + '" font-size="14" fill="' + P.muted + '">' + esc(where(s.id)) + '</text>');
      var lines = wrap(bits.join('. '), 15, colW - 420);
      var yy = y;
      lines.forEach(function (l, i) { cur.push('<text x="' + (m + 420) + '" y="' + r1(yy + 16 + i * 21) + '" font-size="15" fill="' + P.ink + '">' + esc(l) + '</text>'); });
      y += Math.max(1, lines.length) * 21 + 8;
    });
  }
  var apart = (st.rules || []).filter(function (r) { return r.type === 'apart'; });
  if (apart.length) {
    heading('Keep these students apart');
    apart.forEach(function (r) { para(nm(r.a) + ' and ' + nm(r.b), 16); });
  }
  if (st.students.length) {
    heading('Class list');
    var list = st.students.slice().sort(function (a, b) { return S.lastFirst(a.name).localeCompare(S.lastFirst(b.name)); });
    var cols = 3, cw = colW / cols, rows = Math.ceil(list.length / cols), i0 = 0;
    while (i0 < list.length) {
      need(26);
      var fitRows = Math.max(1, Math.floor((ph - m - y) / 24)), chunkRows = Math.min(fitRows, Math.ceil((list.length - i0) / cols));
      for (var c = 0; c < cols; c++) for (var r = 0; r < chunkRows; r++) {
        var s = list[i0 + c * chunkRows + r]; if (!s) continue;
        var parts = s.name.trim().split(/\s+/), label = parts.length > 1 ? parts[parts.length - 1] + ', ' + parts.slice(0, -1).join(' ') : s.name;
        var k = S.seatOf(st, s.id), seatTxt = k && info[k] ? String(info[k].desk) + (info[k].multi ? info[k].letter : '') : '–';
        cur.push('<rect x="' + r1(m + c * cw) + '" y="' + r1(y + r * 24 + 4) + '" width="14" height="14" rx="2" fill="none" stroke="' + P.muted + '"/>');
        cur.push('<text x="' + r1(m + c * cw + 22) + '" y="' + r1(y + r * 24 + 16) + '" font-size="14.5" fill="' + P.ink + '">' + esc(label) + '</text>');
        if (st.deskNums) cur.push('<text x="' + r1(m + (c + 1) * cw - 18) + '" y="' + r1(y + r * 24 + 16) + '" text-anchor="end" font-size="13" fill="' + P.muted + '">' + seatTxt + '</text>');
      }
      i0 += chunkRows * cols; y += chunkRows * 24 + 4;
      if (i0 < list.length) newPage();
    }
  }
  return pages.map(function (items, i) {
    return '<svg xmlns="http://www.w3.org/2000/svg" width="' + pw + '" height="' + ph + '" viewBox="0 0 ' + pw + ' ' + ph + '" font-family="' + S.FONT + '"><rect width="' + pw + '" height="' + ph + '" fill="#fff"/>' +
      items.join('') + (pages.length > 1 ? '<text x="' + (pw - m) + '" y="' + (ph - 24) + '" text-anchor="end" font-size="12" fill="' + P.muted + '">Page ' + (i + 1) + ' of ' + pages.length + '</text>' : '') + '</svg>';
  });
};

/* ---------- presets ---------- */
function L(kind, x, y, extra) {
  var it = {id:uid(), type:'label', kind:kind, x:x, y:y, rot:0, w:S.LABELS[kind].w, text:S.LABELS[kind].text};
  for (var k in extra) it[k] = extra[k];
  if (kind !== 'door') it.h = S.LABELS[kind].h;
  return it;
}
S.newItem = function (spec, x, y, rot) {
  var it = {id:uid(), x:Math.round(x || 0), y:Math.round(y || 0), rot:rot || 0};
  for (var k in spec) it[k] = spec[k];
  if (it.type === 'label') { var Lb = S.LABELS[it.kind]; if (it.w == null) it.w = Lb.w; if (it.kind !== 'door' && it.h == null) it.h = Lb.h; if (it.text == null) it.text = Lb.text; }
  return it;
};
function gridOf(spec, cols, rows, x0, x1, y0, y1) {
  var out = [];
  for (var j = 0; j < rows; j++) for (var i = 0; i < cols; i++) out.push(S.newItem(spec, x0 + (x1 - x0) * (i + 0.5) / cols, y0 + (y1 - y0) * (j + 0.5) / rows));
  return out;
}
var ONE = {type:'desk', n:1, rows:1}, TWO = {type:'desk', n:2, rows:1};
S.PRESETS = [
  ['rows', 'Rows', '30 single desks'],
  ['pairs', 'Pairs', '15 pair desks'],
  ['group4', 'Groups of 4', '8 groups'],
  ['group6', 'Groups of 6', '6 groups'],
  ['ushape', 'U-shape', 'Double U for discussion'],
  ['round', 'Round tables', '6 tables of 6'],
  ['exam', 'Testing rows', '25 spaced desks'],
  ['blank', 'Empty room', 'Add desks yourself']
];
S.presetItems = function (key, D) {
  var W = D.w, H = D.h, i;
  var base = [L('front', W / 2, 30, {w:Math.min(560, W - 300)}), L('door', W - 46, 118, {}), L('window', 16, H / 2 + 40, {rot:90, w:Math.min(420, H - 260)})];
  if (key !== 'blank') base.push(S.newItem({type:'teacher'}, W - 215, 102));
  var d = [];
  if (key === 'rows') d = gridOf(ONE, 6, 5, 80, W - 80, 170, H - 30);
  if (key === 'exam') d = gridOf(ONE, 5, 5, 110, W - 110, 170, H - 30);
  if (key === 'pairs') d = gridOf(TWO, 3, 5, 80, W - 80, 170, H - 30);
  if (key === 'group4') d = gridOf({type:'desk', n:4, rows:2}, 4, 2, 50, W - 50, 200, H - 30);
  if (key === 'group6') d = gridOf({type:'desk', n:6, rows:2}, 3, 2, 50, W - 50, 200, H - 30);
  if (key === 'round') d = gridOf({type:'round', n:6}, 3, 2, 50, W - 50, 200, H - 30);
  if (key === 'ushape') {
    var armTop = 220, armBot = H - 150;
    for (i = 0; i < 5; i++) { var y = armTop + (armBot - armTop) * i / 4; d.push(S.newItem(ONE, 150, y, 90)); d.push(S.newItem(ONE, W - 150, y, -90)); }
    for (i = 0; i < 7; i++) d.push(S.newItem(ONE, 230 + (W - 460) * i / 6, H - 80, 0));
    var iTop = 260, iBot = H - 250;
    for (i = 0; i < 4; i++) { var y2 = iTop + (iBot - iTop) * i / 3; d.push(S.newItem(ONE, 262, y2, 90)); d.push(S.newItem(ONE, W - 262, y2, -90)); }
    for (i = 0; i < 5; i++) d.push(S.newItem(ONE, 340 + (W - 680) * i / 4, H - 190, 0));
  }
  return base.concat(d);
};
S.ADD_DESKS = [
  ['Single desk', {type:'desk', n:1, rows:1}],
  ['Pair desk', {type:'desk', n:2, rows:1}],
  ['Lab table of 4', {type:'desk', n:4, rows:1}],
  ['Group of 3', {type:'desk', n:3, rows:2}],
  ['Group of 4', {type:'desk', n:4, rows:2}],
  ['Group of 5', {type:'desk', n:5, rows:2}],
  ['Group of 6', {type:'desk', n:6, rows:2}],
  ['Group of 8', {type:'desk', n:8, rows:2}],
  ['Round table of 4', {type:'round', n:4}],
  ['Round table of 6', {type:'round', n:6}],
  ['Round table of 8', {type:'round', n:8}],
  ["Teacher's desk", {type:'teacher'}]
];
S.ADD_LABELS = [
  ['Front of room', 'front'], ['Back of room', 'back'], ['Whiteboard', 'board'], ['Projector screen', 'board'],
  ['Door', 'door'], ['Windows', 'window'], ['Custom label', 'note']
];
S.miniSvg = function (items, D) {
  var st = {items:items, seats:{}, students:[], roomW:D.w, roomH:D.h, view:'top'};
  return '<svg viewBox="-8 -8 ' + (D.w + 16) + ' ' + (D.h + 16) + '" aria-hidden="true">' + S.roomSvg(st, {mini:true}) + '</svg>';
};
S.iconSvg = function (spec) {
  var it = S.newItem(spec, 0, 0, 0);
  if (it.type === 'label') { it.w = it.kind === 'door' ? 80 : 120; if (it.kind !== 'door') it.h = it.kind === 'window' ? 24 : 40; }
  var g = geom(it), s = Math.max(g.w, g.h * 1.25) / 2 + 6;
  return '<svg viewBox="' + r1(-s) + ' ' + r1(-s * 0.8) + ' ' + r1(2 * s) + ' ' + r1(1.6 * s) + '" aria-hidden="true"><g>' + S.itemGeoSvg(it) + '</g></svg>';
};

/* ---------- class lists ---------- */
function cleanName(l) {
  l = l.replace(/\t+/g, ' ').replace(/^\d+[.)]\s*/, '').trim();
  var mm = l.match(/^([^,]+),\s*(.+)$/);
  if (mm) l = mm[2].trim() + ' ' + mm[1].trim();
  return l.replace(/\s+/g, ' ');
}
/* textarea: one name per line ("Smith, Maya" → Maya Smith), or one line of comma-separated names */
S.parseNames = function (text) {
  var lines = String(text).split(/\r?\n/).map(function (s) { return s.trim(); }).filter(Boolean);
  if (lines.length === 1 && /[,;]/.test(lines[0])) return lines[0].split(/[,;]/).map(function (s) { return s.trim().replace(/\s+/g, ' '); }).filter(Boolean);
  return lines.map(cleanName).filter(Boolean);
};
function parseCsv(text) {
  var first = text.split(/\r?\n/)[0] || '', delim = (first.split('\t').length > first.split(',').length) ? '\t' : (first.split(';').length > first.split(',').length ? ';' : ',');
  var rows = [], row = [], cell = '', q = false;
  for (var i = 0; i < text.length; i++) {
    var ch = text[i];
    if (q) { if (ch === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += ch; continue; }
    if (ch === '"') q = true;
    else if (ch === delim) { row.push(cell); cell = ''; }
    else if (ch === '\n' || ch === '\r') { if (ch === '\r' && text[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
    else cell += ch;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  return rows.map(function (r) { return r.map(function (c) { return c.trim(); }); }).filter(function (r) { return r.some(Boolean); });
}
S.parseCsv = parseCsv;
/* Roster files from a student information system, Google Classroom or a spreadsheet. */
S.parseRoster = function (text) {
  text = String(text).replace(/^\uFEFF/, '');
  var rows = parseCsv(text); if (!rows.length) return [];
  var h = rows[0].map(function (c) { return c.toLowerCase(); });
  var find = function (re, not) { for (var i = 0; i < h.length; i++) if (re.test(h[i]) && !(not && not.test(h[i]))) return i; return -1; };
  var fi = find(/first|given|preferred/, /last/), li = find(/last|surname|family/, /first/);
  var ni = find(/^(student\s*)?(full\s*)?name$|^student$|^name\b/, /first|last|user|email|teacher|parent|guardian/);
  var hasHeader = fi >= 0 || li >= 0 || ni >= 0 || h.some(function (c) { return /email|id|grade|period/.test(c); });
  var body = hasHeader ? rows.slice(1) : rows, out = [];
  body.forEach(function (r) {
    var name = '';
    if (fi >= 0 && li >= 0) name = (r[fi] || '') + ' ' + (r[li] || '');
    else if (ni >= 0) name = cleanName(r[ni] || '');
    else if (!hasHeader && r.length >= 2 && r[0] && r[1] && !/\s|@|\d/.test(r[0]) && !/@|\d/.test(r[1])) name = r[1] + ' ' + r[0];   // "Smith,Maya"
    else name = cleanName(r.filter(function (c) { return c && !/@|^\d+$/.test(c); })[0] || '');
    name = name.replace(/\s+/g, ' ').trim();
    if (name && !/@/.test(name)) out.push(name);
  });
  return out;
};

/* ---------- PDF (one JPEG image per page) ---------- */
S.pdf = function (images, paper) {
  var pw = paper.w, ph = paper.h, mg = 24, n = images.length;
  var parts = [], len = 0, offs = [], enc = (typeof TextEncoder !== 'undefined') ? new TextEncoder() : null;
  function bytes(s) { if (enc) return enc.encode(s); var b = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) b[i] = s.charCodeAt(i) & 255; return b; }
  function push(x) { var b = typeof x === 'string' ? bytes(x) : x; parts.push(b); len += b.length; }
  function obj(num, body) { offs[num] = len; push(num + ' 0 obj\n'); body(); push('\nendobj\n'); }
  push('%PDF-1.4\n%\u00e2\u00e3\u00cf\u00d3\n');
  var kids = []; for (var k = 0; k < n; k++) kids.push((3 + k * 3) + ' 0 R');
  obj(1, function () { push('<< /Type /Catalog /Pages 2 0 R >>'); });
  obj(2, function () { push('<< /Type /Pages /Kids [' + kids.join(' ') + '] /Count ' + n + ' >>'); });
  images.forEach(function (im, k) {
    var pg = 3 + k * 3, xo = pg + 1, ct = pg + 2;
    var sc = Math.min((pw - 2 * mg) / im.w, (ph - 2 * mg) / im.h), dw = im.w * sc, dh = im.h * sc, dx = (pw - dw) / 2, dy = (ph - dh) / 2;
    var content = 'q ' + dw.toFixed(2) + ' 0 0 ' + dh.toFixed(2) + ' ' + dx.toFixed(2) + ' ' + dy.toFixed(2) + ' cm /Im0 Do Q';
    obj(pg, function () { push('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + pw + ' ' + ph + '] /Resources << /XObject << /Im0 ' + xo + ' 0 R >> >> /Contents ' + ct + ' 0 R >>'); });
    obj(xo, function () { push('<< /Type /XObject /Subtype /Image /Width ' + im.w + ' /Height ' + im.h + ' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ' + im.bytes.length + ' >>\nstream\n'); push(im.bytes); push('\nendstream'); });
    obj(ct, function () { push('<< /Length ' + content.length + ' >>\nstream\n' + content + '\nendstream'); });
  });
  var total = 3 + n * 3, xref = len, x = 'xref\n0 ' + total + '\n0000000000 65535 f \n';
  for (var i = 1; i < total; i++) x += String(offs[i]).padStart(10, '0') + ' 00000 n \n';
  push(x + 'trailer\n<< /Size ' + total + ' /Root 1 0 R >>\nstartxref\n' + xref + '\n%%EOF\n');
  var out = new Uint8Array(len), p = 0; parts.forEach(function (b) { out.set(b, p); p += b.length; });
  return out;
};

/* ---------- CSV export ---------- */
S.csv = function (st) {
  var cell = function (v) { v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
  var rows = [['Desk', 'Seat', 'Student', 'Seat needs', 'Note']];
  var line = function (stu) { return [stu ? (stu.needs || []).map(S.needText).join('; ') : '', stu ? (stu.note || '') : '']; };
  S.seatList(st).forEach(function (s) {
    var stu = S.student(st, st.seats[s.key]);
    rows.push([s.desk, s.multi ? s.letter : '', stu ? stu.name : '(empty)'].concat(line(stu)));
  });
  st.students.forEach(function (s) { if (!S.seatOf(st, s.id)) rows.push(['Not seated', '', s.name].concat(line(s))); });
  return '\uFEFF' + rows.map(function (r) { return r.map(cell).join(','); }).join('\r\n');
};

if (typeof module !== 'undefined' && module.exports) module.exports = S;
else root.SEAT = S;
})(typeof window !== 'undefined' ? window : this);
