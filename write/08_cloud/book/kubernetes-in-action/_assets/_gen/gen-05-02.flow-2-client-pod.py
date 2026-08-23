# 05-02 §방법 ② — 일회성 클라이언트 Pod
# 본문: "다른 Pod 가 이 Pod 에 접근할 수 있는지 시험할 때는 전용 Pod 를 만들어 그 안에서
#        curl 을 돌립니다." Client IP 는 10.244.1.13(요청한 임시 Pod 의 IP).
# 좌표계는 k05_access 가 정본.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx, k05_access as K

d = D(K.W, K.H, "KUBERNETES IN ACTION · 05-02",
      "② 임시 클라이언트 Pod — Pod 가 Pod 에 직접 붙는다",
      "클러스터 안에 curl Pod 를 띄워 kiada 의 IP 로 연결한다. Control Plane 을 거치지 않고 "
      "CNI 가 노드 경계를 넘어 라우팅하므로, kiada 가 보는 것은 그 임시 Pod 의 IP 다.",
      lead="네트워크가 멀쩡해도 정책으로 막힐 수 있다 — Pod 대 Pod 를 시험하는 방법이다")

ddx.band(d, *K.BAND, "Control Plane 은 Pod 를 만들 때만 쓰였고 통신 경로에는 없다")

K.slot(d, K.LAPTOP, "내 노트북", "kubectl run 으로", "Pod 를 만들기만 한다", dim=True)
K.zone(d, K.CP_ZONE, "Control Plane — 통신 경로에는 없다", INFO, dim=True)
K.slot(d, K.API, "API 서버", "관여하지 않는다", "", dim=True)
K.slot(d, K.ETC, "etcd · 스케줄러", "무관", "", dim=True)
K.zone(d, K.WK_ZONE, "클러스터 안 — 두 Pod 는 다른 노드에 있어도 된다", OK)
K.slot(d, K.UPPER, "임시 Pod (curl)", "IP 10.244.1.13", "조사 끝나면 삭제된다", OK)
K.slot(d, K.POD, "kiada Pod", "10.244.2.5:8080", "응답에 Client IP 를 찍는다", INFO)
K.hop(d, K.DROP, "①", K.DROP_CHIP)
K.verdict(d, "① 임시 Pod 에서 kiada 로 — CNI 가 노드 경계를 넘어 라우팅한다", "임시 Pod", "10.244.1.13", "— 요청한 그 Pod 의 IP")
d.legend(590, [("경로에 있는 것", OK), ("kiada Pod", INFO), ("마지막 연결자와 그 경로", ACC)])
d.save("05-02-flow-2-client-pod.svg")
print("ok flow-2-client-pod")
