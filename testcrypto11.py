import itertools, math, operator, time

t0 = time.time()

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
blocks = [nums[i:i+4] for i in range(0, 500, 4)]
b2 = [[x % 2 for x in b] for b in blocks]
b13 = [[x % 13 for x in b] for b in blocks]

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

DI_FLAT = [0.0] * 676
for a in range(26):
    for b in range(26):
        p = TOP_DI.get(chr(65 + a) + chr(65 + b), 0.25 * ENG[a] * ENG[b])
        if a == 16 and b != 20:
            p *= 0.01
        DI_FLAT[a * 26 + b] = math.log(p)

def rank_mod13(rows):
    M = [list(r) for r in rows]
    r = 0
    for c in range(4):
        piv = next((i for i in range(r, len(M)) if M[i][c] % 13 != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], -1, 13)
        M[r] = [(x * inv) % 13 for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % 13 for j in range(4)]
        r += 1
    return r

def inv_mod(mat, mod):
    n = 4
    M = [[mat[r][c] % mod for c in range(n)] + [1 if r == c else 0 for c in range(n)] for r in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] % mod != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        inv = pow(M[c][c], -1, mod)
        M[c] = [(x * inv) % mod for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [(M[r][j] - f * M[c][j]) % mod for j in range(2 * n)]
    return [row[n:] for row in M]

def invert_26(D):
    K2 = inv_mod(D, 2)
    K13 = inv_mod(D, 13)
    if K2 is None or K13 is None:
        return None
    return tuple(tuple((13 * K2[r][c] + 14 * K13[r][c]) % 26 for c in range(4)) for r in range(4))

u_rows = [(0, 1, 0, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1)]
p2_cols = [[(u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3]) % 2 for b in b2] for u in u_rows]

K = 800
heaps = [[] for _ in range(4)]
b0_13, b1_13, b2_13, b3_13 = [b[0] for b in b13], [b[1] for b in b13], [b[2] for b in b13], [b[3] for b in b13]

for v0 in range(13):
    s0 = [v0 * x for x in b0_13]
    for v1 in range(13):
        s01 = [s0[k] + v1 * b1_13[k] for k in range(125)]
        for v2 in range(13):
            s012 = [s01[k] + v2 * b2_13[k] for k in range(125)]
            for v3 in range(13):
                if v0 == 0 and v1 == 0 and v2 == 0 and v3 == 0:
                    continue
                p13_col = [(s012[k] + v3 * b3_13[k]) % 13 for k in range(125)]
                v = (v0, v1, v2, v3)
                for ui in range(4):
                    p2 = p2_cols[ui]
                    sc = sum(LOG_ENG[(13 * p2[k] + 14 * p13_col[k]) % 26] for k in range(125))
                    heaps[ui].append((sc, v, p13_col))

cands = []
for ui, u in enumerate(u_rows):
    heaps[ui].sort(reverse=True)
    p2 = p2_cols[ui]
    top_u = []
    for _, v, p13_col in heaps[ui][:K]:
        row = tuple((13 * u[j] + 14 * v[j]) % 26 for j in range(4))
        col = tuple((13 * p2[k] + 14 * p13_col[k]) % 26 for k in range(125))
        col26 = tuple(x * 26 for x in col)
        top_u.append((v, row, col, col26))
    cands.append(top_u)

add = operator.add
get_di = DI_FLAT.__getitem__

# Two-stage cascade filter across K=800 candidates per row
within_in = {}
within_out = {}
across_out = {}

for i in range(4):
    for j in range(4):
        if i == j:
            continue
        w_out = [[] for _ in range(K)]
        w_in = [[] for _ in range(K)]
        a_out = [[] for _ in range(K)]
        for a in range(K):
            va, _, _, ca26 = cands[i][a]
            ca26_8 = ca26[:8]
            ca26_28 = ca26[:28]
            ca26_wrap = ca26[:-1]
            for b in range(K):
                vb, _, cb, _ = cands[j][b]
                if va == vb:
                    continue
                # Within-block cascade (8 -> 28 -> 125)
                if sum(map(get_di, map(add, ca26_8, cb[:8]))) >= -52.0:
                    if sum(map(get_di, map(add, ca26_28, cb[:28]))) >= -176.0:
                        sc_w = sum(map(get_di, map(add, ca26, cb)))
                        w_out[a].append((sc_w, b))
                        w_in[b].append((sc_w, a))
                # Across-block cascade (8 -> 28 -> 124)
                if sum(map(get_di, map(add, ca26_8, cb[1:9]))) >= -52.0:
                    if sum(map(get_di, map(add, ca26_28, cb[1:29]))) >= -176.0:
                        sc_a = sum(map(get_di, map(add, ca26_wrap, cb[1:])))
                        a_out[a].append((sc_a, b))
        for idx in range(K):
            w_out[idx].sort(reverse=True); del w_out[idx][40:]
            w_in[idx].sort(reverse=True);  del w_in[idx][40:]
            a_out[idx].sort(reverse=True); del a_out[idx][40:]
        within_out[(i, j)] = w_out
        within_in[(i, j)] = w_in
        across_out[(i, j)] = a_out

# Meet-in-the-middle DP across all 24 permutations
best = (-1e18, None, None, None)
for perm in itertools.permutations(range(4)):
    p0, p1, p2, p3 = perm
    in_01 = within_in[(p0, p1)]
    out_12 = within_out[(p1, p2)]
    best_012 = {}
    for a1 in range(K):
        if not in_01[a1] or not out_12[a1]:
            continue
        v1 = cands[p1][a1][0]
        for s01, a0 in in_01[a1]:
            v0 = cands[p0][a0][0]
            for s12, a2 in out_12[a1]:
                v2 = cands[p2][a2][0]
                if v2 == v0 or v2 == v1:
                    continue
                sc = s01 + s12
                key = (a0, a2)
                if key not in best_012 or sc > best_012[key][0]:
                    best_012[key] = (sc, a1)

    in_23 = within_in[(p2, p3)]
    out_30 = across_out[(p3, p0)]
    for a3 in range(K):
        if not in_23[a3] or not out_30[a3]:
            continue
        v3 = cands[p3][a3][0]
        for s23, a2 in in_23[a3]:
            v2 = cands[p2][a2][0]
            for s30, a0 in out_30[a3]:
                prev = best_012.get((a0, a2))
                if prev is None:
                    continue
                sc012, a1 = prev
                total = sc012 + s23 + s30
                if total <= best[0]:
                    continue
                v0, v1 = cands[p0][a0][0], cands[p1][a1][0]
                if rank_mod13([v0, v1, v2, v3]) < 4:
                    continue
                D = (cands[p0][a0][1], cands[p1][a1][1], cands[p2][a2][1], cands[p3][a3][1])
                K_mat = invert_26(D)
                if K_mat is not None:
                    cols = (cands[p0][a0][2], cands[p1][a1][2], cands[p2][a2][2], cands[p3][a3][2])
                    best = (total, D, K_mat, cols)

score, D, K_mat, cols = best
print(f"Elapsed: {time.time() - t0:.2f}s | Digram score: {score:.2f}")
if D is None:
    print("No valid cycle found.")
else:
    pt = "".join(chr(65 + cols[r][k]) for k in range(125) for r in range(4))
    print("Decryption matrix D (mod 26):", D)
    print("Encryption key K    (mod 26):", K_mat)
    print("Plaintext:\n", pt)
