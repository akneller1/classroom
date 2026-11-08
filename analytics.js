/* Private visitor statistics for Mr. K's Classroom (Umami Cloud).

   Only the site owner sees the numbers: they live in the Umami dashboard behind your login
   (https://cloud.umami.is). Nothing is shown on the site itself.

   SETUP: paste the Website ID from Umami (Settings → Websites → Edit → Tracking code) below.
   Until it is filled in, this file does nothing.

   Umami does not use cookies and does not collect names or other personal information.
   It records page views, where visitors came from (referrer), country, device and visit duration.
   This file adds a few events on top of that:
     Open resource       a card, generator shortcut or task card clicked on the home / course / unit pages
     Browse              a course or unit page viewed on the home page (readable page name)
     Generator action    Build, Print student copy, Print teacher key, PowerPoint, Download, New problems, …
     Outbound link       a link that leaves the site (Buy Me a Coffee, email apps, …)
     Report a problem    the "Report a problem" email link on a resource card
     Time on page        sent once a page has been open and visible for 1, 5, 15 and 30 minutes

   Turn counting off for your own browser: open the site once with ?analytics=off at the end of
   the address (e.g. https://akneller1.github.io/classroom/?analytics=off). ?analytics=on turns it back on.
   Do this once on each computer and browser you use. */
