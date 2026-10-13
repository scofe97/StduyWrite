# 타입 스펙: type-process — 구매자 Bob 의 100 USD 가 PayPal 과 외환 제공 은행 E 를 지나 88 EUR 로 바뀌어 판매자 Alice 에게 닿는 여섯 단계. 같은 여덟 계좌를 단계마다 다시 그려 증감이 옮겨 가는 것을 값으로 보인다.
# 사실 출처: 추출본 v1.txt 2175~2230행(Step 1~6, 3.1~3.3·4.1~4.3), PDF 90쪽 그림 · 91쪽(100 USD → 88 EUR). 1 USD = 0.88 EUR 은 그 글의 예시 환율이다. 단계 5 의 출발 계좌는 PDF 90쪽 그림의 5번 화살표(은행 E 의 PayPal EUR 계좌 → 은행 P2)와 같다.
# Layout conventions: 라벨 열 x=24 폭 288, 단계 열 stride 108(x=324+108k, 셀 폭 100), 행 stride 40(y=132 부터 8행), 머리 행 y=88. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 548
d = D(W, H, "BYTEBYTEGO · 07-01 §4",
      "100 USD 는 환전 은행의 자금 풀에서 88 EUR 로 바뀐다",
      "단계마다 계좌 여덟 곳의 증감을 따라가면 달러는 풀에 쌓이고 유로는 풀에서 빠져나갑니다.",
      "환율 1 USD = 0.88 EUR 은 문서용 예시 값입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


LX, LW, CX0, CSTR, CWID = 24, 288, 324, 108, 100
Y_H, Y0, RS = 92, 140, 40
steps = ["1 지급", "2 환전 송금", "3 USD 매도", "4 EUR 매수", "5 EUR 수령", "6 입금"]
rows = [
    ("구매자 Bob · 은행 B", "USD", {1: -100}),
    ("PayPal · 은행 P1", "USD", {1: +100, 2: -100}),
    ("PayPal · 은행 E", "USD", {2: +100, 3: -100}),
    ("은행 E 자금 풀", "USD", {3: +100}),
    ("은행 E 자금 풀", "EUR", {4: -88}),
    ("PayPal · 은행 E", "EUR", {4: +88, 5: -88}),
    ("PayPal · 은행 P2", "EUR", {5: +88, 6: -88}),
    ("판매자 Alice · 은행 A", "EUR", {6: +88}),
]

for k, s in enumerate(steps):
    x = CX0 + k * CSTR
    foc = k in (2, 3)
    if foc:
        d.tone(x, Y_H - 4, CWID, 36, ACC, 4, "14", 1.4)
    else:
        d.box(x, Y_H - 4, CWID, 36, PAPER2, RULE, 0.9, 4)
    d.t(x + CWID / 2, Y_H + 19, s, 12, ACC if foc else INK, _kr(s), "middle", 600)

for r, (name, cur, ch) in enumerate(rows):
    y = Y0 + r * RS
    d.line(LX, y - 4, W - 24, y - 4, RULE, 0.5)
    d.t(LX, y + 20, name, 12, INK, KR, "start")
    d.t(LX + LW - 8, y + 20, cur, 12, SOFT, MONO, "end", 600)
    for step, v in ch.items():
        x = CX0 + (step - 1) * CSTR
        c = OK if v > 0 else WARN
        d.tone(x + 8, y + 4, CWID - 16, 28, c, 4, "18", 1.0)
        d.t(x + CWID / 2, y + 23, f"{'+' if v > 0 else '−'}{abs(v)}", 13, c, MONO, "middle", 600)

d.line(LX, Y0 + 8 * RS - 4, W - 24, Y0 + 8 * RS - 4, RULE, 0.5)
d.t(LX, Y0 + 8 * RS + 24, "열 합계 USD 0 · EUR 0", 12, MUTED, KR, "start")
d.t(CX0 + 2 * CSTR + CWID, Y0 + 8 * RS + 24, "환전은 3 · 4 단계 한 곳", 12, ACC, KR, "middle", 600)

d.legend(H - 44, [("증가", OK), ("감소", WARN), ("환전 단계", ACC)])
d.save("07-01.forex-grid.svg")
