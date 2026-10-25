/* Loads the menu generator (and the core files it reuses) into a Node VM context. */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const WG = path.resolve(__dirname, '..', '..');
const FILES = ['core/rng.js', 'core/frac.js', 'core/tex.js', 'core/framework.js',
  'menu/mathcheck.js', 'menu/figures.js', 'menu/verify.js', 'menu/engine.js', 'menu/skills/kit.js',
  'menu/skills/algebra1-expressions-equations.js', 'menu/skills/algebra1-inequalities.js',
  'menu/skills/algebra1-relations-functions.js', 'menu/skills/algebra1-exponential-functions.js', 'menu/skills/algebra1-factoring-zero-product.js', 'menu/skills/algebra1-statistics-data-modeling.js', 'menu/skills/algebra1-linear-equations-slope.js', 'menu/skills/algebra1-systems-of-equations.js'];
module.exports = function load(extra) {
  const env = { console, Math, Date, JSON, Set, Map, BigInt };
  env.window = env; env.globalThis = env; vm.createContext(env);
  FILES.concat(extra || []).forEach(f => vm.runInContext(fs.readFileSync(path.join(WG, f), 'utf8'), env, { filename: f }));
  return env;
};
module.exports.FILES = FILES;
