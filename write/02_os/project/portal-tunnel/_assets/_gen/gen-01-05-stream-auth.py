# 타입 스펙: type-sequence
# 사실 출처: portal/transport/stream_mux.go:22-27,115-128,158-240,
#   portal/api_server.go:491-516 (serveReverseMux),
#   sdk/reverse_transport.go:104-125 (openMux),
#   portal/identity/lease_token.go:78-82,133-147,
#   portal/lease.go:557-567.
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqMux(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ret_ar" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{MUTED}"/></marker>')
        s.o.insert(20, f'<marker id="ret_acc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{ACC}"/></marker>')
        s.o.insert(21, f'<marker id="ret_bad" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{BAD}"/></marker>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 18}" width="{_w(label, 11)}" height="15" fill="{PAPER}"/>')
        s.t(mx, y - 7, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="14" fill="{PAPER}"/>')
            s.t(mx, y + 14, sub, 10, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-8} L {x+46} {y-8} L {x+46} {y+8} L {x+13} {y+8}", c, 1.4, m="ar")
        s.t(x + 54, y - 2, label, 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 54, y + 12, sub, 10, MUTED, _kr(sub), "start")

W, H = 960, 640
d = SeqMux(W, H,
           "PORTAL-TUNNEL · REVERSE STREAM AUTHENTICATION FLOW",
           "스트림별 Capability 인증 시퀀스 (Open -> 검증 -> 수락/거절 -> Offer)",
           "터널이 새 논리 스트림마다 2바이트 길이와 capability를 전송하고 릴레이가 1바이트 수락(0) 또는 거절(1)로 응답합니다",
           lead="단일 WebSocket 위 새 스트림을 열 때마다 단기 토큰을 인증하고 대기 풀(ready)에 인입하는 절차")

NAMES = (
    ("Tunnel (SDK)", "WASM / connector"),
    ("ReverseMux", "yamux session"),
    ("Relay Server", "serveReverseMux"),
    ("Reverse Pool", "lease.reverse ready"),
)

d.lanes(NAMES, y0=104, lane_w=170)
d.rails(540)

# 액티베이션 바 (간격 및 생명주기 표시)
d.box(d.LX["Tunnel (SDK)"] - 4, 164, 8, 80, fill=PAPER2, stroke=SOFT, sw=0.8)
d.box(d.LX["Tunnel (SDK)"] - 4, 380, 8, 20, fill=PAPER2, stroke=SOFT, sw=0.8)
d.box(d.LX["Relay Server"] - 4, 230, 8, 290, fill=PAPER2, stroke=SOFT, sw=0.8)

# 1. 스트림 개설
d.msg("Tunnel (SDK)", "ReverseMux", "Open(ctx, capability)", 172, INFO, sub="sdk/reverse_transport.go:120")
d.msg("ReverseMux", "Relay Server", "yamux.OpenStream() (SYN)", 206, MUTED, sub="session.Accept() 대기 해제")

# 2. 토큰 전송
d.msg("Tunnel (SDK)", "Relay Server", "[2B len][capability bytes]", 242, ACC, sub="stream_mux.go:186 (최대 8 KiB)")

# 3. 릴레이 검증 (selfmsg)
d.selfmsg("Relay Server", "readReverseStreamCapability()", 278, MUTED, sub="8 KiB 상한 · 10초 타임아웃 검증")
d.selfmsg("Relay Server", "admitReverseCapability()", 314, INFO, sub="capability 토큰 검증 · 임대 대조")

# ALT 프레임
fx, fy, fw, fh = 36, 344, 888, 186
d.box(fx, fy, fw, fh, fill=f"{PAPER2}88", stroke=RULE, sw=1.0, r=4)
# ALT 탭
d.box(fx, fy, 36, 16, fill=PAPER, stroke=RULE, sw=1.0, r=2)
d.t(fx + 18, fy + 11, "ALT", 8, SOFT, fam=MONO, anchor="middle", weight=600)

# Guard 1: authorized
d.t(fx + 44, fy + 12, "[authorized]", 9, OK, fam=MONO, anchor="start")
d.msg("Relay Server", "Tunnel (SDK)", "0x00 (Accepted)", 388, ACC, mk="ret_acc", dash="4 3", sub="ConfirmReverseStream(conn, true)")
d.msg("Relay Server", "Reverse Pool", "lease.reverse.Offer(stream)", 424, OK, sub="대기 풀(ready) 등록 완료")

# 분기 구분선
d.line(fx + 8, 452, fx + fw - 8, 452, RULE, 0.9, dash="4 3")

# Guard 2: unauthorized
d.t(fx + 44, 466, "[unauthorized]", 9, BAD, fam=MONO, anchor="start")
d.msg("Relay Server", "Tunnel (SDK)", "0x01 (Rejected)", 484, BAD, mk="ret_bad", dash="4 3", sub="ConfirmReverseStream(conn, false)")
d.selfmsg("Relay Server", "stream.Close()", 514, BAD, sub="무단 스트림 즉시 차단")

# 범례
d.legend(568, [
    ("동기 요청 / 호출", INFO),
    ("헤드라인 수락 응답 (Focal)", ACC),
    ("인가 완료 대기 풀 등록", OK),
    ("인증 실패 차단", BAD),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-05-stream-auth.svg"))
d.save(out)
print(f"saved: {out}")
