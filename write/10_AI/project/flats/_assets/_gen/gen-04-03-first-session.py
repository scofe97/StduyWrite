# 사실 출처: README.md:158-173 · docs/agents.md:93-125,133-184 · internal/mcpx/client.go:23-37 · internal/mcpx/guide.go:38-49 · internal/mcpx/tools.go:48,78,190-203,852-860 · observations.md:43 · flats-lab/logs/08-mcp-claude-code.md:93-108
# 타입 스펙: type-sequence
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqFirstSession(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')
        s.o.insert(20, f'<marker id="info_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{INFO}"/></marker>')
        s.o.insert(21, f'<marker id="acc_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{ACC}"/></marker>')

    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 80
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 20, y + 22, lab, 11, MUTED, KR, "start")
            x += int(_w(lab, 11)) + 24

    def rails(s, ybot):
        for x in s.LX.values():
            s.line(x, s.lane_top + 6, x, ybot, RULE, 1.0, "3 6")

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        w_lbl = _w(label, 11)
        s.o.append(f'<rect x="{mx - w_lbl/2 - 4}" y="{y - 18}" width="{w_lbl + 8}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 7, label, 11, c, _kr(label), "middle", 600)
        if sub:
            w_sub = _w(sub, 10)
            s.o.append(f'<rect x="{mx - w_sub/2 - 4}" y="{y + 3}" width="{w_sub + 8}" height="15" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

W, H = 980, 750
seq = SeqFirstSession(
    W, H,
    "MCP · FIRST AGENT SESSION WORKFLOW",
    "에이전트 첫 세션의 탐색·초안 저장·승인 분리 흐름",
    "check_client → guide → save_page → create_version → 콘솔 승인 → deploy",
    lead="에이전트는 초안만 직접 작성하며 버전 생성 및 배포는 운영자 콘솔 승인을 거칩니다"
)

seq.lanes([
    ("에이전트 (Claude Code)", "stdio bridge / HTTP client"),
    ("Flats 관리 서버 (/mcp)", "Streamable HTTP 127.0.0.1:7878"),
    ("운영자 웹 콘솔", "브라우저 UI / Same-Origin")
], y0=96, lane_w=240)

seq.rails(680)

# Step 1: 호환성 확인
seq.msg("에이전트 (Claude Code)", "Flats 관리 서버 (/mcp)", "check_client {}", 165, c=INFO, sub="CLI v0.11.0 호환성 점검")
seq.msg("Flats 관리 서버 (/mcp)", "에이전트 (Claude Code)", "compatible (contract 2)", 205, c=OK, mk="ok_left", dash="3 3", sub="guide_revision 반환")

# Step 2: 가이드 탐색
seq.msg("에이전트 (Claude Code)", "Flats 관리 서버 (/mcp)", "guide {topic.index}", 245, c=INFO, sub="작업별 가이드 색인 요청")
seq.msg("Flats 관리 서버 (/mcp)", "에이전트 (Claude Code)", "guideItems 색인 반환", 285, c=OK, mk="ok_left", dash="3 3", sub="topic.page 등 안내")

# Step 3: 초안 저장
seq.msg("에이전트 (Claude Code)", "Flats 관리 서버 (/mcp)", "save_page {slug, html}", 325, c=INFO, sub="Private Draft 저장")
seq.msg("Flats 관리 서버 (/mcp)", "에이전트 (Claude Code)", "Draft rev 1 (405 B)", 365, c=OK, mk="ok_left", dash="3 3", sub="live_version: 0")

# Step 4: 버전 생성 요청 (승인 대기)
seq.msg("에이전트 (Claude Code)", "Flats 관리 서버 (/mcp)", "create_version {slug, rev:1}", 405, c=ACC, sub="초안 동결 및 승인 요청")
seq.msg("Flats 관리 서버 (/mcp)", "에이전트 (Claude Code)", "pending_approval", 445, c=ACC, mk="acc_left", dash="3 3", sub="http://127.0.0.1:7878/approvals/...")

# Step 5: 승인 요청 전달 및 콘솔 승인
seq.msg("에이전트 (Claude Code)", "운영자 웹 콘솔", "승인 URL 전달", 485, c=WARN, sub="apr-<id>")
seq.msg("운영자 웹 콘솔", "Flats 관리 서버 (/mcp)", "POST .../approve", 525, c=OK, sub="X-Flats-Console: 1")

# Step 6: 상태 확인 및 배포 요청
seq.msg("에이전트 (Claude Code)", "Flats 관리 서버 (/mcp)", "get_approval {id}", 565, c=INFO, sub="승인 상태 폴링")
seq.msg("Flats 관리 서버 (/mcp)", "에이전트 (Claude Code)", "status: approved (v1)", 605, c=OK, mk="ok_left", dash="3 3", sub="새 버전 v1 확정")

# Step 7: 배포 활성화 요청
seq.msg("에이전트 (Claude Code)", "Flats 관리 서버 (/mcp)", "deploy {slug, version:1}", 645, c=ACC, sub="라이브 서빙 승인 대기")

seq.legend(H - 46, [
    ("조회 및 검사 호출", INFO),
    ("정상 응답 및 초안 저장", OK),
    ("승인 요청 생성 (대기)", ACC),
    ("사람 운영자 확인 필요", WARN),
])

out_dir = _HERE.parent
svg_path = out_dir / "04-03-first-session.svg"
seq.save(str(svg_path))
print(f"Saved {svg_path}")
