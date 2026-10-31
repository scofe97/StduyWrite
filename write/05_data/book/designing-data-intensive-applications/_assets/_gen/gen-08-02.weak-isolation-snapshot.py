# 08-02 §2 — Read Committed에서 두 계좌 조회 사이에 이체 트랜잭션이 커밋되어 100달러가 사라진 것처럼 보이는 읽기 스큐(Read Skew) 이상 현상 시퀀스.
# 사실 출처: 08-02 본문 §2(L39~L51, 은행 예 L42), 원서 Ch.8 p.19 Figure 8-6 ("Read skew: Aaliyah observes the database in an inconsistent state")
# 타입 스펙: type-sequence
# 검증(10-31 cc-ddia-dverify08): 레인 이름을 본문 표기 Aaliyah 로(본문에 "앨리야" 없음). 값은 Fig 8-6(PDF p.19) 그대로
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in txt)


class KSeq(Seq):
    def lanes(self, names, y0=104, lane_w=170):
        self.LX = {}
        n = len(names)
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
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        fam = KR if _hangul(label) else MONO
        sz = 12 if _hangul(label) else 11
        self.t(mx, y - 8, label, sz, c, fam, "middle", 600)
        if sub:
            sfam = KR if _hangul(sub) else MONO
            self.t(mx, y + 15, sub, 11, MUTED, sfam)

    def selfmsg_left(self, a, label, y, c=MUTED, sub=None):
        x = self.LX[a]
        self.path(f"M {x - 10} {y - 10} L {x - 58} {y - 10} L {x - 58} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
        fam = KR if _hangul(label) else MONO
        sz = 12 if _hangul(label) else 11
        self.t(x - 68, y - 4, label, sz, c, fam, "end", 600)
        if sub:
            self.t(x - 68, y + 13, sub, 11, MUTED, KR, "end")

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)


W = 880
PY = 104
YBOT = 524
LEG = YBOT + 28
H = LEG + 52

s = KSeq(W, H, "08-02 · §2 READ SKEW ANOMALY", "은행 계좌 이체 중 읽기 스큐 이상 현상",
         "Aaliyah가 계좌 1과 계좌 2를 순차 조회하는 사이에 이체가 커밋되어 100달러 증발을 관측한다.",
         "계좌 1 이체 전 500달러 관측 · 계좌 2 이체 후 400달러 관측 · 합계 900달러 불일치")

s.lanes([
    ("Aaliyah", "잔액 조회"),
    ("계좌 1", "Account 1 (잔액 500)"),
    ("계좌 2", "Account 2 (잔액 500)"),
    ("이체 트랜잭션", "Transfer Txn (이체 100)")
], y0=PY, lane_w=170)

s.rails(YBOT)

# 1. Aaliyah -> 계좌 1: 잔액 조회
s.msg("Aaliyah", "계좌 1", "SELECT balance (id=1)", 168, INFO, mk="info", sub="계좌 1 잔액 질의")

# 2. 계좌 1 -> Aaliyah: 500 반환
s.msg("계좌 1", "Aaliyah", "500", 206, OK, mk="ok", sub="이체 전 잔액 관측")

# 3. 이체 트랜잭션 -> 계좌 1: 100달러 입금
s.msg("이체 트랜잭션", "계좌 1", "UPDATE balance = balance + 100", 244, ACC, mk="acc", sub="계좌 1 입금 갱신")
s.state("계좌 1", "balance = 600", 280, ACC)

# 4. 이체 트랜잭션 -> 계좌 2: 100달러 출금
s.msg("이체 트랜잭션", "계좌 2", "UPDATE balance = balance - 100", 318, ACC, mk="acc", sub="계좌 2 출금 갱신")
s.state("계좌 2", "balance = 400", 354, ACC)

# 5. 이체 트랜잭션 커밋 (우측 끝 레인이므로 좌측 루프로 배치)
s.selfmsg_left("이체 트랜잭션", "COMMIT", 388, ACC, sub="이체 커밋 확정")

# 6. Aaliyah -> 계좌 2: 잔액 조회
s.msg("Aaliyah", "계좌 2", "SELECT balance (id=2)", 430, INFO, mk="info", sub="계좌 2 잔액 질의")

# 7. 계좌 2 -> Aaliyah: 400 반환
s.msg("계좌 2", "Aaliyah", "400", 468, BAD, mk="bad", sub="이체 후 잔액 관측")

# 8. Aaliyah 상태 상자 (레인 내부 x=24..194에 안착)
ux = s.LX["Aaliyah"]
s.box(ux - 76, 494, 152, 22, PAPER, WARN, 1.0)
s.t(ux, 509, "합계 900 관측 (100 증발)", 11, WARN, KR, "middle", 600)

s.legend(LEG, [("이체·커밋 (focal)", ACC), ("조회 질의", INFO), ("이체 전 관측", OK), ("이체 후 관측", BAD), ("읽기 스큐", WARN)])
s.save("08-02.weak-isolation-snapshot.svg")
