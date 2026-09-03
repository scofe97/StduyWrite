# 09-01 §7 두 계층에서 오는 두 신원.
# 본문(저자의 별도 상자): principals 는 PeerAuthentication 이 설정한 mTLS 연결의 상대이고,
#       requestPrincipals 는 RequestAuthentication 이 다루는 최종 사용자 쪽이며 JWT 에서 온다.
#       requestPrincipals 는 JWT 의 iss 와 sub 를 iss/sub 형식으로 이어 붙여 만든다.
# 아래 레인의 마지막 칸이 함정이다 — 토큰이 없으면 값이 비고, 그 요청은 그냥 통과한다.
# 타입 스펙: type-swimlane — 같은 요청을 두 계층이 나눠 맡고 각 레인이 다른 필드를 채우는 것이 논점이다.
#           레인마다 왼쪽 여백에 mono eyebrow, 레인 구분선 1px, accent 는 비어 있을 수 있는 칸 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 468
d = D(W, H, "ISTIO IN ACTION · 09-01 §7",
      "같은 요청에 신원이 둘 실린다",
      "전송 계층은 인증서에서, 요청 계층은 토큰에서 신원을 얻는다. 정책이 쓰는 필드 이름이 다른 이유가 "
      "여기 있다. 색이 붙은 칸은 비어 있을 수 있고, 비어도 요청은 통과한다.",
      "requestPrincipals 는 JWT 의 iss 와 sub 를 이어 붙인 값입니다")

LANE_H, LANE_Y0 = 120, 104
lanes = [("TRANSPORT", "사이드카끼리"),
         ("REQUEST", "최종 사용자")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(16, top + 52, name, 9, SOFT, MONO, "start", 600)
    d.t(16, top + 70, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(148, LANE_Y0, 148, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

SW, SH = 168, 64
def sx(j): return 188 + j * 200
def sy(k): return LANE_Y0 + k * LANE_H + 28
def step(k, j, label, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + SW / 2, y + 26, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 46, sub, 11, MUTED, MONO)

for k in (0, 1):
    for j in range(3):
        c = ACC if (k == 1 and j == 2) else MUTED
        m = "acc" if (k == 1 and j == 2) else "ar"
        d.arrow([(sx(j) + SW, sy(k) + SH / 2), (sx(j + 1) - 2, sy(k) + SH / 2)], c, m, 1.5 if m == "acc" else 1.4)

step(0, 0, "X.509 SVID", "상대가 제시")
step(0, 1, "PeerAuthentication", "peer authn filter")
step(0, 2, "SPIFFE ID", "…/ns/istioinaction/sa/webapp")
step(0, 3, "principals", "AuthorizationPolicy")
step(1, 0, "JWT", "Authorization: Bearer")
step(1, 1, "RequestAuthentication", "jwks 로 서명 검증")
step(1, 2, "iss / sub", "auth@istioinaction.io/…")
step(1, 3, "requestPrincipals", "없으면 비어 있다", focal=True)

d.t(24, 376, "정책이 쓰는 필드 이름이 갈리는 이유가 이 두 경로다 — 앞은 mTLS 가 있어야, 뒤는 토큰이 있어야 찬다", 11, SOFT, KR, "start")
d.legend(404, [("토큰이 없으면 비는 칸", ACC), ("인증서에서 오는 경로", MUTED)])
d.save("09-01.two-identities.svg")
