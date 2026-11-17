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
TOP_TRI = {
    "THE":3.5,"AND":2.8,"ING":2.6,"ION":2.2,"TIO":2.1,"ENT":2.0,"ATI":1.9,
    "FOR":1.8,"HER":1.8,"TER":1.7,"HAT":1.7,"THA":1.7,"ERE":1.6,"ATE":1.6,
    "HIS":1.6,"CON":1.6,"RES":1.5,"VER":1.5,"ALL":1.5,"ONS":1.5,"NCE":1.4,
    "MEN":1.4,"ITH":1.4,"TED":1.4,"ERS":1.4,"PRO":1.4,"THI":1.4,"WIT":1.4,
    "ARE":1.3,"ESS":1.3,"NOT":1.3,"IVE":1.3,"WAS":1.3,"ECT":1.3,"REA":1.3,
    "COM":1.3,"EVE":1.3,"PER":1.3,"INT":1.3,"EST":1.3,"STA":1.2,"CTI":1.2,
    "ICA":1.2,"IST":1.2,"EAR":1.2,"AIN":1.2,"ONE":1.2,"OUR":1.2,"ITI":1.2,
    "RAT":1.2,"DIS":1.2,"TUR":1.2,"URB":1.1,"RBE":1.1,"BED":1.1,"UND":1.1,
    "NDI":1.1,"IST":1.1,"STU":1.1,"TRA":1.1,"RAD":1.1,"ADI":1.1,"DIN":1.1,
    "LAN":1.1,"CHE":1.1,"HEM":1.1,"OUT":1.1,"WHI":1.1,"HIC":1.1,"ICH":1.1,
    "FRO":1.1,"ROM":1.1,"HAV":1.1,"AVE":1.1,"MOR":1.1,"ORE":1.1,"CAN":1.1,
    "MAN":1.1,"ANY":1.1,"NEW":1.1,"USE":1.1,"WAY":1.1,"DAY":1.1,"MAY":1.1
}

DI_FLAT = [0.0] * 676
for a in range(26):
    for b in range(26):
        p = TOP_DI.get(chr(65 + a) + chr(65 + b), 0.25 * ENG[a] * ENG[b])
        if a == 16 and b != 20:
            p *= 0.01
        DI_FLAT[a * 26 + b] = math.log(p)

TRI_BONUS = [0.0] * 17576
for tri, val in TOP_TRI.items():
    idx = (ord(tri[0]) - 65) * 676 + (ord(tri[1]) - 65) * 26 + (ord(tri[2]) - 65)
    TRI_BONUS[idx] = val

add = operator.add
get_di = DI_FLAT.__getitem__
get_tri = TRI_BONUS.__getitem__

cols_num = [[lines[r][c] for r in range(25)] for c in range(20)]
eng_order = sorted(range(26), key=lambda i: ENG[i], reverse=True)

def full_score(dec_cols, dec_cols26):
    # All 500 wrap-around digrams + trigram bonuses
    sc = 0.0
    for c in range(19):
        sc += sum(map(get_di, map(add, dec_cols26[c], dec_cols[c + 1])))
    sc += sum(map(get_di, map(add, dec_cols26[19][:-1], dec_cols[0][1:])))
    for c in range(18):
        sc += sum(get_tri(dec_cols26[c][r] * 26 + dec_cols26[c + 1][r] + dec_cols[c + 2][r]) for r in range(25))
    return sc

best_overall = (-1e18, None)
for restart in range(6):
    perms = []
    for c in range(20):
        cnt = [cols_num[c].count(i) for i in range(26)]
        ct_order = sorted(range(26), key=lambda i: cnt[i] + random.random() * 0.6, reverse=True)
        p_map = [0] * 26
        for rank, ct_ch in enumerate(ct_order):
            p_map[ct_ch] = eng_order[rank]
        perms.append(p_map)

    dec_cols = [[perms[c][x] for x in cols_num[c]] for c in range(20)]
    dec_cols26 = [[x * 26 for x in col] for col in dec_cols]
    cur_sc = full_score(dec_cols, dec_cols26)

    for step in range(45000):
        temp = 2.5 * ((0.08 / 2.5) ** (step / 45000.0))
        c = random.randrange(20)
        a, b = random.sample(range(26), 2)
        pa, pb = perms[c][a], perms[c][b]
        perms[c][a], perms[c][b] = pb, pa
        old_col, old_col26 = dec_cols[c], dec_cols26[c]
        new_col = [perms[c][x] for x in cols_num[c]]
        dec_cols[c] = new_col
        dec_cols26[c] = [x * 26 for x in new_col]
        new_sc = full_score(dec_cols, dec_cols26)
        if new_sc >= cur_sc or random.random() < math.exp((new_sc - cur_sc) / temp):
            cur_sc = new_sc
            if cur_sc > best_overall[0]:
                best_overall = (cur_sc, [p[:] for p in perms])
        else:
            perms[c][a], perms[c][b] = pa, pb
            dec_cols[c], dec_cols26[c] = old_col, old_col26

sc, best_perms = best_overall
print(f"Elapsed: {time.time() - t0:.2f}s | Combined Score: {sc:.2f}\n")
print("=== Decrypted Plaintext (25 lines x 20 chars) ===")
full_pt = []
for r in range(25):
    ln = "".join(chr(65 + best_perms[c][cols_num[c][r]]) for c in range(20))
    full_pt.append(ln)
    print(f"{r:2d}: {ln}")

print("\nContinuous Plaintext:\n" + "".join(full_pt))
print("\n=== Recovered Column Alphabets (Cipher A-Z -> Plain) ===")
for c in range(20):
    print(f"Col {c:2d}: " + "".join(chr(65 + best_perms[c][i]) for i in range(26)))
