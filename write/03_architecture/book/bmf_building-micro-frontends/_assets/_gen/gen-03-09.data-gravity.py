# 03-09 §3 — 엣지에서 렌더해도 성능이 나아지지 않는 이유 (저자의 시드니-뉴욕 예).
# 왕복 수치는 원문이 적은 200~250ms 그대로다. 지어낸 숫자를 넣지 않는다.
# 타입 스펙: type-architecture — 지리 경계로 묶은 구성요소와 그 사이 연결. accent 는 성능을 결정하는 긴 경로 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1200
ZY, ZH = 128, 176
Z1_X, Z1_W = 40, 500
Z2_X, Z2_W = 660, 500
LEGEND_Y = ZY + ZH + 88
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-09 §3",
      "엣지가 가까워도 데이터는 멀리 있다",
      "왼쪽 사용자에게 엣지는 가깝지만, 렌더에 필요한 데이터는 오른쪽 리전에 있다. 색이 붙은 긴 경로가 응답 시간을 결정한다.",
      "데이터 중력 — 애플리케이션은 데이터가 있는 곳으로 끌린다")

for x, w, label in ((Z1_X, Z1_W, "SYDNEY · EDGE LOCATION"), (Z2_X, Z2_W, "US-EAST-1 · PRIMARY REGION")):
    d.o.append(f'<rect x="{x}" y="{ZY}" width="{w}" height="{ZH}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{x + 14}" y="{ZY - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(x + 20, ZY + 4, label, 8, SOFT, MONO, "start")

d.box(Z1_X + 28, ZY + 30, Z1_W - 56, 56, PAPER2, RULE, 1.0, 6)
d.t(Z1_X + 48, ZY + 54, "엣지 컴퓨트", 13, INK, KR, "start", 600)
d.t(Z1_X + 48, ZY + 74, "여기서 서버 사이드 렌더를 시도한다", 10, MUTED, KR, "start")
d.box(Z1_X + 28, ZY + 100, Z1_W - 56, 48, f"{INK}08", MUTED, 0.8, 6)
d.t(Z1_X + 48, ZY + 130, "시드니의 사용자 — 엣지까지는 가깝다", 10.5, MUTED, KR, "start")

d.box(Z2_X + 28, ZY + 30, Z2_W - 56, 56, PAPER2, RULE, 1.0, 6)
d.t(Z2_X + 48, ZY + 54, "API 와 데이터베이스", 13, INK, KR, "start", 600)
d.t(Z2_X + 48, ZY + 74, "본사가 뉴욕이라 여기에 둔다", 10, MUTED, KR, "start")
d.box(Z2_X + 28, ZY + 100, Z2_W - 56, 48, f"{INK}08", MUTED, 0.8, 6)
d.t(Z2_X + 48, ZY + 130, "대부분의 조직이 한두 리전에서 운영한다", 10.5, MUTED, KR, "start")

MID = ZY + 58
d.arrow([(Z1_X + Z1_W - 28, MID), (Z2_X + 28, MID)], ACC, "acc", 1.6)
d.o.append(f'<rect x="{(Z1_X + Z1_W + Z2_X) / 2 - 58}" y="{MID - 26}" width="116" height="18" rx="2" fill="{PAPER}"/>')
d.t((Z1_X + Z1_W + Z2_X) / 2, MID - 13, "RTT 200~250ms", 9.5, ACC, MONO)

d.t(W / 2, ZY + ZH + 42, "엣지가 사용자에 더 가까워도 데이터를 가지러 가는 시간이 그대로라서 개선이 거의 없거나 아예 없다", 11, MUTED, KR)
d.legend(LEGEND_Y, [("응답 시간을 결정하는 경로", ACC)])
d.save("03-09.data-gravity.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
