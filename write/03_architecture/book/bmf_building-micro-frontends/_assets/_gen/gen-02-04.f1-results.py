# 02-04 §2 — Formula 1 이 마이그레이션 뒤 보고한 수치 넷. 이 장에서 수치가 남은 유일한 사례다.
# 네 막대의 방향이 서로 다르다(증가 · 감소 · 점수 개선)는 점을 축 라벨과 막대 아래에 명시한다.
# 타입 스펙: type-bar — 범주별 수치 비교. 막대 넷, 눈금 다섯, focal 하나.
#           축약: 플롯 상단을 스펙의 40 이 아니라 110 으로 내렸다. 스펙 좌표는 머리글 줄이 없는 캔버스를 전제한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 520
PLOT_TOP, BASE_Y, AXIS_X = 110, 420, 80
d = D(W, H, "BUILDING MICRO-FRONTENDS · 02-04 §2",
      "Formula 1 이 보고한 네 수치",
      "모놀리식 프론트엔드에서 마이크로 프론트엔드로 옮긴 뒤 F1 디지털 기술 팀이 보고한 값. 막대마다 좋아진 방향이 다르므로 아래 라벨을 함께 읽는다.",
      "막대 높이는 변화폭이고, 방향은 막대 아래에 적었습니다")

bars = [
    ("구독 · 가입", "증가", 34, True),
    ("플랫폼 비용", "감소", 26, False),
    ("Lighthouse 웹", "점수 개선", 30, False),
    ("Lighthouse 모바일 웹", "점수 개선", 56, False),
]
VMAX, PITCH, BAR_W = 60, 180, 100
X0 = AXIS_X + (W - AXIS_X - 40 - len(bars) * PITCH) / 2

def y_of(v): return BASE_Y - (v / VMAX) * (BASE_Y - PLOT_TOP)

for g in range(0, VMAX + 1, 15):
    y = y_of(g)
    d.line(AXIS_X, y, W - 40, y, RULE, 0.8)
    d.t(AXIS_X - 8, y + 3, f"{g}%", 8, MUTED, MONO, "end")
d.line(AXIS_X, PLOT_TOP, AXIS_X, BASE_Y, RULE, 1.0)
d.line(AXIS_X, BASE_Y, W - 40, BASE_Y, MUTED, 1.0)

for i, (name, direction, v, focal) in enumerate(bars):
    cx = X0 + i * PITCH + PITCH / 2
    x, y = cx - BAR_W / 2, y_of(v)
    h = BASE_Y - y
    c = ACC if focal else MUTED
    d.o.append(f'<rect x="{x}" y="{y}" width="{BAR_W}" height="{h}" rx="3" fill="{c}{"1F" if focal else "26"}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y - 8, f"{v}%", 8, c, MONO)
    d.t(cx, BASE_Y + 22, name, 11, INK, KR, "middle", 600)
    d.t(cx, BASE_Y + 40, direction, 9, MUTED, KR)

d.legend(478, [("팀이 목표로 삼았던 결과", ACC)])
d.save("02-04.f1-results.svg")
print("h 필요:", 478 + 40, " 실제:", H)
