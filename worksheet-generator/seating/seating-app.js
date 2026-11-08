/* Seating Chart Maker app. Depends on seating-core.js (window.SEAT). */
(function () {
'use strict';
var S = window.SEAT, esc = S.esc;
var STORE = 'mkseating:v1';
var DAY = 864e5;

/* ================= state ================= */
var data, hist = [], future = [];
var ui = { tab:'room', sel:[], picked:null, hover:null, drag:null, marquee:null, alignOpen:false,
           flash:null, pickPool:null, pickTimer:null, proj:false, projFs:false, ruleSig:'', copySig:'', removeArm:false };

function newChart(name) {
  return { id:S.uid(), name:name, title:'', note:'', subNotes:'', roomW:1024, roomH:768, snap:true, deskNums:false,
    nameStyle:'full', view:'top', showTags:true, items:[], students:[], seats:{}, rules:[], tags:[], history:[],
    auto:{spread:'any', rules:true, needs:true, fresh:true, balance:false} };
}
function normalize(c) {
  var d = newChart(c.name || 'Chart');
  for (var k in d) if (c[k] === undefined || c[k] === null) c[k] = d[k];
  if (!c.id) c.id = S.uid();
  if (c.room) {
    var old = {standard:[1000, 750], wide:[1200, 750], deep:[1000, 950], large:[1300, 950]}[c.room] || [1000, 750];
    if (!c.roomW || c.roomW === 1024 && c.roomH === 768) { c.roomW = old[0]; c.roomH = old[1]; }
    delete c.room;
  }
  c.items = (c.items || []).map(S.migrateItem).filter(S.validItem);
  c.students = (c.students || []).filter(function (s) { return s && s.id && s.name; });
  c.students.forEach(function (s) { s.needs = s.needs || []; s.tags = s.tags || []; if (s.note == null) s.note = ''; s.pin = !!s.pin; });
  c.auto = Object.assign({spread:'any', rules:true, needs:true, fresh:true, balance:false}, c.auto || {});
  c.rules = c.rules || []; c.tags = c.tags || []; c.history = c.history || []; c.seats = c.seats || {};
  S.cleanSeats(c);
  return c;
}
function load() {
  try { data = JSON.parse(localStorage.getItem(STORE)); } catch (e) { data = null; }
  if (!data || !Array.isArray(data.charts) || !data.charts.length) { var c = newChart('Period 1'); data = {charts:[c], cur:c.id}; }
  data.charts.forEach(normalize);
  data.prefs = Object.assign({paper:'letter', big:false, sub:false, tags:false}, data.prefs || {});
  if (!data.firstUse) data.firstUse = Date.now();
  if (!data.charts.some(function (c) { return c.id === data.cur; })) data.cur = data.charts[0].id;
}
var saveTimer;
function save() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(function () {
    try { localStorage.setItem(STORE, JSON.stringify(data)); }
    catch (e) { toast('This browser could not save the chart. Download a backup from the Charts menu.'); }
  }, 150);
}
function flushSave() { clearTimeout(saveTimer); try { localStorage.setItem(STORE, JSON.stringify(data)); } catch (e) {} }
window.addEventListener('pagehide', flushSave);
document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') flushSave(); });
function cur() { for (var i = 0; i < data.charts.length; i++) if (data.charts[i].id === data.cur) return data.charts[i]; return data.charts[0]; }
function dims() { return S.dims(cur()); }
function mode() { return ui.tab === 'room' ? 'arrange' : 'students'; }
function snapshot() { return JSON.stringify(cur()); }
function pushHist(snap) { hist.push(snap); if (hist.length > 80) hist.shift(); future = []; data.changedAt = Date.now(); }
function change(fn) { pushHist(snapshot()); fn(cur()); after(); }
function replaceCur(json) {
  var c = normalize(JSON.parse(json));
  for (var i = 0; i < data.charts.length; i++) if (data.charts[i].id === c.id) data.charts[i] = c;
}
function undo() { if (!hist.length) return; future.push(snapshot()); replaceCur(hist.pop()); ui.picked = null; after(); }
function redo() { if (!future.length) return; hist.push(snapshot()); replaceCur(future.pop()); ui.picked = null; after(); }
function after() { render(); save(); }
function setPref(fn) { fn(cur()); data.changedAt = Date.now(); save(); render(); }   // settings: saved, not in undo history
function findItem(id) { var st = cur(); for (var i = 0; i < st.items.length; i++) if (st.items[i].id === id) return st.items[i]; return null; }
function selItems() { return ui.sel.map(findItem).filter(Boolean); }

/* ================= small UI helpers ================= */
var $ = function (id) { return document.getElementById(id); };
var svg = $('room'), dlg = $('dlg');
var toastTimer;
function toast(msg, ms) { var t = $('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.classList.remove('show'); }, ms || 3000); }
function plural(n, one, many) { return n + ' ' + (n === 1 ? one : (many || one + 's')); }

/* dialogs: ask({title, text, input, value, ok, danger}) resolves to true/false, or the typed text/null */
function openDialog(html, cls) {
  return new Promise(function (resolve) {
    dlg.className = cls || '';
    dlg.innerHTML = html;
    dlg.returnValue = '';
    dlg.onclose = function () { dlg.onclose = null; resolve(dlg.returnValue); };
    dlg.showModal();
  });
}
function ask(o) {
  var html = '<form method="dialog"><h2>' + esc(o.title) + '</h2>' + (o.text ? '<p>' + esc(o.text) + '</p>' : '') +
    (o.input ? '<input id="dlgIn" type="text" value="' + esc(o.value || '') + '" aria-label="' + esc(o.title) + '">' : '') +
    '<div class="dlgbtns"><button value="ok" class="btn ' + (o.danger ? 'primary danger' : 'primary') + '">' + esc(o.ok || 'OK') + '</button>' +
    '<button value="cancel" class="btn quiet" formnovalidate>' + esc(o.cancel || 'Cancel') + '</button></div></form>';
  var p = openDialog(html, 'small');
  var inp = $('dlgIn'); if (inp) { inp.focus(); inp.select(); }
  return p.then(function (v) {
    if (o.input) return v === 'ok' ? (inp.value || '').trim() : null;
    return v === 'ok';
  });
}

/* ================= rendering ================= */
function render() {
  var st = cur(), D = dims(), md = mode();
  ui.sel = ui.sel.filter(function (id) { return findItem(id); });
  var ae = document.activeElement, focusSeat = ae && ae.getAttribute && ae.getAttribute('data-seat'), focusChip = ae && ae.getAttribute && ae.getAttribute('data-sid');
  var report = md === 'students' ? S.check(st) : null, warn = {};
  if (report) report.problems.forEach(function (p) { p.keys.forEach(function (k) { warn[k] = 1; }); });
  var hl = {}; if (ui.hover) hl[ui.hover] = 'drop'; if (ui.flash) hl[ui.flash] = 'flash';
  svg.setAttribute('viewBox', '-12 -12 ' + (D.w + 24) + ' ' + (D.h + 24));
  svg.setAttribute('font-family', S.FONT);
  svg.setAttribute('class', md);
  svg.innerHTML = '<defs><pattern id="mkgrid" width="' + S.FT + '" height="' + S.FT + '" patternUnits="userSpaceOnUse"><path d="M' + S.FT + ' 0H0V' + S.FT + '" fill="none" stroke="' + S.P.grid + '" stroke-width="1"/></pattern></defs>' +
    S.roomSvg(st, {interactive:true, mode:md, sel:ui.sel, grid:true, hl:hl, warn:warn, pick:ui.picked && ui.picked.from, tags:st.showTags && md === 'students', marquee:ui.marquee});
  renderTabs(); renderRoomPanel(); renderClassPanel(); renderSeatsPanel(report);
  renderSelbar(); renderHint();
  $('empty').hidden = st.items.length > 0;
  $('wrap').classList.toggle('is-empty', !st.items.length);
  $('undoBtn').disabled = !hist.length; $('redoBtn').disabled = !future.length;
  renderBackupBar();
  if (ui.proj) renderProj();
  if (focusSeat) { var el = svg.querySelector('[data-seat="' + focusSeat + '"]'); if (el) el.focus({preventScroll:true}); }
  if (focusChip) { var ch = document.querySelector('.chip[data-sid="' + focusChip + '"]'); if (ch) ch.focus({preventScroll:true}); }
}
var queued = false;
function renderSoon() { if (queued) return; queued = true; requestAnimationFrame(function () { queued = false; render(); }); }

function renderTabs() {
  ['room', 'class', 'seats'].forEach(function (t) {
    $('tab-' + t).setAttribute('aria-selected', ui.tab === t);
    $('panel-' + t).hidden = ui.tab !== t;
  });
  var st = cur();
  $('chartSel').innerHTML = data.charts.map(function (c) { return '<option value="' + c.id + '"' + (c.id === data.cur ? ' selected' : '') + '>' + esc(c.name) + '</option>'; }).join('');
  if (document.activeElement !== $('titleIn')) $('titleIn').value = st.title;
  if (document.activeElement !== $('noteIn')) $('noteIn').value = st.note;
  $('viewTop').setAttribute('aria-pressed', st.view !== 'bottom'); $('viewBottom').setAttribute('aria-pressed', st.view === 'bottom');
}
function renderRoomPanel() {
  var st = cur(), D = dims();
  if (document.activeElement !== $('roomWIn')) $('roomWIn').value = Math.round(D.w / S.FT);
  if (document.activeElement !== $('roomHIn')) $('roomHIn').value = Math.round(D.h / S.FT);
  $('snapChk').checked = !!st.snap; $('numChk').checked = !!st.deskNums;
}
var NEED_SHORT = {front:'Front', teacher:'By teacher', door:'By door', back:'Back', nowindow:'No windows'};
function byLast(a, b) { return S.lastFirst(a.name).localeCompare(S.lastFirst(b.name)); }
function renderClassPanel() {
  var st = cur(), tagMap = {};
  st.tags.forEach(function (t) { tagMap[t.id] = t; });
  $('studentsHead').textContent = st.students.length ? 'Students (' + st.students.length + ')' : 'Students';
  var list = st.students.slice().sort(byLast);
  $('studentList').innerHTML = list.map(function (s) {
    var b = '';
    s.tags.forEach(function (t) { if (tagMap[t]) b += '<span class="dot" style="background:' + tagMap[t].color + '" title="' + esc(tagMap[t].name) + '"></span>'; });
    s.needs.forEach(function (n) { b += '<span class="badge need">' + NEED_SHORT[n] + '</span>'; });
    var ap = st.rules.filter(function (r) { return r.type === 'apart' && (r.a === s.id || r.b === s.id); }).length;
    var tg = st.rules.filter(function (r) { return r.type === 'together' && (r.a === s.id || r.b === s.id); }).length;
    if (ap) b += '<span class="badge apart">Apart ' + ap + '</span>';
    if (tg) b += '<span class="badge">Works with ' + tg + '</span>';
    if (s.pin) b += '<span class="badge">Pinned</span>';
    if (s.note) b += '<span class="badge">Note</span>';
    return '<button class="srow" data-edit="' + s.id + '"><span class="nm">' + esc(s.name) + '</span><span class="bd">' + b + '</span></button>';
  }).join('');
  // rule pickers: rebuild only when the class list changes so a half-made choice is kept
  var sig = list.map(function (s) { return s.id + s.name; }).join('|');
  if (sig !== ui.ruleSig) {
    ui.ruleSig = sig;
    var opts = '<option value="">Choose a student</option>' + list.map(function (s) { return '<option value="' + s.id + '">' + esc(s.name) + '</option>'; }).join('');
    ['ruleA', 'ruleB'].forEach(function (id) { var el = $(id), v = el.value; el.innerHTML = opts; el.value = S.student(st, v) ? v : ''; });
  }
  $('ruleList').innerHTML = st.rules.map(function (r) {
    var a = S.student(st, r.a), b = S.student(st, r.b);
    return '<div class="rule"><span class="t"><b>' + esc(a.name) + '</b> <span class="kind ' + r.type + '">' + (r.type === 'apart' ? 'keep apart from' : 'works well with') + '</span> <b>' + esc(b.name) + '</b></span>' +
      '<button class="x" data-rule="' + r.id + '" aria-label="Remove this rule" title="Remove">×</button></div>';
  }).join('') || '<p class="note">No rules yet.</p>';
  $('tagList').innerHTML = st.tags.map(function (t) {
    var n = st.students.filter(function (s) { return s.tags.indexOf(t.id) >= 0; }).length;
    return '<span class="tag"><span class="dot" style="background:' + t.color + '"></span>' + esc(t.name) + ' <span class="dim">' + n + '</span><button class="x" data-tag="' + t.id + '" aria-label="Delete tag ' + esc(t.name) + '">×</button></span>';
  }).join('') || '<p class="note">No tags yet.</p>';
  var others = data.charts.filter(function (c) { return c.id !== st.id && c.students.length; });
  var csig = others.map(function (c) { return c.id + c.name + c.students.length; }).join('|');
  if (csig !== ui.copySig) {
    ui.copySig = csig;
    $('copyFromSel').innerHTML = '<option value="">Choose a chart</option>' + others.map(function (c) { return '<option value="' + c.id + '">' + esc(c.name) + ' (' + plural(c.students.length, 'student') + ')</option>'; }).join('');
  }
  $('copyFromWrap').hidden = !others.length;
}
function seatInfoMap(st) { var m = {}; S.seatList(st).forEach(function (s) { m[s.key] = s; }); return m; }
function renderSeatsPanel(report) {
  var st = cur(), info = seatInfoMap(st), total = Object.keys(info).length, seatedN = 0, un = '', se = '';
  st.students.slice().sort(byLast).forEach(function (stu) {
    var k = S.seatOf(st, stu.id), picked = ui.picked && ui.picked.sid === stu.id;
    var where = k && st.deskNums ? info[k].desk + (info[k].multi ? info[k].letter : '') : '';
    var chip = '<span class="chip' + (k ? ' seated' : '') + (picked ? ' picked' : '') + '" data-sid="' + stu.id + '" tabindex="0" role="button" aria-pressed="' + !!picked + '" aria-label="' + esc(stu.name + (k ? ', ' + S.seatLabel(info[k]) : ', not seated') + (stu.pin ? ', pinned' : '')) + '">' +
      esc(stu.name) + (where ? ' <span class="where">' + where + '</span>' : '') + (stu.pin ? ' <span class="where">pinned</span>' : '') + '</span>';
    if (k) { se += chip; seatedN++; } else un += chip;
  });
  $('unseated').innerHTML = un; $('seated').innerHTML = se;
  var n = st.students.length, need = n - seatedN, line;
  if (!n) line = plural(total, 'seat') + ' in the room. Add students in step 2.';
  else {
    line = plural(total, 'seat') + ', ' + plural(n, 'student') + '. ';
    line += need > 0 ? plural(need, 'student') + (need === 1 ? ' needs' : ' need') + ' a seat.' : 'Everyone is seated.';
    if (n > total) line += ' Add ' + plural(n - total, 'more seat') + ' in step 1.';
  }
  $('countLine').textContent = line;
  var a = st.auto;
  $('spreadSel').value = a.spread; $('optRules').checked = a.rules; $('optNeeds').checked = a.needs; $('optFresh').checked = a.fresh; $('optBalance').checked = a.balance;
  var needsN = st.students.filter(function (s) { return s.needs.length; }).length;
  $('optRulesN').textContent = '(' + plural(st.rules.length, 'rule') + ')';
  $('optNeedsN').textContent = '(' + plural(needsN, 'student') + ')';
  $('optFreshN').textContent = st.history.length ? '(' + plural(st.history.length, 'past seating') + ')' : '(none saved yet)';
  $('optBalanceN').textContent = '(' + plural(st.tags.length, 'tag') + ')';
  var pins = st.students.filter(function (s) { return s.pin && S.seatOf(st, s.id); }).length;
  $('pinNote').textContent = pins ? plural(pins, 'pinned student') + ' will stay in ' + (pins === 1 ? 'their seat' : 'their seats') + '.' : '';
  // rules check
  var r = report || S.check(st), html;
  if (!seatedN) html = '<p class="note">Seat students to check rules and seat needs.</p>';
  else if (!r.rules && !r.needs) html = '<p class="note">No seating rules or seat needs apply yet. Add them in step 2.</p>';
  else if (!r.problems.length) html = '<p class="okline">All ' + (r.rules ? plural(r.rules, 'rule') : '') + (r.rules && r.needs ? ' and ' : '') + (r.needs ? plural(r.needs, 'seat need') : '') + ' are met.</p>';
  else html = '<ul>' + r.problems.map(function (p) { return '<li class="prob">' + esc(p.text) + '</li>'; }).join('') + '</ul>' +
    (r.rules + r.needs - r.problems.length > 0 ? '<p class="note" style="margin-top:6px">' + (r.rules + r.needs - r.problems.length) + ' others are met. Seats with a problem have a red outline.</p>' : '');
  if (r.notes.length) html += '<div class="notes">' + r.notes.map(esc).join('<br>') + '</div>';
  $('report').innerHTML = html;
  $('nameStyleSel').value = st.nameStyle; $('tagDotsChk').checked = !!st.showTags;
  $('historyList').innerHTML = st.history.slice().reverse().map(function (h) {
    var d = new Date(h.date);
    var when = d.toLocaleDateString(undefined, {month:'short', day:'numeric', year:'numeric'}) + ' at ' + d.toLocaleTimeString(undefined, {hour:'numeric', minute:'2-digit'});
    return '<div class="hrow"><span class="t">' + esc(when) + '<br><span class="dim">' + plural(Object.keys(h.seats).length, 'student') + ' seated</span></span>' +
      '<button class="btn small" data-hrestore="' + h.id + '">Restore</button><button class="x" data-hdel="' + h.id + '" aria-label="Delete this saved seating">×</button></div>';
  }).join('');
}
function renderHint() {
  var st = cur(), h;
  if (mode() === 'arrange') {
    if (!st.items.length) h = 'Pick a layout to start, or choose Empty room and add desks one at a time.';
    else if (ui.sel.length > 1) h = 'Drag any selected item to move them together. Arrow keys nudge, Delete removes, Ctrl+D copies.';
    else if (ui.sel.length) h = 'Drag to move. Drag the round handle to turn it. Shift-click or drag a box to select more.';
    else h = 'Drag desks and labels to move them. Click one to change it, or drag a box around several.';
  } else if (ui.picked) {
    var s = S.student(st, ui.picked.sid); h = 'Now click a seat for ' + (s ? s.name : 'this student') + '. Click the name again to cancel.';
  } else if (!st.students.length) h = 'Add your class in step 2.';
  else h = 'Drag a name onto a seat, or click a name and then a seat. Drop on a taken seat to swap. Drag a name back to the list to unseat it.';
  $('hint').textContent = h;
}

/* ================= selection bar ================= */
function renderSelbar() {
  var bar = $('selbar'), items = mode() === 'arrange' ? selItems() : [];
  if (!items.length || (ui.drag && ui.drag.moved) || (ui.drag && ui.drag.kind === 'marquee')) { bar.hidden = true; return; }
  var h = '';
  if (items.length === 1) {
    var it = items[0], lab = it.type === 'label', door = lab && it.kind === 'door';
    h += '<button data-sb="rotl" title="Turn left 15° (Shift+R)" aria-label="Turn left 15 degrees">↺</button><button data-sb="rotr" title="Turn right 15° (R)" aria-label="Turn right 15 degrees">↻</button><button data-sb="turn">Turn 90°</button><span class="sep"></span>';
    if (it.type === 'desk' || it.type === 'round') {
      h += '<button data-sb="seatsDown" aria-label="One fewer seat">Seats −</button><button data-sb="seatsUp" aria-label="One more seat">Seats +</button>';
      if (it.type === 'desk' && (it.n || 1) >= 2) h += '<button data-sb="rows">' + (it.rows === 2 ? 'One row' : 'Two rows') + '</button>';
      if (it.type === 'desk') h += '<button data-sb="narrow">Narrower</button><button data-sb="wide">Wider</button>';
      h += '<span class="sep"></span>';
    } else if (it.type === 'teacher') h += '<button data-sb="narrow">Narrower</button><button data-sb="wide">Wider</button><span class="sep"></span>';
    else if (lab) {
      if (!door) h += '<button data-sb="text">Edit text</button>';
      h += '<button data-sb="narrow">' + (door ? 'Smaller' : 'Shorter') + '</button><button data-sb="wide">' + (door ? 'Bigger' : 'Longer') + '</button><span class="sep"></span>';
    }
  } else {
    h += '<span class="lbl">' + items.length + ' selected</span><button data-sb="turn">Turn 90°</button>' +
      '<button data-sb="align" aria-expanded="' + ui.alignOpen + '">Line up ▾</button><span class="sep"></span>';
  }
  h += '<button data-sb="dup" title="Ctrl+D">Copy</button><button data-sb="del" class="danger" title="Delete">Delete</button>';
  if (items.length > 1 && ui.alignOpen) {
    h += '<span class="break"></span>' + [['left', 'Left edges'], ['cx', 'Centers'], ['right', 'Right edges'], ['top', 'Top edges'], ['cy', 'Middles'], ['bottom', 'Bottom edges'], ['spaceX', 'Space across'], ['spaceY', 'Space down']]
      .map(function (a) { return '<button data-al="' + a[0] + '">' + a[1] + '</button>'; }).join('');
  }
  bar.innerHTML = h; bar.hidden = false;
  var w = $('wrap').getBoundingClientRect(), box = null;
  items.forEach(function (it) {
    var el = svg.querySelector('[data-item="' + it.id + '"]'); if (!el) return;
    var r = el.getBoundingClientRect();
    box = box ? {left:Math.min(box.left, r.left), top:Math.min(box.top, r.top), right:Math.max(box.right, r.right), bottom:Math.max(box.bottom, r.bottom)} : {left:r.left, top:r.top, right:r.right, bottom:r.bottom};
  });
  if (!box) { bar.hidden = true; return; }
  var bw = bar.offsetWidth, bh = bar.offsetHeight;
  var left = Math.max(6, Math.min((box.left + box.right) / 2 - w.left - bw / 2, w.width - bw - 6));
  var top = box.top - w.top - bh - 8;
  if (top < 4) top = box.bottom - w.top + 8;
  if (top + bh > w.height - 4) top = Math.max(4, box.top - w.top + 8);
  bar.style.left = left + 'px'; bar.style.top = top + 'px';
}

/* ================= room geometry helpers ================= */
function svgPt(e) {
  var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
  var p = pt.matrixTransform(svg.getScreenCTM().inverse()), D = dims();
  return cur().view === 'bottom' ? {x:D.w - p.x, y:D.h - p.y} : {x:p.x, y:p.y};
}
function overlaps(a, b) { return a.x1 < b.x2 && a.x2 > b.x1 && a.y1 < b.y2 && a.y2 > b.y1; }
function unionBox(items) {
  var b = null;
  items.forEach(function (it) { var x = S.itemBox(it); b = b ? {x1:Math.min(b.x1, x.x1), y1:Math.min(b.y1, x.y1), x2:Math.max(b.x2, x.x2), y2:Math.max(b.y2, x.y2)} : x; });
  return b;
}
function clampGroup(items) {
  var D = dims(), b = unionBox(items), dx = 0, dy = 0;
  if (!b) return;
  if (b.x2 - b.x1 <= D.w) { if (b.x1 < 0) dx = -b.x1; if (b.x2 > D.w) dx = D.w - b.x2; } else dx = D.w / 2 - (b.x1 + b.x2) / 2;
  if (b.y2 - b.y1 <= D.h) { if (b.y1 < 0) dy = -b.y1; if (b.y2 > D.h) dy = D.h - b.y2; } else dy = D.h / 2 - (b.y1 + b.y2) / 2;
  items.forEach(function (it) { it.x = Math.round(it.x + dx); it.y = Math.round(it.y + dy); });
}
function placeFree(it) {
  var st = cur(), D = dims(), tries = [[0, 0]];
  for (var rr = 1; rr < 14; rr++) for (var a = 0; a < 8; a++) tries.push([Math.cos(a * Math.PI / 4) * rr * 55, Math.sin(a * Math.PI / 4) * rr * 55]);
  for (var i = 0; i < tries.length; i++) {
    it.x = Math.round(D.w / 2 + tries[i][0]); it.y = Math.round(D.h / 2 + tries[i][1]);
    var b = S.itemBox(it);
    if (b.x1 < 4 || b.y1 < 4 || b.x2 > D.w - 4 || b.y2 > D.h - 4) continue;
    if (!st.items.some(function (o) { return overlaps(b, S.itemBox(o)); })) return;
  }
  it.x = D.w / 2; it.y = D.h / 2; clampGroup([it]);
  toast('There is no open space, so it was placed in the middle. Drag it where it goes.', 4000);
}
function dispBox(it) {
  var b = S.itemBox(it), D = dims();
  return cur().view === 'bottom' ? {x1:D.w - b.x2, x2:D.w - b.x1, y1:D.h - b.y2, y2:D.h - b.y1} : b;
}
function moveDisp(it, dx, dy) { var f = cur().view === 'bottom' ? -1 : 1; it.x = Math.round(it.x + f * dx); it.y = Math.round(it.y + f * dy); }

/* ================= pointer: arranging ================= */
svg.addEventListener('pointerdown', function (e) {
  if (e.button && e.button !== 0) return;
  closeMenus();
  if (mode() === 'arrange') arrangeDown(e); else seatDown(e);
});
function arrangeDown(e) {
  var h = e.target.closest('[data-handle]'), g = e.target.closest('[data-item]'), p = svgPt(e);
  var additive = e.shiftKey || e.ctrlKey || e.metaKey;
  if (h && ui.sel.length === 1) {
    ui.drag = {kind:'rotate', id:ui.sel[0], snap:snapshot(), moved:false};
  } else if (g) {
    var id = g.getAttribute('data-item');
    if (additive && ui.sel.indexOf(id) >= 0) { ui.sel = ui.sel.filter(function (x) { return x !== id; }); ui.alignOpen = false; ui.drag = null; render(); return; }
    if (additive) ui.sel.push(id);
    else if (ui.sel.indexOf(id) < 0) { ui.sel = [id]; ui.alignOpen = false; }
    var orig = {};
    ui.sel.forEach(function (i) { var it = findItem(i); orig[i] = {x:it.x, y:it.y}; });
    ui.drag = {kind:'move', id:id, start:p, orig:orig, snap:snapshot(), moved:false, sx:e.clientX, sy:e.clientY, additive:additive};
  } else {
    if (!additive) { ui.sel = []; ui.alignOpen = false; }
    ui.drag = {kind:'marquee', start:p, base:ui.sel.slice(), sx:e.clientX, sy:e.clientY, moved:false};
  }
  try { svg.setPointerCapture(e.pointerId); } catch (err) {}
  render();
  e.preventDefault();
}
svg.addEventListener('pointermove', function (e) {
  var d = ui.drag; if (!d || mode() !== 'arrange') return;
  var p = svgPt(e), st = cur();
  if (d.kind === 'move') {
    if (!d.moved && Math.hypot(e.clientX - d.sx, e.clientY - d.sy) < 4) return;
    var o0 = d.orig[d.id], dx = p.x - d.start.x, dy = p.y - d.start.y;
    if (st.snap && !e.altKey) { dx = Math.round((o0.x + dx) / 8) * 8 - o0.x; dy = Math.round((o0.y + dy) / 8) * 8 - o0.y; }
    var items = selItems();
    items.forEach(function (it) { it.x = d.orig[it.id].x; it.y = d.orig[it.id].y; });
    var b = unionBox(items), D = dims();
    if (b.x2 - b.x1 <= D.w) dx = Math.max(-b.x1, Math.min(D.w - b.x2, dx));
    if (b.y2 - b.y1 <= D.h) dy = Math.max(-b.y1, Math.min(D.h - b.y2, dy));
    items.forEach(function (it) { it.x = d.orig[it.id].x + dx; it.y = d.orig[it.id].y + dy; });
  } else if (d.kind === 'rotate') {
    var it = findItem(d.id); if (!it) return;
    var ang = Math.atan2(p.y - it.y, p.x - it.x) * 180 / Math.PI + 90;
    it.rot = S.signedDeg(e.shiftKey ? Math.round(ang) : Math.round(ang / 15) * 15);
    clampGroup([it]);
  } else if (d.kind === 'marquee') {
    if (!d.moved && Math.hypot(e.clientX - d.sx, e.clientY - d.sy) < 4) return;
    var a = S.view(st, d.start), c = S.view(st, p);
    ui.marquee = {x1:Math.min(a.x, c.x), y1:Math.min(a.y, c.y), x2:Math.max(a.x, c.x), y2:Math.max(a.y, c.y)};
    var rr = {x1:Math.min(d.start.x, p.x), y1:Math.min(d.start.y, p.y), x2:Math.max(d.start.x, p.x), y2:Math.max(d.start.y, p.y)};
    var hit = st.items.filter(function (it2) { return it2.x >= rr.x1 && it2.x <= rr.x2 && it2.y >= rr.y1 && it2.y <= rr.y2; }).map(function (it2) { return it2.id; });
    ui.sel = d.base.concat(hit.filter(function (id) { return d.base.indexOf(id) < 0; }));
  }
  d.moved = true;
  $('selbar').hidden = true;
  renderSoon();
});
function endArrange() {
  var d = ui.drag; ui.drag = null; ui.marquee = null;
  if (!d) return;
  if ((d.kind === 'move' || d.kind === 'rotate') && d.moved) pushHist(d.snap);
  if (d.kind === 'move' && !d.moved && !d.additive && ui.sel.length > 1) ui.sel = [d.id];
  save(); render();
}
svg.addEventListener('pointerup', function () { if (mode() === 'arrange' && ui.drag) endArrange(); });
svg.addEventListener('pointercancel', function () { if (mode() === 'arrange' && ui.drag) endArrange(); });
svg.addEventListener('dblclick', function (e) {
  if (mode() !== 'arrange') return;
  var g = e.target.closest('[data-item]'); if (!g) return;
  var it = findItem(g.getAttribute('data-item'));
  if (it && it.type === 'label' && it.kind !== 'door') editText(it);
});

/* ================= selection actions ================= */
function editText(it) {
  ask({title:'Label text', input:true, value:it.text != null ? it.text : S.LABELS[it.kind].text, ok:'Save'}).then(function (t) {
    if (t === null) return;
    change(function () { findItem(it.id).text = t; });
  });
}
function turnGroup(deg) {
  var items = selItems(); if (!items.length) return;
  change(function () {
    var b = unionBox(items), cx = (b.x1 + b.x2) / 2, cy = (b.y1 + b.y2) / 2;
    items.forEach(function (it) {
      if (items.length > 1) { var q = S.rotPt(it.x - cx, it.y - cy, deg); it.x = Math.round(cx + q.x); it.y = Math.round(cy + q.y); }
      it.rot = S.signedDeg((it.rot || 0) + deg);
    });
    clampGroup(items);
  });
}
function alignSel(kind) {
  var items = selItems(); if (items.length < 2) return;
  change(function () {
    var boxes = items.map(dispBox);
    if (kind === 'spaceX' || kind === 'spaceY') {
      if (items.length < 3) { toast('Select three or more to space them evenly.'); return; }
      var ax = kind === 'spaceX', ord = items.map(function (it, i) { return {it:it, b:boxes[i], c:ax ? (boxes[i].x1 + boxes[i].x2) / 2 : (boxes[i].y1 + boxes[i].y2) / 2}; });
      ord.sort(function (a, b) { return a.c - b.c; });
      var c0 = ord[0].c, c1 = ord[ord.length - 1].c, step = (c1 - c0) / (ord.length - 1);
      ord.forEach(function (o, i) { var dd = c0 + step * i - o.c; moveDisp(o.it, ax ? dd : 0, ax ? 0 : dd); });
      return;
    }
    var t;
    if (kind === 'left') t = Math.min.apply(null, boxes.map(function (b) { return b.x1; }));
    if (kind === 'right') t = Math.max.apply(null, boxes.map(function (b) { return b.x2; }));
    if (kind === 'top') t = Math.min.apply(null, boxes.map(function (b) { return b.y1; }));
    if (kind === 'bottom') t = Math.max.apply(null, boxes.map(function (b) { return b.y2; }));
    if (kind === 'cx') t = boxes.reduce(function (s, b) { return s + (b.x1 + b.x2) / 2; }, 0) / boxes.length;
    if (kind === 'cy') t = boxes.reduce(function (s, b) { return s + (b.y1 + b.y2) / 2; }, 0) / boxes.length;
    items.forEach(function (it, i) {
      var b = boxes[i];
      if (kind === 'left') moveDisp(it, t - b.x1, 0);
      if (kind === 'right') moveDisp(it, t - b.x2, 0);
      if (kind === 'top') moveDisp(it, 0, t - b.y1);
      if (kind === 'bottom') moveDisp(it, 0, t - b.y2);
      if (kind === 'cx') moveDisp(it, t - (b.x1 + b.x2) / 2, 0);
      if (kind === 'cy') moveDisp(it, 0, t - (b.y1 + b.y2) / 2);
    });
    clampGroup(items);
  });
}
function duplicateSel() {
  var items = selItems(); if (!items.length) return;
  var st = cur(), D = dims(), b = unionBox(items), gw = b.x2 - b.x1, gh = b.y2 - b.y1;
  var offs = [[gw + 16, 0], [0, gh + 16], [-(gw + 16), 0], [0, -(gh + 16)], [32, 32]], use = offs[offs.length - 1];
  for (var i = 0; i < offs.length - 1; i++) {
    var o = offs[i], nb = {x1:b.x1 + o[0], y1:b.y1 + o[1], x2:b.x2 + o[0], y2:b.y2 + o[1]};
    if (nb.x1 < 2 || nb.y1 < 2 || nb.x2 > D.w - 2 || nb.y2 > D.h - 2) continue;
    var hits = st.items.some(function (x) { return items.indexOf(x) < 0 && overlaps(S.itemBox(x), nb); });
    if (!hits) { use = o; break; }
  }
  var copies = items.map(function (it) { var c = JSON.parse(JSON.stringify(it)); c.id = S.uid(); c.x += use[0]; c.y += use[1]; return c; });
  change(function (st2) { copies.forEach(function (c) { st2.items.push(c); }); clampGroup(copies.map(function (c) { return findItem(c.id); })); });
  ui.sel = copies.map(function (c) { return c.id; }); render();
}
function removeSel() {
  var ids = ui.sel.slice(); if (!ids.length) return;
  change(function (st) { st.items = st.items.filter(function (i) { return ids.indexOf(i.id) < 0; }); S.cleanSeats(st); });
  ui.sel = []; render();
}
$('selbar').addEventListener('click', function (e) {
  var al = e.target.closest('[data-al]'); if (al) { alignSel(al.getAttribute('data-al')); return; }
  var b = e.target.closest('[data-sb]'); if (!b) return;
  var a = b.getAttribute('data-sb'), items = selItems(); if (!items.length) return;
  if (a === 'align') { ui.alignOpen = !ui.alignOpen; renderSelbar(); return; }
  if (a === 'dup') { duplicateSel(); return; }
  if (a === 'del') { removeSel(); return; }
  if (a === 'turn') { turnGroup(90); return; }
  var it = items[0];
  if (a === 'text') { editText(it); return; }
  change(function (st) {
    var t = findItem(it.id);
    if (a === 'rotl') t.rot = S.signedDeg((t.rot || 0) - 15);
    if (a === 'rotr') t.rot = S.signedDeg((t.rot || 0) + 15);
    if (a === 'seatsUp' || a === 'seatsDown') {
      var dn = a === 'seatsUp' ? 1 : -1, n = (t.n || (t.type === 'round' ? 6 : 1)) + dn;
      var lo = t.type === 'round' ? 3 : (t.rows === 2 ? 2 : 1), hi = t.type === 'round' ? 10 : (t.rows === 2 ? 12 : 10);
      if (n < lo || n > hi) { toast(n < lo ? 'That is the fewest seats for this one.' : 'That is the most seats for this one.'); return; }
      t.n = n; S.cleanSeats(st);
    }
    if (a === 'rows') { t.rows = t.rows === 2 ? 1 : 2; S.cleanSeats(st); }
    if (a === 'wide' || a === 'narrow') {
      var s = a === 'wide' ? 1 : -1;
      if (t.type === 'desk') t.sw = Math.max(56, Math.min(140, (t.sw || 76) + 8 * s));
      else if (t.type === 'teacher') t.w = Math.max(80, Math.min(280, (t.w || 150) + 10 * s));
      else if (t.kind === 'door') t.w = Math.max(50, Math.min(140, t.w + 10 * s));
      else t.w = Math.max(60, Math.min(dims().w, t.w + 40 * s));
    }
    clampGroup([t]);
  });
});

/* ================= keyboard ================= */
document.addEventListener('keydown', function (e) {
  if (dlg.open) return;
  var tag = (e.target.tagName || '').toLowerCase(), typing = tag === 'input' || tag === 'textarea' || tag === 'select';
  var mod = e.ctrlKey || e.metaKey, k = e.key.toLowerCase();
  if (e.key === 'Escape') {
    if (ui.proj) { closeProj(); return; }
    closeMenus(); ui.sel = []; ui.picked = null; ui.alignOpen = false; render(); return;
  }
  if (typing) return;
  if (mod && k === 'z') { e.preventDefault(); if (e.shiftKey) redo(); else undo(); return; }
  if (mod && k === 'y') { e.preventDefault(); redo(); return; }
  if (ui.proj) { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); pickStudent(); } return; }
  if (mode() !== 'arrange') return;
  if (mod && k === 'a') { e.preventDefault(); ui.sel = cur().items.map(function (i) { return i.id; }); render(); return; }
  if (!ui.sel.length) return;
  if (mod && k === 'd') { e.preventDefault(); duplicateSel(); return; }
  if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); removeSel(); return; }
  var step = e.shiftKey ? 1 : 8, dx = 0, dy = 0;
  if (e.key === 'ArrowLeft') dx = -step; if (e.key === 'ArrowRight') dx = step;
  if (e.key === 'ArrowUp') dy = -step; if (e.key === 'ArrowDown') dy = step;
  if (dx || dy) { e.preventDefault(); change(function () { var items = selItems(); items.forEach(function (it) { moveDisp(it, dx, dy); }); clampGroup(items); }); return; }
  if (k === 'r' && !mod) { e.preventDefault(); if (ui.sel.length === 1) change(function () { var t = selItems()[0]; t.rot = S.signedDeg((t.rot || 0) + (e.shiftKey ? -15 : 15)); clampGroup([t]); }); else turnGroup(e.shiftKey ? -90 : 90); }
});

