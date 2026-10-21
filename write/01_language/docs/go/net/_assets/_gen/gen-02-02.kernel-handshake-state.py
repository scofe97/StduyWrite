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
BW = 140            # 1~3 상태 상자 폭
BW4 = 116           # ACCEPTED 상자 폭
GAP = 90            # 상자 사이 — 전이 라벨(11px, 최대 약 80px)이 상자 변에 닿지 않는 폭

# 상태별 왼쪽 x → 중심 x
L1 = 100
L2 = L1 + BW + GAP   # 330
L3 = L2 + BW + GAP   # 560
L4 = L3 + BW + GAP   # 790
X1, X2, X3 = L1 + BW // 2, L2 + BW // 2, L3 + BW // 2
X4 = L4 + BW4 // 2
X_START = 30
X_END = 942

def draw_state(cx, cy, w, h, name, sub, dial_view, c, focal=False, view_c=None):
    x = cx - w // 2
    y = cy - h // 2
    fill = f"{c}1A" if focal else PAPER2
    sw = 1.4 if focal else 1.0
    d.box(x, y, w, h, fill=fill, stroke=c, sw=sw, r=8)
    d.t(cx, cy - 22, name, 13, c, fam=MONO, weight=600)
    d.t(cx, cy - 4, sub, 11, INK, fam=KR)
    d.line(x + 10, cy + 9, x + w - 10, cy + 9, RULE, 0.7)
    d.t(cx, cy + 26, dial_view, 11, view_c or (SOFT if not focal else ACC), fam=KR)

def transition(xa, xb, top, bottom, c, mk, top_c, weight=400):
    # 전이 화살표: 위 라벨은 사건, 아래 라벨은 결과. 둘 다 상자 사이 폭 안에 둔다
    d.arrow([(xa + 4, CY), (xb - 6, CY)], c=c, m=mk)
    mx = (xa + xb) / 2
    d.t(mx, CY - 10, top, 11, top_c, fam=KR, weight=weight)
    d.t(mx, CY + 22, bottom, 11, SOFT, fam=KR)

# 1. 시작점 — 라벨은 화살표 위에 둔다
d.o.append(f'<circle cx="{X_START}" cy="{CY}" r="6" fill="{INK}"/>')
d.arrow([(X_START + 8, CY), (L1 - 6, CY)], c=MUTED, m="ar")
d.t((X_START + L1) / 2 + 4, CY - 12, "Dial() 호출", 11, MUTED, fam=KR)

# 2. State 1: SYN_SENT (클라이언트)
draw_state(X1, CY, BW, BH, "SYN_SENT", "클라이언트 SYN 발송", "Dial 블로킹 대기", MUTED)

# Transition 1 -> 2
transition(L1 + BW, L2, "SYN 도달", "SYN-ACK 응답", MUTED, "ar", INK)

# 3. State 2: SYN_RCVD (서버) — 클라이언트는 이 구간에 SYN-ACK 를 받고 ACK 를 보낸 뒤 Dial 이 성공한다
draw_state(X2, CY, BW, BH, "SYN_RCVD", "서버 SYN 대기열 등록", "SYN-ACK 로 Dial 성공", WARN, view_c=OK)

# Transition 2 -> 3
transition(L2 + BW, L3, "최종 ACK 수신", "3-way 완료", MUTED, "ar", OK)

# 4. State 3: ESTABLISHED (서버 Accept 큐)
draw_state(X3, CY, BW, BH, "ESTABLISHED", "서버 Accept 큐 진입", "Accept 전까지 큐 대기", OK)

# Transition 3 -> 4
transition(L3 + BW, L4, "Accept() 호출", "dequeue", ACC, "acc", ACC, weight=600)

# 5. State 4: ACCEPTED (애플리케이션 net.Conn 획득) - FOCAL
draw_state(X4, CY, BW4, BH, "ACCEPTED", "net.Conn 반환", "연결 I/O 시작", ACC, focal=True)

# 6. 종료점 (ringed dot)
d.arrow([(L4 + BW4 + 4, CY), (X_END - 12, CY)], c=ACC, m="acc")
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="8" fill="none" stroke="{ACC}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{X_END}" cy="{CY}" r="4" fill="{ACC}"/>')

# ── 하단: 커널 대기열 계층 안내 (Linux listen(2) 모델) ──
Q_TOP = 310
QW = 200
# SYN 큐 구역
d.box(X2 - QW // 2, Q_TOP, QW, 84, fill="rgba(227,179,65,0.06)", stroke=WARN, sw=0.8, r=6)
d.t(X2, Q_TOP + 20, "SYN 대기열 (반연결 큐)", 11, WARN, fam=KR, weight=600)
d.t(X2, Q_TOP + 40, "용량: tcp_max_syn_backlog", 11, SOFT, fam=KR)
d.t(X2, Q_TOP + 60, "Linux 기준 · 미완료 연결", 11, MUTED, fam=KR)
d.line(X2, CY + BH // 2 + 4, X2, Q_TOP, WARN, 0.8, "2 3")

# Accept 큐 구역
d.box(X3 - QW // 2, Q_TOP, QW, 84, fill="rgba(63,185,140,0.06)", stroke=OK, sw=0.8, r=6)
d.t(X3, Q_TOP + 20, "Accept 대기열 (완결 큐)", 11, OK, fam=KR, weight=600)
d.t(X3, Q_TOP + 40, "용량: listenerBacklog()", 11, SOFT, fam=KR)
d.t(X3, Q_TOP + 60, "핸드셰이크 완료 소켓 대기", 11, MUTED, fam=KR)
d.line(X3, CY + BH // 2 + 4, X3, Q_TOP, OK, 0.8, "2 3")

# 범례
d.legend(425, [
    ("미완료 단계", MUTED),
    ("SYN 대기열 (반연결 큐)", WARN),
    ("Dial 성공 · 핸드셰이크 완료", OK),
    ("Accept 소켓 획득 (focal)", ACC)
])

out_name = "02-02.kernel-handshake-state.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
