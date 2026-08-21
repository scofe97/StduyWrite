# 11-03 §3 — externalTrafficPolicy Local, 밖에서 온 요청
# 짝인 internal 편과 같은 골격으로 그려 비대칭이 나란히 읽히게 했다.
# 이쪽에는 구제 장치가 있으므로 되돌아가는 화살표가 로드밸런서에 닿는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, RULE, KR
import ddx

d = D(1160, 588, "KUBERNETES IN ACTION · 11-03",
      "externalTrafficPolicy Local — 밖에서 온 요청",
      "요청은 로드밸런서가 고른 노드의 NodePort 에 먼저 닿는다. Local 이면 그 노드의 규칙이 로컬 엔드포인트만 "
      "고르므로 노드 간 홉과 소스 IP 위조가 사라진다. 파드 없는 노드는 헬스체크가 분배에서 빼 준다.",
      "앞단에 노드를 고르는 장치가 있다")

ddx.band(d, 100, 500, "클러스터 밖 → nodePort · LoadBalancer", x=24, w=1112)
ddx.node(d, 150, 300, "외부 클라이언트", "203.0.113.7", 200, 80, INFO)
ddx.node(d, 430, 300, "로드밸런서", "건강한 노드로만", 200, 80)
d.path("M 256 300 L 324 300", MUTED, 1.5, m="ar")

# 파드가 있는 노드
d.box(660, 168, 380, 128, PAPER, RULE, 0.9, 8)
d.t(850, 192, "노드 A — 로컬 파드 있음", 11, SOFT, KR)
ddx.node(d, 850, 246, "파드", "10.244.1.7:8080", 240, 62, focal=True)
d.path("M 536 288 L 600 288 L 600 232 L 654 232", OK, 1.5, m="ok")
d.t(650, 210, "몫을 받는다", 11, OK, KR, "end")

# 파드가 없는 노드
d.box(660, 336, 380, 128, PAPER, RULE, 0.9, 8)
d.t(850, 360, "노드 C — 로컬 파드 없음", 11, SOFT, KR)
ddx.tag(d, 850, 414, "503 을 답한다", WARN, 200)
d.path("M 536 312 L 592 312 L 592 400 L 654 400", WARN, 1.4, m="warn", dash="6 5")
d.t(586, 356, "헬스체크를 보낸다", 11, WARN, KR, "end")
# 되돌아가는 화살표는 로드밸런서로 닿아야 한다 — 허공을 가리키면 무엇이 빼는지 읽히지 않는다
d.path("M 654 440 L 628 440 L 628 276 L 542 276", OK, 1.4, m="ok", dash="6 5")
d.t(660, 490, "503 이면 로드밸런서가 분배에서 뺀다 — healthCheckNodePort", 11, OK, KR, "start")

d.t(24, 526, "소스 IP 는 남지만 파드당 부하는 어긋난다. 로드밸런서는 노드 단위로 나누는데 노드마다 파드 수가 다르기 때문이다.",
     11, MUTED, KR, "start")
d.legend(546, [("닿는 길", OK), ("빠지는 길", WARN), ("로컬만 후보", ACC)])
d.save("11-03-external-traffic-policy-local.svg")
print("ok")
