# 03-02 §5 「재전송」 — 원문이 설명하는 재전송 큐와 타이머의 한 바퀴.
# 원문: 보낼 때 사본을 큐에 넣고 타이머를 시작하고, 확인이 오면 지우고, 타임아웃이면 다시 보낸다.
# 화면에서 재전송을 알아보는 단서는 되돌아오는 칸의 SEQ 가 그대로라는 것이다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나르고,
#           focal 은 화면에 판정으로 찍히는 칸 하나(같은 SEQ 로 다시 보내는 자리)다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 980, 540
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §5",
      "재전송 큐가 도는 한 바퀴",
      "데이터를 실은 세그먼트는 보내는 순간 사본이 재전송 큐에 들어가고 타이머가 시작된다. 확인이 오면 큐에서 지우고, 타이머가 먼저 끝나면 같은 시퀀스 번호로 다시 보낸다. 되풀이되는 동안 시퀀스 번호가 그대로라는 점이 화면에서 재전송을 알아보는 단서다.",
      "번호가 그대로 되풀이되면 그것이 재전송입니다")

NW, NH = 196, 76
CX = [128, 358, 600, 860]
Y_TOP, Y_LOOP = 176, 340

def node(cx, y, title, sub, c=None, focal=False):
    x = cx - NW / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, NW, NH, c, 8)
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 8)
    col = ACC if focal else (c if c else INK)
    d.t(cx, y + 30, title, 13, col, KR, "middle", 600)
    d.t(cx, y + 50, sub, 11, MUTED, KR)

def diamond(cx, y, hw, hh, txt):
    cy = y + hh
    d.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" '
               f'fill="{PAPER2}" stroke="{INK}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, txt, 13, INK, KR, "middle", 600)

MID = Y_TOP + NH / 2
# 가로 줄기 — 보냄 · 큐에 담김 · 확인 여부 · 지움
d.arrow([(CX[0] + NW / 2, MID), (CX[1] - NW / 2 - 4, MID)], MUTED, "ar", 1.4)
d.arrow([(CX[1] + NW / 2, MID), (CX[2] - 112 - 4, MID)], MUTED, "ar", 1.4)
d.arrow([(CX[2] + 112, MID), (CX[3] - NW / 2 - 4, MID)], OK, "ok", 1.4)
# 아니오 갈래 — 아래 통로로 내려가 되돌아온다
d.arrow([(CX[2], MID + 42), (CX[2], Y_LOOP + NH / 2), (CX[1] + NW / 2 + 4, Y_LOOP + NH / 2)],
        ACC, "acc", 1.4)
d.arrow([(CX[1], Y_LOOP), (CX[1], Y_TOP + NH + 4)], ACC, "acc", 1.4)

node(CX[0], Y_TOP, "세그먼트 송신", "데이터와 SEQ 를 실어서")
node(CX[1], Y_TOP, "큐에 사본 · 타이머 시작", "확인이 올 때까지 보관")
diamond(CX[2], Y_TOP, 112, 42, "타임아웃 전에 확인?")
node(CX[3], Y_TOP, "큐에서 지움", "이 세그먼트는 끝", c=OK)
node(CX[1], Y_LOOP, "같은 SEQ 로 다시 보냄", "번호는 그대로", focal=True)

d.t((CX[2] + 112 + CX[3] - NW / 2) / 2, MID - 12, "예", 11, OK, KR, "middle", 600)
d.t(CX[2] + 12, MID + 76, "아니오", 11, ACC, KR, "start", 600)
d.t(CX[1] + 14, Y_TOP + NH + 34, "타이머 재시작", 11, ACC, KR, "start")
d.chip(CX[1], Y_LOOP + NH + 28, "TCP Retransmission", ACC)
d.t(CX[1], Y_LOOP + NH + 52, "Wireshark 가 이 칸에 붙이는 판정", 11, MUTED, KR)

d.legend(H - 48, [("화면에 판정으로 찍히는 칸", ACC), ("정상 종점", OK)])
d.save("03-02.retransmission-queue.svg")
