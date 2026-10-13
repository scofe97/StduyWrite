# 타입 스펙: type-sequence — 같은 Idempotency-Key 를 단 요청 두 건에서 첫 요청은 PSP 청구까지 끝나 응답이 저장되고, 응답이 유실된 뒤의 재시도는 저장된 응답 200 만 돌려받는 왕복(레인 3, 항목 10).
# 사실 출처: IETF draft-ietf-httpapi-idempotency-key-header-07 §2.2(예시 키 8e03978e-40d5-43e8-bc93-6894a57f9324)·§2.4(지문)·§2.6(재시도는 이전 결과를 돌려준다),
#   Stripe 문서 Idempotent requests(첫 요청의 상태 코드와 본문을 저장하고 같은 키의 재시도에 그대로 돌려준다), 추출본 v1.txt 3414~3424행(키는 HTTP 헤더에 담는다).
#   200 은 예시 API 의 상태 코드, 10.00 USD 는 추출본 $10 예시다.
# Layout conventions: 레인 3·폭 200·간격 364, 호출 한 건의 stride 60(라벨 y-9, 부라벨 y+17), 첫 메시지 y=192, 구분선 뒤 +8. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_07_02_seq import SeqKR

W, H = 1000, 912
KEY = "8e03978e-40d5-43e8-bc93-6894a57f9324"
d = SeqKR(W, H, "BYTEBYTEGO · 07-02 §2",
          "같은 키의 두 번째 요청은 저장된 응답 200 만 돌려받는다",
          f"Idempotency-Key {KEY} 를 단 요청 두 건을 서버가 한 번만 처리합니다.",
          "금액과 상태 코드는 예시 API 의 값이고 키는 IETF 초안의 예시 값입니다")
C, S, K = "클라이언트", "결제 서버", "키 저장소"
d.lanes([(C, "client"), (S, "payment system"), (K, "key store")], 100, 200)
d.rails(H - 80)

Y0, ST = 192, 60
d.msg(C, S, "POST /payments", Y0 + 0 * ST, MUTED, "ar", sub=f"key {KEY}")
d.msg(S, K, "키 저장 · 처리 중", Y0 + 1 * ST, WARN, "warn", sub="본문 지문 함께 저장")
d.selfmsg(S, "PSP 청구 10.00 USD", Y0 + 2 * ST, MUTED, sub="청구 성공")
d.msg(S, K, "응답 저장", Y0 + 3 * ST, OK, "ok", sub="200 · 청구 완료")
d.msg(S, C, "200 응답 유실", Y0 + 4 * ST, BAD, "bad", dash="5 4", sub="클라이언트에 도착하지 않음 · 시간 초과")
d.divider(Y0 + 5 * ST - 4, "같은 요청을 같은 키로 다시 보냄", ACC)
d.msg(C, S, "POST /payments", Y0 + 6 * ST + 4, MUTED, "ar", sub=f"key {KEY}")
d.msg(S, K, "키 조회", Y0 + 7 * ST + 4, MUTED, "ar")
d.msg(K, S, "저장된 응답 200", Y0 + 8 * ST + 4, INFO, "info", dash="5 4")
d.msg(S, C, "200 · 저장된 응답", Y0 + 9 * ST + 4, OK, "ok", dash="5 4", sub="PSP 호출 없음")
d.state(S, "PSP 청구 1건 유지", Y0 + 10 * ST + 12, OK)

d.legend(H - 56, [("요청", MUTED), ("처리 중", WARN), ("저장·응답", OK), ("조회", INFO), ("유실", BAD), ("재시도 구분", ACC)])
d.save("07-02.idempotency-sequence.svg")
