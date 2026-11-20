# 사실 출처: internal/mcpx/tools.go:27-90 · internal/mcpx/design.go:17-34 · internal/mcpx/client.go:22-50 · internal/mcpx/guide.go:37-49 · internal/mcpx/reference.go:19-55 · observations.md:38
# 타입 스펙: type-tree
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 980, 690
d = D(
    W, H,
    "FLATS MCP · 36 TOOLS HIERARCHY",
    "엔드포인트 /mcp 로 노출되는 36개 도구 분류 트리",
    "상태 조회 13개 · 초안 쓰기 11개 · 승인 요청 7개 · 안내 계약 5개 묶음 구조",
    lead="모든 도구는 4개 기능군으로 등록되며 승인 결정(approve/reject) 도구는 없습니다"
)

COLS = [
    (
        "상태 및 자원 조회 (13)",
        "읽기 전용 및 상태 폴링",
        [
            ("list_flats", "○", OK),
            ("get_flat", "○", OK),
            ("get_draft", "○", OK),
            ("list_versions", "○", OK),
            ("get_document", "○", OK),
            ("get_design", "○", OK),
            ("list_revisions", "○", OK),
            ("get_revision", "○", OK),
            ("get_logs", "○", OK),
            ("get_approval", "○", OK),
            ("list_env", "○", OK),
            ("list_secrets", "○", OK),
            ("get_network", "○", OK),
        ]
    ),
    (
        "초안·문서 쓰기 (11)",
        "즉각 반영 및 리비전 생성",
        [
            ("create_flat", "✎", INFO),
            ("save_draft", "✎", INFO),
            ("save_draft_from_dir", "✎", INFO),
            ("save_page", "✎", INFO),
            ("save_document", "✎", INFO),
            ("update_document", "✎", INFO),
            ("save_design", "✎", INFO),
            ("pin_revision", "✎", INFO),
            ("rollback_revision", "✎", INFO),
            ("set_env", "✎", INFO),
            ("delete_env", "✎", INFO),
        ]
    ),
    (
        "승인 요청 및 위험 (7)",
        "운영자 콘솔 승인 대기",
        [
            ("create_version", "⚑", ACC),
            ("deploy", "⚑", ACC),
            ("rollback", "▲", BAD),
            ("set_visibility", "⚑", ACC),
            ("delete_flat", "▲", BAD),
            ("delete_version", "⚑", ACC),
            ("open_preview", "✎", INFO),
        ]
    ),
    (
        "호환성 및 안내 (5)",
        "클라이언트 점검 및 명세",
        [
            ("check_client", "○", OK),
            ("get_client_skill", "○", OK),
            ("guide", "○", OK),
            ("get_runtime_reference", "○", OK),
            ("get_content_types", "○", OK),
        ]
    ),
]

X0, STRIDE, GW = 24, 240, 216
RX, RY, RW, RH = 380, 96, 220, 46
GY = 176

# 연결선
d.line(RX + RW/2, RY + RH, RX + RW/2, 160, MUTED, 1.2)
cx = [X0 + i * STRIDE + GW/2 for i in range(4)]
d.line(cx[0], 160, cx[-1], 160, MUTED, 1.2)

for i, (g, gs, leaves) in enumerate(COLS):
    x = X0 + i * STRIDE
    d.line(cx[i], 160, cx[i], GY, MUTED, 1.2)
    sx = x + 10
    last_y = 240 + (len(leaves) - 1) * 28 + 12
    d.line(sx, GY + 46, sx, last_y, RULE, 1.1)
    for k in range(len(leaves)):
        ly = 240 + k * 28 + 12
        d.line(sx, ly, sx + 10, ly, RULE, 1.1)

# 루트 노드
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2, 6)
d.t(RX + RW/2, RY + 20, "루트 엔드포인트 /mcp", 13, INK, MONO, "middle", 600)
d.t(RX + RW/2, RY + 36, "에이전트 노출 도구 36개", 11, MUTED, KR, "middle")

# 4대 묶음 및 잎 노드
for i, (g, gs, leaves) in enumerate(COLS):
    x = X0 + i * STRIDE
    d.box(x, GY, GW, 46, PAPER2, RULE, 1.0, 4)
    d.t(x + GW/2, GY + 20, g, 12, INK, KR, "middle", 600)
    d.t(x + GW/2, GY + 36, gs, 10, MUTED, KR, "middle")

    for k, (name, sym, col) in enumerate(leaves):
        lx, ly = x + 20, 240 + k * 28
        lw = GW - 20
        d.box(lx, ly, lw, 24, PAPER2, RULE, 0.8, 3)
        d.t(lx + 8, ly + 16, name, 10.5, INK, MONO, "start", 500)
        d.t(lx + lw - 10, ly + 16, sym, 11, col, MONO, "end", 700)

d.legend(H - 52, [
    ("○ 읽기 전용 (ro)", OK),
    ("✎ 초안·문서 쓰기", INFO),
    ("⚑ 승인 요청 생성", ACC),
    ("▲ 파괴적 힌트", BAD),
    ("결정 도구(approve/reject) 없음", WARN),
])

out_dir = _HERE.parent
svg_path = out_dir / "04-03-tool-groups.svg"
d.save(str(svg_path))
print(f"Saved {svg_path}")
