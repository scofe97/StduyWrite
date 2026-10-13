# 타입 스펙: type-sequence — 같은 단축 키를 두 번 여는 요청 둘. 첫 요청은 캐시 미스 뒤 DB 를 거쳐 캐시에 채우고 둘째는 캐시 적중으로 끝나며, 둘 다 302 와 Location 으로 돌아간다.
# 사실 출처: 추출본 v2.txt 2266~2278행(캐시 확인 → 없으면 DB → longURL 반환)·2273행(https://tinyurl.com/zn9edcu),
#   RFC 9110 §15.4.3(302 Found 와 Location, https://www.rfc-editor.org/rfc/rfc9110#section-15.4.3). 로드 밸런서는 웹 서버 앞에 있어 레인으로 따로 그리지 않았다.
# Layout conventions: 레인 4개 폭 160, x = 120·440·700·900, 메시지 stride 44~56, 요청 둘 사이 구분선. 모든 좌표 4의 배수.
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


W, H = 1000, 860
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 08-01 §6",
          "단축 키를 여는 요청은 캐시를 먼저 묻는다",
          "캐시에 없으면 DB 에서 longURL 을 읽어 캐시에 넣고, 있으면 DB 를 건너뛰며, 어느 쪽이든 302 와 Location 으로 되돌린다.",
          "같은 키 zn9edcu 를 두 번 열면 둘째는 DB 를 건너뛴다")

d.lanes([("브라우저", "클라이언트"), ("웹 서버", "로드 밸런서 뒤"), ("캐시", "shortURL → longURL"), ("데이터베이스", "원본")],
        (120, 440, 700, 900))
d.rails(800)

d.t(12, 188, "요청 1 · 캐시 미스", 13, SOFT, KR, "start", 600)
d.msg("브라우저", "웹 서버", "GET tinyurl.com/zn9edcu", 220, MUTED)
d.msg("웹 서버", "캐시", "get zn9edcu", 264, MUTED)
d.msg("캐시", "웹 서버", "미스", 308, WARN, dash="5 4")
d.msg("웹 서버", "데이터베이스", "longURL 조회", 360, INFO, sub="shortURL = zn9edcu", dx=-110)
d.msg("데이터베이스", "웹 서버", "longURL", 416, INFO, dash="5 4", dx=-110)
d.msg("웹 서버", "캐시", "set zn9edcu", 460, MUTED)
d.msg("웹 서버", "브라우저", "302 Found", 516, ACC, dash="5 4", sub="Location: …/wiki/Systems_design")

d.line(12, 564, W - 48, 564, RULE, 0.8, "3 6")
d.t(12, 588, "요청 2 · 캐시 적중", 13, SOFT, KR, "start", 600)
d.msg("브라우저", "웹 서버", "GET tinyurl.com/zn9edcu", 620, MUTED)
d.msg("웹 서버", "캐시", "get zn9edcu", 664, MUTED)
d.msg("캐시", "웹 서버", "longURL", 708, OK, dash="5 4")
d.msg("웹 서버", "브라우저", "302 Found", 760, ACC, dash="5 4", sub="Location: …/wiki/Systems_design")

d.legend(H - 40, [("캐시 미스", WARN), ("DB 경로", INFO), ("캐시 적중", OK), ("302 응답", ACC)])
d.save("08-01.redirect-sequence.svg")
