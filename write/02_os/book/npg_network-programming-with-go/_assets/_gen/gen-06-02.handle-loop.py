# 타입 스펙: type-state
# 06-02 TFTP 서버 handle 루프 상태 기계
# 사실 출처: NPG Ch.6 p.18-20 (Listing 6-9, 6-10, Server.handle)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 460
d = D(W, H, "NPG CH.6 — TFTP SERVER STATE MACHINE",
      "TFTP 서버 handle 루프 상태 전이",
      "Listing 6-10 블록 전송·ACK 대기·재전송 및 종료 상태 기계",
      "블록 전송 후 ACK 확인·타임아웃 재전송·완료 분기")

def draw_state(x, y, w, h, name, sub=None, c=MUTED, focal=False):
    fill = f"{c}15" if focal else PAPER2
    stroke = c if focal else RULE
    sw = 1.6 if focal else 1.0
    d.box(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=8)
    d.t(x + w / 2, y + (20 if sub else 28), name, 12, INK if not focal else c, KR, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 36, sub, 11, SOFT, MONO if any(c.isascii() and c.isalnum() for c in sub) else KR, "middle")

# 1. 시작점
d.o.append(f'<circle cx="35" cy="200" r="7" fill="{INK}"/>')
d.t(35, 224, "요청 수신", 11, SOFT, KR, "middle")
d.arrow([(42, 200), (85, 200)], INFO, "info", 1.4)

# 2. 상태 노드들
# PREPARE
draw_state(85, 175, 140, 50, "데이터 준비", "Block++ / 512B", INFO)

# SEND
draw_state(295, 175, 130, 50, "블록 송신", "conn.Write", OK, focal=True)

# WAIT_ACK
draw_state(495, 175, 140, 50, "ACK 대기", "Timeout 6초", WARN, focal=True)

# DONE (전송 완료)
draw_state(720, 110, 95, 50, "전송 완료", "정상 종료", OK)
d.arrow([(815, 135), (840, 135)], OK, "ok", 1.3)
d.o.append(f'<circle cx="848" cy="135" r="8" fill="none" stroke="{OK}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="848" cy="135" r="4" fill="{OK}"/>')

# ABORT (중단)
draw_state(720, 240, 95, 50, "전송 중단", "오류 로그", BAD)
d.arrow([(815, 265), (840, 265)], BAD, "bad", 1.3)
d.o.append(f'<circle cx="848" cy="265" r="8" fill="none" stroke="{BAD}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="848" cy="265" r="4" fill="{BAD}"/>')

# 간선들:
# PREPARE -> SEND
d.arrow([(225, 200), (295, 200)], MUTED, "ar", 1.4)

# SEND -> WAIT_ACK
d.arrow([(425, 200), (495, 200)], MUTED, "ar", 1.4)

# WAIT_ACK -> DONE (ACK 일치 & n < 516)
d.arrow([(635, 190), (675, 190), (675, 135), (720, 135)], OK, "ok", 1.4)
d.t(650, 122, "ACK 일치 (<516B)", 11, OK, KR, "middle", 600)

# WAIT_ACK -> PREPARE 루프 (ACK 일치 & n == 516) [NEXTPACKET]
d.arrow([(565, 175), (565, 100), (155, 100), (155, 175)], OK, "ok", 1.4)
d.t(360, 90, "ACK 일치 (516B 전송 완료) → 다음 블록", 11, OK, KR, "middle", 600)

# WAIT_ACK -> SEND 루프 (타임아웃 / 블록 불일치 & i > 0) [RETRY]
d.arrow([(565, 225), (565, 300), (360, 300), (360, 225)], WARN, "warn", 1.4, dash="4 4")
d.t(462, 316, "타임아웃 (재시도 i > 0, 최대 10회)", 11, WARN, KR, "middle", 600)

# WAIT_ACK -> ABORT (i == 0 소진 또는 Err 수신)
d.arrow([(635, 210), (675, 210), (675, 265), (720, 265)], BAD, "bad", 1.4)
d.t(645, 282, "재시도 소진 / Err 수신", 11, BAD, KR, "middle", 600)

# Legend
d.legend(H - 42, [("정상 진행", OK), ("타임아웃 재전송", WARN), ("오류 중단", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06-02.handle-loop.svg"))
d.save(out)
print(f"saved: {out}")
