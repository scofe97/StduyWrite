# 타입 스펙: type-process — 복구와 유휴 구간에서 창을 조절하고 복원하는 6단계 흐름.
# 사실 출처: RFC 6582 · RFC 6675 · RFC 9937 · RFC 3042 · RFC 7661 · RFC 4015
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 920, 390
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-02", "복구와 유휴 구간에서 창을 다듬는 흐름",
      "손실 감지 후 SACK으로 무엇을 보낼지 정하고, pipe로 얼마나 보낼지 제어한다. 작은 창은 제한 전송으로 돕고 유휴 연결은 감쇠하며 헛 RTO는 이전 창으로 되돌린다.",
      "복구 중 송신량 제어부터 유휴 감쇠와 헛 RTO 복원까지 이어집니다")

CW, CH = 268, 76
GAP = 28
X0 = 26
Y_ROW1 = 118
Y_ROW2 = 246

row1 = [
    ("1. 손실 감지", "중복 ACK 3개 또는 SACK", "복구 절차 진입", WARN),
    ("2. 대상 선정", "SACK 점수판 구멍 탐색", "선택적 재전송", INFO),
    ("3. 송신량 제어", "pipe 추정치 계산", "cwnd − pipe 송신", ACC)
]

row2 = [
    ("4. 작은 창 보조", "제한 전송 메커니즘", "dupACK 1·2에 새 데이터", INFO),
    ("5. 유휴 창 감쇠", "CWV 비사용 기간 검증", "RTO마다 cwnd 반감", WARN),
    ("6. 헛 RTO 복원", "Eifel 응답 알고리즘", "축소된 ssthresh 복원", OK)
]

# Row 1 카드 렌더링
for i, (title, sub, out, color) in enumerate(row1):
    x = X0 + i * (CW + GAP)
    d.tone(x, Y_ROW1, CW, CH, color, 6, "14", 1.2)
    d.t(x + CW/2, Y_ROW1 + 24, title, 14, color, KR, "middle", 600)
    d.t(x + CW/2, Y_ROW1 + 45, sub, 12, MUTED)
    d.t(x + CW/2, Y_ROW1 + 64, out, 12, INK, KR, "middle", 500)
    if i < 2:
        x_next = X0 + (i + 1) * (CW + GAP)
        d.arrow([(x + CW + 4, Y_ROW1 + CH/2), (x_next - 6, Y_ROW1 + CH/2)], MUTED, "ar", 1.5)

# Row 1 -> Row 2 연결 화살표 (오른쪽 아래로 꺾임)
x_r1_end = X0 + 2 * (CW + GAP) + CW/2
d.arrow([(x_r1_end, Y_ROW1 + CH + 4), (x_r1_end, Y_ROW2 - 8)], ACC, "acc", 1.5)

# Row 2 카드 렌더링 (오른쪽에서 왼쪽으로 진행: 4 -> 5 -> 6)
for i, (title, sub, out, color) in enumerate(row2):
    x = X0 + (2 - i) * (CW + GAP)
    d.tone(x, Y_ROW2, CW, CH, color, 6, "14", 1.2)
    d.t(x + CW/2, Y_ROW2 + 24, title, 14, color, KR, "middle", 600)
    d.t(x + CW/2, Y_ROW2 + 45, sub, 12, MUTED)
    d.t(x + CW/2, Y_ROW2 + 64, out, 12, INK, KR, "middle", 500)
    if i < 2:
        x_prev = X0 + (1 - i) * (CW + GAP)
        d.arrow([(x - 4, Y_ROW2 + CH/2), (x_prev + CW + 6, Y_ROW2 + CH/2)], MUTED, "ar", 1.5)

d.save("16-02.chapter-overview.svg")
