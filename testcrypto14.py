import itertools, math, operator, random, time

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

P26 = [[0.0] * 26 for _ in range(26)]
tot = 0.0
for a in range(26):
    for b in range(26):
        p = TOP_DI.get(chr(65 + a) + chr(65 + b), 0.25 * ENG[a] * ENG[b])
        if a == 16 and b != 20:
            p *= 0.01
        P26[a][b] = p
        tot += p

DI_FLAT = [math.log(P26[a][b] / tot) for a in range(26) for b in range(26)]

# 1. Exact 4-bit parity quadgram table
P_EVEN = sum(ENG[0::2])
P_ODD = 1.0 - P_EVEN
P_PAR2 = [[0.0, 0.0], [0.0, 0.0]]
for a in range(26):
    for b in range(26):
        P_PAR2[a % 2][b % 2] += P26[a][b] / tot

LOG_PAR4 = [0.0] * 16
for mask in range(16):
    b0, b1, b2_bit, b3 = (mask >> 3) & 1, (mask >> 2) & 1, (mask >> 1) & 1, mask & 1
    p0 = P_EVEN if b0 == 0 else P_ODD
    p1 = P_EVEN if b1 == 0 else P_ODD
    p2 = P_EVEN if b2_bit == 0 else P_ODD
    prob = p0 * (P_PAR2[b0][b1] / p0) * (P_PAR2[b1][b2_bit] / p1) * (P_PAR2[b2_bit][b3] / p2)
    LOG_PAR4[mask] = math.log(prob)

nib_counts = [0] * 16
for b in b2:
    nib_counts[(b[0] << 3) | (b[1] << 2) | (b[2] << 1) | b[3]] += 1

u_all = [u for u in itertools.product(range(2), repeat=4) if u != (0, 0, 0, 0)]
row_nib = []
for u in u_all:
    m = 0
    for x in range(16):
        bit = ((u[0] & (x >> 3)) ^ (u[1] & (x >> 2)) ^ (u[2] & (x >> 1)) ^ (u[3] & x)) & 1
        m |= (bit << x)
    row_nib.append(m)

linear_hits = []
shifted_hits = []
for i0 in range(15):
    m0 = row_nib[i0]
    for i1 in range(15):
        if i1 == i0:
            continue
        m1 = row_nib[i1]
        for i2 in range(15):
            if i2 == i0 or i2 == i1:
                continue
            u2 = u_all[i2]
            if u2 == tuple(u_all[i0][k] ^ u_all[i1][k] for k in range(4)):
                continue
            m2 = row_nib[i2]
            span = {
                (0,0,0,0), u_all[i0], u_all[i1], u2,
                tuple(u_all[i0][k]^u_all[i1][k] for k in range(4)),
                tuple(u_all[i0][k]^u2[k] for k in range(4)),
                tuple(u_all[i1][k]^u2[k] for k in range(4)),
                tuple(u_all[i0][k]^u_all[i1][k]^u2[k] for k in range(4)),
            }
            for i3 in range(15):
                u3 = u_all[i3]
                if u3 in span:
                    continue
                m3 = row_nib[i3]
                base_map = [
                    (((m0 >> x) & 1) << 3) | (((m1 >> x) & 1) << 2) | (((m2 >> x) & 1) << 1) | ((m3 >> x) & 1)
                    for x in range(16)
                ]
                sc0 = sum(nib_counts[x] * LOG_PAR4[base_map[x]] for x in range(16))
                linear_hits.append((sc0, (u_all[i0], u_all[i1], u2, u3), 0))
                for d2 in range(1, 16):
                    sc = sum(nib_counts[x] * LOG_PAR4[base_map[x] ^ d2] for x in range(16))
                    if sc > -342.0:
                        shifted_hits.append((sc, (u_all[i0], u_all[i1], u2, u3), d2))

linear_hits.sort(reverse=True)
shifted_hits.sort(reverse=True)
print(f"Mod-2 quadgram scan done in {time.time()-t0:.2f}s:")
print("Top 3 Linear (d2=0):")
for sc, U, d2 in linear_hits[:3]:
    print(f"  Score {sc:.2f} | U={U}")
print("Top 3 Shifted (d2!=0):")
for sc, U, d2 in shifted_hits[:3]:
    print(f"  Score {sc:.2f} | U={U} | d2={tuple((d2>>(3-r))&1 for r in range(4))}")

# 2. Fast C-speed CRT & Digram SA + Exhaustive Polish
add = operator.add
get_di = DI_FLAT.__getitem__
CRT26 = tuple(x % 26 for x in range(182))
CRT26_X26 = tuple((x % 26) * 26 for x in range(182))
get_crt = CRT26.__getitem__
get_crt26 = CRT26_X26.__getitem__

b0_13, b1_13, b2_13, b3_13 = [b[0] for b in b13], [b[1] for b in b13], [b[2] for b in b13], [b[3] for b in b13]
all_v = []
for v0 in range(13):
    s0 = [v0 * x for x in b0_13]
    for v1 in range(13):
        s01 = [s0[k] + v1 * b1_13[k] for k in range(125)]
        for v2 in range(13):
            s012 = [s01[k] + v2 * b2_13[k] for k in range(125)]
            for v3 in range(13):
                if v0 or v1 or v2 or v3:
                    p13_14 = tuple(((s012[k] + v3 * b3_13[k]) % 13) * 14 for k in range(125))
                    all_v.append(((v0, v1, v2, v3), p13_14))

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

def pair_w(cL26, cR): return sum(map(get_di, map(add, cL26, cR)))
def pair_a(cL26, cR): return sum(map(get_di, map(add, cL26[:-1], cR[1:])))

