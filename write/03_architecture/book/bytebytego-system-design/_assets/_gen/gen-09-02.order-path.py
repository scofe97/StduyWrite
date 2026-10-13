# 타입 스펙: type-sequence — 시장가 매수 2700 주 한 건이 브로커 → 게이트웨이 → 주문 관리자(위험 점검·잔고) → 시퀀서 → 매칭 엔진에서 체결되고, 체결이 시퀀서를 거쳐 같은 길로 돌아오는 왕복(레인 5, 항목 11).
# 사실 출처: ByteByteGo system-design-101 design-stock-exchange.md(커밋 b28380a, 게이트웨이의 검증·속도 제한·인증·정규화, 주문 관리자의 위험 점검과 잔고 확인, 시퀀서가 주문과 체결을 모두 줄 세움, 체결 둘),
#   호가창 그림의 수량(100.10: 200·400·1100·100, 100.11 의 첫 주문 900)과 2700 − 200 − 400 − 1100 − 100 − 900 = 0. 평균 체결가 100.1033 = (1800 × 100.10 + 900 × 100.11) ÷ 2700 은 직접 계산한 값이다.
# Layout conventions: 레인 5·폭 152·간격 194, 호출 한 건의 stride 56(라벨 y-9, 부라벨 y+17), 첫 메시지 y=192. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_09_02_seq import SeqKR

W, H = 1000, 832
d = SeqKR(W, H, "BYTEBYTEGO · 09-02 §1",
          "주문 한 건은 시퀀서를 지나 매칭 엔진에서 체결되고 같은 길로 돌아온다",
          "호가창 수량은 예시 값이고 평균 체결가 100.1033 은 가중평균으로 계산한 값입니다.",
          "호가창 수량은 예시 값이고 평균 체결가는 계산한 값입니다")
B, G, M, S, E = "브로커", "게이트웨이", "주문 관리자", "시퀀서", "매칭 엔진"
d.lanes([(B, "고객의 앱"), (G, "검증 · 속도 제한"), (M, "위험 점검 · 잔고"), (S, "순서 확정"), (E, "호가창")], 100, 152)
d.rails(H - 80)

Y0, ST = 192, 56
d.msg(B, G, "매수 2700 · 시장가", Y0 + 0 * ST, MUTED, "ar")
d.msg(G, M, "정규화한 주문", Y0 + 1 * ST, MUTED, "ar")
d.selfmsg(M, "위험 점검", Y0 + 2 * ST + 8, WARN, sub="잔고 확인")
d.msg(M, S, "주문 2700", Y0 + 3 * ST + 16, MUTED, "ar")
d.msg(S, E, "순서 확정 주문", Y0 + 4 * ST + 16, MUTED, "ar")
cx = d.LX[E]
d.chip(cx, Y0 + 5 * ST + 20, "100.10 에 1800 주", ACC, 13)
d.chip(cx, Y0 + 5 * ST + 52, "100.11 에 900 주", ACC, 13)
d.msg(E, S, "매수 쪽 체결 2700", Y0 + 6 * ST + 48, OK, "ok", dash="5 4", sub="평균 100.1033")
d.msg(S, M, "순서 확정 체결", Y0 + 7 * ST + 48, OK, "ok", dash="5 4")
d.msg(M, G, "체결 2700", Y0 + 8 * ST + 48, OK, "ok", dash="5 4")
d.msg(G, B, "체결 2700", Y0 + 9 * ST + 48, OK, "ok", dash="5 4")

d.legend(H - 56, [("주문", MUTED), ("점검", WARN), ("호가창 소진", ACC), ("체결", OK)])
d.save("09-02.order-path.svg")
