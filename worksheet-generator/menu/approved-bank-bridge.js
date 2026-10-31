/* Approved content bridge for the native worksheet and assessment pages.
 * This is a read-only content API, NOT a math generator or an MKMENU skill set.
 * Only banks approved in the manifest pass through the existing validator.
 */
(function (root) {
  'use strict';
  var validResources = {
    worksheet: ['short-answer', 'multiple-choice'],
    assessment: ['short-answer', 'multiple-choice', 'select-all', 'open-response'],
    flashcards: ['short-answer', 'multiple-choice'],
    games: ['multiple-choice']
  };
  var status = { state: 'loading', units: [], error: null };
  var ready = Promise.resolve().then(function () {
    if (!root.MK_BANK_LOADER || !root.MK_QUESTION_BANKS)
      throw new Error('Approved question-bank dependencies are unavailable');
    return root.MK_BANK_LOADER.loadFromSite('question-banks/manifest.json', '../');
  }).then(function (units) {
    status = { state: 'ready', units: units.slice(), error: null };
    return status;
  }, function (error) {
    status = { state: 'error', units: [], error: String(error && error.message || error) };
    return status;
  });
  function select(resource, options) {
    options = options || {};
    if (status.state !== 'ready' || !validResources[resource]) return [];
    if (!options.courseId || !options.unitId) return [];
    var permitted = validResources[resource];
    var formats = options.formats
      ? options.formats.filter(function (f) { return permitted.indexOf(f) >= 0; })
      : permitted;
    if (!formats.length) return [];
    return root.MK_QUESTION_BANKS.select({
      courseId: options.courseId, unitId: options.unitId,
      level: options.level, skillIds: options.skillIds, formats: formats,
      limit: options.limit
    });
  }
  function available(courseId, unitId) {
    return status.state === 'ready' &&
      root.MK_QUESTION_BANKS.available(courseId, unitId);
  }
  root.MK_APPROVED_RESOURCE_BANKS = {
    version: 1, ready: ready,
    status: function () { return { state: status.state, units: status.units.slice(), error: status.error }; },
    available: available,
    select: select
  };
})(typeof window !== 'undefined' ? window : globalThis);
