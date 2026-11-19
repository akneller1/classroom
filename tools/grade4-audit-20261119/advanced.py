import json, os
"""4th Grade Math audit #1 and #7 (2026-11-19).

advanced: Advanced items that reuse a Support or Standard template are rewritten in place (ID, skill, level and format
kept) as multi-step, work-backward or explain-why items, up to 16 per skill.
standard (run after): Standard items that reuse a Support template are rewritten in place (ID, skill, level and format
kept) as the skill's Support task with one added step. Items with a picture, error-analysis, true/false, select-all,
open-response and plot items are left alone."""
import random, re
from lib import ABBR, UNITS, mask, mc
import fams

SA_OK = re.compile(r'\$?[\d,]+(\.\d+)?|\d+/\d+|\d+ \d+/\d+|[\d,]+ R \d+|[<>=]|\$?[\d,]+(\.\d+)? (?!left\b|short\b)[a-z]+( [a-z]+){0,2}|\d+ \d+/\d+ [a-z]+( [a-z]+)?|\d+/\d+ [a-z]+|[a-z]+|\d+°|\d+:\d\d')
NOTE_A = ('Original Claude-authored item (family: {fam}). 4th Grade Math audit 2026-11-19 (#1, Advanced); answer computed by '
          'tools/grade4-audit-20261119/fams.py and recomputed by scripts/test-grade4-audit.cjs.')
NOTE_S = ('Original Claude-authored item (family: {fam}). Rewritten from a Support template (was {old}) as a Standard item with an '
          'added step: 4th Grade Math audit 2026-11-19 (#7, Standard); answer recomputed by scripts/test-grade4-audit.cjs.')
STD_PER_SKILL = 16  # keeps some of the Support task variety in each skill
ADV_PER_SKILL = 16


class NoItem(Exception):
    pass


def plain(q):
    """an ordinary SA/MC item without a picture that a new family can stand in for"""
    p = q['prompt']
    return (q['format'] in ('short-answer', 'multiple-choice') and 'diagram' not in q and 'plot' not in q
            and 'solved this problem' not in p and not p.startswith('True or false') and 'Choose the best response' not in p)


def make(gen, r, fmt, seen, avoid):
    for _ in range(600):
        try:
            fm, prompt, ans, steps, wrong = gen[_ % len(gen)](r)
            f = fmt
            if f == 'prefer-sa':
                f = 'short-answer' if SA_OK.fullmatch(ans) else 'multiple-choice'
            if f == 'short-answer' and not SA_OK.fullmatch(ans):
                continue
            opts = mc(ans, wrong, seed=len(seen)) if f == 'multiple-choice' else None
        except (fams.Skip, AssertionError, ZeroDivisionError, StopIteration, ValueError, IndexError):
            continue
        if prompt in seen or mask(prompt) in avoid:
            continue
        seen.add(prompt)
        return fm, prompt, ans, steps, wrong, opts, f
    raise NoItem(', '.join(g.__name__ for g in gen))


def meta_for(fm, steps, wrong, qtype, ans):
    return {'questionType': qtype, 'tags': [], 'explanation': steps[-1], 'distractors': {w: 'a common mistake' for w in [x for x in dict.fromkeys(wrong) if x != ans][:3]}}


def run(o):
    run_advanced(o)
    run_standard(o)


KEEP = set(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asteroid-keep.json')))['ids'])


def std_for(skill, items):
    return sorted({(x['standards'][0] if x['standards'] else '') for x in items})


def run_advanced(o):
    """Advanced items that reuse a Support or Standard template are rewritten in place as harder items (ID, skill, level and
    format kept), up to ADV_PER_SKILL per skill. Rewriting in place keeps the three levels the same size."""
    for u in UNITS:
        for skill, gens in sorted(fams.A.items()):
            if not skill.startswith(u + '-skill-'):
                continue
            items = [q for q in o.items(u) if q['skillId'] == skill]
            lower = {mask(q['prompt']) for q in items if q['level'] != 'honors'}
            clones = sorted([q for q in items if q['level'] == 'honors' and q['id'] not in KEEP and plain(q) and mask(q['prompt']) in lower], key=lambda q: q['id'])
            seen = {q['prompt'] for q in o.items()}
            done = 0
            for q in clones:
                if done >= ADV_PER_SKILL:
                    break
                r = random.Random('g4-adv|' + q['id'])
                try:
                    fm, prompt, ans, steps, wrong, opts, _f = make(gens, r, q['format'], seen, lower)
                except NoItem:
                    continue
                fields = {'prompt': prompt, 'answer': ans, 'solutionSteps': steps, 'sourceNotes': NOTE_A.format(fam=fm).replace('(#1, Advanced)', '(#1, Advanced; rewritten from a lower-level template)')}
                if q['format'] == 'multiple-choice':
                    fields['options'] = opts
                o.edit(q['id'], **fields)
                o.meta_set(q['id'], **meta_for(fm, steps, wrong, "multi-step", ans))
                done += 1


def run_standard(o):
    for u in UNITS:
        for skill, gens in sorted(fams.S.items()):
            if not skill.startswith(u + '-skill-'):
                continue
            items = [q for q in o.items(u) if q['skillId'] == skill]
            sup = {mask(q['prompt']) for q in items if q['level'] == 'cp2'}
            adv = {mask(q['prompt']) for q in items if q['level'] == 'honors'}
            seen = {q['prompt'] for q in o.items()}
            todo = [q for q in items if q['level'] == 'cp1' and q['id'] not in KEEP and plain(q) and mask(q['prompt']) in sup]
            todo.sort(key=lambda q: q['id'])
            for q in todo[:STD_PER_SKILL]:
                r = random.Random('g4-std|' + q['id'])
                old = (re.search(r'family: ([\w-]+)', q['sourceNotes']) or [0, 'unnamed'])[1]
                try:
                    fm, prompt, ans, steps, wrong, opts, _f = make(gens, r, q['format'], seen, sup | adv)
                except NoItem:
                    continue   # this skill's Standard family has no short-answer form
                fields = {'prompt': prompt, 'answer': ans, 'solutionSteps': steps, 'sourceNotes': NOTE_S.format(fam=fm, old=old)}
                if q['format'] == 'multiple-choice':
                    fields['options'] = opts
                o.edit(q['id'], **fields)
                o.meta_set(q['id'], **meta_for(fm, steps, wrong, "multi-step", ans))
