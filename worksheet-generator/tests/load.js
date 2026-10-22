/* Loads the generator (no DOM needed) the same way the browser pages do. */
'use strict';
const path = require('path');
const root = path.join(__dirname, '..');
const files = [
  'core/rng', 'core/frac', 'core/tex', 'core/graph', 'core/framework',
  'units/algebra1/linear-functions/common',
  'units/algebra1/linear-functions/lessons-slope', 'units/algebra1/linear-functions/lessons-graphing',
  'units/algebra1/linear-functions/lessons-writing', 'units/algebra1/linear-functions/lessons-forms',
  'units/algebra1/linear-functions/lessons-applications', 'units/algebra1/linear-functions/index'
];
files.forEach(f => require(path.join(root, f + '.js')));
module.exports = globalThis.MKWS;
