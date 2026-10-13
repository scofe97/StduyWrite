# 타입 스펙: type-sequence — 참여자 넷(클라이언트 · 미들웨어 · Redis · API 서버), 메시지 여덟. 카운터 값이 5 → 6 으로 움직이며 통과가 거절로 갈린다. focal 은 429 응답.
# 사실 출처: 추출본 v2.txt 1127~1148행(카운터를 Redis 에서 가져와 한도와 비교, 넘으면 거절 · 아니면 API 서버로 전달), 1156~1176행(login 분당 5회 규칙),
#   1177~1181행(429). Redis INCR 문서(새 값을 돌려줌). RFC 6585 §4 · RFC 9110 §10.2.3(Retry-After 초 값).
#   키 login:u1:1200 · 12:00:41 · Retry-After 19 는 설명용 설계 값(창 끝 12:01:00 − 12:00:41 = 19초).
# Layout conventions: 레인 폭 176·중심 x=112·368·624·848, 메시지 stride 60(y=196부터), 레일 하단 H-80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 12)/2}" y="{y - 23}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="20" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 13, MUTED, _kr(sub))


W, H = 960, 720
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 04-02 §1",
          "분당 5회 규칙에서 다섯째는 통과하고 여섯째는 429",
          "미들웨어가 요청마다 Redis 카운터를 INCR 로 올려 새 값을 한도 5 와 견주고, 5 는 API 서버로 전달하고 6 은 429 와 Retry-After 19 로 돌려보낸다.",
          "카운터 키 login:u1:1200")

NAMES = (("클라이언트", "사용자 u1"), ("미들웨어", "login 5/분"), ("Redis", "login:u1:1200"), ("API 서버", "로그인 처리"))
d.LX = {"클라이언트": 112, "미들웨어": 368, "Redis": 624, "API 서버": 848}
for nm, sub in NAMES:
    x = d.LX[nm]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 12, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

C, M, R, A = "클라이언트", "미들웨어", "Redis", "API 서버"
d.msg(C, M, "POST /login", 196, INFO, "info", sub="다섯째 요청")
d.msg(M, R, "INCR login:u1:1200", 256, MUTED, "ar")
d.msg(R, M, "= 5", 316, OK, "ok", dash="5 4", sub="5 ≤ 5 · 통과")
d.msg(M, A, "POST /login", 376, OK, "ok", sub="전달")
d.msg(C, M, "POST /login", 436, INFO, "info", sub="여섯째 요청 · 12:00:41")
d.msg(M, R, "INCR login:u1:1200", 496, MUTED, "ar")
d.msg(R, M, "= 6", 556, BAD, "bad", dash="5 4", sub="6 > 5 · 거절")
d.msg(M, C, "429", 616, ACC, "acc", sub="Retry-After: 19")

d.legend(H - 56, [("요청", INFO), ("통과", OK), ("거절", BAD), ("429 응답", ACC)])
d.save("04-02.request-flow.svg")
