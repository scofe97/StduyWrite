# 08-03 §2 — 인터랙티브 트랜잭션 네트워크 대기와 저장 프로시저 단일 스레드 직렬 실행 비교
# 검증(10-31 cc-ddia-dverify08): 저장 프로시저 이름을 Fig 8-9(p37) take_doctor_off_call_if_safe 로, 색 인자 MONO 오류를 INK 로, 본문에 없는 "급락"·"제로" 표현을 본문 말로 고침
# 사실 출처: 08-03 §2(L50~L67), 원서 Ch.8 p.37 Figure 8-9
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY1 = 104
PH1 = 156
PY2 = 276
PH2 = 168
LEG = PY2 + PH2 + 28
H = LEG + 52

d = D(W, H, "08-03 · §2 SERIAL EXECUTION", "인터랙티브 트랜잭션과 저장 프로시저 직렬 실행 비교",
      "네트워크 왕복 대기 지연을 없애고 메모리 내 단일 스레드로 빠르게 완결하는 실행 방식",
      "다단계 네트워크 왕복 · 유휴 대기 · 저장 프로시저 한 번에 제출 · 메모리에서 완결")

# ── 패널 1: 인터랙티브 트랜잭션 (상단) ──────────────────────────
d.box(24, PY1, W - 48, PH1, PAPER2, RULE, 1.0)
d.chip(110, PY1 + 22, "인터랙티브 트랜잭션", WARN, 11)
d.t(W - 40, PY1 + 22, "다단계 왕복 지연 · 단일 스레드 직렬 처리 불가", 11, SOFT, KR, "end")

# 애플리케이션 상자
d.box(40, PY1 + 44, 180, 94, PAPER, RULE, 0.8)
d.t(130, PY1 + 68, "애플리케이션", 12, INK, KR, "middle", 600)
d.t(130, PY1 + 90, "1. SELECT 요청", 11, INFO, KR, "middle")
d.t(130, PY1 + 108, "2. 조건 검사(2>=2)", 11, SOFT, KR, "middle")
d.t(130, PY1 + 126, "3. UPDATE 요청", 11, WARN, KR, "middle")

# 네트워크 왕복 구간
d.tone(250, PY1 + 44, 270, 94, WARN, 6, "12", 1.0)
d.t(385, PY1 + 68, "네트워크 왕복(RTT) 반복", 12, WARN, KR, "middle", 600)
d.t(385, PY1 + 92, "질의 전송 ↔ 결과 수신 대기", 11, MUTED, KR, "middle")
d.t(385, PY1 + 112, "수신 중 DB 스레드 유휴 대기 발생", 11, WARN, KR, "middle")

# 화살표: App -> Net -> DB
d.arrow([(220, PY1 + 91), (250, PY1 + 91)], INFO, "info", 1.2)
d.arrow([(520, PY1 + 91), (550, PY1 + 91)], INFO, "info", 1.2)

# 데이터베이스 상자
d.box(550, PY1 + 44, 290, 94, PAPER, RULE, 0.8)
d.t(695, PY1 + 68, "데이터베이스 서버", 12, INK, KR, "middle", 600)
d.t(695, PY1 + 90, "단일 스레드 순차 처리 시 병목", 11, WARN, KR, "middle")
d.t(695, PY1 + 112, "느린 트랜잭션 하나가 전체를 막음", 11, MUTED, KR, "middle")

# ── 패널 2: 저장 프로시저 직렬 실행 (하단, FOCAL) ────────────────
d.box(24, PY2, W - 48, PH2, PAPER2, ACC, 1.4)
d.chip(110, PY2 + 22, "저장 프로시저 직렬 실행", ACC, 11)
d.t(W - 40, PY2 + 22, "한 번에 제출 · 메모리 데이터로 빠르게 실행 (VoltDB · Redis · Datomic)", 11, SOFT, KR, "end")

# 애플리케이션 상자
d.box(40, PY2 + 44, 200, 104, PAPER, RULE, 0.8)
d.t(140, PY2 + 68, "애플리케이션", 12, INK, KR, "middle", 600)
d.t(140, PY2 + 92, "전체 로직 한 번에 제출", 11, INFO, KR, "middle")
d.t(140, PY2 + 114, "take_doctor_off_call_if_safe", 10, INK, MONO, "middle")
d.t(140, PY2 + 132, "네트워크 1회 왕복", 11, MUTED, KR, "middle")

# 화살표: App -> DB
d.arrow([(240, PY2 + 96), (280, PY2 + 96)], ACC, "acc", 1.4)

# 저장 프로시저 인메모리 실행 엔진 (FOCAL)
d.tone(280, PY2 + 44, 560, 104, OK, 6, "14", 1.2)
d.t(560, PY2 + 68, "단일 스레드 인메모리(RAM) 연속 실행", 12, OK, KR, "middle", 600)

# 내부 3단계 슬롯
sub_w = 166
sub_gap = 12
sx0 = 296
d.box(sx0, PY2 + 82, sub_w, 56, PAPER, RULE, 0.8)
d.t(sx0 + sub_w / 2, PY2 + 102, "1. 당직 조회", 11, INFO, KR, "middle", 600)
d.t(sx0 + sub_w / 2, PY2 + 122, "현재 2명 확인 (RAM)", 11, MUTED, KR, "middle")

d.box(sx0 + sub_w + sub_gap, PY2 + 82, sub_w, 56, PAPER, RULE, 0.8)
d.t(sx0 + sub_w + sub_gap + sub_w / 2, PY2 + 102, "2. 조건 판정 및 갱신", 11, WARN, KR, "middle", 600)
d.t(sx0 + sub_w + sub_gap + sub_w / 2, PY2 + 122, "2명 이상 판정 → 취소 반영", 11, MUTED, KR, "middle")

d.tone(sx0 + 2 * (sub_w + sub_gap), PY2 + 82, sub_w, 56, ACC, 4, "20", 1.2)
d.t(sx0 + 2 * (sub_w + sub_gap) + sub_w / 2, PY2 + 102, "3. 즉시 커밋 완료", 11, ACC, KR, "middle", 600)
d.t(sx0 + 2 * (sub_w + sub_gap) + sub_w / 2, PY2 + 122, "I/O 대기 없음", 11, INK, KR, "middle")

d.legend(LEG, [("질의·호출 요청", INFO), ("네트워크 I/O 유휴 지연", WARN), ("저장 프로시저 실행", OK), ("인메모리 완결 (focal)", ACC)])
d.save("08-03.serial-execution.svg")
