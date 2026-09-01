# 03-08 전체 지도 — 서버 사이드 조합의 세 계층 (원문 Figure 3-21).
# 계층 이름과 각 계층의 설명은 저자의 목록 그대로다. 컴포저에 accent 를 주는 것은 모든 요청이 지나는 단일 지점이기 때문이다.
# 타입 스펙: type-deployment — 환경 경계 안에 무엇이 놓이고 그 사이로 무엇이 오가는가.
#           축약: 원문이 버전이나 레플리카 수를 적지 않으므로 artifact chip 의 버전 태그 자리에 구현 수단을 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1200
Z_X, Z_W = 40, 1120
ZONES = [("EDGE", 104, 118), ("ORIGIN", 246, 152), ("MICRO-FRONTENDS", 432, 124)]
LEGEND_Y = 432 + 124 + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-08",
      "서버 사이드 조합의 세 계층",
      "위에서 아래로 요청이 내려가고 조립된 HTML 이 올라온다. 색이 붙은 컴포저가 모든 요청이 지나는 단일 지점이다.",
      "점선 상자가 배치 경계이고 그 안이 실제로 도는 것입니다")

def zone(y, h, label):
    d.o.append(f'<rect x="{Z_X}" y="{y}" width="{Z_W}" height="{h}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{Z_X + 14}" y="{y - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(Z_X + 20, y + 4, label, 8, SOFT, MONO, "start")

for label, y, h in ZONES:
    zone(y, h, label)

def node(x, y, w, h, tag, name, sub, chips, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    tw = len(tag) * 6.2 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y + 10}" width="{tw}" height="16" rx="2" '
               f'fill="{PAPER}" stroke="{ACC if focal else RULE}" stroke-width="0.8"/>')
    d.t(x + 12 + tw / 2, y + 22, tag, 8, ACC if focal else SOFT, MONO)
    d.t(x + 12 + tw + 14, y + 22, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 12, y + 44, sub, 10, MUTED, KR, "start")
    for i, (cn, cv) in enumerate(chips):
        cy = y + 56 + i * 28
        d.o.append(f'<rect x="{x + 12}" y="{cy}" width="{w - 24}" height="24" rx="4" '
                   f'fill="{INK}0A" stroke="{MUTED}" stroke-width="0.8"/>')
        d.t(x + 24, cy + 16, cn, 10.5, INK, KR, "start")
        d.t(x + w - 24, cy + 16, cv, 9, MUTED, MONO, "end")

node(72, 118, 520, 90, "CDN", "엣지 캐시", "몇 분만 캐시해도 오리진 트래픽이 크게 준다",
     [("캐시된 페이지", "shorter round trip")])
node(72, 260, 520, 124, "POD", "컴포저", "모든 조각을 모아 최종 뷰를 만든다",
     [("server-side includes", "NGINX · HTTPd"), ("커스텀 조합 로직", "Kubernetes")], focal=True)
node(72, 446, 520, 96, "STATIC", "정적 자산으로 배포된 조각", "자동화 파이프라인이 컴파일 시점에 준비한다",
     [("빌드 산출물", "compile time")])
node(640, 446, 520, 96, "APP", "동적 자산으로 서빙되는 조각", "요청마다 템플릿과 데이터를 준비한다",
     [("템플릿 + 데이터", "per request")])

# 경계를 넘는 경로는 link 색, 안에 머무는 경로는 muted
d.arrow([(332, 208), (332, 260)], INFO, "info", 1.4)
d.t(346, 238, "HTTPS:443", 8.5, INFO, MONO, "start")
d.arrow([(300, 384), (300, 446)], INFO, "info", 1.4)
d.t(314, 420, "fetch", 8.5, INFO, MONO, "start")
d.arrow([(400, 384), (400, 414), (900, 414), (900, 446)], INFO, "info", 1.4)
d.t(660, 406, "fetch", 8.5, INFO, MONO, "start")

d.legend(LEGEND_Y, [("모든 요청이 지나는 단일 지점", ACC), ("경계를 넘는 경로", INFO)])
d.save("03-08.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
