# 03-04 §1 — 송신 버퍼와 수신 버퍼 사이로 바이트가 실제로 흐르는 모습과, 창(rwnd)이 그중 무엇의 숫자인지.
# 본문 근거(§1 「변수 넷과 식 둘」·「창은 저장소가 아니라 숫자입니다」): rwnd = RcvBuffer − [LastByteRcvd − LastByteRead],
#   LastByteSent − LastByteAcked ≤ rwnd, 송신 버퍼는 보낸 뒤에도 ACK 가 올 때까지 바이트를 들고 있다.
# 한 순간의 스냅숏이다. RcvBuffer 6 · LastByteRead 2 · LastByteRcvd 4 → rwnd = 6 − (4 − 2) = 4.
#   LastByteAcked 2 · LastByteSent 5 → 미확인 3 ≤ 4. 5번 바이트의 사본이 망을 건너는 중이다.
# 타입 스펙: type-data-flow — 주체(A · B)를 따라 바이트가 앱 → 송신 버퍼 → 망 → 수신 버퍼 → 앱으로 건너간다.
#           축약: 버퍼를 파이프로 그려 칸 순서가 곧 흐름 방향이다(왼쪽 끝으로 들어와 오른쪽 끝으로 나감). 그래서 칸 번호는
#           오른쪽일수록 먼저 들어온 바이트다. 사용자 공간 · 커널 경계는 가로 점선 하나로 둔다. 되돌아오는 ACK 는
#           수신 버퍼의 빈자리 괄호에서 송신 버퍼의 미확인 괄호로 ㄷ자로 잇는다. focal 은 미확인 구간(창 안의 데이터).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 528
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §1",
      "버퍼는 둘, 창은 그중 하나의 빈자리를 적은 숫자입니다",
      "보내는 쪽 A 의 애플리케이션이 send() 로 송신 버퍼에 바이트를 쓰면 TCP 가 세그먼트로 내보내고, 받는 쪽 B 의 수신 버퍼에 쌓인 바이트는 recv() 가 꺼내 간다. 송신 버퍼는 보낸 바이트를 ACK 가 올 때까지 들고 있다. B 는 수신 버퍼의 빈자리 4 를 ACK 의 Window 칸에 실어 보내고, A 는 보냈지만 미확인인 3바이트를 그 숫자 안으로 묶는다.",
      "바이트는 왼쪽 끝으로 들어와 오른쪽 끝으로 나가고, ACK 가 수신 버퍼의 빈자리 수를 되돌려 줍니다")

CELL, Y_CELL, H_CELL = 44, 248, 48
A_X, B_X = 40, 576                                  # 두 버퍼 파이프의 왼쪽 끝
A_CELLS = [("free", ""), ("free", ""), ("ok", "7"), ("ok", "6"), ("acc", "5"), ("acc", "4"), ("acc", "3")]
B_CELLS = [("info", ""), ("info", ""), ("info", ""), ("info", ""), ("warn", "4"), ("warn", "3")]
TONE = {"ok": OK, "acc": ACC, "warn": WARN}

def cx_of(x0, i): return x0 + i * CELL + CELL / 2
A_END, B_END = A_X + len(A_CELLS) * CELL, B_X + len(B_CELLS) * CELL      # 348 · 840
MID = (A_END + B_X) / 2                                                  # 462 — 망

def cell(x, y, w, h, kind, txt):
    if kind == "free":
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4,3"/>')
    elif kind == "info":
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{INFO}10" stroke="{INFO}" stroke-width="1.0" stroke-dasharray="4,3"/>')
    else:
        c = TONE[kind]
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}"/>')
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}22" stroke="{c}" stroke-width="1.2"/>')
        d.t(x + w / 2, y + h / 2 + 5, txt, 14, c, MONO, "middle", 600)

def bracket(x1, x2, y, c):
    d.line(x1, y, x2, y, c, 1.2); d.line(x1, y - 6, x1, y, c, 1.2); d.line(x2, y - 6, x2, y, c, 1.2)

def tick(x, label):
    d.line(x, Y_CELL + H_CELL, x, Y_CELL + H_CELL + 12, MUTED, 1.0)
    d.t(x, Y_CELL + H_CELL + 28, label, 11, MUTED, MONO)

