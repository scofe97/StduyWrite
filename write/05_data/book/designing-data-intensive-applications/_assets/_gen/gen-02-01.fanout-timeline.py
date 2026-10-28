# 02-01 §2 — 한 게시가 팔로워 N 의 타임라인으로 퍼지는 fan-out. 본문이 세운 정의와 수치(5,800 게시/초 × 200)만 그린다.
# 옛 도식의 폴링 A/B 두 단, 스파이크 큐, 극단 케이스 두 줄은 뺐다. 폴링 4억 조회는 §1 본문이 말로 맡고 여기엔 비교 한 칸만 둔다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
CY = 232
LEG = 492
H = LEG + 56

d = D(W, H, "02-01 · FAN-OUT", "한 게시가 팔로워 타임라인으로 퍼지는 fan-out",
      "게시 한 건이 팔로워 수만큼의 타임라인 쓰기로 늘어난다. 초당 5,800 게시에 fan-out 계수 200이면 초당 100만 건이 넘는 쓰기가 된다.",
      "게시 시점에 팔로워별 타임라인에 미리 배달")

d.box(16, CY - 36, 208, 72, PAPER2, INFO, 1.2)
d.t(120, CY - 4, "사용자 게시", 16, INK, KR, "middle", 600)
d.t(120, CY + 20, "5,800 게시/초", 13, MUTED, MONO)

d.tone(304, CY - 36, 176, 72, ACC, 6, "12", 1.4)
d.t(392, CY - 4, "fan-out", 16, ACC, MONO, "middle", 600)
d.t(392, CY + 20, "계수 200", 13, MUTED, KR)

d.arrow([(228, CY), (300, CY)], MUTED, "ar", 1.6)
d.line(480, CY, 548, CY, MUTED, 1.6)
d.line(548, 144, 548, 320, MUTED, 1.6)

TY = [(116, 144, "팔로워 1 타임라인"), (196, 224, "팔로워 2 타임라인"), (292, 320, "팔로워 200 타임라인")]
for y, cy, lab in TY:
    d.box(600, y, 264, 56, PAPER2, INFO, 1.2)
    d.t(732, cy + 5, lab, 14, INK, KR)
    d.arrow([(548, cy), (596, cy)], MUTED, "ar", 1.6)
d.t(732, 276, "⋯", 16, MUTED, MONO)

RY = 392
d.box(16, RY, 416, 72, PAPER2, INFO, 1.2)
d.t(224, RY + 30, "fan-out 쓰기", 15, INK, KR, "middle", 600)
d.t(224, RY + 54, "5,800 × 200 = 100만+ /초", 13, MUTED, MONO)
d.box(448, RY, 416, 72, PAPER, RULE, 1.0)
d.t(656, RY + 30, "폴링 조회 (비교)", 15, INK, KR, "middle", 600)
d.t(656, RY + 54, "4억 /초", 13, MUTED, MONO)

d.legend(LEG, [("핵심 — fan-out", ACC), ("저장되는 데이터", INFO)])
d.save("02-01.fanout-timeline.svg")
