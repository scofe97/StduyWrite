# 사실 출처: 02-02.Memory.md:284-302 · 원문 README.md:509-530
# 타입 스펙: type-tree
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 960, 448
d = D(
    W, H,
    "AUTO MEMORY DIRECTORY · TREE",
    "자동 메모리 디렉터리 구조와 시작·온디맨드 로드",
    "MEMORY.md 시작 진입점 로드와 주제별 토픽 파일의 온디맨드 로드 구조",
    lead="진입점 요약 파일은 세션 시작 시 읽고 토픽 파일은 필요할 때 동적 로드합니다"
)

# 1. 트리 연결선 (노드보다 먼저 그린다)
# Root → 브랜치 버스
d.line(480, 148, 480, 176, RULE, 1.2)
d.line(148, 176, 604, 176, RULE, 1.2)

# 브랜치 A (시작 로드) 드롭
d.line(148, 176, 148, 196, RULE, 1.2)
d.line(148, 228, 148, 264, RULE, 1.2)

# 브랜치 B (온디맨드) 드롭 및 토픽 버스
d.line(604, 176, 604, 196, RULE, 1.2)
d.line(604, 228, 604, 244, RULE, 1.2)
d.line(388, 244, 820, 244, RULE, 1.2)
d.line(388, 244, 388, 264, RULE, 1.2)
d.line(604, 244, 604, 264, RULE, 1.2)
d.line(820, 244, 820, 264, RULE, 1.2)

# 2. 루트 노드
RW, RH = 420, 44
RX = (W - RW) // 2
d.box(RX, 104, RW, RH, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(480, 122, "~/.claude/projects/<project>/memory/", 12, INK, MONO, "middle", 600)
d.t(480, 138, "자동 메모리 루트 디렉터리", 11, MUTED, KR, "middle")

# 3. 2계층 브랜치 헤더
# Branch A: 시작 적재
d.box(48, 196, 200, 32, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(148, 216, "시작 자동 로드", 12, ACC, KR, "middle", 600)

# Branch B: 온디맨드 적재
d.box(296, 196, 616, 32, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(604, 216, "온디맨드 지연 로드 (대화 중 관련 주제 등장 시)", 12, INFO, KR, "middle", 600)

# 4. 3계층 단말 노드 (Leaves)
# Leaf 0: MEMORY.md (Focal)
d.tone(48, 264, 200, 88, ACC, r=6, op="14", sw=1.4)
d.t(148, 284, "MEMORY.md", 13, ACC, MONO, "middle", 600)
d.chip(148, 306, "진입점", ACC, size=11)
d.t(148, 328, "상위 200줄 또는 25KB 로드", 11, INK, KR, "middle")

# Leaf 1: prefers-pnpm.md
d.box(296, 264, 184, 88, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(388, 284, "prefers-pnpm.md", 12, INK, MONO, "middle", 600)
d.chip(388, 306, "feedback", INFO, size=11)
d.t(388, 328, "패키지 도구 선호", 11, MUTED, KR, "middle")
d.t(388, 342, "예시 이름 · 온디맨드 로드", 11, SOFT, KR, "middle")

# Leaf 2: release-checklist.md
d.box(512, 264, 184, 88, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(604, 284, "release-checklist.md", 12, INK, MONO, "middle", 600)
d.chip(604, 306, "project", INFO, size=11)
d.t(604, 328, "릴리스 배포 점검 절차", 11, MUTED, KR, "middle")
d.t(604, 342, "예시 이름 · 온디맨드 로드", 11, SOFT, KR, "middle")

# Leaf 3: team-contacts.md
d.box(728, 264, 184, 88, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(820, 284, "team-contacts.md", 12, INK, MONO, "middle", 600)
d.chip(820, 306, "reference", INFO, size=11)
d.t(820, 328, "담당자 및 외부 참조", 11, MUTED, KR, "middle")
d.t(820, 342, "예시 이름 · 온디맨드 로드", 11, SOFT, KR, "middle")

d.t(604, 376, "프론트매터 있으면 modified 갱신", 11, MUTED, KR, "middle")

# 5. 범례
d.legend(392, [
    ("시작 자동 로드 진입점 (Focal)", ACC),
    ("온디맨드 지연 로드 토픽 파일", INFO),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-02.auto-memory-dir.svg"))
d.save(out)
print(f"saved: {out}")
