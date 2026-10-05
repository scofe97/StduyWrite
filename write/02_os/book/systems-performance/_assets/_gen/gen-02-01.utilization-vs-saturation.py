# 02-01 §9 — 부하가 용량을 넘으면 사용률은 멈추고 포화가 자란다.
# 타입 스펙: type-line — 요청된 일(용량 대비 %)이라는 연속 축 위의 두 계열.
#           원서 그림 2.8(p.17): 용량 기반 사용률 100% 지점 뒤로 포화가 선형으로 는다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 928, 480
X0, Y0, PW, PH = 112, 120, 712, 248
XMAX, YMAX = 200, 100

def px(v): return X0 + PW * v / XMAX
def py(v): return Y0 + PH - PH * v / YMAX

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-01 §9",
       "용량을 넘는 일은 큐에 쌓인다",
       "요청된 일을 용량 대비 % 로 늘려 갈 때, 용량 기반 사용률은 100% 에서 멈추고 처리 못 한 일(포화)이 그 뒤로 선형으로 쌓인다.",
       "원서 그림 2.8 — 용량 기반 사용률 기준")

for v in (0, 50, 100):
    d.line(X0, py(v), X0 + PW, py(v), RULE, 0.8)
    d.t(X0 - 12, py(v) + 4, f"{v}%", 12, SOFT, MONO, "end")
for v in (0, 50, 100, 150, 200):
    d.t(px(v), Y0 + PH + 22, f"{v}%", 12, SOFT, MONO, "middle")
d.t(X0 + PW, Y0 + PH + 44, "요청된 일 (용량 대비) →", 12, SOFT, KR, "end")
d.line(X0, Y0, X0, Y0 + PH, MUTED, 1.0)

d.line(px(100), Y0 + 4, px(100), Y0 + PH, SOFT, 1.0, "4 4")
d.t(px(100) + 8, Y0 + 16, "용량 100%", 12, SOFT, KR, "start")

util = [(0, 0), (100, 100), (200, 100)]
sat = [(0, 0), (100, 0), (200, 100)]
for pts, c, sw in ((util, INFO, 1.6), (sat, ACC, 2.0)):
    s = " ".join(f"{px(a):.1f},{py(b):.1f}" for a, b in pts)
    d.o.append(f'<polyline points="{s}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
d.t(px(44), py(56), "사용률", 13, INFO, KR, "end", 600)
d.t(px(176), py(100) - 12, "더 오르지 않는다", 12, INFO, KR, "middle")
d.t(px(160), py(36), "포화 — 큐에서 기다리는 일", 13, ACC, KR, "start", 600)

d.legend(Y0 + PH + 60, [("사용률", INFO), ("포화", ACC)])
d.save("02-01.utilization-vs-saturation.svg")
