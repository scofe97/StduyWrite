# 03-02 §5 — 클라이언트에서 조각을 잇는 다섯 기법. 저자가 각 기법에 붙인 서술만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(기법) × 열(무엇으로 · 브라우저 · 눈에 띄는 점)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 148 에서 236 으로 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다. 나머지 상수는 공식 그대로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 208, 12, 236, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 36, 40
ROW0 = HEADER_Y + 68
roles = [("무엇으로 로드하나", "loader"), ("브라우저", "support"), ("눈에 띄는 점", "note")]
rows = [
    ("ES modules", "표준 모듈", ["type=module · import map", "모던 브라우저 네이티브", "표준만으로 런타임 조합"], False),
    ("SystemJS", "모듈 로더", ["import map 유사 문법", "로더가 파편화를 흡수", "네이티브 미지원 브라우저까지"], False),
    ("Module Federation", "Webpack 5 도입", ["모듈처럼 임포트", "2.0 부터 번들러 중립", "같은 라이브러리 다른 버전 공존"], True),
    ("Native Federation", "Angular 팀 권장", ["import maps", "웹 표준 기반", "Module Federation 에서 영감"], False),
    ("HTML parsing", "Qiankun 이 사용", ["DOMParser · adoptNode", "표준 DOM API", "script 는 새로 만들어야 평가됨"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-02 §5",
      "조각을 잇는 다섯 기법",
      "수직 분할은 클라이언트에서만 조합하므로 브라우저 표준이 허용하는 범위 안에서 고른다. 색이 붙은 행이 저자가 가장 매끄럽다고 적은 기법이다.",
      "행이 기법이고 열이 그 기법을 가르는 축입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "조합 기법", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 가르는 축", 9, MUTED, KR)
for j, (ko, en) in enumerate(roles):
    x = role_x(j)
    d.o.append(f'<rect x="{x}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(x + ROLE_W / 2, HEADER_Y + 24, ko, 11, PAPER, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, en, 9, PAPER, MONO, "middle", 400, "0.85")

for i, (name, hint, cells, focal) in enumerate(rows):
    y = ROW0 + i * ROW_STRIDE
    d.box(LEFT_PAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LEFT_PAD + 14, y + 16, name, 11.5, INK, KR, "start", 600)
    d.t(LEFT_PAD + 14, y + 30, hint, 8.5, MUTED, KR, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 22, val, 10.5, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 22, val, 10.5, MUTED, KR)

d.legend(LEGEND_Y, [("저자가 가장 매끄럽다고 적은 기법", ACC)])
d.save("03-02.composition-techniques.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
