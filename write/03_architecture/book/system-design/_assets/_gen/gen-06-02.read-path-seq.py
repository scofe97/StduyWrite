# 타입 스펙: type-sequence — 같은 키 name 을 두 번 읽는다. 첫 읽기는 메모리 캐시가 답하고, 캐시가 비운 뒤의 둘째 읽기는 블룸 필터가 후보 SSTable 을 좁힌다.
# 사실 출처: 추출본 v2.txt 1876~1895행(메모리 캐시 확인 → 없으면 블룸 필터 → 키를 담았을 수 있는 SSTable → 결과 → 클라이언트),
#   Cassandra 5.0 bloom filters 문서(https://cassandra.apache.org/doc/5.0/cassandra/managing/operating/bloom_filters.html): 블룸 필터는 "확실히 없다"와 "있을 수 있다" 둘 중 하나만 답한다.
#   get(name) 과 johnNewYork 는 같은 편 §6 쓰기 경로 예시의 키·값.
# Layout conventions: 레인 4개 폭 190, 메시지 stride 44~52, 두 읽기 사이 구분선. 모든 좌표 4의 배수.
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
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
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


W, H = 960, 656
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 06-02 §7",
          "메모리에 없으면 블룸 필터가 열 SSTable 을 좁힌다",
          "메모리 캐시가 답하면 디스크는 건드리지 않고, 못 답하면 블룸 필터를 거쳐 후보 파일만 읽는다.",
          "같은 키 name 을 두 번 읽는다")

d.lanes([("클라이언트", "읽기 요청"),
         ("메모리 캐시", "정렬 보관"),
         ("블룸 필터", "SSTable 마다"),
         ("SSTable", "디스크 · 불변")], lane_w=180)
d.rails(592)

d.t(12, 188, "읽기 1 · 적중", 13, SOFT, KR, "start", 600)
d.msg("클라이언트", "메모리 캐시", "get(name)", 224, MUTED)
d.msg("메모리 캐시", "클라이언트", "johnNewYork", 272, OK, dash="5 4", sub="디스크 접근 없음")

d.line(12, 324, W - 48, 324, RULE, 0.8, "3 6")
d.t(12, 344, "읽기 2 · 미스", 13, SOFT, KR, "start", 600)
d.msg("클라이언트", "메모리 캐시", "get(name)", 380, MUTED)
d.msg("메모리 캐시", "블룸 필터", "없음 → 확인", 436, WARN)
d.msg("블룸 필터", "SSTable", "있을 수 있는 파일", 492, INFO)
d.msg("SSTable", "클라이언트", "johnNewYork", 556, ACC, dash="5 4")

d.legend(H - 40, [("메모리 적중", OK), ("메모리 미스", WARN), ("후보 좁히기", INFO), ("디스크 응답", ACC)])
d.save("06-02.read-path-seq.svg")
