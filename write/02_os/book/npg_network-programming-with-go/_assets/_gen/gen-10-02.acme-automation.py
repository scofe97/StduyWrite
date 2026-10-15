# 타입 스펙: type-sequence
# 10-02 Caddy 와 ACME CA 간 자동 HTTPS 인증서 발급 시퀀스
# 사실 출처: NPG Ch.10 Adding Automatic HTTPS, Caddy official automatic-https docs (RFC 8555)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560
d = Seq(W, H, "NPG CH.10 — AUTOMATIC HTTPS & ACME",
        "도메인 감지와 ACME 자동 HTTPS 발급 시퀀스",
        "Caddy 가 도메인을 감지해 Let's Encrypt 와 HTTP-01 챌린지를 거쳐 인증서를 발급받습니다",
        "도메인 감지 · NewOrder · 포트 80 챌린지 검증 · 포트 443 TLS 서비스 활성화")

y0 = 104
lane_w = 192
bx = 132
cx = 404
sx = 676

d.LX = {"클라이언트": bx, "Caddy 서버": cx, "ACME CA": sx}

d.box(bx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(bx, y0 + 18, "클라이언트", 13, INK, KR, "middle", 600)
d.t(bx, y0 + 34, "외부 브라우저", 11, MUTED, KR, "middle")

d.box(cx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(cx, y0 + 18, "Caddy 서버", 13, INK, KR, "middle", 600)
d.t(cx, y0 + 34, "포트 80 / 443", 11, MUTED, MONO, "middle")

d.box(sx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(sx, y0 + 18, "ACME CA", 13, INK, KR, "middle", 600)
d.t(sx, y0 + 34, "Let's Encrypt", 11, MUTED, MONO, "middle")

d.lane_top = y0 + 44
y_bot = 484
d.line(bx, d.lane_top + 6, bx, y_bot, RULE, 1.0, "3 6")
d.line(cx, d.lane_top + 6, cx, y_bot, RULE, 1.0, "3 6")
d.line(sx, d.lane_top + 6, sx, y_bot, RULE, 1.0, "3 6")

# 활성화 바
d.box(bx - 4, 452, 8, 28, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(cx - 4, 168, 8, 308, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(sx - 4, 220, 8, 212, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 1. Caddy 내부: 도메인 감지
d.arrow([(cx + 4, 168), (cx + 48, 168), (cx + 48, 188), (cx + 8, 188)], c=INFO, m="info")
d.t(cx + 56, 174, "도메인 식별 (example.com)", 12, INFO, KR, "start", 600)
d.t(cx + 56, 192, "host 매처 또는 site address", 11, MUTED, KR, "start")

# 2. Caddy -> ACME CA: NewOrder
d.msg("Caddy 서버", "ACME CA", "NewOrder (example.com)", 224, c=INFO, mk="info", sub="ACME 계정 키 기반 주문 생성")

# 3. ACME CA -> Caddy: HTTP-01 챌린지 발급
d.msg("ACME CA", "Caddy 서버", "HTTP-01 챌린지 반환", 272, c=WARN, mk="warn", dash="4 3", sub="임시 토큰 및 키 인가값 전달")

# 4. Caddy 내부: 챌린지 엔드포인트 임시 바인딩 (ACC FOCAL)
d.arrow([(cx + 4, 316), (cx + 48, 316), (cx + 48, 336), (cx + 8, 336)], c=ACC, m="acc")
d.t(cx + 56, 322, "챌린지 경로 임시 바인딩", 12, ACC, KR, "start", 600)
d.t(cx + 56, 340, "/.well-known/acme-challenge/ (:80)", 10, MUTED, MONO, "start")

# 5. ACME CA -> Caddy: 포트 80 챌린지 검증
d.msg("ACME CA", "Caddy 서버", "GET :80/.well-known/... (검증)", 376, c=WARN, mk="warn", sub="DNS A/AAAA 레코드 대상 HTTP 확인")

# 6. ACME CA -> Caddy: X.509 인증서 발급
d.msg("ACME CA", "Caddy 서버", "X.509 인증서 발급 완료", 424, c=OK, mk="ok", sub="로컬 저장소 캐시 및 갱신 큐 등록")

# 7. 클라이언트 -> Caddy: HTTPS 접속 및 80 리다이렉트
d.msg("클라이언트", "Caddy 서버", "HTTPS 접속 (:443) / 80 리다이렉트", 464, c=OK, mk="ok", sub="TLS 종료 및 백엔드 안전 중계")

# 범례
d.legend(504, [
    ("ACME 프로토콜 통신", INFO),
    ("도메인 소유권 챌린지", WARN),
    ("임시 엔드포인트 바인딩", ACC),
    ("인증서 발급 및 HTTPS 서비스", OK),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "10-02.acme-automation.svg")
d.save(out_path)
print("saved:", out_path)
