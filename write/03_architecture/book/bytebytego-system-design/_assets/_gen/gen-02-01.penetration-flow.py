# 타입 스펙: type-sequence — 없는 키 user:404 하나가 방어 없음·널 캐시·블룸 필터 세 경로에서 어디까지 가는지 보이는 왕복. 레인 4(블룸 필터·앱·캐시·DB), 메시지 9.
# 사실 출처: 추출본 v1.txt 1683~1721행과 PDF 쪽 69 그림(존재하지 않는 키는 캐시와 DB 에 모두 없어 요청마다 DB 에 닿음 · 널 값을 짧은 TTL 로 캐시 · 블룸 필터가 없다고 답하면 캐시와 DB 를 거치지 않음),
#   redis.io Bloom filter 문서(없음은 보장하고 있음은 추정, 문서 기준 Redis 8.0 에 포함). user:404 · 사용자 1·2·3 은 이 편이 정한 예시 값이고 bloom-bits 도식과 같은 값이다.
# Layout conventions: 레인 폭 150, 호출·반환 한 쌍의 stride 72(호출 y, 반환 y+28), 그룹 구분선 3, 그룹 사이 간격 76. 모든 좌표 4의 배수.
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

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, f=0.5):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        s.t(x1 + (x2 - x1) * f, y - 9, label, 12, c, _kr(label), "middle", 600)

    def state(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))

    def group(s, y, label):
        s.line(12, y, s.w - 48, y, RULE, 0.8, "4 4")
        s.t(12, y + 20, label, 12, SOFT, KR, "start", 600)


W, H = 960, 692
d = SeqKR(W, H, "BYTEBYTEGO · 02-01 §2",
          "없는 키는 캐시도 못 막아 DB 까지 간다",
          "user:404 를 조회하면 방어 없이는 요청마다 SELECT 가 나가고, 널 캐시와 블룸 필터는 DB 앞에서 끊습니다",
          "DB 에는 사용자 1·2·3 만 있습니다")
BF, APP, CA, DB = "블룸 필터", "앱", "캐시", "DB"
d.lanes([(BF, "user:1·2·3 등록"), (APP, "user:404 요청"), (CA, "키 없음"), (DB, "사용자 1·2·3")], 100, 150)
d.rails(H - 80)

# 1. 방어 없음 — 캐시 miss 뒤 DB 까지 간다
d.group(168, "방어 없음")
d.msg(APP, CA, "GET user:404", 204)
d.msg(CA, APP, "miss", 232, MUTED, "ar", "5 4")
d.msg(APP, DB, "SELECT id=404", 276, BAD, "bad", f=0.3)
d.msg(DB, APP, "0 rows", 304, BAD, "bad", "5 4", f=0.3)
d.state(DB, "DB 쿼리 1회", 328, BAD)

# 2. 널 캐시 — 없다는 답을 짧은 TTL 로 저장하면 다음 요청은 캐시에서 끝난다
d.group(364, "널 캐시")
d.msg(APP, CA, "SET user:404=null", 400)
d.state(CA, "짧은 TTL", 400, MUTED, 100)
d.msg(APP, CA, "GET user:404", 452)
d.msg(CA, APP, "null", 480, OK, "ok", "5 4")
d.state(DB, "DB 쿼리 0회", 480, OK)

# 3. 블룸 필터 — 필터가 없다고 답하면 캐시와 DB 에 가지 않는다
d.group(524, "블룸 필터")
d.msg(APP, BF, "조회 user:404", 560, ACC, "acc")
d.msg(BF, APP, "없음", 588, OK, "ok", "5 4")
d.state(CA, "캐시·DB 도달 없음", 592, OK)

d.legend(H - 56, [("DB 까지 간 요청", BAD), ("DB 앞에서 끊김", OK), ("필터에 묻는 요청", ACC)])
d.save("02-01.penetration-flow.svg")
