"""Claude 와 MCP 서버, 외부 서비스 간 요청과 응답 흐름.

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
    def lanes(s, names, y0=104, lane_w=196):
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

W, H = 920, 580
d = SeqKR(
    W, H,
    "MCP REQUEST FLOW",
    "Claude 와 MCP 서버, 외부 서비스 간 요청과 응답 흐름",
    "JSON-RPC 도구 호출과 외부 REST·SQL 통신 및 표준 규격 결과 반환 시퀀스",
    lead="Claude Code 는 표준 JSON-RPC 로 요청하고 MCP 서버가 외부 규격으로 변환해 결과를 반환합니다"
)

d.lanes([
    ("Claude Code", "Client"),
    ("MCP 서버", "JSON-RPC"),
    ("외부 서비스", "REST · SQL API")
], y0=104, lane_w=196)

d.rails(496)

# 1. 이슈 조회 요청 (Query)
d.msg("Claude Code", "MCP 서버", "tools/call (list_issues)", 168, MUTED,
      sub="JSON-RPC 도구 호출")

# 2. 외부 API 호출
d.msg("MCP 서버", "외부 서비스", "GET /repos/.../issues", 212, MUTED,
      sub="REST API 쿼리")

# 3. 데이터 응답
d.msg("외부 서비스", "MCP 서버", "200 응답 (이슈 목록)", 256, INFO, mk="info", dash="4 4",
      sub="실시간 JSON 데이터")

# 4. 도구 결과 반환
d.msg("MCP 서버", "Claude Code", "tools/call 결과 반환", 300, INFO, mk="info", dash="4 4",
      sub="표준 형식 결과 전달")

# 5. 이슈 생성 요청 (Action)
d.msg("Claude Code", "MCP 서버", "tools/call (create_issue)", 352, MUTED,
      sub="JSON-RPC 조작 호출")

# 6. 외부 API 실행
d.msg("MCP 서버", "외부 서비스", "POST /repos/.../issues", 396, MUTED,
      sub="REST API 생성 요청")

# 7. 데이터 응답
d.msg("외부 서비스", "MCP 서버", "생성 결과", 440, INFO, mk="info", dash="4 4",
      sub="실행 결과 반환")

# 8. 최종 결과 반환 (focal)
d.msg("MCP 서버", "Claude Code", "최종 결과 반환", 484, ACC, mk="acc", dash="4 4",
      sub="완료 응답")

d.legend(524, [
    ("도구 호출 및 API 요청", MUTED),
    ("외부 데이터 및 표준 응답", INFO),
    ("최종 결과 반환 (Focal)", ACC)
])

d.save("03-03.mcp-request.svg")
