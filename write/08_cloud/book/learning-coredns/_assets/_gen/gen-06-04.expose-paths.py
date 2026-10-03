# 06-04 §6 「클러스터 밖에서 닿게 하기」 — 외부 IP 를 이름으로 알리는 두 길과 원서 사이드바의 권고.
# 본문 근거: 이 노트 §6 — external DNS 는 외부 DNS 서버를 API 로 고치는 컨트롤러, k8s_external 은 CoreDNS 가
#            <service>.<namespace>.<zone> 으로 직접 답하고 SOA·NS 로 위임받는다. 사이드바: 외부 이름 전용 CoreDNS 를 따로.
# 예시 값: 203.0.113.10(문서용 주소)·web·default 는 설명용, services.example.com 은 원서 예제 존.
# 타입 스펙: type-architecture — 구성요소와 이름이 흐르는 경로 둘, 그리고 권고 배치가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING COREDNS · 06-04 §6",
      "외부 IP 를 이름으로 알리는 두 길",
      "LoadBalancer 서비스가 외부 IP 를 받은 뒤 그 이름을 바깥에 알리는 길은 둘이다. external DNS 는 바깥 DNS 서버에 레코드를 써 넣고, "
      "k8s_external 은 CoreDNS 가 위임받은 존에서 직접 답한다.",
      "주황 상자가 원서 사이드바의 권고입니다")


def node(x, y, w, h, title, sub, focal=False, mono_sub=False):
    if focal:
        d.tone(x, y, w, h, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + 12, y + 28, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 12, y + 50, sub, 12, MUTED, MONO if mono_sub else KR, "start")


def arrow(x1, y, x2, label):
    d.path(f"M {x1 + 2} {y} L {x2 - 3} {y}", MUTED, 1.3, m="ar")
    if label:
        d.t((x1 + x2) / 2, y - 8, label, 12, MUTED, KR)


# 공통 출발점
d.t(20, 118, "external DNS", 12, SOFT, KR, "start", 600)
node(20, 128, 170, 68, "Service web", "LB IP 203.0.113.10", mono_sub=False)
node(260, 128, 180, 68, "external-dns 컨트롤러", "Service · Ingress 감시")
node(510, 128, 180, 68, "바깥 DNS 서버", "Route 53 · CoreDNS+etcd …")
arrow(190, 162, 260, "감시")
arrow(440, 162, 510, "API 로 기록")
node(740, 128, 120, 68, "바깥 클라이언트", "그 서버에 질의")
arrow(690, 162, 740, "")

d.t(20, 238, "k8s_external", 12, SOFT, KR, "start", 600)
node(20, 248, 170, 68, "Service web", "LB IP 203.0.113.10")
node(260, 248, 250, 68, "CoreDNS · k8s_external", "services.example.com 존", mono_sub=False)
node(580, 248, 280, 68, "web.default.services.example.com", "A 203.0.113.10 · SOA · NS")
arrow(190, 282, 260, "읽음")
arrow(510, 282, 580, "직접 응답")

node(20, 352, 840, 68, "외부 이름은 전용 CoreDNS 로 따로 띄운다",
     "바깥의 서비스 거부 공격이 클러스터 DNS 를 쓰러뜨리면 클러스터 서비스 상당수가 함께 내려간다", focal=True)

d.t(20, 448, "k8s_external 은 kubernetes 플러그인과 함께일 때만 동작 · 상위 존이 NS 로 위임해야 바깥에서 닿는다", 13, MUTED, KR, "start")

d.legend(464, [("원서 사이드바의 권고", ACC)])
d.save("06-04.expose-paths.svg")
