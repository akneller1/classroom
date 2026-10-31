#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const site={};
const ctx={window:site,Promise};
for(const filename of ['course-catalog.js','question-bank-adapter.js','question-bank-loader.js','worksheet-generator/menu/approved-bank-bridge.js']){
  // The bridge starts loading in a promise microtask after all dependencies exist.
  vm.runInNewContext(fs.readFileSync(path.join(root,filename),'utf8'),ctx,{filename});
}
(async function(){
  // No approved banks currently exist; no resources should be falsely available.
  const bridge=site.MK_APPROVED_RESOURCE_BANKS;
  assert.equal(bridge.select('worksheet',{courseId:'math6',unitId:'fractions-decimals-operations'}).length,0);
  const result=await bridge.ready;
  assert.equal(result.state,'error'); // No browser fetch is installed in this test context.
  assert.equal(bridge.available('math6','fractions-decimals-operations'),false);
  assert.equal(bridge.select('assessment',{courseId:'math6',unitId:'fractions-decimals-operations'}).length,0);
  console.log('PASS approved resource bridge fails closed without a manifest fetcher');
})().catch(function(e){console.error(e);process.exitCode=1;});
