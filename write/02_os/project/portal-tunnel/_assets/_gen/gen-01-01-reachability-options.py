# 타입 스펙: type-flowchart
# 사실 출처: RFC 1918(사설망), RFC 6598(CGNAT), RFC 6886(NAT-PMP), RFC 5389(STUN), RFC 5766(TURN), gosuda/portal-tunnel 아키텍처
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 800
d = D(
    W, H,
    "NETWORKING · INBOUND REACHABILITY DECISION FLOW",
    "외부 인바운드 접근 기술 선택과 실패 조건 분기",
    "공인 IP 보유 여부와 NAT 제어권, NAT 유형(Cone 대 대칭형)에 따른 접근 경로와 최후의 보루인 리버스 터널",
    "포트 포워딩·UPnP·홀 펀칭이 실패하는 조건과 역방향 터널의 도달 보장 원리"
)

def diamond_path(cx, cy, w, h):
    return f"M {cx} {cy - h//2} L {cx + w//2} {cy} L {cx} {cy + h//2} L {cx - w//2} {cy} Z"

def draw_diamond(cx, cy, w, h, fill=PAPER2, stroke=RULE, sw=1.2):
    d.o.append(f'<path d="{diamond_path(cx, cy, w, h)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

cx = 260
rx = 710

# 1. 시작: 서비스 외부 공개 필요
s_y = 100
d.box(cx - 100, s_y, 200, 36, fill=PAPER2, stroke=INFO, sw=1.2, r=18)
d.t(cx, s_y + 22, "사설망 서버 외부 노출 필요", 11, INK, KR, "middle", 600)

d.arrow([(cx, s_y + 36), (cx, 160)], c=INFO, m="info", sw=1.3)

# 2. Decision 1: 공인 IP 직접 할당?
d1_cy = 190
draw_diamond(cx, d1_cy, 220, 60, stroke=INFO)
d.t(cx, d1_cy - 4, "공인 IP 직접 할당?", 11, INK, KR, "middle", 600)
d.t(cx, d1_cy + 12, "호스트 NIC 공인 주소", 9, MUTED, KR, "middle")

# D1 -> Yes (직접 인바운드)
d.arrow([(cx + 110, d1_cy), (rx - 150, d1_cy)], c=OK, m="ok", sw=1.3)
d.t(cx + 130, d1_cy - 8, "Yes", 10, OK, MONO, "middle", 600)
d.box(rx - 150, d1_cy - 24, 300, 48, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(rx, d1_cy - 5, "직접 인바운드 수신", 11, OK, KR, "middle", 600)
d.t(rx, d1_cy + 13, "방화벽 포트 허용만으로 직접 도달", 10, MUTED, KR, "middle")

# D1 -> No (D2로)
d.arrow([(cx, d1_cy + 30), (cx, 280)], c=MUTED, m="ar", sw=1.3)
d.t(cx + 20, d1_cy + 45, "No", 10, MUTED, MONO, "middle", 600)

# 3. Decision 2: 공유기 포트 포워딩 가능?
d2_cy = 310
draw_diamond(cx, d2_cy, 220, 60, stroke=INFO)
d.t(cx, d2_cy - 4, "포트 포워딩 가능?", 11, INK, KR, "middle", 600)
d.t(cx, d2_cy + 12, "공유기 관리 권한 보유", 9, MUTED, KR, "middle")

# D2 -> Yes (포트 포워딩)
d.arrow([(cx + 110, d2_cy), (rx - 150, d2_cy)], c=WARN, m="warn", sw=1.3)
d.t(cx + 130, d2_cy - 8, "Yes", 10, WARN, MONO, "middle", 600)
d.box(rx - 150, d2_cy - 24, 300, 48, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(rx, d2_cy - 5, "공유기 정적 포트 매핑", 11, WARN, KR, "middle", 600)
d.t(rx, d2_cy + 13, "수동 고정 설정 · CGNAT 환경 실패", 10, MUTED, KR, "middle")

# D2 -> No (D3로)
d.arrow([(cx, d2_cy + 30), (cx, 400)], c=MUTED, m="ar", sw=1.3)
d.t(cx + 20, d2_cy + 45, "No", 10, MUTED, MONO, "middle", 600)

# 4. Decision 3: UPnP / NAT-PMP 지원?
d3_cy = 430
draw_diamond(cx, d3_cy, 220, 60, stroke=INFO)
d.t(cx, d3_cy - 4, "UPnP / NAT-PMP 지원?", 11, INK, KR, "middle", 600)
d.t(cx, d3_cy + 12, "자동 포트 매핑 프로토콜", 9, MUTED, KR, "middle")

# D3 -> Yes (UPnP)
d.arrow([(cx + 110, d3_cy), (rx - 150, d3_cy)], c=WARN, m="warn", sw=1.3)
d.t(cx + 130, d3_cy - 8, "Yes", 10, WARN, MONO, "middle", 600)
d.box(rx - 150, d3_cy - 24, 300, 48, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(rx, d3_cy - 5, "동적 포트 자동 매핑", 11, WARN, KR, "middle", 600)
d.t(rx, d3_cy + 13, "보안상 비활성화 흔함 · CGNAT 실패 (PCP 제외)", 10, MUTED, KR, "middle")

# D3 -> No (D4로)
d.arrow([(cx, d3_cy + 30), (cx, 520)], c=MUTED, m="ar", sw=1.3)
d.t(cx + 20, d3_cy + 45, "No", 10, MUTED, MONO, "middle", 600)

# 5. Decision 4: STUN 홀 펀칭 가능?
d4_cy = 550
draw_diamond(cx, d4_cy, 220, 60, stroke=INFO)
d.t(cx, d4_cy - 4, "STUN 홀 펀칭 성공?", 11, INK, KR, "middle", 600)
d.t(cx, d4_cy + 12, "Cone NAT 상호 매핑 일치", 9, MUTED, KR, "middle")

# D4 -> Yes (홀 펀칭)
d.arrow([(cx + 110, d4_cy), (rx - 150, d4_cy)], c=INFO, m="info", sw=1.3)
d.t(cx + 130, d4_cy - 8, "Yes", 10, INFO, MONO, "middle", 600)
d.box(rx - 150, d4_cy - 24, 300, 48, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(rx, d4_cy - 5, "P2P 직접 연결 (WebRTC 등)", 11, INFO, KR, "middle", 600)
d.t(rx, d4_cy + 13, "대칭형↔port-restricted·대칭형 조합 실패", 10, MUTED, KR, "middle")

# D4 -> No (최종 대안으로)
d.arrow([(cx, d4_cy + 30), (cx, 640)], c=BAD, m="bad", sw=1.3)
d.t(cx + 20, d4_cy + 45, "No", 10, BAD, MONO, "middle", 600)

# 6. 최종 노드: 릴레이 / Reverse Tunnel
box_y = 640
d.box(cx - 180, box_y, 740, 64, fill=PAPER2, stroke=ACC, sw=1.6, r=8)
d.t(cx - 180 + 370, box_y + 24, "최후의 보루: 릴레이 및 Reverse Tunnel (portal-tunnel 방식)", 13, ACC, KR, "middle", 600)
d.t(cx - 180 + 370, box_y + 46, "내부 아웃바운드 선개설로 방화벽 우회 · 바깥 방향 연결 허용 시 NAT 종류 무관 도달", 11, INK, KR, "middle")

# 범례
d.legend(740, [
    ("직접 수신 (공인 IP)", OK),
    ("로컬 매핑 (제약형)", WARN),
    ("P2P 통신 (조건부)", INFO),
    ("역방향 터널 (아웃바운드 허용 시)", ACC)
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-01-reachability-options.svg"))
d.save(out)
print(f"saved: {out}")
