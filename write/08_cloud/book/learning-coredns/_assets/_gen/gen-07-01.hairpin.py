# 07-01 §2 — 클러스터 안에서 외부 이름을 부르면 트래픽이 나갔다 온다.
# 원문 근거: "when accessing the site from inside the cluster, we would rather not have the
#            request go to api.example.com, because that will cause traffic to hairpin: it will
#            exit the cluster, go back through the cloud load balancer, and finally come back
#            through the Kubernetes NodePort, where it likely will have yet another hop to get
#            to a pod that services the request. This all adds a lot of latency."
# 타입 스펙: type-architecture — 신뢰 경계(클러스터 안·밖)를 그리고 그 경계를 넘는 경로와
#           넘지 않는 경로를 대조한다. 연결선은 전부 축 정렬 직교 경로로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 610
d = D(W, H, "LEARNING COREDNS · 07-01 §2",
      "외부 이름으로 부르면 트래픽이 나갔다 온다",
      "같은 클러스터 안의 서비스를 api.example.com 으로 부르면 요청이 클러스터를 나가 "
      "로드밸런서와 NodePort 를 돌아 들어온다. 클러스터 이름으로 부르면 그대로 간다.",
      "빨강이 헤어핀, 초록이 rewrite 로 바꿔 놓은 경로입니다")

# 존 — 클러스터 경계 (먼저 그려 뒤에 깔린다)
d.box(20, 150, 520, 300, PAPER, "rgba(245,245,245,0.20)", 0.8, 8)
d.box(34, 154, 150, 14, PAPER, PAPER, 0)
d.t(38, 165, "KUBERNETES CLUSTER", 8, SOFT, MONO, "start")
d.box(700, 154, 108, 14, PAPER, PAPER, 0)
d.t(704, 165, "OUTSIDE", 8, SOFT, MONO, "start")

# 경로 — 상자보다 먼저 그린다
# 헤어핀: 파드 위로 나가 경계를 넘어 LB 로
d.path("M 170 200 L 170 120 L 720 120 L 720 196", BAD, 1.6, m="bad")
d.t(430, 110, "클러스터를 나간다", 11, BAD, KR)
# LB 에서 NodePort 로 되돌아 들어온다
d.path("M 620 228 L 454 228", BAD, 1.6, m="bad")
d.t(586, 218, "다시 들어온다", 11, BAD, KR)
# NodePort 에서 대상 파드로
d.path("M 375 256 L 375 376", BAD, 1.6, m="bad")
d.t(390, 320, "홉이 하나 더", 11, BAD, KR, "start")

# 직행: 파드 아래로 ClusterIP 를 거쳐 대상 파드로
d.path("M 125 256 L 125 376", OK, 1.6, m="ok")
d.path("M 200 408 L 296 408", OK, 1.6, m="ok")

# 노드
d.box(50, 200, 150, 56, PAPER2, RULE, 1.0)
d.t(125, 224, "클라이언트 파드", 13, INK, KR, "middle", 600)
d.t(125, 243, "같은 클러스터 안", 11, MUTED, KR)

d.box(300, 200, 150, 56, PAPER2, RULE, 1.0)
d.t(375, 224, "NodePort", 13, INK, MONO, "middle", 600)
d.t(375, 243, "노드 포트로 진입", 11, MUTED, KR)

d.box(50, 380, 150, 56, PAPER2, RULE, 1.0)
d.t(125, 404, "ClusterIP", 13, INK, MONO, "middle", 600)
d.t(125, 423, "kube-proxy 가 푼다", 11, MUTED, KR)

d.tone(300, 380, 150, 56, OK, 6, "12", 1.4)
d.t(375, 404, "대상 파드", 13, OK, KR, "middle", 600)
d.t(375, 423, "api 서비스", 11, OK, MONO)

d.tone(620, 200, 200, 56, BAD, 6, "12", 1.4)
d.t(720, 224, "클라우드 로드밸런서", 13, BAD, KR, "middle", 600)
d.t(720, 243, "인증서가 가리키는 이름", 11, BAD, KR)

# 아래 대조 밴드
d.box(20, 472, 840, 56, PAPER, RULE, 0.8)
d.t(36, 496, "api.example.com 으로 부르면", 11, BAD, KR, "start", 600)
d.t(36, 518, "api.example.svc.cluster.local 로 부르면", 11, OK, MONO, "start", 600)
d.t(320, 496, "경계를 두 번 넘고 홉이 하나 더 붙는다 — 지연이 크게 늘어난다", 11, MUTED, KR, "start")
d.t(320, 518, "클러스터 안에서 끝난다 — 다만 TLS 인증서 이름이 안 맞는다", 11, MUTED, KR, "start")

d.legend(548, [("헤어핀 경로", BAD), ("클러스터 안 직행", OK)])
d.save("07-01.hairpin.svg")