/* ================= seating by hand ================= */
var ghost = $('ghost');
function seatDown(e) {
  var s = e.target.closest('[data-seat]');
  if (!s) { if (ui.picked) { ui.picked = null; render(); } return; }
  var key = s.getAttribute('data-seat');
  startNameDrag(e, cur().seats[key] || null, key);
}
function startNameDrag(e, sid, fromKey) { ui.drag = {kind:'name', sid:sid, from:fromKey, sx:e.clientX, sy:e.clientY, moved:false, pid:e.pointerId}; if (fromKey) e.preventDefault(); }
window.addEventListener('pointermove', function (e) {
  var d = ui.drag; if (!d || d.kind !== 'name' || e.pointerId !== d.pid) return;
  if (!d.moved) {
    if (!d.sid || Math.hypot(e.clientX - d.sx, e.clientY - d.sy) < 6) return;
    d.moved = true; ui.picked = null;
    var stu = S.student(cur(), d.sid);
    ghost.textContent = stu ? stu.name : ''; ghost.style.display = 'block';
  }
  e.preventDefault();
  ghost.style.left = e.clientX + 'px'; ghost.style.top = e.clientY + 'px';
  var el = document.elementFromPoint(e.clientX, e.clientY);
  var seat = el && el.closest ? el.closest('[data-seat]') : null, key = seat ? seat.getAttribute('data-seat') : null;
  var overList = !!(el && el.closest && el.closest('.chips'));
  document.querySelectorAll('.chips').forEach(function (c) { c.classList.toggle('dropzone', overList && !!S.seatOf(cur(), d.sid)); });
  if (key !== ui.hover) { ui.hover = key; renderSoon(); }
});
window.addEventListener('pointerup', function (e) {
  var d = ui.drag; if (!d || d.kind !== 'name' || e.pointerId !== d.pid) return;
  ui.drag = null; ghost.style.display = 'none';
  document.querySelectorAll('.chips').forEach(function (c) { c.classList.remove('dropzone'); });
  var hover = ui.hover; ui.hover = null;
  if (d.moved) {
    var el = document.elementFromPoint(e.clientX, e.clientY);
    if (hover) seatStudent(d.sid, hover);
    else if (el && el.closest && el.closest('.side') && S.seatOf(cur(), d.sid)) change(function (st) { var k = S.seatOf(st, d.sid); if (k) delete st.seats[k]; });
    else render();
    return;
  }
  if (d.from) seatTap(d.from); else chipTap(d.sid);
});
window.addEventListener('pointercancel', function () { if (ui.drag && ui.drag.kind === 'name') { ui.drag = null; ui.hover = null; ghost.style.display = 'none'; render(); } });
function seatTap(key) {
  var sid = cur().seats[key];
  if (ui.picked) {
    if (ui.picked.from === key) { ui.picked = null; render(); return; }
    var ps = ui.picked.sid; ui.picked = null; seatStudent(ps, key); return;
  }
  if (sid) { ui.picked = {sid:sid, from:key}; render(); }
  else $('hint').textContent = 'Click a name first, then this seat. Or drag a name here.';
}
function chipTap(sid) {
  ui.picked = (ui.picked && ui.picked.sid === sid) ? null : {sid:sid, from:S.seatOf(cur(), sid)};
  render();
}
function seatStudent(sid, toKey) {
  if (cur().seats[toKey] === sid) { render(); return; }
  change(function (st) {
    var fromKey = S.seatOf(st, sid), other = st.seats[toKey];
    if (fromKey) delete st.seats[fromKey];
    if (other && fromKey) st.seats[fromKey] = other;
    st.seats[toKey] = sid;
  });
}
['unseated', 'seated'].forEach(function (id) {
  var box = $(id);
  box.addEventListener('pointerdown', function (e) {
    var c = e.target.closest('.chip'); if (!c || (e.button && e.button !== 0)) return;
    startNameDrag(e, c.getAttribute('data-sid'), null);
  });
  box.addEventListener('keydown', function (e) {
    var c = e.target.closest('.chip'); if (!c) return;
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); chipTap(c.getAttribute('data-sid')); }
  });
});
/* keyboard on seats: Enter places or picks up, Delete unseats, arrow keys move between seats */
svg.addEventListener('keydown', function (e) {
  var s = e.target.closest && e.target.closest('[data-seat]'); if (!s) return;
  var key = s.getAttribute('data-seat');
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); seatTap(key); return; }
  if (e.key === 'Delete' || e.key === 'Backspace') {
    e.preventDefault(); e.stopPropagation();
    if (cur().seats[key]) change(function (st) { delete st.seats[key]; });
    return;
  }
  var dir = {ArrowLeft:[-1, 0], ArrowRight:[1, 0], ArrowUp:[0, -1], ArrowDown:[0, 1]}[e.key]; if (!dir) return;
  e.preventDefault(); e.stopPropagation();
  var r0 = s.getBoundingClientRect(), cx = r0.left + r0.width / 2, cy = r0.top + r0.height / 2, best = null, bd = Infinity;
  svg.querySelectorAll('[data-seat]').forEach(function (el) {
    if (el === s) return;
    var r = el.getBoundingClientRect(), dx = r.left + r.width / 2 - cx, dy = r.top + r.height / 2 - cy;
    var along = dx * dir[0] + dy * dir[1]; if (along <= 4) return;
    var off = Math.abs(dx * dir[1]) + Math.abs(dy * dir[0]), score = along + off * 2.5;
    if (score < bd) { bd = score; best = el; }
  });
  if (best) best.focus();
});

