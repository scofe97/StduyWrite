# 타입 스펙: type-architecture
# 사실 출처: docs/src/routes/keyless-tls/+page.md §Keep the certificate key out of every tunnel,
#   portal/keyless/client.go:40-153, portal/keyless/signer.go:27-61, RFC 8446 §4.4.3, §7.1.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 480
d = D(W, H, "PORTAL-TUNNEL · KEYLESS TLS BOUNDARY",
      "보유 자원과 암호학적 신뢰 경계",
      "Relay는 인증서 개인키와 바인딩 표만 쥐고 세션 키를 갖지 못하며, Tunnel은 로컬 세션 키와 평문을 쥐지만 인증서 개인키가 없습니다.",
      lead="인증서 서명 권한과 세션 암호화 키를 분리해 중계 서버의 평문 도청을 차단합니다")

# 1. 좌측 영역: Browser (클라이언트)
bx, by, bw, bh = 24, 104, 288, 296
d.box(bx, by, bw, bh, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(bx + 16, by + 24, "BROWSER", 9, INFO, MONO, "start", 600)
d.t(bx + 76, by + 24, "클라이언트 브라우저", 12, INK, KR, "start", 600)

browser_items = [
    ("표준 WebPKI", "CA 서명 체인 확인", INFO),
    ("ECDHE 교환", "클라이언트 임시 키 쌍", INFO),
    ("세션 키 도출", "트래픽 암호화/복호화", OK),
    ("원본 평문", "사용자 HTTP 데이터", OK),
]

for i, (title, desc_txt, col) in enumerate(browser_items):
    iy = by + 46 + i * 58
    d.box(bx + 12, iy, bw - 24, 46, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.chip(bx + 64, iy + 23, title, col, size=10)
    d.t(bx + 128, iy + 27, desc_txt, 11, MUTED, KR, "start")

# 2. 중앙 영역: Relay (공개 중계 서버)
rx, ry, rw, rh = 332, 104, 296, 296
d.box(rx, ry, rw, rh, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(rx + 16, ry + 24, "RELAY", 9, WARN, MONO, "start", 600)
d.t(rx + 64, ry + 24, "공개 릴레이 서버", 12, INK, KR, "start", 600)

relay_items = [
    ("인증서 개인키", "relay-cert (서명 전용)", WARN),
    ("바인딩 레지스트리", "BindingRegistry 관리", INFO),
    ("서명 API", "/v1/sign 엔드포인트", INFO),
    ("세션 키 미보유", "L4 바이너리 패스스루", BAD),
]

for i, (title, desc_txt, col) in enumerate(relay_items):
    iy = ry + 46 + i * 58
    d.box(rx + 12, iy, rw - 24, 46, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.chip(rx + 72, iy + 23, title, col, size=10)
    d.t(rx + 144, iy + 27, desc_txt, 11, MUTED, KR, "start")

# 3. 우측 영역: Tunnel (로컬 터널 에이전트)
tx, ty, tw, th = 648, 104, 288, 296
d.box(tx, ty, tw, th, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(tx + 16, ty + 24, "TUNNEL", 9, OK, MONO, "start", 600)
d.t(tx + 72, ty + 24, "로컬 터널 에이전트", 12, INK, KR, "start", 600)

tunnel_items = [
    ("고정 인증서", "체인 PEM · 호스트명 검증", INFO),
    ("ECDHE 교환", "서버 임시 키 쌍 생성", INFO),
    ("세션 키 도출", "t13server 종단 · 평문 복호화", OK),
    ("개인키 미보유", "서명만 relay에 원격 위임", ACC),
]

for i, (title, desc_txt, col) in enumerate(tunnel_items):
    iy = ty + 46 + i * 58
    d.box(tx + 12, iy, tw - 24, 46, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.chip(tx + 64, iy + 23, title, col, size=10)
    d.t(tx + 128, iy + 27, desc_txt, 11, MUTED, KR, "start")

# 연결선/흐름 표시
# 상단: 브라우저 <-> 터널 E2E TLS 세션 키 (릴레이는 L4 바이너리 패스스루)
d.path(f"M {bx + bw} {by + 34} L {rx} {by + 34}", c=MUTED, sw=1.2, dash="4 4")
d.path(f"M {rx + rw} {by + 34} L {tx} {by + 34}", c=MUTED, sw=1.2, dash="4 4")

# 범례
d.legend(424, [
    ("평문/세션키 보유", OK),
    ("공개 인프라/검증", INFO),
    ("서명 권한 보유", WARN),
    ("복호화 권한 없음", BAD),
    ("원격 서명 요청", ACC),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-03-who-holds-what.svg"))
d.save(out)
print(f"saved: {out}")
