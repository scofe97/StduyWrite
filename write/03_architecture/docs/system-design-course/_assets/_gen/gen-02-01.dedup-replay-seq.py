# 타입 스펙: type-sequence — 재발행된 메시지 1001 과 신규 메시지 1002 의 Cassandra upsert 멱등 처리 시퀀스.
# 사실 출처: 요약 §4.4·§4.13, 조사 보고서 행 14·15·17·18, Discord 2017 블로그, 본문 5절(채팅 서버 로컬 로그 재발행, Cassandra (channel_id, message_id) 기본 키 upsert 로 1001 중복 제거, 신규 1002 저장 및 오프셋 커밋).
# Layout conventions: 레인 4개 x = 120, 360, 600, 840 (폭 168), y0 = 104, rails = 148..580. 메시지 stride 40. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import Seq, ACC, OK, WARN, BAD, INFO, MUTED, INK, SOFT, RULE, KR, MONO

W, H = 960, 660


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=168):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w // 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 14, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) // 2 + dx
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))

    def selfmsg_left(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x - 10} {y - 10} L {x - 48} {y - 10} L {x - 48} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
        s.t(x - 56, y - 4, label, 13 if _kr(label) == KR else 12, c, _kr(label), "end", 600)
        if sub:
            s.t(x - 56, y + 16, sub, 12, MUTED, KR, "end")


d = SeqKR(W, H, "SYSTEM DESIGN COURSE · 02-01 §5",
          "재발행된 1001 은 같은 키로 덮어써지고 1002 만 새 행이 된다",
          "Cassandra 기본 키 upsert 로 1001 은 동일 값으로 덮어써 중복을 막고 1002 는 신규 영속합니다.",
          "메시지 ID 1001 중복 제거 및 1002 정상 커밋 시퀀스")

lanes_data = [
    ("채팅 서버", "로그 재발행"),
    ("Kafka", "메시지 브로커"),
    ("저장 서비스", "컨슈머 워커"),
    ("Cassandra", "기본 키 upsert"),
]
lane_xs = (120, 360, 600, 840)

d.lanes(lanes_data, lane_xs, lane_w=168)
d.rails(580)

# Section 1: msg_1001 중복 재발행
d.t(24, 168, "1. 중복 메시지 msg_1001 재발행 처리", 13, SOFT, KR, "start", 600)

d.msg("채팅 서버", "Kafka", "Replay(msg_1001)", 196, WARN, mk="warn", sub="로컬 로그 재전송")
d.msg("Kafka", "저장 서비스", "Poll(msg_1001)", 236, INFO, mk="info", sub="컨슈머 수신")
d.msg("저장 서비스", "Cassandra", "INSERT msg_1001", 276, INFO, mk="info", sub="PK: (room_abc, 1001)")
d.selfmsg_left("Cassandra", "동일 값 덮어쓰기", 316, WARN, sub="upsert 로 중복 제거")
d.msg("저장 서비스", "Kafka", "Commit offset 1001", 356, OK, mk="ok", dash="5 4", sub="오프셋 전진")

# 구분선
d.line(24, 384, W - 24, 384, RULE, 0.8, dash="4 4")

# Section 2: msg_1002 신규 저장
d.t(24, 408, "2. 신규 메시지 msg_1002 정상 영속", 13, SOFT, KR, "start", 600)

d.msg("채팅 서버", "Kafka", "Replay(msg_1002)", 436, INFO, mk="info", sub="신규 메시지 발행")
d.msg("Kafka", "저장 서비스", "Poll(msg_1002)", 476, INFO, mk="info", sub="컨슈머 수신")
d.msg("저장 서비스", "Cassandra", "INSERT msg_1002", 516, ACC, mk="acc", sub="PK: (room_abc, 1002)")
d.selfmsg_left("Cassandra", "신규 행 영속 완료", 556, OK, sub="기본 키 INSERT")
d.msg("저장 서비스", "Kafka", "Commit offset 1002", 580, OK, mk="ok", dash="5 4", sub="최종 오프셋 커밋")

d.legend(H - 44, [
    ("신규 영속 (초점)", ACC),
    ("중복 upsert", WARN),
    ("브로커 전달", INFO),
    ("커밋 완료", OK),
])

out_path = str(ASSETS_DIR / "02-01.dedup-replay-seq.svg")
d.save(out_path)
print(f"saved: {out_path}")