/* ================= step 1: room ================= */
function buildPresetButtons(target) {
  var D = {w:1024, h:768};
  target.innerHTML = S.PRESETS.map(function (p) {
    return '<button class="preset" data-preset="' + p[0] + '">' + S.miniSvg(S.presetItems(p[0], D), D) + '<span>' + p[1] + '</span><small>' + p[2] + '</small></button>';
  }).join('');
  target.addEventListener('click', function (e) { var b = e.target.closest('[data-preset]'); if (b) applyPreset(b.getAttribute('data-preset')); });
}
function applyPreset(key) {
  var st = cur(), name = S.PRESETS.filter(function (p) { return p[0] === key; })[0][1];
  var hasDesks = st.items.some(function (it) { return it.type !== 'label'; });
  var go = hasDesks ? ask({title:'Use the ' + name + ' layout?', text:'This replaces the desks and labels in the room. Seated students move to the new desks in the same order.', ok:'Replace the room'}) : Promise.resolve(true);
  go.then(function (yes) {
    if (!yes) return;
    change(function (st2) {
      var order = S.seatList(st2).map(function (s) { return st2.seats[s.key]; }).filter(Boolean);
      st2.items = S.presetItems(key, S.dims(st2));
      st2.seats = {};
      var seats = S.seatList(st2);
      order.forEach(function (sid, i) { if (seats[i]) st2.seats[seats[i].key] = sid; });
    });
    ui.sel = []; render();
    var left = cur().students.length - Object.keys(cur().seats).length;
    toast(left > 0 && hasDesks ? plural(left, 'student') + ' need a seat now. See step 3.' : 'Layout ready. Drag anything to adjust it.');
  });
}
function buildAddButtons() {
  $('addDesks').innerHTML = S.ADD_DESKS.map(function (d, i) { return '<button class="add" data-desk="' + i + '">' + S.iconSvg(d[1]) + esc(d[0]) + '</button>'; }).join('');
  $('addLabels').innerHTML = S.ADD_LABELS.map(function (d, i) { return '<button class="add" data-label="' + i + '">' + S.iconSvg({type:'label', kind:d[1]}) + esc(d[0]) + '</button>'; }).join('');
  $('addDesks').onclick = function (e) {
    var b = e.target.closest('[data-desk]'); if (!b) return;
    var it = S.newItem(S.ADD_DESKS[+b.getAttribute('data-desk')][1], 0, 0, 0); placeFree(it);
    change(function (st) { st.items.push(it); }); ui.sel = [it.id]; render();
  };
  $('addLabels').onclick = function (e) {
    var b = e.target.closest('[data-label]'); if (!b) return;
    var d = S.ADD_LABELS[+b.getAttribute('data-label')], it = S.newItem({type:'label', kind:d[1], text:d[0]}, 0, 0, 0); placeFree(it);
    change(function (st) { st.items.push(it); }); ui.sel = [it.id]; render();
  };
}
function roomSize() {
  var w = Math.max(12, Math.min(90, Math.round(+$('roomWIn').value || 0))), h = Math.max(12, Math.min(90, Math.round(+$('roomHIn').value || 0)));
  if (!+$('roomWIn').value || !+$('roomHIn').value) { render(); return; }
  change(function (st) { st.roomW = w * S.FT; st.roomH = h * S.FT; st.items.forEach(function (it) { clampGroup([it]); }); });
}
$('roomWIn').onchange = roomSize; $('roomHIn').onchange = roomSize;
$('snapChk').onchange = function () { var v = this.checked; setPref(function (st) { st.snap = v; }); };
$('numChk').onchange = function () { var v = this.checked; setPref(function (st) { st.deskNums = v; }); };
$('clearRoomBtn').onclick = function () {
  if (!cur().items.length) return;
  ask({title:'Clear the room?', text:'All desks and labels are removed. Students stay in the class list. You can undo this.', ok:'Clear the room', danger:true}).then(function (y) {
    if (y) { change(function (st) { st.items = []; st.seats = {}; }); ui.sel = []; render(); }
  });
};