def app(x, label):
    d.box(x, 120, 160, 48, PAPER2, RULE, 1.0, 6)
    d.t(x + 80, 149, label, 13, INK, KR, "middle", 600)

# ── 주체와 층
d.t(A_X, 108, "보내는 쪽 A", 13, INK, KR, "start", 600)
d.t(900, 108, "받는 쪽 B", 13, INK, KR, "end", 600)
d.line(24, 196, W - 24, 196, SOFT, 0.9, dash="4,4")
d.t(MID, 188, "사용자 공간", 11, SOFT, KR, "middle", 600)
d.t(MID, 212, "커널", 11, SOFT, KR, "middle", 600)

# ── 연결선 먼저
A_IN = cx_of(A_X, 0)                                # send() 가 빈자리로 들어오는 자리
B_OUT = cx_of(B_X, len(B_CELLS) - 1)                # recv() 가 꺼내 가는 자리
d.arrow([(A_IN, 168), (A_IN, Y_CELL - 4)], MUTED, "ar", 1.4)
d.t(A_IN + 12, 188, "send()", 12, MUTED, MONO, "start")
d.arrow([(B_OUT, Y_CELL), (B_OUT, 172)], MUTED, "ar", 1.4)
d.t(B_OUT - 12, 188, "recv()", 12, MUTED, MONO, "end")
d.arrow([(A_END, Y_CELL + H_CELL / 2), (B_X - 4, Y_CELL + H_CELL / 2)], ACC, "acc", 1.6)
d.t(MID, Y_CELL - 12, "세그먼트", 12, ACC, KR, "middle", 600)

A_UNACK = (A_X + 4 * CELL, A_END)                   # 보냈지만 미확인 [5][4][3]
B_FREE = (B_X, B_X + 4 * CELL)                      # 빈자리 넷
ya, yb = 348, 420
ma, mb = sum(A_UNACK) / 2, sum(B_FREE) / 2
d.arrow([(B_FREE[0] + 12, ya), (B_FREE[0] + 12, yb), (A_END - 12, yb), (A_END - 12, ya + 8)], INFO, "info", 1.4)

# ── 애플리케이션과 버퍼 파이프
app(32, "애플리케이션")
app(740, "애플리케이션")
d.t(A_X + 2 * CELL, Y_CELL - 12, "송신 버퍼", 13, INK, KR, "start", 600)
d.t(A_X + 2 * CELL + 64, Y_CELL - 12, "SO_SNDBUF", 11, MUTED, MONO, "start")
d.t(B_X, Y_CELL - 12, "수신 버퍼", 13, INK, KR, "start", 600)
d.t(B_X + 64, Y_CELL - 12, "RcvBuffer 6", 11, MUTED, MONO, "start")
for i, (k, t) in enumerate(A_CELLS):
    cell(A_X + i * CELL, Y_CELL, CELL, H_CELL, k, t)
for i, (k, t) in enumerate(B_CELLS):
    cell(B_X + i * CELL, Y_CELL, CELL, H_CELL, k, t)
cell(MID - 16, Y_CELL + 8, 32, 32, "acc", "5")      # 망을 건너는 5번의 사본

tick(A_UNACK[0], "LastByteSent")
tick(A_END, "LastByteAcked")
tick(B_FREE[1], "LastByteRcvd")
tick(B_END, "LastByteRead")

# ── 괄호와 숫자
bracket(A_UNACK[0], A_UNACK[1], ya, ACC)
d.t(ma - 8, ya + 24, "미확인 3", 13, ACC, KR, "middle", 600)
bracket(B_FREE[0], B_FREE[1], ya, INFO)
d.t(mb + 8, ya + 24, "빈자리 4 = rwnd", 13, INFO, KR, "middle", 600)
d.chip(MID, yb, "ACK · Window = 4", INFO, 12)
d.t(ma, yb + 32, "3 ≤ 4 · 1바이트 더 보낼 수 있음", 12, MUTED, KR, "middle", 600)
d.t(mb, yb + 32, "recv() 가 꺼내 가면 늘어남", 12, MUTED, KR, "middle", 600)

d.legend(480, [("보냈지만 미확인", ACC), ("아직 안 보냄", OK), ("도착했지만 안 읽음", WARN), ("빈자리 = rwnd", INFO)])
d.save("03-04.buffers-and-window.svg")
print("ok buffers-and-window")
