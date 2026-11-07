# 08-01 §3 — 프로젝트 역할의 JWT 토큰은 프로젝트의 토큰 목록(status.jwtTokensByRole)에 남은 토큰만 통과하고, proj:<프로젝트>:<역할> 주체로 그 역할의 policies 와 대조해 일치하는 allow 가 있을 때만 허용된다. 삭제한 토큰은 곧바로 Unauthenticated 로 거부된다.
# 본문 근거: 이 노트 ### 3 「프로젝트 역할과 토큰」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 golist 프로젝트에 역할 golist-developer 를 두어 확인했다.
#            `argocd proj role create-token` 으로 만든 토큰은 프로젝트에 id·iat 가 남았고 토큰 값은 만들 때 한 번만 보였다.
#            그 토큰으로 golist 프로젝트의 앱 get·sync 는 허용되고 다른 프로젝트의 앱과 policies 에 없는 동작은 PermissionDenied 였다.
#            `delete-token PROJECT ROLE ISSUED-AT` 로 지운 토큰은 바로 다음 호출부터 Unauthenticated(`JWT token for role 'golist-developer' issued at '…' does not exist in project 'golist'`)였고, 인자는 uuid 가 아니라 iat 였다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/projects.md("Project roles", "JWT tokens"), docs/operator-manual/rbac.md.
#            인증은 status.jwtTokensByRole 을 보고(app_project_types.go GetJWTToken 주석 "JWTTokens are stored under status"), spec.roles[].jwtTokens 는 호환용 사본이다.
# 타입 스펙: type-architecture — 왼쪽 요청에서 오른쪽 판정으로 가는 한 방향 흐름, 가운데 칸 아래로 갈라지는 거부 한 가지.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 08-01 §3",
      "프로젝트 역할의 토큰이 통과하는 길",
      "왼쪽의 호출은 프로젝트 역할의 JWT 토큰을 달고 온다. 가운데 칸이 프로젝트의 토큰 목록(status.jwtTokensByRole)에 그 토큰이 남아 있는지 확인하고, 삭제한 토큰이면 곧바로 Unauthenticated 로 거부한다. "
      "남아 있는 토큰은 proj:프로젝트:역할 주체가 되어 그 역할의 policies 와 암묵으로 붙는 projects get 줄과 대조된다. "
      "일치하는 allow 줄이 있으면 허용하고 없으면 PermissionDenied 로 거부한다.",
      "토큰의 권한은 그 프로젝트의 역할이 가진 줄까지입니다")

A_X, A_W = 24, 150
B_X, B_W = 214, 200
C_X, C_W = 454, 216
O_X, O_W = 708, 148
MID = 235
BOX_Y, BOX_H = 164, 142

# 호출
d.tone(A_X, BOX_Y, A_W, BOX_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, BOX_Y + 38, "호출", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, BOX_Y + 68, "JWT 토큰", 12, MUTED)
d.t(A_X + A_W / 2, BOX_Y + 92, "proj role", 11.5, MUTED, MONO)
d.t(A_X + A_W / 2, BOX_Y + 112, "create-token", 11.5, MUTED, MONO)

# 토큰 확인
d.box(B_X, BOX_Y, B_W, BOX_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, BOX_Y + 38, "토큰 확인", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, BOX_Y + 68, "프로젝트에 남아 있나", 12, MUTED)
d.t(B_X + B_W / 2, BOX_Y + 96, "status.jwtTokensByRole", 11.5, MUTED, MONO)
d.t(B_X + B_W / 2, BOX_Y + 120, "proj:<프로젝트>:<역할>", 11.5, MUTED, MONO)

# 역할 policies
d.tone(C_X, BOX_Y, C_W, BOX_H, ACC, 6, "14", 1.4)
d.t(C_X + C_W / 2, BOX_Y + 38, "역할의 policies 대조", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, BOX_Y + 66, "역할이 가진 줄과 암묵 get 줄", 12, MUTED)
d.t(C_X + C_W / 2, BOX_Y + 94, "applications, sync,", 11.5, MUTED, MONO)
d.t(C_X + C_W / 2, BOX_Y + 114, "<프로젝트>/*, allow", 11.5, MUTED, MONO)

# 결과
outs = [
    (160, OK, "허용", "allow 줄이 일치"),
    (240, BAD, "PermissionDenied", "일치하는 줄 없음"),
]
for y, c, t1, t2 in outs:
    d.tone(O_X, y, O_W, 70, c, 6, "14", 1.2)
    d.t(O_X + O_W / 2, y + 30, t1, 12.5 if len(t1) < 8 else 11.5, INK, KR, "middle", 600)
    d.t(O_X + O_W / 2, y + 52, t2, 12, MUTED)
    ty = y + 35
    d.path(f"M {C_X + C_W + 2} {MID} L {C_X + C_W + 18} {MID} L {C_X + C_W + 18} {ty} L {O_X - 2} {ty}", MUTED, 1.4, m="ar")

# 화살표
d.path(f"M {A_X + A_W + 2} {MID} L {B_X - 2} {MID}", MUTED, 1.4, m="ar")
d.path(f"M {B_X + B_W + 2} {MID} L {C_X - 2} {MID}", MUTED, 1.4, m="ar")

# 삭제한 토큰
DY, DH = 372, 62
d.tone(B_X, DY, B_W, DH, BAD, 6, "14", 1.2)
d.t(B_X + B_W / 2, DY + 28, "Unauthenticated", 11.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, DY + 49, "delete-token 으로 지운 토큰", 12, MUTED)
d.path(f"M {B_X + B_W / 2} {BOX_Y + BOX_H + 2} L {B_X + B_W / 2} {DY - 2}", MUTED, 1.4, m="ar")

d.legend(448, [("호출", INFO), ("토큰 확인", PAPER2), ("역할 대조", ACC), ("허용", OK), ("거부", BAD)])
d.save("08-01.role-token.svg")
