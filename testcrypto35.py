import math, random, re, time, pydoc, inspect

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

# Extract ~5,000+ real English words & quadgrams from Python's built-in stdlib docstrings
import os, sys, json, collections, itertools, functools, pathlib, urllib, http, email
blob_parts = []
for mod in (os, sys, json, collections, itertools, functools, pathlib, urllib, http, email, re, math, random):
    doc = inspect.getdoc(mod) or ""
    blob_parts.append(doc)
    for name in dir(mod)[:60]:
        obj = getattr(mod, name, None)
        d = inspect.getdoc(obj)
        if d:
            blob_parts.append(d[:600])

clean_text = re.sub(r"[^A-Za-z]+", " ", " ".join(blob_parts)).upper()
WORD_SET = {w for w in clean_text.split() if 3 <= len(w) <= 14}
WORD_SET |= {
    "WHEREVER","TEMPERATURE","TEMPERATURES","CONSTANT","UNDISTURBED","CAVES",
    "CAVERNS","CAVERN","EARTH","GROUND","SURFACE","DEPTH","DEPTHS","DEEP",
    "DEEPER","WINTER","SUMMER","SEASON","SEASONS","CLIMATE","WEATHER",
    "MOISTURE","HUMIDITY","PRESSURE","CONDITION","CONDITIONS","NATURAL",
    "NATURALLY","DIRECTLY","COMPLETELY","HOWEVER","ALTHOUGH","BECAUSE",
    "UNDERGROUND","SUBTERRANEAN","ATMOSPHERE","INSIDE","OUTSIDE","REMAINS"
}

# Build log-probability quadgram table from stdlib English prose
Q4_COUNTS = {}
stream_corpus = "".join(w for w in clean_text.split() if len(w) >= 2)
for i in range(len(stream_corpus) - 3):
    q = ((ord(stream_corpus[i])-65)*17576 + (ord(stream_corpus[i+1])-65)*676 +
         (ord(stream_corpus[i+2])-65)*26 + (ord(stream_corpus[i+3])-65))
    Q4_COUNTS[q] = Q4_COUNTS.get(q, 0) + 1

tot_q = sum(Q4_COUNTS.values())
FLOOR_Q = math.log(0.05 / tot_q)
Q4_LOG = {q: math.log(cnt / tot_q) for q, cnt in Q4_COUNTS.items()}
get_q4 = Q4_LOG.get

print(f"Built {len(WORD_SET)} English words & {len(Q4_LOG)} quadgrams in {time.time()-t0:.2f}s.")

# ==============================================================================
# PART 1: Test Quagmire IV (2 independent 26-letter alphabets + 20 key shifts)
# ==============================================================================
def score_q4(s):
    sc = 0.0
    for i in range(497):
        sc += get_q4(s[i]*17576 + s[i+1]*676 + s[i+2]*26 + s[i+3], FLOOR_Q)
    return sc

