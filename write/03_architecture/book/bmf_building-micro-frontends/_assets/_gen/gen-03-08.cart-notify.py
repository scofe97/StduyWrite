# 03-08 §5 — 서버 사이드에서도 남는 조각 사이 통신 (원문 Figure 3-23).
# 저자가 번호로 적은 세 단계를 그대로 옮긴다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1160, 588
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 03-08 §5",
        "장바구니에 담으면 체크아웃 조각이 자기를 고친다",
        "서버 사이드에서는 뷰 안 통신이 드물지만 아예 없지는 않다. 저자가 번호로 적은 세 단계를 그대로 옮겼다.",
        "가운데가 사용자 세션을 확인하는 백엔드이고 양쪽이 뷰 안의 두 조각입니다")

d.lanes([("상품 조각", "product"),
         ("백엔드", "user session"),
         ("체크아웃 조각", "check-out experience")], y0=104, lane_w=280)
d.rails(496)
d.msg("상품 조각", "백엔드", "add to cart", 210, MUTED, sub="사용자가 상품을 담는다")
d.state("백엔드", "session updated", 262, OK)
d.msg("상품 조각", "체크아웃 조각", "notify", 328, ACC, "acc", sub="새 상품이 담겼다고 알린다")
d.selfmsg("체크아웃 조각", "fetch cart", 400, MUTED, sub="갱신된 목록을 가져온다")
d.state("체크아웃 조각", "UI refreshed", 462, OK)
d.legend(520, [("조각 사이를 건너는 알림", ACC), ("조각이 스스로 하는 일", MUTED)])
d.save("03-08.cart-notify.svg")
print("h 필요:", 520 + 40, " 실제:", H)
