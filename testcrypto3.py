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

assert len(RAW) == 500, f"Expected 500 chars, got {len(RAW)}"

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
DI = [[0.0] * 26 for _ in range(26)]
for a in range(26):
    for b in range(26):
        pair = chr(65 + a) + chr(65 + b)
        p = TOP_DI.get(pair, 0.25 * ENG[a] * ENG[b])
        if a == 16 and b != 20:
            p *= 0.01
        DI[a][b] = math.log(p)

def det4(M):
    def det3(m):
        return (
            m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1])
            - m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0])
            + m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0])
        )
    return sum(((-1)**c) * M[0][c] * det3([[M[r][j] for j in range(4) if j != c] for r in range(1, 4)]) for c in range(4))

nums = [ord(c) - 65 for c in RAW]
blocks = [nums[i:i+4] for i in range(0, len(nums), 4)]
b2 = [[x % 2 for x in b] for b in blocks]
b13 = [[x % 13 for x in b] for b in blocks]

u_rows = [(0, 1, 0, 0), (1, 0, 1, 0), (1, 1, 0, 0), (1, 0, 0, 1)]
K = 25
cands = []

for u in u_rows:
    p2 = [(u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3]) % 2 for b in b2]
    scored = []
    for v in itertools.product(range(13), repeat=4):
        if v == (0, 0, 0, 0):
            continue
        score = 0.0
        for k, b in enumerate(b13):
            p13 = (v[0]*b[0] + v[1]*b[1] + v[2]*b[2] + v[3]*b[3]) % 13
            p = (13 * p2[k] + 14 * p13) % 26
            score += LOG_ENG[p]
        scored.append((score, v))
    scored.sort(reverse=True)
    top_k = []
    for _, v in scored[:K]:
        row = tuple((13 * u[j] + 14 * v[j]) % 26 for j in range(4))
        col = tuple(sum(row[j]*b[j] for j in range(4)) % 26 for b in blocks)
        top_k.append((v, row, col))
    cands.append(top_k)

within = {}
across = {}
for i in range(4):
    for j in range(4):
        if i == j:
            continue
        for a in range(K):
            va, _, ca = cands[i][a]
            for b in range(K):
                vb, _, cb = cands[j][b]
                if va == vb:
                    continue
                within[(i, a, j, b)] = sum(DI[ca[k]][cb[k]] for k in range(125))
                across[(i, a, j, b)] = sum(DI[ca[k]][cb[k+1]] for k in range(124))

results = []
for perm in itertools.permutations(range(4)):
    p0, p1, p2, p3 = perm
    for a0 in range(K):
        v0 = cands[p0][a0][0]
        best_to_2 = {}
        for a1 in range(K):
            v1 = cands[p1][a1][0]
            if v1 == v0:
                continue
            s01 = within[(p0, a0, p1, a1)]
            for a2 in range(K):
                v2 = cands[p2][a2][0]
                if v2 == v0 or v2 == v1:
                    continue
                sc = s01 + within[(p1, a1, p2, a2)]
                if a2 not in best_to_2 or sc > best_to_2[a2][0]:
                    best_to_2[a2] = (sc, a1)
        for a2, (sc012, a1) in best_to_2.items():
            v1 = cands[p1][a1][0]
            v2 = cands[p2][a2][0]
            for a3 in range(K):
                v3 = cands[p3][a3][0]
                if v3 == v0 or v3 == v1 or v3 == v2:
                    continue
                D = tuple(cands[perm[r]][(a0, a1, a2, a3)[r]][1] for r in range(4))
                if math.gcd(det4(D) % 26, 26) != 1:
                    continue
                total = sc012 + within[(p2, a2, p3, a3)] + across[(p3, a3, p0, a0)]
                results.append((total, perm, (a0, a1, a2, a3)))

results.sort(reverse=True)
for rank, (score, perm, idxs) in enumerate(results[:3], 1):
    D = tuple(cands[perm[r]][idxs[r]][1] for r in range(4))
    cols = [cands[perm[r]][idxs[r]][2] for r in range(4)]
    pt = "".join(chr(65 + cols[r][k]) for k in range(125) for r in range(4))
    print(f"=== Rank {rank} (digram score: {score:.2f}) ===")
    print("Decryption matrix D (mod 26):", D)
    print("Plaintext:\n", pt, "\n")
