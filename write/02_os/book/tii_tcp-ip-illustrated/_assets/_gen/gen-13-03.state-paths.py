# 13-03 상태 지도: 원서 Figure 13-8·13-9와 §13.5.5의 대표 경로만 재구성.
# 타입 스펙: type-process — 역할별 단계가 좌→우로 진행. 닫기 두 경로의 마지막 상태 차이가 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, WARN, OK, MUTED, INK, SOFT, RULE, KR, MONO

W, H = 1000, 432
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-03 §1–4",
      "TCP의 대표 상태 경로", 
      "원서 Figure 13-8·13-9를 경로별로 다시 묶었다. 능동 열기와 수동 열기는 ESTABLISHED에서 만나고, 능동 닫기는 TIME_WAIT를 거친다. 수동 닫기는 LAST_ACK에서 끝나며 동시 닫기는 양쪽 모두 CLOSING과 TIME_WAIT를 거친다.",
      "두 끝점은 상태를 따로 갖고, 먼저 닫은 쪽의 경로가 길어집니다")

rows = [
    ("능동 열기", 112, ["CLOSED", "SYN_SENT", "ESTABLISHED"], INFO),
    ("수동 열기", 178, ["CLOSED", "LISTEN", "SYN_RCVD", "ESTABLISHED"], INFO),
    ("능동 닫기", 244, ["ESTABLISHED", "FIN_WAIT_1", "FIN_WAIT_2", "TIME_WAIT", "CLOSED"], WARN),
    ("수동 닫기", 310, ["ESTABLISHED", "CLOSE_WAIT", "LAST_ACK", "CLOSED"], OK),
    ("동시 닫기", 376, ["ESTABLISHED", "FIN_WAIT_1", "CLOSING", "TIME_WAIT", "CLOSED"], ACC),
]

X0, BW, BH, GAP = 143, 148, 38, 18
for label, cy, states, color in rows:
    d.t(16, cy + 5, label, 13, color, KR, "start", 600)
    for i, state in enumerate(states):
        x = X0 + i * (BW + GAP)
        if state == "TIME_WAIT":
            d.tone(x, cy - BH / 2, BW, BH, ACC)
        else:
            d.box(x, cy - BH / 2, BW, BH)
        d.t(x + BW / 2, cy + 5, state, 11, ACC if state == "TIME_WAIT" else INK, MONO, "middle", 600)
        if i < len(states) - 1:
            d.arrow([(x + BW + 3, cy), (x + BW + GAP - 3, cy)], color, "ar", 1.5)

d.save("13-03.state-paths.svg")
