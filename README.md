# yajnadevam — a reproducible, critical evaluation of the "Indus script = Sanskrit" claim

This repo consolidates three things so the whole investigation lives in one place:

| folder | origin | what it is |
|--------|--------|------------|
| `ScriptDerivation/` | **vendored** from `github.com/yajnadevam/ScriptDerivation` | the author's original "decipherment" prover (`prove.pl`) + its toy corpus |
| `indus-website/`    | **vendored** from `github.com/yajnadevam/indus-website` | the author's corpus database; `population-script.sql` is our real data source |
| `indus-rigorous/`   | **our work** | a from-scratch toolkit that tests the claim honestly: data loader, statistics, and an unbiased blind search |

The two vendored folders are included unmodified (minus regenerable blobs) for
provenance and reproducibility. All original analysis is in `indus-rigorous/`.

---

## The question

Yajnadevam claims the *first complete decipherment of the Indus script as Paninian
Sanskrit*, justified by one criterion: **"the decipherment is correct because it can
read the corpus beyond the unicity distance."** We tested that criterion.

## What we did (all in `indus-rigorous/`, ~1 min to reproduce)

1. **`load_corpus.py`** — parse the real corpus out of `population-script.sql`:
   **2,543 inscriptions, 11,280 sign tokens, 592 distinct signs** (Mahadevan-scale).
2. **`stats.py`** — entropy / conditional-entropy / unicity-distance analysis vs nulls.
3. **`make_tamil.py`, `make_indic.py`** — transliterate Tamil, Gujarati, Telugu hunspell
   dictionaries into the same collapsed alphabet as the author's Sanskrit dictionary.
4. **`search.py`** — a **blind, anchor-free** decipherment search (simulated annealing).
   Unlike `prove.pl`, it is *not* told the answer; it assigns each sign a sound to
   maximize how much of the corpus segments into real dictionary words — then runs the
   identical protocol against 4 real languages + 3 null "languages."

```
cd indus-rigorous
python3 load_corpus.py        # corpus stats
python3 stats.py              # information theory
python3 make_tamil.py && python3 make_indic.py   # build control dictionaries
python3 search.py             # the decisive blind comparison
```

---

## Findings — separated by evidence tier (this distinction matters)

### Tier 1 — what our experiments actually measured (assumption-free)

**A. The original prover is circular.** `prove.pl` hardcodes the already-decided value of
every neighbouring sign into each regex (inscription `1-3` → regex `an(..?)`, where `an`
is sign 1's prior answer). It cannot derive a *different* assignment, so it proves
consistency of a pre-encoded solution, not a decipherment. Two of its own inscriptions
match **0** dictionary words yet still emit a value — the "contradiction detection" the
README relies on is not implemented.

**B. "Readability" has no power to identify the language.** The blind search, run
identically on every dictionary (fraction of 1,083 inscriptions made readable):

```
dictionary       family       min word len ≥2     min word len ≥3
Tamil          Dravidian          100%               ~98%   \
Sanskrit       Indo-Aryan         100%               ~96%    |  four real languages,
Gujarati       Indo-Aryan         100%               ~96%    |  two families — all tied
Telugu         Dravidian          100%               ~88%   /   (±noise between runs)
English        (control)          100%               ~70%   <- unrelated language
Scrambled       null              100%               ~50%   <- not even a real lexicon
Random          null            30-100%              ~30%
```

At a 2-letter minimum, *every* dictionary — including a scrambled non-lexicon — reads
**100%** of the corpus. Under a stricter rule, four unrelated real languages stay bunched
and statistically indistinguishable. **So "I can read the corpus as Sanskrit" is true —
but equally true for Gujarati, Tamil, and Telugu.** The criterion establishes nothing,
and the data shows *no preference for Sanskrit* (if anything Dravidian edges it, within
noise).

### Tier 2 — external context we did NOT measure (weaker, contested)

Mainstream historical linguistics + ancient-DNA work place Indo-Aryan's arrival/
differentiation in the 2nd millennium BCE, which would make *Paninian* Sanskrit on
2600–1900 BCE seals anachronistic. This **lowers the prior** on the Sanskrit hypothesis
but rests on a *reconstruction* that is genuinely debated (the migration vs. indigenous-
Aryan controversy). We cite it as context, not as something this repo proved.

---

## Conclusion (stated scientifically)

- **From the data:** the decipherment is **unidentified**, not merely unproven. Sanskrit
  is statistically indistinguishable from three other languages under the author's own
  test, so the test cannot single it out. P(valid Sanskrit decipherment | this evidence)
  ≈ P(Gujarati) ≈ P(Tamil) ≈ P(Telugu): the evidence is **uninformative** about identity.
- **With external context:** the dominant (contested) chronology further lowers the prior
  on Sanskrit specifically.
- **Net:** the claim "the Indus script is Sanskrit" is **unsupported and improbable, but
  not disproven.** The only fully honest label remains **undeciphered** — with Dravidian
  and "structured non-linguistic" as the live hypotheses.

Our work refutes the **method**, not the **hypothesis**. Killing the hypothesis itself
would require evidence we do not have.

## Honest limitations
- The blind search covers the top-80 (most constrainable) signs, not all 592.
- Dictionaries are mapped into a Sanskrit-tuned collapsed alphabet; that *helps* Sanskrit,
  and it still showed no edge.
- English is transliterated, not phonotactically faithful.
- None of this proves the script *isn't* Sanskrit — only that this method can't show it is.
