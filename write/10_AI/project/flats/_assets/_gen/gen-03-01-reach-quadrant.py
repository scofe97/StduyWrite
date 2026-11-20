# 사실 출처: README.md:234-237 · docs/networking.md:9-19 · 각 제공자 공식 문서
# 타입 스펙: type-quadrant
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "QUADRANT · REACH & CREDENTIALS",
    "도달 범위와 계정·키 필요 여부로 본 8대 네트워크 제공자",
    "인터넷 공개 여부와 외부 계정·키 요구를 기준으로 제공자들을 사분면에 배치합니다",
    lead="도메인이나 URL 유무가 아니라 패킷 접근 제어와 자격 증명이 공개 범위를 가릅니다"
)

# 2x2 축 중심 및 범위
CX, CY = 500, 304
AXIS_MIN_X, AXIS_MAX_X = 140, 860
AXIS_MIN_Y, AXIS_MAX_Y = 110, 480

# 사분면 배경 구획
# Q1: 우상단 (PUBLIC / KEY REQUIRED)
d.o.append(f'<rect x="{CX}" y="{AXIS_MIN_Y}" width="{AXIS_MAX_X - CX}" height="{CY - AXIS_MIN_Y}" fill="rgba(240,138,89,0.04)" rx="0"/>')
d.t(CX + 20, AXIS_MIN_Y + 24, "01 · PUBLIC / KEY REQUIRED", 10, ACC, MONO, "start", 600)

# Q2: 좌상단 (PUBLIC / NO KEY)
d.o.append(f'<rect x="{AXIS_MIN_X}" y="{AXIS_MIN_Y}" width="{CX - AXIS_MIN_X}" height="{CY - AXIS_MIN_Y}" fill="rgba(227,179,65,0.04)" rx="0"/>')
d.t(AXIS_MIN_X + 20, AXIS_MIN_Y + 24, "02 · PUBLIC / NO KEY", 10, WARN, MONO, "start", 600)

# Q3: 좌하단 (PRIVATE / NO KEY)
d.o.append(f'<rect x="{AXIS_MIN_X}" y="{CY}" width="{CX - AXIS_MIN_X}" height="{AXIS_MAX_Y - CY}" fill="rgba(63,185,140,0.04)" rx="0"/>')
d.t(AXIS_MIN_X + 20, CY + 24, "03 · PRIVATE / NO KEY", 10, OK, MONO, "start", 600)

# Q4: 우하단 (PRIVATE / KEY REQUIRED)
d.o.append(f'<rect x="{CX}" y="{CY}" width="{AXIS_MAX_X - CX}" height="{AXIS_MAX_Y - CY}" fill="rgba(106,149,216,0.04)" rx="0"/>')
d.t(CX + 20, CY + 24, "04 · PRIVATE / KEY REQUIRED", 10, INFO, MONO, "start", 600)

# 축 선 그리기 (Cross)
d.line(AXIS_MIN_X, CY, AXIS_MAX_X, CY, RULE, 1.2)
d.line(CX, AXIS_MAX_Y, CX, AXIS_MIN_Y, RULE, 1.2)

# 축 화살표 끝 마커
d.arrow([(AXIS_MAX_X - 10, CY), (AXIS_MAX_X, CY)], SOFT, "ar", 1.2)
d.arrow([(AXIS_MIN_X + 10, CY), (AXIS_MIN_X, CY)], SOFT, "ar", 1.2)
d.arrow([(CX, AXIS_MIN_Y + 10), (CX, AXIS_MIN_Y)], SOFT, "ar", 1.2)
d.arrow([(CX, AXIS_MAX_Y - 10), (CX, AXIS_MAX_Y)], SOFT, "ar", 1.2)

# 축 라벨
d.t(AXIS_MAX_X + 70, CY + 4, "계정·키 필요", 11, INK, KR, "middle", 600)
d.t(AXIS_MIN_X - 70, CY + 4, "계정·키 없음", 11, INK, KR, "middle", 600)
d.t(CX, AXIS_MIN_Y - 14, "인터넷 누구나 (PUBLIC)", 11, INK, KR, "middle", 600)
d.t(CX, AXIS_MAX_Y + 22, "허락한 기기만 (PRIVATE)", 11, INK, KR, "middle", 600)

# 항목 배치 함수
def item(x, y, name, desc, color=MUTED):
    d.o.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{color}"/>')
    d.t(x + 10, y - 5, name, 11, INK, KR, "start", 600)
    d.t(x + 10, y + 11, desc, 9, SOFT, KR, "start")

# Q1: 우상단 (PUBLIC / KEY REQUIRED)
item(530, 160, "Tailscale Funnel", "Tailscale 계정 · 공개 도메인 서빙", ACC)
item(700, 205, "zrok", "zrok 토큰 · public share 릴레이", ACC)
item(530, 245, "NetBird Expose", "NetBird 계정 · 역방향 프록시", ACC)

# Q2: 좌상단 (PUBLIC / NO KEY)
item(160, 175, "Cloudflare quick", "TryCloudflare · 임시 무작위 주소 · 계정 불필요", WARN)
item(260, 245, "Portal", "포털 릴레이 · 무인증 공개 서빙", WARN)

# Q3: 좌하단 (PRIVATE / NO KEY)
item(200, 395, "Local", "루프백 127.0.0.1 · 단일 머신 한정", OK)

# Q4: 우하단 (PRIVATE / KEY REQUIRED)
item(530, 385, "Tailscale", "tailnet ACL · CGNAT IP · MagicDNS", INFO)
item(690, 435, "NetBird", "Access Policies · WireGuard 피어", INFO)

# 범례
d.legend(515, [
    ("공개 (계정·키 필요)", ACC),
    ("공개 (무인증)", WARN),
    ("사설 오버레이 (ACL·키)", INFO),
    ("로컬 루프백 (기본 활성)", OK)
])

out_path = Path(__file__).parent.parent / "03-01-reach-quadrant.svg"
d.save(str(out_path))
print(f"Saved: {out_path}")
