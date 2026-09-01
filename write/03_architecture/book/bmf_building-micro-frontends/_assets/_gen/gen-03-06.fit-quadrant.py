# 03-06 §4 — 저자가 iframe 이 빛난다고 적은 조건 둘을 축으로 세운다.
# 축은 원문 문장에서 그대로 나온다 — "조각 사이에 통신이 많이 필요하지 않을 때"(가로)와
# "샌드박스로 캡슐화를 강제해야 할 때"(세로).
# 타입 스펙: type-quadrant — consultant special 변형. 두 축이 범위를 잡고 칸마다 이름 붙은 상태가 온다.
#           칸 안 위치는 뜻이 없으므로 점을 찍지 않는다(시나리오 변형인 이유).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 704
CX, CY = 620, 360
CW_, CH_, GAPX = 280, 160, 48
d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-06 §4",
      "iframe 이 맞는 자리를 가르는 두 축",
      "조각 사이에 오갈 정보의 양과 격리를 강제해야 하는 정도로 네 자리를 가른다. 색이 붙은 칸이 저자가 iframe 을 권하는 자리다.",
      "가로가 조각 사이 상호작용의 양, 세로가 격리를 강제해야 하는 정도입니다")

cells = [
    (CX - GAPX - CW_, CY - GAPX - CH_, "01 · FEW / HIGH", "iframe 이 빛나는 자리",
     ["인트라넷 대시보드 · 규제 산업 B2B", "레거시를 새 앱 옆에 격리해 둔다"], True),
    (CX + GAPX, CY - GAPX - CH_, "02 · MANY / HIGH", "다른 격리 수단을 본다",
     ["화면을 가로지르는 상호작용은 조율이 어렵다", "정보 공유가 많으면 맞는 접근이 아니다"], False),
    (CX - GAPX - CW_, CY + GAPX, "03 · FEW / LOW", "값을 치를 이유가 없다",
     ["성능 · 접근성 · 색인 불가를 그냥 떠안는다", "더 현대적인 접근이 낫다"], False),
    (CX + GAPX, CY + GAPX, "04 · MANY / LOW", "가장 나쁜 자리",
     ["중첩된 DOM 에 종단 간 테스트가 길어진다", "반응형 레이아웃까지 겹치면 손이 많이 간다"], False),
]

TOP, BOT = CY - GAPX - CH_ - 40, CY + GAPX + CH_ + 40
LEFT, RIGHT = CX - GAPX - CW_ - 40, CX + GAPX + CW_ + 40
d.path(f"M {LEFT} {CY} H {RIGHT}", INK, 1.2)
d.path(f"M {CX} {TOP} V {BOT}", INK, 1.2)
for a, b in [((LEFT + 12, CY), (LEFT, CY)), ((RIGHT - 12, CY), (RIGHT, CY)),
             ((CX, TOP + 12), (CX, TOP)), ((CX, BOT - 12), (CX, BOT))]:
    d.arrow([a, b], INK, "ar", 1.2)
d.t(LEFT - 12, CY + 4, "FEW", 9, INK, MONO, "end")
d.t(RIGHT + 12, CY + 4, "MANY", 9, INK, MONO, "start")
d.t(CX, TOP - 12, "HIGH", 9, INK, MONO)
d.t(CX, BOT + 20, "LOW", 9, INK, MONO)

for x, y, tag, title, lines, focal in cells:
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW_}" height="{CH_}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.2"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW_}" height="{CH_}" rx="8" fill="{INK}0A" stroke="{MUTED}47" stroke-width="1.0"/>')
    d.t(x + 20, y + 28, tag, 8, ACC if focal else MUTED, MONO, "start", 600)
    d.t(x + 20, y + 60, title, 16, ACC if focal else INK, KR, "start", 600)
    for i, ln in enumerate(lines):
        d.t(x + 20, y + 92 + i * 22, ln, 11, MUTED, KR, "start")

d.legend(BOT + 56, [("저자가 iframe 을 권하는 자리", ACC), ("다른 접근을 보는 자리", MUTED)])
d.save("03-06.fit-quadrant.svg")
print("h 필요:", BOT + 56 + 40, " 실제:", H)
