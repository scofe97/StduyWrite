# 타입 스펙: type-flowchart
# 10-02 Caddy 요청 라우트 평가 순서와 핸들러 분기 흐름
# 사실 출처: NPG Ch.10 Listing 10-13~10-14, Caddy routes/match/handle order
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 500
d = D(W, H, "NPG CH.10 — ROUTE DISPATCH FLOWCHART",
      "경로 매칭 순서와 핸들러 분기 흐름",
      "Caddy 가 등록된 라우트 순서대로 요청 경로를 평가해 프록시와 정적 파일로 분기합니다",
      "Route 1 매칭 · Route 2 폴백 · restrict_prefix 필터 · file_server 서비스")

# 1. 요청 진입 상자 (INFO)
bx1, by1, bw1, bh1 = 36, 140, 160, 228
d.tone(bx1, by1, bw1, bh1, INFO, op="14", sw=1.0)
d.t(bx1 + bw1 / 2, by1 + 24, "클라이언트 요청 진입", 12, INFO, KR, "middle", 600)
d.line(bx1 + 12, by1 + 38, bx1 + bw1 - 12, by1 + 38, RULE, 0.8)

d.chip(bx1 + bw1 / 2, by1 + 68, "GET /backend", INFO, 11)
d.t(bx1 + bw1 / 2, by1 + 94, "백엔드 동적 요청", 11, MUTED, KR, "middle")

d.chip(bx1 + bw1 / 2, by1 + 128, "GET /style.css", INFO, 11)
d.t(bx1 + bw1 / 2, by1 + 154, "정적 스타일시트", 11, MUTED, KR, "middle")

d.chip(bx1 + bw1 / 2, by1 + 188, "GET /.secret", BAD, 11)
d.t(bx1 + bw1 / 2, by1 + 214, "숨김 파일 접근 시도", 11, MUTED, KR, "middle")

# 화살표: 요청 진입 -> Route 1
d.arrow([(196, 180), (248, 180)], c=MUTED, m="ar")

# 2. Route 1 매칭 노드 (INFO)
rx1, ry1, rw1, rh1 = 248, 140, 224, 80
d.tone(rx1, ry1, rw1, rh1, INFO, op="16", sw=1.0)
d.t(rx1 + 16, ry1 + 24, "Route 1", 9, INFO, MONO, "start")
d.t(rx1 + 64, ry1 + 24, "match.path 검사", 12, INK, KR, "start", 600)
d.t(rx1 + 16, ry1 + 46, '["/backend", "/backend/*"]', 10, MUTED, MONO, "start")
d.t(rx1 + 16, ry1 + 66, "경로 일치 여부 순차 평가", 11, MUTED, KR, "start")

# 화살표: Route 1 -> reverse_proxy (일치 YES)
d.arrow([(472, 180), (544, 180)], c=OK, m="ok")
d.t(508, 172, "일치", 11, OK, KR, "middle", 600)

# 3. reverse_proxy 핸들러 상자 (OK)
px1, py1, pw1, ph1 = 544, 140, 216, 80
d.tone(px1, py1, pw1, ph1, OK, op="16", sw=1.0)
d.t(px1 + 16, py1 + 24, "Handler", 9, OK, MONO, "start")
d.t(px1 + 64, py1 + 24, "reverse_proxy", 12, INK, MONO, "start", 600)
d.t(px1 + 16, py1 + 46, "upstreams: localhost:8080", 10, MUTED, MONO, "start")
d.t(px1 + 16, py1 + 66, "백엔드 서비스로 중계", 11, MUTED, KR, "start")

# 화살표: reverse_proxy -> 최종 백엔드 응답
d.arrow([(760, 180), (812, 180)], c=OK, m="ok")

# 4. 백엔드 응답 상자 (OK)
ox1, oy1, ow1, oh1 = 812, 140, 112, 80
d.tone(ox1, oy1, ow1, oh1, OK, op="18", sw=1.2)
d.t(ox1 + ow1 / 2, oy1 + 32, "백엔드 수신", 12, OK, KR, "middle", 600)
d.t(ox1 + ow1 / 2, oy1 + 56, "200 OK (HTML)", 11, INK, MONO, "middle")

# 화살표: Route 1 불일치 -> Route 2
d.arrow([(360, 220), (360, 272)], c=MUTED, m="ar")
d.t(376, 248, "불일치", 11, MUTED, KR, "start")

# 5. Route 2 기본 라우트 노드 (ACC FOCAL)
rx2, ry2, rw2, rh2 = 248, 272, 224, 96
d.tone(rx2, ry2, rw2, rh2, ACC, op="16", sw=1.4)
d.t(rx2 + 16, ry2 + 24, "Route 2", 9, ACC, MONO, "start")
d.t(rx2 + 64, ry2 + 24, "기본 라우트 (폴백)", 12, INK, KR, "start", 600)
d.t(rx2 + 16, ry2 + 48, "match 없음 (모든 요청 수용)", 11, ACC, KR, "start")
d.t(rx2 + 16, ry2 + 70, "배치 순서: 반드시 파일 끝에 위치", 11, MUTED, KR, "start")

# 화살표: Route 2 -> restrict_prefix
d.arrow([(472, 320), (544, 320)], c=MUTED, m="ar")

# 6. restrict_prefix 핸들러 상자 (INFO)
fx1, fy1, fw1, fh1 = 544, 272, 216, 96
d.tone(fx1, fy1, fw1, fh1, INFO, op="16", sw=1.0)
d.t(fx1 + 16, fy1 + 24, "H1", 9, INFO, MONO, "start")
d.t(fx1 + 36, fy1 + 24, "restrict_prefix", 12, INK, MONO, "start", 600)
d.t(fx1 + 16, fy1 + 48, 'prefix = "." 숨김 세그먼트 검사', 11, MUTED, KR, "start")
d.t(fx1 + 16, fy1 + 72, "경로 정규화 후 점 접두사 필터", 11, MUTED, KR, "start")

# 분기 A: 점 접두사 발견 -> 404 차단
d.arrow([(652, 368), (652, 404)], c=BAD, m="bad")
d.t(668, 388, "숨김 탐지", 11, BAD, KR, "start")

# 404 차단 상자 (BAD)
cx1, cy1, cw1, ch1 = 544, 404, 216, 40
d.tone(cx1, cy1, cw1, ch1, BAD, op="18", sw=1.2)
d.t(cx1 + cw1 / 2, cy1 + 25, "404 Not Found 차단", 12, BAD, KR, "middle", 600)

# 분기 B: 정상 경로 통과 -> file_server
d.arrow([(760, 320), (812, 320)], c=OK, m="ok")
d.t(786, 312, "통과", 11, OK, KR, "middle")

# 7. file_server 핸들러 상자 (OK)
sx1, sy1, sw1, sh1 = 812, 272, 112, 96
d.tone(sx1, sy1, sw1, sh1, OK, op="16", sw=1.0)
d.t(sx1 + 12, sy1 + 24, "H2", 9, OK, MONO, "start")
d.t(sx1 + 32, sy1 + 24, "file_server", 11, INK, MONO, "start", 600)
d.t(sx1 + 12, sy1 + 48, "root: ./files", 10, MUTED, MONO, "start")
d.t(sx1 + 12, sy1 + 72, "200 OK 파일", 11, OK, KR, "start")

# 범례
d.legend(456, [
    ("경로 매칭 및 분기", INFO),
    ("기본 라우트 (폴백)", ACC),
    ("정상 처리 및 서비스", OK),
    ("비인가 숨김 경로 차단", BAD),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "10-02.route-dispatch.svg")
d.save(out_path)
print("saved:", out_path)
