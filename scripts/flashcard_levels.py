#!/usr/bin/env python3
"""Give the hand-made flashcard decks an Easy / Medium / Hard level filter.

Each card gets a "level" field. Within each skill the cards are written from easiest to hardest, so the
first third of a skill's cards are Easy, the middle third Medium and the last third Hard (a card that
already has a "level" keeps it, so a teacher can change one by hand). The page gets a Level menu
(All levels / Easy / Medium / Hard) next to the Skill menu, and the card tag shows the level.

Usage: python3 scripts/flashcard_levels.py artifacts/<deck>-flashcards/index.html [...]
Running it twice changes nothing."""
import json, re, sys

LEVELS = ['Easy', 'Medium', 'Hard']
SEL = '<label for="level">Level:</label>\n    <select id="level"><option value="All">All levels</option><option value="Easy">Easy</option><option value="Medium">Medium</option><option value="Hard">Hard</option></select>'


def patch(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'^const CARDS = (\[.*\]);$', s, re.M)
    if not m:
        return 'no CARDS'
    cards = json.loads(m.group(1))
    by = {}
    for c in cards:
        by.setdefault(c.get('skill', ''), []).append(c)
    for group in by.values():
        n = len(group)
        for i, c in enumerate(group):
            if c.get('level') not in LEVELS:
                c['level'] = LEVELS[min(2, int(3 * (i + 0.5) / n))]
    s = s[:m.start(1)] + json.dumps(cards, ensure_ascii=False) + s[m.end(1):]
    if 'id="level"' not in s:
        s = s.replace('<select id="skill"><option value="All">All skills</option></select>', '<select id="skill"><option value="All">All skills</option></select>\n    ' + SEL, 1)
    s = s.replace("deck=CARDS.filter(c=>(skill==='All'||c.skill===skill)&&", "const lv=byId('level')?byId('level').value:'All';\n  deck=CARDS.filter(c=>(skill==='All'||c.skill===skill)&&(lv==='All'||c.level===lv)&&", 1) if "c.level===lv" not in s else s
    s = s.replace("byId('skill').onchange=()=>selectDeck();", "byId('skill').onchange=()=>selectDeck();\nbyId('level').onchange=()=>selectDeck();", 1) if "byId('level').onchange" not in s else s
    s = s.replace("byId('tag').textContent=c?c.skill:'';", "byId('tag').textContent=c?c.skill+(c.level?' · '+c.level:''):'';", 1)
    s = s.replace("Choose another skill or leave missed-only mode.", "Choose another skill or level, or leave missed-only mode.")
    open(path, 'w', encoding='utf-8').write(s)
    return '%d cards: %s' % (len(cards), ', '.join('%s %d' % (L, sum(1 for c in cards if c['level'] == L)) for L in LEVELS))


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, patch(p))
