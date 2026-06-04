#!/usr/bin/env python3
"""Stage 3: BLIND, anchor-free decipherment search.

The original prove.pl hardcodes the answer into each regex. This does not.
Each of the top-K signs is an unknown that the search assigns a phoneme
syllable to. We score a mapping purely by how much of the corpus it turns
into valid dictionary words (word-break segmentation) -- the answer is never
given. We then run the IDENTICAL search and budget against control
"languages" to see whether real Sanskrit is statistically special.

A mapping that lets you "read the corpus" only means something if a
letter-statistics-matched impostor dictionary CANNOT do equally well.
"""
import random, collections, math, sys, os

random.seed(13)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
# portable: ScriptDerivation sits next to indus-rigorous in this repo
SD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ScriptDerivation")
K = 80
ITERS = 6000

# ---------- corpus ----------
seqs = [l.split('\t')[1].split() for l in open(os.path.join(DATA, "sequences.tsv"))]
freq = collections.Counter(s for q in seqs for s in q)
TOP = [g for g, _ in freq.most_common(K)]
topset = set(TOP)
corpus = [q for q in seqs if len(q) >= 2 and all(s in topset for s in q)]
# index: which inscriptions contain each sign (for incremental rescoring)
contains = collections.defaultdict(list)
for i, q in enumerate(corpus):
    for s in set(q):
        contains[s].append(i)
print(f"blind search: K={K} signs, {len(corpus)} covered inscriptions, "
      f"{sum(len(q) for q in corpus)} tokens, {ITERS} iters/run")

# ---------- syllable inventory (over the collapsed alphabet) ----------
C = list("kgcjtdpbnsrymvhlwq")
Vw = ["a", "i", "u", "e", "o"]
SYLL = Vw[:] + C[:] + [c + v for c in C for v in Vw]   # ~ 5+17+85 = 107 values

# ---------- dictionaries ----------
def load_words(path, cap=200000):
    w = set()
    for line in open(path):
        x = line.strip()
        if x:
            w.add(x)
            if len(w) >= cap:
                break
    return w

def random_dict(like, n):
    """control: n random words, lengths sampled from `like`, letters iid by freq."""
    letters = list("aiueokgcjtdpbnsrymvhlwq")
    lens = [len(x) for x in like]
    out = set()
    while len(out) < n:
        L = random.choice(lens)
        out.add("".join(random.choice(letters) for _ in range(L)))
    return out

def load_english(path, cap=200000):
    """real-language control: English mapped into the collapsed alphabet."""
    keep = set("aiueokgcjtdpbnsrymvhlwq")
    tr = str.maketrans({"f": "p", "x": "k", "z": "s"})  # missing letters -> nearest
    w = set()
    for line in open(path, encoding="utf-8", errors="ignore"):
        x = line.strip().lower()
        if not x.isalpha():
            continue
        x = x.translate(tr)
        x = "".join(ch for ch in x if ch in keep)
        if x:
            w.add(x)
            if len(w) >= cap:
                break
    return w

sanskrit = load_words(os.path.join(SD, "mw.txt"))
scrambled = load_words(os.path.join(SD, "mw_scrambled.txt"))
randdict = random_dict(sanskrit, len(scrambled))
english = load_english("/usr/share/dict/american-english")
tamil = load_words(os.path.join(DATA, "tamil_collapsed.txt"))
gujarati = load_words(os.path.join(DATA, "gujarati_collapsed.txt"))
telugu = load_words(os.path.join(DATA, "telugu_collapsed.txt"))
DICTS = {"Sanskrit  (Indo-Ary)": sanskrit,
         "Gujarati  (Indo-Ary)": gujarati,
         "Tamil     (Dravidian)": tamil,
         "Telugu    (Dravidian)": telugu,
         "English   (control)": english,
         "Scrambled (null)": scrambled,
         "Random    (null)": randdict}

# ---------- word-break scorer ----------
def make_segmentable(words, minlen, maxlen=14):
    wl = {}                      # length -> set of words of that length
    for w in words:
        if minlen <= len(w) <= maxlen:
            wl.setdefault(len(w), set()).add(w)
    lengths = sorted(wl)
    def seg(s):                  # can s be fully split into dict words?
        n = len(s)
        ok = [False] * (n + 1); ok[0] = True
        for i in range(1, n + 1):
            for L in lengths:
                j = i - L
                if j < 0: break
                if ok[j] and s[j:i] in wl[L]:
                    ok[i] = True; break
        return ok[n]
    return seg

def render(mapping, q):
    return "".join(mapping[s] for s in q)

def score(mapping, seg):
    return sum(1 for q in corpus if seg(render(mapping, q)))

# ---------- simulated annealing (blind) ----------
def anneal(seg):
    mapping = {s: random.choice(SYLL) for s in TOP}
    cur = score(mapping, seg)
    best = cur
    for it in range(ITERS):
        T = max(0.01, 1.5 * (1 - it / ITERS))
        s = random.choice(TOP)
        old = mapping[s]
        new = random.choice(SYLL)
        if new == old:
            continue
        # incremental: only inscriptions containing s change
        affected = contains[s]
        before = sum(1 for i in affected if seg(render(mapping, corpus[i])))
        mapping[s] = new
        after = sum(1 for i in affected if seg(render(mapping, corpus[i])))
        d = after - before
        if d >= 0 or random.random() < math.exp(d / T):
            cur += d
            if cur > best:
                best = cur
        else:
            mapping[s] = old
    return best

def random_baseline(seg, trials=8):
    vals = []
    for _ in range(trials):
        m = {s: random.choice(SYLL) for s in TOP}
        vals.append(score(m, seg))
    return sum(vals) / len(vals)

# ---------- run identical protocol for every dictionary ----------
M = len(corpus)
for minlen in (2, 3):
    print("\n" + "=" * 66)
    print(f"min word length = {minlen}   (fraction of {M} inscriptions readable)")
    print("=" * 66)
    print(f"{'dictionary':18s} {'random-map':>12s} {'BLIND-annealed':>15s}")
    for name, words in DICTS.items():
        seg = make_segmentable(words, minlen)
        rb = random_baseline(seg)
        bb = anneal(seg)
        print(f"{name:22s} {rb/M*100:11.1f}% {bb/M*100:14.1f}%  "
              f"({bb}/{M})")
