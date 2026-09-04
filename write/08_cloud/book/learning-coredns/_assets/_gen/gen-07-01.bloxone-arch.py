# 07-01 §8 — BloxOne Threat Defense 가 앞 절들을 이어 붙인 자리.
# 원문 근거: "Infoblox configures the stub resolver on B1TD clients to query a local instance of
#            CoreDNS running on the loopback address. This instance of CoreDNS adds an EDNS0
#            option to the query it receives using the rewrite plug-in ... CoreDNS uses the
#            forward plug-in's support for DNS over TLS (DoT) to encrypt communication with the
#            forwarder" / 프록시는 사슬이 아니라 대안이다: "For cases in which several B1TD
#            clients access the B1TD cloud from a single network or site, Infoblox supplies a DNS
#            Forwarding Proxy ... performs the same function as the client-based version, but it
#            can receive queries from a number of clients." / "If not, CoreDNS forwards the query
#            to an instance of Unbound, a fast DNS server that supports full recursion."
# 타입 스펙: type-architecture — 신뢰 경계 둘과 그 사이를 건너는 경로가 본체다. 배치가 아니라
#           통합 지도이므로 deployment 가 아니라 이쪽을 쓴다 (원서에 이미지 버전·복제 수 같은
#           배치 수치가 없어 지어내지 않는다).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, INFO, KR, MONO

W, H = 880, 600
ZS = "rgba(245,245,245,0.20)"
d = D(W, H, "LEARNING COREDNS · 07-01 §8",
      "클라이언트에서 클라우드까지, 같은 소프트웨어 두 자리",
      "클라이언트 쪽 CoreDNS 가 요청에 신원을 실어 DoT 로 넘기고, 클라우드 쪽 CoreDNS 가 "
      "policy 플러그인으로 정책을 적용한다. 정책에 안 걸리면 Unbound 가 재귀를 맡는다.",
      "주황이 이 장의 플러그인이 실제로 하는 일입니다")

# 존 — 먼저 그린다
d.box(20, 130, 300, 330, PAPER, ZS, 0.8, 8)
d.box(34, 134, 152, 14, PAPER, PAPER, 0)
d.t(38, 145, "CLIENT SIDE", 8, SOFT, MONO, "start")

d.box(380, 130, 480, 330, PAPER, ZS, 0.8, 8)
d.box(394, 134, 152, 14, PAPER, PAPER, 0)
d.t(398, 145, "B1TD CLOUD", 8, SOFT, MONO, "start")

# 경로 — 노드보다 먼저
d.path("M 185 210 L 185 244", MUTED, 1.4, m="ar")
d.path("M 320 278 L 453 278", ACC, 1.8, m="acc")
d.t(386, 268, "DoT", 11, ACC, MONO)
d.path("M 320 378 L 390 378 L 390 302 L 453 302", ACC, 1.6, m="acc")
d.path("M 595 210 L 595 244", MUTED, 1.4, m="ar")
d.path("M 595 322 L 595 356", MUTED, 1.4, m="ar")
d.path("M 735 284 L 801 284 L 801 356", INFO, 1.4, m="info")
d.t(745, 276, "정책 없으면", 11, INFO, KR, "start")

# 클라이언트 쪽 — 둘은 사슬이 아니라 대안이다
d.box(50, 170, 270, 40, PAPER2, RULE, 1.0)
d.t(185, 195, "스텁 리졸버 → 루프백", 12, INK, KR, "middle", 600)

d.tone(50, 246, 270, 64, ACC, 6, "12", 1.4)
d.t(185, 270, "기기 안의 CoreDNS", 13, ACC, KR, "middle", 600)
d.t(185, 292, "rewrite edns0 로 신원을 붙인다", 11, ACC, MONO)

d.t(185, 332, "또는 사이트 단위로", 11, SOFT, KR)

d.box(50, 346, 270, 64, PAPER2, RULE, 1.0)
d.t(185, 370, "DNS Forwarding Proxy", 13, INK, MONO, "middle", 600)
d.t(185, 392, "VM 또는 컨테이너 · 같은 일을 대신한다", 11, MUTED, KR)

# 클라우드 쪽
d.box(455, 170, 280, 40, PAPER2, RULE, 1.0)
d.t(595, 195, "애니캐스트 · 로드밸런서", 12, INK, KR, "middle", 600)

d.tone(455, 246, 280, 76, ACC, 6, "12", 1.4)
d.t(595, 270, "클라우드의 CoreDNS", 13, ACC, KR, "middle", 600)
d.t(595, 291, "policy 플러그인이 정책을 찾는다", 11, ACC, KR)
d.t(595, 311, "컨테이너 · 쿠버네티스가 관리", 11, MUTED, KR)

d.tone(455, 358, 280, 64, BAD, 6, "12", 1.4)
d.t(595, 382, "정책에 걸리면", 12, BAD, KR, "middle", 600)
d.t(595, 404, "오류 또는 안내 페이지로 유도", 11, BAD, KR)

d.box(755, 358, 92, 64, PAPER2, INFO, 1.0)
d.t(801, 382, "Unbound", 12, INFO, MONO, "middle", 600)
d.t(801, 404, "완전 재귀", 11, MUTED, KR)

d.box(20, 480, 840, 56, PAPER, RULE, 0.8)
d.t(36, 504, "왜 이 회사가 CoreDNS 를 두 자리에 다 썼는가", 12, INK, KR, "start", 600)
d.t(36, 526, "클라이언트에서는 자원을 거의 안 쓰면서 재작성과 DoT 를 하고, 클라우드에서는 수평 확장과 자체 플러그인을 얻는다",
     11, MUTED, KR, "start")

d.legend(548, [("이 장의 플러그인", ACC), ("정책 적용", BAD), ("재귀는 밖에 맡긴다", INFO)])
d.save("07-01.bloxone-arch.svg")
