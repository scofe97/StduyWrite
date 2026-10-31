# 08-03 §3 — 2단계 잠금(2PL) 공유·독점 잠금 호환성과 2단계 수명주기
# 사실 출처: 08-03 §3(L70~L87), 원서 Ch.8 p.39~43
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 104
PH = 286
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "08-03 · §3 TWO-PHASE LOCKING", "2단계 잠금(2PL)의 상호 차단 규칙과 단계 변화",
      "공유(S)·독점(X) 잠금의 호환성 매트릭스와 취득-해제 2단계 수명주기",
      "상호 배타 차단 · 읽기 대기 · 쓰기 대기 · 확장 단계 잠금 취득 · 커밋 시 일괄 해제")

# ── 패널 1: 잠금 호환성 매트릭스 (좌측) ──────────────────────────
d.box(24, PY, 404, PH, PAPER2, RULE, 1.0)
d.chip(94, PY + 22, "상호 차단 매트릭스", WARN, 11)
d.t(416, PY + 22, "읽기도 쓰기를, 쓰기도 읽기를 차단", 11, SOFT, KR, "end")

# 매트릭스 테이블 영역
MX = 38
MY = 150
CW = 110
CH = 50

# 열 헤더 (요청 잠금)
d.box(MX + 130, MY, CW, 30, PAPER, RULE, 0.8)
d.t(MX + 130 + CW / 2, MY + 19, "공유 요청(S)", 11, INFO, KR, "middle", 600)
d.box(MX + 130 + CW + 8, MY, CW, 30, PAPER, RULE, 0.8)
d.t(MX + 130 + CW + 8 + CW / 2, MY + 19, "독점 요청(X)", 11, WARN, KR, "middle", 600)

# 행 1: 기존 공유 점유
d.box(MX, MY + 38, 122, CH, PAPER, RULE, 0.8)
d.t(MX + 61, MY + 58, "기존 공유 점유", 11, INFO, KR, "middle", 600)
d.t(MX + 61, MY + 74, "(S / 읽기)", 11, SOFT, KR, "middle")

# 셀 (S, S) -> OK
d.tone(MX + 130, MY + 38, CW, CH, OK, 4, "16", 1.0)
d.t(MX + 130 + CW / 2, MY + 58, "허용", 12, OK, KR, "middle", 600)
d.t(MX + 130 + CW / 2, MY + 74, "동시 읽기 가능", 11, MUTED, KR, "middle")

# 셀 (S, X) -> BAD
d.tone(MX + 130 + CW + 8, MY + 38, CW, CH, BAD, 4, "14", 1.0)
d.t(MX + 130 + CW + 8 + CW / 2, MY + 58, "대기 (차단)", 12, BAD, KR, "middle", 600)
d.t(MX + 130 + CW + 8 + CW / 2, MY + 74, "쓰기 대기 발생", 11, MUTED, KR, "middle")

# 행 2: 기존 독점 점유
d.box(MX, MY + 38 + CH + 8, 122, CH, PAPER, RULE, 0.8)
d.t(MX + 61, MY + 38 + CH + 28, "기존 독점 점유", 11, WARN, KR, "middle", 600)
d.t(MX + 61, MY + 38 + CH + 44, "(X / 쓰기)", 11, SOFT, KR, "middle")

# 셀 (X, S) -> BAD
d.tone(MX + 130, MY + 38 + CH + 8, CW, CH, BAD, 4, "14", 1.0)
d.t(MX + 130 + CW / 2, MY + 38 + CH + 28, "대기 (차단)", 12, BAD, KR, "middle", 600)
d.t(MX + 130 + CW / 2, MY + 38 + CH + 44, "읽기 대기 발생", 11, MUTED, KR, "middle")

# 셀 (X, X) -> BAD
d.tone(MX + 130 + CW + 8, MY + 38 + CH + 8, CW, CH, BAD, 4, "14", 1.0)
d.t(MX + 130 + CW + 8 + CW / 2, MY + 38 + CH + 28, "대기 (차단)", 12, BAD, KR, "middle", 600)
d.t(MX + 130 + CW + 8 + CW / 2, MY + 38 + CH + 44, "쓰기 대기 발생", 11, MUTED, KR, "middle")

# 하단 핵심 요약 상자
d.tone(MX, MY + 154, 376, 32, WARN, 4, "10", 0.9)
d.t(MX + 188, MY + 174, "스냅샷 격리와 차이: 읽기조차 쓰기 잠금을 기다림", 11, WARN, KR, "middle", 600)

# ── 패널 2: 2단계 수명주기 (우측, FOCAL) ───────────────────────
d.box(448, PY, 408, PH, PAPER2, ACC, 1.4)
d.chip(538, PY + 22, "2단계 수명주기", ACC, 11)
d.t(844, PY + 22, "취득 단계 유지 후 일괄 해제", 11, SOFT, KR, "end")

RX = 462
RW = 380

# 1단계: 확장 단계 (잠금 취득)
d.tone(RX, 150, RW, 46, INFO, 6, "14", 1.0)
d.t(RX + RW / 2, 168, "1단계: 확장 단계 (Growing Phase)", 11, INFO, KR, "middle", 600)
d.t(RX + RW / 2, 185, "트랜잭션 실행 중 잠금 계속 획득 (해제 불가)", 11, MUTED, KR, "middle")

d.arrow([(RX + RW / 2, 196), (RX + RW / 2, 208)], SOFT, "soft", 1.2)

# 중간: 점유 유지
d.box(RX, 208, RW, 44, PAPER, RULE, 0.8)
d.t(RX + RW / 2, 226, "잠금 점유 유지 (연산 수행)", 11, INK, KR, "middle", 600)
d.t(RX + RW / 2, 242, "모든 읽기·쓰기가 끝날 때까지 잠금 유지", 11, SOFT, KR, "middle")

d.arrow([(RX + RW / 2, 252), (RX + RW / 2, 264)], ACC, "acc", 1.2)

# 2단계: 축소 단계 (일괄 해제, FOCAL)
d.tone(RX, 264, RW, 46, ACC, 6, "20", 1.3)
d.t(RX + RW / 2, 282, "2단계: 축소 단계 (Shrinking Phase)", 11, ACC, KR, "middle", 600)
d.t(RX + RW / 2, 299, "커밋 또는 중단 시 보유 잠금 일괄 해제", 11, INK, KR, "middle")

# 팬텀 방어 보조
d.box(RX, 318, RW, 32, PAPER, RULE, 0.8)
d.t(RX + RW / 2, 338, "팬텀 방어: 서술 잠금 대신 인덱스 범위 잠금 적용", 11, MUTED, KR, "middle")

d.legend(LEG, [("동시 읽기 허용", OK), ("접근 차단 및 대기", BAD), ("확장 단계·요청", INFO), ("2PL 상호 차단", WARN), ("일괄 해제 (focal)", ACC)])
d.save("08-03.two-phase-locking.svg")
