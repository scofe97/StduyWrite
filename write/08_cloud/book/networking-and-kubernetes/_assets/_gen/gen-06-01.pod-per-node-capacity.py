# 06-01.pod-per-node-capacity — 인스턴스의 IP 수용량이 곧 Pod 상한
# 타입 스펙: type-data-flow.md — 인스턴스 타입에서 실제 배포 가능 수까지 네 칸 계산 한 줄
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 560
d = D(W, H, "INSTANCE IP CAPACITY = POD LIMIT",
      "인스턴스 타입의 IP 수용량이 그대로 노드당 Pod 상한이 된다",
      "Pod 마다 ENI 보조 IP 를 하나씩 쓰므로, 인스턴스가 가질 수 있는 IP 수가 곧 담을 수 있는 Pod 수다.",
      lead="Pod 마다 ENI 보조 IP 하나 — 인스턴스의 IP 수가 곧 Pod 수다")
ddx.band(d, 104, 496, "타입을 고르는 순간 노드당 Pod 상한이 함께 정해진다")
ddx.stage_chain(d, 316,
  ["① 인스턴스 타입", "② IP 수용량", "③ 최대 Pod", "④ 실제 가용"],
  [("타입 선택", "m5.large", "eksctl 기본값", None),
   ("ENI × IP", "(ENI 수 × (IP-1))", "+2 를 더한다", None),
   ("상한 29", "노드 하나가 담는 수", "넘으면 Pod 는 waiting", WARN),
   ("실제 27", "시스템 Pod 를 뺀 값", "CNI·kube-proxy 상주", ACC)],
  ["수용량이", "공식으로", "빼고 나면"])
d.t(36, 468, "상한에 걸린 Pod 는 스케줄되지 않고 waiting 으로 남는다 — 노드를 늘리거나 타입을 키워야 한다",
     12, MUTED, KR, "start")
d.legend(512, [("걸리면 스케줄 안 됨", WARN), ("실제로 쓸 수 있는 수", ACC)])
d.save("06-01.pod-per-node-capacity.svg"); print("ok pod-per-node-capacity")
