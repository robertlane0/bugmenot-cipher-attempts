import math, random, time

t0 = time.time()
random.seed(42)

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

assert len(RAW) == 500
print("Unique letters in ciphertext:", len(set(RAW)), sorted(set(RAW)))
print("Letter counts:", {c: RAW.count(c) for c in sorted(set(RAW))})

# Check line-by-line (25 lines x 20 chars) properties
lines = [RAW[i:i+20] for i in range(0, 500, 20)]
for idx, ln in enumerate(lines):
    for g in ("LCMH", "UNID", "WMQB", "ZHHX"):
        if g in ln:
            print(f"Line {idx:2d} (pos {idx*20:3d}..{idx*20+19:3d}): {ln}  <-- contains {g} at col {ln.index(g)}")

# Fast English Quadgram / Digram scorer
ENG = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]
TOP_DI = {
    "TH":0.0356,"HE":0.0307,"IN":0.0243,"ER":0.0205,"AN":0.0199,"RE":0.0185,
    "ON":0.0176,"AT":0.0149,"EN":0.0145,"ND":0.0135,"TI":0.0134,"ES":0.0134,
    "OR":0.0128,"TE":0.0120,"OF":0.0117,"ED":0.0117,"IS":0.0113,"IT":0.0112,
    "AL":0.0109,"AR":0.0107,"ST":0.0105,"TO":0.0104,"NT":0.0104,"NG":0.0095,
    "SE":0.0093,"HA":0.0093,"AS":0.0087,"OU":0.0087,"IO":0.0083,"LE":0.0083,
    "VE":0.0083,"CO":0.0079,"ME":0.0079,"DE":0.0076,"HI":0.0076,"RI":0.0073,
    "RO":0.0073,"IC":0.0070,"NE":0.0069,"EA":0.0069,"RA":0.0069,"CE":0.0065,
    "LI":0.0062,"CH":0.0060,"LL":0.0058,"BE":0.0058,"MA":0.0057,"SI":0.0055,
    "OM":0.0055,"UR":0.0054,"CA":0.0054,"EL":0.0053,"TA":0.0053,"LA":0.0053,
    "NS":0.0051,"DI":0.0050,"FO":0.0049,"HO":0.0048,"PE":0.0048,"EC":0.0048,
    "PR":0.0047,"NO":0.0047,"CT":0.0046,"US":0.0045,"AC":0.0045,"OT":0.0044,
    "IL":0.0043,"TR":0.0043,"LY":0.0043,"NC":0.0042,"ET":0.0041,"UT":0.0041,
    "SS":0.0041,"SO":0.0040,"RS":0.0040,"UN":0.0039,"LO":0.0039,"WA":0.0039,
    "GE":0.0039,"IE":0.0038,"WH":0.0038,"EE":0.0038,"WI":0.0037,"EM":0.0037,
    "AD":0.0037,"OL":0.0036,"RT":0.0036,"PO":0.0036,"WE":0.0036,"NA":0.0035,
    "UL":0.0035,"NI":0.0035,"TS":0.0035,"MO":0.0034,"OW":0.0033,"PA":0.0033,
    "IM":0.0033,"MI":0.0032,"AI":0.0032,"SH":0.0032,"IR":0.0031,"SU":0.0031,
    "ID":0.0030,"OS":0.0030,"IV":0.0030,"IA":0.0029,"AM":0.0029,"FI":0.0029,
    "CI":0.0029,"VI":0.0027,"PL":0.0027,"IG":0.0026,"TU":0.0026,"EV":0.0026,
    "LD":0.0026,"RY":0.0025,"MP":0.0025,"FE":0.0024,"BL":0.0024,"AB":0.0024,
    "GH":0.0023,"TY":0.0023,"OP":0.0023,"WO":0.0023,"SA":0.0022,"AY":0.0022,
    "EX":0.0021,"KE":0.0021,"FR":0.0021,"OO":0.0021,"AV":0.0020,"AG":0.0020,
    "IF":0.0020,"AP":0.0020,"GR":0.0020,"OD":0.0019,"BO":0.0019,"SP":0.0019,
    "RD":0.0019,"DO":0.0019,"OB":0.0018,"GA":0.0018,"QU":0.0015,"CK":0.0015
}
DI_FLAT = [math.log(TOP_DI.get(chr(65+a)+chr(65+b), 0.25*ENG[a]*ENG[b])) for a in range(26) for b in range(26)]
def score_nums(arr):
    return sum(DI_FLAT[arr[i]*26 + arr[i+1]] for i in range(len(arr)-1))

# Test Trifid (27-symbol alphabet: A-Z + #) with SA over periods 5, 10, 20, 500
ALPHA27 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ#")
def dec_trifid(ct_idx, key27, period):
    pos = {ch: (i // 9, (i % 9) // 3, i % 3) for i, ch in enumerate(key27)}
    out = []
    for start in range(0, len(ct_idx), period):
        blk = ct_idx[start:start+period]
        n = len(blk)
        trips = []
        for ch in blk:
            trips.extend(pos[ch])
        r1, r2, r3 = trips[:n], trips[n:2*n], trips[2*n:3*n]
        for k in range(n):
            idx = r1[k]*9 + r2[k]*3 + r3[k]
            out.append(23 if idx == 26 else idx)  # map '#' -> X
    return out

best_tri = (-1e18, None, None)
for period in (20, 5, 10, 500):
    for _ in range(4):
        key = ALPHA27[:]
        random.shuffle(key)
        cur_pt = dec_trifid(RAW, key, period)
        cur_sc = score_nums(cur_pt)
        for step in range(2500):
            temp = 2.5 * ((0.15 / 2.5) ** (step / 2500.0))
            i, j = random.sample(range(27), 2)
            key[i], key[j] = key[j], key[i]
            n_pt = dec_trifid(RAW, key, period)
            n_sc = score_nums(n_pt)
            if n_sc >= cur_sc or random.random() < math.exp((n_sc - cur_sc) / temp):
                cur_sc = n_sc
                if cur_sc > best_tri[0]:
                    best_tri = (cur_sc, period, "".join(key), "".join(chr(65+x) for x in n_pt))
            else:
                key[i], key[j] = key[j], key[i]

print(f"\nBest Trifid (elapsed {time.time()-t0:.2f}s) | Period {best_tri[1]} | Score {best_tri[0]:.1f}")
print("Key:", best_tri[2])
print("PT: ", best_tri[3][:160])
