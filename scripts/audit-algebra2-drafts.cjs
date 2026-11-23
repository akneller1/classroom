#!/usr/bin/env node
/* Audit Claude-authored Algebra 2 drafts. This does NOT approve or publish content.
 * Usage: node scripts/audit-algebra2-drafts.cjs
 * Requires draft JSON files unpacked under question-banks/algebra2/.
 */
'use strict';
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..');
const dir=path.join(root,'question-banks/algebra2');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'question-banks/manifest.json'),'utf8'));
const files=fs.existsSync(dir)?fs.readdirSync(dir).filter(x=>x.endsWith('.json')).sort():[];
const failures=[],warnings=[],stats=[];
const seenGlobal=new Set();
for(const file of files){
 const full=path.join(dir,file),bank=JSON.parse(fs.readFileSync(full,'utf8'));
 const v=cp.spawnSync(process.execPath,[path.join(root,'scripts/check-question-bank.cjs'),full],{encoding:'utf8'});
 if(v.status!==0)failures.push(file+': structural validator failed: '+(v.stderr||v.stdout).trim());
 const formats={},levels={},skillCounts={},assets=new Set();
 for(const q of bank.questions||[]){
  if(seenGlobal.has(q.id))failures.push(file+': repeated question ID '+q.id);
  seenGlobal.add(q.id);
  formats[q.format]=(formats[q.format]||0)+1;
  levels[q.level]=(levels[q.level]||0)+1;
  skillCounts[q.skillId]=(skillCounts[q.skillId]||0)+1;
  if(q.diagram&&q.diagram.type==='image'){
   const src=q.diagram.spec&&q.diagram.spec.src;
   if(typeof src!=='string'||!src.startsWith('question-banks/assets/')||src.includes('..'))failures.push(file+': unsafe diagram path for '+q.id);
   else {
    assets.add(src);
    if(!fs.existsSync(path.join(root,src)))failures.push(file+': missing diagram '+src);
   }
  }
  if(q.format==='open-response'&&(!Array.isArray(q.parts)||q.parts.length<4))failures.push(file+': insufficient open-response parts for '+q.id);
 }
 const meta=path.join(dir,'meta',file.replace(/\.json$/,'.tags.json'));
 if(!fs.existsSync(meta))warnings.push(file+': no companion tags found');
 const small=Object.entries(skillCounts).filter(([,n])=>n<30);
 if(small.length)warnings.push(file+': '+small.length+' skills remain below the 30-question target');
 stats.push({unit:bank.unitId,questions:(bank.questions||[]).length,skills:Object.keys(skillCounts).length,formats,levels,distinctAssets:assets.size});
}
for(const item of manifest.banks||[]){
 if(item.courseId==='algebra2'&&item.approved===true)warnings.push('Algebra 2 has an APPROVED manifest entry: '+item.unitId+'; confirm documented human approval.');
}
if(!files.length)warnings.push('No Algebra 2 draft banks present. Unpack authoring ZIPs before running this audit.');
console.log(JSON.stringify({banks:files.length,questions:stats.reduce((a,x)=>a+x.questions,0),stats,warnings,failures},null,2));
process.exitCode=failures.length?1:0;