# 04-01 전체 지도 — 결정 프레임워크 네 기둥에 이 프로젝트가 실제로 넣은 답.
# 각 칸은 저자가 "the teams have decided to use the following" 아래 적은 넷을 옮긴 것이다.
# 타입 스펙: type-dp-security-matrix — 행(기둥) × 열(선택 · 근거 · 따라오는 것)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 216, 12, 268, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 44, 48
ROW0 = HEADER_Y + 68
roles = [("이 프로젝트의 선택", "choice"), ("왜 그렇게 정했나", "why"), ("따라오는 것", "consequence")]
rows = [
    ("식별", "identify", ["하이브리드 · 서브도메인마다", "한 팀이 통째로 가질 수 있나로 갈랐다", "계정 관리만 수평 분할"], True),
    ("조합", "compose", ["클라이언트 사이드", "팀 역량에 맞고 확장 여지가 있다", "앱 셸이 런타임에 로드한다"], False),
    ("라우팅", "route", ["클라이언트 사이드", "조합을 정하면 자동으로 따라온다", "전역은 셸 · 지역은 조각"], False),
    ("통신", "communicate", ["이벤트 이미터", "조각이 늘어도 팀을 독립으로 둔다", "이벤트와 페이로드를 미리 정의"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-01",
      "네 기둥에 이 프로젝트가 넣은 답",
      "2 장의 결정 프레임워크를 실제 이커머스에 적용한 결과다. 색이 붙은 행이 저자가 통짜로 고르지 않고 서브도메인마다 갈랐다고 밝힌 자리다.",
      "행이 결정해야 할 기둥이고 열이 그 결정의 앞뒤입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "결정 프레임워크", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 이 프로젝트", 9, MUTED, KR)
for j, (ko, en) in enumerate(roles):
    x = role_x(j)
    d.o.append(f'<rect x="{x}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(x + ROLE_W / 2, HEADER_Y + 24, ko, 11, PAPER, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, en, 9, PAPER, MONO, "middle", 400, "0.85")

for i, (name, hint, cells, focal) in enumerate(rows):
    y = ROW0 + i * ROW_STRIDE
    d.box(LEFT_PAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LEFT_PAD + 14, y + 20, name, 12.5, INK, KR, "start", 600)
    d.t(LEFT_PAD + 14, y + 35, hint, 8.5, MUTED, MONO, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 26, val, 10, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 26, val, 10, MUTED, KR)

d.legend(LEGEND_Y, [("통짜로 고르지 않은 기둥", ACC)])
d.save("04-01.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
