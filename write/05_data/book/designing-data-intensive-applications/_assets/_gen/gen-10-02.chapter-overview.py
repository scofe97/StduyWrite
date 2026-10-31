# 10-02 개요 — 네트워크 파티션 시의 가용성 충돌(§1)과 CAP 정리 한계(§2), PACELC 확장(§3), CPU 캐시의 성능 포기(§4), 선형성의 성능 하한(§5) 전체 지도.
# 사실 출처: 10-02 도입(L13~L19), §1(L24~L37), §2(L41~L60), §3(L64~L87), §4(L90~L102), §5(L105~L116)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 248
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "10-02 · CHAPTER OVERVIEW", "선형성의 비용과 CAP 정리 전체 지도",
      "네트워크 파티션 장애(§1)와 CAP 한계(§2), PACELC(§3), CPU 캐시(§4), 성능 하한(§5)의 체계를 정리한다.",
      "불가피한 네트워크 파티션 · CAP의 역사와 한계 · 정상 시 지연 트레이드오프 · 하드웨어의 성능 비선형화 · 지연 불확실성 하한")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "선형성의 두 가지 비용 원천: 불가피한 장애인 네트워크 파티션과 가변적 지연이라는 일상적 현실", 12, INK, KR, "middle", 600)

CW = 156
GAP = 14
X0 = 22

cards = [
    ("§1", "파티션 충돌", "선형성과 가용성 충돌",
     [("단일 리더", "리더 A vs 팔로워 B"),
      ("CP 선택", "선형성 유지·가용성 희생"),
      ("AP 선택", "가용성 유지·선형성 희생")],
     INFO),
    ("§2", "CAP 정리", "역사적 의의와 한계",
     [("선형성만 한정", "타 일관성 모델 배제"),
      ("파티션 8% 미만", "90% 이상 장애는 범위 밖"),
      ("지연 무시", "평시 트레이드오프 배제")],
     WARN),
    ("§3", "PACELC", "정상 시 지연 트레이드오프",
     [("P 분기", "A(가용성) vs C(일관성)"),
      ("E 분기", "L(지연) vs C(일관성)"),
      ("시스템 분류", "PA/EL 및 PC/EC")],
     ACC),
    ("§4", "CPU 캐시", "성능을 위한 비선형화",
     [("멀티코어 캐시", "L1·L2 및 스토어 버퍼"),
      ("비선형화 허용", "메모리 배리어 통제"),
      ("포기 이유", "순수 성능 (CAP 무관)")],
     INFO),
    ("§5", "성능 하한", "Attiya·Welch 하한",
     [("Attiya 하한", "지연 불확실성 비례"),
      ("돌파 불가 제약", "더 빠른 알고리즘 없음"),
      ("약한 일관성", "최종·인과 일관성 우회")],
     OK),
]

FOCAL = 2

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + CW / 2, PY + 20, sec, card_c, 11)
    d.t(x + CW / 2, PY + 44, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 62, role, 11, SOFT, KR, "middle")
    d.line(x + 10, PY + 72, x + CW - 10, PY + 72, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 82 + j * 50
        d.tone(x + 8, iy, CW - 16, 42, card_c, 4, "10", 0.8)
        d.t(x + CW / 2, iy + 17, top_txt, 11.5, INK, KR, "middle", 600)
        d.t(x + CW / 2, iy + 32, bot_txt, 11, MUTED, KR, "middle")

# 하단 범례
d.legend(LEG, [
    ("구조 및 기본 사례", INFO),
    ("이론적 한계와 비판", WARN),
    ("실용적 확장 모델", ACC),
    ("수학적 하한과 우회", OK),
])

d.save("10-02.chapter-overview.svg")