/* ================= step 2: class ================= */
function addStudents(names) {
  var st = cur(), have = {}, added = 0, dup = 0;
  st.students.forEach(function (s) { have[s.name.toLowerCase()] = 1; });
  var fresh = [];
  names.forEach(function (n) { var k = n.toLowerCase(); if (have[k]) { dup++; return; } have[k] = 1; fresh.push(n); });
  if (fresh.length) change(function (st2) { fresh.forEach(function (n) { st2.students.push({id:S.uid(), name:n, needs:[], tags:[], note:'', pin:false}); added++; }); });
  return {added:fresh.length, dup:dup};
}
$('addNamesBtn').onclick = function () {
  var names = S.parseNames($('namesIn').value);
  if (!names.length) { $('namesIn').focus(); toast('Type or paste at least one name.'); return; }
  var r = addStudents(names);
  $('namesIn').value = '';
  toast((r.added ? plural(r.added, 'student') + ' added.' : 'No new names.') + (r.dup ? ' ' + plural(r.dup, 'name was', 'names were') + ' already on the list.' : ''));
};
$('importBtn').onclick = function () { $('rosterIn').click(); };
$('rosterIn').onchange = function () {
  var f = this.files[0]; this.value = ''; if (!f) return;
  if (/\.xlsx?$/i.test(f.name)) { toast('Excel files cannot be read here. In Excel, use Save As and choose CSV, then import that file.', 5000); return; }
  var rd = new FileReader();
  rd.onload = function () {
    var names = S.parseRoster(rd.result);
    if (!names.length) { toast('No names were found in that file. Try copying the names and pasting them into the box.', 5000); return; }
    var box = $('namesIn'); box.value = (box.value.trim() ? box.value.trim() + '\n' : '') + names.join('\n');
    box.focus(); box.scrollTop = 0;
    toast('Found ' + plural(names.length, 'name') + '. Check them, then select Add names.', 4500);
  };
  rd.readAsText(f);
};
$('copyFromSel').onchange = function () {
  var src = data.charts.filter(function (c) { return c.id === this.value; }, this)[0]; this.value = '';
  if (!src) return;
  ask({title:'Copy the class list from ' + src.name + '?', text:'Adds ' + plural(src.students.length, 'student') + ' with their seat needs, tags, rules and notes. Names already on this list are skipped.', ok:'Copy students'}).then(function (y) {
    if (!y) return;
    var copied = 0;
    change(function (st) {
      var have = {}, map = {}, tagMap = {};
      st.students.forEach(function (s) { have[s.name.toLowerCase()] = s.id; });
      src.tags.forEach(function (t) {
        var ex = st.tags.filter(function (x) { return x.name.toLowerCase() === t.name.toLowerCase(); })[0];
        if (!ex) { ex = {id:S.uid(), name:t.name, color:nextTagColor(st)}; st.tags.push(ex); }
        tagMap[t.id] = ex.id;
      });
      src.students.forEach(function (s) {
        var k = s.name.toLowerCase();
        if (have[k]) { map[s.id] = have[k]; return; }
        var ns = {id:S.uid(), name:s.name, needs:s.needs.slice(), note:s.note || '', pin:false, tags:s.tags.map(function (t) { return tagMap[t]; }).filter(Boolean)};
        st.students.push(ns); map[s.id] = ns.id; have[k] = ns.id; copied++;
      });
      src.rules.forEach(function (r) {
        var a = map[r.a], b = map[r.b]; if (!a || !b) return;
        if (!st.rules.some(function (x) { return (x.a === a && x.b === b) || (x.a === b && x.b === a); })) st.rules.push({id:S.uid(), a:a, b:b, type:r.type});
      });
    });
    toast(copied ? plural(copied, 'student') + ' copied.' : 'Everyone from that chart is already here.');
  });
};
$('clearNamesBtn').onclick = function () {
  if (!cur().students.length) return;
  ask({title:'Remove every student?', text:'Also removes their seats, rules and notes from this chart. You can undo this.', ok:'Remove all', danger:true}).then(function (y) {
    if (y) change(function (st) { st.students = []; st.seats = {}; st.rules = []; });
  });
};
$('studentList').addEventListener('click', function (e) { var b = e.target.closest('[data-edit]'); if (b) openStudent(b.getAttribute('data-edit')); });
function setRule(st, a, b, type) {
  st.rules = st.rules.filter(function (r) { return !((r.a === a && r.b === b) || (r.a === b && r.b === a)); });
  if (type) st.rules.push({id:S.uid(), a:a, b:b, type:type});
}
$('addRuleBtn').onclick = function () {
  var a = $('ruleA').value, b = $('ruleB').value, type = $('ruleType').value;
  if (!a || !b) { toast('Choose two students.'); return; }
  if (a === b) { toast('Choose two different students.'); return; }
  change(function (st) { setRule(st, a, b, type); });
  $('ruleB').value = '';
  toast('Rule added. Reseat in step 3 to apply it.');
};
$('ruleList').addEventListener('click', function (e) {
  var x = e.target.closest('[data-rule]'); if (!x) return;
  var id = x.getAttribute('data-rule');
  change(function (st) { st.rules = st.rules.filter(function (r) { return r.id !== id; }); });
});
function nextTagColor(st) {
  var used = st.tags.map(function (t) { return t.color; });
  return S.TAG_COLORS.filter(function (c) { return used.indexOf(c) < 0; })[0] || S.TAG_COLORS[st.tags.length % S.TAG_COLORS.length];
}
function addTag() {
  var name = $('tagIn').value.trim(); if (!name) { $('tagIn').focus(); return; }
  if (cur().tags.some(function (t) { return t.name.toLowerCase() === name.toLowerCase(); })) { toast('That tag already exists.'); return; }
  change(function (st) { st.tags.push({id:S.uid(), name:name, color:nextTagColor(st)}); });
  $('tagIn').value = '';
  toast('Tag added. Select a student above to give them this tag.');
}
$('addTagBtn').onclick = addTag;
$('tagIn').addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); addTag(); } });
$('tagList').addEventListener('click', function (e) {
  var x = e.target.closest('[data-tag]'); if (!x) return;
  var id = x.getAttribute('data-tag'), t = cur().tags.filter(function (q) { return q.id === id; })[0];
  ask({title:'Delete the tag ' + t.name + '?', text:'It is removed from every student. You can undo this.', ok:'Delete tag', danger:true}).then(function (y) {
    if (y) change(function (st) { st.tags = st.tags.filter(function (q) { return q.id !== id; }); st.students.forEach(function (s) { s.tags = s.tags.filter(function (q) { return q !== id; }); }); });
  });
});

