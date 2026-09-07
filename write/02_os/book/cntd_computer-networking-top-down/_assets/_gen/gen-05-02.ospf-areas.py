# 타입 스펙: type-architecture — 영역 셋과 백본, 그리고 영역을 넘는 경로가 반드시 지나는 자리.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.3 OSPF (Support for hierarchy within a single AS)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 580
d = D(W, H, "SECTION 5.3 · OSPF AREAS",
      "AS 안에 다시 경계를 긋습니다",
      "OSPF 가 하나의 AS 를 영역으로 나눈 구조. 링크 상태 브로드캐스트는 영역 안에서만 돌고, 영역을 넘는 경로는 반드시 백본 영역을 거친다.",
      "AS 를 나눈 이유를 AS 안에서 한 번 더 반복합니다")

AREAS = [(40, 170, "영역 1", "링크 상태는 여기서만 돕니다"),
         (370, 500, "영역 2", "자기 영역의 지도만 압니다"),
         (700, 830, "영역 3", "밖은 경계 라우터에게 맡깁니다")]
AW, AY, AH = 260, 112, 96
BY, BH = 232, 40          # 영역 경계 라우터
KY, KH = 296, 92          # 백본

for x, cx, name, sub in AREAS:
    d.box(x, AY, AW, AH, PAPER2, RULE, 1.0, 9)
    d.t(cx, AY + 32, name, 12, INK, KR, "middle", 600)
    d.t(cx, AY + 54, sub, 11, MUTED, KR)
    d.t(cx, AY + 76, "각자 다익스트라", 11, SOFT, KR)
    # 경계 라우터는 자기 영역 바로 아래에
    d.box(cx - 78, BY, 156, BH, PAPER, ACC, 1.4, 6)
    d.t(cx, BY + 25, "영역 경계 라우터", 11, ACC, KR)
    d.path(f"M {cx} {AY + AH} L {cx} {BY}", MUTED, 1.2)
    d.path(f"M {cx} {BY + BH} L {cx} {KY}", ACC, 1.4)

d.tone(40, KY, 920, KH, ACC, 10, "10", 1.6)
d.t(500, KY + 28, "백본 영역 (area 0)", 13, ACC, KR, "middle", 600)
d.t(500, KY + 50, "모든 영역 경계 라우터를 반드시 포함합니다", 11, MUTED, KR)

# 영역을 넘는 트래픽은 백본 안을 지난다
d.arrow([(190, KY + 74), (810, KY + 74)], INFO, "info", 1.8)
d.t(500, KY + 90, "영역 1 에서 영역 3 으로 가는 트래픽은 여기를 지납니다", 11, INFO, KR)

d.t(30, 434, "라우터는 링크 상태가 바뀔 때마다, 그리고 바뀌지 않아도 최소 30분에 한 번 광고를 다시 뿌립니다.", 11, MUTED, KR, "start")
d.t(30, 454, "RFC 2328 은 이 주기적 재광고가 링크 상태 알고리즘에 견고함을 더한다고 적습니다.", 11, MUTED, KR, "start")
d.t(30, 474, "OSPF 메시지는 IP 위에 직접 실리며 상위 프로토콜 번호는 89 입니다.", 11, SOFT, KR, "start")

d.legend(500, [("백본과 영역 경계", ACC), ("영역을 넘는 경로", INFO), ("영역 내부", MUTED)])
d.t(960, 556, "KUROSE-ROSS 9E 5.3 · RFC 2328", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.ospf-areas.svg"
d.save(out)
print("→", out)
