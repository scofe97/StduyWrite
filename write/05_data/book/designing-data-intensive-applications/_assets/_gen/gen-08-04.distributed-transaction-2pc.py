# 08-04 §2 — 2단계 커밋(2PC) 흐름, 커밋 포인트, 코디네이터 장애 시 의심 상태(in doubt) 블로킹 시퀀스.
# 사실 출처: 08-04 §2(L34~L43), 원서 Ch.8 Figure 8-13(PDF p.52 "A successful execution of 2PC") · Figure 8-14(PDF p.55 "The coordinator crashes after participants vote yes")
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 700
H = LEG + 56

class TwoPhaseSeq(Seq):
    def lanes(self, names, y0=104, lane_w=196):
        self.LX = {}
        n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 19, nm, 13, INK, KR, "middle", 600)
            self.t(x, y0 + 36, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
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

    def seq_self(self, a, label, y, c=MUTED, sub=None, to_left=False):
        x = self.LX[a]
        if to_left:
            self.path(f"M {x - 10} {y - 10} L {x - 48} {y - 10} L {x - 48} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            self.t(x - 56, y - 4, label, 12, c, KR, "end", 600)
            if sub:
                self.t(x - 56, y + 14, sub, 12, MUTED, KR, "end")
        else:
            self.path(f"M {x + 10} {y - 10} L {x + 48} {y - 10} L {x + 48} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            self.t(x + 56, y - 4, label, 12, c, KR, "start", 600)
            if sub:
                self.t(x + 56, y + 14, sub, 12, MUTED, KR, "start")

    def seq_state(self, a, txt, y, c, w=156):
        x = self.LX[a]
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 5, txt, 12, c, KR, "middle", 600)

d = TwoPhaseSeq(W, H, "08-04 §2 · TWO-PHASE COMMIT & IN-DOUBT", "2단계 커밋 프로토콜과 코디네이터 장애 의심 상태",
                "1단계 준비 질의와 커밋 약속, 2단계 코디네이터 커밋 포인트와 코디네이터 장애 시 참여자가 잠금을 쥔 채 대기하는 의심 상태.",
                "코디네이터의 준비 질의에 참여자가 예라고 답한 후, 코디네이터 장애가 발생하면 참여자는 결정을 알지 못해 의심 상태에 갇힌다.")

lanes = [
    ("코디네이터", "트랜잭션 관리자"),
    ("데이터베이스 1", "참여자 A"),
    ("데이터베이스 2", "참여자 B"),
]
LX = d.lanes(lanes, y0=104, lane_w=196)
d.rails(646)

# --- 1단계: 준비 (Prepare) ---
d.tone(48, 160, W - 96, 26, INFO, 4, "12", 0.9)
d.t(W / 2, 177, "1단계: 준비 (prepare) — 커밋 가능 여부 질의와 불가역 커밋 능력 약속", 12, INFO, KR, "middle", 600)

d.seq_msg("코디네이터", "데이터베이스 1", "prepare 질의 (커밋 가능 여부)", 212)
d.seq_msg("코디네이터", "데이터베이스 2", "prepare 질의 (커밋 가능 여부)", 240)

d.seq_msg("데이터베이스 1", "코디네이터", "YES 응답 (커밋 능력 약속)", 276, c=OK)
d.seq_msg("데이터베이스 2", "코디네이터", "YES 응답 (커밋 능력 약속)", 304, c=OK)

# --- 커밋 포인트 (Commit Point) ---
d.tone(48, 338, W - 96, 26, ACC, 4, "12", 0.9)
d.t(W / 2, 355, "커밋 포인트 (commit point) — 코디네이터 자체 트랜잭션 로그 기록", 12, ACC, KR, "middle", 600)

d.seq_self("코디네이터", "커밋 결정 자체 로그 기록", 394, c=ACC)
d.seq_state("코디네이터", "커밋 포인트 확정", 426, ACC, w=150)

# --- 2단계: 커밋 지시 및 코디네이터 장애 ---
d.tone(48, 460, W - 96, 26, WARN, 4, "12", 0.9)
d.t(W / 2, 477, "2단계: 커밋 지시 전달 및 코디네이터 장애 시 의심 상태 발생", 12, WARN, KR, "middle", 600)

d.seq_msg("코디네이터", "데이터베이스 2", "commit 지시", 510, c=OK)
d.seq_state("데이터베이스 2", "커밋 완료 · 잠금 해제", 538, OK, w=156)
d.seq_msg("데이터베이스 2", "코디네이터", "ack 응답", 566, c=OK)

# 코디네이터 장애 발생 (y=596)
d.seq_state("코디네이터", "코디네이터 크래시 장애", 596, BAD, w=160)

# DB 1 의심 상태 (y=624)
d.seq_state("데이터베이스 1", "의심 상태 (In Doubt)", 624, WARN, w=156)

# 하단 의심 상태 설명 박스
d.tone(48, 650, W - 96, 38, WARN, 6, "14", 1.2)
d.t(W / 2, 674, "의심 상태 참여자: 코디네이터 복구 전까지 커밋·중단 결정 불가 · 행 잠금 무기한 유지 블록", 12, WARN, KR, "middle", 600)

# 범례
d.legend(LEG, [
    ("준비 단계", INFO),
    ("커밋 불가역 약속", OK),
    ("커밋 포인트", ACC),
    ("의심 상태 블록", WARN),
    ("코디네이터 크래시", BAD)
])

d.save("08-04.distributed-transaction-2pc.svg")
