# 09-01 §2 세 리소스가 요청 하나를 두고 나누어 맡는 일.
# 본문(저자 9.1.6 · 그림 9.3): PeerAuthentication 과 RequestAuthentication 이 자격 증명을 검증하고
#       거기서 꺼낸 값을 필터 메타데이터로 저장하며, AuthorizationPolicy 가 그 값으로 허용·거부를 정한다.
# 앞의 둘은 꺼내 놓기만 하고 판정은 세 번째가 한다 — 이 분업이 §7 의 함정과 이어진다.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 6(최대 12), coral 은 헤드라인 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 620
d = Seq(W, H, "ISTIO IN ACTION · 09-01 §2",
        "앞의 둘은 꺼내 놓고 판정은 뒤가 한다",
        "요청 하나가 세 필터를 차례로 지난다. 두 인증 필터가 자격 증명에서 값을 꺼내 필터 메타데이터에 "
        "쌓아 두고, 인가 필터가 그 값만 보고 판정한다. 색이 붙은 자리가 유일하게 요청을 막는 곳이다.",
        "인증 리소스만 걸어 두면 아무것도 막히지 않습니다")

d.lanes([("들어온 요청", "SVID + JWT"),
         ("PeerAuthentication", "peer authn filter"),
         ("RequestAuthentication", "jwt authn filter"),
         ("AuthorizationPolicy", "rbac filter")], y0=104, lane_w=250)
d.rails(520)

d.msg("들어온 요청", "PeerAuthentication", "상대 인증서 제시", 196, MUTED, "ar", sub="X.509 SVID")
d.selfmsg("PeerAuthentication", "principal 적재", 248, MUTED, sub="cluster.local/ns/…/sa/webapp")
d.msg("PeerAuthentication", "RequestAuthentication", "Authorization 헤더", 312, MUTED, "ar", sub="Bearer JWT")
d.selfmsg("RequestAuthentication", "requestPrincipal 적재", 364, MUTED, sub="iss/sub · claims")
d.msg("RequestAuthentication", "AuthorizationPolicy", "필터 메타데이터", 428, ACC, "acc", sub="이 연결의 신원")
d.selfmsg("AuthorizationPolicy", "허용 또는 거부", 486, ACC, sub="여기서만 요청이 막힌다")

d.t(20, 552, "토큰이 없어도 두 번째 필터는 요청을 통과시킨다 — 클레임이 비어 있을 뿐이다", 11, SOFT, KR, "start")
d.legend(576, [("판정이 일어나는 자리", ACC)])
d.save("09-01.resource-pipeline.svg")
