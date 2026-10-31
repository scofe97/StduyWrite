# 09-03 §5 — 시스템 모델(타이밍·노드 장애)과 안전성·활동성 보장 체계
# 사실 출처: 09-03 §5(L71~L96), 원서 Ch.9 "System Model and Reality", "Safety and liveness"
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
PY = 152
PH = 300
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "09-03 · §5 SYSTEM MODELS & GUARANTEES", "시스템 모델과 안전성·활동성 보장 체계",
      "분산 알고리즘의 타이밍·노드 장애 가정 형식화와 안전성(Safety)·활동성(Liveness) 두 보장 속성",
      "부분 동기 · 크래시-복구 표준 모델 · 안전성 절대 보장 · 활동성 조건부 보장")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "설계 원칙: 안전성은 항상 절대 보장 · 활동성은 네트워크 복구 시 보장", 12, INK, KR, "middle", 600)

PW = 404
GAP = 24
X1 = 24
X2 = X1 + PW + GAP

# === 좌측 패널: 분산 시스템 모델 분류 ===
d.box(X1, PY, PW, PH, PAPER2, RULE, 1.0)
d.box(X1, PY, PW, 32, PAPER, RULE, 0.8)
d.t(X1 + 14, PY + 21, "시스템 모델 가정 (타이밍 · 노드 장애)", 12, INK, KR, "start", 600)
d.t(X1 + PW - 14, PY + 21, "가정 형식화", 11, MUTED, KR, "end")

# 1. 타이밍 모델 (상단)
d.tone(X1 + 12, PY + 44, PW - 24, 102, RULE, 4, "08", 0.8)
d.t(X1 + 22, PY + 64, "타이밍 모델 3종", 11, ACC, KR, "start", 600)

d.t(X1 + 22, PY + 84, "• 동기: 지연·포즈 상한 엄격 보장 (비현실적)", 11, MUTED, KR, "start")
d.t(X1 + 22, PY + 104, "• 부분 동기: 평소 동기 · 때때로 상한 초과 (실제 시스템)", 11, INK, KR, "start", 600)
d.t(X1 + 22, PY + 124, "• 비동기: 타이밍 가정 없음 · 시계 부재 (제한적)", 11, MUTED, KR, "start")

# 2. 노드 장애 모델 (중단)
d.tone(X1 + 12, PY + 154, PW - 24, 96, RULE, 4, "08", 0.8)
d.t(X1 + 22, PY + 174, "노드 장애 모델 3종", 11, ACC, KR, "start", 600)

d.t(X1 + 22, PY + 194, "• 크래시-스톱: 노드 정지 후 영구 종료", 11, MUTED, KR, "start")
d.t(X1 + 22, PY + 214, "• 크래시-복구: 재시작 가능 · 디스크 유지 (실제 시스템)", 11, INK, KR, "start", 600)
d.t(X1 + 22, PY + 234, "• 비잔틴: 노드의 임의 조작 및 거짓말 거동", 11, MUTED, KR, "start")

# 3. 표준 조합 배너 (하단)
d.tone(X1 + 12, PY + 258, PW - 24, 30, ACC, 4, "16", 1.1)
d.t(X1 + PW / 2, PY + 278, "실제 시스템 표준 모델: 부분 동기 + 크래시-복구", 11, ACC, KR, "middle", 600)


# === 우측 패널: 안전성 vs 활동성 보장 ===
d.box(X2, PY, PW, PH, PAPER2, RULE, 1.0)
d.box(X2, PY, PW, 32, PAPER, RULE, 0.8)
d.t(X2 + 14, PY + 21, "알고리즘 보장 속성 (Safety vs Liveness)", 12, INK, KR, "start", 600)
d.t(X2 + PW - 14, PY + 21, "두 보장 속성", 11, MUTED, KR, "end")

# 1. 안전성 (상단)
d.tone(X2 + 12, PY + 44, PW - 24, 114, OK, 4, "10", 1.0)
d.t(X2 + 22, PY + 66, "안전성 (Safety)", 12, OK, KR, "start", 600)
d.t(X2 + PW - 22, PY + 66, "나쁜 일 미발생", 11, OK, KR, "end")
d.line(X2 + 22, PY + 76, X2 + PW - 22, PY + 76, RULE, 0.6)
d.t(X2 + 22, PY + 96, "• 정의: 위반 시점 지목 가능 · 취소 불가능", 11, INK, KR, "start")
d.t(X2 + 22, PY + 116, "• 예시: 펜싱 토큰 유일성 · 단조 시퀀스 식별자", 11, MUTED, KR, "start")
d.t(X2 + 22, PY + 138, "• 보장 원칙: 모든 장애 상황에서 항상 엄격 보장", 11, OK, KR, "start", 600)

# 2. 활동성 (하단)
d.tone(X2 + 12, PY + 168, PW - 24, 120, INFO, 4, "10", 1.0)
d.t(X2 + 22, PY + 190, "활동성 (Liveness)", 12, INFO, KR, "start", 600)
d.t(X2 + PW - 22, PY + 190, "좋은 일 결국 발생", 11, INFO, KR, "end")
d.line(X2 + 22, PY + 200, X2 + PW - 22, PY + 200, RULE, 0.6)
d.t(X2 + 22, PY + 220, "• 정의: 특정 시점 미성립 허용 · 미래 성립 희망", 11, INK, KR, "start")
d.t(X2 + 22, PY + 240, "• 예시: 요청 응답 가용성 · 최종 일관성", 11, MUTED, KR, "start")
d.t(X2 + 22, PY + 262, "• 보장 원칙: 과반수 생존 및 네트워크 복구 시 보장", 11, INFO, KR, "start", 600)


d.legend(LEG, [
    ("표준 모델 (focal)", ACC),
    ("이론적 단순화", MUTED),
    ("안전성 (항상 보장)", OK),
    ("활동성 (조건부 보장)", INFO),
])

d.save("09-03.system-models-safety-liveness.svg")
