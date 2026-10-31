"""생성물 드리프트 검사와 행동 검증 수준으로 본 스킬 저장소 사분면."""
# 사실 출처: dalcom-skills-structure.md:121-206, 300-305, 324-328
# 타입 스펙: type-quadrant
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 560
d = D(
    W, H,
    "REPO POSITIONING · DRIFT VS BEHAVIOR",
    "생성물 드리프트 검사와 행동 검증으로 본 스킬 저장소",
    "가로축은 생성물 드리프트 검사 수준, 세로축은 행동 검증 수준을 나타내며 각 저장소의 검증 경계를 사분면에 배치합니다",
    lead="정적 매니페스트 동기화부터 런타임 CLI 모델 실행 평가까지 저장소마다 기계로 강제하는 경계가 다릅니다"
)

# 2x2 축 중심 및 범위
CX, CY = 480, 290
AX_MIN_X, AX_MAX_X = 140, 820
AX_MIN_Y, AX_MAX_Y = 105, 475

# 사분면 배경 구획 (은은한 틴트)
# Q1: 우상단 (게이트와 실측)
d.o.append(f'<rect x="{CX}" y="{AX_MIN_Y}" width="{AX_MAX_X - CX}" height="{CY - AX_MIN_Y}" fill="rgba(240,138,89,0.04)"/>')
d.t(CX + 18, AX_MIN_Y + 22, "게이트와 실측", 13, ACC, KR, "start", 600)

# Q2: 좌상단 (실측 중심)
d.o.append(f'<rect x="{AX_MIN_X}" y="{AX_MIN_Y}" width="{CX - AX_MIN_X}" height="{CY - AX_MIN_Y}" fill="rgba(245,245,243,0.02)"/>')
d.t(CX - 18, AX_MIN_Y + 22, "실측 중심", 13, SOFT, KR, "end", 600)

# Q3: 좌하단 (수동 관리)
d.o.append(f'<rect x="{AX_MIN_X}" y="{CY}" width="{CX - AX_MIN_X}" height="{AX_MAX_Y - CY}" fill="rgba(94,107,126,0.03)"/>')
d.t(CX - 18, AX_MAX_Y - 14, "수동 관리", 13, SOFT, KR, "end", 600)

# Q4: 우하단 (정적 차단)
d.o.append(f'<rect x="{CX}" y="{CY}" width="{AX_MAX_X - CX}" height="{AX_MAX_Y - CY}" fill="rgba(245,245,243,0.02)"/>')
d.t(CX + 18, AX_MAX_Y - 14, "정적 차단", 13, SOFT, KR, "start", 600)

# 축 선 그리기 (Cross)
d.line(AX_MIN_X, CY, CX, CY, RULE, 1.2)
d.line(CX, AX_MAX_Y, CX, CY, RULE, 1.2)

# 축 화살표 끝 마커 (수평/수직 정렬 필수)
d.path(f"M {CX} {CY} L {AX_MAX_X} {CY}", INK, 1.2, m="ar")
d.path(f"M {CX} {CY} L {AX_MIN_X} {CY}", SOFT, 1.2, m="ar")
d.path(f"M {CX} {CY} L {CX} {AX_MIN_Y}", INK, 1.2, m="ar")
d.path(f"M {CX} {CY} L {CX} {AX_MAX_Y}", SOFT, 1.2, m="ar")

# 축 끝 라벨 (Jobs-minimal: 한 단어, 화살표 팁 너머)
d.t(AX_MAX_X + 20, CY + 5, "게이트", 13, INK, KR, "start", 600)
d.t(AX_MIN_X - 20, CY + 5, "수동", 13, SOFT, KR, "end", 600)
d.t(CX, AX_MIN_Y - 18, "실측", 13, INK, KR, "middle", 600)
d.t(CX, AX_MAX_Y + 24, "정적", 13, SOFT, KR, "middle", 600)

# 항목 배치 함수 (점 + 라벨)
def item(x, y, name, color=MUTED, r=4.5, dx=10, dy=4, anchor="start", weight=500, fam=MONO, size=11):
    d.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
    d.t(x + dx, y + dy, name, size, color if color == ACC else INK, fam, anchor, weight)

# 1. anthropics/skills (좌상단: 드리프트 검사 없음, 스킬 내 절차형 평가 하네스로 gstack·obra 아래·내 저장소 위)
item(260, 255, "anthropics/skills", MUTED, dx=0, dy=-10, anchor="middle")

# 2. mattpocock/skills (좌하단: check-plugin-version 스크립트만 있고 CI·훅 게이트 없음, 행동 평가 없음)
item(360, 380, "mattpocock/skills", MUTED, dx=0, dy=18, anchor="middle")

# 3. gosuda/dalcom-skills (우하단: pre-commit 자가 시험 게이트, 행동 평가 없음)
item(720, 380, "gosuda/dalcom-skills", MUTED, dx=0, dy=18, anchor="middle")

# 4. obra/superpowers (우측 축선 위: 20KB 상한 게이트, 버전 일치 검사, 인트리 CLI)
item(550, 245, "obra/superpowers", MUTED)

# 5. garrytan/gstack (우상단: CI 바이트 일치 검사, 카빙 섹션 로딩 검증)
item(680, 225, "garrytan/gstack", MUTED)

# 6. trailofbits/skills (우상단: 검사기 자가 시험 게이트, 도구 실행·제안 분리 채점)
item(770, 155, "trailofbits/skills", MUTED, dx=-10, anchor="end")

# 7. EveryInc/compound-engineering-plugin (우상단: CI 매니페스트 차단, 8KB 상한, 로컬 다중 CLI 블라인드 채점)
item(790, 124, "EveryInc/compound-engineering", MUTED, dx=-10, anchor="end")

# 8. 내 저장소 (통합 전) — 수동 드리프트 관리, 기존 발동 평가 기준선
item(290, 272, "내 저장소 (통합 전)", SOFT, r=4.0, dx=-12, dy=4, anchor="end", fam=KR, weight=400, size=13)

# 내 저장소 이동 궤적: 세로 위치는 근거가 없어 같은 높이에 두고 가로(드리프트 게이트)만 움직인다
d.path("M 296 272 L 694 272", SOFT, 1.0, dash="3 3")

# 9. 내 저장소 (통합 뒤) — pre-commit 게이트, 렌더링 일치 검사, 반복 eval 및 근접 오답 평가
item(700, 272, "내 저장소 (통합 뒤)", ACC, r=5.5, dx=12, fam=KR, weight=600, size=13)

# 범례 (Y=512, 바닥 마진 여유 확보)
d.legend(512, [
    ("통합 대상 (내 저장소)", ACC),
    ("비교 대상 저장소", MUTED),
    ("통합 전 위치", SOFT)
])

out_path = Path(__file__).resolve().parent.parent / "01-01.repo-quadrant.svg"
d.save(str(out_path))
print(f"Saved: {out_path}")
