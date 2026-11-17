from collections import Counter
import math, random, time

RAW = (
    "DXXR KAKD QMDZ QJPV UQSGDWRM HXCO TGVL TLWE RHIPNJPA ZKNZ SCVP RJWD "
    "XRFTYRMH YUJI PEBD YOOS YNVESLGB OEJM HYIV AMMW TMWECYFI DLGD JWBT "
    "DWCJ OAWAAUZO VKCK PZXN VNJA KXCHGCHT MEZS IERW LCMH LZQEZSNJ MIKN "
    "XLEG QIEW UBESCWBQ XFAS KZWY CKKA RCNKRMPO JGBI JQZB OGFD EVDYUNID "
    "WMQB WNMS SAAQ JUGVAUIH WKRK LADI LCMH OCSFNGBW CYNM MATG SOKF "
    "RCPHPIDY DTYA NXWZ QBMW ZOUGYSSM TJTM PLXV MEDB QHPKIBWR NDHS SJIP "
    "PALV QFMQQKKE ZSZA AWNK SLNS HZWVYRMJ ESQT BSSA WMRA QEGPVPUJ DPQU "
    "WLDH TJJN NYACPJHS EWKL PJUA HNWW DLDGUNID WMQB OVTC VCKH PXMXWSSK "
    "RAEU IUGH RKLB MHJYVOJE JFUT RGDF ZHHX UPCSQMRD WOJM PYJB ZHHX MXIF"
).replace(" ", "")

lines = [RAW[i:i+20] for i in range(0, 500, 20)]

print("=== 1. Column-aligned repeats across the 25 lines (len >= 2) ===")
for length in (8, 4, 3, 2):
    hits = []
    for col in range(20 - length + 1):
        seen = {}
        for r, ln in enumerate(lines):
            sub = ln[col:col+length]
            seen.setdefault(sub, []).append(r)
        for sub, rows in seen.items():
            if len(rows) > 1:
                hits.append((col, sub, rows))
    print(f"Length {length}: {len(hits)} column-aligned repeats -> {hits[:15]}")

print("\n=== 2. Unaligned repeats anywhere in ciphertext (len >= 3) ===")
for length in (8, 4, 3):
    seen = {}
    for i in range(500 - length + 1):
        sub = RAW[i:i+length]
        seen.setdefault(sub, []).append((i, i // 20, i % 20))
    multi = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"Length {length}: {len(multi)} total repeats -> {list(multi.items())[:12]}")

print("\n=== 3. Line-by-line index of coincidence & repeated letters ===")
for r, ln in enumerate(lines):
    c = Counter(ln)
    dups = {k: v for k, v in c.items() if v > 1}
    if len(set(ln)) <= 12 or r < 5:
        print(f"Line {r:2d}: {ln} | unique={len(set(ln))} | dups={dups}")
