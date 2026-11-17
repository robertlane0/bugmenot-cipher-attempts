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
lines = [RAW[i:i+20] for i in range(0, 500, 20)]

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

add = operator.add
get_di = DI_FLAT.__getitem__

# ==============================================================================
# PART A: Period-20 Mixed-Alphabet / Quagmire / Wheel Cipher Solver (20 columns)
# ==============================================================================
cols_num = [[ord(lines[r][c]) - 65 for r in range(25)] for c in range(20)]
# Initialize each column's 26-letter substitution by frequency rank matching English
eng_order = sorted(range(26), key=lambda i: ENG[i], reverse=True)
perms = []
for c in range(20):
    cnt = [cols_num[c].count(i) for i in range(26)]
    ct_order = sorted(range(26), key=lambda i: cnt[i], reverse=True)
    p_map = [0] * 26
    for rank, ct_ch in enumerate(ct_order):
        p_map[ct_ch] = eng_order[rank]
    perms.append(p_map)

dec_cols = [[perms[c][x] for x in cols_num[c]] for c in range(20)]
dec_cols26 = [[x * 26 for x in col] for col in dec_cols]

def col_pair_sc(c):
    return sum(map(get_di, map(add, dec_cols26[c], dec_cols[c + 1])))

cur_q_sc = sum(col_pair_sc(c) for c in range(19))
best_q = (cur_q_sc, [p[:] for p in perms])

for step in range(25000):
    temp = 2.0 * ((0.15 / 2.0) ** (step / 25000.0))
    c = random.randrange(20)
    a, b = random.sample(range(26), 2)
    pa, pb = perms[c][a], perms[c][b]
    old_e = (col_pair_sc(c - 1) if c > 0 else 0.0) + (col_pair_sc(c) if c < 19 else 0.0)
    perms[c][a], perms[c][b] = pb, pa
    new_col = [perms[c][x] for x in cols_num[c]]
    old_col, old_col26 = dec_cols[c], dec_cols26[c]
    dec_cols[c] = new_col
    dec_cols26[c] = [x * 26 for x in new_col]
    new_e = (col_pair_sc(c - 1) if c > 0 else 0.0) + (col_pair_sc(c) if c < 19 else 0.0)
    if new_e >= old_e or random.random() < math.exp((new_e - old_e) / temp):
        cur_q_sc += new_e - old_e
        if cur_q_sc > best_q[0]:
            best_q = (cur_q_sc, [p[:] for p in perms])
    else:
        perms[c][a], perms[c][b] = pa, pb
        dec_cols[c], dec_cols26[c] = old_col, old_col26

print(f"=== PART A: Period-20 Mixed-Alphabet / Wheel Cipher (elapsed {time.time()-t0:.2f}s) ===")
print(f"Digram score: {best_q[0]:.2f}")
q_perms = best_q[1]
for r in range(6):
    print(f"Line {r:2d}: " + "".join(chr(65 + q_perms[c][cols_num[c][r]]) for c in range(20)))

# ==============================================================================
# PART B: 5-Key Periodic 4x4 Hill Cipher (with strict rank-4 invertibility check)
# ==============================================================================
CRT26 = tuple(x % 26 for x in range(182))
CRT26_X26 = tuple((x % 26) * 26 for x in range(182))
get_crt = CRT26.__getitem__
get_crt26 = CRT26_X26.__getitem__

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

