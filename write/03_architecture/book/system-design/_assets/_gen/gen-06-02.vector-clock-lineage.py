# 타입 스펙: type-process — 서버 Sx·Sy·Sz 가 쓴 버전 다섯을 위에서 아래로 놓고, 갈라졌다 합쳐지는 벡터 시계 값을 노드마다 적는다. focal 은 충돌 표지.
# 사실 출처: 추출본 v2.txt 1727~1739행(D1[(Sx,1)] → D2([Sx,2]) → D3([Sx,2],[Sy,1]) · D4([Sx,2],[Sz,1]) → D5([Sx,3],[Sy,1],[Sz,1])),
#   Dynamo 논문 §4.4 Figure 3(https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf).
# Layout conventions: 노드 폭 300·높이 64, 중심 x=480(D1·D2·D5)·270(D3)·690(D4), 줄 y=116·220·372·516. 갈림·합침 수평선 y=332·484. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER2, KR, MONO

W, H = 960, 688
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-02 §1",
      "서버마다 카운터를 올려 가며 갈라진 버전이 합쳐진다",
      "D3 와 D4 는 서로의 카운터를 모두 넘지 못해 충돌이고, D5 는 둘을 읽은 클라이언트가 Sx 에 써서 모두를 넘는다.",
      "쓴 서버의 카운터만 1 오르고, 다른 서버의 카운터는 읽은 값 그대로")

NW, NH = 300, 64


def node(cx, y, title, clock, c, focal=False):
    x = cx - NW // 2
    if c == MUTED:
        d.box(x, y, NW, NH, PAPER2, MUTED, 1.2, 6)
    else:
        d.tone(x, y, NW, NH, c, 6, "12", 1.2)
    d.t(cx, y + 26, title, 14, INK, KR, "middle", 600)
    d.t(cx, y + 48, clock, 13, c if c != MUTED else MUTED, MONO)


# 화살표를 먼저 그려 노드 뒤로 보낸다
d.arrow([(480, 180), (480, 216)], MUTED, "ar", 1.5)
d.t(496, 204, "Sx 쓰기", 13, MUTED, KR, "start")
d.arrow([(480, 284), (480, 332), (270, 332), (270, 368)], MUTED, "ar", 1.5)
d.t(286, 360, "Sy 쓰기", 13, MUTED, KR, "start")
d.arrow([(480, 332), (690, 332), (690, 368)], MUTED, "ar", 1.5)
d.t(706, 360, "Sz 쓰기", 13, MUTED, KR, "start")
d.arrow([(270, 436), (270, 484), (480, 484), (480, 512)], MUTED, "ar", 1.5)
d.line(690, 436, 690, 484, MUTED, 1.5)
d.line(690, 484, 480, 484, MUTED, 1.5)
d.t(496, 504, "Sx 조정 쓰기", 13, MUTED, KR, "start")

node(480, 116, "D1", "D1([Sx,1])", MUTED)
node(480, 220, "D2", "D2([Sx,2])", INFO)
node(270, 372, "D3", "D3([Sx,2],[Sy,1])", WARN)
node(690, 372, "D4", "D4([Sx,2],[Sz,1])", WARN)
node(480, 516, "D5", "D5([Sx,3],[Sy,1],[Sz,1])", OK)

d.chip(480, 404, "충돌", ACC, 12)

d.legend(H - 56, [("선행 버전", INFO), ("충돌한 형제", WARN), ("조정한 결과", OK), ("충돌 표지", ACC)])
d.save("06-02.vector-clock-lineage.svg")
