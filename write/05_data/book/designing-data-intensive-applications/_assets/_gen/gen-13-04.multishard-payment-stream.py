# 13-04 §3 — 이벤트 로그와 스트림 처리기로 하는 멀티샤드 계좌 이체 (원서 Figure 13-2).
# 사실 출처: 13-04 본문 §3(L44~L55), DDIA 2판 Ch.13 p.37~39 Figure 13-2 및 단계 1~4 설명.
# 타입 스펙: type-data-flow
# 2026-10-31 검증: 배너 중립색, 원서 p38~39 낱말(수수료 입금 이벤트·자기 입력 로그·샤드), 원문자·4대·완전 재현 제거
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 920
BANNER_Y = 104
BANNER_H = 36
PANEL_Y = 504
LEG = PANEL_Y + 76
H = LEG + 48

d = D(W, H, "13-04 · §3 MULTISHARD STREAM PROCESSING", "이벤트 로그와 스트림 처리기로 하는 계좌 이체 (Figure 13-2)",
      "원천 계좌 로그에 최초 요청을 단일 원자적 메시지로 기록하고, 스트림 처리기가 로컬 상태 확인 후 대상·수수료 계좌로 이벤트를 발행하는 무결성 아키텍처를 보인다.",
      "Figure 13-2 · 최초 요청 기록의 원자성 · 로컬 상태 잔액 예약 · 출금 이벤트는 자기 입력 로그로 · 요청 ID 중복 제거")

# 상단 공통 전제 배너
d.box(28, BANNER_Y, W - 56, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 23, "원자성 = 원천 계좌 로그에 최초 요청 이벤트 기록 (트랜잭션 아님)", 12, INK, KR, "middle", 600)

# 1. 좌측 상단: 사용자 (User)
d.box(40, 156, 130, 42, PAPER2, OK, 1.2)
d.t(105, 175, "사용자 (User)", 12, INK, KR, "middle", 600)
d.t(105, 190, "요청 ID 생성", 11, MUTED, KR, "middle")

# 사용자 -> 원천 계좌 로그 화살표 (x=70)
d.arrow([(70, 198), (70, 256)], MUTED, "ar", 1.4)
d.t(64, 228, "이체 요청", 11, MUTED, KR, "end")

# 2. 원천 계좌 로그 샤드 (Source account log)
d.box(30, 256, 170, 48, PAPER2, OK, 1.2)
d.t(115, 276, "원천 계좌 로그 샤드", 12, OK, KR, "middle", 600)
d.t(115, 294, "Source account log", 11, MUTED, MONO, "middle")

# 원천 계좌 로그 -> 원천 계좌 스트림 처리기 화살표
d.arrow([(200, 280), (252, 280)], OK, "ok", 1.4)

# 3. 원천 계좌 스트림 처리기 (Source account event processor)
d.box(252, 246, 216, 68, PAPER2, OK, 1.4)
d.chip(360, 260, "원천 계좌 처리기", OK, 11)
d.t(360, 282, "Source Event Processor", 11.5, INK, KR, "middle", 600)
d.t(360, 300, "잔액 검사 및 출금 예약", 11, MUTED, KR, "middle")

# 원천 계좌 상태 DB (로컬)
d.box(280, 354, 160, 46, PAPER, OK, 1.0)
d.t(360, 373, "원천 계좌 상태 DB", 11.5, INK, KR, "middle", 600)
d.t(360, 389, "로컬 잔액 · 처리된 ID", 11, MUTED, KR, "middle")
d.line(360, 314, 360, 354, RULE, 1.0, "3 3")

# 출금 루프백 화살표 (Outgoing payment emitted back to input log)
d.arrow([(360, 246), (360, 216), (150, 216), (150, 256)], ACC, "acc", 1.4)
d.t(255, 208, "출금 이벤트 (Outgoing payment)", 11, ACC, KR, "middle")

