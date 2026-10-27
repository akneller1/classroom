/* Daily Lesson Planner — PowerPoint export.

   MKPLAN.buildDeck(plan, PptxGenJS, {figImage})  → a pptxgenjs presentation (Node tests use this directly)
   MKPLAN.exportPptx(plan)                        → builds the deck in the browser and downloads the .pptx

   The deck follows the day: title + "Today I can…", agenda, then each part of the lesson. Problems are editable
   text (MKPLAN.mathText turns the TeX into Unicode such as x², (1/2)x, ≤, √); graphs, number lines and plots are
   pictures; tables are PowerPoint tables. Every problem slide is followed by its answer slide (worked steps for
   examples); answers and the teacher notes for each part are also in the speaker notes.
   Layout: 13.33" × 7.5" (widescreen). Colors follow the site (ink, blue, yellow). */
(function (G) {
  'use strict';
  var P = (G.MKPLAN = G.MKPLAN || {});
  var INK = '16202E', INK2 = '46536A', BLUE = '2B5FD9', SOFT = 'E3EBFF', YELLOW = 'FFD84D', WHITE = 'FFFFFF', LINE = 'C9D3DB', ANS = '1D5FBF';
  var SEC = { donow: { c: 'B7791F', bg: 'FFF3C4' }, notes: { c: BLUE, bg: SOFT }, examples: { c: BLUE, bg: SOFT }, practice: { c: '2F7A50', bg: 'DFF2E5' }, mixed: { c: '267F86', bg: 'E1F4F4' }, summary: { c: '6446A9', bg: 'F2EDFC' }, exit: { c: '6B3FA0', bg: 'EDE4FA' } };
  var HEAD = 'Arial', BODY = 'Calibri';
  var W = 13.333, H = 7.5, MX = 0.6, TOP = 1.45, BOTTOM = 6.85;

  function T(s) { return P.mathText(s || ''); }
  function lessonTitle(id) { var l = P.lessonById(id); return l ? l.title : id; }
  function problemText(p) {
    var t = T(p.prompt || ''), parts = (p.parts || []).filter(function (x) { return x.prompt; });
    if (p.work && p.work.length) t += '\n' + p.work.map(function (w, i) { return 'Line ' + (i + 1) + ': ' + T('⟨' + w + '⟩'); }).join('\n');
    if (parts.length) t += '\n' + parts.map(function (x) { return (x.label ? '(' + x.label + ') ' : '') + T(x.prompt); }).join('\n');
    return t;
  }
  function answerText(p) {
    var parts = p.parts || [];
    return parts.map(function (x) { return (parts.length > 1 && x.label ? '(' + x.label + ') ' : '') + T(x.answer || ''); }).join('   ');
  }
  function stepsText(p) { return (p.steps || []).filter(function (s) { return s.t || s.m; }).map(function (s, i) { return (i + 1) + '. ' + T(s.t || '') + (s.m ? ' ' + T('⟨' + s.m + '⟩') : ''); }); }
  function isTable(spec) { return spec && (spec.kind === 'table' || spec.kind === 'twoway'); }
  function heavy(p) { return !!p.fig || problemText(p).length > 120 || (p.parts || []).filter(function (x) { return x.prompt; }).length > 1; }
  function chunk(items, maxLight) {
    var out = [], cur = [];
    items.forEach(function (p) {
      var cap = cur.concat([p]).some(heavy) ? 1 : maxLight;
      if (cur.length && cur.length + 1 > cap) { out.push(cur); cur = []; }
      cur.push(p);
    });
    if (cur.length) out.push(cur);
    return out;
  }
  function frameText(f) { return String(f || '').replace(/_{2,}/g, '________'); }

  P.buildDeck = async function (plan, PptxGenJS, opts) {
    opts = opts || {};
    var figImage = opts.figImage || function () { return null; };
    var studentDeck = opts.audience === 'student';
    var d = plan.day, NSL = G.MKMENU.LEVELS[plan.level];
    var pres = new PptxGenJS();
    pres.layout = 'LAYOUT_WIDE';
    pres.author = "Mr. K's Classroom";
    pres.title = 'Day ' + d.day + ': ' + d.title;
    pres.subject = 'Algebra 1 daily lesson';
    pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
    var footer = 'Algebra 1 · Day ' + d.day + ' · ' + d.title + ' · ' + NSL.name;
    pres.defineSlideMaster({ title: 'TITLE', background: { color: INK }, objects: [] });
    pres.defineSlideMaster({
      title: 'CONTENT', background: { color: WHITE },
      objects: [
        { placeholder: { options: { name: 'title', type: 'title', x: MX, y: 0.62, w: W - 2 * MX - 2.2, h: 0.75, fontFace: HEAD, fontSize: 30, bold: true, color: INK, align: 'left', valign: 'middle', margin: 0 }, text: '' } },
        { text: { text: footer, options: { x: MX, y: 7.02, w: W - 2 * MX - 1, h: 0.3, fontFace: BODY, fontSize: 10, color: INK2, margin: 0 } } }
      ],
      slideNumber: { x: W - MX - 0.6, y: 7.02, w: 0.6, h: 0.3, fontFace: BODY, fontSize: 10, color: INK2, align: 'right' }
    });
    var cache = {}, minShown = new Set();
    async function img(spec) { var k = JSON.stringify(spec); if (!(k in cache)) cache[k] = await figImage(spec); return cache[k]; }

    function content(title, sec, minutes) {
      var s = pres.addSlide({ masterName: 'CONTENT' });
      s.addText(title, { placeholder: 'title', fontSize: Math.max(18, Math.min(30, Math.floor((W - 2 * MX - 2.2) * 72 / (0.6 * title.length)))) });
      var st = SEC[sec.id] || SEC.notes;
      s.addText((sec.label || sec.title).toUpperCase(), { x: MX, y: 0.28, w: 4.5, h: 0.32, fontFace: HEAD, fontSize: 12, bold: true, color: st.c, charSpacing: 1.5, margin: 0, isTextBox: true, objectName: 'Section label' });
      if (minutes && !minShown.has(sec)) minShown.add(sec), s.addText(minutes + ' min', { shape: pres.ShapeType.roundRect, x: W - MX - 1.5, y: 0.7, w: 1.5, h: 0.55, rectRadius: 0.27, fill: { color: st.bg }, line: { color: st.c, width: 1.5 }, fontFace: HEAD, fontSize: 18, bold: true, color: INK, align: 'center', valign: 'middle', objectName: 'Minutes' });
      return s;
    }
    function notes(s, lines) { if (studentDeck) return; var t = lines.filter(Boolean).join('\n'); if (t) s.addNotes(t); }
    function teacherNotes(sec) {
      var out = [];
      if (sec.template) out.push('PLAN: ' + sec.template);
      if (sec.prompt) out.push('Prompt: ' + sec.prompt);
      return out;
    }

    /* A card holding one problem (and optionally its answer and steps). */
    async function card(s, p, x, y, w, h, mode, label, fontSize) {
      var st = SEC[mode.sec] || SEC.notes;
      s.addShape(pres.ShapeType.roundRect, { x: x, y: y, w: w, h: h, rectRadius: 0.12, fill: { color: mode.answers ? 'F7F9FC' : WHITE }, line: { color: LINE, width: 1.25 }, objectName: 'Problem card' });
      s.addText(label, { shape: pres.ShapeType.ellipse, x: x + 0.18, y: y + 0.18, w: 0.5, h: 0.5, fill: { color: st.c }, line: { color: st.c }, fontFace: HEAD, fontSize: label.length > 2 ? 12 : 16, bold: true, color: WHITE, align: 'center', valign: 'middle', margin: 0, objectName: 'Problem number' });
      if (p.failed) { s.addText('Write your own problem here.', { x: x + 0.85, y: y + 0.15, w: w - 1.05, h: 0.6, fontFace: BODY, fontSize: 18, italic: true, color: INK2, margin: 0, isTextBox: true }); return; }
      var tx = x + 0.85, tw = w - 1.05, ty = y + 0.18, bottom = y + h - 0.18, one = w > 8;
      var ansLines = mode.answers ? answerText(p) : '', steps = mode.steps ? stepsText(p) : [];
      var ansFig = mode.answers && (p.parts || []).filter(function (x) { return x.answerFig; })[0];
      var blankLine = p.fig && Array.isArray(p.fig.pieces) && !p.fig.pieces.length;
      var spec = mode.answers && ansFig ? ansFig.answerFig : p.fig && !(blankLine && mode.answers) ? p.fig : null;
      // Figure: wide ones (number lines, horizontal tables, box plots) go under the text across the card; others to the right.
      var im = null, ratio = 1.3, figBox = null;
      if (spec) {
        if (isTable(spec)) ratio = spec.kind === 'table' && !spec.vertical ? 1.2 * (spec.rows.length + 1) / 2 : spec.kind === 'twoway' ? 1.8 : 0.9;
        else { im = await img(spec); if (im) ratio = im.w / im.h; else spec = null; }
      }
      if (spec) {
        if (ratio >= 2.2) {
          var fw = tw, fh = Math.min(fw / ratio, (bottom - ty) * 0.42);
          figBox = { x: tx, y: bottom - fh, w: fw, h: fh }; bottom -= fh + 0.12;
        } else {
          var sw = Math.min(tw * (one ? 0.48 : 0.42), one ? 5.2 : 2.6);
          figBox = { x: x + w - sw - 0.18, y: ty, w: sw, h: Math.min(bottom - ty, sw / ratio + 0.01) }; tw -= sw + 0.2;
        }
      }
      var qSize = mode.answers ? (one ? 20 : 16) : fontSize;
      qSize = fitSize(problemText(p), tw, mode.answers ? Math.min(1.6, bottom - ty - 1) : bottom - ty, qSize, mode.answers ? 11 : 14);
      var qLines = Math.ceil(problemText(p).length * qSize * 0.0078 / tw) + (problemText(p).match(/\n/g) || []).length;
      var qH = mode.answers ? Math.min(bottom - ty - 0.9, Math.max(0.45, qLines * qSize / 72 * 1.25 + 0.1)) : bottom - ty;
      s.addText(problemText(p), { x: tx, y: ty, w: tw, h: Math.max(0.2, qH), fit: 'shrink', breakLine: false, fontFace: BODY, fontSize: qSize, color: mode.answers ? INK2 : INK, valign: 'top', margin: [2, 2, 2, 2], isTextBox: true, objectName: 'Problem' });
      if (mode.answers) {
        var ay = ty + qH + 0.1, aSize = one ? 28 : 22;
        var aLines = Math.ceil((ansLines.length + 8) * aSize * 0.0078 / tw), aH = aLines * aSize / 72 * 1.25 + 0.1;
        s.addText([{ text: 'Answer: ', options: { bold: true, color: ANS } }, { text: ansLines, options: { bold: true, color: INK } }], { x: tx, y: ay, w: tw, h: Math.max(0.25, Math.min(aH, bottom - ay)), fit: 'shrink', fontFace: BODY, fontSize: aSize, valign: 'top', margin: [2, 2, 2, 2], isTextBox: true, objectName: 'Answer' });
        if (steps.length) s.addText(steps.map(function (t, i) { return { text: t, options: { breakLine: i < steps.length - 1 } }; }), { x: tx, y: ay + aH + 0.1, w: tw, h: Math.max(0.2, bottom - ay - aH - 0.1), fit: 'shrink', fontFace: BODY, fontSize: one ? 18 : 15, color: INK, valign: 'top', margin: [2, 2, 2, 2], paraSpaceAfter: 4, isTextBox: true, objectName: 'Worked steps' });
      }
      if (spec && figBox) {
        if (isTable(spec)) addFigTable(s, spec, figBox);
        else placeImage(s, im, figBox);
      }
    }
    /* Largest font size (down to min) at which the text fits in w × h inches, estimated from average glyph width. */
    function fitSize(text, w, h, size, min) {
      for (; size > min; size -= 1) {
        var perLine = Math.max(1, Math.floor(w * 72 / (size * 0.5)));
        var lines = String(text).split('\n').reduce(function (n, l) { return n + Math.max(1, Math.ceil(l.length / perLine)); }, 0);
        if (lines * size * 1.25 / 72 + 0.1 <= h) break;
      }
      return size;
    }
    function placeImage(s, im, box) {
      var r = im.w / im.h, w = box.w, h = w / r;
      if (h > box.h) { h = box.h; w = h * r; }
      s.addImage({ data: im.data, x: box.x + (box.w - w) / 2, y: box.y + (box.h - h) / 2, w: w, h: h, altText: im.alt || 'figure' });
    }
    function addFigTable(s, spec, box) {
      var cell = function (v, head) { return { text: typeof v === 'number' ? String(v).replace('-', '−') : T(String(v)), options: head ? { bold: true, fill: { color: 'EEEEEE' } } : {} }; };
      var rows;
      if (spec.kind === 'twoway') rows = [[cell(spec.corner || '', true)].concat(spec.cols.map(function (c) { return cell(c, true); }))].concat(spec.rows.map(function (r) { return [cell(r.label, true)].concat(r.cells.map(function (v) { return cell(v); })); }));
      else if (spec.vertical) rows = [[cell(spec.head[0], true), cell(spec.head[1], true)]].concat(spec.rows.map(function (r) { return [cell(r[0]), cell(r[1])]; }));
      else rows = [[cell(spec.head[0], true)].concat(spec.rows.map(function (r) { return cell(r[0]); })), [cell(spec.head[1], true)].concat(spec.rows.map(function (r) { return cell(r[1]); }))];
      var cols = rows[0].length, cw = Math.min(0.9, box.w / cols);
      var rh = Math.min(0.46, Math.max(0.22, box.h / Math.max(1, rows.length)));
      s.addTable(rows, { x: box.x, y: box.y, w: cw * cols, colW: rows[0].map(function () { return cw; }), fontFace: BODY, fontSize: Math.max(9, Math.min(14, rh * 26)), color: INK, border: { type: 'solid', pt: 1, color: '555555' }, align: 'center', valign: 'middle', rowH: rh, objectName: 'Table' });
    }
    async function grid(s, list, mode, labels) {
      var n = list.length, cols = n === 1 ? 1 : 2, rows = Math.ceil(n / cols), gap = 0.3;
      var cw = (W - 2 * MX - (cols - 1) * gap) / cols, ch = (BOTTOM - TOP - (rows - 1) * gap) / rows;
      var fs = n === 1 ? 32 : rows === 1 ? 26 : 22;
      for (var i = 0; i < n; i++) {
        await card(s, list[i], MX + (i % cols) * (cw + gap), TOP + Math.floor(i / cols) * (ch + gap), cw, ch, mode, labels ? labels[i] : String(list[i].num), fs);
      }
    }
    /* Problem slides, each followed by its answer slide. */
    async function problemSlides(sec, title, items, o) {
      o = o || {};
      var pages = o.onePer || o.steps ? items.map(function (p) { return [p]; }) : chunk(items, Math.min(o.max || 4, 2));
      for (var k = 0; k < pages.length; k++) {
        var list = pages[k], labels = o.labels ? list.map(function (p) { return o.labels(p); }) : null;
        var t = title + (pages.length > 1 && !o.onePer ? ' (' + (k + 1) + ' of ' + pages.length + ')' : '');
        var ansNotes = list.map(function (p) { return (labels ? labels[list.indexOf(p)] : p.num + '.') + ' ' + (p.failed ? '(write your own)' : answerText(p)); });
        if (!o.answersOnly || studentDeck) {
          var s = content(t, sec, k === 0 ? sec.minutes : 0);
          if (o.note && o.note.length < 40 && k === 0) s.addText(o.note, { x: MX + 4.6, y: 0.28, w: 6, h: 0.32, fontFace: BODY, fontSize: 13, italic: true, color: INK2, margin: 0, isTextBox: true });
          await grid(s, list, { sec: sec.id }, labels);
          notes(s, (k === 0 ? teacherNotes(sec).concat(o.extraNotes || []) : []).concat(['ANSWERS:'], ansNotes));
        }
        if (studentDeck) continue;
        var a = content(t.replace(/^(.*?)( \(\d+ of \d+\))?$/, function (_, m1, m2) { return m1 + ' — Answers' + (m2 || ''); }), sec, 0);
        await grid(a, list, { sec: sec.id, answers: true, steps: !!o.steps }, labels);
        notes(a, ['Go over the answers. Ask students to explain a step before revealing the next.'].concat(list.map(function (p) { return p.failed ? '' : (p.num + '. ' + stepsText(p).join(' ')); })));
      }
    }
    function textSlide(sec, title, paras, o) {
      o = o || {};
      var s = content(title, sec, o.minutes);
      var runs = [];
      paras.forEach(function (p, i) { runs.push({ text: p.text, options: { bold: !!p.bold, bullet: p.bullet ? { indent: 22 } : false, fontSize: p.size || 22, color: p.color || INK, breakLine: i < paras.length - 1, paraSpaceAfter: 10 } }); });
      s.addShape(pres.ShapeType.roundRect, { x: MX, y: TOP, w: W - 2 * MX, h: BOTTOM - TOP, rectRadius: 0.12, fill: { color: (SEC[sec.id] || SEC.notes).bg }, line: { color: (SEC[sec.id] || SEC.notes).bg }, objectName: 'Panel' });
      s.addText(runs, { x: MX + 0.4, y: TOP + 0.3, w: W - 2 * MX - 0.8, h: BOTTOM - TOP - 0.6, fontFace: BODY, valign: 'top', margin: 0, fit: 'shrink', isTextBox: true, objectName: 'Body' });
      notes(s, teacherNotes(sec).concat(o.notes || []));
      return s;
    }
    function tableSlides(sec, title, head, rows, o) {
      o = o || {};
      var per = o.per || 7;
      for (var k = 0; k < rows.length; k += per) {
        var s = content(title + (rows.length > per ? ' (' + (k / per + 1) + ' of ' + Math.ceil(rows.length / per) + ')' : ''), sec, k === 0 ? o.minutes : 0);
        var data = [head.map(function (h) { return { text: h, options: { bold: true, color: WHITE, fill: { color: INK } } }; })].concat(rows.slice(k, k + per).map(function (r) { return r.map(function (c) { return { text: c }; }); }));
        s.addTable(data, { x: MX, y: TOP, w: W - 2 * MX, colW: o.colW, fontFace: BODY, fontSize: o.fontSize || 16, color: INK, border: { type: 'solid', pt: 1, color: LINE }, valign: 'middle', rowH: o.rowH || 0.6, autoPage: false, objectName: 'Table' });
        notes(s, k === 0 ? teacherNotes(sec).concat(o.notes || []) : []);
      }
    }

    /* ---- 1. title ---- */
    var t1 = pres.addSlide({ masterName: 'TITLE' });
    var unitLine = d.unit ? 'Unit ' + d.unit + ': ' + d.unit_title + ' · day ' + d.unit_day : d.unit_title;
    t1.addText('ALGEBRA 1 · DAY ' + d.day + ' · ' + d.day_type.toUpperCase(), { x: MX + 0.1, y: 0.75, w: 10, h: 0.4, fontFace: HEAD, fontSize: 16, bold: true, color: YELLOW, charSpacing: 2, margin: 0, isTextBox: true });
    t1.addText(d.title, { x: MX + 0.1, y: 1.25, w: W - 2 * MX - 0.2, h: 1.9, fontFace: HEAD, fontSize: 44, bold: true, color: WHITE, valign: 'top', margin: 0, fit: 'shrink', isTextBox: true, objectName: 'Title' });
    t1.addText(unitLine, { x: MX + 0.1, y: 3.15, w: W - 2 * MX - 0.2, h: 0.45, fontFace: BODY, fontSize: 20, color: 'C9D3E6', margin: 0, isTextBox: true });
    if (d.content_objective) {
      t1.addShape(pres.ShapeType.roundRect, { x: MX + 0.1, y: 4.0, w: W - 2 * MX - 0.2, h: 1.55, rectRadius: 0.15, fill: { color: YELLOW }, line: { color: YELLOW }, objectName: 'Objective card' });
      t1.addText([{ text: 'Today ', options: { bold: true } }, { text: P.iCan(d.content_objective) }], { x: MX + 0.45, y: 4.1, w: W - 2 * MX - 0.9, h: 1.35, fontFace: BODY, fontSize: 24, color: INK, valign: 'middle', margin: 0, fit: 'shrink', isTextBox: true, objectName: 'Objective' });
    }
    if (d.language_objective) t1.addText(d.language_objective.replace(/^Students will/i, 'I will'), { x: MX + 0.1, y: 5.8, w: W - 2 * MX - 0.2, h: 0.8, fontFace: BODY, fontSize: 16, italic: true, color: 'C9D3E6', valign: 'top', margin: 0, fit: 'shrink', isTextBox: true });
    t1.addText(d.standards ? 'Standards: ' + d.standards + '   ·   ' + NSL.name : NSL.name, { x: MX + 0.1, y: 6.85, w: W - 2 * MX, h: 0.3, fontFace: BODY, fontSize: 11, color: '9AA7BF', margin: 0, isTextBox: true });
    notes(t1, ['Standards: ' + (d.standards || ''), 'Content objective: ' + (d.content_objective || ''), 'Language objective: ' + (d.language_objective || ''), P.watchOut(d) ? 'Watch for: ' + P.watchOut(d) : '', d.do_now_strategy ? 'Do Now: ' + d.do_now_strategy : '']
      .concat(plan.coverage.filter(function (c) { return c.cover !== 'full'; }).map(function (c) { return 'Add your own (' + c.id + '): ' + c.note; })));

    /* ---- 2. agenda ---- */
    var ag = content("Today's plan", { id: 'notes', title: 'Agenda' }, 0);
    var n = plan.sections.length, gap = 0.3, cw = n ? (W - 2 * MX - (n - 1) * gap) / n : 0;
    plan.sections.forEach(function (sec, i) {
      var st = SEC[sec.id] || SEC.notes, x = MX + i * (cw + gap);
      ag.addShape(pres.ShapeType.roundRect, { x: x, y: TOP + 0.2, w: cw, h: 3.3, rectRadius: 0.15, fill: { color: st.bg }, line: { color: st.bg }, objectName: 'Agenda card' });
      ag.addText(sec.minutes ? String(sec.minutes) : '–', { x: x + 0.3, y: TOP + 0.45, w: cw - 0.6, h: 1.0, fontFace: HEAD, fontSize: 54, bold: true, color: st.c, margin: 0, isTextBox: true });
      ag.addText('min', { x: x + 0.3, y: TOP + 1.45, w: cw - 0.6, h: 0.35, fontFace: BODY, fontSize: 14, color: INK2, margin: 0, isTextBox: true });
      ag.addText(sec.title, { x: x + 0.3, y: TOP + 1.95, w: cw - 0.6, h: 1.3, fontFace: HEAD, fontSize: 20, bold: true, color: INK, valign: 'top', margin: 0, fit: 'shrink', isTextBox: true });
    });
    if (!n) ag.addText('No lesson sections selected.', {x:MX,y:TOP+1,w:W-2*MX,h:0.7,fontFace:BODY,fontSize:26,color:INK2});
    var voc = P.vocab(d);
    if (voc.length && n) {
      ag.addText('Key vocabulary', { x: MX, y: 5.2, w: 4, h: 0.4, fontFace: HEAD, fontSize: 16, bold: true, color: INK, margin: 0, isTextBox: true });
      ag.addText(voc.join('   ·   '), { x: MX, y: 5.65, w: W - 2 * MX, h: 0.9, fontFace: BODY, fontSize: 20, color: INK, valign: 'top', margin: 0, fit: 'shrink', isTextBox: true });
    }
    notes(ag, plan.sections.map(function (s) { return s.title + ' (' + (s.minutes || 0) + ' min): ' + (s.template || ''); }));

    /* ---- 3. the parts of the day ---- */
    for (var si = 0; si < plan.sections.length; si++) {
      var sec = plan.sections[si], items = [];
      sec.groups.forEach(function (g) { g.items.forEach(function (p) { items.push(p); }); });
      if (sec.prompt) textSlide(sec, sec.title, [{ text: sec.prompt, size: 30 }].concat(items.length ? [] : [{ text: ' ', size: 12 }]), { minutes: sec.minutes });
      if (sec.id === 'notes') await notesSlides(sec);
      if (sec.id === 'examples') await exampleSlides(sec);
      else if (sec.launch) { var lt = P.launchTask(d); textSlide(sec, lt.title, [{ text: lt.student, size: 28 }], { minutes: sec.minutes, notes: [lt.teacher] }); }
      else if (sec.project && sec.id === 'practice') textSlide(sec, 'Project checkpoints', P.projectCheckpoints(d).map(function (c) { return { text: '☐  ' + c, size: 28 }; }), { minutes: sec.minutes });
      if (sec.id === 'notes' || sec.id === 'examples') continue;
      if (sec.quiz) {
        textSlide(sec, sec.title, [{ text: sec.test ? 'Show your work for every problem. Box your final answer.' : 'Show your work. Box your final answer.', size: 30 }, { text: items.length + ' problems · ' + (sec.minutes || '') + ' minutes', size: 22, color: INK2 }], { minutes: sec.minutes, notes: ['The problems are on the printed handout. The answer slides that follow are for going over the ' + (sec.test ? 'test' : 'quiz') + ' afterward.'] });
        if (!studentDeck) await problemSlides(sec, sec.title, items, { answersOnly: true });
      } else if (items.length) {
        for (var gi = 0; gi < sec.groups.length; gi++) {
          var g = sec.groups[gi];
          if (!g.items.length) continue;
          var title = sec.groups.length > 1 && g.name ? (sec.id === 'practice' && /^(We do|You do|Level|Tier|Enrichment|Station|Unit)/.test(g.name) ? g.name : sec.title + ': ' + g.name) : sec.title;
          await problemSlides(sec, title, g.items, { note: g.note || '', extraNotes: g.note ? [g.note] : [], steps: g.name === 'Practice set 1' || /Tier 1/.test(g.name) });
        }
      }
      if (sec.id === 'exit' || sec.id === 'summary') {
        if (sec.frame) textSlide(sec, 'Summary', [{ text: frameText(sec.frame), size: 30 }], { notes: ['Students write the summary sentence on their exit ticket.'] });
        if (sec.selfAssess || sec.confidence) tableSlides(sec, sec.confidence ? 'How confident am I?' : 'How sure am I?', ['Topic', '1', '2', '3', '4'], (sec.selfAssess || sec.confidence).map(function (id) { return [id === 'LAUNCH-2' ? 'Pre-algebra skills' : lessonTitle(id), '', '', '', '']; }), { colW: [W - 2 * MX - 3.2, 0.8, 0.8, 0.8, 0.8], notes: ['1 = not yet, 4 = I could teach it.'] });
        if (sec.iCan) tableSlides(sec, 'I can…', ['', 'I can'], sec.iCan.map(function (id) { var l = P.lessonById(id); return ['☐', l ? P.iCan(l.content_objective) : id]; }), { colW: [0.6, W - 2 * MX - 0.6], rowH: 0.5, fontSize: 15, per: 8 });
        if (sec.iCanUnits) tableSlides(sec, 'How ready am I?', ['Unit', '1', '2', '3', '4'], sec.iCanUnits.map(function (u) { return ['Unit ' + u.unit + ': ' + u.title, '', '', '', '']; }), { colW: [W - 2 * MX - 3.2, 0.8, 0.8, 0.8, 0.8] });
        if (!items.length && !sec.frame && !sec.selfAssess && !sec.confidence && !sec.iCan && !sec.iCanUnits && !sec.prompt) textSlide(sec, sec.title, [{ text: sec.template || 'Reflect on today.', size: 28 }]);
      }
    }

    async function notesSlides(sec) {
      if (sec.routines) { tableSlides(sec, sec.title, ['Routine', 'What it looks like'], P.routines(d), { colW: [3, W - 2 * MX - 3], minutes: sec.minutes, fontSize: 18, rowH: 0.8 }); return; }
      if (sec.project) { tableSlides(sec, sec.title, ['Model', 'Pattern in the data', 'Equation'], [['Linear', 'constant differences (same amount added)', 'y = mx + b'], ['Exponential', 'constant ratios (same factor multiplied)', 'y = a · bˣ'], ['Quadratic', 'constant second differences; rises then falls', 'y = ax² + bx + c']], { colW: [2.4, 6.2, W - 2 * MX - 8.6], minutes: sec.minutes, fontSize: 18, rowH: 0.9, notes: ['Rubric: model choice · equation · graph · explanation · presentation (4 points each).'] }); return; }
      if (sec.corrections) { textSlide(sec, 'Test corrections', [{ text: 'For each missed problem:', bold: true, size: 26 }, { text: 'My error was ________.', bullet: true, size: 26 }, { text: 'The correct approach is ________.', bullet: true, size: 26 }, { text: 'Show the correct work next to it.', bullet: true, size: 26 }], { minutes: sec.minutes }); return; }
      if (sec.reference) {
        var groups = sec.byUnit ? P.byUnit(sec.reference) : [{ ids: sec.reference }];
        groups.forEach(function (g, i) {
          tableSlides(sec, sec.title + (g.unit ? ': Unit ' + g.unit : ''), ['Lesson', 'Key vocabulary', sec.myExample ? 'My example' : 'Key idea'], g.ids.map(function (id) { var l = P.lessonById(id); return [l ? l.title : id, l ? l.key_vocabulary : '', sec.myExample ? '' : P.keyIdea(id)]; }), sec.myExample ? { colW: [4.2, 4.4, W - 2 * MX - 8.6], minutes: i === 0 ? sec.minutes : 0, fontSize: 14, rowH: 0.62 } : { colW: [3.0, 3.2, W - 2 * MX - 6.2], minutes: i === 0 ? sec.minutes : 0, fontSize: 12, rowH: 1.05, per: 4 });
        });
        return;
      }
      // Lesson notes: vocabulary, key idea / watch out, then worked examples (one per slide, each followed by its solution)
      var voc = P.vocab(d);
      if (voc.length) {
        var s = content('Key vocabulary', sec, sec.minutes), cols = voc.length > 4 ? 3 : 2, rows = Math.ceil(voc.length / cols), gp = 0.3;
        var cw2 = (W - 2 * MX - (cols - 1) * gp) / cols, ch2 = Math.min(2.4, (BOTTOM - TOP - (rows - 1) * gp) / rows);
        voc.forEach(function (v, i) {
          var x = MX + (i % cols) * (cw2 + gp), y = TOP + Math.floor(i / cols) * (ch2 + gp);
          s.addShape(pres.ShapeType.roundRect, { x: x, y: y, w: cw2, h: ch2, rectRadius: 0.12, fill: { color: SOFT }, line: { color: SOFT }, objectName: 'Vocabulary card' });
          s.addText(v, { x: x + 0.25, y: y + 0.15, w: cw2 - 0.5, h: 0.55, fontFace: HEAD, fontSize: 22, bold: true, color: INK, margin: 0, fit: 'shrink', isTextBox: true });
          var def = P.define ? P.define(v, d) : '';
          s.addText(def || 'means…', { x: x + 0.25, y: y + 0.72, w: cw2 - 0.5, h: ch2 - 0.85, fontFace: BODY, fontSize: fitSize(def, cw2 - 0.5, ch2 - 0.85, 16, 11), italic: !def, color: def ? INK : INK2, valign: 'top', margin: 0, isTextBox: true, objectName: 'Definition' });
        });
        notes(s, teacherNotes(sec).concat(['Notes style: ' + (d.notes_style || ''), plan.notesMode === 'filled' ? 'Student notes are pre-filled: read the definitions together and add an example.' : 'Students copy each meaning and an example into their notes.']));
      }
      var paras = [], idea = P.keyIdea ? P.keyIdea(d.lesson_id) : '';
      if (idea) paras.push({ text: idea, size: 26, bold: true });
      if (d.sentence_frame) paras.push({ text: 'Say it: ' + frameText(d.sentence_frame), size: 26 });
      if (P.watchOut(d)) paras.push({ text: 'Watch out: ' + P.watchOut(d), size: 24, color: 'A33A1D' });
      if (P.myNotes(d)) P.myNotes(d).split(/\n+/).filter(Boolean).forEach(function (line) { paras.push({ text: line, size: 22, bullet: true }); });
      if (paras.length) textSlide(sec, 'Key idea', paras, { notes: ['Model the sentence frame aloud before Example 1.'] });
    }
    async function exampleSlides(sec) {
      var ex = [];
      sec.groups.forEach(function (g) { g.items.forEach(function (p) { ex.push(p); }); });
      for (var i = 0; i < ex.length; i++) {
        var p = ex[i], t = 'Example ' + (i + 1) + (p.teacherLabel ? ' · ' + p.teacherLabel : '');
        await problemSlides(sec, t, [p], { onePer: true, steps: true, labels: function () { return String(i + 1); } });
      }
    }
    return pres;
  };

  /* ---------- browser: figures → PNG, then download ---------- */
  function svgToPng(svg) {
    return new Promise(function (resolve) {
      var vb = /viewBox="([\d.\s-]+)"/.exec(svg), dims = vb ? vb[1].trim().split(/\s+/).map(Number) : [0, 0, 400, 300];
      var w = dims[2], h = dims[3], scale = 3;
      var src = svg.replace(/<svg([^>]*?) width="[^"]*"/, '<svg$1').replace('<svg', '<svg width="' + w * scale + '" height="' + h * scale + '"');
      if (!/xmlns=/.test(src)) src = src.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
      var im = new G.Image();
      im.onload = function () {
        var c = G.document.createElement('canvas'); c.width = w * scale; c.height = h * scale;
        var ctx = c.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height); ctx.drawImage(im, 0, 0, c.width, c.height);
        resolve({ data: c.toDataURL('image/png'), w: w, h: h, alt: (/aria-label="([^"]*)"/.exec(svg) || [])[1] || 'figure' });
      };
      im.onerror = function () { resolve(null); };
      im.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(src);
    });
  }
  P.figToPng = function (spec) {
    var html = G.MKMENU.figHtml(spec), m = /<svg[\s\S]*<\/svg>/.exec(html);
    return m ? svgToPng(m[0]) : Promise.resolve(null);
  };
  function loadLib() {
    if (G.PptxGenJS) return Promise.resolve(G.PptxGenJS);
    return new Promise(function (resolve, reject) {
      var s = G.document.createElement('script'); s.src = 'vendor/pptxgenjs/pptxgen.bundle.js';
      s.onload = function () { resolve(G.PptxGenJS); }; s.onerror = function () { reject(new Error('Could not load the PowerPoint library.')); };
      G.document.head.appendChild(s);
    });
  }
  P.deckFileName = function (plan, audience) {
    var d = plan.day, slug = d.title.replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50);
    return 'Algebra1-Day' + (d.day < 10 ? '00' : d.day < 100 ? '0' : '') + d.day + '-' + slug + '-' + G.MKMENU.LEVELS[plan.level].name + '-' + (audience === 'student' ? 'Student' : 'Teacher') + '.pptx';
  };
  P.exportPptx = async function (plan, audience) {
    audience = audience === 'student' ? 'student' : 'teacher';
    var Lib = await loadLib();
    var pres = await P.buildDeck(plan, Lib, { figImage: P.figToPng, audience: audience });
    return pres.writeFile({ fileName: P.deckFileName(plan, audience) });
  };
})(typeof window !== 'undefined' ? window : globalThis);