best_q4 = (-1e18, None)
for restart in range(6):
    pt_alpha = list(range(26))
    ct_alpha = list(range(26))
    random.shuffle(pt_alpha)
    random.shuffle(ct_alpha)
    shifts = [random.randrange(26) for _ in range(20)]

    def decode_q4(pa, ca, sh):
        inv_ca = [0]*26
        for idx, ch in enumerate(ca):
            inv_ca[ch] = idx
        res = [0]*500
        for r in range(25):
            base = r * 20
            for c in range(20):
                res[base + c] = pa[(inv_ca[cols_num[c][r]] - sh[c]) % 26]
        return res

    cur_s = decode_q4(pt_alpha, ct_alpha, shifts)
    cur_sc = score_q4(cur_s)
    for step in range(9000):
        temp = 3.0 * ((0.1 / 3.0) ** (step / 9000.0))
        mv = random.randrange(3)
        if mv == 0:
            i, j = random.sample(range(26), 2)
            pt_alpha[i], pt_alpha[j] = pt_alpha[j], pt_alpha[i]
            ns = decode_q4(pt_alpha, ct_alpha, shifts)
            nsc = score_q4(ns)
            if nsc >= cur_sc or random.random() < math.exp((nsc - cur_sc)/temp):
                cur_sc = nsc
                if cur_sc > best_q4[0]: best_q4 = (cur_sc, ns[:])
            else:
                pt_alpha[i], pt_alpha[j] = pt_alpha[j], pt_alpha[i]
        elif mv == 1:
            i, j = random.sample(range(26), 2)
            ct_alpha[i], ct_alpha[j] = ct_alpha[j], ct_alpha[i]
            ns = decode_q4(pt_alpha, ct_alpha, shifts)
            nsc = score_q4(ns)
            if nsc >= cur_sc or random.random() < math.exp((nsc - cur_sc)/temp):
                cur_sc = nsc
                if cur_sc > best_q4[0]: best_q4 = (cur_sc, ns[:])
            else:
                ct_alpha[i], ct_alpha[j] = ct_alpha[j], ct_alpha[i]
        else:
            c = random.randrange(20)
            old_sh = shifts[c]
            shifts[c] = (old_sh + random.randint(1, 25)) % 26
            ns = decode_q4(pt_alpha, ct_alpha, shifts)
            nsc = score_q4(ns)
            if nsc >= cur_sc or random.random() < math.exp((nsc - cur_sc)/temp):
                cur_sc = nsc
                if cur_sc > best_q4[0]: best_q4 = (cur_sc, ns[:])
            else:
                shifts[c] = old_sh

q4_pt = "".join(chr(65 + x) for x in best_q4[1])
print(f"\n=== Quagmire IV Best Quadgram Score: {best_q4[0]:.2f} (elapsed {time.time()-t0:.2f}s) ===")
print("PT[:120]:", q4_pt[:120])

# ==============================================================================
# PART 2: Unconstrained 20-Column Quadgram + Word-Boundary SA (Anchored)
# ==============================================================================
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

ENG = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]
eng_order = sorted(range(26), key=lambda i: ENG[i], reverse=True)

best_col20 = (-1e18, None)
for restart in range(10):
    perms = []
    for c in range(20):
        cnt = [cols_num[c].count(i) for i in range(26)]
        ct_order = sorted(range(26), key=lambda i: cnt[i] + random.random() * 0.8, reverse=True)
        p_map = [None] * 26
        used_pt = set(locked[c].values())
        for ct_fix, pt_fix in locked[c].items():
            p_map[ct_fix] = pt_fix
        rem_pt = [pt for pt in eng_order if pt not in used_pt]
        rem_ct = [ct for ct in ct_order if ct not in locked[c]]
        for ct_ch, pt_ch in zip(rem_ct, rem_pt):
            p_map[ct_ch] = pt_ch
        perms.append(p_map)

    stream = [perms[c][cols_num[c][r]] for r in range(25) for c in range(20)]
    cur_sc = score_q4(stream)

    for step in range(26000):
        temp = 3.2 * ((0.06 / 3.2) ** (step / 26000.0))
        c = random.randrange(20)
        free = [i for i in range(26) if i not in locked[c]]
        a, b = random.sample(free, 2)
        pa, pb = perms[c][a], perms[c][b]
        perms[c][a], perms[c][b] = pb, pa
        old_vals = [stream[r * 20 + c] for r in range(25)]
        for r in range(25):
            stream[r * 20 + c] = perms[c][cols_num[c][r]]
        new_sc = score_q4(stream)
        if new_sc >= cur_sc or random.random() < math.exp((new_sc - cur_sc) / temp):
            cur_sc = new_sc
            if cur_sc > best_col20[0]:
                best_col20 = (cur_sc, [p[:] for p in perms])
        else:
            perms[c][a], perms[c][b] = pa, pb
            for r in range(25):
                stream[r * 20 + c] = old_vals[r]

sc, best_perms = best_col20
print(f"\n=== 20-Column Quadgram Best Score: {sc:.2f} (elapsed {time.time()-t0:.2f}s) ===\n")
full_pt = []
for r in range(25):
    ln = "".join(chr(65 + best_perms[c][cols_num[c][r]]) for c in range(20))
    full_pt.append(ln)
    print(f"{r:2d}: {ln}")

print("\nContinuous Plaintext:\n" + "".join(full_pt))
