# 06-02 §1 — 팔로워 장애 시 로컬 로그의 마지막 트랜잭션을 확인하고 리더에 차분 변경을 요청해 복구하는 catch-up 시퀀스.
# 사실 출처: 06-02 §1(L25~L30), 원서 Ch.6 "Follower failure: Catch-up recovery"
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 580
LEG = H - 56

class CatchUpSeq(Seq):
    def lanes(self, names, y0=104, lane_w=240):
        self.LX = {}; n = len(names)
        span = (self.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
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
            self.path(f"M {x - 10} {y - 10} L {x - 58} {y - 10} L {x - 58} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
            self.t(x - 68, y - 4, label, 12, c, KR, "end", 600)
            if sub:
                self.t(x - 68, y + 15, sub, 12, MUTED, KR, "end")
        else:
            self.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
            self.t(x + 68, y - 4, label, 12, c, KR, "start", 600)
            if sub:
                self.t(x + 68, y + 15, sub, 12, MUTED, KR, "start")

d = CatchUpSeq(W, H, "06-02 §1 · FOLLOWER CATCH-UP RECOVERY", "팔로워 장애와 로컬 로그 기반 catch-up 복구 시퀀스",
               "팔로워가 크래시 후 재기동 시 로컬 로그의 마지막 트랜잭션을 확인하고 리더에 끊긴 동안의 변경을 요청해 적용하고 따라잡는 과정.",
               "마지막 처리 트랜잭션 · 끊긴 동안의 변경 요청 · 적용 · 따라잡음")

lanes = [
    ("팔로워 노드 (Follower)", "로컬 변경 로그 보관"),
    ("리더 노드 (Leader)", "쓰기 수용 및 복제 로그 관리"),
]
LX = d.lanes(lanes, y0=104, lane_w=240)
d.rails(468)

# 1. 팔로워 장애 발생
fx = LX["팔로워 노드 (Follower)"]
d.tone(fx - 130, 156, 260, 26, WARN, 4, "18", 1.0)
d.t(fx, 173, "팔로워 크래시 · 네트워크 일시 단절", 12, WARN, KR, "middle", 600)

# 2. 로컬 로그 확인
d.seq_self("팔로워 노드 (Follower)", "로컬 로그 판독", 208, INFO, sub="결함 전 마지막 처리 트랜잭션", to_left=False)

# 3. 차분 변경 스트림 요청
d.seq_msg("팔로워 노드 (Follower)", "리더 노드 (Leader)", "끊긴 동안의 변경 요청", 258, INFO, "info", sub="마지막 처리 트랜잭션 이후")

# 4. 리더 보관 로그 검색
d.seq_self("리더 노드 (Leader)", "보관 중인 로그", 308, INFO, sub="팔로워가 처리 확인 전이라 남아 있음", to_left=True)

# 5. 차분 스트림 순차 전송 (FOCAL)
d.seq_msg("리더 노드 (Leader)", "팔로워 노드 (Follower)", "밀린 쓰기 전송", 358, ACC, "acc", sub="리더·팔로워 양쪽에 높은 부하")

# 6. 팔로워 변경 적용
d.seq_self("팔로워 노드 (Follower)", "변경 적용", 408, OK, sub="끊긴 동안의 변경 반영", to_left=False)

# 7. 따라잡기 완료 및 복귀
d.tone(fx - 130, 436, 260, 26, OK, 4, "18", 1.0)
d.t(fx, 453, "따라잡음 · 변경 스트림 계속 수신", 12, OK, KR, "middle", 600)

# 8. 하단 리더 로그 보관 한계 박스
d.box(24, 474, W - 48, 34, PAPER2, WARN, 1.0)
d.t(W / 2, 495, "오래 불가용 시 리더의 선택: 로그 보관(디스크 고갈 위험) · 로그 삭제(백업에서 복원)", 12, WARN, KR, "middle", 600)

d.legend(LEG, [("밀린 쓰기 전송 (focal)", ACC), ("변경 요청·로그", INFO), ("적용·따라잡음", OK), ("장애·보관 한계", WARN)])
d.save("06-02.catch-up.svg")
