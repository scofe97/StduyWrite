# 02-01 §2 의도가 Envoy 설정으로 번역되는 경로.
# 본문: 저자는 같은 라우팅 규칙을 두 형태로 나란히 보인다. 운영자가 쓰는 쪽은 의도만 담고,
#       프록시가 받는 쪽은 클러스터 이름과 경로 접두사로 풀린다. 운영자가 아래쪽을 직접 쓰지 않는 것이 이 구조의 값이다.
# 라벨의 값은 원문 예제 그대로다 — x-dark-launch: v2 · outbound|80|v2|catalog.prod.svc.cluster.local.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 5(최대 12), coral 은 헤드라인 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 560
d = Seq(W, H, "ISTIO IN ACTION · 02-01 §2",
        "위쪽은 무엇을 원하는가, 아래쪽은 어떻게 할 것인가",
        "운영자는 의도만 적고 kubectl 로 적용한다. istiod 가 그것을 프록시마다 맞는 낮은 수준 설정으로 "
        "번역해 내려보낸다. 색이 붙은 자리가 번역이 일어나는 곳이고, 운영자는 그 결과물을 쓰지 않는다.",
        "Istio 설정이 CRD 라서 kubectl 로 적용·삭제하는 기존 습관이 그대로 통합니다")

d.lanes([("운영자", "VirtualService"),
         ("Kubernetes API", "CRD"),
         ("istiod", "control plane"),
         ("Envoy", "sidecar")], y0=104, lane_w=248)
d.rails(452)

d.msg("운영자", "Kubernetes API", "kubectl apply", 196, MUTED, "ar", sub="x-dark-launch: v2 -> subset v2")
d.msg("Kubernetes API", "istiod", "리소스 변경 통지", 260, MUTED, "ar", sub="networking.istio.io")
d.selfmsg("istiod", "낮은 수준으로 번역", 316, ACC, sub="cluster 이름과 prefix 로 푼다")
d.msg("istiod", "Envoy", "outbound|80|v2|catalog…", 380, ACC, "acc", sub="운영자가 쓰지 않는 형태")
d.selfmsg("Envoy", "라우팅 적용", 432, MUTED, sub="요청마다 헤더 확인")

d.t(20, 488, "저자는 같은 규칙을 두 형태로 나란히 보여 이 번역을 드러낸다", 11, SOFT, KR, "start")
d.legend(516, [("번역이 일어나는 자리", ACC)])
d.save("02-01.intent-translation.svg")
