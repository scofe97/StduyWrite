# 사실 출처: go1.25.1 src/net/net.go:183, src/net/tcpsock.go:112, src/net/fd_posix.go:17, src/internal/poll/fd_unix.go:18
# 타입 스펙: type-layers
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520

d = D(W, H,
      "NET SOCKET ABSTRACTION STACK",
      "net.Conn 에서 OS 소켓까지의 계층 구조",
      "공개 인터페이스에서 커널 파일 디스크립터로 내려가는 5단계 추상화",
      "추상 스트림 인터페이스, 런타임 poll.FD, 커널 소켓의 책임 분리")

# 좌측 방향 표시 (추상화 ↑ / 커널 ↓)
d.t(48, 120, "추상화", 12, SOFT, fam=KR, anchor="middle")
d.arrow([(48, 134), (48, 240)], SOFT, "soft", 1.2)
d.arrow([(48, 300), (48, 400)], SOFT, "soft", 1.2)
d.t(48, 420, "커널", 12, SOFT, fam=KR, anchor="middle")

LX, LW = 96, 816
layers = [
    ("L1", "net.Conn", "공개 인터페이스", "Read() · Write() · Close() 스트림 추상 계약", PAPER2, RULE, INK),
    ("L2", "*net.TCPConn", "구체 소켓 타입", "CloseRead() · SetKeepAlive() 고유 메서드 (conn 임베드)", PAPER2, RULE, INK),
    ("L3", "net.conn / netFD", "네트워크 디스크립터", "laddr · raddr 주소 관리 및 OS 플랫폼 차이 흡수", PAPER2, RULE, INK),
    ("L4", "poll.FD (internal/poll)", "런타임 I/O 폴러", "논블로킹 read 루프 · netpoller (waitRead) 연동", f"{ACC}14", ACC, ACC),
    ("L5", "OS Socket (Kernel)", "운영체제 소켓", "Sysfd · O_NONBLOCK · epoll/kqueue 이벤트 통지", PAPER2, RULE, INK),
]

y0 = 96
h_layer = 60
gap = 12

for i, (tag, name, role, note, fill, stroke, text_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 태그
    d.box(LX + 16, y + 18, 32, 24, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 32, y + 34, tag, 10, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 계층 이름
    d.t(LX + 64, y + 35, name, 14, text_col, fam=MONO, anchor="start", weight=600)

    # 역할 칩
    d.chip(LX + 320, y + 30, role, stroke if is_focal else MUTED, size=11)

    # 설명 노트
    d.t(LX + LW - 20, y + 35, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
d.legend(464, [
    ("표준 계층", MUTED),
    ("핵심 폴러 계층 (focal)", ACC),
    ("OS 경계", RULE)
])

d.save("01-01.socket-abstraction-layers.svg")
