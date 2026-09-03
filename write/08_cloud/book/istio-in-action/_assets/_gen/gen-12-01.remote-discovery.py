# 12-01 §3 istiod 가 상대 클러스터의 워크로드를 발견하는 경로 — 원문 그림 12.5 · 12.6.
# 본문(원문 12.2.2): Istio 는 설치할 때 istio-reader-service-account 라는 서비스 어카운트를 최소 권한으로
#       만들어 두고, 다른 컨트롤 플레인이 그것으로 인증해 서비스와 엔드포인트 같은 워크로드 정보를 조회할 수
#       있게 한다. 그 서비스 어카운트 토큰을 상대 클러스터에 넘겨 줘야 하며, 안전한 연결을 위한 인증서도 함께
#       넘긴다. istioctl 의 create-remote-secret 이 이 과정을 자동화한다.
#       저자는 API 서버에 요청을 보내는 것을 "일종의 초능력"이라 부르고, 리소스를 되돌릴 수 없는 상태로
#       만들 수도 있다고 적는다.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 6(최대 12), coral 은 한 곳.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 620
d = Seq(W, H, "ISTIO IN ACTION · 12-01 §3",
        "남의 클러스터를 읽으려면 남의 신원이 필요하다",
        "west 의 컨트롤 플레인이 east 의 워크로드를 알려면 east 가 발급한 서비스 어카운트 토큰을 들고 "
        "east 의 API 서버에 인증해야 한다. 색이 붙은 자리가 그 토큰이 west 로 건너오는 지점이다.",
        "저자는 API 서버에 요청을 보내는 것을 일종의 초능력이라 부릅니다")

d.lanes([("운영자", "istioctl"),
         ("east 클러스터", "API server"),
         ("west 의 istiod", "control plane"),
         ("west 의 프록시", "envoy")], y0=104, lane_w=216)
d.rails(524)

d.msg("운영자", "east 클러스터", "create-remote-secret", 196, MUTED, "ar", sub="reader 서비스 어카운트로")
d.msg("east 클러스터", "운영자", "토큰과 CA 데이터", 252, MUTED, "ar", sub="kubeconfig 형식")
d.msg("운영자", "west 의 istiod", "시크릿 적용", 316, ACC, "acc", sub="istio/multiCluster=true 라벨")
d.selfmsg("west 의 istiod", "라벨을 보고 등록", 372, MUTED, sub="Adding cluster_id=east-cluster")
d.msg("west 의 istiod", "east 클러스터", "서비스와 엔드포인트 조회", 436, MUTED, "ar", sub="토큰으로 인증")
d.msg("west 의 istiod", "west 의 프록시", "원격 엔드포인트 반영", 494, MUTED, "ar", sub="xDS")

d.t(24, 556, "primary-primary 에서는 이 과정을 양쪽으로 한 번씩 한다 — 서로가 서로를 읽어야 하기 때문이다", 11, SOFT, KR, "start")
d.legend(576, [("상대의 신원이 건너오는 지점", ACC)])
d.save("12-01.remote-discovery.svg")
