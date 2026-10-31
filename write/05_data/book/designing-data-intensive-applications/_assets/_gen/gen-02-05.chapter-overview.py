# 02-05 개요 — 지속적 유지보수 비용을 줄이는 세 원칙(운영성·단순성·발전성)과 2장 비기능 요구사항 종합의 전체 지도.
# 사실 출처: 02-05 서두(L20, L28~L32), §1(L36~L53), §2(L56~L72), §3(L75~L88), §4(L91~L104)
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

d = D(W, H, "02-05 · CHAPTER OVERVIEW", "유지보수성 전체 지도",
      "운영성과 자동화(§1), 단순성과 추상화(§2), 발전성과 비가역성(§3), 2장 종합(§4)의 흐름과 공통 해법을 조망한다.",
      "운영 체계와 자동화 적정선 · 추상화를 통한 복잡도 관리 · 비가역성 최소화 · 빌딩 블록 공통 해법")

# 상단 공통 전제 배너
d.tone(30, BANNER_Y, W - 60, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "소프트웨어 비용의 대부분은 지속적 유지보수: 운영성 · 단순성 · 발전성 세 원칙", 12, INK, KR, "middle", 600)

CW = 196
GAP = 12
X0 = 30

cards = [
    ("§1", "운영성과 자동화", "운영 팀 지원과 적정선",
     [("운영 팀 일상 지원", "모니터링과 관측성"),
      ("머신 독립과 자가 치유", "이해하기 쉬운 운영 모델"),
      ("자동화의 양날의 검", "엣지 케이스와 적정선")],
     INFO),
    ("§2", "단순성과 추상화", "복잡성 관리와 외관",
     [("진흙 공 위험 방지", "복잡성 절감과 버그 예방"),
      ("복잡도의 두 범주", "도구 진화에 따른 이동"),
      ("핵심 도구 추상화", "세부 은폐와 범용 재사용")],
     ACC),
    ("§3", "발전성과 비가역성", "변화 적응과 유연성",
     [("데이터 시스템 민첩성", "요구사항 진화 적응"),
      ("느슨한 결합과 단순함", "Agile · TDD · 리팩토링"),
      ("변화의 적 비가역성", "되돌릴 수 없으면 위험이 큼")],
     OK),
    ("§4", "2장 종합", "네 요구사항과 빌딩 블록",
     [("성능과 확장성", "신뢰성과 유지보수성"),
      ("공통 해법 빌딩 블록", "트랜잭션 · 인덱스 · 로그"),
      ("정답이 하나가 아님", "상황에 맞는 균형")],
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

        if is_focal and j == 2:
            d.tone(x + 8, iy, CW - 16, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 0:
            d.tone(x + 8, iy, CW - 16, 52, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, INFO, KR, "middle")
        elif i == 2 and j == 2:
            d.tone(x + 8, iy, CW - 16, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        elif i == 3 and j == 1:
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

d.legend(LEG, [("추상화 핵심 도구 (focal)", ACC), ("운영 체계와 자동화", INFO), ("변화 적응과 비가역성", OK), ("2장 요구사항 종합", WARN)])
d.save("02-05.chapter-overview.svg")
