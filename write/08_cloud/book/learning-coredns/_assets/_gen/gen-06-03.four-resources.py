# 06-03 §1 — CoreDNS 파드 하나가 뜨려면 자원 네 범주가 한 파드로 모여야 한다.
# 본문 근거: 이 노트 §1 의 네 범주(API 접근 권한·ConfigMap·Service·Deployment)와 §2~§4 의 이름.
# 매니페스트 근거: kubeadm manifests.go 의 ServiceAccount coredns·ClusterRole system:coredns·Service kube-dns
#            (ports dns 53/UDP · dns-tcp 53/TCP · metrics 9153/TCP)·Deployment coredns.
# 타입 스펙: type-architecture — 구성요소 다섯과 그 사이의 참조 관계가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 510
d = D(W, H, "LEARNING COREDNS · 06-03 §1",
      "네 범주가 한 파드로 모인다",
      "권한 묶음은 파드가 API 서버를 읽게 하고, ConfigMap 은 Corefile 을 넣어 주고, Deployment 는 파드를 띄우고, "
      "Service 는 트래픽을 파드로 보낸다. Corefile 은 이 넷 가운데 하나일 뿐이다.",
      "주황 상자가 넷이 모여야 뜨는 자리입니다")


def card(x, y, w, h, title, lines):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, title, 14, INK, KR, "start", 600)
    for j, (txt, fam) in enumerate(lines):
        d.t(x + 16, y + 50 + j * 20, txt, 12, MUTED, fam, "start")


d.box(330, 104, 220, 52, PAPER2, RULE, 1.0, 8)
d.t(440, 136, "API 서버", 14, INK, KR, "middle", 600)

d.tone(320, 232, 240, 96, ACC, 8, "12", 1.4)
d.t(440, 272, "CoreDNS 파드", 15, ACC, KR, "middle", 600)
d.t(440, 300, "넷이 모여야 뜬다", 12, MUTED, KR)
d.path("M 440 230 L 440 160", MUTED, 1.4, m="ar")
d.t(452, 200, "list · watch", 12, MUTED, MONO, "start")

card(20, 104, 250, 104, "API 접근 권한", [("ServiceAccount coredns", MONO), ("ClusterRole system:coredns", MONO), ("ClusterRoleBinding", MONO)])
card(20, 330, 250, 80, "ConfigMap coredns", [("Corefile · 볼륨으로 마운트", KR)])
card(610, 104, 250, 104, "Deployment coredns", [("복제본 수 · 갱신 전략", KR), ("dnsPolicy · 자원 · 프로브", KR), ("serviceAccountName", MONO)])
card(610, 330, 250, 80, "Service kube-dns", [("53/UDP · 53/TCP · 9153", MONO)])

d.path("M 272 180 L 294 180 L 294 262 L 316 262", MUTED, 1.3, m="ar")
d.path("M 272 370 L 294 370 L 294 300 L 316 300", MUTED, 1.3, m="ar")
d.path("M 608 180 L 586 180 L 586 262 L 564 262", MUTED, 1.3, m="ar")
d.path("M 608 370 L 586 370 L 586 300 L 564 300", MUTED, 1.3, m="ar")

d.t(20, 448, "Corefile 은 넷 중 하나 · ConfigMap 은 앞 편이 다뤘다", 13, MUTED, KR, "start")

d.legend(466, [("넷이 모이는 파드", ACC)])
d.save("06-03.four-resources.svg")
