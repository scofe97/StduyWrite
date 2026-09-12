# 03-01 §2 — 발신자에게는 같은 타임아웃인데 패킷이 사라지는 자리가 다르다.
# 타입 스펙: type-data-flow — 노드 사이를 흐르는 패킷의 경로 위에 소멸 지점을 찍고,
#           그 지점을 보려면 어디에 캡처를 꽂아야 하는지를 아래 칸이 짝지어 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, WARN, OK, KR, MONO

W, H = 880, 460
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 03-01 §2",
      "같은 타임아웃, 다른 소멸 지점",
      "h1 에서 h2 로 가는 경로 위에서 세 고장이 각각 다른 자리에 패킷을 죽인다. 발신자가 보는 증상만으로는 갈리지 않는다.",
      "캡처를 어디에 꽂느냐가 세 고장을 가른다")

NW, NH, Y = 178, 56, 112
X0, STRIDE = 24, 218
nodes = [("h1", "10.4.1.10"), ("r1", "게이트웨이"), ("r2", "리턴 없음"), ("h2", "10.4.2.10")]

for i, (name, sub) in enumerate(nodes):
    x = X0 + i * STRIDE
    d.box(x, Y, NW, NH, PAPER2, RULE, 1.0, 8)
    d.t(x + NW / 2, Y + 24, name, 14, INK, MONO, "middle", 600)
    d.t(x + NW / 2, Y + 44, sub, 11, MUTED, KR)

# 포워드 — 완주한다
for i in range(3):
    x1 = X0 + i * STRIDE + NW
    x2 = X0 + (i + 1) * STRIDE
    d.arrow([(x1, Y + 28), (x2 - 4, Y + 28)], OK, "ok", 1.4)
d.t(X0, Y - 12, "포워드 — 완주한다", 12, OK, KR, "start", 600)

# 리턴 — r2 에서 죽는다
d.path(f"M {X0 + 3 * STRIDE + NW / 2} {Y + NH} V {Y + NH + 34} H {X0 + 2 * STRIDE + NW / 2} V {Y + NH + 10}",
       BAD, 1.5, m="bad")
d.chip(X0 + 2 * STRIDE + NW / 2 + 112, Y + NH + 34, "리턴은 r2 에서 죽는다", BAD)

ROW, RW, RH, RG = 252, 264, 128, 22
faults = [
    (BAD,  "리턴 라우트 누락", "r2 의 테이블에 h1 대역 없음",
     "h2 에 꽂으면 보인다", "request 도달 · reply 발신 · r2 반송"),
    (WARN, "ip_forward=0",    "r1 이 라우터이길 그만둠",
     "r1 에 꽂아야 보인다", "h2 는 0 패킷 · r1 에만 request"),
    (SOFT, "기본 게이트웨이 누락", "h1 커널이 보내기 전에 거절",
     "캡처가 필요 없다", "타임아웃이 아니라 즉시 에러"),
]
for i, (c, title, cause, where, what) in enumerate(faults):
    x = X0 + i * (RW + RG)
    d.tone(x, ROW, RW, RH, c, 8, "10", 1.2)
    d.t(x + 16, ROW + 28, title, 14, c, KR, "start", 600)
    d.t(x + 16, ROW + 52, cause, 12, MUTED, KR, "start")
    d.t(x + 16, ROW + 82, where, 12, INK, KR, "start", 600)
    d.t(x + 16, ROW + 106, what, 11, MUTED, KR, "start")

d.t(24, 432, "즉시 에러는 내 테이블에 길이 없다는 뜻이고, 타임아웃은 보냈는데 소식이 없다는 뜻이다", 12, ACC, KR, "start", 600)
d.save("03-01.where-it-dies.svg")
