# 03-01 §3 — Git 의 ConfigMap·Secret YAML 이 argocd 네임스페이스에 적용되면 API server 는 대개 즉시, 구성 요소 프로세스는 실행 인자를 재시작 뒤에 읽는다.
# 본문 근거: 이 노트 ### 3 「선언적 구성」.
# 검증 근거: kind v0.31.0 에서 argocd-cm 에 help.chatUrl 을 넣자 재시작 없이 GET /api/v1/settings 의 help 에 나타났고,
#            argocd-cmd-params-cm 에 server.log.format: json 을 넣었을 때는 argocd-server 를 rollout restart 한 뒤에야 로그가 JSON 으로 바뀌었다.
#            secret-type: repository 레이블을 단 Secret 을 적용하자 argocd repo list 에 저장소가 나타났고 Secret 을 지우자 사라졌다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/declarative-setup.md(Atomic configuration 표, part-of 레이블 경고, Manage Argo CD Using Argo CD),
#            server-commands/additional-configuration-method.md(argocd-cmd-params-cm 이 각 구성 요소의 플래그를 정한다),
#            argocd-cm.yaml(timeout.reconciliation 은 repo-server 와 application-controller 재시작 필요, 그래서 argocd-cm 은 대개 바로 반영),
#            manifests/install.yaml(Role argocd-server 와 argocd-application-controller 가 secrets·configmaps 를 읽고 argocd-repo-server 용 Role 은 없다).
# 타입 스펙: type-architecture — 한 방향 흐름과 반영 시점 구분.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 520
d = D(W, H, "ARGO CD UP AND RUNNING · 03-01 §3",
      "Git 의 설정 YAML 이 Argo CD 설정이 되는 길",
      "왼쪽의 Git 저장소에 둔 ConfigMap 과 Secret YAML 이 kubectl 이나 Application 동기화로 argocd 네임스페이스에 적용되는 흐름이다. "
      "네임스페이스 안에서 argocd-cm 은 대개 API server 가 바로 읽고, argocd-rbac-cm 과 Secret 도 API server 가 읽으며 Secret 은 application-controller 도 읽는다. "
      "argocd-cmd-params-cm 은 구성 요소 프로세스의 실행 인자가 된다.",
      "argocd-cm 은 대개 바로 읽히고 argocd-cmd-params-cm 은 재시작해야 읽힙니다")

PX, PW_, PY, PH = 410, 250, 100, 352
RX, RW = 710, 158
ROWS = [(140, "argocd-cm", "일반 설정 · 대개 바로 반영", ACC),
        (218, "argocd-rbac-cm", "RBAC 정책", INFO),
        (296, "Secret", "저장소·클러스터 자격 증명", INFO),
        (374, "argocd-cmd-params-cm", "실행 인자 · 재시작 후 반영", WARN)]
BH = 64

d.tone(24, 218, 150, 74, INFO, 6, "14", 1.1)
d.t(99, 249, "Git 저장소", 12.5, INK, KR, "middle", 600)
d.t(99, 272, "ConfigMap·Secret YAML", 11.5, MUTED, KR)
d.path("M 176 255 L 224 255", MUTED, 1.4, m="ar")

d.tone(226, 218, 150, 74, SOFT, 6, "14", 1.1)
d.t(301, 249, "적용", 12.5, INK, KR, "middle", 600)
d.t(301, 272, "kubectl · Application", 11.5, MUTED, KR)
d.path(f"M 378 255 L {PX - 2} 255", MUTED, 1.4, m="ar")

d.box(PX, PY, PW_, PH, SOFT + "0A", SOFT, 0.9, 8)
d.t(PX + 12, PY + 22, "argocd 네임스페이스", 12, MUTED, KR, "start", 600)
for y, name, sub, c in ROWS:
    d.tone(PX + 14, y, PW_ - 28, BH, c, 6, "14", 1.2 if c == ACC else 1.1)
    d.t(PX + PW_ / 2, y + 27, name, 12, INK, MONO)
    d.t(PX + PW_ / 2, y + 49, sub, 11.5, MUTED, KR)

# 목적지
d.tone(RX, 140, RW, 78 * 2 + BH, ACC, 6, "14", 1.4)
d.t(RX + RW / 2, 140 + 40, "API server", 13, INK, KR, "middle", 600)
d.t(RX + RW / 2, 140 + 64, "설정 화면 · API", 11.5, MUTED, KR)
d.tone(RX, 374, RW, BH + 14, WARN, 6, "14", 1.1)
d.t(RX + RW / 2, 374 + 27, "구성 요소 프로세스", 12, INK, KR, "middle", 600)
d.t(RX + RW / 2, 374 + 49, "실행 인자로 읽음", 11.5, MUTED, KR)
d.t(RX + RW / 2, 374 + 67, "컨트롤러는 Secret 도 읽음", 11.5, MUTED, KR)

for y, _, _, _ in ROWS:
    d.path(f"M {PX + PW_ - 12} {y + BH / 2} L {RX - 2} {y + BH / 2}", MUTED, 1.4, m="ar")
# Secret → application-controller (구성 요소 프로세스): API server 칸 옆 틈새로 꺾어 내려간다.
d.path(f"M {PX + PW_ - 12} 350 L 685 350 L 685 388 L {RX - 2} 388", MUTED, 1.4, m="ar")

d.legend(480, [("대개 바로 읽히는 설정", ACC), ("그 밖의 설정", INFO), ("재시작이 필요한 설정", WARN), ("경유", SOFT)])
d.save("03-01.declarative-config.svg")
