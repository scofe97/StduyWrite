# 02-03 개요 — 결함과 장애의 층위 구분에서 시작해 내결함성 시험, 하드웨어·소프트웨어·인간의 3대 결함 방어와 신뢰성의 사회적 책임으로 이어지는 전체 지도.
# 사실 출처: 02-03 서두(L21~L36), §1(L40~L48), §2(L55~L66), §3(L70~L90), §4(L94~L113), §5(L117~L137), §6(L141~L154).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, BAD, KR, MONO

W = 880
BANNER_Y = 100
BANNER_H = 34
Y0 = 152
PH = 216
GAP_Y = 28
Y1 = Y0 + PH + GAP_Y
LEG = Y1 + PH + 28
H = LEG + 56

d = D(W, H, "02-03 · CHAPTER OVERVIEW", "신뢰성과 내결함성 전체 지도",
      "결함과 장애의 층위(§1), 내결함성과 결함 주입(§2), 하드웨어(§3)·소프트웨어(§4)·사람(§5)의 결함 대처, 신뢰성의 사회적 영향(§6)을 조망한다.",
      "결함의 층위 격리 · 내결함 기계 시험 · 3대 결함 원인 방어 · 시스템 신뢰성 책임")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "신뢰성: 잘못되는 일이 생겨도 계속 올바르게 동작하는 것 · 결함을 막기보다 견디는 내결함성", 12, INK, KR, "middle", 600)

CW = 264
GAP_X = 20
X0 = 24

cards = [
    # Row 0: §1, §2, §3
    ("§1", "결함과 장애의 층위", "개념 구분과 층위의 차이",
     [("결함(fault) 정의", "특정 부분 동작 정지"),
      ("장애(failure) 정의", "시스템 전체 서비스 중단"),
      ("층위에 따라 달라짐", "사본을 둔 시스템엔 결함일 뿐")],
     INFO, False),
    ("§2", "내결함성과 결함 주입", "결함 견딤과 확신 확보",
     [("내결함성 목표", "특정 결함 허용치 서비스 지속"),
      ("SPOF 제거", "단일 장애점의 장애 확대 차단"),
      ("카오스 엔지니어링", "일부러 결함 주입해 기계 시험")],
     ACC, True),
    ("§3", "하드웨어 결함과 중복", "독립 고장과 컴포넌트 중복",
     [("독립 고장 특성", "디스크·RAM 등 컴포넌트 결함"),
      ("하드웨어 중복", "RAID · 이중 전원 컴포넌트"),
      ("소프트웨어 수준 고가용", "다중 가용 영역 · 롤링 업그레이드")],
     INFO, False),
    # Row 1: §4, §5, §6
    ("§4", "상관된 소프트웨어 결함", "공유 버그와 연쇄 실패",
     [("강한 결함 상관", "많은 노드의 동일 버그 공유"),
      ("휴면 버그와 가정 붕괴", "비정상 상황 발현 · 연쇄 실패"),
      ("소프트웨어 결함 완화", "프로세스 격리 · 재시작 허용")],
     WARN, False),
    ("§5", "사람의 실수와 포스트모템", "사회기술 시스템과 조직 학습",
     [("사회기술 시스템의 증상", "운영자 설정 변경이 장애 주원인"),
      ("기술적 조치", "테스트 · 롤백 · 모니터링 · 인터페이스"),
      ("무비난 포스트모템", "처벌 없는 전말 공유와 학습")],
     INFO, False),
    ("§6", "신뢰성의 중요성과 사건", "평범한 앱의 신뢰성과 오심",
     [("비즈니스·데이터 영향", "생산성 손실 · 영구 데이터 손실"),
      ("Horizon 버그 오심 사건", "회계 버그로 수백 명 유죄 판결"),
      ("영국법의 컴퓨터 가정", "반대 증거 없으면 올바르게 작동")],
     BAD, False),
]

for idx, (sec, title, role, items, card_c, is_focal) in enumerate(cards):
    row = idx // 3
    col = idx % 3
    x = X0 + col * (CW + GAP_X)
    y = Y0 if row == 0 else Y1

    # 카드 외곽
    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + 36, y + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 16, y + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, y + 45, role, 12, SOFT, KR, "middle")
    d.line(x + 12, y + 54, x + CW - 12, y + 54, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = y + 62 + j * 50
        if is_focal and j == 2:
            d.tone(x + 12, iy, CW - 24, 46, ACC, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 12, ACC, KR, "middle")
        elif idx == 0 and j == 2:
            d.tone(x + 12, iy, CW - 24, 46, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 12, INFO, KR, "middle")
        elif idx == 2 and j == 1:
            d.tone(x + 12, iy, CW - 24, 46, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 12, INFO, KR, "middle")
        elif idx == 3 and j == 0:
            d.tone(x + 12, iy, CW - 24, 46, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 12, WARN, KR, "middle")
        elif idx == 4 and j == 2:
            d.tone(x + 12, iy, CW - 24, 46, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 12, INFO, KR, "middle")
        elif idx == 5 and j == 1:
            d.tone(x + 12, iy, CW - 24, 46, BAD, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 12, BAD, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 46, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 18, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 12, MUTED, KR, "middle")

# 수평 연결 화살표 (Row 0: §1→§2, §2→§3)
d.arrow([(X0 + CW + 1, Y0 + PH / 2), (X0 + CW + GAP_X - 3, Y0 + PH / 2)], SOFT, "soft", 1.3)
d.arrow([(X0 + CW * 2 + GAP_X + 1, Y0 + PH / 2), (X0 + CW * 2 + GAP_X * 2 - 3, Y0 + PH / 2)], SOFT, "soft", 1.3)

# 수평 연결 화살표 (Row 1: §4→§5, §5→§6)
d.arrow([(X0 + CW + 1, Y1 + PH / 2), (X0 + CW + GAP_X - 3, Y1 + PH / 2)], SOFT, "soft", 1.3)
d.arrow([(X0 + CW * 2 + GAP_X + 1, Y1 + PH / 2), (X0 + CW * 2 + GAP_X * 2 - 3, Y1 + PH / 2)], SOFT, "soft", 1.3)

# 범례
d.legend(LEG, [
    ("내결함성 메커니즘 (focal)", ACC),
    ("개념·중복·학습 체계", INFO),
    ("상관 결함·연쇄 실패", WARN),
    ("영구 손실·사회적 피해", BAD)
])

d.save("02-03.chapter-overview.svg")
