# 12-02 §4 — 변경 데이터 캡처(CDC)와 이벤트 소싱의 추상화 수준 및 상태 관리 비교.
# 사실 출처: 12-02 §4(L70~L89), 자주 받는 오해 2(L111), 원서 p.27(CDC 는 키별 컴팩션 가능, 이벤트 소싱은 "Log compaction is not possible in the same way")
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
Y0 = 152
CARD_H = 340
PANEL_Y = Y0 + CARD_H + 12
PANEL_H = 52
LEG = PANEL_Y + PANEL_H + 20
H = LEG + 52

d = D(W, H, "12-02 · §4 EVENT SOURCING VS CDC", "CDC와 이벤트 소싱의 아키텍처 비교",
      "데이터베이스 변경을 스트림으로 다루는 두 접근 방식의 추상화 계층과 상태 모델 대비.",
      "저수준 물리 변경 vs 고수준 도메인 의도 · 최소 침습 도입 vs 전면 설계 · 로그 컴팩션 가능 여부")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "비교 핵심: CDC는 DB 변경을 캡처하고, 이벤트 소싱은 애플리케이션 수준에서 불변 이벤트를 설계", 12, INK, KR, "middle", 600)

CW = 406
GAP = 12
C1_X = 28
C2_X = C1_X + CW + GAP

# Left Card: CDC
d.box(C1_X, Y0, CW, CARD_H, PAPER2, INFO, 1.2)
d.chip(C1_X + 36, Y0 + 20, "저수준", INFO, 11, pad=4)
d.t(C1_X + 70, Y0 + 24, "CDC (변경 데이터 캡처)", 13, INK, KR, "start", 600)
d.line(C1_X + 10, Y0 + 38, C1_X + CW - 10, Y0 + 38, RULE, 0.6)
d.t(C1_X + CW / 2, Y0 + 52, "기존 뮤터블 DB에 최소 침습으로 파생 동기화", 11, MUTED, KR, "middle")

# Right Card: Event Sourcing
d.tone(C2_X, Y0, CW, CARD_H, ACC, 6, "14", 1.4)
d.chip(C2_X + 36, Y0 + 20, "고수준", ACC, 11, pad=4)
d.t(C2_X + 70, Y0 + 24, "이벤트 소싱 (Event Sourcing)", 13, ACC, KR, "start", 600)
d.line(C2_X + 10, Y0 + 38, C2_X + CW - 10, Y0 + 38, RULE, 0.6)
d.t(C2_X + CW / 2, Y0 + 52, "사용자 의도를 불변 이벤트로 기록하고 상태 재생", 11, INK, KR, "middle")

rows = [
    ("추상화 수준",
     "저수준 스토리지 변경 (DB 물리 쓰기 반영)",
     "고수준 애플리케이션 (사용자 비즈니스 의도)",
     INFO, ACC),
    ("이벤트 의미",
     "행 갱신: \"X 행이 B로 변경됨\"",
     "도메인 액션: \"사용자가 Y를 주문함\"",
     INFO, OK),
    ("기존 DB 도입",
     "최소 침습적 연동 (기존 뮤터블 DB 유지)",
     "전면 재설계 (설계 초기부터 이벤트 기반 구축)",
     OK, WARN),
    ("로그 컴팩션",
     "키별 최신값 보존 컴팩션 가능",
     "전체 이력 필요 (같은 방식 컴팩션 불가)",
     OK, WARN),
    ("상태 갱신 방식",
     "UPDATE · DELETE 직접 허용",
     "Append-only 불변 로그 (업데이트·삭제 권장 안 함)",
     INFO, ACC),
]

RY0 = Y0 + 68
RH = 48
RGAP = 6

for idx, (cat, cdc_desc, es_desc, cdc_c, es_c) in enumerate(rows):
    ry = RY0 + idx * (RH + RGAP)

    # CDC row box
    d.box(C1_X + 10, ry, CW - 20, RH, PAPER, RULE, 0.7, r=4)
    d.chip(C1_X + 62, ry + RH / 2, cat, cdc_c, 11, pad=5)
    d.t(C1_X + 116, ry + 28, cdc_desc, 11, INK, KR, "start")

    # ES row box
    d.box(C2_X + 10, ry, CW - 20, RH, PAPER, RULE, 0.7, r=4)
    d.chip(C2_X + 62, ry + RH / 2, cat, es_c, 11, pad=5)
    d.t(C2_X + 116, ry + 28, es_desc, 11, INK, KR, "start")

# 하단 요약 패널
d.tone(28, PANEL_Y, W - 56, PANEL_H, OK, 6, "14", 1.2)
d.t(W / 2, PANEL_Y + 22, "기존 뮤터블 DB에 최소 침습 적용 (CDC)  vs  초기 설계부터 적용, 더 풍부한 이력 (이벤트 소싱)", 13, OK, KR, "middle", 600)
d.t(W / 2, PANEL_Y + 40, "목적이 다른 두 방식 · 어느 쪽이 낫다고 일반화하기 어려움", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("CDC (저수준 캡처)", INFO),
    ("이벤트 소싱 (focal)", ACC),
    ("이점", OK),
    ("제약", WARN),
])

d.save("12-02.event-sourcing-vs-cdc.svg")
