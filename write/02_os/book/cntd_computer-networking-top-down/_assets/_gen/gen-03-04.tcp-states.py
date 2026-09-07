# 03-04 §2 — 원문 Figure 3.39. 클라이언트 TCP 가 지나는 전형적인 상태 순서.
# 전이 라벨은 원문 서술 그대로다(보낸 것 / 받은 것). TIME_WAIT 의 대기 시간도 원문의 세 값을 적었다.
# 타입 스펙: type-state — 유한 상태와 전이. 전이는 `사건 / 동작` 으로 적고 초점 상태 하나에 강조색.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 604
BW, BH = 156, 50
ROW1, ROW2 = 176, 372
TOP = [(126, "CLOSED", ""), (346, "SYN_SENT", "SYN 보냄"), (566, "ESTABLISHED", "데이터 교환"), (806, "FIN_WAIT_1", "FIN 보냄")]
BOT = [(806, "FIN_WAIT_2", "상대 FIN 대기"), (566, "TIME_WAIT", "마지막 ACK 대비"), (306, "CLOSED", "자원 반납")]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §2",
      "클라이언트 TCP 가 지나는 상태",
      "원문 Figure 3.39. 연결을 세우고 데이터를 주고받고 허무는 동안 지나는 상태와 그 전이.",
      "TIME_WAIT 는 마지막 확인 응답이 유실됐을 때를 대비한 자리입니다")

def st(cx, cy, name, sub, c=MUTED, focal=False):
    if focal: d.tone(cx - BW / 2, cy - BH / 2, BW, BH, c, 8, "14", 1.4)
    else: d.box(cx - BW / 2, cy - BH / 2, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(cx, cy - 2, name, 11, c if focal else INK, MONO, "middle", 600)
    if sub: d.t(cx, cy + 16, sub, 11, SOFT, KR)

d.o.append(f'<circle cx="46" cy="{ROW1}" r="6" fill="{INK}"/>')
d.path(f"M 54 {ROW1} L {126 - BW/2 - 10} {ROW1}", MUTED, 1.3, m="ar")

for cx, n, s in TOP: st(cx, ROW1, n, s)
st(806, ROW2, "FIN_WAIT_2", "상대 FIN 대기")
st(566, ROW2, "TIME_WAIT", "30초 · 1분 · 2분", ACC, True)
st(306, ROW2, "CLOSED", "자원 반납", OK, True)

TRANS = [
    ((126, 346), ROW1, "connect() / SYN 보냄", MUTED),
    ((346, 566), ROW1, "SYNACK 받음 / ACK 보냄", MUTED),
    ((566, 806), ROW1, "close() / FIN 보냄", MUTED),
]
for (a, b), y, lab, c in TRANS:
    d.path(f"M {a + BW/2 + 4} {y} L {b - BW/2 - 10} {y}", c, 1.3, m="ar")
    d.t((a + b) / 2, y - 12, lab, 11, SOFT, KR)

d.path(f"M 806 {ROW1 + BH/2 + 4} L 806 {ROW2 - BH/2 - 10}", MUTED, 1.3, m="ar")
d.t(818, (ROW1 + ROW2) / 2, "ACK 받음", 11, SOFT, KR, "start")

d.path(f"M {806 - BW/2 - 4} {ROW2} L {566 + BW/2 + 10} {ROW2}", ACC, 1.4, m="acc")
d.t((806 + 566) / 2, ROW2 - 12, "상대 FIN 받음 / ACK 보냄", 11, ACC, KR)

d.path(f"M {566 - BW/2 - 4} {ROW2} L {306 + BW/2 + 10} {ROW2}", OK, 1.4, m="ok")
d.t((566 + 306) / 2, ROW2 - 12, "대기 시간 만료", 11, OK, KR)
d.o.append(f'<circle cx="{306 - BW/2 - 26}" cy="{ROW2}" r="8" fill="none" stroke="{INK}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{306 - BW/2 - 26}" cy="{ROW2}" r="5" fill="{INK}"/>')
d.path(f"M {306 - BW/2 - 4} {ROW2} L {306 - BW/2 - 16} {ROW2}", MUTED, 1.3, m="ar")

d.t(24, 470, "TIME_WAIT 가 있는 이유는 하나입니다. 마지막 확인 응답이 유실됐을 때 다시 보낼 수 있어야 하기 때문입니다.",
     11, MUTED, KR, "start")
d.t(24, 492, "이 대기가 끝나야 포트 번호를 포함한 자원이 풀립니다. 연결을 먼저 닫는 쪽이 이 상태를 떠안습니다.",
     11, MUTED, KR, "start")
d.t(24, 522, "이 맥에서 sysctl net.inet.tcp.msl 이 15000 ms 이므로 TIME_WAIT 는 2×MSL 인 30초입니다 — 원문이 든 세 값 중 첫 번째와 맞습니다.",
     11, SOFT, KR, "start")

d.legend(H - 44, [("마지막 ACK 재전송 대비", ACC), ("자원이 풀리는 자리", OK), ("나머지 상태", MUTED)])
d.save("03-04.tcp-states.svg")
