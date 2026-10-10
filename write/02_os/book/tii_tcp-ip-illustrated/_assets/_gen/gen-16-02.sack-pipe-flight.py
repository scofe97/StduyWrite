# 타입 스펙: type-data-flow — SACK 점수판에서 pipe 추정치 산출 및 송신 허용량 계산 흐름.
# 사실 출처: RFC 6675 §2~3 · ch16.txt 762~809행
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 440
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-02 §2", "SACK 점수판과 pipe 변수의 송신 제어 흐름",
      "SACK 블록으로 점수판을 갱신해 비행 중인 바이트를 pipe 변수로 추정한다. 점수판은 무엇을 보낼지(손실 구멍) 정하고, cwnd 와 pipe 의 여유분은 얼마나 보낼지 결정한다.",
      "SACK 은 전송 대상을 고르고 pipe 와 cwnd 는 네트워크 주입량을 제어합니다")

# 4개 단계 박스
# 1. 입력 피드백
BX1, BY1, BW1, BH1 = 24, 126, 184, 230
d.box(BX1, BY1, BW1, BH1, PAPER2, RULE, 1.0, 8)
d.tone(BX1, BY1, BW1, 36, INFO, 6, "22", 1.0)
d.t(BX1 + BW1/2, BY1 + 22, "1. 수신 피드백", 13, INFO, KR, "middle", 600)
d.chip(BX1 + BW1/2, BY1 + 68, "누적 ACK 번호", MUTED, 11)
d.chip(BX1 + BW1/2, BY1 + 104, "SACK 옵션 블록", MUTED, 11)
d.t(BX1 + BW1/2, BY1 + 148, "도착한 범위 알림", 12, INK, KR, "middle", 500)
d.t(BX1 + BW1/2, BY1 + 172, "구멍과 수신 분리", 11, MUTED, KR, "middle")
d.t(BX1 + BW1/2, BY1 + 204, "RFC 2018 규격", 11, SOFT, MONO, "middle")

# 2. SACK 점수판
BX2, BY2, BW2, BH2 = 238, 126, 214, 230
d.box(BX2, BY2, BW2, BH2, PAPER2, RULE, 1.0, 8)
d.tone(BX2, BY2, BW2, 36, WARN, 6, "22", 1.0)
d.t(BX2 + BW2/2, BY2 + 22, "2. SACK 점수판", 13, WARN, KR, "middle", 600)
d.t(BX2 + BW2/2, BY2 + 62, "상태 분류 (Scoreboard)", 11, MUTED, KR, "middle")
d.box(BX2 + 12, BY2 + 78, BW2 - 24, 30, PAPER, RULE, 0.8, 4)
d.t(BX2 + BW2/2, BY2 + 98, "SACKed: 수신 확인 바이트", 11, OK, KR, "middle", 600)
d.box(BX2 + 12, BY2 + 116, BW2 - 24, 30, PAPER, RULE, 0.8, 4)
d.t(BX2 + BW2/2, BY2 + 136, "Lost: DupThresh SACK 손실", 11, WARN, KR, "middle", 600)
d.box(BX2 + 12, BY2 + 154, BW2 - 24, 30, PAPER, RULE, 0.8, 4)
d.t(BX2 + BW2/2, BY2 + 174, "In Flight: 비행 중 추정 바이트", 11, INFO, KR, "middle", 600)
d.t(BX2 + BW2/2, BY2 + 208, "재전송 대상 선정", 12, INK, KR, "middle", 500)

# 3. pipe 추정치 계산
BX3, BY3, BW3, BH3 = 482, 126, 204, 230
d.box(BX3, BY3, BW3, BH3, PAPER2, RULE, 1.0, 8)
d.tone(BX3, BY3, BW3, 36, ACC, 6, "22", 1.0)
d.t(BX3 + BW3/2, BY3 + 22, "3. pipe 변수 계산", 13, ACC, KR, "middle", 600)
d.t(BX3 + BW3/2, BY3 + 64, "망 내 비행 데이터 추정", 11, MUTED, KR, "middle")
d.box(BX3 + 12, BY3 + 82, BW3 - 24, 52, PAPER, RULE, 0.8, 4)
d.t(BX3 + BW3/2, BY3 + 102, "pipe =", 12, SOFT, MONO, "middle")
d.t(BX3 + BW3/2, BY3 + 120, "Flight−SACKed−Lost+Rxt", 10, ACC, MONO, "middle", 600)
d.t(BX3 + BW3/2, BY3 + 158, "손실 제외 및 재전송 가산", 12, INK, KR, "middle", 500)
d.t(BX3 + BW3/2, BY3 + 180, "실제 망 부하만 계량", 11, MUTED, KR, "middle")
d.t(BX3 + BW3/2, BY3 + 208, "RFC 6675 알고리즘", 11, SOFT, MONO, "middle")

# 4. 송신 조건 판정
BX4, BY4, BW4, BH4 = 716, 126, 180, 230
d.box(BX4, BY4, BW4, BH4, PAPER2, RULE, 1.0, 8)
d.tone(BX4, BY4, BW4, 36, OK, 6, "22", 1.0)
d.t(BX4 + BW4/2, BY4 + 22, "4. 송신 결정", 13, OK, KR, "middle", 600)
d.t(BX4 + BW4/2, BY4 + 64, "송신 허용 여부 판정", 11, MUTED, KR, "middle")
d.chip(BX4 + BW4/2, BY4 + 96, "cwnd − pipe ≥ SMSS", OK, 11)
d.t(BX4 + BW4/2, BY4 + 140, "여유분만큼 전송", 12, OK, KR, "middle", 600)
d.t(BX4 + BW4/2, BY4 + 164, "1. 손실 구멍 우선 채움", 11, INK, KR, "middle")
d.t(BX4 + BW4/2, BY4 + 186, "2. 없으면 새 데이터 송신", 11, MUTED, KR, "middle")
d.t(BX4 + BW4/2, BY4 + 208, "파이프 버스트 억제", 11, SOFT, KR, "middle")

# 연결 화살표 (1 -> 2 -> 3 -> 4)
d.arrow([(BX1 + BW1 + 2, BY1 + 115), (BX2 - 4, BY2 + 115)], MUTED, "ar", 1.4)
d.arrow([(BX2 + BW2 + 2, BY2 + 115), (BX3 - 4, BY3 + 115)], MUTED, "ar", 1.4)
d.arrow([(BX3 + BW3 + 2, BY3 + 115), (BX4 - 4, BY4 + 115)], OK, "ok", 1.4)

d.save("16-02.sack-pipe-flight.svg")
