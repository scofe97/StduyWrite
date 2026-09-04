# 06-04 §5 — autopath 는 검색 경로 순회를 네트워크에서 CoreDNS 내부로 옮긴다.
# 원문 근거: "CoreDNS will figure out the search path on the server side. When it recognizes a query
#            that looks like it is the first in a search ... it will iterate over that search path
#            itself, internally. This is much, much faster because there is no network involved;
#            it's just an internal loop. If it gets a result, it will return a CNAME pointing to that
#            result." / 대가: "To figure out the search path, CoreDNS needs to know the namespace of
#            the client pod. The only information it has on the client pod is the source IP address
#            of the query ... Enabling pods verified mode does this, but it increases the memory".
# 타입 스펙: type-swimlane — 레인을 건너는 넘겨받음이 논지이고, 반복이 어느 레인에 있는지가 결론이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 540
d = D(W, H, "LEARNING COREDNS · 06-04 §5",
      "반복이 네트워크에서 서버 안으로 옮겨 간다",
      "위 레인은 autopath 없이, 아래 레인은 켜고 난 뒤다. 같은 다섯 번의 시도가 "
      "네트워크 왕복에서 CoreDNS 안의 루프로 자리를 옮긴다.",
      "주황 상자가 옮겨 간 반복입니다")

LANES = [("BEFORE", "autopath 없이", 116), ("AFTER", "autopath 를 켜고", 260)]
LH = 112
LX = 150

for nm, sub, y in LANES:
    d.box(LX, y, 710, LH, PAPER, RULE, 0.8, 6)
    d.t(20, y + 34, nm, 9, SOFT, MONO, "start", 600)
    d.t(20, y + 56, sub, 12, MUTED, KR, "start")

d.line(LX, 244, 860, 244, RULE, 1.0)

d.box(LX + 24, 140, 176, 60, PAPER2, RULE, 1.0)
d.t(LX + 112, 168, "클라이언트", 14, INK, KR, "middle", 600)
d.t(LX + 112, 188, "검색 경로를 돈다", 12, MUTED, KR)
d.tone(LX + 264, 140, 200, 60, BAD, 6, "12", 1.4)
d.t(LX + 364, 168, "네트워크 왕복 여섯", 14, BAD, KR, "middle", 600)
d.t(LX + 364, 188, "실패 다섯 + 성공 하나", 12, BAD, KR)
d.box(LX + 528, 140, 158, 60, PAPER2, RULE, 1.0)
d.t(LX + 607, 168, "CoreDNS", 14, INK, MONO, "middle", 600)
d.t(LX + 607, 188, "여섯 번 처리", 12, MUTED, KR)
d.arrow([(LX + 200, 170), (LX + 260, 170)], MUTED, "ar", 1.4)
d.arrow([(LX + 464, 170), (LX + 524, 170)], MUTED, "ar", 1.4)

d.box(LX + 24, 284, 176, 60, PAPER2, RULE, 1.0)
d.t(LX + 112, 312, "클라이언트", 14, INK, KR, "middle", 600)
d.t(LX + 112, 332, "한 번만 묻는다", 12, MUTED, KR)
d.box(LX + 264, 284, 200, 60, PAPER2, RULE, 1.0)
d.t(LX + 364, 312, "네트워크 왕복 하나", 14, OK, KR, "middle", 600)
d.t(LX + 364, 332, "CNAME 과 A 가 함께", 12, MUTED, KR)
d.tone(LX + 528, 284, 158, 60, ACC, 6, "12", 1.4)
d.t(LX + 607, 310, "CoreDNS", 14, ACC, MONO, "middle", 600)
d.t(LX + 607, 332, "내부 루프 다섯", 12, ACC, KR)
d.arrow([(LX + 200, 314), (LX + 260, 314)], MUTED, "ar", 1.4)
d.arrow([(LX + 464, 314), (LX + 524, 314)], MUTED, "ar", 1.4)

d.tone(20, 396, 840, 56, ACC, 6, "0E", 1.4)
d.t(440, 420, "대가 — 클라이언트 네임스페이스를 출발지 IP 로 알아내야 해서 pods verified 가 필요하다", 13, ACC, KR)
d.t(440, 440, "그 모드는 2절에서 본 대로 메모리를 두 배 안팎 더 쓴다", 12, MUTED, KR)

d.legend(476, [("옮겨 간 반복", ACC), ("없앤 왕복", BAD), ("남은 왕복 하나", OK)])
d.save("06-04.autopath-move.svg")
