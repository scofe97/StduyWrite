# 02-03 §2 — 같은 α 에서 β 가 곡선을 꺾는 모습.
# 타입 스펙: type-line — 확장 차원 N 에 대한 상대 용량 C(N) 두 계열.
#           원서 2.6.3·2.6.4 의 식으로 계산한 값. 파라미터 α = 0.05, β = 0.001 은 설명용으로 고른 값이다(원서 값 아님).
#           Amdahl 은 1/α = 20 을 향해 평평해지고, USL 은 정점 뒤 내려간다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 928, 512
X0, Y0, PW, PH = 96, 120, 736, 280
NMAX, YMAX = 64, 24
A, B = 0.05, 0.001

def amdahl(n): return n / (1 + A * (n - 1))
def usl(n): return n / (1 + A * (n - 1) + B * n * (n - 1))
def px(n): return X0 + PW * n / NMAX
def py(v): return Y0 + PH - PH * v / YMAX

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03 §2",
       "β 하나가 평평함을 하강으로 바꾼다",
       "같은 직렬성 α = 0.05 에서 일관성 β 를 0(Amdahl)과 0.001(USL)로 두고 상대 용량 C(N)을 계산해 그렸다. 파라미터는 설명용 값이다.",
       "α = 0.05 · β = 0.001 — 설명용 값으로 계산")

for v in (0, 8, 16, 24):
    d.line(X0, py(v), X0 + PW, py(v), RULE, 0.8)
    d.t(X0 - 12, py(v) + 4, str(v), 12, SOFT, MONO, "end")
for n in (1, 16, 32, 48, 64):
    d.t(px(n), Y0 + PH + 22, str(n), 12, SOFT, MONO, "middle")
d.t(X0 + PW, Y0 + PH + 44, "확장 차원 N →", 12, SOFT, KR, "end")
d.t(X0 - 12, Y0 - 14, "C(N)", 12, SOFT, MONO, "end")
d.line(X0, Y0, X0, Y0 + PH, MUTED, 1.0)

d.line(px(1), py(1), px(YMAX), py(YMAX), RULE, 1.0, "3 4")
d.t(px(YMAX) + 8, py(YMAX) + 16, "선형", 12, SOFT, KR, "start")
d.line(X0, py(1 / A), X0 + PW, py(1 / A), MUTED, 0.8, "4 4")
d.t(X0 + PW, py(1 / A) - 8, "1/α = 20", 12, MUTED, MONO, "end")

for f, c, sw in ((amdahl, INFO, 1.6), (usl, ACC, 2.0)):
    pts = " ".join(f"{px(n):.1f},{py(f(n)):.1f}" for n in range(1, NMAX + 1))
    d.o.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')
npk = max(range(1, NMAX + 1), key=usl)
d.o.append(f'<circle cx="{px(npk):.1f}" cy="{py(usl(npk)):.1f}" r="4" fill="{ACC}"/>')
d.t(px(npk), py(usl(npk)) - 14, f"정점 N = {npk}", 12, ACC, KR, "middle", 600)
d.t(px(60), py(amdahl(60)) - 12, "Amdahl · β = 0", 13, INFO, KR, "end", 600)
d.t(px(60), py(usl(60)) + 22, "USL · β = 0.001", 13, ACC, KR, "end", 600)

d.legend(Y0 + PH + 60, [("Amdahl", INFO), ("USL", ACC)])
d.save("02-03.amdahl-vs-usl.svg")
