# 05-05 §2 — 저자가 SSR 조각을 만들 때 알아야 한다고 든 캐시 세 종류. 수치는 원문이 적은 것만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(캐시 종류) × 열(어디에 · 무엇을 담나 · 저자가 든 효과)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 232, 12, 268, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 48, 52
ROW0 = HEADER_Y + 68
roles = [("어디에 두나", "where"), ("무엇을 담나", "what"), ("저자가 든 효과", "effect")]
rows = [
    ("CDN", "첫 방어선", ["세계 각지의 엣지", "정적 자산 · 개인화 없는 HTML · 공용 API 응답", "인기 콘텐츠 요청의 80~90%"], True),
    ("인메모리 캐시", "Redis · cache-aside", ["렌더링 계층 옆", "렌더된 HTML 조각과 API 응답", "1MB HTML 을 5 밀리초에"], False),
    ("웜 캐시", "미리 채워 둔다", ["위 두 곳 어디든", "자주 쓰는 데이터와 비싼 연산 결과", "첫 요청자가 느린 경험을 겪지 않는다"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 50
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-05 §2",
      "알아야 할 캐시 세 종류",
      "5 초짜리 TTL 하나만 걸어도 백엔드 부담이 크게 준다는 것이 이 절의 요지다. 색이 붙은 행이 트래픽 급증의 첫 방어선이다.",
      "행이 캐시 종류이고 열이 그 캐시를 가르는 축입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "캐시 종류", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 가르는 축", 9, MUTED, KR)
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
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 28, val, 9.5, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 28, val, 9.5, MUTED, KR)

d.t(LEFT_PAD + 14, rows_bottom + 24, "TTL 은 콘텐츠 변동성에 맞춘다", 10, INK, KR, "start", 600)
d.t(LEFT_PAD + 240, rows_bottom + 24, "속보 30초 · 스포츠 점수 5~15초 · 아카이브는 며칠", 10, MUTED, MONO, "start")

d.legend(LEGEND_Y, [("트래픽 급증의 첫 방어선", ACC)])
d.save("05-05.cache-types.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
