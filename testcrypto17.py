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

# 1. Check column-wise reading (20 columns of 25 chars) for Product Cipher (Sub + Transposition)
cols20 = ["".join(lines[r][c] for r in range(25)) for c in range(20)]
col_stream = "".join(cols20)
def ioc(s):
    n = len(s)
    return sum(s.count(chr(65+i))*(s.count(chr(65+i))-1) for i in range(26)) / (n*(n-1))

print("1. Transposed (20x25 column-major) IoC:", round(ioc(col_stream), 4))
for p in range(1, 26):
    avg = sum(ioc(col_stream[o::p]) for o in range(p)) / p
    if avg > 0.048:
        print(f"   Column-major periodic IoC at period {p}: {avg:.4f}")

# 2. Check all 5 four-letter group positions (g = 0..4 -> cols 0..3, 4..7, 8..11, 12..15, 16..19)
#    for 2x2 Hill / digram IoC inside each 20-char line!
print("\n2. Group-specific (cols 0..3, 4..7, 8..11, 12..15, 16..19) 1-gram & 2-gram IoC:")
for g in range(5):
    grp_blocks = [ln[4*g:4*g+4] for ln in lines]
    flat = "".join(grp_blocks)
    d0 = [b[:2] for b in grp_blocks]
    d1 = [b[2:] for b in grp_blocks]
    di_ioc0 = sum(d0.count(x)*(d0.count(x)-1) for x in set(d0)) / (25*24)
    di_ioc1 = sum(d1.count(x)*(d1.count(x)-1) for x in set(d1)) / (25*24)
    print(f"   Group {g} (cols {4*g:2d}..{4*g+3:2d}): 1-gram IoC={ioc(flat):.4f} | first-digram IoC={di_ioc0:.4f} | second-digram IoC={di_ioc1:.4f}")

# 3. Check 2-letter digram IoC at EVERY column offset c = 0..18 across the 25 lines
print("\n3. Digram IoC at each column pair (c, c+1) across the 25 lines (random = 0.0015, English = ~0.0070):")
for c in range(19):
    digs = [ln[c:c+2] for ln in lines]
    d_ioc = sum(digs.count(x)*(digs.count(x)-1) for x in set(digs)) / (25*24)
    print(f"   Cols ({c:2d},{c+1:2d}): {d_ioc:.4f}", end="\n" if c % 4 == 3 else " | ")
