# 02-03 §1~§2 — 조합을 어디서 하느냐가 라우팅과 적합한 분할과 확장 부담을 함께 정한다.
# 셀 값은 전부 원문 서술에서 나온다. 지어낸 판정은 넣지 않는다.
# 타입 스펙: type-dp-security-matrix — 행(조합 위치) × 열(따라오는 결정)의 격자.
#           축약: 권한 등급(full/rw/read/none) 대신 서술 값을 쓰고, 열 폭을 148 에서 236 으로 넓혔다.
#           한글 서술 값이 148px 에 안 들어가기 때문이며 나머지 상수(행 높이 36 · stride 40 · 헤더 52)는 공식 그대로다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 208, 12, 236, 16, 48
# 스펙의 header_y=72 는 리드 줄이 없는 캔버스를 전제한다. 리드(y=74)를 쓰므로 28 내린다.
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 36, 40
ROW0 = HEADER_Y + 68
roles = [("라우팅 위치", "routing"), ("적합한 분할", "split"), ("확장 부담", "scalability")]
rows = [
    ("클라이언트 사이드", "app shell 이 CDN 에서 조각을 가져온다",
     ["클라이언트", "수평 · 수직 모두", "없음"], True),
    ("엣지 사이드", "CDN 이 ESI 로 화면을 조립한다",
     ["엣지 · URL 기준", "주로 수평", "없음 · 고급 라우팅 불가"], False),
    ("서버 사이드", "오리진이 화면을 조립한다",
     ["오리진", "주로 수평", "버스트 트래픽에 취약"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 02-03 §1~§2",
      "어디서 합치느냐가 나머지를 정한다",
      "조합 위치 셋과 그에 따라오는 라우팅 위치·적합한 분할·확장 부담. 저자가 주로 권하는 것은 클라이언트와 서버 사이드다.",
      "행이 조합 위치이고 열이 그 선택에 따라오는 것들입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "조합 위치", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 따라오는 결정", 9, MUTED, KR)
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
        if focal and j == 0:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 22, val, 11, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 22, val, 11, MUTED, KR)

d.legend(LEGEND_Y, [("저자가 기본으로 권하는 조합", ACC)])
d.save("02-03.composition-matrix.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
