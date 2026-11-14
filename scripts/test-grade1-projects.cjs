'use strict';
const assert = require('node:assert/strict'), fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const root = path.resolve(process.argv[2] || '.');
const context = {window:{}};vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/menu/printables-projects.js'),'utf8'),context);
const PR=context.window.MKMENU.printables;
const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'grade1-projects-manifest.json'),'utf8'));
assert.equal(Object.keys(expected).length,12);
let files=0;
for(const [unit,projects] of Object.entries(expected)) {
 assert.equal(PR.PROJECTS[unit].length,1,unit);
 for(const p of PR.PROJECTS[unit]) {
  assert.equal(p.slug,projects[0].slug);
  const f=PR.projectFiles(p);
  const links=[f.thumb,f.page,f.supports,...['cp2','cp1','honors','teacher'].flatMap(level=>Object.values(f[level]))];
  for(const link of links) {
   const target=path.resolve(root,'worksheet-generator',link);
   assert.ok(target.startsWith(root+path.sep));
   assert.ok(fs.statSync(target).size>100,`${unit}: missing or empty ${link}`);files++;
  }
  const dir=path.resolve(root,'artifacts',p.folder), html=fs.readFileSync(path.join(dir,'index.html'),'utf8');
  for(const [,href] of html.matchAll(/href="([^"]+)"/g)) if(!href.startsWith('../../')) assert.ok(fs.existsSync(path.resolve(dir,href)),href);
 }
}
console.log(`Grade 1 projects: 12 unit mappings and ${files} resource links passed.`);
