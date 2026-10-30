# 04-03 §2 — B-tree 제자리 덮어쓰기의 크래시 손상을 방지하는 WAL 선행 기록과 크래시 후 복구 시퀀스.
# 사실 출처: 04-03 본문 §2(L44~L50) — 제자리 덮어쓰기 위험, torn page, WAL append-only 기록, fsync 내구성, 크래시 후 로그 재생 일관 상태 복원.
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, KR, MONO

W = 880
LEG = 584
H = LEG + 56

class WalSeq(Seq):
    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 11, MUTED, KR, "middle")

    def seq_self(self, a, label, y, c=MUTED, sub=None):
        x = self.LX[a]
        self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        self.t(x + 68, y - 4, label, 12, c, KR, "start", 600)
        if sub:
            self.t(x + 68, y + 15, sub, 11, MUTED, KR, "start")

d = WalSeq(W, H, "04-03 · WRITE-AHEAD LOG & CRASH RECOVERY", "B-tree WAL 선행 기록과 크래시 복구 시퀀스",
           "페이지 덮어쓰기 전 WAL에 먼저 기록해 내구성을 얻고, 비정상 크래시 시 로그 재생으로 트리를 복구한다.",
           "쓰기 요청 · WAL 선행 기록(fsync) · 버퍼 수정 · 크래시 발생 · 로그 재생 복구")

lanes = [
    ("애플리케이션", "Client / App"),
    ("B-tree 엔진", "메모리 버퍼"),
    ("디스크 WAL", "Append-only Log"),
    ("디스크 페이지", "Data File · Disk"),
]
LX = d.lanes(lanes, y0=104, lane_w=176)
d.rails(552)

# 1. 쓰기 요청
d.seq_msg("애플리케이션", "B-tree 엔진", "쓰기 요청 (키 갱신·분할)", 174, INFO, "info", sub="1단계: 수정 요청 전달", is_mono=False)

# 2. WAL 선행 기록 (내구성 확보 - FOCAL)
d.seq_msg("B-tree 엔진", "디스크 WAL", "WAL append (수정 내역)", 212, ACC, "acc", sub="2단계: 트리 수정 전 선행 기록", is_mono=False)
d.seq_msg("디스크 WAL", "B-tree 엔진", "fsync 플러시 완료", 256, OK, "ok", dash="4 3", sub="내구성 확보 (disk write)", is_mono=False)

# 3. 메모리 버퍼 갱신 및 응답
d.seq_self("B-tree 엔진", "버퍼 풀 페이지 수정", 298, INFO, sub="메모리에 잠시 버퍼링 (디스크 쓰기 지연)")
d.seq_msg("B-tree 엔진", "애플리케이션", "쓰기 성공 반환", 342, MUTED, "ar", dash="4 3", sub=None, is_mono=False)

# 4. 크래시 프레임 (FAIL / RECOVERY)
fx1 = LX["B-tree 엔진"] - 80
fx2 = LX["디스크 페이지"] + 80
fw = fx2 - fx1

d.box(fx1, 372, fw, 172, PAPER2, BAD, 1.0)
d.box(fx1, 372, 80, 20, PAPER, BAD, 1.0)
d.t(fx1 + 40, 386, "CRASH", 10, BAD, MONO, "middle", 600)

# 크래시 표시선
d.line(fx1 + 10, 412, fx1 + fw - 10, 412, BAD, 1.0, dash="4 3")
d.t(fx1 + fw / 2, 402, "비정상 종료 (메모리 버퍼 유실 · 디스크 페이지 미반영)", 12, BAD, KR, "middle")

# 복구 재생
d.seq_msg("B-tree 엔진", "디스크 WAL", "WAL 로그 재생", 438, INFO, "info", sub="로그 순서대로 다시 읽기", is_mono=False)
d.seq_msg("디스크 WAL", "B-tree 엔진", "로그 레코드 전달", 486, MUTED, "ar", dash="4 3", sub=None, is_mono=False)
d.seq_msg("B-tree 엔진", "디스크 페이지", "페이지 복원 덮어쓰기", 522, OK, "ok", sub="고아 페이지 방지 및 일관 상태 복원", is_mono=False)

d.legend(LEG, [
    ("선행 기록 (내구성 확보)", ACC),
    ("복구 및 정상 반영", OK),
    ("비정상 크래시 발생", BAD),
    ("기본 제어 흐름", INFO)
])

d.save("04-03.wal-crash-recovery.svg")