def solve_group(g):
    blks = [[ord(ln[4*g + j]) - 65 for j in range(4)] for ln in lines]
    b2 = [[x % 2 for x in b] for b in blks]
    b13 = [[x % 13 for x in b] for b in blks]

    u_scored = sorted(
        [(sum(1 for b in b2 if (u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3]) % 2 == 0), u)
         for u in itertools.product(range(2), repeat=4) if u != (0, 0, 0, 0)],
        reverse=True
    )
    u_rows = []
    for _, u in u_scored:
        if rank_mod(u_rows + [u], 2) > len(u_rows):
            u_rows.append(u)
            if len(u_rows) == 4:
                break

    p2_13 = [tuple(((u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3]) % 2) * 13 for b in b2) for u in u_rows]
    b0_13, b1_13, b2_13, b3_13 = [b[0] for b in b13], [b[1] for b in b13], [b[2] for b in b13], [b[3] for b in b13]

    all_v = []
    for v0 in range(13):
        s0 = [v0 * x for x in b0_13]
        for v1 in range(13):
            s01 = [s0[k] + v1 * b1_13[k] for k in range(25)]
            for v2 in range(13):
                s012 = [s01[k] + v2 * b2_13[k] for k in range(25)]
                for v3 in range(13):
                    if v0 or v1 or v2 or v3:
                        all_v.append(((v0, v1, v2, v3), tuple(((s012[k] + v3 * b3_13[k]) % 13) * 14 for k in range(25))))

    pools = []
    for ui in range(4):
        base = p2_13[ui]
        scored = []
        for v, p13_14 in all_v:
            c = tuple(map(get_crt, map(add, base, p13_14)))
            scored.append((sum(map(LOG_ENG.__getitem__, c)), v, c, tuple(x * 26 for x in c)))
        scored.sort(reverse=True)
        pools.append([(v, c, c26) for _, v, c, c26 in scored[:500]])

    def pair_w(cL26, cR): return sum(map(get_di, map(add, cL26, cR)))

    best_g = (-1e18, None, None)
    for perm in itertools.permutations(range(4)):
        # Pick 4 linearly independent mod-13 vectors to initialize
        cur = []
        for r in range(4):
            for cand in pools[perm[r]]:
                if rank_mod([x[0] for x in cur] + [cand[0]], 13) > r:
                    cur.append(cand)
                    break
        for step in range(900):
            temp = 2.0 * ((0.15 / 2.0) ** (step / 900.0))
            r = random.randrange(4)
            cand = pools[perm[r]][random.randrange(500)]
            other_v = [cur[k][0] for k in range(4) if k != r]
            if rank_mod(other_v + [cand[0]], 13) < 4:
                continue
            old_e = pair_w(cur[0][2], cur[1][1]) if r == 0 else (
                    (pair_w(cur[0][2], cur[1][1]) + pair_w(cur[1][2], cur[2][1])) if r == 1 else (
                    (pair_w(cur[1][2], cur[2][1]) + pair_w(cur[2][2], cur[3][1])) if r == 2 else
                    pair_w(cur[2][2], cur[3][1])))
            new_e = pair_w(cand[2], cur[1][1]) if r == 0 else (
                    (pair_w(cur[0][2], cand[1]) + pair_w(cand[2], cur[2][1])) if r == 1 else (
                    (pair_w(cur[1][2], cand[1]) + pair_w(cand[2], cur[3][1])) if r == 2 else
                    pair_w(cur[2][2], cand[1])))
            if new_e >= old_e or random.random() < math.exp((new_e - old_e) / temp):
                cur[r] = cand

        # Coordinate polish preserving rank_mod(..., 13) == 4
        for r in range(4):
            base = p2_13[perm[r]]
            other_v = [cur[k][0] for k in range(4) if k != r]
            best_r = (
                pair_w(cur[0][2], cur[1][1]) if r == 0 else (
                (pair_w(cur[0][2], cur[1][1]) + pair_w(cur[1][2], cur[2][1])) if r == 1 else (
                (pair_w(cur[1][2], cur[2][1]) + pair_w(cur[2][2], cur[3][1])) if r == 2 else
                pair_w(cur[2][2], cur[3][1]))),
                cur[r]
            )
            for v, p13_14 in all_v:
                s_sum = tuple(map(add, base, p13_14))
                c = tuple(map(get_crt, s_sum))
                c26 = tuple(map(get_crt26, s_sum))
                sc_r = pair_w(c26, cur[1][1]) if r == 0 else (
                       (pair_w(cur[0][2], c) + pair_w(c26, cur[2][1])) if r == 1 else (
                       (pair_w(cur[1][2], c) + pair_w(c26, cur[3][1])) if r == 2 else
                       pair_w(cur[2][2], c)))
                if sc_r > best_r[0] and rank_mod(other_v + [v], 13) == 4:
                    best_r = (sc_r, (v, c, c26))
            cur[r] = best_r[1]

        final_sc = pair_w(cur[0][2], cur[1][1]) + pair_w(cur[1][2], cur[2][1]) + pair_w(cur[2][2], cur[3][1])
        D = tuple(tuple((13 * u_rows[perm[r]][c] + 14 * cur[r][0][c]) % 26 for c in range(4)) for r in range(4))
        if final_sc > best_g[0]:
            best_g = (final_sc, D, [cur[r][1] for r in range(4)])
    return best_g

print(f"\n=== PART B: 5-Key Periodic 4x4 Hill Cipher ===")
for g in range(5):
    sc, D, cols = solve_group(g)
    sample = " ".join("".join(chr(65 + cols[r][k]) for r in range(4)) for k in range(6))
    print(f"Group {g} | Score: {sc:.2f} | Sample: {sample}")
print(f"Total elapsed: {time.time() - t0:.2f}s")
