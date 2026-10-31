'use strict';
const fs=require('fs');
const report=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const findings=[];
for(const topic of report.topics)for(const scope of topic.targets){
 const seen=new Set();
 for(const q of scope.questions||[]){
  const key=[topic.topic,scope.courseId,scope.level,q.reviewKey];
  const text=String(q.prompt||'')+'|'+String(q.partPrompt||'');
  if(seen.has(text))findings.push({key,issue:'repeated-question-text'});
  seen.add(text);
  if(q.hasFigure)findings.push({key,issue:'figure-requires-visual-inspection'});
  if(!q.prompt)findings.push({key,issue:'missing-prompt'});
  if((q.options||[]).filter(o=>o.correct).length!==1)findings.push({key,issue:'invalid-correct-choice-count'});
  if(new Set((q.options||[]).map(o=>String(o.text))).size!==(q.options||[]).length)findings.push({key,issue:'duplicate-choice-text'});
 }
}
const result={mathVerified:false,publicationApproved:false,findings};
fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2));
console.log('Review flags: '+findings.length+'; no math approval');
