(function () {
  'use strict';

  var L = window.LIBRARY;
  var app = document.getElementById('main');
  var nav = document.getElementById('nav');
  var q = document.getElementById('q');
  var skip = document.getElementById('skip');

  var token = '';
  var query = '';
  var filters = {};
  var focusKey = null;
  var firstRender = true;
  var ignoreHash = false;
  var saved = loadSaved();

  /* ---------- storage ---------- */
  function loadSaved() {
    try {
      var v = JSON.parse(localStorage.getItem('mrk-saved') || '[]');
      return Array.isArray(v) ? v : [];
    } catch (e) { return []; }
  }
  function storeSaved() {
    try { localStorage.setItem('mrk-saved', JSON.stringify(saved)); } catch (e) {}
  }
  function isSaved(path) { return saved.indexOf(path) >= 0; }
  function toggleSaved(path) {
    var i = saved.indexOf(path);
    if (i >= 0) saved.splice(i, 1); else saved.push(path);
    storeSaved();
  }

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function toArr(v) { return v == null ? [] : (Array.isArray(v) ? v : [v]); }
  function acts(n) { return n === 1 ? '1 activity' : n + ' activities'; }
  function units(n) { return n === 1 ? '1 unit' : n + ' units'; }
  function courseToken(c) { return c.id; }
  function unitToken(c, u) { return c.id + '.' + u.id; }
  function href(t) { return '#' + encodeURIComponent(t).replace(/%2E/g, '.'); }
  function courseCount(c) {
    return c.units.reduce(function (n, u) { return n + u.artifacts.length; }, 0);
  }
  function unitsWithActivities(c) {
    return c.units.filter(function (u) { return u.artifacts.length; }).length;
  }
  function everything() {
    var out = [];
    L.courses.forEach(function (c) {
      c.units.forEach(function (u) {
        u.artifacts.forEach(function (a) { out.push({ a: a, c: c, u: u }); });
      });
    });
    return out;
  }
  function isNew(a) {
    var t = a.added ? Date.parse(a.added) : NaN;
    if (isNaN(t)) return false;
    return (Date.now() - t) < (L.newDays || 30) * 86400000;
  }
  var ACTIVITY_FORMATS = [
    { id: 'showdown', name: 'Showdown / Jeopardy', description: 'Choose a category and point value, solve the problem, then reveal the worked solution. A game-show format for class or team review.' },
    { id: 'connect-four', name: 'Connect 4', description: 'Solve math problems to earn a disc. Teams take turns building a row of four while blocking their opponents.' },
    { id: 'mazes', name: 'Mazes', description: 'Solve each problem and follow the matching answer through a printable maze. Show your work as you find the path to the finish.' },
    { id: 'flashcards', name: 'Flashcards', description: 'Practice at your own pace, reveal worked solutions, and mark cards to revisit. Useful for independent study and quick review.' },
    { id: 'picture-reveal', name: 'Picture Reveal', description: 'Answer math questions to uncover a hidden picture, with feedback and worked solutions along the way.' },
    { id: 'error-analysis', name: 'Error Analysis', description: 'Examine a worked example, identify the mistake, and explain how to fix it. Printable practice that builds mathematical reasoning.' },
    { id: 'topic-games', name: 'Topic-Specific Games', description: 'Explore focused math challenges such as Slope Links Mini Golf and Zombie Fence, where the topic becomes part of the game.' },
    { id: 'other', name: 'More Activities', description: 'Explore additional practice and resources across Algebra and Geometry.' }
  ];
  function activityFormat(a) {
    var path = a.path || '';
    if (/jeopardy|showdown/i.test(path)) return 'showdown';
    if (/connect-four|inequality-four/i.test(path)) return 'connect-four';
    if (/maze/i.test(path)) return 'mazes';
    if (/flashcards/i.test(path)) return 'flashcards';
    if (/picture-reveal/i.test(path)) return 'picture-reveal';
    if (/error-analysis/i.test(path)) return 'error-analysis';
    if (toArr(a.type).indexOf('Game') >= 0) return 'topic-games';
    return 'other';
  }
  function formatItems(format) {
    return everything().filter(function (it) { return activityFormat(it.a) === format.id; });
  }
  function activityTableHtml() {
    return '<table class="activity-table"><caption class="sr">Browse resources by activity format</caption>' +
      '<thead><tr><th scope="col">Activity type</th><th scope="col">Description</th></tr></thead><tbody>' +
      ACTIVITY_FORMATS.map(function (format) {
        var items = formatItems(format);
        var n = items.length;
        if (!n) return '';
        var preview = items.filter(function (it) { return !!it.a.thumb; })[0];
        return '<tr><th scope="row"><a class="activity-category" href="' + href('activity.' + format.id) + '">' +
          (preview ? '<img class="activity-preview" src="' + esc(preview.a.thumb) + '" alt="" width="72" height="48" loading="lazy">' : '') +
          '<span class="activity-label"><span class="activity-name">' + esc(format.name) + '</span>' +
          '<span class="activity-count">' + acts(n) + '</span></span></a></th><td>' + esc(format.description) + '</td></tr>';
      }).join('') + '</tbody></table>';
  }

  /* ---------- decorative art ---------- */
  var ART = {
    curve:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="100" y="20" width="80" height="110" rx="6"/>' +
      '<line class="s-thin" x1="20" y1="130" x2="190" y2="130"/>' +
      '<line class="s-thin" x1="100" y1="10" x2="100" y2="150"/>' +
      '<path class="s" d="M 30 20 Q 100 200 170 20"/>' +
      '<circle class="f" cx="65" cy="87.5" r="7"/><circle class="f" cx="135" cy="87.5" r="7"/><circle class="f" cx="100" cy="110" r="7"/>' +
      '</svg>',
    triangle:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<polygon class="f-soft" points="100,20 30,130 170,130"/>' +
      '<circle class="s-thin" cx="100" cy="91.6" r="38.4"/>' +
      '<polygon class="s" points="100,20 30,130 170,130"/>' +
      '<path class="s" d="M 52 130 A 22 22 0 0 0 44 114"/>' +
      '<circle class="f" cx="100" cy="20" r="7"/><circle class="f" cx="30" cy="130" r="7"/><circle class="f" cx="170" cy="130" r="7"/>' +
      '</svg>'
  };
  function artFor(c) { return ART[c.art] || ''; }

  var STAR =
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2 6.3 20.3l1.2-6.4L2.8 9.5l6.4-.8z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';
  var STAR_ON =
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2 6.3 20.3l1.2-6.4L2.8 9.5l6.4-.8z" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';

  /* ---------- pieces ---------- */
  function crumbs(list) {
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + list.map(function (item, i) {
      var last = i === list.length - 1;
      return '<li>' + (last ? '<span aria-current="page">' + esc(item[0]) + '</span>'
                            : '<a href="' + item[1] + '">' + esc(item[0]) + '</a>') + '</li>';
    }).join('') + '</ol></nav>';
  }

  function saveBtnHtml(path) {
    var on = isSaved(path);
    return '<button type="button" class="btn btn-ghost save" data-path="' + esc(path) + '" aria-pressed="' + on + '">' +
      (on ? STAR_ON : STAR) + '<span>' + (on ? 'Saved' : 'Save') + '</span></button>';
  }

  function activityUrl(a) { return 'activity.html?path=' + encodeURIComponent(a.path); }

  function cardHtml(it, showWhere) {
    var a = it.a;
    var tags = [];
    if (isNew(a)) tags.push('<li class="tag tag-new">New</li>');
    toArr(a.type).concat(toArr(a.level)).forEach(function (t) { tags.push('<li class="tag">' + esc(t) + '</li>'); });
    var topics = toArr(a.topics);
    return '<li class="card" data-color="' + esc(it.c.color || '') + '" data-path="' + esc(a.path) + '">' +
      '<a class="thumb" href="' + esc(activityUrl(a)) + '" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">' +
        (a.thumb ? '<img src="' + esc(a.thumb) + '" alt="" loading="lazy">' : '') + '</a>' +
      '<div class="card-body">' +
        (showWhere ? '<p class="where">' + esc(it.c.name) + ', ' + esc(it.u.name) + '</p>' : '') +
        (tags.length ? '<ul class="tags">' + tags.join('') + '</ul>' : '') +
        '<h3><a href="' + esc(activityUrl(a)) + '" target="_blank" rel="noopener">' + esc(a.title) +
          '<span class="sr"> (opens in a new tab)</span></a></h3>' +
        '<p class="desc">' + esc(a.description || '') + '</p>' +
        (topics.length ? '<p class="topics">' + esc(topics.join(', ')) + '</p>' : '') +
        '<div class="actions"><a class="btn btn-open" href="' + esc(activityUrl(a)) + '" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">Open activity</a>' +
          saveBtnHtml(a.path) + '</div>' +
      '</div></li>';
  }

  function chip(field, val, label) {
    var on = (filters[field] || '') === val;
    return '<button type="button" class="chip" data-field="' + field + '" data-val="' + esc(val) +
           '" aria-pressed="' + on + '">' + esc(label) + '</button>';
  }
  function chipsHtml(items) {
    var out = '';
    [['type', 'Type'], ['level', 'Level']].forEach(function (f) {
      var seen = [];
      items.forEach(function (it) {
        toArr(it.a[f[0]]).forEach(function (v) { if (seen.indexOf(v) < 0) seen.push(v); });
      });
      if (seen.length < 2) return;
      out += '<div class="chips" role="group" aria-label="Filter by ' + f[1].toLowerCase() + '">' +
             '<span class="chips-label">' + f[1] + '</span>' + chip(f[0], '', 'All');
      seen.forEach(function (v) { out += chip(f[0], v, v); });
      out += '</div>';
    });
    return out ? '<div class="filters">' + out + '</div>' : '';
  }
  function applyFilters(items) {
    return items.filter(function (it) {
      return Object.keys(filters).every(function (k) {
        return !filters[k] || toArr(it.a[k]).indexOf(filters[k]) >= 0;
      });
    });
  }
  function cardsHtml(items, showWhere) {
    var shown = applyFilters(items);
    if (!shown.length) {
      return '<div class="empty"><h2>No matches</h2><p>No activities fit these filters. Choose All to see everything here.</p></div>';
    }
    return '<ul class="cards">' + shown.map(function (it) { return cardHtml(it, showWhere); }).join('') + '</ul>';
  }

  /* ---------- views ---------- */
  function homeView() {
    return {
      title: L.title,
      html:
        '<section class="hero"><div class="wrap">' +
          '<div class="hero-copy"><h1 tabindex="-1">' + esc(L.title).replace(/&#39;/g, '’') + '</h1>' +
          '<p class="lede">' + esc(L.tagline) + '</p></div>' +
        '</div></section>' +
        '<section class="section"><div class="wrap"><h2 class="sr">Courses</h2><ul class="courses">' +
          L.courses.map(function (c) {
            var n = courseCount(c);
            return '<li><a class="course" data-color="' + esc(c.color || '') + '" href="' + href(courseToken(c)) + '">' +
              '<h3>' + esc(c.name) + '</h3><p>' + esc(c.blurb || '') + '</p>' +
              '<p class="count">' + (n ? acts(n) + ' in ' + units(unitsWithActivities(c)) : 'First activities coming soon') + '</p>' +
              artFor(c) + '</a></li>';
          }).join('') + '</ul></div></section>' +
        '<section class="section"><div class="wrap"><div class="section-head"><h2>Browse by activity</h2></div>' +
          activityTableHtml() + '</div></section>'
    };
  }

  function bandHtml(c, inner, extra) {
    return '<section class="band"' + (c ? ' data-color="' + esc(c.color || '') + '"' : '') + '><div class="wrap">' + inner + '</div></section>';
  }

  function courseView(c) {
    var n = courseCount(c);
    var inner =
      '<div class="band-grid"><div>' +
        crumbs([['Home', '#'], [c.name, null]]) +
        '<h1 tabindex="-1">' + esc(c.name) + '</h1>' +
        (c.blurb ? '<p class="band-blurb">' + esc(c.blurb) + '</p>' : '') +
        '<p class="band-meta">' + (n ? acts(n) + ' in ' + unitsWithActivities(c) + ' of ' + units(c.units.length) : units(c.units.length) + ', activities coming soon') + '</p>' +
      '</div>' + (c.art ? '<div class="band-art" aria-hidden="true">' + artFor(c) + '</div>' : '') + '</div>';
    return {
      title: c.name,
      html: bandHtml(c, inner) +
        '<section class="section"><div class="wrap"><h2 class="sr">Units</h2><ul class="units">' +
        c.units.map(function (u) {
          var k = u.artifacts.length;
          if (!k) {
            return '<li><div class="unit soon" data-color="' + esc(c.color || '') + '"><h3>' + esc(u.name) + '</h3>' +
              '<div class="unit-meta"><span class="unit-count">Coming soon</span></div></div></li>';
          }
          var minis = u.artifacts.slice(0, 3).filter(function (a) { return a.thumb; }).map(function (a) {
            return '<img src="' + esc(a.thumb) + '" alt="" loading="lazy">';
          }).join('');
          return '<li><a class="unit" data-color="' + esc(c.color || '') + '" href="' + href(unitToken(c, u)) + '"><h3>' + esc(u.name) + '</h3>' +
            '<div class="unit-meta"><span class="unit-count">' + acts(k) + '</span>' + (minis ? '<span class="minis">' + minis + '</span>' : '') + '</div></a></li>';
        }).join('') + '</ul></div></section>'
    };
  }

  function unitView(c, u) {
    var items = u.artifacts.map(function (a) { return { a: a, c: c, u: u }; });
    var inner =
      crumbs([['Home', '#'], [c.name, href(courseToken(c))], [u.name, null]]) +
      '<h1 tabindex="-1">' + esc(u.name) + '</h1>' +
      '<p class="band-meta">' + (items.length ? acts(items.length) : 'Coming soon') + '</p>';
    return {
      title: u.name + ', ' + c.name,
      html: bandHtml(c, inner) +
        '<section class="section"><div class="wrap">' +
        (items.length ? chipsHtml(items) + cardsHtml(items, false)
                      : '<div class="empty"><h2>Coming soon</h2><p>No activities in this unit yet. <a href="' + href(courseToken(c)) + '">Back to ' + esc(c.name) + '</a></p></div>') +
        '</div></section>'
    };
  }

  function activityIndexView() {
    return {
      title: 'Browse by activity',
      html: bandHtml(null, crumbs([['Home', '#'], ['Browse by activity', null]]) + '<h1 tabindex="-1">Browse by activity</h1>') +
        '<section class="section"><div class="wrap">' + activityTableHtml() + '</div></section>'
    };
  }

  function activityView(format) {
    var items = formatItems(format);
    var inner = crumbs([['Home', '#'], ['Browse by activity', '#activities'], [format.name, null]]) +
      '<h1 tabindex="-1">' + esc(format.name) + '</h1>' +
      '<p class="band-blurb">' + esc(format.description) + '</p><p class="band-meta">' + acts(items.length) + ' across Algebra and Geometry</p>';
    return {
      title: format.name,
      html: bandHtml(null, inner) + '<section class="section"><div class="wrap">' +
        (items.length ? chipsHtml(items) + cardsHtml(items, true) : '<div class="empty"><h2>Coming soon</h2><p>No activities in this format yet.</p></div>') + '</div></section>'
    };
  }

  function savedView() {
    var items = everything().filter(function (it) { return isSaved(it.a.path); });
    var inner = crumbs([['Home', '#'], ['Saved', null]]) + '<h1 tabindex="-1">Saved activities</h1>' +
      '<p class="band-meta">' + acts(items.length) + '</p>';
    return {
      title: 'Saved activities',
      html: bandHtml(null, inner) +
        '<section class="section"><div class="wrap">' +
        (items.length ? chipsHtml(items) + cardsHtml(items, true)
                      : '<div class="empty"><h2>Nothing saved yet</h2><p>Choose Save on any activity and it will be listed here. Saved activities stay in this browser.</p></div>') +
        '</div></section>'
    };
  }

  function searchView(text) {
    var terms = text.toLowerCase().split(/\s+/).filter(Boolean);
    var items = everything().filter(function (it) {
      var hay = [it.a.title, it.a.description, it.u.name, it.c.name]
        .concat(toArr(it.a.type), toArr(it.a.level), toArr(it.a.topics)).join(' ').toLowerCase();
      return terms.every(function (t) { return hay.indexOf(t) >= 0; });
    });
    var inner = '<h1 tabindex="-1">Results for “' + esc(text) + '”</h1><p class="band-meta">' + acts(items.length) + '</p>';
    return {
      title: 'Search: ' + text,
      html: bandHtml(null, inner) +
        '<section class="section"><div class="wrap">' +
        (items.length ? chipsHtml(items) + cardsHtml(items, true)
                      : '<div class="empty"><h2>No matches</h2><p>Nothing matches “' + esc(text) + '”. Try a topic such as slope or inequalities, or <a href="#">browse by course</a>.</p></div>') +
        '</div></section>'
    };
  }

  function notFoundView() {
    return {
      title: 'Page not found',
      html: bandHtml(null, '<h1 tabindex="-1">Page not found</h1>') +
        '<section class="section"><div class="wrap"><div class="empty"><h2>That page does not exist</h2><p><a href="#">Go to the home page</a> and choose a course.</p></div></div></section>'
    };
  }

  function resolve(t) {
    if (!t) return { name: 'home' };
    if (t === 'saved') return { name: 'saved' };
    if (t === 'activities') return { name: 'activities' };
    if (t.indexOf('activity.') === 0) {
      var format = ACTIVITY_FORMATS.filter(function (f) { return f.id === t.slice(9); })[0];
      return format ? { name: 'activity', format: format } : { name: 'nf' };
    }
    var parts = t.split('.');
    var c = L.courses.filter(function (x) { return x.id === parts[0]; })[0];
    if (!c) return { name: 'nf' };
    if (!parts[1]) return { name: 'course', c: c };
    var u = c.units.filter(function (x) { return x.id === parts[1]; })[0];
    return u ? { name: 'unit', c: c, u: u } : { name: 'nf' };
  }

  /* ---------- render ---------- */
  function updateNav(r) {
    var html = L.courses.map(function (c) {
      var cur = r && r.c && r.c.id === c.id ? ' aria-current="page"' : '';
      return '<a href="' + href(courseToken(c)) + '"' + cur + '>' + esc(c.name) + '</a>';
    }).join('');
    html += '<a href="#activities"' + (r && (r.name === 'activities' || r.name === 'activity') ? ' aria-current="page"' : '') + '>Activities</a>';
    var curSaved = r && r.name === 'saved' ? ' aria-current="page"' : '';
    html += '<a href="#saved"' + curSaved + '>Saved' +
      (saved.length ? ' <span class="badge" aria-label="' + saved.length + ' saved">' + saved.length + '</span>' : '') + '</a>';
    nav.innerHTML = html;
  }

  function render(keepFocus) {
    var r = resolve(token);
    var view;
    if (query) view = searchView(query);
    else if (r.name === 'home') view = homeView();
    else if (r.name === 'course') view = courseView(r.c);
    else if (r.name === 'unit') view = unitView(r.c, r.u);
    else if (r.name === 'saved') view = savedView();
    else if (r.name === 'activities') view = activityIndexView();
    else if (r.name === 'activity') view = activityView(r.format);
    else view = notFoundView();

    app.innerHTML = view.html;
    try { document.title = view.title === L.title ? L.title : view.title + ' | ' + L.title; } catch (e) {}
    updateNav(query ? null : r);

    if (focusKey) {
      Array.prototype.forEach.call(app.querySelectorAll('.chip'), function (b) {
        if (b.getAttribute('data-field') + '|' + b.getAttribute('data-val') === focusKey) b.focus();
      });
      focusKey = null;
    } else if (!keepFocus && !firstRender) {
      var h = app.querySelector('h1');
      if (h) h.focus({ preventScroll: true });
      window.scrollTo(0, 0);
    }
    firstRender = false;
  }

  function go(t) {
    token = t;
    query = '';
    q.value = '';
    filters = {};
    try {
      if (location.hash.replace(/^#/, '') !== t) { ignoreHash = true; location.hash = t; }
    } catch (e) { ignoreHash = false; }
    render(false);
  }

  /* ---------- events ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (a && !e.metaKey && !e.ctrlKey && !e.shiftKey && a.getAttribute('target') !== '_blank') {
      e.preventDefault();
      var h = a.getAttribute('href').replace(/^#/, '');
      var t = h; try { t = decodeURIComponent(h); } catch (err) {}
      go(t);
      return;
    }

    var s = e.target.closest ? e.target.closest('.save') : null;
    if (s) {
      var path = s.getAttribute('data-path');
      toggleSaved(path);
      var r = resolve(token);
      if (!query && r.name === 'saved') {
        render(true);
        var first = app.querySelector('.save');
        if (first) first.focus(); else { var h1 = app.querySelector('h1'); if (h1) h1.focus({ preventScroll: true }); }
        return;
      }
      Array.prototype.forEach.call(document.querySelectorAll('.save'), function (b) {
        if (b.getAttribute('data-path') !== path) return;
        var on = isSaved(path);
        b.setAttribute('aria-pressed', on);
        b.innerHTML = (on ? STAR_ON : STAR) + '<span>' + (on ? 'Saved' : 'Save') + '</span>';
      });
      updateNav(query ? null : r);
      return;
    }

    var c = e.target.closest ? e.target.closest('.chip') : null;
    if (c) {
      var field = c.getAttribute('data-field'), val = c.getAttribute('data-val');
      if (val) filters[field] = val; else delete filters[field];
      focusKey = field + '|' + val;
      render(true);
      return;
    }


  });

  document.getElementById('searchForm').addEventListener('submit', function (e) { e.preventDefault(); });
  q.addEventListener('input', function () {
    query = q.value.trim();
    filters = {};
    render(true);
  });
  q.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && q.value) { q.value = ''; query = ''; filters = {}; render(true); }
  });
  skip.addEventListener('click', function () { app.focus(); });

  window.addEventListener('hashchange', function () {
    if (ignoreHash) { ignoreHash = false; return; }
    var t = location.hash.replace(/^#/, '');
    try { t = decodeURIComponent(t); } catch (e) {}
    if (t === token && !query) return;
    token = t; query = ''; q.value = ''; filters = {};
    render(false);
  });

  /* ---------- start ---------- */
  (function init() {
    var foot = document.getElementById('foot');
    if (foot) foot.textContent = L.footer || '';
    var bn = document.getElementById('brandName');
    if (bn) bn.textContent = L.title.replace(/'/g, '’');
    var t = '';
    try { t = decodeURIComponent(location.hash.replace(/^#/, '')); } catch (e) {}
    token = t;
    render(true);
  })();
})();
