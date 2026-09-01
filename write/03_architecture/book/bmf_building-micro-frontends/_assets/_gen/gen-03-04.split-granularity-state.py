# 03-04 §1 — 분할의 입도가 어떤 방아쇠로 옮겨 다니는가.
# 상태 이름과 전이 문구는 저자의 서술에서만 옮긴다 — "굵게 시작해 진화하면서 다듬어라",
# "한 뷰에 6~7 개를 넘으면 리모트 컴포넌트를 만들고 있는 것", "합쳐야 하니 리팩토링하라".
# 타입 스펙: type-state — 유한한 상태와 그 사이 전이. accent 는 독자가 알아채야 할 상태(여기서는 잘못된 상태) 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
SW, SH, SY = 240, 68, 176
XS = (90, 470, 850)          # 왼쪽 좌표
MY = SY + SH / 2             # 214
BACK_Y = SY + SH + 84        # 되돌아오는 전이의 수평 구간
LEGEND_Y = BACK_Y + 56
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-04 §1",
      "분할의 입도는 방아쇠를 만나 옮겨 간다",
      "저자는 굵게 시작해 다듬으라고 말한다. 색이 붙은 상태가 너무 멀리 갔다는 신호가 켜진 자리다.",
      "화살표 위 글이 그 전이를 일으키는 방아쇠입니다")

states = [
    ("굵은 분할", "책임을 높은 수준에서 나눈다", False),
    ("다듬어진 분할", "애플리케이션이 자라며 경계를 조정한다", False),
    ("과분할", "조각이 아니라 리모트 컴포넌트다", True),
]

# 시작점
d.o.append(f'<circle cx="36" cy="{MY}" r="6" fill="{INK}"/>')
d.arrow([(44, MY), (XS[0] - 2, MY)], MUTED, "ar", 1.4)

# 전이 — 노드보다 먼저 그린다
d.arrow([(XS[0] + SW, MY), (XS[1] - 2, MY)], MUTED, "ar", 1.4)
d.t((XS[0] + SW + XS[1]) / 2, MY - 12, "팀 인지 부하가 커진다", 10, MUTED, KR)
d.arrow([(XS[1] + SW, MY), (XS[2] - 2, MY)], MUTED, "ar", 1.4)
d.t((XS[1] + SW + XS[2]) / 2, MY - 26, "한 뷰에 6~7 개 초과", 10, MUTED, KR)
d.t((XS[1] + SW + XS[2]) / 2, MY - 10, "여럿이 같은 API 를 부른다", 10, MUTED, KR)
d.path(f"M {XS[2] + SW / 2} {SY + SH} V {BACK_Y} H {XS[1] + SW / 2} V {SY + SH + 2}",
       ACC, 1.5, m="acc")
d.t((XS[1] + XS[2]) / 2 + SW / 2, BACK_Y + 20, "합쳐서 되돌린다 · 초기에 리팩토링하는 편이 훨씬 싸다", 10.5, ACC, KR)

for x, (name, sub, focal) in zip(XS, states):
    if focal:
        d.tone(x, SY, SW, SH, ACC, 8, "14", 1.4)
        d.t(x + SW / 2, SY + 28, name, 14, ACC, KR, "middle", 600)
        d.t(x + SW / 2, SY + 48, sub, 9.5, ACC, KR)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 8)
        d.t(x + SW / 2, SY + 28, name, 14, INK, KR, "middle", 600)
        d.t(x + SW / 2, SY + 48, sub, 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("너무 멀리 갔다는 신호가 켜진 상태", ACC)])
d.save("03-04.split-granularity-state.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
