# 13-02 세부 도식 — 람다 아키텍처(이중 경로) vs 카파 아키텍처(단일 스트림 통합) 구조 비교
# 사실 출처: 13-02 본문 §3(L44~L54), 원서 Ch.13 p.10~12 (Lambda architecture problems, Kappa architecture, event replay, exactly-once, event-time windowing)
# 2026-10-31 검증: 원서 p.10 은 람다 구조를 그리지 않는다(문제 많아 쓰이지 않음만). 람다 칸은 본문 L53 어휘(배치 정확·느림, 스트림 빠름·근사치, 읽기 시점 병합, 두 번 구현)로, 레이어 이름 제거
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY1 = 100
PH1 = 172
PY2 = 286
PH2 = 206
LEG = PY2 + PH2 + 20
H = LEG + 46

d = D(W, H, "13-02 · SECTION 3", "람다 아키텍처와 카파 아키텍처의 구조 비교",
      "배치·스트림 병렬 운영(람다)과 단일 스트림 엔진 통합(카파)의 구조 비교",
      "배치·스트림 이중 경로 · 읽기 시점 병합 · 단일 스트림 엔진 · 카파 세 조건")

# 1. 람다 아키텍처 패널
d.box(24, PY1, 832, PH1, PAPER2, RULE, 0.9)
d.chip(24 + 40, PY1 + 20, "람다 모델", WARN, 11)
d.t(24 + 86, PY1 + 24, "람다 아키텍처 (이중 경로 운영)", 13, INK, KR, "start", 600)
d.t(24 + 14, PY1 + 44, "배치와 스트림을 병렬 운영 · 읽기 시점에 결과 병합", 11, SOFT, KR, "start")
d.line(24 + 8, PY1 + 54, 24 + 832 - 8, PY1 + 54, RULE, 0.8)

# 람다 내부 컴포넌트
# 원시 이벤트
d.box(38, PY1 + 68, 100, 92, PAPER, RULE, 0.6)
d.t(88, PY1 + 102, "입력 이벤트", 12, INK, KR, "middle", 600)
d.t(88, PY1 + 122, "두 경로에", 11, MUTED, KR, "middle")
d.t(88, PY1 + 138, "병렬 입력", 11, MUTED, KR, "middle")

# 중간 2개 레이어
d.box(158, PY1 + 64, 250, 46, PAPER, RULE, 0.6)
d.t(168, PY1 + 84, "배치 처리 (정확 · 느림)", 12, INK, KR, "start", 600)
d.t(168, PY1 + 100, "같은 비즈니스 로직 구현 1", 11, MUTED, KR, "start")

d.box(158, PY1 + 118, 250, 46, PAPER, RULE, 0.6)
d.t(168, PY1 + 138, "스트림 처리 (빠름 · 근사치)", 12, INK, KR, "start", 600)
d.t(168, PY1 + 154, "같은 비즈니스 로직 구현 2", 11, MUTED, KR, "start")

# 서빙 레이어
d.box(428, PY1 + 68, 156, 92, PAPER, RULE, 0.6)
d.t(438, PY1 + 96, "읽기 시점 병합", 12, INK, KR, "start", 600)
d.t(438, PY1 + 118, "배치 결과 + 스트림 결과", 11, INK, KR, "start")
d.t(438, PY1 + 138, "읽을 때 합침", 11, MUTED, KR, "start")

# 클라이언트
d.box(604, PY1 + 68, 104, 92, PAPER, RULE, 0.6)
d.t(656, PY1 + 104, "읽기 요청", 12, INK, KR, "middle", 600)
d.t(656, PY1 + 128, "합친 결과", 11, MUTED, KR, "middle")

# 우측 한계점 경고 박스
d.tone(724, PY1 + 64, 120, 100, WARN, 4, "16", 1.0)
d.t(784, PY1 + 86, "람다의 부담", 11, WARN, KR, "middle", 600)
d.t(784, PY1 + 108, "같은 로직을", 11, INK, KR, "middle")
d.t(784, PY1 + 128, "다른 프레임워크로 두 번", 11, INK, KR, "middle")
d.t(784, PY1 + 148, "개발·유지·테스트 부담", 11, WARN, KR, "middle")

# 람다 화살표
d.arrow([(138, PY1 + 114), (148, PY1 + 114), (148, PY1 + 87), (154, PY1 + 87)], MUTED, "ar", 1.1)
d.arrow([(138, PY1 + 114), (148, PY1 + 114), (148, PY1 + 141), (154, PY1 + 141)], MUTED, "ar", 1.1)

