"""Write thin game pages: artifacts/<unit>-<game>/index.html for a menu skill set."""
import sys, os
repo, unit_dir, set_id, unit_label = sys.argv[1:5]
skills = sys.argv[5] if len(sys.argv) > 5 else ''
V = 'games-7'
GAMES = [('flashcards', 'Flashcards'), ('showdown', 'Showdown'), ('connect-four', 'Connect Four'), ('tic-tac-toe', 'Tic-Tac-Toe'), ('picture-reveal', 'Picture Reveal')]
skill_file = 'skills/' + set_id + '.js'
core = ['core/rng.js', 'core/frac.js', 'core/tex.js', 'core/graph.js?v=full-audit-v2', 'core/framework.js', 'core/render.js',
        'menu/mathcheck.js?v=menu-pow-1', 'menu/figures.js?v=menu-pow-1', 'menu/verify.js?v=menu-pow-1', 'menu/engine.js?v=menu-pow-1',
        'menu/skills/kit.js?v=menu-pow-1', 'menu/' + skill_file + '?v=menu-pow-1', 'menu/render.js?v=menu-pow-1', 'games/bank.js?v=' + V, 'games/games.js?v=' + V]
for g, name in GAMES:
    title = unit_label + ' ' + name if g != 'picture-reveal' else unit_label + ': Picture Reveal'
    d = os.path.join(repo, 'artifacts', unit_dir + '-' + g); os.makedirs(d, exist_ok=True)
    W = '../../worksheet-generator/'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{W}vendor/katex/katex.min.css">
<link rel="stylesheet" href="{W}games/games.css?v={V}">
</head>
<body data-unit="{set_id}" data-game="{g}" data-title="{title}"{(' data-skills="' + skills + '"') if skills else ''}>
<main id="app" class="gm-app"><div class="gm-panel gm-loading">Loading…</div></main>
<noscript><p style="padding:20px">This game needs JavaScript.</p></noscript>
<script src="{W}vendor/katex/katex.min.js"></script>
''' + ''.join(f'<script src="{W}{s}"></script>\n' for s in core) + '</body>\n</html>\n'
    open(os.path.join(d, 'index.html'), 'w').write(html)
    print(d)
