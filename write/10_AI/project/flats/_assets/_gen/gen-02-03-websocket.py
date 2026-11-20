# 사실 출처: internal/runtime/ws.go:37-57,104-133,186-200,330-360,420-440 · internal/runtime/prelude.js:505-555 · docs/runtime-api-v1.md:243-259
# 타입 스펙: type-sequence
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 700

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub), "middle")

    def selfmsg(s, a, label, y, c=MUTED, sub=None, to_left=False):
        x = s.LX[a]
        dx = -42 if to_left else 42
        d_arrow = -1 if to_left else 1
        s.path(f"M {x + 10 * d_arrow} {y - 10} L {x + dx} {y - 10} L {x + dx} {y + 10} L {x + 12 * d_arrow} {y + 10}", c, 1.4, m="ar")
        anchor = "end" if to_left else "start"
        tx = x + dx - 8 if to_left else x + dx + 8
        s.t(tx, y - 4, label, 11, c, _kr(label), anchor, 600)
        if sub:
            s.t(tx, y + 14, sub, 10, MUTED, _kr(sub), anchor)

d = SeqKR(
    W, H,
    "SEQUENCE · WEBSOCKET PROTOCOL",
    "WebSocket 생명주기와 메시지 교환 흐름",
    "RFC 6455 101 업그레이드 수납 후 전용 VM 콜백과 큐 기반 송출 파이프라인 구동",
    lead="브라우저 ── Upgrade / 101 ──> worker (upgradeWS) ── 전용 VM ──> open / message / close"
)

lanes = d.lanes([
    ("방문자 브라우저", "WebSocket Client"),
    ("flats worker", "Go wsConn & wsHub"),
    ("WebSocket VM", "QuickJS Runtime")
], y0=96, lane_w=190)

d.rails(672)

def sec(y, txt, c):
    w = sum(11 if "가" <= ch <= "힣" else 6.6 for ch in txt) + 16
    d.box(28, y - 13, w, 20, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.t(36, y + 2, txt, 11, c, fam=KR, anchor="start", weight=600)

# 1. 프로토콜 업그레이드
sec(159, "1. WebSocket 핸드셰이크", INFO)
d.msg("방문자 브라우저", "flats worker", "GET / (Upgrade: websocket)", 176, INFO, "info", sub="Key: <nonce>")
d.selfmsg("flats worker", "upgradeWS & wsAccept", 214, INFO, sub="SHA-1(Key + GUID) 계산")
d.msg("flats worker", "방문자 브라우저", "101 Switching Protocols", 252, OK, "ok", sub="Accept: <hash>")
d.msg("flats worker", "WebSocket VM", "__flats_ws(\"open\")", 290, ACC, "acc", sub="open(ws, env)")

# 2. 메시지 수신 및 송신
sec(330, "2. 메시지 왕복 처리", OK)
d.msg("방문자 브라우저", "flats worker", "readFrame (Masked, ≤1 MiB)", 356, MUTED, "ar", sub="opText/opBinary 디코딩")
d.msg("flats worker", "WebSocket VM", "__flats_ws(\"message\")", 398, OK, "ok", sub="message(ws, data, env)")
d.msg("WebSocket VM", "flats worker", "ws.send(data) -> hostCall", 442, ACC, "acc", sub="host(\"ws.send\", [id, data])")
d.selfmsg("flats worker", "sendQ 큐잉 (≤256건)", 484, WARN, sub="연결 4 MiB · flat 16 MiB")
d.msg("flats worker", "방문자 브라우저", "writer() 프레임 전송", 524, OK, "ok", sub="Unmasked Text 송출")

# 3. 하트비트 및 유휴 만료
sec(562, "3. 하트비트 및 유휴 만료", WARN)
d.msg("flats worker", "방문자 브라우저", "30s 주기 ping (opPing 0x9)", 588, MUTED, "ar", sub="브라우저 자동 pong")
d.selfmsg("flats worker", "2분 무응답 시 end(1001)", 628, BAD, sub="wsReadIdleTimeout 만료", to_left=True)
d.msg("flats worker", "WebSocket VM", "__flats_ws(\"close\")", 664, BAD, "bad", sub="close(ws, env)")

out_svg = Path(__file__).parent.parent / "02-03-websocket.svg"
d.save(str(out_svg))
print(f"Generated: {out_svg}")
