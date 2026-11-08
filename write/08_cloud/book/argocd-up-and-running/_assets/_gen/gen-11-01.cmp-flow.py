# 11-01 §1 — repo-server 는 Application 의 plugin 설정과 소스 디렉터리를 유닉스 소켓으로 CMP 사이드카에 보내고, 사이드카가 init 과 generate 를 돌려 stdout 에 찍은 YAML 을 매니페스트로 돌려받는다. 플러그인이 맞지 않으면 내장 도구(Helm·Kustomize·Directory)로 넘어가거나 오류가 난다.
# 본문 근거: 이 노트 ### 1 「플러그인이 필요한 때와 CMP 의 구조」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 echo-demo 사이드카(discover.fileName 지정)를 붙여 확인했다.
#            사이드카 로그에 init 과 generate 가 한 번의 GenerateManifest 호출로 실행되었고, generate 의 stdout 이 매니페스트가 되었다.
#            discover 가 맞지 않는 소스에 plugin.name 을 지정하면 `could not find cmp-server plugin with name "…" supporting the given repository` 로 실패했다.
#            plugin 필드를 비운 Application 은 discover 가 맞는 플러그인이 없으면 내장 도구로 렌더되었다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/config-management-plugins.md, util/app/discovery/discovery.go L91-133, L159-221.
# 타입 스펙: type-architecture — 왼쪽 Application 에서 오른쪽 매니페스트로 가는 한 방향 흐름, repo-server 아래로 갈라지는 내장 도구 한 가지.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 11-01 §1",
      "매니페스트가 플러그인을 거쳐 나오는 길",
      "왼쪽의 Application 은 소스 경로와 plugin 설정을 가진다. 가운데 repo-server 가 소스 디렉터리를 유닉스 소켓으로 CMP 사이드카에 보낸다. "
      "사이드카는 init 과 generate 를 차례로 실행하고 generate 가 stdout 에 찍은 YAML 을 매니페스트로 돌려준다. "
      "plugin 이름이 없고 discover 가 맞는 플러그인도 없으면 repo-server 는 내장 도구인 Helm·Kustomize·Directory 로 렌더한다.",
      "플러그인은 repo-server 옆 사이드카이고 결과는 stdout 의 YAML 입니다")

A_X, A_W = 24, 150
B_X, B_W = 214, 200
C_X, C_W = 454, 216
O_X, O_W = 708, 148
MID = 235
BOX_Y, BOX_H = 164, 142

# Application
d.tone(A_X, BOX_Y, A_W, BOX_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, BOX_Y + 38, "Application", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, BOX_Y + 68, "소스 경로", 12, MUTED)
d.t(A_X + A_W / 2, BOX_Y + 92, "plugin.name", 11.5, MUTED, MONO)
d.t(A_X + A_W / 2, BOX_Y + 112, "plugin.env", 11.5, MUTED, MONO)

# repo-server
d.box(B_X, BOX_Y, B_W, BOX_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, BOX_Y + 38, "argocd-repo-server", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, BOX_Y + 68, "저장소 복제, 플러그인 고르기", 12, MUTED)
d.t(B_X + B_W / 2, BOX_Y + 96, "소스 디렉터리를 tar 로 전송", 12, MUTED)
d.t(B_X + B_W / 2, BOX_Y + 120, "plugins/<이름>[-<버전>].sock", 11.5, MUTED, MONO)

# CMP 사이드카
d.tone(C_X, BOX_Y, C_W, BOX_H, ACC, 6, "14", 1.4)
d.t(C_X + C_W / 2, BOX_Y + 38, "CMP 사이드카", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, BOX_Y + 66, "plugin.yaml 의 spec", 12, MUTED)
d.t(C_X + C_W / 2, BOX_Y + 94, "discover → init → generate", 11.5, MUTED, MONO)
d.t(C_X + C_W / 2, BOX_Y + 118, "generate 의 stdout = YAML", 11.5, MUTED, MONO)

# 결과
d.tone(O_X, 160, O_W, 70, OK, 6, "14", 1.2)
d.t(O_X + O_W / 2, 190, "매니페스트", 12.5, INK, KR, "middle", 600)
d.t(O_X + O_W / 2, 212, "YAML 여러 문서", 12, MUTED)
d.tone(O_X, 240, O_W, 70, BAD, 6, "14", 1.2)
d.t(O_X + O_W / 2, 270, "렌더 오류", 12.5, INK, KR, "middle", 600)
d.t(O_X + O_W / 2, 292, "종료 코드가 0 이 아님", 12, MUTED)
for ty in (195, 275):
    d.path(f"M {C_X + C_W + 2} {MID} L {C_X + C_W + 18} {MID} L {C_X + C_W + 18} {ty} L {O_X - 2} {ty}", MUTED, 1.4, m="ar")

# 화살표
d.path(f"M {A_X + A_W + 2} {MID} L {B_X - 2} {MID}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} {MID} L {C_X - 2} {MID}", MUTED, 1.4, m="ar")

# 내장 도구
DY, DH = 372, 62
d.tone(B_X, DY, B_W, DH, WARN, 6, "14", 1.2)
d.t(B_X + B_W / 2, DY + 28, "내장 도구", 11.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, DY + 49, "Helm, Kustomize, Directory", 11.5, MUTED)
d.path(f"M {B_X + B_W / 2} {BOX_Y + BOX_H + 2} L {B_X + B_W / 2} {DY - 2}", MUTED, 1.4, m="ar")
d.chip(B_X + B_W / 2 + 74, 340, "플러그인 없음", MUTED, 11)

d.legend(448, [("Application", INFO), ("repo-server", PAPER2), ("사이드카", ACC), ("성공", OK), ("실패", BAD), ("대체 경로", WARN)])
d.save("11-01.cmp-flow.svg")
