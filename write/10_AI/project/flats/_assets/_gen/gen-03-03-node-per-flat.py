# 사실 출처: docs/design.md:31 · docs/networking.md:88-91 · internal/expose/tsnet/tsnet.go:103 · internal/expose/tsnet/funnel.go:38
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 520
d = D(
    W, H,
    "ARCHITECTURE · NODE ISOLATION",
    "flats serve 내 tsnet 격리와 Funnel",
    "flat별 tsnet 노드와 Funnel 분기"
)

def zone(x, y, w, h, label, sub=""):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 20, label, 11, SOFT, KR, "start", 600)
    if sub:
        d.t(x + 85, y + 20, sub, 9, MUTED, MONO, "start")

zone(20, 85, 625, 415, "flats serve", "embeds tsnet · 노드 예시")

# 1. flat A (예시)
d.tone(40, 130, 275, 160, INFO, 6, "12", 1.1)
d.t(54, 154, "노드 1: <slug-a>", 11.5, INFO, KR, "start", 600)
d.t(54, 176, "<slug-a>.<tailnet>.ts.net", 9.5, INK, MONO, "start")
d.t(54, 196, "상태: tsnet/<slug-a>/", 9.5, MUTED, KR, "start")
d.t(54, 216, ":443 TLS / :80 HTTP", 9.5, MUTED, KR, "start")
d.t(54, 236, "ACME 인증서", 9.5, SOFT, KR, "start")
d.box(52, 252, 110, 24, PAPER2, OK, 0.8)
d.t(107, 268, "Private Only", 9, OK, MONO, "middle", 600)

# 2. flat B (Funnel 예시)
d.tone(345, 130, 275, 160, ACC, 6, "14", 1.2)
d.t(359, 154, "노드 2: <slug-b>", 11.5, ACC, KR, "start", 600)
d.t(359, 176, "<slug-b>.<tailnet>.ts.net", 9.5, INK, MONO, "start")
d.t(359, 196, "상태: tsnet/<slug-b>/", 9.5, MUTED, KR, "start")
d.t(359, 216, "ListenFunnel(\":443\", FunnelOnly)", 9, INK, MONO, "start")
d.t(359, 236, "Private + Public 443 공존", 9.5, MUTED, KR, "start")
d.box(357, 252, 140, 24, PAPER2, WARN, 0.8)
d.t(427, 268, "Public (Funnel)", 9, WARN, MONO, "middle", 600)

# 3. 미리보기 노드 (예시)
d.tone(40, 315, 275, 160, OK, 6, "12", 1.1)
d.t(54, 339, "노드 3: 미리보기", 11.5, OK, KR, "start", 600)
d.t(54, 361, "<slug>-<rand>.<tailnet>.ts.net", 9, INK, MONO, "start")
d.t(54, 381, "상태: mem.Store (ephemeral)", 9.5, MUTED, KR, "start")
d.t(54, 401, "독립 origin 격리", 9.5, SOFT, KR, "start")
d.t(54, 421, "배포 시 노드 로그아웃", 9.5, WARN, KR, "start")
d.box(52, 437, 130, 24, PAPER2, OK, 0.8)
d.t(117, 453, "Ephemeral Preview", 9, OK, MONO, "middle", 600)

# 4. 콘솔 도메인 노드 (설정값)
d.tone(345, 315, 275, 160, INFO, 6, "12", 1.1)
d.t(359, 339, "노드 4: 콘솔 도메인", 11.5, INFO, KR, "start", 600)
d.t(359, 361, "<console>.<tailnet>.ts.net", 9.5, INK, MONO, "start")
d.t(359, 381, "tailscale.console_hosts", 9.5, MUTED, MONO, "start")
d.t(359, 401, "관리 콘솔 · API", 9.5, MUTED, KR, "start")
d.t(359, 421, "WhoIs 승인자 기록", 9.5, SOFT, KR, "start")
d.box(357, 437, 120, 24, PAPER2, INFO, 0.8)
d.t(417, 453, "Console Domain", 9, INFO, MONO, "middle", 600)

# 우측 영역
d.tone(710, 130, 270, 160, INFO, 6, "14", 1.2)
d.t(725, 158, "Tailnet 사설망 (Private)", 12, INFO, KR, "start", 600)
d.t(725, 186, "CGNAT 100.x.y.z 피어", 10, INK, KR, "start")
d.t(725, 210, "Tailnet ACL 제어", 10, MUTED, KR, "start")
d.t(725, 234, "노드 1, 2, 3, 4 도달", 10, INFO, KR, "start")

d.tone(710, 315, 270, 160, WARN, 6, "14", 1.2)
d.t(725, 343, "공용 인터넷 (Public)", 12, WARN, KR, "start", 600)
d.t(725, 371, "누구나 접속 가능", 10, INK, KR, "start")
d.t(725, 395, "Funnel 릴레이 경유 (TCP)", 10, MUTED, KR, "start")
d.t(725, 419, "신원 헤더 삭제", 9.5, WARN, KR, "start")

# 연결선 (교차 없는 독립 라우팅)
# 1. 노드 1 (사설) -> 상단 경로 경유 Tailnet 진입
d.arrow([(260, 130), (260, 108), (632, 108), (632, 148), (710, 148)], INFO, "info")

# 2. 노드 2 (사설) -> Tailnet 직접 연결 (수평)
d.arrow([(620, 172), (710, 172)], INFO, "info")

# 3. 노드 3 & 노드 4 (사설) -> 중간 트렁크 경유 Tailnet 진입
d.arrow([(177, 315), (177, 302)], OK, "ok")
d.arrow([(482, 315), (482, 302)], INFO, "info")
d.arrow([(177, 302), (632, 302), (632, 196), (710, 196)], INFO, "info")

# 4. 노드 2 (Funnel 공개) -> 우측 전용 통로로 공용 인터넷 연결 (라벨 분리 배치)
d.arrow([(620, 264), (660, 264), (660, 395), (710, 395)], WARN, "warn", sw=1.8)
d.t(670, 305, "Funnel 개방", 9, WARN, KR, "start")

p = Path(__file__).parent.parent / "03-03-node-per-flat.svg"
d.save(p)
print(f"saved {p}")
