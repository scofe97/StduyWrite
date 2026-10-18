# 타입 스펙: type-sequence
# 사실 출처: RFC 9110 §7.8, RFC 6455 §1.3,
#   portal/api_server.go:558-577, portal/transport/stream_mux.go:31-33,
#   docs/src/routes/architecture/+page.md §Reverse Session.
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqUpgrade(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')
        s.o.insert(20, f'<marker id="info_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{INFO}"/></marker>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 18}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 6, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 9.5)/2}" y="{y + 4}" width="{_w(sub, 9.5)}" height="14" fill="{PAPER}"/>')
            s.t(mx, y + 14, sub, 9.5, MUTED, _kr(sub))

    def bi_msg(s, a, b, label, y, c=OK, sub=None, mk_l="ok_left", mk_r="ok"):
        x1, x2 = s.LX[a], s.LX[b]
        s.o.append(f'<path d="M {x1 + 12} {y} L {x2 - 12} {y}" fill="none" stroke="{c}" stroke-width="1.5" marker-start="url(#{mk_l})" marker-end="url(#{mk_r})"/>')
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 18}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 6, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 9.5)/2}" y="{y + 4}" width="{_w(sub, 9.5)}" height="14" fill="{PAPER}"/>')
            s.t(mx, y + 14, sub, 9.5, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-8} L {x+46} {y-8} L {x+46} {y+8} L {x+13} {y+8}", c, 1.4, m="ar")
        s.t(x + 54, y - 2, label, 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 54, y + 12, sub, 9.5, MUTED, _kr(sub), "start")

W, H = 960, 580
d = SeqUpgrade(W, H, "PORTAL-TUNNEL · HTTP UPGRADE & HIJACK",
               "HTTP Upgrade 와 연결 하이재킹 프로토콜 전환",
               "클라이언트와 서버가 Upgrade 헤더와 101 Switching Protocols 응답을 교환한 뒤 소켓 제어권을 가로채 동일한 TCP 연결 위에서 임의의 양방향 바이너리 프레이밍으로 전환합니다.",
               "HTTP/1.1 핸드셰이크를 마친 소켓을 하이재커로 가로채 바이너리 역방향 터널로 승격합니다")

NAMES = (
    ("클라이언트", "SDK · 터널 에이전트"),
    ("중계 서버", "HTTP 인그레스 · 릴레이")
)
d.LX = {"client": 200, "server": 640}
KEYS = ["client", "server"]

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 90, 100, 180, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, KR)

d.lane_top = 144
d.rails(H - 72)

# 1. TCP Handshake + TLS
d.msg("client", "server", "TCP 3-way Handshake + TLS 1.3", 175, SOFT, "soft", sub="단일 암호화 전송로 수립")

# 2. GET /sdk/connect HTTP/1.1 with Upgrade
d.msg("client", "server", "GET /sdk/connect HTTP/1.1", 225, INFO, "info", sub="Connection: Upgrade, Upgrade: raw")

# 3. Server Hijack
d.selfmsg("server", "http.Hijacker 제어권 인수", 275, ACC, sub="conn, rw, err := hijacker.Hijack()")

# 4. 101 Switching Protocols
d.msg("server", "client", "HTTP/1.1 101 Switching Protocols", 325, OK, "ok", sub="Connection: Upgrade, Upgrade: raw")

# 5. 상태 전이 칩
d.chip(420, 375, "프로토콜 전환 완료 (동일 TCP 소켓 유지)", WARN, 11)

# 6. 양방향 바이너리 프레임
d.bi_msg("client", "server", "양방향 바이너리 프레이밍 전송", 425, OK, sub="raw 바이트 브리징")

# 7. 테넌트 종단 트래픽 양방향 중계
d.bi_msg("client", "server", "테넌트 역방향 세션 양방향 중계", 475, INFO, sub="HTTP 프레임워크 우회 및 소켓 직접 입출력", mk_l="info_left", mk_r="info")

# 범례
d.legend(532, [
    ("기반 연결 수립", SOFT),
    ("HTTP 제어 요청", INFO),
    ("소켓 하이잭 인수", ACC),
    ("바이너리 터널 프레이밍", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-02-upgrade.svg"))
d.save(out)
print(f"saved: {out}")
