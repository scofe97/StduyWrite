# 13-01 §4 — 컨트롤러 복제를 2개로 늘리면 관리 대상 클러스터가 샤드 0 과 1 에 나뉜다. Secret 이 없는 in-cluster 는 ID 가 비어 늘 샤드 0, 기본(legacy)은 Secret uid 를 해시해 고르고, 클러스터 Secret 의 shard 필드가 있으면 그 값으로 고정된다.
# 본문 근거: 이 노트 ### 4 「확장과 샤딩」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 StatefulSet 을 2 개로 늘린 뒤 argocd admin cluster stats 로 확인했다.
#            두 클러스터는 in-cluster 와 같은 클러스터를 노드 주소로 한 번 더 등록한 Secret(remote) 이다. 기본값에서 remote 는 샤드 1, in-cluster 는 샤드 0 이었고,
#            remote Secret 에 shard "0" 을 쓰자 stats 가 remote 를 샤드 0 으로 보였다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/high_availability.md (argocd-application-controller 절), argocd-cmd-params-cm.yaml (controller.sharding.algorithm).
# 타입 스펙: type-architecture — 왼쪽 클러스터에서 오른쪽 컨트롤러 샤드로 가는 배정, 실선은 기본 배정, 점선은 고정.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 392
d = D(W, H, "ARGO CD UP AND RUNNING · 13-01 §4",
      "클러스터가 샤드에 나뉘는 모양",
      "컨트롤러 StatefulSet 이 두 개로 뜨면 Pod 번호 0 과 1 이 각각 샤드가 된다. Secret 이 없는 in-cluster 는 늘 샤드 0 이고, "
      "Secret 으로 등록한 클러스터는 기본 알고리즘이 uid 해시로 샤드를 고른다. 클러스터 Secret 에 shard 값을 쓰면 그 샤드로 고정되며 점선이 그 배정이다.",
      "클러스터마다 처리하는 컨트롤러가 정해집니다")

CX, CW, BH = 24, 270, 64
SX, SW = 586, 270
Y0, Y1 = 130, 250
d.tone(CX, Y0, CW, BH, INFO, 6, "14", 1.1)
d.t(CX + 16, Y0 + 26, "in-cluster", 12.5, INK, KR, "start", 600)
d.t(CX + 16, Y0 + 48, "kubernetes.default.svc", 11.5, MUTED, MONO, "start")
d.tone(CX, Y1, CW, BH, INFO, 6, "14", 1.1)
d.t(CX + 16, Y1 + 26, "remote", 12.5, INK, KR, "start", 600)
d.t(CX + 16, Y1 + 48, "클러스터 Secret", 11.5, MUTED, KR, "start")

d.tone(SX, Y0, SW, BH, ACC, 6, "14", 1.4)
d.t(SX + 16, Y0 + 26, "샤드 0", 12.5, INK, KR, "start", 600)
d.t(SX + 16, Y0 + 48, "application-controller-0", 11.5, MUTED, MONO, "start")
d.tone(SX, Y1, SW, BH, ACC, 6, "14", 1.4)
d.t(SX + 16, Y1 + 26, "샤드 1", 12.5, INK, KR, "start", 600)
d.t(SX + 16, Y1 + 48, "application-controller-1", 11.5, MUTED, MONO, "start")

d.path(f"M {CX + CW + 2} {Y0 + 32} L {SX - 2} {Y0 + 32}", MUTED, 1.4, m="ar")
d.path(f"M {CX + CW + 2} {Y1 + 32} L {SX - 2} {Y1 + 32}", MUTED, 1.4, m="ar")
d.chip(440, Y0 + 14, "Secret 없음 → 0", MUTED)
d.chip(440, Y1 + 50, "uid 해시", MUTED)

VX = 500
d.path(f"M {CX + CW + 2} {Y1 + 16} L {VX} {Y1 + 16} L {VX} {Y0 + 52} L {SX - 2} {Y0 + 52}", WARN, 1.4, m="warn", dash="5 4")
d.chip(VX, 214, 'shard: "0"', WARN)

d.legend(330, [("클러스터", INFO), ("컨트롤러 샤드", ACC), ("shard 고정", WARN)])
d.save("13-01.shard-assign.svg")
