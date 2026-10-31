# 13-02 세부 도식 — 재처리를 통한 점진적 스키마 전환과 신구 뷰 공존 메커니즘
# 사실 출처: 13-02 본문 §2(L34~L42), 원서 Ch.13 p.7~9 (railway dual gauge 3선식 비유, dual views side-by-side, gradual traffic shifting, reversible rollback)
# 2026-10-31 검증: 배너 중립화, 원서 p.9(소수 사용자로 성능·버그 확인, 비율 확대, 구 뷰 삭제, 쉽게 되돌림) 어휘로 교체
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 100
BANNER_H = 34
PY = 146
PH = 280
LEG = PY + PH + 22
H = LEG + 48

d = D(W, H, "13-02 · SECTION 2", "재처리를 통한 신구 파생 뷰 공존과 점진적 전환",
      "기존 데이터를 새 변환 코드로 재처리해 신구 파생 뷰를 함께 유지하는 점진적 전환",
      "히스토리 재처리 · 3선식 · 신구 뷰 공존 · 점진적 전환 · 모든 단계 되돌릴 수 있음")

# 상단 3선식 철도 비유 배너
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 22, "철도 3선식(dual gauge) = 두 규격 열차 공존 · 신구 스키마 파생 뷰를 동시에 유지해 점진 전환", 12, INK, KR, "middle", 600)

X1 = 24
W1 = 186

X2 = 238
W2 = 350

X3 = 616
W3 = 240

# 1구역: 원천 로그 저장소
d.box(X1, PY, W1, PH, PAPER2, RULE, 0.9)
d.chip(X1 + 28, PY + 20, "원천", ACC, 11)
d.t(X1 + 52, PY + 24, "원천 데이터", 13, INK, KR, "start", 600)
d.t(X1 + 14, PY + 46, "누적된 히스토리", 11, SOFT, KR, "start")

d.line(X1 + 8, PY + 58, X1 + W1 - 8, PY + 58, RULE, 0.8)

b1_items = [
    ("누적 히스토리", "대용량 기존 데이터"),
    ("새 변환 코드", "완전히 다른 모델로"),
    ("재처리", "새 스키마 파생 뷰 생성"),
]
for idx, (head, sub) in enumerate(b1_items):
    iy = PY + 72 + idx * 64
    d.box(X1 + 8, iy, W1 - 16, 52, PAPER, RULE, 0.6)
    d.t(X1 + 14, iy + 20, head, 12, INK, KR, "start", 600)
    d.t(X1 + 14, iy + 38, sub, 11, MUTED, KR, "start")

# 2구역 상단: 구 파생 뷰 (구 스키마)
d.box(X2, PY, W2, 134, PAPER2, RULE, 0.9)
d.chip(X2 + 34, PY + 20, "구 뷰", MUTED, 11)
d.t(X2 + 64, PY + 24, "구 파생 뷰 (구 스키마)", 13, INK, KR, "start", 600)
d.t(X2 + 14, PY + 46, "같은 원천에서 독립 파생", 11, SOFT, KR, "start")
d.line(X2 + 8, PY + 58, X2 + W2 - 8, PY + 58, RULE, 0.8)

d.box(X2 + 8, PY + 68, W2 - 16, 56, PAPER, RULE, 0.6)
d.t(X2 + 14, PY + 89, "대부분 사용자 계속 라우팅", 12, INK, KR, "start", 600)
d.t(X2 + 14, PY + 109, "문제 시 돌아갈 동작 시스템", 11, MUTED, KR, "start")

# 2구역 하단: 신 파생 뷰 (신 스키마) - Focal
d.box(X2, PY + 146, W2, 134, PAPER2, OK, 1.4)
d.chip(X2 + 34, PY + 166, "신 뷰", OK, 11)
d.t(X2 + 64, PY + 170, "신 파생 뷰 (신 스키마)", 13, OK, KR, "start", 600)
d.t(X2 + 14, PY + 192, "새 변환 코드로 히스토리 재처리", 11, SOFT, KR, "start")
d.line(X2 + 8, PY + 204, X2 + W2 - 8, PY + 204, RULE, 0.8)

d.box(X2 + 8, PY + 214, W2 - 16, 56, PAPER, RULE, 0.6)
d.t(X2 + 14, PY + 235, "구 뷰와 나란히 유지", 12, INK, KR, "start", 600)
d.t(X2 + 14, PY + 255, "히스토리 재처리로 생성 · 소수 사용자 검증", 11, MUTED, KR, "start")

# 3구역: 점진적 라우팅 전환 & 가역성
d.box(X3, PY, W3, PH, PAPER2, RULE, 0.9)
d.chip(X3 + 28, PY + 20, "전환", INFO, 11)
d.t(X3 + 52, PY + 24, "점진적 라우팅 전환", 13, INK, KR, "start", 600)
d.t(X3 + 14, PY + 46, "사용자 비율을 단계적으로 이동", 11, SOFT, KR, "start")
d.line(X3 + 8, PY + 58, X3 + W3 - 8, PY + 58, RULE, 0.8)

steps = [
    ("1단계: 소수 사용자 이동", "성능 테스트 · 버그 찾기"),
    ("2단계: 비율 점진 확대", "문제 없을 때 비율 증가"),
    ("3단계: 구 뷰 제거", "모든 사용자 이동 후 삭제"),
]
for idx, (title, sub) in enumerate(steps):
    iy = PY + 68 + idx * 50
    d.box(X3 + 8, iy, W3 - 16, 42, PAPER, RULE, 0.6)
    d.t(X3 + 14, iy + 17, title, 12, INK, KR, "start", 600)
    d.t(X3 + 14, iy + 33, sub, 11, MUTED, KR, "start")

# 3구역 하단 롤백 안전망 박스
d.tone(X3 + 8, PY + 224, W3 - 16, 46, WARN, 4, "16", 1.0)
d.t(X3 + 14, PY + 243, "모든 단계 되돌릴 수 있음", 11, WARN, KR, "start", 600)
d.t(X3 + 14, PY + 260, "문제 시 구 뷰로 복귀", 11, INK, KR, "start")

# 연결 화살표 (수평 및 직각 엘보)
d.arrow([(X1 + W1, PY + 67), (X2 - 4, PY + 67)], MUTED, "ar", 1.2)
d.arrow([(X1 + W1, PY + 213), (X2 - 4, PY + 213)], OK, "ok", 1.3)

MID_X = (X2 + W2 + X3) / 2
d.arrow([(X2 + W2, PY + 67), (MID_X, PY + 67), (MID_X, PY + 89), (X3 - 4, PY + 89)], MUTED, "ar", 1.2)
d.arrow([(X2 + W2, PY + 213), (MID_X, PY + 213), (MID_X, PY + 139), (X3 - 4, PY + 139)], OK, "ok", 1.3)

d.legend(LEG, [
    ("신 파생 뷰 (focal)", OK),
    ("원천 데이터", ACC),
    ("점진적 라우팅", INFO),
    ("되돌리기 (가역성)", WARN),
])

d.save("13-02.reprocessing-dual-view.svg")
