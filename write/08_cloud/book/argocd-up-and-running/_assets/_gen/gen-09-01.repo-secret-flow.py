# 09-01 §3 — 보호된 저장소의 HTTPS 자격 증명은 argocd repo add 나 UI 가 argocd 네임스페이스에 저장소 Secret 으로 만든다. argocd-application-controller 와 argocd-server 가 그 Secret 을 읽어 요청에 담아 argocd-repo-server 에 넘기고, argocd-repo-server 는 넘겨받은 자격 증명으로 Git 저장소에 접속한다. Secret 이 없으면 authentication required 로 끝난다.
# 본문 근거: 이 노트 ### 3 「보호된 저장소의 HTTPS 자격 증명」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 기본 인증을 요구하는 Git 서버(스모크용 가짜 자격 증명)에서 확인했다.
#            저장소를 등록하기 전 Application 은 `authentication required` 로 실패했고, argocd repo add 로 등록하면 argocd 네임스페이스에 라벨 argocd.argoproj.io/secret-type=repository 를 단 Secret 이 생겼으며 refresh 뒤 Application 이 Synced 가 되었다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/private-repositories.md("HTTPS Username And Password Credential"),
#            docs/operator-manual/declarative-setup.md("Repositories"), docs/user-guide/commands/argocd_repo_add.md,
#            docs/operator-manual/security.md("Git & Helm Repositories": repo-server 는 Kubernetes 권한도 저장소 자격 증명도 갖지 않음),
#            docs/operator-manual/tls.md(repo-server 끝점은 argocd-server 와 argocd-application-controller 가 저장소 작업을 요청할 때 접근),
#            controller/state.go · server/application/application.go 의 db.GetRepository 호출.
# 타입 스펙: type-architecture — 왼쪽 등록에서 오른쪽 접속으로 가는 한 방향 흐름, 아래 가지는 실패.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 400
d = D(W, H, "ARGO CD UP AND RUNNING · 09-01 §3",
      "저장소 등록이 접속으로 이어지는 길",
      "왼쪽의 등록 명령이나 UI 가 저장소 주소와 사용자 이름과 토큰을 argocd 네임스페이스의 Secret 으로 만든다. 가운데에서는 argocd-application-controller 와 argocd-server 가 그 Secret 을 읽어 요청에 담아 argocd-repo-server 에 넘긴다. "
      "오른쪽에서는 argocd-repo-server 가 넘겨받은 자격 증명으로 Git 저장소에 HTTPS 로 접속한다. "
      "Secret 이 없는 상태에서 보호된 저장소를 가리키면 접속이 인증 단계에서 거절되어 authentication required 오류로 끝난다.",
      "등록한 Secret 이 접속의 열쇠다")

GAP = 30
Y = 124
RH = 108
# (너비, 색, 줄들[(글, 크기, 굵기, 글꼴, 색)])
cols = [
    (120, INFO, [("repo add 또는 UI", 12.5, 600, KR, INK), ("주소 · 사용자 · 토큰", 12, 400, KR, MUTED)]),
    (124, ACC, [("저장소 Secret", 12.5, 600, KR, INK), ("argocd 네임스페이스", 12, 400, KR, MUTED)]),
    (226, WARN, [("argocd-application-controller", 11, 600, MONO, INK), ("argocd-server", 11, 600, MONO, INK),
                 ("Secret 을 읽어 요청에 담음", 12, 400, KR, MUTED)]),
    (160, OK, [("argocd-repo-server", 12.5, 600, MONO, INK), ("넘겨받은 자격 증명으로 접속", 12, 400, KR, MUTED)]),
    (100, OK, [("Git 저장소", 12.5, 600, KR, INK), ("HTTPS 로 clone", 12, 400, KR, MUTED)]),
]

x = 15
xs = []
for w, c, lines in cols:
    xs.append((x, w))
    d.tone(x, Y, w, RH, c, 6, "14", 1.3)
    ys = (Y + 46, Y + 72) if len(lines) == 2 else (Y + 36, Y + 56, Y + 82)
    for yy, (txt, sz, wt, fam, col) in zip(ys, lines):
        d.t(x + w / 2, yy, txt, sz, col, fam, "middle", wt)
    x += w + GAP

cy = Y + RH / 2
for i in range(len(cols) - 1):
    d.path(f"M {xs[i][0] + xs[i][1] + 2} {cy} L {xs[i + 1][0] - 2} {cy}", MUTED, 1.4, m="ar")

FY = 262
FH = 70
fx = xs[3][0]
fw = xs[4][0] + xs[4][1] - fx
d.tone(fx, FY, fw, FH, BAD, 6, "14", 1.2)
d.t(fx + fw / 2, FY + 40, "Secret 이 없으면 authentication required", 12.5, INK, KR, "middle", 600)
d.path(f"M {fx + xs[3][1] / 2} {Y + RH + 2} L {fx + xs[3][1] / 2} {FY - 2}", MUTED, 1.4, m="ar")

d.legend(354, [("등록", INFO), ("저장소 Secret", ACC), ("읽어서 넘김", WARN), ("접속", OK), ("거절", BAD)])
d.save("09-01.repo-secret-flow.svg")
