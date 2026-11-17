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
LOG_ENG = [math.log(p) for p in ENG]

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
DI_MAT = [[math.log(TOP_DI.get(chr(65+a)+chr(65+b), 0.25*ENG[a]*ENG[b]) * (0.01 if a==16 and b!=20 else 1.0))
           for b in range(26)] for a in range(26)]
DI_FLAT = [DI_MAT[a][b] for a in range(26) for b in range(26)]
get_di = DI_FLAT.__getitem__

CORPUS = (
    "THE EARTH IS SURROUNDED BY AN ATMOSPHERE OF GASES THAT PROTECTS ALL LIVING THINGS "
    "FROM THE HARSH RADIATION OF THE SUN AND HELPS MAINTAIN A STABLE TEMPERATURE ON THE SURFACE "
    "WHEREVER WE GO BENEATH THE GROUND INTO DEEP CAVES AND CAVERNS WE FIND THAT THE TEMPERATURE "
    "REMAINS ALMOST COMPLETELY CONSTANT THROUGHOUT THE ENTIRE YEAR REGARDLESS OF WHETHER IT IS "
    "SUMMER OR WINTER OUTSIDE ON THE SURFACE OF THE EARTH THE WEATHER CHANGES FROM DAY TO DAY "
    "AND FROM SEASON TO SEASON WITH GREAT HEAT IN SUMMER AND EXTREME COLD IN WINTER HOWEVER "
    "UNDERGROUND AT A DEPTH OF ONLY A FEW METERS THESE CHANGES DISAPPEAR AND THE AIR REMAINS "
    "COOL AND STEADY UNDISTURBED BY WIND RAIN OR SUNLIGHT BECAUSE ROCK AND SOIL CONDUCT HEAT "
    "VERY SLOWLY THE INTERIOR OF A DEEP CAVERN REFLECTS THE AVERAGE ANNUAL TEMPERATURE OF THE "
    "REGION IN WHICH IT IS LOCATED THIS NATURAL CONDITION HAS BEEN USED BY HUMANS AND ANIMALS "
    "FOR THOUSANDS OF YEARS FOR SHELTER STORAGE AND PROTECTION AGAINST EXTREME WEATHER CONDITIONS "
    "IN ADDITION TO CONSTANT TEMPERATURE THE AIR INSIDE MANY CAVES HAS HIGH HUMIDITY AND VERY "
    "LITTLE AIR MOVEMENT CREATING A UNIQUE ENVIRONMENT WHERE SPECIALIZED CREATURES CAN SURVIVE "
    "WITHOUT LIGHT OR DIRECT ENERGY FROM THE SUN SCIENTIFIC OBSERVATION OF THESE UNDERGROUND "
    "CHAMBERS SHOWS HOW GEOLOGICAL FORMATIONS DEVELOP OVER MILLIONS OF YEARS THROUGH THE SLOW "
    "ACTION OF WATER DISSOLVING LIMESTONE AND OTHER SOLUBLE ROCKS BENEATH THE SURFACE "
    "OBSERVATION PROTECTION CONDITION CONDITIONS FORMATION FORMATIONS LOCATION VARIATION "
    "TEMPERATURE CONSTANT REMAINS UNDISTURBED COMPLETELY DIRECTLY NATURALLY GENERALLY "
    "THEREFORE MOREOVER FURTHERMORE SUBTERRANEAN GEOTHERMAL PRESSURE MOISTURE"
).replace(" ", "")

Q4_BONUS = {}
for i in range(len(CORPUS) - 3):
    idx = ((ord(CORPUS[i])-65)*17576 + (ord(CORPUS[i+1])-65)*676 + (ord(CORPUS[i+2])-65)*26 + (ord(CORPUS[i+3])-65))
    Q4_BONUS[idx] = min(2.6, Q4_BONUS.get(idx, 1.0) + 0.35)
get_q4 = Q4_BONUS.get

