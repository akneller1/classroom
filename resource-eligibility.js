/* Shared resource eligibility for approved question-bank content.
 * Existing games stay unchanged until an explicit adapter is added.
 * No grade-specific mathematics or diagrams are generated here.
 */
(function (root) {
  'use strict';
  var bank = root.MK_QUESTION_BANKS;
  var RULES = {
    flashcards: ['short-answer','multiple-choice'],
    'connect-4': ['short-answer','multiple-choice'],
    'tic-tac-toe': ['short-answer','multiple-choice'],
    'picture-reveal': ['short-answer','multiple-choice'],
    'showdown': ['short-answer','multiple-choice','select-all'],
    'detective': ['short-answer','multiple-choice'],
    'escape-room': ['short-answer','multiple-choice'],
    worksheets: ['short-answer','multiple-choice','select-all','open-response'],
    assessments: ['short-answer','multiple-choice','select-all','open-response'],
    'readiness-check': ['short-answer','multiple-choice','select-all','open-response']
  };
  function describe(activity, courseId, unitId, level, skillIds) {
    if (!Object.prototype.hasOwnProperty.call(RULES, activity)) return {ready:false,count:0,reason:'Unsupported activity type',questions:[]};
    if (!bank || !bank.available(courseId,unitId)) return {ready:false,count:0,reason:'No approved question bank for this unit',questions:[]};
    var questions = bank.select({courseId:courseId,unitId:unitId,skillIds:skillIds,level:level,formats:RULES[activity]});
    return {ready:questions.length>0,count:questions.length,reason:questions.length?'':'No approved questions matching these skills or difficulty',questions:questions};
  }
  root.MK_RESOURCE_ELIGIBILITY={version:1,formats:RULES,describe:describe};
})(typeof window !== 'undefined' ? window : globalThis);
