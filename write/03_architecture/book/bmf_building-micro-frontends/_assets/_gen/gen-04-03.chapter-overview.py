# 04-03 전체 지도 — 이 편이 다루는 조각 셋을 같은 축으로 세운다.
# 분할 방식과 React 버전과 라우팅은 저자가 각 조각의 설정과 서술에서 밝힌 것만 옮겼다.
# 타입 스펙: type-dp-security-matrix — 행(조각) × 열(분할 방식 · React · 라우팅)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 232, 12, 244, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 44, 48
ROW0 = HEADER_Y + 68
roles = [("분할 방식", "split"), ("React 버전", "shareScope"), ("라우팅", "routing")]
rows = [
    ("홈 조각", "HomeMFE", ["수직 분할", "17.0.2 · react17 스코프", "셸이 준 1 단계 경로만"], False),
    ("카탈로그 조각", "Catalog", ["수직 분할", "기본 스코프", "지역 라우팅을 스스로 짠다"], False),
    ("계정 관리 조각", "MyAccountMFE", ["수평 분할 · 메타 셸", "18.2.0 · 기본 스코프", "리모트 둘을 스스로 로드"], True),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-03",
      "세 조각이 서로 다른 이유",
      "같은 프로젝트 안에서도 조각마다 분할 방식과 라이브러리 버전과 라우팅이 갈린다. 색이 붙은 행이 호스트이면서 동시에 리모트인 조각이다.",
      "행이 조각이고 열이 그 조각을 가르는 축입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "조각", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 가르는 축", 9, MUTED, KR)
for j, (ko, en) in enumerate(roles):
    x = role_x(j)
    d.o.append(f'<rect x="{x}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(x + ROLE_W / 2, HEADER_Y + 24, ko, 11, PAPER, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, en, 9, PAPER, MONO, "middle", 400, "0.85")

for i, (name, hint, cells, focal) in enumerate(rows):
    y = ROW0 + i * ROW_STRIDE
    d.box(LEFT_PAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LEFT_PAD + 14, y + 20, name, 12, INK, KR, "start", 600)
    d.t(LEFT_PAD + 14, y + 35, hint, 8.5, MUTED, MONO, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 26, val, 10, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 26, val, 10, MUTED, KR)

d.legend(LEGEND_Y, [("호스트이면서 리모트인 조각", ACC)])
d.save("04-03.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