d.arrow([(408, PY1 + 87), (418, PY1 + 87), (418, PY1 + 114), (424, PY1 + 114)], MUTED, "ar", 1.1)
d.arrow([(408, PY1 + 141), (418, PY1 + 141), (418, PY1 + 114), (424, PY1 + 114)], MUTED, "ar", 1.1)

d.arrow([(584, PY1 + 114), (600, PY1 + 114)], MUTED, "ar", 1.1)


# 2. 카파 아키텍처 패널 (Focal)
d.box(24, PY2, 832, PH2, PAPER2, ACC, 1.4)
d.chip(24 + 40, PY2 + 20, "카파 모델", ACC, 11)
d.t(24 + 86, PY2 + 24, "카파 아키텍처 (단일 스트림 엔진 통합)", 13, ACC, KR, "start", 600)
d.t(24 + 14, PY2 + 44, "배치는 스트림의 특수한 경우 · 실시간과 히스토리 재처리를 단일 엔진으로 일원화", 11, SOFT, KR, "start")
d.line(24 + 8, PY2 + 54, 24 + 832 - 8, PY2 + 54, RULE, 0.8)

# 카파 파이프라인 행
d.box(38, PY2 + 66, 150, 56, PAPER, RULE, 0.6)
d.t(50, PY2 + 88, "로그 브로커 (Kafka)", 12, INK, KR, "start", 600)
d.t(50, PY2 + 106, "최근 이벤트 · 히스토리 재생", 11, MUTED, KR, "start")

d.tone(214, PY2 + 66, 280, 56, ACC, 4, "16", 1.2)
d.t(228, PY2 + 88, "단일 스트림 처리 엔진", 12, ACC, KR, "start", 600)
d.t(228, PY2 + 106, "히스토리 재주입도 같은 엔진·같은 코드", 11, INK, KR, "start")

d.box(520, PY2 + 66, 180, 56, PAPER, RULE, 0.6)
d.t(532, PY2 + 88, "파생 뷰", 12, INK, KR, "start", 600)
d.t(532, PY2 + 106, "스트림 엔진 하나가 갱신", 11, MUTED, KR, "start")

d.box(726, PY2 + 66, 118, 56, PAPER, RULE, 0.6)
d.t(785, PY2 + 88, "읽기 요청", 12, INK, KR, "middle", 600)
d.t(785, PY2 + 106, "파생 뷰 조회", 11, MUTED, KR, "middle")

# 카파 파이프라인 화살표
d.arrow([(188, PY2 + 94), (210, PY2 + 94)], ACC, "acc", 1.2)
d.arrow([(494, PY2 + 94), (516, PY2 + 94)], ACC, "acc", 1.2)
d.arrow([(700, PY2 + 94), (722, PY2 + 94)], MUTED, "ar", 1.2)

# 카파 3대 필수 전제 조건 박스들
d.box(38, PY2 + 134, 252, 58, PAPER, RULE, 0.6)
d.chip(70, PY2 + 152, "조건 1", OK, 11)
d.t(108, PY2 + 156, "이벤트 재재생", 12, INK, KR, "start", 600)
d.t(50, PY2 + 178, "같은 엔진으로 히스토리 재생", 11, MUTED, KR, "start")

d.box(302, PY2 + 134, 268, 58, PAPER, RULE, 0.6)
d.chip(334, PY2 + 152, "조건 2", OK, 11)
d.t(372, PY2 + 156, "정확히 한 번 의미론", 12, INK, KR, "start", 600)
d.t(314, PY2 + 178, "장애가 없었던 것과 같은 결과", 11, MUTED, KR, "start")

d.box(582, PY2 + 134, 262, 58, PAPER, RULE, 0.6)
d.chip(614, PY2 + 152, "조건 3", OK, 11)
d.t(652, PY2 + 156, "이벤트 시간 윈도우", 12, INK, KR, "start", 600)
d.t(594, PY2 + 178, "처리 시간 아닌 이벤트 시간 기준", 11, MUTED, KR, "start")

d.legend(LEG, [
    ("카파 단일 엔진 (focal)", ACC),
    ("카파 세 조건", OK),
    ("람다 이중 경로", WARN),
])

d.save("13-02.lambda-vs-kappa.svg")
