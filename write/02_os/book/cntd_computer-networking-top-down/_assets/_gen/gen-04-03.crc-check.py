# 04-03 §1 곁노트 — CRC. 보낼 때 나머지를 붙이고, 받아서 같은 계산을 해 맞춰 본다.
# 2026-09-14 신설: 손으로 쓴 SVG 만 있어 타입 선택 절차를 한 번도 거치지 않은 장이었다.
#   바닥에 세 줄짜리 설명 문단이 그대로 얹혀 있었는데, 그건 도식이 아니라 본문이라 걷어냈다.
#   (왜 개수 세기가 아니라 나머지인가 / IPv6 헤더 체크섬 근거 — 본문 산문으로 옮긴다.)
# 타입 스펙: type-data-flow — 같은 데이터가 보내는 쪽에서 받는 쪽으로 건너가며 무엇이 달라지는가.
#           위아래 두 줄은 같은 계산을 거친 같은 프레임이고, 갈리는 것은 나머지 한 값뿐이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 420

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-03 §1",
      "나머지를 붙여 보내고 받아서 다시 셉니다",
      "이더넷 프레임 끝에 붙는 4바이트 CRC. 보내는 쪽이 데이터를 정해진 수로 나눈 나머지를 붙여 보내면 "
      "받는 쪽이 같은 계산을 다시 해 두 값을 맞춰 본다. 어긋나면 그 홉에서 버려지고 위층까지 가지 않는다.",
      "링크를 건너다 깨졌는지 그 홉에서 바로 잡아냅니다")

DATA = "1 1 0 1 0 1 1 0"
SENT = "1 1 0 1 0 1 1 0 1 0 1"
FLIPPED = "1 1 1 1 0 1 1 0 1 0 1"   # 셋째 비트가 0→1 로 뒤집힌 프레임

# ── 보내는 쪽 — 데이터 → 나눗셈 → 나머지를 뒤에 붙임
d.t(24, 126, "보내는 쪽", 13, SOFT, KR, "start", 600)
d.box(24, 140, 168, 38, PAPER2, RULE, 1.0, 5)
d.t(108, 164, DATA, 13, INK, MONO)
d.t(108, 194, "보낼 데이터", 12, MUTED, KR)

d.path("M 200 159 L 244 159", MUTED, 1.3, m="ar")
d.tone(252, 140, 132, 38, INFO, 5, "14", 1.2)
d.t(318, 164, "정해진 수로 나눔", 12, INFO, KR)

d.path("M 392 159 L 436 159", MUTED, 1.3, m="ar")
d.tone(444, 140, 108, 38, ACC, 5, "14", 1.2)
d.t(498, 164, "나머지 101", 13, ACC, MONO)

d.path("M 560 159 L 604 159", MUTED, 1.3, m="ar")
d.box(612, 140, 244, 38, PAPER2, ACC, 1.2, 5)
d.t(734, 164, SENT, 13, INK, MONO)
d.t(734, 194, "뒤에 붙여 보냄", 12, MUTED, KR)

# ── 받는 쪽 두 갈래 — 같은 프레임, 갈리는 것은 다시 센 나머지뿐
CASES = [(24, OK, "무사히 건넜을 때", SENT, "다시 센 나머지 101", "붙어 온 값과 같음 → 통과", None),
         (452, BAD, "비트 하나가 뒤집혔을 때", FLIPPED, "다시 센 나머지 011", "붙어 온 값과 다름 → 버림", 600)]

for x0, c, head, bits, again, verdict, flip in CASES:
    d.tone(x0, 228, 404, 116, c, 6, "0A", 1.2)
    d.t(x0 + 20, 252, head, 13, c, KR, "start", 600)
    d.box(x0 + 20, 264, 244, 34, PAPER2, c, 1.1, 5)
    d.t(x0 + 142, 286, bits, 13, INK, MONO)
    if flip:
        d.t(x0 + 68, 258, "0→1", 11, BAD, MONO)
    d.t(x0 + 20, 320, again, 12, c, KR, "start")
    d.t(x0 + 20, 338, verdict, 12, MUTED, KR, "start")

d.legend(H - 44, [("붙여 보낸 나머지", ACC), ("통과", OK), ("그 홉에서 버림", BAD)])
d.save("04-03.crc-check.svg")
print("ok crc-check")
