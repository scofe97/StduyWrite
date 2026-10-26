"""훅 설정 파일의 탐색 계층과 적용 우선순위 구조.

# 타입 스펙: type-tree
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "HOOK CONFIG SOURCES · SCOPE HIERARCHY",
    "훅 설정 파일의 탐색 계층과 적용 범위",
    "조직 정책부터 사용자 전역, 프로젝트 공유, 로컬 파일, 컴포넌트 확장까지의 설정 위치",
    lead="훅 설정은 계층별 파일에서 수집되어 병합 실행되며 상위 정책이 하위 제어를 강제합니다"
)

# Y 좌표 슬롯
ys = [104, 184, 264, 344, 424]
root_cy = 264

# 1. 직교 연결선 (type-tree 규약: 노드보다 먼저 그린다)
# 루트 → 버스
d.line(184, root_cy, 220, root_cy, SOFT, 1.0)
# 수직 버스
d.line(220, ys[0] + 26, 220, ys[4] + 26, SOFT, 1.0)

# 버스 → 중간 브랜치 & 중간 브랜치 → 리프
for y in ys:
    cy = y + 26
    d.line(220, cy, 256, cy, SOFT, 1.0)
    d.line(440, cy, 480, cy, SOFT, 1.0)

# 2. 루트 노드 (좌측)
d.box(24, root_cy - 30, 160, 60, PAPER2, RULE, 1.0)
d.t(104, root_cy - 5, "훅 설정 소스", 14, INK, KR, "middle", 600)
d.t(104, root_cy + 16, "hooks configuration", 11, MUTED, MONO, "middle")

# 3. 중간 브랜치 (범위 분류)
branches = [
    ("조직 정책", "엔터프라이즈", False),
    ("사용자 전역", "개인 개발 환경", False),
    ("프로젝트 공유", "팀 협업 저장소", False),
    ("로컬 프로젝트", "개인 작업 공간", False),
    ("컴포넌트 확장", "플러그인·스킬", False),
]

for (title, sub, is_focal), y_top in zip(branches, ys):
    d.box(256, y_top, 184, 52, PAPER2, RULE, 1.0)
    d.t(348, y_top + 22, title, 13, INK, KR, "middle", 600)
    d.t(348, y_top + 40, sub, 12.5, MUTED, KR, "middle")

# 4. 리프 노드 (실제 파일 경로 및 특성)
leaves = [
    ("매니지드 정책", "시스템 관리자 강제 규칙 일괄 배포", False, False),
    ("~/.claude/settings.json", "모든 프로젝트 세션 공통 적용", True, False),
    (".claude/settings.json", "형상 관리 커밋 및 팀원 동기화", True, True),
    (".claude/settings.local.json", "개인 전용 설정 및 git 미커밋 격리", True, False),
    ("hooks/hooks.json", "플러그인 번들 및 SKILL.md 프론트매터", True, False),
]

for (path_txt, desc_txt, is_mono, is_focal), y_top in zip(leaves, ys):
    bx, bw = 480, 448
    if is_focal:
        d.tone(bx, y_top, bw, 52, ACC, 6, "14", 1.4)
        d.t(bx + 18, y_top + 22, path_txt, 12.5, ACC, MONO if is_mono else KR, "start", 600)
        d.t(bx + 18, y_top + 40, desc_txt, 12.5, ACC, KR, "start")
    else:
        d.box(bx, y_top, bw, 52, PAPER2, RULE, 1.0)
        d.t(bx + 18, y_top + 22, path_txt, 12.5, INK, MONO if is_mono else KR, "start", 600)
        d.t(bx + 18, y_top + 40, desc_txt, 12.5, MUTED, KR, "start")

out_path = _HERE.parent / "04-01.hook-config-sources.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
