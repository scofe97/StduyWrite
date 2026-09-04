# a0-03 §6 토큰 하나가 인증서가 되기까지.
# 본문(부록 C.2.6 의 다섯 걸음): 서비스 어카운트 토큰이 프록시 컨테이너에 할당되고, 토큰과 CSR 이
#       istiod 로 가고, istiod 가 TokenReview API 로 토큰을 검증하고, 성공하면 인증서를 서명해
#       응답하고, 파일럿 에이전트가 Envoy SDS 로 그 인증서를 프록시에 설정한다.
# 타입 스펙: type-sequence — 참여자 사이 시간 순 주고받기가 논점이다. 레인 + 메시지, 상태는 칩으로.
#           축약: 규격에서 이탈한 한 걸음(TokenReview 를 CA 가 함)에 accent 를 걸어 표시한다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, KR, MONO

W, H = 1000, 640
d = Seq(W, H, "ISTIO IN ACTION · A0-03 §6",
        "쿠버네티스가 준 토큰이 SPIFFE 신원이 된다",
        "파드에 마운트된 서비스 어카운트 토큰에서 시작해 에이전트가 SPIFFE ID 를 만들고 CSR 에 담는다. "
        "CA 가 토큰을 검증한 뒤 서명하고, 에이전트가 SDS 로 인증서를 프록시에 넣는다.",
        "색이 붙은 걸음이 규격에서 이탈한 자리입니다 — 원래는 에이전트의 몫입니다")

d.lanes([("쿠버네티스", "API 서버"),
         ("파일럿 에이전트", "workload endpoint"),
         ("Istio CA", "workload API"),
         ("Envoy 프록시", "service proxy")], y0=104, lane_w=216)
d.rails(516)

d.msg("쿠버네티스", "파일럿 에이전트", "service account token", 196, MUTED, "ar", sub="파드에 마운트된 시크릿")
d.selfmsg("파일럿 에이전트", "SPIFFE ID 를 만든다", 252, MUTED, sub="페이로드를 디코딩해 조립")
d.msg("파일럿 에이전트", "Istio CA", "token + CSR", 316, MUTED, "ar", sub="URI 타입 SAN 에 넣어서")
d.msg("Istio CA", "쿠버네티스", "TokenReview", 372, ACC, "acc", sub="규격상 에이전트의 몫이었다")
d.msg("Istio CA", "파일럿 에이전트", "signed certificate", 436, MUTED, "ar", sub="검증에 성공했을 때")
d.msg("파일럿 에이전트", "Envoy 프록시", "SDS", 492, MUTED, "ar", sub="인증서와 키를 넣는다")

d.state("Envoy 프록시", "mTLS 가능", 552, INFO)

d.t(24, 580, "토큰의 페이로드는 고칠 수 없다 — 고치면 서명 검증에 실패한다", 11, SOFT, KR, "start")
d.legend(596, [("규격에서 이탈한 걸음", ACC), ("부트스트랩이 끝난 상태", INFO)])
d.save("a0-03.bootstrap-steps.svg")
