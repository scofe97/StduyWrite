# 타입 스펙: type-sequence — 동일 reservation_id 재전송 시 유일 키 위반(23505)을 잡아 200 OK 로 기존 예약을 돌려주는 멱등 시퀀스.
# 사실 출처: 본문 01-01.md §3(UUID 7f3a8b2c-9d1e-4a6f-b8c2-3e5f7a1b2c3d, 1차 요청 201 Created, 재전송 23505 unique_violation 감지, 200 OK 기존 예약 반환),
#   요약 §3.7·§3.9, 조사 보고서 #5.
# Layout conventions: 캔버스 960×800, 레인 셋 x = 160·480·800 (폭 216), 레일 y = 148..736, 메시지 y = 200..712. 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, ACC, OK, WARN, BAD, MUTED, INK, SOFT, RULE, KR, MONO

W, H = 960, 800


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=216):
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

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13 if _kr(label) == KR else 12, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 15, sub, 12, MUTED, KR, "start")


d = SeqKR(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01 §3",
    "같은 예약 ID 로 두 번 보낸 요청은 기존 예약을 반환한다",
    "동일 UUID 멱등 키 재요청 시 PostgreSQL 유일 키 위반(23505)을 잡아 기존 예약 데이터를 200 OK 로 돌려줍니다.",
    "요청 1(201 Created) → 네트워크 지연/재전송 → 요청 2(23505 위반) → 복구 분기 → 200 OK"
)

lanes_data = [
    ("앱", "클라이언트"),
    ("예약 API", "서버 애플리케이션"),
    ("PostgreSQL", "유일 키 제약 (reservations)"),
]
lane_xs = (160, 480, 800)

d.lanes(lanes_data, lane_xs, lane_w=216)
d.rails(736)

# 1. 첫 번째 요청 (신규 정상 생성)
d.t(36, 168, "1. 첫 번째 예약 요청: 신규 INSERT 및 201 Created", 13, SOFT, KR, "start", 600)

d.msg("앱", "예약 API", "POST /reservations", 200, MUTED, mk="ar", sub="id: 7f3a8b2c-9d1e-4a6f-b8c2-3e5f7a1b2c3d")
d.msg("예약 API", "PostgreSQL", "INSERT INTO reservations", 248, MUTED, mk="ar", sub="PK reservation_id 삽입")
d.msg("PostgreSQL", "예약 API", "INSERT 성공 (커밋)", 296, OK, mk="ok", dash="5 4", sub="신규 예약 행 영속 완료")
d.msg("예약 API", "앱", "201 Created", 344, OK, mk="ok", dash="5 4", sub="예약 완료 응답 반환")

# 구분선: 네트워크 타임아웃 / 중복 클릭 발생
d.line(36, 384, 924, 384, RULE, 0.8, dash="4 4")
d.t(36, 408, "2. 동일 UUID 재요청 · 23505 위반 감지 · 200 OK 반환", 13, SOFT, KR, "start", 600)

# 2. 두 번째 요청 (동일 UUID 재전송)
d.msg("앱", "예약 API", "POST /reservations (재전송)", 440, WARN, mk="warn", sub="같은 UUID 7f3a8b2c…")
d.msg("예약 API", "PostgreSQL", "INSERT INTO reservations", 488, WARN, mk="warn", sub="동일 기본 키 삽입 시도")
d.msg("PostgreSQL", "예약 API", "SQLSTATE 23505", 536, BAD, mk="bad", dash="5 4", sub="unique_violation 유일 키 제약 위반")
d.selfmsg("예약 API", "23505 감지 · 기존 예약 조회", 584, WARN, sub="유일 제약 예외 포착 후 복구 분기")
d.msg("예약 API", "PostgreSQL", "SELECT reservation_id", 624, MUTED, mk="ar", sub="기존 예약 데이터 단건 조회")
d.msg("PostgreSQL", "예약 API", "기존 예약 행 반환", 668, OK, mk="ok", dash="5 4", sub="CONFIRMED 행 반환")
d.msg("예약 API", "앱", "200 OK (focal)", 712, ACC, mk="acc", dash="5 4", sub="동일 예약 데이터 반환 · 중복 결제 방지")

# 범례
d.legend(756, [
    ("201 신규 생성", OK),
    ("중복 재전송", WARN),
    ("23505 위반", BAD),
    ("200 OK 반환 (focal)", ACC),
])

out_path = Path(__file__).parent.parent / "01-01.idempotent-retry.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
