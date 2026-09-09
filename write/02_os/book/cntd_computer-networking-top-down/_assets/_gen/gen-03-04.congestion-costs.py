# 03-04 §4 — 원문 3.6.1 의 세 시나리오에서 뽑히는 네 가지 대가. 그 넷이 모여 혼잡 붕괴가 된다.
# 각 가지의 문구는 원문이 이탤릭으로 강조한 "cost of a congested network" 문장 그대로다.
# 타입 스펙: type-fishbone — 머리에 결과를 두고 뼈마다 그것을 만드는 원인 갈래를 단다.
#           축약: 스펙의 기준 캔버스(HEAD 1200 · viewBox 1440)가 이 책의 폭 규칙 880~1000 을 넘으므로
#           가지 간격 dx/dy 를 96/168 에서 64/112 로 줄였다. 비율 1.75(약 60도)는 그대로 지킨다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 608
SPINE_Y = 300
SX0, SX1 = 90, 800
DX, DY = 64, 112

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §4",
      "혼잡의 대가는 넷입니다",
      "원문이 시나리오 셋을 거치며 뽑아내는 대가. 지연 증가에서 시작해 상류 작업의 낭비까지 가면 혼잡 붕괴가 된다.",
      "원문은 혼잡 제어 방법을 꺼내기 전에 혼잡이 무엇을 망가뜨리는지부터 보여 줍니다")

# 등뼈
d.path(f"M {SX0} {SPINE_Y} L {SX1} {SPINE_Y}", MUTED, 1.6, m="ar")
d.tone(SX1 + 8, SPINE_Y - 44, 168, 88, ACC, 8, "14", 1.4)
d.t(SX1 + 92, SPINE_Y - 12, "혼잡 붕괴", 13, ACC, KR, "middle", 600)
d.t(SX1 + 92, SPINE_Y + 10, "부하를 올리는데", 11, SOFT, KR)
d.t(SX1 + 92, SPINE_Y + 28, "처리량이 내려갑니다", 11, SOFT, KR)

BONES = [
    (1, "시나리오 1", "큐잉 지연이 커집니다", "도착률이 링크 용량에 가까워질수록", INFO),
    (-1, "시나리오 2", "재전송을 해야 합니다", "버려진 패킷을 메우려고", WARN),
    (1, "시나리오 2", "불필요한 재전송이 낭비합니다", "이미 도착한 패킷의 사본을 나릅니다", WARN),
    (-1, "시나리오 3", "상류의 작업이 버려집니다", "중간에서 버려지면 거기까지의 전송 용량이 전부", OK),
]
BX = [190, 320, 450, 580]
for (side, sc, title, why, c), bx in zip(BONES, BX):
    ex, ey = bx + DX, SPINE_Y - side * DY
    d.path(f"M {ex} {ey} L {bx} {SPINE_Y}", c, 1.3)
    ty = ey - (14 if side > 0 else -14)
    d.t(ex + 6, ty - 18, sc, 11, SOFT, MONO, "start")
    d.t(ex + 6, ty, title, 12, c, KR, "start", 600)
    d.t(ex + 6, ty + 20, why, 11, SOFT, KR, "start")

d.t(24, 508, "시나리오 2 의 숫자 — 제공 부하가 R/2 일 때 처리량은 R/3 입니다. 0.5R 중 0.333R 만 원래 데이터이고 0.166R 은 재전송입니다.",
     11, MUTED, KR, "start")
d.t(24, 530, "패킷마다 평균 두 번 전달되면 처리량이 R/4 로 수렴합니다. 링크는 쉬지 않는데 쓸모 있는 일은 줄어듭니다.",
     11, MUTED, KR, "start")

d.legend(H - 44, [("셋이 모인 결과", ACC), ("지연 쪽 대가", INFO), ("재전송 쪽 대가", WARN), ("낭비 쪽 대가", OK)])
d.save("03-04.congestion-costs.svg")
