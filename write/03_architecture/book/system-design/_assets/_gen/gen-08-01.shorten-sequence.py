# 타입 스펙: type-sequence — 새 longURL 하나가 단축되는 한 번의 요청. 중복 조회가 비면 ID 를 받아 base62 로 바꾸고 행을 넣은 뒤 단축 URL 을 돌려준다.
# 사실 출처: 추출본 v2.txt 2118~2122행(POST api/v1/data/shorten)·2242~2255행(여섯 단계와 예: ID 2009215674938 → zn9edcu)·PDF 128쪽 Table 8-4,
#   계산: 2009215674938 = 62×32406704434 + 30(u) … 마지막 몫 35(z) → zn9edcu (7 자, 62^6 = 56,800,235,584 이상이고 62^7 미만).
# Layout conventions: 레인 4개 폭 160, x = 120·440·700·900, 메시지 stride 44~56. 모든 좌표 4의 배수.
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

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="acc")
        s.t(x + 68, y - 4, label, 12, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 13, sub, 12, MUTED, _kr(sub), "start")


W, H = 1000, 660
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 08-01 §6",
          "처음 보는 longURL 은 ID 를 받아 zn9edcu 가 된다",
          "longURL 이 DB 에 없으면 유일 ID 를 받아 base62 로 바꾸고 행으로 저장한 뒤 단축 URL 을 돌려준다.",
          "ID 2009215674938 이 일곱 글자로 바뀐다")

d.lanes([("브라우저", "클라이언트"), ("웹 서버", "단축 서비스"), ("데이터베이스", "id · shortURL · longURL"), ("ID 생성기", "유일 ID")],
        (120, 440, 700, 900))
d.rails(588)

d.msg("브라우저", "웹 서버", "POST api/v1/data/shorten", 204, MUTED, sub="longUrl: …/wiki/Systems_design")
d.msg("웹 서버", "데이터베이스", "longURL 조회", 264, INFO)
d.msg("데이터베이스", "웹 서버", "없음", 304, WARN, dash="5 4")
d.msg("웹 서버", "ID 생성기", "새 ID 요청", 360, MUTED, dx=-90)
d.msg("ID 생성기", "웹 서버", "2009215674938", 404, OK, dash="5 4", dx=-90)
d.selfmsg("웹 서버", "base62 → zn9edcu", 460, ACC)
d.msg("웹 서버", "데이터베이스", "INSERT 한 행", 516, INFO)
d.msg("웹 서버", "브라우저", "tinyurl.com/zn9edcu", 556, OK, dash="5 4")

d.legend(H - 40, [("DB 경로", INFO), ("조회 결과 없음", WARN), ("ID 수신", OK), ("base62 변환", ACC)])
d.save("08-01.shorten-sequence.svg")
