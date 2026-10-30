# 03-01 §3 — ORM의 N+1 쿼리 문제 시퀀스. 댓글 목록 1회 조회 후 각 댓글마다 사용자 조회 왕복.
# 사실 출처: 03-01 §3(L66~L81), 원서 Ch.3 Relational Versus Document Models §Object-Relational Mismatch
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 560
H = LEG + 56

class OrmSeq(Seq):
    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 12, MUTED, KR, "middle")

d = OrmSeq(W, H, "03-01 · ORM IMPEDANCE MISMATCH", "ORM의 N+1 쿼리 문제와 조인 fetch",
           "ORM이 댓글 목록을 1회 조회한 뒤 댓글마다 작성자를 따로 조회해 총 N+1 쿼리가 되는 구조를 보인다.",
           "목록 1회 조회 · 연관 작성자 N회 반복 조회 · 총 1+N 쿼리 · 조인 fetch 해결")

# 두 참여자 레인
lanes = [
    ("애플리케이션", "ORM · Hibernate"),
    ("데이터베이스", "RDBMS · SQL"),
]
LX = d.lanes(lanes, y0=104, lane_w=220)
d.rails(432)

# 1. 초기 쿼리 (1회)
d.seq_msg("애플리케이션", "데이터베이스", "SELECT * FROM comments", 168, INFO, "info", sub="1단계: 댓글 N개 목록 조회 (1회)", is_mono=True)
d.seq_msg("데이터베이스", "애플리케이션", "댓글 N개 반환 (comment_id · user_id)", 220, MUTED, "ar", dash="4 3", sub=None)

# 2. 루프 프레임 (N회 반복)
fx1, fx2 = LX["애플리케이션"] - 74, LX["데이터베이스"] + 74
fw = fx2 - fx1
d.box(fx1, 248, fw, 184, PAPER2, WARN, 1.0)
d.box(fx1, 248, 160, 22, PAPER, WARN, 1.0)
d.t(fx1 + 80, 263, "LOOP · 댓글 N회 반복", 11, WARN, KR, "middle", 600)

d.seq_msg("애플리케이션", "데이터베이스", "SELECT * FROM users WHERE id = c[1].user_id", 284, WARN, "warn", sub="2단계: 댓글 1 작성자 개별 조회", is_mono=True)
d.seq_msg("데이터베이스", "애플리케이션", "user 1 정보 반환", 334, MUTED, "ar", dash="4 3", sub=None)

d.t((LX["애플리케이션"] + LX["데이터베이스"]) / 2, 362, "··· 댓글 2부터 N까지 개별 쿼리 반복 ···", 12, SOFT, KR, "middle")

d.seq_msg("애플리케이션", "데이터베이스", "SELECT * FROM users WHERE id = c[N].user_id", 390, WARN, "warn", sub=None, is_mono=True)
d.seq_msg("데이터베이스", "애플리케이션", "user N 정보 반환", 416, MUTED, "ar", dash="4 3", sub=None)

# 3. N+1 문제 상태 요약 칩
mx = (LX["애플리케이션"] + LX["데이터베이스"]) / 2
d.tone(mx - 150, 448, 300, 28, WARN, 6, "1C", 1.2)
d.t(mx, 466, "총 1 + N 회 쿼리 · DB 안 조인보다 느림", 12, WARN, KR, "middle", 600)

# 4. 해법: 조인 fetch 대조 박스
d.tone(fx1, 492, fw, 48, OK, 6, "14", 1.2)
d.t(fx1 + 16, 512, "해법 · 조인 fetch · 쿼리 1회", 13, OK, KR, "start", 600)
d.t(fx1 + 16, 530, "SELECT * FROM comments JOIN users", 12, INK, MONO, "start")

d.legend(LEG, [("ORM 반복 쿼리 (N회)", WARN), ("조인 fetch 해법", OK), ("초기 목록 쿼리 (1회)", INFO), ("DB 반환 (응답)", MUTED)])
d.save("03-01.orm-n-plus-one.svg")
