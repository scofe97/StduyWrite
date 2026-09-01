# 05-04 §5 — 존 사이에 무엇을 어디로 넘길 것인가. 저자가 데이터 성격별로 나눈 대로 옮긴다.
# 쿠키 속성 셋(HttpOnly · Secure · SameSite)은 원문이 든 값 그대로다.
# 타입 스펙: type-dp-security-matrix — 행(데이터 성격) × 열(어디에 두나 · 왜 · 주의)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 236, 12, 264, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 48, 52
ROW0 = HEADER_Y + 68
roles = [("어디에 두나", "where"), ("왜", "why"), ("주의", "caveat")]
rows = [
    ("일시적 · 가벼운 것", "검색어 · 상품 ID · 프로모 코드", ["쿼리 스트링", "한 번 넘기고 버리면 되는 값", "URL 에 드러난다"], False),
    ("탭 안에서만 쓰는 것", "세션 스토리지", ["같은 서브도메인 안", "브라우저가 알아서 지운다", "다른 서브도메인은 못 본다"], False),
    ("지속적이거나 민감한 것", "장바구니 수 · 사용자 선호", ["백엔드 저장소와 API", "어느 존에서도 같은 값이어야 한다", "존마다 따로 두면 어긋난다"], False),
    ("인증 토큰", "JWT", ["HttpOnly 쿠키", "요청 헤더에 자동으로 실린다", "web storage 에는 절대 두지 않는다"], True),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 52
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-04 §5",
      "존 사이에 무엇을 어디로 넘기나",
      "존이 독립 애플리케이션이라 데이터마다 넘기는 길이 다르다. 색이 붙은 행이 저자가 저장 위치를 못 박은 자리다.",
      "행이 데이터의 성격이고 열이 그에 따른 결정입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "데이터의 성격", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 따라오는 결정", 9, MUTED, KR)
for j, (ko, en) in enumerate(roles):
    x = role_x(j)
    d.o.append(f'<rect x="{x}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(x + ROLE_W / 2, HEADER_Y + 24, ko, 11, PAPER, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, en, 9, PAPER, MONO, "middle", 400, "0.85")

for i, (name, hint, cells, focal) in enumerate(rows):
    y = ROW0 + i * ROW_STRIDE
    d.box(LEFT_PAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LEFT_PAD + 14, y + 22, name, 11.5, INK, KR, "start", 600)
    d.t(LEFT_PAD + 14, y + 38, hint, 8.5, MUTED, KR, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        last = (focal and j == len(cells) - 1)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 28, val, 10, WARN if last else ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 28, val, 10, MUTED, KR)

# 쿠키 속성 셋 — 표 아래 각주 띠
d.box(LEFT_PAD, rows_bottom + 8, W - LEFT_PAD - RIGHT_PAD + 36, 0.1, PAPER2, RULE, 0)
d.t(LEFT_PAD + 14, rows_bottom + 22, "쿠키에 반드시 걸 속성 셋", 10, INK, KR, "start", 600)
d.t(LEFT_PAD + 190, rows_bottom + 22, "HttpOnly (XSS) · Secure (HTTPS 만) · SameSite=Lax 또는 Strict (CSRF)", 10, MUTED, MONO, "start")

d.legend(LEGEND_Y, [("저장 위치를 못 박은 행", ACC), ("저자가 금지한 자리", WARN)])
d.save("05-04.data-placement.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