/* student details dialog */
function openStudent(sid) {
  var st = cur(), s = S.student(st, sid); if (!s) return;
  var others = st.students.filter(function (o) { return o.id !== sid; }).sort(byLast);
  var rel = {apart:[], together:[]};
  st.rules.forEach(function (r) { if (r.a === sid) rel[r.type].push(r.b); else if (r.b === sid) rel[r.type].push(r.a); });
  var fs = {name:s.name, note:s.note, pin:s.pin, needs:s.needs.slice(), tags:s.tags.slice()};
  var k = S.seatOf(st, sid), info = seatInfoMap(st), sc = S.needScores(st, S.seatList(st));
  var what = {door:'a door', teacher:"a teacher's desk", nowindow:'windows'};
  function relHtml(type) {
    return '<div class="picklist">' + rel[type].map(function (id) { var o = S.student(st, id); return '<span class="tag">' + esc(o.name) + '<button type="button" class="x" data-unrel="' + type + ':' + id + '" aria-label="Remove ' + esc(o.name) + '">×</button></span>'; }).join('') + '</div>' +
      '<select class="inline" style="width:100%" data-addrel="' + type + '" aria-label="' + (type === 'apart' ? 'Keep apart from' : 'Works well with') + '"><option value="">Add a student</option>' +
      others.filter(function (o) { return rel.apart.indexOf(o.id) < 0 && rel.together.indexOf(o.id) < 0; }).map(function (o) { return '<option value="' + o.id + '">' + esc(o.name) + '</option>'; }).join('') + '</select>';
  }
  function body() {
    var needs = S.NEEDS.map(function (n) {
      return '<label class="check"><input type="checkbox" data-need="' + n[0] + '"' + (fs.needs.indexOf(n[0]) >= 0 ? ' checked' : '') + '> ' + n[1] +
        (!sc[n[0]] ? ' <span class="dim">(add ' + what[n[0]] + ' to the room)</span>' : '') + '</label>';
    }).join('');
    var tags = st.tags.length ? st.tags.map(function (t) { return '<label class="check"><input type="checkbox" data-tagc="' + t.id + '"' + (fs.tags.indexOf(t.id) >= 0 ? ' checked' : '') + '> <span class="dot" style="background:' + t.color + '"></span> ' + esc(t.name) + '</label>'; }).join('')
      : '<p class="note">No tags yet. Add tags in step 2 under Tags.</p>';
    return '<label class="field"><span>Name</span><input type="text" id="sdName" value="' + esc(fs.name) + '"></label>' +
      '<p class="note">' + (k ? 'Seated at ' + esc(S.seatLabel(info[k])) + '.' : 'Not seated yet.') + '</p>' +
      '<label class="check"><input type="checkbox" id="sdPin"' + (fs.pin ? ' checked' : '') + '> Keep in this seat when reseating</label>' +
      '<h3>Seat needs</h3>' + needs +
      '<div class="cols2"><div><h3>Keep apart from</h3>' + relHtml('apart') + '</div><div><h3>Works well with</h3>' + relHtml('together') + '</div></div>' +
      '<h3>Tags</h3>' + tags +
      '<h3>Note for a substitute</h3><textarea id="sdNote" placeholder="Helps hand out papers. Allergic to peanuts.">' + esc(fs.note) + '</textarea>';
  }
  function readForm() {
    var f = $('sdBody'); if (!f) return;
    fs.name = $('sdName').value; fs.note = $('sdNote').value; fs.pin = $('sdPin').checked;
    fs.needs = [].slice.call(f.querySelectorAll('[data-need]:checked')).map(function (x) { return x.getAttribute('data-need'); });
    fs.tags = [].slice.call(f.querySelectorAll('[data-tagc]:checked')).map(function (x) { return x.getAttribute('data-tagc'); });
  }
  function redraw() { readForm(); var b = $('sdBody'), sc0 = b.scrollTop; b.innerHTML = body(); b.scrollTop = sc0; }
  var html = '<form method="dialog"><h2>' + esc(s.name) + '</h2><div class="body" id="sdBody">' + body() + '</div>' +
    '<div class="dlgbtns"><button value="ok" class="btn primary">Save</button><button value="cancel" class="btn quiet" formnovalidate>Cancel</button>' +
    '<button type="button" class="btn quiet danger left" id="sdRemove">Remove student</button></div></form>';
  ui.removeArm = false;
  var done = openDialog(html);
  dlg.onchange = function (e) {
    var sel = e.target.closest('[data-addrel]'); if (!sel || !sel.value) return;
    var type = sel.getAttribute('data-addrel'); rel[type].push(sel.value); redraw();
    var again = dlg.querySelector('[data-addrel="' + type + '"]'); if (again) again.focus();
  };
  dlg.onclick = function (e) {
    var x = e.target.closest('[data-unrel]');
    if (x) { var p = x.getAttribute('data-unrel').split(':'); rel[p[0]] = rel[p[0]].filter(function (id) { return id !== p[1]; }); redraw(); return; }
    if (e.target.id === 'sdRemove') {
      if (!ui.removeArm) { ui.removeArm = true; e.target.textContent = 'Select again to remove'; return; }
      ui.removeArm = false; dlg.close('remove');
    }
  };
  done.then(function (v) {
    if (v === 'ok') readForm();
    dlg.onchange = null; dlg.onclick = null;
    if (v === 'remove') {
      change(function (st2) { st2.students = st2.students.filter(function (q) { return q.id !== sid; }); S.cleanSeats(st2); });
      toast(s.name + ' was removed. Undo brings them back.');
      return;
    }
    if (v !== 'ok') return;
    change(function (st2) {
      var t = S.student(st2, sid); if (!t) return;
      t.name = fs.name.trim() || t.name; t.note = fs.note.trim(); t.pin = fs.pin; t.needs = fs.needs; t.tags = fs.tags;
      st2.rules = st2.rules.filter(function (r) { return r.a !== sid && r.b !== sid; });
      rel.apart.forEach(function (id) { st2.rules.push({id:S.uid(), a:sid, b:id, type:'apart'}); });
      rel.together.forEach(function (id) { st2.rules.push({id:S.uid(), a:sid, b:id, type:'together'}); });
    });
  });
}

