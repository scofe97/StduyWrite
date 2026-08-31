# 02-02 §5 — 저자가 준 경계 점검 네 항목을 두 축으로 세운다.
# 축은 저자의 문장에서 그대로 나온다 — "노출하는 API 표면을 줄여라"(넓이)와
# "마이크로 프론트엔드는 컴포넌트보다 거칠다 · 세밀한 것을 피하라"(입도).
# 타입 스펙: type-quadrant — consultant special 변형. 두 축이 범위를 잡고 칸마다 이름 붙은 상태가 온다.
#           칸 안 위치는 뜻이 없으므로 점을 찍지 않는다(표준 변형이 아니라 시나리오 변형인 이유).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 704
CX, CY = 620, 360
CW_, CH_, GAPX = 280, 160, 48
d = D(W, H, "BUILDING MICRO-FRONTENDS · 02-02 §5",
      "경계가 잘 그어졌는지 재는 두 축",
      "노출하는 API 표면의 넓이와 조각의 입도로 네 자리를 가른다. 색이 붙은 칸이 저자가 권하는 자리다.",
      "가로가 컨테이너에 노출하는 계약의 넓이, 세로가 조각의 입도입니다")

cells = [
    # (x, y, 태그, 제목, 설명 줄들, focal)
    (CX - GAPX - CW_, CY - GAPX - CH_, "01 · NARROW / COARSE", "잘 그어진 경계",
     ["세션 토큰이나 제품 ID 정도만 받는다", "도메인 하나를 통째로 소유한다"], True),
    (CX + GAPX, CY - GAPX - CH_, "02 · WIDE / COARSE", "컨테이너가 문맥을 쥔다",
     ["속성을 많이 노출해 소유권이 넘어간다", "배포마다 팀 사이 조율이 붙는다"], False),
    (CX - GAPX - CW_, CY + GAPX, "03 · NARROW / FINE", "컴포넌트에 가깝다",
     ["계약은 좁지만 너무 잘다", "뷰마다 조각이 늘고 중첩이 깊어진다"], False),
    (CX + GAPX, CY + GAPX, "04 · WIDE / FINE", "가장 나쁜 자리",
     ["결합이 늘고 외부 의존이 쌓인다", "컨텍스트가 컨테이너로 새어 나간다"], False),
]

# 축 먼저 — 양끝 화살표, 칸 사이를 지난다
TOP, BOT = CY - GAPX - CH_ - 40, CY + GAPX + CH_ + 40
LEFT, RIGHT = CX - GAPX - CW_ - 40, CX + GAPX + CW_ + 40
d.path(f"M {LEFT} {CY} H {RIGHT}", INK, 1.2)
d.path(f"M {CX} {TOP} V {BOT}", INK, 1.2)
for pts in [((LEFT + 12, CY), (LEFT, CY)), ((RIGHT - 12, CY), (RIGHT, CY)),
            ((CX, TOP + 12), (CX, TOP)), ((CX, BOT - 12), (CX, BOT))]:
    d.arrow([pts[0], pts[1]], INK, "ar", 1.2)
d.t(LEFT - 12, CY + 4, "NARROW", 9, INK, MONO, "end")
d.t(RIGHT + 12, CY + 4, "WIDE", 9, INK, MONO, "start")
d.t(CX, TOP - 12, "COARSE", 9, INK, MONO)
d.t(CX, BOT + 20, "FINE", 9, INK, MONO)

for x, y, tag, title, lines, focal in cells:
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW_}" height="{CH_}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.2"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW_}" height="{CH_}" rx="8" fill="{INK}0A" stroke="{MUTED}47" stroke-width="1.0"/>')
    d.t(x + 20, y + 28, tag, 8, ACC if focal else MUTED, MONO, "start", 600)
    d.t(x + 20, y + 60, title, 16, ACC if focal else INK, KR, "start", 600)
    for i, ln in enumerate(lines):
        d.t(x + 20, y + 92 + i * 22, ln, 11, MUTED, KR, "start")

d.legend(BOT + 56, [("저자가 권하는 자리", ACC), ("피해야 할 자리", MUTED)])
d.save("02-02.boundary-test.svg")
print("h 필요:", BOT + 56 + 40, " 실제:", H)
