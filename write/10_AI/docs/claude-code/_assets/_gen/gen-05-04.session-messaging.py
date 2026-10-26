"""세션 사이 메시지 전달과 notify_when_idle 유휴 통지 순서.

# 타입 스펙: type-sequence
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=200):
        s.LX = {
            names[0][0]: 240,
            names[1][0]: 640,
        }
        for nm, sub in names:
            x = s.LX[nm]
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 12.5, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 48} {y - 10} L {x + 48} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 58, y - 4, label, 12.5, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 58, y + 15, sub, 12, MUTED, _kr(sub), "start")

W, H = 960, 540
d = SeqKR(
    W, H,
    "SESSION MESSAGING · IDLE NOTIFICATION",
    "세션 간 메시지 전달과 유휴 통지 순서",
    "SendMessage 호출과 notify_when_idle 옵션을 통한 비동기 작업 유휴 알림 흐름",
    lead="작업 중인 대상 세션에 메시지를 전송하고 유휴 전환 시 단발 알림을 수신합니다"
)

# 참여자 레인 정의 (중앙 집중 배치로 오버플로 방지)
d.lanes([
    ("메인 세션", "요청자 (caller)"),
    ("대상 세션", "auth-refactor"),
], y0=104, lane_w=200)

d.rails(464)

# 1. 대상 세션 탐색
d.selfmsg("메인 세션", "ListAgents", 176, INFO, sub="대상 식별자 조회")

# 2. 메시지 전송 및 유휴 통지 예약
d.msg("메인 세션", "대상 세션", "SendMessage(to, message)", 244, INFO,
      sub="notify_when_idle: true 예약")

# 3. 대상 세션 활성화 및 작업 실행
d.box(d.LX["대상 세션"] - 4, 252, 8, 124, fill=PAPER2, stroke=INFO, sw=1.0)
d.chip(d.LX["대상 세션"] + 88, 296, "장시간 비동기 작업 수행", INFO, 11.5)

# 4. 대상 세션 작업 완료 및 유휴 상태 전이
d.selfmsg("대상 세션", "유휴 상태 전환", 360, MUTED, sub="단발 완료 알림 발화")

# 5. 유휴 통지 반환 (Focal: Accent, Dashed return message)
d.msg("대상 세션", "메인 세션", "단발 유휴 완료 통지", 416, ACC, mk="acc", dash="4 4",
      sub="구독 자동 만료 · 폴링 제거")

# 6. 메인 세션 후속 작업 재개
d.chip(d.LX["메인 세션"], 452, "후속 작업 진행", OK, 11.5)

# 범례
d.legend(492, [
    ("유휴 완료 통지 (Focal)", ACC),
    ("세션 메시지 요청", INFO),
    ("완료 및 진행 상태", OK),
])

d.save("05-04.session-messaging.svg")
