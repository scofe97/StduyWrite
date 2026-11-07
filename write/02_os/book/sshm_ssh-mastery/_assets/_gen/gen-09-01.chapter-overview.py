# 타입 스펙: type-architecture
# 사실 출처: SSH Mastery Ch.9 Port Forwarding, RFC 4254 §7, OpenSSH V_10_6_P1 ssh.1, 2026-11-07 실측
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 500

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def nx(j):
    return COL_X + j * STRIDE

def ny(i):
    return ROW_Y + i * ROW_STRIDE

d = D(W, H, "ARCHITECTURE · 09-01 OVERVIEW",
      "세 가지 포워딩의 수신 지점과 목적지",
      "09-01 의 개념도입니다. 첫 줄은 클라이언트가 포트를 열고 서버가 목적지에 연결하는 local 포워딩입니다. "
      "둘째 줄은 서버가 포트를 열고 클라이언트 쪽이 목적지에 연결하는 remote 포워딩입니다. "
      "셋째 줄은 클라이언트가 SOCKS 프록시로 포트를 열고 서버가 요청이 정한 주소에 연결하는 dynamic 포워딩입니다.",
      lead="왼쪽 칩은 ssh 옵션이고 화살표 위 글자는 단계 이름입니다.")

def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")

def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)

for i, opt in enumerate(("-L", "-R", "-D")):
    d.chip(34, ny(i) + NH / 2 - 4, opt, MUTED, 11, 4)

# local
node(0, 0, "클라이언트의 수신 포트", "18100", INFO)
node(0, 1, "direct-tcpip 채널", "SSH 연결 1개 위", OK)
node(0, 2, "서버가 연결하는 목적지", "127.0.0.1:18101", ACC)
harrow(0, 0, "접속 수락")
harrow(0, 1, "채널 열기", ACC, "acc")

# remote
node(1, 0, "서버의 수신 포트", "127.0.0.1:2222", INFO)
node(1, 1, "forwarded-tcpip 채널", "SSH 연결 1개 위", OK)
node(1, 2, "클라이언트가 연결하는 목적지", "127.0.0.1:18099", ACC)
harrow(1, 0, "접속 수락")
harrow(1, 1, "채널 열기", ACC, "acc")

# dynamic
node(2, 0, "클라이언트의 SOCKS 포트", "127.0.0.1:19999", INFO)
node(2, 1, "direct-tcpip 채널", "SSH 연결 1개 위", OK)
node(2, 2, "서버가 연결하는 목적지", "SOCKS 요청이 정한 주소", ACC)
harrow(2, 0, "SOCKS 핸드셰이크")
harrow(2, 1, "채널 열기", ACC, "acc")

d.legend(440, [("수신 지점", INFO), ("채널", OK), ("목적지", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "09-01.chapter-overview.svg"
d.save(str(svg_path))
print("ok 09-01 chapter-overview")
