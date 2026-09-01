# 05-03 §3 — F1 이 보고한 "Latest F1 News" 페이지의 시간 지표 전후. 저자가 초 단위로 적은 값 그대로다.
# 사업 지표(구독 34% · 비용 26% · Lighthouse 점수)는 02-04 의 막대 도식에 이미 있으므로 여기서는 시간만 다룬다.
# 타입 스펙: type-bar — 범주별 수치 비교. 눈금 다섯, focal 하나.
#           축약: 스펙의 막대 넷은 단일 계열 기준이고 여기서는 전 · 후 두 계열이라 범주마다 막대를 쌍으로 놓는다.
#                플롯 상단을 스펙의 40 이 아니라 118 로 내렸다(머리글 줄이 있는 캔버스).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1180, 560
PLOT_TOP, BASE_Y, AXIS_X = 118, 420, 96
VMAX = 10
d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-03 §3",
      "F1 이 보고한 시간 지표의 전후",
      "모놀리스에서 조각으로 옮긴 뒤 Latest F1 News 페이지에서 잰 값이다. 색이 붙은 쌍이 가장 크게 줄어든 지표다.",
      "왼쪽이 옮기기 전, 오른쪽이 옮긴 뒤입니다. 단위는 초이고 낮을수록 좋습니다")

bars = [
    ("FCP", "데스크톱", 2.0, 0.8, False),
    ("Speed Index", "데스크톱", 4.3, 3.0, False),
    ("LCP", "모바일", 8.7, 3.2, True),
    ("Speed Index", "모바일", 7.3, 5.2, False),
]
PITCH, BAR_W, GAP = 248, 76, 16
X0 = AXIS_X + (W - AXIS_X - 40 - len(bars) * PITCH) / 2

def y_of(v): return BASE_Y - (v / VMAX) * (BASE_Y - PLOT_TOP)

for g in range(0, VMAX + 1, 2):
    y = y_of(g)
    d.line(AXIS_X, y, W - 40, y, RULE, 0.8)
    d.t(AXIS_X - 8, y + 3, f"{g}s", 8, MUTED, MONO, "end")
d.line(AXIS_X, PLOT_TOP, AXIS_X, BASE_Y, RULE, 1.0)
d.line(AXIS_X, BASE_Y, W - 40, BASE_Y, MUTED, 1.0)

for i, (name, device, before, after, focal) in enumerate(bars):
    cx = X0 + i * PITCH + PITCH / 2
    c = ACC if focal else MUTED
    for k, (v, lab) in enumerate(((before, "전"), (after, "후"))):
        x = cx - BAR_W - GAP / 2 + k * (BAR_W + GAP)
        y = y_of(v)
        op = "1F" if focal else "26"
        fill = f"{c}{op}" if k == 1 else f"{c}0F"
        d.o.append(f'<rect x="{x}" y="{y}" width="{BAR_W}" height="{BASE_Y - y}" rx="3" '
                   f'fill="{fill}" stroke="{c}" stroke-width="1.1"{"" if k == 1 else " stroke-dasharray=\'4 3\'"}/>')
        d.t(x + BAR_W / 2, y - 8, f"{v}", 8.5, c, MONO)
        d.t(x + BAR_W / 2, BASE_Y + 18, lab, 8.5, SOFT, KR)
    d.t(cx, BASE_Y + 40, name, 11.5, INK, KR, "middle", 600)
    d.t(cx, BASE_Y + 58, device, 9, MUTED, KR)

d.legend(496, [("가장 크게 줄어든 지표", ACC), ("나머지 지표", MUTED)])
d.save("05-03.f1-timings.svg")
print("h 필요:", 496 + 40, " 실제:", H)
