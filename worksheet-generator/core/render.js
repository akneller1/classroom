/* Rendering: TeX -> KaTeX, worksheet and answer-key blocks, and measured pagination onto
   US-Letter pages (nothing is ever split across a page break). */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var doc = G.document;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function math(markup) {
    return String(markup).replace(/⟨([^⟩]*)⟩/g, function (m, tex) {
      try { return G.katex.renderToString(tex.replace(/\\frac/g, '\\dfrac'), { throwOnError: false, output: 'html' }); }
      catch (e) { return esc(tex); }
    });
  }
  function figHtml(spec, widthIn) { return NS.graph(spec, { widthIn: widthIn }); }
  function fillFigs(html, p, widthIn) {
    return html.replace(/\[\[fig:(\d+)\]\]/g, function (m, i) { return '<div class="fig inline">' + figHtml(p.figs[+i], widthIn) + '</div>'; });
  }
  function el(tag, cls, html) { var e = doc.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }
  function isBlank(spec) { return spec && !(spec.lines && spec.lines.length) && !(spec.points && spec.points.length); }

  var SPACE_EXTRA = [0, 0.12, 0.42];     // extra room (in) under a figure row, by workspace setting

  /* ---------- student worksheet ---------- */
  function studentBlock(p, L, num, si, pi, settings) {
    var sIdx = NS.spaceIndex(settings.space);
    var fw = L.figWidth || 2.6;
    var layout = L.layout;
    var hasRightFig = p.fig && p.figWhere === 'right';
    var b = el('div', 'prob ' + (hasRightFig ? 'row' : layout === 'full' ? 'full' : 'half'));
    b.setAttribute('data-s', si); b.setAttribute('data-p', pi);
    b.appendChild(el('div', 'num', num + '.'));
    var body = el('div', 'pbody');
    body.appendChild(el('div', 'q', fillFigs(math(p.prompt), p, p.figs ? fw : fw)));
    if (p.fig && p.figWhere === 'below') body.appendChild(el('div', 'fig below', figHtml(p.fig, fw)));
    if (!hasRightFig) {
      var space = (p.space || L.space)[sIdx];
      if (space > 0) { var w = el('div', 'work'); w.style.height = space + 'in'; body.appendChild(w); }
    }
    b.appendChild(body);
    if (hasRightFig) {
      var f = el('div', 'fig right', figHtml(p.fig, fw));
      f.style.marginBottom = SPACE_EXTRA[sIdx] + 'in';
      b.appendChild(f);
    }
    var btn = el('button', 'regen no-print', '↻');
    btn.type = 'button'; btn.title = 'Replace just this problem with a new one'; btn.setAttribute('aria-label', 'Regenerate problem ' + num);
    b.appendChild(btn);
    return b;
  }

  function sectionHead(L, unit, first, catChanged) {
    var cat = unit.categories.filter(function (c) { return c.lessons.indexOf(L.id) >= 0; })[0];
    var h = el('div', 'sec');
    var html = '';
    if (catChanged && cat) html += '<div class="catbar">' + esc(cat.letter) + ' · ' + esc(cat.name) + '</div>';
    html += '<div class="sec-title"><span class="pill">Skill ' + L.num + '</span> ' + esc(L.title) + '</div>' +
      '<div class="sec-ins">' + esc(L.instruction) + '</div>';
    h.innerHTML = html;
    return h;
  }

  function docHeader(settings, unit, ver, kind) {
    var title = (settings.title && settings.title.trim()) || unit.defaultTitle;
    var h = el('div', 'ws-head');
    var right = (settings.versions > 1 ? '<span class="vtag">Version ' + ver.label + '</span>' : '');
    if (kind === 'key') {
      h.innerHTML = '<div class="ws-title-row"><div class="ws-title">' + esc(title) + '</div>' +
        '<div class="ws-right"><span class="vtag keytag">Answer Key' + (settings.versions > 1 ? ' · Version ' + ver.label : '') + '</span></div></div>' +
        '<div class="ws-sub">Teacher copy · ' + (settings.keyMode === 'worked' ? 'worked solutions' : 'final answers') + '</div>';
    } else {
      h.innerHTML = '<div class="ws-title-row"><div class="ws-title">' + esc(title) + '</div><div class="ws-right">' + right + '</div></div>' +
        (settings.showNameDate ? '<div class="ws-name"><span>Name <i class="ln long"></i></span><span>Date <i class="ln mid"></i></span><span>Period <i class="ln short"></i></span></div>' : '');
    }
    return h;
  }

  function studentUnits(ver, settings, unit) {
    var units = [{ el: docHeader(settings, unit, ver, 'student'), keep: true, head: true }];
    var n = 0, lastCat = null;
    ver.sections.forEach(function (sec, si) {
      var L = NS.registry.lessons[sec.lessonId];
      units.push({ el: sectionHead(L, unit, si === 0, L.category !== lastCat), keep: true });
      lastCat = L.category;
      if (L.layout === 'half') {
        for (var i = 0; i < sec.problems.length; i += 2) {
          var row = el('div', 'rowpair');
          for (var j = i; j < Math.min(i + 2, sec.problems.length); j++) row.appendChild(studentBlock(sec.problems[j], L, n + j + 1, si, j, settings));
          units.push({ el: row });
        }
      } else {
        sec.problems.forEach(function (p, pi) { units.push({ el: studentBlock(p, L, n + pi + 1, si, pi, settings) }); });
      }
      n += sec.problems.length;
    });
    return units;
  }

  /* ---------- answer key ---------- */
  function keyBlock(p, L, num, si, pi, settings) {
    var worked = settings.keyMode === 'worked';
    var b = el('div', 'kprob');
    b.setAttribute('data-s', si); b.setAttribute('data-p', pi);
    var qhtml = fillFigs(math(p.keyPrompt || p.prompt), p, 1.55);
    var fig = p.answerFig || (p.fig && !isBlank(p.fig) ? p.fig : null);
    var figW = worked ? 1.9 : 1.55;
    var body = el('div', 'kbody');
    body.appendChild(el('div', 'kq', qhtml));
    body.appendChild(el('div', 'ka', '<b class="alabel">Answer:</b> ' + math(p.answer)));
    if (worked && p.steps && p.steps.length) {
      var ol = el('ol', 'ksteps');
      p.steps.forEach(function (s) { ol.appendChild(el('li', '', math(s))); });
      body.appendChild(ol);
    }
    b.appendChild(el('div', 'num', num + '.'));
    b.appendChild(body);
    if (fig) {
      var kf = el('div', 'fig kfig', figHtml(fig, figW));
      b.appendChild(kf);
      b.classList.add('hasfig');
    }
    return b;
  }

  function keyUnits(ver, settings, unit) {
    var units = [{ el: docHeader(settings, unit, ver, 'key'), keep: true, head: true }];
    var n = 0, worked = settings.keyMode === 'worked';
    ver.sections.forEach(function (sec, si) {
      var L = NS.registry.lessons[sec.lessonId];
      var h = el('div', 'sec ksec', '<div class="sec-title"><span class="pill">Skill ' + L.num + '</span> ' + esc(L.title) + '</div>');
      units.push({ el: h, keep: true });
      var blocks = sec.problems.map(function (p, pi) { return keyBlock(p, L, n + pi + 1, si, pi, settings); });
      if (!worked) {                                   // final answers: pair short entries two to a row
        for (var i = 0; i < blocks.length;) {
          var a = blocks[i], c = blocks[i + 1];
          var wide = function (e) { return e.classList.contains('hasfig') || e.querySelector('svg,table,.panels'); };
          if (c && !wide(a) && !wide(c)) {
            var row = el('div', 'rowpair kpair'); row.appendChild(a); row.appendChild(c); units.push({ el: row }); i += 2;
          } else { units.push({ el: a }); i += 1; }
        }
      } else blocks.forEach(function (bk) { units.push({ el: bk }); });
      n += sec.problems.length;
    });
    return units;
  }

  /* ---------- pagination ---------- */
  function makePage(unitName, ver, settings, kind) {
    var pg = el('section', 'page');
    pg.innerHTML = '<div class="pg-run"></div><div class="pg-body"></div><div class="pg-foot"><span class="pf-l"></span><span class="pf-r"></span></div>';
    return pg;
  }

  /* Lays the units onto fixed Letter pages. Each group of units is placed into the real page body
     and kept only if it actually fits, so the layout can never disagree with what prints. */
  function paginate(units, info) {
    var stage = el('div', 'measure-stage');
    doc.body.appendChild(stage);
    // first pass: lay everything out once so web fonts start loading, then wait for them
    var warm = makePage(); stage.appendChild(warm);
    var wb = warm.querySelector('.pg-body'); wb.style.height = 'auto'; wb.style.overflow = 'visible';
    units.forEach(function (u) { wb.appendChild(u.el); });
    void wb.offsetHeight;
    var ready = (G.document.fonts && G.document.fonts.ready) ? G.document.fonts.ready : Promise.resolve();
    return ready.then(function () {
      void wb.offsetHeight;
      stage.removeChild(warm);
      var groups = [], cur = null;
      units.forEach(function (u) {
        if (!cur) cur = { items: [] };
        cur.items.push(u);
        if (!u.keep) { groups.push(cur); cur = null; }
      });
      if (cur) groups.push(cur);
      var pages = [], body = null;
      function newPage() {
        var pg = makePage();
        if (!pages.length) pg.classList.add('first');
        pages.push(pg); stage.appendChild(pg);
        body = pg.querySelector('.pg-body');
      }
      function fits() { return body.scrollHeight <= body.clientHeight; }
      newPage();
      groups.forEach(function (g) {
        g.items.forEach(function (u) { body.appendChild(u.el); });
        if (!fits() && body.children.length > g.items.length) {   // does not fit: move the group to a fresh page
          newPage();
          g.items.forEach(function (u) { body.appendChild(u.el); });
        }
      });
      pages.forEach(function (pg) { stage.removeChild(pg); });
      doc.body.removeChild(stage);
      var total = pages.length;
      pages.forEach(function (pg, i) {
        pg.querySelector('.pf-l').textContent = info.footer;
        pg.querySelector('.pf-r').textContent = 'Page ' + (i + 1) + ' of ' + total;
        if (i > 0) pg.querySelector('.pg-run').innerHTML = '<span>' + esc(info.runLeft) + '</span><span>' + esc(info.runRight) + '</span>';
      });
      return pages;
    });
  }

  NS.render = { esc: esc, math: math, studentUnits: studentUnits, keyUnits: keyUnits, paginate: paginate, figHtml: figHtml };
})(typeof window !== 'undefined' ? window : globalThis);
