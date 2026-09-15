# 04-03 §1 · 홉마다 바뀌는 세 바이트 — 같은 20바이트를 홉마다 한 행으로 쌓아 대조한다.
# 논지는 "무엇이 바뀌나"가 아니라 "17바이트는 그대로이고 3바이트만 바뀐다"이므로,
# 필드 지도(header-budget)와 겹치지 않게 *같은 자리의 값이 행마다 어떻게 변하는가*만 본다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다(계약 §타입을 본문이 정한다).
#           행 = 홉, 열 = 바이트 오프셋. 바뀌는 칸에만 색을 준다.
#           timeline 을 검토했으나 축이 시간이 아니라 바이트 오프셋이라 기각.
#           layers 도 검토했으나 위아래가 추상 수준이 아니라 같은 층의 반복이라 기각.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, WARN, OK, KR, MONO

W, H = 940, 448
d = D(W, H, "IPV4 HEADER · HOP BY HOP",
      "홉마다 바뀌는 것은 세 바이트뿐입니다",
      "같은 IP 헤더 20바이트를 홉마다 한 행으로 쌓아 대조한 격자. 17바이트는 끝까지 그대로이고 "
      "TTL 1바이트와 그 때문에 다시 계산되는 헤더 체크섬 2바이트만 바뀐다.",
      "회색 17칸은 출발할 때 값 그대로, 색칠한 3칸만 라우터가 고쳐 씁니다")

# ── 격자: 20열 × 3행. 열 폭 40, 행 높이 44, 4의 배수 ──
X0, Y0 = 132, 132
CW, RH, G = 38, 44, 2
STRIDE = CW + G

# 오프셋 눈금 — 바뀌는 자리만 숫자를 적는다
for i in range(20):
    x = X0 + i * STRIDE
    lab = str(i) if i in (8, 10, 11) else ""
    if lab:
        d.t(x + CW / 2, Y0 - 14, lab, 10, WARN, MONO, "middle", 600)
d.t(X0 - 12, Y0 - 14, "byte", 10, SOFT, MONO, "end")

# (홉 이름, 부제, TTL 값, 체크섬 2바이트)
ROWS = [
    ("출발 · 이 기계", "tcpdump 로 실측한 값", "40", ("c1", "00"), OK),
    ("라우터 1 통과", "TTL 64 → 63", "3f", ("c2", "00"), WARN),
    ("라우터 2 통과", "TTL 63 → 62", "3e", ("c3", "00"), WARN),
]

# 바뀌지 않는 17바이트의 실측 값 (offset → hex)
FIXED = {0: "45", 1: "00", 2: "00", 3: "54", 4: "f6", 5: "82", 6: "00", 7: "00",
         9: "01", 12: "c0", 13: "a8", 14: "00", 15: "7c",
         16: "01", 17: "01", 18: "01", 19: "01"}

for r, (name, sub, ttl, (ck_hi, ck_lo), tint) in enumerate(ROWS):
    y = Y0 + r * (RH + G)
    d.t(X0 - 12, y + 20, name, 12, INK, KR, "end", 600)
    d.t(X0 - 12, y + 36, sub, 11, MUTED, KR, "end")
    for i in range(20):
        x = X0 + i * STRIDE
        if i == 8:
            val, col = ttl, tint
        elif i == 10:
            val, col = ck_hi, tint
        elif i == 11:
            val, col = ck_lo, tint
        else:
            val, col = FIXED[i], None
        if col:
            d.tone(x, y, CW, RH, col, 3, "1E", 1.3)
            d.t(x + CW / 2, y + 27, val, 12, col, MONO, "middle", 600)
        else:
            d.box(x, y, CW, RH, PAPER2, f"{INK}33", 0.9, 3)
            d.t(x + CW / 2, y + 27, val, 11, MUTED, MONO, "middle")

YBOT = Y0 + 3 * (RH + G)

# ── 바뀌는 세 칸만 아래에서 묶어 이름을 준다 ──
def brace(i0, i1, label, sub, col):
    xa = X0 + i0 * STRIDE
    xb = X0 + i1 * STRIDE + CW
    cx = (xa + xb) / 2
    d.path(f"M {xa} {YBOT + 8} L {xa} {YBOT + 16} L {xb} {YBOT + 16} L {xb} {YBOT + 8}",
           col, 1.2)
    d.t(cx, YBOT + 38, label, 12, col, KR, "middle", 600)
    d.t(cx, YBOT + 56, sub, 11, MUTED, KR, "middle")

brace(8, 8, "TTL", "", WARN)
brace(10, 11, "헤더 체크섬", "", WARN)

# 두 이름의 부제는 한 줄로 합쳐 브레이스 아래에 둔다 (겹침 회피)
d.t(X0 + 10 * STRIDE, YBOT + 58, "1씩 줄고, 그 때문에 다시 계산됨", 11, MUTED, KR, "middle")

# 그대로 가는 구간은 한 번만 말한다
d.t(X0 + 2 * STRIDE, YBOT + 38, "나머지 17바이트", 12, SOFT, KR, "middle")
d.t(X0 + 2 * STRIDE, YBOT + 58, "출발할 때 값 그대로", 11, MUTED, KR, "middle")
d.t(X0 + 16 * STRIDE, YBOT + 38, "주소 8바이트", 12, SOFT, KR, "middle")
d.t(X0 + 16 * STRIDE, YBOT + 58, "라우터가 고치지 않음", 11, MUTED, KR, "middle")

d.line(40, 384, W - 40, 384, RULE, 0.8)
d.t(W // 2, 410, "TTL −1 → 체크섬 +0x0100 · 20바이트 재훑기 없음",
    12, MUTED, KR, "middle")
d.t(900, 434, "RFC 791 · 20B, NO OPTIONS · RFC 1624 INCREMENTAL UPDATE", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.hop-rewrite.svg"
d.save(out)
print("ok →", out)
