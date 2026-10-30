# 05-02 개요 — 표준 텍스트 형식의 결함에서 스키마 제약 모델과 필드명을 포함하는 이진 변형까지의 발전 축.
# 사실 출처: 본문 §1(L33~L43), §2(L50~L69), §3(L76~L84)
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
PH = 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "05-02 · CHAPTER OVERVIEW", "JSON·XML·이진 변형 전체 지도",
      "표준 텍스트 인코딩의 결함에서 출발해 스키마 제약 모델과 필드명을 데이터에 포함하는 이진 변형의 한계까지 세 절의 흐름을 잇는다.",
      "표준 텍스트 결함 · 스키마 제약 모델 · 이진 변형과 한계")

CW = 264
GAP = 16
X0 = 24

cards = [
    ("§1", "텍스트 형식의 결함", "표현과 정밀도 한계",
     [("2^53 초과 정수", "부동소수 정밀도 손실"),
      ("이진 문자열 미지원", "Base64 로 크기 약 1/3 증가"),
      ("그래도 데이터 교환엔 충분", "합의의 어려움이 효율보다 큼")],
     INFO),
    ("§2", "JSON Schema", "open vs closed 모델",
     [("open model (기본)", "정의 안 된 필드 허용"),
      ("closed model", "명시된 필드 외 거부"),
      ("금지된 것의 정의", "정의된 필드 제약 위반 검증")],
     WARN),
    ("§3", "JSON 이진 변형", "필드명 보존과 절감 한계",
     [("MessagePack 66B", "텍스트 JSON 81B 대비 소폭 절감"),
      ("스키마 규정 부재", "모든 필드명을 데이터에 포함"),
      ("공간 절감 한계", "스키마 기반이면 절반 바이트")],
     ACC),
]

FOCAL = 2

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
    d.t(x + CW / 2 + 14, PY + 26, title, 13.5, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64
        if is_focal and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 1 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif is_focal and j == 0:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, MONO if any(c in top_txt for c in "^") else KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("핵심 한계·절감율", ACC), ("형식 결함·교환", INFO), ("스키마 규칙·모델", WARN), ("실제 측정값", OK)])
d.save("05-02.chapter-overview.svg")
