# 사실 출처: go doc net.TCPConn, KeepAliveConfig, src/net/tcpsockopt_*.go, sockopt_posix.go (go1.25.1)
# 타입 스펙: type-tree
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 580

d = D(W, H,
      "TCPCONN METHOD TO SOCKET OPTION TREE",
      "TCPConn 메서드와 커널 소켓 옵션 대응 지도",
      "Go 표준 라이브러리 TCPConn 제어 손잡이가 설정하는 운영체제 커널 옵션",
      "소켓 메서드 계통별 매핑: keepalive · 버퍼/지연 · linger/종료 · zero-copy 전송")

# ── 1. 루트 노드 (x = 36, y = 248, w = 140, h = 68) ──
RX, RY, RW, RH = 36, 248, 140, 68
d.box(RX, RY, RW, RH, fill=PAPER2, stroke=ACC, sw=1.4)
d.t(RX + RW // 2, RY + 26, "net.TCPConn", 14, ACC, fam=KR, anchor="middle", weight=600)
d.t(RX + RW // 2, RY + 46, "소켓 제어 손잡이", 11, MUTED, fam=KR, anchor="middle")

# ── 2. 브랜치 & 세부 리프 정의 ──
groups = [
    (96, "연결 유지",
     ["SetKeepAlive()", "SetKeepAlivePeriod()", "SetKeepAliveConfig()"],
     "SOL_SOCKET · IPPROTO_TCP",
     ["SO_KEEPALIVE (프로브)", "TCP_KEEPIDLE (유휴 주기)", "TCP_KEEPINTVL · KEEPCNT"],
     INFO, False),

    (204, "버퍼 & 전송 지연",
     ["SetNoDelay()", "SetReadBuffer()", "SetWriteBuffer()"],
     "IPPROTO_TCP · SOL_SOCKET",
     ["TCP_NODELAY (Nagle 해제)", "SO_RCVBUF (수신 버퍼)", "SO_SNDBUF (송신 버퍼)"],
     OK, False),

    (312, "종료 & Linger 제어",
     ["CloseRead() · CloseWrite()", "SetLinger(sec > 0)", "SetLinger(sec == 0)"],
     "시스템 콜 · SOL_SOCKET",
     ["SHUT_RD · SHUT_WR (FIN)", "SO_LINGER (배경 전송)", "SO_LINGER (RST 강제 종료)"],
     ACC, True),

    (420, "제로카피 & MPTCP",
     ["ReadFrom() · WriteTo()", "ReadFrom(*os.File)", "MultipathTCP()"],
     "커널 전송 · 프로토콜 질의",
     ["splice(2) (파이프)", "sendfile(2) (파일)", "MPTCP 활성 여부 조회"],
     WARN, False),
]

# 루트 -> 카테고리 분기 버스 배선 (직교 연결선)
BUS_X = 208
d.line(RX + RW, RY + RH // 2, BUS_X, RY + RH // 2, RULE, 1.2)
d.line(BUS_X, groups[0][0] + 44, BUS_X, groups[-1][0] + 44, RULE, 1.2)

for y, gtitle, methods, opt_level, opts, col, is_focal in groups:
    mid_y = y + 44
    # 버스 -> 2열 수평 화살표
    d.arrow([(BUS_X, mid_y), (240, mid_y)], col, "ar", 1.2)

    # 2열: 메서드 그룹 상자 (x = 240, w = 264, h = 88)
    d.box(240, y, 264, 88, fill=PAPER2, stroke=ACC if is_focal else RULE, sw=1.2 if is_focal else 0.9)
    d.t(252, y + 20, gtitle, 12, col, fam=KR, anchor="start", weight=600)
    for m_idx, m_name in enumerate(methods):
        d.t(252, y + 38 + m_idx * 16, m_name, 10, INK, fam=MONO, anchor="start")

    # 2열 -> 3열 수평 화살표
    d.arrow([(504, mid_y), (544, mid_y)], col, "ar", 1.2)

    # 3열: 커널 소켓 옵션 / 시스템 콜 상자 (x = 544, w = 380, h = 88)
    d.box(544, y, 380, 88, fill=PAPER2, stroke=col, sw=1.2 if is_focal else 1.0)
    d.t(556, y + 20, opt_level, 11, col, fam=MONO, anchor="start", weight=600)
    for o_idx, o_name in enumerate(opts):
        d.t(556, y + 38 + o_idx * 16, o_name, 10, MUTED, fam=KR, anchor="start")

# 범례 (y = 536)
d.legend(536, [
    ("연결 유지 옵션", INFO),
    ("버퍼·지연 옵션", OK),
    ("종료·Linger 제어 (focal)", ACC),
    ("제로카피·프로토콜 옵션", WARN)
])

out_name = "04-01.tcpconn-socket-options.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
