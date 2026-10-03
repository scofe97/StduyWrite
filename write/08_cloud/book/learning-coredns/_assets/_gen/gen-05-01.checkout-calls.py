# 05-01 §1 — 결제 서비스 하나가 금액을 계산하려면 세 서비스의 주소가 필요하다.
# 본문 근거: 이 노트 §1 69줄(원서 5장 도입부 소매 애플리케이션 예의 요지 — 결제가 장바구니·카탈로그·배송비에서 값을 모은다).
#            원서 영문을 대조하지 못해 영문 인용은 싣지 않는다.
# 타입 스펙: type-architecture — 구성요소 넷과 호출 관계, 그리고 아직 비어 있는 주소가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 550
d = D(W, H, "LEARNING COREDNS · 05-01 §1",
      "결제 한 번에 세 곳의 주소가 필요하다",
      "결제 서비스는 장바구니에서 품목 목록을, 카탈로그에서 가격을, 배송비 서비스에서 배송료를 가져와야 "
      "최종 금액을 낸다. 호출 관계는 정해졌지만 각 상대의 IP 와 포트는 아직 비어 있다.",
      "붉은 글자가 아직 모르는 주소입니다")

d.box(40, 196, 220, 96, PAPER2, RULE, 1.0, 8)
d.t(150, 236, "결제 (Checkout)", 15, INK, KR, "middle", 600)
d.t(150, 262, "최종 금액을 계산", 12, MUTED, KR)

targets = [("장바구니", "품목 목록", 104), ("상품 카탈로그", "품목별 가격", 204), ("배송비", "배송료", 304)]
for name, what, y in targets:
    my = y + 40
    if my == 244:
        d.path(f"M 262 244 L 576 244", MUTED, 1.4, m="ar")
    else:
        d.path(f"M 262 244 L 420 244 L 420 {my} L 576 {my}", MUTED, 1.4, m="ar")
    d.t(498, my - 10, what, 12, MUTED, KR)
    d.box(580, y, 260, 80, PAPER2, RULE, 1.0, 8)
    d.t(600, y + 32, name, 14, INK, KR, "start", 600)
    d.t(600, y + 58, "IP ? · 포트 ?", 13, BAD, KR, "start")

d.tone(40, 400, 480, 60, ACC, 8, "12", 1.4)
d.t(60, 426, "세 곳의 IP 와 포트를 결제 서비스는 어떻게 아는가", 14, ACC, KR, "start", 600)
d.t(60, 448, "이 물음에 답하는 기능 · 서비스 디스커버리", 12, MUTED, KR, "start")

d.t(20, 494, "여섯 조각 · 프로필 · 카탈로그 · 장바구니 · 결제 · 배송비 · 지불", 13, MUTED, KR, "start")

d.legend(510, [("서비스 디스커버리가 답할 물음", ACC), ("아직 모르는 주소", BAD)])
d.save("05-01.checkout-calls.svg")
