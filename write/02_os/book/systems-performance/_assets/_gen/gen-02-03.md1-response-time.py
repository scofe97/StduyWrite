# 02-03 §3 — M/D/1 평균 응답 시간, 서비스 시간 1ms.
# 타입 스펙: type-line — 사용률에 대한 응답 시간 한 계열.
#           원서 p.55 의 식 r = s(2 − ρ) / (2(1 − ρ)) 와 R 코드 범위(0~10ms)를 따른다.
#           표시점: 60% → 1.75, 66.7% → 2.0, 80% → 3.0 (식으로 계산).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, WARN, RULE, KR, MONO

W, H = 928, 512
X0, Y0, PW, PH = 96, 120, 736, 280
YMAX = 10
S = 1.0

def r(u): return S * (2 - u) / (2 * (1 - u))
def px(u): return X0 + PW * u
def py(v): return Y0 + PH - PH * v / YMAX

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03 §3",
       "사용률이 오르면 응답 시간이 가팔라진다",
       "M/D/1 식으로 서비스 시간 1ms 인 디스크의 평균 응답 시간을 사용률 0~95% 에서 계산했다. 점 셋은 60%·66.7%·80% 의 계산값이다.",
       "원서 그림 2.19 · r = s(2 − ρ) / (2(1 − ρ))")

for v in (0, 2, 4, 6, 8, 10):
    d.line(X0, py(v), X0 + PW, py(v), RULE, 0.8)
    d.t(X0 - 12, py(v) + 4, f"{v}ms", 12, SOFT, MONO, "end")
for u in (0, 20, 40, 60, 80, 100):
    d.t(px(u / 100), Y0 + PH + 22, f"{u}%", 12, SOFT, MONO, "middle")
d.t(X0 + PW, Y0 + PH + 44, "사용률 ρ →", 12, SOFT, KR, "end")
d.line(X0, Y0, X0, Y0 + PH, MUTED, 1.0)

pts = " ".join(f"{px(k / 1000):.1f},{py(r(k / 1000)):.1f}" for k in range(0, 951, 5))
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{INFO}" stroke-width="1.8" stroke-linejoin="round"/>')

MARKS = [(0.6, "60% · 1.75ms", ACC, "end", -12, -12), (2 / 3, "66.7% · 2.0ms", WARN, "start", 14, 24),
         (0.8, "80% · 3.0ms", WARN, "start", 14, 22)]
for u, lab, c, anc, dx, dy in MARKS:
    d.o.append(f'<circle cx="{px(u):.1f}" cy="{py(r(u)):.1f}" r="4" fill="{c}"/>')
    d.line(px(u), py(r(u)), px(u), Y0 + PH, c, 0.8, "3 4")
    d.t(px(u) + dx, py(r(u)) + dy, lab, 13, c, MONO, anc, 600)
d.t(px(0.6) - 12, py(r(0.6)) + 34, "원서 문장: 60% 를 넘으면 두 배", 12, ACC, KR, "end")

d.legend(Y0 + PH + 60, [("평균 응답 시간", INFO), ("원서 문장과 나란히 둘 값", ACC), ("두 배 · 세 배 지점", WARN)])
d.save("02-03.md1-response-time.svg")
