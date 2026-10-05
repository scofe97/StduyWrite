# 02-01 §8 — 부하에 따른 처리량(knee)과 응답 시간 악화의 세 모양.
# 타입 스펙: type-line — 부하라는 연속 축 위의 추세. 두 패널을 나란히 둔다.
#           축약: 원서 그림 2.6·2.7(p.13)의 개형만 옮긴다. 값이 없어 축 눈금을 두지 않는다.
#           곡선 식(그리기용): 처리량 y = x − 2(x − 0.45)²₊, 응답 시간은 knee 0.5 뒤 가속.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, WARN, OK, RULE, KR, MONO

W, H = 928, 496
PW, PH, Y0 = 368, 248, 120
PANELS = [(76, "처리량"), (512, "평균 응답 시간")]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-01 §8",
       "knee 를 지나면 처리량은 꺾이고 지연은 오른다",
       "왼쪽은 부하에 따른 처리량, 오른쪽은 같은 부하 축에서 평균 응답 시간이 나빠지는 세 모양이다. 개형만 보이며 축에 값이 없다.",
       "원서 그림 2.6·2.7 의 개형")

def axes(x0, title):
    d.line(x0, Y0, x0, Y0 + PH, MUTED, 1.0)
    d.line(x0, Y0 + PH, x0 + PW, Y0 + PH, MUTED, 1.0)
    d.t(x0, Y0 - 12, title, 13, INK, KR, "start", 600)
    d.t(x0 + PW, Y0 + PH + 24, "부하 →", 12, SOFT, KR, "end")

def poly(x0, f, c, sw):
    pts = []
    for i in range(0, 101):          # 그림 영역 위로 나가면 거기서 선을 멈춘다(평평하게 자르지 않는다)
        x = i / 100
        y = max(f(x), 0)
        if y > 1: break
        pts.append(f"{x0 + PW * x:.1f},{Y0 + PH - PH * y:.1f}")
    d.o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linejoin="round"/>')

KNEE = 0.45
for x0, title in PANELS:
    axes(x0, title)
    kx = x0 + PW * KNEE
    d.line(kx, Y0 + 8, kx, Y0 + PH, SOFT, 1.0, "4 4")
    d.t(kx + 6, Y0 + PH - 10, "knee", 12, SOFT, MONO, "start")

# 왼쪽 — 처리량
x0 = PANELS[0][0]
poly(x0, lambda x: x if x < KNEE else x - 2.0 * (x - KNEE) ** 2, ACC, 2.0)
d.t(x0 + PW * 0.18, Y0 + PH - PH * 0.30, "선형", 13, MUTED, KR, "middle")
d.t(x0 + PW * 0.70, Y0 + PH - PH * 0.62, "경합 · 정점", 13, ACC, KR, "middle", 600)
d.t(x0 + PW * 0.94, Y0 + PH - PH * 0.30, "감소", 13, ACC, KR, "end", 600)

# 오른쪽 — 응답 시간 세 모양
x0 = PANELS[1][0]
base = lambda x: 0.12 + 0.18 * x
poly(x0, base, OK, 1.4)
poly(x0, lambda x: base(x) + 1.1 * max(0, x - 0.5) ** 2, INFO, 1.4)
poly(x0, lambda x: base(x) + 9.0 * max(0, x - 0.5) ** 2, WARN, 1.8)
d.t(x0 + PW - 4, Y0 + PH - PH * 0.30 + 22, "선형 · 503 반환", 12, OK, KR, "end")
d.t(x0 + PW - 4, Y0 + PH - PH * 0.575 - 14, "느린 악화 · CPU", 12, INFO, KR, "end")
d.t(x0 + PW * 0.82, Y0 + 20, "빠른 악화", 12, WARN, KR, "start", 600)
d.t(x0 + PW * 0.82, Y0 + 38, "메모리 · 디스크", 12, WARN, KR, "start")

d.legend(Y0 + PH + 44, [("처리량", ACC), ("빠른 악화", WARN), ("느린 악화", INFO), ("에러 반환", OK)])
d.save("02-01.scalability-degradation.svg")
