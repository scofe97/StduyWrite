# 04-04 §2 — 장바구니 컴포넌트가 셸 헤더 안에 살면서도 자기 도메인을 지키는 흐름.
# 저자가 든 세 책임(노출 여부 · 담긴 개수 · 체크아웃 시작)을 시간축에 편다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1220, 660
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 04-04 §2",
        "장바구니는 셸 안에 살지만 셸의 것이 아니다",
        "셸이 노출 여부를 정하면 체크아웃 도메인이 셸로 샌다. 그래서 컴포넌트가 스스로 판단하고 스스로 개수를 가져온다.",
        "가운데 레인이 셸 헤더 안에 얹힌 장바구니 컴포넌트입니다")

d.lanes([("상품 조각", "catalog domain"),
         ("장바구니 컴포넌트", "check-out domain"),
         ("애플리케이션 셸", "shell")], y0=104, lane_w=300)
d.rails(568)
d.selfmsg("장바구니 컴포넌트", "checkVisibility(url)", 208, ACC,
          sub="노출 여부를 스스로 정한다")
d.selfmsg("상품 조각", "POST /cart", 274, MUTED, sub="백엔드에 상품을 담는다")
d.msg("상품 조각", "장바구니 컴포넌트", "emit(event)", 344, ACC, "acc",
      sub="이미터를 거쳐 담겼다고 알린다")
d.selfmsg("장바구니 컴포넌트", "GET /cart", 408, MUTED, sub="현재 담긴 개수를 가져온다")
d.state("장바구니 컴포넌트", "배지 갱신", 466, OK)
d.msg("장바구니 컴포넌트", "애플리케이션 셸", "navigate('/checkout')", 520, MUTED,
      sub="사용자가 누르면 URL 만 바꾼다")
d.state("애플리케이션 셸", "체크아웃 조각 로드", 560, OK)
d.legend(600, [("도메인이 셸로 새지 않게 하는 자리", ACC), ("컴포넌트가 스스로 하는 일", MUTED)])
d.save("04-04.cart-component.svg")
print("h 필요:", 600 + 40, " 실제:", H)
