# 08-03 §4 — 직렬화 가능 스냅샷 격리(SSI)의 낡은 MVCC 읽기 감지와 트랜잭션 중단 시퀀스
# 검증(10-31 cc-ddia-dverify08): Fig 8-10(p47)에 없는 버전 이름 v1 을 "기존 버전"으로
# 사실 출처: 08-03 §4(L89~L109), 원서 Ch.8 p.46~47 Figure 8-10
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in str(txt))


class KSeq(Seq):
    def lanes(self, names, y0=104, lane_w=200):
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

    def msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = self.LX[a], self.LX[b]; d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 9, label, 11, c, KR if _hangul(label) else MONO, "middle", 600)
        if sub:
            self.t(mx, y + 17, sub, 11, MUTED, KR if _hangul(sub) else MONO)

    def selfmsg(self, a, label, y, c=MUTED, sub=None):
        x = self.LX[a]
        self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        self.t(x + 68, y - 4, label, 11, c, KR if _hangul(label) else MONO, "start", 600)
        if sub:
            self.t(x + 68, y + 13, sub, 11, MUTED, KR, "start")

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)


W = 880
PY = 104
YBOT = 476
LEG = YBOT + 28
H = LEG + 52

s = KSeq(W, H, "08-03 · §4 SSI CONFLICT DETECTION", "SSI의 낡은 MVCC 읽기 감지와 트랜잭션 중단",
         "트랜잭션이 읽은 스냅샷 전제가 다른 커밋으로 무너졌을 때 커밋 시점에 감지하여 중단하는 흐름",
         "MVCC 가시성 규칙 · 미커밋 쓰기 무시 추적 · 선행 커밋 · 낡은 전제 감지 · ABORT 롤백")

s.lanes([
    ("트랜잭션 42", "Aaliyah 당직 취소"),
    ("데이터베이스", "MVCC 스토리지 & 관리자"),
    ("트랜잭션 43", "Bryce 당직 취소"),
], lane_w=200)

s.rails(YBOT)

# 초기 DB 상태
s.box(428 - 140, 160, 280, 26, PAPER, RULE, 0.8)
s.t(428, 177, "초기: Aaliyah(True), Bryce(True) · 당직 2명", 11, INFO, KR, "middle")

# t1: 42 UPDATE (미커밋 쓰기)
s.msg("트랜잭션 42", "데이터베이스", "UPDATE doctors (on_call=false)", 204, WARN, sub="Aaliyah 새 버전 생성 (inserted_by=42, 미커밋)")

# t2: 43 SELECT (스냅샷 가시성 규칙으로 42 무시)
s.msg("트랜잭션 43", "데이터베이스", "SELECT COUNT(*) (당직 의사 수)", 248, INFO, sub="42 미커밋 무시 · 기존 버전 읽음 (반환: 2명)")

# t3: 트랜잭션 관리자의 추적 기록
s.tone(428 - 150, 276, 300, 26, INFO, 4, "16", 1.0)
s.t(428, 293, "추적: 43이 미커밋 쓰기를 무시하고 읽음 기록", 11, INFO, KR, "middle", 600)

# t4: 43 UPDATE
s.msg("트랜잭션 43", "데이터베이스", "UPDATE doctors (on_call=false)", 328, WARN, sub="Bryce 새 버전 생성 (inserted_by=43)")

# t5: 42 COMMIT
s.msg("트랜잭션 42", "데이터베이스", "COMMIT (성공)", 368, OK, sub="Aaliyah=false 커밋 확정")

# t6: 43 COMMIT 시도 및 검사
s.msg("트랜잭션 43", "데이터베이스", "COMMIT 시도", 408, INFO, sub="충돌 검사: 무시했던 42의 쓰기가 이미 커밋됨")

# t7: 43 ABORT 응답
s.msg("데이터베이스", "트랜잭션 43", "ABORT (직렬화 충돌 중단)", 454, BAD, sub="낡은 전제 기반 쓰기 무효화 → 재시도 유도")

s.legend(LEG, [("스냅샷 읽기·검사", INFO), ("버전 갱신 쓰기", WARN), ("선행 커밋 성공", OK), ("낡은 전제 감지·중단 (focal)", BAD)])
s.save("08-03.ssi.svg")
