# Indus Script — a rigorous, *honest* analysis toolkit

This is **not** a decipherment. Nobody has a credible, accepted decipherment of the
Indus script, and any tool that claims to "read" it as language X is almost certainly
exploiting the circularity demonstrated below. This toolkit instead does what the
original `yajnadevam/ScriptDerivation` only *claims* to do: test the decipherability
question with an unbiased search and proper controls.

Pipeline (run in order):

| stage | script | question |
|-------|--------|----------|
| 1 | `load_corpus.py` | turn the indus-website SQL dump into clean sign sequences |
| 2 | `stats.py` | is the corpus language-like? is it past the unicity distance? |
| 3 | `search.py` | can a **blind** search read it as Sanskrit — and *only* Sanskrit? |

Data source: `indus-website/population-script.sql` (GLYPHSEQUENCE table) →
**2,543 inscriptions, 11,280 sign tokens, 592 distinct signs** (Mahadevan-scale;
the most frequent sign, the "jar," is 11.2% of tokens — a known corpus fact).

## What it found

**Stage 2 — the corpus is structured, and the unicity argument is necessary-but-not-sufficient.**
- Conditional entropy 3.61 bits vs 4.98 for an order-shuffled null → real sequential
  structure (leans toward Rao 2009 "language-like", against Farmer "non-linguistic").
- The aggregate corpus (11,280 tokens) **does exceed** the Shannon unicity distance
  (~1,200–1,750 tokens). So the author isn't numerically absurd. *But*: 34% of signs
  are hapax (appear once) and ~half appear ≤2×, so per-sign the key is **unidentifiable
  for a third of the inventory no matter how much corpus you add**. And the method
  inflates `H(key)` during solving (dictionary augmentation, multi-sign-per-syllable),
  which voids the bound outright.

**Stage 3 — the decisive control the whole debate was missing.**
A blind simulated-annealing search (no hardcoded answers) assigns each of the top-80
signs a syllable to maximize how much of the corpus segments into real dictionary words.
Run identically against four "languages":

```
                          BLIND-annealed % of 1083 inscriptions readable
dictionary       family   min word len = 2     min word len = 3
Tamil          Dravidian      100.0%               98.5%   \
Sanskrit       Indo-Aryan     100.0%               95.7%    |  FOUR real languages,
Gujarati       Indo-Aryan     100.0%               95.7%    |  two families, all tied
Telugu         Dravidian      100.0%               91.1%   /
English        (control)      100.0%               75.1%   <- unrelated language
Scrambled       null          100.0%               47.6%   <- not even a real lexicon
Random          null           48.8%               30.3%
```

**Conclusion:** "I can read the whole corpus" is *non-discriminative*. At a 2-letter
minimum every dictionary -- including random letters -- reads 100% under a blindly
optimized mapping. Under the stricter 3-letter rule, **Tamil/Dravidian (97.1%) reads the
corpus at least as well as Sanskrit (95.0%)** -- with a *smaller* dictionary (80k vs 134k),
so it is not a size artifact, and despite a phoneme-collapse step that was tuned to
Sanskrit phonology. The earlier apparent "Sanskrit edge" (vs English/nulls) vanishes the
moment a real rival language from the mainstream hypothesis is tested.

So the same method "proves" the Indus script is **Tamil** at least as strongly as it
"proves" Sanskrit. Both cannot be true -- which means the criterion ("readability =
decipherment") is the thing that is broken. This is the control experiment the entire
debate was missing, and it falsifies Yajnadevam's correctness criterion outright.

## Honest limitations
- Stage 3 searches the top-80 (most constrainable) signs, not all 592.
- The English control is transliterated into a collapsed alphabet; phonotactics differ.
- A genuine Old-Tamil/Dravidian lexicon would be a better second control than English.
- None of this proves the script *isn't* Sanskrit — it proves the *method* can't show it is.
