# 사실 출처: internal/api/guard.go:15-41,118-171 · docs/design.md:485-526 · observations.md:39
# 타입 스펙: type-dp-security-matrix
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 980, 520
d = D(
    W, H,
    "MANAGEMENT SERVER · REQUEST GUARDS MATRIX",
    "요청 유형별 보안 검증 통과 및 거부 매트릭스",
    "동일 출처 정책(SOP) 한계를 보완하는 HostGuard·CORS Preflight·Sec-Fetch-Site 다층 방어",
    lead="루프백 주소에 바인딩된 관리 서버라도 브라우저 요청과 악의적 Rebinding을 선제적으로 차단합니다"
)

cols = [
    ("요청 주체", 210),
    ("Host 검증", 140),
    ("Origin 검증", 140),
    ("Preflight 헤더", 140),
    ("Sec-Fetch-Site", 140),
    ("최종 판정", 150),
]

rows = [
    {
        "role": "콘솔 웹 콘솔",
        "sub": "http://127.0.0.1:7878",
        "cells": [
            ("일치", "127.0.0.1", OK),
            ("일치", "동일 Origin", OK),
            ("X-Flats-Console", "커스텀 헤더", OK),
            ("same-origin", "브라우저 검증", OK),
            ("통과", "API·승인 허용", OK),
        ]
    },
    {
        "role": "타 사이트 웹페이지",
        "sub": "http://evil.example",
        "cells": [
            ("통과 가능", "루프백 직접 지정", WARN),
            ("불일치 (403)", "evil 도메인", BAD),
            ("Preflight 유도", "CORS 미허락", BAD),
            ("cross-site (403)", "errCrossSite", BAD),
            ("403 거부", "CSRF 차단", BAD),
        ]
    },
    {
        "role": "DNS Rebinding",
        "sub": "evil -> 127.0.0.1",
        "cells": [
            ("불일치 (403)", "HostGuard 차단", BAD, True),  # Focal
            ("불일치 (403)", "allowedOrigin 거부", BAD),
            ("미발생", "동일 Origin 간주", WARN),
            ("헤더 없음", "비신뢰 HTTP 미전송", WARN),
            ("403 거부", "Rebinding 차단", BAD),
        ]
    },
    {
        "role": "CLI 및 로컬 에이전트",
        "sub": "CLI · stdio bridge",
        "cells": [
            ("일치", "로컬 루프백", OK),
            ("생략", "Origin 없음", OK),
            ("X-Flats-Client", "JSON 헤더", OK),
            ("생략", "비브라우저", OK),
            ("통과", "API·MCP 허용", OK),
        ]
    },
]

x0 = 24
y0 = 100
col_xs = []
cur_x = x0
for title, w in cols:
    col_xs.append((cur_x, w))
    cur_x += w + 8

# 열 헤더 그리기
for i, (title, w) in enumerate(cols):
    cx, cw = col_xs[i]
    d.box(cx, y0, cw, 32, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(cx + cw / 2, y0 + 20, title, 11, INK, KR, "middle", 600)

# 행 데이터 그리기
row_h = 68
for r_idx, r in enumerate(rows):
    ry = y0 + 40 + r_idx * (row_h + 8)

    # 행 머리 (요청 주체)
    rx, rw = col_xs[0]
    d.box(rx, ry, rw, row_h, fill=PAPER2, stroke=RULE, sw=1.0)
    d.t(rx + 14, ry + 28, r["role"], 12, INK, KR, "start", 600)
    d.t(rx + 14, ry + 48, r["sub"], 10, MUTED, MONO, "start")

    # 각 열 셀 그리기
    for c_idx, cell in enumerate(r["cells"]):
        cx, cw = col_xs[c_idx + 1]
        val, sub, col = cell[0], cell[1], cell[2]
        is_focal = len(cell) > 3 and cell[3]

        if is_focal:
            d.tone(cx, ry, cw, row_h, ACC, op="22", sw=1.6)
            d.t(cx + cw / 2, ry + 28, val, 11, ACC, KR, "middle", 600)
            d.t(cx + cw / 2, ry + 48, sub, 10, ACC, KR, "middle")
        else:
            op_val = "18" if col in (OK, BAD) else "12"
            d.tone(cx, ry, cw, row_h, col, op=op_val, sw=1.0)
            d.t(cx + cw / 2, ry + 28, val, 11, col, KR, "middle", 600)
            d.t(cx + cw / 2, ry + 48, sub, 10, MUTED, KR, "middle")

# 범례
d.legend(468, [
    ("통과 및 정상 허용", OK),
    ("차단 및 요청 거부", BAD),
    ("위협 및 우회 위험", WARN),
    ("핵심 방어 관문 (HostGuard)", ACC),
])

out_dir = _HERE.parent
svg_path = out_dir / "04-01-browser-guards.svg"
d.save(str(svg_path))
print(f"Saved {svg_path}")
