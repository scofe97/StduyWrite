# 사실 출처: gosuda/portal-tunnel 0a3b9c06 · sdk/listener.go:37(defaultReadyTarget=2) · portal/server.go:968-1014(InspectClientHello, bridgeLeaseConn) · 로컬 실측(2026-10-17, README 「직접 띄워 보기」)
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 540
d = D(
    W, H,
    "ARCHITECTURE · REVERSE TUNNEL & TLS BOUNDARY",
    "아웃바운드 역방향 연결과 로컬 테넌트 TLS 종단 구조",
    "터널이 외부 릴레이로 TCP 연결을 미리 열어두고, 브라우저의 암호화 요청이 그 연결을 거꾸로 타고 들어옵니다",
    "번호는 연결 수립과 요청 전달 순서"
)


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 20, label, 11, SOFT, KR, "start", 600)


def badge(cx, cy, n, c):
    d.o.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="{PAPER}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, n, 11, c, MONO, "middle", 600)


# 영역 정의 (W=1000)
zone(32, 104, 356, 368, "사설망 (로컬 호스트 · NAT 내부)")
zone(404, 104, 152, 368, "경계 (NAT · 방화벽)")
zone(572, 104, 396, 368, "공인망 (인터넷 · Relay)")

# 노드 좌표 (4의 배수)
LOCAL_X, LOCAL_Y, LOCAL_W, LOCAL_H = 44, 168, 120, 76
TUNNEL_X, TUNNEL_Y, TUNNEL_W, TUNNEL_H = 240, 168, 136, 252

NAT_X, NAT_Y, NAT_W, NAT_H = 424, 216, 112, 160

RELAY_X, RELAY_Y, RELAY_W, RELAY_H = 584, 168, 144, 252
CLIENT_X, CLIENT_Y, CLIENT_W, CLIENT_H = 832, 216, 124, 152

# 화살표 연결선 (노드보다 먼저 렌더링)
# 1. 터널 -> 릴레이 사전 아웃바운드 연결 (NAT 아래: y = 412)
d.arrow([(TUNNEL_X + TUNNEL_W, 412), (RELAY_X, 412)], OK, "ok", 1.6)

# 2. 브라우저 -> 릴레이 공개 요청 (y = 260)
d.arrow([(CLIENT_X, 260), (RELAY_X + RELAY_W, 260)], INFO, "ar", 1.6)

# 3. 릴레이 -> 터널 암호문 전달 (NAT 위: y = 184)
d.arrow([(RELAY_X, 184), (TUNNEL_X + TUNNEL_W, 184)], ACC, "acc", 1.8)

# 4. 터널 -> 로컬 서비스 평문 전달 (y = 206)
d.arrow([(TUNNEL_X, 206), (LOCAL_X + LOCAL_W, 206)], INFO, "ar", 1.4)

# 5. 차단된 직접 인바운드 시도 (y = 160, 점선 + X)
d.path("M 528 160 L 452 160", BAD, 1.2, dash="4 4")
d.t(440, 164, "✕", 14, BAD, MONO, "middle", 600)

# 노드 상자 렌더링
# 로컬 서비스
d.box(LOCAL_X, LOCAL_Y, LOCAL_W, LOCAL_H, PAPER2, INFO, 1.1)
d.t(LOCAL_X + LOCAL_W / 2, LOCAL_Y + 30, "로컬 서비스", 13, INK, KR, "middle", 600)
d.t(LOCAL_X + LOCAL_W / 2, LOCAL_Y + 52, "127.0.0.1:13000", 11, MUTED, MONO, "middle")

# Portal Tunnel 노드 (Focal Accent)
d.tone(TUNNEL_X, TUNNEL_Y, TUNNEL_W, TUNNEL_H, ACC, op="12", sw=1.5)
d.t(TUNNEL_X + TUNNEL_W / 2, TUNNEL_Y + 28, "Portal Tunnel", 13, INK, KR, "middle", 600)
d.t(TUNNEL_X + TUNNEL_W / 2, TUNNEL_Y + 48, "테넌트 TLS 1.3 종단", 11, ACC, KR, "middle", 600)
d.t(TUNNEL_X + TUNNEL_W / 2, TUNNEL_Y + 84, "세션 키 도출 (E2E)", 10, SOFT, KR, "middle")
d.t(TUNNEL_X + TUNNEL_W / 2, TUNNEL_Y + 112, "readyTarget = 2", 10, OK, MONO, "middle")
d.t(TUNNEL_X + TUNNEL_W / 2, TUNNEL_Y + 140, "secp256k1 신원", 10, SOFT, MONO, "middle")
d.t(TUNNEL_X + TUNNEL_W / 2, TUNNEL_Y + 168, "127.0.0.1 로컬 중계", 10, MUTED, KR, "middle")

