# 14-01 개요 — 예측 분석과 알고리즘 감옥(§1), 편향과 차별(§2), 책임과 설명 가능성(§3), 피드백 루프와 시스템 사고(§4) 전체 지도.
# 사실 출처: 14-01 본문 서두(L16~L18), §1(L26~L33), §2(L36~L45), §3(L52~L61), §4(L64~L73), 원서 Ch.14 PDF p.2~3 Predictive Analytics, p.3 Bias and Discrimination, p.4~5 Responsibility and Accountability, p.5~6 Feedback Loops
# 10-31 검증(cc-ddia-dverify14): 배너 INFO→중립(§3 범례 색과 겹침), 원서에 없는 '편향 세탁'·'악순환 차단'·'오류 구제' 를 본문 낱말로
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 96
BANNER_H = 44
CARD_Y = 160
CARD_H = 248
LEG = 432
H = LEG + 56

d = D(W, H, "14-01 · CHAPTER OVERVIEW", "예측 분석의 윤리 전체 지도",
      "사람에 대한 자동 예측 시스템이 과거 편향을 학습·증폭하고 자기강화 루프로 이어지는 구조와 시스템 사고.",
      "알고리즘 감옥 · 대리 변수와 편향 증폭 · 책임과 구제 · 피드백 루프와 시스템 사고")

# 상단 공통 전제 배너 (INFO 는 §3 범례 색이라 중립 박스로 둔다)
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 18, "사람에 대한 자동 결정 체계: 데이터 기반 예측 분석의 윤리적 쟁점", 13, INK, KR, "middle", 600)
d.t(W / 2, BANNER_Y + 34, "과거 외삽으로 차별 증폭 · 시스템 사고로 많은 결과 사전 예측", 12, MUTED, KR, "middle")

# 4개 컬럼 기하 (CW=196, GAP=16, X0=24)
CW = 196
GAP = 16
X0 = 24
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]

# 루트 배너 → 4개 카드 배선 버스
BUS_Y = 150
d.line(W / 2, BANNER_Y + BANNER_H, W / 2, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[3], BUS_Y, RULE, 1.2)
for i in range(4):
    d.line(cx[i], BUS_Y, cx[i], CARD_Y, ACC if i == 1 else RULE, 1.2)

cards = [
    ("예측 분석과 배제", "§1", [
        "개인 재범·대출·보험 예측",
        "조직의 거절 판정 누적",
        "알고리즘 감옥 사회 배제",
        "증거와 항소 기회 부재"
    ], WARN, False),
    ("편향과 차별 증폭", "§2", [
        "데이터 기반 규칙 추론",
        "보호 특성과 대리 변수 상관",
        "불투명한 패턴 · 편향 증폭",
        "사람의 도덕적 상상력 개입"
    ], ACC, True),
    ("책임과 설명 가능성", "§3", [
        "개인 이력 대 유사 집단 통계",
        "신용 점수와 예측 분석 대조",
        "대리 변수의 고정관념화",
        "개별 사례의 확률적 오류"
    ], INFO, False),
    ("피드백과 시스템 사고", "§4", [
        "추천 에코 챔버와 양극화",
        "신용 점수와 고용 하향 나선",
        "알고리즘 가격 담합 수렴",
        "상호작용 포함 전체 시스템"
    ], OK, False),
]

for i, (title, sec_chip, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, CARD_Y, CW, CARD_H, color, 6, "14", 1.4)
    else:
        d.box(x, CARD_Y, CW, CARD_H, PAPER2, RULE, 1.0)

    # 섹션 칩과 제목
    chip_x = x + 30
    d.chip(chip_x, CARD_Y + 22, sec_chip, color, 12, pad=5)
    d.t(x + CW / 2 + 16, CARD_Y + 26, title, 13, INK, KR, "middle", 600)
    d.line(x + 10, CARD_Y + 42, x + CW - 10, CARD_Y + 42, RULE, 0.8)

    # 4개 항목
    for j, it in enumerate(items):
        iy = CARD_Y + 62 + j * 44
        d.box(x + 8, iy - 13, CW - 16, 30, PAPER, RULE, 0.6, r=4)
        d.t(x + CW / 2, iy + 6, it, 12, INK if not is_focal else color, KR, "middle")

# 범례 (간결한 명사구로 우측 마진 여유 확보)
d.legend(LEG, [
    ("위험 분류 (§1)", WARN),
    ("편향 증폭 (§2 focal)", ACC),
    ("설명 책임 (§3)", INFO),
    ("시스템 사고 (§4)", OK)
])

d.save("14-01.chapter-overview.svg")
