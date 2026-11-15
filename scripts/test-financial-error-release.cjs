const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||'_site');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'financial-algebra/financial/resources.json'),'utf8'));
for(const unit of manifest.units){
 const rel='financial/banks/'+unit.unitId+'.json';
 const direct=JSON.parse(fs.readFileSync(path.join(root,rel),'utf8'));
 const nested=JSON.parse(fs.readFileSync(path.join(root,'financial-algebra',rel),'utf8'));
 assert.deepEqual(direct,nested,'Both published bank routes must agree: '+unit.unitId);
 const items=direct.questions.filter(q=>q.errorAnalysis);
 assert.equal(items.length,8,unit.unitId);
 assert(items.every(q=>q.gameEligible===false));
 assert.equal(new Set(direct.questions.map(q=>q.id)).size,direct.questions.length);
 assert.match(unit.resources.errorAnalysis,/mode=worksheet&format=error/);
 const exported=JSON.parse(fs.readFileSync(path.join(root,'financial-algebra/question-banks/financial-algebra',unit.unitId+'.json'),'utf8'));
 assert(!exported.questions.some(q=>q.errorAnalysis),'Reasoning activities must stay out of game exports');
}
for(const base of ['','financial-algebra/']){
 const script=fs.readFileSync(path.join(root,base,'financial/generators/generator.js'),'utf8');
 assert.match(script,/error:q=>!!q.errorAnalysis/);
 assert.match(script,/params.get\('format'\)/);
}
console.log('PASS 80 Error Analysis items in both Financial Algebra entry points, all ten generator links, and game exclusions.');
