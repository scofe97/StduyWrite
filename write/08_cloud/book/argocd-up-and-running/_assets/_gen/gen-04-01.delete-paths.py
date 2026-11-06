# 04-01 §3 — Application 을 지우는 방법 다섯 가지가 대상 네임스페이스의 리소스를 남기거나 지운다.
#            finalizer 가 없는 삭제는 Application 만 지우고, resources-finalizer.argocd.argoproj.io 계열 finalizer 가 있는 삭제는 리소스를 연쇄 삭제한다.
# 본문 근거: 이 노트 ### 3 「수명 주기」의 삭제 부분.
# 검증 근거: kind v0.31.0 의 v3.6.1 에서 finalizer 없는 guestbook 을 kubectl 로 지우자 Deployment·Service 가 guestbook 네임스페이스에 남았고,
#            foreground finalizer 를 단 kustomize-guestbook 과 background finalizer 를 단 helm-guestbook 은 리소스까지 사라졌으며(끝 상태만 확인),
#            argocd app delete --cascade=false 는 리소스를 남기고 argocd app delete 는 리소스를 지웠다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/app_deletion.md("The default propagation policy for cascading deletion is foreground cascading deletion",
#            "When you invoke argocd app delete with --cascade, the finalizer is added automatically",
#            UI 절의 "Waits for all managed resources to be deleted before the Application is removed" 와 "The Application is removed immediately, and resources are deleted in the background").
# 타입 스펙: type-flowchart — 행마다 삭제 방법 → Argo CD 의 처리 → 리소스의 결과.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 452
d = D(W, H, "ARGO CD UP AND RUNNING · 04-01 §3",
      "Application 삭제가 리소스에 닿는 다섯 가지 길",
      "각 줄은 삭제 방법, Argo CD 의 처리, 대상 네임스페이스에 남는 리소스의 결과를 왼쪽에서 오른쪽으로 잇는다. "
      "finalizer 가 없거나 CLI 에서 cascade 를 끄면 Application 만 지워지고 리소스가 남는다. "
      "foreground finalizer, background finalizer, 기본 CLI 삭제는 리소스까지 지운다.",
      "finalizer 가 있어야 리소스까지 지워집니다")

C1X, C1W = 24, 360
C2X, C2W = 414, 222
C3X, C3W = 662, 194
Y0, RH, PITCH = 120, 44, 54

d.t(C1X, 106, "삭제 방법", 11, MUTED, KR, "start")
d.t(C2X, 106, "Argo CD 의 처리", 11, MUTED, KR, "start")
d.t(C3X, 106, "대상 네임스페이스", 11, MUTED, KR, "start")

ROWS = [
    ("kubectl delete", "finalizer 없음", "Application 만 삭제", "리소스 정리 없음", "리소스 남음", "관리하던 리소스 그대로", WARN),
    ("kubectl delete", "resources-finalizer.argocd.argoproj.io", "연쇄 삭제 · foreground", "리소스 삭제 뒤 Application 제거", "리소스 삭제됨", "Application 이 관리한 리소스", OK),
    ("kubectl delete", "resources-finalizer.argocd.argoproj.io/background", "연쇄 삭제 · background", "Application 제거 뒤 리소스 정리", "리소스 삭제됨", "Application 이 관리한 리소스", OK),
    ("argocd app delete", "기본값", "연쇄 삭제 · foreground", "CLI 가 finalizer 를 붙임", "리소스 삭제됨", "Application 이 관리한 리소스", OK),
    ("argocd app delete", "--cascade=false", "Application 만 삭제", "finalizer 를 붙이지 않음", "리소스 남음", "관리하던 리소스 그대로", WARN),
]
for i, (t1, s1, t2, s2, t3, s3, c3) in enumerate(ROWS):
    y = Y0 + i * PITCH
    d.tone(C1X, y, C1W, RH, INFO, 6, "14", 1.1)
    d.t(C1X + C1W / 2, y + 19, t1, 12, INK, MONO, "middle", 600)
    d.t(C1X + C1W / 2, y + 36, s1, 11, MUTED, MONO if s1.startswith(("resources", "--")) else KR)
    d.tone(C2X, y, C2W, RH, SOFT, 6, "14", 1.1)
    d.t(C2X + C2W / 2, y + 19, t2, 12, INK, KR, "middle", 600)
    d.t(C2X + C2W / 2, y + 36, s2, 11, MUTED)
    d.tone(C3X, y, C3W, RH, c3, 6, "14", 1.2)
    d.t(C3X + C3W / 2, y + 19, t3, 12, INK, KR, "middle", 600)
    d.t(C3X + C3W / 2, y + 36, s3, 11, MUTED)
    my = y + RH / 2
    d.path(f"M {C1X + C1W + 2} {my} L {C2X - 2} {my}", MUTED, 1.4, m="ar")
    d.path(f"M {C2X + C2W + 2} {my} L {C3X - 2} {my}", MUTED, 1.4, m="ar")

d.legend(412, [("삭제 방법", INFO), ("Argo CD 의 처리", SOFT), ("리소스가 남는 결과", WARN), ("리소스가 지워지는 결과", OK)])
d.save("04-01.delete-paths.svg")
