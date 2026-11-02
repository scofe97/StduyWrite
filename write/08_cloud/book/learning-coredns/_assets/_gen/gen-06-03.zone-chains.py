# 06-03 §6 — 서버 블록 앞에 존을 여럿 적으면 존마다 독립 체인이 생기고 쿠버네티스 캐시가 그만큼 겹친다.
# 본문 근거: 이 노트 §6 「나누면 메모리를 더 씁니다」(원서 요지 — 블록 앞에 나열한 존마다 독립 플러그인 체인, 쿠버네티스 캐시 중복).
#            존 이름 셋은 원서 변수 CLUSTER_DOMAIN REVERSE_CIDRS 자리에 넣은 예시다(본문의 in-addr.arpa · ip6.arpa 언급).
# 원서 근거: 6장 "Kubernetes" p.33("A Better Configuration", plug-in chain duplication).
# 타입 스펙: type-architecture — 설정 한 줄이 구성요소 몇 벌로 펼쳐지는지가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 440
d = D(W, H, "LEARNING COREDNS · 06-03 §6",
      "1.8.5 전엔 존 셋이면 체인도 셋",
      "1.8.5 전에는 서버 블록 앞에 나열한 존마다 독립 플러그인 체인이 서서 API 캐시가 존 수만큼 겹쳤다. "
      "1.8.5 부터는 같은 블록의 존이 플러그인 인스턴스를 공유한다.",
      "주황 띠가 같은 데이터를 겹쳐 담던 자리입니다")

d.box(20, 140, 250, 110, PAPER2, RULE, 1.0, 8)
for j, txt in enumerate(["cluster.local", "in-addr.arpa", "ip6.arpa {"]):
    d.t(36, 172 + j * 26, txt, 13, INK, MONO, "start", 600)
d.t(145, 276, "존 셋 · 체인 셋", 13, MUTED, KR)
d.path("M 272 195 L 316 195", MUTED, 1.4, m="ar")

d.tone(322, 196, 544, 64, ACC, 8, "0E", 1.4)
for i, zone in enumerate(["cluster.local", "in-addr.arpa", "ip6.arpa"]):
    x = 330 + i * 180
    d.t(x + 8, 128, f"체인 {i + 1}", 12, SOFT, KR, "start", 600)
    d.t(x + 8, 144, zone, 12, MUTED, MONO, "start")
    d.box(x, 152, 170, 36, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, 175, "errors · health", 12, MUTED, MONO, "start")
    d.box(x, 202, 170, 52, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, 224, "kubernetes", 13, ACC, MONO, "start", 600)
    d.t(x + 12, 244, f"API 캐시 사본 {i + 1}", 12, MUTED, KR, "start")
    d.box(x, 266, 170, 36, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, 289, "나머지 플러그인", 12, MUTED, KR, "start")

d.t(20, 344, "1.8.5 전 · 존 수만큼 사본 · 1.8.5 부터는 한 벌", 13, MUTED, KR, "start")
d.t(20, 366, "존 이름은 예시 · 변수 CLUSTER_DOMAIN REVERSE_CIDRS 자리", 12, SOFT, KR, "start")

d.legend(384, [("1.8.5 전에 겹치던 API 캐시", ACC)])
d.save("06-03.zone-chains.svg")
