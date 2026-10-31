# 08-01 §5 — 다중 객체 쓰기(메일 삽입과 미읽은 카운터 갱신) 간 트랜잭션 부재로 인한 격리성 위반과 불일치 읽기 시퀀스.
# 사실 출처: 08-01 §5(L55~L68), 원서 Ch.8 Single-Object and Multi-Object Operations(PDF p.9~10) 및 Figure 8-2(PDF p.10)
# 타입 스펙: type-sequence
# 검증(10-31 cc-ddia-dverify08): 범례 "지연 반영"(WARN) 이 조회 화살표에 쓰이고 뒤늦은 UPDATE 는 범례 밖 회색이던 것을 맞춤, 바닥 칸의 "원자적" 을 본문 L70 표현으로. 값은 Fig 8-2(PDF p.10) 그대로
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 620
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

d = CompSeq(W, H, "08-01 · §5 MULTI-OBJECT ANOMALY", "다중 객체 연산의 격리성 위반과 불일치 읽기 시퀀스",
            "이메일 삽입과 미읽은 카운터 갱신이 한 트랜잭션으로 묶이지 않아 수신자에게 어긋난 중간 상태가 노출되는 과정.",
            "메일 레코드 삽입 · 목록 조회와 카운터 불일치 · 더티 읽기 발생 · 뒤늦은 카운터 갱신")

lx = d.lanes([
    ("사용자 1 (발신)", "User 1"),
    ("데이터베이스", "초기 unread = 0"),
    ("사용자 2 (수신)", "User 2"),
], y0=104, lane_w=200)

d.rails(576)

# 1. 사용자 1: 메일 삽입
d.seq_msg("사용자 1 (발신)", "데이터베이스", "INSERT into emails", 168, INFO, "info", sub="recipient_id=2 메일 저장", is_mono=True)
d.seq_msg("데이터베이스", "사용자 1 (발신)", "OK", 216, OK, "ok", sub="메일 테이블 저장 완료", is_mono=True)

# 2. 사용자 2: 메일 목록 조회
d.seq_msg("사용자 2 (수신)", "데이터베이스", "SELECT from emails", 264, INFO, "info", sub="수신 메일 목록 조회", is_mono=True)
d.seq_msg("데이터베이스", "사용자 2 (수신)", "('Hello', true)", 312, INFO, "info", sub="새 메일 1건 반환", is_mono=True)

# 3. 사용자 2: 미읽은 카운터 조회 (불일치 발생)
d.seq_msg("사용자 2 (수신)", "데이터베이스", "SELECT from mailboxes", 360, INFO, "info", sub="미읽은 카운터 조회", is_mono=True)
d.seq_msg("데이터베이스", "사용자 2 (수신)", "unread = 0", 408, INFO, "info", sub="카운터 0 반환 (미갱신)", is_mono=True)

# 4. 사용자 2 측 이상 현상 박스 (focal)
d.tone(lx["사용자 2 (수신)"] - 140, 440, 280, 24, ACC, 4, "18", 1.4)
d.t(lx["사용자 2 (수신)"], 456, "목록에는 메일 있음 · 카운터는 0 (더티 읽기)", 11, ACC, KR, "middle", 600)

# 5. 사용자 1: 뒤늦은 카운터 갱신
d.seq_msg("사용자 1 (발신)", "데이터베이스", "UPDATE mailboxes", 496, WARN, "warn", sub="뒤늦은 카운터 갱신", is_mono=True)
d.seq_msg("데이터베이스", "사용자 1 (발신)", "OK", 544, OK, "ok", sub="카운터 1 반영 완료", is_mono=True)

# 6. 하단 결론 톤 박스
d.tone(lx["데이터베이스"] - 150, 576, 300, 24, INFO, 4, "18", 1.0)
d.t(lx["데이터베이스"], 592, "다중 객체 트랜잭션 필요 · 두 쓰기를 한 트랜잭션으로", 11, INFO, KR, "middle", 600)

d.legend(LEG, [
    ("이상 현상 (focal)", ACC),
    ("완료 응답", OK),
    ("삽입·조회", INFO),
    ("지연 반영", WARN),
])

d.save("08-01.multi-object-anomaly.svg")
