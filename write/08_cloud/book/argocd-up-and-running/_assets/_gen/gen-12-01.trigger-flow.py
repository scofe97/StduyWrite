# 12-01 §5 — Git push 는 EventListener 가 받고, TriggerBinding 이 본문의 after 를 revision 으로 꺼내고, TriggerTemplate 이 PipelineRun 을 만든다.
#            PipelineRun 안에서 lint Task 다음에 동기화 Task 가 그 SHA 로 argocd app sync --revision 을 부른다.
# 본문 근거: 이 노트 ### 5 「Tekton Triggers 로 push 에서 PipelineRun 까지」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1, Tekton Pipelines v1.18.0, Triggers v0.37.2 를 설치해 확인했다.
#            after 를 담은 POST 는 HTTP 202 로 접수돼 PipelineRun(lint, sync)이 모두 Succeeded 였고, 자동 동기화를 끈 앱이 그 SHA 로 Synced 가 됐다.
#            본문이 {} 이면 202 인데 PipelineRun 은 없었고 EventListener 로그에 "$(body.after): after is not found" 가 남았다.
# 공식 근거: tektoncd/triggers v0.37.2 docs/eventlisteners.md, tektoncd/pipeline v1.18.0 docs/tasks.md·pipelines.md, argo-cd v3.6.1 argocd_app_sync.md.
# 타입 스펙: type-architecture — 위쪽 줄은 이벤트가 PipelineRun 이 되는 길, 아래쪽 상자는 PipelineRun 안에서 Argo CD 로 가는 길, 둘 다 왼쪽에서 오른쪽.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 12-01 §5",
      "push 에서 Argo CD 동기화까지",
      "위쪽 줄에서 Git push 이벤트가 EventListener 로 들어오면 TriggerBinding 이 본문의 after 값을 revision 으로 꺼내고 TriggerTemplate 이 그 값으로 PipelineRun 을 만든다. "
      "아래쪽 PipelineRun 안에서는 lint Task 가 먼저 돌고, 이어서 동기화 Task 가 프로젝트 역할 토큰으로 argocd app sync --revision 과 app wait --health 를 불러 Argo CD 에 그 SHA 를 동기화시킨다.",
      "검증을 통과한 SHA 만 Argo CD 에 닿습니다")

TOP_Y, TOP_H = 132, 92
A_X, A_W = 24, 118
B_X, B_W = 172, 160
C_X, C_W = 362, 200
D_X, D_W = 592, 264
MIDT = TOP_Y + TOP_H / 2

# 상단 줄
d.tone(A_X, TOP_Y, A_W, TOP_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, TOP_Y + 34, "Git push", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, TOP_Y + 60, "after = 새 SHA", 11.5, MUTED, MONO)

d.box(B_X, TOP_Y, B_W, TOP_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, TOP_Y + 30, "EventListener", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, TOP_Y + 54, "el-push-listener", 11.5, MUTED, MONO)
d.t(B_X + B_W / 2, TOP_Y + 76, "8080, 접수하면 202", 12, MUTED)

d.box(C_X, TOP_Y, C_W, TOP_H, PAPER2, RULE, 1.0)
d.t(C_X + C_W / 2, TOP_Y + 30, "TriggerBinding", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, TOP_Y + 54, "revision = $(body.after)", 11.5, MUTED, MONO)
d.t(C_X + C_W / 2, TOP_Y + 76, "본문에서 값 꺼냄", 12, MUTED)

d.box(D_X, TOP_Y, D_W, TOP_H, PAPER2, RULE, 1.0)
d.t(D_X + D_W / 2, TOP_Y + 30, "TriggerTemplate", 12.5, INK, KR, "middle", 600)
d.t(D_X + D_W / 2, TOP_Y + 54, "revision = $(tt.params.revision)", 11.5, MUTED, MONO)
d.t(D_X + D_W / 2, TOP_Y + 76, "PipelineRun 을 만듦", 12, MUTED)

for x0, x1 in [(A_X + A_W, B_X), (B_X + B_W, C_X), (C_X + C_W, D_X)]:
    d.path(f"M {x0 + 2} {MIDT} L {x1 - 2} {MIDT}", MUTED, 1.4, m="ar")

# PipelineRun 컨테이너
PR_X, PR_Y, PR_W, PR_H = 172, 262, 474, 140
d.box(PR_X, PR_Y, PR_W, PR_H, PAPER2, RULE, 1.0)
d.t(PR_X + 18, PR_Y + 26, "PipelineRun", 12.5, INK, KR, "start", 600)
d.t(PR_X + PR_W - 18, PR_Y + 26, "revision = SHA", 11.5, MUTED, MONO, "end")

L_X, L_W, IN_Y, IN_H = 196, 126, 296, 76
d.box(L_X, IN_Y, L_W, IN_H, PAPER2, RULE, 1.0)
d.t(L_X + L_W / 2, IN_Y + 32, "lint", 12.5, INK, KR, "middle", 600)
d.t(L_X + L_W / 2, IN_Y + 56, "린트 Task", 12, MUTED)

S_X, S_W = 358, 270
d.tone(S_X, IN_Y, S_W, IN_H, ACC, 6, "14", 1.4)
d.t(S_X + S_W / 2, IN_Y + 26, "동기화 Task", 12.5, INK, KR, "middle", 600)
d.t(S_X + S_W / 2, IN_Y + 48, "app sync --revision <SHA>", 11.5, MUTED, MONO)
d.t(S_X + S_W / 2, IN_Y + 66, "app wait --health", 11.5, MUTED, MONO)

d.path(f"M {L_X + L_W + 2} {IN_Y + IN_H / 2} L {S_X - 2} {IN_Y + IN_H / 2}", MUTED, 1.4, m="ar")

# 템플릿 → PipelineRun
d.path(f"M {D_X + 40} {TOP_Y + TOP_H + 2} L {D_X + 40} {PR_Y - 2}", MUTED, 1.4, m="ar")

# Argo CD
AC_X, AC_W = 690, 166
d.tone(AC_X, IN_Y, AC_W, IN_H, OK, 6, "14", 1.2)
d.t(AC_X + AC_W / 2, IN_Y + 30, "Argo CD", 12.5, INK, KR, "middle", 600)
d.t(AC_X + AC_W / 2, IN_Y + 54, "역할 토큰: get·sync", 12, MUTED)
d.path(f"M {S_X + S_W + 2} {IN_Y + IN_H / 2} L {AC_X - 2} {IN_Y + IN_H / 2}", MUTED, 1.4, m="ar")
d.t(AC_X + AC_W / 2, IN_Y + IN_H + 22, "automated 정책은 꺼 둠", 11.5, MUTED)

d.legend(448, [("이벤트", INFO), ("변환·검사", PAPER2), ("실행", ACC), ("Argo CD", OK)])
d.save("12-01.trigger-flow.svg")
