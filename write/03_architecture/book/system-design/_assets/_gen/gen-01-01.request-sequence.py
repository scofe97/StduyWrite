# 타입 스펙: type-sequence — 클라이언트 · DNS · 웹 서버 세 레인의 요청·응답 네 번. Seq 계열이 한글을 mono 로 내보내므로 SeqKR 로 감싼다.
# 사실 출처: 추출본 v2.txt 80~99행(요청 흐름 1~4 · api.mysite.com · 15.125.23.214 · GET /users/12), PDF 6쪽 요청 흐름 그림, PDF 7쪽 JSON 응답 그림("id": 12 · "firstName": "John"),
#   RFC 1035 §3.2.2(TYPE A = a host address), RFC 9110 §15.3.1(200 OK)
# Layout conventions: 레인 폭 210 · 레인 y=104, 메시지 stride 60(y=196·256·316·376), 모든 좌표 4의 배수.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, Seq, ACC, OK, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 14, INK, KR, "middle", 600)
            s.t(x, y0 + 38, sub, 13, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 20, sub, 13, MUTED, _kr(sub))


W, H = 960, 504
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 01-01 §1",
          "이름이 IP 가 되고 요청이 JSON 이 된다",
          "클라이언트가 api.mysite.com 을 DNS 에 묻고, 받은 15.125.23.214 로 GET /users/12 를 보내 id 12 사용자의 JSON 을 받는다.",
          "네 번의 왕복 위에서 값이 이름에서 주소로, 주소에서 객체로 바뀝니다")
LX = d.lanes([("DNS", "이름 서버"), ("클라이언트", "브라우저 · 앱"), ("웹 서버", "서버 한 대")], 104, 210)
d.rails(420)

ROWS = (196, 256, 316, 376)
d.msg("클라이언트", "DNS", "api.mysite.com", ROWS[0], MUTED, "ar", None, "도메인 이름")
d.msg("DNS", "클라이언트", "15.125.23.214", ROWS[1], INFO, "info", "5 5", "A 레코드 · IP 주소")
d.msg("클라이언트", "웹 서버", "GET /users/12", ROWS[2], MUTED, "ar", None, "HTTP 요청")
d.msg("웹 서버", "클라이언트", '{"id": 12, "firstName": "John", …}', ROWS[3], OK, "ok", "5 5", "상태 200 · JSON 응답")
for i, y in enumerate(ROWS, 1):
    d.t(24, y + 4, str(i), 13, SOFT, MONO, "start", 600)

d.legend(H - 56, [("요청", MUTED), ("응답", INFO), ("성공 응답", OK)])
d.save("01-01.request-sequence.svg")
print("ok request-sequence")
