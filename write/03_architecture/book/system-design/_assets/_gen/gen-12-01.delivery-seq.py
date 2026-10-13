# 타입 스펙: type-sequence — 사용자 B 가 새 메시지 하나(ID 301)를 받는 동안 폴링·롱 폴링·웹소켓에서 오간 요청과 응답을 레인 둘 위에 세 묶음으로 쌓는다.
# 사실 출처: 방식별 흐름은 추출본 v2.txt 3234~3269행(폴링·롱 폴링·웹소켓)과 RFC 6202 §2.1(https://www.rfc-editor.org/rfc/rfc6202#section-2.1),
#   RFC 6455 §1.3(Upgrade 요청과 101 Switching Protocols 응답, https://www.rfc-editor.org/rfc/rfc6455#section-1.3).
#   설명용 예시(그림·추출본에 없는 값): 쿼리 after=300 과 ID 300·301. 300 은 사용자 B 가 마지막으로 본 ID, 301 은 새 메시지 ID 로 둔 예시다.
#   메시지 12 개(스펙 한도), 레인 2 개.
# Layout conventions: 레인 폭 200, x = 180·820, 메시지 stride 40~56, 묶음 사이 구분선. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=160):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))


W, H = 1000, 872
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 12-01 §2",
          "새 메시지 301 을 받기까지 요청은 폴링 3 번, 롱 폴링 1 번, 웹소켓 1 번이다",
          "웹소켓만 서버가 먼저 보낸다. 폴링은 빈 응답이 쌓이고 롱 폴링은 응답마다 새 요청이 따른다.",
          "사용자 B 가 마지막으로 본 ID 는 300")

d.lanes([("사용자 B", "받는 쪽"), ("채팅 서버", "HTTP · 웹소켓")], (180, 820), lane_w=200)
d.rails(796)

d.t(12, 188, "폴링 · 요청 3 번", 13, SOFT, KR, "start", 600)
d.msg("사용자 B", "채팅 서버", "GET after=300", 220, MUTED)
d.msg("채팅 서버", "사용자 B", "200 []", 260, WARN, dash="5 4")
d.msg("사용자 B", "채팅 서버", "GET after=300", 300, MUTED)
d.msg("채팅 서버", "사용자 B", "200 []", 340, WARN, dash="5 4")
d.msg("사용자 B", "채팅 서버", "GET after=300", 380, MUTED)
d.msg("채팅 서버", "사용자 B", "200 [301]", 420, OK, dash="5 4")

d.line(12, 448, W - 48, 448, RULE, 0.8, "3 6")
d.t(12, 472, "롱 폴링 · 받기까지 요청 1 번", 13, SOFT, KR, "start", 600)
d.msg("사용자 B", "채팅 서버", "GET after=300", 504, MUTED, sub="서버 응답 보류")
d.msg("채팅 서버", "사용자 B", "200 [301]", 568, OK, dash="5 4")
d.msg("사용자 B", "채팅 서버", "GET after=301", 612, MUTED, sub="응답 직후 재요청")

d.line(12, 640, W - 48, 640, RULE, 0.8, "3 6")
d.t(12, 664, "웹소켓 · 핸드셰이크 1 번", 13, SOFT, KR, "start", 600)
d.msg("사용자 B", "채팅 서버", "GET /chat · Upgrade: websocket", 696, MUTED)
d.msg("채팅 서버", "사용자 B", "101 Switching Protocols", 736, INFO, dash="5 4")
d.msg("채팅 서버", "사용자 B", "프레임 id 301", 780, ACC, dash="5 4", sub="서버 먼저 전송")

d.legend(H - 40, [("요청", MUTED), ("빈 응답", WARN), ("새 메시지", OK), ("101 전환", INFO), ("서버가 먼저", ACC)])
d.save("12-01.delivery-seq.svg")
