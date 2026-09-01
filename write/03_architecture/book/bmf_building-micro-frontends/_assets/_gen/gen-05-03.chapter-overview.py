# 05-03 전체 지도 — CDN 이 1 단계 URL 로 각 조각 애플리케이션에 요청을 보낸다 (원문 Figure 5-2).
# 경로와 조각 이름은 저자가 든 예 그대로다. 조합 계층이 없다는 점이 이 방식의 요점이다.
# 타입 스펙: type-deployment — 환경 경계 안에 무엇이 놓이고 그 사이로 무엇이 오가는가.
#           축약: 원문이 버전이나 레플리카 수를 적지 않으므로 artifact chip 의 버전 태그 자리에 캐시 정책을 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1280
Z_X, Z_W = 40, 1200
EDGE_Y, EDGE_H = 104, 96
APP_Y, APP_H = 250, 176
LEGEND_Y = APP_Y + APP_H + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-03",
      "CDN 이 1 단계 URL 로 갈라 보낸다",
      "조합 계층이 없다. 요청이 경로 첫 조각만 보고 곧바로 그 도메인의 애플리케이션에 닿는다. 색이 붙은 상자가 그 판단을 내리는 유일한 자리다.",
      "점선 상자가 배치 경계이고 그 안이 실제로 도는 것입니다")

for label, y, h in (("EDGE", EDGE_Y, EDGE_H), ("INDEPENDENT APPLICATIONS · 팀마다 따로 배포한다", APP_Y, APP_H)):
    d.o.append(f'<rect x="{Z_X}" y="{y}" width="{Z_W}" height="{h}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{Z_X + 14}" y="{y - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(Z_X + 20, y + 4, label, 8, SOFT, MONO, "start")

# 엣지 — 유일한 판단 지점
d.tone(400, EDGE_Y + 14, 480, 68, ACC, 6, "12", 1.4)
tag = "CDN"
tw = len(tag) * 6.2 + 12
d.o.append(f'<rect x="412" y="{EDGE_Y + 24}" width="{tw}" height="16" rx="2" fill="{PAPER}" stroke="{ACC}" stroke-width="0.8"/>')
d.t(412 + tw / 2, EDGE_Y + 36, tag, 8, ACC, MONO)
d.t(412 + tw + 14, EDGE_Y + 36, "경로 첫 조각으로 보낸다", 13, ACC, KR, "start", 600)
d.t(412, EDGE_Y + 60, "엣지 컴퓨트로 재작성해도 된다 · 마이그레이션 규칙을 여기 가둔다", 9.5, MUTED, KR, "start")

apps = [
    ("/", "홈 페이지", "동적 데이터가 있어 짧게 캐시"),
    ("/catalog", "카탈로그", "동적 데이터가 있어 짧게 캐시"),
    ("/check-out", "체크아웃", "개인화가 많아 캐시를 우회하기도"),
]
AW = 372
for i, (path, name, cache) in enumerate(apps):
    x = 64 + i * (AW + 24)
    d.box(x, APP_Y + 30, AW, 116, PAPER2, RULE, 1.0, 6)
    tg = "APP"
    tw2 = len(tg) * 6.2 + 12
    d.o.append(f'<rect x="{x + 14}" y="{APP_Y + 42}" width="{tw2}" height="16" rx="2" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(x + 14 + tw2 / 2, APP_Y + 54, tg, 8, SOFT, MONO)
    d.t(x + 14 + tw2 + 14, APP_Y + 54, name, 12.5, INK, KR, "start", 600)
    d.o.append(f'<rect x="{x + 14}" y="{APP_Y + 70}" width="{AW - 28}" height="24" rx="4" '
               f'fill="{INK}0A" stroke="{MUTED}" stroke-width="0.8"/>')
    d.t(x + 26, APP_Y + 86, path, 10.5, INK, MONO, "start")
    d.t(x + AW - 26, APP_Y + 86, cache, 9, MUTED, KR, "end")
    d.t(x + 14, APP_Y + 118, "하나가 죽어도 나머지는 그대로 뜬다", 9.5, MUTED, KR, "start")
    d.arrow([(640, EDGE_Y + 82), (640, APP_Y + 8), (x + AW / 2, APP_Y + 8), (x + AW / 2, APP_Y + 30)], INFO, "info", 1.4)

d.legend(LEGEND_Y, [("라우팅 판단이 일어나는 유일한 자리", ACC), ("경로별 라우팅", INFO)])
d.save("05-03.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", 64 + 2 * (AW + 24) + AW)
