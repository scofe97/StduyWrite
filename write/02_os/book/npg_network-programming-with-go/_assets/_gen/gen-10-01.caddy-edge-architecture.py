# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.10 Figure 10-1 (Caddy reverse proxying client requests), p.2-3 (Let's Encrypt Integration, Edge network)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 460
d = D(W, H, "NPG CH.10 — CADDY EDGE ARCHITECTURE",
      "Caddy 에지 아키텍처와 TLS 자동 관리",
      "클라이언트와 백엔드 사이에서 TLS 종단과 인증서 자동 발급·갱신을 전담합니다",
      "공개 인터넷과 내부 사설망 경계에서 네트워크 토폴로지를 은닉하는 구조")

# 1. ACME CA (상단 중앙: 기본 발급자 Let's Encrypt)
ca_x, ca_y, ca_w, ca_h = 345, 96, 270, 52
d.box(ca_x, ca_y, ca_w, ca_h, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(ca_x + ca_w / 2, ca_y + 20, "Let's Encrypt", 12, INFO, MONO, "middle", 600)
d.t(ca_x + ca_w / 2, ca_y + 38, "기본 공개 ACME 인증 기관 (CA)", 11, MUTED, KR, "middle")

# ACME CA <-> Caddy 수직 연결선
d.line(475, ca_y + ca_h, 475, 178, c=INFO, sw=1.4)
d.arrow([(475, 160), (475, 178)], c=INFO, m="info", sw=1.4)
d.t(490, 162, "ACME 프로토콜 (발급·갱신)", 11, INFO, KR, "start")

# 2. Zone 1: 클라이언트 (좌측)
c_x, c_y, c_w, c_h = 24, 180, 190, 196
d.box(c_x, c_y, c_w, c_h, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(c_x + 16, c_y + 24, "CLIENT TIER", 9, SOFT, MONO, "start", 600)
d.t(c_x + c_w / 2, c_y + 54, "웹 브라우저", 13, INK, KR, "middle", 600)
d.t(c_x + c_w / 2, c_y + 74, "Web Browser / Mobile", 11, MUTED, MONO, "middle")

d.box(c_x + 16, c_y + 96, c_w - 32, 38, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(c_x + c_w / 2, c_y + 114, "HTTPS 포트 443", 11, OK, KR, "middle")
d.t(c_x + c_w / 2, c_y + 128, "TLS 암호화 채널", 11, MUTED, KR, "middle")

d.box(c_x + 16, c_y + 142, c_w - 32, 38, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(c_x + c_w / 2, c_y + 160, "HTTP 포트 80", 11, WARN, KR, "middle")
d.t(c_x + c_w / 2, c_y + 174, "자동 HTTPS 리다이렉트", 11, MUTED, KR, "middle")

# 3. Zone 2: Caddy 에지 서버 (중앙)
cad_x, cad_y, cad_w, cad_h = 296, 180, 368, 196
d.box(cad_x, cad_y, cad_w, cad_h, fill=PAPER2, stroke=ACC, sw=1.2, r=8)
d.t(cad_x + 16, cad_y + 24, "EDGE SERVER", 9, ACC, MONO, "start", 600)
d.t(cad_x + cad_w / 2, cad_y + 26, "Caddy 웹 서버 (에지 프록시)", 13, INK, KR, "middle", 600)

# Caddy 내부 모듈 1: TLS 종단
d.box(cad_x + 16, cad_y + 42, cad_w - 32, 42, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(cad_x + 28, cad_y + 60, "Automatic HTTPS 엔진", 11, INFO, KR, "start", 600)
d.t(cad_x + cad_w - 28, cad_y + 60, "TLS 종단 · 90일 만료 관리", 11, MUTED, KR, "end")
d.t(cad_x + 28, cad_y + 76, "포트 80 / 443 소켓 수신 (ACME 챌린지 검증)", 11, SOFT, KR, "start")

# Caddy 내부 모듈 2: 리버스 프록시
d.box(cad_x + 16, cad_y + 92, cad_w - 32, 42, fill=PAPER, stroke=ACC, sw=0.9, r=4)
d.t(cad_x + 28, cad_y + 110, "reverse_proxy 모듈", 11, ACC, MONO, "start", 600)
d.t(cad_x + cad_w - 28, cad_y + 110, "부하 분산 · 토폴로지 은닉", 11, MUTED, KR, "end")
d.t(cad_x + 28, cad_y + 126, "백엔드 헬스체크 및 요청 중계", 11, SOFT, KR, "start")

# Caddy 내부 모듈 3: 관리 API
d.box(cad_x + 16, cad_y + 142, cad_w - 32, 42, fill=PAPER, stroke=RULE, sw=0.9, r=4)
d.t(cad_x + 28, cad_y + 160, "Admin API (localhost:2019)", 11, INK, MONO, "start", 600)
d.t(cad_x + cad_w - 28, cad_y + 160, "무중단 JSON 설정 갱신", 11, MUTED, KR, "end")
d.t(cad_x + 28, cad_y + 176, "GET /config/ · POST /load", 10, SOFT, MONO, "start")

# 4. Zone 3: 백엔드 서비스 (우측)
b_x, b_y, b_w, b_h = 746, 180, 190, 196
d.box(b_x, b_y, b_w, b_h, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(b_x + 16, b_y + 24, "BACKEND TIER", 9, SOFT, MONO, "start", 600)
d.t(b_x + b_w / 2, b_y + 54, "Go 백엔드 서비스", 13, INK, KR, "middle", 600)
d.t(b_x + b_w / 2, b_y + 74, "net/http Web Service", 11, MUTED, MONO, "middle")

d.box(b_x + 16, b_y + 96, b_w - 32, 38, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(b_x + b_w / 2, b_y + 114, "내부 사설 네트워크", 11, INK, KR, "middle")
d.t(b_x + b_w / 2, b_y + 128, "사설망 격리 환경", 11, MUTED, KR, "middle")

d.box(b_x + 16, b_y + 142, b_w - 32, 38, fill=PAPER, stroke=WARN, sw=0.8, r=4)
d.t(b_x + b_w / 2, b_y + 160, "HTTP 포트 8080 수신", 11, WARN, MONO, "middle")
d.t(b_x + b_w / 2, b_y + 174, "순수 비즈니스 로직 전담", 11, MUTED, KR, "middle")

# 연결선 1: 클라이언트 -> Caddy (수평)
d.line(c_x + c_w, 278, cad_x, 278, c=OK, sw=1.4)
d.arrow([(cad_x - 14, 278), (cad_x, 278)], c=OK, m="ok", sw=1.4)
d.t((c_x + c_w + cad_x) / 2, 268, "HTTPS 요청", 11, OK, KR, "middle")

# 연결선 2: Caddy -> Go 백엔드 (수평)
d.line(cad_x + cad_w, 278, b_x, 278, c=WARN, sw=1.4)
d.arrow([(b_x - 14, 278), (b_x, 278)], c=WARN, m="warn", sw=1.4)
d.t((cad_x + cad_w + b_x) / 2, 268, "HTTP 전달", 11, WARN, KR, "middle")

# 범례
d.legend(406, [
    ("에지 웹 서버", ACC),
    ("인증서 자동 발급 (ACME)", INFO),
    ("암호화 구간 (HTTPS)", OK),
    ("내부망 통신 (HTTP)", WARN),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "10-01.caddy-edge-architecture.svg"))
d.save(out)
print(f"saved: {out}")
