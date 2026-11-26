# 사실 출처: Spring Security 7.1.1 SessionRegistryImpl·SecurityContextLogoutHandler·ConcurrentSessionFilter
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*d} {y} L {x2-12*d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 12, c, _kr(label), "start")
        if sub:
            s.t(x + 68, y + 13, sub, 12, MUTED, _kr(sub), "start")


seq = SeqKR(
    880, 960,
    "SEQUENCE · PASSWORD CHANGE, ALL SESSIONS CUT",
    "비밀번호 변경: 지금 세션은 바로, 다른 세션은 다음 요청에서",
    "expireAll 로 만료를 표시하고 지금 세션만 그 자리에서 무효화, 브라우저 B 는 다음 요청에서 401",
    "UserSessions.expireAll · SecurityContextLogoutHandler · ConcurrentSessionFilter"
)

seq.lanes([
    ("브라우저 A", "쿠키 sid-A"),
    ("서버", "컨트롤러 · 필터"),
    ("SessionRegistry", "서버 메모리 표"),
    ("브라우저 B", "쿠키 sid-B"),
], y0=104, lane_w=160)

ROWS_A = [196, 252, 308, 364, 420, 476]
BAND = 540
ROWS_B = [628, 684, 740, 796, 852]
END_Y = 884

for _x in seq.LX.values():
    seq.line(_x, seq.lane_top + 6, _x, BAND - 12, RULE, 1.0, "3 6")
    seq.line(_x, BAND + 36, _x, END_Y, RULE, 1.0, "3 6")

# 장면 1: 브라우저 A 가 비밀번호를 바꾼다
seq.msg("브라우저 A", "서버", "POST /api/my/password", ROWS_A[0], INK, sub="본문: 현재 · 새 비밀번호")
seq.selfmsg("서버", "changePassword", ROWS_A[1], INFO, sub="새 해시 저장")
seq.msg("서버", "SessionRegistry", "expireAll(userId)", ROWS_A[2], ACC, sub="sid-A · sid-B 둘 다")
seq.selfmsg("SessionRegistry", "expireNow()", ROWS_A[3], ACC, sub="expired = true")
seq.selfmsg("서버", "logout()", ROWS_A[4], BAD, sub="sid-A 세션 무효화")
seq.msg("서버", "브라우저 A", "204 No Content", ROWS_A[5], OK, dash="3 3", sub="Set-Cookie: JSESSIONID 삭제")

# 시간 경과 띠
seq.line(32, BAND, 848, BAND, RULE, 1.0, dash="4 3")
seq.t(36, BAND + 24, "시간 경과 · sid-B 는 톰캣 메모리에 그대로", 12, SOFT, KR, "start")

# 장면 2: 브라우저 B 의 다음 요청
seq.msg("브라우저 B", "서버", "GET /api/my/account", ROWS_B[0], INK, sub="Cookie: JSESSIONID=sid-B")
seq.msg("서버", "SessionRegistry", "getSessionInformation", ROWS_B[1], INFO, sub="키: sid-B")
seq.msg("SessionRegistry", "서버", "expired = true", ROWS_B[2], BAD, dash="3 3", sub="만료 표시 확인")
seq.selfmsg("서버", "logout()", ROWS_B[3], BAD, sub="sid-B 세션 무효화")
seq.msg("서버", "브라우저 B", "401 Unauthorized", ROWS_B[4], BAD, dash="3 3", sub="컨트롤러 미도달")

seq.legend(END_Y + 20, [
    ("만료 표시 (핵심)", ACC),
    ("무효화 · 차단", BAD),
    ("정상 응답 (204)", OK),
    ("저장 · 조회", INFO),
])

out_path = Path(__file__).parent.parent / "02-02.session-invalidation.svg"
seq.save(str(out_path))
print(f"생성 완료: {out_path}")