def max_assign_26(w):
    n = 26
    u, v, p, way = [0.0]*(n+1), [0.0]*(n+1), [0]*(n+1), [0]*(n+1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [1e18] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = 1e18
            j1 = 0
            row_w = w[i0 - 1]
            for j in range(1, n + 1):
                if not used[j]:
                    cur = -row_w[j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    ans = [0] * n
    for j in range(1, n + 1):
        ans[p[j] - 1] = j - 1
    return ans

def hungarian_polish(perms, locked):
    for _ in range(4):
        changed = False
        order = list(range(20))
        random.shuffle(order)
        for c in order:
            W = [[LOG_ENG[pt] * 0.25 for pt in range(26)] for _ in range(26)]
            for r in range(25):
                ct_ch = cols_num[c][r]
                idx = r * 20 + c
                if idx > 0:
                    prev_c = (c - 1) % 20
                    prev_r = (idx - 1) // 20
                    prev_pt = perms[prev_c][cols_num[prev_c][prev_r]]
                    row_di = DI_MAT[prev_pt]
                    w_row = W[ct_ch]
                    for pt in range(26):
                        w_row[pt] += row_di[pt]
                if idx < 499:
                    next_c = (c + 1) % 20
                    next_r = (idx + 1) // 20
                    next_pt = perms[next_c][cols_num[next_c][next_r]]
                    w_row = W[ct_ch]
                    for pt in range(26):
                        w_row[pt] += DI_MAT[pt][next_pt]
            for ct_fix, pt_fix in locked[c].items():
                for pt in range(26):
                    W[ct_fix][pt] = 1e6 if pt == pt_fix else -1e6
            new_p = max_assign_26(W)
            if new_p != perms[c]:
                perms[c] = new_p
                changed = True
        if not changed:
            break

# Lock ONLY the rock-solid anchors:
# 1) Line 11 & 21 cols 0..7: UNIDWMQB -> WHEREVER
# 2) Line 9 cols 15..19 + Line 10 cols 0..6: MPLXV + MEDBQHP -> TEMPERATURES
CRIBS = [
    (11, 0, "WHEREVER"),
    (9, 15, "TEMPE"),
    (10, 0, "RATURES"),
]
locked = [dict() for _ in range(20)]
for r, start_c, word in CRIBS:
    for offset, ch in enumerate(word):
        c = start_c + offset
        locked[c][lines[r][c]] = ord(ch) - 65

eng_order = sorted(range(26), key=lambda i: ENG[i], reverse=True)

def score_fast(s):
    sc = 0.0
    for i in range(499):
        sc += get_di(s[i] * 26 + s[i + 1])
    for i in range(497):
        v = get_q4(s[i] * 17576 + s[i + 1] * 676 + s[i + 2] * 26 + s[i + 3])
        if v:
            sc += v
    return sc

best_overall = (-1e18, None)
for restart in range(10):
    perms = []
    for c in range(20):
        cnt = [cols_num[c].count(i) for i in range(26)]
        ct_order = sorted(range(26), key=lambda i: cnt[i] + random.random() * 0.9, reverse=True)
        p_map = [None] * 26
        used_pt = set(locked[c].values())
        for ct_fix, pt_fix in locked[c].items():
            p_map[ct_fix] = pt_fix
        rem_pt = [pt for pt in eng_order if pt not in used_pt]
        rem_ct = [ct for ct in ct_order if ct not in locked[c]]
        for ct_ch, pt_ch in zip(rem_ct, rem_pt):
            p_map[ct_ch] = pt_ch
        perms.append(p_map)

    # Start with exact Hungarian assignment, then run 4-gram SA + Hungarian polish
    hungarian_polish(perms, locked)
    stream = [perms[c][cols_num[c][r]] for r in range(25) for c in range(20)]
    cur_sc = score_fast(stream)
    if cur_sc > best_overall[0]:
        best_overall = (cur_sc, [p[:] for p in perms])

    for step in range(22000):
        temp = 2.0 * ((0.035 / 2.0) ** (step / 22000.0))
        c = random.randrange(20)
        a, b = random.sample(range(26), 2)
        if a in locked[c] or b in locked[c]:
            continue
        pa, pb = perms[c][a], perms[c][b]
        perms[c][a], perms[c][b] = pb, pa
        old_vals = [stream[r * 20 + c] for r in range(25)]
        for r in range(25):
            stream[r * 20 + c] = perms[c][cols_num[c][r]]
        new_sc = score_fast(stream)
        if new_sc >= cur_sc or random.random() < math.exp((new_sc - cur_sc) / temp):
            cur_sc = new_sc
            if cur_sc > best_overall[0]:
                best_overall = (cur_sc, [p[:] for p in perms])
        else:
            perms[c][a], perms[c][b] = pa, pb
            for r in range(25):
                stream[r * 20 + c] = old_vals[r]

sc, best_perms = best_overall
print(f"Elapsed: {time.time() - t0:.2f}s | Combined Score: {sc:.2f}\n")
full_pt = []
for r in range(25):
    ln = "".join(chr(65 + best_perms[c][cols_num[c][r]]) for c in range(20))
    full_pt.append(ln)
    print(f"{r:2d}: {ln}")

print("\nContinuous Plaintext:\n" + "".join(full_pt))
