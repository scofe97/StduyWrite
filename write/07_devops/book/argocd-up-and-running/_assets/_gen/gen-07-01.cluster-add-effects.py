# 07-01 §2 — argocd cluster add 를 옵션 없이 한 번 실행하면 원격 클러스터에 관리용 ServiceAccount·ClusterRole·ClusterRoleBinding·토큰 Secret 을 만들고, 허브에는 cluster Secret 을 만든다.
# 본문 근거: 이 노트 ### 2 「원격 클러스터 등록」.
# 검증 근거: kind v0.31.0 의 v3.6.1 로 argocd cluster add --cluster-endpoint kube-public 를 실행해
#            ServiceAccount "argocd-manager" created in namespace "kube-system" / ClusterRole "argocd-manager-role" created /
#            ClusterRoleBinding "argocd-manager-role-binding" created / Created bearer token secret "argocd-manager-long-lived-token" for ServiceAccount "argocd-manager" 로그(JSON 로그의 msg 값)를 확인하고,
#            허브 argocd 네임스페이스에 라벨 argocd.argoproj.io/secret-type=cluster 인 Secret 이 생김을 kubectl 로 확인.
# 공식 근거: argo-cd v3.6.1 util/clusterauth/clusterauth.go(ArgoCDManager 이름 상수와 규칙), docs/getting_started.md("installs a ServiceAccount (argocd-manager), into the kube-system namespace ... binds the service account to an admin-level ClusterRole").
# 타입 스펙: type-flowchart — 한 명령에서 두 클러스터로 갈라지는 생성 결과.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 448
d = D(W, H, "ARGO CD UP AND RUNNING · 07-01 §2",
      "argocd cluster add 가 만드는 것",
      "왼쪽의 argocd CLI 가 kubeconfig 컨텍스트로 원격 클러스터에 접속해 가운데 상자의 네 리소스를 만들고, 허브 클러스터에는 Argo CD API server 를 거쳐 오른쪽의 cluster Secret 이 저장된다. "
      "옵션 없이 실행할 때 네 리소스는 ServiceAccount, ClusterRole, ClusterRoleBinding, 토큰 Secret 이다.",
      "옵션 없이 한 번 실행하면 원격에는 관리용 계정과 권한을, 허브에는 접속 정보를 둡니다")

d.tone(24, 150, 170, 76, INFO, 6, "14", 1.1)
d.t(24 + 85, 150 + 30, "argocd CLI", 12.5, INK, MONO, "middle", 600)
d.t(24 + 85, 150 + 52, "kubeconfig 컨텍스트", 11, MUTED)

FX, FY, FW, FH = 250, 100, 360, 262
d.tone(FX, FY, FW, FH, SOFT, 6, "10", 1.1)
d.t(FX + 16, FY + 26, "원격 클러스터에 생성", 13, INK, KR, "start", 600)
ITEMS = [
    ("ServiceAccount · kube-system", "argocd-manager"),
    ("ClusterRole", "argocd-manager-role"),
    ("ClusterRoleBinding", "argocd-manager-role-binding"),
    ("토큰 Secret", "argocd-manager-long-lived-token"),
]
for i, (lab, name) in enumerate(ITEMS):
    y = FY + 44 + i * 54
    d.tone(FX + 20, y, FW - 40, 44, INFO, 6, "14", 1.1)
    d.t(FX + FW / 2, y + 19, lab, 12, INK, KR, "middle", 600)
    d.t(FX + FW / 2, y + 35, name, 11, MUTED, MONO)

d.arrow([(196, 170), (FX - 2, 170)], MUTED)
d.t(223, 160, "생성", 11.5, MUTED, KR, "middle", 600)

HX, HY, HW, HH = 670, 150, 186, 96
d.tone(HX, HY, HW, HH, ACC, 6, "10", 1.3)
d.t(HX + HW / 2, HY + 26, "허브 클러스터", 13, INK, KR, "middle", 600)
d.tone(HX + 16, HY + 40, HW - 32, 44, ACC, 6, "14", 1.4)
d.t(HX + HW / 2, HY + 40 + 19, "cluster Secret", 12, INK, MONO, "middle", 600)
d.t(HX + HW / 2, HY + 40 + 35, "argocd 네임스페이스", 11, MUTED)

d.arrow([(109, 228), (109, 384), (HX + HW / 2, 384), (HX + HW / 2, HY + HH + 2)], MUTED)
d.chip(430, 384, "Argo CD API 로 등록", MUTED, 11)

d.legend(404, [("실행 도구", INFO), ("원격에 생기는 리소스", INFO), ("허브에 생기는 Secret", ACC)])
d.save("07-01.cluster-add-effects.svg")
