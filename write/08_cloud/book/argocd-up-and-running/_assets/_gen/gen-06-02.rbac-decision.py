# 06-02 §3 — RBAC 는 요청의 주체로 g 줄에서 역할을 찾고 주체 자신과 그 역할의 p 줄을 대조해 deny 가 일치하면 거부, allow 만 일치하면 허용, 일치가 없으면 거부한다. policy.default 의 역할이 주는 권한은 deny 로 막히지 않고 따로 허용된다.
# 본문 근거: 이 노트 ### 3 「RBAC 정책 읽는 법」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치해 argocd admin settings rbac can 과 argocd account can-i 로 확인했다.
#            allow `applications, *, */*` 와 deny `applications, delete, */*` 를 deny 가 앞에 있을 때와 뒤에 있을 때 모두 두어 delete 는 No, get 과 sync 는 Yes 였다.
#            policy.default 가 비어 있으면 어느 정책에도 없는 계정의 get 은 No, --default-role role:readonly 를 주면 get 은 Yes 이고 sync 는 No 였다.
#            deny 줄 `p, bob, applications, get, */*, deny` 가 있어도 --default-role role:readonly 에서 bob 의 get 은 Yes 였고 --default-role 이 없으면 No 였다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/rbac.md("Even if more specific policies with the `allow` effect match as well, the `deny` will have priority.",
#            "The order in which the policies appears in the policy file configuration has no impact", "All authenticated users get at least the permissions granted by the default policies.").
# 타입 스펙: type-architecture — 왼쪽 요청에서 오른쪽 판정으로 가는 한 방향 흐름, 오른쪽 끝에서 결과 셋으로 갈라진다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 06-02 §3",
      "RBAC 가 요청을 허용하거나 거부하는 길",
      "왼쪽의 요청에서 시작해 g 줄이 주체가 받은 역할을 찾고 주체 자신과 그 역할의 p 줄을 요청과 대조한다. "
      "deny 가 하나라도 일치하면 거부하고 allow 만 일치하면 허용하며 일치하는 줄이 없으면 거부한다. 줄이 적힌 순서는 결과에 영향을 주지 않는다. "
      "아래쪽의 policy.default 의 역할은 이 대조와 별개로 권한을 주며 deny 로 막히지 않는다.",
      "결과를 가르는 것은 줄의 순서가 아니라 deny 가 일치하는지입니다")

A_X, A_W = 24, 150
B_X, B_W = 214, 200
C_X, C_W = 454, 216
O_X, O_W = 708, 148
MID = 235
BOX_Y, BOX_H = 170, 130

# 요청
d.tone(A_X, BOX_Y, A_W, BOX_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, BOX_Y + 36, "요청", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, BOX_Y + 66, "주체 · 그룹", 12, MUTED)
d.t(A_X + A_W / 2, BOX_Y + 88, "자원 · 동작", 12, MUTED)
d.t(A_X + A_W / 2, BOX_Y + 110, "객체", 12, MUTED)

# g 줄
d.box(B_X, BOX_Y, B_W, BOX_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, BOX_Y + 36, "g 줄: 역할 찾기", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, BOX_Y + 64, "주체 자신과 받은 역할", 12, MUTED)
d.t(B_X + B_W / 2, BOX_Y + 92, "g, Developers,", 11.5, MUTED, MONO)
d.t(B_X + B_W / 2, BOX_Y + 112, "role:developers", 11.5, MUTED, MONO)

# p 줄
d.tone(C_X, BOX_Y, C_W, BOX_H, SOFT, 6, "14", 1.1)
d.t(C_X + C_W / 2, BOX_Y + 36, "p 줄: 허용 · 거부 대조", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, BOX_Y + 64, "주체 자신과 그 역할의 줄", 12, MUTED)
d.t(C_X + C_W / 2, BOX_Y + 92, "p, role:developers,", 11.5, MUTED, MONO)
d.t(C_X + C_W / 2, BOX_Y + 112, "applications, *, */*, allow", 11.5, MUTED, MONO)

# 기본 역할
DY, DH = 364, 62
d.tone(B_X, DY, B_W, DH, ACC, 6, "14", 1.4)
d.t(B_X + B_W / 2, DY + 28, "policy.default 의 역할", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, DY + 49, "인증된 모두에게 적용", 12, MUTED)

# 결과
outs = [
    (118, BAD, "거부", "deny 줄이 일치"),
    (200, OK, "허용", "allow 줄만 일치"),
    (282, BAD, "거부", "일치하는 줄 없음"),
]
for y, c, t1, t2 in outs:
    d.tone(O_X, y, O_W, 70, c, 6, "14", 1.2)
    d.t(O_X + O_W / 2, y + 30, t1, 12.5, INK, KR, "middle", 600)
    d.t(O_X + O_W / 2, y + 52, t2, 12, MUTED)
    ty = y + 35
    d.path(f"M {C_X + C_W + 2} {MID} L {C_X + C_W + 18} {MID} L {C_X + C_W + 18} {ty} L {O_X - 2} {ty}", MUTED, 1.4, m="ar")

# 화살표
d.path(f"M {A_X + A_W + 2} {MID} L {B_X - 2} {MID}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} {MID} L {C_X - 2} {MID}", MUTED, 1.4, m="ar")
d.tone(O_X, DY, O_W, DH, OK, 6, "14", 1.2)
d.t(O_X + O_W / 2, DY + 28, "허용", 12.5, INK, KR, "middle", 600)
d.t(O_X + O_W / 2, DY + 49, "기본 역할의 권한", 12, MUTED)
d.path(f"M {B_X + B_W + 2} {DY + DH / 2} L {O_X - 2} {DY + DH / 2}", MUTED, 1.4, m="ar")
d.chip((B_X + B_W + O_X) / 2, DY + DH / 2, "deny 로 막히지 않음", MUTED, 11)

d.legend(448, [("요청", INFO), ("규칙 조회", SOFT), ("기본 역할", ACC), ("허용", OK), ("거부", BAD)])
d.save("06-02.rbac-decision.svg")
