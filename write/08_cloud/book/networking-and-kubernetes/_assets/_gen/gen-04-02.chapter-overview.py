import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 544
d = D(W, H, "04-02 · CNI AND kube-proxy", "주소를 주는 쪽과 트래픽을 잇는 쪽 — 두 직군이 만나 서비스가 된다", "CNI 는 주소를 주고 kube-proxy 는 트래픽을 잇는다. 둘이 만나야 ClusterIP 가 Pod 까지 닿는다.", lead="CNI 는 주소를 주고 kube-proxy 는 트래픽을 잇는다")
ddx.band(d, 104, 496, "명세는 얇고 구현체가 갈린다 — 갈리는 지점은 정책 지원이다")
ddx.stage_chain(d, 316, ["§1 명세", "§2 구현체", "§3 실습", "§4 kube-proxy"], [("네 연산", "JSON stdin·stdout", "바이너리 하나면 끝", None),
   ("구현체", "4대 비교", "정책 지원이 관문", None),
   ("실습", "KIND · Cilium", "기본 CNI 를 끄고", None),
   ("번역기", "ClusterIP → Pod", "iptables 가 기본값", ACC)], ["구현이", "띄워 보면", "트래픽은"])
d.t(36, 468, "CNI 가 주소를 다 준 뒤에야 kube-proxy 가 할 일이 생긴다 — 순서가 있는 두 직군이다", 12, MUTED, KR, "start")
d.legend(512, [("트래픽을 잇는 쪽", ACC)])
d.save("04-02.chapter-overview.svg"); print("ok 04-02")
