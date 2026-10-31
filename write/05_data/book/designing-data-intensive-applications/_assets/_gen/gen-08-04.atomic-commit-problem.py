# 08-04 §1 — 다중 노드 독립 커밋 실패 시 발생하는 영구적 데이터 불일치 시퀀스.
# 검증(10-31 cc-ddia-dverify08): "발주"(주문) 오용을 "실행"으로 · 중단 상태 칩과 Abort 라벨 겹침을 벌림
# 사실 출처: 08-04 §1(L26~L28), 원서 Ch.8 Figure 8-12(PDF p.50~51) "When a transaction involves multiple database nodes, it may commit on some and fail on others."
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 580
H = LEG + 56

class AtomicSeq(Seq):
    def lanes(self, names, y0=104, lane_w=156):
        self.LX = {}
        n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 19, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 36, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
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
            self.path(f"M {x - 10} {y - 10} L {x - 48} {y - 10} L {x - 48} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            self.t(x - 56, y - 4, label, 11, c, KR, "end", 600)
            if sub:
                self.t(x - 56, y + 14, sub, 11, MUTED, KR, "end")
        else:
            self.path(f"M {x + 10} {y - 10} L {x + 48} {y - 10} L {x + 48} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            self.t(x + 56, y - 4, label, 11, c, KR, "start", 600)
            if sub:
                self.t(x + 56, y + 14, sub, 11, MUTED, KR, "start")

    def seq_state(self, a, txt, y, c, w=140):
        x = self.LX[a]
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 5, txt, 11, c, KR, "middle", 600)

d = AtomicSeq(W, H, "08-04 §1 · ATOMIC COMMITMENT PROBLEM", "다중 노드 독립 커밋 실패와 영구 불일치",
              "트랜잭션이 여러 노드에 걸쳐 있을 때 독립 커밋을 시도하면 한 노드만 커밋되고 다른 노드는 중단되어 영구적 데이터 불일치가 발생한다.",
              "클라이언트 1의 트랜잭션이 데이터베이스 2에서만 커밋된 사이 클라이언트 2가 이를 읽어 소급 롤백이 불가능해진다.")

lanes = [
    ("클라이언트 1 (앱)", "트랜잭션 T1 실행"),
    ("데이터베이스 1", "참여 노드 1 (중단)"),
    ("데이터베이스 2", "참여 노드 2 (커밋)"),
    ("클라이언트 2 (앱)", "트랜잭션 T2 읽기"),
]
LX = d.lanes(lanes, y0=104, lane_w=160)
d.rails(510)

# 1. T1 쓰기 요청
d.seq_msg("클라이언트 1 (앱)", "데이터베이스 1", "쓰기 요청 (T1)", 168)
d.seq_msg("클라이언트 1 (앱)", "데이터베이스 2", "쓰기 요청 (T1)", 196)

# 2. DB 2 커밋 성공
d.seq_msg("클라이언트 1 (앱)", "데이터베이스 2", "독립 커밋 요청", 232)
d.seq_state("데이터베이스 2", "커밋 확정 (가시화)", 264, OK, w=130)
d.seq_msg("데이터베이스 2", "클라이언트 1 (앱)", "커밋 완료 응답", 296, c=OK)

# 3. 클라이언트 2의 커밋 데이터 관측
d.seq_msg("클라이언트 2 (앱)", "데이터베이스 2", "읽기 요청 (T2)", 332, c=INFO)
d.seq_msg("데이터베이스 2", "클라이언트 2 (앱)", "커밋된 새 데이터 반환", 360, c=INFO)
d.seq_state("클라이언트 2 (앱)", "새 데이터 관측 의존", 388, INFO, w=140)

# 4. DB 1 커밋 실패 (중단)
d.seq_msg("클라이언트 1 (앱)", "데이터베이스 1", "독립 커밋 요청", 420)
d.seq_state("데이터베이스 1", "제약 위반 · 중단 롤백", 440, BAD, w=146)
d.seq_msg("데이터베이스 1", "클라이언트 1 (앱)", "중단 통보 (Abort)", 480, c=BAD)

# 5. 하단 영구 불일치 경고 박스
d.tone(48, 510, W - 96, 50, BAD, 6, "16", 1.4)
d.t(W / 2, 530, "영구 불일치 발생: DB 2는 커밋 확정 · DB 1은 중단 롤백", 13, BAD, KR, "middle", 600)
d.t(W / 2, 548, "클라이언트 2가 커밋 데이터를 이미 읽어 소급 롤백 불가능 (원자 커밋 파괴)", 12, INK, KR, "middle")

# 범례
d.legend(LEG, [
    ("커밋 성공", OK),
    ("중단 롤백", BAD),
    ("새 데이터 관측", INFO),
    ("정상 요청 흐름", MUTED)
])

d.save("08-04.atomic-commit-problem.svg")
