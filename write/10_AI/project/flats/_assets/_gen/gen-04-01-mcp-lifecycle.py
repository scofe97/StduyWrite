# 사실 출처: https://modelcontextprotocol.io/specification · internal/mcpx/mcpx.go:24-45 · internal/cli/mcpbridge.go:203-223 · observations.md:38
# 타입 스펙: type-sequence
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class McpLifecycleSeq(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')

    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 70
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 20, y + 22, lab, 11, MUTED, KR, "start")
            x += int(_w(lab, 11)) + 20

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        w_lbl = _w(label, 11)
        s.o.append(f'<rect x="{mx - w_lbl/2}" y="{y - 18}" width="{w_lbl}" height="15" fill="{PAPER}"/>')
        s.t(mx, y - 7, label, 11, c, _kr(label), "middle", 600)
        if sub:
            w_sub = _w(sub, 10)
            s.o.append(f'<rect x="{mx - w_sub/2}" y="{y + 4}" width="{w_sub}" height="14" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

W, H = 960, 620
seq = McpLifecycleSeq(
    W, H,
    "MCP · STREAMABLE HTTP PROTOCOL LIFECYCLE",
    "MCP 수명주기와 Streamable HTTP 메시지 교환",
    "초기화(initialize)부터 도구 목록 조회(tools/list) 및 실행(tools/call)까지의 전송 규격",
    lead="모든 JSON-RPC 메시지는 POST /mcp 로 전송되며 상태 비저장(Stateless)으로 도구 메타데이터를 교환합니다"
)

seq.lanes([
    ("Client (Coding Agent)", "stdio bridge / HTTP client"),
    ("Flats Host (MCP Server)", "Streamable HTTP /mcp :7878")
], y0=96, lane_w=280)

# 단계별 교환 (y 좌표)
# 1. initialize
seq.msg("Client (Coding Agent)", "Flats Host (MCP Server)",
        'POST /mcp (id:1 "initialize")', 185, c=ACC, mk="ar",
        sub="Accept: application/json, text/event-stream")

seq.msg("Flats Host (MCP Server)", "Client (Coding Agent)",
        "200 OK (capabilities 응답)", 235, c=OK, mk="ok_left",
        sub="serverInfo · tools 기능 선언")

# 2. initialized 알림
seq.msg("Client (Coding Agent)", "Flats Host (MCP Server)",
        'POST /mcp ("notifications/initialized")', 295, c=MUTED, mk="ar",
        sub="초기화 완료 (단방향 알림)")

seq.msg("Flats Host (MCP Server)", "Client (Coding Agent)",
        "202 Accepted (알림 수락)", 345, c=MUTED, mk="ok_left", dash="3 3",
        sub="응답 본문 없음")

# 3. tools/list
seq.msg("Client (Coding Agent)", "Flats Host (MCP Server)",
        'POST /mcp (id:2 "tools/list")', 405, c=INFO, mk="ar",
        sub="도구 목록 조회 (POST /mcp)")

seq.msg("Flats Host (MCP Server)", "Client (Coding Agent)",
        "200 OK (도구 36종 메타데이터)", 455, c=OK, mk="ok_left",
        sub="tools: [save_draft, create_version, ...]")

# 4. tools/call
seq.msg("Client (Coding Agent)", "Flats Host (MCP Server)",
        'POST /mcp (id:3 "tools/call")', 515, c=ACC, mk="ar",
        sub='params: {name: "save_draft", args: {...}}')

seq.msg("Flats Host (MCP Server)", "Client (Coding Agent)",
        "200 OK (도구 실행 결과)", 565, c=OK, mk="ok_left",
        sub='result: {"content":[{"type":"text", ...}]}')

seq.rails(590)

seq.legend(588, [
    ("초기화 (Handshake)", ACC),
    ("초기화 알림 (Notification)", MUTED),
    ("도구 목록 (Discovery)", INFO),
    ("성공 응답 (Result)", OK)
])

out_dir = _HERE.parent
svg_path = out_dir / "04-01-mcp-lifecycle.svg"
seq.save(str(svg_path))
print(f"Saved {svg_path}")
