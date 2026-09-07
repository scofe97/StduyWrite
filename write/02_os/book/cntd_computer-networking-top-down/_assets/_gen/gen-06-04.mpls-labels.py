# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 MPLS 구간을 묶고 관계에 라벨을 단다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.5.1 Figure 6.29 —
#   토폴로지(R5·R6 은 보통 IP, R1~R4 는 MPLS, D 는 R3 에 A 는 R1 에 붙음)와 네 라우터의 포워딩 표 값 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 548
d = D(W, H, "SECTION 6.5.1 · MPLS-ENHANCED FORWARDING",
      "라벨을 갈아 끼우며 넘깁니다",
      "MPLS 라우터는 들어온 라벨로 표를 찾아 나가는 라벨로 바꿔 달고 내보낸다. IP 주소를 꺼내 최장 접두어 일치를 하지 않는다.",
      "토폴로지와 표 값은 원문 Figure 6.29 그대로입니다")

d.tone(184, 108, 480, 164, INFO, 8, "0A", 1.0)
d.t(240, 128, "MPLS 구간", 11, INFO, KR, "middle", 600)

NODES = [("R6", 40, 140, MUTED), ("R5", 40, 210, MUTED), ("R4", 200, 148, ACC),
         ("R3", 360, 148, INFO), ("R2", 360, 210, INFO), ("R1", 520, 210, INFO),
         ("D", 680, 148, OK), ("A", 680, 210, OK)]
for name, x, y, c in NODES:
    w = 72 if name in ("A", "D") else 88
    d.tone(x, y, w, 44, c, 6, "1E" if c is ACC else "14", 1.5 if c is ACC else 1.1)
    d.t(x + w / 2, y + 28, name, 13, c, MONO, "middle", 600)

d.path("M 128 162 L 162 162 L 162 168 L 196 168", MUTED, 1.2, m="ar")
d.path("M 128 232 L 162 232 L 162 180 L 196 180", MUTED, 1.2, m="ar")
d.path("M 288 170 L 356 170", INFO, 1.3, m="info")
d.path("M 244 192 L 244 232 L 356 232", INFO, 1.3, m="info")
d.path("M 448 162 L 564 162 L 564 206", INFO, 1.3, m="info")
d.path("M 448 232 L 516 232", INFO, 1.3, m="info")
d.path("M 608 232 L 676 232", OK, 1.3, m="ok")
d.path("M 404 148 L 404 98 L 716 98 L 716 144", OK, 1.3, m="ok")

d.chip(322, 158, "10 · 12", INFO, 10)
d.chip(244, 214, "8", INFO, 10)
d.chip(564, 182, "6", INFO, 10)
d.chip(482, 244, "6", INFO, 10)
d.chip(560, 98, "9", OK, 10)
d.t(84, 268, "보통 IP 라우터", 10, SOFT, KR)

TABLES = [
    (24, "R4 의 표", [("—", "10", "A", "0"), ("—", "12", "D", "0"), ("—", "8", "A", "1")], ACC),
    (270, "R3 의 표", [("10", "6", "A", "1"), ("12", "9", "D", "0")], INFO),
    (516, "R2 의 표", [("8", "6", "A", "0")], INFO),
    (762, "R1 의 표", [("6", "—", "A", "0")], INFO),
]
TY, TW, TH = 300, 226, 128
for x, title, rows, c in TABLES:
    d.box(x, TY, TW, TH, PAPER2, f"{c}55", 1.4 if c is ACC else 1.0, 6)
    d.t(x + 14, TY + 24, title, 11, c, KR, "start", 600)
    d.line(x + 14, TY + 34, x + TW - 14, TY + 34, RULE, 0.8)
    for j, head in enumerate(["들어온", "나가는", "목적지", "포트"]):
        d.t(x + 14 + j * 54, TY + 54, head, 10, SOFT, KR, "start")
    for i, row in enumerate(rows):
        y = TY + 78 + i * 22
        for j, v in enumerate(row):
            d.t(x + 14 + j * 54, y, v, 11, INK if j < 2 else MUTED, MONO, "start")

d.line(24, 452, W - 48, 452, RULE, 0.8)
d.t(24, 472, "R4 는 A 로 가는 길을 둘 갖습니다. 포트 0 으로 라벨 10 을 달아 R3 을 거치거나, 포트 1 로 라벨 8 을 달아 R2 를 거칩니다.",
     11, MUTED, KR, "start")
d.t(24, 490, "IP 라우팅이었다면 최소 비용 경로 하나만 썼을 자리입니다. 이 갈림이 MPLS 트래픽 엔지니어링의 출발점입니다.",
     11, MUTED, KR, "start")

d.legend(508, [("경로가 둘인 자리", ACC), ("MPLS 라우터", INFO), ("목적지", OK), ("보통 IP 라우터", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-04.mpls-labels.svg"
d.save(out)
print("→", out)
