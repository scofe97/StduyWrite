# 타입 스펙: type-sequence — 가맹점이 매입사·카드 네트워크를 거쳐 발급사에 승인을 묻고 100.00 EUR 보류를 받은 뒤, 승인 유효 기간 안에 청구하는 왕복(레인 4, 메시지 8).
# 사실 출처: Stripe 문서 "Place a hold on a payment method"(authorize 는 금액을 보류하고, 유효 기간 안에 capture 하지 않으면 풀린다. 카드 비대면 고객 개시 거래 Visa·Mastercard 7일),
#   EU 규정 2015/751 전문 (29)(발급사가 거래를 승인한다)·제7조 3항(승인 메시지와 청산 메시지는 분리된다). 100.00 EUR 은 문서용 예시 금액이다.
# Layout conventions: 레인 4·폭 160·간격 256, 호출 한 건의 stride 68(라벨 y-9, 부라벨 y+17), 첫 메시지 y=204. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_07_01_seq import SeqKR

W, H = 1000, 868
d = SeqKR(W, H, "BYTEBYTEGO · 07-01 §2",
          "승인은 금액을 보류할 뿐이고 청구는 유효 기간 안에 따로 온다",
          "가맹점의 승인 요청 한 건이 발급사까지 왕복하고, 보류된 100.00 EUR 을 유효 기간 안에 청구합니다.",
          "금액은 문서용 예시이고 유효 기간은 카드 비대면 고객 개시 거래 기준입니다")
MR, AQ, NW, IS = "가맹점", "매입사", "카드 네트워크", "발급사"
d.lanes([(MR, "payee"), (AQ, "acquirer"), (NW, "scheme"), (IS, "issuer")], 100, 160)
d.rails(H - 80)

Y0, S = 204, 68
d.msg(MR, AQ, "승인 요청 100.00 EUR", Y0 + 0 * S, MUTED, "ar", sub="카드 정보 · 금액")
d.msg(AQ, NW, "승인 요청 전달", Y0 + 1 * S, MUTED, "ar", sub="발급사로 라우팅")
d.msg(NW, IS, "승인 요청 100.00 EUR", Y0 + 2 * S, MUTED, "ar")
d.state(IS, "100.00 EUR 보류", Y0 + 3 * S, WARN)
d.msg(IS, NW, "승인 응답", Y0 + 4 * S, OK, "ok", dash="5 4", sub="승인 또는 거절")
d.msg(NW, AQ, "승인 응답", Y0 + 5 * S, OK, "ok", dash="5 4")
d.msg(AQ, MR, "승인 · 보류 중", Y0 + 6 * S, OK, "ok", dash="5 4", sub="이 시점에 돈은 아직 안 움직임")
d.divider(Y0 + 7 * S - 8, "승인 유효 기간 안 · 비대면 고객 개시 7일", ACC)
d.msg(MR, AQ, "청구 100.00 EUR", Y0 + 8 * S - 12, ACC, "acc", sub="기한이 지나면 보류가 풀림")

d.legend(H - 56, [("요청", MUTED), ("응답", OK), ("보류", WARN), ("청구", ACC)])
d.save("07-01.auth-sequence.svg")
