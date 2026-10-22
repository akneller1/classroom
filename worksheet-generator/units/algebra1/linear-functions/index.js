/* Algebra 1 — Linear Functions: unit catalog.  Adding another unit (for example Geometry or
   Algebra 2) means creating a sibling folder under units/ that calls registerUnit and
   registerLesson, plus a small HTML page that loads it. Nothing in core/ changes. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  NS.registerUnit({
    id: 'algebra1-linear-functions', course: 'Algebra 1', color: 'blue', name: 'Linear Functions',
    defaultTitle: 'Linear Functions Practice',
    categories: [
      { id: 'slope', letter: 'A', name: 'Slope', lessons: ['lf-slope-two-points', 'lf-slope-graph', 'lf-slope-table', 'lf-slope-missing-coordinate', 'lf-slope-classify'] },
      { id: 'graphing', letter: 'B', name: 'Graphing Linear Equations', lessons: ['lf-graph-slope-intercept', 'lf-graph-table', 'lf-graph-intercepts', 'lf-graph-horizontal-vertical'] },
      { id: 'writing', letter: 'C', name: 'Writing Linear Equations', lessons: ['lf-write-from-graph', 'lf-write-two-points', 'lf-write-slope-point', 'lf-write-parallel-perpendicular'] },
      { id: 'forms', letter: 'D', name: 'Forms of Linear Equations', lessons: ['lf-identify-slope-intercept', 'lf-std-to-slope-intercept', 'lf-slope-intercept-to-std', 'lf-write-point-slope', 'lf-point-slope-to-slope-intercept'] },
      { id: 'applications', letter: 'E', name: 'Applications', lessons: ['lf-interpret-slope-intercept', 'lf-word-problems', 'lf-compare-functions'] }
    ]
  });
})(typeof window !== 'undefined' ? window : globalThis);
