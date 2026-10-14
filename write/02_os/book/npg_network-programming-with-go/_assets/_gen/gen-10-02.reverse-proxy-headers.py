# 타입 스펙: type-sequence
# 10-02 리버스 프록시 뒤의 소켓 주소 변화와 X-Forwarded-For 신뢰 경계
# 사실 출처: NPG Ch.10 Listing 10-9~10-10, 10-13, Caddy reverseproxy TrustedProxies
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560
d = Seq(W, H, "NPG CH.10 — REVERSE PROXY & HEADERS",
        "리버스 프록시 뒤의 주소 변화와 헤더 신뢰 경계",
        "Caddy 가 백엔드 앞단에서 중계하며 클라이언트 IP 와 신뢰 경계를 관리합니다",
        "RemoteAddr 변경 · X-Forwarded-For 주입 · 스푸핑 차단 원리")

y0 = 104
lane_w = 192
bx = 132
cx = 404
sx = 676

d.LX = {"클라이언트": bx, "Caddy 프록시": cx, "Go 백엔드": sx}

d.box(bx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(bx, y0 + 18, "클라이언트", 13, INK, KR, "middle", 600)
d.t(bx, y0 + 34, "198.51.100.42:54321", 11, MUTED, MONO, "middle")

d.box(cx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(cx, y0 + 18, "Caddy 프록시", 13, INK, KR, "middle", 600)
d.t(cx, y0 + 34, "localhost:2020", 11, MUTED, MONO, "middle")

d.box(sx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(sx, y0 + 18, "Go 백엔드", 13, INK, KR, "middle", 600)
d.t(sx, y0 + 34, "localhost:8080", 11, MUTED, MONO, "middle")

d.lane_top = y0 + 44
y_bot = 476
d.line(bx, d.lane_top + 6, bx, y_bot, RULE, 1.0, "3 6")
d.line(cx, d.lane_top + 6, cx, y_bot, RULE, 1.0, "3 6")
d.line(sx, d.lane_top + 6, sx, y_bot, RULE, 1.0, "3 6")

# 활성화 바
d.box(bx - 4, 168, 8, 268, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(cx - 4, 168, 8, 268, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(sx - 4, 272, 8, 116, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 1. 클라이언트 -> Caddy: GET /backend
d.msg("클라이언트", "Caddy 프록시", "GET /backend", 168, c=INFO, mk="info", sub="RemoteAddr: 198.51.100.42:54321")

# 2. Caddy 내부 판단: trusted_proxies 검사
d.arrow([(cx + 4, 212), (cx + 48, 212), (cx + 48, 232), (cx + 8, 232)], c=ACC, m="acc")
d.t(cx + 56, 218, "trusted_proxies 검사", 12, ACC, KR, "start", 600)
d.t(cx + 56, 236, "클라이언트 미신뢰 (신뢰 경계 확립)", 11, MUTED, KR, "start")

# 3. Caddy -> 백엔드: GET /backend (X-Forwarded-For 주입)
d.msg("Caddy 프록시", "Go 백엔드", "GET /backend (새 연결)", 272, c=ACC, mk="acc", sub="X-Forwarded-For: 198.51.100.42")

# 4. 백엔드 내부 로그 기록
d.arrow([(sx + 4, 320), (sx + 48, 320), (sx + 48, 340), (sx + 8, 340)], c=INFO, m="info")
d.t(sx + 56, 326, "RemoteAddr = 127.0.0.1:49152", 11, INK, MONO, "start", 600)
d.t(sx + 56, 344, "X-Forwarded-For: 198.51.100.42", 11, MUTED, MONO, "start")

# 5. 백엔드 -> Caddy: 200 OK (HTML 본문)
d.msg("Go 백엔드", "Caddy 프록시", "200 OK (HTML 본문)", 384, c=OK, mk="ok", sub="style.css · hiking.svg 참조 포함")

# 6. Caddy -> 클라이언트: 200 OK 중계
d.msg("Caddy 프록시", "클라이언트", "200 OK (중계 전달)", 432, c=OK, mk="ok", sub="클라이언트 응답 스트림 반환")

# 범례
d.legend(500, [
    ("외부 클라이언트 요청", INFO),
    ("Caddy 중계 및 신뢰 경계", ACC),
    ("백엔드 수신 및 최종 응답", OK),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "10-02.reverse-proxy-headers.svg")
d.save(out_path)
print("saved:", out_path)
