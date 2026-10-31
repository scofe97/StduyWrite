# 10-02 §1 — 네트워크 파티션 발생 시 선형성과 가용성의 충돌 및 두 리전의 CP·AP 선택.
# 사실 출처: 10-02 §1(L24~L37), DDIA 2판 Ch.10 Figure 10-7 "A network interruption forcing a choice between linearizability and availability" (PDF p.17)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
Y_BOX = 104
H_BOX = 208
Y_BOT = 336
H_BOT = 114
LEG = Y_BOT + H_BOT + 28
H = LEG + 48

d = D(W, H, "10-02 · §1 PARTITION CONFLICT", "네트워크 파티션 시 선형성과 가용성의 충돌",
      "두 리전 사이 링크 단절 시 팔로워 리전의 요청 거부(CP)와 독립 처리(AP) 선택 구조.",
      "단일 리더 구성 · 복제 링크 단절 · 최신성 검증 불가 · CP 요청 거부 · AP 분기 처리")

# 1. 좌측: 리전 A (단일 리더)
X_A = 24
W_A = 356
d.box(X_A, Y_BOX, W_A, H_BOX, PAPER2, RULE, 0.9)
d.t(X_A + 16, Y_BOX + 24, "리전 A (Region A) — 리더 데이터센터", 12.5, INK, KR, "start", 600)

# 리전 A 클라이언트
d.box(X_A + 16, Y_BOX + 42, 120, 52, PAPER, RULE, 0.8)
d.t(X_A + 76, Y_BOX + 64, "클라이언트 A", 12, INK, KR, "middle", 600)
d.t(X_A + 76, Y_BOX + 82, "로컬 읽기·쓰기 요청", 11, MUTED, KR, "middle")

# 리전 A 리더 DB
d.tone(X_A + 196, Y_BOX + 42, 144, 52, OK, 6, "18", 1.2)
d.t(X_A + 268, Y_BOX + 64, "리더 DB", 13, OK, KR, "middle", 600)
d.t(X_A + 268, Y_BOX + 82, "읽기·쓰기 정상 처리", 11, INK, KR, "middle")

# 클라이언트 A -> 리더 DB 화살표
d.arrow([(X_A + 136, Y_BOX + 68), (X_A + 192, Y_BOX + 68)], OK, "ok", 1.4)

# 리전 A 상태 요약
d.tone(X_A + 16, Y_BOX + 114, W_A - 32, 74, OK, 4, "10", 0.8)
d.t(X_A + 28, Y_BOX + 138, "리더 정상 처리", 11.5, OK, KR, "start", 600)
d.t(X_A + 28, Y_BOX + 158, "• 클라이언트 요청 정상 서빙 유지", 11, INK, KR, "start")
d.t(X_A + 28, Y_BOX + 176, "• 리전 B 로 복제 중단", 11, MUTED, KR, "start")


# 2. 우측: 리전 B (팔로워 복제본)
X_B = 500
W_B = 356
d.box(X_B, Y_BOX, W_B, H_BOX, PAPER2, RULE, 0.9)
d.t(X_B + 16, Y_BOX + 24, "리전 B (Region B) — 팔로워 데이터센터", 12.5, INK, KR, "start", 600)

# 리전 B 팔로워 DB
d.tone(X_B + 20, Y_BOX + 42, 144, 52, WARN, 6, "18", 1.2)
d.t(X_B + 92, Y_BOX + 64, "팔로워 DB", 13, WARN, KR, "middle", 600)
d.t(X_B + 92, Y_BOX + 82, "리더 연결 단절 고립", 11, INK, KR, "middle")

# 리전 B 클라이언트
d.box(X_B + 220, Y_BOX + 42, 120, 52, PAPER, RULE, 0.8)
d.t(X_B + 280, Y_BOX + 64, "클라이언트 B", 12, INK, KR, "middle", 600)
d.t(X_B + 280, Y_BOX + 82, "로컬 읽기·쓰기 시도", 11, MUTED, KR, "middle")

# 클라이언트 B -> 팔로워 DB 화살표
d.arrow([(X_B + 220, Y_BOX + 68), (X_B + 168, Y_BOX + 68)], WARN, "warn", 1.4)

