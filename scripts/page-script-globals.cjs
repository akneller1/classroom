'use strict';
/* For tests that run a page's inline script in a vm sandbox: load the page's own local
 * <script src> files (e.g. worksheet-generator/core/math-display.js) the way the browser
 * does, and return the MK_* globals they define. Each file runs without a DOM, so it only
 * defines its API and skips any page wiring. */
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const root = path.resolve(__dirname, '..');
module.exports = function pageScriptGlobals(html, pageFile) {
  const out = {};
  for (const m of html.matchAll(/<script\b[^>]*\bsrc="([^"?]+)(?:\?[^"]*)?"[^>]*>/gi)) {
    if (/^(?:https?:)?\/\//.test(m[1])) continue;
    const file = path.resolve(path.dirname(path.resolve(root, pageFile)), m[1]);
    if (!fs.existsSync(file)) continue;
    const lib = {}; lib.window = lib; vm.createContext(lib);
    vm.runInContext(fs.readFileSync(file, 'utf8'), lib, { filename: path.relative(root, file), timeout: 2000 });
    for (const k of Object.keys(lib)) if (/^MK_/.test(k)) out[k] = lib[k];
  }
  return out;
};
