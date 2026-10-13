# 타입 스펙: type-process — 미국 기업 A 가 한국 기업 B 에 USD 100 을 보낼 때 메시지는 네 은행·기관을 지나고 계좌 기록은 각자 다른 모양으로 바뀐다. 정산은 미국 안에서 한 번만 일어난다.
# 사실 출처: BIS Bulletin No 87 "Next generation correspondent banking"(2024-05-30) Graph 1.B — Firm A 의 예금 −USD 100, 연방준비 준비금 −USD 100 → 대리 은행 준비금 +USD 100,
#   B 은행의 nostro 계정 +USD 100, Firm B 의 예금 +KRW 120,000, 본문 "Settlement occurs only in the United States". USD 100 → KRW 120,000 은 그 글의 예시 환산 값이다.
# Layout conventions: 카드 폭 216·높이 164, 가로 stride 240(x=24+240k), 카드 y=124, 화살표는 카드 사이 24 간격. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 396
d = D(W, H, "BYTEBYTEGO · 07-01 §3",
      "국경을 넘는 돈은 메시지를 따라 은행 장부 네 곳이 차례로 바뀐다",
      "메시지는 은행을 따라 이어지지만 돈의 정산은 연방준비제도 장부 한 곳에서 일어납니다.",
      "USD 100 → KRW 120,000 은 BIS 가 든 예시 값입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y = 216, 164, 240, 24, 124
cards = [
    ("A 의 은행", "미국", "고객 예금", "−USD 100", "기업 A 의 예금 계좌", INFO),
    ("연방준비제도", "미국", "A 은행 준비금 −USD 100", "대리 은행 준비금 +USD 100", "정산이 일어나는 곳", ACC),
    ("대리 은행", "미국", "B 은행의 달러 계정", "+USD 100", "nostro 계정", INFO),
    ("B 의 은행", "한국", "고객 예금", "+KRW 120,000", "기업 B 의 예금 계좌", OK),
]
for k, (name, where, l1, l2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(cx, Y + 28, name, 13, c if c == ACC else INK, _kr(name), "middle", 600)
    d.t(x + CW - 12, Y + 28, where, 12, SOFT, KR, "end")
    d.line(x + 12, Y + 44, x + CW - 12, Y + 44, RULE, 0.6)
    d.t(cx, Y + 80, l1, 12, MUTED, _kr(l1), "middle")
    d.t(cx, Y + 108, l2, 13, c if c == ACC else c, _kr(l2), "middle", 600)
    d.t(cx, Y + 144, sub, 12, MUTED, _kr(sub), "middle")
    if k < 3:
        d.arrow([(x + CW + 2, Y + CH / 2), (x + STRIDE - 4, Y + CH / 2)], MUTED, "ar", 1.4)

d.t(24, Y + CH + 36, "메시지가 장부 갱신을 조율", 12, MUTED, KR, "start")
d.t(W - 48, Y + CH + 36, "정산은 미국 안에서 한 번", 12, ACC, KR, "end", 600)

d.legend(H - 44, [("정산 장부", ACC), ("은행 장부 갱신", INFO), ("수취인 입금", OK)])
d.save("07-01.correspondent-process.svg")
