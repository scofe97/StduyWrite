# 05-05 §1 — durable execution의 WAL 기반 exactly-once 재실행(Replay) 메커니즘.
# 사실 출처: 05-05 본문 §1(L32~L36) · 원서 Durable Execution and Workflows(PDF p.28~29, Figure 5-7·Example 5-5) — 사기 탐지→카드 차감→은행 입금, 모든 RPC·상태 변경을 WAL 같은 지속 저장소에 로깅, 재실행 때 성공한 호출은 호출하는 척 이전 결과 반환.
# 원서·본문에 엔드포인트·금액·응답 코드가 없으므로 도식에도 두지 않는다. 실패 지점은 본문 L36 의 "카드 청구는 됐는데 은행 입금은 안 된 상태"를 따른다.
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 696
H = LEG + 56

def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in txt)


class DurableSeq(Seq):
    # dd.Seq.lanes 는 lane 부제를 MONO 로 찍는다. 한글이 든 부제는 KR 로 쓴다.
    def lanes(self, names, y0=104, lane_w=210):
        self.LX = {}; n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, KR if _hangul(sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 12, MUTED, KR, "middle")

    def seq_self(self, a, label, y, c=MUTED, sub=None):
        x = self.LX[a]
        self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        self.t(x + 68, y - 4, label, 12, c, KR, "start", 600)
        if sub:
            self.t(x + 68, y + 15, sub, 12, MUTED, KR, "start")

d = DurableSeq(W, H, "05-05 §1 · DURABLE EXECUTION", "durable execution 크래시 복구와 Replay 시퀀스",
               "워크플로우 엔진이 모든 RPC·상태 변경을 WAL 같은 지속 저장소에 로깅하고, 실패한 태스크를 재실행할 때 성공한 호출은 이전 결과로 대신해 exactly-once 의미론을 제공한다.",
               "호출과 로깅 · 입금 전 실패 · 재실행 때 성공한 호출 건너뜀 · 남은 호출 실행")

lanes = [
    ("워크플로우 엔진", "Temporal · Restate"),
    ("지속 저장소", "write-ahead log 같은 로그"),
    ("외부 서비스", "사기 탐지 · 카드 · 은행"),
]
LX = d.lanes(lanes, y0=104, lane_w=196)
d.rails(664)

# 1. 태스크 1 (사기 탐지)
d.seq_msg("워크플로우 엔진", "외부 서비스", "1: 사기 탐지 호출", 176, INFO, "info", sub=None, is_mono=False)
d.seq_msg("외부 서비스", "워크플로우 엔진", "결과 반환", 212, MUTED, "ar", dash="4 3", sub=None, is_mono=False)
d.seq_msg("워크플로우 엔진", "지속 저장소", "RPC 결과 로깅", 248, INFO, "info", sub="호출·상태 변경을 순서대로 기록", is_mono=False)

# 2. 태스크 2 (카드 청구)
d.seq_msg("워크플로우 엔진", "외부 서비스", "2: 카드 차감", 288, INFO, "info", sub=None, is_mono=False)
d.seq_msg("외부 서비스", "워크플로우 엔진", "결과 반환", 324, MUTED, "ar", dash="4 3", sub=None, is_mono=False)
d.seq_msg("워크플로우 엔진", "지속 저장소", "RPC 결과 로깅", 360, INFO, "info", sub="카드는 이미 청구됨", is_mono=False)

# 3. 크래시 프레임 (FAIL)
fx1 = LX["워크플로우 엔진"] - 98
fx2 = LX["외부 서비스"] + 98
fw = fx2 - fx1

d.box(fx1, 392, fw, 44, PAPER2, BAD, 1.0)
d.chip(440, 414, "실행 중 실패 · 카드 청구 뒤, 은행 입금 전", BAD, 12)

# 4. 복구 및 Replay 재생
d.seq_msg("워크플로우 엔진", "지속 저장소", "재실행 · 로그 읽기", 460, INFO, "info", sub=None, is_mono=False)
d.seq_msg("지속 저장소", "워크플로우 엔진", "성공한 호출 1 · 2 의 결과", 496, MUTED, "ar", dash="4 3", sub=None, is_mono=False)

# 5. 캐시 결과 사용 및 RPC 생략
d.chip(LX["워크플로우 엔진"] + 110, 530, "1 · 2 는 호출하는 척 · 이전 결과 반환", OK, 12)

# 6. 중단된 태스크 3 실행 (은행 입금 — Focal ACC)
d.seq_msg("워크플로우 엔진", "외부 서비스", "3: 은행 입금", 566, ACC, "acc", sub="실패 전 못 한 호출만 실제로 보냄", is_mono=False)
d.seq_msg("외부 서비스", "워크플로우 엔진", "결과 반환", 608, MUTED, "ar", dash="4 3", sub=None, is_mono=False)
d.seq_msg("워크플로우 엔진", "지속 저장소", "RPC 결과 로깅", 644, OK, "ok", sub="결제를 정확히 한 번 처리", is_mono=False)

d.legend(LEG, [
    ("호출·로깅", INFO),
    ("실행 중 실패", BAD),
    ("호출 건너뜀·이전 결과", OK),
    ("남은 호출 실행 (exactly-once)", ACC)
])
d.save("05-05.durable-execution.svg")
