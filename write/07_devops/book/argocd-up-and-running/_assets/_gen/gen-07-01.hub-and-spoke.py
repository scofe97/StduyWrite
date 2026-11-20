# 07-01 §1 — 허브 클러스터의 Application controller 가 cluster Secret 의 주소와 자격 증명으로 원격 클러스터의 API server 에 접속해 매니페스트를 밀어 넣는다(push 모델).
#            허브 자신인 in-cluster 는 Secret 없이 기본으로 등록되어 있다.
# 본문 근거: 이 노트 ### 1 「클러스터 정의와 허브 앤 스포크」.
# 검증 근거: kind v0.31.0(Kubernetes v1.35.0) 두 개에 Argo CD v3.6.1 을 허브에만 설치하고, 설치 직후 cluster Secret 이 없는데도 argocd cluster list 에 in-cluster 가 보임을 확인.
#            spoke 를 등록한 뒤 destination.name: spoke 인 Application 이 Synced/Healthy 가 되고 리소스가 spoke 의 네임스페이스에만 생김을 확인.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/declarative-setup.md("Cluster credentials are stored in secrets", 라벨 argocd.argoproj.io/secret-type: cluster),
#            docs/getting_started.md("https://kubernetes.default.svc should be used as the application's K8s API server address").
# 타입 스펙: type-architecture — 허브 안의 구성 요소와 바깥의 접속 대상.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 424
d = D(W, H, "ARGO CD UP AND RUNNING · 07-01 §1",
      "허브가 원격 클러스터로 밀어 넣는 길",
      "왼쪽의 허브 클러스터 안에서 Application 과 cluster Secret 이 Application controller 로 모이고, controller 가 오른쪽의 원격 클러스터 API server 로 접속한다. "
      "허브 자신인 in-cluster 는 Secret 없이 기본으로 등록되어 있다.",
      "연결은 허브에서 원격으로만 나갑니다")

HX, HY, HW, HH = 24, 100, 520, 250
d.tone(HX, HY, HW, HH, SOFT, 6, "10", 1.1)
d.t(HX + 16, HY + 26, "허브 클러스터 — Argo CD 가 설치된 곳", 13, INK, KR, "start", 600)

BX, BW, BH = 44, 190, 58
d.tone(BX, 150, BW, BH, INFO, 6, "14", 1.1)
d.t(BX + BW / 2, 150 + 24, "Application", 12.5, INK, MONO, "middle", 600)
d.t(BX + BW / 2, 150 + 44, "대상 이름 spoke", 11, MUTED)

d.tone(BX, 250, BW, BH, ACC, 6, "14", 1.4)
d.t(BX + BW / 2, 250 + 24, "cluster Secret", 12.5, INK, MONO, "middle", 600)
d.t(BX + BW / 2, 250 + 44, "argocd 네임스페이스", 11, MUTED)

CX, CW, CY, CH = 290, 230, 193, 66
d.tone(CX, CY, CW, CH, ACC, 6, "14", 1.4)
d.t(CX + CW / 2, CY + 27, "Application controller", 12.5, INK, MONO, "middle", 600)
d.t(CX + CW / 2, CY + 48, "저장된 자격 증명으로 접속", 11, MUTED)

d.arrow([(BX + BW + 2, 179), (262, 179), (262, 214), (CX - 2, 214)], MUTED)
d.arrow([(BX + BW + 2, 279), (262, 279), (262, 238), (CX - 2, 238)], MUTED)

d.tone(CX, 290, CW, 44, INFO, 6, "14", 1.1)
d.t(CX + CW / 2, 290 + 19, "in-cluster · Secret 없음", 12, INK, KR, "middle", 600)
d.t(CX + CW / 2, 290 + 35, "kubernetes.default.svc", 11, MUTED, MONO)
d.arrow([(CX + CW / 2, CY + CH + 2), (CX + CW / 2, 288)], MUTED)

SX, SY, SW, SH = 640, 140, 216, 140
d.tone(SX, SY, SW, SH, INFO, 6, "10", 1.1)
d.t(SX + SW / 2, SY + 28, "원격 클러스터", 13, INK, KR, "middle", 600)
d.tone(SX + 20, SY + 54, SW - 40, 64, INFO, 6, "14", 1.2)
d.t(SX + SW / 2, SY + 54 + 28, "API server", 12.5, INK, MONO, "middle", 600)
d.t(SX + SW / 2, SY + 54 + 48, "Secret 의 server 주소", 11, MUTED)

d.arrow([(CX + CW + 2, 226), (SX - 2, 226)], MUTED)
d.t((CX + CW + SX) / 2, 214, "push", 11.5, MUTED, MONO, "middle", 600)

d.legend(380, [("배포 대상 선언", INFO), ("접속 정보 · 실행", ACC), ("허브 안쪽 범위", SOFT)])
d.save("07-01.hub-and-spoke.svg")
