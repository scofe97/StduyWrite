# 04-02.chapter-overview — 이 편을 "입력 줄 → 출력 줄 → 얼마나 → 누가 먼저 → 누가 정하나" 다섯 박자로 읽는 지도
# 카드의 절 번호·이름·한 줄·항목 셋은 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다.
# 타입 스펙: type-process — 단계마다 같은 의미 슬롯이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서다. 04-01.chapter-overview 와 같은 골격·stride 를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, INFO, KR, MONO

W, H = 1000, 406
X0, GAP, CARD_Y, CARD_H = 12, 16, 132, 196
N = 5
CARD_W = (W - 48 - X0 - GAP * (N - 1)) / N

d = D(W, H, "CHAPTER MAP · 04-02",
      "줄은 어디에 서고 누가 먼저 나가는가 — 다섯 박자로 읽는 지도",
      "04-02 편의 전체 구조. 줄이 서는 두 자리(입력·출력)에서 출발해 버퍼를 얼마나 둘지, 누가 먼저 나갈지를 거쳐 그 순서를 누가 정하느냐는 정책 물음에 닿는다.",
      lead="입력 줄 → 출력 줄 → 얼마나 둘까 → 누가 먼저 → 누가 정하나")

CARDS = [("§1", "입력 줄",   "패브릭이 느리면 선다", INFO, ["· N 배 빠르면 안 선다", "· HOL 블로킹", "· 58% 에서 발산"]),
         ("§2", "출력 줄",   "빨라도 생긴다",        INFO, ["· 출력 링크는 하나", "· 꼬리 버리기", "· AQM 선제 표시"]),
         ("§3", "얼마나 둘까", "버퍼는 소금이다",    ACC,  ["· RTT × C", "· 흐름 많으면 ÷√N", "· 버퍼블로트"]),
         ("§4", "누가 먼저", "규율 넷",              INFO, ["· FIFO · 우선순위", "· 라운드 로빈 · WFQ", "· 일 보존"]),
         ("§5", "누가 정하나", "기술에서 정책으로",  INFO, ["· 클래스는 ISP 가", "· 망 중립성", "· FCC 2015 → 2024"])]

for i, (tag, title, sub, c, bullets) in enumerate(CARDS):
    x = X0 + (CARD_W + GAP) * i
    cx = x + CARD_W / 2
    d.t(cx, 118, tag, 9, SOFT, MONO)
    d.tone(x, CARD_Y, CARD_W, CARD_H, c, 6, "10", 1.4)
    d.t(cx, 166, title, 14, c, KR, "middle", 600)
    d.line(x + 14, 182, x + CARD_W - 14, 182, f"{c}44", 0.9)
    d.t(cx, 206, sub, 12, INK)
    for j, b in enumerate(bullets):
        d.t(x + 12, 236 + j * 24, b, 12, MUTED, KR, "start")
    if i < N - 1:
        d.path(f"M {x+CARD_W+2} {CARD_Y+CARD_H/2} L {x+CARD_W+GAP-3} {CARD_Y+CARD_H/2}", MUTED, 1.4, m="ar")

d.t(W / 2, 350, "강조된 칸이 이 편의 한 줄입니다 — 버퍼는 소금 같아서 알맞으면 낫게 하고 많으면 못 먹게 합니다.", 12, MUTED)
d.legend(362, [("도입·전개", INFO), ("이 편의 한 줄", ACC)])
d.save("04-02.chapter-overview.svg")
