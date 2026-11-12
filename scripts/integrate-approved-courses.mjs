// Assemble approved course sources into the GitHub Pages artifact.
// The development repository remains separate; only the artifact is modified.
import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const stage=path.resolve(process.env.GRADE5_SOURCE_DIR || '../FinancialAlgebra');
const out=path.join(root,'_site');
if(!fs.existsSync(path.join(stage,'grade5.html')))throw Error('Approved Grade 5 source checkout is missing');
if(!fs.existsSync(path.join(out,'index.html')))throw Error('Build the Classroom site before integrating approved courses');
const dst=path.join(out,'grade5');
fs.rmSync(dst,{recursive:true,force:true});
fs.mkdirSync(dst,{recursive:true});
const skipTop=new Set(['.git','.github','node_modules','_site','tests','docs','scripts','tools','financial','question-banks','artifacts','grade1.html','grade2.html','grade3.html','grade4.html','index.html','activity.html','coverage.html','skills.html','INTEGRATION.md','README.md','package.json','package-lock.json','COURSE_TEMPLATE.md']);
const skipNames=/^(?:GRADE[1-4]_BANK_HANDOFF|FINANCIAL_ALGEBRA|FA_INTEGRATION)/i;
function copy(src, target, depth=0){
 fs.mkdirSync(target,{recursive:true});
 for(const item of fs.readdirSync(src,{withFileTypes:true})){
  if(depth===0&&(skipTop.has(item.name)||skipNames.test(item.name)||/^grade[1-4][-.]/i.test(item.name)))continue;
  if(item.name==='.git'||item.name==='node_modules'||item.name==='.DS_Store'||item.name==='__pycache__')continue;
  const from=path.join(src,item.name),to=path.join(target,item.name);
  if(item.isDirectory())copy(from,to,depth+1);
  else if(item.isFile()&&!/\.(?:md|py|pyc)$/i.test(item.name))fs.copyFileSync(from,to);
 }
}
copy(stage,dst);
// Only copy approved Grade 5 artifact directories. No Financial Algebra or other unpublished courses.
const artifacts=path.join(stage,'artifacts'),published=path.join(dst,'artifacts');
if(fs.existsSync(artifacts)){
 fs.mkdirSync(published,{recursive:true});
 for(const item of fs.readdirSync(artifacts,{withFileTypes:true})){
  if(item.isDirectory()&&/^math5(?:-|$)/i.test(item.name))copy(path.join(artifacts,item.name),path.join(published,item.name),1);
 }
}
let html=fs.readFileSync(path.join(dst,'grade5.html'),'utf8');
html=html.replace(/<title>[^<]*<\/title>/,'<title>5th Grade Math | Mr. K\'s Classroom</title>')
 .replace(/href="index\.html">Financial Algebra<\/a>/g,'href="../index.html">All courses</a>')
 .replace(/href="https:\/\/mrksclassroom\.com\/" target="_blank" rel="noopener">Main Classroom ↗<\/a>/g,'')
 .replace(/<a href="grade[1-4]\.html"[\s\S]*?<\/a>/g,'')
 .replace(/<span class="course-wip-label">[\s\S]*?<\/span>/g,'')
 .replace(/Grade 5 resources are being developed and tested here before transfer to the main Classroom site\. The original curriculum outline is preserved within the course page\./g,'Grade 5 mathematics: games, generators, printable resources, and understanding checks.')
 .replace(/href="grade5\.html"/g,'href="index.html"')
 .replace(/href="index\.html"/g, (x,offset)=>x);
// Local Grade 5 page uses the original source's relative URLs; renaming it to index.html preserves them.
fs.writeFileSync(path.join(dst,'index.html'),html);
// Previously the publisher deleted grade5.html while games, projects and teacher tools linked to it.
// Preserve old lesson/game links with a same-folder redirect that retains the unit hash and query.
fs.writeFileSync(path.join(dst,'grade5.html'),"<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n<meta name=\"robots\" content=\"noindex,follow\">\n<title>Grade 5 | Mr. K's Classroom</title>\n<meta http-equiv=\"refresh\" content=\"0; url=./index.html\">\n<script>location.replace('./index.html'+location.search+location.hash);</script>\n</head><body><p>Continue to <a href=\"./index.html\">5th Grade Math</a>.</p></body></html>\n");
// Grade 5 breadcrumb links point back to its own landing page.
const siteJs=path.join(dst,'src','grade5-site.js');
if(fs.existsSync(siteJs)){
 const js=fs.readFileSync(siteJs,'utf8').replace(/\['Home','index\.html'\]/g,"['Home','../index.html']");
 fs.writeFileSync(siteJs,js);
}
// The development data contains unapproved courses; Grade 5 pages use only math5.
const sitemap=path.join(out,'sitemap.xml');
let xml=fs.readFileSync(sitemap,'utf8');
if(!xml.includes('https://mrksclassroom.com/grade5/'))xml=xml.replace('</urlset>','  <url><loc>https://mrksclassroom.com/grade5/</loc></url>\n</urlset>');
fs.writeFileSync(sitemap,xml);
// Explicit contract prevents a missing or empty course from being deployed.
const required=['index.html','manifest.json','question-bank-loader.js','question-bank-adapter.js','src/grade5-site.js','grade5-resource-catalog.js','worksheet-generator/grade5-games.html','worksheet-generator/grade5-understanding-check.html','math5'];
for(const rel of required)if(!fs.existsSync(path.join(dst,rel)))throw Error('Grade 5 output missing '+rel);
console.log('Approved Grade 5 assembled at _site/grade5/; staging repository unchanged.');
