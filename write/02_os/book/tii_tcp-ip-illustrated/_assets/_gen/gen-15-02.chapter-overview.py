# 타입 스펙: type-process — 창 광고에서 0 창, persist 탐침, 재개로 이어지는 흐름.
# 사실 출처: 원서 §15.5–15.5.2.1 — 3000B 창 광고, 버퍼 포화로 0 창 광고, 업데이트 유실 방지 탐침, 재개.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 920, 390
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-02", "수신 창 제어와 persist 타이머의 재개 흐름",
      "수신자는 버퍼 여유에 따라 창을 광고하고, 버퍼가 차면 0 창으로 송신을 멈춘다. 창 업데이트 유실(가상 시나리오)로 인한 교착을 송신자의 persist 탐침이 해소한다.",
      "0 창 광고는 송신을 멈추고 persist 탐침은 닫힌 창을 다시 두드립니다")

CW, CH, GAP, X0, Y = 152, 136, 32, 24, 136
steps = [
    ("1. 창 광고", "정상 수신 여유", "win = 3000", "데이터 계속 전송", OK),
    ("2. 버퍼 포화", "앱 미소비로 포화", "win = 0", "송신 전면 중단", BAD),
    ("3. 갱신 유실", "순수 ACK 유실(가상)", "win 1535 유실", "양측 무한 대기", WARN),
    ("4. persist 탐침", "타이머 만료 작동", "1B ZWP", "강제 ACK 유도", ACC),
    ("5. 전송 재개", "열린 창 크기 갱신", "win = 1535", "정상 전송 재개", OK),
]

for i, (title, sub1, val, sub2, color) in enumerate(steps):
    x = X0 + i * (CW + GAP)
    d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 6)
    d.tone(x, Y, CW, 30, color, 6, "18", 1.0)
    d.t(x + CW/2, Y + 20, title, 13, color, KR, "middle", 600)
    d.t(x + CW/2, Y + 54, sub1, 12, MUTED, KR, "middle")
    d.chip(x + CW/2, Y + 82, val, color, 12)
    d.t(x + CW/2, Y + 114, sub2, 12, INK, KR, "middle", 500)
    if i < len(steps) - 1:
        nx = x + CW
        d.arrow([(nx + 4, Y + CH/2), (nx + GAP - 4, Y + CH/2)], MUTED, "ar", 1.5)

d.legend(H - 52, [("정상 수신 및 재개", OK), ("버퍼 고갈(0 창)", BAD), ("교착 위험", WARN), ("persist 탐침", ACC)])
d.save("15-02.chapter-overview.svg")
