# 03-03 §4 — 저자가 든 500KB 예제. 같은 앱을 SPA 로 낼 때와 수직 분할로 낼 때 사용자가 받는 양.
# 세 막대의 값은 원문 수치 그대로다 — 전체 500(비인증 로직 100 · 인증 로직 150 · 공유 의존성 250).
# 타입 스펙: type-bar — 범주별 수치 비교. 막대 셋, 눈금 다섯, focal 하나.
#           축약: 플롯 상단을 스펙의 40 이 아니라 110 으로 내렸다(리드 줄이 있는 캔버스).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 520
PLOT_TOP, BASE_Y, AXIS_X = 110, 420, 80
d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-03 §4",
      "사용자가 실제로 받는 양",
      "같은 500KB 애플리케이션을 SPA 로 낼 때와 수직 분할로 낼 때. 아끼는 쪽은 랜딩만 보고 떠나는 사용자다.",
      "막대 아래가 그 사용자가 받는 것의 내역입니다")

bars = [
    ("SPA · 모든 사용자", "로직 250 + 공유 250", 500, False),
    ("수직 · 비인증 영역만", "로직 100 미만 + 공유 250", 350, True),
    ("수직 · 인증까지 간 사용자", "앞에서 다 받지는 않는다", 500, False),
]
VMAX, PITCH, BAR_W = 500, 200, 110
X0 = AXIS_X + (W - AXIS_X - 40 - len(bars) * PITCH) / 2

def y_of(v): return BASE_Y - (v / VMAX) * (BASE_Y - PLOT_TOP)

for g in range(0, VMAX + 1, 125):
    y = y_of(g)
    d.line(AXIS_X, y, W - 40, y, RULE, 0.8)
    d.t(AXIS_X - 8, y + 3, f"{g}KB", 8, MUTED, MONO, "end")
d.line(AXIS_X, PLOT_TOP, AXIS_X, BASE_Y, RULE, 1.0)
d.line(AXIS_X, BASE_Y, W - 40, BASE_Y, MUTED, 1.0)

for i, (name, sub, v, focal) in enumerate(bars):
    cx = X0 + i * PITCH + PITCH / 2
    x, y = cx - BAR_W / 2, y_of(v)
    c = ACC if focal else MUTED
    d.o.append(f'<rect x="{x}" y="{y}" width="{BAR_W}" height="{BASE_Y - y}" rx="3" fill="{c}{"1F" if focal else "26"}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y - 8, ("약 " if focal else "") + f"{v}KB", 8, c, MONO)
    d.t(cx, BASE_Y + 22, name, 11, INK, KR, "middle", 600)
    d.t(cx, BASE_Y + 40, sub, 9, MUTED, KR)

d.legend(478, [("수직 분할이 아끼는 자리", ACC)])
d.save("03-03.bundle-math.svg")
print("h 필요:", 478 + 40, " 실제:", H)
