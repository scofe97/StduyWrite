# 06-03 §2 — 사용자가 데이터를 작성한 직후 복제가 지연된 팔로워에서 조회하여 자기 입력이 사라진 것처럼 보이는 read-your-writes 위반 시퀀스.
# 사실 출처: 06-03 §2(L41~L44), 원서 Ch.6 p.17 Figure 6-3
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO


def _hangul(txt):
    return any("가" <= ch <= "힣" for ch in txt)


class KSeq(Seq):
    # dd.Seq 는 레인 부제·메시지·상태 칩을 MONO 로 찍는다. 한글이 든 텍스트는 KR 로 쓴다.
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

    def msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = self.LX[a], self.LX[b]; d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 9, label, 12 if _hangul(label) else 11, c, KR if _hangul(label) else MONO, "middle", 600)
        if sub:
            self.t(mx, y + 17, sub, 11, MUTED, KR if _hangul(sub) else MONO)

    def selfmsg(self, a, label, y, c=MUTED, sub=None):
        x = self.LX[a]
        self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        self.t(x + 68, y - 4, label, 12 if _hangul(label) else 11, c, KR if _hangul(label) else MONO, "start", 600)
        if sub:
            self.t(x + 68, y + 13, sub, 11, MUTED, KR, "start")

    def state(self, a, txt, y, c):
        x = self.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        self.t(x, y + 4, txt, 11, c, KR if _hangul(txt) else MONO)

W = 880
PY = 104
YBOT = 428
LEG = YBOT + 28
H = LEG + 52

s = KSeq(W, H, "06-03 · §2 READ-YOUR-WRITES ANOMALY", "read-your-writes 이상 시퀀스",
        "사용자가 댓글을 작성한 직후 복제가 지연된 팔로워에서 조회해 자기 입력이 사라진 것처럼 보이는 현상",
        "댓글 작성(INSERT) · 리더 성공 응답 · 비동기 복제 편차 · stale 팔로워 빈 결과 · 유실 착각")

# 참여자 레인 4개
s.lanes([
    ("사용자 1234", "User 1234"),
    ("리더", "Leader"),
    ("팔로워 1", "Follower 1 (정상)"),
    ("팔로워 2", "Follower 2 (지연)")
], y0=PY, lane_w=160)

s.rails(YBOT)

# 1. 댓글 작성 (User 1234 -> Leader)
s.msg("사용자 1234", "리더", "INSERT comments (1234, 55555, 'Sounds good!')", 176, ACC, mk="acc", sub="댓글 작성 요청")

# 2. 저장 확인 (Leader -> User 1234)
s.msg("리더", "사용자 1234", "insert OK", 222, OK, mk="ok", sub="쓰기 성공 응답")

# 3. 비동기 복제 전파 (Leader -> Follower 1)
s.msg("리더", "팔로워 1", "INSERT comments... (55555 복제)", 268, OK, mk="ok", sub="정상 복제 즉시 반영")

# 4. 작성 직후 댓글 조회 (User 1234 -> Follower 2)
s.msg("사용자 1234", "팔로워 2", "SELECT * WHERE reply_to = 55555", 314, INFO, mk="info", sub="작성 직후 페이지 조회")

# 5. 미반영 빈 결과 응답 (Follower 2 -> User 1234)
s.msg("팔로워 2", "사용자 1234", "0건 (No results!)", 360, BAD, mk="bad", sub="지연으로 낡은 상태 반환")

# 6. 사용자 유실 착각 상태 & 뒤늦은 복제 도달
ux = s.LX["사용자 1234"]
s.box(ux - 80, 396, 160, 24, PAPER, WARN, 1.0)
s.t(ux, 412, "이상: 댓글 유실 착각", 11, WARN, KR, "middle", 600)

s.msg("리더", "팔로워 2", "INSERT comments... (뒤늦은 복제)", 406, MUTED, mk="ar", dash="4 4", sub="뒤처진 팔로워에 복제 도착")

s.legend(LEG, [("쓰기 요청", ACC), ("조회 질의", INFO), ("정상 반영·응답", OK), ("유실 착각 이상", WARN), ("미반영 결과", BAD)])
s.save("06-03.read-your-writes.svg")
