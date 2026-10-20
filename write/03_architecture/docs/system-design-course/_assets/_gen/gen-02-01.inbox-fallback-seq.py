# 타입 스펙: type-sequence — 오프라인 수신함의 선 DB 커밋 후 Redis 캐시 쓰기와, Redis 장애 시 DB 폴백 읽기 시퀀스. focal 은 DB 폴백 조회.
# 사실 출처: 요약 §4.4·§4.18, 조사 보고서 행 3·4·12, 본문 2절(관계형 DB tb_user_inbox 에 delivered IS NULL 로 선영속 후 Redis 캐시 적재, 정상 시 Redis 메모리 조회, 장애 시 타임아웃 후 DB 디스크 폴백 조회, 메시지 ID msg_1001).
# Layout conventions: 3개 레인(채팅 서버·DB 수신함·Redis 수신함), W=960, H=824. 메시지 간격 44px 이상. 모든 좌표 4의 배수.
import pathlib
import sys

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import Seq, ACC, BAD, INFO, INK, KR, MONO, MUTED, OK, RULE, SOFT, WARN

W, H = 960, 824


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=180):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w // 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 14, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) // 2 + dx
        s.t(mx, y - 9, label, 12 if _kr(label) == KR else 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12 if _kr(sub) == KR else 11, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 56} {y - 10} L {x + 56} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 12 if _kr(label) == KR else 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 16, sub, 11, MUTED, KR, "start")


d = SeqKR(
    W,
    H,
    "SYSTEM DESIGN COURSE · 02-01 §2",
    "수신함 쓰기와 Redis 장애 때의 읽기 폴백",
    "정본 DB 에 먼저 영속한 뒤 Redis 캐시를 채우고, Redis 다운 시 DB 에서 읽어 메시지를 보존합니다.",
    "선 DB 영속 (msg_1001) → Redis 캐시 → [정상] Redis 적중 / [장애] DB 폴백",
)

lanes_data = [
    ("채팅 서버", "애플리케이션"),
    ("DB 수신함", "tb_user_inbox 정본"),
    ("Redis 수신함", "inbox 캐시"),
]
lane_xs = (160, 500, 800)

d.lanes(lanes_data, lane_xs, lane_w=180)
d.rails(752)


# -------------------------------------------------------------
# 1. 수신함 쓰기 (선 DB 커밋 후 Redis 캐시)
# -------------------------------------------------------------
d.t(24, 168, "1. 오프라인 수신함 쓰기 (선 DB 커밋 · 후 Redis 캐시)", 13, SOFT, KR, "start", 600)

d.msg("채팅 서버", "DB 수신함", "INSERT msg_1001 (delivered IS NULL)", 196, INFO, mk="info", sub="정본 테이블 영속화")
d.msg("DB 수신함", "채팅 서버", "커밋 완료 (200 OK)", 240, OK, mk="ok", dash="5 4", sub="내구성 확보 확인")
d.msg("채팅 서버", "Redis 수신함", "RPUSH inbox:user_bob msg_1001", 284, INFO, mk="info", sub="캐시 리스트 적재")
d.msg("Redis 수신함", "채팅 서버", "캐시 적재 완료", 328, OK, mk="ok", dash="5 4", sub="읽기 가속 준비")


# 구분선 1
d.line(24, 360, W - 24, 360, RULE, 0.8, dash="4 4")


# -------------------------------------------------------------
# 2. 정상 읽기 (Redis 캐시 적중)
# -------------------------------------------------------------
d.t(24, 384, "2. 정상 읽기 경로 (수신자 재접속 시 Redis 캐시 적중)", 13, SOFT, KR, "start", 600)

d.msg("채팅 서버", "Redis 수신함", "LRANGE inbox:user_bob 0 -1", 416, INFO, mk="info", sub="수신함 캐시 조회")
d.msg("Redis 수신함", "채팅 서버", "msg_1001 반환 (메모리 조회)", 460, OK, mk="ok", dash="5 4", sub="메모리 즉시 전달")


# 구분선 2
d.line(24, 492, W - 24, 492, RULE, 0.8, dash="4 4")


# -------------------------------------------------------------
# 3. 장애 읽기 (Redis 다운 시 DB 폴백)
# -------------------------------------------------------------
d.t(24, 516, "3. 장애 읽기 경로 (Redis 다운 시 DB 폴백)", 13, SOFT, KR, "start", 600)

d.msg("채팅 서버", "Redis 수신함", "LRANGE inbox:user_bob 0 -1", 548, WARN, mk="warn", sub="캐시 조회 시도")
d.msg("Redis 수신함", "채팅 서버", "타임아웃 · 연결 거부", 592, BAD, mk="bad", dash="5 4", sub="Redis 노드 크래시")
d.selfmsg("채팅 서버", "경고 로그 · DB 폴백 전환", 636, WARN, sub="안전망 가동")
d.msg("채팅 서버", "DB 수신함", "SELECT WHERE delivered IS NULL", 680, ACC, mk="acc", sub="정본 테이블 조회 (디스크, 더 느림)")
d.msg("DB 수신함", "채팅 서버", "msg_1001 반환", 724, OK, mk="ok", dash="5 4", sub="수신자 정상 전달")


# -------------------------------------------------------------
# 범례 (Legend)
# -------------------------------------------------------------
d.legend(
    H - 44,
    [
        ("정상 요청", INFO),
        ("성공 응답", OK),
        ("장애 감지", BAD),
        ("폴백 전환", WARN),
        ("DB 복구 읽기 (초점)", ACC),
    ],
)

out_path = str(ASSETS_DIR / "02-01.inbox-fallback-seq.svg")
d.save(out_path)
print(f"saved: {out_path}")
