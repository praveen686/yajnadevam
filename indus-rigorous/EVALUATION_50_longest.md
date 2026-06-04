# Evaluation of Yajnadevam's "50 Longest Indus inscriptions and their [readings]"

Object evaluated: `../50_Longest_Indus_inscriptions_and_their.pdf` (the author's flagship
evidence — the 50 longest inscriptions, each given a Sanskrit reading, translation,
word-by-word grammatical gloss with dictionary citations, and a Rigveda "reference").

This is the concrete artifact behind the "we read beyond the unicity distance" claim. It is
serious, internally consistent, laborious work on **real** CISI seals (M-314, H-1657, …),
and the readings are genuine grammatical Sanskrit, not invented words. Evaluated as
*evidence for the decipherment*, however, it is a **readability showcase** — and readability
is exactly the criterion `search.py` (Stage 3) shows to be non-discriminating (four
unrelated languages read the corpus equally well). Four properties of the document, each
demonstrable from it, explain why the readings look compelling without being evidence.

## 1. The "scriptural references" share no vocabulary with the readings
Each reading is printed next to a Rigveda verse *translation*, suggesting corroboration.
But the RV verse and the reading are different texts with **no shared words** — the pairing
is thematic only:

| # | reading (translit.) | cited verse | shared words |
|---|---------------------|-------------|--------------|
| 5 | `dhakka vaha māṃsaja-āśa-varam` | RV 10.169.1 "waters rich in fatness… O Rudra" | none (theme: Rudra/fat) |
| 6 | `tat-dadanam rava amam-añjas-saraṃ` | RV 9.80.2 "powerful Soma…" | none (theme: Soma) |
| 11 | `dadā tava vaśam añja-dahra` | RV 1.36.11 "Agni… powers shine out" | none (theme: Agni) |

So the Vedic citations are **unfalsifiable thematic garnish**, not textual matches.

## 2. An anachronistic, ~3,000-year dictionary inflates the key space
Word-source tags span the entire diachronic range of Sanskrit, used to read 2600–1900 BCE
seals. Tag frequencies in the document: **80× [RV]** (Ṛgveda) but also **17× [MBh]**
(Mahābhārata), **5× [Hariv]** (Harivaṃśa, ~1st–4th c. **CE**), **3× [BhP]** (Bhāgavata
Purāṇa, ~9th–10th c. **CE**), plus **[Śiś]** (Śiśupālavadha, 7th c. CE court epic),
**[Suśr]** (Suśruta medical saṃhitā), **[Kāv]** (classical kāvya). Examples in situ:
`māṃsaja` "fat" [Suśr]; `mākha` "oblation" [Hariv] (recurring); `varam` "choicest" [MBh].

Drawing vocabulary from texts up to **three–four thousand years later** than the seals is a
fundamental anachronism, and — in the paper's own cryptographic terms — it is precisely the
**H(key) inflation that voids the unicity bound** (paper §2.4.2). "Beyond the unicity
distance" assumes one fixed source language; a Rigvedic-to-medieval lexicon is effectively a
much larger key, so reading "past" the bound is expected, not surprising.

## 3. Free morphological generation makes almost any string parseable
Nearly every content word is built as *root + freely chosen affix*: `vaha`[√vah+loṭ 2s],
`rava`[√ru+ac], `āma`[√am+loṭ 1s], `mamada`[√mad+liṭ 1s], `vaja`[√vaj+loṭ 2s]. Imperatives,
perfects, agent-nouns and participles are assigned at will; combined with free
word-segmentation, sandhi, and **bracketed supplied letters** (e.g. `aśva-modā[n]` — adding
a sign not in the inscription), grammatical Sanskrit becomes achievable for nearly any
phoneme string. Achieving it therefore is not evidence the underlying language is Sanskrit.

## 4. Thematic monotony is a tell, not a confirmation
Nearly all 50 read as invocations to Rudra/Shiva/Soma/sacrifice: ~**31× "roar(er)", 12×
soma, 10× Rudra, 9× cup, 14× sacrifice**. This is (a) exactly the decipherer's prior
expectation (Vedic religion) — the signature of confirmation bias — and (b) unlike a real
seal corpus, which mainstream scholarship reads as names / titles / administration / trade.
Near-uniform Shaivite hymnody is what a flexible method *produces*, not what a decipherment
necessarily *finds*.

## Verdict
The document **showcases readability**, which we have already shown is non-discriminating;
the four properties above explain why the readings look convincing without identifying the
language. This is **not a disproof** — the readings could in principle be correct — but it
provides **no discriminating evidence**, and it does not engage the one genuinely external
anchor (mixed Indus/Brahmi inscriptions, paper §2.8.3), which is absent from this file. Net:
it reinforces the Stage 3 conclusion and adds one sharp, concrete point beyond the abstract
unicity argument — the **anachronistic multi-millennium lexicon**.
