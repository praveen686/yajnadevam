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

**Stage 4 — the *morphological* discriminator (paper §2.8.1) is two-edged, not decisive.**
Yajnadevam's real argument against Dravidian is not readability but morphology (after
Bonta 2023): that the same sign-strings recur in initial/medial/final positions, implying
fusional multi-stem *compounding* (Sanskrit) rather than position-locked agglutinative
suffixing (Dravidian). `morphology.py` measures this directly on the corpus:

- His positive claim holds only weakly, and weakens as strings get longer — exactly where
  his "3+-stem compound" argument needs it: of recurring length-3 substrings, **54% are
  position-LOCKED and only 6% appear in all three positions** (length-2: 60% mobile).
- The dominant positional signal is the *opposite* of fusional compounding: **7 signs lock
  to final position** (sign 817 → 88% final, 820 → 77%, 861 → 70%, …) and **~21% of all
  inscriptions end in just 5 signs.** Strong terminal markers are the classic *suffixing*
  signature — the very feature Mahadevan and Dravidianists read as evidence *for* a
  Dravidian/agglutinative language. (Yajnadevam concedes "the terminal jar sign is likely
  a case marker" — i.e. an affix-like element.)
- **Conclusion:** positional structure *underdetermines* the language family. A terminal
  marker is compatible with both a Sanskrit compound-final inflection and a Dravidian case
  suffix; sign positions alone cannot tell them apart. So §2.8.1 is necessary context, not
  a discriminator — the same verdict as readability (Stage 3) and aggregate unicity.
- *What we could not test:* the mixed Indus/Brahmi inscriptions (§2.8.3) are his one
  genuinely *external* anchor (sign values constrained by known Brahmi, reading Sanskrit).
  Confirming or refuting those needs that inscription set, which is not in this corpus —
  it is the live open question, not something Stages 1–4 settle.

## Honest limitations
- Stage 3 searches the top-80 (most constrainable) signs, not all 592.
- The English control is transliterated into a collapsed alphabet; phonotactics differ.
- A genuine Old-Tamil/Dravidian lexicon would be a better second control than English.
- Stage 4 measures sign *position*, not morpheme structure; without phonetic values it
  cannot prove a terminal marker is a suffix vs. a compound-final inflection — which is
  itself why positional data underdetermines the family.
- None of this proves the script *isn't* Sanskrit — it proves the *method* can't show it is.
