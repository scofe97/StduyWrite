# TLS 인증서 체인 결합 순서와 Nginx·HAProxy 및 openssl s_client 검증 경로
# 타입 스펙: type-architecture
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(W, H, "02_OS / REVERSE-PROXY · 01-04",
      "TLS 인증서 체인 결합 순서와 신뢰 사슬 검증 경로",
      "서버 인증서와 중간 체인의 결합 순서, Nginx·HAProxy 설정 규칙, 그리고 역순·누락 시의 오류 판정 메커니즘",
      lead="RFC 8446 규약(서버 인증서 맨 앞→중간 CA, 루트는 생략 가능), 프록시 결합(Nginx chained crt·HAProxy pem), openssl s_client 검증")

# 2개 대구획 (좌: 정상 체인 구성과 신뢰 사슬 검증, 우: 결합 오류와 장애 판정 경로)
zones = [
    {"name": "정상 체인 구성과 TLS 신뢰 사슬 검증", "sub": "RFC 8446 규약 준수 및 프록시 결합 순서", "x": 28, "w": 436},
    {"name": "체인 결합 오류와 장애 감지 경로", "sub": "역순 배치 mismatch 와 중간 인증서 누락 장애", "x": 496, "w": 436}
]

for z in zones:
    d.box(z["x"], 100, z["w"], 46, PAPER2, RULE, 1.0, 6)
    d.t(z["x"] + z["w"] / 2, 120, z["name"], 13, INK, KR, "middle", 600)
    d.t(z["x"] + z["w"] / 2, 136, z["sub"], 11, MUTED, KR, "middle")

# -------------------------------------------------------------
# 좌측: 정상 체인 구성 파이프라인
# -------------------------------------------------------------
# 1-1. 올바른 인증서 결합 구조
d.box(28, 160, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(42, 180, "1. 올바른 인증서 결합 구조 (RFC 8446 규약)", 12, INK, KR, "start", 600)
d.t(42, 198, "cat server.crt intermediate.crt > chained.crt", 11, MUTED, MONO, "start")
d.box(40, 206, 412, 28, PAPER2, OK, 1.0, 4)
d.t(50, 224, "서버(Leaf) 인증서 맨 앞 배치 → 중간 CA 체인 후속 연결 (루트 생략)", 11, OK, KR, "start")

# 1-2. 프록시 로드 및 개인키 매칭
d.box(28, 256, 436, 96, PAPER2, RULE, 0.9, 6)
d.t(42, 276, "2. 프록시 로드 및 개인키 매칭 성공", 12, INK, KR, "start", 600)
d.t(42, 294, "Nginx: ssl_certificate | HAProxy: crt site.pem", 11, MUTED, MONO, "start")
d.box(40, 302, 198, 40, PAPER2, INFO, 1.0, 4)
d.t(50, 318, "Nginx 정상 로드:", 11, INFO, KR, "start", 600)
d.t(50, 334, "첫 인증서 공개키 == 개인키 짝", 11, INK, KR, "start")

d.box(254, 302, 198, 40, PAPER2, INFO, 1.0, 4)
d.t(264, 318, "HAProxy 단일 PEM:", 11, INFO, KR, "start", 600)
d.t(264, 334, "서버 + 중간 체인 + 비밀키", 11, INK, KR, "start")

# 1-3. 클라이언트 신뢰 사슬 검증 성공
d.box(28, 364, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(42, 384, "3. 클라이언트 신뢰 사슬 검증 성공 (Verify return code: 0)", 12, INK, KR, "start", 600)
d.t(42, 402, "openssl s_client -showcerts -servername example.com", 11, MUTED, MONO, "start")
d.t(42, 420, "서버가 보낸 중간 CA 로 로컬 루트 CA 신뢰 앵커까지 체인 완성", 11, OK, KR, "start", 600)

# -------------------------------------------------------------
# 우측: 체인 결합 오류 파이프라인
# -------------------------------------------------------------
# 2-1. 결합 순서 전도 (중간 CA 가 맨 앞)
d.box(496, 160, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(510, 180, "1. 결합 순서 전도: intermediate.crt + server.crt", 12, INK, KR, "start", 600)
d.t(510, 198, "cat intermediate.crt server.crt > wrong.crt", 11, MUTED, MONO, "start")
d.box(508, 206, 412, 28, PAPER2, BAD, 1.0, 4)
d.t(518, 224, "Nginx 기동 실패: key values mismatch (개인키와 중간CA 불일치)", 11, BAD, KR, "start", 600)

# 2-2. 중간 인증서 누락 (사일런트 실패)
d.box(496, 256, 436, 96, PAPER2, RULE, 0.9, 6)
d.t(510, 276, "2. 중간 체인 누락 (기동은 정상, 접속에서 실패)", 12, INK, KR, "start", 600)
d.t(510, 294, "ssl_certificate server.crt; (중간 CA 번들 누락)", 11, MUTED, MONO, "start")
d.box(508, 302, 198, 40, PAPER2, WARN, 1.0, 4)
d.t(518, 318, "프록시 데몬 상태:", 11, WARN, KR, "start", 600)
d.t(518, 334, "정상 기동 (첫 인증서 일치)", 11, MUTED, KR, "start")

d.box(722, 302, 198, 40, PAPER2, BAD, 1.0, 4)
d.t(732, 318, "클라이언트 검증:", 11, BAD, KR, "start", 600)
d.t(732, 334, "체인 단절 (핸드셰이크 거부)", 11, BAD, KR, "start")

# 2-3. openssl 검증 실패
d.box(496, 364, 436, 84, PAPER2, RULE, 0.9, 6)
d.t(510, 384, "3. 검증 실패: 발급자 인증서를 찾지 못함", 12, INK, KR, "start", 600)
d.t(510, 402, "openssl verify error 20 · 21 (Verify return code ≠ 0)", 11, BAD, MONO, "start")
d.t(510, 420, "중간 인증서를 저장해 둔 브라우저만 통과할 수 있음", 11, WARN, KR, "start")

# 연결 화살표 (두 구획 분리선)
d.line(480, 100, 480, 448, RULE, 0.8, "4 4")

# 하단 범례
d.legend(H - 44, [
    ("정상 결합 / 신뢰 사슬 완성", OK),
    ("규약 준수 / 프록시 구성", INFO),
    ("설정 오류 / 핸드셰이크 실패", BAD)
])

out_path = os.path.join(os.path.dirname(__file__), "..", "01-04.chapter-overview.svg")
d.save(out_path)
print("ok generated 01-04.chapter-overview.svg")
