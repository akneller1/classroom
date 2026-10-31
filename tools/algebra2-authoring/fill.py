"""Fill a skill to a target count by calling randomized item makers; failed makers (duplicate prompt,
duplicate options, failed math assert) are rolled back cleanly so IDs stay contiguous."""
import copy


def skill_count(B, S):
    sid = f"{B.unit}-skill-{S:02d}"
    return sum(1 for q in B.qs if q["skillId"] == sid)


def fill(B, S, target, makers, rng, max_tries=400):
    tries = 0
    while skill_count(B, S) < target and tries < max_tries:
        tries += 1
        snap = (len(B.qs), dict(B.count), set(B.seen), dict(B.meta))
        try:
            rng.choice(makers)()
        except (AssertionError, ZeroDivisionError, ValueError, StopIteration):
            del B.qs[snap[0]:]; B.count = snap[1]; B.seen = snap[2]; B.meta = snap[3]
    return skill_count(B, S)
