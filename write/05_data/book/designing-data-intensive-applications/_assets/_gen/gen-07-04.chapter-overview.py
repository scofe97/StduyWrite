# 07-04 개요 — 보조 인덱스의 두 전략(로컬·글로벌)과 7장 종합(두 샤딩 축·세 과제) 전체 지도.
# 사실 출처: 07-04 본문 서두(L14~L16), §1(L26~L36), §2(L42~L54), §3(L58~L64), §4(L68~L88).
#   §1·§2 는 같은 보조 인덱스 질의의 두 전략이라 화살표로 잇지 않고 위 괄호로 묶어 §3(선택 기준)에 넘긴다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 118, 276
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "07-04 · CHAPTER OVERVIEW", "보조 인덱스와 7장 종합 전체 지도",
      "기본키 샤딩 경계를 따르지 않는 보조 인덱스의 두 전략과 7장 전체의 두 샤딩 축·세 운영 과제를 조망한다.",
      "로컬 보조 인덱스 · 글로벌 보조 인덱스 · 선택 기준 · 7장 종합 구조")

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "로컬 보조 인덱스", "샤드별 독립 인덱싱",
     [("단일 샤드 쓰기", "자기 샤드 인덱스만 갱신"),
      ("전 샤드 질의", "scatter/gather 발생"),
      ("꼬리 지연 증폭", "가장 느린 샤드 대기")],
     INFO),
    ("§2", "글로벌 보조 인덱스", "용어 분할 인덱스",
     [("단일 샤드 읽기", "인덱스 fan-out 방지"),
      ("다중 샤드 쓰기", "원자적 갱신엔 분산 트랜잭션"),
      ("비동기 갱신", "DynamoDB · 인덱스 stale")],
     ACC),
    ("§3", "로컬 vs 글로벌", "읽기·쓰기 비율 · 목록 길이",
     [("읽기 많음·목록 짧음", "글로벌 인덱스 유리"),
      ("쓰기 빈번·일관성 중요", "로컬 인덱스 단순"),
      ("두 조건 동시 검색", "포스팅 목록 교집합 비용")],
     WARN),
    ("§4", "7장 종합", "두 샤딩 축과 세 과제",
     [("두 샤딩 축", "키 범위 vs 해시 샤딩"),
      ("세 운영 과제", "라우팅·리밸런싱·보조 인덱스"),
      ("8장 분산 트랜잭션", "여러 샤드 동시 변경")],
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
        iy = PY + 68 + j * 66

        if is_focal and j == 0:
            d.tone(x + 12, iy, CW - 24, 54, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 42, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 0:
            d.tone(x + 12, iy, CW - 24, 54, INFO, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 42, bot_txt, 12, INFO, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 12, iy, CW - 24, 54, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 42, bot_txt, 12, WARN, KR, "middle")
        elif i == 3 and j == 2:
            d.tone(x + 12, iy, CW - 24, 54, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 42, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 42, bot_txt, 12, MUTED, KR, "middle")

# §1·§2 묶음 괄호 → §3
CX = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]
BYK = PY - 12
d.line(CX[0], PY - 2, CX[0], BYK, SOFT, 1.2)
d.line(CX[1], PY - 2, CX[1], BYK, SOFT, 1.2)
d.arrow([(CX[0], BYK), (CX[2], BYK), (CX[2], PY - 3)], SOFT, "soft", 1.2)
d.t((CX[0] + CX[1]) / 2, BYK - 6, "같은 질의의 두 전략", 11, SOFT, KR, "middle")

# §3 → §4 연결 화살표
for i in (2,):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("로컬 보조 인덱스", INFO), ("글로벌 보조 인덱스", ACC), ("선택 기준", WARN), ("7장 종합", OK)])
d.save("07-04.chapter-overview.svg")
