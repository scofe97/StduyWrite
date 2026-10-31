# 08-02 §1 — Read Committed에서 아직 커밋되지 않은 쓰기는 다른 트랜잭션에 보이지 않고 구 커밋 값을 반환하는 더티 읽기 방지 시퀀스.
# 사실 출처: 08-02 본문 §1(L24~L36), 원서 Ch.8 p.16 Figure 8-4 ("No dirty reads: user 2 sees the new value for x only after user 1's transaction has committed")
# 타입 스펙: type-sequence
# 검증(10-31 cc-ddia-dverify08): Fig 8-4(PDF p.16) 에 없는 커밋 뒤 OK 응답 제거, "로컬 반영" → "미커밋 쓰기 확인"
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in txt)


class KSeq(Seq):
    def lanes(self, names, y0=104, lane_w=180):
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

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)


W = 880
PY = 104
YBOT = 596
LEG = YBOT + 28
H = LEG + 52

s = KSeq(W, H, "08-02 · §1 READ COMMITTED", "Read Committed의 더티 읽기 방지 시퀀스",
         "트랜잭션 1의 쓰기는 커밋되기 전까지 트랜잭션 2에 보이지 않고 구 커밋 값 2를 반환한다.",
         "미커밋 쓰기 은폐 · 구 커밋 버전 반환 · 커밋 후 신규 값 3 가시화")

s.lanes([
    ("사용자 1", "User 1"),
    ("데이터베이스", "Database (초기 x=2)"),
    ("사용자 2", "User 2")
], y0=PY, lane_w=180)

s.rails(YBOT)

# Y 간격을 38~40px로 넓혀 라벨과 서브텍스트 겹침 방지
# 1. User 1: set x = 3
s.msg("사용자 1", "데이터베이스", "set x = 3", 168, ACC, mk="acc", sub="미커밋 쓰기")

# 2. Database -> User 1: OK
s.msg("데이터베이스", "사용자 1", "OK", 206, OK, mk="ok", sub="미커밋 쓰기 확인")

# 3. User 2: get x
s.msg("사용자 2", "데이터베이스", "get x", 244, INFO, mk="info", sub="조회 요청")

# 4. Database -> User 2: 2 (구 값 반환)
s.msg("데이터베이스", "사용자 2", "2", 282, OK, mk="ok", sub="더티 읽기 방지: 구 커밋 값")

# 5. User 1: set y = 3
s.msg("사용자 1", "데이터베이스", "set y = 3", 320, ACC, mk="acc", sub="추가 쓰기")

# 6. Database -> User 1: OK
s.msg("데이터베이스", "사용자 1", "OK", 358, OK, mk="ok", sub="미커밋 쓰기 확인")

# 7. User 2: get x (재조회)
s.msg("사용자 2", "데이터베이스", "get x", 396, INFO, mk="info", sub="재조회 요청")

# 8. Database -> User 2: 2 (여전히 구 값 반환)
s.msg("데이터베이스", "사용자 2", "2", 434, OK, mk="ok", sub="미커밋 상태 유지: 구 값")

# 9. User 1: Commit
s.msg("사용자 1", "데이터베이스", "Commit", 472, ACC, mk="acc", sub="트랜잭션 1 커밋 요청")


# 11. User 2: get x (커밋 후 조회)
s.msg("사용자 2", "데이터베이스", "get x", 548, INFO, mk="info", sub="커밋 후 조회 요청")

# 12. Database -> User 2: 3 (신규 커밋 값 반환)
s.msg("데이터베이스", "사용자 2", "3", 584, ACC, mk="acc", sub="커밋 후 신규 값 반영")

s.legend(LEG, [("쓰기·커밋 요청 (focal)", ACC), ("조회 질의", INFO), ("정상 응답·더티 읽기 방지", OK)])
s.save("08-02.read-committed.svg")
