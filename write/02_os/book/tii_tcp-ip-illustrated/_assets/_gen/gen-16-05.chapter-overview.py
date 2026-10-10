# 타입 스펙: type-process — 버퍼블로트 지연부터 AQM·ECN 완화와 혼잡 제어 공격 방어까지 4단계 흐름과 공격 방어.
# 사실 출처: ch16.txt 2851~3162행 — 대용량 버퍼 지연(16.10), RED 조기 감지(16.11), ECN 왕복 피드백(16.11), 비정상 수신자 공격(16.12).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 460
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-05",
      "버퍼블로트·AQM·ECN 4단계 흐름과 공격 방어",
      "대용량 버퍼로 인한 큐잉 지연 폭증을 능동 대기열 관리(AQM)로 조기 감지하고, 명시적 혼잡 통보(ECN)로 패킷 손실 없이 송신 창을 줄이며, 조작된 ACK 로 전송률을 가로채는 수신자 공격을 방어합니다.",
      "손실 전에 혼잡을 알리고 비정상 수신자의 가속을 억제합니다")

CW, CH, GAP = 158, 200, 18
X0 = 24
Y = 136

STEPS = [
    ("1단계", "버퍼블로트", "지연 축적", "버퍼 포화", "초 단위 지연", BAD),
    ("2단계", "AQM 개입", "조기 감지", "평균 큐 추적", "임의 버림·표시", WARN),
    ("3단계", "ECN 통보", "무손실 알림", "IP 헤더 표시", "CE 비트 전환", OK),
    ("4단계", "피드백 감속", "왕복 알림", "ECE → cwnd 반감", "CWR 로 해제", ACC),
    ("별도 축", "공격 방어", "수신자 기만", "ACK 분할·위조", "ABC·상한 방어", INFO),
]

for i, (step, title, tag, metric, desc, color) in enumerate(STEPS):
    x = X0 + i * (CW + GAP)
    focal = (color == ACC)

    # 1~4단계는 혼잡 감지·통보의 인과 흐름, 5단계는 수신자 기만 공격 및 방어
    if i < 3:
        d.arrow([(x + CW + 2, Y + CH // 2), (x + CW + GAP - 4, Y + CH // 2)], MUTED, "ar", 1.4)

    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)

    d.t(x + CW // 2, Y + 26, step, 11, SOFT, MONO, "middle", 600)
    d.t(x + CW // 2, Y + 52, title, 15, ACC if focal else INK, KR, "middle", 600)

    # 태그 칩
    d.chip(x + CW // 2, Y + 84, tag, color, 11, 8)

    # 구분선
    d.line(x + 16, Y + 106, x + CW - 16, Y + 106, RULE, 0.6)

    # 핵심 지표 및 설명
    d.t(x + CW // 2, Y + 134, metric, 11, color, KR, "middle", 600)
    d.t(x + CW // 2, Y + 160, desc, 11, MUTED, KR, "middle")

# 4단계에서 1단계로의 피드백 안정화 순환 화살표
d.path(f"M {X0 + 3 * (CW + GAP) + CW // 2} {Y + CH + 4} "
       f"L {X0 + 3 * (CW + GAP) + CW // 2} {Y + CH + 22} "
       f"L {X0 + CW // 2} {Y + CH + 22} "
       f"L {X0 + CW // 2} {Y + CH + 8}",
       OK, 1.2, m="ok", dash="4 4")
d.t(X0 + 1 * (CW + GAP) + CW // 2 + 50, Y + CH + 36, "cwnd 감소로 큐 지연 완화", 11, OK, KR, "middle")

d.legend(H - 48, [
    ("버퍼블로트", BAD),
    ("AQM 개입", WARN),
    ("ECN 통보", OK),
    ("창 축소 (초점)", ACC),
    ("공격 방어", INFO),
])

d.save("16-05.chapter-overview.svg")
