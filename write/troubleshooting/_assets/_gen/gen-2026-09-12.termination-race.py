# 2026-09-12 B — Pod 종료 시 두 갈래가 동시에 시작되고 서로 기다리지 않는다.
# 회차에서 학습자가 PID 1·exec 를 스스로 짚었으나 "왜 죽는 Pod 에 요청이 계속 오는가"
# 에서 한 칸 모자랐다. 공식 문서의 "at the same time" 이 그 답이라 두 갈래를 나란히 세운다.
# 타입 스펙: type-sequence — 여러 행위자가 시간축 위에서 주고받는 순서. 장애 재구성이
#           스펙이 명시한 용도다. flowchart 를 검토했으나 분기가 아니라 동시 진행이라
#           기각. swimlane 도 검토했으나 레인 간 handoff 가 아니라 무handoff 가 요점이라 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import Seq, ACC, MUTED, SOFT, INK, BAD, RULE, KR, MONO

W, H = 840, 656
d = Seq(W, H, "TROUBLESHOOTING DRILL · 2026-09-12 B",
        "종료는 두 갈래로 동시에 갑니다",
        "kubelet 이 컨테이너를 내리는 일과 컨트롤 플레인이 EndpointSlice 에서 빼는 일은 "
        "동시에 시작되고 서로를 기다리지 않는다. 앱이 먼저 죽고 전파가 늦으면 그 틈이 502 가 된다.",
        lead="왼쪽이 신호 갈래, 오른쪽이 전파 갈래입니다. 둘은 서로 신호를 주고받지 않습니다.")

d.lanes([
    ("컨트롤 플레인", "EndpointSlice"),
    ("kubelet", "노드"),
    ("셸 PID 1", "sh -c"),
    ("앱", "java · 8080"),
], y0=118, lane_w=172)

d.rails(556)

Y = 190
d.msg("kubelet", "셸 PID 1", "SIGTERM", Y, ACC, sub="PID 1 에게만 보냅니다")
d.msg("컨트롤 플레인", "kubelet", "Pod 제거 평가", Y, SOFT, dash="4 4",
      sub="같은 시각에 시작됩니다")

d.state("셸 PID 1", "셸 종료", Y + 70, BAD)
d.t(d.LX["셸 PID 1"] + 92, Y + 74, "자식에게 전달하지 않습니다", 12, MUTED, KR, "start")

d.msg("셸 PID 1", "앱", "SIGKILL", Y + 130, BAD, sub="PID 1 이 죽으면 커널이 정리합니다")
d.state("앱", "즉사", Y + 186, BAD)
d.t(d.LX["앱"] - 102, Y + 190, "graceful 코드는 호출되지 않습니다", 12, MUTED, KR, "end")

d.t(d.LX["컨트롤 플레인"], Y + 186, "전파는 아직 진행 중", 12, SOFT, KR, "middle")

d.msg("컨트롤 플레인", "앱", "이 구간의 요청", Y + 250, BAD, dash="3 5",
      sub="프록시는 살아 있고 8080 은 비었습니다 → connection refused → 502")

d.t(W // 2, 596, "preStop 의 sleep 은 왼쪽 갈래를 늦춰 오른쪽이 끝날 시간을 법니다",
    13, ACC, KR, "middle", 600)
d.t(W // 2, 620, "그 sleep 동안 kubelet 은 SIGTERM 을 아직 보내지 않습니다",
    12, MUTED, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-12.termination-race.svg"))
print("ok")
