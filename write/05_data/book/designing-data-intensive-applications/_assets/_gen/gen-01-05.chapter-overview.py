# 01-05 개요 — 프라이버시 규제 준수에서 출발해 법과 설계의 충돌, 데이터 최소화 원칙, 1장 전체 네 트레이드오프 축을 아우르는 전체 지도.
# 사실 출처: 01-05 서두(L26~L28), §1(L33~L40), §2(L44~L56), §3(L62~L78), §4(L83~L93)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "01-05 · CHAPTER OVERVIEW", "법·규제와 1장 트레이드오프 종합 지도",
      "프라이버시 규제와 법적 권리, 잊힐 권리와 불변 로그의 설계 충돌, 데이터 최소화 원칙, 1장 전체의 네 트레이드오프 축을 조망한다.",
      "프라이버시 규제 · 법과 설계 기초 충돌 · 데이터 최소화 원칙 · 1장 네 트레이드오프 종합")

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "법·규제 준수", "프라이버시 통제권",
     [("개인 데이터 통제권", "GDPR · CCPA 권리 보장"),
      ("사회적 영향 인식", "정치 · 대출 · 자동화 결정"),
      ("다루는 사람의 책임", "윤리적 영향 고려 · 법 준수")],
     INFO),
    ("§2", "설계 기초 충돌", "삭제 권리 vs 불변 로그",
     [("잊힐 권리", "right to be forgotten"),
      ("append-only 로그", "불변 파일 한가운데 삭제"),
      ("파생 데이터셋", "ML 학습 데이터 삭제 과제")],
     ACC),
    ("§3", "데이터 최소화", "Datensparsamkeit",
     [("저장 위험 비용", "유출 · 벌금 · 안전 위험"),
      ("big data 대비", "투기적 저장 배제"),
      ("GDPR 의무 셋", "목적 한정 · 보관 기간 제한")],
     WARN),
    ("§4", "1장 트레이드오프", "정답이 하나가 아닌 네 축",
     [("운영 vs 분석", "기록 시스템 vs 파생 데이터"),
      ("클라우드 vs 셀프 호스팅", "저장과 연산을 분리"),
      ("분산 vs 단일 노드", "서두르지 않는 분산"),
      ("비즈니스 vs 사용자 권리", "법적 요구 구현은 아직 미정형")],
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
    d.chip(x + 28, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        n = len(items)
        STEP, IH, TY, BY = (64, 52, 22, 40) if n == 3 else (48, 42, 18, 34)
        iy = PY + 68 + j * STEP

        if is_focal and j == 1:
            d.tone(x + 8, iy, CW - 16, IH, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + TY, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + BY, bot_txt, 12, ACC, KR, "middle")
        elif is_focal:
            d.tone(x + 8, iy, CW - 16, IH, ACC, 6, "12", 1.0)
            d.t(x + CW / 2, iy + TY, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + BY, bot_txt, 12, MUTED, KR, "middle")
        elif i == 0 and j == 0:
            d.tone(x + 8, iy, CW - 16, IH, INFO, 6, "1A", 1.2)
            d.t(x + CW / 2, iy + TY, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + BY, bot_txt, 12, INFO, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 8, iy, CW - 16, IH, WARN, 6, "1A", 1.2)
            d.t(x + CW / 2, iy + TY, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + BY, bot_txt, 12, WARN, KR, "middle")
        elif i == 3 and j == 3:
            d.tone(x + 8, iy, CW - 16, IH, OK, 6, "1A", 1.2)
            d.t(x + CW / 2, iy + TY, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + BY, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 8, iy, CW - 16, IH, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + TY, top_txt, 12, INK, MONO if not any('가' <= c <= '힣' for c in top_txt) else KR, "middle", 600)
            d.t(x + CW / 2, iy + BY, bot_txt, 12, MUTED, MONO if not any('가' <= c <= '힣' for c in bot_txt) else KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [
    ("설계 기초 충돌 (focal)", ACC),
    ("프라이버시 규제", INFO),
    ("저장 위험과 최소화", WARN),
    ("1장 트레이드오프 종합", OK),
])
d.save("01-05.chapter-overview.svg")
