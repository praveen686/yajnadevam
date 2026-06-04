#!/usr/bin/env python3
"""Stage 4: test the *morphological* discriminator Yajnadevam uses to rule out
Dravidian (paper s2.8.1).

His argument (after Bonta 2023): the Indus inscriptions show "the same strings of
signs in initial, medial and final positions", which he reads as evidence of
fusional multi-stem COMPOUNDING (characteristic of Sanskrit) and *against*
agglutinative suffixing (Dravidian, where affixes are position-locked).

This is a *different* claim from readability, and our blind search (stage 3) does
not test it. Here we measure it directly on the real corpus, two ways:

  (A) Per-sign positional bias. Agglutinative/suffixing languages have a small set
      of high-frequency signs locked to FINAL position (case markers / postpositions).
      Fusional compounding predicts no such terminal lock. Mahadevan and others long
      noted strong terminal signs in the Indus corpus (the "jar"), historically read
      as a SUFFIX/marker -- i.e. a Dravidian-compatible signature. We quantify it.

  (B) Substring positional mobility. His positive claim: recurring multi-sign strings
      appear across initial/medial/final positions. We measure what fraction of
      recurring substrings are positionally mobile vs locked.

We report both, and state plainly what positional structure can and cannot decide.
No language is assumed anywhere.
"""
import collections, os, statistics as st

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
seqs = [l.rstrip("\n").split("\t")[1].split() for l in open(os.path.join(DATA, "sequences.tsv"))]
seqs = [q for q in seqs if len(q) >= 2]                 # need >=2 signs to have a position
N = len(seqs)
freq = collections.Counter(s for q in seqs for s in q)
TOT_TOK = sum(freq.values())
print(f"inscriptions (len>=2): {N}   tokens: {TOT_TOK}   distinct signs: {len(freq)}")

# ---------- (A) per-sign positional bias ----------
# For each sign, tally position-class of every occurrence in inscriptions of len>=2.
pos = collections.defaultdict(lambda: collections.Counter())   # sign -> {initial,medial,final}
for q in seqs:
    last = len(q) - 1
    for i, s in enumerate(q):
        cls = "initial" if i == 0 else ("final" if i == last else "medial")
        pos[s][cls] += 1

# expected final-rate if position were random ~ mean(1/len) weighted by occurrences;
# simplest fair baseline: corpus-wide share of tokens that are final = N/TOT_TOK
base_final = N / TOT_TOK
base_initial = N / TOT_TOK
print(f"\nbaseline (position-blind) initial-rate = final-rate = {base_final:.3f}")

MINF = 20
strong_final, strong_initial = [], []
for s, c in freq.items():
    if c < MINF:
        continue
    tot = sum(pos[s].values())
    fr = pos[s]["final"] / tot
    ir = pos[s]["initial"] / tot
    if fr >= 0.60:
        strong_final.append((s, c, fr))
    if ir >= 0.60:
        strong_initial.append((s, c, ir))

strong_final.sort(key=lambda x: -x[2])
strong_initial.sort(key=lambda x: -x[2])
print(f"\n(A) POSITIONAL LOCK among signs with freq>={MINF}:")
print(f"  strongly FINAL signs (final-rate>=0.60): {len(strong_final)}  "
      f"<- suffix/marker-like (agglutinative-compatible)")
for s, c, fr in strong_final[:8]:
    print(f"      sign {s:>4}  freq {c:4d}  final-rate {fr:.2f}")
print(f"  strongly INITIAL signs (initial-rate>=0.60): {len(strong_initial)}")
for s, c, ir in strong_initial[:8]:
    print(f"      sign {s:>4}  freq {c:4d}  initial-rate {ir:.2f}")

# how concentrated is "final position" on a few signs? (suffix systems => concentrated)
final_counter = collections.Counter()
for q in seqs:
    final_counter[q[-1]] += 1
topfinal = final_counter.most_common(5)
share = sum(c for _, c in topfinal) / N
print(f"\n  share of all {N} inscriptions ending in one of the top-5 terminal signs: {share:.1%}")
print(f"      top terminal signs: " + ", ".join(f"{s}({c})" for s, c in topfinal))

# ---------- (B) substring positional mobility ----------
def substrings(q, L):
    return [tuple(q[i:i+L]) for i in range(len(q) - L + 1)]

MINS = 5
for L in (2, 3):
    occ = collections.defaultdict(lambda: collections.Counter())   # gram -> position classes
    total = collections.Counter()
    for q in seqs:
        n = len(q)
        for i in range(n - L + 1):
            g = tuple(q[i:i+L])
            total[g] += 1
            cls = "initial" if i == 0 else ("final" if i + L == n else "medial")
            occ[g][cls] += 1
    recurring = [g for g, c in total.items() if c >= MINS]
    if not recurring:
        print(f"\n(B) L={L}: no substrings occur >= {MINS} times")
        continue
    mobile = sum(1 for g in recurring if len(occ[g]) >= 2)        # appears in >=2 position classes
    mobile3 = sum(1 for g in recurring if len(occ[g]) == 3)       # all three positions
    locked = len(recurring) - mobile
    print(f"\n(B) length-{L} substrings occurring >= {MINS}x : {len(recurring)}")
    print(f"      positionally MOBILE (>=2 position classes): {mobile} ({mobile/len(recurring):.0%})"
          f"   [his claim]")
    print(f"      in ALL three positions                    : {mobile3} ({mobile3/len(recurring):.0%})")
    print(f"      position-LOCKED (single class)            : {locked} ({locked/len(recurring):.0%})")
