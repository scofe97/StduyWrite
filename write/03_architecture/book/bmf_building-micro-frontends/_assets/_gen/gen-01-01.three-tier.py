# 01-01 §1 — 원문 Figure 1-1 의 3계층 모놀리스.
# 본문이 "그 끝에 남는 그림이 3계층 구조입니다 — 표현·애플리케이션·영속"을 결론으로 삼는다.
# 타입 스펙: type-layers — 계층을 위에서 아래로 쌓고, 층마다 이 단계에서 고른 결정을 오른쪽에 적는다.
#           focal 은 PRESENTATION 한 층에만 — 이 층이 1장 뒤쪽에서 통짜로 남는 자리다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1092, 428
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-01 §1",
      "3계층 모놀리스 — 신생 프로젝트가 남기는 그림",
      "원문 Figure 1-1. 표현·애플리케이션·영속 세 계층이 각각 하나이고, 아티팩트와 파이프라인도 하나다.",
      "층마다 오른쪽이 이 단계에서 실제로 고르는 결정입니다. 아래 셋을 하나의 배포 단위가 덮습니다")

LX, LW, LH, L0, STRIDE = 88, 824, 68, 112, 84      # 높이 68 · 폭 824 (스펙 56–72 / 800–880)

layers = [
    ("PRESENTATION", "표현 계층 — 프론트엔드",
     "JS 프레임워크 · SSR/SPA · 코드 컨벤션 · 린팅 · CSS 규칙", True),
    ("APPLICATION", "애플리케이션 계층 — API 층",
     "단일 코드베이스 · 파이프라인 하나 · 옆으로 늘려 확장", False),
    ("PERSISTENCE", "영속 계층 — 데이터베이스",
     "graph / NoSQL / SQL 중 사업에 맞는 하나", False),
]

for i, (tag, name, note, focal) in enumerate(layers):
    y = L0 + i * STRIDE
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(LX + 20, y + 26, tag, 9, ACC if focal else SOFT, MONO, "start")
    d.t(LX + 20, y + 48, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 20, y + 42, note, 10, MUTED, KR, "end")

# 왼쪽 여백의 방향 지시자 — 스펙이 요구하는 위치(스택 밖)
ARR_X, TOP, BOT = 56, L0 + 8, L0 + 2 * STRIDE + LH - 8
d.arrow([(ARR_X, BOT), (ARR_X, TOP)], SOFT, "soft", 1.2)
d.o.append(f'<text x="{ARR_X - 8}" y="{(TOP + BOT) / 2}" text-anchor="middle" '
           f'font-family="{MONO}" font-size="9" fill="{SOFT}" '
           f'transform="rotate(-90 {ARR_X - 8} {(TOP + BOT) / 2})">abstraction ^</text>')

# 하나의 배포 단위임을 오른쪽 대괄호로 — 이 편의 논지가 "층이 셋이어도 단위는 하나"다
BR_X, BR_W = LX + LW + 16, 10
d.path(f"M {BR_X} {TOP} L {BR_X + BR_W} {TOP} L {BR_X + BR_W} {BOT} L {BR_X} {BOT}", MUTED, 1.2)
d.line(BR_X + BR_W, (TOP + BOT) / 2, BR_X + BR_W + 6, (TOP + BOT) / 2, MUTED, 1.2)
BR_CY = (TOP + BOT) / 2
for k, seg in enumerate(("아티팩트 하나", "파이프라인 하나")):
    d.t(BR_X + BR_W + 12, BR_CY - 4 + k * 18, seg, 11, MUTED, KR, "start")

d.legend(384, [("1장 뒤쪽에서 통짜로 남는 층", ACC)])
d.save("01-01.three-tier.svg")
print("h 필요:", 384 + 22 + 16, " 실제:", H, " 하단끝:", BOT, "/", H)
