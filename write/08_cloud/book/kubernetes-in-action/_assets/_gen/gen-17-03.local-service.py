# 17-03 §3 — 이름으로 부르되 같은 노드로만
# 앞의 둘이 노드 IP 를 알아야 했다면 이쪽은 Service 이름만으로 된다. 그 이득과 함께,
# 에이전트 없는 노드에서 어떻게 되는지가 같은 그림에 있어야 판단이 선다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 660, "KUBERNETES IN ACTION · 17-03",
      "이름으로 부르되 노드를 넘지 않는다",
      "internalTrafficPolicy 를 Local 로 두면 그 노드의 엔드포인트만 후보가 된다. 앱은 Service 이름 "
      "하나만 알면 되고 노드 IP 를 조합할 필요가 없다.",
      "다른 노드로 넘기는 길이 아예 없다")

for i, (nm, has, c, note) in enumerate((("노드 A — 에이전트 있음", True, OK, "같은 노드 것으로 간다"),
                                        ("노드 C — 에이전트 없음", False, BAD, "엔드포인트 0 개처럼 — 연결 실패"))):
    y0 = 176 + i * 216
    d.box(90, y0, 1040, 180, PAPER, RULE, 0.9, 8)
    d.t(610, y0 + 28, nm, 11, SOFT, KR)
    ddx.node(d, 260, y0 + 100, "클라이언트 파드", "http://agent", 240, 66, INFO)
    if has:
        ddx.node(d, 700, y0 + 100, "로컬 에이전트", "이 노드의 것", 240, 66, OK)
        d.path("M 382 " + str(y0 + 100) + " L 578 " + str(y0 + 100), OK, 1.5, m="ok")
    else:
        ddx.tag(d, 700, y0 + 100, "후보가 없다", BAD, 240)
        d.path("M 382 " + str(y0 + 100) + " L 578 " + str(y0 + 100), BAD, 1.4, m="bad", dash="5 5")
    d.t(1000, y0 + 100, note, 11, c, KR)

d.t(24, 636 - 40, "그래서 사실상 DaemonSet 전용이다 — 모든 노드에 에이전트가 하나씩 있다는 전제 위에서만 성립한다. "
                  "11-03 에서 본 그 성질이 여기서 조건이 된다.", 11, MUTED, KR, "start")
d.legend(612, [("부르는 쪽", INFO), ("닿는다", OK), ("막힌다", BAD)])
d.save("17-03-local-service.svg")
print("ok")
