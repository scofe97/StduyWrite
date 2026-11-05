# 02-02 §2 — Dashboard 는 인증 정보를 API 서버에 그대로 넘기기만 하므로, 토큰의 권한이 화면에 보이는 범위를 정한다.
# 근거 문장: "Dashboard only acts as a proxy and passes all auth information to it [the API server].
#            In case of forbidden access corresponding warnings will be displayed in Dashboard."
#           (github.com/kubernetes/dashboard docs/user/access-control/README.md)
# 타입 스펙: type-sequence — 세 주체 사이의 시간순 왕복이고, 같은 토큰으로 보낸 두 요청의 응답이 갈리는 지점이 논지다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, INK, PAPER2, RULE, KR, MONO


def _kr(txt):
    """한글이 섞인 라벨은 한글 스택으로 — mono 에 넣으면 자간이 벌어진다(스타일 계약 §타이포그래피)."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 38, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))


W, H = 880, 560
d = SeqKR(W, H, "CKS STUDY GUIDE · 02-02 §2",
          "Dashboard 는 토큰을 넘기고 API 서버가 판정한다",
          "브라우저가 붙여 넣은 observer-user 토큰을 Dashboard 가 API 서버에 그대로 전달한다. "
          "cluster-observer ClusterRole 이 허용한 Deployment 목록은 200 으로, 허용하지 않은 Pod 목록은 403 으로 돌아온다.",
          "같은 토큰으로 보낸 두 요청의 응답이 갈리는 곳이 API 서버입니다")

d.lanes([("브라우저", "https 로 접속한 로그인 화면"),
         ("Dashboard", "namespace kubernetes-dashboard"),
         ("API 서버", ":6443")], y0=104, lane_w=240)
d.rails(470)

d.msg("브라우저", "Dashboard", "토큰 붙여넣기", 196, MUTED, sub="ServiceAccount observer-user")
d.msg("Dashboard", "API 서버", "list deployments", 258, MUTED, sub="인증 정보를 그대로 전달")
d.msg("API 서버", "Dashboard", "200 OK", 320, ACC, mk="acc", dash="5 4", sub="cluster-observer 가 허용")
d.msg("Dashboard", "API 서버", "list pods", 382, MUTED, sub="같은 토큰")
d.msg("API 서버", "Dashboard", "403 Forbidden", 444, BAD, mk="bad", dash="5 4", sub="허용 규칙 없음")

d.legend(496, [("허용된 응답", ACC), ("거부된 응답", BAD)])
d.save("02-02.dashboard-token-path.svg")
