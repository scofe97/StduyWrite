# 08-03 개요 — Write Skew와 직렬화 격리 전체 지도
# 검증(10-31 cc-ddia-dverify08): "중복 예약"을 본문 §1 팬텀 예시 "회의실 예약 충돌"로
# 사실 출처: 08-03 서두(L15~L22), §1(L25~L48), §2(L50~L68), §3(L70~L87), §4(L89~L109)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 276
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "08-03 · CHAPTER OVERVIEW", "Write Skew와 직렬화 격리 전체 지도",
      "스냅샷 격리에서 발생하는 쓰기 스큐·팬텀 문제와 이를 해결하는 세 가지 직렬화 구현 접근법",
      "전제 조건 붕괴 · 단일 스레드 직렬 실행 · 2단계 잠금 · 직렬화 가능 스냅샷 격리")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "공통 과제: 조건 확인 후 쓰기(check-then-act) 패턴에서 전제 조건 붕괴를 막는 직렬화 보장", 12, INK, KR, "middle", 600)

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "쓰기 스큐·팬텀", "스냅샷 격리 한계",
     [("이상 현상", "전제 붕괴 · 팬텀 발생"),
      ("취약 사례", "당직 의사 0명 · 회의실 예약 충돌"),
      ("방어 한계", "행 잠금 불가 · 충돌 구체화")],
     BAD),
    ("§2", "직렬 실행", "단일 스레드 순차 처리",
     [("구현 원리", "인메모리 + 저장 프로시저"),
      ("적용 시스템", "VoltDB · Redis · Datomic"),
      ("제약 사항", "단일 코어 한계 · 다중 샤드 지연")],
     INFO),
    ("§3", "2단계 잠금", "비관적 상호 차단",
     [("잠금 규칙", "공유(S)·독점(X) 상호 차단"),
      ("팬텀 방지", "인덱스 범위 잠금 적용"),
      ("제약 사항", "지연 시간 증가 · 잦은 데드락")],
     WARN),
    ("§4", "SSI", "낙관적 충돌 감지",
     [("무차단 실행", "잠금 없이 진행 후 커밋 검사"),
      ("감지 기법", "낡은 MVCC 읽기 추적"),
      ("적용 시스템", "PostgreSQL · CockroachDB")],
     ACC),
]

FOCAL = 3

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + 28, PY + 24, sec, card_c, 12)
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 11, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 66

        if j == 0:
            d.tone(x + 10, iy, CW - 20, 54, card_c, 6, "14", 1.0)
            d.t(x + CW / 2, iy + 22, top_txt, 11, card_c, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        elif is_focal and j == 1:
            d.tone(x + 10, iy, CW - 20, 54, ACC, 6, "20", 1.3)
            d.t(x + CW / 2, iy + 22, top_txt, 11, ACC, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        elif j == 1:
            d.box(x + 10, iy, CW - 20, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 11, SOFT, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, INK, KR, "middle")
        else:
            d.box(x + 10, iy, CW - 20, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 11, SOFT, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("쓰기 스큐·이상 (§1)", BAD), ("직렬 실행 (§2)", INFO), ("2단계 잠금 (§3)", WARN), ("SSI 최신 접근 (§4)", ACC)])
d.save("08-03.chapter-overview.svg")
