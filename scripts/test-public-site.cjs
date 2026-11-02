/* Validate only the generated public-site contract; existing activity mathematics has separate checks. */
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const out=path.resolve('_site'),home=fs.readFileSync(path.join(out,'index.html'),'utf8');
assert(home.includes('mk-static'),'Missing crawlable catalog');assert(home.includes('og:image'),'Missing link-preview metadata');
assert(home.includes('assets/fonts/classroom-fonts.css'),'Homepage fonts must be local');
for(const dir of ['.git','.github','scripts','audits','incoming','docs','tools','patches'])assert(!fs.existsSync(path.join(out,dir)),'Working files published: '+dir);
assert(!home.includes('u/math6/')&&!home.includes('u/prealgebra7/'),'Hidden courses exposed in catalog');
const sitemap=fs.readFileSync(path.join(out,'sitemap.xml'),'utf8');
assert(!sitemap.includes('/u/math6/')&&!sitemap.includes('/u/prealgebra7/'),'Hidden courses exposed in sitemap');
const courses=fs.readdirSync(path.join(out,'u'));assert.equal(courses.length,4);let count=0;
const checkLinks=(file,text)=>{for(const match of text.matchAll(/(?:href|src)="([^"<>]+)"/g)){
 const link=match[1].replace(/&amp;/g,'&');if(/^(?:https?:|data:|mailto:|#)/.test(link))continue;
 const raw=link.split(/[?#]/)[0];if(!raw)continue;
 const target=path.resolve(path.dirname(file),decodeURIComponent(raw));assert(target===out||target.startsWith(out+path.sep),'Link escapes site: '+link);assert(fs.existsSync(target),'Missing generated link '+path.relative(out,file)+': '+link);
}};
checkLinks(path.join(out,'index.html'),home);
for(const course of courses){
 const courseFile=path.join(out,'u',course,'index.html'),courseHtml=fs.readFileSync(courseFile,'utf8');
 assert(courseHtml.includes('rel="canonical"'),'Missing course canonical: '+course);
 assert(courseHtml.includes('meta name="description"'),'Missing course description: '+course);
 checkLinks(courseFile,courseHtml);
 for(const unit of fs.readdirSync(path.join(out,'u',course),{withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>x.name)){
 const file=path.join(out,'u',course,unit,'index.html'),html=fs.readFileSync(file,'utf8');
 assert(html.includes('../../../#'+course+'.'+unit),'Incorrect app route: '+course+'/'+unit);
 for(const page of ['lesson-planner.html','worksheet.html','printables.html','menu-assessment.html'])assert(html.includes('worksheet-generator/'+page),'Missing generator '+page+' in '+course+'/'+unit);
 assert(html.includes('<a href="../">'),'Missing course breadcrumb: '+course+'/'+unit);
 checkLinks(file,html);count++;
}
}
assert.equal(count,40);assert.equal((sitemap.match(/<loc>/g)||[]).length,45);
assert(home.includes('footer-bottom')&&home.includes('Feedback or report an issue'),'Missing feedback footer');
assert(home.includes('mailto:akneller@gmail.com?subject=')&&home.includes('Feedback%20or%20issue%3A'),'Footer feedback must open a prepared email to the site owner');
assert(!home.includes('github.com/akneller1/classroom/issues/new'),'Footer feedback must not send visitors to GitHub');
assert(home.includes('data-feedback-chooser'),'Footer feedback must open the email client chooser');
assert(home.includes('id="feedbackChooser"') && home.includes('id="feedbackGmail"') && home.includes('id="feedbackOutlook"') && home.includes('id="feedbackDefault"'),'Feedback dialog must offer Gmail, Outlook and default mail');
assert(home.includes('src="feedback.js?v=email-choice-20261102"'),'Feedback chooser script missing from homepage');
const feedbackScript=fs.readFileSync(path.join(out,'feedback.js'),'utf8');
new (require('node:vm').Script)(feedbackScript,{filename:'feedback.js'});
for(const required of ['mail.google.com/mail/u/0/','outlook.live.com/mail/0/deeplink/compose','a.report-problem','dialog.showModal()','gmailUrl.searchParams.set(\'body\', body)','outlookUrl.searchParams.set(\'body\', body)','nativeMail.href = links.native']){
 assert(feedbackScript.includes(required),'Missing feedback chooser behavior: '+required);
}
const publicApp=fs.readFileSync(path.join(out,'app.js'),'utf8');
assert(publicApp.includes("'mailto:akneller@gmail.com?subject='"),'Per-resource issue reports must use direct email');
assert(publicApp.includes("encodeURIComponent(body)"),'Per-resource report must include activity link and problem template');
assert(publicApp.includes('class="report-problem"'),'Activity report links must remain available for email chooser');
assert(home.includes('app.js?v=browse-game-category-20261102'),'Homepage must load fresh Browsing filters');
assert(publicApp.includes('function belongsToGroup(a, group)'),'Browse Activities classification missing');
assert(publicApp.includes("if (a.unitSpecific === true) return 'Unit-specific';"),'Unit-specific tag missing');
assert(publicApp.includes("if (key === 'category') { state.format = ''; state.gameMode = ''; }"),'Category changes must clear stale choices');
assert(publicApp.includes("match-game"),'Matching games must be recognized');
assert(!publicApp.includes('github.com/akneller1/classroom/issues/new'),'Per-resource reports must not send visitors to GitHub');
assert(!home.includes('.main-nav { display: none; }'),'Header navigation hidden');
for(const file of ['favicon.svg','social-preview.png','apple-touch-icon.png'])assert(fs.existsSync(path.join(out,'assets',file)),'Missing branding asset '+file);
assert(fs.existsSync(path.join(out,'schemas')),'Runtime schemas missing');assert(fs.existsSync(path.join(out,'legacy-crosswalk-audit.js')),'Runtime grade bridge dependency missing');
console.log('PASS public build: four visible courses, 40 unit pages, generator links, sitemap, local fonts, metadata, assets and excluded working files');

/* Keep Grade 6/7 available in source data but absent from public course cards,
 * navigation, and search. Retain the four published courses and 2 x 2 layout. */
const publishedData=fs.readFileSync(path.join(out,'data.js'),'utf8');
for(const courseId of ['prealgebra7','math6']){
 const p=publishedData.indexOf('"id": "'+courseId+'"');
 assert(p>=0,'Missing preserved course data: '+courseId);
 const marker=publishedData.indexOf('"comingSoon": true',p);
 assert(marker>p&&marker-p<10000,'Hidden course must remain unpublished: '+courseId);
}
const app=fs.readFileSync(path.join(out,'app.js'),'utf8');
assert(app.includes('var HIDDEN_COURSES = { math6: true, prealgebra7: true };'),'Grade 6/7 hide switch missing');
assert(app.includes('c.comingSoon && !HIDDEN_COURSES[c.id]'),'Hidden courses must not appear as Coming soon cards or nav links');
assert(app.includes('!c.comingSoon && !HIDDEN_COURSES[c.id]'),'Hidden courses must not appear in published course views or search');
const stylesheet=fs.readFileSync(path.join(out,'styles.css'),'utf8');
assert(stylesheet.includes('grid-template-columns:repeat(2,minmax(0,1fr))'),'Missing two-column homepage subject grid');
console.log('PASS Grade 6/7 hidden with source preserved; four published courses in a two-by-two grid');

/* Projects regression: previously authored Algebra 1, Geometry, and Algebra 2
 * projects must be available in the Activity Builder, with intact download assets. */
{
 const vm=require('node:vm');
 const builderPath=path.join(out,'worksheet-generator','printables.html');
 const builderHtml=fs.readFileSync(builderPath,'utf8');
 const scriptPath='menu/printables-projects.js';
 assert(builderHtml.includes('src="'+scriptPath+'?v='),'Activity Builder does not load existing project catalog');
 const catalogScript=fs.readFileSync(path.join(out,'worksheet-generator',scriptPath),'utf8');
 const context={window:{}};
 vm.runInNewContext(catalogScript,context,{timeout:5000,filename:scriptPath});
 const pr=context.window.MKMENU?.printables;
 assert(pr&&pr.PROJECTS&&typeof pr.projectFiles==='function','Project catalog did not initialize');
 const projects=Object.values(pr.PROJECTS).flat();
 assert.equal(projects.length,37,'Expected the 37 previously authored projects');
 for(const project of projects){
   const files=pr.projectFiles(project);
   const refs=[files.thumb,files.page,files.teacher.pdf,files.teacher.docx];
   for(const level of ['cp2','cp1','honors']){
     refs.push(files[level].pdf,files[level].docx,files[level].pptx);
   }
   for(const ref of refs){
     const asset=path.resolve(path.dirname(builderPath),ref);
     assert(asset.startsWith(out+path.sep),'Project asset escapes public site: '+ref);
     assert(fs.existsSync(asset),'Missing saved project asset: '+ref);
   }
 }
 const kinds=fs.readFileSync(path.join(out,'worksheet-generator/menu/printables.js'),'utf8');
 assert(kinds.includes("id: 'project'"),'Projects missing from Activity Builder formats');
 console.log('PASS Activity Builder project catalog: '+projects.length+' projects with PDF, Word, PowerPoint and teacher guides');
}

/* Protect every published activity link, thumbnail, and active teacher key from
 * being silently disconnected by future UI/catalog changes. This is a link
 * integrity check, not an assertion that the mathematics is human-reviewed. */
{
 const source=fs.readFileSync(path.join(out,'data.js'),'utf8');
 const activePaths=new Set();
 let checked=0;
 for(const [,field,url] of source.matchAll(/"(path|thumb)"\s*:\s*"([^"]+)"/g)){
  if(/^(?:https?:|data:|mailto:|#)/i.test(url))continue;
  const plain=url.split(/[?#]/,1)[0];
  const target=path.resolve(out,plain);
  assert(target.startsWith(out+path.sep),'Catalog '+field+' escapes public site: '+url);
  assert(fs.existsSync(target),'Broken catalog '+field+': '+url);
  if(field==='path')activePaths.add(url);
  checked++;
 }
 assert(checked>=1000,'Catalog seems to have lost activity or thumbnail records');
 const meta=fs.readFileSync(path.join(out,'resource-details.js'),'utf8');
 const details=JSON.parse(meta.replace(/^\s*window\.RESOURCE_DETAILS\s*=\s*/, '').replace(/;\s*$/, ''));
 let keyCount=0;
 for(const [resource,info] of Object.entries(details)){
  if(!activePaths.has(resource)||!info.answerKey)continue;
  const target=path.resolve(out,info.answerKey);
  assert(target.startsWith(out+path.sep),'Teacher key escapes public site: '+info.answerKey);
  assert(fs.existsSync(target),'Missing teacher key for '+resource+': '+info.answerKey);
  keyCount++;
 }
 console.log('PASS catalog integrity: '+checked+' published activity/thumbnail references and '+keyCount+' active teacher answer keys');
}
