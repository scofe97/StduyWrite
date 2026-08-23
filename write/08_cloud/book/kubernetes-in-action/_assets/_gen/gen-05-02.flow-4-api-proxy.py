# 05-02 §방법 ④ — API 서버를 통한 접근
# 본문: "kubectl get --raw 가 API 서버에 요청을 보내고 API 서버가 그것을 Pod 로 프록시합니다."
#        → Client IP 는 172.18.0.5(API 서버). kubelet 은 거치지 않는다.
# 좌표계는 k05_access 가 정본.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx, k05_access as K

d = D(K.W, K.H, "KUBERNETES IN ACTION · 05-02",
      "④ API 서버 프록시 — kubelet 을 건너뛴다",
      "kubectl get --raw 로 API 서버에 요청하면 API 서버가 직접 Pod 로 프록시한다. "
      "kubelet 이 경로에 없으므로 홉이 하나 줄고, 마지막으로 붙은 것은 API 서버다.",
      lead="추가 명령도 port-forward 설정도 필요 없다 — 덜 알려졌지만 빠르다")

ddx.band(d, *K.BAND, "③ 과 같은 곳에서 출발하지만 kubelet 을 건너뛴다 — 그만큼 Client IP 가 달라진다")

K.slot(d, K.LAPTOP, "내 노트북", "kubectl get --raw", "원래 요청자", OK)
K.zone(d, K.CP_ZONE, "Control Plane", INFO)
K.slot(d, K.API, "API 서버", "172.18.0.5 · Pod 로 프록시", "", OK)
K.slot(d, K.ETC, "etcd · 스케줄러", "무관", "", dim=True)
K.zone(d, K.WK_ZONE, "Worker 노드 — kiada 를 호스팅하는 노드", OK)
K.slot(d, K.UPPER, "kubelet", "경로에 없다", "건너뛴다", dim=True)
K.slot(d, K.POD, "kiada Pod", "10.244.2.5:8080", "응답에 Client IP 를 찍는다", INFO)
K.hop(d, K.TO_API, "①", K.TO_API_CHIP)
K.hop(d, f"M {K.API[0]+K.API[2]//2+6} {K.API[1]+14} L 562 {K.API[1]+14} L 562 {K.POD[1]} "
         f"L {K.POD[0]-K.POD[2]//2-10} {K.POD[1]}", "②", (562, 326))
K.verdict(d, "① 내 노트북 → API 서버   ② API 서버 → kiada Pod (kubelet 을 건너뛴다)", "API 서버", "172.18.0.5", "— 내 노트북은 한 홉 뒤라 보이지 않는다")
d.legend(590, [("경로에 있는 것", OK), ("kiada Pod", INFO), ("마지막 연결자와 그 경로", ACC)])
d.save("05-02-flow-4-api-proxy.svg")
print("ok flow-4-api-proxy")
