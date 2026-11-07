'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),g={console,URLSearchParams,setTimeout,clearTimeout};g.window=g;g.globalThis=g;
g.fetch=async url=>({ok:true,json:async()=>JSON.parse(fs.readFileSync(path.resolve(root,'worksheet-generator',url),'utf8'))});
vm.createContext(g);
for(const m of fs.readFileSync(path.join(root,'worksheet-generator/worksheet.html'),'utf8').matchAll(/<script[^>]*src="([^"?]+)[^"]*"[^>]*><\/script>/g)){
 if(/vendor|math-display|menu\/app|approved-resource-preview/.test(m[1]))continue;
 vm.runInContext(fs.readFileSync(path.resolve(root,'worksheet-generator',m[1]),'utf8'),g,{filename:m[1]});
}
g.MK_COURSE_BANKS_READY.then(()=>{
 vm.runInContext(fs.readFileSync(path.join(root,'worksheet-generator/menu/printables.js'),'utf8'),g);
 const P=g.MKMENU.printables;let count=0;const failures=[];
 for(const [id,set] of Object.entries(g.MKMENU.skillSets).filter(([id])=>!process.env.TARSIA_UNIT||id===process.env.TARSIA_UNIT))for(const level of ['cp2','cp1','honors'])for(const seed of ['fit-a']){
  const cfg=P.defaultConfig(id,'tarsia');cfg.level=level;cfg.seed=seed;
  console.log('CHECK '+id+'/'+level);const b=P.build(cfg,0);if(b.error){failures.push(id+'/'+level+'/'+seed+': '+b.error);continue;}
  assert(b.items.length>=18);assert.equal(new Set(b.items.map(i=>i.key.replace(/\s+/g,'').toLowerCase())).size,b.items.length);
  for(const it of b.items){if(set.authoredBank){assert(it.p.prompt.length<=110,id);assert(!/[\r\n]/.test(it.p.prompt),id);assert(!it.p.fig,id);assert(it.key.length<=20,id);const q=g.MK_QUESTION_BANKS.select({courseId:id.split('-')[0],unitId:id.split('-').slice(1).join('-')}).find(q=>q.id===it.p.sourceId);assert(g.MKMENU.tarsiaEligible(q));assert.equal(q.level,level);}}
  count++;
 }
 console.log(JSON.stringify({passed:count,failures},null,2));if(failures.length)process.exitCode=1;
}).catch(e=>{console.error(e);process.exitCode=1});
