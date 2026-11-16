import './apply-kid-player.mjs';
// Apply reviewed images after all pinned course sources and Classroom content overlays.
import fs from 'node:fs';import path from 'node:path';import os from 'node:os';import {execFileSync} from 'node:child_process';
const out=path.resolve(process.argv[2]||'_site'),tmp=fs.mkdtempSync(path.join(os.tmpdir(),'mk-pictures-'));
const read=f=>JSON.parse(fs.readFileSync(f));let count=0,copies=0;
try{execFileSync('unzip',['-q','content-updates/kid-friendly/pictures.zip','-d',tmp]);
for(const phase of [3,5,6,7])for(const sub of ['', 'grade4-package']){
 const pkg=path.join(tmp,'phase'+phase,sub),dir=path.join(pkg,'patches');if(!fs.existsSync(dir))continue;
 for(const course of fs.readdirSync(dir))for(const file of fs.readdirSync(path.join(dir,course))){
  const {edits}=read(path.join(dir,course,file)),grade=course.replace('math','grade'),unit=file.replace('.story-pictures.json','');
  const bankFiles=[path.join(out,'question-banks',grade,unit+'.json'),path.join(out,grade,course==='math5'?'math5':'question-banks/'+course,unit+'.json')];
  for(const [index,bankFile] of bankFiles.entries()){
   if(!fs.existsSync(bankFile))throw Error('Missing deployed bank '+bankFile);const bank=read(bankFile),byId=new Map(bank.questions.map(q=>[q.id,q]));
   for(const edit of edits){const q=byId.get(edit.id);if(!q)throw Error('Missing question '+edit.id);
    const diagram=structuredClone(edit.changes.diagram.to),src=diagram.spec.src,png=fs.readFileSync(path.join(pkg,'assets',src));
    if(png.subarray(0,8).toString('hex')!=='89504e470d0a1a0a'||!diagram.spec.alt)throw Error('Invalid picture '+edit.id);
    const target='question-banks/assets/kid-friendly/'+grade+'/'+unit+'/'+edit.id+'.png';diagram.spec.src=target;
    if(q.diagram&&JSON.stringify(q.diagram)!==JSON.stringify(diagram))throw Error('Diagram conflict '+edit.id);
    q.diagram=diagram;const note=edit.changes.sourceNotes?.append;if(note&&!String(q.sourceNotes||'').includes(note))q.sourceNotes=(q.sourceNotes||'')+note;
    const dest=path.join(out,index?grade:'',target);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,png);copies++;
   }fs.writeFileSync(bankFile,JSON.stringify(bank));
  }count+=edits.length;
 }
}
if(count!==1195)throw Error('Expected 1195 pictures, got '+count);
console.log(`Kid-friendly phases 3, 5–7: ${count} illustrations, ${copies} bank/player copies.`);
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
