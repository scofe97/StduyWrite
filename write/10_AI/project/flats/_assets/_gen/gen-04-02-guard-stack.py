# 사실 출처: internal/app/serve.go:545-561,673-684 · internal/api/guard.go:15-41,122-171 · internal/api/api.go:88-178 · docs/surfaces.md:17-46
# 타입 스펙: type-layers
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "MANAGEMENT SERVER · REQUEST GUARD STACK",
    "관리 서버 요청 가드 계층 구조",
    "HostGuard·Mux·agentRequest·consoleRequest 4단계 검증 체계",
    lead="루프백 리스너(127.0.0.1:7878) 유입 요청의 가드 검증과 핸들러 라우팅 흐름입니다"
)

# 좌측 진행 화살표 (요청 유입 흐름: 위에서 아래로)
d.t(48, 114, "요청 유입 ↓", 10, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(48, 128), (48, 464)], SOFT, "soft", 1.2)
d.t(48, 480, "핸들러 도달", 10, SOFT, fam=KR, anchor="middle", weight=600)

LX, LW = 96, 848
layers = [
    ("L1", "TCP 소켓 리스너 바인딩", "serve.go:522 · net.Listen",
     "127.0.0.1:7878 바인딩", "단일 TCP 리스너 · 비루프백 경고",
     "연결 수신", OK,
     PAPER2, RULE, INK),
    ("L2", "전체 요청 관문 HostGuard", "guard.go:15-41 · loopbackGuard",
     "Host & Origin 검증", "DNS Rebinding 차단 · null 거절",
     "403 Forbidden", BAD,
     PAPER2, RULE, INK),
    ("L3", "경로 다중화 & 접두사 분기", "serve.go:545-556 · ServeMux",
     "/api · /console/api · /mcp", "경로별 전용 가드 라우팅",
     "404 Not Found", WARN,
     PAPER2, RULE, INK),
    ("L4", "표면별 CSRF 격리 가드", "guard.go:122-171 · request guards",
     "요청 헤더 계약 강제", "Fetch Metadata & 전용 헤더 검사",
     "403 / 415 거부", BAD,
     PAPER2, RULE, INK),
    ("L5", "핵심 핸들러 & 승인 분기", "api.go:88-178 · if console 분기",
     "운영자 결정 권한 격리", "승인 핸들러 콘솔 전용 등록 (/api 미등록)",
     "승인 결정 보호", ACC,
     f"{ACC}14", ACC, ACC),
]

y0 = 100
h_layer = 64
gap = 10

for i, (tag, name, path_txt, chip_txt, note, block_term, rej_col, fill, stroke, text_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 태그
    tag_bg = ACC if is_focal else RULE
    d.box(LX + 12, y + 16, 36, 32, fill=PAPER, stroke=tag_bg, sw=1.0, r=4)
    d.t(LX + 30, y + 36, tag, 11, ACC if is_focal else INK, fam=MONO, weight=600)

    # 이름 및 경로
    d.t(LX + 58, y + 27, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.t(LX + 58, y + 47, path_txt, 10, MUTED, fam=MONO, anchor="start")

    # 핵심 규칙 칩 (중간 좌측)
    d.chip(LX + 360, y + 32, chip_txt, c=ACC if is_focal else OK, size=10, pad=7)

    # 설명 노트 (중간 우측)
    d.t(LX + 465, y + 36, note, 11, MUTED, fam=KR, anchor="start")

    # 차단 칩 (우측 끝)
    d.chip(LX + LW - 65, y + 32, block_term, c=rej_col, size=10, pad=6)

# 범례
d.legend(478, [
    ("정상 통과 및 구조 계층", OK),
    ("차단 및 거절 발생점", BAD),
    ("경로 미일치 경고", WARN),
    ("핵심 승인 격리 계층 (if console)", ACC),
])

out_dir = _HERE.parent
svg_path = out_dir / "04-02-guard-stack.svg"
d.save(str(svg_path))
print(f"Saved {svg_path}")
