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
DI_FLAT = [math.log(TOP_DI.get(chr(65+a)+chr(65+b), 0.25*ENG[a]*ENG[b]) * (0.01 if a==16 and b!=20 else 1.0))
           for a in range(26) for b in range(26)]
get_di = DI_FLAT.__getitem__

# ==============================================================================
# TEST 1: Exact Global Viterbi for Periodic Affine Cipher (C = a_c * P + b_c mod 26)
# ==============================================================================
COPRIME = [a for a in range(1, 26, 2) if a != 13]
AFF_MAPS = []
for a in COPRIME:
    inv_a = pow(a, -1, 26)
    for b in range(26):
        # Decryption map ct -> pt
        AFF_MAPS.append(((a, b), tuple((inv_a * (ct - b)) % 26 for ct in range(26))))

# Precompute decoded columns for all 312 affine maps per column
col_aff_dec = [[tuple(mp[x] for x in cols_num[c]) for _, mp in AFF_MAPS] for c in range(20)]
dp_prev = [0.0] * 312
back = [[0] * 312 for _ in range(20)]

for c in range(1, 20):
    dp_cur = [-1e18] * 312
    prev_cands = col_aff_dec[c - 1]
    cur_cands = col_aff_dec[c]
    # Keep top 80 states from c-1 for speed
    top_prev = sorted(range(312), key=lambda i: dp_prev[i], reverse=True)[:80]
    for j in range(312):
        cj = cur_cands[j]
        best_v, best_i = -1e18, 0
        for i in top_prev:
            pi = prev_cands[i]
            sc = dp_prev[i] + sum(get_di(pi[r]*26 + cj[r]) for r in range(25))
            if sc > best_v:
                best_v, best_i = sc, i
        dp_cur[j] = best_v
        back[c][j] = best_i
    dp_prev = dp_cur

best_j = max(range(312), key=lambda j: dp_prev[j])
aff_idx = [0] * 20
aff_idx[19] = best_j
for c in range(19, 0, -1):
    aff_idx[c - 1] = back[c][aff_idx[c]]

aff_pt = "".join(chr(65 + col_aff_dec[c][aff_idx[c]][r]) for r in range(25) for c in range(20))
print(f"=== TEST 1: Periodic Affine (312 maps/col, elapsed {time.time()-t0:.2f}s) ===")
print(f"Score: {dp_prev[best_j]:.2f} | PT[:120]: {aff_pt[:120]}")

# ==============================================================================
# TEST 2: Line-Resetting Enigma / Reciprocal Involutions (13 disjoint pairs/col)
# ==============================================================================
# Check first if ANY column has a fixed point under our previous WHEREVER/TEMPERATURES cribs:
# Notice UNIDWMQB -> WHEREVER has NO fixed points (U!=W, N!=H, I!=E, D!=R, W!=E, M!=V, Q!=E, B!=R)!
# AND TEMPERATURES (MPLXV + MEDBQHP) has NO fixed points (M!=T, P!=E, L!=M, X!=P, V!=E, M!=R, E!=A, D!=T, B!=U, Q!=R, H!=E, P!=S)!
def rand_involution():
    arr = list(range(26))
    random.shuffle(arr)
    inv = [0] * 26
    for i in range(0, 26, 2):
        a, b = arr[i], arr[i + 1]
        inv[a], inv[b] = b, a
    return inv

best_enigma = (-1e18, None)
for restart in range(6):
    invs = [rand_involution() for _ in range(20)]
    stream = [invs[c][cols_num[c][r]] for r in range(25) for c in range(20)]
    cur_sc = sum(get_di(stream[i]*26 + stream[i+1]) for i in range(499))
    for step in range(22000):
        temp = 2.2 * ((0.04 / 2.2) ** (step / 22000.0))
        c = random.randrange(20)
        # Swap two pairs in involution c: (a <-> b) and (d <-> e) => (a <-> d) and (b <-> e)
        a, d = random.sample(range(26), 2)
        b, e = invs[c][a], invs[c][d]
        if d == b:
            continue
        invs[c][a], invs[c][d] = d, a
        invs[c][b], invs[c][e] = e, b
        old_vals = [stream[r * 20 + c] for r in range(25)]
        for r in range(25):
            stream[r * 20 + c] = invs[c][cols_num[c][r]]
        new_sc = sum(get_di(stream[i]*26 + stream[i+1]) for i in range(499))
        if new_sc >= cur_sc or random.random() < math.exp((new_sc - cur_sc) / temp):
            cur_sc = new_sc
            if cur_sc > best_enigma[0]:
                best_enigma = (cur_sc, [p[:] for p in invs])
        else:
            invs[c][a], invs[c][b] = b, a
            invs[c][d], invs[c][e] = e, d
            for r in range(25):
                stream[r * 20 + c] = old_vals[r]

en_sc, en_invs = best_enigma
en_pt = "".join(chr(65 + en_invs[c][cols_num[c][r]]) for r in range(25) for c in range(20))
print(f"\n=== TEST 2: Line-Resetting Enigma / Reciprocal Involutions (elapsed {time.time()-t0:.2f}s) ===")
print(f"Score: {en_sc:.2f} | PT[:160]:\n{en_pt[:160]}")
print(f"Lines 11 & 21 (WHEREVER check): {en_pt[220:240]} | {en_pt[420:440]}")
