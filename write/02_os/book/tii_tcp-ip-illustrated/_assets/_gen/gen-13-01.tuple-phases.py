# 13-01 §1 — 같은 서버 포트에 붙은 두 연결이 4-tuple 로 갈리고, 각 연결이 수립 · 데이터 전송 · 종료 세 국면을 따로 지난다.
# 사실 출처: 원서 13.2 — "A TCP connection is defined to be a 4-tuple consisting of two IP addresses and two port numbers",
#   "three phases: setup, data transfer (called established), and teardown (closing)".
#   4-tuple 값: 원서 13.7.1 의 netstat -a -n -t 출력. 서버 ::ffff:10.0.0.1:22 에 같은 호스트 10.0.0.3 의 두 클라이언트가
#   16137 · 16140 에서 붙고 둘 다 ESTABLISHED. 16137 이 먼저, 16140 이 나중에 붙었다("We now initiate another client request").
#   TCP 는 네 값을 모두 써서 세그먼트를 가른다("demultiplexes incoming segments using all four values").
#   국면별 세그먼트: 원서 13.2.1 · 13.2.2(SYN · SYN+ACK · ACK / FIN · ACK · FIN · ACK).
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 시간 축 + 행마다 국면 막대.
#           축약: 라벨 열을 4-tuple 네 칸으로 가르고, 시간 축에는 눈금이 없다(순서만 나른다, 막대 길이는 설명용).
#           netstat 시점 이후의 종료 막대는 원서 출력 밖이라 점선으로 둔다. focal 은 두 행에서 유일하게 다른 원격 포트 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 472
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01 §1",
      "연결의 이름은 4-tuple, 생애는 세 국면",
      "원서 13.7 의 netstat 출력에서 서버 10.0.0.1 의 22번 포트에 같은 호스트 10.0.0.3 의 클라이언트 둘이 붙어 있다. 네 값 가운데 원격 포트만 "
      "16137 과 16140 으로 달라 두 연결이 갈린다. 각 연결은 수립 · 데이터 전송 · 종료 세 국면을 저마다 지나며, 시간 축은 순서만 나타낸다.",
      "같은 서버 포트의 두 연결 — 네 값 중 원격 포트만 다릅니다")

# 라벨 열 — 4-tuple 네 칸
CX, CW = [24, 116, 208, 300], 92
COLS = ["로컬 IP", "로컬 포트", "원격 IP", "원격 포트"]
ROWS = [("10.0.0.1", "22", "10.0.0.3", "16137"), ("10.0.0.1", "22", "10.0.0.3", "16140")]
FOCAL_COL = 3
Y_HEAD, ROW0, STRIDE, RH = 112, 136, 64, 48

# 국면 영역
TX0, TX1 = 416, 896
PH = [("수립", INFO, 96), ("데이터 전송", OK, 208), ("종료", WARN, 96)]
OFFS = [416, 480]          # 둘째 연결은 나중에 붙었다
X_NETSTAT = 672

# 머리 행
for i, name in enumerate(COLS):
    c = ACC if i == FOCAL_COL else SOFT
    d.t(CX[i] + CW / 2, Y_HEAD + 8, name, 12, c, KR, "middle", 600)
d.t(TX0, Y_HEAD + 8, "시간 순서 →", 12, SOFT, KR, "start", 600)
d.line(24, Y_HEAD + 16, TX1, Y_HEAD + 16, RULE, 0.8)

# focal 열 배경
fy0 = ROW0 - 4
d.o.append(f'<rect x="{CX[FOCAL_COL]}" y="{fy0}" width="{CW}" height="{STRIDE + RH + 8}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')

# netstat 시점
yb = ROW0 + STRIDE + RH + 8
d.line(X_NETSTAT, ROW0 - 8, X_NETSTAT, yb, MUTED, 1.0, "3 4")
d.t(X_NETSTAT, yb + 16, "netstat 시점 · 둘 다 ESTABLISHED", 12, MUTED, KR, "middle", 600)

for r, vals in enumerate(ROWS):
    y = ROW0 + r * STRIDE
    for i, v in enumerate(vals):
        if i != FOCAL_COL:
            d.box(CX[i] + 4, y, CW - 8, RH, PAPER2, RULE, 0.8, 6)
        d.t(CX[i] + CW / 2, y + 29, v, 13, ACC if i == FOCAL_COL else INK, MONO, "middle", 600)
    x = OFFS[r]
    for name, c, w in PH:
        by = y + 10
        if x >= X_NETSTAT:   # netstat 출력 이후 — 원서 밖
            d.o.append(f'<rect x="{x}" y="{by}" width="{w}" height="28" rx="4" fill="none" stroke="{c}" stroke-width="1.1" stroke-dasharray="5 4"/>')
        else:
            d.tone(x, by, w, 28, c, 4, "14", 1.0)
        d.t(x + w / 2, by + 19, name, 12, c, KR, "middle", 600)
        x += w

# 국면 열쇠 — 국면마다 오가는 세그먼트와 이 편의 절
KY, KW, KH = 300, 280, 76
KEYS = [("수립 · setup", "SYN · SYN+ACK · ACK", "세그먼트 셋 · §2", INFO),
        ("데이터 전송 · established", "데이터 · ACK", "12-01 의 재전송 · 창", OK),
        ("종료 · teardown", "FIN · ACK · FIN · ACK", "세그먼트 넷 · §3", WARN)]
for i, (name, segs, where, c) in enumerate(KEYS):
    x = 24 + i * (KW + 16)
    d.box(x, KY, KW, KH, PAPER2, RULE, 0.8, 8)
    d.t(x + 16, KY + 24, name, 13, c, KR, "start", 600)
    d.t(x + 16, KY + 46, segs, 12, INK, MONO, "start")
    d.t(x + 16, KY + 66, where, 12, MUTED, KR, "start")

d.legend(H - 56, [("두 연결을 가르는 칸", ACC), ("수립", INFO), ("데이터 전송", OK), ("종료", WARN)])
d.save("13-01.tuple-phases.svg")
