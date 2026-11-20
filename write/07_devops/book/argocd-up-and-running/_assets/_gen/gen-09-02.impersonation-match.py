# 09-02 §3 — impersonation 을 켜면 sync 는 프로젝트의 destinationServiceAccounts 를 위에서부터 훑어 대상 server·namespace 와 처음 맞는 서비스 계정을 고르고, 그 계정의 권한으로 클러스터를 호출한다. 일치하는 항목이 없으면 enforced 기본값(true)에서는 오류, false 에서는 컨트롤러 계정으로 진행한다.
# 본문 근거: 이 노트 ### 3 「Application Sync Impersonation」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 argocd-cm 의 application.sync.impersonation.enabled 를 "true" 로 바꿔 확인했다(컨트롤러 재시작 없이 적용되었다).
#            매핑이 없는 프로젝트의 sync 는 `no matching service account found for destination server https://kubernetes.default.svc and namespace …` 로 끝났다.
#            매핑은 있으나 서비스 계정에 권한이 없으면 dry run 단계에서 `User "system:serviceaccount:<네임스페이스>:<서비스 계정>" cannot get resource …` 로 Failed 였고, 네임스페이스와 서비스 계정이 아직 없어도 같은 forbidden 이었다.
#            Deployment 권한만 준 Role 에서는 ConfigMap 이 forbidden 이라 sync 전체가 Failed 였고 Deployment 도 만들어지지 않았다. ConfigMap 권한을 더하자 Succeeded 였다.
#            enforced 를 "false" 로 두고 매핑을 없앤 프로젝트는 컨트롤러 계정으로 sync 가 Succeeded 였다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/app-sync-using-impersonation.md("Configure enforcement behavior", "Configuring destination service accounts"), docs/operator-manual/argocd-cm.yaml.
# 타입 스펙: type-architecture — 왼쪽 요청에서 오른쪽 판정으로 가는 한 방향 흐름, 가운데 칸 아래로 갈라지는 일치 없음 두 가지.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 440
d = D(W, H, "ARGO CD UP AND RUNNING · 09-02 §3",
      "sync 가 서비스 계정을 고르는 길",
      "왼쪽의 sync 요청은 Application 의 대상 server 와 namespace 를 들고 온다. 가운데 칸이 프로젝트의 destinationServiceAccounts 를 위에서부터 훑어 처음 맞는 서비스 계정을 고른다. "
      "고른 계정의 권한으로 클러스터를 호출해 Role 이 허용하면 적용되고 허용하지 않으면 forbidden 으로 Failed 가 된다. 맞는 항목이 없으면 enforced 가 true 일 때는 오류, false 일 때는 컨트롤러 계정으로 진행한다.",
      "sync 의 권한은 고른 서비스 계정의 Role 까지입니다")

A_X, A_W = 24, 150
B_X, B_W = 214, 200
C_X, C_W = 454, 216
O_X, O_W = 708, 148
MID = 170
BOX_Y, BOX_H = 112, 116

# sync 요청
d.tone(A_X, BOX_Y, A_W, BOX_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, BOX_Y + 36, "sync 요청", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, BOX_Y + 64, "Application 의 대상", 12, MUTED)
d.t(A_X + A_W / 2, BOX_Y + 90, "server · namespace", 11.5, MUTED, MONO)

# 매칭
d.tone(B_X, BOX_Y, B_W, BOX_H, ACC, 6, "14", 1.4)
d.t(B_X + B_W / 2, BOX_Y + 36, "서비스 계정 매칭", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, BOX_Y + 64, "첫 일치 항목", 12, MUTED)
d.t(B_X + B_W / 2, BOX_Y + 90, "destinationServiceAccounts", 11.5, MUTED, MONO)

# 권한 대조
d.box(C_X, BOX_Y, C_W, BOX_H, PAPER2, RULE, 1.0)
d.t(C_X + C_W / 2, BOX_Y + 36, "그 계정의 권한 검사", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, BOX_Y + 64, "네임스페이스 안의 Role", 12, MUTED)
d.t(C_X + C_W / 2, BOX_Y + 90, "Role · RoleBinding", 11.5, MUTED, MONO)

# 결과
outs = [
    (BOX_Y - 6, OK, "적용", "Role 허용"),
    (BOX_Y + 64, BAD, "forbidden", "Role 에 없는 리소스"),
]
for y, c, t1, t2 in outs:
    d.tone(O_X, y, O_W, 58, c, 6, "14", 1.2)
    d.t(O_X + O_W / 2, y + 26, t1, 12.5, INK, KR, "middle", 600)
    d.t(O_X + O_W / 2, y + 46, t2, 11.5, MUTED)
    ty = y + 29
    d.path(f"M {C_X + C_W + 2} {MID} L {C_X + C_W + 18} {MID} L {C_X + C_W + 18} {ty} L {O_X - 2} {ty}", MUTED, 1.4, m="ar")

# 화살표
d.path(f"M {A_X + A_W + 2} {MID} L {B_X - 2} {MID}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} {MID} L {C_X - 2} {MID}", MUTED, 1.4, m="ar")

# 일치 없음 두 가지
RY, RH = 290, 62
d.t(B_X + B_W / 2, 270, "일치 없음", 11.5, WARN, KR, "middle", 600)
nomatch = [
    (60, 230, BAD, "오류", "no matching service account"),
    (330, 270, WARN, "컨트롤러 계정 사용", "enforced: false"),
]
for x, w, c, t1, t2 in nomatch:
    d.tone(x, RY, w, RH, c, 6, "14", 1.2)
    d.t(x + w / 2, RY + 28, t1, 12.5, INK, KR, "middle", 600)
    d.t(x + w / 2, RY + 49, t2, 11.5, MUTED, MONO)
ax = 60 + 115
bx = 330 + 135
d.path(f"M {B_X + 40} {BOX_Y + BOX_H + 2} L {B_X + 40} 258 L {ax} 258 L {ax} {RY - 2}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W - 40} {BOX_Y + BOX_H + 2} L {B_X + B_W - 40} 258 L {bx} 258 L {bx} {RY - 2}", MUTED, 1.4, m="ar")

d.legend(388, [("요청", INFO), ("매칭", ACC), ("권한 검사", PAPER2), ("적용", OK), ("거부", BAD), ("대체", WARN)])
d.save("09-02.impersonation-match.svg")
