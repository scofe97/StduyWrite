# 타입 스펙: type-architecture
# 사실 출처: docs/src/routes/concepts/+page.md §Relay And Tunnel Responsibilities, docs/maintainer/architecture.md §Package Boundaries
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 480
d = D(W, H, "PORTAL-TUNNEL · RELAY AND TUNNEL OWNERSHIP",
      "Relay와 Tunnel의 책임 분리와 Reverse Session",
      "공개 중계 서버와 로컬 터널 프로세스가 소유하는 자원 및 역방향 세션 연결 경계",
      lead="릴레이는 공개 입구와 라우팅을 맡고 터널 프로세스는 신원 관리와 종단 보안을 전담합니다")

# 1. 좌측 영역: Relay Server (공개 중계 서버)
rx, ry, rw, rh = 36, 104, 372, 296
d.box(rx, ry, rw, rh, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(rx + 16, ry + 24, "RELAY SERVER", 9, INFO, MONO, "start", 600)
d.t(rx + 110, ry + 24, "공개 중계 서버 소유 영역", 12, INK, KR, "start", 600)

relay_items = [
    ("공개 인그레스", "SNI 라우터 (:443) · 포트 할당", INFO),
    ("Lease 등록소", "도메인 라우팅 테이블 · 유효기간", INFO),
    ("SNI 라우팅", "ClientHello 검사 · 세션 바인딩", INFO),
    ("인증서 관리", "와일드카드 인증서 · /v1/sign 서명", INFO),
    ("정책 집행", "진입 토큰 예산 · 속도 제한 · 차단", WARN),
]

for i, (title, desc_txt, col) in enumerate(relay_items):
    iy = ry + 42 + i * 50
    d.box(rx + 14, iy, rw - 28, 42, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.chip(rx + 76, iy + 21, title, col, size=11)
    d.t(rx + 146, iy + 25, desc_txt, 11, MUTED, KR, "start")

# 2. 우측 영역: Tunnel Process (로컬 클라이언트)
tx, ty, tw, th = 552, 104, 372, 296
d.box(tx, ty, tw, th, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(tx + 16, ty + 24, "TUNNEL PROCESS", 9, OK, MONO, "start", 600)
d.t(tx + 128, ty + 24, "로컬 터널 프로세스 소유 영역", 12, INK, KR, "start", 600)

tunnel_items = [
    ("Identity 키", "secp256k1 개인키 · SIWE 서명", OK),
    ("TLS 종단", "테넌트 TLS 핸드셰이크 · 세션 키", OK),
    ("로컬 프록시", "로컬 서비스 대상 포트 포워딩", OK),
    ("경로 라우팅", "Routed HTTP · 헤더 주입", OK),
    ("MITM 자가검증", "Self-Probe · TLS exporter 검증", WARN),
]

for i, (title, desc_txt, col) in enumerate(tunnel_items):
    iy = ty + 42 + i * 50
    d.box(tx + 14, iy, tw - 28, 42, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.chip(tx + 76, iy + 21, title, col, size=11)
    d.t(tx + 146, iy + 25, desc_txt, 11, MUTED, KR, "start")

# 3. 중앙 영역: Reverse Session (Focal)
cx, cw = 408, 144
# 상단 화살표: Tunnel -> Relay 아웃바운드 역방향 연결 (GET /sdk/connect)
d.arrow([(tx, 156), (rx + rw, 156)], c=ACC, m="acc", sw=1.6)
d.t(cx + cw // 2, 140, "아웃바운드 연결", 12, ACC, KR, "middle", 600)
d.t(cx + cw // 2, 172, "GET /sdk/connect", 11, MUTED, MONO, "middle")

# 중앙 칩: 세션 풀
d.box(cx + 14, 208, cw - 28, 76, fill=PAPER2, stroke=ACC, sw=1.4, r=6)
d.t(cx + cw // 2, 230, "Reverse Session", 11, ACC, MONO, "middle", 600)
d.t(cx + cw // 2, 248, "ReversePool", 11, INK, MONO, "middle")
d.t(cx + cw // 2, 268, "대기 세션 2개 유지", 11, MUTED, KR, "middle")

# 하단 화살표: Relay -> Tunnel 활성화 마커 및 트래픽 중계
d.arrow([(rx + rw, 336), (tx, 336)], c=INFO, m="info", sw=1.6)
d.t(cx + cw // 2, 320, "활성화 마커 전달", 12, INFO, KR, "middle", 600)
d.t(cx + cw // 2, 352, "0x02 TLS / 0x01 TCP", 11, MUTED, MONO, "middle")

# 범례
d.legend(424, [
    ("Relay 소유", INFO),
    ("Tunnel 소유", OK),
    ("역방향 세션", ACC),
    ("정책 집행", WARN),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "00-02-ownership.svg"))
d.save(out)
print(f"saved: {out}")
