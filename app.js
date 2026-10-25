(function () {
  'use strict';

  var L = window.LIBRARY;
  var courseOrder = { algebra: 0, geometry: 1, algebra2: 2 };
  L.courses.sort(function (a, b) {
    return (courseOrder[a.id] == null ? 99 : courseOrder[a.id]) -
      (courseOrder[b.id] == null ? 99 : courseOrder[b.id]);
  });
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
    { id: 'worksheet-generator', name: 'Worksheet Generator', description: 'Build practice worksheets for any unit: choose skills and CP2, CP1 or Honors difficulty, short answer or multiple choice, up to three versions, and an answer key with worked solutions. Every answer is checked.' },
    { id: 'assessment-generator', name: 'Assessment Generator', description: 'Build a standard unit test (multiple choice and short answer) or a choice-based restaurant-menu assessment: pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys.' },
    { id: 'partner-checks', name: 'Partner Checks', description: 'Partners solve different problems with matching answers, compare results, and work together to resolve mistakes. Includes Partner A and Partner B worksheets.' },
    { id: 'showdown', name: 'Showdown / Jeopardy', description: 'Choose a category and point value, solve the problem, then reveal the worked solution. A game-show format for class or team review.' },
    { id: 'connect-four', name: 'Connect 4', description: 'Solve math problems to earn a disc. Teams take turns building a row of four while blocking their opponents.' },
    { id: 'tic-tac-toe', name: 'Tic-Tac-Toe', description: 'Two teams solve multiple-choice math problems to claim squares and make three in a row. A wrong answer gives the other team a chance to steal. Includes an optional timer.' },
    { id: 'mazes', name: 'Mazes', description: 'Solve each problem and follow the matching answer through a printable maze. Show your work as you find the path to the finish.' },
    { id: 'flashcards', name: 'Flashcards', description: 'Practice at your own pace, reveal worked solutions, and mark cards to revisit. Useful for independent study and quick review.' },
    { id: 'color-by-number', name: 'Color by Number', description: 'Solve math problems, match each answer to a color, and complete a themed picture. Printable activities for practice and review.' },
    { id: 'picture-reveal', name: 'Picture Reveal', description: 'Answer math questions to uncover a hidden picture, with feedback and worked solutions along the way.' },
    { id: 'error-analysis', name: 'Error Analysis', description: 'Examine a worked example, identify the mistake, and explain how to fix it. Printable practice that builds mathematical reasoning.' },
    { id: 'detective-games', name: 'Detective Games', description: 'Solve math problems to unlock clues, eliminate suspects, and crack a themed mystery. Type your answers and use the case board to identify the culprit.' },
    { id: 'escape-rooms', name: 'Escape Rooms', description: 'Work together to solve math puzzles, decode clues, and unlock five rooms before the timer runs out. Includes hints and a final challenge.' },
    { id: 'topic-games', name: 'Topic-Specific Games', description: 'Explore focused math challenges such as Slope Links Mini Golf and Zombie Fence, where the topic becomes part of the game.' },
    { id: 'cheat-sheets', name: 'Cheat Sheets', description: 'Colorful, printable front-and-back study guides with key vocabulary, formulas, worked examples, graphs, and reminders.' },
    { id: 'whodunnit', name: 'Whodunnit', description: 'Solve problems on printable clue cards, eliminate suspects on a case board, and solve the mystery. Includes space to show your work.' },
    { id: 'tarsia', name: 'Tarsia Puzzles', description: 'Cut out triangles and match math problems to their answers to build a hexagon. Printable puzzles with space to show your work.' },
    { id: 'assessment-menus', name: 'Assessment Menus', description: 'Choose problems from a menu of point values to demonstrate your understanding. Printable assessments with student choice, scoring guidance, and teacher keys.' },
    { id: 'stations', name: 'Stations', description: 'Printable station-work activities with sets of problems for small-group rotation, review, and independent practice.' },
    { id: 'other', name: 'More Activities', description: 'Explore additional practice and resources across Algebra 1, Algebra 2, and Geometry.' }
  ];
  function activityFormat(a) {
    if (/worksheet-generator\/menu-assessment/i.test(a.path || '')) return 'assessment-generator';
    if (/worksheet-generator\//i.test(a.path || '')) return 'worksheet-generator';
    if (/partner-check/i.test(a.path || '')) return 'partner-checks';
    var path = a.path || '';
    if (/jeopardy|showdown/i.test(path)) return 'showdown';
    if (/connect-four|inequality-four/i.test(path)) return 'connect-four';
    if (/tic-tac-toe/i.test(path)) return 'tic-tac-toe';
    if (/whodunnit/i.test(path)) return 'whodunnit';
    if (/tarsia/i.test(path)) return 'tarsia';
    if (/assessment-menu/i.test(path)) return 'assessment-menus';
    if (/escape-room/i.test(path)) return 'escape-rooms';
    if (/maze/i.test(path)) return 'mazes';
    if (/flashcards/i.test(path)) return 'flashcards';
    if (/color-by-number/i.test(path)) return 'color-by-number';
    if (/picture-reveal/i.test(path)) return 'picture-reveal';
    if (/stations/i.test(path) || /stations/i.test(a.title || '')) return 'stations';
    if (/cheat.sheet/i.test(path) || /cheat.sheet/i.test(a.title || '')) return 'cheat-sheets';
    if (/error-analysis/i.test(path)) return 'error-analysis';
    if (toArr(a.topics).some(function (topic) { return /detective game/i.test(topic); })) return 'detective-games';
    if (toArr(a.type).indexOf('Game') >= 0) return 'topic-games';
    return 'other';
  }
  function formatItems(format) {
    return everything().filter(function (it) { return activityFormat(it.a) === format.id; });
  }
  var RESOURCE_GROUPS = [
    { id: 'games', name: 'Games', formats: ['showdown', 'connect-four', 'tic-tac-toe', 'picture-reveal', 'detective-games', 'escape-rooms', 'topic-games'] },
    { id: 'study-guides', name: 'Study Guides', formats: ['cheat-sheets', 'flashcards'] },
    { id: 'worksheets', name: 'Printable Worksheets', formats: ['worksheet-generator', 'assessment-generator', 'partner-checks', 'mazes', 'color-by-number', 'error-analysis', 'stations', 'whodunnit', 'tarsia', 'assessment-menus', 'other'] }
  ];
  var FORMAT_SUMMARIES = {
    'worksheet-generator': 'Choose skills and create customized printable worksheets with answer keys.',
    'assessment-generator': 'Build a test or a menu assessment with verified answer keys.',
    'partner-checks': 'Solve different problems, compare matching answers, and check each other’s work.',
    'showdown': 'Choose a question and point value for team review.',
    'connect-four': 'Solve problems to earn discs and connect four.',
    'tic-tac-toe': 'Answer correctly to claim a square and make three in a row.',
    'picture-reveal': 'Solve problems to uncover a hidden picture.',
    'detective-games': 'Unlock clues, eliminate suspects, and solve the mystery.',
    'escape-rooms': 'Solve math puzzles and unlock rooms before time runs out.',
    'topic-games': 'Explore focused challenges, from mini golf to Zombie Fence.',
    'cheat-sheets': 'Review key vocabulary, formulas, and worked examples.',
    'flashcards': 'Practice at your own pace and reveal worked solutions.',
    'mazes': 'Follow correct answers to find a path through the maze.',
    'color-by-number': 'Match answers to colors to complete a themed picture.',
    'error-analysis': 'Find the mistake and explain how to correct it.',
    'whodunnit': 'Solve clue cards, clear suspects, and crack a printable mystery.',
    'tarsia': 'Match problems and answers on triangle pieces to build a hexagon.',
    'assessment-menus': 'Choose problems at different point values to build your assessment.',
    'stations': 'Rotate through problem sets for practice and review.',
    'other': 'Explore more practice resources.'
  };
  function activityDirectoryHtml() {
    return '<div class="resource-columns">' + RESOURCE_GROUPS.map(function (group) {
      var formats = group.formats.map(function (id) {
        return ACTIVITY_FORMATS.filter(function (format) { return format.id === id; })[0];
      });
      return '<section class="resource-column" aria-labelledby="resource-' + group.id + '">' +
        '<h3 id="resource-' + group.id + '">' + esc(group.name) + '</h3><ul class="resource-types">' +
        formats.map(function (format) {
          var items = formatItems(format);
          if (!items.length) return '';
          var preview = items.filter(function (it) { return !!it.a.thumb; })[0];
          return '<li><a class="resource-type" href="' + href('activity.' + format.id) + '">' +
            (preview ? '<img src="' + esc(preview.a.thumb) + '" alt="" width="144" height="90" loading="lazy">' : '') +
            '<h4>' + esc(format.name) + '</h4><p>' + esc(FORMAT_SUMMARIES[format.id]) + '</p>' +
            '<span class="resource-count">' + acts(items.length) + '</span></a></li>';
        }).join('') + '</ul></section>';
    }).join('') + '</div>';
  }

  /* ---------- decorative art ---------- */
  var ART = {
    linear:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="35" y="20" width="140" height="115" rx="6"/>' +
      '<path class="s-thin" d="M 35 45 H 175 M 35 75 H 175 M 35 105 H 175 M 65 20 V 135 M 100 20 V 135 M 135 20 V 135"/>' +
      '<path class="s" d="M 20 135 H 185 M 35 145 V 10"/>' +
      '<path class="s" d="M 45 120 L 165 30"/>' +
      '<circle class="f" cx="65" cy="105" r="6"/><circle class="f" cx="105" cy="75" r="6"/><circle class="f" cx="145" cy="45" r="6"/>' +
      '</svg>',
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
  function artFor(c) { return ART[c.id === 'algebra' ? 'linear' : c.art] || ''; }

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

  function activityUrl(a) { return /^worksheet-generator\/[a-z0-9_\-/]+\.html(#unit=[a-z0-9\-]+)?$/i.test(a.path || '') ? a.path : 'activity.html?path=' + encodeURIComponent(a.path); }

  function actionLabel(a) {
    var format = activityFormat(a);
    if (format === 'worksheet-generator') return 'Create worksheet';
    if (format === 'assessment-generator') return 'Build assessment';
    if (format === 'cheat-sheets') return 'View study guide';
    if (format === 'flashcards') return 'Study flashcards';
    if (/\.pdf$/i.test(a.path)) return 'Open PDF';
    return toArr(a.type).indexOf('Game') >= 0 ? 'Play' : 'Open activity';
  }
  function resourceInfo(a) {
    var m = (window.RESOURCE_DETAILS || {})[a.path];
    if (!m) return '';
    var labels = [m.pages + (m.pages === 1 ? ' page' : ' pages')];
    if (m.embeddedKey) labels.push('Answer key included');
    if (m.answerKey) labels.push('Separate teacher key');
    if (m.studentOnly) labels.push('Student worksheets only');
    if (m.referenceSheet) labels.push('Reference sheet');
    return '<p class="resource-info">' + labels.map(esc).join(' · ') + '</p>';
  }
  function reportUrl(a) {
    var url = 'https://akneller1.github.io/classroom/' + activityUrl(a);
    var body = 'Activity: ' + a.title + '\nLink: ' + url + '\n\nProblem (broken link, incorrect answer, unclear directions, or other):\n\nProblem number / steps to reproduce:\n\nExpected result:\n';
    return 'https://github.com/akneller1/classroom/issues/new?title=' + encodeURIComponent('Resource problem: ' + a.title) + '&body=' + encodeURIComponent(body);
  }
  function cardHtml(it, showWhere, compact) {
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
        '<h3><a href="' + esc(activityUrl(a)) + '" target="_blank" rel="noopener">' + esc(a.title) +
          '<span class="sr"> (opens in a new tab)</span></a></h3>' +
        '<p class="desc">' + esc(shortDescription(a)) + '</p>' + resourceInfo(a) +
        '<div class="actions"><a class="btn btn-open" href="' + esc(activityUrl(a)) + '" target="_blank" rel="noopener" >' + esc(actionLabel(a)) + '<span class="sr"> (opens in a new tab)</span></a>' +
          saveBtnHtml(a.path) + '</div>' +
        '<a class="report-problem" href="' + esc(reportUrl(a)) + '" target="_blank" rel="noopener">Report a problem<span class="sr"> with ' + esc(a.title) + '</span> (GitHub)</a>' +
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
    return '<ul class="cards grouped-cards">' + shown.map(function (it) { return cardHtml(it, showWhere); }).join('') + '</ul>';
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
          }).join('') + '</ul></div></section>'
    };
  }

  function bandHtml(c, inner, extra) {
    return '<section class="band"' + (c ? ' data-color="' + esc(c.color || '') + '"' : '') + '><div class="wrap">' + inner + '</div></section>';
  }


  function shortDescription(a) {
    var text = (a.description || FORMAT_SUMMARIES[activityFormat(a)] || '').trim();
    if (text.length <= 155) return text;
    var sentence = text.match(/^.{40,154}?[.!?](?:\s|$)/);
    if (sentence) return sentence[0].trim();
    return text.slice(0, 152).replace(/\s+\S*$/, '') + '…';
  }

  function groupedCardsHtml(items, showWhere) {
    var shown = applyFilters(items);
    if (!shown.length) return '<div class="empty"><h2>No matches</h2><p>No activities fit these filters. Choose All to see everything here.</p></div>';
    return '<div class="activity-groups">' + RESOURCE_GROUPS.map(function (group) {
      var members = shown.filter(function (it) { return group.formats.indexOf(activityFormat(it.a)) !== -1; });
      if (!members.length) return '';
      return '<section class="activity-group" aria-labelledby="group-' + group.id + '">' +
        '<h2 id="group-' + group.id + '">' + esc(group.name) + '<span>' + acts(members.length) + '</span></h2>' +
        '<ul class="cards grouped-cards">' + members.map(function (it) { return cardHtml(it, showWhere, true); }).join('') + '</ul></section>';
    }).join('') + '</div>';
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
        '<section class="section"><div class="wrap"><h2 class="course-units-title">Browse by unit</h2><ul class="units">' +
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
    var generator = u.artifacts.filter(function (a) { return activityFormat(a) === 'worksheet-generator'; })[0];
    var menuGen = u.artifacts.filter(function (a) { return activityFormat(a) === 'assessment-generator'; })[0];
    var inner =
      crumbs([['Home', '#'], [c.name, href(courseToken(c))], [u.name, null]]) +
      '<h1 tabindex="-1">' + esc(u.name) + '</h1>' +
      '<p class="band-meta">' + (items.length ? acts(items.length) : 'Coming soon') + '</p>' +
      (generator ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(generator)) + '" target="_blank" rel="noopener">Create a worksheet<span class="sr"> (opens in a new tab)</span></a><p>Practice with short-answer or multiple-choice questions. Choose skills and CP2, CP1 or Honors difficulty; prints with an answer key.</p></div>' : '') +
      (menuGen ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(menuGen)) + '" target="_blank" rel="noopener">Build an assessment<span class="sr"> (opens in a new tab)</span></a><p>A standard test (multiple choice and short answer) or a choice menu. Choose skills and CP2, CP1 or Honors difficulty, then edit every problem before you print.</p></div>' : '');
    return {
      title: u.name + ', ' + c.name,
      html: bandHtml(c, inner) +
        '<section class="section"><div class="wrap">' +
        (items.length ? chipsHtml(items) + groupedCardsHtml(items, false)
                      : '<div class="empty"><h2>Coming soon</h2><p>No activities in this unit yet. <a href="' + href(courseToken(c)) + '">Back to ' + esc(c.name) + '</a></p></div>') +
        '</div></section>'
    };
  }


  function browseState(defaultFormat) {
    var params = new URLSearchParams(token.split('?')[1] || '');
    return { subject: params.get('subject') || '', unit: params.get('unit') || '',
      format: params.get('format') || defaultFormat || '', page: Math.max(1, parseInt(params.get('page'), 10) || 1) };
  }
  function browseToken(state) {
    var params = new URLSearchParams();
    ['subject', 'unit', 'format'].forEach(function (key) { if (state[key]) params.set(key, state[key]); });
    if (state.page > 1) params.set('page', state.page);
    return 'activities' + (params.toString() ? '?' + params.toString() : '');
  }
  function browseResults(state) {
    return everything().filter(function (it) {
      return (!state.subject || it.c.id === state.subject) &&
        (!state.unit || unitToken(it.c, it.u) === state.unit) &&
        (!state.format || activityFormat(it.a) === state.format);
    });
  }
  function browseSelect(id, label, choices, selected, allLabel) {
    return '<label for="browse-' + id + '">' + label +
      '<select id="browse-' + id + '" data-browse="' + id + '"><option value="">' + allLabel + '</option>' +
      choices.map(function (choice) { return '<option value="' + esc(choice.id) + '"' +
        (choice.id === selected ? ' selected' : '') + '>' + esc(choice.name) + '</option>'; }).join('') +
      '</select></label>';
  }
  function activityIndexView(defaultFormat) {
    var state = browseState(defaultFormat);
    var unitChoices = [];
    L.courses.forEach(function (c) {
      if (state.subject && state.subject !== c.id) return;
      c.units.forEach(function (u) { if (u.artifacts.length) unitChoices.push({
        id: unitToken(c, u), name: (state.subject ? '' : c.name + ' — ') + u.name
      }); });
    });
    var formats = [];
    RESOURCE_GROUPS.forEach(function (group) {
      group.formats.forEach(function (id) {
        var format = ACTIVITY_FORMATS.filter(function (f) { return f.id === id; })[0];
        if (format && formatItems(format).length) formats.push(format);
      });
    });
    var items = browseResults(state);
    var pages = Math.max(1, Math.ceil(items.length / 24));
    state.page = Math.min(state.page, pages);
    var offset = (state.page - 1) * 24;
    var visible = items.slice(offset, offset + 24);
    var controls = '<div class="browse-filters" role="group" aria-label="Filter activities">' +
      browseSelect('subject', 'Subject', L.courses, state.subject, 'All subjects') +
      browseSelect('unit', 'Unit', unitChoices, state.unit, 'All units') +
      browseSelect('format', 'Activity Type', formats, state.format, 'All activity types') +
      '<button type="button" class="btn browse-clear" id="browse-clear">Clear filters</button></div>';
    var pager = '';
    if (pages > 1) {
      var previous = Object.assign({}, state, { page: state.page - 1 });
      var next = Object.assign({}, state, { page: state.page + 1 });
      pager = '<nav class="browse-pagination" aria-label="Results pages">' +
        (state.page > 1 ? '<a class="btn" href="' + esc(href(browseToken(previous))) + '">Previous</a>' : '') +
        '<span>Page ' + state.page + ' of ' + pages + '</span>' +
        (state.page < pages ? '<a class="btn" href="' + esc(href(browseToken(next))) + '">Next</a>' : '') + '</nav>';
    }
    return {
      title: 'Browse activities',
      html: bandHtml(null, crumbs([['Home', '#'], ['Activities', null]]) +
        '<h1 tabindex="-1">Browse activities</h1><p class="band-blurb">Choose a subject, unit, or activity type to find what you need.</p>') +
        '<section class="section"><div class="wrap">' + controls +
        '<p class="browse-count" role="status" aria-live="polite">' + acts(items.length) +
        (items.length ? ' · Showing ' + (offset + 1) + '–' + (offset + visible.length) : '') + '</p>' +
        (visible.length ? '<ul class="cards grouped-cards">' + visible.map(function (it) { return cardHtml(it, true, true); }).join('') + '</ul>' :
          '<div class="empty"><h2>No matching activities</h2><p>Try a different activity type or clear the filters to browse everything.</p></div>') +
        pager + '</div></section>'
    };
  }
  function activityView(format) { return activityIndexView(format.id); }

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


  function searchWords(text) {
    return String(text || '').toLowerCase().replace(/flash\s+cards/g, 'flashcards')
      .replace(/connect\s*(?:four|4)/g, 'connect4').replace(/algebra\s*1/g, 'algebra1')
      .replace(/algebra\s*2/g, 'algebra2').replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function searchView(text) {
    var terms = searchWords(text).split(/\s+/).filter(Boolean);
    var items = everything().filter(function (it) {
      var format = ACTIVITY_FORMATS.filter(function (f) { return f.id === activityFormat(it.a); })[0];
      var hay = searchWords([it.a.title, it.a.description, it.u.name, it.c.name, format ? format.name : '']
        .concat(toArr(it.a.type), toArr(it.a.level), toArr(it.a.topics)).join(' '));
      return terms.every(function (term) { return hay.indexOf(term) >= 0; });
    });
    items.sort(function (a, b) {
      function score(it) { var title = searchWords(it.a.title); return terms.filter(function (t) { return title.indexOf(t) >= 0; }).length; }
      return score(b) - score(a);
    });
    var inner = crumbs([['Home', '#'], ['Search', null]]) +
      '<h1 tabindex="-1">Results for “' + esc(text) + '”</h1><p class="band-meta" role="status">' +
      acts(applyFilters(items).length) + '</p>';
    return {
      title: 'Search: ' + text,
      html: bandHtml(null, inner) +
        '<section class="section"><div class="wrap"><button class="btn clear-search" type="button" id="clear-search">Clear search</button>' +
        (items.length ? chipsHtml(items) + cardsHtml(items, true) :
          '<div class="empty"><h2>No matches</h2><p>Try a topic such as slope, an activity type such as flashcards, or a subject such as Algebra 1.</p><p><a href="#activities">Browse with subject, unit, and activity filters</a></p></div>') +
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
    t = t.split('?')[0];
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
  document.addEventListener('change', function (e) {
    var key = e.target.getAttribute && e.target.getAttribute('data-browse');
    if (!key) return;
    var route = resolve(token);
    var state = browseState(route.format ? route.format.id : '');
    state[key] = e.target.value;
    state.page = 1;
    if (key === 'subject') state.unit = '';
    if (key === 'unit' && state.unit) state.subject = state.unit.split('.')[0];
    go(browseToken(state));
    var control = document.getElementById('browse-' + key);
    if (control) control.focus({ preventScroll: true });
  });

  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('#clear-search')) { go(token); q.focus(); return; }
    if (e.target.closest && e.target.closest('#browse-clear')) {
      go('activities');
      var subject = document.getElementById('browse-subject');
      if (subject) subject.focus({ preventScroll: true });
      return;
    }
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
