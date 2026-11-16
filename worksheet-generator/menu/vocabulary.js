/* Vocabulary assessment parts reuse the activity maker's banks and task wording.
   Vocabulary keys are checked against those sources; creative responses have sample keys. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, T = G.MK_VOCAB_TASKS, RNG = G.MKWS.rng;
  var formats = {vocab_blank:'Vocabulary · Fill in the blank', vocab_match:'Vocabulary · Matching set (up to 5 terms)', vocab_draw:'Vocabulary · Draw and label', vocab_example:'Vocabulary · Write an example'};
  Object.assign(NS.FORMATS, formats);
  NS.isVocabularyFormat = function (f) { return Object.prototype.hasOwnProperty.call(formats, f); };
  NS.vocabularyTerms = function (cfg, format) {
    return T.terms(cfg.unitId).filter(function (t) {
      return (!cfg.vocabularyTerms || cfg.vocabularyTerms.indexOf(t.term) >= 0) && (format !== 'vocab_draw' || t.draw);
    });
  };
  function extend(set) {
    if (!set || !T.terms(set.id).length || /^topic-/.test(set.id)) return set;
    set.skills = set.skills.filter(function (s) { return !s.vocabulary; });
    Object.keys(formats).forEach(function (format) {
      set.skills.push({id:format, name:formats[format], tag:'V', vocabulary:true, blurb:'Uses the shared vocabulary bank.', generate:function () { throw Error('Vocabulary selection required'); }});
    });
    set.byId = {}; set.skills.forEach(function (s) { set.byId[s.id] = s; });
    // Vocabulary is selected per part, independently of the math skill coverage rules.
    return set;
  }
  var register = NS.registerSkillSet;
  NS.registerSkillSet = function (set) { return extend(register(set)); };
  Object.keys(NS.skillSets).forEach(function (id) { extend(NS.skillSets[id]); });
  var sectionSkills = NS.sectionSkills;
  NS.sectionSkills = function (cfg, si) {
    var format = NS.sectionFormat(cfg, si);
    if (NS.isVocabularyFormat(format)) return NS.vocabularyTerms(cfg, format).length && (format !== 'vocab_match' || NS.vocabularyTerms(cfg, format).length >= 2) ? [format] : [];
    return sectionSkills(cfg, si).filter(function (id) { return !NS.isVocabularyFormat(id); });
  };
  var coverageTags=NS.coverageTags;
  NS.coverageTags=function(cfg,state){return coverageTags(cfg,state).filter(function(t){return t!=='V';});};
  var skillFormatOk = NS.skillFormatOk, available = NS.formatAvailable;
  NS.skillFormatOk = function (unit, skill, format, c) {
    if (NS.isVocabularyFormat(skill) || NS.isVocabularyFormat(format)) return skill === format && T.terms(unit).some(function (t) { return format !== 'vocab_draw' || t.draw; });
    return skillFormatOk.apply(NS, arguments);
  };
  NS.formatAvailable = function (cfg, si, format) {
    if (NS.isVocabularyFormat(format)) { var terms = NS.vocabularyTerms(cfg, format); return terms.length >= (format === 'vocab_match' ? 2 : 1); }
    var temp = Object.assign({}, cfg, {sections:cfg.sections.slice()});
    temp.sections[si] = Object.assign({}, cfg.sections[si], {qformat:format});
    if (NS.isVocabularyFormat(cfg.sections[si].qformat)) temp.sections[si].skills = null;
    return available(temp, si, format);
  };
  NS.vocabularyPolicy = function (policy, cfg, si) {
    policy.vocabularyFormat = NS.sectionFormat(cfg, si);
    policy.vocabularyTerms = cfg.vocabularyTerms;
    policy.vocabularyWordBank = !!cfg.vocabularyWordBank;
  };
  function make(unit, format, terms, level, seed, wordbank) {
    var rng = RNG.make(RNG.hash(String(seed))), chosen = rng.shuffle(terms), t = chosen[0], p = {variant:format, prompt:'', parts:[], steps:[], space:[0.5,0.7,1]};
    if (format === 'vocab_match') {
      chosen = chosen.slice(0,5); var definitions = rng.shuffle(chosen);
      p.prompt = 'Match each term to its definition. Write the correct letter.\n' + definitions.map(function (x,i) { return String.fromCharCode(65+i)+'. '+x.definition; }).join('\n');
      p.parts = chosen.map(function (x,i) { return {label:String(i+1), prompt:'____ '+x.term, answer:String.fromCharCode(65+definitions.indexOf(x))+' — '+x.term}; });
      p.steps = [{t:'Award equal credit for each correct match.',w:1}]; p.space=[0.1,0.15,0.2];
    } else if (format === 'vocab_blank') {
      p.prompt = (level === 'honors' ? 'Identify the term and give a distinguishing feature or condition.\n' : 'Write the term for this definition.\n') + t.definition;
      if (wordbank) p.prompt += '\nWord bank: '+rng.shuffle(terms.map(function(x){return x.term;})).join(' · ');
      p.parts = [{answer:t.term}];
      p.steps = [{t:t.definition,w:1}];
      if (level === 'honors') p.steps.push({t:'Accept a correct distinguishing feature or condition consistent with the definition.',w:1});
    } else if (format === 'vocab_draw') {
      p.prompt = level === 'honors' ? T.honorsTask(t,'draw') : t.draw;
      p.parts = [{answer:'One acceptable representation: '+(t.example || t.definition)+'. Other mathematically correct drawings are accepted.'}];
      p.steps = [{t:'Check that the drawing illustrates '+t.term+': '+t.definition,w:1},{t:'Check labels and mathematical accuracy.'+(level==='honors'?' Check the contrasting case and explanation.':''),w:1}];
      p.space=[1.5,2,2.5];
    } else {
      p.prompt = level === 'honors' ? T.honorsTask(t,'example') : t.term+': Write your own example and justify it.';
      p.parts = [{answer:'Sample: '+(t.example || t.definition)+'. Other valid answers are accepted.'}];
      p.steps = [{t:'Use the definition: '+t.definition,w:1},{t:'Check the example and justification.'+(level==='honors'?' Check all additional constructions and comparisons requested.':''),w:1}]; p.space=[1,1.4,1.8];
    }
    p.vocabulary = {unit:unit,format:format,terms:terms.map(function(x){return x.term;}),level:level,seed:String(seed),wordbank:!!wordbank};
    return p;
  }
  var generate = NS.generateProblem;
  NS.generateProblem = function (unit, skill, c, policy, seed, used) {
    if (!NS.isVocabularyFormat(skill)) return generate.apply(NS, arguments);
    policy = policy || {}; var format = NS.isVocabularyFormat(policy.vocabularyFormat) ? policy.vocabularyFormat : skill;
    var terms = NS.vocabularyTerms({unitId:unit,vocabularyTerms:policy.vocabularyTerms},format);
    if (terms.length < (format === 'vocab_match' ? 2 : 1)) return {failed:true,reason:'Select more vocabulary terms for this format.'};
    for (var attempt=0; attempt<80; attempt++) {
      var p = make(unit,format,terms,policy.level, String(seed)+'|vocab|'+attempt,policy.vocabularyWordBank);
      // Versions share a finite vocabulary. Prevent repeated questions within each version.
      var scope = String(seed).split('|')[1] || '0';
      var key = 'vocab|'+scope+'|'+format+'|'+(format==='vocab_match' ? p.parts.map(function(x){return x.prompt;}).sort().join('|') : p.prompt.split('\nWord bank:')[0]);
      if (used && used.keys.has(key)) continue;
      p.uid=NS.uid('p'); p.skill=skill; p.c=c; p.tag='V'; p.key=key; p.sig=key; p.source='vocabulary';
      p.verify={status:'verified',issues:[]};
      if (used) { used.keys.add(key); used.sigs.add(key); }
      return p;
    }
    return {failed:true,reason:'No different vocabulary question remains. Select more terms or reduce the question count.'};
  };
  var verify = NS.verifyProblem;
  NS.verifyProblem = function (p, policy) {
    if (!p.vocabulary || p.edited || p.manual) return verify.apply(NS, arguments);
    var m=p.vocabulary, terms=NS.vocabularyTerms({unitId:m.unit,vocabularyTerms:m.terms},m.format);
    if (!NS.isVocabularyFormat(m.format) || !terms.length) return {ok:false,status:'mismatch',issues:['Vocabulary source is unavailable.']};
    var expected=make(m.unit,m.format,terms,m.level,m.seed,m.wordbank);
    var fields=['prompt','parts','steps','variant'];
    var ok=fields.every(function(k){return JSON.stringify(p[k])===JSON.stringify(expected[k]);}) && !p.fig && !p.work;
    return {ok:ok,status:ok?'verified':'mismatch',issues:ok?[]:['Vocabulary question or key differs from its source. Regenerate or edit and review it.'],bankKey:ok};
  };
  var rules=NS.checkRules;
  NS.checkRules=function(cfg,state){
    var r=rules(cfg,state);
    cfg.sections.forEach(function(s){
      if (!NS.isVocabularyFormat(s.qformat)) return;
      var n=NS.vocabularyTerms(cfg,s.qformat).length;
      if(s.qformat!=='vocab_match' && s.offered>n) r.errors.push(s.name+': only '+n+' vocabulary terms are selected for this format. Reduce the question count or select more terms.');
      if(s.qformat==='vocab_match' && n<=5 && s.offered>1) r.errors.push(s.name+': this selection supports one matching set. Add terms or use one question.');
    });
    return r;
  };
  NS.refreshVocabulary=function(state){
    state.config.sections.forEach(function(section,si){
      if(!NS.isVocabularyFormat(section.qformat))return;
      state.versions[0].sections[si].items.slice().forEach(function(p){
        var locked=state.versions.some(function(v){return v.sections[si].items.some(function(q){return q.slot===p.slot&&(q.pinned||q.edited||q.manual);});});
        if(!locked)NS.setDifficulty(state,0,p.uid,p.c);
      });
    });
  };
  var blockers=NS.blockers;
  NS.blockers=function(state){
    var list=blockers(state);
    state.versions.forEach(function(v){v.sections.forEach(function(s,si){s.items.forEach(function(p){
      var f=NS.sectionFormat(state.config,si);
      if(!p.failed && !p.manual && !p.edited && (NS.isVocabularyFormat(f) || p.vocabulary) && (!p.vocabulary || p.vocabulary.format!==f)) list.push('Move or regenerate the question to match its part’s vocabulary format.');
    });});});return list;
  };
})(window);
