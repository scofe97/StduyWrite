# 06-01 §2 동기 vs 비동기 vs 반동기 — 팔로워 1 은 동기로 확인을 기다리고 팔로워 2 는 비동기로 지연 전파되는 시퀀스.
# 사실 출처: 06-01 본문 §2(L44~L54), DDIA 2판 6장 Figure 6-2 "Leader-based replication with one synchronous and one asynchronous follower"
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO


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
H = 572
LEG = H - 56

s = KSeq(W, H, "06-01 · §2 SEQUENCE", "동기 vs 비동기 vs 반동기 복제 시퀀스",
        "리더는 동기 팔로워의 확인 응답을 받은 뒤 클라이언트에 성공을 확정 통보하지만, 비동기 팔로워에는 확인 대기 없이 변경을 보내 지연이 발생할 수 있다.",
        "클라이언트 갱신 요청 · 동기 확인 대기 · 성공 확정 통보 · 비동기 지연 전파")

# 4개 참여자 레인
s.lanes([
    ("클라이언트", "User 1234"),
    ("리더", "Leader · Primary"),
    ("팔로워 1 (동기)", "Follower 1 (Sync)"),
    ("팔로워 2 (비동기)", "Follower 2 (Async)"),
], y0=104, lane_w=190)

s.rails(458)

# 1. 클라이언트 -> 리더 쓰기 요청
s.msg("클라이언트", "리더", "프로필 이미지 갱신 요청", 176, INFO, mk="info", sub="set picture_url = 'me-new.jpg'")

# 2. 리더 로컬 저장소 기록
s.selfmsg("리더", "로컬 저장소 기록", 216, ACC, sub="새 데이터 먼저 기록")

# 3. 리더 -> 팔로워 1 동기 복제 로그 전송
s.msg("리더", "팔로워 1 (동기)", "복제 로그 전송 (동기)", 260, ACC, mk="acc", sub="수신 확인 대기 (동기 복제)")

# 4. 리더 -> 팔로워 2 비동기 복제 로그 전송 (Figure 6-2: 팔로워 1 의 OK 를 기다리지 않고 함께 보낸다)
s.msg("리더", "팔로워 2 (비동기)", "복제 로그 전송 (비동기)", 314, MUTED, dash="4 4", sub="응답 대기 없음 · 뒤처질 수 있음")

# 5. 팔로워 1 로컬 변경 적용
s.selfmsg("팔로워 1 (동기)", "로컬 변경 적용", 352, OK, sub="동일 순서로 로그 반영")

# 6. 팔로워 1 -> 리더 수신 확인 응답
s.msg("팔로워 1 (동기)", "리더", "수신 확인 응답 (OK)", 390, OK, mk="ok", sub="팔로워 최신 사본 확보 완료")

# 7. 리더 -> 클라이언트 쓰기 성공 통보
s.msg("리더", "클라이언트", "쓰기 성공 확정 통보", 428, OK, mk="ok", sub="클라이언트에 커밋 완료 반환")

# 8. 팔로워 2 상태 (복제 지연)
s.state("팔로워 2 (비동기)", "아직 미적용 · 복제 지연", 428, WARN)

# 하단 반동기 설명 배너
s.tone(24, 470, W - 48, 34, INFO, 4, "12", 0.9)
s.t(W / 2, 491, "반동기(semisynchronous): 팔로워 하나만 동기 · 동기 팔로워 불가용 시 비동기 하나를 동기로 승격", 12, INK, KR, "middle", 500)

s.legend(LEG, [("동기 복제 (focal)", ACC), ("성공 확정", OK), ("비동기 복제", MUTED), ("복제 지연 위험", WARN)])
s.save("06-01.sync-async-replication.svg")
