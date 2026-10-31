# 01-01 개요 — 운영 시스템에서 생성된 데이터가 분석 시스템으로 적재되고 환류되며 기록과 파생으로 나뉘는 전체 지도.
# 사실 출처: 01-01 서두(L18~L28), §1(L51~L57), §2(L72~L82), §3(L95~L114), §4(L140~L156), §5(L179~L185), §6(L194~L198), §7(L209~L214), §8(L220~L230), §9(L239~L243), §10(L250~L254)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 276
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "01-01 · CHAPTER OVERVIEW", "운영·분석 시스템과 기록·파생 데이터 전체 지도",
      "운영 시스템의 단건 point query에서 분석 적재, 실시간 환류, 기록과 파생 권위 구분으로 이어지는 흐름을 조망한다.",
      "운영 데이터 생성 · 분석 저장소 적재 · 실시간 분석과 환류 · 데이터 권위와 파생")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "데이터의 이동: 백엔드 입력 생성 → 분석용 복사본 적재 → 스트림·reverse ETL 환류 · 권위는 운영 쪽에 남음", 12, INK, KR, "middle", 600)

CW = 196
GAP = 12
X0 = 32

cards = [
    ("§1 ~ §3", "운영 데이터 생성", "백엔드와 OLTP 트랜잭션",
     [("프론트엔드·백엔드 §1", "모든 사용자 데이터 대리 관리"),
      ("운영 시스템 분리 §2", "데이터 생성 백엔드 서비스"),
      ("OLTP point query §3", "키로 소수 레코드 조회")],
     INFO),
    ("§4 · §5", "분석 시스템 적재", "웨어하우스와 데이터 레이크",
     [("ETL 파이프라인 §4", "추출·변환·적재 데이터 이동"),
      ("데이터 웨어하우스 §4", "읽기 전용 복사본·대량 집계"),
      ("데이터 레이크 §5", "원본 파일 보존·sushi 원칙")],
     OK),
    ("§6", "실시간 분석과 환류", "스트림 처리와 reverse ETL",
     [("이벤트 스트림 §6", "초 단위 빠른 실시간 대응"),
      ("reverse ETL §6", "분석 모델 운영 시스템 배포"),
      ("운영 피드백 §6", "운영과 분석의 경계 순환")],
     WARN),
    ("§7 ~ §10", "데이터 권위와 파생", "진실의 원천과 사본 갱신",
     [("기록 시스템 §7", "진실의 원천·최초 기록 정본"),
      ("파생 데이터 시스템 §8", "캐시·인덱스·재생성 가능"),
      ("도구 중립·갱신 §9·§10", "쓰임이 결정·변경 전파 통합")],
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

    # 절 헤더
    d.chip(x + CW / 2, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2, PY + 46, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 64, role, 11.5, SOFT, KR, "middle")
    d.line(x + 10, PY + 74, x + CW - 10, PY + 74, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 84 + j * 60

        if is_focal and j == 0:
            d.tone(x + 10, iy, CW - 20, 50, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 21, top_txt, 12.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, bot_txt, 11.5, ACC, KR, "middle")
        elif i == 0 and j == 2:
            d.tone(x + 10, iy, CW - 20, 50, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 21, top_txt, 12.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, bot_txt, 11.5, INFO, KR, "middle")
        elif i == 1 and j == 1:
            d.tone(x + 10, iy, CW - 20, 50, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 21, top_txt, 12.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, bot_txt, 11.5, OK, KR, "middle")
        elif i == 2 and j == 1:
            d.tone(x + 10, iy, CW - 20, 50, WARN, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 21, top_txt, 12.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, bot_txt, 11.5, WARN, KR, "middle")
        else:
            d.box(x + 10, iy, CW - 20, 50, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 21, top_txt, 12.5, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 39, bot_txt, 11.5, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 1, y), (x2 - 3, y)], SOFT, "soft", 1.3)

d.legend(LEG, [
    ("운영 생성 (OLTP)", INFO),
    ("분석 적재 (OLAP)", OK),
    ("실시간 환류", WARN),
    ("권위와 파생 (focal)", ACC),
])

d.save("01-01.chapter-overview.svg")
