# a0-02 §3 파드 하나가 만들어지는 동안.
# 본문(부록 B.1.2): "Automatic sidecar injection uses Kubernetes mutating admission webhooks to
#       inject data-plane components into the Pod definition before it is applied to the
#       Kubernetes datastore." MutatingWebhookConfiguration 이 API 서버에게 어떤 이벤트를
#       외부 서비스로 보낼지 알려 준다. 사이드카를 넣는 것은 istio-sidecar-injector.
# 타입 스펙: type-sequence — 참여자 사이 시간 순 주고받기가 논점이다. 레인 + 메시지, 상태는 칩으로.
#           축약: 라벨이 붙지 않는 자리에서 저장 시점이 논점이라 그 자리에 상태 칩을 둔다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, KR, MONO

W, H = 1000, 572
d = Seq(W, H, "ISTIO IN ACTION · A0-02 §3",
        "부품은 저장되기 전에 끼워진다",
        "kubectl 이 올린 파드 정의가 API 서버에 닿으면, 서버는 MutatingWebhookConfiguration 을 보고 "
        "그 이벤트를 istiod 로 보낸다. 고쳐진 정의가 돌아온 뒤에야 데이터스토어에 저장된다.",
        "그래서 라벨을 나중에 붙였다면 이미 뜬 파드는 다시 만들어야 합니다")

d.lanes([("kubectl", "사람이 친다"),
         ("API 서버", "admission chain"),
         ("istiod", "sidecar injector"),
         ("데이터스토어", "etcd")], y0=104, lane_w=216)
d.rails(468)

d.msg("kubectl", "API 서버", "create Pod", 196, MUTED, "ar", sub="부품 없는 정의")
d.selfmsg("API 서버", "웹훅 설정을 본다", 252, MUTED, sub="istio-sidecar-injector")
d.msg("API 서버", "istiod", "admission review", 316, ACC, "acc", sub="네임스페이스 라벨이 맞을 때만")
d.msg("istiod", "API 서버", "patch", 372, ACC, "acc", sub="컨테이너 둘 + init 하나")
d.msg("API 서버", "데이터스토어", "저장", 436, MUTED, "ar", sub="이때는 이미 고쳐진 정의")

d.state("API 서버", "저장 전", 288, INFO)

d.t(24, 496, "라벨이 없으면 이 왕복이 아예 일어나지 않는다 — 파드에 사이드카가 안 붙으면 여기부터 본다", 11, SOFT, KR, "start")
d.legend(516, [("주입이 일어나는 왕복", ACC), ("아직 저장되지 않은 구간", INFO)])
d.save("a0-02.webhook-path.svg")
