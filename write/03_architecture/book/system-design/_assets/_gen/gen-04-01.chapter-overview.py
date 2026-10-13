# 타입 스펙: type-process — 알고리즘 다섯을 칸으로 세우고 줄마다 저장 · 판정 · 대가라는 같은 슬롯을 반복한다(주체가 없는 단계 지도 → Stage framework with semantic slots).
# 사실 출처: 추출본 v2.txt 957~1126행(다섯 알고리즘 · 매개변수 · 장단점), 1105~1112행(근사식 3 + 5 × 0.7 = 6.5), 1042~1052행(경계 10건). 버킷 크기 4 는 §3 예시, 큐 크기 3 은 §4 예시 값이다.
# Layout conventions: 행 이름 열 x=24, 알고리즘 칸 폭 152 · 간격 12(x=124 부터 stride 164), 머리 y=96 높이 48, 슬롯 줄 y=156·232·308 높이 64(stride 76). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 460
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01",
      "다섯 알고리즘이 요청을 세는 방식",
      "토큰 버킷은 토큰 수, 누출 버킷은 FIFO 큐, 고정 윈도는 창마다 카운터, 이동 윈도 로그는 타임스탬프, 이동 윈도 카운터는 카운터 둘을 저장하고 그 차이가 판정과 대가를 가른다.",
      "저장하는 상태가 다르면 판정과 대가가 갈린다")

X0, CW, STRIDE = 124, 152, 164
HY, HH = 96, 48
ROWS = (156, 232, 308)
RH = 64

HEADS = (("§3", "토큰 버킷"), ("§4", "누출 버킷"), ("§5", "고정 윈도 카운터"),
         ("§6", "이동 윈도 로그"), ("§7", "이동 윈도 카운터"))

CELLS = (
    # 저장
    (("토큰 수", "버킷 크기 4"), ("FIFO 큐", "큐 크기 3"), ("카운터 1개", "창마다"),
     ("타임스탬프", "요청마다 1개"), ("카운터 2개", "이전 · 현재 창")),
    # 판정
    (("토큰 1개 소비", "없으면 버림"), ("큐에 담기", "가득이면 버림"), ("카운터 + 1", "한도면 버림"),
     ("오래된 것 제거", "크기 ≤ 한도"), ("이전 창 × 겹침", "+ 현재 창")),
    # 대가
    (("값 두 개", "조정 어려움"), ("큐가 막히면", "최근 요청 거절"), ("경계에서", "한도 2배 통과"),
     ("거절 요청도", "저장 · 메모리"), ("균등 분포를", "가정한 근사")),
)

for i, (no, name) in enumerate(HEADS):
    x = X0 + STRIDE * i
    d.box(x, HY, CW, HH, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 18, no, 12, SOFT, MONO)
    d.t(x + CW / 2, HY + 38, name, 14, INK, KR, "middle", 600)

for r, tag in enumerate(("저장", "판정", "대가")):
    y = ROWS[r]
    d.t(24, y + 38, tag, 14, SOFT, KR, "start", 600)
    for i in range(5):
        x = X0 + STRIDE * i
        l1, l2 = CELLS[r][i]
        if r == 0:
            d.tone(x, y, CW, RH, INFO, 6, "12", 1.2)
            c = INFO
        elif r == 1:
            d.box(x, y, CW, RH, PAPER2, RULE, 1.0, 6)
            c = INK
        else:
            c = ACC if i == 2 else WARN
            d.tone(x, y, CW, RH, c, 6, "14" if i == 2 else "12", 1.4 if i == 2 else 1.2)
        d.t(x + CW / 2, y + 28, l1, 14, c, KR, "middle", 600)
        d.t(x + CW / 2, y + 50, l2, 13, MUTED, KR)

d.legend(H - 56, [("저장하는 상태", INFO), ("대가", WARN), ("경계 오차", ACC)])
d.save("04-01.chapter-overview.svg")
