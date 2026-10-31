# 02-04 개요 — 부하를 기술하는 차원에서 출발해 세 확장 아키텍처 비교, 애플리케이션 고유 설계와 단순성 원칙으로 이어지는 전체 지도.
# 사실 출처: 02-04 서두(L21~L33), §1(L37~L57), §2(L59~L83), §3(L85~L99)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 260
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "02-04 · CHAPTER OVERVIEW", "확장성과 세 가지 아키텍처 전체 지도",
      "부하를 기술하는 차원(§1), 수직·수평 확장 아키텍처 비교(§2), 확장성 원칙과 단순성(§3)을 조망한다.",
      "부하 차원 정량화 · shared-nothing 선형 확장 잠재력 · 분해와 불필요한 복잡성 회피")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "확장성 설계 축: 부하 차원 기술 · 확장 아키텍처 비교 · 분해와 단순성 원칙", 12, INK, KR, "middle", 600)

CW = 248
GAP = 28
X0 = 40

cards = [
    ("§1", "부하 기술 차원", "부하 정량화와 선형 확장성",
     [("부하 측정 차원", "처리량 · 피크 · 읽기쓰기 비율"),
      ("두 가지 평가 시각", "성능 영향 분석 · 필요 자원 산정"),
      ("선형 확장성 기준", "자원 2배 투입 시 부하 2배 처리")],
     INFO),
    ("§2", "수직·수평 아키텍처", "세 구조와 선형 확장 잠재력",
     [("shared-memory", "수직 확장 · 비용 선형 초과"),
      ("shared-disk", "공유 디스크 · 락 경합 한계"),
      ("shared-nothing", "수평 분산 · 선형 확장 잠재력")],
     ACC),
    ("§3", "확장성 원칙", "애플리케이션 고유 설계",
     [("만능 아키텍처 부재", "magic scaling sauce 없음"),
      ("작은 부분으로 분해", "마이크로서비스 · 샤딩 분할"),
      ("불필요 복잡성 회피", "단일 머신 우선 · 실용적 절충")],
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
        iy = PY + 68 + j * 64

        if is_focal and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif is_focal and (j == 0 or j == 1):
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif i == 0 and j == 0:
            d.tone(x + 12, iy, CW - 24, 52, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, INFO, KR, "middle")
        elif i == 2 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("수평 확장 잠재력 (focal)", ACC), ("부하 기술 차원", INFO), ("공유 자원 한계", WARN), ("실용적 단순성", OK)])
d.save("02-04.chapter-overview.svg")
