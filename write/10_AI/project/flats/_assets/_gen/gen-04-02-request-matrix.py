# 사실 출처: internal/api/guard.go:15-41,122-171 · internal/api/api.go:88-178 · docs/design.md:485-526 · observations.md:39
# 타입 스펙: type-dp-security-matrix
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "MANAGEMENT SERVER · REQUEST MATRIX",
    "요청 주체 및 엔드포인트별 판정 매트릭스",
    "가드 검증에 따른 엔드포인트별 응답 코드",
    lead="주체별 API 접근 및 승인 결정 요청 도달 결과입니다"
)

cols = [
    ("요청 주체", 190),
    ("GET /api/flats", 220),
    ("POST /api/flats/{slug}/deploy", 260),
    ("POST /console/api/approvals/{id}/approve", 270),
]

rows = [
    {
        "role": "CLI 도구",
        "sub": "X-Flats-Client: cli",
        "cells": [
            ("200 OK", "safeMethod", OK),
            ("202 Accepted", "pending_approval", OK),
            ("403 Forbidden", "Console 헤더 누락", BAD),
        ]
    },
    {
        "role": "HTTP API 클라이언트",
        "sub": "Content-Type: app/json",
        "cells": [
            ("200 OK", "safeMethod", OK),
            ("202 Accepted", "pending_approval", OK),
            ("403 Forbidden", "Console 헤더 누락", BAD),
        ]
    },
    {
        "role": "콘솔 브라우저",
        "sub": "X-Flats-Console: 1",
        "cells": [
            ("200 OK", "sameOrigin", OK),
            ("202 Accepted", "pending_approval", OK),
            ("200 OK", "승인 결정 집행", ACC, True),  # Focal
        ]
    },
    {
        "role": "타 사이트 페이지",
        "sub": "http://evil.example",
        "cells": [
            ("403 Forbidden", "allowedOrigin 불일치", BAD),
            ("403 Forbidden", "cross-site 차단", BAD),
            ("403 Forbidden", "Preflight 미인가", BAD),
        ]
    },
    {
        "role": "Rebinding 호스트",
        "sub": "Host: evil.example:17878",
        "cells": [
            ("403 [실측]", "HostGuard 차단", BAD),
            ("403 Forbidden", "코드 추론 (가드)", BAD),
            ("403 Forbidden", "코드 추론 (가드)", BAD),
        ]
    },
]

x0 = 24
y0 = 96
col_xs = []
cur_x = x0
for title, w in cols:
    col_xs.append((cur_x, w))
    cur_x += w + 8

# 열 헤더
for i, (title, w) in enumerate(cols):
    cx, cw = col_xs[i]
    d.box(cx, y0, cw, 32, fill=PAPER2, stroke=RULE, sw=1.0)
    font_size = 11
    if i == 3:
        font_size = 9.5
    elif i == 2:
        font_size = 10.5
    d.t(cx + cw / 2, y0 + 20, title, font_size, INK, KR if i == 0 else MONO, "middle", 600)

# 행 데이터
row_h = 58
for r_idx, r in enumerate(rows):
    ry = y0 + 38 + r_idx * (row_h + 8)

    # 행 머리 (요청 주체)
    rx, rw = col_xs[0]
    d.box(rx, ry, rw, row_h, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(rx + 14, ry + 25, r["role"], 12, INK, KR, "start", 600)
    d.t(rx + 14, ry + 43, r["sub"], 10, MUTED, MONO, "start")

    # 각 열 셀
    for c_idx, cell in enumerate(r["cells"]):
        cx, cw = col_xs[c_idx + 1]
        val, sub, col = cell[0], cell[1], cell[2]
        is_focal = len(cell) > 3 and cell[3]

        if is_focal:
            d.tone(cx, ry, cw, row_h, ACC, op="22", sw=1.6)
            d.t(cx + cw / 2, ry + 25, val, 11, ACC, KR, "middle", 600)
            d.t(cx + cw / 2, ry + 43, sub, 10, ACC, KR, "middle")
        else:
            op_val = "18" if col in (OK, BAD) else "12"
            d.tone(cx, ry, cw, row_h, col, op=op_val, sw=1.0)
            d.t(cx + cw / 2, ry + 25, val, 11, col, KR, "middle", 600)
            d.t(cx + cw / 2, ry + 43, sub, 10, MUTED, KR, "middle")

# 범례
d.legend(484, [
    ("정상 통과 (200 / 202)", OK),
    ("차단 및 거부 (403)", BAD),
    ("유일한 승인 실행점 (콘솔 전용)", ACC),
])

out_dir = _HERE.parent
svg_path = out_dir / "04-02-request-matrix.svg"
d.save(str(svg_path))
print(f"Saved {svg_path}")
