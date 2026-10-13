# 타입 스펙: type-dp-security-matrix — 격자 문법을 가격 레벨 × 큐 위치 행렬로 쓴다. 같은 호가창을 시장가 매수 2700 주가 들어오기 전과 뒤로 나란히 놓아 100.10 의 네 주문과 100.11 의 첫 주문이 사라지는 모양을 보인다(두 패널).
# 사실 출처: ByteByteGo 호가창 그림의 가격 레벨과 큐 수량(매도: 100.13 100·200, 100.12 600·900, 100.11 900·700·400, 100.10 200·400·1100·100 / 매수: 100.08 500·600·900, 100.07 100·700, 100.06 1100·400·300·200, 100.05 500·100),
#   같은 그림의 식 2700 − 200 − 400 − 1100 − 100 − 900 = 0, 최우선 매도 100.10 → 100.11 로 오름. 호가 차이 0.02 와 0.03 은 최우선 매도 − 최우선 매수(100.08)로 직접 계산한 값이다.
# Layout conventions: 패널 폭 452(왼쪽 x=12, 오른쪽 x=504), 가격 열 72, 큐 칸 폭 72·stride 76, 행 stride 40·높이 36, 매도 4행과 매수 4행 사이 간격 36. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 628
d = D(W, H, "BYTEBYTEGO · 09-02 §4",
      "시장가 매수 2700 주는 100.10 의 1800 주를 비우고 100.11 의 첫 주문 900 주를 채운다",
      "수량은 예시 호가창의 값이고 호가 차이는 직접 계산한 값입니다.",
      "수량은 예시 값이고 호가 차이 0.02 와 0.03 은 계산한 값입니다")

ASK = [("100.13", [100, 200]), ("100.12", [600, 900]), ("100.11", [900, 700, 400]), ("100.10", [200, 400, 1100, 100])]
BID = [("100.08", [500, 600, 900]), ("100.07", [100, 700]), ("100.06", [1100, 400, 300, 200]), ("100.05", [500, 100])]
ASK_AFTER = [("100.13", [100, 200]), ("100.12", [600, 900]), ("100.11", [700, 400]), ("100.10", [])]
CONSUMED = {("100.10", 0), ("100.10", 1), ("100.10", 2), ("100.10", 3), ("100.11", 0)}


def panel(px, title, ask, spread, best_ask, after):
    d.t(px, 100, title, 13, INK, KR, "start", 600)
    d.t(px, 132, "매도 호가", 13, MUTED, KR, "start")
    ya = 144
    for r, (price, qs) in enumerate(ask):
        y = ya + r * 40
        d.t(px + 64, y + 24, price, 13, INK, MONO, "end", 600)
        if not qs:
            d.o.append(f'<rect x="{px + 76}" y="{y}" width="72" height="36" rx="4" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 4"/>')
            d.t(px + 76 + 36, y + 24, "비움", 13, MUTED, KR, "middle")
        for k, q in enumerate(qs):
            x = px + 76 + k * 76
            hit = (not after) and (price, k) in CONSUMED
            c = ACC if hit else BAD
            d.o.append(f'<rect x="{x}" y="{y}" width="72" height="36" rx="4" fill="{c}22" stroke="{c}" stroke-width="{1.4 if hit else 1.0}"/>')
            d.t(x + 36, y + 24, str(q), 13, c if hit else INK, MONO, "middle", 600 if hit else 400)
        if price == best_ask:
            d.chip(px + 76 + 4 * 76 + 36, y + 18, "최우선", BAD, 13)
    ys = ya + 4 * 40
    d.t(px + 64, ys + 20, "호가 차이", 13, MUTED, KR, "end")
    d.t(px + 76, ys + 20, spread, 13, INK, MONO, "start", 600)
    d.t(px, ys + 44, "매수 호가", 13, MUTED, KR, "start")
    yb = ys + 56
    for r, (price, qs) in enumerate(BID):
        y = yb + r * 40
        d.t(px + 64, y + 24, price, 13, INK, MONO, "end", 600)
        for k, q in enumerate(qs):
            x = px + 76 + k * 76
            d.o.append(f'<rect x="{x}" y="{y}" width="72" height="36" rx="4" fill="{OK}22" stroke="{OK}" stroke-width="1.0"/>')
            d.t(x + 36, y + 24, str(q), 13, INK, MONO, "middle")
        if price == "100.08":
            d.chip(px + 76 + 4 * 76 + 36, y + 18, "최우선", OK, 13)


panel(12, "체결 전", ASK, "0.02", "100.10", False)
panel(504, "체결 뒤", ASK_AFTER, "0.03", "100.11", True)
d.arrow([(464, 228), (496, 228)], ACC, "acc", 1.6)
d.t(480, 212, "2700", 13, ACC, MONO, "middle", 600)
d.t(W / 2, 544, "2700 − 200 − 400 − 1100 − 100 − 900 = 0", 13, INK, MONO, "middle")
d.legend(H - 56, [("대기 중인 매도", BAD), ("대기 중인 매수", OK), ("체결되는 주문", ACC)])
d.save("09-02.order-book.svg")