# NAT · 방화벽 노드
d.box(NAT_X, NAT_Y, NAT_W, NAT_H, PAPER2, WARN, 1.1)
d.t(NAT_X + NAT_W / 2, NAT_Y + 26, "NAT · 방화벽", 13, INK, KR, "middle", 600)
d.t(NAT_X + NAT_W / 2, NAT_Y + 46, "conntrack 테이블", 11, MUTED, MONO, "middle")
d.t(NAT_X + NAT_W / 2, NAT_Y + 80, "인바운드 차단", 10, BAD, KR, "middle")
d.t(NAT_X + NAT_W / 2, NAT_Y + 104, "아웃바운드 허용", 10, OK, KR, "middle")
d.t(NAT_X + NAT_W / 2, NAT_Y + 128, "상태 기반 역추적", 10, MUTED, KR, "middle")

# Relay Server 노드
d.box(RELAY_X, RELAY_Y, RELAY_W, RELAY_H, PAPER2, INFO, 1.1)
d.t(RELAY_X + RELAY_W / 2, RELAY_Y + 28, "Relay Server", 13, INK, KR, "middle", 600)
d.t(RELAY_X + RELAY_W / 2, RELAY_Y + 48, ":443 SNI 라우터", 11, INFO, KR, "middle")
d.t(RELAY_X + RELAY_W / 2, RELAY_Y + 84, "ClientHello 파싱", 10, SOFT, KR, "middle")
d.t(RELAY_X + RELAY_W / 2, RELAY_Y + 112, "암호문 원시 브리지", 10, MUTED, KR, "middle")
d.t(RELAY_X + RELAY_W / 2, RELAY_Y + 140, "/v1/sign 키리스 서명", 10, SOFT, KR, "middle")
d.t(RELAY_X + RELAY_W / 2, RELAY_Y + 168, "테넌트 평문 불투명", 10, OK, KR, "middle")

# 외부 브라우저 노드
d.box(CLIENT_X, CLIENT_Y, CLIENT_W, CLIENT_H, PAPER2, INFO, 1.1)
d.t(CLIENT_X + CLIENT_W / 2, CLIENT_Y + 36, "외부 브라우저", 13, INK, KR, "middle", 600)
d.t(CLIENT_X + CLIENT_W / 2, CLIENT_Y + 58, "curl / Web Client", 11, MUTED, KR, "middle")
d.t(CLIENT_X + CLIENT_W / 2, CLIENT_Y + 98, "demo-f7dc... 접속", 10, INFO, MONO, "middle")

# 배지와 라벨
# 1번: 아웃바운드 연결
badge(480, 412, "1", OK)
d.t(480, 436, "outbound TCP (ready=2)", 11, OK, MONO, "middle")

# 2번: 공개 요청
badge(780, 260, "2", INFO)
d.t(780, 236, "SNI: demo-...", 10, INFO, MONO, "middle")

# 3번: 암호문 포워딩
badge(480, 184, "3", ACC)
d.t(480, 206, "ciphertext (기존 세션 탑승)", 11, ACC, KR, "middle")

# 4번: 로컬 중계
badge(202, 206, "4", INFO)
d.t(202, 184, "평문 HTTP 중계", 10, INFO, KR, "middle")

# 차단 라벨 (경계 상단)
d.t(484, 146, "인바운드 직접 연결 불가", 11, BAD, KR, "middle")

d.legend(H - 44, [
    ("테넌트 TLS 종단 (복호화 수행 · 세션 키 보유)", ACC),
    ("사전 개설된 아웃바운드 역방향 연결", OK),
    ("암호문 중계 및 애플리케이션 트래픽", INFO),
    ("외부 진입 차단 (방화벽 · 공인 IP 부재)", BAD),
])

out_path = Path(__file__).parent.parent / "00-01-reverse-tunnel.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")

