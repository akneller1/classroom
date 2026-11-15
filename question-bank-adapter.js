/* Shared, read-only question bank adapter.
 * No grade-specific math, diagrams, or question generation lives here.
 * A bank is NOT student-ready unless explicitly marked verified after external review.
 */
(function (root) {
  'use strict';
  var catalog = root.MK_COURSE_CATALOG;
  var banks = Object.create(null);
  var FORMATS = ['short-answer', 'multiple-choice', 'select-all', 'open-response', 'plot'];
  var LEVELS = ['cp2', 'cp1', 'honors'];
  function copy(value) { return JSON.parse(JSON.stringify(value)); }
  function key(courseId, unitId) { return courseId + '/' + unitId; }
  // Correct singular agreement in authored word problems without changing answers,
  // checks or problem counts. This covers every consumer of the shared banks:
  // worksheets, assessments, stations, games and study guides.
  var singularNouns = {
    apples:'apple', balls:'ball', beads:'bead', blocks:'block', books:'book', boxes:'box',
    cars:'car', crayons:'crayon', pens:'pen', rocks:'rock', shells:'shell', stickers:'sticker',
    marbles:'marble', buttons:'button', hats:'hat', eggs:'egg', leaves:'leaf', cups:'cup',
    kites:'kite', cookies:'cookie', cats:'cat', dogs:'dog', birds:'bird', ducks:'duck',
    frogs:'frog', bugs:'bug', bees:'bee', counters:'counter', dots:'dot', circles:'circle',
    squares:'square', cubes:'cube', pencils:'pencil', markers:'marker', chairs:'chair',
    students:'student', coins:'coin', toys:'toy'
  };
  function correctProse(s) {
    if (typeof s !== 'string' || !/\bThere are 1\b/i.test(s)) return s;
    return s
      .replace(/\bThere are 1 (red|yellow|blue|green) and (\d+) (red|yellow|blue|green) counters\b/gi,
        function (_, a, n, b) { return 'There is 1 ' + a + ' counter and ' + n + ' ' + b + ' ' + (n === '1' ? 'counter' : 'counters'); })
      .replace(/\bThere are 1 dot and (\d+) dots\b/gi,
        function (_, n) { return 'There is 1 dot and ' + n + ' ' + (n === '1' ? 'dot' : 'dots'); })
      .replace(/\bThere are 1\b/gi, 'There is 1')
      .replace(/\b1\s+((?:(?:more|empty|red|yellow|blue|green|big|small)\s+)?)([a-z]+)\b/gi,
        function (match, qualifier, noun) {
          var singular = singularNouns[noun.toLowerCase()];
          return singular ? '1 ' + qualifier + singular : match;
        });
  }
  function polishProse(value) {
    if (typeof value === 'string') return correctProse(value);
    if (Array.isArray(value)) return value.map(polishProse);
    if (!value || typeof value !== 'object') return value;
    Object.keys(value).forEach(function (field) { value[field] = polishProse(value[field]); });
    return value;
  }
  function validate(bank) {
    var errors = [], seen = Object.create(null);
    if (!bank || typeof bank !== 'object' || bank.schemaVersion !== 1) errors.push('Expected schema version 1.');
    if (!bank || !catalog || !catalog.getSkillRecords) return { ok: false, errors: errors.concat('Course catalog unavailable.') };
    var records = catalog.getSkillRecords(bank.courseId, bank.unitId);
    if (!records.length) errors.push('Unknown course or unit.');
    var skills = Object.create(null);
    records.forEach(function (s) { skills[s.id] = true; });
    if (!Array.isArray(bank.questions)) errors.push('questions must be an array.');
    (Array.isArray(bank.questions) ? bank.questions : []).forEach(function (q, i) {
      var where = 'questions[' + i + ']';
      if (!q || typeof q !== 'object') { errors.push(where + ' invalid'); return; }
      if (typeof q.id !== 'string' || !q.id.trim() || seen[q.id]) errors.push(where + ' missing/duplicate id');
      seen[q.id] = true;
      if (!skills[q.skillId]) errors.push(where + ' unknown skillId');
      if (LEVELS.indexOf(q.level) < 0) errors.push(where + ' invalid level');
      if (FORMATS.indexOf(q.format) < 0) errors.push(where + ' invalid format');
      if (typeof q.prompt !== 'string' || !q.prompt.trim()) errors.push(where + ' missing prompt');
      if (q.answer === undefined || q.answer === null) errors.push(where + ' missing answer');
      if (!Array.isArray(q.solutionSteps) || !q.solutionSteps.length) errors.push(where + ' missing worked steps');
      if (q.format === 'multiple-choice' || q.format === 'select-all') {
        var choices = Array.isArray(q.options) ? q.options : [];
        var n = choices.filter(function (o) { return o && o.correct === true; }).length;
        if (choices.length < 2 || (q.format === 'multiple-choice' && n !== 1) || (q.format === 'select-all' && n < 2)) errors.push(where + ' invalid choices');
      }
      if (q.format === 'open-response' && (!Array.isArray(q.parts) || q.parts.length < 4)) errors.push(where + ' needs four parts');
      if (q.format === 'plot') {
        var plot=q.plot, axis=plot&&(plot.grid||plot.numberLine||(plot.categories&&(plot.key||plot.valueAxis))), tools=['picture-graph','bar-graph','line-plot','number-line-point','points','number-line-inequality','line','system','region','abs','parabola','sqrt','cbrt','exponential'];
        if(!plot||tools.indexOf(plot.tool)<0||!plot.target||!axis||!plot.feedback||!plot.answerKey||typeof plot.answerKey.alt!=='string'||!plot.answerKey.alt.trim()||typeof plot.answerKey.src!=='string'||!/^question-banks\/assets\/[a-zA-Z0-9_/-]+\.png$/.test(plot.answerKey.src)||plot.answerKey.src.includes('..'))errors.push(where+' invalid plot specification');
      }
      if (q.diagram) {
        var d=q.diagram, spec=d.spec||{};
        if (d.type==='image') {
          if (typeof spec.src!=='string' || !spec.src.startsWith('question-banks/assets/') || !/^[a-zA-Z0-9_/-]+[.](png|jpg|jpeg|webp)$/.test(spec.src.slice('question-banks/assets/'.length)) || spec.src.includes('..') || typeof spec.alt!=='string' || !spec.alt.trim())
            errors.push(where+' invalid local image diagram');
        } else if (['svg','coordinate-plane','number-line','geometry-figure'].indexOf(d.type)<0)
          errors.push(where+' unsupported diagram type');
      }
    });
    return { ok: !errors.length, errors: errors };
  }
  function register(bank, opts) {
    var result = validate(bank);
    if (!result.ok) return result;
    var k = key(bank.courseId, bank.unitId);
    if (banks[k]) return { ok: false, errors: ['Bank already registered: ' + k] };
    banks[k] = { data: polishProse(copy(bank)), verified: !!(opts && opts.verified === true) };
    return { ok: true, errors: [], verified: banks[k].verified };
  }
  function available(courseId, unitId, opts) {
    var b = banks[key(courseId, unitId)];
    if (!b) return false;
    return !!(b.verified || (opts && opts.includeUnverified === true));
  }
  function select(options) {
    options = options || {};
    var b = banks[key(options.courseId, options.unitId)];
    if (!b || (!b.verified && options.includeUnverified !== true)) return [];
    var acceptedSkills = options.skillIds && options.skillIds.length ? options.skillIds : null;
    var acceptedFormats = options.formats && options.formats.length ? options.formats : null;
    var questions = b.data.questions.filter(function (q) {
      return (!options.level || q.level === options.level) &&
        (!acceptedSkills || acceptedSkills.indexOf(q.skillId) >= 0) &&
        (!acceptedFormats || acceptedFormats.indexOf(q.format) >= 0);
    });
    return copy(typeof options.limit === 'number' && options.limit >= 0 ? questions.slice(0, options.limit) : questions);
  }
  function coverage(courseId, unitId) {
    var skillRecords = catalog ? catalog.getSkillRecords(courseId, unitId) : [];
    var b = banks[key(courseId, unitId)];
    return skillRecords.map(function (skill) {
      var counts = { cp2: 0, cp1: 0, honors: 0 };
      if (b) b.data.questions.forEach(function (q) { if (q.skillId === skill.id && Object.prototype.hasOwnProperty.call(counts, q.level)) counts[q.level]++; });
      return { id: skill.id, name: skill.name, counts: counts, verified: !!(b && b.verified) };
    });
  }
  root.MK_QUESTION_BANKS = { version: 1, validate: validate, register: register, available: available, select: select, coverage: coverage };
})(typeof window !== 'undefined' ? window : globalThis);
