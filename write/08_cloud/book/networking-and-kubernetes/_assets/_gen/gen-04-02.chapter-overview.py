# 타입 스펙: type-process.md — 단계 머리 + 한 줄 체인. 칸마다 같은 의미 슬롯(절 번호 · 이름 ·
#           한 줄 요약 · 꼬리표)이 같은 자리에 반복된다(semantic-patterns 의 "Stage framework
#           with semantic slots"). 화살표는 데이터가 아니라 읽는 순서를 나른다.
#           2026-08-28 type-data-flow 에서 옮겼다 — data-flow 정본은 "who does what at each
#           stage" 와 role-scoped lane 을 전제로 하는데, 편 지도에는 주체도 레인도 없다.
#           엄밀히는 두 정본 다 주체 기반이라 편 지도는 표의 공백에 가깝고, 주체 없이도 맞는
#           유일한 라우팅 규칙이 위 semantic-patterns 한 줄이라 그쪽을 따랐다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 560
d = D(W, H, "04-02 · CNI AND kube-proxy", "주소를 주는 쪽과 트래픽을 잇는 쪽 — 두 직군이 만나 서비스가 된다", "CNI 는 주소를 주고 kube-proxy 는 트래픽을 잇는다. 둘이 만나야 ClusterIP 가 Pod 까지 닿는다.", lead="CNI 는 주소를 주고 kube-proxy 는 트래픽을 잇는다")
ddx.band(d, 104, 496, "명세는 얇고 구현체가 갈린다 — 갈리는 지점은 정책 지원이다")
ddx.stage_chain(d, 316, ["§1 명세", "§2 구현체", "§3 실습", "§4 kube-proxy"], [("네 연산", "JSON stdin·stdout", "바이너리 하나면 끝", None),
   ("구현체", "4대 비교", "정책 지원이 관문", None),
   ("실습", "KIND · Cilium", "기본 CNI 를 끄고", None),
   ("번역기", "ClusterIP → Pod", "iptables 가 기본값", ACC)], ["구현이", "띄워 보면", "트래픽은"])
d.t(36, 468, "CNI 가 주소를 다 준 뒤에야 kube-proxy 가 할 일이 생긴다 — 순서가 있는 두 직군이다", 12, MUTED, KR, "start")
d.legend(512, [("트래픽을 잇는 쪽", ACC)])
d.save("04-02.chapter-overview.svg"); print("ok 04-02")
