# 08-01 §4 — 동시 실행 트랜잭션의 카운터 증분 경쟁 조건과 갱신 손실(lost update) 시퀀스.
# 사실 출처: 08-01 §4(L47~L53), 원서 Ch.8 Isolation(PDF p.6) 및 Figure 8-1(PDF p.6, 카운터 42에서 44 기대했으나 43으로 갱신 손실)
# 타입 스펙: type-sequence
# 검증(10-31 cc-ddia-dverify08): Fig 8-1(PDF p.6) 에는 트랜잭션·커밋이 없고 get/set/OK 뿐이라 "커밋" 라벨을 "쓰기" 로
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 652
H = LEG + 56

class CompSeq(Seq):
    def lanes(self, names, y0=104, lane_w=200):
        self.LX = {}; n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 11, MUTED, KR, "middle")

    def seq_self(self, a, label, y, c=MUTED, sub=None, to_left=False):
        x = self.LX[a]
        if to_left:
            self.path(f"M {x - 10} {y - 10} L {x - 58} {y - 10} L {x - 58} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            self.t(x - 68, y - 4, label, 12, c, MONO, "end", 600)
            if sub:
                self.t(x - 68, y + 15, sub, 11, MUTED, KR, "end")
        else:
            self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            self.t(x + 68, y - 4, label, 12, c, MONO, "start", 600)
            if sub:
                self.t(x + 68, y + 15, sub, 11, MUTED, KR, "start")

d = CompSeq(W, H, "08-01 · §4 ISOLATION & LOST UPDATE", "동시 카운터 증분 경쟁 조건과 갱신 손실 시퀀스",
            "두 클라이언트가 동시에 카운터 42를 읽고 각각 1을 더해 쓸 때 격리성 부재로 갱신이 손실되는 과정.",
            "동시 카운터 조회 · 로컬 증분 계산 · 같은 값 덮어쓰기 · 최종 값 43 갱신 손실")

lx = d.lanes([
    ("클라이언트 1", "Client 1"),
    ("데이터베이스", "초기 counter = 42"),
    ("클라이언트 2", "Client 2"),
], y0=104, lane_w=200)

d.rails(608)

# 1. 클라이언트 1: GET counter
d.seq_msg("클라이언트 1", "데이터베이스", "GET counter", 168, INFO, "info", sub="카운터 값 조회", is_mono=True)
d.seq_msg("데이터베이스", "클라이언트 1", "42", 216, INFO, "info", sub="현재 값 42 반환", is_mono=True)

# 2. 클라이언트 2: GET counter (동시 조회)
d.seq_msg("클라이언트 2", "데이터베이스", "GET counter", 264, INFO, "info", sub="동시 카운터 값 조회", is_mono=True)
d.seq_msg("데이터베이스", "클라이언트 2", "42", 312, INFO, "info", sub="현재 값 42 반환 (동일 값)", is_mono=True)

# 3. 클라이언트 1 로컬 연산 및 쓰기
d.seq_self("클라이언트 1", "[42 + 1 = 43]", 356, INFO, sub="로컬 증분 계산", to_left=False)
d.seq_msg("클라이언트 1", "데이터베이스", "SET counter = 43", 400, OK, "ok", sub="1차 쓰기", is_mono=True)
d.seq_msg("데이터베이스", "클라이언트 1", "OK", 448, OK, "ok", sub="쓰기 성공 (DB=43)", is_mono=True)

# 4. 클라이언트 2 로컬 연산 및 덮어쓰기
d.seq_self("클라이언트 2", "[42 + 1 = 43]", 492, WARN, sub="로컬 증분 계산", to_left=True)
d.seq_msg("클라이언트 2", "데이터베이스", "SET counter = 43", 536, WARN, "warn", sub="2차 쓰기 (덮어쓰기)", is_mono=True)
d.seq_msg("데이터베이스", "클라이언트 2", "OK", 584, WARN, "warn", sub="쓰기 성공 (DB=43)", is_mono=True)

# 5. 최종 이상 현상 박스
d.tone(lx["데이터베이스"] - 140, 616, 280, 24, ACC, 4, "18", 1.4)
d.t(lx["데이터베이스"], 632, "최종 counter = 43 (기대치 44 · 갱신 손실)", 11, ACC, KR, "middle", 600)

d.legend(LEG, [
    ("갱신 손실 (focal)", ACC),
    ("첫 쓰기", OK),
    ("조회·연산", INFO),
    ("덮어쓰기", WARN),
])

d.save("08-01.isolation-race-condition.svg")
