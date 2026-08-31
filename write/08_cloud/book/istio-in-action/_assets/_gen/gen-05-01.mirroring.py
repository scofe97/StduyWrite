# 05-01 §4 미러된 요청은 응답을 버린다.
# 본문: "webapp 의 Istio 프록시가 실요청을 v1 로 보내고 그 응답을 돌려주는 동시에, 복제본을 v2 로 보내고 v2 의 응답은
# 무시한다. 색이 붙은 선이 그 복제본." 로그: v2 쪽 Host 는 catalog.istioinaction-shadow:80.
# 타입 스펙: type-architecture — 구성요소(webapp · 사이드카 · catalog v1 · catalog v2)와 연결. 존 하나(catalog 서비스), 초점 1(미러 경로).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 468
d = D(W, H, "ISTIO IN ACTION · 05-01 §4",
      "미러된 요청은 응답을 버린다",
      "webapp 의 사이드카가 실요청을 catalog v1 로 보내고 응답을 돌려준다. 같은 요청의 복제본을 catalog v2 로 fire-and-forget 으로 보내며 v2 의 응답은 무시한다. 복제본의 Host 에는 -shadow 가 붙는다.",
      "실사용자는 v1 의 응답만 봅니다. v2 는 실제 트래픽을 받되 아무에게도 영향을 주지 않습니다")

def node(x, y, w, h, title, subs, focal=False, mono=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, y + 26, title, 14, ACC if focal else INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w / 2, y + 48 + i * 18, s, 11 if mono else 12, MUTED, MONO if mono else KR)

# 존 — catalog 서비스(두 subset)
d.o.append(f'<rect x="596" y="108" width="380" height="280" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
d.o.append(f'<rect x="608" y="112" width="300" height="18" rx="2" fill="{PAPER}"/>')
d.t(758, 129, "catalog · DestinationRule subset", 12, SOFT, KR)

WA = (40, 200, 160, 72)     # webapp
SC = (260, 176, 220, 120)   # webapp 사이드카(Istio 프록시)
V1 = (640, 148, 300, 72)    # catalog v1
V2 = (640, 292, 300, 72)    # catalog v2

# 화살표 먼저
d.path(f"M 200 236 H 258", MUTED, 1.2, m="ar")                       # webapp → 사이드카
d.path(f"M 480 208 H 638", MUTED, 1.2, m="ar")                       # 실요청 → v1
d.t(540, 198, "실요청 100%", 12, MUTED, KR)
d.path(f"M 638 232 H 482", MUTED, 1.2, m="ar", dash="4 3")           # v1 응답 ← 
d.t(540, 250, "응답 → 사용자", 12, MUTED, KR)
d.path(f"M 480 268 H 552 Q 560 268 560 276 V 320 Q 560 328 568 328 H 638", ACC, 1.4, m="acc")   # 복제본 → v2
d.t(548, 312, "복제본 · fire-and-forget", 12, ACC, KR, "end")
d.path(f"M 638 352 H 600", SOFT, 1.0, m="soft", dash="2 4")          # v2 응답 — 버려짐
d.t(596, 372, "응답은 무시", 12, SOFT, KR, "end")

node(*WA, "webapp", ["요청을 보낸 앱"])
node(*SC, "Istio 프록시", ["webapp 사이드카", "VirtualService mirror:"], mono=False)
node(*V1, "catalog v1", ["Host: catalog.istioinaction:80"], mono=True)
node(*V2, "catalog v2", ["Host: catalog.istioinaction-shadow:80"], focal=True, mono=True)

d.legend(412, [("미러 경로 — 응답이 버려진다", ACC), ("실요청과 응답", MUTED)])
d.save("05-01.mirroring.svg")