# 4. 우측 상단: 대상 계좌 파티션 (Destination account)
# 원천 처리기 -> 대상 계좌 로그 화살표
d.arrow([(468, 268), (506, 268), (506, 202), (544, 202)], INFO, "info", 1.4)
d.t(512, 244, "입금 이벤트", 11, INFO, KR, "start")

# 대상 계좌 로그 샤드
d.box(544, 178, 170, 48, PAPER2, INFO, 1.2)
d.t(629, 198, "대상 계좌 로그 샤드", 12, INFO, KR, "middle", 600)
d.t(629, 216, "Destination account log", 11, MUTED, MONO, "middle")

# 대상 로그 -> 대상 처리기 화살표
d.arrow([(714, 202), (738, 202)], INFO, "info", 1.4)

# 대상 계좌 스트림 처리기
d.box(738, 168, 154, 68, PAPER2, INFO, 1.2)
d.chip(815, 182, "대상 계좌 처리기", INFO, 11)
d.t(815, 204, "이벤트 스트림 처리", 11.5, INK, KR, "middle", 600)
d.t(815, 222, "요청 ID로 중복 제거", 11, MUTED, KR, "middle")

# 대상 계좌 상태 DB
d.box(751, 272, 128, 44, PAPER, INFO, 1.0)
d.t(815, 290, "대상 계좌 상태 DB", 11.5, INK, KR, "middle", 600)
d.t(815, 305, "입금액 상태 반영", 11, MUTED, KR, "middle")
d.line(815, 236, 815, 272, RULE, 1.0, "3 3")

# 5. 우측 하단: 수수료 계좌 파티션 (Fees account)
# 원천 처리기 -> 수수료 계좌 로그 화살표
d.arrow([(468, 288), (506, 288), (506, 372), (544, 372)], WARN, "warn", 1.4)
d.t(512, 334, "수수료 입금 이벤트", 11, WARN, KR, "start")

# 수수료 계좌 로그 샤드
d.box(544, 348, 170, 48, PAPER2, WARN, 1.2)
d.t(629, 368, "수수료 계좌 로그 샤드", 12, WARN, KR, "middle", 600)
d.t(629, 386, "Fees account log", 11, MUTED, MONO, "middle")

# 수수료 로그 -> 수수료 처리기 화살표
d.arrow([(714, 372), (738, 372)], WARN, "warn", 1.4)

# 수수료 계좌 스트림 처리기
d.box(738, 338, 154, 68, PAPER2, WARN, 1.2)
d.chip(815, 352, "수수료 처리기", WARN, 11)
d.t(815, 374, "이벤트 스트림 처리", 11.5, INK, KR, "middle", 600)
d.t(815, 392, "요청 ID로 중복 제거", 11, MUTED, KR, "middle")

# 수수료 계좌 상태 DB
d.box(751, 442, 128, 44, PAPER, WARN, 1.0)
d.t(815, 460, "수수료 계좌 상태 DB", 11.5, INK, KR, "middle", 600)
d.t(815, 475, "입금액 상태 반영", 11, MUTED, KR, "middle")
d.line(815, 406, 815, 442, RULE, 1.0, "3 3")

# 하단 4대 메커니즘 정리 패널
d.box(28, PANEL_Y, W - 56, 52, PAPER2, RULE, 1.0)
d.t(W / 2, PANEL_Y + 20, "분산 트랜잭션 없이 무결성을 얻는 네 메커니즘 (본문 §3)", 11.5, INK, KR, "middle", 600)
d.t(W / 2, PANEL_Y + 38, "단일 메시지 기록 · 결정론적 파생 함수 · 요청 ID 중복 제거 · 불변 메시지 재처리", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("원천 계좌 샤드", OK),
    ("대상 계좌 샤드", INFO),
    ("수수료 계좌 샤드", WARN),
    ("출금 이벤트 → 자기 입력 로그", ACC)
])

d.save("13-04.multishard-payment-stream.svg")
