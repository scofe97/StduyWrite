# 13-03 §3 — 허가는 반대 방향으로 나온다
# 본문이 "위치를 외울 게 아니라 허가하는 사람이 있는 곳으로 이해하라"고 한다. 그러니 참조 화살표와
# 허가 화살표를 반대 방향으로 그려, ReferenceGrant 가 대상 쪽에 서는 이유가 그림에서 나오게 한다.
# 타입 스펙: type-architecture.md — 네임스페이스 둘을 경계로 두고 그 사이를 건너는 연결 둘. 참조는 왼쪽에서 오른쪽으로,
#           허가는 반대 방향으로 난다 — 방향이 반대라는 것이 논지라 간선의 뜻이 서로 다르다.
#           2026-08-28 정정: dependency 는 팬인·순환용이라 여기 해당이 없고, 네임스페이스는 호스트가
#           아니라 deployment 의 존도 아니다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 13-03",
      "허가하는 쪽에 허가서가 선다",
      "참조하는 쪽만으로 결정되면 서비스 소유자의 의사가 빠진다. 그래서 허가 주체가 소유자여야 하고, "
      "그 결과가 오브젝트 위치로 나타난다.",
      "ReferenceGrant 는 참조 대상의 네임스페이스에 만든다")

for x0, ns in ((90, "kiada"), (680, "service-namespace")):
    d.box(x0, 168, 430, 232, PAPER, RULE, 0.9, 8)
    d.t(x0 + 215, 194, f"namespace: {ns}", 11, SOFT, MONO)

ddx.node(d, 305, 250, "HTTPRoute", "backendRefs 에 적는다", 260, 76, INFO)
ddx.node(d, 895, 250, "Service", "남의 팀 것", 260, 76, OK)
d.path("M 438 250 L 758 250", INFO, 1.6, m="info")
d.t(598, 232, "참조 — 왼쪽에서 오른쪽으로", 11, INFO, KR)

d.o.append(f'<rect x="{895-160}" y="322" width="320" height="62" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(895, 348, "ReferenceGrant", 13, ACC, MONO, "middle", 600)
d.t(895, 370, "from: HTTPRoute in kiada  ·  to: Service", 9, MUTED, MONO)
d.path("M 732 353 L 438 353 L 438 292", ACC, 1.6, m="acc")
d.t(598, 336, "허가 — 반대 방향으로 나온다", 11, ACC, KR)

d.t(24, 446, "그래서 위치를 외울 게 아니라 '허가하는 사람이 있는 곳'으로 이해하면 된다. "
             "소유자가 자기 네임스페이스에 허가서를 세운다.", 11, MUTED, KR, "start")
d.t(24, 484, "같은 원칙인데 소유자가 뒤집히는 경우가 Gateway 공유다", 12, SOFT, KR, "start")
d.t(24, 508, "· 진입점의 주인은 Gateway 이므로 허가도 Gateway 쪽 allowedRoutes 에서 낸다", 11, MUTED, KR, "start")
d.t(24, 530, "· 둘 다 '자기 것을 가진 쪽이 허가한다'는 한 규칙이고, 무엇을 소유했는지에 따라 자리만 달라진다",
     11, MUTED, KR, "start")
d.legend(556, [("참조하는 쪽", INFO), ("참조되는 쪽", OK), ("허가서가 서는 자리", ACC)])
d.save("13-03-reference-grant-direction.svg")
print("ok")
