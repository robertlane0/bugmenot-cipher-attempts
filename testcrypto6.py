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

assert len(RAW) == 500
nums = [ord(c) - 65 for c in RAW]

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

P26 = [[0.0] * 26 for _ in range(26)]
tot = 0.0
for a in range(26):
    for b in range(26):
        p = TOP_DI.get(chr(65+a)+chr(65+b), 0.25*ENG[a]*ENG[b])
        if a == 16 and b != 20:
            p *= 0.01
        P26[a][b] = p
        tot += p

DI26 = [[math.log(P26[a][b] / tot) for b in range(26)] for a in range(26)]
DI13 = [[math.log((P26[r1][r2] + P26[r1+13][r2] + P26[r1][r2+13] + P26[r1+13][r2+13]) / tot) for r2 in range(13)] for r1 in range(13)]
LOG_ENG13 = [math.log(ENG[r] + ENG[r + 13]) for r in range(13)]

def di_score(seq):
    return sum(DI26[seq[i]][seq[i+1]] for i in range(len(seq)-1))

# 1. Autokey (Plaintext & Ciphertext Autokey, Primer lengths 1..25)
best_ak = (-1e18, "", "")
for m in range(1, 26):
    for mode in ("Vig-PT", "Beau-PT", "Var-PT"):
        pt = [0] * 500
        for r in range(m):
            best_p0, best_sc = 0, -1e18
            for p0 in range(26):
                cur = p0
                sc = LOG_ENG[cur]
                for i in range(r + m, 500, m):
                    if mode == "Vig-PT":
                        cur = (nums[i] - cur) % 26
                    elif mode == "Beau-PT":
                        cur = (cur - nums[i]) % 26
                    else:
                        cur = (nums[i] + cur) % 26
                    sc += LOG_ENG[cur]
                if sc > best_sc:
                    best_sc, best_p0 = sc, p0
            cur = best_p0
            pt[r] = cur
            for i in range(r + m, 500, m):
                cur = (nums[i] - cur) % 26 if mode == "Vig-PT" else ((cur - nums[i]) % 26 if mode == "Beau-PT" else (nums[i] + cur) % 26)
                pt[i] = cur
        sc = di_score(pt)
        if sc > best_ak[0]:
            best_ak = (sc, f"{mode} (primer len {m})", "".join(chr(65+x) for x in pt))
    for mode in ("Vig-CT", "Beau-CT", "Var-CT"):
        pt = [(nums[i] - nums[i-m]) % 26 if mode == "Vig-CT" else ((nums[i-m] - nums[i]) % 26 if mode == "Beau-CT" else (nums[i] + nums[i-m]) % 26) for i in range(m, 500)]
        sc = di_score(pt)
        if sc > best_ak[0]:
            best_ak = (sc, f"{mode} (primer len {m})", "?"*m + "".join(chr(65+x) for x in pt))

print(f"=== Best Autokey ===\n{best_ak[1]} | Score: {best_ak[0]:.1f}\n{best_ak[2]}\n")

# 2. Progressive Key Vigenere / Beaufort / Variant
best_pr = (-1e18, "", "")
for L in (1, 2, 4, 5, 10, 20):
    for B in (1, 4, 20):
        for step in range(1, 26):
            adj = [(nums[i] - step * (i // B)) % 26 for i in range(500)]
            pt = [0] * 500
            for r in range(L):
                col = adj[r::L]
                best_k = max(range(26), key=lambda k: sum(LOG_ENG[(c - k) % 26] for c in col))
                for idx, c in enumerate(col):
                    pt[r + idx*L] = (c - best_k) % 26
            sc = di_score(pt)
            if sc > best_pr[0]:
                best_pr = (sc, f"Prog-Vig L={L}, B={B}, step={step}", "".join(chr(65+x) for x in pt))

print(f"=== Best Progressive Key ===\n{best_pr[1]} | Score: {best_pr[0]:.1f}\n{best_pr[2]}\n")

# 3. Mod-2 Parity Check + Deep 4x4 Hill Search (M = 900, unshifted d=0)
blocks = [nums[i:i+4] for i in range(0, 500, 4)]
b2 = [[x % 2 for x in b] for b in blocks]
b13 = [[x % 13 for x in b] for b in blocks]

print("=== Mod-2 Even Parity Rates (15 vectors) ===")
for u in itertools.product(range(2), repeat=4):
    if u != (0, 0, 0, 0):
        ev = sum(1 for b in b2 if (u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3]) % 2 == 0)
        if ev >= 67 or ev <= 58:
            print(f"u={u}: {ev}/125 even ({ev/1.25:.1f}%)")

def rank_mod(rows, mod):
    M_mat = [list(r) for r in rows]
    r = 0
    for c in range(4):
        piv = next((i for i in range(r, len(M_mat)) if M_mat[i][c] % mod != 0), None)
        if piv is None:
            continue
        M_mat[r], M_mat[piv] = M_mat[piv], M_mat[r]
        inv = pow(M_mat[r][c], -1, mod)
        M_mat[r] = [(x * inv) % mod for x in M_mat[r]]
        for i in range(len(M_mat)):
            if i != r and M_mat[i][c] != 0:
                f = M_mat[i][c]
                M_mat[i] = [(M_mat[i][j] - f * M_mat[r][j]) % mod for j in range(4)]
        r += 1
    return r

scored13 = []
for v in itertools.product(range(13), repeat=4):
    if v == (0, 0, 0, 0):
        continue
    col = tuple((v[0]*b[0] + v[1]*b[1] + v[2]*b[2] + v[3]*b[3]) % 13 for b in b13)
    sc = sum(LOG_ENG13[x] for x in col)
    scored13.append((sc, v, col))

scored13.sort(reverse=True)
M = 900
cands13 = [(v, col) for _, v, col in scored13[:M]]

within13 = [[0.0] * M for _ in range(M)]
across13 = [[0.0] * M for _ in range(M)]
for i in range(M):
    ci = cands13[i][1]
    for j in range(M):
        if i != j:
            cj = cands13[j][1]
            within13[i][j] = sum(DI13[ci[k]][cj[k]] for k in range(125))
            across13[i][j] = sum(DI13[ci[k]][cj[k + 1]] for k in range(124))

BEAM = 600
states = [(0.0, (i,)) for i in range(M)]
for step in range(1, 4):
    nxt = []
    for sc, path in states:
        prev = path[-1]
        prev_vecs = [cands13[idx][0] for idx in path]
        for j in range(M):
            vj = cands13[j][0]
            if rank_mod(prev_vecs + [vj], 13) <= step:
                continue
            add = within13[prev][j] + (across13[j][path[0]] if step == 3 else 0.0)
            nxt.append((sc + add, path + (j,)))
    nxt.sort