/* ================= step 3: seats ================= */
function haveDesksAndNames() {
  var st = cur();
  if (!st.students.length) { toast('Add your class in step 2 first.'); return false; }
  if (!S.seatList(st).length) { toast('Add desks in step 1 first.'); return false; }
  return true;
}
function saveHistory(st, quiet) {
  if (Object.keys(st.seats).length < 2) { if (!quiet) toast('Seat at least two students first.'); return false; }
  var last = st.history[st.history.length - 1];
  if (last && JSON.stringify(last.seats) === JSON.stringify(st.seats)) { if (!quiet) toast('These seats are already saved.'); return false; }
  st.history.push({id:S.uid(), date:new Date().toISOString(), seats:JSON.parse(JSON.stringify(st.seats)), pairs:S.neighborPairs(st)});
  while (st.history.length > 12) st.history.shift();
  return true;
}
function autoSeat(modeName) {
  if (!haveDesksAndNames()) return;
  var st = cur(), a = st.auto;
  if (modeName === 'empty' && st.students.every(function (s) { return S.seatOf(st, s.id); })) { toast('Everyone already has a seat.'); return; }
  change(function (st2) {
    if (modeName === 'all') saveHistory(st2, true);
    st2.seats = S.solve(st2, {mode:modeName, spread:a.spread, rules:a.rules, needs:a.needs, fresh:a.fresh, balance:a.balance}).seats;
  });
  var r = S.check(cur()), left = cur().students.length - Object.keys(cur().seats).length, msg;
  if (left > 0) msg = 'Seated. ' + plural(left, 'student') + ' still need a seat; add more desks in step 1.';
  else if (!r.problems.length) msg = 'Everyone is seated' + (r.rules + r.needs ? ' and every rule and seat need is met.' : '.');
  else msg = 'Seated. ' + plural(r.problems.length, 'rule or need', 'rules or needs') + ' could not be met. See Rules check.';
  toast(msg, 4500);
}
$('reseatBtn').onclick = function () { autoSeat('all'); };
$('fillBtn').onclick = function () { autoSeat('empty'); };
$('spreadSel').onchange = function () { var v = this.value; setPref(function (st) { st.auto.spread = v; }); };
[['optRules', 'rules'], ['optNeeds', 'needs'], ['optFresh', 'fresh'], ['optBalance', 'balance']].forEach(function (p) {
  $(p[0]).onchange = function () { var v = this.checked; setPref(function (st) { st.auto[p[1]] = v; }); };
});
$('alphaBtn').onclick = function () {
  if (!haveDesksAndNames()) return;
  change(function (st) {
    var keep = {}, used = {};
    st.students.forEach(function (s) { var k = S.seatOf(st, s.id); if (s.pin && k) { keep[k] = s.id; used[s.id] = 1; } });
    st.seats = keep;
    var free = S.seatList(st).filter(function (s) { return !keep[s.key]; });
    st.students.filter(function (s) { return !used[s.id]; }).sort(byLast).forEach(function (s, i) { if (free[i]) st.seats[free[i].key] = s.id; });
  });
};
$('clearSeatsBtn').onclick = function () {
  if (!Object.keys(cur().seats).length) return;
  change(function (st) { saveHistory(st, true); st.seats = {}; });
  toast('Seats cleared. The old seats were saved under Past seatings.');
};
$('nameStyleSel').onchange = function () { var v = this.value; setPref(function (st) { st.nameStyle = v; }); };
$('tagDotsChk').onchange = function () { var v = this.checked; setPref(function (st) { st.showTags = v; }); };
$('saveHistBtn').onclick = function () { var ok = false; change(function (st) { ok = saveHistory(st); }); if (ok) toast('Current seats saved.'); };
$('historyList').addEventListener('click', function (e) {
  var r = e.target.closest('[data-hrestore]'), d = e.target.closest('[data-hdel]');
  if (r) {
    var id = r.getAttribute('data-hrestore');
    ask({title:'Restore these seats?', text:'The current seats are saved under Past seatings first.', ok:'Restore'}).then(function (y) {
      if (!y) return;
      change(function (st) { var h = st.history.filter(function (x) { return x.id === id; })[0]; if (!h) return; saveHistory(st, true); st.seats = JSON.parse(JSON.stringify(h.seats)); S.cleanSeats(st); });
      toast('Seats restored.');
    });
  }
  if (d) { var hid = d.getAttribute('data-hdel'); change(function (st) { st.history = st.history.filter(function (x) { return x.id !== hid; }); }); }
});

