# 13-03 §1 — 어디서 푸느냐가 어느 Route 를 쓰는지까지 정한다
# 12-02 의 termination/passthrough 도식과 겹치지 않게, 여기서는 '그래서 어느 Route 오브젝트를
# 쓰는가'까지 끌고 간다. listener 프로토콜 이름이 갈리는 이유도 같은 축이다.
# 타입 스펙: type-data-flow.md — 같은 네 단계를 termination 과 passthrough 두 방식으로 지나는 두 벌의 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1220, 662, "KUBERNETES IN ACTION · 13-03",
      "푸는 자리가 Route 종류까지 정한다",
      "게이트웨이가 복호화하면 안의 HTTP 를 이해하므로 HTTPRoute 로 경로까지 가른다. "
      "통과시키면 SNI 호스트명만 남아 TLSRoute 로 호스트만 가른다.",
      "listener 프로토콜 이름이 HTTPS 와 TLS 로 갈리는 이유")

def row(y0, label, proto, gw_sub, route, route_sub, can, c, focal):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1172)
    cy = y0 + 116
    ddx.node(d, 160, cy, "클라이언트", "HTTPS", 200, 84, INFO)
    ddx.node(d, 470, cy, "게이트웨이", gw_sub, 250, 84, focal=focal)
    d.path(f"M 262 {cy} L 342 {cy}", ACC, 1.5, m="acc")
    d.chip(302, cy - 28, proto, SOFT, 9)
    if focal:
        d.o.append(f'<rect x="{760-120}" y="{cy-42}" width="240" height="84" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(640, cy - 42, 240, 84, "#161B22", c, 1.1, 6); tc = c
    d.t(760, cy - 12, route, 13, tc, MONO, "middle", 600)
    d.t(760, cy + 12, route_sub, 11, MUTED, KR)
    d.path(f"M 596 {cy} L 634 {cy}", MUTED, 1.5, m="ar")
    ddx.node(d, 1050, cy, "백엔드", can, 220, 84, c)
    d.path(f"M 882 {cy} L 936 {cy}", MUTED, 1.5, m="ar")

row(100, "termination — listener protocol: HTTPS", "TLS", "복호화한다 — 안이 HTTP 임을 안다",
    "HTTPRoute", "경로 · 헤더까지 가른다", "평문 HTTP 를 받는다", OK, True)
row(340, "passthrough — listener protocol: TLS", "TLS", "복호화하지 않는다",
    "TLSRoute", "SNI 호스트만 가른다", "여기서 종료한다 · E2E", WARN, False)

d.t(24, 596, "HTTPS 와 TLS 라는 이름이 갈리는 것은 게이트웨이가 무엇을 안다고 선언하는가가 다르기 때문이다. "
             "아는 만큼만 가를 수 있다.", 11, MUTED, KR, "start")
d.legend(614, [("클라이언트", INFO), ("안까지 안다", OK), ("호스트만 안다", WARN), ("이 자리에서 갈린다", ACC)])
d.save("13-03-tls-terminate-vs-passthrough.svg")
print("ok")
