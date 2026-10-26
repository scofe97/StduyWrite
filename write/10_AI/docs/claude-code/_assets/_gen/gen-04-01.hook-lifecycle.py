"""Claude Code 와 훅 프로세스 사이의 이벤트 전달과 판정 수명주기.

# 타입 스펙: type-sequence
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class HookSeq(Seq):
    def lanes(s, names, y0=104, lane_w=196):
        s.LX = {
            "Claude Code": 220,
            "훅 프로세스": 540,
        }
        for nm, sub in names:
            x = s.LX[nm]
            s.box(x - lane_w / 2, y0, lane_w, 44, stroke=RULE, sw=1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 11.5, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def act(s, who, y_top, h):
        x = s.LX[who]
        s.o.append(f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_top + h}" stroke="rgba(245,245,243,0.08)" stroke-width="8"/>')
        s.o.append(f'<line x1="{x - 4}" y1="{y_top}" x2="{x - 4}" y2="{y_top + h}" stroke="{MUTED}" stroke-width="0.8"/>')
        s.o.append(f'<line x1="{x + 4}" y1="{y_top}" x2="{x + 4}" y2="{y_top + h}" stroke="{MUTED}" stroke-width="0.8"/>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 8 * d} {y} L {x2 - 10 * d} {y}", c, 1.4, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 16, sub, 11, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 6} {y - 10} L {x + 32} {y - 10} L {x + 32} {y + 10} L {x + 9} {y + 10}", c, 1.3, m="ar")
        s.t(x + 40, y - 3, label, 12, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 40, y + 15, sub, 11, MUTED, _kr(sub), "start")

W, H = 820, 500
d = HookSeq(
    W, H,
    "HOOK LIFECYCLE · EVENT & DECISION",
    "훅 프로세스 이벤트 전달과 수명주기 판정",
    "이벤트 발생 시 stdin JSON 전달과 종료 코드·stdout JSON 에 따른 판정 분기",
    lead="표준 입력으로 세션 맥락을 받고 종료 코드와 표준 출력으로 도구 실행을 제어합니다"
)

# 1. 라이프라인 레인
d.lanes([
    ("Claude Code", "런타임 제어"),
    ("훅 프로세스", "독립 프로세스")
], y0=96, lane_w=196)

# 2. 라이프라인 레일
d.rails(464)

# 3. 액티베이션 바
d.act("Claude Code", 152, 290)
d.act("훅 프로세스", 172, 250)

# 4. 이벤트 트리거 및 stdin JSON 전달
d.msg("Claude Code", "훅 프로세스", "stdin JSON 전달", 176, INFO, "info", sub="session_id · hook_event_name · tool_input")

# 5. 프로세스 내부 검증 (Self-message)
d.selfmsg("훅 프로세스", "정책 규칙 검증", 218, MUTED, sub="보안 패턴 대조 및 인자 검사")

# 6. ALT 프레임 (exit 0 정상 vs exit 2 차단)
fx, fy, fw, fh = 60, 260, 700, 180
d.o.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="4" fill="rgba(245,245,243,0.03)" stroke="{RULE}" stroke-width="1"/>')
# ALT 탭
d.o.append(f'<rect x="{fx}" y="{fy}" width="42" height="18" rx="2" fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
d.t(fx + 21, fy + 12, "ALT", 9, SOFT, MONO, "middle", 600)

# Region 1: exit 0
d.t(236, fy + 15, "[exit 0 · 정상 종료]", 11, OK, MONO, "start", 600)
d.msg("훅 프로세스", "Claude Code", "stdout JSON 반환", 302, ACC, "acc", dash="4 3", sub='permissionDecision: "allow"')

# Divider
div_y = 352
d.line(fx + 8, div_y, fx + fw - 8, div_y, RULE, 1.0, dash="4 3")

# Region 2: exit 2
d.t(236, div_y + 17, "[exit 2 · 차단 오류]", 11, BAD, MONO, "start", 600)
d.msg("훅 프로세스", "Claude Code", "stderr 차단 사유 전달", 396, BAD, "bad", dash="4 3", sub="도구 실행 즉시 취소 및 오류 메시지")

out_path = _HERE.parent / "04-01.hook-lifecycle.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
