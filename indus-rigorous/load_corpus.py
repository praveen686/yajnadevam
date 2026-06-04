#!/usr/bin/env python3
"""Stage 1: parse the indus-website SQL dump into a clean, analysis-ready corpus.

Outputs (under data/):
  sequences.tsv  : sealid \t space-separated glyphid sequence (in IDX order)
  glyphs.tsv     : glyphid \t unicode \t token_frequency
Prints a corpus summary.

No decipherment, no assumptions about language. Just the raw sign sequences.
"""
import re, sys, collections, os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_SQL = os.path.join(_HERE, "..", "indus-website", "population-script.sql")
SQL = sys.argv[1] if len(sys.argv) > 1 else _DEFAULT_SQL
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)

text = open(SQL, encoding="utf-8", errors="replace").read()

def block(table):
    """Return the text of the INSERT INTO <table> ... ; statement."""
    m = re.search(r"INSERT INTO %s\b.*?;" % re.escape(table), text, re.S)
    return m.group(0) if m else ""

# --- GLYPHSEQUENCE: (sealid, glyphid, idx) ---
seq_rows = re.findall(r"\((\d+),\s*(\d+),\s*(\d+)\)", block("GLYPHSEQUENCE"))
seqs = collections.defaultdict(list)           # sealid -> list of (idx, glyphid)
for sealid, glyphid, idx in seq_rows:
    seqs[int(sealid)].append((int(idx), int(glyphid)))

inscriptions = {}                               # sealid -> [glyphid,...] in idx order
for sealid, pairs in seqs.items():
    pairs.sort()
    inscriptions[sealid] = [g for _, g in pairs]

# --- GLYPH: (glyphid, "unicode") --- best-effort, sequences are the source of truth
uni = {}
for gid, code in re.findall(r'\((\d+)\s*,\s*"([^"]*)"\)', block("GLYPH")):
    uni[int(gid)] = code

# token frequencies straight from the sequences
freq = collections.Counter(g for s in inscriptions.values() for g in s)

# --- write clean files ---
with open(os.path.join(OUT, "sequences.tsv"), "w") as f:
    for sealid in sorted(inscriptions):
        f.write("%d\t%s\n" % (sealid, " ".join(map(str, inscriptions[sealid]))))

with open(os.path.join(OUT, "glyphs.tsv"), "w") as f:
    for gid in sorted(freq):
        f.write("%d\t%s\t%d\n" % (gid, uni.get(gid, ""), freq[gid]))

# --- summary ---
lengths = [len(s) for s in inscriptions.values()]
N_tok = sum(lengths)
V = len(freq)
hapax = sum(1 for g, c in freq.items() if c == 1)
import statistics as st
print("=== Indus corpus (from indus-website SQL) ===")
print(f"inscriptions (seals)      : {len(inscriptions)}")
print(f"sign tokens (total)       : {N_tok}")
print(f"distinct signs (types)    : {V}")
print(f"hapax signs (freq==1)      : {hapax}  ({100*hapax/V:.1f}% of types)")
print(f"mean inscription length   : {st.mean(lengths):.2f}")
print(f"median / max length       : {st.median(lengths)} / {max(lengths)}")
print(f"length histogram (len:count):")
lh = collections.Counter(lengths)
for L in sorted(lh)[:18]:
    bar = "#" * min(60, lh[L] * 60 // max(lh.values()))
    print(f"   {L:2d}: {lh[L]:5d} {bar}")
print("top 12 signs by frequency :")
for g, c in freq.most_common(12):
    print(f"   sign {g:4d}  freq {c:4d}  ({100*c/N_tok:.1f}%)")
