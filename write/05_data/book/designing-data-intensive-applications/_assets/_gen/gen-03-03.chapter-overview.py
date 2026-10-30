# 03-03 개요 — 분석용 데이터 웨어하우스의 세 스키마 관례(OBT·별 스키마·눈송이 스키마)를 정규화 축 위에 나란히 비교한다.
# 사실 출처: 본문 §1(별 스키마와 fact·dimension), §2(눈송이 스키마와 subdimension), §3(OBT와 비정규화 조인 사전 계산)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 104
CW, GAP, X0 = 264, 16, 28
CH = 296
AXIS_Y = PY
CARDS_Y = AXIS_Y + 44
SUMM_Y = CARDS_Y + CH + 16
SUMM_H = 40
LEG = SUMM_Y + SUMM_H + 24
H = LEG + 56

d = D(W, H, "03-03 · CHAPTER OVERVIEW", "분석용 스키마의 정규화 축과 세 가지 관례",
      "데이터 웨어하우스의 스키마는 정규화 정도에 따라 OBT(dimension 을 fact 에 접음), 별 스키마, 눈송이 스키마(더 정규화)로 나란히 놓인다. 별 스키마가 분석가에게 더 단순해 흔히 선호된다.",
      "정규화 수준에 따른 세 관례의 비교")

# 상단 정규화 축 안내 바
d.box(X0, AXIS_Y, W - X0 * 2, 32, PAPER2, RULE, 0.9)
d.t(X0 + 16, AXIS_Y + 20, "비정규화 (조인 최소화)", 12, WARN, KR, "start", 600)
# 중간 축: 텍스트 좌우로 화살표 선 배치
d.line(X0 + 176, AXIS_Y + 16, W / 2 - 116, AXIS_Y + 16, RULE, 1.2)
d.t(W / 2, AXIS_Y + 20, "정규화 수준 (Normalization)", 11, SOFT, MONO, "middle")
d.arrow([(W / 2 + 116, AXIS_Y + 16), (W - X0 - 180, AXIS_Y + 16)], SOFT, "soft", 1.2)
d.t(W - X0 - 16, AXIS_Y + 20, "정규화 (중복 최소화)", 12, INFO, KR, "end", 600)

# 세 카드: OBT (§3), 별 스키마 (§1, Focal), 눈송이 스키마 (§2)
cards = [
    {
        "x": X0,
        "sec": "§3 OBT",
        "title": "단일 넓은 테이블",
        "sub": "완전 비정규화 · One Big Table",
        "color": WARN,
        "focal": False,
        "items": [
            ("테이블 구조", "단일 테이블 1개 (fact + dimension)"),
            ("조인 방식", "조인 사전 계산 (precomputed)"),
            ("컬럼 구성", "dimension 정보를 접은 비정규화 컬럼"),
            ("쿼리 특성", "조인 없이 조회 · 때로 더 빠름"),
        ],
        "tradeoff": "저장 공간 증가 · 조인 제거",
        "tc": WARN,
    },
    {
        "x": X0 + CW + GAP,
        "sec": "§1 별 스키마",
        "title": "fact 와 dimension",
        "sub": "dimension 은 문자열 보관 · 흔히 선호",
        "color": ACC,
        "focal": True,
        "items": [
            ("테이블 구조", "중앙 fact + 둘러싼 dimension"),
            ("조인 방식", "fact → dimension 외래 키 1단계"),
            ("컬럼 구성", "fact 속성 + dimension 메타데이터"),
            ("쿼리 특성", "분석가에게 더 단순"),
        ],
        "tradeoff": "정규화는 덜 · 다루기는 단순",
        "tc": ACC,
    },
    {
        "x": X0 + (CW + GAP) * 2,
        "sec": "§2 눈송이 스키마",
        "title": "subdimension 분해",
        "sub": "높은 정규화 · snowflake",
        "color": INFO,
        "focal": False,
        "items": [
            ("테이블 구조", "fact → dimension → subdimension"),
            ("조인 방식", "외래 키 2단계 이상 다중 조인"),
            ("컬럼 구성", "브랜드 · 카테고리 별도 테이블 분리"),
            ("쿼리 특성", "분석가에게 별보다 덜 단순"),
        ],
        "tradeoff": "더 정규화 · 조인 계층 증가",
        "tc": INFO,
    },
]

for c in cards:
    x = c["x"]
    if c["focal"]:
        d.tone(x, CARDS_Y, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, CARDS_Y, CW, CH, PAPER2, c["color"], 1.1)

    # 절 번호 칩
    d.chip(x + CW / 2, CARDS_Y + 22, c["sec"], c["color"], 11)

    # 제목 및 부제
    d.t(x + CW / 2, CARDS_Y + 54, c["title"], 15, INK, KR, "middle", 600)
    d.t(x + CW / 2, CARDS_Y + 74, c["sub"], 12, c["color"], KR, "middle")

    # 구분선
    d.line(x + 16, CARDS_Y + 88, x + CW - 16, CARDS_Y + 88, RULE, 0.8)

    # 세부 항목
    for i, (label, val) in enumerate(c["items"]):
        iy = CARDS_Y + 106 + i * 34
        d.t(x + 16, iy, label, 12, SOFT, KR, "start", 600)
        d.t(x + 16, iy + 17, val, 12, INK, KR, "start")

    # 카드 하단 요약
    d.tone(x + 12, CARDS_Y + CH - 36, CW - 24, 26, c["tc"], 4, "18", 1.0)
    d.t(x + CW / 2, CARDS_Y + CH - 19, c["tradeoff"], 11, c["tc"], KR, "middle", 600)

# 하단 종합 요약 바
d.box(X0, SUMM_Y, W - X0 * 2, SUMM_H, PAPER2, RULE, 0.9)
d.t(X0 + 20, SUMM_Y + 24, "핵심 기준", 12, ACC, KR, "start", 600)
d.t(X0 + 84, SUMM_Y + 24, "분석 데이터는 바뀌지 않는 이력 · 비정규화의 일관성·쓰기 부담이 덜함", 12, MUTED, KR, "start")

d.legend(LEG, [("별 스키마 (focal)", ACC), ("더 정규화한 변형", INFO), ("더 비정규화한 변형", WARN)])
d.save("03-03.chapter-overview.svg")
