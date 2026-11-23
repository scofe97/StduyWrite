# 타입 스펙: type-sequence
# 03-02 docker login 의 토큰 인증 흐름 (Docker Hub 공개 값)
import sys; sys.path.insert(0, ".")
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 688


class TSeq(Seq):
    def msg2(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        """msg 와 같되 라벨 x 를 따로 줄 수 있다(가운데 레인 선을 비키려고)."""
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, MONO, "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, MONO)


d = TSeq(W, H, "DEVOPS · CONTAINER · 03-02",
         "docker login 의 토큰 인증 흐름",
         "GET /v2/ 가 401 로 돌아오는 데서 시작해 Bearer 토큰을 받고 config.json 에 계정을 저장하는 순서",
         lead="Docker Hub 에서 잰 값. 토큰은 저장하지 않고 pull·push 때마다 범위를 달아 다시 받습니다")

L = d.lanes([("CLI", "docker login"),
             ("dockerd", "daemon"),
             ("레지스트리", "registry-1.docker.io"),
             ("토큰 서버", "auth.docker.io")], y0=104, lane_w=168)
CLI, DD, REG, TOK = "CLI", "dockerd", "레지스트리", "토큰 서버"

Y0, STEP = 192, 48
ys = [Y0 + STEP * i for i in range(9)]
d.rails(ys[-1] + 28)

d.msg2(CLI, DD, "계정 전달", ys[0], MUTED, "ar")
d.msg2(DD, REG, "GET /v2/", ys[1], MUTED, "ar")
d.msg2(REG, DD, "401", ys[2], BAD, "bad", dash="5 4", sub="Bearer realm · service")
d.msg2(DD, TOK, "GET /token", ys[3], MUTED, "ar", sub="Basic 계정 · scope", lx=(L[REG] + L[TOK]) / 2 + 12)
d.msg2(TOK, DD, "200 token", ys[4], ACC, "acc", dash="5 4", lx=(L[REG] + L[TOK]) / 2 + 12)
d.msg2(DD, REG, "GET /v2/", ys[5], MUTED, "ar", sub="Authorization: Bearer")
d.msg2(REG, DD, "200", ys[6], OK, "ok", dash="5 4")
d.msg2(DD, CLI, "Login Succeeded", ys[7], OK, "ok", dash="5 4")
d.selfmsg(CLI, "config.json", ys[8], OK, sub="auths[주소] 에 저장")

d.legend(H - 56, [
    ("호출", MUTED),
    ("401 거절", BAD),
    ("토큰 발급", ACC),
    ("성공과 저장", OK),
])

d.save("03-02.token-auth.svg")
print("ok gen-03-02.token-auth")
