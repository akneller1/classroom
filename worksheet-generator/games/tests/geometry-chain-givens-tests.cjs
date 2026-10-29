/* In games and flashcards a chain part is asked on its own: every part after the first must state the earlier results.
   Run: node worksheet-generator/games/tests/geometry-chain-givens-tests.cjs */
'use strict';
const assert = require('node:assert'), path = require('path');
const env = require(path.join(__dirname, '..', '..', 'menu', 'tests', 'load.cjs'))(['games/bank.js']);
const NS = env.MKMENU, GB = env.MKGAMES;
let items = 0, chains = 0;
for (const setId of Object.keys(NS.skillSets).filter(s => /^geometry-/.test(s)))
  for (const sk of NS.skillSets[setId].skills.filter(s => s.tag === 'INVEST' || /investigation/.test(s.id)))
    for (const c of [5, 6, 7]) for (let i = 0; i < 6; i++) {
      const its = GB.makeItems(setId, sk.id, c, { intOnly: false, level: 'game' }, 'givens:' + sk.id + c + i, { keys: new Set(), sigs: new Set() });
      if (!its.length) continue; chains++;
      for (const it of its) {
        const k = it.k, p = it.p; items++;
        if (k === 0) assert(!/Results from the earlier parts/.test(it.q.ask), 'part a has no givens');
        else for (let j = 0; j < k; j++) assert(it.q.ask.indexOf(p.parts[j].answer) >= 0, sk.id + ' part ' + k + ' must state the answer of part ' + j);
      }
    }
assert(chains > 100 && items > 200, 'enough chains exercised: ' + chains + '/' + items);
console.log('Chain givens: ' + items + ' game items from ' + chains + ' Honors chains state every earlier result.');
