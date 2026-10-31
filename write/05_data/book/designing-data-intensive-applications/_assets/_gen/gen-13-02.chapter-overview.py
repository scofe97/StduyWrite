# 13-02 개요 — 비동기 파생(§1), 재처리 진화(§2), 람다·카파(§3), DB 언번들링(§4), 연합 vs 언번들드(§5) 전체 지도.
# 사실 출처: 13-02 본문 서두(L14~L18), §1(L24~L31), §2(L34~L41), §3(L44~L53), §4(L56~L68), §5(L71~L82), 원서 Ch.13 p.3~16
# 2026-10-31 검증: 배너 중립화, 라벨을 본문 어휘로 교체(3대·즉시 롤백·듀얼 뷰 등 근거 없는 말 제거)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 244
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "13-02 · CHAPTER OVERVIEW", "배치·스트림 통합과 DB 언번들링 전체 지도",
      "비동기 파생(§1), 재처리 진화(§2), 람다·카파 통합(§3), DB 언번들링(§4), 연합 vs 언번들드(§5)의 체계.",
      "비동기 파생 · 재처리와 3선식 · 람다와 카파 · DB 내부 기능 외부 조합 · 읽기 통합 vs 쓰기 통합")

# 상단 공통 전제 배너
d.box(20, BANNER_Y, W - 40, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 23, "배치·스트림 단일 엔진 통합 + DB 내부 기능 외부 조합 → 유연하고 유지보수 쉬운 시스템", 12, INK, KR, "middle", 600)

X0 = 20
CW = 162
GAP = 7

cards = [
    ("§1", "비동기 파생", "내결함성과 격리",
     [("장애 국소화", "느린·실패 소비자 무영향"),
      ("버퍼링 격리", "이벤트 로그 버퍼링"),
      ("교차 샤드 인덱스", "비동기 유지 시 신뢰성 최고")],
     WARN, False),
    ("§2", "재처리 진화", "점진적 스키마 전환",
     [("히스토리 재처리", "누적 데이터로 새 뷰"),
      ("3선식 공존", "신구 파생 뷰 동시 유지"),
      ("점진적 전환", "모든 단계 되돌릴 수 있음")],
     OK, False),
    ("§3", "람다와 카파", "단일 엔진 통합",
     [("람다 이중 부담", "배치·스트림 중복 구현"),
      ("카파 단일 경로", "스트림 하나로 통합"),
      ("세 가지 조건", "재생·정확히 한 번·이벤트 시간")],
     ACC, True),
    ("§4", "DB 언번들링", "내부 기능 외재화",
     [("인덱스·구체화 뷰", "외부로 꺼내 조합"),
      ("CREATE INDEX ≈ CDC", "기존 데이터 재처리 + 갱신"),
      ("조직 전체 = 거대 DB", "파생 시스템 = 인덱스 타입")],
     INFO, False),
    ("§5", "연합과 언번들드", "통합 관점의 대비",
     [("연합 = 읽기 통합", "통합 쿼리 인터페이스"),
      ("언번들드 = 쓰기 통합", "CDC·이벤트 로그로 동기화"),
      ("느슨한 결합", "Unix 철학 · 독립 개발")],
     OK, False),
]

for idx, (sec, title, role, items, card_c, is_focal) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 상단 헤더: 절 칩 + 제목 + 부제목
    d.chip(x + 28, y + 20, sec, card_c, 11)
    d.t(x + 50, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 14, y + 46, role, 11, SOFT, KR, "start")

    d.line(x + 8, y + 58, x + CW - 8, y + 58, RULE, 0.8)

    # 3개 항목
    iy0 = y + 80
    for i_idx, (head, sub) in enumerate(items):
        iy = iy0 + i_idx * 52
        d.box(x + 6, iy - 14, CW - 12, 44, PAPER, RULE, 0.6)
        d.t(x + 12, iy + 2, head, 12, INK, KR, "start", 600)
        d.t(x + 12, iy + 20, sub, 11, MUTED, KR, "start")

# 카드 간 연결 화살표
for idx in range(4):
    ax = X0 + (idx + 1) * CW + idx * GAP
    ay = PY + PH / 2
    d.arrow([(ax + 1, ay), (ax + GAP - 1, ay)], MUTED, "ar", 1.0)

d.legend(LEG, [
    ("단일 엔진 통합 (focal)", ACC),
    ("재처리·통합 방식", OK),
    ("DB 언번들링", INFO),
    ("비동기성·내결함성", WARN),
])

d.save("13-02.chapter-overview.svg")
