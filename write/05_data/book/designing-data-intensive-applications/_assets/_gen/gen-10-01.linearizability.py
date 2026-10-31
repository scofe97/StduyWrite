# 10-01 §1 — 복제 지연과 외부 통신 채널 간 경쟁으로 인한 선형성 위반 시퀀스.
# 사실 출처: 10-01 §1(L26~L29), DDIA 2판 Ch.10 Figure 10-1(PDF p.4) — 심판·리더·팔로워 2개·Aaliyah·Bryce 레인,
#   Aaliyah 는 팔로워 1, Bryce 는 팔로워 2 에서 읽고 리더→팔로워 2 복제가 늦게 도착한다.
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 640
H = LEG + 52

class CompSeq(Seq):
    def lanes(self, names, xs, y0=104, lane_w=100):
        self.LX = {}
        for (nm, sub), x in zip(names, xs):
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False, lx=None):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 16, sub, 11, MUTED, KR, "middle")

    def seq_self(self, a, label, y, c=MUTED, sub=None, to_left=False):
        x = self.LX[a]
        if to_left:
            self.path(f"M {x - 10} {y - 10} L {x - 58} {y - 10} L {x - 58} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            self.t(x - 68, y - 4, label, 12, c, KR, "end", 600)
            if sub:
                self.t(x - 68, y + 15, sub, 11, MUTED, KR, "end")
        else:
            self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            self.t(x + 68, y - 4, label, 12, c, KR, "start", 600)
            if sub:
                self.t(x + 68, y + 15, sub, 11, MUTED, KR, "start")

d = CompSeq(W, H, "10-01 · §1 LINEARIZABILITY VIOLATION", "복제 지연으로 인한 비선형적 읽기 시퀀스",
            "Aaliyah 는 최종 점수를 읽었는데, 그 말을 듣고 나중에 읽은 Bryce 는 늦은 팔로워에서 구 값을 받는다.",
            "심판 쓰기 · 팔로워 1 빠른 복제 · 새 값 확인 · 말로 전달 · 팔로워 2 구 값 · 늦은 복제")

lx = d.lanes([
    ("심판", "Referee"),
    ("리더", "Leader"),
    ("팔로워 1", "Follower 1"),
    ("팔로워 2", "Follower 2"),
    ("Aaliyah", "클라이언트"),
    ("Bryce", "클라이언트"),
], [74, 226, 378, 530, 682, 812], y0=104, lane_w=100)

d.rails(540)

# 1~2. 심판이 리더에 최종 점수를 쓰고 OK 를 받는다
d.seq_msg("심판", "리더", "INSERT", 176, OK, "ok", sub="최종 점수 1 : 0", is_mono=True)
d.seq_msg("리더", "심판", "OK", 228, MUTED, "ar", is_mono=True)

# 3. 팔로워 1 로 가는 복제는 빨리 도착한다
d.seq_msg("리더", "팔로워 1", "복제", 256, OK, "ok", sub="빨리 도착")

# 4~5. Aaliyah 는 팔로워 1 에서 새 값을 읽는다
d.seq_msg("Aaliyah", "팔로워 1", "SELECT", 304, INFO, "info", is_mono=True, lx=606)
d.seq_msg("팔로워 1", "Aaliyah", "새 값 · 경기 끝", 344, OK, "ok", lx=606)

# 6. DB 밖 통로로 전달
d.seq_msg("Aaliyah", "Bryce", "말로 전달", 392, ACC, "acc", sub="DB 밖 통로")

# 7~8. Bryce 는 팔로워 2 에서 구 값을 읽는다
d.seq_msg("Bryce", "팔로워 2", "SELECT", 440, INFO, "info", is_mono=True, lx=747)
d.seq_msg("팔로워 2", "Bryce", "구 값 · 진행 중", 480, BAD, "bad", lx=747)

# 9. 팔로워 2 로 가는 복제는 그 뒤에 도착한다
d.seq_msg("리더", "팔로워 2", "복제", 520, WARN, "warn", dash="4,3", sub="뒤늦게 도착", lx=454)

# 하단 판정 박스
d.tone(34, 560, W - 68, 54, BAD, 6, "14", 1.2)
d.t(W / 2, 582, "선형성 위반", 13, BAD, KR, "middle", 600)
d.t(W / 2, 600, "Aaliyah 가 새 값을 읽은 뒤 시작한 Bryce 의 읽기가 구 값을 받았다", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("새 값 쓰기·복제·응답", OK),
    ("조회", INFO),
    ("DB 밖 전달", ACC),
    ("복제 지연", WARN),
    ("구 값 응답", BAD),
])

d.save("10-01.linearizability.svg")
