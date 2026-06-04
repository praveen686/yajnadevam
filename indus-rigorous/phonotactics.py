#!/usr/bin/env python3
"""Stage 5: test Yajnadevam's PHONOTACTICS defense (his talk, ~37:00 and live demo).

His rebuttal to "you could read it as any language": a cryptogram in language A
cannot be forced into language B because each language has a unique transition graph
(phonotactics), so beyond the unicity distance only the TRUE language fits. In the talk
he only ever *demonstrates Sanskrit's gaps* (greps Monier-Williams for non-existent
patterns); he never tests whether a RIVAL language fits the Indus corpus worse. This is
that missing control.

Stronger than Stage 3 (which scored word-segmentation): here we score the actual
phonotactic fit. For each candidate language we build a character bigram model from its
(collapsed-alphabet) lexicon, then run a blind simulated-annealing search that maps the
top-K Indus signs to letters so as to MINIMIZE the rendered corpus's per-bigram
cross-entropy under that language's model. We compare the best achievable fit across
languages, normalized by each language's own intrinsic bigram entropy.

Prediction if Yajnadevam is right: Sanskrit achieves a fit close to its intrinsic entropy
(gap ~ 0) while rivals cannot. Prediction if readability/Stage-3 is right: all real
languages reach a similar gap, i.e. phonotactic fit does not single out Sanskrit either.
No answer is given to the search; the mapping is optimized per language (which favors
each language equally).
"""
import random, collections, math, os

random.seed(17)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ScriptDerivation")
K = 80
ITERS = 4000
ALPHA = 0.5                      # add-k smoothing

# ---------- corpus ----------
seqs = [l.split('\t')[1].split() for l in open(os.path.join(DATA, "sequences.tsv"))]
freq = collections.Counter(s for q in seqs for s in q)
TOP = [g for g, _ in freq.most_common(K)]
topset = set(TOP)
corpus = [q for q in seqs if len(q) >= 2 and all(s in topset for s in q)]
contains = collections.defaultdict(list)
for i, q in enumerate(corpus):
    for s in set(q):
        contains[s].append(i)
print(f"phonotactics: K={K} signs, {len(corpus)} covered inscriptions, "
      f"{sum(len(q) for q in corpus)} tokens, {ITERS} iters/run\n")

# ---------- dictionaries ----------
def load(path, cap=200000):
    w = []
    for line in open(path, encoding="utf-8", errors="ignore"):
        x = line.strip().lower()
        if x:
            w.append(x)
            if len(w) >= cap:
                break
    return w

LANGS = {
    "Sanskrit  (Indo-Ary)": load(os.path.join(SD, "mw.txt")),
    "Gujarati  (Indo-Ary)": load(os.path.join(DATA, "gujarati_collapsed.txt")),
    "Tamil     (Dravidian)": load(os.path.join(DATA, "tamil_collapsed.txt")),
    "Telugu    (Dravidian)": load(os.path.join(DATA, "telugu_collapsed.txt")),
    "Scrambled (null)":      load(os.path.join(SD, "mw_scrambled.txt")),
}
ALPHABET = sorted({c for ws in LANGS.values() for w in ws for c in w})
LETTERS = [c for c in ALPHABET]
print(f"collapsed alphabet ({len(LETTERS)}): {''.join(LETTERS)}")

# ---------- per-language character bigram model ----------
def build_model(words):
    """bigram counts over ^word$, return logP(b|a) with add-ALPHA smoothing + intrinsic H."""
    syms = LETTERS + ["^", "$"]
    Vt = len(syms)
    ctx = collections.Counter()
    big = collections.Counter()
    for w in words:
        s = "^" + w + "$"
        for a, b in zip(s, s[1:]):
            ctx[a] += 1
            big[(a, b)] += 1
    def logp(a, b):
        return math.log((big[(a, b)] + ALPHA) / (ctx[a] + ALPHA * Vt))
    # intrinsic cross-entropy: mean NLL per bigram of the language's own words
    tot = 0.0; n = 0
    for w in words:
        s = "^" + w + "$"
        for a, b in zip(s, s[1:]):
            tot += -logp(a, b); n += 1
    return logp, tot / n

MODELS = {name: build_model(ws) for name, ws in LANGS.items()}

# ---------- blind search: minimize rendered-corpus bigram NLL under a model ----------
def insc_nll(mapping, q, logp):
    s = "^" + "".join(mapping[g] for g in q) + "$"
    return sum(-logp(a, b) for a, b in zip(s, s[1:]))

def anneal(logp):
    mapping = {g: random.choice(LETTERS) for g in TOP}
    nll = [insc_nll(mapping, q, logp) for q in corpus]
    cur = sum(nll)
    nbig = sum(len(q) + 1 for q in corpus)          # bigrams incl. boundaries
    best = cur
    for it in range(ITERS):
        T = max(0.01, 2.0 * (1 - it / ITERS))
        g = random.choice(TOP)
        old = mapping[g]
        new = random.choice(LETTERS)
        if new == old:
            continue
        aff = contains[g]
        before = sum(nll[i] for i in aff)
        mapping[g] = new
        after = sum(insc_nll(mapping, corpus[i], logp) for i in aff)
        d = after - before
        if d <= 0 or random.random() < math.exp(-d / T):
            for i in aff:
                nll[i] = insc_nll(mapping, corpus[i], logp)
            cur += d
            best = min(best, cur)
        else:
            mapping[g] = old
    return best / nbig                                # achieved mean NLL per bigram

print(f"\n{'language':22s} {'intrinsic H':>11s} {'achieved fit':>13s} {'gap':>7s}")
print("=" * 58)
rows = []
for name, (logp, H) in MODELS.items():
    fit = anneal(logp)
    rows.append((name, H, fit, fit - H))
    print(f"{name:22s} {H:11.3f} {fit:13.3f} {fit - H:+7.3f}")
print("\n(lower achieved fit = better phonotactic match; gap = achieved - intrinsic.")
print(" Yajnadevam's claim predicts Sanskrit gap ~0 and rivals' gap large.)")
