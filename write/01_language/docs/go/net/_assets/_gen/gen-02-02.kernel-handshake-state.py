# 사실 출처: go1.25.1 src/net/sock_posix.go:150, src/internal/poll/fd_unix.go:594, RFC 793, gonet-lab 00-01
# 타입 스펙: type-state
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480

d = D(W, H,
      "TCP HANDSHAKE AND ACCEPT QUEUE STATE TRANSITIONS",
      "커널 핸드셰이크와 Accept 큐 상태 전이",
      "클라이언트 SYN 부터 커널 대기열을 거쳐 Accept() 소켓 획득까지의 상태 변화",
      "Dial 의 성공은 Accept 호출이 아니라 커널의 핸드셰이크 완료 시점에 확정됩니다")

# 상태 박스 높이 및 Y 좌표
CY = 208
BH = 88
BW = 168

# 상태별 X 중심 좌표
X_START = 40
X1 = 150    # SYN_SENT
X2 = 380    # SYN_RCVD (SYN 큐)
X3 = 620    # ESTABLISHED (Accept 큐)
X4 = 840    # ACCEPTED (소켓 반환)
X_END = 932

def draw_state(cx, cy, w, h, name, sub, dial_view, c, focal=False):
    x = cx - w // 2
    y = cy - h // 2
    fill = f"{c}1A" if focal else PAPER2
    sw = 1.4 if focal else 1.0
    d.box(x, y, w, h, fill=fill, stroke=c, sw=sw, r=8)
    d.t(cx, cy - 22, name, 13, c, fam=MONO, weight=600)
    d.t(cx, cy - 4, sub, 11, INK, fam=KR)
    d.line(x + 10, cy + 9, x + w - 10, cy + 9, RULE, 0.7)
    d.t(cx, cy + 24, dial_view, 10, SOFT if not focal else ACC, fam=KR)

# 1. 시작점
d.o.append(f'<circle cx="{X_START}" cy="{CY}" r="6" fill="{INK}"/>')
d.arrow([(X_START + 8, CY), (X1 - BW // 2 - 6, CY)], c=MUTED, m="ar")
d.t((X_START + X1 - BW // 2) // 2, CY - 12, "Dial() 호출", 10, MUTED, fam=KR)

# 2. State 1: SYN_SENT
draw_state(X1, CY, BW, BH, "SYN_SENT", "클라이언트 SYN 발송", "Dial 블로킹 대기", MUTED)

# Transition 1 -> 2
d.arrow([(X1 + BW // 2 + 4, CY), (X2 - BW // 2 - 6, CY)], c=MUTED, m="ar")
d.t((X1 + BW // 2 + X2 - BW // 2) // 2, CY - 16, "SYN 도달", 10, INK, fam=KR)
d.t((X1 + BW // 2 + X2 - BW // 2) // 2, CY - 4, "SYN-ACK 응답", 9, SOFT, fam=KR)

# 3. State 2: SYN_RCVD
draw_state(X2, CY, BW, BH, "SYN_RCVD", "커널 SYN 대기열 등록", "핸드셰이크 진행 중", WARN)

# Transition 2 -> 3
d.arrow([(X2 + BW // 2 + 4, CY), (X3 - BW // 2 - 6, CY)], c=MUTED, m="ar")
d.t((X2 + BW // 2 + X3 - BW // 2) // 2, CY - 16, "최종 ACK 수신", 10, OK, fam=KR)
d.t((X2 + BW // 2 + X3 - BW // 2) // 2, CY - 4, "3-way 완료", 9, SOFT, fam=KR)

# 4. State 3: ESTABLISHED (Accept 큐)
draw_state(X3, CY, BW, BH, "ESTABLISHED", "커널 Accept 큐 진입", "Dial 즉시 성공!", OK)

# Transition 3 -> 4
d.arrow([(X3 + BW // 2 + 4, CY), (X4 - BW // 2 - 6, CY)], c=ACC, m="acc")
d.t((X3 + BW // 2 + X4 - BW // 2) // 2, CY - 16, "Accept() 호출", 10, ACC, fam=KR, weight=600)
d.t((X3 + BW // 2 + X4 - BW // 2) // 2, CY - 4, "큐에서 dequeue", 9, SOFT, fam=KR)

# 5. State 4: ACCEPTED (애플리케이션 net.Conn 획득) - FOCAL
draw_state(X4, CY, 136, BH, "ACCEPTED", "net.Conn 반환", "연결 I/O 시작", ACC, focal=True)

# 6. 종료점 (ringed dot)
d.arrow([(X4 + 136 // 2 + 4, CY), (X_END - 12, CY)], c=ACC, m="acc")
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="8" fill="none" stroke="{ACC}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="4" fill="{ACC}"/>')

# ── 하단: 커널 대기열 계층 안내 ──
Q_TOP = 310
# SYN 큐 구역
d.box(X2 - BW // 2 - 8, Q_TOP, BW + 16, 84, fill="rgba(227,179,65,0.06)", stroke=WARN, sw=0.8, r=6)
d.t(X2, Q_TOP + 20, "SYN 대기열 (반가상 연결)", 11, WARN, fam=KR, weight=600)
d.t(X2, Q_TOP + 38, "용량: tcp_max_syn_backlog", 10, SOFT, fam=MONO)
d.t(X2, Q_TOP + 56, "미완료 SYN 패킷 보관", 10, MUTED, fam=KR)
d.line(X2, CY + BH // 2 + 4, X2, Q_TOP, WARN, 0.8, "2 3")

# Accept 큐 구역
d.box(X3 - BW // 2 - 8, Q_TOP, BW + 16, 84, fill="rgba(63,185,140,0.06)", stroke=OK, sw=0.8, r=6)
d.t(X3, Q_TOP + 20, "Accept 대기열 (완성 연결)", 11, OK, fam=KR, weight=600)
d.t(X3, Q_TOP + 38, "용량: maxListenerBacklog()", 10, SOFT, fam=MONO)
d.t(X3, Q_TOP + 56, "핸드셰이크 완료 소켓 대기", 10, MUTED, fam=KR)
d.line(X3, CY + BH // 2 + 4, X3, Q_TOP, OK, 0.8, "2 3")

# 범례
d.legend(425, [
    ("미완료 단계", MUTED),
    ("SYN 대기열 (반연결)", WARN),
    ("핸드셰이크 완료 · Dial 성공", OK),
    ("Accept 소켓 획득 (focal)", ACC)
])

d.save("write/01_language/docs/go/net/_assets/02-02.kernel-handshake-state.svg")
