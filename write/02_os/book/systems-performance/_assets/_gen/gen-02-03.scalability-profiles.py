# 02-03 §1 — 확장성 프로파일 다섯을 같은 축 모양으로 나란히.
# 타입 스펙: type-line — 확장 차원(x)에 대한 성능(y) 추세. 작은 그림 다섯 장.
#           원서 그림 2.16(p.50)의 개형만 옮긴다. 축에 값이 없다.
#           그리기용 식(가로 0~1 을 N = 0~20 으로, 세로는 C(N)/20 — 어느 곡선도 선형 기준선 위로 가지 않는다):
#           경합 = Amdahl α 0.08, 일관성 = USL α 0.02·β 0.004, knee = 0.5 뒤 기울기 0.25, 천장 = 0.6 에서 평평.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 928, 400
X0, PW, PH, STRIDE, Y0 = 32, 148, 148, 180, 132

def amdahl(n, a): return n / (1 + a * (n - 1))
def usl(n, a, b): return n / (1 + a * (n - 1) + b * n * (n - 1))
N = 20
PROFILES = [
    ("선형", lambda x: x),
    ("경합", lambda x: amdahl(x * N, 0.08) / N),
    ("일관성", lambda x: usl(x * N, 0.02, 0.004) / N),
    ("knee point", lambda x: x if x < 0.5 else 0.5 + 0.25 * (x - 0.5)),
    ("확장성 천장", lambda x: min(x, 0.6)),
]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03 §1",
       "모델 없이도 모양으로 가린다",
       "가로축은 확장 차원(코어·스레드·부하), 세로축은 결과 성능이다. 다섯 프로파일의 개형을 같은 크기 그림에 나란히 놓았다.",
       "원서 그림 2.16 의 개형 · 축에 값 없음")

for i, (name, f) in enumerate(PROFILES):
    x0 = X0 + i * STRIDE
    d.line(x0, Y0, x0, Y0 + PH, MUTED, 1.0)
    d.line(x0, Y0 + PH, x0 + PW, Y0 + PH, MUTED, 1.0)
    d.line(x0, Y0 + PH, x0 + PW, Y0, RULE, 0.8, "3 4")          # 선형 기준선
    pts = " ".join(f"{x0 + PW * k / 100:.1f},{Y0 + PH - PH * min(f(k / 100), 1):.1f}" for k in range(101))
    focal = name == "일관성"
    c = ACC if focal else INFO
    d.o.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{2.0 if focal else 1.6}" stroke-linejoin="round"/>')
    d.t(x0 + PW / 2, Y0 + PH + 28, name, 13, ACC if focal else INK, KR, "middle", 600)

d.t(X0, Y0 + PH + 52, "점선 = 선형 기준", 12, SOFT, KR, "start")
d.legend(Y0 + PH + 72, [("성능 곡선", INFO), ("유일하게 내려가는 모양", ACC)])
d.save("02-03.scalability-profiles.svg")
