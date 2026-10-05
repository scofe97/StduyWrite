# 14-03 §4 — 원서 Figure 14-13 을 대신한다.
# 사실 출처(ch14.txt §14.8.1): dupthresh 3. 약한 재정렬(인접한 두 패킷이 자리를 바꿈)은 중복 ACK 하나만 만들어
#   무시되고 TCP 가 극복한다. 심한 재정렬에서는 패킷 4 가 세 자리 뒤처져 중복 ACK 셋이 생기고, 빠른 재전송이
#   불려 수신자에 중복 세그먼트가 생긴다.
# 축약: 왼쪽 패널의 패킷 번호는 원서 본문에 없어, 오른쪽과 같은 4 가 한 자리만 뒤처진(4·5 가 바뀐) 경우로 대비했다.
#       ACK 표기는 원서 Figure 14-12·14-14 와 같이 '이미 도착한 것'(A3 = 3 까지 도착)이다.
#       오른쪽에서 원본 4 와 재전송본 4 중 어느 쪽이 먼저 닿는지는 원서 본문에 없어, 원본이 먼저 닿는 쪽을 그렸다.
# 타입 스펙: type-sequence — 송신자·망·수신자 세 레인을 두 패널에 나란히 둔다. 망 레인이 있어야 보낸 순서와
#           도착 순서를 수평 화살표만으로 나눠 그릴 수 있다. 반환(ACK)은 점선.
#           focal 은 오른쪽 패널의 불필요한 빠른 재전송 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 920, 728
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-03 §4",
      "재정렬 깊이가 중복 ACK 문턱을 넘는가",
      "송신자가 4·5·6(·7) 을 차례로 보냈다. 왼쪽은 4 와 5 가 자리를 바꿔 도착해 중복 ACK 가 하나만 생기고, 문턱 3 에 못 미쳐 무시된다. "
      "오른쪽은 4 가 세 자리 뒤처져 5·6·7 이 먼저 닿고 중복 ACK 가 셋 쌓인다. 송신자는 4 를 빠르게 재전송하고, 늦게 닿은 원본 4 때문에 수신자는 4 를 두 번 받는다. "
      "ACK 번호는 원서 그림처럼 이미 도착한 마지막 패킷을 가리킨다.",
      "같은 재정렬도 깊이가 dupthresh 를 넘으면 손실로 읽힙니다")

STRIDE = 40
Y0 = 216
PANELS = [(12, "약한 재정렬 · 4·5 자리 바꿈"), (468, "심한 재정렬 · 4 가 세 자리 뒤처짐")]
OFF = (56, 196, 336)
BOT = Y0 + 10 * STRIDE + 24
LX = {}
for pi, (px, title) in enumerate(PANELS):
    d.t(px + 12, 112, title, 13, INK, KR, "start", 600)
    for name, off in zip(("송신자", "망", "수신자"), OFF):
        x = px + off
        LX[(pi, name)] = x
        d.box(x - 48, 128, 96, 40, PAPER2, RULE, 1.0)
        d.t(x, 153, name, 12, INK, KR, "middle", 600)
        d.line(x, 174, x, BOT, RULE, 1.0, "3 6")
d.line(460, 104, 460, BOT, RULE, 0.8)

def msg(p, a, b, label, row, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
    x1, x2 = LX[(p, a)], LX[(p, b)]; dd = 1 if x2 > x1 else -1
    y = Y0 + row * STRIDE
    d.path(f"M {x1 + 8 * dd} {y} L {x2 - 10 * dd} {y}", c, 1.5, m=mk, dash=dash)
    mx = lx if lx is not None else (x1 + x2) / 2
    d.t(mx, y - 7, label, 12, c, _kr(label), "middle", 600)
    if sub: d.t(mx, y + 14, sub, 11, MUTED, _kr(sub))

def note(p, row, txt, c):
    d.t(LX[(p, "수신자")] + 14, Y0 + row * STRIDE + 4, txt, 11, c, _kr(txt), "start")

S, N, R = "송신자", "망", "수신자"
# 왼쪽 — 약한 재정렬
ack_x = lambda p: (LX[(p, N)] + LX[(p, R)]) / 2
msg(0, S, N, "4 · 5 · 6", 0, INFO, "info")
msg(0, N, R, "5", 1, INFO, "info")
msg(0, R, S, "A3", 2, WARN, "warn", "5 4", sub="중복 1개 · 문턱 미달", lx=ack_x(0))
msg(0, N, R, "4", 3, INFO, "info")
msg(0, R, S, "A5", 4, MUTED, "ar", "5 4", lx=ack_x(0))
msg(0, N, R, "6", 5, INFO, "info")
msg(0, R, S, "A6", 6, MUTED, "ar", "5 4", lx=ack_x(0))
note(0, 3, "구멍 메움", INFO)

# 오른쪽 — 심한 재정렬
msg(1, S, N, "4 · 5 · 6 · 7", 0, INFO, "info")
for k, n in enumerate(("5", "6", "7")):
    msg(1, N, R, n, 1 + 2 * k, INFO, "info")
    msg(1, R, S, "A3", 2 + 2 * k, WARN, "warn", "5 4", lx=ack_x(1),
        sub="중복 3개 · 문턱 도달" if k == 2 else None)
msg(1, S, N, "4 빠른 재전송", 7, ACC, "acc")
msg(1, N, R, "4 원본", 8, INFO, "info")
msg(1, R, S, "A7", 9, MUTED, "ar", "5 4", lx=ack_x(1))
msg(1, N, R, "4 재전송본", 10, ACC, "acc")
note(1, 10, "중복 4", BAD)

d.legend(H - 56, [("불필요한 빠른 재전송", ACC), ("중복 ACK", WARN), ("수신자 중복 수신", BAD), ("데이터", INFO)])
d.save("14-03.reordering-dupthresh.svg")
