# 타입 스펙: type-sequence
# 사실 출처: RFC 9000 §1.2, RFC 9113 §5.1,
#   docs/maintainer/architecture.md,
#   write/02_os/project/portal-tunnel/01-05.stream_mux·yamux.md,
#   write/02_os/project/portal-tunnel/01-07.quic_backhaul·datagram.md.
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

W, H = 960, 680
d = D(W, H, "PORTAL-TUNNEL · HEAD-OF-LINE BLOCKING",
      "TCP 다중화와 QUIC의 패킷 유실 전파 비교",
      "동일한 패킷 손실이 발생했을 때 TCP 단일 스트림 다중화는 무관한 스트림까지 전체 대기시키지만 QUIC은 독립 스트림 오프셋을 통해 유실 스트림만 격리 대기시킵니다.",
      "단일 TCP 연결 다중화는 패킷 유실 시 모든 스트림이 멈추고 QUIC은 손실 스트림만 격리합니다")

# 참가자 레인 X 좌표
LX = {"sender": 180, "stack": 500, "app": 800}

# 상단 트랙: TCP 위 다중화 (HTTP/2 · yamux)
d.box(24, 96, W - 48, 252, PAPER2, RULE, 1.0)
d.t(40, 120, "TCP 위 다중화: 단일 바이트 스트림 순서 보장 (HTTP/2 · yamux)", 12, WARN, KR, "start", 600)

for k, (nm, sub) in [("sender", ("송신 호스트", "다중 스트림 송신")),
                      ("stack", ("수신 TCP 스택", "단일 순서 큐")),
                      ("app", ("수신 애플리케이션", "Stream A · B"))]:
    x = LX[k]
    d.box(x - 70, 132, 140, 36, PAPER, RULE, 0.8)
    d.t(x, 148, nm, 11, INK, KR, "middle", 600)
    d.t(x, 161, sub, 9, MUTED, _kr(sub))
    d.line(x, 168, x, 336, RULE, 0.8, "3 4")

# TCP 메시지 흐름
def msg(a, b, label, y, c=MUTED, mk="ar", sub=None, dash=None):
    x1, x2 = LX[a], LX[b]
    dd = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.4, m=mk, dash=dash)
    mx = (x1 + x2) / 2
    d.o.append(f'<rect x="{mx - _w(label, 10)/2}" y="{y - 15}" width="{_w(label, 10)}" height="14" fill="{PAPER}"/>')
    d.t(mx, y - 5, label, 10, c, _kr(label), "middle", 600)
    if sub:
        d.o.append(f'<rect x="{mx - _w(sub, 9)/2}" y="{y + 3}" width="{_w(sub, 9)}" height="13" fill="{PAPER}"/>')
        d.t(mx, y + 13, sub, 9, MUTED, _kr(sub))

def lost_msg(a, b, label, y, c=BAD, sub=None):
    x1, x2 = LX[a], LX[b]
    mx = (x1 + x2) / 2
    d.line(x1 + 10, y, mx - 10, y, c, 1.4, "4 4")
    d.line(mx - 8, y - 8, mx + 8, y + 8, BAD, 2.0)
    d.line(mx - 8, y + 8, mx + 8, y - 8, BAD, 2.0)
    d.o.append(f'<rect x="{mx - _w(label, 10)/2}" y="{y - 18}" width="{_w(label, 10)}" height="14" fill="{PAPER}"/>')
    d.t(mx, y - 7, label, 10, c, _kr(label), "middle", 600)
    if sub:
        d.o.append(f'<rect x="{mx - _w(sub, 9)/2}" y="{y + 6}" width="{_w(sub, 9)}" height="13" fill="{PAPER}"/>')
        d.t(mx, y + 16, sub, 9, BAD, _kr(sub))

# 1. 패킷 1 (Stream A: Chunk 1) 정상
msg("sender", "stack", "패킷 1 (Stream A)", 188, INFO, "info")
msg("stack", "app", "Stream A 수신", 188, INFO, "info")

# 2. 패킷 2 (Stream A: Chunk 2) 유실
lost_msg("sender", "stack", "패킷 2 (Stream A)", 224, BAD, sub="네트워크 유실")

# 3. 패킷 3 (Stream B: Chunk 1) 도착했으나 대기
msg("sender", "stack", "패킷 3 (Stream B)", 260, WARN, "warn")
# 커널 스택 상태 칩
d.chip(LX["stack"], 286, "수신 버퍼 억류 (HOL 블로킹)", BAD, 10)

# 4. 재전송 도착 후 동시 전달
msg("sender", "stack", "패킷 2 재전송", 318, OK, "ok")
msg("stack", "app", "Stream A · B 일괄 전달", 318, OK, "ok")


# 하단 트랙: QUIC 전송 (RFC 9000)
d.box(24, 364, W - 48, 252, PAPER2, RULE, 1.0)
d.t(40, 388, "QUIC 전송: 스트림별 독립 순서 큐 (RFC 9000)", 12, OK, KR, "start", 600)

for k, (nm, sub) in [("sender", ("송신 호스트", "독립 스트림 프레이밍")),
                      ("stack", ("수신 QUIC 스택", "스트림별 독립 큐")),
                      ("app", ("수신 애플리케이션", "Stream A · B"))]:
    x = LX[k]
    d.box(x - 70, 400, 140, 36, PAPER, RULE, 0.8)
    d.t(x, 416, nm, 11, INK, KR, "middle", 600)
    d.t(x, 429, sub, 9, MUTED, _kr(sub))
    d.line(x, 436, x, 604, RULE, 0.8, "3 4")

# QUIC 메시지 흐름
# 1. 패킷 1 (Stream A: Offset 0) 정상
msg("sender", "stack", "패킷 1 (Stream A)", 456, INFO, "info")
msg("stack", "app", "Stream A 수신", 456, INFO, "info")

# 2. 패킷 2 (Stream A: Offset 100) 유실
lost_msg("sender", "stack", "패킷 2 (Stream A)", 492, BAD, sub="네트워크 유실")

# 3. 패킷 3 (Stream B: Offset 0) 도착 즉시 앱 전달!
msg("sender", "stack", "패킷 3 (Stream B)", 528, OK, "ok")
msg("stack", "app", "Stream B 즉시 전달", 528, OK, "ok")
d.chip(LX["stack"], 554, "Stream A만 격리 대기 (Stream B 정상 진행)", OK, 10)

# 4. Stream A 재전송 도착
msg("sender", "stack", "패킷 2 재전송", 586, OK, "ok")
msg("stack", "app", "Stream A 수신 완료", 586, OK, "ok")

# 범례
d.legend(634, [
    ("정상 스트림 전달", INFO),
    ("패킷 유실", BAD),
    ("버퍼 억류 (HOL)", WARN),
    ("재전송 및 복구", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-02-hol.svg"))
d.save(out)
print(f"saved: {out}")
