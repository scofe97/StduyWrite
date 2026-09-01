# 05-04 전체 지도 — 저자의 티셔츠 가게 프로젝트가 나눈 세 존. 홈 존이 진입점이자 교통 조정자다.
# 존 이름과 책임은 원문 그대로다. rewrites 는 서버 수준에서 처리되므로 브라우저는 핸드오프를 모른다.
# 타입 스펙: type-architecture — 논리 경계(존)로 묶은 구성요소와 그 사이 연결.
#           accent 는 진입점이자 프록시 노릇을 하는 단 하나의 존.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1280
Z_X, Z_W = 40, 1200
ENTRY_Y, ENTRY_H = 108, 116
ZONE_Y, ZONE_H = 268, 158
LEGEND_Y = ZONE_Y + ZONE_H + 34
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-04",
      "홈 존이 진입점이자 교통 조정자다",
      "세 존이 각자 독립된 Next.js 애플리케이션이지만 사용자에게는 한 도메인이다. 색이 붙은 존이 자기 몫을 처리하면서 나머지도 프록시한다.",
      "화살표는 rewrites 로 투명하게 전달되는 요청입니다")

for label, y, h in (("ENTRY ZONE · 사용자가 닿는 도메인", ENTRY_Y, ENTRY_H),
                    ("REMOTE ZONES · 각자 독립 배포", ZONE_Y, ZONE_H)):
    d.o.append(f'<rect x="{Z_X}" y="{y}" width="{Z_W}" height="{h}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{Z_X + 14}" y="{y - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(Z_X + 20, y + 4, label, 8, SOFT, MONO, "start")

d.tone(360, ENTRY_Y + 22, 560, 78, ACC, 6, "12", 1.4)
d.t(382, ENTRY_Y + 48, "홈 존", 14, ACC, KR, "start", 600)
d.t(382, ENTRY_Y + 70, "랜딩 페이지를 직접 그리고", 10.5, MUTED, KR, "start")
d.t(382, ENTRY_Y + 88, "나머지 경로는 next.config.js 의 rewrites 로 넘긴다", 10.5, MUTED, KR, "start")

zones = [
    ("카탈로그 존", "/catalog/:path*", "상품 목록과 상세 · 핵심 쇼핑 경험", 300),
    ("계정 존", "/account/:path*", "인증과 프로필 · 민감한 작업을 갈라 둔다", 700),
]
for name, path, sub, x in zones:
    d.box(x, ZONE_Y + 34, 380, 104, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, ZONE_Y + 62, name, 13, INK, KR, "start", 600)
    d.o.append(f'<rect x="{x + 20}" y="{ZONE_Y + 74}" width="340" height="24" rx="4" '
               f'fill="{INK}0A" stroke="{MUTED}" stroke-width="0.8"/>')
    d.t(x + 32, ZONE_Y + 90, path, 10, INK, MONO, "start")
    d.t(x + 20, ZONE_Y + 120, sub, 9.5, MUTED, KR, "start")
    d.arrow([(640, ENTRY_Y + 100), (640, ZONE_Y + 12), (x + 190, ZONE_Y + 12), (x + 190, ZONE_Y + 34)],
            INFO, "info", 1.4)

d.o.append(f'<rect x="500" y="{ZONE_Y - 34}" width="280" height="16" fill="{PAPER}"/>')
d.t(640, ZONE_Y - 22, "rewrites · 서버에서 프록시된다", 8.5, INFO, MONO)
d.t(160, ENTRY_Y + 62, "사용자는", 11, MUTED, KR)
d.t(160, ENTRY_Y + 82, "도메인 하나만 본다", 11, MUTED, KR)

d.legend(LEGEND_Y, [("진입점이자 프록시인 존", ACC), ("서버 수준 재작성", INFO)])
d.save("05-04.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", 700 + 380)
