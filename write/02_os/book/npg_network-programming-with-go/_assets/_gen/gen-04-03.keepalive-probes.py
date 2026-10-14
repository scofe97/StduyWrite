# 타입 스펙: type-sequence
# 사실 출처: NPG 04-03 §2 · Listing 4-25 (KeepAliveConfig), p.33-34
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 568
d = D(W, H, "TCP KEEPALIVE PROBES",
      "OS 커널의 TCP keepalive 탐침과 소켓 파기",
      "유휴 시간(Idle) 후 탐침 전송, 간격(Interval) 재탐침 및 횟수(Count) 초과 시 소켓 파기 시퀀스",
      "커널 빈 ACK 탐침 반복 후 무응답 지속 시 소켓 파기 및 앱 Read 에러 통보")

# 참여자 레인 정의
y0 = 104
lane_w = 170

LX = {
    "app": 160,
    "kernel": 440,
    "peer": 720,
}

roles = [
    ("app", "Go 애플리케이션", "conn.Read() 블로킹 대기"),
    ("kernel", "로컬 커널 (OS)", "KeepAliveConfig 제어"),
    ("peer", "원격 호스트 (피어)", "크래시 / 네트워크 단절"),
]

for key, name, sub in roles:
    x = LX[key]
    d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    d.t(x, y0 + 19, name, 12, INK, KR, "middle", 600)
    d.t(x, y0 + 35, sub, 11, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "middle")

lane_top = y0 + 44
y_bot = 506

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

# 1. 앱 Read() 블로킹
msg("app", "kernel", 172, "conn.Read(buf) 수신 대기", MUTED, "ar")

# 2. 커널 유휴 시간 경과 (Idle: 30s)
self_action("kernel", 204, "유휴 시간 경과 (Idle: 30s)", MUTED, "ar", right=True)

# 3. 1차 탐침
msg("kernel", "peer", 240, "1차 탐침 (Probe #1: 빈 ACK)", WARN, "warn")
d.t(LX["peer"] + 14, 244, "응답 없음", 11, MUTED, KR, "start")

# 4. 재전송 간격 경과 (Interval: 10s)
self_action("kernel", 274, "재탐침 간격 경과 (Interval: 10s)", WARN, "warn", right=True)

# 5. 2차 탐침
msg("kernel", "peer", 310, "2차 탐침 (Probe #2: 빈 ACK)", WARN, "warn")
d.t(LX["peer"] + 14, 314, "응답 없음", 11, MUTED, KR, "start")

# 6. 중간 생략 구분선
d.line(410, 336, 470, 336, RULE, 0.8, "3 4")
d.t(440, 354, "… Interval: 10s 마다 재탐침 반복 (3·4차) …", 11, MUTED, KR, "middle")
d.line(410, 370, 470, 370, RULE, 0.8, "3 4")

# 7. 5차 탐침 (Count: 5 최종 도달)
msg("kernel", "peer", 396, "5차 탐침 (Probe #5: Count 5 도달)", BAD, "bad")
d.t(LX["peer"] + 14, 400, "최종 무응답", 11, BAD, KR, "start")

# 8. 소켓 파기
self_action("kernel", 432, "Count: 5 초과 → 소켓 강제 파기", BAD, "bad", right=True)

# 9. 앱 Read 에러 반환
msg("kernel", "app", 466, "Read 에러 반환 (connection timed out)", BAD, "bad", dash="3 3")

# 10. 앱 에러 처리
self_action("app", 492, "소켓 정리 및 에러 핸들링", BAD, "bad", right=True)

# 범례
d.legend(H - 44, [("정상 수신 대기 / 유휴", MUTED), ("keepalive 탐침 (무응답)", WARN), ("실패 한도 초과 / 소켓 파기", BAD)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-03.keepalive-probes.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
