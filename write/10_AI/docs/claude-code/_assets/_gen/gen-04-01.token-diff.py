"""UserPromptSubmit 과 Stop 훅 쌍을 활용한 요청별 토큰 차분 측정 흐름.

# 타입 스펙: type-sequence
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class DiffSeq(Seq):
    def lanes(s, names, y0=104, lane_w=176):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, stroke=RULE, sw=1.0)
            s.t(x, y0 + 20, nm, 12.5, INK, KR if any("가" <= c <= "힣" for c in nm) else MONO, "middle", 600)
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
            s.t(mx, y + 16, sub, 11.5, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 6} {y - 10} L {x + 36} {y - 10} L {x + 36} {y + 10} L {x + 9} {y + 10}", c, 1.3, m="ar")
        s.t(x + 44, y - 3, label, 12, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 44, y + 15, sub, 11.5, MUTED, _kr(sub), "start")

W, H = 880, 580
d = DiffSeq(
    W, H,
    "TOKEN DIFF TRACKING · HOOK PAIR LIFECYCLE",
    "UserPromptSubmit 과 Stop 훅의 토큰 차분 측정",
    "요청 시작 시 pre_tokens 기록과 응답 완료 시 delta 계산 및 보고 흐름",
    lead="프롬프트 제출 시 기준 토큰을 임시 파일에 적고 응답이 끝날 때(Stop) 차분을 계산해 보고합니다"
)

# 1. 라이프라인 레인
d.lanes([
    ("Claude Code", "런타임"),
    ("context-tracker", "훅"),
    ("transcript.jsonl", "대화 기록"),
    ("임시 상태 파일", "claude-context-<id>.json")
], y0=96, lane_w=196)

# 2. 라이프라인 레일
d.rails(548)

# 3. 액티베이션 바
d.act("Claude Code", 152, 380)
d.act("context-tracker", 168, 140)
d.act("context-tracker", 380, 148)

# --- 1단계: UserPromptSubmit ---
d.msg("Claude Code", "context-tracker", "UserPromptSubmit", 172, INFO, "info", sub="stdin JSON")
d.msg("context-tracker", "transcript.jsonl", "read_transcript()", 202, MUTED, "ar")
d.msg("transcript.jsonl", "context-tracker", "텍스트 반환", 228, MUTED, "ar", dash="4 3")
d.selfmsg("context-tracker", "count_tokens()", 256, MUTED, sub="추정 토큰")
d.msg("context-tracker", "임시 상태 파일", "pre_tokens 저장", 286, MUTED, "ar", sub='{"pre_tokens": N}')
d.msg("context-tracker", "Claude Code", "exit 0", 312, OK, "ok", dash="4 3")

# --- 중간 세션 진행 구분선 ---
mid_y = 348
d.line(40, mid_y, W - 40, mid_y, RULE, 1.0, dash="3 3")
d.t(W / 2, mid_y - 6, "모델 응답 생성", 11.5, SOFT, KR, "middle")

# --- 2단계: Stop ---
d.msg("Claude Code", "context-tracker", "Stop 이벤트", 384, INFO, "info", sub="stdin JSON")
d.msg("context-tracker", "transcript.jsonl", "read_transcript()", 414, MUTED, "ar")
d.msg("context-tracker", "임시 상태 파일", "pre_tokens 로드", 442, MUTED, "ar")
d.selfmsg("context-tracker", "delta 계산", 472, ACC, sub="current - pre")
d.msg("context-tracker", "Claude Code", "stderr 출력", 508, ACC, "acc", dash="4 3", sub="토큰 증분")

out_path = _HERE.parent / "04-01.token-diff.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
