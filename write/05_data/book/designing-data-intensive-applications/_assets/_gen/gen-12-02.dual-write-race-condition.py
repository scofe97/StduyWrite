# 12-02 §1 — 듀얼 라이트에서 두 쓰기가 엇갈려(interleaved) 도착해 생기는 영구 불일치 레이스 컨디션 시퀀스.
# 원서 Figure 12-4(p.19): 레인 Client 1·Database·Search index·Client 2, DB 는 A→B, 인덱스는 B→A. 원서는 원인을 "unlucky timing" 으로만 적어 네트워크 지연을 라벨에 넣지 않는다.
# 사실 출처: 12-02 §1(L29~L33), DDIA 2판 Ch.12 Figure 12-4(PDF p.19) — Client 1, Database, Search index, Client 2 레인,
#   Client 1 은 X=A, Client 2 는 X=B 동시 쓰기, DB 는 A→B, 검색 인덱스는 B→A 도착으로 불일치.
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 712
H = LEG + 52

class DualWriteSeq(Seq):
    def lanes(self, names, xs, y0=104, lane_w=130):
        self.LX = {}
        for (nm, sub), x in zip(names, xs):
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False, lx=None, sub_c=MUTED):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 11, sub_c, KR, "middle")

    def chip_state(self, a, txt, y, c):
        x = self.LX[a]
        w = len(txt) * 9.5 + 18
        self.box(x - w / 2, y - 11, w, 22, PAPER, c, 1.0, r=4)
        self.t(x, y + 4, txt, 11, c, KR, "middle", 600)

d = DualWriteSeq(W, H, "12-02 · §1 DUAL WRITE RACE CONDITION", "듀얼 라이트 레이스 컨디션과 영구 불일치",
                 "두 클라이언트의 쓰기가 데이터베이스와 검색 인덱스에 서로 다른 순서로 도착해 두 시스템이 영구적으로 불일치한다.",
                 "Client 1 쓰기 (X=A) · Client 2 쓰기 (X=B) · DB 순서 (A→B) · 검색 인덱스 순서 (B→A) · 영구 불일치")

lx = d.lanes([
    ("클라이언트 1", "Client 1"),
    ("데이터베이스", "OLTP DB"),
    ("검색 인덱스", "Search Index"),
    ("클라이언트 2", "Client 2"),
], [105, 315, 565, 775], y0=104, lane_w=130)

d.rails(600)

# 1. Client 1 -> DB: set X = A
d.seq_msg("클라이언트 1", "데이터베이스", "set X = A", 172, INFO, "info", sub="동시 쓰기 요청 1", is_mono=True)
d.seq_msg("데이터베이스", "클라이언트 1", "OK", 212, OK, "ok", dash="4,3", is_mono=True)
d.chip_state("데이터베이스", "DB: X = A", 238, INFO)

# 2. Client 2 -> DB: set X = B
d.seq_msg("클라이언트 2", "데이터베이스", "set X = B", 280, WARN, "warn", sub="동시 쓰기 요청 2 (DB에 2번째 도착)", is_mono=True, lx=545)
d.seq_msg("데이터베이스", "클라이언트 2", "OK", 320, OK, "ok", dash="4,3", is_mono=True, lx=545)
d.chip_state("데이터베이스", "DB 최종값: X = B", 346, WARN)

# 3. Client 2 -> Search Index: set X = B
d.seq_msg("클라이언트 2", "검색 인덱스", "set X = B", 388, WARN, "warn", sub="인덱스에 1번째 도착", is_mono=True)
d.seq_msg("검색 인덱스", "클라이언트 2", "OK", 428, OK, "ok", dash="4,3", is_mono=True)
d.chip_state("검색 인덱스", "인덱스: X = B", 454, WARN)

# 4. Client 1 -> Search Index: set X = A (인덱스에 2번째 도착)
d.seq_msg("클라이언트 1", "검색 인덱스", "set X = A", 496, INFO, "info", sub="인덱스에 2번째 도착", is_mono=True, lx=335, sub_c=BAD)
d.seq_msg("검색 인덱스", "클라이언트 1", "OK", 536, OK, "ok", dash="4,3", is_mono=True, lx=335)
d.chip_state("검색 인덱스", "인덱스 최종값: X = A", 562, BAD)

# 하단 판정 패널
d.tone(28, 620, W - 56, 62, BAD, 6, "14", 1.2)
d.t(W / 2, 644, "영구적 데이터 불일치: DB 최종값 X = B  ≠  검색 인덱스 최종값 X = A", 13, BAD, KR, "middle", 600)
d.t(W / 2, 666, "저장소마다 다른 쓰기 순서 · 오류 없는 영구 불일치", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("클라이언트 1 (X=A)", INFO),
    ("클라이언트 2 (X=B)", WARN),
    ("정상 응답 (OK)", OK),
    ("순서 역전·불일치", BAD),
])

d.save("12-02.dual-write-race-condition.svg")