/* ================= tabs, header fields ================= */
document.querySelector('.tabs').addEventListener('click', function (e) {
  var b = e.target.closest('[data-tab]'); if (!b) return;
  ui.tab = b.getAttribute('data-tab'); ui.sel = []; ui.picked = null; ui.alignOpen = false; render();
});
document.querySelector('.tabs').addEventListener('keydown', function (e) {
  var order = ['room', 'class', 'seats'], i = order.indexOf(ui.tab);
  if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
    e.preventDefault(); ui.tab = order[(i + (e.key === 'ArrowRight' ? 1 : 2)) % 3]; ui.sel = []; ui.picked = null; render(); $('tab-' + ui.tab).focus();
  }
});
$('viewTop').onclick = function () { setPref(function (st) { st.view = 'top'; }); };
$('viewBottom').onclick = function () { setPref(function (st) { st.view = 'bottom'; }); };
$('titleIn').oninput = function () { cur().title = this.value; data.changedAt = Date.now(); save(); };
$('noteIn').oninput = function () { cur().note = this.value; data.changedAt = Date.now(); save(); };
$('undoBtn').onclick = undo; $('redoBtn').onclick = redo;

/* ================= charts menu, backup, files ================= */
function toggleMenu(btn, menu) { var open = menu.hidden; closeMenus(); menu.hidden = !open; btn.setAttribute('aria-expanded', open); if (open) { var f = menu.querySelector('button'); if (f) f.focus(); } }
function closeMenus() { $('chartMenu').hidden = true; $('chartMenuBtn').setAttribute('aria-expanded', 'false'); }
$('chartMenuBtn').onclick = function (e) { e.stopPropagation(); toggleMenu(this, $('chartMenu')); };
document.addEventListener('click', function (e) { if (!e.target.closest('.menuwrap')) closeMenus(); });
$('chartSel').onchange = function () { data.cur = this.value; hist = []; future = []; ui.sel = []; ui.picked = null; ui.pickPool = null; after(); };
function nextName() { var n = data.charts.length + 1; while (data.charts.some(function (c) { return c.name === 'Period ' + n; })) n++; return 'Period ' + n; }
function uniqueName(n) { var base = n, i = 2; while (data.charts.some(function (c) { return c.name === n; })) n = base + ' (' + (i++) + ')'; return n; }
function addChart(c, msg) { data.charts.push(c); data.cur = c.id; hist = []; future = []; ui.sel = []; ui.picked = null; ui.pickPool = null; data.changedAt = Date.now(); after(); if (msg) toast(msg); }
$('chartMenu').addEventListener('click', function (e) {
  var b = e.target.closest('[data-act]'); if (!b) return;
  var a = b.getAttribute('data-act'), st = cur();
  closeMenus();
  if (a === 'new') ask({title:'New chart', input:true, value:nextName(), ok:'Create chart'}).then(function (n) {
    if (n === null) return; addChart(newChart(uniqueName(n || nextName())), 'New chart ready. Pick a layout.'); ui.tab = 'room'; render();
  });
  if (a === 'copyroom') ask({title:'New class in the same room', text:'Copies the desks and labels. The class list starts empty.', input:true, value:nextName(), ok:'Create chart'}).then(function (n) {
    if (n === null) return;
    var c = JSON.parse(JSON.stringify(st)); c.id = S.uid(); c.name = uniqueName(n || nextName()); c.title = ''; c.students = []; c.seats = {}; c.rules = []; c.tags = []; c.history = []; c.subNotes = '';
    addChart(normalize(c), 'Same room, empty class list. Add students in step 2.'); ui.tab = 'class'; render();
  });
  if (a === 'dup') { var c2 = JSON.parse(JSON.stringify(st)); c2.id = S.uid(); c2.name = uniqueName(st.name + ' copy'); addChart(normalize(c2), 'Chart copied.'); }
  if (a === 'rename') ask({title:'Rename this chart', input:true, value:st.name, ok:'Rename'}).then(function (n) { if (n) { st.name = n; data.changedAt = Date.now(); after(); } });
  if (a === 'backup') downloadBackup();
  if (a === 'open') $('fileIn').click();
  if (a === 'delete') ask({title:'Delete “' + st.name + '”?', text:'This chart and its class list are removed from this browser. This cannot be undone.', ok:'Delete chart', danger:true}).then(function (y) {
    if (!y) return;
    data.charts = data.charts.filter(function (c) { return c.id !== st.id; });
    if (!data.charts.length) data.charts.push(newChart('Period 1'));
    data.cur = data.charts[0].id; hist = []; future = []; data.changedAt = Date.now(); after(); toast('Chart deleted.');
  });
});
function stamp() { var d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
function downloadBackup() {
  var payload = {app:'mk-seating-chart', version:2, savedAt:new Date().toISOString(), charts:data.charts};
  download(new Blob([JSON.stringify(payload)], {type:'application/json'}), 'seating-charts-backup-' + stamp() + '.json');
  data.backupAt = Date.now(); save(); renderBackupBar();
  toast('Backup downloaded. Keep it somewhere safe, like Google Drive. Open it from the Charts menu.', 5000);
}
function renderBackupBar() {
  var now = Date.now(), any = data.charts.some(function (c) { return c.students.length; });
  var changed = (data.changedAt || 0) > (data.backupAt || 0);
  var due = data.backupAt ? now - data.backupAt > 14 * DAY : now - (data.firstUse || now) > 30 * 60000;
  $('backupBar').hidden = !(any && changed && due && now > (data.snoozeUntil || 0));
}
$('backupNow').onclick = downloadBackup;
$('backupLater').onclick = function () { data.snoozeUntil = Date.now() + 7 * DAY; save(); renderBackupBar(); };
$('fileIn').onchange = function () {
  var f = this.files[0]; this.value = ''; if (!f) return;
  var rd = new FileReader();
  rd.onload = function () {
    var j; try { j = JSON.parse(rd.result); } catch (err) { j = null; }
    var list = j && Array.isArray(j.charts) ? j.charts : (j && (j.chart || j) && Array.isArray((j.chart || j).items) ? [j.chart || j] : null);
    if (!list || !list.length) { toast('That is not a seating chart file. Use a file saved from this page.'); return; }
    var go = list.length > 1 ? ask({title:'Add ' + list.length + ' charts from this backup?', text:'They are added next to your current charts. Charts with the same name get a number added.', ok:'Add charts'}) : Promise.resolve(true);
    go.then(function (y) {
      if (!y) return;
      var last = null;
      list.forEach(function (c) {
        if (!c || !Array.isArray(c.items) || !Array.isArray(c.students)) return;
        c = normalize(JSON.parse(JSON.stringify(c))); c.id = S.uid(); c.name = uniqueName(c.name || 'Chart');
        data.charts.push(c); last = c;
      });
      if (!last) { toast('No charts could be read from that file.'); return; }
      data.cur = last.id; hist = []; future = []; ui.sel = []; data.changedAt = Date.now(); after();
      toast(list.length > 1 ? plural(list.length, 'chart') + ' added.' : 'Opened “' + last.name + '”.');
    });
  };
  rd.readAsText(f);
};

/* ================= print and export ================= */
function slug() { var st = cur(); return ((st.title.trim() || st.name).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'class') + '-seating-chart'; }
function download(blob, name) {
  var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
}
function chartSvg() { return S.exportSvg(cur(), {big:data.prefs.big, tags:data.prefs.tags}); }
function pageSvgs() {
  var pages = [chartSvg()];
  if (data.prefs.sub) pages = pages.concat(S.notesSvgs(cur(), S.PAPER[data.prefs.paper]));
  return pages;
}
function rasterize(svgStr, scale) {
  return new Promise(function (resolve, reject) {
    var m = svgStr.match(/width="(\d+)" height="(\d+)"/), W = +m[1], H = +m[2], img = new Image();
    img.onload = function () {
      var c = document.createElement('canvas'); c.width = Math.round(W * scale); c.height = Math.round(H * scale);
      var x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); x.drawImage(img, 0, 0, c.width, c.height); resolve(c);
    };
    img.onerror = reject;
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgStr);
  });
}
function jpegBytes(c) { var url = c.toDataURL('image/jpeg', 0.92), bin = atob(url.split(',')[1]), b = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) b[i] = bin.charCodeAt(i); return {bytes:b, w:c.width, h:c.height}; }
function fillPrint() {
  $('printArea').innerHTML = pageSvgs().map(function (s) { return '<div class="pg">' + s + '</div>'; }).join('');
  $('pageStyle').textContent = '@page{size:' + (data.prefs.paper === 'a4' ? 'A4' : 'letter') + ' landscape;margin:0.35in}';
}
window.addEventListener('beforeprint', fillPrint);
function doExport(kind) {
  if (kind === 'print') { fillPrint(); setTimeout(function () { window.print(); }, 50); return; }
  if (kind === 'svg') { download(new Blob([chartSvg()], {type:'image/svg+xml'}), slug() + '.svg'); toast('Downloading the SVG drawing.'); }
  if (kind === 'csv') { download(new Blob([S.csv(cur())], {type:'text/csv'}), slug() + '.csv'); toast('Downloading the class list.'); }
  if (kind === 'png') rasterize(chartSvg(), 2).then(function (c) { c.toBlob(function (bl) { download(bl, slug() + '.png'); }, 'image/png'); toast('Downloading the PNG image.'); })
    .catch(function () { toast('The image could not be made in this browser. Try Print instead.'); });
  if (kind === 'pdf') Promise.all(pageSvgs().map(function (s, i) { return rasterize(s, i ? 2.2 : 2.4); })).then(function (cs) {
    download(new Blob([S.pdf(cs.map(jpegBytes), S.PAPER[data.prefs.paper])], {type:'application/pdf'}), slug() + '.pdf');
    toast('Downloading the PDF.');
  }).catch(function () { toast('The PDF could not be made in this browser. Use Print and choose Save as PDF.'); });
}
$('exportBtn').onclick = function () {
  var st = cur(), p = data.prefs;
  var html = '<form method="dialog"><h2>Print and export</h2><div class="body">' +
    '<label class="field"><span>Paper</span><select id="exPaper"><option value="letter">US Letter</option><option value="a4">A4</option></select></label>' +
    '<label class="check"><input type="checkbox" id="exBig"' + (p.big ? ' checked' : '') + '> Larger names</label>' +
    '<label class="check"><input type="checkbox" id="exNums"' + (st.deskNums ? ' checked' : '') + '> Show desk numbers</label>' +
    (st.tags.length ? '<label class="check"><input type="checkbox" id="exTags"' + (p.tags ? ' checked' : '') + '> Show tag colors</label>' : '') +
    '<label class="check"><input type="checkbox" id="exSub"' + (p.sub ? ' checked' : '') + '> Add notes for a substitute (PDF and Print)</label>' +
    '<div id="exSubBox"' + (p.sub ? '' : ' hidden') + '><label class="field"><span>Notes for the substitute: schedule, helpers, where things are</span><textarea id="exSubNotes">' + esc(st.subNotes || '') + '</textarea></label>' +
    '<p class="note">Student notes and seat needs from step 2, keep-apart rules and a class list with check boxes for attendance are added after the chart.</p></div>' +
    '<h3>Print or download</h3><div class="expgrid">' +
    '<button type="button" class="btn primary" data-x="print">Print<small>Landscape, choose Save as PDF there too</small></button>' +
    '<button type="button" class="btn" data-x="pdf">PDF<small>Ready to print or email</small></button>' +
    '<button type="button" class="btn" data-x="png">PNG image<small>Chart only, for slides or email</small></button>' +
    '<button type="button" class="btn" data-x="svg">SVG drawing<small>Chart only, sharp at any size</small></button>' +
    '<button type="button" class="btn" data-x="csv">Class list (CSV)<small>Desks, seats, needs and notes for Excel or Sheets</small></button>' +
    '</div></div><div class="dlgbtns"><button value="close" class="btn quiet">Close</button></div></form>';
  openDialog(html).then(function () { dlg.onchange = null; dlg.onclick = null; dlg.oninput = null; });
  $('exPaper').value = p.paper;
  dlg.onchange = function (e) {
    var id = e.target.id;
    if (id === 'exPaper') p.paper = e.target.value;
    if (id === 'exBig') p.big = e.target.checked;
    if (id === 'exTags') p.tags = e.target.checked;
    if (id === 'exSub') { p.sub = e.target.checked; $('exSubBox').hidden = !p.sub; }
    if (id === 'exNums') { cur().deskNums = e.target.checked; render(); }
    save();
  };
  dlg.oninput = function (e) { if (e.target.id === 'exSubNotes') { cur().subNotes = e.target.value; data.changedAt = Date.now(); save(); } };
  dlg.onclick = function (e) {
    var b = e.target.closest('[data-x]'); if (!b) return;
    var k = b.getAttribute('data-x');
    if (k === 'print') dlg.close();
    doExport(k);
  };
};

