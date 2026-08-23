# 05-02 §방법 ③ — kubectl port-forward
# 본문: "curl 프로세스가 프록시에 연결하고, 프록시가 API 서버에, API 서버가 Pod 를 호스팅하는
#        노드의 Kubelet 에, Kubelet 이 Pod 의 loopback 장치(localhost)를 통해 컨테이너에
#        연결합니다." → Client IP 는 127.0.0.1.
# 좌표계는 k05_access 가 정본. 네 방법 중 유일하게 모든 컴포넌트가 경로에 있다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx, k05_access as K

d = D(K.W, K.H, "KUBERNETES IN ACTION · 05-02",
      "③ port-forward — 홉이 가장 많고, 마지막 홉이 Pod 자신이다",
      "curl → 프록시 → API 서버 → kubelet → Pod 의 loopback 순으로 간다. 마지막에 kubelet 이 "
      "Pod 의 lo 로 붙기 때문에, 컨테이너는 요청이 자기 자신에게서 온 것으로 본다.",
      lead="가장 쉬운 방법이지만 내부적으로는 가장 복잡하다 — 경로 어딘가가 깨지면 Pod 는 멀쩡해도 안 된다")

ddx.band(d, *K.BAND, "네 방법 중 유일하게 모든 컴포넌트가 경로에 있다")

K.slot(d, K.LAPTOP, "내 노트북", "curl → 프록시", "원래 요청자", OK)
K.zone(d, K.CP_ZONE, "Control Plane", INFO)
K.slot(d, K.API, "API 서버", "인증하고 중계한다", "", OK)
K.slot(d, K.ETC, "etcd · 스케줄러", "무관", "", dim=True)
K.zone(d, K.WK_ZONE, "Worker 노드 — kiada 를 호스팅하는 노드", OK)
K.slot(d, K.UPPER, "kubelet", "노드 에이전트", "Pod 에 실제로 붙는 것", OK)
K.slot(d, K.POD, "kiada Pod", "lo 127.0.0.1 · eth0 10.244.2.5", "lo 에 바인딩돼야 닿는다", INFO)
K.hop(d, K.TO_API, "①", K.TO_API_CHIP)
K.hop(d, f"M {K.API[0]+K.API[2]//2+6} {K.UPPER[1]} L {K.UPPER[0]-K.UPPER[2]//2-10} {K.UPPER[1]}",
      "②", (568, K.UPPER[1]))
K.hop(d, K.DROP, "③", K.DROP_CHIP)
K.verdict(d, "① 프록시 → API 서버   ② API 서버 → kubelet   ③ kubelet → Pod 의 loopback", "Pod 자신의 loopback", "127.0.0.1", "— 원래 요청자는 세 홉 뒤라 보이지 않는다")
d.legend(590, [("경로에 있는 것", OK), ("kiada Pod", INFO), ("마지막 연결자와 그 경로", ACC)])
d.save("05-02-flow-3-port-forward.svg")
print("ok flow-3-port-forward")
