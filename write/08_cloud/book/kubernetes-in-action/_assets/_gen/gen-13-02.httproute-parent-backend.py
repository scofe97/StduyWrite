# 13-02 §1 — 위로 붙고 아래로 보낸다
# HTTPRoute 는 두 방향으로 참조한다는 것이 요점이라, 좌우가 아니라 위아래로 놓아야
# parentRefs 와 backendRefs 의 방향이 이름 그대로 읽힌다.
# 타입 스펙: type-dependency.md — parentRefs 는 위를, backendRefs 는 아래를 가리킨다. 참조의 방향 자체가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1120, 650, "KUBERNETES IN ACTION · 13-02",
      "위로 붙고 아래로 보낸다",
      "HTTPRoute 는 parentRefs 로 게이트웨이에 붙고 backendRefs 로 서비스에 보낸다. 둘 다 배열이라 "
      "게이트웨이 여럿에 붙을 수도, 서비스 여럿으로 나눌 수도 있다.",
      "kiada Gateway 와 kiada Service 를 잇는 가장 단순한 Route")

ddx.node(d, 560, 180, "Gateway  kiada", "플랫폼 팀이 만든 입구", 300, 76, INFO)
d.o.append(f'<rect x="380" y="292" width="360" height="112" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(560, 322, "HTTPRoute  kiada", 13, ACC, MONO, "middle", 600)
d.t(560, 346, "hostnames: kiada.example.com", 10, MUTED, MONO)
d.t(560, 368, "이 호스트로 온 요청만 매칭", 11, MUTED, KR)
ddx.node(d, 560, 500, "Service  kiada", "port: 80", 300, 76, OK)

d.path("M 560 288 L 560 222", ACC, 1.6, m="acc")
d.t(576, 258, "parentRefs — 이 게이트웨이에 붙는다", 11, ACC, KR, "start")
d.path("M 560 408 L 560 458", ACC, 1.6, m="acc")
d.t(576, 438, "backendRefs — 여기로 보낸다", 11, ACC, KR, "start")

d.t(180, 180, "여럿일 수 있다", 11, SOFT, KR)
d.t(180, 500, "여럿일 수 있다", 11, SOFT, KR)
d.line(300, 180, 404, 180, MUTED, 0.8, "3 5")
d.line(300, 500, 404, 500, MUTED, 0.8, "3 5")

d.t(24, 560, "만든 뒤 YAML 을 보면 없던 필드가 기본값으로 채워진다 — parentRefs 에 kind: Gateway, "
             "backendRefs 에 kind: Service·weight: 1, rule 에 모든 요청을 받는 matches 가 붙는다.",
     11, MUTED, KR, "start")
d.t(24, 582, "참조가 특정 kind 로 고정되지 않고 가장 흔한 kind 로 기본값이 잡히는 이 패턴이 Gateway API 를 확장 가능하게 한다.",
     11, MUTED, KR, "start")
d.legend(602, [("붙는 곳·보낼 곳", INFO), ("Route 와 그 참조", ACC)])
d.save("13-02-httproute-parent-backend.svg")
print("ok")
