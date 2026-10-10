# 타입 스펙: type-process — 혼잡 감지부터 손실 후 재시작까지 다섯 단계 처리 흐름.
# 사실 출처: ch16.txt 1~688행 — 혼잡 감지, min(cwnd, awnd), 느린 시작(IW, 2^k), 혼잡 회피(1 SMSS/RTT), ssthresh 갱신 및 복구.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 460
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-01",
      "혼잡 제어의 다섯 단계 — 감지·한도·증가·회피·복구",
      "망 상태를 패킷 손실로 짐작하고 수신자 광고 창과 혼잡 창 중 작은 값으로 송신량을 제한한다. 느린 시작으로 창을 지수적으로 키운 뒤 임계값부터 혼잡 회피로 선형 증가시키며 손실 시 창을 절반으로 줄여 재시작한다.",
      "송신 창 = min(cwnd, awnd) 제어 아래 세 국면이 순환합니다")

CW, CH, GAP = 158, 206, 18
X0 = 24
Y = 136

STEPS = [
    ("1단계", "혼잡 감지", "망의 묵묵부답", "RTO 만료", "중복 ACK 3개", WARN),
    ("2단계", "송신 한도", "두 제동 장치", "W = min(cwnd, awnd)", "FlightSize ≤ W", INFO),
    ("3단계", "느린 시작", "지수적 탐색", "ACK 마다 SMSS 증가", "왕복마다 2배 증가", OK),
    ("4단계", "혼잡 회피", "선형적 증가", "왕복당 1 SMSS", "cwnd += SMSS²/cwnd", ACC),
    ("5단계", "손실 복구", "승수적 감소", "ssthresh = 비행/2", "Tahoe 1 · Reno 반감", BAD),
]

for i, (step, title, tag, metric, desc, color) in enumerate(STEPS):
    x = X0 + i * (CW + GAP)
    focal = (color == ACC)

    if i < len(STEPS) - 1:
        d.arrow([(x + CW + 2, Y + CH // 2), (x + CW + GAP - 4, Y + CH // 2)], MUTED, "ar", 1.4)

    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)

    d.t(x + CW // 2, Y + 26, step, 11, SOFT, MONO, "middle", 600)
    d.t(x + CW // 2, Y + 50, title, 15, ACC if focal else INK, KR, "middle", 600)

    # 태그 칩 (한글 하한 11px 준수)
    d.chip(x + CW // 2, Y + 80, tag, color, 11, 8)

    # 구분선
    d.line(x + 16, Y + 102, x + CW - 16, Y + 102, RULE, 0.6)

    # 수식/핵심 값
    d.t(x + CW // 2, Y + 130, metric, 11, color, MONO if "=" in metric or "≤" in metric or "²" in metric else KR, "middle", 600)
    d.t(x + CW // 2, Y + 158, desc, 11, MUTED, KR, "middle")

# 5단계 복귀 순환 화살표 (Reno -> 4단계, RTO·Tahoe -> 3단계)
x3 = X0 + 2 * (CW + GAP) + CW // 2
x4 = X0 + 3 * (CW + GAP) + CW // 2
x5 = X0 + 4 * (CW + GAP) + CW // 2

# 1) Reno (빠른 회복 완료 후 혼잡 회피 복귀)
d.path(f"M {x5 - 28} {Y + CH} "
       f"L {x5 - 28} {Y + CH + 26} "
       f"L {x4} {Y + CH + 26} "
       f"L {x4} {Y + CH + 2}",
       ACC, 1.2, m="acc", dash="4 4")
d.t((x4 + x5 - 28) // 2, Y + CH + 16, "Reno(3 dupACK): 혼잡 회피 복귀", 11, ACC, KR, "middle", 600)

# 2) RTO 만료 및 Tahoe (느린 시작 재개)
d.path(f"M {x5 + 28} {Y + CH} "
       f"L {x5 + 28} {Y + CH + 46} "
       f"L {x3} {Y + CH + 46} "
       f"L {x3} {Y + CH + 2}",
       BAD, 1.2, m="bad", dash="4 4")
d.t((x3 + x4) // 2, Y + CH + 36, "RTO·Tahoe: 느린 시작 재개", 11, BAD, KR, "middle", 600)

d.legend(H - 48, [
    ("정상 진행", OK),
    ("혼잡 회피", ACC),
    ("손실 복구", BAD),
    ("한도 제약", INFO),
    ("혼잡 의심", WARN),
])

d.save("16-01.chapter-overview.svg")
