# 사실 출처: docs/networking.md:9-19,113-283 · docs/network-provider-lifecycle.md:239-428
# 타입 스펙: type-quadrant
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "QUADRANT · URL LIFETIME & CREDENTIALS",
    "URL 수명과 계정·키 요구 조건으로 본 네트워크 제공자 비교",
    "URL 유지성(영속성)과 외부 인증 자격 증명 요구 여부에 따른 4대 배치",
    lead="접근 제어 방식과 무관하게 터널 복구 시 URL 고정 여부와 계정 의존성이 가치를 결정합니다"
)

# 2x2 축 중심 및 범위
CX, CY = 500, 304
AXIS_MIN_X, AXIS_MAX_X = 140, 860
AXIS_MIN_Y, AXIS_MAX_Y = 110, 480

# 사분면 배경 구획
# Q1: 우상단 (URL 유지 / 계정·키 필요)
d.o.append(f'<rect x="{CX}" y="{AXIS_MIN_Y}" width="{AXIS_MAX_X - CX}" height="{CY - AXIS_MIN_Y}" fill="rgba(240,138,89,0.04)" rx="0"/>')
d.t(CX + 20, AXIS_MIN_Y + 24, "01 · URL PERSISTENT / KEY REQUIRED", 10, ACC, MONO, "start", 600)

# Q2: 좌상단 (URL 가변 / 계정·키 필요)
d.o.append(f'<rect x="{AXIS_MIN_X}" y="{AXIS_MIN_Y}" width="{CX - AXIS_MIN_X}" height="{CY - AXIS_MIN_Y}" fill="rgba(106,149,216,0.04)" rx="0"/>')
d.t(AXIS_MIN_X + 20, AXIS_MIN_Y + 24, "02 · URL DYNAMIC / KEY REQUIRED", 10, INFO, MONO, "start", 600)

# Q3: 좌하단 (URL 가변 / 계정·키 불필요)
d.o.append(f'<rect x="{AXIS_MIN_X}" y="{CY}" width="{CX - AXIS_MIN_X}" height="{AXIS_MAX_Y - CY}" fill="rgba(227,179,65,0.04)" rx="0"/>')
d.t(AXIS_MIN_X + 20, CY + 24, "03 · URL DYNAMIC / NO KEY", 10, WARN, MONO, "start", 600)

# Q4: 우하단 (URL 유지 / 계정·키 불필요)
d.o.append(f'<rect x="{CX}" y="{CY}" width="{AXIS_MAX_X - CX}" height="{AXIS_MAX_Y - CY}" fill="rgba(63,185,140,0.04)" rx="0"/>')
d.t(CX + 20, CY + 24, "04 · URL PERSISTENT / NO KEY", 10, OK, MONO, "start", 600)

# 축 선 그리기 (Cross)
d.line(AXIS_MIN_X, CY, AXIS_MAX_X, CY, RULE, 1.2)
d.line(CX, AXIS_MAX_Y, CX, AXIS_MIN_Y, RULE, 1.2)

# 축 화살표 끝 마커
d.arrow([(AXIS_MAX_X - 10, CY), (AXIS_MAX_X, CY)], SOFT, "ar", 1.2)
d.arrow([(AXIS_MIN_X + 10, CY), (AXIS_MIN_X, CY)], SOFT, "ar", 1.2)
d.arrow([(CX, AXIS_MIN_Y + 10), (CX, AXIS_MIN_Y)], SOFT, "ar", 1.2)
d.arrow([(CX, AXIS_MAX_Y - 10), (CX, AXIS_MAX_Y)], SOFT, "ar", 1.2)

# 축 라벨
d.t(AXIS_MAX_X + 70, CY + 4, "URL 유지 (영속)", 11, INK, KR, "middle", 600)
d.t(AXIS_MIN_X - 70, CY + 4, "URL 바뀜 (가변)", 11, INK, KR, "middle", 600)
d.t(CX, AXIS_MIN_Y - 14, "계정·키 필요", 11, INK, KR, "middle", 600)
d.t(CX, AXIS_MAX_Y + 22, "계정·키 불필요 (무인증)", 11, INK, KR, "middle", 600)

# 항목 배치 함수
def item(x, y, name, desc, color=INK, muted=False):
    fill_col = SOFT if muted else color
    text_col = SOFT if muted else INK
    desc_col = MUTED if muted else SOFT
    r = 3.5 if muted else 4.5
    d.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill_col}"/>')
    d.t(x + 10, y - 5, name, 11, text_col, KR, "start", 500 if muted else 600)
    d.t(x + 10, y + 11, desc, 9, desc_col, KR, "start")

# 1. zrok (예약): 우상단 (URL 유지 / 계정·키 필요)
item(525, 160, "zrok (예약 share)", "zrok 계정 토큰 · slug 이름 예약 기록 영속화", ACC)

# 2. NetBird (Private): 우상단 (URL 유지 / 계정·키 필요)
item(525, 240, "NetBird (Private)", "setup key (UUID) · extra DNS label 고정 FQDN", ACC)

# 3. NetBird Expose: 좌상단 (URL 바뀜 / 계정·키 필요)
item(180, 190, "NetBird Expose (Public)", "setup key (UUID) · 역방향 프록시 세션 재개 시 새 URL", INFO)

# 4. Cloudflare quick: 좌하단 (URL 바뀜 / 계정·키 불필요)
item(180, 390, "Cloudflare quick", "계정 불필요 · 유휴 시 회수 · random trycloudflare.com", WARN)

# 5. 참고 항목 (흐리게 - MUTED/SOFT)
# Portal: 우하단 (URL 유지 / 계정·키 불필요)
item(540, 390, "Portal (참고)", "릴레이 무인증 · slug 기반 공개 서빙 유지", SOFT, muted=True)

# Tailscale Funnel: 우상단 (URL 유지 / 계정·키 필요)
item(695, 160, "Tailscale Funnel (참고)", "tailnet 노드 키 · FQDN 도메인 유지", SOFT, muted=True)

# 범례
d.legend(515, [
    ("중점 제공자 (URL 유지)", ACC),
    ("중점 제공자 (URL 가변)", INFO),
    ("익명·무인증 (URL 가변)", WARN),
    ("참고 제공자 (흐리게)", SOFT)
])

out_path = Path(__file__).parent.parent / "03-05-provider-compare.svg"
d.save(str(out_path))
print(f"Saved: {out_path}")
