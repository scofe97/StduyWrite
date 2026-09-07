# 01-04 §2 — 트래픽 강도 La/R 가 1 에 가까워질 때 평균 큐잉 지연이 어떻게 자라는가.
# 원문 Figure 1.19 는 축에 눈금을 두지 않은 *질적* 그림이고("The qualitative dependence...")
# 이 도식도 같다. 곡선의 모양은 대기행렬 이론의 표준 결과 rho/(1-rho) 로 뽑았고,
# 원문이 근거로 드는 Kleinrock 의 큐잉 이론이 그 출처다. y 축에 숫자를 두지 않는 이유가 이것이다.
# 타입 스펙: type-line — 연속 지표 위의 추세. 꺾은선으로 그리고 초점 계열에만 꼭짓점을 찍는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 568
PX0, PX1, PY0, PY1 = 130, 900, 132, 396

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-04 §2",
      "트래픽 강도가 1 에 가까워질 때",
      "원문 그림 1.19 와 같은 질적 관계. 가로축은 트래픽 강도 La/R 이고 세로축은 평균 큐잉 지연이다. 강도가 조금만 더 올라도 지연은 훨씬 크게 뛴다.",
      "세로축에 눈금이 없는 것은 원문과 같습니다 — 값이 아니라 모양이 요점입니다")

XS = [i / 20 for i in range(0, 19)]          # 0 ~ 0.90
def xpx(r): return PX0 + r / 0.95 * (PX1 - PX0)
def ypx(v): return PY1 - min(v / 9.0, 1.0) * (PY1 - PY0)

for r in (0, 0.25, 0.5, 0.75, 0.95):
    x = xpx(r)
    d.line(x, PY0, x, PY1, RULE, 0.8)
    d.t(x, PY1 + 26, f"{r:.2f}".rstrip("0").rstrip(".") if r else "0", 11, MUTED, MONO)
d.line(PX0, PY1, PX1, PY1, MUTED, 1.0)
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)
d.t(PX0 - 14, PY0 - 14, "평균 큐잉 지연", 11, SOFT, KR, "end")
d.t((PX0 + PX1) / 2, PY1 + 52, "트래픽 강도  La / R", 11, SOFT, MONO)

pts = " ".join(f"{xpx(r):.1f},{ypx(r / (1 - r)):.1f}" for r in XS)
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round"/>')
for r in (0.25, 0.5, 0.75, 0.9):
    d.o.append(f'<circle cx="{xpx(r):.1f}" cy="{ypx(r / (1 - r)):.1f}" r="4" fill="{ACC}"/>')

d.line(xpx(0.95), PY0, xpx(0.95), PY1, BAD, 1.4, "5 5")
d.t(xpx(0.95) - 10, PY0 + 18, "La/R > 1 이면 큐가 끝없이 자랍니다", 11, BAD, KR, "end")

d.t(PX0 - 106, 486, "원문의 황금률 — 트래픽 강도가 1 을 넘지 않도록 시스템을 설계하십시오. 늘 막히는 도로에 평소보다 조금 더 몰리면 지연이 크게 뛰는 것과 같습니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("평균 큐잉 지연", ACC), ("넘으면 안 되는 선", BAD)])
d.save("01-04.traffic-intensity.svg")
