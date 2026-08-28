# 05-02 §방법 ① — 워커 노드에서 접근
# 본문: "워커 노드에 로그인해 거기서 Pod 와 통신할 수 있습니다 ... 통신이 로컬에서 일어나
#        성공 확률이 가장 높습니다." Client IP 는 10.244.2.1(노드·브리지).
# 좌표계는 k05_access 가 정본 — 네 장 연작이라 stride 를 파일로 강제한다.
# 타입 스펙: type-architecture.md — 네 방법 연작의 첫 장이다. 점선 경계가 Control Plane · Worker 노드 영역을 표시하고
#           경로에 없는 컴포넌트를 흐리게 둔다 — 무엇이 경로에 없는지가 이 장의 논지다.
#           type-data-flow 는 역할 레인 1~4 × 단계 열 × 타입 있는 페이로드 칩이 입력 계약인
#           데이터 플랫폼 전용 타입이라 여기엔 맞지 않는다. type-architecture 의 Best for 에
#           "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx, k05_access as K

d = D(K.W, K.H, "KUBERNETES IN ACTION · 05-02",
      "방법 1 워커 노드에서 — 중계가 하나도 없다",
      "노드에 로그인해 그 노드에서 curl 한다. Control Plane 도 kubelet 도 관여하지 않고 "
      "노드가 kiada 에 직접 붙으므로, kiada 가 보는 것은 노드의 브리지 IP 다.",
      lead="가장 짧은 경로다 — 통신 문제를 좁힐 때 여기서부터 시험한다")

ddx.band(d, *K.BAND, "경로에 없는 컴포넌트는 흐리게 두었다 — 없는 것이 이 방법의 특징이다")

K.slot(d, K.LAPTOP, "내 노트북", "이 방법에서는", "쓰이지 않는다", dim=True)
K.zone(d, K.CP_ZONE, "Control Plane — 통신 경로에는 없다", INFO, dim=True)
K.slot(d, K.API, "API 서버", "관여하지 않는다", "", dim=True)
K.slot(d, K.ETC, "etcd · 스케줄러", "무관", "", dim=True)
K.zone(d, K.WK_ZONE, "Worker 노드 — kiada 를 호스팅하는 그 노드", OK)
K.slot(d, K.UPPER, "노드 셸 (curl)", "docker exec 로 로그인", "브리지 IP 10.244.2.1", OK)
K.slot(d, K.POD, "kiada Pod", "10.244.2.5:8080", "응답에 Client IP 를 찍는다", INFO)
K.hop(d, K.DROP, "①", K.DROP_CHIP)
K.verdict(d, "① 노드 셸에서 kiada 로 — 같은 노드 안이라 중계가 없다", "노드", "10.244.2.1", "— 노드의 브리지 IP")
d.legend(590, [("경로에 있는 것", OK), ("kiada Pod", INFO), ("마지막 연결자와 그 경로", ACC)])
d.save("05-02-flow-1-worker-node.svg")
print("ok flow-1-worker-node")
