# 08-02 개요 — 약한 격리 수준의 목표(동시성 확보)와 Read Committed(§1), 스냅샷 격리(§2), MVCC(§3), 갱신 손실 방지(§4)로 이어지는 이상 현상 방어 사다리.
# 사실 출처: 08-02 서두(L13~L19), §1(L23~L33), §2(L35~L45), §3(L47~L63), §4(L64~L80), 원서 Ch.8 p.15~28
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "08-02 · CHAPTER OVERVIEW", "약한 격리 수준과 스냅샷 격리 전체 지도",
      "Read Committed(§1), 스냅샷 격리(§2), MVCC 구조(§3), 갱신 손실 방지(§4)의 단계적 방어 체계를 조망한다.",
      "Read Committed · 스냅샷 격리 · MVCC 다중 버전 · 갱신 손실 방지 기법")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "약한 격리 수준의 목표: 직렬화 성능 비용 회피 · 이상 현상 단계별 통제", 12, INK, KR, "middle", 600)

CW = 196
GAP = 12
X0 = 32

cards = [
    ("§1", "Read Committed", "커밋된 데이터만 읽기·쓰기",
     [("더티 읽기 방지", "커밋 전 쓰기 은폐"),
      ("더티 쓰기 방지", "행 수준 잠금"),
      ("읽기 스큐 허용", "한 시점 일관성 미보장")],
     INFO),
    ("§2", "스냅샷 격리", "시작 시점 일관된 스냅샷",
     [("읽기 스큐 방지", "트랜잭션 시작 시점 고정"),
      ("긴 읽기 쿼리 보호", "백업·분석 불일치 제거"),
      ("명칭 혼란 주의", "Repeatable Read 이명")],
     ACC),
    ("§3", "MVCC 구조", "다중 버전 동시성 제어",
     [("행 버전 태깅", "inserted_by · deleted_by"),
      ("비차단 동시성", "읽기와 쓰기 상호 비차단"),
      ("가비지 컬렉션", "오래된 버전 나중에 정리")],
     OK),
    ("§4", "갱신 손실 방지", "읽기-수정-쓰기 충돌 해소",
     [("원자적 쓰기 연산", "읽기-수정-쓰기 불필요"),
      ("명시적 잠금·CAS", "FOR UPDATE · 조건부 쓰기"),
      ("자동 감지·중단", "갱신 손실 감지 시 중단")],
     WARN),
]

FOCAL = 1

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 24, sec, card_c, 11)
    d.t(x + CW / 2 + 12, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64

        if is_focal and j == 0:
            d.tone(x + 8, iy, CW - 16, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 0:
            d.tone(x + 8, iy, CW - 16, 52, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, INFO, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 8, iy, CW - 16, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        elif i == 3 and j == 2:
            d.tone(x + 8, iy, CW - 16, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        else:
            d.box(x + 8, iy, CW - 16, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 1, y), (x2 - 3, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("스냅샷 격리 (focal)", ACC), ("기본 격리", INFO), ("MVCC 다중 버전", OK), ("자동 감지·중단", WARN)])
d.save("08-02.chapter-overview.svg")
