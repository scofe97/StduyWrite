"""사용자 요청부터 메타데이터 일치, 본문 로드, 템플릿 참조까지의 스킬 실행 흐름.

# 타입 스펙: type-sequence
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, INFO, INK, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=176):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
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
        s.t(mx, y - 10, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}",
               c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 12, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 14, sub, 12, MUTED, _kr(sub), "start")

W, H = 920, 620
d = SeqKR(
    W, H,
    "SKILL EXECUTION TRACE",
    "스킬 실행과 단계적 로딩 흐름",
    "사용자 요청부터 메타데이터 일치, 본문 주입, 부속 템플릿 참조까지의 시퀀스",
    lead="상시 로드된 메타데이터를 거쳐 필요한 시점에만 본문과 리소스를 호출합니다"
)

d.lanes([
    ("사용자", "User"),
    ("Claude Code", "Agent"),
    ("스킬 본문", "Level 2"),
    ("부속 리소스", "Level 3")
], y0=104, lane_w=176)

d.rails(544)

# 1. 사용자 요청
d.msg("사용자", "Claude Code", "코드 리뷰 요청", 176, MUTED,
      sub='Review code...')

# 2. 메타데이터 일치 확인
d.selfmsg("Claude Code", "메타데이터 일치 확인", 218, MUTED,
          sub="Level 1 매칭")

# 3. 스킬 본문 로드
d.msg("Claude Code", "스킬 본문", "Read SKILL.md", 262, MUTED,
      sub="code-review-specialist")

# 4. Level 2 지시문 주입 (return)
d.msg("스킬 본문", "Claude Code", "Level 2 지시문 주입", 304, INFO, mk="info", dash="4 4",
      sub="본문 로드")

# 5. 템플릿 필요 판단
d.selfmsg("Claude Code", "템플릿 필요 판단", 346, MUTED,
          sub="checklist 결정")

# 6. 부속 리소스 요청
d.msg("Claude Code", "부속 리소스", "Read templates/review-checklist.md", 390, MUTED,
      sub="Level 3 참조")

# 7. 템플릿 반환 (return)
d.msg("부속 리소스", "Claude Code", "템플릿 반환", 432, INFO, mk="info", dash="4 4",
      sub="지침 전달")

# 8. 작업 수행
d.selfmsg("Claude Code", "지시문 기반 분석", 474, MUTED,
          sub="점검 수행")

# 9. 최종 결과 응답 (focal)
d.msg("Claude Code", "사용자", "최종 결과 응답", 522, ACC, mk="acc",
      sub="보고서 반환")

d.legend(572, [("호출 요청 및 내부 처리", MUTED), ("데이터 주입 반환", INFO), ("최종 결과 응답 (focal)", ACC)])
d.save("03-01.skill-execution.svg")
