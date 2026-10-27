/* Menu Assessment Generator — print rendering.

   Builds US-Letter pages for
     • the student menu (cover + order form, menu sections, optional work pages, optional reference page)
     • the teacher key (optional teacher guide, then every OFFERED dish with answer, worked solution
       and a partial-credit rubric)
   Blocks are measured in the real browser layout and packed onto pages, so a dish, a figure or a
   math expression is never split across a page break. Student pages are built only from the
   student-facing fields (prompt, parts' prompts), never from answers or steps.

   Reuses KaTeX rendering from core/render.js (MKWS.render.math) and core/graph.js for blank
   coordinate planes. */
(function (G) {
  'use strict';
  var WS = G.MKWS, NS = (G.MKMENU = G.MKMENU || {}), doc = G.document;
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function math(m) { return WS.render.math(m); }                       // trusted markup (reference page)
  /* Untrusted text (teacher edits, loaded files): escape everything outside ⟨…⟩; KaTeX renders the math safely. */
  function mathSafe(m) { return String(m === undefined || m === null ? '' : m).split(/(⟨[^⟩]*⟩)/).map(function (part) { return /^⟨/.test(part) ? WS.render.math(part) : esc(part); }).join(''); }
  NS.mathSafe = mathSafe;
  function el(tag, cls, html) { var e = doc.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }

  var DENS = { compact: 0, standard: 1, spacious: 2 };

  /* ---------- labels ---------- */
  NS.sectionLetter = function (cfg, si) {
    var used = {}, out = [];
    cfg.sections.forEach(function (s, i) {
      var base = (s.name || 'S').replace(/[^A-Za-z]/g, '').toUpperCase() || 'S', L = base[0], k = 1;
      if (/^CHEF/.test(base)) L = 'S';
      while (used[L] && k < base.length) { L = base[0] + base[k]; k++; }
      if (used[L]) L = L + (i + 1);
      used[L] = 1; out.push(L);
    });
    return out[si];
  };
  function dishLabel(cfg, si, i) {
    if (NS.isTest(cfg)) { var n = i + 1; for (var k = 0; k < si; k++) n += cfg.sections[k].offered | 0; return String(n); }   // a test numbers its questions straight through
    return NS.sectionLetter(cfg, si) + (i + 1);
  }
  NS.dishLabel = dishLabel;
  function ptsText(n) { n = Math.round(n * 100) / 100; return n + (n === 1 ? ' pt' : ' pts'); }
  function plural(n, one, many) { return n + ' ' + (n === 1 ? one : many); }

  /* ---------- rubric ---------- */
  /* Split a dish's points across its worked-solution steps (by weight), in whole or half points. */
  NS.rubric = function (p, points) {
    var steps = (p.steps || []).filter(function (s) { return (s.w || 0) > 0; });
    if (!steps.length) return [{ pts: points, text: 'Correct answer with supporting work.' }];
    var unit = Number.isInteger(points) ? 1 : 0.5, units = Math.round(points / unit);
    var W = steps.reduce(function (s, x) { return s + x.w; }, 0);
    var raw = steps.map(function (s) { return units * s.w / W; }), base = raw.map(Math.floor), left = units - base.reduce(function (a, b) { return a + b; }, 0);
    raw.map(function (r, i) { return [r - Math.floor(r), i]; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, left).forEach(function (x) { base[x[1]]++; });
    var lines = [], carry = '';
    steps.forEach(function (s, i) {
      var txt = (s.t || '') + (s.m ? ' ' + '⟨' + s.m + '⟩' : '');
      if (base[i] === 0) { carry += (carry ? ' ' : '') + txt; return; }
      lines.push({ pts: base[i] * unit, text: (carry ? carry + ' ' : '') + txt }); carry = '';
    });
    if (carry && lines.length) lines[lines.length - 1].text += ' ' + carry;
    return lines;
  };

  /* ---------- student pieces ---------- */
  function nameLines(cfg) {
    return '<div class="mm-name"><span>Name <i class="ln long"></i></span><span>Class / period <i class="ln mid"></i></span><span>Date <i class="ln mid"></i></span></div>';
  }
  function verTag(state, vIdx, kind) {
    var v = state.versions.length > 1 ? 'Version ' + state.versions[vIdx].label : '';
    if (kind === 'key') return '<span class="mm-vtag mm-keytag">Teacher key' + (v ? ' · ' + v : '') + '</span>';
    return v ? '<span class="mm-vtag">' + v + '</span>' : '';
  }
  function directions(state, vIdx, rules) {
    var cfg = state.config, ver = state.versions[vIdx], li = [];
    var parts = cfg.sections.map(function (s) { return '<b>' + s.required + ' ' + esc(s.name) + '</b> (' + ptsText(+s.points) + ' each)'; });
    var last = parts.length > 1 ? parts.slice(0, -1).join(', ') + ' and ' + parts[parts.length - 1] : parts[0];
    li.push('Order ' + last + '. The most you can earn is <b>' + rules.maxScore + ' points</b>.');
    var forced = [];
    ver.sections.forEach(function (s, si) { s.items.forEach(function (it, i) { if (it.required) forced.push(dishLabel(cfg, si, i)); }); });
    if (forced.length) li.push('Everyone must complete ' + (forced.length === 1 ? 'dish ' : 'dishes ') + '<b>' + forced.join(', ') + '</b>. ' + (forced.length === 1 ? 'It counts' : 'They count') + ' toward the number you order from ' + (forced.length === 1 ? 'its' : 'their') + ' section.');
    var tags = rules.tags;
    if (tags.length) li.push('Your ' + rules.totalRequired + ' dishes must include <b>at least one of each skill</b>: ' + tags.map(function (t) { return '<span class="mm-chip">' + esc(t) + '</span>'; }).join(' ') + ' (the label next to each dish).');
    li.push('Mark your choices on the order form below <b>and</b> on the dishes themselves (“My pick”). Only marked dishes are graded.');
    li.push(cfg.layout.format === 'menu-only' ? 'Show your work on the work pages. Write the dish number at the top of each box.' : 'Show your work in the space for each dish. Points are given for correct steps as well as correct answers.');
    li.push('Look at every page before you choose!');
    return '<div class="mm-box mm-dirs"><h3>How to order</h3><ol>' + li.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ol></div>';
  }
  function orderForm(state, vIdx) {
    var cfg = state.config, ver = state.versions[vIdx];
    var cols = cfg.sections.map(function (s, si) {
      return '<div class="mm-of-col"><div class="mm-of-h">' + esc(s.name) + '</div><div class="mm-of-sub">' + ptsText(+s.points) + ' each · choose ' + s.required + '</div>' +
        ver.sections[si].items.map(function (it, i) {
          return '<div class="mm-of-row"><span class="mm-box-chk"></span><b>' + dishLabel(cfg, si, i) + '</b>' + (it.tag ? '<span class="mm-chip">' + esc(it.tag) + '</span>' : '') + (it.required ? '<span class="mm-req">must do</span>' : '') + '</div>';
        }).join('') + '</div>';
    }).join('');
    return '<div class="mm-of" style="grid-template-columns:repeat(' + Math.min(cfg.sections.length, 4) + ',1fr)">' + cols + '</div>';
  }
  function scoreTable(state, rules) {
    var cfg = state.config;
    return '<table class="mm-tbl mm-score"><thead><tr><th>Course</th><th>Dishes</th><th>Points each</th><th>Possible</th><th>Score (teacher)</th></tr></thead><tbody>' +
      cfg.sections.map(function (s) { return '<tr><td>' + esc(s.name) + '</td><td>' + s.required + '</td><td>' + (+s.points) + '</td><td>' + (s.required * s.points) + '</td><td></td></tr>'; }).join('') +
      '<tr class="mm-tot"><td>Total</td><td>' + rules.totalRequired + '</td><td></td><td>' + rules.maxScore + '</td><td></td></tr></tbody></table>';
  }
  function skillCheck(rules) {
    if (!rules.tags.length) return '';
    return '<div class="mm-box mm-skillchk"><b>My skill check</b> (circle each skill you have covered): ' + rules.tags.map(esc).join(' · ') + '</div>';
  }
  function proofLayout(p) {
    var isShared = p.fig && p.fig.case === 'shared';
    var flow = /-flow-/.test(p.variant || '');
    var first = isShared ? 'AB is congruent to AB' : 'Angle AOB is congruent to angle COD';
    var second = isShared ? 'Triangle ABC is congruent to triangle ABD' : 'Triangle AOB is congruent to triangle COD';
    var rows = [first,second,'Corresponding angles are congruent','Solve the printed equation for x'];
    var blanks = ['Reason: __________________','Reason: __________________','Reason: __________________','x = __________'];
    if (flow) return '<div class="mm-proof-flow" style="display:flex;flex-direction:column;align-items:center;gap:7px;margin:12px 0;break-inside:avoid">' +
      rows.map(function (st,i) { return '<div style="width:94%;border:1.5px solid #222;border-radius:5px;padding:9px 12px;background:white;box-sizing:border-box"><b>Step '+(i+1)+':</b> '+esc(st)+'<div style="border-top:1px solid #aaa;margin-top:7px;padding-top:6px">'+blanks[i]+'</div></div>'+(i<3?'<div style="font-size:19px;line-height:15px">↓</div>':''); }).join('')+'</div>';
    return '<table class="mm-proof-table" style="width:100%;border-collapse:collapse;margin:12px 0;break-inside:avoid"><thead><tr><th style="border:1px solid #333;text-align:left;padding:8px;background:#eee;width:54%">Statements</th><th style="border:1px solid #333;text-align:left;padding:8px;background:#eee">Reasons</th></tr></thead><tbody>'+
      rows.map(function (st,i) { return '<tr><td style="border:1px solid #555;padding:10px 8px;vertical-align:top">'+(i+1)+'. '+esc(st)+'</td><td style="border:1px solid #555;padding:10px 8px;vertical-align:top">'+blanks[i]+'</td></tr>'; }).join('')+'</tbody></table>';
  }
  function promptHtml(p, forKey) {
    var h = '<div class="mm-q">' + mathSafe(p.prompt || '') + '</div>';
    if (p.work && p.work.length) h += '<ol class="mm-work-lines">' + p.work.map(function (w, i) { return '<li><span>Line ' + (i + 1) + ':</span> ' + mathSafe('⟨' + w + '⟩') + '</li>'; }).join('') + '</ol>';
    if (p.fig && NS.figHtml && !(forKey && Array.isArray(p.fig.pieces) && !p.fig.pieces.length)) h += NS.figHtml(p.fig);   // the key skips blank student number lines; tables and graphs stay
    if (/^geo-structured-proof-/.test(p.variant || '')) return h + proofLayout(p);
    var parts = (p.parts || []).filter(function (pt) { return pt.prompt; });
    if (parts.length) h += '<div class="mm-parts">' + parts.map(function (pt) { return '<div><b>' + (pt.label ? '(' + esc(pt.label) + ')' : '') + '</b> ' + mathSafe(pt.prompt) + '</div>'; }).join('') + '</div>';
    return h;
  }
  function isWide(p) {
    var txt = WS.render ? (p.prompt || '').replace(/⟨[^⟩]*⟩/g, 'xxxxxxxxxx') : '';
    var parts = (p.parts || []).filter(function (pt) { return pt.prompt; }).length;
    return parts > 0 || txt.length > 150;
  }
  function workspace(p, cfg) {
    var d = DENS[cfg.layout.density]; if (d === undefined) d = 1;
    if (cfg.layout.format === 'menu-only') return '';
    var h = (p.space || [1, 1.3, 1.6])[d];
    var grid = cfg.layout.grid;
    var inner = grid === 'coordinate' ? '<div class="mm-plane">' + WS.graph({ xmin: -8, xmax: 8, ymin: -8, ymax: 8, lines: [], points: [] }, { widthIn: 1.9 }) + '</div>' : '';
    if (grid === 'coordinate') h = Math.max(h, 2.15);
    return '<div class="mm-work' + (grid === 'graph' ? ' mm-graph' : '') + '" style="height:' + h.toFixed(2) + 'in">' + inner + '</div>';
  }
  function dishHtml(p, cfg, si, i, sec) {
    var lab = dishLabel(cfg, si, i);
    if (p.failed) return '<div class="mm-dish mm-missing"><div class="mm-dh"><b>' + lab + '</b></div><div class="mm-q">[No verified problem — fix this in the editor before printing.]</div></div>';
    return '<div class="mm-dish' + (isWide(p) ? ' wide' : '') + '" data-uid="' + esc(p.uid) + '"><div class="mm-dh"><span><b>' + lab + '</b>' + (p.tag ? '<span class="mm-chip">' + esc(p.tag) + '</span>' : '') +
      (p.required ? '<span class="mm-req">everyone must do</span>' : '') + '</span><span class="mm-pick"><span class="mm-box-chk"></span>My pick · ' + ptsText(+sec.points) + '</span></div>' +
      promptHtml(p) + workspace(p, cfg) + '</div>';
  }

  /* ---------- standard test ---------- */
  var LET = 'ABCDEFGH';
  function choicesHtml(p) {
    var txt = p.mc.opts.map(function (o) { return o.replace(/⟨[^⟩]*⟩/g, 'xxxxxx'); }), long = txt.some(function (t) { return t.length > 34; });
    return '<ol class="mm-choices' + (long ? ' one' : '') + '">' + p.mc.opts.map(function (o, k) { return '<li><span class="mm-bubble">' + LET[k] + '</span><span>' + mathSafe(o) + '</span></li>'; }).join('') + '</ol>';
  }
  NS.choicesHtml = choicesHtml;
  function multiHtml(p) { return '<div class="mm-multidir">' + esc(p.multi.direction || 'Select all values that satisfy the inequality.') + '</div><ol class="mm-choices one">' + p.multi.opts.map(function (o, k) { return '<li><span style="display:inline-flex;align-items:center;gap:7px;margin-right:9px;white-space:nowrap;"><span style="display:inline-block;width:15px;height:15px;border:1.5px solid currentColor;border-radius:2px;box-sizing:border-box;"></span><b>' + LET[k] + '</b></span><span>' + mathSafe(o) + '</span></li>'; }).join('') + '</ol>'; }
  function testDirections(state, rules) {
    var cfg = state.config, nQ = cfg.sections.reduce(function (n, s) { return n + (s.offered | 0); }, 0);
    var ws = NS.isWorksheet(cfg);
    var li = [ws ? 'Answer <b>all ' + nQ + ' questions</b>.' : 'Answer <b>all ' + nQ + ' questions</b>. The test is worth <b>' + rules.maxScore + ' points</b>.'];
    cfg.sections.forEach(function (s, si) {
      var fmt = NS.sectionFormat(cfg, si), fm = fmt === 'mc' ? 'circle the letter of the best answer' : fmt === 'multi' ? 'select every value that satisfies the inequality' : fmt === 'mcas' ? 'answer every part and explain your reasoning' : ws ? 'show your work' : 'show your work; points are given for correct steps as well as the answer';
      li.push('<b>Part ' + (si + 1) + ' · ' + esc(s.name) + '</b>' + (ws ? '' : ' (' + ptsText(+s.points) + ' each)') + ': ' + fm + '.');
    });
    return '<div class="mm-box mm-dirs"><h3>Directions</h3><ol>' + li.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ol></div>';
  }
  function testScoreTable(state, rules) {
    var cfg = state.config;
    return '<table class="mm-tbl mm-score"><thead><tr><th>Part</th><th>Questions</th><th>Points each</th><th>Possible</th><th>Score (teacher)</th></tr></thead><tbody>' +
      cfg.sections.map(function (s, si) { return '<tr><td>' + (si + 1) + ' · ' + esc(s.name) + '</td><td>' + s.offered + '</td><td>' + (+s.points) + '</td><td>' + (s.offered * s.points) + '</td><td></td></tr>'; }).join('') +
      '<tr class="mm-tot"><td>Total</td><td>' + rules.totalOffered + '</td><td></td><td>' + rules.maxScore + '</td><td></td></tr></tbody></table>';
  }
  function testQHtml(p, cfg, si, i, sec) {
    var lab = dishLabel(cfg, si, i);
    if (p.failed) return '<div class="mm-dish mm-missing"><div class="mm-dh"><b>' + lab + '.</b></div><div class="mm-q">[No verified problem — fix this in the editor before printing.]</div></div>';
    var fmt = NS.sectionFormat(cfg, si), mc = fmt === 'mc' && p.mc, multi = fmt === 'multi' && p.multi, mcas = fmt === 'mcas';
    if ((fmt === 'multi' && (!multi || !Array.isArray(p.multi.keys) || p.multi.keys.length < 2)) || (mcas && p.mcasFail)) {
      return '<div class="mm-dish mm-missing"><div class="mm-q">[No valid question for this format. Regenerate or select another skill before printing.]</div></div>';
    }
    var space = mc || multi ? '<div class="mm-work mm-scratch" style="height:' + (((p.space || [1])[0]) * 0.45).toFixed(2) + 'in"></div>' : workspace(p, { layout: { format: 'together', density: mcas ? 'spacious' : cfg.layout.density, grid: cfg.layout.grid } });
    return '<div class="mm-dish mm-tq' + (mcas || multi || isWide(p) || (mc && /one/.test(choicesHtml(p).slice(0, 30))) ? ' wide' : '') + '" data-uid="' + esc(p.uid) + '"><div class="mm-dh"><span><b>' + lab + '.</b></span>' + (NS.isWorksheet(cfg) ? '' : '<span class="mm-pts">' + ptsText(+sec.points) + '</span>') + '</div>' +
      promptHtml(p) + (mc ? choicesHtml(p) : multi ? multiHtml(p) : '') + (fmt === 'multi' && !multi ? '<p class="mm-flag bad">Cannot make verified choices: ' + esc(p.multiFail || 'Try another skill') + '</p>' : '') + (mcas && p.mcasFail ? '<p class="mm-flag bad">Cannot make a verified multi-part problem: ' + esc(p.mcasFail) + '</p>' : '') + space + '</div>';
  }
  function testStudentBlocks(state, vIdx) {
    var cfg = state.config, ver = state.versions[vIdx], rules = NS.checkRules(cfg, state), B = [];
    B.push({ html: '<div class="mm-head"><div><div class="mm-title">' + esc(cfg.title) + '</div><div class="mm-sub">' + esc(cfg.subtitle || '') + '</div></div>' + verTag(state, vIdx, 'student') + '</div>' + nameLines(cfg) });
    var ws = NS.isWorksheet(cfg);
    B.push({ html: testDirections(state, rules) + (ws ? '' : testScoreTable(state, rules)) });
    cfg.sections.forEach(function (sec, si) {
      var items = ver.sections[si].items;
      var sub = ws ? esc(sec.note || (NS.sectionFormat(cfg, si) === 'mc' ? 'Choose the best answer.' : 'Show your work.')) : ptsText(+sec.points) + ' each' + (sec.note ? ' · ' + esc(sec.note) : '');
      var head = '<div class="mm-sechead"><div><div class="mm-sectitle">Part ' + (si + 1) + ' · ' + esc(sec.name) + '</div><div class="mm-secsub">' + sub + '</div></div></div>';
      B.push({ html: head, keep: true, sectionHead: si });
      var row = [];
      function flush() { if (row.length) { B.push({ cls: 'tight', html: '<div class="mm-row">' + row.join('') + (row.length === 1 ? '<div></div>' : '') + '</div>', sec: si }); row = []; } }
      items.forEach(function (it, i) {
        var h = testQHtml(it, cfg, si, i, sec);
        if (/mm-tq wide/.test(h)) { flush(); B.push({ cls: 'tight', html: h, sec: si }); }
        else { row.push(h); if (row.length === 2) flush(); }
      });
      flush();
    });
    if (cfg.layout.reference) {
      var set = NS.skillSets[cfg.unitId];
      B.push({ html: '<div class="mm-sechead"><div><div class="mm-sectitle">Reference page</div><div class="mm-secsub">' + esc(set.unitName) + '</div></div></div>', keep: true, page: 'new' });
      B.push({ html: '<div class="mm-ref">' + math(set.reference || '') + '</div>' });
    }
    return B;
  }

  /* Blocks for one version of the student document. Each block: {html, cls, page:'new'?, keep:true?} */
  function studentBlocks(state, vIdx) {
    if (NS.isTest(state.config)) return testStudentBlocks(state, vIdx);
    var cfg = state.config, ver = state.versions[vIdx], rules = NS.checkRules(cfg, state), B = [];
    B.push({ html: '<div class="mm-head"><div><div class="mm-title">' + esc(cfg.title) + '</div><div class="mm-sub">' + esc(cfg.subtitle || '') + '</div></div>' + verTag(state, vIdx, 'student') + '</div>' + nameLines(cfg) });
    B.push({ html: directions(state, vIdx, rules) });
    B.push({ html: orderForm(state, vIdx) });
    B.push({ html: skillCheck(rules) + scoreTable(state, rules) });
    cfg.sections.forEach(function (sec, si) {
      var items = ver.sections[si].items;
      var head = '<div class="mm-sechead"><div><div class="mm-sectitle">' + esc(sec.name) + '</div><div class="mm-secsub">' + ptsText(+sec.points) + ' each · choose ' + sec.required + (sec.note ? ' · ' + esc(sec.note) : '') + '</div></div><span>Name <i class="ln mid"></i></span></div>';
      B.push({ html: head, keep: true, page: si === 0 || cfg.layout.format !== 'menu-only' ? 'new' : null, sectionHead: si });
      // pair half-width dishes into rows
      var row = [];
      function flush() { if (row.length) { B.push({ cls: 'tight', html: '<div class="mm-row">' + row.join('') + (row.length === 1 ? '<div></div>' : '') + '</div>', sec: si }); row = []; } }
      items.forEach(function (it, i) {
        var h = dishHtml(it, cfg, si, i, sec);
        if (isWide(it)) { flush(); B.push({ cls: 'tight', html: h, sec: si }); }
        else { row.push(h); if (row.length === 2) flush(); }
      });
      flush();
    });
    if (cfg.layout.format === 'menu-only') {
      var n = rules.totalRequired;
      B.push({ html: '<div class="mm-sechead"><div><div class="mm-sectitle">Work pages</div><div class="mm-secsub">One box for each dish you ordered · write the dish number first</div></div><span>Name <i class="ln mid"></i></span></div>', keep: true, page: 'new' });
      var d = DENS[cfg.layout.density]; if (d === undefined) d = 1;
      for (var k = 0; k < n; k++) B.push({ html: '<div class="mm-workbox"><div class="mm-dh"><span>Dish <i class="ln short"></i></span><span>Points <i class="ln short"></i></span></div><div class="mm-work' + (cfg.layout.grid === 'graph' ? ' mm-graph' : '') + '" style="height:' + [2.1, 2.6, 3.2][d] + 'in"></div></div>' });
    }
    if (cfg.layout.reference) {
      var set = NS.skillSets[cfg.unitId];
      B.push({ html: '<div class="mm-sechead"><div><div class="mm-sectitle">Reference page</div><div class="mm-secsub">' + esc(set.unitName) + '</div></div></div>', keep: true, page: 'new' });
      B.push({ html: '<div class="mm-ref">' + math(set.reference || '') + '</div>' });
    }
    return B;
  }

  /* ---------- teacher key ---------- */
  function statusBadge(p) {
    if (p.failed) return '<span class="mm-flag bad">NO VERIFIED PROBLEM</span>';
    var s = p.verify && p.verify.status;
    if (s === 'verified') return p.edited ? '<span class="mm-flag ok">edited · re-verified</span>' : '';
    if (p.approved) return '<span class="mm-flag warn">teacher-entered answer · approved</span>';
    return '<span class="mm-flag bad">answer NOT verified</span>';
  }
  function keyRow(p, cfg, si, i, sec) {
    var lab = dishLabel(cfg, si, i);
    if (p.failed) return '<tr><td><b>' + lab + '</b></td><td colspan="3">' + statusBadge(p) + '</td></tr>';
    var fmt = NS.sectionFormat(cfg, si), mcOn = fmt === 'mc' && p.mc, multiOn = fmt === 'multi' && p.multi;
    var ans = multiOn ? '<b>' + p.multi.keys.map(function (k) { return 'ABCDEFGH'[k]; }).join(', ') + '</b> · ' + p.multi.keys.map(function (k) { return mathSafe(p.multi.opts[k]); }).join('; ') : mcOn ? '<b class="mm-letter">' + 'ABCDEFGH'[p.mc.key] + '</b> ' + mathSafe(p.parts[0].answer) + (p.mcNote ? '<div class="mm-flag warn">' + esc(p.mcNote) + '</div>' : '')
      : (p.parts || []).map(function (pt) { return (pt.label ? '(' + esc(pt.label) + ') ' : '') + mathSafe(pt.answer) + (pt.answerFig && NS.figHtml ? NS.figHtml(pt.answerFig) : ''); }).join('<br>');
    var steps = (p.steps || []).filter(function (s) { return s.t || (s.m && s.w > 0); }).map(function (s) { return '<li>' + mathSafe(s.t) + (s.m ? ' ' + mathSafe('⟨' + s.m + '⟩') : '') + '</li>'; }).join('');
    var mcasOn = fmt === 'mcas' && !p.mcasFail;
    var mcasParts = (p.parts || []).filter(function (pt) { return pt.prompt && pt.answer; });
    var mcasRub = mcasParts.map(function (pt, ix) { var per = +sec.points / mcasParts.length; return '<li><b>' + (pt.label ? '(' + esc(pt.label) + ')' : '(' + String.fromCharCode(97 + ix) + ')') + ' · ' + (Math.round(per * 100) / 100) + ' pts</b>: correct answer with supporting reasoning.</li>'; }).join('');
    var rub = mcasOn ? mcasRub : multiOn ? '<li><b>' + ptsText(+sec.points) + '</b>: select every correct statement and no incorrect statements.</li>' : mcOn ? '<li><b>' + ptsText(+sec.points) + '</b>: choice ' + 'ABCDEFGH'[p.mc.key] + '. No partial credit.</li>' : NS.rubric(p, +sec.points).map(function (r) { return '<li><b>' + ptsText(r.pts) + '</b>: ' + mathSafe(r.text) + '</li>'; }).join('');
    if (NS.sectionFormat(cfg, si) === 'mc' && !p.mc && !p.failed) rub = '<li><span class="mm-flag warn">Printed as short answer: ' + esc(p.mcFail || 'no choices') + '</span></li>' + rub;
    var ws = NS.isWorksheet(cfg), fallback = NS.sectionFormat(cfg, si) === 'mc' && !p.mc ? '<div class="mm-flag warn">Printed as short answer: ' + esc(p.mcFail || 'no choices') + '</div>' : '';
    return '<tr><td><b>' + lab + '</b><div class="mm-chip">' + esc(p.tag || '') + '</div>' + (p.required && !NS.isTest(cfg) ? '<div class="mm-req">must do</div>' : '') + '</td><td>' + promptHtml(p, true) + (mcOn ? choicesHtml(p) : multiOn ? multiHtml(p) : '') + statusBadge(p) + '</td>' +
      '<td><div class="mm-ans"><b>Answer:</b> ' + ans + '</div>' + (ws ? fallback : '') + (steps ? '<ol class="mm-steps">' + steps + '</ol>' : '') + '</td>' + (ws ? '' : '<td><ul class="mm-rub">' + rub + '</ul></td>') + '</tr>';
  }
  function guideBlocks(state, vIdx) {
    var cfg = state.config, ver = state.versions[vIdx], rules = NS.checkRules(cfg, state), set = NS.skillSets[cfg.unitId], B = [];
    B.push({ html: '<div class="mm-head"><div><div class="mm-title">Assessment Menu: Teacher Guide</div><div class="mm-sub">' + esc(cfg.title) + ' · ' + esc(NS.LEVELS[cfg.level].long) + ' · design notes, grading and answer key</div></div>' + verTag(state, vIdx, 'key') + '</div>' });
    var why = [];
    why.push('<b>Points are capped by section.</b> Students complete exactly ' + cfg.sections.map(function (s) { return s.required; }).join(' / ') + ' dishes, so they cannot fill the total with the easiest problems.');
    var top = cfg.sections.slice().sort(function (a, b) { return b.points - a.points; })[0];
    if (top && rules.maxScore) why.push('<b>' + esc(top.name) + ' carry ' + Math.round(100 * top.required * top.points / rules.maxScore) + '% of the grade.</b>');
    if (rules.tags.length) why.push('<b>Skill coverage rule.</b> The ' + rules.totalRequired + ' picks must include at least one dish from each skill group below.');
    why.push('<b>Harder dishes reward process.</b> Each rubric gives credit for correct steps, so a partly correct attempt at a harder dish can earn more than a perfect easy one in the same time.');
    B.push({ html: '<div class="mm-box"><h3>Why students cannot just pick the easy ones</h3><ol>' + why.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ol></div>' });
    var groups = {}; ver.sections.forEach(function (s, si) { s.items.forEach(function (it, i) { (groups[it.tag] = groups[it.tag] || []).push(dishLabel(cfg, si, i)); }); });
    B.push({ html: '<table class="mm-tbl"><thead><tr><th>Skill group</th><th>What it covers</th><th>Dishes</th></tr></thead><tbody>' + Object.keys(groups).map(function (t) {
      var names = set.skills.filter(function (s) { return s.tag === t; }).map(function (s) { return s.name; }).join('; ');
      return '<tr><td><b>' + esc(t) + '</b></td><td>' + esc((set.tags[t] || '') + (names ? ': ' + names : '')) + '</td><td>' + groups[t].join(', ') + '</td></tr>';
    }).join('') + '</tbody></table>' });
    var cum = 0, rows = cfg.sections.map(function (s, i) { cum += s.required * s.points; return '<tr><td>' + (i === 0 ? 'Only ' : '') + cfg.sections.slice(0, i + 1).map(function (x) { return esc(x.name); }).join(' + ') + '</td><td>' + cum + '</td></tr>'; }).join('');
    B.push({ html: '<table class="mm-tbl mm-narrow"><thead><tr><th>If a student only does…</th><th>Maximum</th></tr></thead><tbody>' + rows + '</tbody></table>' });
    B.push({ html: '<div class="mm-box"><h3>Grading and options</h3><ul><li>Grade only the marked dishes using the rubrics on the next pages (partial credit is built in). Total possible: <b>' + rules.maxScore + '</b>.</li><li>If a student marks more than the required number in a section, grade the first ones marked, or apply your own policy (for example, grade the dishes that score lowest).</li><li>Check the skill rule on the order form before totaling. If a skill group is missing, apply your own policy.</li><li>Problems marked <i>teacher-entered</i> were written or changed by hand; their answers were approved by you rather than computed.</li><li>The key is for this version only' + (state.versions.length > 1 ? ' (Version ' + ver.label + ')' : '') + '. Each version has its own key.</li></ul></div>' });
    B.push({ html: '<table class="mm-tbl mm-gradebook"><thead><tr><th>Student</th>' + cfg.sections.map(function (s) { return '<th>' + esc(s.name) + ' (of ' + s.required * s.points + ')</th>'; }).join('') + '<th>Skills OK?</th><th>Total</th></tr></thead><tbody>' +
      new Array(7).join('<tr><td></td>' + cfg.sections.map(function () { return '<td></td>'; }).join('') + '<td></td><td></td></tr>') + '</tbody></table>' });
    return B;
  }
  function testGuideBlocks(state, vIdx) {
    var cfg = state.config, ver = state.versions[vIdx], rules = NS.checkRules(cfg, state), set = NS.skillSets[cfg.unitId], B = [];
    B.push({ html: '<div class="mm-head"><div><div class="mm-title">' + esc(cfg.title) + ': ' + (NS.isWorksheet(cfg) ? 'Answer Key' : 'Teacher Key') + '</div><div class="mm-sub">' + esc(NS.LEVELS[cfg.level].long) + ' · ' + rules.totalOffered + ' questions' + (NS.isWorksheet(cfg) ? '' : ' · ' + rules.maxScore + ' points') + '</div></div>' + verTag(state, vIdx, 'key') + '</div>' });
    var quick = [];
    ver.sections.forEach(function (s, si) { s.items.forEach(function (it, i) { if (NS.sectionFormat(cfg, si) === 'mc' && it.mc) quick.push('<td><b>' + dishLabel(cfg, si, i) + '.</b> ' + 'ABCDEFGH'[it.mc.key] + '</td>'); else if (NS.sectionFormat(cfg, si) === 'multi' && it.multi) quick.push('<td><b>' + dishLabel(cfg, si, i) + '.</b> ' + it.multi.keys.map(function (k) { return 'ABCDEFGH'[k]; }).join(', ') + '</td>'); }); });
    if (quick.length) { var rows = []; for (var k = 0; k < quick.length; k += 10) rows.push('<tr>' + quick.slice(k, k + 10).join('') + '</tr>'); B.push({ html: '<div class="mm-box"><h3>Quick key: multiple choice</h3><table class="mm-tbl mm-quick"><tbody>' + rows.join('') + '</tbody></table></div>' }); }
    var groups = {}; ver.sections.forEach(function (s, si) { s.items.forEach(function (it, i) { (groups[it.tag] = groups[it.tag] || []).push(dishLabel(cfg, si, i)); }); });
    B.push({ html: '<table class="mm-tbl"><thead><tr><th>Skill group</th><th>What it covers</th><th>Questions</th></tr></thead><tbody>' + Object.keys(groups).map(function (t) {
      return '<tr><td><b>' + esc(t) + '</b></td><td>' + esc(set.tags[t] || '') + '</td><td>' + groups[t].join(', ') + '</td></tr>'; }).join('') + '</tbody></table>' });
    return B;
  }
  function keyBlocks(state, vIdx) {
    var cfg = state.config, ver = state.versions[vIdx], B = [], test = NS.isTest(cfg), ws = NS.isWorksheet(cfg);
    if (cfg.layout.guide !== false) B = test ? testGuideBlocks(state, vIdx) : guideBlocks(state, vIdx);
    cfg.sections.forEach(function (sec, si) {
      B.push({ html: '<div class="mm-head"><div><div class="mm-title mm-t2">Answer Key: ' + (test ? 'Part ' + (si + 1) + ' · ' : '') + esc(sec.name) + (ws ? '' : ' (' + ptsText(+sec.points) + ' each)') + '</div><div class="mm-sub">' + (ws ? 'Every question, with the answer and a worked solution.' : test ? 'Every question, with the answer and a worked solution' + (NS.sectionFormat(cfg, si) === 'mc' ? '.' : ' and a suggested partial-credit rubric.') : 'Every offered dish, with worked solutions and a suggested partial-credit rubric.') + '</div></div>' + verTag(state, vIdx, 'key') + '</div>', keep: true, page: ws || (si === 0 && cfg.layout.guide === false) ? null : (test && si > 0 ? null : 'new') });
      ver.sections[si].items.forEach(function (it, i) {
        var cols = ws ? '<colgroup><col style="width:.82in"><col style="width:2.6in"><col></colgroup>' : '<colgroup><col style="width:.82in"><col style="width:2.1in"><col><col style="width:2.05in"></colgroup>';
        B.push({ cls: 'tight', html: '<table class="mm-tbl mm-key">' + cols + (i === 0 ? '<thead><tr><th>' + (test ? 'Question' : 'Dish') + '</th><th>Problem</th><th>Answer and solution</th>' + (ws ? '' : '<th>Rubric</th>') + '</tr></thead>' : '') + '<tbody>' + keyRow(it, cfg, si, i, sec) + '</tbody></table>' });
      });
    });
    return B;
  }

  /* ---------- pagination ---------- */
  function newPage(state, vIdx, kind) {
    var cfg = state.config, pg = el('div', 'page mm-page' + (kind === 'key' ? ' mm-keypage' : ''));
    var foot = el('div', 'mm-foot');
    foot.innerHTML = '<span>' + esc(cfg.title) + (state.versions.length > 1 ? ' · Version ' + state.versions[vIdx].label : '') + (kind === 'key' ? ' · TEACHER KEY' : '') + '</span><span class="mm-pno"></span>';
    var body = el('div', 'mm-body');
    pg.appendChild(body); pg.appendChild(foot);
    return { page: pg, body: body };
  }
  /* Returns a Promise of an array of page elements. */
  NS.renderPages = function (state, vIdx, kind) {
    var blocks = kind === 'key' ? keyBlocks(state, vIdx) : studentBlocks(state, vIdx);
    var stage = el('div', 'measure-stage mm-stage'); doc.body.appendChild(stage);
    var pages = [], cur = null, overflow = [];
    function start() { cur = newPage(state, vIdx, kind); stage.appendChild(cur.page); pages.push(cur); }
    var ready = doc.fonts && doc.fonts.ready ? doc.fonts.ready : Promise.resolve();
    return ready.then(function () {
      start();
      var i = 0;
      while (i < blocks.length) {
        var b = blocks[i];
        if (b.page === 'new' && cur.body.childNodes.length) start();
        // keep a heading together with the next block
        var group = [b]; if (b.keep && blocks[i + 1]) group.push(blocks[i + 1]);
        var els = group.map(function (g) { var e = el('div', 'mm-blk' + (g.cls ? ' ' + g.cls : ''), g.html); if (kind === 'student' && NS.isWorksheet(state.config) && g.cls === 'tight' && cur.body.querySelector('.mm-blk.tight')) e.style.paddingTop = (Math.max(0, Math.min(10, +state.config.layout.spaceAdjust || 0)) * 6) + 'px'; cur.body.appendChild(e); return e; });
        if (cur.body.scrollHeight > cur.body.clientHeight + 1) {
          els.forEach(function (e) { cur.body.removeChild(e); });
          if (cur.body.childNodes.length) {
            start();
            // repeat the section heading on a continuation page
            if (b.sec !== undefined && !b.keep) {
              var sh = blocks.filter(function (x) { return x.sectionHead === b.sec; })[0];
              if (sh) { var hc = el('div', 'mm-blk mm-cont', sh.html.replace('</div><div class="mm-secsub">', ' <span class="mm-contd">(continued)</span></div><div class="mm-secsub">')); cur.body.appendChild(hc); }
            }
          }
          // A row moved to a new page must not inherit inter-row spacing.
          if (!cur.body.querySelector('.mm-blk.tight')) els.forEach(function (e) { if (e.classList.contains('tight')) e.style.paddingTop = ''; });
          els.forEach(function (e) { cur.body.appendChild(e); });
          if (cur.body.scrollHeight > cur.body.clientHeight + 1) overflow.push(i);
        }
        i += group.length;
      }
      pages.forEach(function (p, k) { p.page.querySelector('.mm-pno').textContent = 'Page ' + (k + 1) + ' of ' + pages.length; stage.removeChild(p.page); });
      doc.body.removeChild(stage);
      var out = pages.map(function (p) { return p.page; });
      out.overflow = overflow;
      return out;
    });
  };
})(typeof window !== 'undefined' ? window : globalThis);
