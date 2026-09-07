# 03-01 §6 — UDP 체크섬 계산. 값은 원문 3.3.2 의 예제 그대로이고 세 단계를 파이썬으로 검산해 일치를 확인했다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(하는 일 · 결과 비트 · 왜 그렇게 하나)이 반복되고 왼쪽에서 오른쪽으로 흐른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 560
BW, BH, BY = 212, 176, 156
XS = [140, 380, 620, 860]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-01 §6",
      "체크섬은 어떻게 계산되나",
      "원문 3.3.2 의 예제. 16비트 낱말을 더하고 넘침을 되감은 뒤 1의 보수를 취한다. 받는 쪽은 체크섬까지 더해 전부 1이 나오는지 본다.",
      "세 단계의 비트값을 파이썬으로 검산했고 원문과 모두 일치합니다")

STEPS = [
    ("1. 16비트로 자른다", ["0110011001100000", "0101010101010101", "1000111100001100"],
     "세그먼트를 16비트 낱말로 나눕니다", MUTED, False),
    ("2. 더하고 되감는다", ["1011101110110101", "+ 1000111100001100", "= 0100101011000010"],
     "넘친 자리를 버리지 않고 다시 더합니다", MUTED, False),
    ("3. 1의 보수", ["0100101011000010", "↓ 0 과 1 을 뒤집는다", "1011010100111101"],
     "이것이 체크섬 필드에 들어갑니다", ACC, True),
    ("4. 받는 쪽 검산", ["0100101011000010", "+ 1011010100111101", "= 1111111111111111"],
     "전부 1 이면 오류가 없습니다", OK, True),
]

for x, (title, lines, why, c, focal) in zip(XS, STEPS):
    if focal:
        d.tone(x - BW / 2, BY, BW, BH, c, 6, "14", 1.4)
    else:
        d.box(x - BW / 2, BY, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x, BY + 28, title, 12, c if focal else INK, KR, "middle", 600)
    for i, ln in enumerate(lines):
        d.t(x, BY + 62 + i * 24, ln, 11, SOFT if not focal else c, MONO)
    d.t(x, BY + 152, why, 11, SOFT, KR)

for i in range(3):
    d.path(f"M {XS[i] + BW / 2 + 4} {BY + BH / 2} L {XS[i+1] - BW / 2 - 10} {BY + BH / 2}",
           MUTED, 1.2, m="ar")

d.t(24, 400, "링크 층이 이미 오류를 검사하는데 왜 또 하는가. 경로의 모든 링크가 검사한다는 보장이 없고, 링크를 제대로 건너도 라우터 메모리에서 비트가 뒤집힐 수 있습니다.",
     11, MUTED, KR, "start")
d.t(24, 422, "종단 간 원칙 — 낮은 층에 놓인 기능은 높은 층에서 그것을 제공하는 비용에 비해 중복이거나 값이 거의 없을 수 있습니다.",
     11, MUTED, KR, "start")
d.t(24, 452, "UDP 는 오류를 검출만 하고 회복은 하지 않습니다. 구현에 따라 손상된 세그먼트를 버리거나 경고와 함께 올려 줍니다.",
     11, SOFT, KR, "start")

d.legend(H - 44, [("체크섬 값", ACC), ("수신 측 검산", OK), ("계산 단계", MUTED)])
d.save("03-01.udp-checksum.svg")
