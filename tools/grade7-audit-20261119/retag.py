"""Grade 7 audit #11 (2026-11-19): standards tags say what an item practices.
 * Constructions vocabulary (spatial-thinking-skill-07) is G-CO.D.12, not 7.G.A.2 (drawing triangles from conditions);
   the 7.G.A.2 items added in batch G2 carry that tag.
 * Counting faces, edges and vertices (area-volume-skill-04) is not 7.G.A.3 (cross-sections); it keeps 6.G.A.4.
 * Angle pairs: parallel lines cut by a transversal are 8.G.A.5; complementary, supplementary and vertical angles are
   7.G.B.5, and the angle equations add 7.EE.B.4a.
 * Choosing a sampling method is 7.SP.A.1; predicting from a random sample is 7.SP.A.2.
 * Equations with no solution or infinitely many solutions are 8.EE.C.7a; one-solution equations are 8.EE.C.7b.
Idempotent; items added by later batches are tagged where they are written."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib


def tags_for(q):
    sk, p, a = q['skillId'], q['prompt'], str(q.get('answer'))
    text = p + ' ' + ' '.join(x.get('prompt', '') for x in q.get('parts', []))
    if '-g7-' in q['id']:
        return None
    if sk == 'spatial-thinking-skill-07':
        return [s for s in q['standards'] if s != '7.G.A.2'] or ['G-CO.D.12']
    if sk == 'area-volume-skill-04' and not re.search(r'cross.section|slice', text, re.I):
        return ['6.G.A.4']
    if sk == 'spatial-thinking-skill-02':
        if re.search(r'transversal|parallel', text, re.I):
            return ['8.G.A.5']
        if re.search(r'\(\d*x', text):
            return ['7.G.B.5', '7.EE.B.4a']
        return ['7.G.B.5']
    if sk == 'data-analysis-probability-skill-08':
        if re.search(r'sampling method|representative|biased', text, re.I):
            return ['7.SP.A.1']
        return ['7.SP.A.2', '7.RP.A.3']
    if sk == 'solving-equations-inequalities-skill-05':
        if re.search(r'no solution|infinitely many', text + ' ' + a, re.I):
            return ['8.EE.C.7a', '8.EE.C.7']
        return ['8.EE.C.7b', '8.EE.C.7']
    return None


def main():
    banks = lib.load()
    n = 0
    for u, q in lib.items(banks):
        t = tags_for(q)
        if t is not None and t != q['standards']:
            q['standards'] = t
            n += 1
    lib.save(banks)
    print('retagged:', n)


if __name__ == '__main__':
    main()
