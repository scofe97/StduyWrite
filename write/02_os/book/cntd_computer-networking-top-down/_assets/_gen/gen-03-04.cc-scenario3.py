# 03-04 §4 시나리오 3 — 원문 Figure 3.47·3.48. 호스트 넷이 겹치는 두 홉 경로로 보내고, A–C 는 R2 에서 B–D 와 경쟁한다.
# 본문 근거: "부하가 아주 작을 때는 처리량이 부하를 따라 올라가고 · 아주 커지면 R2 에서 B–D 도착률이 A–C 보다 훨씬 커져
#   A–C 가 R2 를 통과하는 양이 0 으로 간다 · 두 번째 홉에서 버려지면 첫 홉이 쓴 일이 통째로 낭비". 곡선은 원문 그림의 개략이다.
# 타입 스펙: type-line — 제공 부하에 따른 A–C 처리량 곡선. 위쪽 띠의 토폴로지는 두 홉과 경쟁 지점을 알리는 문맥이다.
import sys; sys.path.insert(0, ".")
from _cc_common import *

W, H = 1000, 560
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §4",
      "시나리오 3 — 부하를 올리면 처리량이 오히려 0 으로 갑니다",
      "원문 Figure 3.47·3.48. 두 번째 홉에서 버려지는 패킷은 첫 홉이 쓴 전송 용량을 통째로 낭비한다. 이것이 혼잡 붕괴다.",
      "A–C 는 R1 과 R2 를 지나고, R2 에서 B–D 와 버퍼를 놓고 경쟁합니다")

ty = 150
host(d, 60, ty, "A"); router(d, 190, ty, "R1"); router(d, 330, ty, "R2", None, BAD); host(d, 470, ty, "C")
link(d, 82, ty, 172, ty, ACC, "A–C 1홉", -10); link(d, 208, ty, 312, ty, ACC, "2홉", -10); link(d, 348, ty, 448, ty, ACC)
host(d, 330, ty - 52, "B"); link(d, 330, ty - 38, 330, ty - 18, BAD)
router(d, 470, ty + 72, "R3"); d.path(f"M 330 {ty + 16} L 330 {ty + 72} L 452 {ty + 72}", BAD, 1.3, m="bad"); d.t(400, ty + 66, "B–D 가 R2 를 가득 채움", 11, BAD, KR)
d.t(560, ty - 14, "부하가 커지면 R2 에서 B–D 도착률이 A–C 보다 훨씬 커짐", 11, MUTED, KR, "start")
d.t(560, ty + 4, "R2 가 A–C 패킷을 버리면 R1 이 그것을 나른 일이 낭비", 11, BAD, KR, "start")
d.t(560, ty + 22, "R1 이 그냥 버리고 놀았어도 망의 형편은 똑같이 나빴을 것", 11, MUTED, KR, "start")

xt = [(0, "작음"), (0.5, ""), (1, "아주 큼")]
c = Chart(d, 24, 196, 952, 300, "λ'in (A–C 의 제공 부하)", "A–C 처리량 λout", xt, [(0, "0"), (0.5, ""), (1, "")])
pts = [(0, 0), (0.12, 0.28), (0.24, 0.5), (0.36, 0.62), (0.48, 0.58), (0.6, 0.44), (0.72, 0.28), (0.84, 0.13), (0.96, 0.03)]
c.series(pts, ACC, focal=True)
c.note(0.3, 0.8, "부하를 따라 오르다가", ACC, "start")
c.note(0.66, 0.56, "R2 에서 밀려 0 으로 — 네 번째 대가", BAD, "start")

d.legend(H - 44, [("A–C 처리량", ACC), ("경쟁·낭비가 생기는 자리", BAD)])
d.save("03-04.cc-scenario3.svg")
print("ok cc-scenario3")
