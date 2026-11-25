# 05-01 §4 미러된 요청은 응답을 버린다.
# 본문 근거: 05-01 §4 ("webapp 의 Istio 프록시가 실요청을 v1 로 보내고 그 응답을 돌려주는 동시에, 복제본을 v2 로 보내고 v2 의 응답은 무시").
# 값 근거: ch05.txt §5.4 (lines 1223, 1239) — v1 Host: catalog.istioinaction:80, v2 Host: catalog.istioinaction-shadow:80.
# 타입 스펙: type-architecture — 구성요소(webapp · 사이드카 · catalog v1 · catalog v2)와 연결. 존 하나(catalog 서비스), 초점 1(미러 경로).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 468
d = D(W, H, "ISTIO IN ACTION · 05-01 §4",
      "미러된 요청은 응답을 버린다",
      "webapp 의 사이드카가 실요청을 catalog v1 로 보내고 응답을 돌려준다. 같은 요청의 복제본을 catalog v2 로 fire-and-forget 으로 보내며 v2 의 응답은 무시한다. 복제본의 Host 에는 -shadow 가 붙는다.",
      "v2 는 실제 트래픽을 받되 실사용자 응답에는 영향이 없습니다. 쓰기 부작용은 앱이 -shadow 로 막습니다")

def node(x, y, w, h, title, subs, focal=False, mono=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, y + 26, title, 14, ACC if focal else INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w / 2, y + 50 + i * 20, s, 11 if mono else 13, MUTED, MONO if mono else KR)

# 존 — catalog 서비스(두 subset)
d.o.append(f'<rect x="612" y="108" width="324" height="284" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
d.o.append(f'<rect x="624" y="100" width="236" height="16" rx="2" fill="{PAPER}"/>')
d.t(742, 113, "catalog · DestinationRule subset", 13, SOFT, KR)

WA = (28, 200, 152, 72)     # webapp
SC = (232, 176, 208, 120)   # webapp 사이드카(Istio 프록시)
V1 = (636, 148, 280, 72)    # catalog v1
V2 = (636, 292, 280, 72)    # catalog v2

# 화살표 먼저
d.path("M 180 236 H 230", MUTED, 1.2, m="ar")                       # webapp → 사이드카
d.path("M 440 208 H 634", MUTED, 1.2, m="ar")                       # 실요청 → v1
d.t(526, 196, "실요청 100%", 13, MUTED, KR)
d.path("M 634 232 H 442", MUTED, 1.2, m="ar", dash="4 3")           # v1 응답 ←
d.t(526, 252, "v1 응답", 13, MUTED, KR)
d.path("M 230 256 H 182", MUTED, 1.2, m="ar", dash="4 3")          # 사이드카 → webapp 응답
d.t(206, 276, "응답", 12, MUTED, KR)
d.path("M 440 268 H 532 Q 540 268 540 276 V 320 Q 540 328 548 328 H 634", ACC, 1.4, m="acc")   # 복제본 → v2
d.t(528, 312, "복제본 · fire-and-forget", 13, ACC, KR, "end")
d.path("M 634 352 H 584", SOFT, 1.0, m="soft", dash="2 4")          # v2 응답 — 존 경계 밖으로 빼서 겹침 방지
d.t(576, 376, "응답은 무시", 13, SOFT, KR, "end")

node(*WA, "webapp", ["요청을 보낸 앱"])
node(*SC, "Istio 프록시", ["webapp 사이드카", "VirtualService mirror:"], mono=False)
node(*V1, "catalog v1", ["Host: catalog.istioinaction:80"], mono=True)
node(*V2, "catalog v2", ["Host: catalog.istioinaction-shadow:80"], focal=True, mono=True)

d.legend(412, [("미러 경로 — 응답이 버려진다", ACC), ("실요청과 응답", MUTED)])
d.save("05-01.mirroring.svg")
