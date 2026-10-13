# 타입 스펙: type-process — 구매 한 건이 거래 계층에서 지시로 바뀌고, 청산 계층에서 은행 A·B 의 100 과 500 이 순액 400 으로 상계되며, 정산 계층에서 준비금 두 곳만 움직이는 세 층. 정보 흐름과 자금 흐름이 갈리는 자리.
# 사실 출처: 추출본 v1.txt 2950~3025행(Transaction/Payment and clearing/Settlement layer, pay-in 1.1~1.6, "Bank A owns Bank B $100 and Bank B owns bank A $500", 순액 Bank B pays Bank A $400), PDF 120·121쪽 그림과 본문.
#   BIS Bulletin No 87(2024-05-30) "the central bank settles the payment between intermediaries" (국내 결제의 정산 기관).
# Layout conventions: 층 3개, 층 머리 폭 144(x=24), 카드 폭 208·높이 84, 카드 stride 232(x=192+232k), 층 y=108·252·396 (stride 144), 층 사이 화살표는 수직. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 576
d = D(W, H, "BYTEBYTEGO · 07-01 §5",
      "은행 장부의 100 과 500 은 하루 끝에 준비금 400 한 번이 된다",
      "구매에서 이체 지시까지는 정보만 움직이고, 청산이 서로의 채무를 상계한 뒤에야 준비금이 움직입니다.",
      "금액은 단위 없는 달러 예시이며 결제 은행 이름은 A · B 로 줄였습니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


HX, HW, CX0, CSTR, CW, CH = 24, 144, 192, 232, 208, 84
layers = [
    (108, "거래 계층", "정보 흐름", INFO),
    (252, "결제·청산 계층", "정보 흐름", INFO),
    (396, "정산 계층", "자금 흐름", ACC),
]
for y, name, kind, c in layers:
    if c == ACC:
        d.tone(HX, y, HW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(HX, y, HW, CH, PAPER2, RULE, 0.9, 6)
    d.t(HX + HW / 2, y + 36, name, 13, ACC if c == ACC else INK, KR, "middle", 600)
    d.t(HX + HW / 2, y + 60, kind, 12, MUTED, KR, "middle")
    d.line(CX0 - 12, y - 8, W - 24, y - 8, RULE, 0.5)


def card(x, y, t, v, c=INFO, foc=False):
    if foc:
        d.tone(x, y, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + CW / 2, y + 32, t, 13, INK, _kr(t), "middle", 600)
    d.t(x + CW / 2, y + 60, v, 12, ACC if foc else c, _kr(v), "middle", 600)


Y1, Y2, Y3 = 108, 252, 396
# 거래 계층: 1.1 → 1.2 → 1.3
card(CX0 + 0 * CSTR, Y1, "Bob 의 구매", "1.1 Amazon 주문")
card(CX0 + 1 * CSTR, Y1, "이체 요청", "1.2 Amazon → PayPal")
card(CX0 + 2 * CSTR, Y1, "토큰으로 이체", "1.3 은행 B → 은행 A")
for k in range(2):
    x = CX0 + k * CSTR + CW
    d.arrow([(x + 2, Y1 + CH / 2), (x + CSTR - CW - 4, Y1 + CH / 2)], MUTED, "ar", 1.4)

# 결제·청산 계층: 명세 두 장 → 청산 기관
card(CX0 + 0 * CSTR, Y2, "은행 A 명세", "A 가 B 에게 100")
card(CX0 + 1 * CSTR, Y2, "은행 B 명세", "B 가 A 에게 500")
card(CX0 + 2 * CSTR, Y2, "청산 기관 상계", "순액 B → A 400", foc=True)
for k in range(2):
    x = CX0 + k * CSTR + CW
    d.arrow([(x + 2, Y2 + CH / 2), (x + CSTR - CW - 4, Y2 + CH / 2)], MUTED, "ar", 1.4)

# 정산 계층: 준비금 두 곳
card(CX0 + 1 * CSTR, Y3, "은행 B 준비금", "−400", WARN)
card(CX0 + 2 * CSTR, Y3, "은행 A 준비금", "+400", OK)
d.arrow([(CX0 + 1 * CSTR + CW + 2, Y3 + CH / 2), (CX0 + 2 * CSTR - 4, Y3 + CH / 2)], ACC, "acc", 1.6)

# 층 사이 화살표
xa = CX0 + 2 * CSTR + CW / 2
d.arrow([(xa, Y1 + CH + 2), (xa, Y2 - 4)], MUTED, "ar", 1.4)
d.arrow([(xa, Y2 + CH + 2), (xa, Y3 - 4)], ACC, "acc", 1.6)

d.legend(H - 44, [("정보 흐름", INFO), ("상계 결과", ACC), ("준비금 감소", WARN), ("준비금 증가", OK)])
d.save("07-01.netting-process.svg")
