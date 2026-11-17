import itertools, math

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

# Check mod-2 parity bias for each of the 5 group positions g = 0..4 (25 blocks each)
for g in range(5):
    blks = [[(ord(ln[4*g + j]) - 65) % 2 for j in range(4)] for ln in lines]
    ranked = []
    for u in itertools.product(range(2), repeat=4):
        if u != (0, 0, 0, 0):
            ev = sum(1 for b in blks if (u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3]) % 2 == 0)
            ranked.append((ev, u))
    ranked.sort(reverse=True)
    print(f"Group {g} (cols {4*g:2d}..{4*g+3:2d}) top mod-2 rows (out of 25): {ranked[:5]}")

# Also check if ANY single-letter column c=0..19 has an unusual frequency distribution (chi-squared)
ENG = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]
sorted_eng = sorted(ENG, reverse=True)
print("\nSorted letter frequency correlation per column c=0..19 (monoalphabetic check):")
for c in range(20):
    col = [lines[r][c] for r in range(25)]
    freqs = sorted([col.count(chr(65+i))/25.0 for i in range(26)], reverse=True)
    corr = sum(freqs[i]*sorted_eng[i] for i in range(26))
    print(f"col {c:2d}: max_cnt={int(freqs[0]*25)} corr={corr:.4f}", end="\n" if c % 4 == 3 else " | ")
