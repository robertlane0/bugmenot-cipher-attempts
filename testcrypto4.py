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

# Build 26x26 and marginalized 13x13 digram log-probability tables
P26 = [[0.0] * 26 for _ in range(26)]
tot = 0.0
for a in range(26):
    for b in range(26):
        pair = chr(65 + a) + chr(65 + b)
        p = TOP_DI.get(pair, 0.25 * ENG[a] * ENG[b])
        if a == 16 and b != 20:
            p *= 0.01
        P26[a][b] = p
        tot += p

DI26 = [[math.log(P26[a][b] / tot) for b in range(26)] for a in range(26)]
DI13 = [[0.0] * 13 for _ in range(13)]
for r1 in range(13):
    for r2 in range(13):
        p13 = (P26[r1][r2] + P26[r1 + 13][r2] + P26[r1][r2 + 13] + P26[r1 + 13][r2 + 13]) / tot
        DI13[r1][r2] = math.log(p13)

LOG_ENG13 = [math.log(ENG[r] + ENG[r + 13]) for r in range(13)]

def rank_mod(rows, mod):
    M = [list(r) for r in rows]
    r = 0
    for c in range(4):
        piv = next((i for i in range(r, len(M)) if M[i][c] % mod != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], -1, mod)
        M[r] = [(x * inv) % mod for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % mod for j in range(4)]
        r += 1
    return r

nums = [ord(c) - 65 for c in RAW]
blocks = [nums[i:i+4] for i in range(0, len(nums), 4)]
b2 = [[x % 2 for x in b] for b in blocks]
b13 = [[x % 13 for x in b] for b in blocks]

# 1. Score all 28,560 nonzero mod-13 vectors x 13 shifts
scored13 = []
for v in itertools.product(range(13), repeat=4):
    if v == (0, 0, 0, 0):
        continue
    raw_col = [(v[0]*b[0] + v[1]*b[1] + v[2]*b[2] + v[3]*b[3]) % 13 for b in b13]
    cnt = [0] * 13
    for x in raw_col:
        cnt[x] += 1
    for s in range(13):
        sc = sum(cnt[r] * LOG_ENG13[(r + s) % 13] for r in range(13))
        scored13.append((sc, v, s))

scored13.sort(reverse=True)
M = 220
cands13 = []
for _, v, s in scored13[:M]:
    col = tuple(((v[0]*b[0] + v[1]*b[1] + v[2]*b[2] + v[3]*b[3] + s) % 13) for b in b13)
    cands13.append((v, s, col))

# 2. Precompute 13x13 within-block and across-block digram scores
within13 = [[0.0] * M for _ in range(M)]
across13 = [[0.0] * M for _ in range(M)]
for i in range(M):
    ci = cands13[i][2]
    for j in range(M):
        if i == j:
            continue
        cj = cands13[j][2]
        within13[i][j] = sum(DI13[ci[k]][cj[k]] for k in range(125))
        across13[i][j] = sum(DI13[ci[k]][cj[k + 1]] for k in range(124))

# 3. Beam search over 4 linearly independent mod-13 rows
BEAM = 400
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
    nxt.sort(reverse=True)
    states = nxt[:BEAM]

# 4. Resolve mod-2 rows & shifts via exact 26x26 digram DP for top mod-13 solutions
u_opts = [(u, s2) for u in itertools.product(range(2), repeat=4) if u != (0, 0, 0, 0) for s2 in range(2)]
final_results = []

for _, path in states[:5]:
    # Build 30 mod-2 candidates per row combined via CRT with the recovered mod-13 column
    row_cands = []
    for pos in range(4):
        v, s13, col13 = cands13[path[pos]]
        opts = []
        for u, s2 in u_opts:
            col26 = tuple((13 * ((u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3] + s2) % 2) + 14 * col13[k]) % 26 for k, b in enumerate(b2))
            row26 = tuple((13 * u[j] + 14 * v[j]) % 26 for j in range(4))
            d26 = (13 * s2 + 14 * s13) % 26
            opts.append((u, row26, d26, col26))
        row_cands.append(opts)

    for a0 in range(30):
        u0, r0, d0, c0 = row_cands[0][a0]
        best2 = {}
        for a1 in range(30):
            u1, r1, d1, c1 = row_cands[1][a1]
            if u1 == u0:
                continue
            s01 = sum(DI26[c0[k]][c1[k]] for k in range(125))
            for a2 in range(30):
                u2, r2, d2, c2 = row_cands[2][a2]
                if rank_mod([u0, u1, u2], 2) < 3:
                    continue
                sc = s01 + sum(DI26[c1[k]][c2[k]] for k in range(125))
                if a2 not in best2 or sc > best2[a2][0]:
                    best2[a2] = (sc, a1)
        for a2, (sc012, a1) in best2.items():
            u1, r1, d1, c1 = row_cands[1][a1]
            u2, r2, d2, c2 = row_cands[2][a2]
            for a3 in range(30):
                u3, r3, d3, c3 = row_cands[3][a3]
                if rank_mod([u0, u1, u2, u3], 2) < 4:
                    continue
                total = sc012 + sum(DI26[c2[k]][c3[k]] for k in range(125)) + sum(DI26[c3[k]][c0[k + 1]] for k in range(124))
                D = (r0, r1, r2, r3)
                d_vec = (d0, d1, d2, d3)
                cols = (c0, c1, c2, c3)
                final_results.append((total, D, d_vec, cols))

final_results.sort(reverse=True)
for rank, (score, D, d_vec, cols) in enumerate(final_results[:3], 1):
    pt = "".join(chr(65 + cols[r][k]) for k in range(125) for r in range(4))
    print(f"=== Rank {rank} (26x26 digram score: {score:.2f}) ===")
    print("Decryption matrix D (mod 26):", D)
    print("Additive shift d (mod 26):   ", d_vec)
    print("Plaintext:\n", pt, "\n")