def solve_for_U(U, d2):
    d2_bits = [(d2 >> (3 - r)) & 1 for r in range(4)]
    p2_13 = [
        tuple(((U[r][0]*b[0] + U[r][1]*b[1] + U[r][2]*b[2] + U[r][3]*b[3] + d2_bits[r]) % 2) * 13 for b in b2)
        for r in range(4)
    ]
    # Build top-1500 pool per row (s13=0 for linear, all s13 for shifted)
    s13_range = (0,) if d2 == 0 else range(13)
    pools = []
    for r in range(4):
        base = p2_13[r]
        scored = []
        for v, p13_14 in all_v:
            for s13 in s13_range:
                shift = (s13 * 14) % 182
                c = tuple(get_crt((x + y + shift) % 182) for x, y in zip(base, p13_14)) if s13 else tuple(map(get_crt, map(add, base, p13_14)))
                sc = sum(map(LOG_ENG.__getitem__, c))
                scored.append((sc, v, s13, c))
        scored.sort(reverse=True)
        pools.append([(v, s13, c, tuple(x * 26 for x in c)) for _, v, s13, c in scored[:1500]])

    best_u = (-1e18, None)
    for _ in range(5):
        cur = [pools[r][random.randrange(250)] for r in range(4)]
        cur_sc = pair_w(cur[0][3], cur[1][2]) + pair_w(cur[1][3], cur[2][2]) + pair_w(cur[2][3], cur[3][2]) + pair_a(cur[3][3], cur[0][2])
        for step in range(6000):
            temp = 2.5 * ((0.15 / 2.5) ** (step / 6000.0))
            r = random.randrange(4)
            cand = pools[r][random.randrange(1500)]
            if any(cand[0] == cur[k][0] for k in range(4) if k != r):
                continue
            old_e = (pair_a(cur[3][3], cur[0][2]) + pair_w(cur[0][3], cur[1][2])) if r == 0 else (
                    (pair_w(cur[0][3], cur[1][2]) + pair_w(cur[1][3], cur[2][2])) if r == 1 else (
                    (pair_w(cur[1][3], cur[2][2]) + pair_w(cur[2][3], cur[3][2])) if r == 2 else
                    (pair_w(cur[2][3], cur[3][2]) + pair_a(cur[3][3], cur[0][2]))))
            new_e = (pair_a(cur[3][3], cand[2]) + pair_w(cand[3], cur[1][2])) if r == 0 else (
                    (pair_w(cur[0][3], cand[2]) + pair_w(cand[3], cur[2][2])) if r == 1 else (
                    (pair_w(cur[1][3], cand[2]) + pair_w(cand[3], cur[3][2])) if r == 2 else
                    (pair_w(cur[2][3], cand[2]) + pair_a(cand[3], cur[0][2]))))
            if new_e >= old_e or random.random() < math.exp((new_e - old_e) / temp):
                cur[r] = cand
                cur_sc += new_e - old_e
                if cur_sc > best_u[0]:
                    best_u = (cur_sc, list(cur))

    # Exhaustive C-speed coordinate polish on the best SA candidate (for d2=0)
    cur = best_u[1]
    if d2 == 0:
        for _ in range(2):
            for r in range(4):
                base = p2_13[r]
                best_r = (
                    (pair_a(cur[3][3], cur[0][2]) + pair_w(cur[0][3], cur[1][2])) if r == 0 else (
                    (pair_w(cur[0][3], cur[1][2]) + pair_w(cur[1][3], cur[2][2])) if r == 1 else (
                    (pair_w(cur[1][3], cur[2][2]) + pair_w(cur[2][3], cur[3][2])) if r == 2 else
                    (pair_w(cur[2][3], cur[3][2]) + pair_a(cur[3][3], cur[0][2])))),
                    cur[r]
                )
                for v, p13_14 in all_v:
                    if any(v == cur[k][0] for k in range(4) if k != r):
                        continue
                    s_sum = tuple(map(add, base, p13_14))
                    c = tuple(map(get_crt, s_sum))
                    c26 = tuple(map(get_crt26, s_sum))
                    sc_r = (pair_a(cur[3][3], c) + pair_w(c26, cur[1][2])) if r == 0 else (
                           (pair_w(cur[0][3], c) + pair_w(c26, cur[2][2])) if r == 1 else (
                           (pair_w(cur[1][3], c) + pair_w(c26, cur[3][2])) if r == 2 else
                           (pair_w(cur[2][3], c) + pair_a(c26, cur[0][2]))))
                    if sc_r > best_r[0]:
                        best_r = (sc_r, (v, 0, c, c26))
                cur[r] = best_r[1]

    final_sc = pair_w(cur[0][3], cur[1][2]) + pair_w(cur[1][3], cur[2][2]) + pair_w(cur[2][3], cur[3][2]) + pair_a(cur[3][3], cur[0][2])
    D = tuple(tuple((13 * U[j][c] + 14 * cur[j][0][c]) % 26 for c in range(4)) for j in range(4))
    d_vec = tuple((13 * d2_bits[j] + 14 * cur[j][1]) % 26 for j in range(4))
    return final_sc, D, d_vec, [x[2] for x in cur]

candidates_to_try = linear_hits[:2] + shifted_hits[:1]
best_overall = (-1e18, None, None, None)
for _, U, d2 in candidates_to_try:
    res = solve_for_U(U, d2)
    if res[0] > best_overall[0]:
        best_overall = res

sc, D, d_vec, cols = best_overall
print(f"\nTotal elapsed: {time.time()-t0:.2f}s | Best digram score: {sc:.2f}")
print("Decryption matrix D (mod 26):", D)
print("Encryption key K    (mod 26):", invert_26(D))
print("Additive shift d    (mod 26):", d_vec)
print("Plaintext:\n", "".join(chr(65 + cols[r][k]) for k in range(125) for r in range(4)))
