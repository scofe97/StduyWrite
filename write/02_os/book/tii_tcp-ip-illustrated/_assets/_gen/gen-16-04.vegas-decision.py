# 타입 스펙: type-flowchart — RTT 측정값에 따른 TCP Vegas 의 창 증감 판정 순서도.
# 사실 출처: ch16.txt 2550~2660행 — Expected = cwnd/baseRTT, Actual = cwnd/RTT, Diff 계산 후 α=1, β=3 기준 분기.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 560
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-04 §5",
      "TCP Vegas 의 큐 지연 기반 혼잡 판정 순서도 (수치 흐름 예시)",
      "매 왕복 시간마다 기대 처리량과 실측 처리량의 차이(Diff)로 병목 큐의 패킷 점유량을 추정한다. baseRTT=100ms, RTT=125ms, cwnd=20 예시에서 Diff=4는 β=3을 초과하므로 창을 19로 줄여 버퍼를 비운다.",
      "손실이 나기 전에 버퍼 대기열을 감지해 선제적으로 속도를 조절합니다")

CX = W // 2  # 460

# 1. 시작 노드: RTT 측정
N1_Y, N1_W, N1_H = 106, 440, 54
d.box(CX - N1_W // 2, N1_Y, N1_W, N1_H, PAPER2, RULE, 1.0, 24)
d.t(CX, N1_Y + 20, "왕복 시간(RTT) 및 혼잡 창 관측", 13, INK, KR, "middle", 600)
d.t(CX, N1_Y + 38, "관측 예시: baseRTT = 100ms, RTT = 125ms, cwnd = 20", 11, INFO, MONO, "middle")

# 화살표 1 -> 2
d.arrow([(CX, N1_Y + N1_H), (CX, N1_Y + N1_H + 18)], MUTED, "ar", 1.4)

# 2. 계산 노드: Diff 추정
N2_Y, N2_W, N2_H = N1_Y + N1_H + 18, 480, 60
d.box(CX - N2_W // 2, N2_Y, N2_W, N2_H, PAPER2, RULE, 1.0, 6)
d.t(CX, N2_Y + 22, "버퍼 대기열 추정 (Diff 계산)", 13, INK, KR, "middle", 600)
d.t(CX, N2_Y + 44, "Diff = 20 × (1 - 100 / 125) = 4 패킷 적체", 12, INFO, MONO, "middle", 600)

# 화살표 2 -> 3
d.arrow([(CX, N2_Y + N2_H), (CX, N2_Y + N2_H + 18)], MUTED, "ar", 1.4)

# 3. 판단 마름모: Diff 크기 판정
DY, DW, DH = N2_Y + N2_H + 18, 300, 64
d.o.append(f'<polygon points="{CX},{DY} {CX + DW // 2},{DY + DH // 2} {CX},{DY + DH} {CX - DW // 2},{DY + DH // 2}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(CX, DY + DH // 2 - 4, "대기열 크기 판정 (예: Diff = 4)", 12, INK, KR, "middle", 600)
d.t(CX, DY + DH // 2 + 16, "기준 임계값 α = 1, β = 3", 11, MUTED, KR, "middle")

# 4. 세 갈래 분기 상자
BY = DY + DH + 36
BW, BH = 260, 76
LX = 24
MX = CX - BW // 2
RX = W - 24 - BW

# 분기 1: Diff < α (버퍼 부족 -> 증가)
d.tone(LX, BY, BW, BH, OK, 6, "12", 1.2)
d.t(LX + BW // 2, BY + 20, "cwnd ← cwnd + 1 (20 → 21)", 12, OK, MONO, "middle", 600)
d.t(LX + BW // 2, BY + 38, "Diff < 1 (예: RTT=104ms, Diff=0.8)", 11, OK, MONO, "middle")
d.t(LX + BW // 2, BY + 56, "링크 유휴 방지 (선형 가산)", 11, MUTED, KR, "middle")

# 분기 2: α ≤ Diff ≤ β (적정 버퍼 -> 유지)
d.tone(MX, BY, BW, BH, INFO, 6, "12", 1.2)
d.t(MX + BW // 2, BY + 20, "cwnd 유지 (20 패킷 유지)", 12, INFO, MONO, "middle", 600)
d.t(MX + BW // 2, BY + 38, "1 ≤ Diff ≤ 3 (예: RTT=110ms, Diff=1.8)", 11, INFO, MONO, "middle")
d.t(MX + BW // 2, BY + 56, "적정 대기열 안정 운용", 11, MUTED, KR, "middle")

# 분기 3: Diff > β (버퍼 과적 -> 감소, 예시 경로)
d.tone(RX, BY, BW, BH, WARN, 6, "16", 1.5)
d.t(RX + BW // 2, BY + 20, "cwnd ← cwnd - 1 (20 → 19)", 12, WARN, MONO, "middle", 600)
d.t(RX + BW // 2, BY + 38, "Diff > 3 (예시 경로: Diff = 4)", 11, WARN, MONO, "middle", 600)
d.t(RX + BW // 2, BY + 56, "큐 지연 해소 (선형 감산)", 11, WARN, KR, "middle")

# 화살표 연결 (마름모 -> 세 상자)
mid_y = DY + DH // 2

# 왼쪽 화살표
d.path(f"M {CX - DW // 2} {mid_y} L {LX + BW // 2} {mid_y} L {LX + BW // 2} {BY - 6}", OK, 1.4, m="ok")
d.t(LX + BW // 2 + 54, mid_y - 8, "Diff < α", 11, OK, MONO, "middle")

# 가운데 화살표
d.arrow([(CX, DY + DH), (CX, BY - 6)], INFO, "info", 1.4)
d.t(CX + 14, BY - 12, "α ≤ Diff ≤ β", 11, INFO, MONO, "start")

# 오른쪽 화살표 (예시 경로 강조)
d.path(f"M {CX + DW // 2} {mid_y} L {RX + BW // 2} {mid_y} L {RX + BW // 2} {BY - 6}", WARN, 1.8, m="warn")
d.t(RX + BW // 2 - 54, mid_y - 8, "Diff > β (해당)", 11, WARN, MONO, "middle", 600)

# 하단 수렴 화살표 (다음 RTT)
BOT_Y = BY + BH + 20
d.line(LX + BW // 2, BY + BH, LX + BW // 2, BOT_Y, RULE, 1.0)
d.line(MX + BW // 2, BY + BH, MX + BW // 2, BOT_Y, RULE, 1.0)
d.line(RX + BW // 2, BY + BH, RX + BW // 2, BOT_Y, RULE, 1.0)
d.line(LX + BW // 2, BOT_Y, RX + BW // 2, BOT_Y, RULE, 1.0)
d.arrow([(CX, BOT_Y), (CX, BOT_Y + 16)], MUTED, "ar", 1.4)
d.t(CX, BOT_Y + 30, "다음 RTT 전송에 갱신 창 적용 (예시 경로: cwnd = 19)", 11, MUTED, KR, "middle")

d.legend(H - 44, [
    ("선형 가산 (Diff < α)", OK),
    ("창 유지 (α ≤ Diff ≤ β)", INFO),
    ("선형 감산 (Diff > β, 예시)", WARN),
])

d.save("16-04.vegas-decision.svg")
