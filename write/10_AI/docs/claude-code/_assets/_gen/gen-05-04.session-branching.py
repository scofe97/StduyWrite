"""원래 세션에서 포크·브랜치·서브태스크로 갈라질 때 복사 대상과 컨텍스트 분리 구조.

# 타입 스펙: type-tree
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 480
d = D(
    W, H,
    "SESSION MANAGEMENT · BRANCHING TOPOLOGY",
    "세션 복제와 분기 제어 체계",
    "현재 대화 세션에서 하위 에이전트, 독립 백그라운드 세션, 직접 전환 복사본으로 갈라지는 분기 구조",
    lead="명령어에 따라 대화 맥락 상속 범위와 실행 위치 및 결과 회수 여부가 나뉩니다 (/subtask·/fork 는 에이전트 뷰를 켠 경우)"
)

# 1. 연결선 (type-tree 규약: 노드보다 먼저 그린다)
root_x, root_y, root_w, root_h = 24, 224, 168, 64
root_cy = root_y + root_h // 2
bus_x = 224

# 루트 -> 버스
d.line(root_x + root_w, root_cy, bus_x, root_cy, SOFT, 1.0)

# 버스 수직선
ys = [108, 224, 340]
cys = [y + 32 for y in ys]
d.line(bus_x, cys[0], bus_x, cys[2], SOFT, 1.0)

# 버스 -> 브랜치 & 브랜치 -> 리프
for cy in cys:
    d.line(bus_x, cy, 256, cy, SOFT, 1.0)
    d.line(464, cy, 504, cy, SOFT, 1.0)

# 2. 루트 노드 (좌측: 현재 세션 대화)
d.box(root_x, root_y, root_w, root_h, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(root_x + root_w // 2, root_cy - 8, "현재 세션 대화", 13, INK, KR, "middle", 600)
d.t(root_x + root_w // 2, root_cy + 12, "원본 컨텍스트", 11.5, MUTED, KR, "middle")

# 3. 중간 브랜치 (명령어 및 분기 방식)
branches = [
    ("/subtask <작업>", "하위 에이전트 생성", False),
    ("/fork [프롬프트]", "독립 세션 복제", True),
    ("/branch [이름]", "작업 세션 직접 전환", False),
]

for (cmd, role, is_focal), y_top in zip(branches, ys):
    bx, bw = 256, 208
    if is_focal:
        d.tone(bx, y_top, bw, 64, ACC, 6, "14", 1.4)
        d.t(bx + bw // 2, y_top + 26, cmd, 13, ACC, MONO, "middle", 600)
        d.t(bx + bw // 2, y_top + 46, role, 12, INK, KR, "middle")
    else:
        d.box(bx, y_top, bw, 64, fill=PAPER2, stroke=RULE, sw=1.0)
        d.t(bx + bw // 2, y_top + 26, cmd, 13, INK, MONO, "middle", 600)
        d.t(bx + bw // 2, y_top + 46, role, 12, MUTED, KR, "middle")

# 4. 리프 노드 (우측: 상속 범위, 실행 위치, 결과 회수)
leaves = [
    ("대화 맥락 전체 상속 · 백그라운드 실행", "완료 시 메인 대화창에 결과 요약 반환", OK),
    ("현재까지 대화 복사 · 독립 백그라운드", "결과 반환 없음 (완전 독립 병렬 검증)", ACC),
    ("분기 복사본 세션으로 사용자 직접 전환", "원본 대화 보존 (/resume 복귀 가능)", INFO),
]

for (line1, line2, c), y_top in zip(leaves, ys):
    bx, bw = 504, 432
    d.box(bx, y_top, bw, 64, fill=PAPER, stroke=RULE, sw=0.9)
    d.t(bx + 18, y_top + 26, line1, 12.5, INK, KR, "start", 600)
    d.t(bx + 18, y_top + 46, line2, 12, c, KR, "start")

# 5. 범례
d.legend(436, [
    ("독립 백그라운드 분기 (Focal)", ACC),
    ("결과 요약 회수", OK),
    ("직접 전환 분기", INFO),
])

d.save("05-04.session-branching.svg")
