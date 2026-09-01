# 03-09 §1 — 모던 SSR 프레임워크 넷이 각자 고른 길. 각 칸은 원문 서술에서만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(프레임워크) × 열(무엇으로 나누나 · 자바스크립트를 어떻게 다루나 · 두드러진 점)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 216, 12, 244, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 40, 44
ROW0 = HEADER_Y + 68
roles = [("무엇으로 나누나", "unit"), ("자바스크립트", "javascript"), ("두드러진 점", "note")]
rows = [
    ("Next.js", "풀스택 React", ["멀티 존 · 페이지 그룹", "서버 컴포넌트로 0 에 가깝게", "같은 도메인을 나눠 쓴다"], True),
    ("Astro.js", "콘텐츠 우선", ["서버 아일랜드", "필요한 곳만 하이드레이트", "기본이 자바스크립트 0"], False),
    ("Qwik", "컨테이너", ["컨테이너 단위 독립 배포", "하이드레이션 대신 재개", "상호작용 때만 로드"], False),
    ("htmx", "HTML 확장", ["서버가 돌려준 HTML 조각", "복잡한 번들이 없다", "리버스 프록시로 라우팅"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-09 §1",
      "네 프레임워크가 각자 고른 길",
      "같은 결과를 낼 수 있지만 기본값과 최적화가 다르다. 색이 붙은 행이 저자가 수평 분할에 자연스럽게 맞는다고 든 쪽이다.",
      "행이 프레임워크이고 열이 그 선택을 가르는 축입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "프레임워크", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 가르는 축", 9, MUTED, KR)
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

d.legend(LEGEND_Y, [("수평 분할에 자연스럽게 맞는다고 든 쪽", ACC)])
d.save("03-09.framework-matrix.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