/* ================= projector and student picker ================= */
function renderProj() {
  var st = cur(), D = dims(), hl = {};
  if (ui.flash) hl[ui.flash] = 'flash';
  $('projTitle').textContent = (st.title || '').trim() || st.name;
  var ps = $('projSvg');
  ps.setAttribute('viewBox', '-12 -12 ' + (D.w + 24) + ' ' + (D.h + 24));
  ps.setAttribute('font-family', S.FONT);
  ps.innerHTML = S.roomSvg(st, {big:true, hl:hl});
}
function openProj() {
  if (!cur().items.length) { toast('Set up the room first.'); return; }
  ui.proj = true; $('proj').hidden = false; renderProj();
  var el = $('proj');
  if (el.requestFullscreen) el.requestFullscreen().then(function () { ui.projFs = true; }).catch(function () { ui.projFs = false; });
  $('projExit').focus();
}
function closeProj() {
  ui.proj = false; $('proj').hidden = true; $('projCard').hidden = true;
  if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(function () {});
  ui.projFs = false; $('projBtn').focus();
}
document.addEventListener('fullscreenchange', function () { if (!document.fullscreenElement && ui.proj && ui.projFs) closeProj(); });
$('projBtn').onclick = openProj; $('projExit').onclick = closeProj;
function pickStudent() {
  var st = cur(), keys = Object.keys(st.seats);
  if (!keys.length) { toast('Seat students first, then pick.'); return; }
  var seated = keys.map(function (k) { return st.seats[k]; });
  var pool = (ui.pickPool || []).filter(function (sid) { return seated.indexOf(sid) >= 0; });
  if (!pool.length) pool = S.shuffle(seated.slice());
  var sid = pool.pop(); ui.pickPool = pool;
  var key = S.seatOf(st, sid), stu = S.student(st, sid);
  clearTimeout(ui.pickTimer); $('pickCard').hidden = true; $('projCard').hidden = true;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches, steps = reduce || keys.length < 2 ? 0 : 12, i = 0;
  function paint() { if (ui.proj) renderProj(); else render(); }
  (function step() {
    if (i < steps) { var k; do { k = keys[Math.floor(Math.random() * keys.length)]; } while (k === ui.flash && keys.length > 1); ui.flash = k; i++; paint(); ui.pickTimer = setTimeout(step, 55 + i * i * 2.4); return; }
    ui.flash = key; paint();
    var card = ui.proj ? $('projCard') : $('pickCard');
    card.innerHTML = esc(stu.name) + '<small>' + (pool.length ? plural(pool.length, 'student') + ' left before anyone repeats' : 'Everyone has had a turn. The next pick starts over.') + '</small>';
    card.hidden = false;
    ui.pickTimer = setTimeout(function () { ui.flash = null; card.hidden = true; paint(); }, 9000);
  })();
}
$('pickBtn').onclick = pickStudent; $('projPick').onclick = pickStudent;

/* ================= start ================= */
$('backLink').addEventListener('click', function (e) {
  try { if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) { e.preventDefault(); history.back(); } } catch (err) {}
});
window.addEventListener('resize', function () { renderSelbar(); });
load();
buildPresetButtons($('presetList'));
buildPresetButtons($('emptyPresets'));
buildAddButtons();
render();
window.MKSEAT = {data:function () { return data; }, cur:cur, ui:ui, render:render};
})();
