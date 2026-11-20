# 사실 출처: internal/expose/portal/portal.go:395-406 · internal/core/service.go:503-542 · 로컬 실측(2026-10-16, v0.9.1)
# 타입 스펙: type-data-flow
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560
d = D(
    W, H,
    "SURFACE · PUBLIC VS LOCAL MANAGEMENT ROUTING",
    "공개 터널 표면과 로컬 관리 포트의 격리",
    "공개 주소와 로컬 루프백 간의 엔드포인트 응답 및 접근 격리 실측 비교",
    lead="공개 주소 ──> flat 콘텐츠 200 / 관리 경로 404 vs 로컬 7878 ──> API 200 · MCP 도구 목록"
)

# 2개 구획: 공개 주소 vs 로컬 루프백
def zone(x, y, w, h, label, c):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{c}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 22, label, 11, c, KR, "start", 600)

zone(30, 96, 435, 380, "공개 주소: https://<slug>.<relay 도메인>", ACC)
zone(495, 96, 435, 380, "로컬 관리 주소: http://127.0.0.1:7878", INFO)

# 1. 공개 주소 파이프라인
d.box(46, 134, 403, 56, PAPER2, RULE, 1.0)
d.t(60, 156, "라우팅 파이프라인", 11, SOFT, KR, "start", 600)
d.t(60, 175, "Relay ──> publicHandler ──> siteHandler", 11, ACC, MONO, "start")

# 공개 주소 결과 목록
results_pub = [
    ("GET /", "200 text/html (11157B)", OK),
    ("GET /mcp", "404 text/plain (19B)", BAD),
    ("POST /mcp", "method not allowed", BAD),
    ("GET /api/flats", "404 text/plain (19B)", BAD),
    ("GET /console", "404 text/plain (19B)", BAD),
]

y_pos = 206
for req, res, col in results_pub:
    d.box(46, y_pos, 403, 42, PAPER2, RULE, 0.9)
    d.t(60, y_pos + 26, req, 11, INK, MONO, "start", 600)
    d.chip(360, y_pos + 21, res, col, size=10, pad=6)
    y_pos += 48

# 2. 로컬 관리 파이프라인
d.box(511, 134, 403, 56, PAPER2, RULE, 1.0)
d.t(525, 156, "라우팅 파이프라인", 11, SOFT, KR, "start", 600)
d.t(525, 175, "127.0.0.1:7878 LISTEN ──> Management Router", 11, INFO, MONO, "start")

results_loc = [
    ("GET /api/flats", "200 flat 목록 JSON", OK),
    ("POST /mcp", "result.tools 배열 반환", OK),
    ("GET /mcp", "405 Method Not Allowed", WARN),
    ("GET /api/system", "404 Not Found", MUTED),
]

y_pos = 206
for req, res, col in results_loc:
    d.box(511, y_pos, 403, 42, PAPER2, RULE, 0.9)
    d.t(525, y_pos + 26, req, 11, INK, MONO, "start", 600)
    d.chip(810, y_pos + 21, res, col, size=10, pad=6)
    y_pos += 48

# 하단 공통 바인딩 상태
d.tone(30, 492, 900, 48, MUTED, 6, "10", 1.0)
d.t(46, 521, "포트 바인딩:", 11, SOFT, KR, "start", 600)
d.t(124, 521, "127.0.0.1:7878 LISTEN · 127.0.0.1:7879 LISTEN (Portal 공개 중에도 외부 LISTEN 없음)", 11, INK, MONO, "start")

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-04-public-surface.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
