# 02-03 §4 — 요청률과 CPU 사용량의 직선을 전 CPU 100% 까지 외삽.
# 타입 스펙: type-line — 요청률(x)에 대한 CPU 사용률(y) 한 계열과 외삽.
#           원서 p.57: 1,000 req/s 에서 CPU 16개 평균 40% → 요청당 0.64% → 1,600 / 0.64 = 2,500 req/s.
#           세로축은 전체 CPU 용량 대비 % (16 CPU × 100% = 100%).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, BAD, RULE, KR, MONO

W, H = 928, 512
X0, Y0, PW, PH = 96, 120, 736, 280
XMAX, YMAX = 3000, 120
PER_REQ = 16 * 40 / 1000            # CPU% (한 CPU = 100%) per request
LIMIT = 100 * 16 / PER_REQ          # 2,500

def px(v): return X0 + PW * v / XMAX
def py(v): return Y0 + PH - PH * v / YMAX
def util(req): return req * PER_REQ / 16   # 전체 용량 대비 %

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03 §4",
       "점 하나로 그은 직선이 2,500 에서 벽에 닿는다",
       "초당 1,000 요청에서 CPU 16개가 평균 40% 였다. 요청당 사용량이 일정하다고 보고 직선을 전 CPU 100% 까지 늘이면 2,500 req/s 다.",
       "원서 p.57 의 계산 · 거친 최선 추정")

for v in (0, 40, 80, 100):
    d.line(X0, py(v), X0 + PW, py(v), RULE, 0.8)
    d.t(X0 - 12, py(v) + 4, f"{v}%", 12, SOFT, MONO, "end")
for v in (0, 1000, 2000, 2500, 3000):
    d.t(px(v), Y0 + PH + 22, f"{v:,}", 12, SOFT, MONO, "middle")
d.t(X0 + PW, Y0 + PH + 44, "요청/s →", 12, SOFT, KR, "end")
d.t(X0 - 12, Y0 - 14, "CPU 16개 합", 12, SOFT, KR, "end")
d.line(X0, Y0, X0, Y0 + PH, MUTED, 1.0)

d.line(X0, py(100), X0 + PW, py(100), BAD, 1.0, "5 5")
d.t(X0 + PW, py(100) - 8, "전 CPU 100%", 12, BAD, KR, "end")

d.o.append(f'<polyline points="{px(0):.1f},{py(0):.1f} {px(1000):.1f},{py(util(1000)):.1f}" fill="none" stroke="{INFO}" stroke-width="1.8"/>')
d.o.append(f'<polyline points="{px(1000):.1f},{py(util(1000)):.1f} {px(LIMIT):.1f},{py(100):.1f}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-dasharray="6 5"/>')
d.o.append(f'<circle cx="{px(1000):.1f}" cy="{py(40):.1f}" r="5" fill="{INFO}"/>')
d.o.append(f'<circle cx="{px(LIMIT):.1f}" cy="{py(100):.1f}" r="5" fill="{ACC}"/>')
d.t(px(1000) + 12, py(40) + 22, "측정 · 1,000 req/s · 40%", 13, INFO, KR, "start", 600)
d.t(px(LIMIT) - 12, py(100) - 12, f"외삽 · {LIMIT:,.0f} req/s", 13, ACC, KR, "end", 600)
d.line(px(LIMIT), py(100), px(LIMIT), Y0 + PH, ACC, 0.8, "3 4")

d.legend(Y0 + PH + 60, [("측정한 점", INFO), ("외삽", ACC), ("자원 한계", BAD)])
d.save("02-03.resource-limit-extrapolation.svg")
