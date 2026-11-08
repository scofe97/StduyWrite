# 14-01 §5 — Image Updater 는 레지스트리에서 새 태그를 찾아 ImageUpdater 리소스의 규칙으로 고른 뒤, argocd 방식은 Application 의 helm 매개변수를, git 방식은 Git 커밋을 고친다. 어느 쪽이든 Argo CD 가 동기화한다.
# 본문 근거: 이 노트 「Image Updater 설정과 write-back」「Image Updater 실습 관찰」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 과 Image Updater v1.4.0 을 설치해 argocd 방식을 관찰했다.
#            Application demo 의 spec.source.helm.parameters 에 image.name 과 image.tag=1.0.1 이 생겼고 Deployment 의 이미지가 1.0.1 이 되었다.
#            git 칸의 `.argocd-source-<app>.yaml` 은 update-methods.md 의 설명을 따랐다.
# 공식 근거: argocd-image-updater v1.4.0 docs/basics/update-methods.md, pkg/argocd/gitcreds.go.
# 타입 스펙: type-architecture — 왼쪽 레지스트리에서 오른쪽 클러스터로 가는 흐름, Image Updater 뒤에서 둘로 갈라지는 write-back.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 14-01 §5",
      "새 이미지 태그가 Application 에 반영되는 두 길",
      "Image Updater 는 레지스트리에서 새 태그를 찾고 ImageUpdater 리소스에 적은 전략으로 고른다. "
      "argocd 방식은 Application 의 helm 매개변수를 직접 고치고, git 방식은 추적 브랜치에 커밋한다. "
      "어느 길이든 Argo CD 가 바뀐 소스를 동기화해 Deployment 의 이미지를 바꾼다.",
      "태그 감시는 Image Updater 가, 동기화는 Argo CD 가 맡습니다")

A_X, A_W = 24, 156
B_X, B_W = 214, 196
C_X, C_W = 446, 232
D_X, D_W = 712, 144
TOP_Y, BOT_Y, RH = 150, 280, 104

d.tone(A_X, 172, A_W, 156, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, 210, "레지스트리", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, 240, "demo/app", 11.5, MUTED, MONO)
d.t(A_X + A_W / 2, 264, "1.0.0, 1.0.1", 11.5, MUTED, MONO)
d.t(A_X + A_W / 2, 292, "새 태그 도착", 12, MUTED)

d.box(B_X, 172, B_W, 156, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, 210, "Image Updater", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, 238, "ImageUpdater 리소스", 11.5, MUTED, MONO)
d.t(B_X + B_W / 2, 262, "updateStrategy: semver", 11.5, MUTED, MONO)
d.t(B_X + B_W / 2, 290, "약 2분마다 확인", 12, MUTED)

d.tone(C_X, TOP_Y, C_W, RH, OK, 6, "14", 1.4)
d.t(C_X + C_W / 2, TOP_Y + 30, "argocd 방식 (기본값)", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, TOP_Y + 58, "Application 리소스를 직접 수정", 12, MUTED)
d.t(C_X + C_W / 2, TOP_Y + 82, "helm.parameters: image.tag", 11.5, MUTED, MONO)

d.tone(C_X, BOT_Y, C_W, RH, WARN, 6, "14", 1.2)
d.t(C_X + C_W / 2, BOT_Y + 30, "git 방식", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, BOT_Y + 58, "추적 브랜치에 커밋", 12, MUTED)
d.t(C_X + C_W / 2, BOT_Y + 82, ".argocd-source-<app>.yaml", 11.5, MUTED, MONO)

d.tone(D_X, 190, D_W, 120, ACC, 6, "14", 1.2)
d.t(D_X + D_W / 2, 222, "Argo CD", 12.5, INK, KR, "middle", 600)
d.t(D_X + D_W / 2, 252, "소스 변경 감지", 12, MUTED)
d.t(D_X + D_W / 2, 276, "동기화", 12, MUTED)

d.path(f"M {A_X + A_W + 2} 250 L {B_X - 2} 250", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} 250 L 428 250 L 428 {TOP_Y + RH / 2} L {C_X - 2} {TOP_Y + RH / 2}", MUTED, 1.4, m="ar")
d.path(f"M 428 250 L 428 {BOT_Y + RH / 2} L {C_X - 2} {BOT_Y + RH / 2}", MUTED, 1.4, m="ar")
d.path(f"M {C_X + C_W + 2} {TOP_Y + RH / 2} L 695 {TOP_Y + RH / 2} L 695 236 L {D_X - 2} 236", MUTED, 1.4, m="ar")
d.path(f"M {C_X + C_W + 2} {BOT_Y + RH / 2} L 695 {BOT_Y + RH / 2} L 695 264 L {D_X - 2} 264", MUTED, 1.4, m="ar")

d.legend(448, [("레지스트리", INFO), ("Image Updater", PAPER2), ("리소스 수정", OK), ("Git 커밋", WARN), ("Argo CD", ACC)])
d.save("14-01.tag-writeback-flow.svg")
