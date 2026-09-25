# 03-02 학습 목표 뒤 전체 지도 — 동적 라우팅 고장을 추적하는 사다리 네 칸.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(번호 · 단계 이름 · 확인할 질문 · 그 칸을 보는
#           명령)이 반복되고 화살표가 추적 순서를 나른다. 세로 stride 로 놓아 사다리 형태를 만든다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 444
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 03-02",
      "동적 라우팅 고장을 추적하는 사다리",
      "이웃·광고·수신·설치 네 칸을 순서대로 확인하면 어느 칸에서 끊겼는지가 곧 원인 부위다. 이 편의 두 고장이 각각 1번 칸과 2번 칸에서 끊긴다.",
      "어느 칸에서 끊겼는지 찾으면 원인 부위가 나온다")

RW, RH, GAP, X0, Y0 = 832, 62, 14, 24, 104
rungs = [
    ("1", "이웃과 세션", "상대와 관계가 맺어졌는가",
     "show ip ospf neighbor · show ip bgp summary", BAD, "OSPF area 불일치가 여기서 끊긴다"),
    ("2", "광고", "내가 실제로 내보내고 있는가",
     "show ip bgp neighbors <peer> advertised-routes", BAD, "BGP network 문 누락이 여기서 끊긴다"),
    ("3", "수신", "상대가 받았는가",
     "show ip bgp summary 의 PfxRcd", SOFT, ""),
    ("4", "설치", "라우팅 테이블에 들어갔는가",
     "show ip route ospf · show ip route bgp", SOFT, ""),
]

for i, (n, title, q, cmd, c, note) in enumerate(rungs):
    y = Y0 + i * (RH + GAP)
    if c is BAD:
        d.tone(X0, y, RW, RH, BAD, 8, "10", 1.2)
    else:
        d.box(X0, y, RW, RH, PAPER2, RULE, 1.0, 8)
    d.t(X0 + 18, y + 26, n, 13, c if c is BAD else SOFT, MONO, "start", 600)
    d.t(X0 + 44, y + 26, title, 14, c if c is BAD else INK, KR, "start", 600)
    d.t(X0 + 150, y + 26, q, 12, MUTED, KR, "start")
    d.t(X0 + 18, y + 48, cmd, 11, SOFT, MONO, "start")
    if note:
        d.t(X0 + RW - 18, y + 48, note, 12, c, KR, "end", 600)
    if i < 3:
        d.arrow([(X0 + 30, y + RH), (X0 + 30, y + RH + GAP - 2)], MUTED, "ar", 1.3)

d.t(24, 420, "네 칸이 다 이어져야 통신이 된다 — 04장의 왕복 원리가 동적 라우팅에서도 그대로다",
    12, ACC, KR, "start", 600)
d.save("03-02.tracking-ladder.svg")
