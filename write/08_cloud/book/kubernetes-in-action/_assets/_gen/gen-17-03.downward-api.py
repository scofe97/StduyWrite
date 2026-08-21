# 17-03 §1 — 노드 IP 를 앱이 어떻게 아는가
# hostPort 를 쓰려면 노드 IP 가 필요한데 그 값은 스케줄 전에는 없다. 08-03 에서 세운 Downward
# API 가 그 자리를 메운다는 것이 요점이라, 값의 출처가 Pod status 임이 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 600, "KUBERNETES IN ACTION · 17-03",
      "노드 IP 는 스케줄된 뒤에야 안다",
      "hostPort 로 부르려면 자기가 뜬 노드의 IP 가 필요하다. 그 값은 파드가 노드에 배정된 뒤에 "
      "status 에 채워지므로, 매니페스트에 미리 적을 수 없다.",
      "08-03 의 Downward API 가 이 자리를 메운다")

ddx.node(d, 190, 300, "Pod status", "hostIP — 스케줄 뒤 채워진다", 280, 88, INFO)
d.o.append(f'<rect x="{600-150}" y="256" width="300" height="88" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(600, 288, "fieldRef", 13, ACC, MONO, "middle", 600)
d.t(600, 312, "status.hostIP", 11, MUTED, MONO)
d.path("M 332 300 L 442 300", ACC, 1.5, m="acc")

ddx.node(d, 1000, 300, "환경변수 NODE_IP", "http://$(NODE_IP):9090", 280, 88, OK)
d.path("M 752 300 L 852 300", OK, 1.5, m="ok")

d.t(600, 400, "앱은 인프라 구조를 알 필요 없이 값만 받는다", 11, SOFT, KR)

d.t(24, 468, "이 조합이 hostPort 방식의 대가다 — Local Service 를 쓰면 이 단계가 통째로 사라지고 "
             "Service 이름 하나로 끝난다.", 11, MUTED, KR, "start")
d.t(24, 490, "그래서 §4 의 판정은 '노드 IP 를 조합할 것인가, 이름으로 부를 것인가'로 좁혀진다.",
     11, MUTED, KR, "start")
d.legend(516, [("값의 출처", INFO), ("주입 방식", ACC), ("앱이 받는 것", OK)])
d.save("17-03-downward-api.svg")
print("ok")
