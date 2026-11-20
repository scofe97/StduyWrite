# 사실 출처: README.md:228-253 · docs/networking.md · RFC 6598 · Tailscale / Cloudflare / Portal 공식 문서
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "DATA FLOW · REVERSE TUNNEL & OVERLAY",
    "공개 릴레이 역방향 터널과 오버레이 사설망 트래픽 흐름",
    "인바운드 포트 개방 없이 아웃바운드 세션으로 요청을 중계하거나 가상 IP로 직접 피어링합니다",
    lead="공개: 방문자 ──> 릴레이 ──(아웃바운드)──> 로컬 클라이언트 / 사설: 피어 ──> 100.x.y.z ──> tsnet"
)

# 2개 대형 트랙 배경
def track(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{c}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 22, label, 11, SOFT, KR, "start", 600)

track(20, 100, 960, 195, "1. 공개 릴레이 역방향 터널 경로 (Public Relay · Reverse Tunnel)", ACC)
track(20, 310, 960, 195, "2. 오버레이 사설 네트워크 경로 (Private Overlay VPN · Mesh)", INFO)

# ─────────────────────────────────────────────────────────────
# 1. 상단 트랙: 공개 릴레이 경로
# ─────────────────────────────────────────────────────────────
# 노드 1: 방문자 브라우저
d.tone(40, 140, 185, 70, INFO, 6, "14", 1.2)
d.t(54, 164, "인터넷 방문자", 12, INFO, KR, "start", 600)
d.t(54, 186, "https://<name>.<relay>", 10, INK, MONO, "start")
d.t(54, 200, "누구나 접속 가능 (Public)", 9, SOFT, KR, "start")

# 노드 2: 공개 릴레이 에지
d.box(270, 140, 190, 70, PAPER2, RULE, 1.0)
d.t(285, 164, "공개 릴레이 에지", 12, INK, KR, "start", 600)
d.t(285, 184, "공용 IP · SNI/TCP 중계 / TLS 종료", 9.5, ACC, KR, "start")
d.t(285, 198, "중계(Funnel·Portal) / 종료(Cloudflare)", 8.5, SOFT, KR, "start")

# 노드 3: 기기 내 제공자 클라이언트
d.tone(525, 140, 210, 70, ACC, 6, "14", 1.2)
d.t(540, 164, "호스트 제공자 클라이언트", 12, ACC, KR, "start", 600)
d.t(540, 186, "아웃바운드 터널 수납", 10, INK, KR, "start")
d.t(540, 200, "인바운드 포트 개방 없음", 9, SOFT, KR, "start")

# 노드 4: flat 핸들러 직접 호출
d.tone(780, 140, 180, 70, OK, 6, "14", 1.2)
d.t(795, 164, "flat 핸들러", 12, OK, KR, "start", 600)
d.t(795, 186, "siteHandler 직접 호출", 10, INK, KR, "start")
d.t(795, 200, "루프백 포트 경유 없음", 9, SOFT, KR, "start")

# 화살표 (상단 트랙)
# 방문자 -> 릴레이
d.arrow([(225, 175), (270, 175)], INFO, "info")
# 릴레이 -> 로컬 클라이언트 (터널 요청 전달)
d.arrow([(460, 165), (525, 165)], ACC, "acc")
d.t(492, 155, "요청 중계", 9, ACC, KR, "middle")
# 로컬 클라이언트 -> 릴레이 (아웃바운드 세션 유지, 점선)
d.arrow([(525, 190), (460, 190)], MUTED, "ar", dash="3 3")
d.t(492, 202, "아웃바운드 연결", 8, MUTED, KR, "middle")
# 로컬 클라이언트 -> 핸들러
d.arrow([(735, 175), (780, 175)], OK, "ok")
d.t(757, 165, "직접 호출", 9, OK, KR, "middle")


# ─────────────────────────────────────────────────────────────
# 2. 하단 트랙: 오버레이 사설 경로
# ─────────────────────────────────────────────────────────────
# 노드 1: 허락된 피어 기기
d.tone(40, 350, 185, 70, INFO, 6, "14", 1.2)
d.t(54, 374, "허락된 피어 기기", 12, INFO, KR, "start", 600)
d.t(54, 396, "인증된 tailnet / NetBird", 10, INK, KR, "start")
d.t(54, 410, "가상망 내부 접근 (Private)", 9, SOFT, KR, "start")

# 노드 2: 가상 오버레이 IP
d.box(275, 350, 190, 70, PAPER2, RULE, 1.0)
d.t(290, 374, "가상 오버레이 IP", 12, INK, KR, "start", 600)
d.t(290, 396, "100.x.y.z (MagicDNS)", 11, INFO, MONO, "start")
d.t(290, 410, "CGNAT 100.64.0.0/10 대역", 9, SOFT, KR, "start")

# 노드 3: 로컬 피어 노드
d.tone(515, 350, 215, 70, INFO, 6, "14", 1.2)
d.t(530, 374, "로컬 피어 노드 (tsnet / NetBird peer)", 11.5, INFO, KR, "start", 600)
d.t(530, 396, "WireGuard 종단 · ACL 검사", 10, INK, KR, "start")
d.t(530, 410, "직접 UDP 또는 DERP 경유", 9, SOFT, KR, "start")

# 노드 4: flat 핸들러 직접 호출
d.tone(780, 350, 180, 70, OK, 6, "14", 1.2)
d.t(795, 374, "flat 핸들러", 12, OK, KR, "start", 600)
d.t(795, 396, "siteHandler 직접 호출", 10, INK, KR, "start")
d.t(795, 410, "루프백 포트 경유 없음", 9, SOFT, KR, "start")

# 화살표 (하단 트랙)
# 피어 기기 -> 가상 IP
d.arrow([(225, 385), (275, 385)], INFO, "info")
d.t(250, 375, "DNS 해석", 9, MUTED, KR, "middle")
# 가상 IP -> 로컬 피어 노드
d.arrow([(465, 385), (515, 385)], INFO, "info")
d.t(490, 375, "암호화 터널", 9, INFO, KR, "middle")
# 로컬 피어 노드 -> 핸들러
d.arrow([(730, 385), (780, 385)], OK, "ok")
d.t(755, 375, "직접 호출", 9, OK, KR, "middle")

# 범례
d.legend(518, [
    ("공개 트래픽 (인터넷 릴레이)", ACC),
    ("사설 트래픽 (오버레이 VPN)", INFO),
    ("flat 핸들러 (siteHandler)", OK)
])

out_path = Path(__file__).parent.parent / "03-01-outbound-relay.svg"
d.save(str(out_path))
print(f"Saved: {out_path}")
