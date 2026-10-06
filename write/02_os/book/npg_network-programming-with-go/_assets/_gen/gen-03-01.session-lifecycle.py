# 03-01 세션 생애주기 — 소켓 상태 전이와 Go API
# 사실 출처: NPG Ch.3 Fig 3-1, 3-4 (p.3, p.7)
# 타입 스펙: type-state — 클라이언트와 서버의 TCP 소켓 상태 기계와 API 호출 및 세그먼트 전이
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 420
d = D(W, H, "NPG CH.3 — TCP STATE MACHINE",
      "TCP 세션 상태 전이와 Go API",
      "소켓 호출과 패킷 송수신에 따른 상태 전이",
      "핸드셰이크로 ESTABLISHED 에 도달하고 FIN·RST 로 종료")

# State Boxes definition
def draw_state(x, y, w, h, name, role_tag=None, c=MUTED, focal=False):
    fill = f"{c}15" if focal else PAPER2
    stroke = c if focal else RULE
    sw = 1.6 if focal else 1.0
    d.box(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=8)
    d.t(x + w / 2, y + (h / 2 + 5 if not role_tag else h / 2 - 2), name, 13, INK if not focal else c, MONO, "middle", 600)
    if role_tag:
        d.t(x + w / 2, y + h / 2 + 13, role_tag, 11, SOFT, KR, "middle")

# Initial Start Dot
d.o.append(f'<circle cx="30" cy="180" r="7" fill="{INK}"/>')
d.t(30, 205, "시작", 11, SOFT, KR, "middle")

# Client branch (Top)
d.arrow([(37, 180), (55, 180), (55, 150), (160, 150)], c=INFO, m="info")
d.t(105, 140, "Dial / SYN", 11, INFO, MONO, "middle", 600)

# Server branch (Bottom)
d.arrow([(37, 180), (55, 180), (55, 210), (160, 210)], c=WARN, m="warn")
d.t(105, 228, "Listen / Accept", 11, WARN, MONO, "middle", 600)

# ESTABLISHED (Center Focal)
draw_state(160, 145, 130, 70, "ESTABLISHED", "세션 수립", OK, focal=True)

# RST Transition (Direct to CLOSED)
d.arrow([(225, 215), (225, 330), (765, 330), (765, 205)], c=BAD, m="bad", dash="4 4")
d.t(495, 322, "RST (강제 리셋)", 11, BAD, KR, "middle", 600)

# Client Termination (Top lane)
# ESTABLISHED -> FIN_WAIT_1
d.arrow([(245, 145), (245, 120), (335, 120)], c=INFO, m="info")
d.t(290, 110, "Close / FIN", 11, INFO, MONO, "middle", 600)
draw_state(335, 95, 115, 50, "FIN_WAIT_1", "클라이언트", INFO)

# FIN_WAIT_1 -> TIME_WAIT
d.arrow([(450, 120), (570, 120)], c=MUTED, m="ar")
d.t(510, 110, "FIN 수신 / ACK 송신", 11, MUTED, KR, "middle")
draw_state(570, 95, 115, 50, "TIME_WAIT", "2*MSL 대기", WARN)

# TIME_WAIT -> CLOSED
d.arrow([(685, 120), (710, 120), (710, 165), (730, 165)], c=MUTED, m="ar")
d.t(710, 110, "시한 만료", 11, MUTED, KR, "middle")

# Server Termination (Bottom lane)
# ESTABLISHED -> CLOSE_WAIT
d.arrow([(245, 215), (245, 240), (335, 240)], c=WARN, m="warn")
d.t(290, 255, "FIN 수신", 11, WARN, KR, "middle")
draw_state(335, 215, 115, 50, "CLOSE_WAIT", "서버 수신", WARN)

# CLOSE_WAIT -> LAST_ACK
d.arrow([(450, 240), (570, 240)], c=WARN, m="warn")
d.t(510, 230, "Close / FIN", 11, WARN, MONO, "middle", 600)
draw_state(570, 215, 115, 50, "LAST_ACK", "최종 ACK 대기", WARN)

# LAST_ACK -> CLOSED
d.arrow([(685, 240), (710, 240), (710, 195), (730, 195)], c=MUTED, m="ar")
d.t(710, 255, "ACK 수신", 11, MUTED, KR, "middle")

# Final CLOSED (End Ring)
draw_state(730, 155, 65, 50, "CLOSED", None, MUTED)
d.arrow([(795, 180), (805, 180)], c=MUTED, m="ar")
d.o.append(f'<circle cx="817" cy="180" r="8" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="817" cy="180" r="4" fill="{MUTED}"/>')

# Legend
d.legend(375, [("클라이언트", INFO), ("서버", WARN), ("수립", OK), ("리셋", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-01.session-lifecycle.svg"))
d.save(out)
print(f"saved: {out}")
