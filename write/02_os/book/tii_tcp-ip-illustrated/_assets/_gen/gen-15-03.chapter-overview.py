# 타입 스펙: type-process — BDP 대역폭·지연 곱에서 버퍼 한계, 자동 조정, 긴급 포인터, 창 공격으로 이어지는 흐름.
# 사실 출처: 원서 §15.5.4–15.7 — 100ms·1Gbps 경로 BDP 13MB, 64KB 고정 버퍼 한계, 2×MSS 자동 조정, URG 6146 위치 표시, 0 창 악용 공격.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER2, RULE, KR, MONO, INFO

W, H = 920, 390
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-03", "수신 버퍼 자동 조정과 창 제어의 신뢰성·보안 흐름",
      "고속 경로를 채우기 위해 수신 버퍼를 자동으로 키우고, 긴급 포인터와 0 창을 둘러싼 실제 동작과 공격을 분석합니다.",
      "수신 버퍼는 자동 조정으로 커지고 긴급 포인터는 위치 표시만 남깁니다")

CW, CH, GAP, X0, Y = 152, 136, 32, 24, 136
steps = [
    ("1. BDP 경로", "대역폭·지연 곱", "1Gbps · 100ms", "12.5MB 필요 용량", INFO),
    ("2. 고정 버퍼", "64KB 한계 병목", "win = 65535", "처리율 99% 낭비", WARN),
    ("3. 자동 조정", "소비·RTT 연동", "최대 67808B", "2×MSS 씩 확장", OK),
    ("4. 긴급 표시", "0 창 중 위치 전달", "URG · 6146", "인라인 순서 보존", ACC),
    ("5. 창 공격", "상대 자원 잠금", "0 창 고착", "persist 무한 탐침", BAD),
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

d.legend(H - 52, [("경로 잠재력", INFO), ("고정 버퍼 병목", WARN), ("수신 버퍼 자동 조정", OK), ("긴급 표시(URG)", ACC), ("자원 고갈 공격", BAD)])
d.save("15-03.chapter-overview.svg")
