#!/usr/bin/env python3
"""Transliterate Gujarati (Indo-Aryan) and Telugu (Dravidian) hunspell dicts
into the SAME collapsed alphabet as Sanskrit, using the SAME collapse rules as
mw.txt: voiced stops kept (g/j/d/b), aspiration dropped, retroflex->dental,
nasals->n, sibilants->s, vocalic-r->r, anusvara->n, long vowels->doubled.
"""
import os, re
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ALPHA = "aiueokgcjtdpbnsrymvhlwq"

def cmap(pairs):                      # list of (hexbase, latin) -> {char: latin}
    return {chr(int(h, 16)): v for h, v in pairs}

# ---- Gujarati  (U+0A80) ----
GU_CONS = cmap([
 ("0A95","k"),("0A96","k"),("0A97","g"),("0A98","g"),("0A99","n"),
 ("0A9A","c"),("0A9B","c"),("0A9C","j"),("0A9D","j"),("0A9E","n"),
 ("0A9F","t"),("0AA0","t"),("0AA1","d"),("0AA2","d"),("0AA3","n"),
 ("0AA4","t"),("0AA5","t"),("0AA6","d"),("0AA7","d"),("0AA8","n"),
 ("0AAA","p"),("0AAB","p"),("0AAC","b"),("0AAD","b"),("0AAE","m"),
 ("0AAF","y"),("0AB0","r"),("0AB2","l"),("0AB3","l"),("0AB5","v"),
 ("0AB6","s"),("0AB7","s"),("0AB8","s"),("0AB9","h")])
GU_INDEP = cmap([
 ("0A85","a"),("0A86","aa"),("0A87","i"),("0A88","ii"),("0A89","u"),("0A8A","uu"),
 ("0A8B","r"),("0A8F","e"),("0A90","ai"),("0A93","o"),("0A94","au"),
 ("0A8D","e"),("0A91","o")])
GU_MATRA = cmap([
 ("0ABE","aa"),("0ABF","i"),("0AC0","ii"),("0AC1","u"),("0AC2","uu"),("0AC3","r"),
 ("0AC4","r"),("0AC7","e"),("0AC8","ai"),("0ACB","o"),("0ACC","au"),
 ("0AC5","e"),("0AC9","o")])
GU_VIRAMA, GU_NASAL = chr(0x0ACD), {chr(0x0A82),chr(0x0A81)}

# ---- Telugu  (U+0C00) ----
TE_CONS = cmap([
 ("0C15","k"),("0C16","k"),("0C17","g"),("0C18","g"),("0C19","n"),
 ("0C1A","c"),("0C1B","c"),("0C1C","j"),("0C1D","j"),("0C1E","n"),
 ("0C1F","t"),("0C20","t"),("0C21","d"),("0C22","d"),("0C23","n"),
 ("0C24","t"),("0C25","t"),("0C26","d"),("0C27","d"),("0C28","n"),
 ("0C2A","p"),("0C2B","p"),("0C2C","b"),("0C2D","b"),("0C2E","m"),
 ("0C2F","y"),("0C30","r"),("0C31","r"),("0C32","l"),("0C33","l"),("0C34","l"),
 ("0C35","v"),("0C36","s"),("0C37","s"),("0C38","s"),("0C39","h")])
TE_INDEP = cmap([
 ("0C05","a"),("0C06","aa"),("0C07","i"),("0C08","ii"),("0C09","u"),("0C0A","uu"),
 ("0C0B","r"),("0C0C","l"),("0C0E","e"),("0C0F","ee"),("0C10","ai"),
 ("0C12","o"),("0C13","oo"),("0C14","au"),("0C60","r")])
TE_MATRA = cmap([
 ("0C3E","aa"),("0C3F","i"),("0C40","ii"),("0C41","u"),("0C42","uu"),("0C43","r"),
 ("0C44","r"),("0C46","e"),("0C47","ee"),("0C48","ai"),("0C4A","o"),("0C4B","oo"),
 ("0C4C","au")])
TE_VIRAMA, TE_NASAL = chr(0x0C4D), {chr(0x0C02),chr(0x0C01)}

def make_translit(CONS, INDEP, MATRA, VIRAMA, NASAL):
    def f(w):
        out=[]; i=0; n=len(w)
        while i<n:
            ch=w[i]
            if ch in CONS:
                out.append(CONS[ch])
                nxt=w[i+1] if i+1<n else ''
                if nxt in MATRA: out.append(MATRA[nxt]); i+=2; continue
                if nxt==VIRAMA: i+=2; continue
                out.append('a'); i+=1; continue
            if ch in INDEP: out.append(INDEP[ch]); i+=1; continue
            if ch in NASAL: out.append('n'); i+=1; continue
            i+=1
        s="".join(out)
        return s if re.fullmatch("[%s]+"%ALPHA, s) else ""
    return f

def build(dic, tr, label, samples):
    words=set()
    with open(os.path.join(DATA,dic),encoding="utf-8") as fh:
        next(fh,None)
        for line in fh:
            t=tr(line.strip().split("/")[0])
            if t: words.add(t)
    out=os.path.join(DATA, label+"_collapsed.txt")
    open(out,"w").write("\n".join(sorted(words))+"\n")
    print(f"{label}: {len(words)} words")
    for raw in samples: print(f"   {raw} -> {tr(raw)}")
    return out

gu = make_translit(GU_CONS,GU_INDEP,GU_MATRA,GU_VIRAMA,GU_NASAL)
te = make_translit(TE_CONS,TE_INDEP,TE_MATRA,TE_VIRAMA,TE_NASAL)
build("gu_IN.dic", gu, "gujarati", ["ગુજરાત","પાણી","માછલી","નદી","ઘર"])
build("te_IN.dic", te, "telugu",   ["చేప","నీరు","ఇల్లు","నది","ఊరు"])
