# 11-03 §3 — internalTrafficPolicy Local, 안에서 온 요청
# external 편과 같은 골격. 다른 점은 앞단에 노드를 고르는 장치가 없다는 것이고,
# 그래서 구제책 없음이 이 도식의 focal 이다.
# 타입 스펙: type-architecture.md — 노드 안의 클라이언트 파드와 대상 파드를 잇는 구성도 두 벌.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, RULE, KR
import ddx

d = D(1000, 570, "KUBERNETES IN ACTION · 11-03",
      "internalTrafficPolicy Local — 안에서 온 요청",
      "요청은 클라이언트 파드가 있는 노드에서 시작해 cluster IP 로 향한다. 앞단에서 노드를 골라 주는 장치가 없어 "
      "부하 불균등도 생기지 않지만, 로컬 엔드포인트가 없으면 패킷이 버려져 연결이 시간 초과로 끝난다.",
      "앞단에 노드를 고르는 장치가 없다")

ddx.band(d, 100, 500, "클러스터 안 파드 → cluster IP")

# 파드가 있는 노드
d.box(48, 168, 440, 128, PAPER, RULE, 0.9, 8)
d.t(268, 192, "노드 A — 로컬 파드 있음", 11, SOFT, KR)
ddx.node(d, 150, 246, "클라이언트 파드", "curl http://quote", 170, 62, INFO)
ddx.node(d, 390, 246, "파드", "10.244.1.7", 130, 62, OK)
d.path("M 241 246 L 319 246", OK, 1.5, m="ok")

# 파드가 없는 노드
d.box(48, 336, 440, 128, PAPER, RULE, 0.9, 8)
d.t(268, 360, "노드 C — 로컬 파드 없음", 11, SOFT, KR)
ddx.node(d, 150, 414, "클라이언트 파드", "curl http://quote", 170, 62, INFO)
ddx.tag(d, 390, 414, "Connection timed out", BAD, 170)
d.path("M 241 414 L 299 414", BAD, 1.5, m="bad", dash="5 5")

d.t(520, 214, "노드 A 의 클라이언트는 같은 노드 파드로만 간다", 11, OK, KR, "start")
d.t(520, 236, "홉도 SNAT 도 없다", 11, MUTED, KR, "start")
ddx.focal_tag(d, 620, 400, "막을 장치가 없다", 190)
d.t(520, 444, "healthCheckNodePort 같은 구제책이 여기에는 없다 —", 11, MUTED, KR, "start")
d.t(520, 466, "모든 노드에 파드가 하나씩 있다는 전제 위에서만 성립한다", 11, MUTED, KR, "start")

d.legend(522, [("클라이언트", INFO), ("닿는 길", OK), ("끊기는 길", BAD), ("구제책 없음", ACC)])
d.save("11-03-internal-traffic-policy-local.svg")
print("ok")
