import math, operator, random, time

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
nums = [ord(c) - 65 for c in RAW]
lines = [nums[i:i+20] for i in range(0, 500, 20)]
cols_num = [[lines[r][c] for r in range(25)] for c in range(20)]

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
DI_FLAT = [0.0] * 676
for a in range(26):
    for b in range(26):
        p = TOP_DI.get(chr(65 + a) + chr(65 + b), 0.25 * ENG[a] * ENG[b])
        if a == 16 and b != 20:
            p *= 0.01
        DI_FLAT[a * 26 + b] = math.log(p)

# High-value English 4-grams & 5-grams
QUAD_LIST = [
    "TION","ATIO","THER","THAT","WITH","MENT","IONS","THIS","HERE","FROM",
    "OULD","IGHT","HAVE","HICH","WHIC","THES","THEI","EIR","EVER","WHER",
    "HERE","REVE","CONS","ONST","NSTA","STAN","TANT","TEMP","EMPE","MPER",
    "PERA","ERAT","RATU","ATUR","TURE","GREA","REAT","HEAT","CAVE","AVES",
    "DIST","ISTU","STUR","TURB","URBE","RBED","UNDIS","NDIST","CONGR",
    "UNDER","GROU","ROUN","OUND","WATE","ATER","EART","ARTH","DEEP","INTO",
    "SOME","MORE","MOST","ONLY","SUCH","ALSO","THAN","THEN","THEM","THEY",
    "WERE","BEEN","SAID","EACH","TIME","VERY","WHEN","WHAT","YOUR","WILL",
    "MAKE","LIKE","LONG","LOOK","MANY","PART","OVER","WORK","LIFE","EVEN",
    "BACK","GOOD","MUCH","WELL","DOWN","SIDE","FIND","HEAD","LAND","HAND",
    "HIGH","NEAR","NEXT","OPEN","SEEM","BOTH","FORM","KEEP","LAST","LEFT",
    "LESS","LINE","MIND","MOVE","MUST","NAME","NEED","ONCE","PLAY","REAL",
    "SAME","SHOW","TAKE","TELL","TURN","USED","WANT","WAYS","WORD","YEAR"
]
QUAD_SET = {w[:4] for w in QUAD_LIST if len(w) >= 4}
QUAD_ARR = [0.0] * (26 ** 4)
for q in QUAD_SET:
    idx = ((ord(q[0])-65)*17576 + (ord(q[1])-65)*676 + (ord(q[2])-65)*26 + (ord(q[3])-65))
    QUAD_ARR[idx] = 2.4

add = operator.add
get_di = DI_FLAT.__getitem__
get_q = QUAD_ARR.__getitem__

# Confirmed crib anchors from UNIDWMQB -> WHEREVER at cols 0..7
CRIB = {
    0: (ord('U')-65, ord('W')-65),
    1: (ord('N')-65, ord('H')-65),
    2: (ord('I')-65, ord('E')-65),
    3: (ord('D')-65, ord('R')-65),
    4: (ord('W')-65, ord('E')-65),
    5: (ord('M')-65, ord('V')-65),
    6: (ord('Q')-65, ord('E')-65),
    7: (ord('B')-65, ord('R')-65),
}

eng_order = sorted(range(26), key=lambda i: ENG[i], reverse=True)

def score_all(dec_cols):
    # Flatten 25x20 -> 500 stream
    stream = [dec_cols[c][r] for r in range(25) for c in range(20)]
    sc = sum(get_di(stream[i]*26 + stream[i+1]) for i in range(499))
    for i in range(497):
        sc += get_q(stream[i]*17576 + stream[i+1]*676 + stream[i+2]*26 + stream[i+3])
    return sc

best_overall = (-1e18, None)
for restart in range(5):
    perms = []
    locked_ct = [None] * 20
    for c in range(20):
        cnt = [cols_num[c].count(i) for i in range(26)]
        ct_order = sorted(range(26), key=lambda i: cnt[i] + random.random() * 0.5, reverse=True)
        p_map = [0] * 26
        for rank, ct_ch in enumerate(ct_order):
            p_map[ct_ch] = eng_order[rank]
        if c in CRIB:
            ct_fix, pt_fix = CRIB[c]
            locked_ct[c] = ct_fix
            other_ct = p_map.index(pt_fix)
            p_map[ct_fix], p_map[other_ct] = pt_fix, p_map[ct_fix]
        perms.append(p_map)

    dec_cols = [[perms[c][x] for x in cols_num[c]] for c in range(20)]
    cur_sc = score_all(dec_cols)

    for step in range(22000):
        temp = 2.2 * ((0.06 / 2.2) ** (step / 22000.0))
        c = random.randrange(20)
        a, b = random.sample(range(26), 2)
        if a == locked_ct[c] or b == locked_ct[c]:
            continue
        pa, pb = perms[c][a], perms[c][b]
        perms[c][a], perms[c][b] = pb, pa
        old_col = dec_cols[c]
        dec_cols[c] = [perms[c][x] for x in cols_num[c]]
        new_sc = score_all(dec_cols)
        if new_sc >= cur_sc or random.random() < math.exp((new_sc - cur_sc) / temp):
            cur_sc = new_sc
            if cur_sc > best_overall[0]:
                best_overall = (cur_sc, [p[:] for p in perms])
        else:
            perms[c][a], perms[c][b] = pa, pb
            dec_cols[c] = old_col

sc, best_perms = best_overall
print(f"Elapsed: {time.time() - t0:.2f}s | Score: {sc:.2f}\n")
full_pt = []
for r in range(25):
    ln = "".join(chr(65 + best_perms[c][cols_num[c][r]]) for c in range(20))
    full_pt.append(ln)
    print(f"{r:2d}: {ln}")

print("\nContinuous Plaintext:\n" + "".join(full_pt))
