# 03-07 §5 — 3장이 든 격리 수단 셋이 무엇을 어떻게 가르는가. 각 칸은 원문 서술에서만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(격리 수단) × 열(무엇을 격리하나)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 216, 12, 232, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 40, 44
ROW0 = HEADER_Y + 68
roles = [("CSS", "style"), ("자바스크립트", "script"), ("의존성 공유", "sharing")]
rows = [
    ("iframe", "별도 HTML 문서", ["문서가 달라 완전히 갈린다", "실행 컨텍스트가 갈린다", "빌드 시점에만 공유"], False),
    ("웹 컴포넌트", "같은 DOM 트리", ["섀도 DOM 으로 스코프", "전역 window 를 함께 쓴다", "버전이 갈리면 충돌"], False),
    ("Web Fragments", "같은 DOM 트리", ["섀도 DOM 으로 스코프", "숨겨진 iframe 안에서 실행", "네트워크 수준에서 공유"], True),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-07 §5",
      "무엇을 어디까지 격리하는가",
      "3장이 든 격리 수단 셋을 같은 축으로 세운다. 색이 붙은 행이 CloudFlare 가 2025 년에 내놓은 접근이다.",
      "행이 수단이고 열이 그 수단이 가르는 것입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "격리 수단", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 가르는 것", 9, MUTED, KR)
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

d.legend(LEGEND_Y, [("두 겹으로 감싸는 새 접근", ACC)])
d.save("03-07.isolation-matrix.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
