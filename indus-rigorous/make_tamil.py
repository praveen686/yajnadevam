#!/usr/bin/env python3
"""Transliterate the LibreOffice Tamil hunspell dict into the SAME collapsed
alphabet used for Sanskrit/English, so the blind search treats it identically.

Tamil Unicode -> Latin, then the same collapse philosophy as mw.txt:
retroflex->dental, all nasals->n, sibilants->s, zh->r, long vowels->doubled.
"""
import os, re
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

cons = {  # consonant base -> collapsed latin (inherent 'a' added later)
 'க':'k','ங':'n','ச':'c','ஜ':'j','ஞ':'n','ட':'t','ண':'n','த':'t','ந':'n',
 'ன':'n','ப':'p','ம':'m','ய':'y','ர':'r','ற':'r','ல':'l','ள':'l','ழ':'r',
 'வ':'v','ஶ':'s','ஷ':'s','ஸ':'s','ஹ':'h'}
indep = {'அ':'a','ஆ':'aa','இ':'i','ஈ':'ii','உ':'u','ஊ':'uu','எ':'e','ஏ':'ee',
 'ஐ':'ai','ஒ':'o','ஓ':'oo','ஔ':'au','ஃ':''}
matra = {'ா':'aa','ி':'i','ீ':'ii','ு':'u','ூ':'uu','ெ':'e','ே':'ee','ை':'ai',
 'ொ':'o','ோ':'oo','ௌ':'au'}
PULLI = '்'

def translit(w):
    out = []; i = 0; n = len(w)
    while i < n:
        ch = w[i]
        if ch in cons:
            out.append(cons[ch])
            nxt = w[i+1] if i+1 < n else ''
            if nxt in matra: out.append(matra[nxt]); i += 2; continue
            if nxt == PULLI: i += 2; continue        # bare consonant
            out.append('a'); i += 1; continue         # inherent vowel
        if ch in indep: out.append(indep[ch]); i += 1; continue
        i += 1                                        # skip digits/aaytham/etc.
    s = "".join(out)
    return s if re.fullmatch(r"[aiueokgcjtdpbnsrymvhlwq]+", s) else ""

words = set()
with open(os.path.join(DATA, "ta_IN.dic"), encoding="utf-8") as f:
    next(f, None)                                     # skip count line
    for line in f:
        base = line.strip().split("/")[0]             # drop hunspell affix flags
        t = translit(base)
        if t:
            words.add(t)

with open(os.path.join(DATA, "tamil_collapsed.txt"), "w") as f:
    for w in sorted(words):
        f.write(w + "\n")

print(f"Tamil words transliterated: {len(words)}")
print("samples:")
for raw in ["அரசன்", "தமிழ்", "கடல்", "மீன்", "நீர்", "மரம்", "வீடு", "பெண்"]:
    print(f"  {raw}  ->  {translit(raw)}")
