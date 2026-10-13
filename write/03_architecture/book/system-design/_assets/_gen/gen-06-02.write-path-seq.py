# 타입 스펙: type-sequence — 쓰기 한 번이 커밋 로그에 남고 메모리 캐시에 들어간 뒤, 캐시가 차면 정렬된 채로 SSTable 이 된다.
# 사실 출처: 추출본 v2.txt 1862~1875행(커밋 로그에 영속 → 메모리 캐시에 저장 → 임계에 닿으면 SSTable 로 flush · SSTable 은 정렬된 <key, value> 목록),
#   Cassandra 5.0 storage-engine 문서(https://cassandra.apache.org/doc/5.0/cassandra/architecture/storage-engine.html): 커밋 로그 append-only · memtable 정렬 보관 · flush 로 불변 SSTable.
#   put(name, johnNewYork) 는 같은 절의 충돌 예에 쓰인 키·값을 그대로 쓴 예시다.
# Layout conventions: 레인 4개 폭 190, 메시지 stride 56, 디스크·메모리 구분은 레인 소제목으로. 모든 좌표 4의 배수.
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

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))


W, H = 960, 480
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 06-02 §6",
          "쓰기는 로그에 남고 메모리에 앉았다가 디스크 파일이 된다",
          "응답에 필요한 일은 순차 기록과 메모리 삽입이고, 정렬된 파일 쓰기는 캐시가 찰 때 한꺼번에 일어난다.",
          "커밋 로그 → 메모리 캐시 → SSTable")

d.lanes([("클라이언트", "쓰기 요청"),
         ("커밋 로그", "디스크 · 추가만"),
         ("메모리 캐시", "정렬 보관"),
         ("SSTable", "디스크 · 불변")], lane_w=180)
d.rails(396)

d.msg("클라이언트", "커밋 로그", "append", 216, INFO, sub="put(name, johnNewYork)")
d.msg("클라이언트", "메모리 캐시", "put", 280, OK, sub="put(name, johnNewYork)", lx=470)
d.msg("메모리 캐시", "SSTable", "flush", 352, ACC, sub="임계 도달 · 정렬된 <key, value>")

d.legend(H - 56, [("영속 기록", INFO), ("메모리 삽입", OK), ("디스크 파일 생성", ACC)])
d.save("06-02.write-path-seq.svg")
