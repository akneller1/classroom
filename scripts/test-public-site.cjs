/* Validate only the generated public-site contract; existing activity mathematics has separate checks. */
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const out=path.resolve('_site'),home=fs.readFileSync(path.join(out,'index.html'),'utf8');
assert(home.includes('mk-static'),'Missing crawlable catalog');assert(home.includes('og:image'),'Missing link-preview metadata');
assert(home.includes('assets/fonts/classroom-fonts.css'),'Homepage fonts must be local');
for(const dir of ['.git','.github','scripts','audits','incoming','docs','tools','patches'])assert(!fs.existsSync(path.join(out,dir)),'Working files published: '+dir);
assert(home.includes('u/math6/')&&home.includes('u/prealgebra7/'),'Grade 6/7 missing from catalog');
const sitemap=fs.readFileSync(path.join(out,'sitemap.xml'),'utf8');
assert(sitemap.includes('/u/math6/')&&sitemap.includes('/u/prealgebra7/'),'Grade 6/7 missing from sitemap');
const courses=fs.readdirSync(path.join(out,'u'));assert.equal(courses.length,9);let count=0;
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
 if(course === 'statistics') {
  assert(html.includes('Activities coming soon'),'Statistics must identify the course outline');
  assert(!html.includes('worksheet-generator/'),'Statistics must not link to unavailable generators');
 } else for(const page of ['lesson-planner.html','worksheet.html','printables.html','menu-assessment.html'])assert(html.includes('worksheet-generator/'+page),'Missing generator '+page+' in '+course+'/'+unit);
 assert(html.includes('<a href="../">'),'Missing course breadcrumb: '+course+'/'+unit);
 checkLinks(file,html);count++;
}
}
assert.equal(count,81);assert.equal((sitemap.match(/<loc>/g)||[]).length,91);
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
assert.match(home, /<script\s+src="app\.js\?v=[^"\s]+"\s*><\/script>/, 'Homepage must load a versioned browsing script');
assert(publicApp.includes('function belongsToGroup(a, group)'),'Browse Activities classification missing');
assert(publicApp.includes("if (a.unitSpecific === true) return 'Unit-specific';"),'Unit-specific tag missing');
assert(publicApp.includes("if (key === 'category') { state.format = ''; state.gameMode = ''; }"),'Category changes must clear stale choices');
assert(publicApp.includes("match-game"),'Matching games must be recognized');
assert(!publicApp.includes('github.com/akneller1/classroom/issues/new'),'Per-resource reports must not send visitors to GitHub');
assert(!home.includes('.main-nav { display: none; }'),'Header navigation hidden');
for(const file of ['favicon.svg','social-preview.png','apple-touch-icon.png'])assert(fs.existsSync(path.join(out,'assets',file)),'Missing branding asset '+file);
assert(fs.existsSync(path.join(out,'schemas')),'Runtime schemas missing');assert(fs.existsSync(path.join(out,'legacy-crosswalk-audit.js')),'Runtime grade bridge dependency missing');
console.log('PASS public build: nine visible courses, 81 unit pages, generator links, sitemap, local fonts, metadata, assets and excluded working files');

/* All nine courses are public, including restored Grade 6 and Grade 7. */
const publishedData=fs.readFileSync(path.join(out,'data.js'),'utf8');
const dataContext={window:{}};
require('node:vm').runInNewContext(publishedData,dataContext);
for(const courseId of ['prealgebra7','math6','calculus','precalculus']){
 const course=dataContext.window.LIBRARY.courses.find(c=>c.id===courseId);
 assert(course&&!course.comingSoon,'Course must be visible: '+courseId);
 if(['precalculus','calculus'].includes(courseId)){
  assert.equal(course.planned,false,'Course must expose activities: '+courseId);
  for(const u of course.units)for(const game of ['showdown','connect-four','tic-tac-toe','escape-room','detective','picture-reveal','flashcards'])
   assert(u.artifacts.some(a=>a.path.includes('course='+courseId+'&unit='+u.id+'&game='+game)),'Missing '+courseId+'/'+u.id+'/'+game);
 }
}
const app=fs.readFileSync(path.join(out,'app.js'),'utf8');
assert(app.includes('var HIDDEN_COURSES = {};'),'All courses must be unhidden');
const stylesheet=fs.readFileSync(path.join(out,'styles.css'),'utf8');
assert(stylesheet.includes('grid-template-columns:repeat(2,minmax(0,1fr))'),'Missing two-column homepage subject grid');
console.log('PASS Grade 6/7 restored; nine visible courses in a two-column grid');

/* Regression: middle-school activity links must not redirect back home. */
{
 const gameFile=path.join(out,'worksheet-generator','middle-school-game.html');
 const practiceFile=path.join(out,'worksheet-generator','grade-practice.html');
 for(const file of [gameFile,practiceFile]){
   const html=fs.readFileSync(file,'utf8');
   assert(!/location\s*\.\s*replace\s*\(\s*['"]\.\.\/index\.html['"]\s*\)/.test(html),
     'Middle-school activity redirects home: '+path.basename(file));
   assert(!/get\s*\(\s*['"]course['"]\s*\)\s*!==\s*['"]prealgebra['"]/.test(html),
     'Middle-school activity still blocks Grade 6/7: '+path.basename(file));
 }
 const practiceHtml=fs.readFileSync(practiceFile,'utf8');
 for(const id of ['math6','prealgebra7','prealgebra'])
   assert(practiceHtml.includes('<option value="'+id+'"'),
     'Missing course in middle-school practice picker: '+id);
 const gameHtml=fs.readFileSync(gameFile,'utf8');
 assert(gameHtml.includes('games/grade-game-setup.js'),
   'Middle-school game must load the grade-specific engine');
 assert(publicApp.includes('middle-school-game.html?course=') &&
        publicApp.includes('grade-practice.html?course='),
   'Middle-school activity cards do not target the expected pages');
 const publishedData=fs.readFileSync(path.join(out,'data.js'),'utf8');
 assert(publishedData.includes('course=prealgebra&unit='),
   'Grade 8 games must retain direct course/unit routes');
 console.log('PASS Grade 6/7 activity navigation; Grade 8 links preserved');
}


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
 assert.equal(projects.length,81,'Expected 81 authored projects (37 Algebra 1, Geometry and Algebra 2 + 44 for 6th Grade, Pre-Algebra 7, Pre-Algebra 8, Precalculus and Calculus)');
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
