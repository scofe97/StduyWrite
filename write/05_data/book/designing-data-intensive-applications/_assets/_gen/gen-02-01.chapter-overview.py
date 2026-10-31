# 02-01 개요 — 사용자·게시·팔로우 관계형 조인, 쓰기 시점 fan-out 배달, 구체화 뷰 트레이드오프와 극단 케이스 전체 지도.
# 사실 출처: 02-01 서두(L28~L35), §1(L38~L58), §2(L62~L73), §3(L77~L87)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 252
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "02-01 · CHAPTER OVERVIEW", "사례 연구 — 소셜 네트워크 홈 타임라인 전체 지도",
      "관계형 스키마와 읽기 시점 조인(§1), fan-out 배달과 부하 이전(§2), 구체화 뷰 트레이드오프와 극단 케이스(§3)를 조망한다.",
      "관계형 조인과 폴링 폭발 · 쓰기 시점 fan-out 배달 · 구체화 뷰 트레이드오프와 극단 케이스")

# 상단 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "소셜 네트워크 전제: 하루 5억 게시 · 평균 200 팔로우/팔로워 · 유명인 편차", 12, INK, KR, "middle", 600)

CW = 252
GAP = 26
X0 = 36

cards = [
    ("§1", "사용자·게시·팔로우", "관계형 스키마와 조인 질의",
     [("관계형 3개 테이블", "users · posts · follows 모델"),
      ("읽기 시점 SQL 조인", "팔로우 최신 1,000건 질의"),
      ("5초 주기 폴링 폭발", "초당 4억 건 발신자별 조회")],
     INFO),
    ("§2", "fan-out 타임라인", "쓰기 시점 배달과 캐시 응답",
     [("쓰기 시점 능동 푸시", "팔로워 홈 타임라인에 삽입"),
      ("fan-out 배달 처리", "계수 200 · 초당 100만+ 쓰기"),
      ("캐시 즉시 응답", "큐 적재로 스파이크 지연 완충")],
     ACC),
    ("§3", "구체화 뷰", "파생 데이터와 극단 케이스",
     [("파생 구체화 뷰", "읽기 가속 대 쓰기 부담 절충"),
      ("다수 팔로잉 샘플링", "높은 쓰기율 시 일부 쓰기 생략"),
      ("유명인 하이브리드 병합", "별도 저장 후 읽기 시점 병합")],
     OK),
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
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 58

        if is_focal and j == 1:
            d.tone(x + 12, iy, CW - 24, 48, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 0:
            d.tone(x + 12, iy, CW - 24, 48, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, INFO, KR, "middle")
        elif i == 0 and j == 2:
            d.tone(x + 12, iy, CW - 24, 48, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, WARN, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 12, iy, CW - 24, 48, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, OK, KR, "middle")
        elif i == 2 and j == 2:
            d.tone(x + 12, iy, CW - 24, 48, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, WARN, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 48, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 20, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 36, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("핵심 fan-out (focal)", ACC), ("관계형 읽기 경로", INFO), ("구체화 뷰와 최적화", OK), ("부하 폭발·극단 케이스", WARN)])
d.save("02-01.chapter-overview.svg")
