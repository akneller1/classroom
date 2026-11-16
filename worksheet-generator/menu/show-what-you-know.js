/* Two reviewed, disjoint question sets for every Grade 1–2 unit. */
(function(G){'use strict';const NS=G.MKMENU,data=G.MK_SHOW_WHAT_YOU_KNOW;
NS.showWhatYouKnowUnit=function(id){const m=/^(grade[12])-(.+)$/.exec(id);return m&&data?.courses[m[1]]?.[m[2]]};
NS.applyShowWhatYouKnow=function(cfg){const unit=NS.showWhatYouKnowUnit(cfg.unitId);if(!unit)throw Error('No reviewed quiz for this unit');
 cfg.showWhatYouKnow=unit;cfg.mode='test';cfg.title='Show What You Know';cfg.level='cp1';cfg.coverage.on=false;cfg.versions=Math.min(2,cfg.versions||1);
 cfg.sections=unit.versions.A.map((id,i)=>{const q=NS.authoredQuestion(id);if(!q)throw Error('Missing reviewed question '+id);return {id:NS.uid('swk'),name:'',note:'',points:1,offered:1,required:1,tier:1,adjust:0,skills:[q.skillId],qformat:q.format==='multiple-choice'?'mc':'open'}});
 Object.keys(cfg.skills).forEach(k=>cfg.skills[k]=true);return cfg;
};
const sync=NS.syncStructure;
NS.syncStructure=function(state,fresh){const before=state.versions.length;const result=sync.apply(this,arguments);if(state.config.showWhatYouKnow&&before>0&&state.versions.length>before){const freshState=NS.newAssessment(Object.assign({},state.config));for(let i=before;i<state.versions.length;i++)state.versions[i]=freshState.versions[i]}return result};
const create=NS.newAssessment;
NS.newAssessment=function(cfg){const state=create.apply(this,arguments);if(!cfg.showWhatYouKnow)return state;
 state.versions.forEach((version,vi)=>{const picks=cfg.showWhatYouKnow.versions[vi===1?'B':'A'];version.sections.forEach((section,si)=>{const old=section.items[0],q=NS.authoredQuestion(picks[si]);if(!q)throw Error('Missing reviewed question '+picks[si]);const p=NS.authoredProblem(q,cfg.unitId,q.level==='cp2'?1:4);Object.assign(p,{uid:NS.uid('swkq'),slot:old.slot,required:true,pinned:false});if(q.format==='multiple-choice'){p.mc=NS.makeChoices(p);if(p.mc.fail)throw Error('Invalid reviewed choices '+q.id)}section.items=[p]})});return state;
};
})(window);
