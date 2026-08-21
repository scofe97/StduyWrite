# 11-03 §3 — internalTrafficPolicy Local, 안에서 온 요청
# external 편과 같은 골격. 다른 점은 앞단에 노드를 고르는 장치가 없다는 것이고,
# 그래서 구제책 없음이 이 도식의 focal 이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, RULE, KR
import ddx

d = D(1160, 588, "KUBERNETES IN ACTION · 11-03",
      "internalTrafficPolicy Local — 안에서 온 요청",
      "요청은 클라이언트 파드가 있는 노드에서 시작해 cluster IP 로 향한다. 앞단에서 노드를 골라 주는 장치가 없어 "
      "부하 불균등도 생기지 않지만, 로컬 엔드포인트가 없으면 막을 장치 없이 연결이 실패한다.",
      "앞단에 노드를 고르는 장치가 없다")

ddx.band(d, 100, 500, "클러스터 안 파드 → cluster IP", x=24, w=1112)

# 파드가 있는 노드
d.box(120, 168, 460, 128, PAPER, RULE, 0.9, 8)
d.t(350, 192, "노드 A — 로컬 파드 있음", 11, SOFT, KR)
ddx.node(d, 240, 246, "클라이언트 파드", "curl http://quote", 200, 62, INFO)
ddx.node(d, 480, 246, "파드", "10.244.1.7", 150, 62, OK)
d.path("M 346 246 L 400 246", OK, 1.5, m="ok")

# 파드가 없는 노드
d.box(120, 336, 460, 128, PAPER, RULE, 0.9, 8)
d.t(350, 360, "노드 C — 로컬 파드 없음", 11, SOFT, KR)
ddx.node(d, 240, 414, "클라이언트 파드", "curl http://quote", 200, 62, INFO)
ddx.tag(d, 480, 414, "Connection refused", BAD, 190)
d.path("M 346 414 L 380 414", BAD, 1.5, m="bad", dash="5 5")

d.t(640, 214, "노드 A 의 클라이언트는 같은 노드 파드로만 간다", 11, OK, KR, "start")
d.t(640, 236, "홉도 SNAT 도 없다", 11, MUTED, KR, "start")
ddx.focal_tag(d, 830, 400, "막을 장치가 없다", 190)
d.t(640, 444, "healthCheckNodePort 같은 구제책이 여기에는 없다 —", 11, MUTED, KR, "start")
d.t(640, 466, "모든 노드에 파드가 하나씩 있다는 전제 위에서만 성립한다", 11, MUTED, KR, "start")

d.t(24, 526, "그래서 사실상 DaemonSet 전용 장치다. replica 세 개짜리 Deployment 에 걸면 파드 없는 노드의 클라이언트가 전부 거절당한다.",
     11, MUTED, KR, "start")
d.legend(546, [("닿는 길", OK), ("끊기는 길", BAD), ("구제책 없음", ACC)])
d.save("11-03-internal-traffic-policy-local.svg")
print("ok")
