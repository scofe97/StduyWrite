# 03-01 학습 목표 뒤 전체 지도 — 이 편의 절들이 TCP 상태 전이를 따라간다.
# 원문의 상태 표와 세 handshake 표에 적힌 전이만 그린다. 없는 전이를 채우지 않는다.
#   서버 쪽 여는 경로(CLOSED → LISTEN → SYN-RECEIVED → ESTABLISHED)는 원문 종료 절 전이 표의 TCP-B 열에 있다.
#   세그먼트 셋 종료(FIN_WAIT-1 에서 곧장 TIME_WAIT)와 동시 종료(CLOSING)는 원문 표에 없어 그리지 않는다.
# 타입 스펙: type-state — 주체 하나의 상태 전이. 전이 라벨은 무엇이 오갔는지(플래그)를 적고,
#           focal 은 애플리케이션 버그로 갇히는 상태 하나(CLOSE_WAIT).
#           배치: 위 두 줄이 여는 경로(클라이언트·서버), 아래 두 줄이 닫는 경로(FIN 을 받은 쪽·먼저 보낸 쪽).
#           분기선은 줄 사이 corridor 만 타고, 전이 라벨 띠(각 줄 윗변 위 24px)와 겹치지 않는다.
#           라벨은 자기 선 바로 곁(선 위 8~10px)에 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-01",
      "TCP 연결의 상태 전이",
      "원문이 표로 적은 상태 전이를 한 장으로 이은 것. 위 두 줄이 연결을 여는 경로로 클라이언트는 SYN_SENT 를, 서버는 LISTEN 과 SYN_RECEIVED 를 지나 ESTABLISHED 에서 만난다. 아래 두 줄이 닫는 경로로, FIN 을 받은 쪽과 먼저 보낸 쪽이 서로 다른 상태를 지난다.",
      "여는 길은 ESTABLISHED 로 모이고, 닫는 길은 누가 먼저 FIN 을 보냈는지로 갈립니다")

X = [72, 304, 536, 768]          # 가로 stride 232
SW, SH = 208, 52
Y_A, Y_B, Y_C, Y_D = 120, 216, 336, 464   # 여는 줄 stride 96, 닫는 줄 stride 128
COR_P, COR_A = 292, 420          # 수동 종료 corridor · 능동 종료 corridor 의 y
P_IN, P_PAS, P_ACT = 808, 872, 936   # ESTABLISHED 아랫변 포트 — 서버 여는 길 · 수동 분기 · 능동 분기

def cx(col): return X[col] + SW / 2
def mid(y): return y + SH / 2

def state(col, y, name, sub, c=None, focal=False):
    x = X[col]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, SW, SH, c, 8)
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    col_c = ACC if focal else (c if c else INK)
    d.t(x + SW / 2, y + 22, name, 13, col_c, MONO, "middle", 600)
    d.t(x + SW / 2, y + 40, sub, 11, MUTED, KR)

def right(c1, c2, y, label, col=MUTED, mk="ar"):
    # 이웃한 두 상태 — 틈이 24px 라 라벨은 줄 윗변 위 라벨 띠에 둔다
    d.arrow([(X[c1] + SW, mid(y)), (X[c2] - 4, mid(y))], col, mk, 1.4)
    d.t((X[c1] + SW + X[c2]) / 2, y - 12, label, 11, col, MONO)

# ── 전이선 먼저 (z-order)
# 여는 경로 — 클라이언트
right(0, 1, Y_A, "SYN 송신")
d.arrow([(X[1] + SW, mid(Y_A)), (X[3] - 4, mid(Y_A))], MUTED, "ar", 1.4)
d.t((X[1] + SW + X[3]) / 2, mid(Y_A) - 10, "SYN,ACK 수신 · ACK 송신", 11, MUTED, MONO)
# 여는 경로 — 서버
d.arrow([(cx(0), Y_A + SH), (cx(0), Y_B - 4)], MUTED, "ar", 1.4)
d.t(cx(0) - 12, Y_A + SH + 26, "passive OPEN", 11, MUTED, MONO, "end")
right(0, 1, Y_B, "SYN 수신 · SYN,ACK 송신")
d.arrow([(X[1] + SW, mid(Y_B)), (P_IN, mid(Y_B)), (P_IN, Y_A + SH + 4)], MUTED, "ar", 1.4)
d.t((X[1] + SW + P_IN) / 2, mid(Y_B) - 10, "ACK 수신", 11, MUTED, MONO)
# 닫는 경로 — FIN 을 받은 쪽(수동 종료)
d.arrow([(P_PAS, Y_A + SH), (P_PAS, COR_P), (cx(0), COR_P), (cx(0), Y_C - 4)], INFO, "info", 1.4)
d.t((cx(0) + P_PAS) / 2 + 120, COR_P - 8, "FIN 수신 · ACK 송신", 11, INFO, KR)
right(0, 1, Y_C, "close() · FIN 송신", INFO, "info")
right(1, 2, Y_C, "ACK 수신", INFO, "info")
# 닫는 경로 — 먼저 FIN 을 보낸 쪽(능동 종료)
d.arrow([(P_ACT, Y_A + SH), (P_ACT, COR_A), (cx(0), COR_A), (cx(0), Y_D - 4)], MUTED, "ar", 1.4)
d.t((cx(0) + P_ACT) / 2 + 120, COR_A - 8, "close() · FIN 송신", 11, MUTED, KR)
right(0, 1, Y_D, "ACK 수신")
right(1, 2, Y_D, "FIN 수신 · ACK 송신")
right(2, 3, Y_D, "2×MSL 경과")

# ── 상태
state(0, Y_A, "CLOSED", "원문의 \"가상의 상태\"")
state(1, Y_A, "SYN_SENT", "클라이언트가 연결 시작")
state(3, Y_A, "ESTABLISHED", "데이터를 주고받는 중", c=OK)
state(0, Y_B, "LISTEN", "서버가 연결 대기")
state(1, Y_B, "SYN_RECEIVED", "서버가 요청 받음")
state(0, Y_C, "CLOSE_WAIT", "애플리케이션이 안 닫음", focal=True)
state(1, Y_C, "LAST_ACK", "마지막 ACK 대기")
state(2, Y_C, "CLOSED", "수동 종료 끝", c=OK)
state(0, Y_D, "FIN_WAIT-1", "소켓 닫음")
state(1, Y_D, "FIN_WAIT-2", "상대의 FIN 대기")
state(2, Y_D, "TIME_WAIT", "2×MSL 동안 머무름")
state(3, Y_D, "CLOSED", "능동 종료 끝", c=OK)

d.legend(552, [("안 닫으면 갇히는 자리", ACC), ("정상 종점", OK), ("FIN 을 받은 쪽", INFO), ("먼저 FIN 을 보낸 쪽", MUTED)])
d.save("03-01.tcp-states.svg")
