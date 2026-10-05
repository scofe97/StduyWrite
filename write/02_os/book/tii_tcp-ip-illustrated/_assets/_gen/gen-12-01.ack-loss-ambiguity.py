# 12-01 §1 — 패킷이 사라진 경우와 ACK 가 사라진 경우는 송신자에게 똑같이 보인다.
# 원문 12.1.1: ACK 가 버려지면 송신자는 원래 패킷이 버려진 경우와 쉽게 구분하지 못하므로 그냥 다시 보낸다.
#              그러면 수신자는 사본을 둘 이상 받을 수 있고, 순서 번호로 이미 본 것인지 가려 버린다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지를 두 판으로 나란히 놓는다.
#           축약: 스펙의 out-of-scope "lost message" 를 끊긴 선 끝의 ✕ 로 그린다(저장소 cntd 03-03 three-scenarios 관례).
#           송신자 레인 옆 괄호가 타이머 대기 구간이고, 두 판의 괄호와 재전송 줄이 같은 높이라 같은 장면임이 보인다.
#           focal 은 오른쪽 판에서 수신자가 사본을 번호로 버리는 칩 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §1",
      "패킷이 사라졌나, ACK 가 사라졌나",
      "왼쪽은 데이터 패킷이 가는 길에 버려진 경우, 오른쪽은 패킷은 도착했지만 돌아오는 ACK 가 버려진 경우다. "
      "송신자 쪽에서는 두 판 모두 타이머가 만료될 때까지 ACK 를 못 받는 같은 장면이라 둘 다 다시 보낸다. "
      "오른쪽 수신자는 같은 번호를 두 번 받게 되고, 순서 번호로 사본을 알아보고 버린다.",
      "송신자 레인만 보면 두 판이 똑같습니다 — 그래서 수신자 쪽에 번호가 필요합니다")

PANELS = [(24, "가는 패킷이 버려짐"), (472, "돌아오는 ACK 가 버려짐")]
PW = 424
LANE_W = 128
Y_LANE, Y_BOT = 128, 452
Y1, Y_RCV, Y2, Y_RE, Y_DUP, Y_ACK2 = 216, 244, 284, 340, 372, 404
T_TOP, T_BOT = Y1 + 8, Y_RE - 8

def panel(px, title, ack_lost):
    sx, rx = px + 80, px + PW - 80
    d.t(px + PW / 2, 108, title, 13, INK, KR, "middle", 600)
    for x, nm in ((sx, "송신자"), (rx, "수신자")):
        d.box(x - LANE_W / 2, Y_LANE, LANE_W, 36, PAPER2, RULE, 1.0, 6)
        d.t(x, Y_LANE + 23, nm, 13, INK, KR, "middle", 600)
        d.line(x, Y_LANE + 42, x, Y_BOT, RULE, 1.0, "3 6")
    # 1. 첫 전송
    if ack_lost:
        d.path(f"M {sx + 8} {Y1} L {rx - 10} {Y1}", INFO, 1.5, m="info")
    else:
        mid = (sx + rx) / 2
        d.path(f"M {sx + 8} {Y1} L {mid} {Y1}", INFO, 1.5, dash="5 4")
        d.t(mid + 10, Y1 + 5, "✕", 15, BAD, KR, "start", 700)
    d.t((sx + rx) / 2, Y1 - 10, "패킷 #1", 12, INFO, KR, "middle", 600)
    # 2. ACK (오른쪽 판에서만 출발했다가 버려짐)
    if ack_lost:
        mid = (sx + rx) / 2
        d.path(f"M {rx - 8} {Y2} L {mid} {Y2}", MUTED, 1.5, dash="5 4")
        d.t(mid - 10, Y2 + 5, "✕", 15, BAD, KR, "end", 700)
        d.t((sx + rx) / 2 + 40, Y2 - 10, "ACK #1", 12, MUTED, MONO, "middle", 600)
        d.chip(rx, Y_RCV, "#1 처음 받음", OK, 12)
    # 송신자 타이머 괄호 — 두 판이 같은 높이
    d.path(f"M {sx - 14} {T_TOP} H {sx - 22} V {T_BOT} H {sx - 14}", SOFT, 1.2)
    d.t(sx - 30, (T_TOP + T_BOT) / 2 + 4, "타이머", 12, SOFT, KR, "end")
    # 3. 재전송
    d.path(f"M {sx + 8} {Y_RE} L {rx - 10} {Y_RE}", INFO, 1.5, m="info")
    d.t((sx + rx) / 2, Y_RE - 10, "패킷 #1 다시", 12, INFO, KR, "middle", 600)
    # 4. 수신자 판정
    if ack_lost:
        w = 136
        d.o.append(f'<rect x="{rx - w / 2}" y="{Y_DUP - 10}" width="{w}" height="22" rx="4" '
                   f'fill="{PAPER}" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(rx, Y_DUP + 5, "#1 이미 받음 · 버림", 12, ACC, KR, "middle", 600)
    else:
        d.chip(rx, Y_DUP, "#1 처음 받음", OK, 12)
    # 5. ACK
    d.path(f"M {rx - 8} {Y_ACK2} L {sx + 10} {Y_ACK2}", MUTED, 1.5, m="ar", dash="5 4")
    d.t((sx + rx) / 2, Y_ACK2 - 10, "ACK #1", 12, MUTED, MONO, "middle", 600)

for px, title in PANELS:
    panel(px, title, px > 400)
d.line(W / 2, 100, W / 2, Y_BOT, RULE, 0.8)

d.legend(H - 64, [("사본을 번호로 가려냄", ACC), ("데이터 패킷", INFO), ("버려진 자리", BAD), ("수신자가 처음 받음", OK)])
d.save("12-01.ack-loss-ambiguity.svg")
