# 03-04 §6 — 인증 토큰을 어디에 두는가. 저자가 든 선택지와 각각에 붙인 제약만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(저장 위치) × 열(누가 읽나 · 도메인 제약 · 대가)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다. 나머지 상수는 공식 그대로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 208, 12, 244, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 40, 44
ROW0 = HEADER_Y + 68
roles = [("누가 읽나", "reader"), ("도메인 제약", "scope"), ("대가", "cost")]
rows = [
    ("localStorage", "브라우저 영속 저장소", ["조각이 각자 꺼내 쓴다", "같은 서브도메인이어야 한다", "규약으로만 강제된다"], False),
    ("sessionStorage", "탭 단위 저장소", ["조각이 각자 꺼내 쓴다", "같은 서브도메인이어야 한다", "탭을 닫으면 사라진다"], False),
    ("쿠키", "domain 속성 사용", ["조각이 각자 꺼내 쓴다", ".mysite.com 으로 하위 도메인 공유", "요청마다 실려 나간다"], False),
    ("앱 셸 미들웨어", "요청을 가로채 헤더 추가", ["조각은 토큰을 모른다", "셸이 붙이므로 제약이 없다", "토큰이 필요 없는 API 는 예외 처리"], True),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-04 §6",
      "토큰을 어디에 두는가",
      "수평 분할에서는 한 뷰의 여러 조각이 같은 토큰을 필요로 한다. 색이 붙은 행이 조각에게서 토큰을 아예 걷어내는 선택지다.",
      "행이 저장 위치이고 열이 그 선택에 따라오는 제약입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "저장 위치", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 따라오는 제약", 9, MUTED, KR)
for j, (ko, en) in enumerate(roles):
    x = role_x(j)
    d.o.append(f'<rect x="{x}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(x + ROLE_W / 2, HEADER_Y + 24, ko, 11, PAPER, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, en, 9, PAPER, MONO, "middle", 400, "0.85")

for i, (name, hint, cells, focal) in enumerate(rows):
    y = ROW0 + i * ROW_STRIDE
    d.box(LEFT_PAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LEFT_PAD + 14, y + 18, name, 11.5, INK, KR, "start", 600)
    d.t(LEFT_PAD + 14, y + 32, hint, 8.5, MUTED, KR, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 24, val, 10, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 24, val, 10, MUTED, KR)

d.legend(LEGEND_Y, [("조각에서 토큰을 걷어내는 선택지", ACC)])
d.save("03-04.token-storage.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
