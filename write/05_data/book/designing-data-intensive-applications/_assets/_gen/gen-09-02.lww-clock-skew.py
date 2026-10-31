# 09-02 §3 — 다중 리더 복제에서 클럭 스큐로 인한 타임스탬프 역전과 LWW 데이터 유실 시퀀스.
# 사실 출처: 09-02 §3(L49~L57), 원서 Ch.9 Timestamps for ordering events & Figure 9-3(p.160~164, A의 x=1 t=42.004 s, B의 x=2 t=42.003 s 역전)
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 608
H = LEG + 56

class LwwSeq(Seq):
    def custom_lanes(self, names, y0=104, lane_w=130):
        self.LX = {}
        n = len(names)
        x_first = 28 + lane_w / 2
        x_last = W - 28 - lane_w / 2
        span = x_last - x_first
        for i, (nm, sub, c) in enumerate(names):
            x = x_first + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 46, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 38, sub, 11, c, KR if any('가' <= ch <= '힣' for ch in sub) else MONO)
        self.lane_top = y0 + 46
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.4, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 11.5, MUTED, KR, "middle")

    def seq_self(self, a, label, y, c=MUTED, sub=None, to_left=False, is_mono=False):
        x = self.LX[a]
        dx = -46 if to_left else 46
        d_end = -12 if to_left else 12
        self.path(f"M {x + (10 if not to_left else -10)} {y - 10} L {x + dx} {y - 10} L {x + dx} {y + 10} L {x + d_end} {y + 10}", c, 1.3, m="ar")
        tx = x + dx + (-8 if to_left else 8)
        align = "end" if to_left else "start"
        self.t(tx, y - 4, label, 11.5, c, MONO if is_mono else KR, align, 600)
        if sub:
            self.t(tx, y + 15, sub, 11.5, MUTED, KR, align)

d = LwwSeq(W, H, "09-02 · §3 TIMESTAMP ORDERING RISK", "다중 리더 쓰기의 타임스탬프 역전과 LWW 유실 시퀀스",
           "클라이언트 B의 x=2 증분이 인과적으로 나중이지만 클럭 스큐로 작은 타임스탬프가 붙어 조용히 유실되는 과정.",
           "선행 쓰기 x=1 · 후행 증분 x=2 · 클럭 스큐 역전 · LWW 충돌 해소 오판단 · 데이터 유실")

lx = d.custom_lanes([
    ("클라이언트 A", "Client A", INFO),
    ("노드 1", "Node 1", INFO),
    ("노드 3", "Node 3 (스큐 3 ms 이하)", WARN),
    ("클라이언트 B", "Client B", WARN),
    ("노드 2", "Node 2", BAD),
], y0=104, lane_w=130)

d.rails(566)

# 1. 클라이언트 A -> 노드 1: 쓰기 x = 1
d.seq_msg("클라이언트 A", "노드 1", "쓰기: x = 1", 168, INFO, "info", sub="선행 쓰기 요청")

# 2. 노드 1 로컬 타임스탬프 부여
d.seq_self("노드 1", "t = 42.004 s", 212, INFO, sub="벽시계 타임스탬프 부여", to_left=False, is_mono=True)

# 3. 노드 1 -> 노드 3: 복제
d.seq_msg("노드 1", "노드 3", "복제: x = 1", 256, OK, "ok", sub="t = 42.004 s 전달")

# 4. 클라이언트 B -> 노드 3: x=1 읽고 x=2 로 증분 쓰기
d.seq_msg("클라이언트 B", "노드 3", "증분: x = 2", 304, WARN, "warn", sub="인과적 후행 쓰기")

# 5. 노드 3 로컬 타임스탬프 부여 (클럭 스큐로 인해 42.003 s)
d.seq_self("노드 3", "t = 42.003 s", 348, WARN, sub="클럭 스큐로 과거 시각 기록", to_left=True, is_mono=True)

# 6. 노드 1 -> 노드 2 복제
d.seq_msg("노드 1", "노드 2", "복제: x = 1 (42.004 s)", 400, OK, "ok", sub="노드 1 쓰기 전파")

# 7. 노드 3 -> 노드 2 복제
d.seq_msg("노드 3", "노드 2", "복제: x = 2 (42.003 s)", 452, WARN, "warn", sub="노드 3 쓰기 전파")

# 8. 노드 2 LWW 비교 연산
d.seq_self("노드 2", "LWW: 42.004 > 42.003", 504, BAD, sub="큰 타임스탬프 x=1 선택", to_left=True, is_mono=True)

# 9. 노드 2 최종 상태 박스 (focal) - 캔버스 우측 28px 여백 준수
box_w = 230
box_x = W - 28 - box_w
d.tone(box_x, 540, box_w, 26, ACC, 4, "18", 1.4)
d.t(box_x + box_w / 2, 557, "x = 2 유실 · x = 1 보존 (역전)", 11.5, ACC, KR, "middle", 600)

d.legend(LEG, [
    ("데이터 유실 (focal)", ACC),
    ("선행 쓰기 A", INFO),
    ("후행 쓰기 B", WARN),
    ("정상 복제", OK),
    ("LWW 오판단", BAD),
])

d.save("09-02.lww-clock-skew.svg")
