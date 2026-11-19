"""Shorthand for the Grade 6 teaching notes: rec(obj, idea, voc, watch, frame, *cards), card(h, big, *steps).
Text may hold ⟨TeX⟩ math and {{blanks}} (a blank is printed on completed notes and left empty on guided notes)."""


def card(h, big, *steps):
    return {'h': h, 'big': big, 'steps': list(steps)}


def rec(obj, idea, voc, watch, frame, *cards):
    return {'obj': obj, 'idea': idea, 'voc': [list(v) for v in voc], 'watch': watch, 'frame': frame, 'cards': list(cards)}
