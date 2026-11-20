# 사실 출처: README.md:38-39 · docs/design.md Approvals · 비교 제품군 공식 문서
# 타입 스펙: type-quadrant
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "QUADRANT · HOSTING & GOVERNANCE",
    "호스팅 위치와 공개 승인 여부로 본 flats의 위치",
    "인프라 격리와 사람 승인 통제를 기준으로 비교 제품군을 사분면에 배치합니다",
    "flats는 로컬 머신 격리와 사람 검토를 결합해 공개 전 콘솔 승인을 요구합니다"
)

# 2x2 축 중심 및 범위
CX, CY = 500, 304
AXIS_MIN_X, AXIS_MAX_X = 160, 840
AXIS_MIN_Y, AXIS_MAX_Y = 110, 480

# 사분면 배경 구획
# Q1: 우상단 (LOCAL / APPROVAL) - Focal
d.o.append(f'<rect x="{CX}" y="{AXIS_MIN_Y}" width="{AXIS_MAX_X - CX}" height="{CY - AXIS_MIN_Y}" fill="rgba(240,138,89,0.05)" rx="0"/>')
d.t(CX + 20, AXIS_MIN_Y + 24, "01 · LOCAL / APPROVAL", 10, ACC, MONO, "start", 600)

# Q2: 좌상단 (CLOUD / APPROVAL)
d.t(AXIS_MIN_X + 20, AXIS_MIN_Y + 24, "02 · CLOUD / APPROVAL", 10, SOFT, MONO, "start")

# Q3: 좌하단 (CLOUD / DIRECT)
d.t(AXIS_MIN_X + 20, CY + 24, "03 · CLOUD / DIRECT", 10, SOFT, MONO, "start")

# Q4: 우하단 (LOCAL / DIRECT)
d.t(CX + 20, CY + 24, "04 · SELF-HOST / DIRECT", 10, SOFT, MONO, "start")

# 축 선 그리기 (Cross)
d.line(AXIS_MIN_X, CY, AXIS_MAX_X, CY, RULE, 1.2)
d.line(CX, AXIS_MAX_Y, CX, AXIS_MIN_Y, RULE, 1.2)

# 축 화살표 끝 마커
d.arrow([(AXIS_MAX_X - 10, CY), (AXIS_MAX_X, CY)], SOFT, "ar", 1.2)
d.arrow([(AXIS_MIN_X + 10, CY), (AXIS_MIN_X, CY)], SOFT, "ar", 1.2)
d.arrow([(CX, AXIS_MIN_Y + 10), (CX, AXIS_MIN_Y)], SOFT, "ar", 1.2)
d.arrow([(CX, AXIS_MAX_Y - 10), (CX, AXIS_MAX_Y)], SOFT, "ar", 1.2)

# Jobs-minimal 단일 단어 축 라벨
d.t(AXIS_MAX_X + 68, CY + 4, "LOCAL / SELF-HOST", 10, INK, MONO, "middle", 600)
d.t(AXIS_MIN_X - 38, CY + 4, "CLOUD", 10, INK, MONO, "middle", 600)
d.t(CX, AXIS_MIN_Y - 14, "APPROVAL", 10, INK, MONO, "middle", 600)
d.t(CX, AXIS_MAX_Y + 22, "DIRECT", 10, INK, MONO, "middle", 600)

# 사분면 내 항목 배치 함수
def item(x, y, name, desc, color=MUTED, focal=False):
    r = 5 if focal else 4
    d.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
    if focal:
        d.o.append(f'<circle cx="{x}" cy="{y}" r="{r + 4}" fill="none" stroke="{color}" stroke-width="1.2" stroke-dasharray="2 2"/>')
        d.t(x + 14, y - 6, name, 13, color, KR, "start", 600)
        d.t(x + 14, y + 12, desc, 10, INK, KR, "start")
    else:
        d.t(x + 12, y - 5, name, 11, INK, KR, "start", 500)
        d.t(x + 12, y + 11, desc, 9, SOFT, KR, "start")

# 1. flats (Q1 우상단 - 초점 항목)
item(640, 190, "flats", "단일 바이너리 · 콘솔 승인 동결", ACC, focal=True)

# 2. Coolify (Q4 우하단)
item(640, 400, "Coolify", "셀프호스트 PaaS · Git 웹훅 배포", INFO)

# 3. Bottom-Left 사분면 (CLOUD / DIRECT) 항목들 (2열 배치, 세로축 x=500 침범 방지)
item(180, 350, "Cloudflare Pages/Workers", "글로벌 에지 · wrangler 배포", MUTED)
item(180, 405, "Claude Artifacts", "Anthropic 호스팅 · 세션 간 저장(20MB)", MUTED)
item(180, 455, "Netlify", "에지 호스팅 · Git 연동 배포", MUTED)
item(335, 370, "Val Town", "Deno 기반 · 브라우저 즉시 실행", MUTED)
item(335, 430, "Vercel", "서버리스 · Git 연동 배포", MUTED)

# 범례
d.legend(515, [
    ("초점 제품 (flats)", ACC),
    ("셀프호스트 PaaS (Coolify)", INFO),
    ("클라우드 호스팅 서비스", MUTED)
])

out_path = Path(__file__).parent.parent / "00-01-positioning.svg"
d.save(str(out_path))
print(f"Saved: {out_path}")
