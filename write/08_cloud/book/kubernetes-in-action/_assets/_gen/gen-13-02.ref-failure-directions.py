# 13-02 §1 — 같은 사건이 양쪽에 다르게 기록된다
# 본문이 "한쪽만 보면 한 문장만 읽게 된다"로 팁의 근거를 댄다. 그러니 두 방향을 좌우가 아니라
# 위아래로 두고, 같은 오타가 Gateway 쪽과 Route 쪽에 어떻게 다르게 남는지를 나란히 보인다.
# 타입 스펙: type-dp-security-matrix.md — 행은 조건 둘, 열은 보는 방향과 False 일 때 reason. 왼쪽 참조 그래프는 그 방향을 읽는 열쇠다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 660, "KUBERNETES IN ACTION · 13-02",
      "조건 둘은 보는 방향이 다르다",
      "존재하지 않는 이름을 적어도 apply 는 성공한다. 스키마가 보는 것은 필드가 있는지와 문자열인지까지이고, "
      "그 이름의 오브젝트가 실제로 있는지는 다른 오브젝트를 조회해야 알 수 있다.",
      "13-01 §2 의 '모양은 강제해도 행동은 못 한다'가 참조에도 적용된다")

ddx.node(d, 300, 180, "Gateway", "부모", 260, 72, INFO)
d.o.append(f'<rect x="170" y="286" width="260" height="88" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(300, 318, "HTTPRoute", 13, ACC, MONO, "middle", 600)
d.t(300, 342, "두 방향으로 참조한다", 11, MUTED, KR)
ddx.node(d, 300, 480, "Service", "백엔드", 260, 72, OK)
d.path("M 300 282 L 300 220", ACC, 1.5, m="acc")
d.path("M 300 378 L 300 440", ACC, 1.5, m="acc")
d.t(316, 256, "parentRefs", 11, ACC, MONO, "start")
d.t(316, 414, "backendRefs", 11, ACC, MONO, "start")

ddx.matrix(
    d, x0=456, hdr_y=180, row_h=96, gap=14, focal_col=1,
    cols=[(200, "조건"), (196, "보는 방향"), (290, "False 일 때 reason")],
    rows=[
        ([("Accepted", "붙었는가"), ("위쪽", "부모 Gateway"),
          ("NoMatchingParent", "NoMatchingListenerHostname")], INFO),
        ([("ResolvedRefs", "보낼 곳이 있는가"), ("아래쪽", "백엔드"),
          ("BackendNotFound", "RefNotPermitted · InvalidKind")], OK),
    ])

d.t(24, 546, "그래서 backendRefs 만 오타를 내면 Accepted: True 인데 ResolvedRefs: False 가 된다 — "
             "부모에는 붙었고 보낼 곳이 없는 상태다.", 11, MUTED, KR, "start")
d.t(24, 568, "같은 사건이 양쪽에 다르게 적힌다. Gateway 쪽은 attachedRoutes: 0 으로 '붙은 게 없다'를, "
             "Route 쪽은 Accepted: False 로 '붙을 곳을 못 찾았다'를 남긴다.", 11, MUTED, KR, "start")
d.legend(596, [("위를 보는 조건", INFO), ("아래를 보는 조건", OK), ("두 방향 참조", ACC)])
d.save("13-02-ref-failure-directions.svg")
print("ok")
