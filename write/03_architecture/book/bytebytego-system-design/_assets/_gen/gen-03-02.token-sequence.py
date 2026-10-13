# 타입 스펙: type-sequence — 클라이언트가 인증 서버에서 토큰을 받고, 웹 서버에 Bearer 헤더로 두 번 요청하며, 만료 뒤 401 을 받고 갱신 토큰으로 새 토큰을 받는 왕복.
# 사실 출처: RFC 6749 §5.1 예시 응답(access_token 2YotnFZFEjr1zCsicMWpAA · expires_in 3600 · refresh_token tGzv3JOkF0XG5Qx2TlKWIA), §6 갱신 요청(grant_type=refresh_token&refresh_token=tGzv3JOkF0XG5Qx2TlKWIA),
#   RFC 6750 §2.1 `Authorization: Bearer <토큰>` 헤더 형식과 §3 예시 `401 Unauthorized` + `WWW-Authenticate: Bearer … error="invalid_token"`. /orders 는 이 노트가 만든 예시 경로. 추출본 v1.txt 940~965행(토큰 방식 1~4단계).
# Layout conventions: 레인 3·폭 200, 호출·반환 한 쌍(호출 y, 반환 y+28)의 y 는 196·316·444·524(첫 쌍 뒤 만료 칩 자리와 시간 경과 구분선 y=396 을 비움). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
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
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        s.t((x1 + x2) / 2, y - 9, label, 12, c, _kr(label), "middle", 600)

    def state(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 880, 660
d = SeqKR(W, H, "BYTEBYTEGO · 03-02 §2",
          "토큰이 비밀번호 대신 요청마다 따라간다",
          "토큰은 3600 초 동안 Bearer 헤더로 쓰이고 만료 뒤에는 401 을 받아 새 토큰을 받습니다",
          "토큰 발급 → 사용 → 만료 → 갱신")
AS, CL, WS = "인증 서버", "클라이언트", "웹 서버"
d.lanes([(AS, "토큰 발급"), (CL, "토큰 보관"), (WS, "리소스")], 100, 200)
d.rails(H - 80)

Y0, S = 196, 64
BEARER = "GET /orders · Bearer 2YotnFZF…"
pairs = [
    (CL, AS, "POST /token", "access_token 2YotnFZF…", MUTED, OK),
    (CL, WS, BEARER, "200 orders", MUTED, OK),
    (CL, WS, BEARER, '401 · error="invalid_token"', ACC, BAD),
    (CL, AS, "POST /token · refresh_token", "access_token 새 값", MUTED, OK),
]
YS = [196, 316, 444, 524]
for k, (a, b, call, ret, cc, rc) in enumerate(pairs):
    y = YS[k]
    d.msg(a, b, call, y, cc, "acc" if cc == ACC else "ar")
    d.msg(b, a, ret, y + 28, rc, "bad" if rc == BAD else ("ok" if rc == OK else "ar"), dash="5 4")

d.state(CL, "expires_in 3600", 268, OK, dx=0)
d.line(40, 396, W - 64, 396, RULE, 0.8, "4 4")
d.t(W - 64, 388, "3600 초 뒤", 12, MUTED, KR, "end")

d.legend(H - 56, [("성공", OK), ("거절됨", BAD), ("만료된 토큰", ACC)])
d.save("03-02.token-sequence.svg")
