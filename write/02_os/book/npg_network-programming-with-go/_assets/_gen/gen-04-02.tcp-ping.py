# 타입 스펙: type-sequence
# 사실 출처: NPG 04-02 §3 · Listing 4-22 (ping.go), p.30-32
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 620
d = D(W, H, "TCP PING",
      "TCP 핸드셰이크 지연 측정과 응답 분기",
      "ICMP 차단 환경에서 net.DialTimeout 기반 지연 측정과 열린·닫힌·차단 포트 응답 분기",
      "SYN 전송 후 SYN-ACK 수신 시간(dur) 측정 및 RST·타임아웃 분기")

# 참여자 레인 정의
y0 = 104
lane_w = 170

LX = {
    "ping": 160,
    "dialer": 440,
    "target": 720,
}

roles = [
    ("ping", "ping 도구", "ping.go · 내 기계"),
    ("dialer", "내 OS TCP 스택", "net.DialTimeout 호출"),
    ("target", "대상 호스트", "target:port · 상대 기계"),
]

for key, name, sub in roles:
    x = LX[key]
    d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    d.t(x, y0 + 19, name, 12, INK, KR, "middle", 600)
    d.t(x, y0 + 35, sub, 11, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "middle")

lane_top = y0 + 44
y_bot = 554

# 수직 레일
for x in LX.values():
    d.line(x, lane_top + 6, x, y_bot, RULE, 1.0, "3 6")

def msg(k1, k2, y, label, col, mk="ar", dash=None, sub=None):
    x1, x2 = LX[k1], LX[k2]
    d.arrow([(x1, y), (x2, y)], col, mk, 1.4, dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y - 8, label, 11, col, MONO if any(c.isascii() for c in label) else KR, "middle", 600)
    if sub:
        d.t(mx, y + 16, sub, 11, MUTED, KR, "middle")

def self_action(k, y, label, col, mk="ar", right=True):
    x = LX[k]
    dx = 38 if right else -38
    d.path(f"M {x} {y-8} L {x+dx} {y-8} L {x+dx} {y+8} L {x} {y+8}", col, 1.3, m=mk)
    tx = x + dx + (8 if right else -8)
    anchor = "start" if right else "end"
    d.t(tx, y + 4, label, 11, col, KR, anchor, 600)

# 1. ping 도구 호출
msg("ping", "dialer", 172, "DialTimeout(target, *timeout)", MUTED, "ar")

# 2. ALT 복합 프래그먼트 프레임
fx, fy, fw, fh = 68, 202, 744, 348
d.box(fx, fy, fw, fh, fill=PAPER, stroke=RULE, sw=0.9, r=4)
d.box(fx, fy, 40, 18, fill=PAPER2, stroke=RULE, sw=0.9, r=2)
d.t(fx + 20, fy + 12, "ALT", 8, SOFT, MONO, "middle", 600)

# 분기 1: 열린 포트 (예: 80, 443)
d.t(fx + 52, fy + 14, "[열린 포트: 80·443]", 11, OK, KR, "start", 600)
msg("dialer", "target", 236, "SYN 전송", OK, "ok")
msg("target", "dialer", 260, "SYN-ACK 수신", OK, "ok")
msg("dialer", "ping", 284, "conn 반환 (dur 계산)", OK, "ok", dash="3 3", sub="dur = time.Since(t0)")
self_action("ping", 316, "c.Close() (측정 완결)", OK, "ok", right=True)

# 구분선 1
d.line(fx, 334, fx + fw, 334, RULE, 0.8, "3 4")

# 분기 2: 닫힌 포트 (리스너 부재)
d.t(fx + 52, 348, "[닫힌 포트: 리스너 부재]", 11, BAD, KR, "start", 600)
msg("dialer", "target", 368, "SYN 전송", MUTED, "ar")
msg("target", "dialer", 392, "RST 수신 (연결 거부)", BAD, "bad")
msg("dialer", "ping", 416, "err (!Timeout) 반환", BAD, "bad", dash="3 3")
self_action("ping", 436, "os.Exit(1) 종료", BAD, "bad", right=True)

# 구분선 2
d.line(fx, 452, fx + fw, 452, RULE, 0.8, "3 4")

# 분기 3: 차단된 포트 (방화벽 무응답)
d.t(fx + 52, 466, "[차단된 포트: 방화벽 필터링]", 11, WARN, KR, "start", 600)
msg("dialer", "target", 486, "SYN 전송 (패킷 드롭)", WARN, "warn")
d.t(LX["target"] + 14, 490, "응답 없음", 11, MUTED, KR, "start")
self_action("dialer", 510, "*timeout 만료", WARN, "warn", right=True)
msg("dialer", "ping", 532, "err (nErr.Timeout) 반환", WARN, "warn", dash="3 3")

# 범례
d.legend(H - 44, [("핸드셰이크 성공 (열린 포트)", OK), ("연결 거부 RST (닫힌 포트)", BAD), ("타임아웃 무응답 (차단 포트)", WARN)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-02.tcp-ping.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
