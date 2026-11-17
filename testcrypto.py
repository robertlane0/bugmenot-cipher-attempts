import itertools, math

CT = (
    "DXXRKAKDQMDZQJPVUQSGDWRMHXCOTGVLTWERHIPNJPAZKNZSCVPRJWDXRFTYRMHYUJIPEBD"
    "YOOSYNVESLGBOEJMHYIVAMMWTMWECYFIDLGDJWBTDWCJOAWAAUZOVKCKPZXNVNJAKXCHGCHT"
    "MEZSIERWLCMHLZQEZSNJMIKNXLEGQIEWUBESCWBQXFASKZWYCKKARCNKRMPOJGBIJQZBOGFD"
    "EVDYUNIDWMQBWNMSSAAQJUGVAUIHWKRKLADILCMHOCSFNGBWCYNMMATGSOKFRCPHPIDYDTYA"
    "NXWZQBMWZOUGYSSMTJTMPLXVMEDBQHPKIBWRNDHSSJIPPALVQFMQQKKEZSZAAWNKSLNSHZWV"
    "YRMJESQTBSSAWMRAQEGPVPUJDPQUWLDHTJJNNYACPJHSEWKLPJUAHNWW"
    "DLDGUNIDWMQBOVTCVCKHPXMXWSSKRAEUIGHRKLBMHJYVOJEJFUTRGDFZHHXUPCSQMRD"
    "WOJMPYJBZHHXMXIF"
)
# Exact 500-char ciphertext reconstructed from the 101 groups:
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

ENG = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
]
LOG_ENG = [math.log(p) for p in ENG]

nums = [ord(c) - 65 for c in RAW]
blocks = [nums[i:i+4] for i in range(0, len(nums), 4)]
b2 = [[x % 2 for x in b] for b in blocks]
b13 = [[x % 13 for x in b] for b in blocks]

# Known mod-2 rows from parity bias analysis:
u_rows = [(0, 1, 0, 0), (1, 0, 1, 0), (1, 1, 0, 0), (1, 0, 0, 1)]
recovered_rows = []

for u in u_rows:
    p2 = [(u[0]*b[0] + u[1]*b[1] + u[2]*b[2] + u[3]*b[3]) % 2 for b in b2]
    best_score, best_row = -1e18, None
    for v in itertools.product(range(13), repeat=4):
        if v == (0, 0, 0, 0):
            continue
        score = 0.0
        for k, b in enumerate(b13):
            p13 = (v[0]*b[0] + v[1]*b[1] + v[2]*b[2] + v[3]*b[3]) % 13
            p = (13 * p2[k] + 14 * p13) % 26
            score += LOG_ENG[p]
        if score > best_score:
            best_score = score
            best_row = tuple((13 * u[j] + 14 * v[j]) % 26 for j in range(4))
    recovered_rows.append(best_row)

# Test all 24 row permutations using common English digrams:
COMMON_DI = {"TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND", "TI", "ES", "OR", "TE", "OF"}
best_perm_score, best_text, best_D = -1, "", None

for perm in itertools.permutations(recovered_rows):
    out = []
    for b in blocks:
        for r in perm:
            out.append(chr(65 + sum(r[j]*b[j] for j in range(4)) % 26))
    txt = "".join(out)
    di_score = sum(1 for i in range(len(txt) - 1) if txt[i:i+2] in COMMON_DI)
    if di_score > best_perm_score:
        best_perm_score, best_text, best_D = di_score, txt, perm

print("Decryption matrix D (mod 26):", best_D)
print("Plaintext:\n", best_text)
