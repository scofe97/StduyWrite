# 01-03 §2 — 원문의 수치 예. 같은 1 Mbps 링크에서 회선 교환은 열 명, 패킷 교환은 서른다섯 명을 받는다.
# 값 출처: 원문 1.3.2 "Packet Switching Versus Circuit Switching" — 사용자는 활성 시 100 kbps 를
#          내고 활성 확률은 0.1. 패킷 교환에서 35명일 때 11명 이상이 동시에 활성일 확률은 약 0.0004.
# 타입 스펙: type-bar — 범주별 단일 수치 비교. y축은 0에서 시작하고 눈금 다섯을 둔다.
#           축약: 스펙의 막대 수 권장 범위(4~8)보다 적은 둘이다. 원문이 비교하는 값이 둘뿐이라
#           범주를 지어내지 않고 둘로 둔다 — 잘림 없는 0 기준 축이라 비교는 정직하다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 588
PX0, PX1, PY0, PY1 = 130, 900, 132, 400
YMAX = 40

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-03 §2",
      "같은 링크로 몇 명을 받나",
      "원문의 수치 예. 1 Mbps 링크를 쓰는 사용자가 활성일 때 100 kbps 를 내고 활성 확률이 0.1 일 때, 두 방식이 감당하는 사용자 수. 회선 교환은 수요와 무관하게 미리 떼어 두고, 패킷 교환은 필요할 때만 나눠 준다.",
      "패킷 교환 쪽이 성능을 거의 그대로 두면서 세 배 넘는 사용자를 받습니다")

def ypx(v): return PY1 - (v / YMAX) * (PY1 - PY0)

for g in range(0, YMAX + 1, 10):
    y = ypx(g)
    d.line(PX0, y, PX1, y, RULE, 0.8)
    d.t(PX0 - 12, y + 4, str(g), 11, MUTED, MONO, "end")
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)
d.line(PX0, PY1, PX1, PY1, MUTED, 1.0)
d.t(PX0 - 12, PY0 - 16, "동시 사용자 수", 11, SOFT, KR, "end")

BARS = [("회선 교환", "1 Mbps ÷ 100 kbps = 10", 10, False),
        ("패킷 교환", "11명 이상 동시 활성 확률 0.0004", 35, True)]
BW, PITCH = 220, 390
for i, (name, sub, v, focal) in enumerate(BARS):
    cx = PX0 + 66 + i * PITCH + BW / 2
    x, y = cx - BW / 2, ypx(v)
    h = PY1 - y
    if focal: d.tone(x, y, BW, h, ACC, 4)
    else: d.box(x, y, BW, h, PAPER2, MUTED, 1.0, 4)
    d.t(cx, y - 12, f"{v}명", 12, ACC if focal else MUTED, MONO, "middle", 600)
    d.t(cx, PY1 + 26, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, PY1 + 46, sub, 11, MUTED, KR)

d.t(PX0 - 106, 492, "회선 교환은 수요와 무관하게 미리 떼어 두고 남는 시간은 버려집니다. 패킷 교환은 보낼 것이 있는 사용자끼리만 링크를 나눠 씁니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("필요할 때만 나눠 주는 쪽", ACC)])
d.save("01-03.packet-vs-circuit.svg")
