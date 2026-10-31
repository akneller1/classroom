(function () {
  'use strict';

  var L = window.LIBRARY;
  var courseOrder = { math6: 0, prealgebra7: 1, prealgebra: 2, algebra: 3, geometry: 4, algebra2: 5 };
  L.courses.sort(function (a, b) {
    return (courseOrder[a.id] == null ? 99 : courseOrder[a.id]) -
      (courseOrder[b.id] == null ? 99 : courseOrder[b.id]);
  });
  /* Courses marked "comingSoon" in data.js stay in the files but are hidden from navigation, search and
     browsing: the home page and the menu show them as "Coming soon". */
  var SOON = L.courses.filter(function (c) { return c.comingSoon; });
  L.courses = L.courses.filter(function (c) { return !c.comingSoon; });
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
  /* Units are numbered in course order: "Unit 3: Linear Inequalities". */
  function unitNum(c, u) { return c.units.indexOf(u) + 1; }
  function unitLabel(c, u) { return 'Unit ' + unitNum(c, u) + ': ' + u.name; }
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
    { id: 'lesson-planner', name: 'Daily Lesson Planner', description: 'Plan any of the 180 Algebra 1 days from the scope and sequence: objectives, vocabulary, sentence frame and misconception, plus a Do Now, worked examples, practice and an exit ticket at CP2, CP1 or Honors level. Prints a student handout and a teacher key with every answer checked.' },
    { id: 'worksheet-generator', name: 'Worksheet Generator', description: 'Build practice worksheets for any unit: choose skills and CP2, CP1 or Honors difficulty, short answer or multiple choice, up to three versions, and an answer key with worked solutions. Every answer is checked.' },
    { id: 'assessment-generator', name: 'Assessment Generator', description: 'Build a standard unit test (multiple choice and short answer) or a choice-based restaurant-menu assessment: pick skills and CP2, CP1 or Honors difficulty, review and edit every problem, then print student copies (Versions A–C) and teacher keys.' },
    { id: 'printable-generator', name: 'Printable Generators', description: 'Make a maze, color-by-number page, Tarsia puzzle, error analysis or partner check for any unit: CP2, CP1 or Honors, up to three versions, and an answer key with every answer checked.' },
    { id: 'partner-checks', name: 'Partner Checks', description: 'Partners solve different problems with matching answers, compare results, and work together to resolve mistakes. Includes Partner A and Partner B worksheets.' },
    { id: 'showdown', name: 'Showdown / Jeopardy', description: 'Choose a category and point value, solve the problem, then reveal the worked solution. A game-show format for class or team review.' },
    { id: 'connect-four', name: 'Connect 4', description: 'Solve math problems to earn a disc. Teams take turns building a row of four while blocking their opponents.' },
    { id: 'tic-tac-toe', name: 'Tic-Tac-Toe', description: 'Two teams solve multiple-choice math problems to claim squares and make three in a row. A wrong answer gives the other team a chance to steal. Includes an optional timer.' },
    { id: 'mazes', name: 'Mazes', description: 'Solve each problem and follow the matching answer through a printable maze. Show your work as you find the path to the finish.' },
    { id: 'interactive-practice-test', name: 'Assessment Readiness Check', description: 'Complete a generated online assessment, receive worked solutions and skill-by-skill feedback, and practice missed concepts with fresh questions.' },
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
    { id: 'other', name: 'More Activities', description: 'Explore additional practice and resources.' }
  ];
  function activityFormat(a) {
    if (/worksheet-generator\/practice-test\.html/i.test(a.path || '')) return 'interactive-practice-test';
    if (/worksheet-generator\/lesson-planner\.html/i.test(a.path || '')) return 'lesson-planner';
    if (/worksheet-generator\/printables\.html/i.test(a.path || '')) return 'printable-generator';
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
  /* Teaching mode metadata: derived from game mechanics, not the generic 'Game' type. */
  function gameMode(a) {
    var f = activityFormat(a);
    if (['showdown', 'connect-four', 'tic-tac-toe'].indexOf(f) >= 0) return 'Team Games';
    if (f === 'escape-rooms') return 'Collaborative Challenges';
    if (['picture-reveal', 'detective-games', 'topic-games'].indexOf(f) >= 0) return 'Individual Review';
    return '';
  }
  var GAME_MODES = ['Individual Review', 'Team Games', 'Collaborative Challenges'];
  function formatItems(format) {
    return everything().filter(function (it) { return activityFormat(it.a) === format.id; });
  }
  var RESOURCE_GROUPS = [
    { id: 'generators', name: 'Generators', formats: ['lesson-planner', 'worksheet-generator', 'assessment-generator', 'printable-generator'] },
    { id: 'games', name: 'Games', formats: ['showdown', 'connect-four', 'tic-tac-toe', 'picture-reveal', 'detective-games', 'escape-rooms', 'topic-games'] },
    { id: 'study-guides', name: 'Study Guides', formats: ['cheat-sheets', 'flashcards', 'interactive-practice-test'] },
    { id: 'worksheets', name: 'Printable Worksheets', formats: ['partner-checks', 'mazes', 'color-by-number', 'error-analysis', 'stations', 'whodunnit', 'tarsia', 'assessment-menus', 'other'] }
  ];
  var FORMAT_SUMMARIES = {
    'lesson-planner': 'Plan a day: Do Now, notes, practice and exit ticket from the 180-day scope and sequence.',
    'worksheet-generator': 'Choose skills and create customized printable worksheets with answer keys.',
    'assessment-generator': 'Build a test or a menu assessment with verified answer keys.',
    'printable-generator': 'Make mazes, color-by-number pages, Tarsia puzzles, error analysis and partner checks with answer keys.',
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
    'interactive-practice-test': 'Take a unit-style assessment, identify weak skills, and check your improvement.',
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
    return '<div class="resource-columns">' + RESOURCE_GROUPS.filter(function (group) { return group.id !== 'worksheets'; }).map(function (group) {
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
    sixth:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="28" y="23" width="144" height="112" rx="8"/>' +
      '<path class="s-thin" d="M 43 57 H 157 M 43 96 H 157 M 80 36 V 123 M 119 36 V 123"/>' +
      '<circle class="f" cx="61" cy="46" r="8"/><circle class="f" cx="99" cy="46" r="8"/><circle class="f" cx="138" cy="46" r="8"/>' +
      '<path class="s" d="M 54 83 H 106 M 80 68 V 97 M 128 82 H 153 M 128 91 H 153"/>' +
      '</svg>',
    seventh:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="20" y="28" width="160" height="105" rx="8"/>' +
      '<path class="s" d="M 39 70 H 162 M 99 43 V 113"/>' +
      '<text x="63" y="61" text-anchor="middle" font-size="25" font-weight="800" fill="currentColor">3</text>' +
      '<text x="137" y="61" text-anchor="middle" font-size="25" font-weight="800" fill="currentColor">4</text>' +
      '<text x="99" y="105" text-anchor="middle" font-size="27" font-weight="800" fill="currentColor">7</text>' +
      '</svg>',
    eighth:
      '<svg class="art" viewBox="0 0 200 160" aria-hidden="true" focusable="false">' +
      '<rect class="f-soft" x="25" y="23" width="150" height="114" rx="8"/>' +
      '<path class="s" d="M 47 79 H 150 M 53 49 L 103 79 L 151 40"/>' +
      '<circle class="f" cx="53" cy="49" r="7"/><circle class="f" cx="103" cy="79" r="7"/><circle class="f" cx="151" cy="40" r="7"/>' +
      '<path class="s-thin" d="M 103 79 L 103 113 M 47 113 H 150"/>' +
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
  function artFor(c) { var byCourse = { math6: 'sixth', prealgebra7: 'seventh', prealgebra: 'eighth', algebra: 'linear', geometry: 'triangle', algebra2: 'curve' }; return ART[byCourse[c.id] || c.art] || ''; }

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

  function activityUrl(a) { return /^worksheet-generator\/[a-z0-9_\-/]+\.html(#unit=[a-z0-9\-]+(&kind=[a-z]+)?)?$/i.test(a.path || '') ? a.path : 'activity.html?path=' + encodeURIComponent(a.path); }

  function actionLabel(a) {
    var format = activityFormat(a);
    if (/worksheet-generator\/printables\.html/.test(a.path || '')) return 'Make printable';
    if (format === 'lesson-planner') return 'Plan a day';
    if (format === 'worksheet-generator') return 'Create worksheet';
    if (format === 'assessment-generator') return 'Build assessment';
    if (format === 'cheat-sheets') return 'View study guide';
    if (format === 'interactive-practice-test') return 'Take practice test';
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
      '<a class="thumb" href="' + esc(activityUrl(a)) + '" tabindex="-1" aria-hidden="true">' +
        (a.thumb ? '<img src="' + esc(a.thumb) + '" alt="" loading="lazy">' : '') + '</a>' +
      '<div class="card-body">' +
        (showWhere ? '<p class="where">' + esc(it.c.name) + ', ' + esc(unitLabel(it.c, it.u)) + '</p>' : '') +
        '<h3><a href="' + esc(activityUrl(a)) + '">' + esc(a.title) +
          '</a></h3>' +
        (gameMode(a) ? '<span class="game-mode-tag">' + esc(gameMode(a)) + '</span>' : '') +
        '<p class="desc">' + esc(shortDescription(a)) + '</p>' + resourceInfo(a) +
        '<div class="actions"><a class="btn btn-open" href="' + esc(activityUrl(a)) + '">' + esc(actionLabel(a)) + '</a>' +
          saveBtnHtml(a.path) + (/practice-test\.html#unit=([a-z0-9-]+)/i.test(a.path || '') ? '<button type="button" class="btn btn-ghost readiness-activity-share" data-readiness-unit="' + esc(/#unit=([a-z0-9-]+)/i.exec(a.path)[1]) + '">Copy student link</button>' : '') + '</div>' +
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
          '<div class="hero-copy"><p class="hero-eyebrow">MR. K’S CLASSROOM · BUILT FOR TEACHERS</p><h1 tabindex="-1">Less planning.<br><span>More teaching.</span></h1>' +
          '<p class="lede">Create differentiated math lessons, worksheets, activities, and assessments in minutes. Spend less time preparing and more time teaching.</p></div>' +
          '<div class="hero-generator-panel">' + generatorLinks(null, null, false) + '</div>' +
        '</div></section>' +
        '<section class="section explore-courses"><div class="wrap"><div class="explore-heading"><p class="section-kicker">YOUR CLASSROOM</p><h2>Explore by subject</h2><p>Find curriculum-aligned resources and tools for every unit.</p></div><ul class="courses">' +
          L.courses.map(function (c) {
            var n = courseCount(c);
            return '<li><a class="course" data-color="' + esc(c.color || '') + '" href="' + href(courseToken(c)) + '">' +
              '<h3>' + esc(c.name) + '</h3><p>' + esc(c.blurb || '') + '</p>' +
              '<p class="count">' + (n ? units(unitsWithActivities(c)) + ' ready to explore' : 'Coming soon') + '</p>' +
              artFor(c) + '</a></li>';
          }).join('') + SOON.map(function (c) {
            return '<li><div class="course soon" data-color="' + esc(c.color || '') + '" aria-disabled="true">' +
              '<h3>' + esc(c.name) + '</h3><p>' + esc(c.blurb || '') + '</p><p class="count">Coming soon</p>' + artFor(c) + '</div></li>';
          }).join('') + '</ul></div></section>' +
        '<section class="section more-resources-section"><div class="wrap"><div class="more-resources-heading"><div><p class="section-kicker">BEYOND THE GENERATORS</p><h2>Explore more resources</h2><p>Ready-to-use ways to practice, review, and reinforce skills.</p></div><a class="more-resources-all" href="#activities?subject=algebra">Browse all resources →</a></div>' +
        '<div class="more-resource-links">' +
          '<a class="more-resource-link" href="#activities?subject=algebra&category=games"><span class="more-resource-symbol" aria-hidden="true">◈</span><span><strong>Games</strong><small>Interactive challenges, team competitions, and engaging review.</small></span><span class="more-resource-arrow" aria-hidden="true">→</span></a>' +
          '<a class="more-resource-link" href="#activities?subject=algebra&category=study-guides"><span class="more-resource-symbol" aria-hidden="true">▤</span><span><strong>Study Guides</strong><small>Helpful reference sheets, worked examples, and review resources.</small></span><span class="more-resource-arrow" aria-hidden="true">→</span></a>' +
        '</div></div></section>'
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

  function subskillsHtml(u, courseId) {
    var skills = window.MK_COURSE_CATALOG.getSkills(courseId, u.id);
    function lines(list) {
      return '<ul class="unit-skills">' + list.map(function (skill) {
        return '<li class="unit-skill">' + esc(skill) + '</li>';
      }).join('') + '</ul>';
    }
    if (skills.length <= 4) return lines(skills);
    return lines(skills.slice(0, 4)) +
      '<details class="unit-lesson-details"><summary><span class="show-label">Show all ' + skills.length + ' lessons</span>' +
      '<span class="hide-label">Show fewer lessons</span></summary>' +
      lines(skills.slice(4)) + '</details>';
  }

  function lessonCount(c) {
    return c.units.reduce(function (sum, unit) {
      return sum + window.MK_COURSE_CATALOG.getSkills(c.id, unit.id).length;
    }, 0);
  }
  function courseView(c) {
    var n = courseCount(c);
    var inner =
      '<div class="band-grid"><div>' +
        crumbs([['Home', '#'], [c.name, null]]) +
        '<h1 tabindex="-1">' + esc(c.name) + '</h1>' +
        (c.blurb ? '<p class="band-blurb">' + esc(c.blurb) + '</p>' : '') +
        '<p class="band-meta">' + ((c.id === 'math6' || c.id === 'prealgebra7' || c.id === 'prealgebra') ? units(c.units.length) + ' with ' + lessonCount(c) + ' lessons; interactive practice available for selected topics' : (c.id === 'algebra' || c.id === 'geometry' || c.id === 'algebra2') ? units(c.units.length) + ' with skills, generators, games, and study guides' : (n ? acts(n) + ' in ' + unitsWithActivities(c) + ' of ' + units(c.units.length) : units(c.units.length) + ', activities coming soon')) + '</p>' +
      '</div>' + (c.art ? '<div class="band-art" aria-hidden="true">' + artFor(c) + '</div>' : '') + '</div>';
    return {
      title: c.name,
      html: bandHtml(c, inner) +
        ((c.id === 'math6' || c.id === 'prealgebra' || c.id === 'prealgebra7') ? '' : '<section class="section"><div class="wrap">' + generatorLinks(c, null, true) + '</div></section>') +
        '<section class="section"><div class="wrap"><h2 class="course-units-title">Browse by unit</h2><ul class="units">' +
        c.units.map(function (u) {
          var k = u.artifacts.length;
          if (!k && c.id !== 'geometry' && c.id !== 'algebra2' && c.id !== 'prealgebra' && c.id !== 'prealgebra7' && c.id !== 'math6') {
            return '<li><div class="unit soon" data-color="' + esc(c.color || '') + '"><h3>' + '<span class="unit-num">Unit ' + unitNum(c, u) + '</span>' + esc(u.name) + '</h3>' +
              '<div class="unit-meta"><span class="unit-count">Coming soon</span></div></div></li>';
          }
          var minis = u.artifacts.slice(0, 3).filter(function (a) { return a.thumb; }).map(function (a) {
            return '<img src="' + esc(a.thumb) + '" alt="" loading="lazy">';
          }).join('');
          if (c.id === 'algebra' || c.id === 'geometry' || c.id === 'algebra2' || c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6') {
            return '<li><div class="unit algebra-unit-card" data-color="' + esc(c.color || '') + '">' +
              '<h3><a class="unit-title-link" href="' + href(unitToken(c, u)) + '">' +
              '<span class="unit-num">Unit ' + unitNum(c, u) + '</span>' + esc(u.name) + '</a></h3>' +
              '<div class="unit-meta" data-lesson-list="true">' + subskillsHtml(u, c.id) + '</div>' +
              '<a class="unit-open-link" href="' + href(unitToken(c, u)) + '">Open unit →</a></div></li>';
          }
          return '<li><a class="unit" data-color="' + esc(c.color || '') + '" href="' + href(unitToken(c, u)) + '"><h3>' + '<span class="unit-num">Unit ' + unitNum(c, u) + '</span>' + esc(u.name) + '</h3>' +
            '<div class="unit-meta"><span class="unit-count">' + acts(k) + '</span>' + (minis ? '<span class="minis">' + minis + '</span>' : '') + '</div></a></li>';
        }).join('') + '</ul></div></section>'
    };
  }

  /* Algebra 1 unit pages prioritize the four creation tools; legacy printables remain
     in the library, global search, and activity browser rather than being duplicated here. */
  var GENERATOR_ACTIONS = [
    { format: 'lesson-planner', title: 'Lesson Plan', icon: '📖', description: 'Objectives, notes, examples, practice, and exit tickets.', page: 'lesson-planner.html' },
    { format: 'worksheet-generator', title: 'Worksheet', icon: '📝', description: 'Differentiated questions, versions, and answer keys.', page: 'worksheet.html' },
    { format: 'printable-generator', title: 'Activity', icon: '🧩', description: 'Mazes, puzzles, partner checks, and more.', page: 'printables.html' },
    { format: 'assessment-generator', title: 'Assessment', icon: '📋', description: 'Tests and choice-based assessments.', page: 'menu-assessment.html' }
  ];
  function generatorLinks(c, u, compact) {
    var items = u ? u.artifacts : [];
    var unitId = '';
    if (u) {
      if (c.id === 'geometry') {
        items.some(function (a) { var m = /#unit=([a-z0-9-]+)/.exec(a.path || ''); if (m) { unitId = m[1]; return true; } return false; });
      } else unitId = 'algebra1-' + u.id;
    }
    return '<div class="generator-banner' + (compact ? ' compact' : '') + '">' +
      '<div class="generator-banner-heading"><h2>' + (compact ? (u ? 'Create Resources for This Unit' : 'Create Resources for This Course') : 'What would you like to do today?') + '</h2>' +
      (!compact ? '<p>Choose a generator, select your unit, and make classroom-ready resources.</p>' : '') + '</div>' +
      '<ul class="generator-shortcuts">' + GENERATOR_ACTIONS.map(function (tool) {
        var match = items.filter(function (a) { return activityFormat(a) === tool.format; })[0];
        var url = match ? activityUrl(match) : 'worksheet-generator/' + tool.page;
        if (c && c.id === 'geometry') {
          var supported = !u || !!unitId;
          if (!supported) return '<li><span class="generator-shortcut" aria-disabled="true" title="Geometry question banks still in development"><span class="generator-shortcut-icon" aria-hidden="true">◌</span><span class="generator-shortcut-copy"><strong>' + esc(tool.title) + '</strong><small>Coming soon</small></span></span></li>';
          url = 'worksheet-generator/' + tool.page + (unitId ? '#unit=' + unitId : '');
        }
        if (match && tool.format === 'printable-generator') url = url.replace(/&kind=[a-z]+$/, '');
        return '<li><a class="generator-shortcut" href="' + esc(url) + '">' +
          '<span class="generator-shortcut-icon" aria-hidden="true">' + ({'lesson-planner':'▤','worksheet-generator':'≡','printable-generator':'✦','assessment-generator':'☑'}[tool.format]) + '</span>' +
          '<span class="generator-shortcut-copy"><strong>' + (compact ? esc(tool.title) : 'Create a ' + esc(tool.title)) + '</strong>' +
          (!compact ? '<small>' + esc(tool.description) + '</small>' : '') +
          '</span></a></li>';
      }).join('') + '</ul></div>';
  }
  function unitPager(c, u) {
    var list = c.units.filter(function (x) { return x === u || x.artifacts.length || c.id === 'geometry' || c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6' || c.id === 'algebra2'; });
    var i = list.indexOf(u);
    if (list.length < 2) return '';
    function link(t, dir) {
      if (!t) return '<span class="pager-spot"></span>';
      var arrow = '<span class="pager-arrow" aria-hidden="true">' + (dir === 'prev' ? '&larr;' : '&rarr;') + '</span>';
      var text = '<span class="pager-text"><span class="pager-dir">' + (dir === 'prev' ? 'Previous unit' : 'Next unit') + '</span>' +
        '<span class="pager-name">' + esc(unitLabel(c, t)) + '</span></span>';
      return '<a class="pager-link pager-' + dir + '" href="' + href(unitToken(c, t)) + '" rel="' + dir + '">' +
        (dir === 'prev' ? arrow + text : text + arrow) + '</a>';
    }
    return '<nav class="unit-pager" data-color="' + esc(c.color || '') + '" aria-label="Unit navigation">' +
      link(list[i - 1], 'prev') + link(list[i + 1], 'next') + '</nav>';
  }
  function algebraUnitView(c, u) {
    var items = u.artifacts.map(function (a) { return { a: a, c: c, u: u }; });
    var gameFormats = RESOURCE_GROUPS.filter(function (g) { return g.id === 'games'; })[0].formats;
    var guideFormats = RESOURCE_GROUPS.filter(function (g) { return g.id === 'study-guides'; })[0].formats;
    // Unit pages must expose the online practice test directly, just like the global directory.
    // Keep one card per unit even when older cached catalogs or format filters are in use.
    var hasPractice = c.id === 'geometry' || items.some(function(it){return /practice-test[.]html/i.test(it.a.path||'');});
    if (!hasPractice) {
      var unitMap = {'foundations-algebra':'algebra1-foundations','expressions-equations':'algebra1-expressions-equations','inequalities':'algebra1-inequalities','relations-functions':'algebra1-relations-functions','linear-equations-slope':'algebra1-linear-equations-slope','systems-of-equations':'algebra1-systems-of-equations','exponents-exponential-functions':'algebra1-exponents-scientific-notation','exponential-functions':'algebra1-exponential-functions','polynomials-factoring':'algebra1-polynomials','factoring-zero-product':'algebra1-factoring-zero-product','quadratics':'algebra1-quadratics','statistics-data-modeling':'algebra1-statistics-data-modeling'};
      if(unitMap[u.id]) items.push({a:{title:'Interactive Practice Test',path:'worksheet-generator/practice-test.html#unit='+unitMap[u.id],thumb:'thumbs/practice-test.svg',description:'Online practice assessment with worked solutions and targeted skill review.',type:'Study Guide'},c:c,u:u});
    }
    function category(id, title, formats) {
      var matches = items.filter(function (it) { return formats.indexOf(activityFormat(it.a)) >= 0; });
      // Include the practice test deterministically in each supported Algebra 1 unit.
      // Use the same card renderer and thumbnail as the other study guides.
      if (id === 'study-guides') {
        var current = items.filter(function (it) { return /practice-test[.]html/i.test(it.a.path || ''); });
        if (current.length && !matches.some(function (it) { return /practice-test[.]html/i.test(it.a.path || ''); })) matches.push(current[0]);
      }
      if (!matches.length) return '';
      return '<section class="algebra-unit-section" aria-labelledby="algebra-' + id + '">' +
        '<h2 id="algebra-' + id + '">' + esc(title) + '</h2>' +
        '<ul class="cards grouped-cards">' + matches.map(function (it) { return cardHtml(it, false, true); }).join('') + '</ul>' +
        '</section>';
    }
    var inner = crumbs([['Home', '#'], [c.name, href(courseToken(c))], [unitLabel(c, u), null]]) +
      '<h1 tabindex="-1">' + esc(unitLabel(c, u)) + '</h1>' +
      '<p class="band-meta">Create custom resources or explore games and study guides for this unit.</p>';
    return {
      title: unitLabel(c, u) + ', ' + c.name,
      html: bandHtml(c, inner) +
        '<section class="section"><div class="wrap algebra-unit-layout">' + unitPager(c, u) +
        generatorLinks(c, u, true) +
        category('games', 'Games', gameFormats) +
        category('study-guides', 'Study Guides', guideFormats) +
        (c.id === 'algebra2' ? contentBriefSection(c, u) + contentReadinessSection(c, u) : '') +
        unitPager(c, u) + '</div></section>'
    };
  }

  function contentReadinessSection(c, u) {
    var list = [
      ['flashcards', 'Flashcards'], ['connect-4', 'Connect 4'],
      ['tic-tac-toe', 'Tic-Tac-Toe'], ['picture-reveal', 'Picture Reveal'],
      ['showdown', 'Showdown'], ['detective', 'Detective'],
      ['escape-room', 'Escape Rooms'], ['worksheets', 'Worksheets'],
      ['assessments', 'Assessments'], ['readiness-check', 'Assessment Readiness Check']
    ];
    var adapter = window.MK_RESOURCE_ELIGIBILITY;
    return '<section class="algebra-unit-section"><h2>Content readiness</h2>' +
      '<p class="course-skill-hint">Future resources share the same approved question bank. This checks the new bank system only; it does not evaluate existing legacy resources.</p>' +
      '<div class="resource-readiness-grid">' + list.map(function (item) {
        var status = adapter.describe(item[0], c.id, u.id);
        return '<div class="resource-readiness-row"><strong>' + esc(item[1]) + '</strong><span>' +
          (status.ready ? status.count + ' approved questions' : 'Awaiting approved questions') + '</span>' +
          (item[0] === 'flashcards' && status.ready ? '<a href="worksheet-generator/approved-flashcards.html?course=' + encodeURIComponent(c.id) + '&unit=' + encodeURIComponent(u.id) + '">Open approved flashcards</a>' : '') +
          (['connect-4', 'tic-tac-toe', 'picture-reveal'].indexOf(item[0]) >= 0 && status.ready ? '<a href="worksheet-generator/approved-games.html?course=' + encodeURIComponent(c.id) + '&unit=' + encodeURIComponent(u.id) + '">Open approved review games</a>' : '') + '</div>';
      }).join('') + '</div></section>';
  }
  function contentBriefSection(c, u) {
    var skills = window.MK_COURSE_CATALOG.getSkillRecords(c.id, u.id);
    return '<section class="algebra-unit-section"><h2>Lessons and Subskills</h2>' +
      '<p class="course-skill-hint">Select lessons for a content brief. <a href="coverage.html?course=' + encodeURIComponent(c.id) + '">View course question coverage</a>.</p>' +
      '<div class="course-skill-actions"><button type="button" class="course-skill-select" data-skill-action="all">Select all</button><button type="button" class="course-skill-select" data-skill-action="none">Clear</button><button type="button" class="course-skill-select" data-skill-action="copy">Copy content brief</button><span class="course-skill-status" role="status" aria-live="polite"></span></div>' +
      '<ol class="course-skill-checklist" data-course-id="' + esc(c.id) + '" data-unit-id="' + esc(u.id) + '">' + skills.map(function (s) {return '<li><label><input type="checkbox" value="' + esc(s.id) + '" checked><span>' + esc(s.name) + '</span></label></li>';}).join('') + '</ol></section>';
  }
  function gradePracticeLinks(c, u) {
    var crosswalk = window.MK_SKILL_CROSSWALK;
    if (!crosswalk || typeof crosswalk.matches !== 'function') return '';
    var topics = crosswalk.matches().filter(function (m) {
      return m.targets.some(function (t) { return t && t.courseId === c.id && t.unitId === u.id; });
    });
    if (!topics.length) return '';
    return '<section class="algebra-unit-section"><h2>Interactive Practice</h2>' +
      '<p>Practice questions with immediate answer feedback, organized by lesson topic.</p>' +
      '<ul class="cards grouped-cards">' + topics.map(function (m) {
        var target = m.targets.find(function (t) { return t && t.courseId === c.id && t.unitId === u.id; });
        var url = 'worksheet-generator/grade-practice.html?course=' + encodeURIComponent(c.id) +
          '&topic=' + encodeURIComponent(m.key) + '&level=cp1';
        return '<li class="card"><strong>' + esc(target.name) + '</strong><p>' +
          [['practice','Practice'],['flashcards','Flashcards'],['game','Review game'],['worksheet','Worksheet']].map(function(format){
            return '<a style="display:inline-block;margin:.25rem .75rem .25rem 0" href="' + esc(url+'&mode='+format) + '">' + esc(format==='game'?'Review Game':format==='practice'?'Practice':format==='worksheet'?'Worksheet':'Flashcards') + '</a>';
          }).join('') + '</p></li>';
      }).join('') + '</ul></section>';
  }
  function unitView(c, u) {
    if (c.id === 'prealgebra' || c.id === 'prealgebra7' || c.id === 'math6') {
      var skills = window.MK_COURSE_CATALOG.getSkillRecords(c.id, u.id);
      var intro = crumbs([['Home', '#'], [c.name, href(courseToken(c))], [unitLabel(c, u), null]]) +
        '<h1 tabindex="-1">' + esc(unitLabel(c, u)) + '</h1>' +
        '<p class="band-meta">' + skills.length + ' lessons · ' + esc(c.name) + ' curriculum</p>';
      return { title: unitLabel(c, u) + ', ' + c.name,
        html: bandHtml(c, intro) + '<section class="section"><div class="wrap algebra-unit-layout">' +
          unitPager(c, u) + gradePracticeLinks(c, u) + contentBriefSection(c, u) + contentReadinessSection(c, u) +
          '<section class="algebra-unit-section"><h2>More resources in development</h2>' +
          '<p>Additional worksheet generators, review games, and study guides are planned for this unit.</p></section>' +
          unitPager(c, u) + '</div></section>' };
    }
    if (c.id === 'algebra' || c.id === 'geometry' || c.id === 'algebra2') return algebraUnitView(c, u);
    var items = u.artifacts.map(function (a) { return { a: a, c: c, u: u }; });
    var planner = u.artifacts.filter(function (a) { return activityFormat(a) === 'lesson-planner'; })[0];
    var generator = u.artifacts.filter(function (a) { return activityFormat(a) === 'worksheet-generator'; })[0];
    var menuGen = u.artifacts.filter(function (a) { return activityFormat(a) === 'assessment-generator'; })[0];
    var inner =
      crumbs([['Home', '#'], [c.name, href(courseToken(c))], [unitLabel(c, u), null]]) +
      '<h1 tabindex="-1">' + esc(unitLabel(c, u)) + '</h1>' +
      '<p class="band-meta">' + (items.length ? acts(items.length) : 'Coming soon') + '</p>' +
      (planner ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(planner)) + '">Plan a lesson</a><p>Pick any day of this unit: objectives, vocabulary, Do Now, notes, practice and exit ticket, printed as a student handout and a teacher key.</p></div>' : '') +
      (generator ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(generator)) + '">Create a worksheet</a><p>Practice with short-answer or multiple-choice questions. Choose skills and CP2, CP1 or Honors difficulty; prints with an answer key.</p></div>' : '') +
      (menuGen ? '<div class="unit-generator"><a class="btn" href="' + esc(activityUrl(menuGen)) + '">Build an assessment</a><p>A standard test (multiple choice and short answer) or a choice menu. Choose skills and CP2, CP1 or Honors difficulty, then edit every problem before you print.</p></div>' : '');
    return {
      title: unitLabel(c, u) + ', ' + c.name,
      html: bandHtml(c, inner) +
        '<section class="section"><div class="wrap">' + unitPager(c, u) +
        (items.length ? chipsHtml(items) + groupedCardsHtml(items, false)
                      : '<div class="empty"><h2>Coming soon</h2><p>No activities in this unit yet. <a href="' + href(courseToken(c)) + '">Back to ' + esc(c.name) + '</a></p></div>') +
        unitPager(c, u) + '</div></section>'
    };
  }


  function browseState(defaultFormat) {
    var params = new URLSearchParams(token.split('?')[1] || '');
    return { subject: params.get('subject') || '', unit: params.get('unit') || '', category: params.get('category') || '', gameMode: params.get('gameMode') || '',
      format: params.get('format') || defaultFormat || '', page: Math.max(1, parseInt(params.get('page'), 10) || 1) };
  }
  function browseToken(state) {
    var params = new URLSearchParams();
    ['subject', 'unit', 'category', 'format', 'gameMode'].forEach(function (key) { if (state[key]) params.set(key, state[key]); });
    if (state.page > 1) params.set('page', state.page);
    return 'activities' + (params.toString() ? '?' + params.toString() : '');
  }
  function browseResults(state) {
    return everything().filter(function (it) {
      return (!state.subject || it.c.id === state.subject) &&
        (!state.unit || unitToken(it.c, it.u) === state.unit) &&
        (!state.category || RESOURCE_GROUPS.some(function (g) { return g.id === state.category && g.formats.indexOf(activityFormat(it.a)) >= 0; })) &&
        (!state.format || activityFormat(it.a) === state.format) &&
        (!state.gameMode || gameMode(it.a) === state.gameMode);
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
        id: unitToken(c, u), name: (state.subject ? '' : c.name + ' — ') + unitLabel(c, u)
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
      browseSelect('category', 'Category', RESOURCE_GROUPS.map(function (g) { return { id: g.id, name: g.name }; }), state.category, 'All categories') +
      browseSelect('format', 'Activity Type', formats, state.format, 'All activity types') +
      ((state.category === 'games' || state.gameMode) ? browseSelect('gameMode', 'Game Mode', GAME_MODES.map(function (name) { return { id: name, name: name }; }), state.gameMode, 'All game modes') : '') +
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
      var hay = searchWords([it.a.title, it.a.description, it.u.name, 'unit ' + unitNum(it.c, it.u), it.c.name, format ? format.name : '']
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

  function soonView(c) {
    return {
      title: c.name + ': coming soon',
      html: bandHtml(c, '<h1 tabindex="-1">' + esc(c.name) + '</h1>') +
        '<section class="section"><div class="wrap"><div class="empty"><h2>Coming soon</h2><p>' + esc(c.name) + ' activities are being rebuilt in the same style as Algebra 1. <a href="#algebra">Browse Algebra 1</a> in the meantime.</p></div></div></section>'
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
    var hid = SOON.filter(function (x) { return x.id === parts[0]; })[0];
    if (!c && hid) return { name: 'soon', c: hid };
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
    }).join('') + SOON.map(function (c) { return '<span class="soon-link" title="Coming soon">' + esc(c.name) + ' <small>Coming soon</small></span>'; }).join('');
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
    else if (r.name === 'soon') view = soonView(r.c);
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
    var skillButton = e.target.closest ? e.target.closest('[data-skill-action]') : null;
    if (skillButton) {
      var list = app.querySelector('.course-skill-checklist');
      if (!list) return;
      var checks = Array.prototype.slice.call(list.querySelectorAll('input[type="checkbox"]'));
      var action = skillButton.getAttribute('data-skill-action');
      if (action === 'all' || action === 'none') { checks.forEach(function (input) { input.checked = action === 'all'; }); return; }
      if (action === 'copy') {
        var courseId = list.getAttribute('data-course-id'), unitId = list.getAttribute('data-unit-id');
        var records = window.MK_COURSE_CATALOG.getSkillRecords(courseId, unitId);
        var chosen = checks.filter(function (input) { return input.checked; }).map(function (input) { return records.filter(function (s) { return s.id === input.value; })[0]; }).filter(Boolean);
        var status = app.querySelector('.course-skill-status');
        if (!chosen.length) { if (status) status.textContent = 'Select at least one lesson.'; return; }
        var course = L.courses.filter(function (item) { return item.id === courseId; })[0];
        var unit = course && course.units.filter(function (item) { return item.id === unitId; })[0];
        var brief = JSON.stringify({schemaVersion:1,courseId:courseId,courseName:course.name,unitId:unitId,unitName:unit.name,selectedSkills:chosen,difficulties:['cp2','cp1','honors'],formats:['short-answer','multiple-choice','select-all','open-response'],requirements:['Generate verified answers and worked solutions','Multiple-choice answers and distractors must be independently checked','Open-response questions must contain at least four parts','Supply precise diagram specifications where needed','Do not modify existing course question banks'],questionBankSchema:'schemas/question-bank.schema.json'},null,2);
        function fallback() {
          var box = document.createElement('textarea'); box.value = brief; box.style.position = 'fixed'; box.style.opacity = '0'; document.body.appendChild(box); box.select();
          var ok = false; try { ok = document.execCommand('copy'); } catch (_) {}
          document.body.removeChild(box); if (status) status.textContent = ok ? 'Content brief copied.' : 'Copy unavailable in this browser.';
        }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(brief).then(function(){if(status) status.textContent='Content brief copied.';}, fallback);
        else fallback();
        return;
      }
    }
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
  /* Back: the previous page in this tab (course, unit, browse page or search); home when there is none. */
  var backBtn = document.getElementById('backBtn');
  if (backBtn) backBtn.addEventListener('click', function () {
    var fromSite = document.referrer && document.referrer.indexOf(location.origin) === 0;
    if (history.length > 1 && (fromSite || (history.state && history.state.mk) || sessionStorageGet())) history.back();
    else if (location.hash && location.hash !== '#') location.hash = '';
    else history.back();
  });
  function sessionStorageGet() { try { return sessionStorage.getItem('mk-nav') === '1'; } catch (e) { return false; } }
  window.addEventListener('hashchange', function () { try { sessionStorage.setItem('mk-nav', '1'); } catch (e) { /* ignore */ } });
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

  window.addEventListener('mk-banks-ready', function () { if (!query && resolve(token).name === 'unit') render(true); });

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
