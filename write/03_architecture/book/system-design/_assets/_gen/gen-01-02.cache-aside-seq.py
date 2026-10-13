# 타입 스펙: type-sequence — 같은 키 myKey 를 두 번 읽는 요청 둘. 첫 요청은 캐시 미스 뒤 DB 를 거쳐 캐시에 채우고, 둘째 요청은 캐시 적중으로 끝난다.
# 사실 출처: 추출본 v2.txt 234~237행(캐시 확인 → 없으면 DB 질의 → 캐시 저장 → 응답)·PDF 15쪽 코드 조각(cache.set('myKey','hi there',3600*SECONDS)),
#   memcached 1.6.45 doc/protocol.txt L209(저장 명령 문법 set <key> <flags> <exptime> <bytes>)·L243(exptime)·L275(STORED)·L308(VALUE <key> <flags> <bytes>) —
#   https://github.com/memcached/memcached/blob/1.6.45/doc/protocol.txt . 'hi there' 는 8바이트, flags 는 0 으로 둔 값. 미스 응답 END 는 같은 문서의 get 응답 규칙.
# Layout conventions: 레인 3개 폭 210, 메시지 stride 44, 요청 둘 사이 구분선. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO


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
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))


W, H = 960, 688
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 01-02 §1",
          "같은 키를 두 번 읽으면 두 번째는 DB 를 건너뛴다",
          "미스 뒤에는 DB 에서 읽어 캐시에 3600초 동안 채우고, 같은 키의 다음 요청은 캐시가 답한다.",
          "get 이 END 로 끝나면 미스, VALUE 가 오면 적중")

d.lanes([("웹 서버", "cache-aside"),
         ("캐시", "memcached"),
         ("데이터베이스", "원본")])
d.rails(624)

d.t(12, 188, "요청 1 · 미스", 13, SOFT, KR, "start", 600)
d.msg("웹 서버", "캐시", "get myKey", 216, MUTED)
d.msg("캐시", "웹 서버", "END", 260, WARN, dash="5 4", sub="키 없음")
d.msg("웹 서버", "데이터베이스", "DB 질의", 316, INFO)
d.msg("데이터베이스", "웹 서버", "결과 행", 360, INFO, dash="5 4")
d.msg("웹 서버", "캐시", "set myKey 0 3600 8", 416, OK, sub="exptime 3600초")
d.msg("캐시", "웹 서버", "STORED", 476, OK, dash="5 4")

d.line(12, 516, W - 48, 516, RULE, 0.8, "3 6")
d.t(12, 536, "요청 2 · 적중", 13, SOFT, KR, "start", 600)
d.msg("웹 서버", "캐시", "get myKey", 568, MUTED)
d.msg("캐시", "웹 서버", "VALUE myKey 0 8", 612, ACC, dash="5 4")

d.legend(H - 40, [("캐시 미스", WARN), ("DB 경로", INFO), ("캐시 채움", OK), ("적중", ACC)])
d.save("01-02.cache-aside-seq.svg")