# 리전 B 문제 요약
d.tone(X_B + 16, Y_BOX + 114, W_B - 32, 74, WARN, 4, "10", 0.8)
d.t(X_B + 28, Y_BOX + 138, "팔로워 고립 상태", 11.5, WARN, KR, "start", 600)
d.t(X_B + 28, Y_BOX + 158, "• 최신 데이터 검증 불가 (스테일 읽기)", 11, INK, KR, "start")
d.t(X_B + 28, Y_BOX + 176, "• 선형성 쓰기 불가능 (리더 도달 불가)", 11, MUTED, KR, "start")


# 3. 중앙: 네트워크 파티션 단절 링크
X_MID = 440
d.tone(388, Y_BOX + 42, 104, 52, BAD, 4, "18", 1.2)
d.t(X_MID, Y_BOX + 64, "네트워크 파티션", 12, BAD, KR, "middle", 600)
d.t(X_MID, Y_BOX + 82, "복제 링크 단절", 11, MUTED, KR, "middle")

# 단절 표시선
d.line(X_A + W_A - 16, Y_BOX + 68, 384, Y_BOX + 68, BAD, 1.4, dash="4 3")
d.line(496, Y_BOX + 68, X_B + 16, Y_BOX + 68, BAD, 1.4, dash="4 3")
d.line(502, Y_BOX + 56, 510, Y_BOX + 80, BAD, 2.0)
d.line(370, Y_BOX + 56, 378, Y_BOX + 80, BAD, 2.0)


# 4. 하단: 파티션 시 두 가지 선택 비교 (CP vs AP)
CW_BOT = 404

# CP 선택
d.box(24, Y_BOT, CW_BOT, H_BOT, PAPER2, INFO, 1.1)
d.chip(24 + 50, Y_BOT + 22, "CP 선택", INFO, 11)
d.t(24 + 92, Y_BOT + 24, "선형성 보장 우선 · 가용성 희생", 12.5, INK, KR, "start", 600)
d.line(34, Y_BOT + 38, 24 + CW_BOT - 10, Y_BOT + 38, RULE, 0.8)

d.t(36, Y_BOT + 56, "• 동작: 리전 B는 최신성 미보장으로 요청 거부 및 대기", 11.5, INK, KR, "start")
d.t(36, Y_BOT + 74, "• 비용: 리전 B 서비스 중단 상태 발생 (가용성 상실)", 11.5, MUTED, KR, "start")
d.tone(34, Y_BOT + 84, CW_BOT - 20, 22, INFO, 3, "12", 0.8)
d.t(24 + CW_BOT / 2, Y_BOT + 99, "선형성 유지 목적의 로컬 가용성 차단", 11, INFO, KR, "middle", 600)

# AP 선택
d.box(452, Y_BOT, CW_BOT, H_BOT, PAPER2, ACC, 1.1)
d.chip(452 + 50, Y_BOT + 22, "AP 선택", ACC, 11)
d.t(452 + 92, Y_BOT + 24, "가용성 유지 우선 · 선형성 희생", 12.5, INK, KR, "start", 600)
d.line(462, Y_BOT + 38, 452 + CW_BOT - 10, Y_BOT + 38, RULE, 0.8)

d.t(464, Y_BOT + 56, "• 동작: 각 리전이 독립적으로 읽기·쓰기 처리 허용", 11.5, INK, KR, "start")
d.t(464, Y_BOT + 74, "• 비용: 파티션 동안 양 리전 데이터 분기 발생 (선형성 상실)", 11.5, MUTED, KR, "start")
d.tone(462, Y_BOT + 84, CW_BOT - 20, 22, ACC, 3, "12", 0.8)
d.t(452 + CW_BOT / 2, Y_BOT + 99, "가용성 유지 목적의 데이터 불일치 허용", 11, ACC, KR, "middle", 600)


# 범례
d.legend(LEG, [
    ("정상 리더", OK),
    ("링크 단절", BAD),
    ("팔로워 고립", WARN),
    ("CP 선택", INFO),
    ("AP 선택", ACC),
])

d.save("10-02.linearizability-cost-cap.svg")
