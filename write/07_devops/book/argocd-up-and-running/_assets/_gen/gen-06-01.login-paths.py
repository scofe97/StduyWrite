# 06-01 §3 — 로컬 계정·Dex·직접 OIDC 세 로그인 길은 서로 다른 곳에서 토큰이 만들어지고, API server 가 그 토큰의 발급자·사용자 이름·그룹을 읽는 한 곳으로 모인다.
# 본문 근거: 이 노트 ### 1 「admin 과 로컬 사용자」, ### 3 「SSO — Dex 와 직접 OIDC」.
# 검증 근거: kind v0.31.0(Kubernetes v1.35.0)에 Argo CD v3.6.1 을 설치해 로컬 계정(argocd account get-user-info → Issuer: argocd)과
#            Dex mockCallback 커넥터(argocd login --sso → Issuer: <url>/api/dex, Groups: authors), oidc.config 키 이름(/api/v1/settings 의 oidcConfig)을 확인.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/user-management/index.md(SSO 두 방식, 콜백 /api/dex/callback·/auth/callback),
#            util/settings/settings.go(IssuerURL: oidc.config 의 issuer 우선, 없으면 <url>/api/dex), docs/operator-manual/argocd-cm.yaml(dex.config·oidc.config·accounts.*).
# 타입 스펙: type-architecture — 입구 셋이 한 서버로 모이는 수렴형.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 464
d = D(W, H, "ARGO CD UP AND RUNNING · 06-01 §3",
      "로컬 계정과 SSO 두 방식의 로그인 길",
      "세 줄의 로그인 길이 왼쪽에서 오른쪽으로 이어진다. 로컬 계정은 비밀번호 확인 뒤 Argo CD 가 토큰을 발급하고, "
      "Dex 방식은 argocd-dex-server 가 외부 IdP 를 거쳐 토큰을 발급하며, 직접 OIDC 방식은 OIDC IdP 가 토큰을 발급한다. "
      "세 토큰은 모두 오른쪽의 API server 가 발급자와 사용자 이름과 그룹을 읽는 곳으로 모인다.",
      "세 길은 토큰을 만드는 곳이 다르고 API server 가 읽는 것은 같습니다")

ROW_Y = (110, 206, 302)
ROW_H = 84
C1_X, C1_W = 24, 140
C2_X, C2_W = 214, 170
C3_X, C3_W = 454, 150
C4_X, C4_W = 674, 190
TOP, BOT = 110, 386

lanes = [
    ("로컬 계정", "accounts.<이름>"),
    ("SSO · Dex", "dex.config"),
    ("SSO · 직접 OIDC", "oidc.config"),
]
checks = [
    ("비밀번호 확인", "argocd-secret", "bcrypt 해시"),
    ("argocd-dex-server", "커넥터 → 외부 IdP", "/api/dex/callback"),
    ("OIDC IdP", "Keycloak 등", "/auth/callback"),
]
issuers = [
    ("발급: Argo CD", "iss: argocd"),
    ("발급: Dex", "iss: <url>/api/dex"),
    ("발급: IdP", "iss: oidc issuer"),
]


def mid(y):
    return y + ROW_H / 2


for y, (name, key), (t2, s2a, s2b), (t3, s3) in zip(ROW_Y, lanes, checks, issuers):
    d.tone(C1_X, y, C1_W, ROW_H, INFO, 6, "14", 1.1)
    d.t(C1_X + C1_W / 2, y + 36, name, 12.5, INK, KR, "middle", 600)
    d.t(C1_X + C1_W / 2, y + 60, key, 11.5, MUTED, MONO)

    d.box(C2_X, y, C2_W, ROW_H, PAPER2, RULE, 1.0)
    d.t(C2_X + C2_W / 2, y + 28, t2, 12.5, INK, KR, "middle", 600)
    d.t(C2_X + C2_W / 2, y + 50, s2a, 11.5, MUTED, KR)
    d.t(C2_X + C2_W / 2, y + 68, s2b, 11.5, MUTED, MONO)

    d.tone(C3_X, y, C3_W, ROW_H, SOFT, 6, "14", 1.1)
    d.t(C3_X + C3_W / 2, y + 36, t3, 12.5, INK, KR, "middle", 600)
    d.t(C3_X + C3_W / 2, y + 60, s3, 11.5, MUTED, MONO)

    d.path(f"M {C1_X + C1_W + 2} {mid(y)} L {C2_X - 2} {mid(y)}", MUTED, 1.4, m="ar")
    d.path(f"M {C2_X + C2_W + 2} {mid(y)} L {C3_X - 2} {mid(y)}", MUTED, 1.4, m="ar")
    d.path(f"M {C3_X + C3_W + 2} {mid(y)} L {C4_X - 2} {mid(y)}", MUTED, 1.4, m="ar")

d.tone(C4_X, TOP, C4_W, BOT - TOP, ACC, 6, "14", 1.4)
d.t(C4_X + C4_W / 2, TOP + 36, "API server", 13, INK, KR, "middle", 600)
for i, s in enumerate(["토큰 검증", "발급자 · 사용자 이름", "groups 클레임", "다음: RBAC (06-02)"]):
    d.t(C4_X + C4_W / 2, TOP + 92 + i * 36, s, 11.5, MUTED, KR)

d.legend(420, [("로그인 길", INFO), ("API server", ACC), ("확인 · 발급", SOFT)])
d.save("06-01.login-paths.svg")
