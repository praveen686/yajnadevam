#!/usr/bin/env python3
"""Stage 2: statistical / null-model harness on the real Indus sign sequences.

Three honest questions:
  (1) Is the corpus 'language-like' in its sequential structure?
      -> unigram vs conditional (bigram) entropy, compared to shuffled & uniform nulls
         (the Rao et al. 2009 test, with the Sproat caveat noted in the writeup).
  (2) How constrainable is the sign inventory at all?
      -> per-sign occurrence distribution; a sign seen once can never be cross-checked.
  (3) What does the unicity-distance argument actually require, numerically?
      -> H(key)/redundancy in sign-tokens, with assumptions stated and varied.

No language is assumed anywhere here. This measures the corpus, not a reading.
"""
import math, collections, os, random

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
random.seed(7)

# --- load sequences ---
seqs = []
for line in open(os.path.join(DATA, "sequences.tsv")):
    sid, rest = line.rstrip("\n").split("\t")
    seqs.append(rest.split())

tokens = [s for seq in seqs for s in seq]
N = len(tokens)
freq = collections.Counter(tokens)
V = len(freq)

def H(counter):
    tot = sum(counter.values())
    return -sum((c/tot)*math.log2(c/tot) for c in counter.values())

H1 = H(freq)                       # unigram entropy (bits/sign)
Hmax = math.log2(V)                # max possible (uniform over V)

# --- conditional entropy H(next | prev) using bigrams with boundary markers ---
def cond_entropy(sequences):
    bi = collections.Counter()
    uni = collections.Counter()
    for seq in sequences:
        s = ["<S>"] + seq + ["</S>"]
        for a, b in zip(s, s[1:]):
            bi[(a, b)] += 1
            uni[a] += 1
    # H(B|A) = sum_a p(a) * H(B|A=a)
    by_a = collections.defaultdict(collections.Counter)
    for (a, b), c in bi.items():
        by_a[a][b] += c
    total = sum(uni.values())
    h = 0.0
    for a, cnt in by_a.items():
        pa = uni[a] / total
        h += pa * H(cnt)
    return h

Hcond_real = cond_entropy(seqs)

# null: shuffle all tokens, keep length structure -> destroys sequential order
def shuffled_corpus():
    pool = tokens[:]
    random.shuffle(pool)
    out, i = [], 0
    for seq in seqs:
        out.append(pool[i:i+len(seq)]); i += len(seq)
    return out

Hcond_shuf = sum(cond_entropy(shuffled_corpus()) for _ in range(5)) / 5

print("=" * 64)
print("(1) LANGUAGE-LIKENESS  (entropy in bits per sign)")
print("=" * 64)
print(f"  V (sign types)                         : {V}")
print(f"  H_max  = log2(V)  [uniform upper bound] : {Hmax:.3f}")
print(f"  H1     unigram entropy                  : {H1:.3f}")
print(f"  H(next|prev)  real corpus               : {Hcond_real:.3f}")
print(f"  H(next|prev)  order-shuffled null (x5)  : {Hcond_shuf:.3f}")
drop = Hcond_shuf - Hcond_real
print(f"  sequential structure (shuf - real)      : {drop:.3f}  "
      f"({'present' if drop > 0.15 else 'WEAK'})")
print("  --> a real language sits well below H1 in conditional entropy;")
print("      a random system sits at H1; rigid/DNA-like sits near 0.")

print()
print("=" * 64)
print("(2) CONSTRAINABILITY OF THE SIGN INVENTORY")
print("=" * 64)
occ = collections.Counter(freq.values())          # how many signs have freq k
cum = 0
for k in [1, 2, 3, 4, 5]:
    nsign = sum(n for f, n in occ.items() if f == k)
    print(f"  signs occurring exactly {k}x : {nsign:4d}")
ge = lambda t: sum(1 for c in freq.values() if c >= t)
print(f"  signs occurring 1x (hapax)  : {ge(1)-ge(2):4d}  "
      f"({100*(ge(1)-ge(2))/V:.0f}% of inventory -> NOT cross-checkable)")
print(f"  signs occurring >= 2x        : {ge(2):4d}  ({100*ge(2)/V:.0f}%)")
print(f"  signs occurring >= 5x        : {ge(5):4d}  ({100*ge(5)/V:.0f}%)")
print(f"  signs occurring >=10x        : {ge(10):4d}  ({100*ge(10)/V:.0f}%)")

# bigram repetition: how much repeated context exists to constrain on?
bigrams = collections.Counter()
for seq in seqs:
    for a, b in zip(seq, seq[1:]):
        bigrams[(a, b)] += 1
rep_bi = sum(1 for c in bigrams.values() if c >= 2)
print(f"  distinct bigrams             : {len(bigrams)}")
print(f"  bigrams repeating (>=2x)     : {rep_bi}  ({100*rep_bi/len(bigrams):.0f}%)")

print()
print("=" * 64)
print("(3) UNICITY DISTANCE  (what the README's claim actually needs)")
print("=" * 64)
print("  U = H(key) / D    [Shannon], in sign-tokens of ciphertext")
print("  D (redundancy/sign) measured from the corpus itself:")
for label, Hbase in [("vs uniform (H_max - H1)", Hmax - H1),
                     ("vs conditional (H1 - Hcond)", H1 - Hcond_real)]:
    print(f"    D = {Hbase:5.3f}  [{label}]")
# key entropy: each of V signs -> one of A candidate phoneme-values
print("  H(key) = V * log2(A)   (A = candidate values per sign):")
D_choices = Hmax - H1   # most generous (largest) redundancy -> smallest U
for A in [30, 60, 120]:
    Hk = V * math.log2(A)
    U = Hk / max(D_choices, 1e-9)
    verdict = "corpus EXCEEDS U" if N > U else "corpus BELOW U"
    print(f"    A={A:4d}: H(key)={Hk:7.0f} bits -> U ~= {U:8.0f} tokens  "
          f"[{N} available -> {verdict}]")

print()
print("  So the AGGREGATE corpus passes the unicity test. But that is")
print("  necessary, NOT sufficient. Why it still doesn't give uniqueness:")
# (a) redundancy is concentrated on a few signs; a third of the key is starved.
top12 = sum(c for _, c in freq.most_common(12))
hapax_tok = ge(1) - ge(2)
print(f"  (a) redundancy is NON-uniform: top 12 signs = {100*top12/N:.0f}% of all")
print(f"      tokens, while {hapax_tok} hapax signs ({100*hapax_tok/V:.0f}% of the key)")
print(f"      get ONE observation each. The U-formula averages over this;")
print(f"      per-sign, ~half the inventory (<=2 occurrences) is unidentifiable")
print(f"      no matter how many more inscriptions you add.")
print(f"  (b) D here is the corpus's own sign redundancy; Shannon needs the")
print(f"      PLAINTEXT (collapsed-Sanskrit) redundancy, which is lower -> U larger.")
print(f"  (c) FATAL: the method inflates H(key) while solving (dictionary")
print(f"      augmentation, multi-sign-per-syllable, free vowels/sandhi). If the")
print(f"      key can grow on demand, U is unbounded and the proof is void.")
