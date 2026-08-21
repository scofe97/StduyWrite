# 02-02.nat-table-traverse — 지나는 자리와 그 직후 패킷 상태를 세로로 짝지운다
# 본문 요구: "패킷 하나가 nat 테이블을 지나는 동안 — 어느 규칙에 걸려 어느 필드가 바뀌는가"
# 타입 스펙: type-swimlane.md 레인 둘. 여섯 자리라 글자를 한 단 줄이고 fit 으로 강제한다.
#           마지막 칸은 조건부라 점선 표시를 덧붙인다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 636
d = D(W, H, "nat TABLE · WHERE IT LANDS, WHAT CHANGES",
      "패킷 하나가 nat 테이블을 지나는 동안 — 어느 규칙에 걸려 어느 필드가 바뀌는가",
      "위는 지나는 자리와 거기서 걸린 규칙, 아래는 그 직후 패킷 상태다. 마지막 칸은 노드에서 온 요청일 때만 일어난다.",
      lead="위는 지나는 자리와 걸린 규칙 · 아래는 그 직후 패킷 상태 (kind 실측)")

BW, BH, GAP = 140, 104, 16
CX = [40 + BW // 2 + i * (BW + GAP) for i in range(6)]           # 110 266 422 578 734 890
TOP, BOT = 292, 460

ddx.band(d, 104, 588, "체인을 갈아타는 동안 헤더는 그대로이고, 바뀌는 자리는 두 곳뿐이다")
ddx.lane_pair(d, CX, TOP, BOT, BW, BH,
              "지나는 자리와 거기서 걸린 규칙", "그 직후 패킷 상태 — kind 실측",
              [("PREROUTING", "nat 첫 자리", "-j KUBE-SERVICES"),
               ("KUBE-SERVICES", "-d 10.96.192.224/32", "-j KUBE-SVC-LOLE4…"),
               ("KUBE-SVC-LOLE4…", "! -s 10.244.0.0/16 먼저", "Pod 출발지라 불일치"),
               ("KUBE-SEP-2MJG…", "확률 0.3333 으로 도달", "-j DNAT"),
               ("KUBE-POSTROUTING", "! --mark 0x4000", "-j RETURN"),
               ("노드에서 온 요청이면", "! -s 10.244.0.0/16 매치", "KUBE-MARK-MASQ")],
              [("src 10.244.1.11", "dst 10.96.192.224:8080", "mark 0x0"),
               ("헤더 그대로", "체인만 갈아탄다", "mark 0x0"),
               ("마크가 안 붙는다", "조건 불일치로 건너뜀", "mark 0x0 유지"),
               ("목적지가 바뀐다", "dst → 10.244.1.66:8080", "conntrack 에 기록"),
               ("출발지는 그대로", "src 10.244.1.11", "MASQUERADE 안 탐"),
               ("출발지도 바뀐다", "src → 10.244.1.1:39387", "--random-fully")],
              ["도착", "점프", "건너뜀", "변환", "통과", "재작성"],
              sizes=(11, 9, 9))

# 마지막 칸은 조건부 — 늘 일어나지 않는다
lx = CX[5] - BW // 2 - 8
d.o.append(f'<rect x="{lx}" y="{TOP-BH//2-10}" width="{BW+16}" height="{BOT+BH//2+10-(TOP-BH//2-10)}" '
           f'rx="8" fill="none" stroke="{WARN}" stroke-width="1.4" stroke-dasharray="7 6"/>')
d.t(CX[5], BOT + BH // 2 + 30, "노드에서 온 요청일 때만", 11, WARN, KR)

d.t(36, 560, "체인을 몇 번 갈아타도 헤더는 그대로다 — 실제로 바뀌는 자리는 DNAT 한 번과 "
             "조건부 MASQUERADE 한 번뿐이다", 12, MUTED, KR, "start")
d.legend(604, [("지나는 자리", INFO), ("그 직후 상태", ACC), ("조건부", WARN)])
d.save("02-02.nat-table-traverse.svg")
print("ok nat-table-traverse")
