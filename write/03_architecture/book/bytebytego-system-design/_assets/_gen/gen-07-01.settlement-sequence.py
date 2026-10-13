# 타입 스펙: type-sequence — 청구 100.00 EUR 이 매입사·카드 네트워크를 거쳐 청산 기록이 되고, 발급사가 인터체인지(상한 0.30 EUR)를 뺀 순액을 매입사에 정산한 뒤 가맹점에 입금되는 왕복(레인 4, 메시지 5).
# 사실 출처: EU 규정 2015/751 제4조(신용카드 인터체인지 상한 거래액의 0,3 %) · 제5조(발급사가 받는 보수) · 제2조 (10)·(12) · 제7조 3항(승인과 청산 메시지는 분리), ECB OP131 3.1절(발급사가 대금 지급을 지시받고 인터체인지는 매입사가 발급사에 낸다),
#   미 연준 Regulation II 최종 규칙 76 FR 43394 배경 절(청산 메시지로 하루치 순 정산 위치 계산, 인터체인지 반영).
#   계산: 100.00 × 0.003 = 0.30 EUR, 100.00 − 0.30 = 99.70 EUR (상한 기준 순액, 실제 인터체인지는 더 낮을 수 있다). 100.00 EUR 과 신용카드 가정은 문서용 예시다.
#   입금 100.00 − 가맹점 수수료는 이 편의 단순화이며 실제 정산 방식은 계약마다 다르다.
# Layout conventions: 레인 4·폭 160·간격 256, 호출 한 건의 stride 68(라벨 y-9, 부라벨 y+17), 첫 메시지 y=204. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_07_01_seq import SeqKR

W, H = 1000, 676
d = SeqKR(W, H, "BYTEBYTEGO · 07-01 §2",
          "발급사의 정산 지출은 청구액에서 인터체인지를 뺀 값이다",
          "청구 100.00 EUR 의 청산 기록이 발급사까지 가고, 신용카드 상한 0.3% 를 기준으로 발급사의 순지출은 99.70 EUR 입니다.",
          "금액은 문서용 예시이고 인터체인지는 상한 0.3% 를 기준으로 계산했습니다")
MR, AQ, NW, IS = "가맹점", "매입사", "카드 네트워크", "발급사"
d.lanes([(MR, "payee"), (AQ, "acquirer"), (NW, "scheme"), (IS, "issuer")], 100, 160)
d.rails(H - 80)

Y0, S = 204, 68
d.msg(MR, AQ, "청구 100.00 EUR", Y0 + 0 * S, MUTED, "ar", sub="승인 때 보류된 금액")
d.msg(AQ, NW, "청산 기록 100.00 EUR", Y0 + 1 * S, MUTED, "ar")
d.msg(NW, IS, "청산 기록 100.00 EUR", Y0 + 2 * S, MUTED, "ar", sub="인터체인지 ≤ 0.30 EUR")
d.state(IS, "소지자 청구", Y0 + 3 * S, WARN)
d.msg(IS, AQ, "정산 99.70 EUR", Y0 + 4 * S, ACC, "acc", sub="100.00 − 0.30 (발급사 순지출)", dx=128)
d.msg(AQ, MR, "입금 100.00 EUR − 수수료", Y0 + 5 * S, OK, "ok", dash="5 4", sub="수수료(인터체인지 포함) 차감")

d.legend(H - 56, [("청구·청산 기록", MUTED), ("정산", ACC), ("소지자 청구", WARN), ("입금", OK)])
d.save("07-01.settlement-sequence.svg")
