"""원본 저장소와 .claude/worktrees 하위 격리 워크트리 디렉터리 구조.

# 타입 스펙: type-tree
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 524
d = D(
    W, H,
    "GIT WORKTREES · DIRECTORY TOPOLOGY",
    "원본 저장소와 격리 워크트리 디렉터리 구조",
    "메인 작업 공간의 변경 충돌을 방지하는 .claude/worktrees 하위 격리 워크트리 및 공유 Git 객체 배치",
    lead="공유 .git 객체를 참조하며 메인 작업 공간과 독립된 디렉터리에서 작업을 병렬 수행합니다"
)

# 1. 연결선 (type-tree 규약: 노드보다 먼저 그린다)
# Root 하향선
d.line(480, 148, 480, 172, RULE, 1.0)
# 1계층 수평 버스 (.git, src, .claude/worktrees)
d.line(148, 172, 720, 172, RULE, 1.0)
# 1계층 드롭선
d.line(148, 172, 148, 196, RULE, 1.0)
d.line(368, 172, 368, 196, RULE, 1.0)
d.line(720, 172, 720, 196, RULE, 1.0)

# .claude/worktrees 하위 드롭선 및 2계층 버스
d.line(720, 256, 720, 284, RULE, 1.0)
d.line(608, 284, 832, 284, RULE, 1.0)
d.line(608, 284, 608, 308, RULE, 1.0)
d.line(832, 284, 832, 308, RULE, 1.0)

# 2. 루트 노드 (원본 Git 저장소)
d.box(350, 100, 260, 48, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(480, 120, "<repo>/", 13, INK, MONO, "middle", 600)
d.t(480, 137, "원본 Git 저장소 루트", 11.5, MUTED, KR, "middle")

# 3. 1계층 노드 (메인 객체 및 작업 공간)
# .git/
d.box(48, 196, 200, 84, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(148, 218, ".git/", 13, INK, MONO, "middle", 600)
d.t(148, 240, "공유 Git 객체 저장소", 12, INK, KR, "middle")
d.t(148, 260, "메타데이터 및 refs 보존", 11.5, MUTED, KR, "middle")

# src/
d.box(268, 196, 200, 84, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(368, 218, "src/", 13, INK, MONO, "middle", 600)
d.t(368, 240, "메인 작업 디렉터리", 12, INK, KR, "middle")
d.t(368, 260, "메인 작업 영향 없음", 11.5, MUTED, KR, "middle")

# .claude/worktrees/ (Focal! Accent!)
d.tone(590, 196, 260, 60, ACC, r=6, op="14", sw=1.4)
d.t(720, 220, ".claude/worktrees/", 13, ACC, MONO, "middle", 600)
d.t(720, 241, "격리 워크트리 루트 디렉터리", 12, INK, KR, "middle")

# 4. 2계층 노드 (.claude/worktrees 하위 격리 폴더)
# feature-auth/
d.box(508, 308, 200, 136, fill=PAPER, stroke=RULE, sw=0.9)
d.t(608, 330, "<워크트리이름>/", 12.5, INK, MONO, "middle", 600)
d.t(608, 350, "기능 개발 격리 공간", 12, INK, KR, "middle")
d.t(608, 372, ".git 포인터 파일", 11.5, MUTED, KR, "middle")
d.t(608, 392, "sparsePaths 부분 체크아웃", 11.5, INFO, KR, "middle")
d.t(608, 414, "이름 없으면 변경 없을 때 삭제", 11.5, OK, KR, "middle")
d.t(608, 432, "이름 붙으면 종료 시 확인", 11.5, MUTED, KR, "middle")

# bg-worker/
d.box(732, 308, 200, 136, fill=PAPER, stroke=RULE, sw=0.9)
d.t(832, 330, "<백그라운드용>/", 12.5, INK, MONO, "middle", 600)
d.t(832, 350, "백그라운드 세션 공간", 12, INK, KR, "middle")
d.t(832, 372, "bgIsolation 전용 격리", 11.5, MUTED, KR, "middle")
d.t(832, 392, "주기 스윕으로 정리", 11.5, OK, KR, "middle")
d.t(832, 414, "(작업 남으면 보존)", 11.5, OK, KR, "middle")

# 5. 범례
d.legend(476, [
    ("격리 워크트리 루트", ACC),
    ("선택적 부분 체크아웃", INFO),
    ("자동 정리 수명주기", OK),
])

d.save("05-04.worktree-dirs.svg")
