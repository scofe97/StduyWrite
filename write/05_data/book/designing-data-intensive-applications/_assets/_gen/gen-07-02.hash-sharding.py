# 07-02 §1 해시 함수로 균등 분산 — 문자열 파티션 키의 32비트 해시 공간 균등 사상과 샤딩용 해시 함수 요건.
# 사실 출처: 07-02 본문 §1(L23~L28), DDIA 2판 7장 p.10~11 "Sharding by Hash of Key" (그림 없음)
# 2026-10-31 검증: 원서에 예시 키·해시 값이 없어 user_1001·0x1F2A803B 같은 지어낸 값을 빼고 본문 문장(L26·L28)만 라벨로 남김
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
PY = 150
PH = 264
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "07-02 · §1 DATA FLOW", "해시 함수를 통한 파티션 키의 균등 분산",
      "유사한 문자열 파티션 키라도 해시 함수를 거쳐 0부터 2³²−1 공간에 균등하게 분포하며, 샤딩에는 프로세스 독립적인 해시 함수를 사용한다.",
      "문자열 키 입력 · 32비트 균등 분포 · 샤딩 적합 해시(MD5·Murmur3) vs 부적합(hashCode)")

# 상단 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "비슷한 입력도 전혀 다른 위치로 · 같은 키는 어느 프로세스에서든 같은 값", 12, INK, KR, "middle", 600)

# Column 1: 입력 파티션 키
X1 = 28; CW1 = 216
d.box(X1, PY, CW1, PH, PAPER2, RULE, 0.9)
d.chip(X1 + CW1 / 2, PY + 20, "입력 파티션 키", MUTED, 12)
d.t(X1 + CW1 / 2, PY + 42, "문자열 키", 12, SOFT, KR, "middle")
d.line(X1 + 12, PY + 52, X1 + CW1 - 12, PY + 52, RULE, 0.8)

keys = [
    ("아주 비슷한 문자열", "편향된 입력"),
    ("같은 키", "어느 프로세스에서든"),
]
for i, (k, sub) in enumerate(keys):
    ky = PY + 76 + i * 92
    d.box(X1 + 14, ky, CW1 - 28, 72, PAPER, RULE, 0.8)
    d.t(X1 + CW1 / 2, ky + 30, k, 13, INK, KR, "middle", 600)
    d.t(X1 + CW1 / 2, ky + 50, sub, 12, MUTED, KR, "middle")

# Column 2: 해시 함수 엔진
X2 = 268; CW2 = 300
d.box(X2, PY, CW2, PH, PAPER2, RULE, 0.9)
d.chip(X2 + CW2 / 2, PY + 20, "해시 함수 엔진", OK, 12)
d.t(X2 + CW2 / 2, PY + 42, "알고리즘별 샤딩 적합성 비교", 12, SOFT, KR, "middle")
d.line(X2 + 12, PY + 52, X2 + CW2 - 12, PY + 52, RULE, 0.8)

# 상단: 샤딩 적합 (OK)
d.tone(X2 + 14, PY + 64, CW2 - 28, 92, OK, 6, "18", 1.2)
d.t(X2 + CW2 / 2, PY + 86, "샤딩 적합 해시 함수", 13, INK, KR, "middle", 600)
d.t(X2 + CW2 / 2, PY + 106, "MD5 (MongoDB) · Murmur3", 12, OK, KR, "middle")
d.t(X2 + CW2 / 2, PY + 124, "암호학적 강도 불필요", 12, SOFT, KR, "middle")

# 하단: 샤딩 부적합 (BAD)
d.tone(X2 + 14, PY + 166, CW2 - 28, 86, BAD, 6, "18", 1.2)
d.t(X2 + CW2 / 2, PY + 188, "샤딩 부적합 해시 함수", 13, INK, KR, "middle", 600)
d.t(X2 + CW2 / 2, PY + 208, "Object.hashCode() · Object#hash", 12, BAD, MONO, "middle")
d.t(X2 + CW2 / 2, PY + 226, "Java · Ruby · 프로세스마다 다른 값", 12, SOFT, KR, "middle")
d.t(X2 + CW2 / 2, PY + 242, "샤딩에 쓸 수 없음", 12, MUTED, KR, "middle")

# Column 3: 32비트 균등 해시 공간
X3 = 592; CW3 = 260
d.box(X3, PY, CW3, PH, PAPER2, RULE, 0.9)
d.chip(X3 + CW3 / 2, PY + 20, "32비트 균등 해시 공간", INFO, 12)
d.t(X3 + CW3 / 2, PY + 42, "0 ~ 2³²−1 (0 ~ 4,294,967,295)", 12, SOFT, MONO, "middle")
d.line(X3 + 12, PY + 52, X3 + CW3 - 12, PY + 52, RULE, 0.8)

outputs = [
    ("고르게 분포한 출력", "전혀 다른 위치에 떨어짐"),
    ("같은 해시값", "같은 입력 → 같은 출력"),
]
for i, (top_v, sub_v) in enumerate(outputs):
    oy = PY + 76 + i * 92
    d.tone(X3 + 14, oy, CW3 - 28, 72, INFO, 6, "16", 1.0)
    d.t(X3 + CW3 / 2, oy + 30, top_v, 13, INK, KR, "middle", 600)
    d.t(X3 + CW3 / 2, oy + 50, sub_v, 12, INFO, KR, "middle")

# 연결 화살표: Col 1 -> Col 2 -> Col 3
d.arrow([(X1 + CW1, PY + 110), (X2 + 14, PY + 110)], MUTED, "ar", 1.4)
d.arrow([(X2 + CW2 - 14, PY + 110), (X3, PY + 110)], INFO, "info", 1.4)

d.legend(LEG, [("샤딩 적합 해시", OK), ("해시 공간 균등 분산", INFO), ("샤딩 부적합 해시", BAD), ("입력 파티션 키", MUTED)])
d.save("07-02.hash-sharding.svg")
