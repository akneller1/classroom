/* Mr. K's Classroom: shared header for activity pages that are opened on their own (a shared student
   link, a game, a lab, a project). Added to published pages by scripts/add-site-header.mjs.
   - Shows the logo (to the home page) and a Back link to the activity's unit.
   - Stays out of the way: not shown inside the activity viewer (iframe), on pages that already show the
     Mr. K's Classroom name at the top, when printing, or in full screen.
   - Student links (student=1) show the logo only.
   - Pages that fill the whole window get a small floating badge instead of a bar, so nothing is pushed off screen.
   The script tag may carry data-course, data-unit, data-course-name and data-unit-name. */
(function () {
  'use strict';
  if (window.__mkSiteHeader) return;
  window.__mkSiteHeader = true;
  try { if (window.top !== window.self) return; } catch (e) { return; }

  var me = document.currentScript || document.querySelector('script[src*="site-header.js"]');
  var data = (me && me.dataset) || {};
  var params = new URLSearchParams(location.search);
  var COURSES = {
    grade1: '1st Grade Math', grade2: '2nd Grade Math', grade3: '3rd Grade Math', grade4: '4th Grade Math',
    grade5: '5th Grade Math', math6: '6th Grade Math', prealgebra7: 'Pre-Algebra (7th)', prealgebra: 'Pre-Algebra (8th)',
    algebra: 'Algebra 1', geometry: 'Geometry', algebra2: 'Algebra 2', precalculus: 'Precalculus', calculus: 'Calculus',
    statistics: 'Statistics', discrete: 'Discrete Math', 'financial-algebra': 'Financial Algebra'
  };
  var course = data.course || params.get('course') || (location.pathname.indexOf('/financial/') === 0 ? 'financial-algebra' : '') ||
    ((/^\/(grade[1-5])\//.exec(location.pathname) || [])[1] || '');
  var unit = data.unit || params.get('unit') || '';
  var courseName = data.courseName || COURSES[course] || '';
  var unitName = data.unitName || '';
  var student = params.get('student') === '1' || params.get('student') === 'true';
  var home = '/';
  var back = course ? home + '#' + encodeURIComponent(course) + (unit ? '.' + encodeURIComponent(unit) : '') : '';
  var backLabel = unitName ? 'Back to ' + unitName : unit ? 'Back to unit' : courseName ? 'Back to ' + courseName : 'Back';

  var CSS = '' +
    '.mk-site-header{box-sizing:border-box;display:flex;align-items:center;gap:.75rem;min-height:42px;padding:.35rem max(1rem,env(safe-area-inset-left));' +
    'background:#f7f8fc;color:#17213d;border-bottom:1px solid #d9dee7;font:600 15px/1.2 "Atkinson Hyperlegible",system-ui,-apple-system,"Segoe UI",sans-serif;position:relative;z-index:2147483000}' +
    '.mk-site-header a{color:inherit;text-decoration:none;border-radius:8px;padding:.3rem .45rem;display:inline-flex;align-items:center;gap:.45rem}' +
    '.mk-site-header a:hover{background:rgba(23,33,61,.07)}.mk-site-header a:focus-visible{outline:3px solid #1f5fbf;outline-offset:1px}' +
    '.mk-site-header .mk-logo{font:800 16px/1 "Bricolage Grotesque","Atkinson Hyperlegible",system-ui,sans-serif;letter-spacing:-.01em}' +
    '.mk-site-header .mk-mark{width:22px;height:22px;border-radius:6px;background:#17213d;color:#fff;display:inline-grid;place-items:center;font:800 13px/1 system-ui,sans-serif}' +
    '.mk-site-header .mk-course{color:#566173;font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
    '.mk-site-header .mk-back{margin-left:auto;white-space:nowrap}' +
    '.mk-site-header.mk-float{position:fixed;left:10px;bottom:10px;min-height:0;padding:.2rem;border:1px solid #d9dee7;border-radius:12px;box-shadow:0 4px 14px rgba(0,0,0,.15);opacity:.92}' +
    '.mk-site-header.mk-float .mk-course{display:none}.mk-site-header.mk-float .mk-back{margin-left:0}' +
    '@media (prefers-color-scheme:dark){.mk-site-header{background:#161c27;color:#e8ecf2;border-color:#2b3340}.mk-site-header .mk-course{color:#a3adbb}' +
    '.mk-site-header .mk-mark{background:#e8ecf2;color:#161c27}.mk-site-header a:hover{background:rgba(255,255,255,.08)}}' +
    '@media (max-width:520px){.mk-site-header .mk-course{display:none}}' +
    '@media print{.mk-site-header{display:none!important}}' +
    ':fullscreen .mk-site-header,.mk-site-header:fullscreen{display:none!important}';

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function alreadyBranded() {
    if (document.querySelector('.mk-site-header,.activity-bar,.site-header,[data-mk-brand]')) return true;
    var els = document.body.querySelectorAll('header,nav,a,h1,div,p,span');
    for (var i = 0; i < els.length && i < 400; i++) {
      var el = els[i];
      if (el.children.length > 6) continue;
      var t = el.textContent || '';
      if (!/Mr\.?\s?K[’']?s?\s+Classroom/i.test(t) || t.length > 120) continue;
      var r = el.getBoundingClientRect();
      if (r.width && r.height && r.top < 160) return true;
    }
    return false;
  }
  function fillsWindow() {
    var cs = getComputedStyle(document.body), hs = getComputedStyle(document.documentElement);
    return cs.overflow === 'hidden' || cs.overflowY === 'hidden' || hs.overflow === 'hidden' || hs.overflowY === 'hidden';
  }
  function render() {
    if (!document.body || alreadyBranded()) return;
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
    var bar = document.createElement('div');
    bar.className = 'mk-site-header' + (fillsWindow() ? ' mk-float' : '');
    bar.setAttribute('role', 'navigation');
    bar.setAttribute('aria-label', "Mr. K's Classroom");
    var html = '<a class="mk-logo" href="' + home + '"><span class="mk-mark" aria-hidden="true">K</span>Mr. K’s Classroom</a>';
    if (courseName && !student) html += '<span class="mk-course">' + esc(courseName) + (unitName ? ' · ' + esc(unitName) : '') + '</span>';
    if (!student) {
      var sameSite = document.referrer && document.referrer.indexOf(location.origin) === 0;
      var href = back || (sameSite ? document.referrer : home);
      html += '<a class="mk-back" href="' + esc(href) + '">← ' + esc(back || sameSite ? backLabel : 'All activities') + '</a>';
    }
    bar.innerHTML = html;
    document.body.insertBefore(bar, document.body.firstChild);
  }
  function start() { setTimeout(render, 400); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
