# 06-05 §1 — 다중 리더 환경에서 두 사용자의 동시 쓰기 충돌과 LWW(last write wins)에 의한 데이터 손실 시퀀스.
# 사실 출처: 06-05 §1(L30~L34), DDIA 2판 6장 Figure 6-9 및 "Last write wins (discarding concurrent writes)" (PDF p.22~23).
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 656
H = LEG + 56

class LwwSeq(Seq):
    def lanes(self, names, y0=104, lane_w=160):
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
        self.t(mx, y - 8, label, 11, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 11, MUTED, KR, "middle")

    def seq_self(self, a, label, y, c=MUTED, sub=None, to_left=False):
        x = self.LX[a]
        if to_left:
            self.path(f"M {x - 10} {y - 10} L {x - 52} {y - 10} L {x - 52} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            self.t(x - 60, y - 4, label, 11, c, KR, "end", 600)
            if sub:
                self.t(x - 60, y + 14, sub, 11, MUTED, KR, "end")
        else:
            self.path(f"M {x + 10} {y - 10} L {x + 52} {y - 10} L {x + 52} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            self.t(x + 60, y - 4, label, 11, c, KR, "start", 600)
            if sub:
                self.t(x + 60, y + 14, sub, 11, MUTED, KR, "start")

    def state_box(self, a, txt, y, c=OK, w=110):
        x = self.LX[a]
        self.box(x - w / 2, y - 11, w, 22, PAPER2, c, 1.1, r=4)
        self.t(x, y + 4, txt, 11, c, MONO if not any("가" <= ch <= "힣" for ch in txt) else KR, "middle", 600)

d = LwwSeq(W, H, "06-05 · LWW CONCURRENT WRITE & DATA LOSS", "LWW 동시 쓰기와 조용한 데이터 손실",
           "다중 리더 환경에서 타임스탬프 기반 LWW가 일관 수렴을 달성하는 과정과 조용한 데이터 유실을 보인다.",
           "동시 로컬 쓰기 접수 · 비동기 복제 교환 · 최대 타임스탬프 채택과 폐기 · 데이터 손실")

lanes = [
    ("사용자 1", "클라이언트 1"),
    ("리더 1", "사용자 1의 로컬 리더"),
    ("리더 2", "사용자 2의 로컬 리더"),
    ("사용자 2", "클라이언트 2"),
]
LX = d.lanes(lanes, y0=104, lane_w=160)
d.rails(572)

# 1단계: 로컬 동시 쓰기
d.tone(24, 160, W - 48, 26, INFO, 4, "14", 1.0)
d.t(W / 2, 177, "1단계: 동시 쓰기 — 사용자 1과 2가 각자 로컬 리더에 독립적으로 갱신 요청", 12, INK, KR, "middle", 600)

d.seq_msg("사용자 1", "리더 1", "쓰기: title = 'B'", 212, INFO, sub="타임스탬프가 더 큼")
d.seq_msg("사용자 2", "리더 2", "쓰기: title = 'C'", 212, INFO, sub="타임스탬프가 더 작음")

d.state_box("리더 1", "title = 'B'", 252, OK, 100)
d.state_box("리더 2", "title = 'C'", 252, OK, 100)

d.seq_msg("리더 1", "사용자 1", "OK (로컬 리더에 적용)", 288, OK, dash="4 4")
d.seq_msg("리더 2", "사용자 2", "OK (로컬 리더에 적용)", 288, OK, dash="4 4")

# 2단계: 비동기 복제 및 충돌 판정
d.tone(24, 328, W - 48, 26, INFO, 4, "14", 1.0)
d.t(W / 2, 345, "2단계: 비동기 복제 — 두 리더 간 복제 로그 교환 및 타임스탬프 비교", 12, INK, KR, "middle", 600)

# 리더 1 -> 리더 2 복제 및 판정
d.seq_msg("리더 1", "리더 2", "복제: title = 'B'", 384, ACC, sub="타임스탬프와 함께 전달")
d.seq_self("리더 2", "'B' 의 타임스탬프가 더 큼", 416, OK, sub="'B' 가 이김 · 'C' 를 덮어씀")
d.state_box("리더 2", "title = 'B' (갱신)", 448, OK, 120)

# 리더 2 -> 리더 1 복제 및 판정
d.seq_msg("리더 2", "리더 1", "복제: title = 'C'", 484, BAD, sub="타임스탬프와 함께 전달")
d.seq_self("리더 1", "'C' 의 타임스탬프가 더 작음", 516, BAD, sub="'C' 를 조용히 버림", to_left=True)
d.state_box("리더 1", "title = 'B' (유지)", 548, OK, 120)

# 3단계: 최종 결과 및 대가
d.tone(24, 588, W - 48, 44, ACC, 4, "18", 1.2)
d.t(W / 2, 606, "결과: 두 리더 모두 title = 'B' 로 일관 상태에 수렴", 12, INK, KR, "middle", 600)
d.t(W / 2, 622, "대가: 사용자 2의 쓰기 'C' 가 조용히 버려지는 데이터 손실", 11, ACC, KR, "middle", 600)

d.legend(LEG, [("로컬 쓰기 접수", INFO), ("타임스탬프 우세 (채택)", OK), ("타임스탬프 열세 (폐기)", BAD), ("데이터 손실 (focal)", ACC)])
d.save("06-05.conflict-resolution.svg")
