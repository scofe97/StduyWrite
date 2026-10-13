# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 알고리즘 다섯, 열은 저장 · 메모리 · 몰린 요청 · 한계이고 칸 색이 강점(ok) · 조건부(warn) · 약점(bad)을 가른다.
# 사실 출처: 추출본 v2.txt 993~1000행(토큰 버킷 장단점), 1020~1027행(누출 버킷), 1053~1059행(고정 윈도), 1089~1094행(이동 윈도 로그), 1118~1126행(이동 윈도 카운터).
# Layout conventions: 알고리즘 이름 열 x=24 폭 200, 열 넷 폭 168 · 간격 8(x=240 부터 stride 176), 머리 y=96 높이 40, 줄 y=148 부터 stride 68 높이 60. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 560
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01 §8",
      "다섯 알고리즘은 메모리와 정확도를 맞바꾼다",
      "다섯 알고리즘 모두 메모리가 작지만 이동 윈도 로그만 요청마다 타임스탬프를 남겨 크고, 고정 윈도는 경계에서 한도의 두 배가 통과하며, 이동 윈도 카운터는 근사값을 쓴다.",
      "칸 색은 강점 · 조건부 · 약점")

X0, CW, STRIDE = 240, 168, 176
HY, RY, RS, RH = 96, 148, 68, 60

COLS = ("저장하는 것", "메모리", "몰린 요청", "한계 · 쓰임")
# 행: 이름, [(윗줄, 아랫줄, 색)] × 4
ROWS = (
    ("토큰 버킷", (("토큰 수", "", None), ("작음", "", OK), ("통 크기까지", "한꺼번에 통과", WARN), ("값 두 개", "조정 어려움", WARN))),
    ("누출 버킷", (("FIFO 큐", "", None), ("작음", "큐 크기만큼", OK), ("일정 속도로", "유출", OK), ("큐가 막히면", "최근 요청 거절", WARN))),
    ("고정 윈도 카운터", (("창마다 카운터", "", None), ("작음", "", OK), ("경계에서", "한도 2배 통과", ACC), ("창 끝 초기화가", "맞는 쓰임", OK))),
    ("이동 윈도 로그", (("타임스탬프", "전부", None), ("큼", "요청마다 하나", BAD), ("어느 구간도", "한도 이내", OK), ("거절 요청도", "저장", BAD))),
    ("이동 윈도 카운터", (("카운터 2개", "", None), ("작음", "", OK), ("이전 창 평균으로", "완화", OK), ("균등 분포를", "가정한 근사", WARN))),
)

for i, name in enumerate(COLS):
    x = X0 + STRIDE * i
    d.box(x, HY, CW, 40, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 26, name, 14, INK, KR, "middle", 600)

for r, (name, cells) in enumerate(ROWS):
    y = RY + RS * r
    d.t(24, y + 36, name, 14, INK, KR, "start", 600)
    for i, (a, b, c) in enumerate(cells):
        x = X0 + STRIDE * i
        if c is None:
            d.box(x, y, CW, RH, PAPER2, RULE, 1.0, 6)
            col = INK
        else:
            d.tone(x, y, CW, RH, c, 6, "14" if c == ACC else "12", 1.4 if c == ACC else 1.2)
            col = c
        if b:
            d.t(x + CW / 2, y + 26, a, 14, col, KR, "middle", 600)
            d.t(x + CW / 2, y + 48, b, 13, MUTED, KR)
        else:
            d.t(x + CW / 2, y + 36, a, 14, col, KR, "middle", 600)

d.legend(H - 56, [("강점", OK), ("조건부", WARN), ("약점", BAD), ("경계 오차", ACC)])
d.save("04-01.comparison-matrix.svg")
