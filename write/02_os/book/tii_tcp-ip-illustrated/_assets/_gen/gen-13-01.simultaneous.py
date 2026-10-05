# 13-01 §4 — 원서 그림 13-3(동시 열기)과 13-4(동시 닫기)를 나란히.
# 원문 13.2.2: 동시 열기는 양쪽이 상대의 SYN 을 받기 전에 자기 SYN 을 보내야 하고 두 SYN 은 망에서 엇갈린다.
#   세그먼트 넷이 오가며(보통보다 하나 많음) SYN 비트는 그 SYN 이 확인될 때까지 각 세그먼트에 켜져 있다.
#   동시 닫기는 보통 닫기와 세그먼트 수가 같고 순서만 엇갈린다. 예시 포트: A 7777 ↔ B 8888.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지를 두 판으로 나란히 놓는다.
#           축약: 엇갈림이 논지라 메시지를 수평 화살표가 아니라 아래로 기운 선(line, 화살촉 없음)으로 그린다
#           (12-01 stop-and-wait-vs-window 와 같은 선택). 시간은 아래로만 흐르므로 기울기가 곧 방향이다.
#           focal 은 왼쪽 판에서 엇갈린 SYN 둘이 만나는 교차점 표시 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 560
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01 §4",
      "동시 열기와 동시 닫기 — 세그먼트가 엇갈릴 때",
      "왼쪽은 A(포트 7777)와 B(포트 8888)가 서로에게 동시에 능동 열기를 한 경우로, 두 SYN 이 망에서 엇갈린 뒤 각자 SYN,ACK 를 보내 세그먼트가 넷이 된다. "
      "오른쪽은 양쪽이 동시에 FIN 을 보낸 경우로, 세그먼트 수는 보통 닫기와 같은 넷이고 순서만 엇갈린다.",
      "동시 열기는 하나가 더 들고, 동시 닫기는 순서만 바뀝니다")

PW = 424
Y_LANE, T0, DROP = 104, 184, 96

def lanes(px, title):
    ax, bx = px + 72, px + PW - 72
    d.t(px + PW / 2, 100, title, 13, INK, KR, "middle", 600)
    for x, nm, sub in ((ax, "A", "포트 7777"), (bx, "B", "포트 8888")):
        d.box(x - 52, Y_LANE + 12, 104, 44, PAPER2, RULE, 1.0, 6)
        d.t(x, Y_LANE + 31, nm, 13, INK, KR, "middle", 600)
        d.t(x, Y_LANE + 48, sub, 11, MUTED, KR)
        d.line(x, Y_LANE + 60, x, 470, RULE, 1.0, "3 6")
    return ax, bx

def seg(x1, t1, x2, label, c, side):
    t2 = t1 + DROP
    d.line(x1, t1, x2, t2, c, 1.6)
    if side == "L": d.t(x1 - 8, t1 + 4, label, 12, c, MONO, "end", 600)
    else: d.t(x1 + 8, t1 + 4, label, 12, c, MONO, "start", 600)

# 동시 열기
ax, bx = lanes(24, "동시 열기 · 세그먼트 4")
seg(ax, T0, bx, "SYN", INFO, "L")
seg(bx, T0, ax, "SYN", INFO, "R")
mx, my = (ax + bx) / 2, T0 + DROP / 2
d.o.append(f'<circle cx="{mx}" cy="{my}" r="9" fill="{ACC}22" stroke="{ACC}" stroke-width="1.4"/>')
d.t(mx, my - 16, "엇갈림", 12, ACC, KR, "middle", 600)
seg(ax, T0 + DROP + 24, bx, "SYN, ACK", OK, "L")
seg(bx, T0 + DROP + 24, ax, "SYN, ACK", OK, "R")
d.chip(ax, 448, "연결 수립", OK, 12)
d.chip(bx, 448, "연결 수립", OK, 12)

# 동시 닫기
ax2, bx2 = lanes(472, "동시 닫기 · 세그먼트 4")
seg(ax2, T0, bx2, "FIN", WARN, "L")
seg(bx2, T0, ax2, "FIN", WARN, "R")
seg(ax2, T0 + DROP + 24, bx2, "ACK", MUTED, "L")
seg(bx2, T0 + DROP + 24, ax2, "ACK", MUTED, "R")
d.chip(ax2, 448, "닫힘", MUTED, 12)
d.chip(bx2, 448, "닫힘", MUTED, 12)

d.line(W / 2, 88, W / 2, 480, RULE, 0.8)
d.legend(H - 56, [("엇갈리는 지점", ACC), ("SYN", INFO), ("SYN,ACK · 수립", OK), ("FIN", WARN)])
d.save("13-01.simultaneous.svg")
