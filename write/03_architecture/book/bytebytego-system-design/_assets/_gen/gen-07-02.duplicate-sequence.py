# 타입 스펙: type-sequence — 클라이언트의 결제 요청 한 건이 서버와 PSP 에서 청구까지 끝났는데 응답만 사라지고, 같은 요청을 다시 보내면 PSP 가 두 번 청구하는 왕복(레인 3, 항목 8).
# 사실 출처: 추출본 v1.txt 3402~3412행(재시도는 최소 한 번을 보장, $10 결제가 네 번째 시도에서 성공), IETF draft-ietf-httpapi-idempotency-key-header-07 §1
#   (POST 가 시간 초과되면 클라이언트는 리소스가 만들어졌는지 모른다). 10.00 USD 는 위 $10 예시, 시간 초과 뒤 재전송과 청구 두 건은 이 도식의 설명용 시나리오다.
# Layout conventions: 레인 3·폭 200·간격 364, 호출 한 건의 stride 60(라벨 y-9, 부라벨 y+17), 첫 메시지 y=192. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_07_02_seq import SeqKR

W, H = 1000, 780
d = SeqKR(W, H, "BYTEBYTEGO · 07-02 §1",
          "응답이 사라지면 재시도는 같은 청구를 한 번 더 만든다",
          "서버는 10.00 USD 를 청구했지만 클라이언트는 그 사실을 몰라 같은 요청을 다시 보냅니다.",
          "예시 API 의 요청이고 금액은 문서용 예시이며 키가 없는 두 요청은 서버에서 구별되지 않습니다")
C, S, P = "클라이언트", "결제 서버", "PSP"
d.lanes([(C, "client"), (S, "payment system"), (P, "psp")], 100, 200)
d.rails(H - 80)

Y0, ST = 192, 60
d.msg(C, S, "POST /payments", Y0 + 0 * ST, MUTED, "ar", sub="10.00 USD · 키 없음")
d.msg(S, P, "청구 10.00 USD", Y0 + 1 * ST, MUTED, "ar")
d.msg(P, S, "청구 성공", Y0 + 2 * ST, OK, "ok", dash="5 4")
d.msg(S, C, "응답 유실", Y0 + 3 * ST, BAD, "bad", dash="5 4", sub="클라이언트에 도착하지 않음")
d.divider(Y0 + 4 * ST + 4, "클라이언트가 같은 요청을 다시 보냄", ACC)
d.msg(C, S, "POST /payments", Y0 + 5 * ST + 8, WARN, "warn", sub="10.00 USD · 키 없음")
d.msg(S, P, "청구 10.00 USD", Y0 + 6 * ST + 8, WARN, "warn")
d.state(P, "청구 2건 · 20.00 USD", Y0 + 7 * ST + 8, BAD)

d.legend(H - 56, [("요청", MUTED), ("성공", OK), ("재시도", WARN), ("유실·중복", BAD), ("재시도 구분", ACC)])
d.save("07-02.duplicate-sequence.svg")
