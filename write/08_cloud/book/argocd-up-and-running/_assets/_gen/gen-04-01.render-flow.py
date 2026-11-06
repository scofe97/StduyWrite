# 04-01 §2 — Application 의 spec.source 가 가리키는 Git·Helm 저장소를 Repository Server 가 Helm·Kustomize·디렉터리 중 하나로 매니페스트로 만들고,
#            Application Controller 가 그 매니페스트를 spec.destination 이 가리키는 클러스터와 네임스페이스에 맞춘다.
# 본문 근거: 이 노트 ### 2 「템플릿 도구」.
# 검증 근거: kind v0.31.0 에 v3.6.1 을 설치하고 argocd-example-apps 의 guestbook(디렉터리)·helm-guestbook(Chart.yaml)·kustomize-guestbook(kustomization.yaml)
#            폴더와 podinfo 차트 6.17.0 을 각각 Application 으로 만들어 Synced 가 되는 것을 확인했고, helm ls -A 가 비어 있고 helm.sh/release.v1 Secret 이 0개인 것을 확인했다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/tool_detection.md("Helm if there's a file matching Chart.yaml", "Kustomize if there's a kustomization.yaml, kustomization.yml, or Kustomization",
#            "Otherwise it is assumed to be a plain directory application"), docs/user-guide/helm.md("Helm is only used to inflate charts with helm template"),
#            docs/operator-manual/config-management-plugins.md("The Argo CD repo server component is in charge of building Kubernetes manifests").
# 타입 스펙: type-architecture — 왼쪽 소스에서 오른쪽 대상으로 가는 한 방향 흐름, 가운데 칸에 렌더 경로 세 갈래.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 372
d = D(W, H, "ARGO CD UP AND RUNNING · 04-01 §2",
      "소스가 매니페스트가 되어 대상에 닿는 길",
      "왼쪽의 Git 저장소와 Helm 저장소는 Application 의 source 가 가리키는 곳이다. "
      "가운데의 Repository Server 는 폴더 안의 파일을 보고 Helm, Kustomize, 일반 디렉터리 가운데 하나로 매니페스트를 만든다. "
      "오른쪽의 Application Controller 는 그 매니페스트를 destination 이 가리키는 클러스터와 네임스페이스의 실제 상태와 비교한다.",
      "매니페스트를 만드는 곳은 Repository Server 하나입니다")

# 칸 좌표
AX, AW = 24, 190
BX, BW = 262, 240
CX, CW = 540, 170
DX, DW = 750, 106
BOX_Y, BOX_H = 116, 180
A_Y = (140, 226)
A_H = 70
MID_Y, MID_H = 166, 80   # C, D 칸

# 위쪽 필드 이름
d.chip(119, 104, "spec.source", INFO)
d.chip(803, 104, "spec.destination", INFO)

# 소스 두 칸
d.tone(AX, A_Y[0], AW, A_H, INFO, 6, "14", 1.1)
d.t(AX + AW / 2, A_Y[0] + 30, "Git 저장소", 12.5, INK, KR, "middle", 600)
d.t(AX + AW / 2, A_Y[0] + 53, "path 의 폴더", 11.5, MUTED)
d.tone(AX, A_Y[1], AW, A_H, INFO, 6, "14", 1.1)
d.t(AX + AW / 2, A_Y[1] + 30, "Helm 저장소", 12.5, INK, KR, "middle", 600)
d.t(AX + AW / 2, A_Y[1] + 53, "chart 와 버전", 11.5, MUTED)

# Repository Server 와 세 갈래
d.box(BX, BOX_Y, BW, BOX_H, SOFT + "0A", SOFT, 0.9, 8)
d.t(BX + 12, BOX_Y + 24, "Repository Server", 12, MUTED, KR, "start", 600)
rows = [("Helm 렌더", "Chart.yaml 이 있으면", ACC),
        ("Kustomize 렌더", "kustomization.yaml 이 있으면", ACC),
        ("디렉터리 YAML", "그 밖의 폴더", SOFT)]
for i, (title, sub, c) in enumerate(rows):
    y = BOX_Y + 36 + i * 46
    d.tone(BX + 12, y, BW - 24, 40, c, 6, "14", 1.2 if c == ACC else 1.1)
    d.t(BX + BW / 2, y + 17, title, 12, INK, KR, "middle", 600)
    d.t(BX + BW / 2, y + 33, sub, 11, MUTED)

# Application Controller, 대상
d.tone(CX, MID_Y, CW, MID_H, INFO, 6, "14", 1.4)
d.t(CX + CW / 2, MID_Y + 34, "Application Controller", 12.5, INK, KR, "middle", 600)
d.t(CX + CW / 2, MID_Y + 58, "실제 상태와 비교", 11.5, MUTED)
d.tone(DX, MID_Y, DW, MID_H, SOFT, 6, "14", 1.1)
d.t(DX + DW / 2, MID_Y + 34, "대상 클러스터", 12.5, INK, KR, "middle", 600)
d.t(DX + DW / 2, MID_Y + 58, "네임스페이스", 11.5, MUTED)

# 화살표
d.path(f"M {AX + AW + 2} {A_Y[0] + A_H / 2} L {BX - 2} {A_Y[0] + A_H / 2}", MUTED, 1.4, m="ar")
d.path(f"M {AX + AW + 2} {A_Y[1] + A_H / 2} L {BX - 2} {A_Y[1] + A_H / 2}", MUTED, 1.4, m="ar")
d.path(f"M {BX + BW + 2} {MID_Y + MID_H / 2} L {CX - 2} {MID_Y + MID_H / 2}", MUTED, 1.4, m="ar")
d.path(f"M {CX + CW + 2} {MID_Y + MID_H / 2} L {DX - 2} {MID_Y + MID_H / 2}", MUTED, 1.4, m="ar")

d.legend(330, [("소스", INFO), ("도구별 렌더 경로", ACC), ("일반 디렉터리와 대상", SOFT)])
d.save("04-01.render-flow.svg")
