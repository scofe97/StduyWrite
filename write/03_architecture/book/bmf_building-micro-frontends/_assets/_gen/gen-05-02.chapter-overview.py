# 05-02 전체 지도 — HTML 조각 방식의 전경 (원문 Figure 5-1).
# 팀마다 다른 언어를 쓴다는 저자의 예(JavaScript · Python · .NET)를 그대로 옮긴다.
# 타입 스펙: type-architecture — 신뢰 경계(엣지 / 오리진 / 업스트림)로 묶은 구성요소와 그 사이 연결.
#           accent 는 모든 요청이 지나면서도 비즈니스를 모르는 단 하나의 상자.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1240
Z_X, Z_W = 40, 1160
ZONES = [("EDGE", 104, 92), ("ORIGIN", 238, 188), ("UPSTREAM SERVICES · 팀마다 다른 언어", 468, 116)]
LEGEND_Y = 468 + 116 + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-02",
      "UI 컴포저가 조각을 꿰맨다",
      "요청은 CDN 에서 출발해 컴포저에 닿고, 컴포저가 업스트림에서 HTML 조각을 받아 템플릿에 끼운다. 색이 붙은 상자는 비즈니스 로직을 모른다.",
      "위에서 아래로 요청이 내려가고 조립된 HTML 이 올라옵니다")

for label, y, h in ZONES:
    d.o.append(f'<rect x="{Z_X}" y="{y}" width="{Z_W}" height="{h}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{Z_X + 14}" y="{y - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(Z_X + 20, y + 4, label, 8, SOFT, MONO, "start")

def node(x, y, w, h, name, sub, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + 18, y + 26, name, 12.5, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 46, sub, 9.5, MUTED, KR, "start")

node(420, 118, 400, 64, "CDN", "캐싱과 보안 · 캐시에 있으면 여기서 끝난다")
node(420, 252, 400, 60, "게이트웨이", "동적 조립이 필요한 요청만 넘긴다")
node(360, 336, 520, 76, "UI 컴포저", "템플릿을 로드하고 조각을 끼워 스트리밍한다", focal=True)

langs = [("상품 정보", "JavaScript", 64), ("고객 리뷰", "Python", 456), ("개인화 추천", ".NET", 848)]
for name, lang, x in langs:
    d.box(x, 482, 328, 84, PAPER2, RULE, 1.0, 6)
    d.t(x + 18, 508, name, 12.5, INK, KR, "start", 600)
    d.t(x + 18, 528, lang, 9.5, MUTED, MONO, "start")
    d.t(x + 18, 550, "HTML 조각을 HTTP 로 돌려준다", 9.5, MUTED, KR, "start")

d.arrow([(620, 182), (620, 252)], INFO, "info", 1.4)
d.arrow([(620, 312), (620, 336)], INFO, "info", 1.4)
for x, ax in ((64, 480), (456, 620), (848, 760)):
    cx = x + 164
    d.arrow([(ax, 412), (ax, 446), (cx, 446), (cx, 482)], INFO, "info", 1.4)
d.t(634, 222, "HTTP", 8.5, INFO, MONO, "start")
d.t(620, 440, "병렬 요청 · Promise.allSettled", 8.5, INFO, MONO)

d.legend(LEGEND_Y, [("비즈니스 로직을 모르는 조립 지점", ACC), ("네트워크를 건너는 요청", INFO)])
d.save("05-02.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", 848 + 328)