(function () {
  'use strict';
  if (typeof window === 'undefined' || typeof document === 'undefined' || !window.location) return;
  var WEBSITE_ID = '309c294f-46be-4e91-bc1d-480170c70a3d';                                   // ← paste your Umami Website ID here
  var SCRIPT_URL = 'https://cloud.umami.is/script.js';   // the src in Umami's Tracking code
  var DOMAINS = ['akneller1.github.io'];                 // only count visits to the live site

  var W = window, D = document;
  var cfg = W.MK_ANALYTICS_CONFIG || {};                 // tests can override the three settings above
  if (cfg.websiteId !== undefined) WEBSITE_ID = cfg.websiteId;
  if (cfg.scriptUrl) SCRIPT_URL = cfg.scriptUrl;
  if (cfg.domains) DOMAINS = cfg.domains;

  function ls(op, k, v) { try { return op === 'get' ? W.localStorage.getItem(k) : op === 'set' ? W.localStorage.setItem(k, v) : W.localStorage.removeItem(k); } catch (e) { return null; } }
  var m = /[?&]analytics=(off|on)\b/.exec(W.location.search);
  if (m) { if (m[1] === 'off') ls('set', 'umami.disabled', '1'); else ls('remove', 'umami.disabled'); }

  if (!WEBSITE_ID) return;                               // not set up yet
  if (W.top !== W) return;                               // inside an iframe (e.g. the embedded Vocabulary Builder): the outer page counts
  if (DOMAINS.indexOf(W.location.hostname) < 0) return;  // previews, local copies and test servers are not counted
  if (ls('get', 'umami.disabled')) return;               // the owner's own browsers

  /* ---------- load Umami ---------- */
  var s = D.createElement('script');
  s.defer = true; s.src = SCRIPT_URL;
  s.setAttribute('data-website-id', WEBSITE_ID);
  s.setAttribute('data-domains', DOMAINS.join(','));
  (D.head || D.documentElement).appendChild(s);

  /* ---------- sending ---------- */
  var queue = [], PENDING = 'mk-analytics-pending';
  function clip(v, n) { v = String(v == null ? '' : v).replace(/\s+/g, ' ').trim(); return v.length > n ? v.slice(0, n - 1) + '…' : v; }
  function ready() { return W.umami && typeof W.umami.track === 'function'; }
  function send(name, data) {
    if (!ready()) { queue.push([name, data]); return; }
    try { W.umami.track(clip(name, 50), data || undefined); } catch (e) { /* never break the page */ }
  }
  /* A click that opens another page in this tab would cancel the request, so it is kept in this tab's
     session storage and sent from the next page (every page of the site loads this file). */
  function later(name, data) {
    try {
      var list = JSON.parse(W.sessionStorage.getItem(PENDING) || '[]');
      list.push([name, data]); W.sessionStorage.setItem(PENDING, JSON.stringify(list.slice(-10)));
    } catch (e) { send(name, data); }
  }
  function flush() {
    try { var list = JSON.parse(W.sessionStorage.getItem(PENDING) || '[]'); W.sessionStorage.removeItem(PENDING); list.forEach(function (x) { send(x[0], x[1]); }); } catch (e) { /* ignore */ }
    var q = queue; queue = []; q.forEach(function (x) { send(x[0], x[1]); });
  }
  var tries = 0;
  (function wait() { if (ready()) flush(); else if (tries++ < 40) setTimeout(wait, 250); })();

  /* ---------- where am I ---------- */
  var path = W.location.pathname, file = path.split('/').pop() || 'index.html';
  var TOOLS = {
    'worksheet.html': 'Worksheet Generator', 'menu-assessment.html': 'Assessment Generator', 'printables.html': 'Printable Generator',
    'lesson-planner.html': 'Lesson Planner', 'seating-chart.html': 'Seating Chart', 'vocabulary.html': 'Vocabulary Builder', 'activity.html': 'Activity'
  };
  var HOME = file === 'index.html' && !/worksheet-generator\//.test(path);
  function pageName() { return clip(D.title.replace(/\s*\|\s*Mr\. K.s Classroom\s*$/i, '').replace(/\s*·\s*Mr\. K.s Classroom\s*$/i, ''), 100) || file; }
  function unitArg() {
    var h = W.location.hash + W.location.search, u = /[#&?]unit=([a-z0-9\-]+)/i.exec(h);
    if (u) return u[1];
    var c = /[#&?]course=([a-z0-9]+)/i.exec(h), d = /[#&?]day=([0-9]+)/i.exec(h);   // lesson planner
    return d ? (c ? c[1] : 'algebra1') + ' day ' + d[1] : '';
  }

  /* ---------- clicks ---------- */
  var ACTIONS = {
    mmBuildBtn: 'Build', mmRebuild: 'Rebuild', mmDownload: 'Download file', mmSaveNamed: 'Save in browser', mmRegenAll: 'New problems', mmRegenVer: 'New problems',
    prPrintS: 'Print student copy', prPrintK: 'Print teacher key', prPlay: 'Play online', prNew: 'New problems',
    plPrintS: 'Print student handout', plPrintK: 'Print teacher key', plPptxStudent: 'Student PowerPoint', plPptxTeacher: 'Teacher PowerPoint', plNew: 'New problems'
  };
  function actionOf(el) {
    var b = el.closest && el.closest('button, a');
    if (!b) return null;
    if (b.id && ACTIONS[b.id]) return ACTIONS[b.id];
    var p = b.getAttribute('data-print');
    if (p) return p === 'key' ? 'Print teacher key' : 'Print student copy';
    return null;
  }
  D.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var act = actionOf(t);
    if (act) { send('Generator action', { action: act, tool: (TOOLS[file] || pageName()) + (unitArg() ? ' · ' + unitArg() : '') }); return; }

    var a = t.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/^mailto:/i.test(href)) {
      var card = a.closest('.card');
      send(a.classList.contains('report-problem') ? 'Report a problem' : 'Email link', { item: clip(card && card.querySelector('h3') ? card.querySelector('h3').textContent : a.textContent, 100) });
      return;
    }
    var url; try { url = new URL(a.href, W.location.href); } catch (err) { return; }
    if (!/^https?:$/.test(url.protocol)) return;
    var newTab = a.target === '_blank' || e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1;
    if (url.host !== W.location.host) {
      (newTab ? send : later)('Outbound link', { url: clip(url.host + url.pathname, 200) });
      return;
    }
    if (url.pathname === W.location.pathname && url.search === W.location.search) return;   // a #route on the same page: counted as Browse
    if (!HOME) return;                                                                     // resource opens are tracked from the home / course / unit pages
    var box = a.closest('.card, .generator-shortcut, .task-card');
    var title = box ? (box.querySelector('h3, h2, strong') || box).textContent : a.textContent;
    (newTab ? send : later)('Open resource', { title: clip(title, 120), from: pageName() });
  }, true);

  /* ---------- course and unit browsing (the home page draws each course/unit view from the #route) ---------- */
  if (HOME) {
    var lastPage = '';
    var browse = function () {
      setTimeout(function () {   // app.js renders on the same hashchange; read the title it sets
        var name = pageName();
        if (name && name !== lastPage) { lastPage = name; if (W.location.hash.length > 1) send('Browse', { page: name }); }
      }, 300);
    };
    W.addEventListener('hashchange', browse);
    browse();
  }

  /* ---------- time on page: milestones of visible time, sent while the page is still open ---------- */
  var MILESTONES = [1, 5, 15, 30], visible = 0, last = Date.now(), next = 0;
  function tick() {
    var now = Date.now();
    if (D.visibilityState === 'visible') visible += now - last;
    last = now;
    while (next < MILESTONES.length && visible >= MILESTONES[next] * 60000) {
      send('Time on page', { minutes: MILESTONES[next], page: TOOLS[file] || pageName() });
      next++;
    }
  }
  D.addEventListener('visibilitychange', tick);
  setInterval(tick, 15000);
})();
