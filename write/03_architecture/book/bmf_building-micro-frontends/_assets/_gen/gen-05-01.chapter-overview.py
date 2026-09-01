# 05-01 전체 지도 — 서버에서 렌더한 조각을 합치는 다섯 방식. 저자가 조합 접근으로 나열한 것만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(조합 방식) × 열(무엇인가 · 맞는 자리 · 조심할 것)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 244, 12, 272, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 48, 52
ROW0 = HEADER_Y + 68
roles = [("무엇인가", "what"), ("맞는 자리", "fit"), ("조심할 것", "caveat")]
rows = [
    ("HTML 조각", "transclusion", ["백엔드가 HTML 덩어리를 돌려준다", "굵은 분할 · 여러 언어를 쓰는 팀", "조각과 팀이 늘면 관리가 어려워진다"], True),
    ("프레임워크 기능", "Next.js · Astro", ["멀티 존 · 서버 아일랜드", "이미 그 프레임워크를 쓰는 팀", "프레임워크마다 규약이 다르다"], False),
    ("웹 컴포넌트 + shadow root", "declarative shadow DOM", ["섀도 DOM 으로 스타일과 로직 격리", "여러 프레임워크가 섞인 곳", "2023 년 이후 브라우저를 전제한다"], False),
    ("Module Federation", "runtime composition", ["런타임에 코드와 의존성을 공유", "독립 빌드 · 독립 배포가 중요할 때", "양방향 공유로 미끄러지기 쉽다"], False),
    ("수직 분할 + 독립 인프라", "first-level URL", ["1 단계 URL 마다 별개 애플리케이션", "도메인 경계가 뚜렷한 조직", "런타임 조합의 세밀함을 포기한다"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-01",
      "서버에서 조각을 합치는 다섯 방식",
      "조합을 어떻게 할지가 이 장의 핵심 결정이다. 색이 붙은 행이 다음 편에서 코드까지 따라가는 고전적 방식이다.",
      "행이 조합 방식이고 열이 그 방식을 가르는 축입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "조합 방식", 11, INK, KR, "middle", 600)
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
    d.t(LEFT_PAD + 14, y + 37, hint, 8.5, MUTED, MONO, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 28, val, 10, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 28, val, 10, MUTED, KR)

d.legend(LEGEND_Y, [("다음 편에서 코드까지 따라가는 방식", ACC)])
d.save("05-01.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
