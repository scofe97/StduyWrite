# 06-01.pod-per-node-capacity — 인스턴스의 IP 수용량이 곧 Pod 상한
# 타입 스펙: type-architecture.md — 상자에 든 것은 계산 단계의 값(인스턴스 타입 · ENI×IP · 29 · 27)이다.
#           38개 메뉴에 이 형태(주체 레인 없는 값·단계 사슬)를 담을 타입이 없다 —
#           layout 문법만 architecture 를 따르고 그 사실을 여기 적어 둔다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
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
